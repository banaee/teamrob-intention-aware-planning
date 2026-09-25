# domains/kitting/tasks.py
"""
Task schema definitions for the kitting domain: the tree of task schemas (T-H).
These are the HTN compound tasks — decomposed into action schema sequences.
Each is a WorkTask (may be assigned), a PersonalTask (never assigned) or a
HumanOnlyTask (never given to a robot); a method's steps hold the action schema
objects they call.
"""

from shared.types import (Var, Const, ConditionSchema, ActionStep, MethodSchema,
                          WorkTask, PersonalTask, HumanOnlyTask, LANDMARK_TYPE)
from domains.kitting.actions import pick_up, move_to, place, wait_at, stand

_item      = Var("?item")
_kitting_table = Var("?kitting_table")
_coffee_machine = Var("?coffee_machine")
_ac_switch = Var("?ac_switch")

# target and entity are used in move_to and wait_at actions, respectively.
_target    = Var("?target")
_entity    = Var("?entity")

#   
_other     = Var("?other")   # whatever else the agent may be holding when this task starts
_agent = Var("?agent")
_landmark = Var("?landmark")
_duration = Var("?duration")


deliver_item = WorkTask(
    name="deliver_item",
    parameters=[_item, _kitting_table],
    parameter_types={"?item": "item", "?kitting_table": "kitting_table"},
    # ?kitting_table is not free: the item's destination is a fact of the
    # station (the layout's "destination"), so it is not enumerated and is
    # resolved from ?item when the task instance does not bind it; a bound
    # table is used as given (T-B1a).
    determined_parameters={"?kitting_table": ("destination_of", "?item")},
    methods=[
        MethodSchema(
            name="deliver_already_held",
            parameters=[_item, _kitting_table],
            guards=[
                ConditionSchema("holding", (_agent, _item)),
            ],
            steps=[
                ActionStep(move_to, {_target: _kitting_table}),
                ActionStep(place, {_item: _item, _target: _kitting_table}),
            ],
        ),
        MethodSchema(
            name="deliver_with_return",
            parameters=[_item, _kitting_table],
            guards=[
                ConditionSchema("holding", (_agent, _other)),
                ConditionSchema("not_equal", (_other, _item)),
            ],
            derived_vars={"?other_container": ("home_container_of", "?other")},
            steps=[
                ActionStep(move_to, {_target: Var("?other_container")}),
                ActionStep(place, {_item: _other, _target: Var("?other_container")}),
                ActionStep(move_to, {_target: _item}),
                ActionStep(pick_up, {_item: _item}),
                ActionStep(move_to, {_target: _kitting_table}),
                ActionStep(place, {_item: _item, _target: _kitting_table}),
            ],
        ),
        MethodSchema(
            name="deliver_default",
            parameters=[_item, _kitting_table],
            guards=[],
            steps=[
                ActionStep(move_to, {_target: _item}),
                ActionStep(pick_up, {_item: _item}),
                ActionStep(move_to, {_target: _kitting_table}),
                ActionStep(place, {_item: _item, _target: _kitting_table}),
            ],
        ),
    ],
)

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
        )
    ],
)

ac_activation = PersonalTask(
    name="ac_activation",
    parameters=[_ac_switch],
    parameter_types={"?ac_switch": "ac_switch"},
    methods=[
        MethodSchema(
            name="ac_activation_default",
            parameters=[_ac_switch],
            guards=[],
            steps=[
                ActionStep(move_to, {_target: _ac_switch}),
                ActionStep(wait_at, {_entity: _ac_switch, _duration: Const("PT2S")}),
            ],
        )
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
