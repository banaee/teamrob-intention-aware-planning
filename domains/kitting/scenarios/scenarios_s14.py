# domains/kitting/scenarios/scenarios_s14.py
"""
Kitting scenarios on env_setup_14: T-K part 1's tests of context knowledge, round 1, the round without context
knowledge (the IRB; analysis/kitting/irb/tk1/README.md). One module per setup. The room is env_layout_16, the dense room;
the shift env_setup_14: item_0 on shelf_0, item_1 on shelf_1, item_2 on shelf_2, all designated to kitting_table_0.
The recognizer is tested in isolation: the robot at (-400, 400) with an empty task pool, observing only. The human
starts at the kitting table, is assigned every delivery (never in an order), delivers them in one order, the same
in every scenario of this module (item_0, item_2, item_1), and ends every script with the exit
walk to corner_NE from the table. The only thing that varies is where one foreseeable task is placed: between
tasks (after the first, second or third delivery, so that a delivery stays live) or inside the second delivery
between its actions (the events at move_to occurrence 0, pick_up, move_to occurrence 1). _01 is the control,
the deliveries alone. No other deviation. Prior on (assignment knowledge); context knowledge is not built. The
durations are the schemas'. Every run stays below step 500 (TODO-66's context weight; the set's README).
T-K part 1, step 4 (4 October 2026; analysis/kitting/irb/tk2/README.md): the setup states the default timeline of
context facts, break_time from 178 to 300 (every scenario of round 1 without an A/C activation
meets it); each script with an A/C activation states its own, room_warm from 150 to the
run's end (Hadi's 3A). From _12 on, the scenarios
run a script of round 1 (or a new one) under a timeline of their own (Hadi's 3B to 3F, ccode's P1 to P9), with
context knowledge on; their off side is round 1's run of the same script.
"""

from shared.types import AgentConfig, ScenarioConfig, Script, Timeline
from domains.kitting.actions import move_to, pick_up
from domains.kitting.facts import BREAK_TIME, ROOM_WARM
from domains.kitting.script import deliver_item, coffee_break, go_to, ac_activation, window


_TK1 = (
    "T-K part 1, round 1 (no context knowledge), IRB on env_layout_16: the recognizer in isolation, against "
    "expectations derived from the records before the run (analysis/kitting/irb/tk1/). The robot at (-400, 400) "
    "with an empty task pool, observing only; the human starts at the kitting table, is assigned "
    "deliver_item(item_0), deliver_item(item_1), deliver_item(item_2) and delivers them in the order "
    "item_0, item_2, item_1, then the exit walk to corner_NE. Prior on. "
)

_TK2 = (
    "T-K part 1, step 4 (context knowledge on), IRB on env_layout_16: the recognizer in isolation, against expectations "
    "derived before the run (analysis/kitting/irb/tk2/). "
)

