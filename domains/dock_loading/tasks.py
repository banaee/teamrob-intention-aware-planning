"""
Task schema definitions for the dock_loading domain: the tree of task schemas (T-H).
These are the HTN compound tasks — decomposed into action schema sequences.
Each is a WorkTask (may be assigned), a PersonalTask (never assigned) or a
HumanOnlyTask (never given to a robot); a method's steps hold the action schema
objects they call. The forms are kitting's (domains/kitting/tasks.py).

TASKS:
    WorkTasks:
        deliver_pallet(?pallet, ?delivery_bay)       — the robot's: a pallet from the truck to its delivery bay
        load_return(?pallet, ?truck)                 — the robot's: an empty pallet back into the truck
        confirm_delivered_pallet(?pallet, ?delivery_bay) — the human's: scan a pallet standing in its delivery bay
    PersonalTasks (foreseeable):
        coffee_break(?coffee_machine)                — walk to the coffee machine and wait
        office_break(?office_chair)                  — walk through the office door to the chair and wait
    HumanOnlyTasks:
        go_to(?landmark), stand(?duration), go_to_and_stand(?landmark, ?duration)

METHODS (T-G stage 1; docs/handoffs/plan_T-G_stage1.md, section 4; design_records.md, "T-G: the second domain's
rulings", B8 and B11 as amended):
    A task has a method for every area its agent can be in, selected by in_area(?agent, <area>): the robot on the truck
    side and in the hall, the human in the hall and in the office. No method is written for another area: an agent
    there is a defect, and the absence of a method is the check.
    Passing the gate is a plain step, move_to(dock_gate), in the methods whose route crosses it; those methods require
    is_open(dock_gate). The office door is a plain point on the way, move_to(office_door), with no state (stage 1).
    The robot's held-object rule (B8): a method per held-object case, in this order: the task's own pallet held;
    another empty pallet held; another full pallet held (after the empty case, so it applies to a full one); nothing
    held. Another held pallet is returned to its origin first (home_container_of: the setup's initial container,
    stage 1), and the route continues from the area it is then in. Method names: <task>_<case>_<area>.
    A pallet's destination is its designation (destination_of): deliver_pallet's bay, load_return's truck,
    confirm_delivered_pallet's bay; a binding written in the task instance is kept.
    The area ids, dock_gate and office_door are named here, as this domain's convention.
"""

from shared.types import (Var, Const, ConditionSchema, ActionStep, MethodSchema,
                          WorkTask, PersonalTask, HumanOnlyTask, LANDMARK_TYPE, AREA_FACT)
from domains.dock_loading.actions import move_to, pick_up, place, wait_at, scan_it, stand

_pallet = Var("?pallet")
_delivery_bay = Var("?delivery_bay")
_truck = Var("?truck")
_coffee_machine = Var("?coffee_machine")
_office_chair = Var("?office_chair")
_other = Var("?other")              # another pallet the agent may be holding when the task starts
_other_home = Var("?other_home")    # that pallet's origin
_agent = Var("?agent")
_landmark = Var("?landmark")
_duration = Var("?duration")

# target and entity are used in move_to and wait_at actions, respectively;
# item is the parameter of pick_up, place and scan_it.
_target = Var("?target")
_entity = Var("?entity")
_item = Var("?item")

TRUCK_SIDE = Const("area_truck_side")
HALL = Const("area_hall")
OFFICE = Const("area_office")
GATE = Const("dock_gate")
OFFICE_DOOR = Const("office_door")


# The steps the methods are written in; each call returns a new step.
def _go(target):
    return ActionStep(move_to, {_target: target})


def _pick(item):
    return ActionStep(pick_up, {_item: item})


def _put(item, target):
    return ActionStep(place, {_item: item, _target: target})


# The guards.
def _in(area):
    return ConditionSchema(AREA_FACT, (_agent, area))


def _gate_open():
    return ConditionSchema("is_open", (GATE,))


def _holds(item):
    return ConditionSchema("holding", (_agent, item))


def _another_held():
    """Another pallet held: binds ?other."""
    return [ConditionSchema("holding", (_agent, _other)), ConditionSchema("not_equal", (_other, _pallet))]


