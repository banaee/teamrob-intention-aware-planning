# domains/kitting/scenarios/scenarios_s15.py
"""
Kitting scenarios on env_setup_15: T-K part 1's tests of context knowledge, round 1, the round without context
knowledge (the IRB; analysis/kitting/irb/tk1/README.md). One module per setup. The room is env_layout_17, the room where the A/C switch competes with deliveries;
the shift env_setup_15: item_1 on shelf_1, item_2 on shelf_2, item_3 on shelf_3, item_4 on shelf_4, all designated to kitting_table_0.
The recognizer is tested in isolation: the robot at (-400, 400) with an empty task pool, observing only. The human
starts at the kitting table, is assigned every delivery (never in an order), delivers them in one order, the same
in every scenario of this module (item_3, item_2, item_1, item_4), and ends every script with the exit
walk to corner_NE from the table. The only thing that varies is where one foreseeable task is placed: between
tasks (after the first, second or third delivery, so that a delivery stays live) or inside the second delivery
between its actions (the events at move_to occurrence 0, pick_up, move_to occurrence 1). _01 is the control,
the deliveries alone. No other deviation. Prior on (assignment knowledge); context knowledge is not built. The
durations are the schemas'. Every run stays below step 500 (TODO-66's context weight; the set's README).
T-K part 1, step 4 (4 October 2026; analysis/kitting/irb/tk2/README.md): the setup states the default timeline of
context facts, break_time from 178 to 300 (every scenario of round 1 without an A/C activation
meets it); each script with an A/C activation states its own, room_warm from 150 to the
run's end (Hadi's 3A). From _14 on, the scenarios
run a script of round 1 (or a new one) under a timeline of their own (Hadi's 3B to 3F, ccode's P1 to P9), with
context knowledge on; their off side is round 1's run of the same script.
"""

from shared.types import AgentConfig, ScenarioConfig, Script, Timeline
from domains.kitting.actions import move_to, pick_up
from domains.kitting.facts import BREAK_TIME, ROOM_WARM
from domains.kitting.script import deliver_item, coffee_break, go_to, ac_activation, window


_TK1 = (
    "T-K part 1, round 1 (no context knowledge), IRB on env_layout_17: the recognizer in isolation, against "
    "expectations derived from the records before the run (analysis/kitting/irb/tk1/). The robot at (-400, 400) "
    "with an empty task pool, observing only; the human starts at the kitting table, is assigned "
    "deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4) and delivers them in the order "
    "item_3, item_2, item_1, item_4, then the exit walk to corner_NE. Prior on. "
)

_TK2 = (
    "T-K part 1, step 4 (context knowledge on), IRB on env_layout_17: the recognizer in isolation, against expectations "
    "derived before the run (analysis/kitting/irb/tk2/). "
)