scenario_s14_01 = ScenarioConfig(
    id="scenario_s14_01",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    description=_TK1 + (
        "scenario_s14_01, deliveries alone, the control. Purpose: the control: the deliveries alone, no foreseeable task. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_02 = ScenarioConfig(
    id="scenario_s14_02",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    description=_TK1 + (
        "scenario_s14_02, coffee_break after the first delivery. Purpose: coffee_break between tasks, after the first delivery (item_0); deliveries of item_2, item_1 still live. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_03 = ScenarioConfig(
    id="scenario_s14_03",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    description=_TK1 + (
        "scenario_s14_03, coffee_break after the second delivery. Purpose: coffee_break between tasks, after the second delivery (item_2); deliveries of item_1 still live. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_04 = ScenarioConfig(
    id="scenario_s14_04",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    description=_TK1 + (
        "scenario_s14_04, coffee_break inside the second delivery, after the walk to the shelf, before the grasp. Purpose: coffee_break inside the second delivery (item_2), after the walk to the shelf, before the grasp; the delivery resumes after it. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_05 = ScenarioConfig(
    id="scenario_s14_05",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    description=_TK1 + (
        "scenario_s14_05, coffee_break inside the second delivery, after the grasp, the item in hand. Purpose: coffee_break inside the second delivery (item_2), after the grasp, the item in hand; the delivery resumes after it. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_06 = ScenarioConfig(
    id="scenario_s14_06",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    description=_TK1 + (
        "scenario_s14_06, coffee_break inside the second delivery, after the carry to the table, before the place, the item in hand. Purpose: coffee_break inside the second delivery (item_2), after the carry to the table, before the place, the item in hand; the delivery resumes after it. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=1),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_07 = ScenarioConfig(
    id="scenario_s14_07",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    timeline=Timeline((window(ROOM_WARM, 150),)),
    description=_TK1 + (
        "scenario_s14_07, ac_activation after the first delivery. Purpose: ac_activation between tasks, after the first delivery (item_0); deliveries of item_2, item_1 still live. Modelled behaviour only, besides the exit walk. Its own timeline (T-K part 1, step 4, Hadi's 3A): room_warm from 150 to the run's end, no break_time."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_08 = ScenarioConfig(
    id="scenario_s14_08",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    timeline=Timeline((window(ROOM_WARM, 150),)),
    description=_TK1 + (
        "scenario_s14_08, ac_activation after the second delivery. Purpose: ac_activation between tasks, after the second delivery (item_2); deliveries of item_1 still live. Modelled behaviour only, besides the exit walk. Its own timeline (T-K part 1, step 4, Hadi's 3A): room_warm from 150 to the run's end, no break_time."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_09 = ScenarioConfig(
    id="scenario_s14_09",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    timeline=Timeline((window(ROOM_WARM, 150),)),
    description=_TK1 + (
        "scenario_s14_09, ac_activation inside the second delivery, after the walk to the shelf, before the grasp. Purpose: ac_activation inside the second delivery (item_2), after the walk to the shelf, before the grasp; the delivery resumes after it. Modelled behaviour only, besides the exit walk. Its own timeline (T-K part 1, step 4, Hadi's 3A): room_warm from 150 to the run's end, no break_time."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0").at(move_to, ac_activation("ac_switch_0"), occurrence=0),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_10 = ScenarioConfig(
    id="scenario_s14_10",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    timeline=Timeline((window(ROOM_WARM, 150),)),
    description=_TK1 + (
        "scenario_s14_10, ac_activation inside the second delivery, after the grasp, the item in hand. Purpose: ac_activation inside the second delivery (item_2), after the grasp, the item in hand; the delivery resumes after it. Modelled behaviour only, besides the exit walk. Its own timeline (T-K part 1, step 4, Hadi's 3A): room_warm from 150 to the run's end, no break_time."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0").at(pick_up, ac_activation("ac_switch_0")),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_11 = ScenarioConfig(
    id="scenario_s14_11",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    timeline=Timeline((window(ROOM_WARM, 150),)),
    description=_TK1 + (
        "scenario_s14_11, ac_activation inside the second delivery, after the carry to the table, before the place, the item in hand. Purpose: ac_activation inside the second delivery (item_2), after the carry to the table, before the place, the item in hand; the delivery resumes after it. Modelled behaviour only, besides the exit walk. Its own timeline (T-K part 1, step 4, Hadi's 3A): room_warm from 150 to the run's end, no break_time."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0").at(move_to, ac_activation("ac_switch_0"), occurrence=1),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_12 = ScenarioConfig(
    id="scenario_s14_12",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    timeline=Timeline((window(BREAK_TIME, 70, 250),)),
    description=_TK2 + (
        "scenario_s14_12, scenario_s14_02's script, its own timeline: break_time from 70 to 250. Purpose: 3B, the window's edge before the human leaves for the break (during the first delivery)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_13 = ScenarioConfig(
    id="scenario_s14_13",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    timeline=Timeline((window(BREAK_TIME, 110, 250),)),
    description=_TK2 + (
        "scenario_s14_13, scenario_s14_02's script, its own timeline: break_time from 110 to 250. Purpose: 3B, the window's edge during the walk to the coffee machine."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_14 = ScenarioConfig(
    id="scenario_s14_14",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    timeline=Timeline((window(BREAK_TIME, 150, 250),)),
    description=_TK2 + (
        "scenario_s14_14, scenario_s14_02's script, its own timeline: break_time from 150 to 250. Purpose: 3B, the window's edge during the wait at the coffee machine."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_15 = ScenarioConfig(
    id="scenario_s14_15",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    timeline=Timeline((window(ROOM_WARM, 70),)),
    description=_TK2 + (
        "scenario_s14_15, scenario_s14_07's script, its own timeline: room_warm from 70 to the run's end. Purpose: 3C, room_warm's edge before the human leaves for the A/C switch (during the first delivery)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_16 = ScenarioConfig(
    id="scenario_s14_16",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    timeline=Timeline((window(ROOM_WARM, 110),)),
    description=_TK2 + (
        "scenario_s14_16, scenario_s14_07's script, its own timeline: room_warm from 110 to the run's end. Purpose: 3C, room_warm's edge during the walk to the A/C switch."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_17 = ScenarioConfig(
    id="scenario_s14_17",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    timeline=Timeline((window(ROOM_WARM, 0, 110),)),
    description=_TK2 + (
        "scenario_s14_17, scenario_s14_07's script, its own timeline: room_warm from 0 to 110. Purpose: 3C, room_warm from the start, its end during the walk to the A/C switch."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_18 = ScenarioConfig(
    id="scenario_s14_18",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    timeline=Timeline((window(BREAK_TIME, 60, 250),)),
    description=_TK2 + (
        "scenario_s14_18, scenario_s14_03's script, its own timeline: break_time from 60 to 250. Purpose: 3D, the window opens during the first delivery, the second lies inside it, the break comes late in it; the window closes during the wait."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_19 = ScenarioConfig(
    id="scenario_s14_19",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    timeline=Timeline(()),
    description=_TK2 + (
        "scenario_s14_19, scenario_s14_03's script, its own timeline stated empty: no timeline fact holds. Purpose: 3E, no timeline fact, one delivery live, then the break: the early admission and its retraction."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_20 = ScenarioConfig(
    id="scenario_s14_20",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    timeline=Timeline((window(BREAK_TIME, 0),)),
    description=_TK2 + (
        "scenario_s14_20, scenario_s14_01's script, its own timeline: break_time from 0 to the run's end. Purpose: P3, every delivery against the raised coffee break in the dense room."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s14_21 = ScenarioConfig(
    id="scenario_s14_21",
    setup="env_setup_14",
    reference_layouts=["env_layout_16"],
    description=_TK2 + (
        "scenario_s14_21, scenario_s14_08's script, no timeline of its own: the setup's default applies (break_time from 178 to 300). Purpose: P5, the A/C activation while its cluster neighbour, the coffee break, is raised and the A/C is ordinary."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 450),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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