def _empty(item):
    return ConditionSchema("is_empty", (item,))


_return_other = {"?other_home": ("home_container_of", "?other")}


# =============================================================================
# WorkTask, the robot's: DELIVER_PALLET
# =============================================================================

# No condition on the pallet being full (answer 1): an assigned delivery of an
# empty pallet is refused at load, its destination being the truck.
deliver_pallet = WorkTask(
    name="deliver_pallet",
    parameters=[_pallet, _delivery_bay],
    parameter_types={"?pallet": "pallet", "?delivery_bay": "delivery_bay"},
    determined_parameters={"?delivery_bay": ("destination_of", "?pallet")},
    methods=[
        MethodSchema(
            name="deliver_pallet_held_truck_side",
            parameters=[_pallet, _delivery_bay],
            guards=[_in(TRUCK_SIDE), _holds(_pallet), _gate_open()],
            steps=[_go(GATE), _go(_delivery_bay), _put(_pallet, _delivery_bay)],
        ),
        MethodSchema(
            name="deliver_pallet_held_hall",
            parameters=[_pallet, _delivery_bay],
            guards=[_in(HALL), _holds(_pallet)],
            steps=[_go(_delivery_bay), _put(_pallet, _delivery_bay)],
        ),
        MethodSchema(
            name="deliver_pallet_return_empty_truck_side",
            parameters=[_pallet, _delivery_bay],
            guards=[_in(TRUCK_SIDE), *_another_held(), _empty(_other), _gate_open()],
            derived_vars=_return_other,
            steps=[_go(GATE), _go(_other_home), _put(_other, _other_home),
                   _go(GATE), _go(_pallet), _pick(_pallet),
                   _go(GATE), _go(_delivery_bay), _put(_pallet, _delivery_bay)],
        ),
        MethodSchema(
            name="deliver_pallet_return_empty_hall",
            parameters=[_pallet, _delivery_bay],
            guards=[_in(HALL), *_another_held(), _empty(_other), _gate_open()],
            derived_vars=_return_other,
            steps=[_go(_other_home), _put(_other, _other_home),
                   _go(GATE), _go(_pallet), _pick(_pallet),
                   _go(GATE), _go(_delivery_bay), _put(_pallet, _delivery_bay)],
        ),
        MethodSchema(
            name="deliver_pallet_return_full_truck_side",
            parameters=[_pallet, _delivery_bay],
            guards=[_in(TRUCK_SIDE), *_another_held(), _gate_open()],
            derived_vars=_return_other,
            steps=[_go(_other_home), _put(_other, _other_home),
                   _go(_pallet), _pick(_pallet),
                   _go(GATE), _go(_delivery_bay), _put(_pallet, _delivery_bay)],
        ),
        MethodSchema(
            name="deliver_pallet_return_full_hall",
            parameters=[_pallet, _delivery_bay],
            guards=[_in(HALL), *_another_held(), _gate_open()],
            derived_vars=_return_other,
            steps=[_go(GATE), _go(_other_home), _put(_other, _other_home),
                   _go(_pallet), _pick(_pallet),
                   _go(GATE), _go(_delivery_bay), _put(_pallet, _delivery_bay)],
        ),
        MethodSchema(
            name="deliver_pallet_default_truck_side",
            parameters=[_pallet, _delivery_bay],
            guards=[_in(TRUCK_SIDE), _gate_open()],
            steps=[_go(_pallet), _pick(_pallet),
                   _go(GATE), _go(_delivery_bay), _put(_pallet, _delivery_bay)],
        ),
        MethodSchema(
            name="deliver_pallet_default_hall",
            parameters=[_pallet, _delivery_bay],
            guards=[_in(HALL), _gate_open()],
            steps=[_go(GATE), _go(_pallet), _pick(_pallet),
                   _go(GATE), _go(_delivery_bay), _put(_pallet, _delivery_bay)],
        ),
    ],
)


# =============================================================================
# WorkTask, the robot's: LOAD_RETURN
# =============================================================================

