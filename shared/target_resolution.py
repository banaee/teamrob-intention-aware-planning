"""
shared/target_resolution.py

PURPOSE:
    One answer to "where is the thing this action targets?", shared by every
    reader of positions in the cognitive layer — the projector (segments) and
    the recognizer (chord target, zone) — so that neither carries its own
    weaker copy of the lookup (I1 audit §4).

    Resolution has two halves, both in shared/:
      1. Grounding — AdaptivePlanner.decompose() turns a task, its bindings and
         the live WorldState into GroundedActions with every Var resolved
         through task bindings, guard-bound vars, derived vars and step
         bindings. Nothing here re-implements that.
      2. Location — this module turns a grounded movement action into a
         position: the action's movement_target_key names the binding, the
         binding names an object, the object is wherever it currently is.

    CURRENT location, deliberately: an agent walking to fetch an object walks
    to where the object is now — a shelf, the table it was delivered to, or
    another agent's hands. The planner's derived var `home_container_of`
    answers a different question ("where does this object belong", a symbolic
    destination for a return) and stays a derived var; the two are not merged.

    A carried object is wherever its holder is. WorldState.object_locations
    maps a carried object to the holder's agent id, which is a key of
    agent_positions and never of object_positions — that is the whole test; no
    predicate name, no parameter name, no object type.

WHAT THIS MODULE DOES NOT DO:
    - Does NOT select methods or resolve variables (shared/planner.py)
    - Does NOT know any domain's parameter or object names
    - Does NOT import from mesa_sim/ or ros_sim/
"""

from typing import Optional, Tuple

from shared.types import GroundedAction, WorldState


def object_position(obj_id: str, world: WorldState) -> Optional[Tuple[float, float]]:
    """
    Where `obj_id` is now, or None if the world does not know it. A carried
    object resolves through its holder's position.
    """
    holder = world.object_locations.get(obj_id)
    if holder is not None and holder in world.agent_positions:
        return world.agent_positions[holder]
    return world.object_positions.get(obj_id)


def movement_target_id(action: GroundedAction) -> Optional[str]:
    """
    The object a movement action heads for — the value bound to the schema's
    movement_target_key — or None for a non-movement action.
    """
    key = action.schema.movement_target_key
    if key is None:
        return None
    return action.bindings.get(key)


def movement_target_position(
    action: GroundedAction, world: WorldState
) -> Optional[Tuple[float, float]]:
    """
    Position of the object `action` heads for, or None when the action is not
    a movement or its target has no known position.
    """
    target_id = movement_target_id(action)
    if target_id is None:
        return None
    return object_position(target_id, world)
