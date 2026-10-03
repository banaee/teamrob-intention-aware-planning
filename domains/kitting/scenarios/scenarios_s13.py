# domains/kitting/scenarios/scenarios_s13.py
"""
Kitting scenarios on env_setup_13: T-K part 1's tests of context knowledge, round 1, the round without context
knowledge (the IRB; analysis/kitting/irb/tk1/README.md). One module per setup. The room is env_layout_15, the basic room;
the shift env_setup_13: item_1 on shelf_1, item_2 on shelf_2, item_3 on shelf_3, item_4 on shelf_4, all designated to kitting_table_0.
The recognizer is tested in isolation: the robot at (-400, 400) with an empty task pool, observing only. The human
starts at the kitting table, is assigned every delivery (never in an order), delivers them in one order, the same
in every scenario of this module (item_3, item_2, item_1, item_4), and ends every script with the exit
walk to corner_NE from the table. The only thing that varies is where one foreseeable task is placed: between
tasks (after the first, second or third delivery, so that a delivery stays live) or inside the second delivery
between its actions (the events at move_to occurrence 0, pick_up, move_to occurrence 1). _01 is the control,
the deliveries alone. No other deviation. Prior on (assignment knowledge); context knowledge is not built. The
durations are the schemas'. Every run stays below step 500 (TODO-66's context weight; the set's README).
"""

from shared.types import AgentConfig, ScenarioConfig, Script
from domains.kitting.actions import move_to, pick_up
from domains.kitting.script import deliver_item, coffee_break, go_to


_TK1 = (
    "T-K part 1, round 1 (no context knowledge), IRB on env_layout_15: the recognizer in isolation, against "
    "expectations derived from the records before the run (analysis/kitting/irb/tk1/). The robot at (-400, 400) "
    "with an empty task pool, observing only; the human starts at the kitting table, is assigned "
    "deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4) and delivers them in the order "
    "item_3, item_2, item_1, item_4, then the exit walk to corner_NE. Prior on. "
)

scenario_s13_01 = ScenarioConfig(
    id="scenario_s13_01",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    description=_TK1 + (
        "scenario_s13_01, deliveries alone, the control. Purpose: the control: the deliveries alone, no foreseeable task. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s13_02 = ScenarioConfig(
    id="scenario_s13_02",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    description=_TK1 + (
        "scenario_s13_02, coffee_break after the first delivery. Purpose: coffee_break between tasks, after the first delivery (item_3); deliveries of item_2, item_1, item_4 still live. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s13_03 = ScenarioConfig(
    id="scenario_s13_03",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    description=_TK1 + (
        "scenario_s13_03, coffee_break after the second delivery. Purpose: coffee_break between tasks, after the second delivery (item_2); deliveries of item_1, item_4 still live. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s13_04 = ScenarioConfig(
    id="scenario_s13_04",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    description=_TK1 + (
        "scenario_s13_04, coffee_break after the third delivery. Purpose: coffee_break between tasks, after the third delivery (item_1); deliveries of item_4 still live. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s13_05 = ScenarioConfig(
    id="scenario_s13_05",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    description=_TK1 + (
        "scenario_s13_05, coffee_break inside the second delivery, after the walk to the shelf, before the grasp. Purpose: coffee_break inside the second delivery (item_2), after the walk to the shelf, before the grasp; the delivery resumes after it. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s13_06 = ScenarioConfig(
    id="scenario_s13_06",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    description=_TK1 + (
        "scenario_s13_06, coffee_break inside the second delivery, after the grasp, the item in hand. Purpose: coffee_break inside the second delivery (item_2), after the grasp, the item in hand; the delivery resumes after it. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s13_07 = ScenarioConfig(
    id="scenario_s13_07",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    description=_TK1 + (
        "scenario_s13_07, coffee_break inside the second delivery, after the carry to the table, before the place, the item in hand. Purpose: coffee_break inside the second delivery (item_2), after the carry to the table, before the place, the item in hand; the delivery resumes after it. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=1),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)
