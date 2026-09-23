# domains/kitting/script.py
"""
The kitting author primitives of the human action script (T-C1, built in T-C2a):
MoveTo, PickUp, Place, each a ScriptAction of the kitting action schema of the
same meaning, and Stay (domain-generic, grounds to nothing). Names and variables
are read from the action schemas, never retyped. The vocabulary (interrupt,
deviate, abandon) and the list helpers are domain-generic, in domains/script.py.

    from domains.kitting.script import MoveTo, PickUp, Place, Stay, interrupt, deviate, abandon
"""

from typing import Tuple, Union

from shared.types import ScriptAction, Stay
from domains.kitting.actions import move_to, pick_up, place
from domains.script import interrupt, deviate, abandon, insert_after, insert_before, retarget, truncate

__all__ = ["MoveTo", "PickUp", "Place", "Stay",
           "interrupt", "deviate", "abandon", "insert_after", "insert_before", "retarget", "truncate"]


def MoveTo(target: Union[str, Tuple[float, float]]) -> ScriptAction:
    """Walk to an item, a table, a landmark; a coordinate pair is admitted by the
    form (for Phase 7's exporter), never written by an author."""
    return ScriptAction.of(move_to.name, {move_to.movement_target_key: target})


def PickUp(item: str) -> ScriptAction:
    return ScriptAction.of(pick_up.name, {pick_up.moved_object_key: item})


def Place(item: str, table: str) -> ScriptAction:
    return ScriptAction.of(place.name, {place.moved_object_key: item, place.moved_to_key: table})
