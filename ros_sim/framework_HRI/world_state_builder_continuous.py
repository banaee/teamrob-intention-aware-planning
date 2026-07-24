"""
continuous_sim/world_state_builder_continuous.py

PURPOSE:
    Translates ContinuousWorld ground truth into a symbolic WorldState snapshot.
    This is the boundary between the continuous physics world and the cognitive layer.

    Direct equivalent of mesa_sim/world_state_builder.py — same predicates,
    same structure, different data source (ContinuousWorld instead of FactoryModel).

WHAT THIS MODULE DOES:
    - Reads robot and human positions from ContinuousWorld → derives zones
    - Reads item states → derives object locations
    - Emits symbolic predicates from the above
    - Returns a fresh WorldState each call (stateless — no caching)

WHAT THIS MODULE DOES NOT DO:
    - Does NOT modify world state — read-only
    - Does NOT call the cognitive layer
    - Does NOT know about PRIEST, ROS, or planning

PREDICATES GENERATED:
    in_zone(agent_id, zone_id)      — coarse spatial context, used by IR
    at(agent_id, obj_id)            — fine proximity, used by executor completion
    holding(agent_id, item_id)      — manipulation state
    obj_at(item_id, location_id)    — item location

PROXIMITY_THRESHOLD:
    Same semantics as mesa_sim/world_state_builder.py.
    Mesa used 30.0 world-units (Mesa units ~ cm).
    Here everything is in metres, so threshold is 0.4 m — same as
    the PRIEST goal-reached check (local_planner line 145: dist < 0.4**2).

CALLED BY:
    continuous_sim/run_continuous.py  (once per cognitive cycle)

OUTPUTS:
    shared.types.WorldState  consumed by shared/replanning.py and shared/planner.py
"""

from __future__ import annotations

from typing import Dict, Set

import numpy as np

from shared.types import AgentState, WorldState, Predicate, Const
from continuous_sim.world import ContinuousWorld


# Proximity threshold in metres.
# Agent must be within this distance of an object to emit at(agent, object).
# Matches the PRIEST goal-reached threshold (0.4 m).
PROXIMITY_THRESHOLD = 0.4   # metres


def build_world_state(world: ContinuousWorld, sim_time: float) -> WorldState:
    """
    Build a symbolic WorldState from the current ContinuousWorld state.

    Parameters
    ----------
    world    : ContinuousWorld — read-only
    sim_time : current simulation time in seconds (world.sim_time)

    Returns
    -------
    WorldState with agent_states, object_locations, object_zones, predicates.
    """

    agent_states:     Dict[str, AgentState] = {}
    object_locations: Dict[str, str]        = {}
    object_zones:     Dict[str, str]        = {}
    predicates:       Set[Predicate]        = set()

    # ------------------------------------------------------------------
    # Robot
    # ------------------------------------------------------------------
    robot_zone = world.get_zone_of_position(world.robot.x, world.robot.y)

    agent_states[world.robot_id] = AgentState(
        agent_id=world.robot_id,
        current_zone=robot_zone or "unknown",
        holding=world.robot_holding,
        current_task=None,   # filled in by run_continuous from task_planner
    )

    if robot_zone:
        predicates.add(Predicate("in_zone", (Const(world.robot_id), Const(robot_zone))))

    if world.robot_holding:
        predicates.add(Predicate("holding", (Const(world.robot_id), Const(world.robot_holding))))

    _add_proximity_predicates(
        agent_id=world.robot_id,
        ax=world.robot.x,
        ay=world.robot.y,
        world=world,
        predicates=predicates,
    )

    # ------------------------------------------------------------------
    # Human
    # ------------------------------------------------------------------
    human_zone = world.get_zone_of_position(world.human.x, world.human.y)

    agent_states[world.human.agent_id] = AgentState(
        agent_id=world.human.agent_id,
        current_zone=human_zone or "unknown",
        holding=None,       # scripted human does not pick items (yet)
        current_task=None,
    )

    if human_zone:
        predicates.add(Predicate("in_zone", (Const(world.human.agent_id), Const(human_zone))))

    _add_proximity_predicates(
        agent_id=world.human.agent_id,
        ax=world.human.x,
        ay=world.human.y,
        world=world,
        predicates=predicates,
    )

    # ------------------------------------------------------------------
    # Items
    # ------------------------------------------------------------------
    for item_id, item in world.items.items():

        if item.held_by:
            location = item.held_by
            # Item zone follows its carrier
            if item.held_by == world.robot_id:
                zone = robot_zone or "unknown"
            elif item.held_by == world.human.agent_id:
                zone = human_zone or "unknown"
            else:
                zone = "unknown"
        else:
            location = item.location_id
            zone = world.get_zone_of_position(item.x, item.y) or "unknown"

        object_locations[item_id] = location
        object_zones[item_id]     = zone
        predicates.add(Predicate("obj_at", (Const(item_id), Const(location))))

    return WorldState(
        timestamp=sim_time,
        agent_states=agent_states,
        object_locations=object_locations,
        object_zones=object_zones,
        predicates=predicates,
    )


# =============================================================================
# Proximity helper — mirrors mesa_sim/world_state_builder._add_proximity_predicates
# =============================================================================

def _add_proximity_predicates(
    agent_id: str,
    ax: float,
    ay: float,
    world: ContinuousWorld,
    predicates: Set[Predicate],
) -> None:
    """
    Emit at(agent, object) for every shelf and uncarried item within
    PROXIMITY_THRESHOLD metres of (ax, ay).
    """
    # Shelves and named locations
    for shelf_id, (sx, sy) in world.shelves.items():
        dx = ax - sx
        dy = ay - sy
        if float(np.sqrt(dx * dx + dy * dy)) <= PROXIMITY_THRESHOLD:
            predicates.add(Predicate("at", (Const(agent_id), Const(shelf_id))))

    # Uncarried items
    for item_id, item in world.items.items():
        if item.held_by is not None:
            continue
        dx = ax - item.x
        dy = ay - item.y
        if float(np.sqrt(dx * dx + dy * dy)) <= PROXIMITY_THRESHOLD:
            predicates.add(Predicate("at", (Const(agent_id), Const(item_id))))
