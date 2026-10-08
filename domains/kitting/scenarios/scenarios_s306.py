# domains/kitting/scenarios/scenarios_s306.py
"""
Kitting scenarios on env_setup_306, a copy of Hadi's env_setup_304 (T-pres, the deck's replays; design_records.md,
"T-pres, the talk", NEW SCENARIOS FOR THE REPLAYS): copies of Hadi's scenarios under new ids, his own files untouched;
outside every measured set. The room is env_layout_07.
_01: scenario_s304_14 without the first coffee break, the robot starting at (-750, -200) instead of (-750, 400), and
with its own timeline: break_time in force over the coffee break (talk stage 5, context: the situation makes a behaviour
more likely, and the robot adapts earlier). The robot's start was chosen from a grid of starts run with the override
scenario.robot_0.start_position, as the one where the robot chooses its next task between the two ticks at which the
coffee break is trusted with and without context knowledge; what the robot then does is the framework's own result. Run twice, context knowledge off and on
(configs/kitting/tpres/stage5_s306_01_ck_off.yaml, _ck_on.yaml): one situation without and with context knowledge. The
window is placed from the run with context knowledge off (in which the timeline acts on nothing), before the run with
it on, half-open in ticks (AM46).
"""

from shared.types import AgentConfig, ScenarioConfig, Script, Timeline
from domains.kitting.facts import BREAK_TIME
from domains.kitting.script import deliver_item, coffee_break, go_to, window


scenario_s306_01 = ScenarioConfig(
    id="scenario_s306_01",
    setup="env_setup_306",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 50, 120),)),
    description=(
        "scenario_s306_01: T-pres, talk stage 5: scenario_s304_14 without the first coffee break, the robot's start "
        "moved; break_time in force from 50 to 120, over the coffee break (58 to 118 in the run with context knowledge "
        "off)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -300),
            scheduled_tasks=Script([
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_53", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_52", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-750, -200),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)
