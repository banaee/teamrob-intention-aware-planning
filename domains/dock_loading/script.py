"""
The dock_loading call forms (kitting's form, domains/kitting/script.py): the
authored surface of a scenario, one function per task schema of the
dock_loading tree, each returning a TaskInstance of that schema. The variables
are read from the schema's declared parameters, never retyped. A determined
parameter (a pallet's bay or truck) is bound only when the author states it;
omitted, the planner resolves it from the pallet's designation.

    from domains.dock_loading.script import confirm_delivered_pallet, go_to
    Script([confirm_delivered_pallet("pallet_0")], closing=[go_to("desk")])

dock_loading's, not the world's: the functions name this domain's schemas and
its words. The script types and the event sugar (Script, RepeatableEntry, .at,
.during, drop) are generic, in shared/types.py.
"""

from typing import Optional

from shared.types import Const, TaskInstance
from domains.dock_loading import tasks

__all__ = ["deliver_pallet", "load_return", "confirm_delivered_pallet", "coffee_break", "office_break",
           "go_to", "stand", "go_to_and_stand"]


def deliver_pallet(pallet: str, bay: Optional[str] = None) -> TaskInstance:
    """A delivery of `pallet`; `bay` binds its destination, omitted: the pallet's designation."""
    pallet_var, bay_var = tasks.deliver_pallet.parameters
    bindings = {pallet_var: Const(pallet)}
    if bay is not None:
        bindings[bay_var] = Const(bay)
    return TaskInstance(schema=tasks.deliver_pallet, bindings=bindings)


def load_return(pallet: str, truck: Optional[str] = None) -> TaskInstance:
    """The return of the empty `pallet`; `truck` binds its destination, omitted: the pallet's designation."""
    pallet_var, truck_var = tasks.load_return.parameters
    bindings = {pallet_var: Const(pallet)}
    if truck is not None:
        bindings[truck_var] = Const(truck)
    return TaskInstance(schema=tasks.load_return, bindings=bindings)


def confirm_delivered_pallet(pallet: str, bay: Optional[str] = None) -> TaskInstance:
    """The scan of `pallet` in its bay; `bay` binds the bay, omitted: the pallet's designation."""
    pallet_var, bay_var = tasks.confirm_delivered_pallet.parameters
    bindings = {pallet_var: Const(pallet)}
    if bay is not None:
        bindings[bay_var] = Const(bay)
    return TaskInstance(schema=tasks.confirm_delivered_pallet, bindings=bindings)


def coffee_break(machine: str) -> TaskInstance:
    machine_var, = tasks.coffee_break.parameters
    return TaskInstance(schema=tasks.coffee_break, bindings={machine_var: Const(machine)})


def office_break(chair: str) -> TaskInstance:
    chair_var, = tasks.office_break.parameters
    return TaskInstance(schema=tasks.office_break, bindings={chair_var: Const(chair)})


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
