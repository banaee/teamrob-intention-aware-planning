# domains/kitting/script.py
"""
The kitting call forms (T-H3): the authored surface of a scenario, one function
per task schema of the kitting tree, each returning a TaskInstance of that
schema. The variables are read from the schema's declared parameters, never
retyped. A determined parameter (deliver_item's table) is bound only when the
author states it; omitted, the planner resolves it from the station.

    from domains.kitting.script import deliver_item, coffee_break, ac_activation, go_to, stand, go_to_and_stand
    Script([deliver_item("item_3").at(pick_up, coffee_break("coffee_machine_0")), go_to("door")])

Kitting's, not the world's: the functions name kitting's schemas and its words
(`table=`), and world/ holds no use case. The script types and the event sugar
(Script, .at, .during, drop) are generic, in shared/types.py.
"""

from typing import Optional

from shared.types import Const, TaskInstance
from domains.kitting import tasks

__all__ = ["deliver_item", "coffee_break", "ac_activation", "go_to", "stand", "go_to_and_stand"]


def deliver_item(item: str, table: Optional[str] = None) -> TaskInstance:
    """A delivery of `item`; `table` binds its destination (a binding-level
    deviation when it is not the station's), omitted: the station's."""
    item_var, table_var = tasks.deliver_item.parameters
    bindings = {item_var: Const(item)}
    if table is not None:
        bindings[table_var] = Const(table)
    return TaskInstance(schema=tasks.deliver_item, bindings=bindings)


def coffee_break(machine: str) -> TaskInstance:
    machine_var, = tasks.coffee_break.parameters
    return TaskInstance(schema=tasks.coffee_break, bindings={machine_var: Const(machine)})


def ac_activation(switch: str) -> TaskInstance:
    switch_var, = tasks.ac_activation.parameters
    return TaskInstance(schema=tasks.ac_activation, bindings={switch_var: Const(switch)})


def go_to(landmark: str) -> TaskInstance:
    landmark_var, = tasks.go_to.parameters
    return TaskInstance(schema=tasks.go_to, bindings={landmark_var: Const(landmark)})


def stand(duration: str) -> TaskInstance:
    """Standing still for `duration` (ISO-8601, the body converts it)."""
    duration_var, = tasks.stand_task.parameters
    return TaskInstance(schema=tasks.stand_task, bindings={duration_var: Const(duration)})


def go_to_and_stand(landmark: str, duration: str) -> TaskInstance:
    """Walking to `landmark` and standing there for `duration`."""
    landmark_var, duration_var = tasks.go_to_and_stand.parameters
    return TaskInstance(schema=tasks.go_to_and_stand,
                        bindings={landmark_var: Const(landmark), duration_var: Const(duration)})
