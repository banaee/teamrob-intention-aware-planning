# domains/kitting/scenarios/scenarios_s16.py
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
    return AgentConfig(
        agent_id="human_0",
        agent_type="human",
        start_position=(0, 450),
        scheduled_tasks=Script(script),
        assigned_tasks=[deliver_item("item_4", table="kitting_table_0")],
        observes=[],
    )


def _robot(start, item):
    return AgentConfig(
        agent_id="robot_0",
        agent_type="robot",
        start_position=start,
        assigned_tasks=[deliver_item(item, table="kitting_table_1")],
        observes=["human_0"],
    )


scenario_s16_01 = ScenarioConfig(
    id="scenario_s16_01",
    setup="env_setup_16",
    reference_layouts=["env_layout_18"],
    timeline=Timeline(()),
    description=_TK5 + (
        "scenario_s16_01, the delivery, no context fact (cases 3 and, with _02, 2). The robot carries item_5 from "
        "shelf_5 along the south wall and, unheld, passes the point where the human stands at shelf_4 and turns north "
        "(ticks 45 to 48). Run with context knowledge off and on: on, the lone delivery is admitted on the human's "
        "first step and its plan holds the turn; off, no projection reaches past the arrival."
    ),
    agents=[
        _human([deliver_item("item_4", table="kitting_table_0"), go_to("corner_NE")]),
        _robot((-470, -120), "item_5"),
    ],
)

scenario_s16_02 = ScenarioConfig(
    id="scenario_s16_02",
    setup="env_setup_16",
    reference_layouts=["env_layout_18"],
    timeline=Timeline((window(BREAK_TIME, 0),)),
    description=_TK5 + (
        "scenario_s16_02, scenario_s16_01's script and robot under break_time from tick 0 to the run's end (case 2: "
        "raised, against: the human delivers through the whole break time). Run with context knowledge on."
    ),
    agents=[
        _human([deliver_item("item_4", table="kitting_table_0"), go_to("corner_NE")]),
        _robot((-470, -120), "item_5"),
    ],
)

scenario_s16_03 = ScenarioConfig(
    id="scenario_s16_03",
    setup="env_setup_16",
    reference_layouts=["env_layout_18"],
    timeline=Timeline(()),
    description=_TK5 + (
        "scenario_s16_03, a coffee break, then the delivery, no context fact (case 4, and with _04 case 1). The robot "
        "carries item_6 from shelf_6 along the east wall and, unheld, passes the point where the human stands at the "
        "coffee machine as the stand begins (36 cm at tick 43, 12 cm at 45). Run with context knowledge off and on: on, "
        "the lone delivery is admitted on the human's first step and holds until its retraction at 43."
    ),
    agents=[
        _human([coffee_break("coffee_machine_0"), deliver_item("item_4", table="kitting_table_0"), go_to("corner_NE")]),
        _robot((-200, 0), "item_6"),
    ],
)

scenario_s16_04 = ScenarioConfig(
    id="scenario_s16_04",
    setup="env_setup_16",
    reference_layouts=["env_layout_18"],
    timeline=Timeline((window(BREAK_TIME, 0),)),
    description=_TK5 + (
        "scenario_s16_04, scenario_s16_03's script and robot under break_time from tick 0 to the run's end (case 1: "
        "raised, in accord: the coffee break inside break time, its stand at the machine). Run with context knowledge on."
    ),
    agents=[
        _human([coffee_break("coffee_machine_0"), deliver_item("item_4", table="kitting_table_0"), go_to("corner_NE")]),
        _robot((-200, 0), "item_6"),
    ],
)

scenario_s16_05 = ScenarioConfig(
    id="scenario_s16_05",
    setup="env_setup_16",
    reference_layouts=["env_layout_18"],
    timeline=Timeline(()),
    description=_TK5 + (
        "scenario_s16_05, the A/C, then the delivery, no context fact (case 5). The robot walks from the north-east to "
        "shelf_5 for item_5 and, unheld, crosses the human's walk to the A/C switch at about tick 24 (29 cm), 67 to 84 "
        "cm from where the projection of the delivery puts the human. Run with context knowledge off and on: on, the "
        "delivery is admitted on the human's first step and the movement does not correct it before the switch."
    ),
    agents=[
        _human([ac_activation("ac_switch_0"), deliver_item("item_4", table="kitting_table_0"), go_to("corner_NE")]),
        _robot((400, 210), "item_5"),
    ],
)

scenario_s16_06 = ScenarioConfig(
    id="scenario_s16_06",
    setup="env_setup_16",
    reference_layouts=["env_layout_18"],
    timeline=Timeline((window(ROOM_WARM, 0),)),
    description=_TK5 + (
        "scenario_s16_06, scenario_s16_05's script and robot under room_warm from tick 0 to the run's end (case 5's "
        "third side: the A/C raised, in accord). Run with context knowledge on."
    ),
    agents=[
        _human([ac_activation("ac_switch_0"), deliver_item("item_4", table="kitting_table_0"), go_to("corner_NE")]),
        _robot((400, 210), "item_5"),
    ],
)
