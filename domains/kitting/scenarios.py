# domains/kitting/scenarios.py
"""
Scenario definitions for the kitting domain.
Task assignments reference domain schemas directly — no string parsing,
no YAML, no ? prefix conventions.
is_foreseeable is declared on TaskSchema — not repeated here.
"""

from shared.types import Var, Const, TaskInstance, AgentConfig, ScenarioConfig
from domains.kitting.tasks import deliver_item, coffee_break, ac_activation


scenario_01 = ScenarioConfig(
    id="scenario_01",
    name="basic_kitting_with_coffee_break",
    description=(
        "Human and robot each deliver items to the kitting table. "
        "Human deviates to a coffee break after completing their first delivery. "
        "Robot must recognize the deviation and replan accordingly."
    ),
    env_layout="env1_layout",
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2")}),
                TaskInstance(schema=coffee_break,  bindings={}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(200, 200),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7")}),
            ],
            observes=["human_0"],
        ),
    ],
)