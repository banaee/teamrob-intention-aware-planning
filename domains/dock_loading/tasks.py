# domains/dock_loading/tasks.py
"""
Task schema definitions for the dock_loading domain.
These are the HTN compound tasks — decomposed into action sequences.

TASKS:
    Robot assigned:
        deliver_pallet(?pallet, ?dest)  — pick up full pallet from truck, deliver to hall area
        load_return(?pallet)            — pick up empty pallet from bay, load back to truck

    Human assigned:
        confirm_delivered_pallet(?pallet)            — move to pallet at delivery area and scan it

    Human foreseeable:
        coffee_break()                  — move to coffee machine and wait

METHODS NOTE:
    deliver_pallet and load_return each have two methods guarded by gate state:
        - "gate_open"   — gate_is_open in WorldState  (Phase 2.1: only this path runs)
        - "gate_closed" — gate_is_closed in WorldState (TODO: implement open_gate action)
    For Phase 2.1 the gate is always open, so the gate_closed method is a stub with
    an empty steps list and will never be selected. It exists to document the structure.
"""

from shared.types import Var, Const, ConditionSchema, StepCall, MethodSchema, TaskSchema
from domains.dock_loading.actions import move_to, pick_up, place, wait_at, scan_it

_pallet = Var("?pallet")
_delivery_bay = Var("?delivery_bay")
_empty_pallet_bay = Var("?empty_pallet_bay")
_coffee_machine = Var("?coffee_machine")
_office_chair= Var("?office_chair")

# target and entity are used in move_to and wait_at actions, respectively.
_target = Var("?target")
_entity = Var("?entity")


# =============================================================================
# Robot assigned: DELIVER_PALLET
# =============================================================================

deliver_pallet = TaskSchema(
    name="deliver_pallet",
    parameters=[_pallet, _delivery_bay],
    parameter_types={"?pallet": "pallet", "?delivery_bay": "delivery_bay"},
    methods=[
        MethodSchema(
            name="deliver_pallet_gate_open",
            parameters=[_pallet, _delivery_bay],
            guards=[
                ConditionSchema("gate_is_open", (Const("dock_gate"),)),
            ],
            step_calls=[
                StepCall(
                    action_name="move_to",
                    bindings={_target: Const("dock_gate")},
                ),
                StepCall(
                    action_name="move_to",
                    bindings={_target: _pallet},
                ),
                StepCall(
                    action_name="pick_up",
                    bindings={_pallet: _pallet},
                ),
                StepCall(
                    action_name="move_to",
                    bindings={_target: Const("dock_gate")},
                ),
                StepCall(
                    action_name="move_to",
                    bindings={_target: _delivery_bay},
                ),
                StepCall(
                    action_name="place",
                    bindings={_pallet: _pallet, _target: _delivery_bay},
                ),
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
        #         StepCall("move_to",   {_target: Const("dock_gate")}),
        #         StepCall("open_gate", {_entity: Const("dock_gate")}),
        #         StepCall("move_to",   {_target: _pallet}),
        #         StepCall("pick_up",   {_pallet: _pallet}),
        #         StepCall("move_to",   {_target: Const("dock_gate")}),
        #         StepCall("move_to",   {_target: _delivery_bay}),
        #         StepCall("place",     {_pallet: _pallet, _target: _delivery_bay}),
        #     ],
        # ),
    ],
    is_assigned=True,
    is_foreseeable=False,
)


# =============================================================================
# Robot assigned: LOAD_RETURN
# =============================================================================

load_return = TaskSchema(
    name="load_return",
    parameters=[_pallet],
    parameter_types={"?pallet": "pallet"},
    methods=[
        MethodSchema(
            name="load_return_gate_open",
            parameters=[_pallet],
            guards=[
                ConditionSchema("gate_is_open", (Const("dock_gate"),)),
            ],
            step_calls=[
                StepCall(
                    action_name="move_to",
                    bindings={_target: _pallet},
                ),
                StepCall(
                    action_name="pick_up",
                    bindings={_pallet: _pallet},
                ),
                StepCall(
                    action_name="move_to",
                    bindings={_target: Const("dock_gate")},
                ),
                StepCall(
                    action_name="move_to",
                    bindings={_target: Const("truck_interior")},
                ),
                StepCall(
                    action_name="place",
                    bindings={_pallet: _pallet, _target: Const("truck_interior")},
                ),
            ],
        ),
        # TODO: gate_closed method — same pattern as deliver_pallet
    ],
    is_assigned=True,
    is_foreseeable=False,
)


# =============================================================================
# Human assigned: CONFIRM_DELIVERED_PALLET
# =============================================================================

confirm_delivered_pallet = TaskSchema(
    name="confirm_delivered_pallet",
    parameters=[_pallet],
    methods=[
        MethodSchema(
            name="confirm_delivered_pallet_default",
            parameters=[_pallet],
            guards=[],
            step_calls=[
                StepCall(
                    action_name="move_to",
                    bindings={_target: _pallet},
                ),
                StepCall(
                    action_name="scan_it",
                    bindings={_pallet: _pallet},
                ),
            ],
        ),
    ],
    is_assigned=True,
    is_foreseeable=False,
)


# =============================================================================
# Human foreseeable: COFFEE_BREAK
# =============================================================================

coffee_break = TaskSchema(
    name="coffee_break",
    parameters=[_coffee_machine],
    parameter_types={"?coffee_machine": "coffee_machine"},
    methods=[
        MethodSchema(
            name="coffee_break_default",
            parameters=[_coffee_machine],
            guards=[],
            step_calls=[
                StepCall(
                    action_name="move_to",
                    bindings={_target: _coffee_machine},
                ),
                StepCall(
                    action_name="wait_at",
                    bindings={_entity: _coffee_machine, Var("?duration"): Const("PT60S")},
                ),
            ],
        ),
    ],
    is_assigned=False,
    is_foreseeable=True,
)

office_break = TaskSchema(
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
                step_calls=[
                    StepCall(
                        action_name="move_to",
                        bindings={_target: (Const("office_door"))}
                    ),
                    StepCall(
                        action_name="move_to",
                        bindings={_target: _office_chair},
                    ),
                    StepCall(
                        action_name="wait_at",
                        bindings={_entity: _office_chair, Var("?duration"): Const("PT60S")},                  ),
                    StepCall(
                        action_name="move_to",
                        bindings={_target: Const("office_door")},
                    ),
                    StepCall(
                        action_name="move_to",
                        bindings={_target: Const("dock_gate")}
                    ),
                ],
            ),
            # TODO: office_door method — same pattern as deliver_pallet
        ],
    is_assigned=False,
    is_foreseeable=True,
)