# Applicable to an empty pallet only: every method requires is_empty(?pallet).
load_return = WorkTask(
    name="load_return",
    parameters=[_pallet, _truck],
    parameter_types={"?pallet": "pallet", "?truck": "truck"},
    determined_parameters={"?truck": ("destination_of", "?pallet")},
    methods=[
        MethodSchema(
            name="load_return_held_truck_side",
            parameters=[_pallet, _truck],
            guards=[_in(TRUCK_SIDE), _empty(_pallet), _holds(_pallet)],
            steps=[_go(_truck), _put(_pallet, _truck)],
        ),
        MethodSchema(
            name="load_return_held_hall",
            parameters=[_pallet, _truck],
            guards=[_in(HALL), _empty(_pallet), _holds(_pallet), _gate_open()],
            steps=[_go(GATE), _go(_truck), _put(_pallet, _truck)],
        ),
        MethodSchema(
            name="load_return_return_empty_truck_side",
            parameters=[_pallet, _truck],
            guards=[_in(TRUCK_SIDE), _empty(_pallet), *_another_held(), _empty(_other), _gate_open()],
            derived_vars=_return_other,
            steps=[_go(GATE), _go(_other_home), _put(_other, _other_home),
                   _go(_pallet), _pick(_pallet),
                   _go(GATE), _go(_truck), _put(_pallet, _truck)],
        ),
        MethodSchema(
            name="load_return_return_empty_hall",
            parameters=[_pallet, _truck],
            guards=[_in(HALL), _empty(_pallet), *_another_held(), _empty(_other), _gate_open()],
            derived_vars=_return_other,
            steps=[_go(_other_home), _put(_other, _other_home),
                   _go(_pallet), _pick(_pallet),
                   _go(GATE), _go(_truck), _put(_pallet, _truck)],
        ),
        MethodSchema(
            name="load_return_return_full_truck_side",
            parameters=[_pallet, _truck],
            guards=[_in(TRUCK_SIDE), _empty(_pallet), *_another_held(), _gate_open()],
            derived_vars=_return_other,
            steps=[_go(_other_home), _put(_other, _other_home),
                   _go(GATE), _go(_pallet), _pick(_pallet),
                   _go(GATE), _go(_truck), _put(_pallet, _truck)],
        ),
        MethodSchema(
            name="load_return_return_full_hall",
            parameters=[_pallet, _truck],
            guards=[_in(HALL), _empty(_pallet), *_another_held(), _gate_open()],
            derived_vars=_return_other,
            steps=[_go(GATE), _go(_other_home), _put(_other, _other_home),
                   _go(GATE), _go(_pallet), _pick(_pallet),
                   _go(GATE), _go(_truck), _put(_pallet, _truck)],
        ),
        MethodSchema(
            name="load_return_default_truck_side",
            parameters=[_pallet, _truck],
            guards=[_in(TRUCK_SIDE), _empty(_pallet), _gate_open()],
            steps=[_go(GATE), _go(_pallet), _pick(_pallet),
                   _go(GATE), _go(_truck), _put(_pallet, _truck)],
        ),
        MethodSchema(
            name="load_return_default_hall",
            parameters=[_pallet, _truck],
            guards=[_in(HALL), _empty(_pallet), _gate_open()],
            steps=[_go(_pallet), _pick(_pallet),
                   _go(GATE), _go(_truck), _put(_pallet, _truck)],
        ),
    ],
)


# =============================================================================
# WorkTask, the human's: CONFIRM_DELIVERED_PALLET
# =============================================================================

# Applicable only while the pallet stands in its delivery bay (B2).
confirm_delivered_pallet = WorkTask(
    name="confirm_delivered_pallet",
    parameters=[_pallet, _delivery_bay],
    parameter_types={"?pallet": "pallet", "?delivery_bay": "delivery_bay"},
    determined_parameters={"?delivery_bay": ("destination_of", "?pallet")},
    methods=[
        MethodSchema(
            name="confirm_delivered_pallet_hall",
            parameters=[_pallet, _delivery_bay],
            guards=[_in(HALL), ConditionSchema("obj_at", (_pallet, _delivery_bay))],
            steps=[_go(_pallet), ActionStep(scan_it, {_item: _pallet})],
        ),
        MethodSchema(
            name="confirm_delivered_pallet_office",
            parameters=[_pallet, _delivery_bay],
            guards=[_in(OFFICE), ConditionSchema("obj_at", (_pallet, _delivery_bay))],
            steps=[_go(OFFICE_DOOR), _go(_pallet), ActionStep(scan_it, {_item: _pallet})],
        ),
    ],
)


