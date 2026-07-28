# domains/kitting/tasks.py
"""
Task schema definitions for the kitting domain.
These are the HTN compound tasks — decomposed into action schema sequences.
"""

from shared.types import Var, Const, ConditionSchema, StepCall, MethodSchema, TaskSchema
from domains.kitting.actions import pick_up, move_to, place, wait_at

_item      = Var("?item")
_kitting_table = Var("?kitting_table")
_coffee_machine = Var("?coffee_machine")
_ac_switch = Var("?ac_switch")

# target and entity are used in move_to and wait_at actions, respectively.
_target    = Var("?target")
_entity    = Var("?entity")


deliver_item = TaskSchema(
    name="deliver_item",
    parameters=[_item, _kitting_table],
    parameter_types={"?item": "item", "?kitting_table": "kitting_table"},
    methods=[
        MethodSchema(
            name="deliver_default",
            parameters=[_item, _kitting_table],
            guards=[],
            step_calls=[
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
                    bindings={_target: _kitting_table}
                ),
                StepCall(
                    action_name="place",
                    bindings={_item: _item, _target: _kitting_table},
                ),
            ],
        )
    ],
    is_assigned=True,
    is_foreseeable=False,
)

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
                    bindings={_entity: _coffee_machine, Var("?duration"): Const("PT60S")},   # using processcompletion 
                ),
            ],
        )
    ],
    is_assigned=False,
    is_foreseeable=True,
)

ac_activation = TaskSchema(
    name="ac_activation",
    parameters=[_ac_switch],
    parameter_types={"?ac_switch": "ac_switch"},
    methods=[
        MethodSchema(
            name="ac_activation_default",
            parameters=[_ac_switch],
            guards=[],
            step_calls=[
                StepCall(
                    action_name="move_to",
                    bindings={_target: _ac_switch},
                ),
                StepCall(
                    action_name="wait_at",
                    bindings={_entity: _ac_switch, Var("?duration"): Const("PT2S")},  # using processcompletion
                ),
            ],
        )
    ],
    is_assigned=False,
    is_foreseeable=True,
)