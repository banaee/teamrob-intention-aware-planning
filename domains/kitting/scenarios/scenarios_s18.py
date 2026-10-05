# domains/kitting/scenarios/scenarios_s18.py
"""
Kitting scenarios on env_setup_18: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_02; the shift
env_setup_18: a second shift: the human's parts on the west and south shelves around the break corner (shelf_1 beside the coffee machine and the A/C switch), the robot's on the east and south-east shelves.
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

# ---- script 008: deliveries only, the first one's approach heading toward the break corner (shelf_1 behind the coffee machine and the A/C switch)
scenario_s18_01 = ScenarioConfig(
    id="scenario_s18_01",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s18_01: script 008 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only, the first one's approach heading toward the break corner (shelf_1 behind "
        "the coffee machine and the A/C switch). Aspects: deliveries: three, west and south; approach toward "
        "the machine and the switch; robot: east, apart. Expectation: on against off: each delivery admitted "
        "earlier or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_02 = ScenarioConfig(
    id="scenario_s18_02",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s18_02: script 008 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only, the first one's approach heading toward the break corner (shelf_1 behind "
        "the coffee machine and the A/C switch). Aspects: deliveries: three, west and south; approach toward "
        "the machine and the switch; robot: east, apart. Expectation: on against off: each delivery admitted "
        "earlier or equal (the assigned tasks share most of the prior). working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, 200),
            assigned_tasks=[
                deliver_item("item_14", table="kitting_table_0"),
                deliver_item("item_15", table="kitting_table_0"),
                deliver_item("item_16", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_03 = ScenarioConfig(
    id="scenario_s18_03",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 113),)),
    description=(
        "scenario_s18_03: script 008 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 113. Purpose: deliveries only, the "
        "first one's approach heading toward the break corner (shelf_1 behind the coffee machine and the A/C "
        "switch). Aspects: deliveries: three, west and south; approach toward the machine and the switch; "
        "robot: east, apart. Expectation: the delivery under break_time admitted later than with no fact, "
        "near off; a delivery whose walk heads toward the machine may lose its admission to the raised "
        "coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_04 = ScenarioConfig(
    id="scenario_s18_04",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 113),)),
    description=(
        "scenario_s18_04: script 008 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 113. Purpose: deliveries only, the "
        "first one's approach heading toward the break corner (shelf_1 behind the coffee machine and the A/C "
        "switch). Aspects: deliveries: three, west and south; approach toward the machine and the switch; "
        "robot: east, apart. Expectation: the delivery under break_time admitted later than with no fact, "
        "near off; a delivery whose walk heads toward the machine may lose its admission to the raised "
        "coffee break. working robot: the decisions as off where no admission moves; an earlier admission of "
        "a delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, 200),
            assigned_tasks=[
                deliver_item("item_14", table="kitting_table_0"),
                deliver_item("item_15", table="kitting_table_0"),
                deliver_item("item_16", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_05 = ScenarioConfig(
    id="scenario_s18_05",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(ROOM_WARM, 0, 113),)),
    description=(
        "scenario_s18_05: script 008 of step 5e, the idle robot, its own timeline, room_warm over a delivery "
        "(the human works through it): room_warm from 0 to 113. Purpose: deliveries only, the first one's "
        "approach heading toward the break corner (shelf_1 behind the coffee machine and the A/C switch). "
        "Aspects: deliveries: three, west and south; approach toward the machine and the switch; robot: "
        "east, apart. Expectation: the delivery under room_warm admitted later than with no fact, by less "
        "than under break_time (raised 0.5 against 2)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_06 = ScenarioConfig(
    id="scenario_s18_06",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(ROOM_WARM, 0, 113),)),
    description=(
        "scenario_s18_06: script 008 of step 5e, the working robot, its own timeline, room_warm over a "
        "delivery (the human works through it): room_warm from 0 to 113. Purpose: deliveries only, the first "
        "one's approach heading toward the break corner (shelf_1 behind the coffee machine and the A/C "
        "switch). Aspects: deliveries: three, west and south; approach toward the machine and the switch; "
        "robot: east, apart. Expectation: the delivery under room_warm admitted later than with no fact, by "
        "less than under break_time (raised 0.5 against 2). working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, 200),
            assigned_tasks=[
                deliver_item("item_14", table="kitting_table_0"),
                deliver_item("item_15", table="kitting_table_0"),
                deliver_item("item_16", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 009: a coffee break at the end, after two deliveries
scenario_s18_07 = ScenarioConfig(
    id="scenario_s18_07",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s18_07: script 009 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the end, after two deliveries. Aspects: foreseeable: at the end; start: "
        "west wall; robot: south-east start, east and south shelves. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, 200),
            scheduled_tasks=Script([
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_08 = ScenarioConfig(
    id="scenario_s18_08",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s18_08: script 009 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the end, after two deliveries. Aspects: foreseeable: at the end; start: "
        "west wall; robot: south-east start, east and south shelves. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength). working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, 200),
            scheduled_tasks=Script([
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -300),
            assigned_tasks=[
                deliver_item("item_16", table="kitting_table_0"),
                deliver_item("item_17", table="kitting_table_0"),
                deliver_item("item_15", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_09 = ScenarioConfig(
    id="scenario_s18_09",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 141, 219),)),
    description=(
        "scenario_s18_09: script 009 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 141 to 219. Purpose: a coffee break at the end, after "
        "two deliveries. Aspects: foreseeable: at the end; start: west wall; robot: south-east start, east "
        "and south shelves. Expectation: the coffee break (raised by break_time) admitted earlier than off "
        "and than on with no fact; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, 200),
            scheduled_tasks=Script([
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_10 = ScenarioConfig(
    id="scenario_s18_10",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 141, 219),)),
    description=(
        "scenario_s18_10: script 009 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 141 to 219. Purpose: a coffee break at the end, "
        "after two deliveries. Aspects: foreseeable: at the end; start: west wall; robot: south-east start, "
        "east and south shelves. Expectation: the coffee break (raised by break_time) admitted earlier than "
        "off and than on with no fact; a delivery inside a window admitted later than with no fact. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; the coffee break admitted earlier, the robot's decision "
        "against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, 200),
            scheduled_tasks=Script([
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -300),
            assigned_tasks=[
                deliver_item("item_16", table="kitting_table_0"),
                deliver_item("item_17", table="kitting_table_0"),
                deliver_item("item_15", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_11 = ScenarioConfig(
    id="scenario_s18_11",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 53),)),
    description=(
        "scenario_s18_11: script 009 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 53. Purpose: a coffee break at the end, "
        "after two deliveries. Aspects: foreseeable: at the end; start: west wall; robot: south-east start, "
        "east and south shelves. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, 200),
            scheduled_tasks=Script([
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_12 = ScenarioConfig(
    id="scenario_s18_12",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 53),)),
    description=(
        "scenario_s18_12: script 009 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 53. Purpose: a coffee break at the end, "
        "after two deliveries. Aspects: foreseeable: at the end; start: west wall; robot: south-east start, "
        "east and south shelves. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off. working robot: the decisions as off where no admission moves; an earlier admission "
        "of a delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, 200),
            scheduled_tasks=Script([
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -300),
            assigned_tasks=[
                deliver_item("item_16", table="kitting_table_0"),
                deliver_item("item_17", table="kitting_table_0"),
                deliver_item("item_15", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 010: a second coffee break soon after the first (its recency fact holding)
scenario_s18_13 = ScenarioConfig(
    id="scenario_s18_13",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s18_13: script 010 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a second coffee break soon after the first (its recency fact holding). Aspects: "
        "foreseeable: two coffee breaks, between and at the end; robot: north-east start, apart. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior); a coffee break admitted later than off (ordinary strength); the second under its "
        "recency fact (suppressed), later still."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, -100),
            scheduled_tasks=Script([
                deliver_item("item_11", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_12", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_14 = ScenarioConfig(
    id="scenario_s18_14",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s18_14: script 010 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a second coffee break soon after the first (its recency fact holding). Aspects: "
        "foreseeable: two coffee breaks, between and at the end; robot: north-east start, apart. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior); a coffee break admitted later than off (ordinary strength); the second under its "
        "recency fact (suppressed), later still. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, -100),
            scheduled_tasks=Script([
                deliver_item("item_11", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_12", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, 300),
            assigned_tasks=[
                deliver_item("item_14", table="kitting_table_0"),
                deliver_item("item_15", table="kitting_table_0"),
                deliver_item("item_17", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_15 = ScenarioConfig(
    id="scenario_s18_15",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 64, 142), window(BREAK_TIME, 211, 289),)),
    description=(
        "scenario_s18_15: script 010 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 64 to 142, break_time from 211 to 289. Purpose: a second "
        "coffee break soon after the first (its recency fact holding). Aspects: foreseeable: two coffee "
        "breaks, between and at the end; robot: north-east start, apart. Expectation: the coffee break "
        "(raised by break_time) admitted earlier than off and than on with no fact; the second one "
        "suppressed by its recency fact, the window gives it nothing; a delivery inside a window admitted "
        "later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, -100),
            scheduled_tasks=Script([
                deliver_item("item_11", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_12", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_16 = ScenarioConfig(
    id="scenario_s18_16",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 64, 142), window(BREAK_TIME, 211, 289),)),
    description=(
        "scenario_s18_16: script 010 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 64 to 142, break_time from 211 to 289. Purpose: a "
        "second coffee break soon after the first (its recency fact holding). Aspects: foreseeable: two "
        "coffee breaks, between and at the end; robot: north-east start, apart. Expectation: the coffee "
        "break (raised by break_time) admitted earlier than off and than on with no fact; the second one "
        "suppressed by its recency fact, the window gives it nothing; a delivery inside a window admitted "
        "later than with no fact. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; the coffee break admitted "
        "earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, -100),
            scheduled_tasks=Script([
                deliver_item("item_11", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_12", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, 300),
            assigned_tasks=[
                deliver_item("item_14", table="kitting_table_0"),
                deliver_item("item_15", table="kitting_table_0"),
                deliver_item("item_17", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_17 = ScenarioConfig(
    id="scenario_s18_17",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 64),)),
    description=(
        "scenario_s18_17: script 010 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 64. Purpose: a second coffee break soon "
        "after the first (its recency fact holding). Aspects: foreseeable: two coffee breaks, between and at "
        "the end; robot: north-east start, apart. Expectation: the delivery under break_time admitted later "
        "than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, -100),
            scheduled_tasks=Script([
                deliver_item("item_11", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_12", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_18 = ScenarioConfig(
    id="scenario_s18_18",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 64),)),
    description=(
        "scenario_s18_18: script 010 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 64. Purpose: a second coffee break soon "
        "after the first (its recency fact holding). Aspects: foreseeable: two coffee breaks, between and at "
        "the end; robot: north-east start, apart. Expectation: the delivery under break_time admitted later "
        "than with no fact, near off. working robot: the decisions as off where no admission moves; an "
        "earlier admission of a delivery moves the response decision earlier or leaves it; under the window "
        "the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, -100),
            scheduled_tasks=Script([
                deliver_item("item_11", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_12", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_11", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, 300),
            assigned_tasks=[
                deliver_item("item_14", table="kitting_table_0"),
                deliver_item("item_15", table="kitting_table_0"),
                deliver_item("item_17", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 011: unmodelled with a foreseeable task: a delivery abandoned at shelf_1 beside the coffee machine before the grasp, then a coffee break
scenario_s18_19 = ScenarioConfig(
    id="scenario_s18_19",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s18_19: script 011 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery abandoned at shelf_1 beside the coffee "
        "machine before the grasp, then a coffee break. Aspects: unmodelled: an abandoned delivery (before "
        "the grasp); foreseeable: right after it, at the same corner. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength); the abandoned delivery admitted while the human walks "
        "to it, then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 100),
            scheduled_tasks=Script([
                deliver_item("item_10", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_12", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_20 = ScenarioConfig(
    id="scenario_s18_20",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s18_20: script 011 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery abandoned at shelf_1 beside the coffee "
        "machine before the grasp, then a coffee break. Aspects: unmodelled: an abandoned delivery (before "
        "the grasp); foreseeable: right after it, at the same corner. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength); the abandoned delivery admitted while the human walks "
        "to it, then retracted as the evidence turns. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 100),
            scheduled_tasks=Script([
                deliver_item("item_10", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_12", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, -100),
            assigned_tasks=[
                deliver_item("item_14", table="kitting_table_0"),
                deliver_item("item_16", table="kitting_table_0"),
                deliver_item("item_17", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_21 = ScenarioConfig(
    id="scenario_s18_21",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 43, 83),)),
    description=(
        "scenario_s18_21: script 011 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 43 to 83. Purpose: unmodelled with a foreseeable task: a "
        "delivery abandoned at shelf_1 beside the coffee machine before the grasp, then a coffee break. "
        "Aspects: unmodelled: an abandoned delivery (before the grasp); foreseeable: right after it, at the "
        "same corner. Expectation: the coffee break (raised by break_time) admitted earlier than off and "
        "than on with no fact; a delivery inside a window admitted later than with no fact; the abandoned "
        "delivery admitted while the human walks to it, then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 100),
            scheduled_tasks=Script([
                deliver_item("item_10", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_12", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_22 = ScenarioConfig(
    id="scenario_s18_22",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 43, 83),)),
    description=(
        "scenario_s18_22: script 011 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 43 to 83. Purpose: unmodelled with a foreseeable "
        "task: a delivery abandoned at shelf_1 beside the coffee machine before the grasp, then a coffee "
        "break. Aspects: unmodelled: an abandoned delivery (before the grasp); foreseeable: right after it, "
        "at the same corner. Expectation: the coffee break (raised by break_time) admitted earlier than off "
        "and than on with no fact; a delivery inside a window admitted later than with no fact; the "
        "abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it; the coffee break admitted earlier, the robot's "
        "decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 100),
            scheduled_tasks=Script([
                deliver_item("item_10", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_12", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, -100),
            assigned_tasks=[
                deliver_item("item_14", table="kitting_table_0"),
                deliver_item("item_16", table="kitting_table_0"),
                deliver_item("item_17", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_23 = ScenarioConfig(
    id="scenario_s18_23",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 83, 153),)),
    description=(
        "scenario_s18_23: script 011 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 83 to 153. Purpose: unmodelled with a "
        "foreseeable task: a delivery abandoned at shelf_1 beside the coffee machine before the grasp, then "
        "a coffee break. Aspects: unmodelled: an abandoned delivery (before the grasp); foreseeable: right "
        "after it, at the same corner. Expectation: the delivery under break_time admitted later than with "
        "no fact, near off; the abandoned delivery admitted while the human walks to it, then retracted as "
        "the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 100),
            scheduled_tasks=Script([
                deliver_item("item_10", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_12", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_24 = ScenarioConfig(
    id="scenario_s18_24",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 83, 153),)),
    description=(
        "scenario_s18_24: script 011 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 83 to 153. Purpose: unmodelled with a "
        "foreseeable task: a delivery abandoned at shelf_1 beside the coffee machine before the grasp, then "
        "a coffee break. Aspects: unmodelled: an abandoned delivery (before the grasp); foreseeable: right "
        "after it, at the same corner. Expectation: the delivery under break_time admitted later than with "
        "no fact, near off; the abandoned delivery admitted while the human walks to it, then retracted as "
        "the evidence turns. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; under the window the "
        "delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 100),
            scheduled_tasks=Script([
                deliver_item("item_10", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_12", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_10", table="kitting_table_0"),
                deliver_item("item_12", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, -100),
            assigned_tasks=[
                deliver_item("item_14", table="kitting_table_0"),
                deliver_item("item_16", table="kitting_table_0"),
                deliver_item("item_17", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 012: unmodelled alone: a walk to the far corner and a stand of 30 ticks there between two deliveries
scenario_s18_25 = ScenarioConfig(
    id="scenario_s18_25",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s18_25: script 012 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a walk to the far corner and a stand of 30 ticks there between two "
        "deliveries. Aspects: unmodelled: a walk elsewhere with a stand (30 ticks); robot: south-west start, "
        "crossing the human's walk to the corner. Expectation: on against off: each delivery admitted "
        "earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the "
        "walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_13", table="kitting_table_0"),
                go_to_and_stand("corner_SE", "PT60S"),
                deliver_item("item_11", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_26 = ScenarioConfig(
    id="scenario_s18_26",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s18_26: script 012 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a walk to the far corner and a stand of 30 ticks there between two "
        "deliveries. Aspects: unmodelled: a walk elsewhere with a stand (30 ticks); robot: south-west start, "
        "crossing the human's walk to the corner. Expectation: on against off: each delivery admitted "
        "earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the "
        "walk elsewhere, except a hypothesis whose target lies on the walk. working robot: the decisions as "
        "off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_13", table="kitting_table_0"),
                go_to_and_stand("corner_SE", "PT60S"),
                deliver_item("item_11", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -300),
            assigned_tasks=[
                deliver_item("item_15", table="kitting_table_0"),
                deliver_item("item_17", table="kitting_table_0"),
                deliver_item("item_16", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_27 = ScenarioConfig(
    id="scenario_s18_27",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 79),)),
    description=(
        "scenario_s18_27: script 012 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 79. Purpose: unmodelled alone: a walk "
        "to the far corner and a stand of 30 ticks there between two deliveries. Aspects: unmodelled: a walk "
        "elsewhere with a stand (30 ticks); robot: south-west start, crossing the human's walk to the "
        "corner. Expectation: the delivery under break_time admitted later than with no fact, near off; no "
        "admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_13", table="kitting_table_0"),
                go_to_and_stand("corner_SE", "PT60S"),
                deliver_item("item_11", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_28 = ScenarioConfig(
    id="scenario_s18_28",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 79),)),
    description=(
        "scenario_s18_28: script 012 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 79. Purpose: unmodelled alone: a walk "
        "to the far corner and a stand of 30 ticks there between two deliveries. Aspects: unmodelled: a walk "
        "elsewhere with a stand (30 ticks); robot: south-west start, crossing the human's walk to the "
        "corner. Expectation: the delivery under break_time admitted later than with no fact, near off; no "
        "admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the "
        "walk. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_13", table="kitting_table_0"),
                go_to_and_stand("corner_SE", "PT60S"),
                deliver_item("item_11", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -300),
            assigned_tasks=[
                deliver_item("item_15", table="kitting_table_0"),
                deliver_item("item_17", table="kitting_table_0"),
                deliver_item("item_16", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_29 = ScenarioConfig(
    id="scenario_s18_29",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(ROOM_WARM, 0, 79),)),
    description=(
        "scenario_s18_29: script 012 of step 5e, the idle robot, its own timeline, room_warm over a delivery "
        "(the human works through it): room_warm from 0 to 79. Purpose: unmodelled alone: a walk to the far "
        "corner and a stand of 30 ticks there between two deliveries. Aspects: unmodelled: a walk elsewhere "
        "with a stand (30 ticks); robot: south-west start, crossing the human's walk to the corner. "
        "Expectation: the delivery under room_warm admitted later than with no fact, by less than under "
        "break_time (raised 0.5 against 2)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_13", table="kitting_table_0"),
                go_to_and_stand("corner_SE", "PT60S"),
                deliver_item("item_11", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -450),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s18_30 = ScenarioConfig(
    id="scenario_s18_30",
    setup="env_setup_18",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(ROOM_WARM, 0, 79),)),
    description=(
        "scenario_s18_30: script 012 of step 5e, the working robot, its own timeline, room_warm over a "
        "delivery (the human works through it): room_warm from 0 to 79. Purpose: unmodelled alone: a walk to "
        "the far corner and a stand of 30 ticks there between two deliveries. Aspects: unmodelled: a walk "
        "elsewhere with a stand (30 ticks); robot: south-west start, crossing the human's walk to the "
        "corner. Expectation: the delivery under room_warm admitted later than with no fact, by less than "
        "under break_time (raised 0.5 against 2). working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_13", table="kitting_table_0"),
                go_to_and_stand("corner_SE", "PT60S"),
                deliver_item("item_11", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_13", table="kitting_table_0"),
                deliver_item("item_11", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -300),
            assigned_tasks=[
                deliver_item("item_15", table="kitting_table_0"),
                deliver_item("item_17", table="kitting_table_0"),
                deliver_item("item_16", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)
