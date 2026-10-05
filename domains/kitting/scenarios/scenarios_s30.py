# domains/kitting/scenarios/scenarios_s30.py
"""
Kitting scenarios on env_setup_30: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_20; the shift
env_setup_30: the near shift: the west shelves to the north table kitting_table_0, the east shelves to the south table kitting_table_1; shelf_2 and shelf_4 hold two parts each.
Each script stands here in two forms: the idle robot (an empty task pool, observing only; the recognition test-bed) and
the working robot (the planning test-bed); each form once with no timeline (the setup states none) and, where the
script holds what it needs, as copies with a timeline of their own (AM40): "accord", the raising fact over the ticks
where the human does the foreseeable task; "through", break_time over a delivery the human works through; "through_rw",
room_warm over a delivery (deliveries-only scripts in a room with an A/C switch). The windows are placed from the
instrument's replay of the script (analysis/instruments/irb/trajectory.py), before any run, half-open in ticks (AM46).
Every new script ends with the exit walk (docs/assumptions.md 1.1); the human is assigned every delivery it performs
and any it never starts. The durations are the schemas'. Each description states the script's purpose, the aspects it
varies and the expectation in kind, written before the runs.
"""

from shared.types import AgentConfig, ScenarioConfig, Script, Timeline, drop
from domains.kitting.actions import move_to, pick_up
from domains.kitting.facts import BREAK_TIME, ROOM_WARM
from domains.kitting.script import deliver_item, coffee_break, ac_activation, go_to, stand, go_to_and_stand, window