# =============================================================================
# PersonalTasks (foreseeable): COFFEE_BREAK, OFFICE_BREAK
# =============================================================================

coffee_break = PersonalTask(
    name="coffee_break",
    parameters=[_coffee_machine],
    parameter_types={"?coffee_machine": "coffee_machine"},
    methods=[
        MethodSchema(
            name="coffee_break_hall",
            parameters=[_coffee_machine],
            guards=[_in(HALL)],
            steps=[
                _go(_coffee_machine),
                ActionStep(wait_at, {_entity: _coffee_machine, _duration: Const("PT60S")}),
            ],
        ),
        MethodSchema(
            name="coffee_break_office",
            parameters=[_coffee_machine],
            guards=[_in(OFFICE)],
            steps=[
                _go(OFFICE_DOOR),
                _go(_coffee_machine),
                ActionStep(wait_at, {_entity: _coffee_machine, _duration: Const("PT60S")}),
            ],
        ),
    ],
)

# B6, reduced (stage 1): the office door has no state and is a point on the
# way; the break ends at the chair with the wait.
office_break = PersonalTask(
    name="office_break",
    parameters=[_office_chair],
    parameter_types={"?office_chair": "office_chair"},
    methods=[
        MethodSchema(
            name="office_break_hall",
            parameters=[_office_chair],
            guards=[_in(HALL)],
            steps=[
                _go(OFFICE_DOOR),
                _go(_office_chair),
                ActionStep(wait_at, {_entity: _office_chair, _duration: Const("PT90S")}),
            ],
        ),
        MethodSchema(
            name="office_break_office",
            parameters=[_office_chair],
            guards=[_in(OFFICE)],
            steps=[
                _go(_office_chair),
                ActionStep(wait_at, {_entity: _office_chair, _duration: Const("PT90S")}),
            ],
        ),
    ],
)


# Human-only tasks (T-H): never given to a robot, so no hypothesis describes them.
# dock_loading's landmarks lie in the hall.

go_to = HumanOnlyTask(
    name="go_to",
    parameters=[_landmark],
    parameter_types={"?landmark": LANDMARK_TYPE},
    methods=[
        MethodSchema(
            name="go_to_hall",
            parameters=[_landmark],
            guards=[_in(HALL)],
            steps=[_go(_landmark)],
        ),
        MethodSchema(
            name="go_to_office",
            parameters=[_landmark],
            guards=[_in(OFFICE)],
            steps=[_go(OFFICE_DOOR), _go(_landmark)],
        ),
    ],
)

# ?duration is typed through the stand action's duration_key, not parameter_types.
stand_task = HumanOnlyTask(
    name="stand",
    parameters=[_duration],
    methods=[
        MethodSchema(
            name="stand_default",
            parameters=[_duration],
            guards=[],
            steps=[
                ActionStep(stand, {_duration: _duration}),
            ],
        )
    ],
)

# Walking to a landmark and standing there, as one decision (T-H3).
go_to_and_stand = HumanOnlyTask(
    name="go_to_and_stand",
    parameters=[_landmark, _duration],
    parameter_types={"?landmark": LANDMARK_TYPE},
    methods=[
        MethodSchema(
            name="go_to_and_stand_hall",
            parameters=[_landmark, _duration],
            guards=[_in(HALL)],
            steps=[_go(_landmark), ActionStep(stand, {_duration: _duration})],
        ),
        MethodSchema(
            name="go_to_and_stand_office",
            parameters=[_landmark, _duration],
            guards=[_in(OFFICE)],
            steps=[_go(OFFICE_DOOR), _go(_landmark), ActionStep(stand, {_duration: _duration})],
        ),
    ],
)
