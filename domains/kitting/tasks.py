# domains/kitting/tasks.py
"""
Task schema definitions for the kitting domain.
These are the HTN compound tasks — decomposed into action schema sequences.
"""

from shared.types import Var, Const, ConditionSchema, StepCall, MethodSchema, TaskSchema
from domains.kitting.actions import pick_up, move_to, place, wait_at

_item      = Var("?item")
_target    = Var("?target")
_entity    = Var("?entity")

# TODO: later Var("?coffee_machine") and Var("?ac_switch") for more flexible task definitions, 
# if needed. For now, hardcoding to specific constant objects for simplicity.

deliver_item = TaskSchema(
    name="deliver_item",
    parameters=[_item],
    methods=[
        MethodSchema(
            name="deliver_default",
            parameters=[_item],
            guards=[],
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
                    bindings={_target: Const("kitting_table")},
                ),
                StepCall(
                    action_name="place",
                    bindings={_item: _item, _target: Const("kitting_table")},
                ),
            ],
        )
    ],
    is_assigned=True,
    is_foreseeable=False,
)

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
                    bindings={_entity: Const("coffee_machine_0"), Var("?duration"): Const("PT60S")},   # using processcompletion 
                ),
            ],
        )
    ],
    is_assigned=False,
    is_foreseeable=True,
)

ac_activation = TaskSchema(
    name="ac_activation",
    parameters=[],
    methods=[
        MethodSchema(
            name="ac_activation_default",
            parameters=[],
            guards=[],
            steps=[
                StepCall(
                    action_name="move_to",
                    bindings={_target: Const("ac_switch_0")},
                ),
                StepCall(
                    action_name="wait_at",
                    bindings={_entity: Const("ac_switch_0"), Var("?duration"): Const("PT2S")},  # using processcompletion
                ),
            ],
        )
    ],
    is_assigned=False,
    is_foreseeable=True,
)