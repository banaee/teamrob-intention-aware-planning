"""
mesa_sim/world_state_builder.py

PURPOSE:
    Translates Mesa ground truth into a symbolic WorldState snapshot.
    This is the boundary between the simulator's physical representation
    and the cognitive layer's symbolic reasoning.

WHAT THIS MODULE DOES:
    - Reads agent positions from Mesa space → derives the agents' areas (area_fact)
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
    Spatial (area-level — read by method guards):
        Predicate("in_area", (Const(agent_id), Const(area_id)))
        — shared.types.area_fact, the one definition every computed state reads too

    Spatial (object-level — used by executor completion checking):
        Predicate("at", (Const(agent_id), Const(obj_id)))
        — emitted when agent is within PROXIMITY_THRESHOLD of an env object or item

    Manipulation:
        Predicate("holding", (Const(agent_id), Const(item_id)))
        Predicate("obj_at", (Const(item_id), Const(location_id)))

    Process:
        Predicate("waited", (Const(agent_id), Const(obj_id)))
        — emitted while agent.waited_at is set: the executor sets it on the last
          STAND of a wait (nearest fixed object) and clears it on the agent's
          next step/grasp/release/touch. wait_at's completion condition; the
          body runs the timer, so the body says when the wait is over.

    Object states (T-G A5):
        Predicate(<declared state>, (Const(obj_id),)), or with no argument for a
        fact about no object — every fact the environment holds
        (SimModel.state_facts), emitted as held; the builder derives none.

PREDICATE NAMING RATIONALE:
    "in_area" and "at" are intentionally distinct:
    - in_area(agent, area) — coarse spatial context for IR
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

from shared.types import AgentState, WorldState, Workspace, Predicate, Const, area_at, area_fact

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
            - object_areas       for all items
            - object_positions   for all env objects and items, for IR direction-based likelihood
            - predicates         derived symbolic facts
    """

    timestamp = float(model.schedule.steps)
    agent_states: Dict[str, AgentState] = {}
    agent_positions: Dict[str, Tuple[float, float]] = {}
    object_locations: Dict[str, str] = {}
    object_areas: Dict[str, str] = {}
    object_home_container: Dict[str, str] = {}
    object_destination: Dict[str, str] = {}
    object_positions: Dict[str, Tuple[float, float]] = {}
    fixed_object_positions: Dict[str, Tuple[float, float]] = {}
    predicates: Set[Predicate] = set()

    # ------------------------------------------------------------------
    # Agent states — humans
    # ------------------------------------------------------------------
    for agent_id, human in model.humans.items():
        agent_states[agent_id] = AgentState(
            agent_id=agent_id,
            holding=human.carrying,
            current_task=human.current_task,
        )

        # Record agent position 
        agent_positions[agent_id] = (human.pos[0], human.pos[1])

        # Area-level predicate — the one definition (A9, R2)
        fact = area_fact(agent_id, agent_positions[agent_id], model.areas)
        if fact is not None:
            predicates.add(fact)

        # Manipulation predicate
        if human.carrying:
            predicates.add(Predicate("holding", (Const(agent_id), Const(human.carrying))))

        # Process predicate — a completed wait the agent has not yet moved on from
        if human.waited_at:
            predicates.add(Predicate("waited", (Const(agent_id), Const(human.waited_at))))

        # Object-level proximity predicates — for executor completion checking
        _add_proximity_predicates(agent_id, human.pos, model, predicates)

    # ------------------------------------------------------------------
    # Agent states — robots
    # ------------------------------------------------------------------
    for agent_id, robot in model.robots.items():
        agent_states[agent_id] = AgentState(
            agent_id=agent_id,
            holding=robot.carrying,
            current_task=robot.current_task,
        )

        # Record agent position
        agent_positions[agent_id] = (robot.pos[0], robot.pos[1])

        # Area-level predicate — the one definition (A9, R2)
        fact = area_fact(agent_id, agent_positions[agent_id], model.areas)
        if fact is not None:
            predicates.add(fact)

        # Manipulation predicate
        if robot.carrying:
            predicates.add(Predicate("holding", (Const(agent_id), Const(robot.carrying))))

        # Process predicate — a completed wait the agent has not yet moved on from
        if robot.waited_at:
            predicates.add(Predicate("waited", (Const(agent_id), Const(robot.waited_at))))

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
                area_id = _area_id(carrier.pos, model) if carrier else "unknown"
            else:
                location = obj.at_location
                area_id = _area_id(obj.position, model)

            object_locations[obj_id] = location
            predicates.add(Predicate("obj_at", (Const(obj_id), Const(location))))
            object_areas[obj_id] = area_id
            object_home_container[obj_id] = obj.home_container   # obj.home_container itself never mutates after load, 
                                                                 # but the WorldState dict is still refreshed here each call, 
                                                                 # like object_areas/object_locations above
            if obj.destination is not None:
                object_destination[obj_id] = obj.destination   # static like home_container
            object_positions[obj_id] = tuple(obj.position)
        else:
            # Fixed object — direct position/area, no held_by/at_location semantics.
            object_positions[obj_id] = tuple(obj.position)
            fixed_object_positions[obj_id] = tuple(obj.position)   # static, for the fallback projection (T-D P)
            object_areas[obj_id] = _area_id(obj.position, model) or "unknown"

    # ------------------------------------------------------------------
    # The object states the environment holds (T-G A5; A6, assumptions 5.3)
    # ------------------------------------------------------------------
    predicates |= model.state_facts

    # ------------------------------------------------------------------
    # TODO Phase 4: derive additional predicates
    # Examples:
    #   path_clear — check if any obstacle is between robot and its target
    #   in_area_occupied — another agent is already in this area
    #   item_delivered — obj_at(item_id, kitting_table)
    # ------------------------------------------------------------------

    return WorldState(
        timestamp=timestamp,
        agent_states=agent_states,
        agent_positions=agent_positions,
        object_locations=object_locations,
        object_areas=object_areas,
        object_home_container=object_home_container,
        object_destination=object_destination,
        object_positions=object_positions,
        fixed_object_positions=fixed_object_positions,
        # The room's rectangle, static (T-D P): the body's space, built from the layout's width and height.
        workspace=Workspace(x_min=model.space.x_min, x_max=model.space.x_max,
                            y_min=model.space.y_min, y_max=model.space.y_max),
        areas=model.areas,   # the declared areas (A9), static
        predicates=predicates,
    )


