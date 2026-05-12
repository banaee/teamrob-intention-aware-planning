# domains/dock_loading/tasks.py
"""
Task schema definitions for the dock_loading domain.
These are the HTN compound tasks — decomposed into action operator sequences.

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
from domains.dock_loading.actionOperators import move_to, pick_up, place, wait_at, scan_it

_item = Var("?item")
_dest   = Var("?dest")
_target = Var("?target")
_entity = Var("?entity")


# =============================================================================
# Robot assigned: DELIVER_PALLET
# =============================================================================

deliver_pallet = TaskSchema(
    name="deliver_pallet",
    parameters=[_item, _dest],
    methods=[
        MethodSchema(
            name="deliver_pallet_gate_open",
            parameters=[_item, _dest],
            guards=[
                ConditionSchema("gate_is_open", (Const("dock_gate"),)),
            ],
            steps=[
                StepCall(
                    action_name="move_to",
                    bindings={_target: Const("dock_gate")},
                ),
                StepCall(
                    action_name="move_to",
                    bindings={_target: _item},
                ),
                StepCall(
                    action_name="pick_up",
                    bindings={_item: _item},
                ),
                StepCall(
                    action_name="move_to",
                    bindings={_target: Const("dock_gate")},
                ),
                StepCall(
                    action_name="move_to",
                    bindings={_target: _dest},
                ),
                StepCall(
                    action_name="place",
                    bindings={_item: _item, _target: _dest},
                ),
            ],
        ),
        # TODO: implement open_gate ActionOperator, then fill this method
        # MethodSchema(
        #     name="deliver_pallet_gate_closed",
        #     parameters=[_item, _dest],
        #     guards=[
        #         ConditionSchema("gate_is_closed", (Const("dock_gate"),)),
        #     ],
        #     steps=[
        #         StepCall("move_to",   {_target: Const("dock_gate")}),
        #         StepCall("open_gate", {_entity: Const("dock_gate")}),
        #         StepCall("move_to",   {_target: _item}),
        #         StepCall("pick_up",   {_item: _item}),
        #         StepCall("move_to",   {_target: Const("dock_gate")}),
        #         StepCall("move_to",   {_target: _dest}),
        #         StepCall("place",     {_item: _item, _target: _dest}),
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
    parameters=[_item],
    methods=[
        MethodSchema(
            name="load_return_gate_open",
            parameters=[_item],
            guards=[
                ConditionSchema("gate_is_open", (Const("dock_gate"),)),
            ],
            steps=[
                StepCall(
                    action_name="move_to",
                    bindings={_target: _item},
                ),
                StepCall(
                    action_name="pick_up",
                    bindings={_item: _item},
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
                    bindings={_item: _item, _target: Const("truck_interior")},
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
    parameters=[_item],
    methods=[
        MethodSchema(
            name="confirm_delivered_pallet_default",
            parameters=[_item],
            guards=[],
            steps=[
                StepCall(
                    action_name="move_to",
                    bindings={_target: _item},
                ),
                StepCall(
                    action_name="scan_it",
                    bindings={_item: _item},
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
    parameters=[],
    methods=[
        MethodSchema(
            name="coffee_break_default",
            parameters=[],
            guards=[],
            steps=[
                StepCall(
                    action_name="move_to",
                    bindings={_target: Const("coffee_machine_0")},
                ),
                StepCall(
                    action_name="wait_at",
                    bindings={_entity: Const("coffee_machine_0"), Var("?duration"): Const("PT60S")},
                ),
            ],
        ),
    ],
    is_assigned=False,
    is_foreseeable=True,
)

go_to_office = TaskSchema(
    name="go_to_office",
    parameters=[],
    methods=[MethodSchema(
        name="go_to_office_default",
        parameters=[],
        guards=[],
        steps=[
            StepCall("move_to", {Var("?target"): Const("office_door")}),
            StepCall("wait_at", {Var("?entity"): Const("office_door"), Var("?duration"): Const("PT80S")}),
        ],
    )],
    is_assigned=False,
    is_foreseeable=True,
)
