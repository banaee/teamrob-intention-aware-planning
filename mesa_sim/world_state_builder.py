"""
mesa_sim/world_state_builder.py

PURPOSE:
    Translates Mesa ground truth into a symbolic WorldState snapshot.
    This is the boundary between the simulator's physical representation
    and the cognitive layer's symbolic reasoning.

WHAT THIS MODULE DOES:
    - Reads agent positions from Mesa space → derives current zones
    - Reads env_objects () from model → derives object locations
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
import logging
from typing import TYPE_CHECKING, Dict, Set, Tuple
import math

from shared.types import AgentState, WorldState, Predicate, Const

if TYPE_CHECKING:
    from mesa_sim.sim_model import SimModel


# Distance threshold for object-level "at" predicate
# Agent must be within this many world units of an object to be considered "at" it
PROXIMITY_THRESHOLD = 30.0  # TODO Phase 4: read from mesa_configs.yaml


def build_world_state(model: SimModel) -> WorldState:
    """
    Build a symbolic WorldState snapshot from current Mesa ground truth.

    INPUT:
        model   — SimModel instance (read-only)

    OUTPUT:
        WorldState with:
            - agent_states       for all humans and robots
            - agent_positions    for all humans and robots, for IR direction-based likelihood
            - object_locations   for all items
            - object_zones       for all items
            - object_positions   for all env objects and items, for IR direction-based likelihood
            - predicates         derived symbolic facts
    """

    timestamp = float(model.schedule.steps)
    agent_states: Dict[str, AgentState] = {}
    agent_positions: Dict[str, Tuple[float, float]] = {}
    object_locations: Dict[str, str] = {}
    object_zones: Dict[str, str] = {}
    object_home_container: Dict[str, str] = {}
    object_positions: Dict[str, Tuple[float, float]] = {}
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

        # Record agent position 
        agent_positions[agent_id] = (human.pos[0], human.pos[1])

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

        # Record agent position
        agent_positions[agent_id] = (robot.pos[0], robot.pos[1])

        # Zone-level predicate — for IR context reasoning
        if zone:
            predicates.add(Predicate("in_zone", (Const(agent_id), Const(zone))))

        # Manipulation predicate
        if robot.carrying:
            predicates.add(Predicate("holding", (Const(agent_id), Const(robot.carrying))))

        # Object-level proximity predicates — for executor completion checking
        _add_proximity_predicates(agent_id, robot.pos, model, predicates)

    # ------------------------------------------------------------------
    # # Environment Object positions — for IR direction-based likelihood, items are already included above
    # # one pass over model.objects (before: two loops items and objects)
    # # ------------------------------------------------------------------
  
    for obj_id, obj in model.objects.items():
        if obj.is_portable:
            if obj.held_by:
                location = obj.held_by
                carrier = model.humans.get(obj.held_by) or model.robots.get(obj.held_by)
                zone = model.get_zone_of_position(
                    carrier.pos[0], carrier.pos[1]
                ) if carrier else "unknown"
            else:
                location = obj.at_location
                zone = model.get_zone_of_position(obj.position[0], obj.position[1])

            if obj.is_scanned:
                predicates.add(Predicate("scanned", (Const(obj_id),)))

            object_locations[obj_id] = location
            predicates.add(Predicate("obj_at", (Const(obj_id), Const(location))))
            object_zones[obj_id] = zone
            object_home_container[obj_id] = obj.home_container   # obj.home_container itself never mutates after load, 
                                                                 # but the WorldState dict is still refreshed here each call, 
                                                                 # like object_zones/object_locations above
            object_positions[obj_id] = tuple(obj.position)
        else:
            # Fixed object — direct position/zone, no held_by/at_location semantics.
            object_positions[obj_id] = tuple(obj.position)
            object_zones[obj_id] = model.get_zone_of_position(obj.position[0], obj.position[1]) or "unknown"

    # ------------------------------------------------------------------
    # Phase 2.1: dock gate always open — TODO: derive from gate state
    # ------------------------------------------------------------------
    # predicates.add(Predicate("gate_is_open", (Const("dock_gate"),)))
    for obj_id, obj in model.objects.items():
            if obj.type == "gate" and obj.is_open is not False:
                predicates.add(Predicate("gate_is_open", (Const(obj_id),)))
        
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
        agent_positions=agent_positions,
        object_locations=object_locations,
        object_zones=object_zones,
        object_home_container=object_home_container,
        object_positions=object_positions,
        predicates=predicates,
    )


# =============================================================================
# Proximity helpers
# =============================================================================

def _add_proximity_predicates(
    agent_id: str,
    agent_pos: tuple,
    model: "SimModel",
    predicates: Set[Predicate],
) -> None:
    """
    Emit at(agent, object) for all objects within PROXIMITY_THRESHOLD.
    Skips obstacles (not task-relevant targets) and currently-held objects
    (they travel with the agent, not proximity-checkable at a fixed point).
    """
    ax, ay = agent_pos

    for obj_id, obj in model.objects.items():
        if obj.type == "obstacle" or obj.held_by:
            continue
        ox, oy = obj.position
        dist = math.sqrt((ax - ox) ** 2 + (ay - oy) ** 2)
        if dist <= PROXIMITY_THRESHOLD:
            predicates.add(Predicate("at", (Const(agent_id), Const(obj_id))))
            
    # TODO: flagged rather than fixed — obj.type == "obstacle". Same shape of hardcoding as "?item" was, technically. 
    # I'm treating it differently because "obstacle" reads as a physics/rendering category every domain would plausibly share 
    # (something that blocks movement but is never a task target), not a domain-semantic label like "item"/"pallet." 
    # But that's a judgment call, not a fact — if you want full rigor, 
    # this could instead be "skip objects with no plausible task relevance," derived from 
    # whether any TaskSchema.parameter_types value ever equals this object's type 
    # (i.e., "is this type ever a valid task target anywhere in the domain"). 
    # That's a bigger, cross-cutting mechanism though