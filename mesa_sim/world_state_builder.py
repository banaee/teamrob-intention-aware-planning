"""
mesa_sim/world_state_builder.py

PURPOSE:
    Translates Mesa ground truth into a symbolic WorldState snapshot.
    This is the boundary between the simulator's physical representation
    and the cognitive layer's symbolic reasoning.

WHAT THIS MODULE DOES:
    - Reads agent positions from Mesa space → derives current zones
    - Reads env_objects and items from model → derives object locations
    - Derives symbolic predicates from the above (e.g. "at", "holding", "item_at")
    - Returns a fresh WorldState each time it is called

WHAT THIS MODULE DOES NOT DO:
    - Does NOT persist state — WorldState is ephemeral, built and discarded each step
    - Does NOT modify any model state — read-only
    - Does NOT know about IR, planning, or replanning logic
    - Does NOT handle ROS — ROS has its own world_state_builder_ros.py

CALLED BY:
    - mesa_sim/agents.py (RobotAgent.step) — once per step before cognitive loop

OUTPUTS:
    - shared.types.WorldState  consumed by shared/replanning.py and shared/planner.py

PREDICATES GENERATED (Predicate objects in WorldState.predicates):
    Spatial:
        Predicate("at", (agent_id, zone_id))
        Predicate("item_at", (item_id, location_id))
    Manipulation:
        Predicate("holding", (agent_id, item_id))
        # TODO: add more as needed by planner

COORDINATE SYSTEM:
    Uses center-origin coordinates from domain1.json directly.
    Zone lookup delegates to model.get_zone_of_position(x, y).
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Set

from shared.types import AgentState, WorldState, Predicate

if TYPE_CHECKING:
    from mesa_sim.sim_model import FactoryModel


def build_world_state(model: FactoryModel) -> WorldState:
    """
    Build a symbolic WorldState snapshot from current Mesa ground truth.

    INPUT:
        model   — FactoryModel instance (read-only)

    OUTPUT:
        WorldState with:
            - agent_states    for all humans and robots
            - object_locations for all items
            - predicates      derived symbolic facts
    """

    timestamp = float(model.schedule.steps)
    agent_states: Dict[str, AgentState] = {}
    object_locations: Dict[str, str] = {}
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
        if zone:
            predicates.add(Predicate("at", (agent_id, zone)))
        if human.carrying:
            predicates.add(Predicate("holding", (agent_id, human.carrying)))

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
        if zone:
            predicates.add(Predicate("at", (agent_id, zone)))
        if robot.carrying:
            predicates.add(Predicate("holding", (agent_id, robot.carrying)))

    # ------------------------------------------------------------------
    # Object locations — items
    # ------------------------------------------------------------------
    for item_id, item in model.items.items():
        if item.held_by:
            # Item is being carried — location is the carrying agent
            location = item.held_by
        elif item.at_location:
            # Item is resting at a shelf or kitting table
            location = item.at_location
        else:
            location = "unknown"

        object_locations[item_id] = location
        predicates.add(Predicate("item_at", (item_id, location)))

    # ------------------------------------------------------------------
    # TODO Phase 4: derive additional predicates
    # Examples:
    #   path_clear — check if any obstacle is between robot and its target
    #   zone_occupied({zone_id}) — another agent is already in this zone
    #   item_delivered({item_id}) — item_at(item_id, kitting_table)
    # ------------------------------------------------------------------

    return WorldState(
        timestamp=timestamp,
        agent_states=agent_states,
        object_locations=object_locations,
        predicates=predicates,
    )
