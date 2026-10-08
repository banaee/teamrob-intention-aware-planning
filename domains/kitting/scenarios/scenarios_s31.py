
"""
Kitting scenarios on env_setup_16: T-K part 1, step 5, the planning cases with context knowledge and a working robot
(design_records.md, "T-K", THE PLANNING CASES, RULED (KT15), THE ROOM, RULED and STEP 5, STAGE 1, REVISED: THE SET;
analysis/kitting/mpb/tk/README.md). One module per setup. The room is env_layout_18 (env_layout_17 plus the robot's
table kitting_table_1 and its shelves shelf_5 and shelf_6); the shift env_setup_16: item_4 on shelf_4 for
kitting_table_0 (the human's), item_5 on shelf_5 and item_6 on shelf_6 for kitting_table_1 (the robot's; disjoint
from the human's items and shelves).
The human starts at the kitting table, is assigned deliver_item(item_4) alone (the state of step 4's last delivery:
item_4, coffee_break and ac_activation live) and ends every script with the exit walk to corner_NE. Three scripts:
the delivery; a coffee break, then the delivery; the A/C, then the delivery. Each script runs on up to three sides:
context knowledge off and on (the scenario without a timeline: no context fact holds), and on with the raising fact
for the true task (the scenario stating its own timeline, the fact from tick 0 to the run's end). The robot has one
task, from a start that puts its route where the projection of the admitted task differs from the fallback projection:
the human's turn at shelf_4 (_01, _02), the human's stand at the coffee machine (_03, _04), the walk to the A/C switch
where the projection of the delivery lies elsewhere (_05, _06). Modelled behaviour only, besides the exit walk.
"""

from shared.types import AgentConfig, ScenarioConfig, Script, Timeline
from domains.kitting.script import deliver_item, coffee_break, go_to, ac_activation, window
from domains.kitting.facts import BREAK_TIME, ROOM_WARM


_TK5 = (
    "T-K part 1, step 5, the planning cases (analysis/kitting/mpb/tk/): the human starts at kitting_table_0, is assigned "
    "deliver_item(item_4) alone and ends with the exit walk to corner_NE; the robot has one task. "
)


def _human(script):
    return 



scenario_s31_01 = ScenarioConfig(
    id="scenario_s31_01",
    setup="env_setup_31",
    reference_layouts=["env_layout_30"],
    timeline=Timeline(()),
    description=_TK5 + (
        "scenario_s31_01, a coffee break, Hadi test on top of scenario_s16_03."
    ),
    agents=[
        AgentConfig(
        agent_id="human_0",
        agent_type="human",
        start_position=(-200, -300),
        scheduled_tasks=Script([coffee_break("coffee_machine_0"), 
                deliver_item("item_4", table="kitting_table_0"), 
                go_to("corner_NE")]
                               ),
        assigned_tasks=[deliver_item("item_4", table="kitting_table_0")],
        observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-300, 0),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_1"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),    
    ],
)