scenario_s15_01 = ScenarioConfig(
    id="scenario_s15_01",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    description=_TK1 + (
        "scenario_s15_01, deliveries alone, the control. Purpose: the control: the deliveries alone, no foreseeable task. Modelled behaviour only, besides the exit walk."
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

scenario_s15_02 = ScenarioConfig(
    id="scenario_s15_02",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    description=_TK1 + (
        "scenario_s15_02, coffee_break after the first delivery. Purpose: coffee_break between tasks, after the first delivery (item_3); deliveries of item_2, item_1, item_4 still live. Modelled behaviour only, besides the exit walk."
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

scenario_s15_03 = ScenarioConfig(
    id="scenario_s15_03",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    description=_TK1 + (
        "scenario_s15_03, coffee_break after the second delivery. Purpose: coffee_break between tasks, after the second delivery (item_2); deliveries of item_1, item_4 still live. Modelled behaviour only, besides the exit walk."
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

scenario_s15_04 = ScenarioConfig(
    id="scenario_s15_04",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    description=_TK1 + (
        "scenario_s15_04, coffee_break after the third delivery. Purpose: coffee_break between tasks, after the third delivery (item_1); deliveries of item_4 still live. Modelled behaviour only, besides the exit walk."
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

scenario_s15_05 = ScenarioConfig(
    id="scenario_s15_05",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    description=_TK1 + (
        "scenario_s15_05, coffee_break inside the second delivery, after the walk to the shelf, before the grasp. Purpose: coffee_break inside the second delivery (item_2), after the walk to the shelf, before the grasp; the delivery resumes after it. Modelled behaviour only, besides the exit walk."
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

scenario_s15_06 = ScenarioConfig(
    id="scenario_s15_06",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    description=_TK1 + (
        "scenario_s15_06, coffee_break inside the second delivery, after the grasp, the item in hand. Purpose: coffee_break inside the second delivery (item_2), after the grasp, the item in hand; the delivery resumes after it. Modelled behaviour only, besides the exit walk."
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

scenario_s15_07 = ScenarioConfig(
    id="scenario_s15_07",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    description=_TK1 + (
        "scenario_s15_07, coffee_break inside the second delivery, after the carry to the table, before the place, the item in hand. Purpose: coffee_break inside the second delivery (item_2), after the carry to the table, before the place, the item in hand; the delivery resumes after it. Modelled behaviour only, besides the exit walk."
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

scenario_s15_08 = ScenarioConfig(
    id="scenario_s15_08",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    timeline=Timeline((window(ROOM_WARM, 150),)),
    description=_TK1 + (
        "scenario_s15_08, ac_activation after the first delivery. Purpose: ac_activation between tasks, after the first delivery (item_3); deliveries of item_2, item_1, item_4 still live. Modelled behaviour only, besides the exit walk. Its own timeline (T-K part 1, step 4, Hadi's 3A): room_warm from 150 to the run's end, no break_time."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
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

scenario_s15_09 = ScenarioConfig(
    id="scenario_s15_09",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    timeline=Timeline((window(ROOM_WARM, 150),)),
    description=_TK1 + (
        "scenario_s15_09, ac_activation after the second delivery. Purpose: ac_activation between tasks, after the second delivery (item_2); deliveries of item_1, item_4 still live. Modelled behaviour only, besides the exit walk. Its own timeline (T-K part 1, step 4, Hadi's 3A): room_warm from 150 to the run's end, no break_time."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
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

scenario_s15_10 = ScenarioConfig(
    id="scenario_s15_10",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    timeline=Timeline((window(ROOM_WARM, 150),)),
    description=_TK1 + (
        "scenario_s15_10, ac_activation after the third delivery. Purpose: ac_activation between tasks, after the third delivery (item_1); deliveries of item_4 still live. Modelled behaviour only, besides the exit walk. Its own timeline (T-K part 1, step 4, Hadi's 3A): room_warm from 150 to the run's end, no break_time."
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
                ac_activation("ac_switch_0"),
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

scenario_s15_11 = ScenarioConfig(
    id="scenario_s15_11",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    timeline=Timeline((window(ROOM_WARM, 150),)),
    description=_TK1 + (
        "scenario_s15_11, ac_activation inside the second delivery, after the walk to the shelf, before the grasp. Purpose: ac_activation inside the second delivery (item_2), after the walk to the shelf, before the grasp; the delivery resumes after it. Modelled behaviour only, besides the exit walk. Its own timeline (T-K part 1, step 4, Hadi's 3A): room_warm from 150 to the run's end, no break_time."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0").at(move_to, ac_activation("ac_switch_0"), occurrence=0),
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

scenario_s15_12 = ScenarioConfig(
    id="scenario_s15_12",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    timeline=Timeline((window(ROOM_WARM, 150),)),
    description=_TK1 + (
        "scenario_s15_12, ac_activation inside the second delivery, after the grasp, the item in hand. Purpose: ac_activation inside the second delivery (item_2), after the grasp, the item in hand; the delivery resumes after it. Modelled behaviour only, besides the exit walk. Its own timeline (T-K part 1, step 4, Hadi's 3A): room_warm from 150 to the run's end, no break_time."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0").at(pick_up, ac_activation("ac_switch_0")),
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

scenario_s15_13 = ScenarioConfig(
    id="scenario_s15_13",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    timeline=Timeline((window(ROOM_WARM, 150),)),
    description=_TK1 + (
        "scenario_s15_13, ac_activation inside the second delivery, after the carry to the table, before the place, the item in hand. Purpose: ac_activation inside the second delivery (item_2), after the carry to the table, before the place, the item in hand; the delivery resumes after it. Modelled behaviour only, besides the exit walk. Its own timeline (T-K part 1, step 4, Hadi's 3A): room_warm from 150 to the run's end, no break_time."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0").at(move_to, ac_activation("ac_switch_0"), occurrence=1),
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

scenario_s15_14 = ScenarioConfig(
    id="scenario_s15_14",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    timeline=Timeline((window(ROOM_WARM, 50),)),
    description=_TK2 + (
        "scenario_s15_14, scenario_s15_08's script, its own timeline: room_warm from 50 to the run's end. Purpose: 3C, room_warm's edge before the human leaves for the A/C switch (during the first delivery)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
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

scenario_s15_15 = ScenarioConfig(
    id="scenario_s15_15",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    timeline=Timeline((window(ROOM_WARM, 90),)),
    description=_TK2 + (
        "scenario_s15_15, scenario_s15_08's script, its own timeline: room_warm from 90 to the run's end. Purpose: 3C, room_warm's edge during the walk to the A/C switch."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
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

scenario_s15_16 = ScenarioConfig(
    id="scenario_s15_16",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    timeline=Timeline((window(ROOM_WARM, 0, 90),)),
    description=_TK2 + (
        "scenario_s15_16, scenario_s15_08's script, its own timeline: room_warm from 0 to 90. Purpose: 3C, room_warm from the start, its end during the walk to the A/C switch."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
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

scenario_s15_17 = ScenarioConfig(
    id="scenario_s15_17",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    timeline=Timeline((window(BREAK_TIME, 178, 300), window(ROOM_WARM, 150))),
    description=_TK2 + (
        "scenario_s15_17, scenario_s15_04's script, its own timeline: break_time from 178 to 300; room_warm from 150 to the run's end. Purpose: 3F, both facts: the coffee break inside break_time with the A/C raised."
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

scenario_s15_18 = ScenarioConfig(
    id="scenario_s15_18",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    timeline=Timeline((window(ROOM_WARM, 0),)),
    description=_TK2 + (
        "scenario_s15_18, scenario_s15_01's script, its own timeline: room_warm from 0 to the run's end. Purpose: P2, a warm room in which the human never switches the A/C on: the deliveries beside the switch against the raised A/C."
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

scenario_s15_19 = ScenarioConfig(
    id="scenario_s15_19",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    timeline=Timeline(()),
    description=_TK2 + (
        "scenario_s15_19, scenario_s15_10's script, its own timeline stated empty: no timeline fact holds. Purpose: P4, case 3E with the A/C activation, whose switch stands beside the lone delivery's shelf."
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
                ac_activation("ac_switch_0"),
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

scenario_s15_20 = ScenarioConfig(
    id="scenario_s15_20",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    timeline=Timeline((window(BREAK_TIME, 178, 300), window(ROOM_WARM, 150))),
    description=_TK2 + (
        "scenario_s15_20, scenario_s15_10's script, its own timeline: break_time from 178 to 300; room_warm from 150 to the run's end. Purpose: P6, case 3F's mirror: the A/C activation the true task with both facts."
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
                ac_activation("ac_switch_0"),
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

scenario_s15_21 = ScenarioConfig(
    id="scenario_s15_21",
    setup="env_setup_15",
    reference_layouts=["env_layout_17"],
    timeline=Timeline((window(BREAK_TIME, 307),)),
    description=_TK2 + (
        "scenario_s15_21, a new script: the four deliveries of scenario_s15_01, then the coffee_break (no delivery live; break_time from 307, the tick the last delivery's terminal fact first holds), its own timeline: break_time from 307 to the run's end. Purpose: P9, the coffee break with no delivery live, inside break_time."
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
                coffee_break("coffee_machine_0"),
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
