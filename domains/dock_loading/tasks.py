"""
Task schema definitions for the dock_loading domain: the tree of task schemas (T-H).
These are the HTN compound tasks — decomposed into action schema sequences.
Each is a WorkTask (may be assigned), a PersonalTask (never assigned) or a
HumanOnlyTask (never given to a robot); a method's steps hold the action schema
objects they call. The forms are kitting's (domains/kitting/tasks.py).

TASKS:
    WorkTasks:
        deliver_pallet(?pallet, ?delivery_bay)  — the robot's: a pallet from the truck to a delivery bay
        load_return(?pallet)                    — the robot's: an empty pallet back into the truck
        confirm_delivered_pallet(?pallet)       — the human's: walk to the pallet and scan it
    PersonalTasks (foreseeable):
        coffee_break(?coffee_machine)           — walk to the coffee machine and wait
        office_break(?office_chair)             — walk through the office door to the chair and wait
    HumanOnlyTasks:
        go_to(?landmark), stand(?duration), go_to_and_stand(?landmark, ?duration)

Each task's methods are still build 1's (one method per task; office_break's
door condition holds in no world); T-G stage 1, step 7 replaces them
(docs/handoffs/plan_T-G_stage1.md, section 4).
"""

from shared.types import (Var, Const, ConditionSchema, ActionStep, MethodSchema,
                          WorkTask, PersonalTask, HumanOnlyTask, LANDMARK_TYPE)
from domains.dock_loading.actions import move_to, pick_up, place, wait_at, scan_it, stand

_pallet = Var("?pallet")
_delivery_bay = Var("?delivery_bay")
_empty_pallet_bay = Var("?empty_pallet_bay")
_coffee_machine = Var("?coffee_machine")
_office_chair= Var("?office_chair")

# target and entity are used in move_to and wait_at actions, respectively;
# item is the parameter of pick_up, place and scan_it, which a step binds to ?pallet.
_target = Var("?target")
_entity = Var("?entity")
_item = Var("?item")
_landmark = Var("?landmark")
_duration = Var("?duration")


# =============================================================================
# WorkTask, the robot's: DELIVER_PALLET
# =============================================================================

deliver_pallet = WorkTask(
    name="deliver_pallet",
    parameters=[_pallet, _delivery_bay],
    parameter_types={"?pallet": "pallet", "?delivery_bay": "delivery_bay"},
    methods=[
        MethodSchema(
            name="deliver_pallet_gate_open",
            parameters=[_pallet, _delivery_bay],
            guards=[
                ConditionSchema("is_open", (Const("dock_gate"),)),
            ],
            steps=[
                ActionStep(move_to, {_target: Const("dock_gate")}),
                ActionStep(move_to, {_target: _pallet}),
                ActionStep(pick_up, {_item: _pallet}),
                ActionStep(move_to, {_target: Const("dock_gate")}),
                ActionStep(move_to, {_target: _delivery_bay}),
                ActionStep(place, {_item: _pallet, _target: _delivery_bay}),
            ],
        ),
        # TODO: implement open_gate ActionSchema, then fill this method
        # MethodSchema(
        #     name="deliver_pallet_gate_closed",
        #     parameters=[_pallet, _delivery_bay],
        #     guards=[
        #         ConditionSchema("gate_is_closed", (Const("dock_gate"),)),
        #     ],
        #     steps=[
        #         ActionStep(move_to,   {_target: Const("dock_gate")}),
        #         ActionStep(open_gate, {_entity: Const("dock_gate")}),
        #         ActionStep(move_to,   {_target: _pallet}),
        #         ActionStep(pick_up,   {_item: _pallet}),
        #         ActionStep(move_to,   {_target: Const("dock_gate")}),
        #         ActionStep(move_to,   {_target: _delivery_bay}),
        #         ActionStep(place,     {_item: _pallet, _target: _delivery_bay}),
        #     ],
        # ),
    ],
)


# =============================================================================
# WorkTask, the robot's: LOAD_RETURN
# =============================================================================

load_return = WorkTask(
    name="load_return",
    parameters=[_pallet],
    parameter_types={"?pallet": "pallet"},
    methods=[
        MethodSchema(
            name="load_return_gate_open",
            parameters=[_pallet],
            guards=[
                ConditionSchema("is_open", (Const("dock_gate"),)),
            ],
            steps=[
                ActionStep(move_to, {_target: _pallet}),
                ActionStep(pick_up, {_item: _pallet}),
                ActionStep(move_to, {_target: Const("dock_gate")}),
                ActionStep(move_to, {_target: Const("truck_interior")}),
                ActionStep(place, {_item: _pallet, _target: Const("truck_interior")}),
            ],
        ),
        # TODO: gate_closed method — same pattern as deliver_pallet
    ],
)


# =============================================================================
# WorkTask, the human's: CONFIRM_DELIVERED_PALLET
# =============================================================================

confirm_delivered_pallet = WorkTask(
    name="confirm_delivered_pallet",
    parameters=[_pallet],
    parameter_types={"?pallet": "pallet"},
    methods=[
        MethodSchema(
            name="confirm_delivered_pallet_default",
            parameters=[_pallet],
            guards=[],
            steps=[
                ActionStep(move_to, {_target: _pallet}),
                ActionStep(scan_it, {_item: _pallet}),
            ],
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
            name="coffee_break_default",
            parameters=[_coffee_machine],
            guards=[],
            steps=[
                ActionStep(move_to, {_target: _coffee_machine}),
                ActionStep(wait_at, {_entity: _coffee_machine, _duration: Const("PT60S")}),
            ],
        ),
    ],
)

office_break = PersonalTask(
    name="office_break",
    parameters=[_office_chair],
    parameter_types={"?office_chair": "office_chair"},
    methods=[
            MethodSchema(
                name="office_break_default",
                parameters=[_office_chair],
                guards=[
                    ConditionSchema("door_is_open", (Const("office_door"),))
                ],
                steps=[
                    ActionStep(move_to, {_target: (Const("office_door"))}),
                    ActionStep(move_to, {_target: _office_chair}),
                    ActionStep(wait_at, {_entity: _office_chair, _duration: Const("PT60S")}),
                    ActionStep(move_to, {_target: Const("office_door")}),
                    ActionStep(move_to, {_target: Const("dock_gate")}),
                ],
            ),
            # TODO: office_door method — same pattern as deliver_pallet
        ],
)


# Human-only tasks (T-H): never given to a robot, so no hypothesis describes them.

go_to = HumanOnlyTask(
    name="go_to",
    parameters=[_landmark],
    parameter_types={"?landmark": LANDMARK_TYPE},
    methods=[
        MethodSchema(
            name="go_to_default",
            parameters=[_landmark],
            guards=[],
            steps=[
                ActionStep(move_to, {_target: _landmark}),
            ],
        )
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
            name="go_to_and_stand_default",
            parameters=[_landmark, _duration],
            guards=[],
            steps=[
                ActionStep(move_to, {_target: _landmark}),
                ActionStep(stand, {_duration: _duration}),
            ],
        )
    ],
)