# =============================================================================
# Proximity helpers
# =============================================================================

def _area_id(position, model: "SimModel"):
    """The id of the declared area holding `position` (area_at), or None."""
    area = area_at(position, model.areas)
    return area.id if area is not None else None


def within_proximity(agent_pos: Tuple[float, float], obj_pos: Tuple[float, float]) -> bool:
    """True when an agent at `agent_pos` is "at" an object at `obj_pos`: within
    PROXIMITY_THRESHOLD. The one test, read by `at` and by the walk's stop
    (action_decomposer.walk_positions)."""
    ax, ay = agent_pos
    ox, oy = obj_pos
    return math.sqrt((ax - ox) ** 2 + (ay - oy) ** 2) <= PROXIMITY_THRESHOLD


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
    for obj_id, obj in model.objects.items():
        if obj.type == "obstacle" or obj.held_by:
            continue
        if within_proximity(agent_pos, obj.position):
            predicates.add(Predicate("at", (Const(agent_id), Const(obj_id))))
            
    # TODO: flagged rather than fixed — obj.type == "obstacle". Same shape of hardcoding as "?item" was, technically. 
    # I'm treating it differently because "obstacle" reads as a physics/rendering category every domain would plausibly share 
    # (something that blocks movement but is never a task target), not a domain-semantic label like "item"/"pallet." 
    # But that's a judgment call, not a fact — if you want full rigor, 
    # this could instead be "skip objects with no plausible task relevance," derived from 
    # whether any TaskSchema.parameter_types value ever equals this object's type 
    # (i.e., "is this type ever a valid task target anywhere in the domain"). 
    # That's a bigger, cross-cutting mechanism though