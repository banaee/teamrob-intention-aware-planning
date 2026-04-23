"""
mesa_sim/world_state_builder.py

PURPOSE:
    Translates Mesa ground truth into a symbolic WorldState snapshot.
    This is the boundary between the simulator's physical representation
    and the cognitive layer's symbolic reasoning.

WHAT THIS MODULE DOES:
    - Reads agent positions from Mesa space → derives current zones
    - Reads env_objects and items from model → derives object locations
    - Derives symbolic predicates from the above
    - Returns a fresh WorldState each time it is called

WHAT THIS MODULE DOES NOT DO:
    - Does NOT persist state — WorldState is ephemeral, built and discarded each step
    - Does NOT modify any model state — read-only
    - Does NOT know about IR, planning, or replanning logic
    - Does NOT handle ROS — ROS has its own world_state_builder_ros.py

CALLED BY:
    - mesa_sim/sim_agents.py (RobotAgent.step, HumanAgent.step)

OUTPUTS:
    - shared.types.WorldState  consumed by shared/replanning.py and shared/planner.py

PREDICATES GENERATED:
    Spatial (zone-level — used by IR context reasoning):
        Predicate("in_zone", (Const(agent_id), Const(zone_id)))

    Spatial (object-level — used by executor completion checking):
        Predicate("at", (Const(agent_id), Const(obj_id)))
        — emitted when agent is within PROXIMITY_THRESHOLD of an env object or item

    Manipulation:
        Predicate("holding", (Const(agent_id), Const(item_id)))
        Predicate("obj_at", (Const(item_id), Const(location_id)))

PREDICATE NAMING RATIONALE:
    "in_zone" and "at" are intentionally distinct:
    - in_zone(agent, zone) — coarse spatial context for IR
    - at(agent, object)    — fine-grained proximity for execution completion
    Conflating them under a single "at" predicate caused a semantic mismatch
    where move_to completion was never satisfied. Kept separate.

PROXIMITY_THRESHOLD:
    Distance in world units within which an agent is considered "at" an object.
    Currently hardcoded — TODO Phase 4: read from mesa_configs.yaml.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Set
import math

from shared.types import AgentState, WorldState, Predicate, Const

if TYPE_CHECKING:
    from mesa_sim.sim_model import FactoryModel


# Distance threshold for object-level "at" predicate
# Agent must be within this many world units of an object to be considered "at" it
PROXIMITY_THRESHOLD = 30.0  # TODO Phase 4: read from mesa_configs.yaml


def build_world_state(model: FactoryModel) -> WorldState:
    """
    Build a symbolic WorldState snapshot from current Mesa ground truth.

    INPUT:
        model   — FactoryModel instance (read-only)

    OUTPUT:
        WorldState with:
            - agent_states       for all humans and robots
            - object_locations   for all items
            - object_zones       for all items
            - predicates         derived symbolic facts
    """

    timestamp = float(model.schedule.steps)
    agent_states: Dict[str, AgentState] = {}
    object_locations: Dict[str, str] = {}
    object_zones: Dict[str, str] = {}
    predicates: Set[Predicate] = set()

    # ------------------------------------------------------------------
    # Agent states — humans
    # ------------------------------------------------------------------
    for agent_id, human in model.humans.items():
        zone = model.get_zone_of_position(human.pos[0], human.pos[1])
        agent_states[agent_id] = AgentState(
            agent_id=agent_id,
            current_zone=zone or "unknown",
            holding=human.carrying,
            current_task=human.current_task,
        )

        # Zone-level predicate — for IR context reasoning
        if zone:
            predicates.add(Predicate("in_zone", (Const(agent_id), Const(zone))))

        # Manipulation predicate
        if human.carrying:
            predicates.add(Predicate("holding", (Const(agent_id), Const(human.carrying))))

        # Object-level proximity predicates — for executor completion checking
        _add_proximity_predicates(agent_id, human.pos, model, predicates)

    # ------------------------------------------------------------------
    # Agent states — robots
    # ------------------------------------------------------------------
    for agent_id, robot in model.robots.items():
        zone = model.get_zone_of_position(robot.pos[0], robot.pos[1])
        agent_states[agent_id] = AgentState(
            agent_id=agent_id,
            current_zone=zone or "unknown",
            holding=robot.carrying,
            current_task=robot.current_task,
        )

        # Zone-level predicate — for IR context reasoning
        if zone:
            predicates.add(Predicate("in_zone", (Const(agent_id), Const(zone))))

        # Manipulation predicate
        if robot.carrying:
            predicates.add(Predicate("holding", (Const(agent_id), Const(robot.carrying))))

        # Object-level proximity predicates — for executor completion checking
        _add_proximity_predicates(agent_id, robot.pos, model, predicates)

    # ------------------------------------------------------------------
    # Object locations — items
    # ------------------------------------------------------------------
    for obj_id, obj in model.get_movable_objects().items():
        if obj.held_by:
            location = obj.held_by
            carrier = model.humans.get(obj.held_by) or model.robots.get(obj.held_by)
            zone = model.get_zone_of_position(
                carrier.pos[0], carrier.pos[1]
            ) if carrier else "unknown"
        elif obj.at_location:
            location = obj.at_location
            zone = model.get_zone_of_position(obj.position[0], obj.position[1])
        else:
            location = "unknown"
            zone = "unknown"

        object_locations[obj_id] = location
        object_zones[obj_id] = zone
        predicates.add(Predicate("obj_at", (Const(obj_id), Const(location))))
        if obj.is_scanned:
            predicates.add(Predicate("scanned", (Const(obj_id),)))

    # Phase 2.1: dock gate always open — TODO: derive from gate state
    predicates.add(Predicate("gate_is_open", (Const("dock_gate"),)))


    # ------------------------------------------------------------------
    # TODO Phase 4: derive additional predicates
    # Examples:
    #   path_clear — check if any obstacle is between robot and its target
    #   in_zone_occupied — another agent is already in this zone
    #   item_delivered — obj_at(item_id, kitting_table)
    # ------------------------------------------------------------------

    return WorldState(
        timestamp=timestamp,
        agent_states=agent_states,
        object_locations=object_locations,
        object_zones=object_zones,
        predicates=predicates,
    )


# =============================================================================
# Proximity helpers
# =============================================================================

def _add_proximity_predicates(
    agent_id: str,
    agent_pos: tuple,
    model: "FactoryModel",
    predicates: Set[Predicate],
) -> None:
    """
    Emit at(agent, object) predicates for all env objects and items
    within PROXIMITY_THRESHOLD of the agent.

    These are consumed by executor._is_action_complete() to check
    move_to completion: at(agent, target_object) in world.predicates.

    ENV OBJECTS: shelves, kitting_table, coffee_machine, ac_switch
    ITEMS: only if not currently held (held items travel with agent)
    """
    ax, ay = agent_pos

    # Check env objects (shelves, kitting_table, coffee_machine, ac_switch, etc.)
    for obj_id, obj in model.env_objects.items():
        if obj.obj_type == "obstacle":
            continue
        ox, oy = obj.position
        dist = math.sqrt((ax - ox) ** 2 + (ay - oy) ** 2)
        if dist <= PROXIMITY_THRESHOLD:
            predicates.add(Predicate("at", (Const(agent_id), Const(obj_id))))

    # Check items — only uncarried items have a fixed position
    for item_id, item in model.items.items():
        if item.held_by:
            continue
        ix, iy = item.position
        dist = math.sqrt((ax - ix) ** 2 + (ay - iy) ** 2)
        if dist <= PROXIMITY_THRESHOLD:
            predicates.add(Predicate("at", (Const(agent_id), Const(item_id))))