# ---- script 096: deliveries only: two parts from one shelf to the north table
scenario_s30_01 = ScenarioConfig(
    id="scenario_s30_01",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_01: script 096 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: two parts from one shelf to the north table. Aspects: deliveries: two "
        "from shelf_2; robot: east, two parts from one shelf, apart. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, 100),
            scheduled_tasks=Script([
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_77", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_77", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_02 = ScenarioConfig(
    id="scenario_s30_02",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_02: script 096 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: two parts from one shelf to the north table. Aspects: deliveries: two "
        "from shelf_2; robot: east, two parts from one shelf, apart. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior). working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, 100),
            scheduled_tasks=Script([
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_77", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_77", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, -100),
            assigned_tasks=[
                deliver_item("item_74", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_03 = ScenarioConfig(
    id="scenario_s30_03",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 46),)),
    description=(
        "scenario_s30_03: script 096 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 46. Purpose: deliveries only: two parts "
        "from one shelf to the north table. Aspects: deliveries: two from shelf_2; robot: east, two parts "
        "from one shelf, apart. Expectation: the delivery under break_time admitted later than with no fact, "
        "near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, 100),
            scheduled_tasks=Script([
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_77", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_77", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_04 = ScenarioConfig(
    id="scenario_s30_04",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 46),)),
    description=(
        "scenario_s30_04: script 096 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 46. Purpose: deliveries only: two parts "
        "from one shelf to the north table. Aspects: deliveries: two from shelf_2; robot: east, two parts "
        "from one shelf, apart. Expectation: the delivery under break_time admitted later than with no fact, "
        "near off. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, 100),
            scheduled_tasks=Script([
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_77", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_77", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, -100),
            assigned_tasks=[
                deliver_item("item_74", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 097: deliveries only: four, alternating tables
scenario_s30_05 = ScenarioConfig(
    id="scenario_s30_05",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_05: script 097 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: four, alternating tables. Aspects: deliveries: four, alternating; start: "
        "by the door; robot: north-west start, crossing. Expectation: on against off: each delivery admitted "
        "earlier or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, -300),
            scheduled_tasks=Script([
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_76", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_76", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_06 = ScenarioConfig(
    id="scenario_s30_06",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_06: script 097 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: four, alternating tables. Aspects: deliveries: four, alternating; start: "
        "by the door; robot: north-west start, crossing. Expectation: on against off: each delivery admitted "
        "earlier or equal (the assigned tasks share most of the prior). working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, -300),
            scheduled_tasks=Script([
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_76", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_76", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, 300),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_74", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_07 = ScenarioConfig(
    id="scenario_s30_07",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 97),)),
    description=(
        "scenario_s30_07: script 097 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 97. Purpose: deliveries only: four, "
        "alternating tables. Aspects: deliveries: four, alternating; start: by the door; robot: north-west "
        "start, crossing. Expectation: the delivery under break_time admitted later than with no fact, near "
        "off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, -300),
            scheduled_tasks=Script([
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_76", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_76", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_08 = ScenarioConfig(
    id="scenario_s30_08",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 97),)),
    description=(
        "scenario_s30_08: script 097 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 97. Purpose: deliveries only: four, "
        "alternating tables. Aspects: deliveries: four, alternating; start: by the door; robot: north-west "
        "start, crossing. Expectation: the delivery under break_time admitted later than with no fact, near "
        "off. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, -300),
            scheduled_tasks=Script([
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_76", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_76", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, 300),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_74", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 098: a coffee break at the start, the machine along the wall from kitting_table_0
scenario_s30_09 = ScenarioConfig(
    id="scenario_s30_09",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_09: script 098 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the start, the machine along the wall from kitting_table_0. Aspects: "
        "foreseeable: at the start; start: kitting_table_0, first walk toward the machine; deliveries: two "
        "to kitting_table_1. Expectation: on against off: each delivery admitted earlier or equal (the "
        "assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-450, 350),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_10 = ScenarioConfig(
    id="scenario_s30_10",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_10: script 098 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the start, the machine along the wall from kitting_table_0. Aspects: "
        "foreseeable: at the start; start: kitting_table_0, first walk toward the machine; deliveries: two "
        "to kitting_table_1. Expectation: on against off: each delivery admitted earlier or equal (the "
        "assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength). working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-450, 350),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, -300),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_76", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_11 = ScenarioConfig(
    id="scenario_s30_11",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 60),)),
    description=(
        "scenario_s30_11: script 098 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 0 to 60. Purpose: a coffee break at the start, the "
        "machine along the wall from kitting_table_0. Aspects: foreseeable: at the start; start: "
        "kitting_table_0, first walk toward the machine; deliveries: two to kitting_table_1. Expectation: "
        "the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a "
        "delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-450, 350),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_12 = ScenarioConfig(
    id="scenario_s30_12",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 60),)),
    description=(
        "scenario_s30_12: script 098 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 0 to 60. Purpose: a coffee break at the start, the "
        "machine along the wall from kitting_table_0. Aspects: foreseeable: at the start; start: "
        "kitting_table_0, first walk toward the machine; deliveries: two to kitting_table_1. Expectation: "
        "the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a "
        "delivery inside a window admitted later than with no fact. working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-450, 350),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, -300),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_76", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_13 = ScenarioConfig(
    id="scenario_s30_13",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 60, 140),)),
    description=(
        "scenario_s30_13: script 098 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 60 to 140. Purpose: a coffee break at the "
        "start, the machine along the wall from kitting_table_0. Aspects: foreseeable: at the start; start: "
        "kitting_table_0, first walk toward the machine; deliveries: two to kitting_table_1. Expectation: "
        "the delivery under break_time admitted later than with no fact, near off; a delivery whose walk "
        "heads toward the machine may lose its admission to the raised coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-450, 350),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_14 = ScenarioConfig(
    id="scenario_s30_14",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 60, 140),)),
    description=(
        "scenario_s30_14: script 098 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 60 to 140. Purpose: a coffee break at the "
        "start, the machine along the wall from kitting_table_0. Aspects: foreseeable: at the start; start: "
        "kitting_table_0, first walk toward the machine; deliveries: two to kitting_table_1. Expectation: "
        "the delivery under break_time admitted later than with no fact, near off; a delivery whose walk "
        "heads toward the machine may lose its admission to the raised coffee break. working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it; under the window the delivery's admission and the robot's decision "
        "on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-450, 350),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, -300),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_76", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 099: a coffee break between deliveries
scenario_s30_15 = ScenarioConfig(
    id="scenario_s30_15",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_15: script 099 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break between deliveries. Aspects: foreseeable: between deliveries; start: "
        "south-west corner. Expectation: on against off: each delivery admitted earlier or equal (the "
        "assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -450),
            scheduled_tasks=Script([
                deliver_item("item_71", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_75", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_75", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_16 = ScenarioConfig(
    id="scenario_s30_16",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_16: script 099 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break between deliveries. Aspects: foreseeable: between deliveries; start: "
        "south-west corner. Expectation: on against off: each delivery admitted earlier or equal (the "
        "assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength). working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -450),
            scheduled_tasks=Script([
                deliver_item("item_71", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_75", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_75", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, 200),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_17 = ScenarioConfig(
    id="scenario_s30_17",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 56, 119),)),
    description=(
        "scenario_s30_17: script 099 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 56 to 119. Purpose: a coffee break between deliveries. "
        "Aspects: foreseeable: between deliveries; start: south-west corner. Expectation: the coffee break "
        "(raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a "
        "window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -450),
            scheduled_tasks=Script([
                deliver_item("item_71", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_75", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_75", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_18 = ScenarioConfig(
    id="scenario_s30_18",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 56, 119),)),
    description=(
        "scenario_s30_18: script 099 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 56 to 119. Purpose: a coffee break between "
        "deliveries. Aspects: foreseeable: between deliveries; start: south-west corner. Expectation: the "
        "coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery "
        "inside a window admitted later than with no fact. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -450),
            scheduled_tasks=Script([
                deliver_item("item_71", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_75", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_75", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, 200),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_19 = ScenarioConfig(
    id="scenario_s30_19",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 56),)),
    description=(
        "scenario_s30_19: script 099 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 56. Purpose: a coffee break between "
        "deliveries. Aspects: foreseeable: between deliveries; start: south-west corner. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -450),
            scheduled_tasks=Script([
                deliver_item("item_71", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_75", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_75", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_20 = ScenarioConfig(
    id="scenario_s30_20",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 56),)),
    description=(
        "scenario_s30_20: script 099 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 56. Purpose: a coffee break between "
        "deliveries. Aspects: foreseeable: between deliveries; start: south-west corner. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off. working robot: the decisions "
        "as off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it; under the window the delivery's admission and the robot's decision on it "
        "later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -450),
            scheduled_tasks=Script([
                deliver_item("item_71", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_75", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_75", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, 200),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 100: a coffee break inside a south-west delivery after the grasp
scenario_s30_21 = ScenarioConfig(
    id="scenario_s30_21",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_21: script 100 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a south-west delivery after the grasp. Aspects: foreseeable: inside "
        "a delivery, after the grasp; robot: east, apart. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted "
        "later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -100),
            scheduled_tasks=Script([
                deliver_item("item_76", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_72", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_76", table="kitting_table_0"),
                deliver_item("item_72", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_22 = ScenarioConfig(
    id="scenario_s30_22",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_22: script 100 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a south-west delivery after the grasp. Aspects: foreseeable: inside "
        "a delivery, after the grasp; robot: east, apart. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted "
        "later than off (ordinary strength). working robot: the decisions as off where no admission moves; "
        "an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -100),
            scheduled_tasks=Script([
                deliver_item("item_76", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_72", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_76", table="kitting_table_0"),
                deliver_item("item_72", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(800, -300),
            assigned_tasks=[
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_23 = ScenarioConfig(
    id="scenario_s30_23",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 25, 113),)),
    description=(
        "scenario_s30_23: script 100 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 25 to 113. Purpose: a coffee break inside a south-west "
        "delivery after the grasp. Aspects: foreseeable: inside a delivery, after the grasp; robot: east, "
        "apart. Expectation: the coffee break (raised by break_time) admitted earlier than off and than on "
        "with no fact; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -100),
            scheduled_tasks=Script([
                deliver_item("item_76", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_72", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_76", table="kitting_table_0"),
                deliver_item("item_72", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_24 = ScenarioConfig(
    id="scenario_s30_24",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 25, 113),)),
    description=(
        "scenario_s30_24: script 100 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 25 to 113. Purpose: a coffee break inside a "
        "south-west delivery after the grasp. Aspects: foreseeable: inside a delivery, after the grasp; "
        "robot: east, apart. Expectation: the coffee break (raised by break_time) admitted earlier than off "
        "and than on with no fact; a delivery inside a window admitted later than with no fact. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; the coffee break admitted earlier, the robot's decision "
        "against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -100),
            scheduled_tasks=Script([
                deliver_item("item_76", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_72", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_76", table="kitting_table_0"),
                deliver_item("item_72", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(800, -300),
            assigned_tasks=[
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_25 = ScenarioConfig(
    id="scenario_s30_25",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 146, 194),)),
    description=(
        "scenario_s30_25: script 100 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 146 to 194. Purpose: a coffee break inside a "
        "south-west delivery after the grasp. Aspects: foreseeable: inside a delivery, after the grasp; "
        "robot: east, apart. Expectation: the delivery under break_time admitted later than with no fact, "
        "near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -100),
            scheduled_tasks=Script([
                deliver_item("item_76", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_72", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_76", table="kitting_table_0"),
                deliver_item("item_72", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_26 = ScenarioConfig(
    id="scenario_s30_26",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 146, 194),)),
    description=(
        "scenario_s30_26: script 100 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 146 to 194. Purpose: a coffee break inside a "
        "south-west delivery after the grasp. Aspects: foreseeable: inside a delivery, after the grasp; "
        "robot: east, apart. Expectation: the delivery under break_time admitted later than with no fact, "
        "near off. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -100),
            scheduled_tasks=Script([
                deliver_item("item_76", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_72", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_76", table="kitting_table_0"),
                deliver_item("item_72", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(800, -300),
            assigned_tasks=[
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_74", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 101: two coffee breaks around three deliveries, at the start and at the end
scenario_s30_27 = ScenarioConfig(
    id="scenario_s30_27",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_27: script 101 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: two coffee breaks around three deliveries, at the start and at the end. Aspects: "
        "foreseeable: two, at the start and at the end; deliveries: three, both tables. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "a coffee break admitted later than off (ordinary strength); the second under its recency fact "
        "(suppressed), later still."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_28 = ScenarioConfig(
    id="scenario_s30_28",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_28: script 101 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: two coffee breaks around three deliveries, at the start and at the end. Aspects: "
        "foreseeable: two, at the start and at the end; deliveries: three, both tables. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "a coffee break admitted later than off (ordinary strength); the second under its recency fact "
        "(suppressed), later still. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, -200),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_76", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_29 = ScenarioConfig(
    id="scenario_s30_29",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 45), window(BREAK_TIME, 294, 374),)),
    description=(
        "scenario_s30_29: script 101 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 0 to 45, break_time from 294 to 374. Purpose: two coffee "
        "breaks around three deliveries, at the start and at the end. Aspects: foreseeable: two, at the "
        "start and at the end; deliveries: three, both tables. Expectation: the coffee break (raised by "
        "break_time) admitted earlier than off and than on with no fact; the second one suppressed by its "
        "recency fact, the window gives it nothing; a delivery inside a window admitted later than with no "
        "fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_30 = ScenarioConfig(
    id="scenario_s30_30",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 45), window(BREAK_TIME, 294, 374),)),
    description=(
        "scenario_s30_30: script 101 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 0 to 45, break_time from 294 to 374. Purpose: two "
        "coffee breaks around three deliveries, at the start and at the end. Aspects: foreseeable: two, at "
        "the start and at the end; deliveries: three, both tables. Expectation: the coffee break (raised by "
        "break_time) admitted earlier than off and than on with no fact; the second one suppressed by its "
        "recency fact, the window gives it nothing; a delivery inside a window admitted later than with no "
        "fact. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; the coffee break admitted earlier, the "
        "robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, -200),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_76", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_31 = ScenarioConfig(
    id="scenario_s30_31",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 45, 123),)),
    description=(
        "scenario_s30_31: script 101 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 45 to 123. Purpose: two coffee breaks around "
        "three deliveries, at the start and at the end. Aspects: foreseeable: two, at the start and at the "
        "end; deliveries: three, both tables. Expectation: the delivery under break_time admitted later than "
        "with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_32 = ScenarioConfig(
    id="scenario_s30_32",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 45, 123),)),
    description=(
        "scenario_s30_32: script 101 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 45 to 123. Purpose: two coffee breaks around "
        "three deliveries, at the start and at the end. Aspects: foreseeable: two, at the start and at the "
        "end; deliveries: three, both tables. Expectation: the delivery under break_time admitted later than "
        "with no fact, near off. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; under the window the "
        "delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_78", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, -200),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_76", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 102: unmodelled alone: a long stand, 60 ticks, at kitting_table_1
scenario_s30_33 = ScenarioConfig(
    id="scenario_s30_33",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_33: script 102 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a long stand, 60 ticks, at kitting_table_1. Aspects: unmodelled: a stand "
        "(60 ticks), between deliveries. Expectation: on against off: each delivery admitted earlier or "
        "equal (the assigned tasks share most of the prior); no admission during the stand or the walk "
        "elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, 200),
            scheduled_tasks=Script([
                deliver_item("item_74", table="kitting_table_1"),
                stand("PT120S"),
                deliver_item("item_75", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_74", table="kitting_table_1"),
                deliver_item("item_75", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_34 = ScenarioConfig(
    id="scenario_s30_34",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_34: script 102 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a long stand, 60 ticks, at kitting_table_1. Aspects: unmodelled: a stand "
        "(60 ticks), between deliveries. Expectation: on against off: each delivery admitted earlier or "
        "equal (the assigned tasks share most of the prior); no admission during the stand or the walk "
        "elsewhere, except a hypothesis whose target lies on the walk. working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, 200),
            scheduled_tasks=Script([
                deliver_item("item_74", table="kitting_table_1"),
                stand("PT120S"),
                deliver_item("item_75", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_74", table="kitting_table_1"),
                deliver_item("item_75", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, -100),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_72", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_35 = ScenarioConfig(
    id="scenario_s30_35",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 48),)),
    description=(
        "scenario_s30_35: script 102 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 48. Purpose: unmodelled alone: a long "
        "stand, 60 ticks, at kitting_table_1. Aspects: unmodelled: a stand (60 ticks), between deliveries. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off; no admission "
        "during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, 200),
            scheduled_tasks=Script([
                deliver_item("item_74", table="kitting_table_1"),
                stand("PT120S"),
                deliver_item("item_75", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_74", table="kitting_table_1"),
                deliver_item("item_75", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_36 = ScenarioConfig(
    id="scenario_s30_36",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 48),)),
    description=(
        "scenario_s30_36: script 102 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 48. Purpose: unmodelled alone: a long "
        "stand, 60 ticks, at kitting_table_1. Aspects: unmodelled: a stand (60 ticks), between deliveries. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off; no admission "
        "during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; under the window the delivery's admission and the robot's "
        "decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, 200),
            scheduled_tasks=Script([
                deliver_item("item_74", table="kitting_table_1"),
                stand("PT120S"),
                deliver_item("item_75", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_74", table="kitting_table_1"),
                deliver_item("item_75", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, -100),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_72", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 103: unmodelled alone: a walk to corner_SW and a stand of 40 ticks between deliveries
scenario_s30_37 = ScenarioConfig(
    id="scenario_s30_37",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_37: script 103 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a walk to corner_SW and a stand of 40 ticks between deliveries. Aspects: "
        "unmodelled: a walk elsewhere with a stand (40 ticks). Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); no admission during the "
        "stand or the walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 0),
            scheduled_tasks=Script([
                deliver_item("item_71", table="kitting_table_0"),
                go_to_and_stand("corner_SW", "PT80S"),
                deliver_item("item_76", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_76", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_38 = ScenarioConfig(
    id="scenario_s30_38",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_38: script 103 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a walk to corner_SW and a stand of 40 ticks between deliveries. Aspects: "
        "unmodelled: a walk elsewhere with a stand (40 ticks). Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); no admission during the "
        "stand or the walk elsewhere, except a hypothesis whose target lies on the walk. working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 0),
            scheduled_tasks=Script([
                deliver_item("item_71", table="kitting_table_0"),
                go_to_and_stand("corner_SW", "PT80S"),
                deliver_item("item_76", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_76", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, 100),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_75", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_39 = ScenarioConfig(
    id="scenario_s30_39",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 66),)),
    description=(
        "scenario_s30_39: script 103 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 66. Purpose: unmodelled alone: a walk "
        "to corner_SW and a stand of 40 ticks between deliveries. Aspects: unmodelled: a walk elsewhere with "
        "a stand (40 ticks). Expectation: the delivery under break_time admitted later than with no fact, "
        "near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target "
        "lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 0),
            scheduled_tasks=Script([
                deliver_item("item_71", table="kitting_table_0"),
                go_to_and_stand("corner_SW", "PT80S"),
                deliver_item("item_76", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_76", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_40 = ScenarioConfig(
    id="scenario_s30_40",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 66),)),
    description=(
        "scenario_s30_40: script 103 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 66. Purpose: unmodelled alone: a walk "
        "to corner_SW and a stand of 40 ticks between deliveries. Aspects: unmodelled: a walk elsewhere with "
        "a stand (40 ticks). Expectation: the delivery under break_time admitted later than with no fact, "
        "near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target "
        "lies on the walk. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; under the window the "
        "delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 0),
            scheduled_tasks=Script([
                deliver_item("item_71", table="kitting_table_0"),
                go_to_and_stand("corner_SW", "PT80S"),
                deliver_item("item_76", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_71", table="kitting_table_0"),
                deliver_item("item_76", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, 100),
            assigned_tasks=[
                deliver_item("item_73", table="kitting_table_1"),
                deliver_item("item_75", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 104: unmodelled with a foreseeable task: a delivery abandoned after the grasp, a coffee break with the part in hand; the second delivery never started
scenario_s30_41 = ScenarioConfig(
    id="scenario_s30_41",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_41: script 104 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery abandoned after the grasp, a coffee break "
        "with the part in hand; the second delivery never started. Aspects: unmodelled: an abandoned "
        "delivery (after the grasp), a never-started delivery; foreseeable: after them. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "a coffee break admitted later than off (ordinary strength); the never-started delivery never "
        "admitted (no observation warrant); the abandoned delivery admitted while the human walks to it, "
        "then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, -100),
            scheduled_tasks=Script([
                deliver_item("item_78", table="kitting_table_1").at(pick_up, drop),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_78", table="kitting_table_1"),
                deliver_item("item_73", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_42 = ScenarioConfig(
    id="scenario_s30_42",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_42: script 104 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery abandoned after the grasp, a coffee break "
        "with the part in hand; the second delivery never started. Aspects: unmodelled: an abandoned "
        "delivery (after the grasp), a never-started delivery; foreseeable: after them. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "a coffee break admitted later than off (ordinary strength); the never-started delivery never "
        "admitted (no observation warrant); the abandoned delivery admitted while the human walks to it, "
        "then retracted as the evidence turns. working robot: the decisions as off where no admission moves; "
        "an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, -100),
            scheduled_tasks=Script([
                deliver_item("item_78", table="kitting_table_1").at(pick_up, drop),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_78", table="kitting_table_1"),
                deliver_item("item_73", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, 300),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_77", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_43 = ScenarioConfig(
    id="scenario_s30_43",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 9, 88),)),
    description=(
        "scenario_s30_43: script 104 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 9 to 88. Purpose: unmodelled with a foreseeable task: a "
        "delivery abandoned after the grasp, a coffee break with the part in hand; the second delivery never "
        "started. Aspects: unmodelled: an abandoned delivery (after the grasp), a never-started delivery; "
        "foreseeable: after them. Expectation: the coffee break (raised by break_time) admitted earlier than "
        "off and than on with no fact; a delivery inside a window admitted later than with no fact; the "
        "never-started delivery never admitted (no observation warrant); the abandoned delivery admitted "
        "while the human walks to it, then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, -100),
            scheduled_tasks=Script([
                deliver_item("item_78", table="kitting_table_1").at(pick_up, drop),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_78", table="kitting_table_1"),
                deliver_item("item_73", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_44 = ScenarioConfig(
    id="scenario_s30_44",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 9, 88),)),
    description=(
        "scenario_s30_44: script 104 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 9 to 88. Purpose: unmodelled with a foreseeable "
        "task: a delivery abandoned after the grasp, a coffee break with the part in hand; the second "
        "delivery never started. Aspects: unmodelled: an abandoned delivery (after the grasp), a "
        "never-started delivery; foreseeable: after them. Expectation: the coffee break (raised by "
        "break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted "
        "later than with no fact; the never-started delivery never admitted (no observation warrant); the "
        "abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it; the coffee break admitted earlier, the robot's "
        "decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, -100),
            scheduled_tasks=Script([
                deliver_item("item_78", table="kitting_table_1").at(pick_up, drop),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_78", table="kitting_table_1"),
                deliver_item("item_73", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, 300),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_77", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 105: unmodelled with a foreseeable task: a delivery to the other table (item_75 to kitting_table_0), a coffee break at the end
scenario_s30_45 = ScenarioConfig(
    id="scenario_s30_45",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_45: script 105 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery to the other table (item_75 to "
        "kitting_table_0), a coffee break at the end. Aspects: unmodelled: a delivery to the other table; "
        "foreseeable: at the end; robot: to kitting_table_0, where the human delivers twice. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "a coffee break admitted later than off (ordinary strength); the delivery to the other table: "
        "admitted on the walk to the shelf, then its carry unexplained; no other hypothesis admitted there."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -450),
            scheduled_tasks=Script([
                deliver_item("item_75", table="kitting_table_0"),
                deliver_item("item_71", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_71", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_46 = ScenarioConfig(
    id="scenario_s30_46",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s30_46: script 105 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery to the other table (item_75 to "
        "kitting_table_0), a coffee break at the end. Aspects: unmodelled: a delivery to the other table; "
        "foreseeable: at the end; robot: to kitting_table_0, where the human delivers twice. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "a coffee break admitted later than off (ordinary strength); the delivery to the other table: "
        "admitted on the walk to the shelf, then its carry unexplained; no other hypothesis admitted there. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -450),
            scheduled_tasks=Script([
                deliver_item("item_75", table="kitting_table_0"),
                deliver_item("item_71", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_71", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, -300),
            assigned_tasks=[
                deliver_item("item_76", table="kitting_table_0"),
                deliver_item("item_72", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_47 = ScenarioConfig(
    id="scenario_s30_47",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 188, 251),)),
    description=(
        "scenario_s30_47: script 105 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 188 to 251. Purpose: unmodelled with a foreseeable task: "
        "a delivery to the other table (item_75 to kitting_table_0), a coffee break at the end. Aspects: "
        "unmodelled: a delivery to the other table; foreseeable: at the end; robot: to kitting_table_0, "
        "where the human delivers twice. Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; a delivery inside a window admitted later than with no "
        "fact; the delivery to the other table: admitted on the walk to the shelf, then its carry "
        "unexplained; no other hypothesis admitted there."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -450),
            scheduled_tasks=Script([
                deliver_item("item_75", table="kitting_table_0"),
                deliver_item("item_71", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_71", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_48 = ScenarioConfig(
    id="scenario_s30_48",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 188, 251),)),
    description=(
        "scenario_s30_48: script 105 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 188 to 251. Purpose: unmodelled with a foreseeable "
        "task: a delivery to the other table (item_75 to kitting_table_0), a coffee break at the end. "
        "Aspects: unmodelled: a delivery to the other table; foreseeable: at the end; robot: to "
        "kitting_table_0, where the human delivers twice. Expectation: the coffee break (raised by "
        "break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted "
        "later than with no fact; the delivery to the other table: admitted on the walk to the shelf, then "
        "its carry unexplained; no other hypothesis admitted there. working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -450),
            scheduled_tasks=Script([
                deliver_item("item_75", table="kitting_table_0"),
                deliver_item("item_71", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_71", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, -300),
            assigned_tasks=[
                deliver_item("item_76", table="kitting_table_0"),
                deliver_item("item_72", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_49 = ScenarioConfig(
    id="scenario_s30_49",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 93, 188),)),
    description=(
        "scenario_s30_49: script 105 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 93 to 188. Purpose: unmodelled with a "
        "foreseeable task: a delivery to the other table (item_75 to kitting_table_0), a coffee break at the "
        "end. Aspects: unmodelled: a delivery to the other table; foreseeable: at the end; robot: to "
        "kitting_table_0, where the human delivers twice. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off; the delivery to the other table: admitted on the walk "
        "to the shelf, then its carry unexplained; no other hypothesis admitted there."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -450),
            scheduled_tasks=Script([
                deliver_item("item_75", table="kitting_table_0"),
                deliver_item("item_71", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_71", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 25),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s30_50 = ScenarioConfig(
    id="scenario_s30_50",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 93, 188),)),
    description=(
        "scenario_s30_50: script 105 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 93 to 188. Purpose: unmodelled with a "
        "foreseeable task: a delivery to the other table (item_75 to kitting_table_0), a coffee break at the "
        "end. Aspects: unmodelled: a delivery to the other table; foreseeable: at the end; robot: to "
        "kitting_table_0, where the human delivers twice. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off; the delivery to the other table: admitted on the walk "
        "to the shelf, then its carry unexplained; no other hypothesis admitted there. working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it; under the window the delivery's admission and the robot's decision "
        "on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -450),
            scheduled_tasks=Script([
                deliver_item("item_75", table="kitting_table_0"),
                deliver_item("item_71", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_75", table="kitting_table_1"),
                deliver_item("item_71", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, -300),
            assigned_tasks=[
                deliver_item("item_76", table="kitting_table_0"),
                deliver_item("item_72", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)


# T-F part 1, part 1b (5 October 2026): copies with a fact in force (analysis/kitting/tf1/make_copies.py; REPORT.md, "Part 1").
scenario_s30_51 = ScenarioConfig(
    id="scenario_s30_51",
    setup="env_setup_30",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 9),)),
    description=(
        "T-F part 1, part 1b: scenario_s30_42's copy with a fact in force, not in accord: break_time over ticks 0 to 9 (deliver_item(item_78,kitting_table_1)). "
        "Everything else is scenario_s30_42's (analysis/kitting/tf1/make_copies.py)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, -100),
            scheduled_tasks=Script([
                deliver_item("item_78", table="kitting_table_1").at(pick_up, drop),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_78", table="kitting_table_1"),
                deliver_item("item_73", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, 300),
            assigned_tasks=[
                deliver_item("item_72", table="kitting_table_0"),
                deliver_item("item_77", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

