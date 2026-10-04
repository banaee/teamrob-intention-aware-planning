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
T-K part 1, step 4 (4 October 2026; analysis/kitting/irb/tk2/README.md): the setup states the default timeline of
context facts, break_time from 178 to 300 (every scenario of round 1 above meets it). From _08 on, the scenarios
run a script of round 1 (or a new one) under a timeline of their own (Hadi's 3B to 3F, ccode's P1 to P9), with
context knowledge on; their off side is round 1's run of the same script.
"""

from shared.types import AgentConfig, ScenarioConfig, Script, Timeline
from domains.kitting.actions import move_to, pick_up
from domains.kitting.facts import BREAK_TIME, ROOM_WARM
from domains.kitting.script import deliver_item, coffee_break, go_to, window


_TK1 = (
    "T-K part 1, round 1 (no context knowledge), IRB on env_layout_15: the recognizer in isolation, against "
    "expectations derived from the records before the run (analysis/kitting/irb/tk1/). The robot at (-400, 400) "
    "with an empty task pool, observing only; the human starts at the kitting table, is assigned "
    "deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4) and delivers them in the order "
    "item_3, item_2, item_1, item_4, then the exit walk to corner_NE. Prior on. "
)

_TK2 = (
    "T-K part 1, step 4 (context knowledge on), IRB on env_layout_15: the recognizer in isolation, against expectations "
    "derived before the run (analysis/kitting/irb/tk2/). "
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

scenario_s13_08 = ScenarioConfig(
    id="scenario_s13_08",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    timeline=Timeline((window(BREAK_TIME, 50, 200),)),
    description=_TK2 + (
        "scenario_s13_08, scenario_s13_02's script, its own timeline: break_time from 50 to 200. Purpose: 3B, the window's edge before the human leaves for the break (during the first delivery)."
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

scenario_s13_09 = ScenarioConfig(
    id="scenario_s13_09",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    timeline=Timeline((window(BREAK_TIME, 90, 200),)),
    description=_TK2 + (
        "scenario_s13_09, scenario_s13_02's script, its own timeline: break_time from 90 to 200. Purpose: 3B, the window's edge during the walk to the coffee machine."
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

scenario_s13_10 = ScenarioConfig(
    id="scenario_s13_10",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    timeline=Timeline((window(BREAK_TIME, 120, 200),)),
    description=_TK2 + (
        "scenario_s13_10, scenario_s13_02's script, its own timeline: break_time from 120 to 200. Purpose: 3B, the window's edge during the wait at the coffee machine."
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

scenario_s13_11 = ScenarioConfig(
    id="scenario_s13_11",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    timeline=Timeline((window(BREAK_TIME, 40, 190),)),
    description=_TK2 + (
        "scenario_s13_11, scenario_s13_03's script, its own timeline: break_time from 40 to 190. Purpose: 3D, the window opens during the first delivery, the second lies inside it, the break comes late in it; the window closes during the wait."
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

scenario_s13_12 = ScenarioConfig(
    id="scenario_s13_12",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    timeline=Timeline((window(BREAK_TIME, 40, 150),)),
    description=_TK2 + (
        "scenario_s13_12, scenario_s13_03's script, its own timeline: break_time from 40 to 150. Purpose: 3D, as scenario_s13_11, the window closing during the walk to the coffee machine."
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

scenario_s13_13 = ScenarioConfig(
    id="scenario_s13_13",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    timeline=Timeline(()),
    description=_TK2 + (
        "scenario_s13_13, scenario_s13_04's script, its own timeline stated empty: no timeline fact holds. Purpose: 3E, no timeline fact, one delivery live, then the break: the early admission and its retraction."
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

scenario_s13_14 = ScenarioConfig(
    id="scenario_s13_14",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    timeline=Timeline((window(BREAK_TIME, 0),)),
    description=_TK2 + (
        "scenario_s13_14, scenario_s13_01's script, its own timeline: break_time from 0 to the run's end. Purpose: P1, every delivery against the raised coffee break, the coffee machine's neighbour item_2 included."
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

scenario_s13_15 = ScenarioConfig(
    id="scenario_s13_15",
    setup="env_setup_13",
    reference_layouts=["env_layout_15"],
    timeline=Timeline(()),
    description=_TK2 + (
        "scenario_s13_15, a new script: the deliveries of scenario_s13_01 with the coffee_break inside the last delivery (item_4), after the walk to the shelf, before the grasp, its own timeline stated empty: no timeline fact holds. Purpose: P7, a lone delivery admitted early and rightly, then cut by the break inside it."
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
                deliver_item("item_4", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
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
