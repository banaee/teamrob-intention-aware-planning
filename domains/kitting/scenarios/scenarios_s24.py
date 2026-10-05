# domains/kitting/scenarios/scenarios_s24.py
"""
Kitting scenarios on env_setup_24: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_07; the shift
env_setup_24: a second shift: the human's parts on shelf_1 (behind the coffee machine), shelf_5 (beside it) and shelf_3 (across the table); the robot's on shelf_2, shelf_3 and shelf_1.
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

# ---- script 041: deliveries only: the first walk passes the coffee machine to shelf_1 behind it
scenario_s24_01 = ScenarioConfig(
    id="scenario_s24_01",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s24_01: script 041 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: the first walk passes the coffee machine to shelf_1 behind it. Aspects: "
        "deliveries: two, south then north; approach toward the machine; robot: south-west start, crossing "
        "on the south route. Expectation: on against off: each delivery admitted earlier or equal (the "
        "assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 300),
            scheduled_tasks=Script([
                deliver_item("item_51", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_51", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_02 = ScenarioConfig(
    id="scenario_s24_02",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s24_02: script 041 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: the first walk passes the coffee machine to shelf_1 behind it. Aspects: "
        "deliveries: two, south then north; approach toward the machine; robot: south-west start, crossing "
        "on the south route. Expectation: on against off: each delivery admitted earlier or equal (the "
        "assigned tasks share most of the prior). working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 300),
            scheduled_tasks=Script([
                deliver_item("item_51", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_51", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -200),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_03 = ScenarioConfig(
    id="scenario_s24_03",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 94),)),
    description=(
        "scenario_s24_03: script 041 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 94. Purpose: deliveries only: the first "
        "walk passes the coffee machine to shelf_1 behind it. Aspects: deliveries: two, south then north; "
        "approach toward the machine; robot: south-west start, crossing on the south route. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads "
        "toward the machine may lose its admission to the raised coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 300),
            scheduled_tasks=Script([
                deliver_item("item_51", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_51", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_04 = ScenarioConfig(
    id="scenario_s24_04",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 94),)),
    description=(
        "scenario_s24_04: script 041 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 94. Purpose: deliveries only: the first "
        "walk passes the coffee machine to shelf_1 behind it. Aspects: deliveries: two, south then north; "
        "approach toward the machine; robot: south-west start, crossing on the south route. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off; a delivery whose walk heads "
        "toward the machine may lose its admission to the raised coffee break. working robot: the decisions "
        "as off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it; under the window the delivery's admission and the robot's decision on it "
        "later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 300),
            scheduled_tasks=Script([
                deliver_item("item_51", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_51", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -200),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_05 = ScenarioConfig(
    id="scenario_s24_05",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(ROOM_WARM, 0, 94),)),
    description=(
        "scenario_s24_05: script 041 of step 5e, the idle robot, its own timeline, room_warm over a delivery "
        "(the human works through it): room_warm from 0 to 94. Purpose: deliveries only: the first walk "
        "passes the coffee machine to shelf_1 behind it. Aspects: deliveries: two, south then north; "
        "approach toward the machine; robot: south-west start, crossing on the south route. Expectation: the "
        "delivery under room_warm admitted later than with no fact, by less than under break_time (raised "
        "0.5 against 2)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 300),
            scheduled_tasks=Script([
                deliver_item("item_51", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_51", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_06 = ScenarioConfig(
    id="scenario_s24_06",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(ROOM_WARM, 0, 94),)),
    description=(
        "scenario_s24_06: script 041 of step 5e, the working robot, its own timeline, room_warm over a "
        "delivery (the human works through it): room_warm from 0 to 94. Purpose: deliveries only: the first "
        "walk passes the coffee machine to shelf_1 behind it. Aspects: deliveries: two, south then north; "
        "approach toward the machine; robot: south-west start, crossing on the south route. Expectation: the "
        "delivery under room_warm admitted later than with no fact, by less than under break_time (raised "
        "0.5 against 2). working robot: the decisions as off where no admission moves; an earlier admission "
        "of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 300),
            scheduled_tasks=Script([
                deliver_item("item_51", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_51", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -200),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 042: a coffee break at the end, after a delivery from the shelf beside the machine
scenario_s24_07 = ScenarioConfig(
    id="scenario_s24_07",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s24_07: script 042 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the end, after a delivery from the shelf beside the machine. Aspects: "
        "foreseeable: at the end; robot: south-west start. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted "
        "later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 500),
            scheduled_tasks=Script([
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_52", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_08 = ScenarioConfig(
    id="scenario_s24_08",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s24_08: script 042 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the end, after a delivery from the shelf beside the machine. Aspects: "
        "foreseeable: at the end; robot: south-west start. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted "
        "later than off (ordinary strength). working robot: the decisions as off where no admission moves; "
        "an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 500),
            scheduled_tasks=Script([
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_52", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -200),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_09 = ScenarioConfig(
    id="scenario_s24_09",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 147, 207),)),
    description=(
        "scenario_s24_09: script 042 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 147 to 207. Purpose: a coffee break at the end, after a "
        "delivery from the shelf beside the machine. Aspects: foreseeable: at the end; robot: south-west "
        "start. Expectation: the coffee break (raised by break_time) admitted earlier than off and than on "
        "with no fact; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 500),
            scheduled_tasks=Script([
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_52", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_10 = ScenarioConfig(
    id="scenario_s24_10",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 147, 207),)),
    description=(
        "scenario_s24_10: script 042 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 147 to 207. Purpose: a coffee break at the end, "
        "after a delivery from the shelf beside the machine. Aspects: foreseeable: at the end; robot: "
        "south-west start. Expectation: the coffee break (raised by break_time) admitted earlier than off "
        "and than on with no fact; a delivery inside a window admitted later than with no fact. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; the coffee break admitted earlier, the robot's decision "
        "against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 500),
            scheduled_tasks=Script([
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_52", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -200),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_11 = ScenarioConfig(
    id="scenario_s24_11",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 83),)),
    description=(
        "scenario_s24_11: script 042 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 83. Purpose: a coffee break at the end, "
        "after a delivery from the shelf beside the machine. Aspects: foreseeable: at the end; robot: "
        "south-west start. Expectation: the delivery under break_time admitted later than with no fact, near "
        "off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 500),
            scheduled_tasks=Script([
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_52", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_12 = ScenarioConfig(
    id="scenario_s24_12",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 83),)),
    description=(
        "scenario_s24_12: script 042 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 83. Purpose: a coffee break at the end, "
        "after a delivery from the shelf beside the machine. Aspects: foreseeable: at the end; robot: "
        "south-west start. Expectation: the delivery under break_time admitted later than with no fact, near "
        "off. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 500),
            scheduled_tasks=Script([
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_52", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -200),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 043: a second coffee break soon after the first, at the start and after the first delivery
scenario_s24_13 = ScenarioConfig(
    id="scenario_s24_13",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s24_13: script 043 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a second coffee break soon after the first, at the start and after the first delivery. "
        "Aspects: foreseeable: two coffee breaks, at the start and between. Expectation: on against off: "
        "each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee "
        "break admitted later than off (ordinary strength); the second under its recency fact (suppressed), "
        "later still."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -300),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
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
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_14 = ScenarioConfig(
    id="scenario_s24_14",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s24_14: script 043 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a second coffee break soon after the first, at the start and after the first delivery. "
        "Aspects: foreseeable: two coffee breaks, at the start and between. Expectation: on against off: "
        "each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee "
        "break admitted later than off (ordinary strength); the second under its recency fact (suppressed), "
        "later still. working robot: the decisions as off where no admission moves; an earlier admission of "
        "a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -300),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
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
            start_position=(-600, 600),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_15 = ScenarioConfig(
    id="scenario_s24_15",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 51), window(BREAK_TIME, 90, 150),)),
    description=(
        "scenario_s24_15: script 043 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 0 to 51, break_time from 90 to 150. Purpose: a second "
        "coffee break soon after the first, at the start and after the first delivery. Aspects: foreseeable: "
        "two coffee breaks, at the start and between. Expectation: the coffee break (raised by break_time) "
        "admitted earlier than off and than on with no fact; the second one suppressed by its recency fact, "
        "the window gives it nothing; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -300),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
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
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_16 = ScenarioConfig(
    id="scenario_s24_16",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 51), window(BREAK_TIME, 90, 150),)),
    description=(
        "scenario_s24_16: script 043 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 0 to 51, break_time from 90 to 150. Purpose: a "
        "second coffee break soon after the first, at the start and after the first delivery. Aspects: "
        "foreseeable: two coffee breaks, at the start and between. Expectation: the coffee break (raised by "
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
            start_position=(300, -300),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
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
            start_position=(-600, 600),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_17 = ScenarioConfig(
    id="scenario_s24_17",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 51, 90),)),
    description=(
        "scenario_s24_17: script 043 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 51 to 90. Purpose: a second coffee break "
        "soon after the first, at the start and after the first delivery. Aspects: foreseeable: two coffee "
        "breaks, at the start and between. Expectation: the delivery under break_time admitted later than "
        "with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -300),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
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
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_18 = ScenarioConfig(
    id="scenario_s24_18",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 51, 90),)),
    description=(
        "scenario_s24_18: script 043 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 51 to 90. Purpose: a second coffee break "
        "soon after the first, at the start and after the first delivery. Aspects: foreseeable: two coffee "
        "breaks, at the start and between. Expectation: the delivery under break_time admitted later than "
        "with no fact, near off. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; under the window the "
        "delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -300),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
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
            start_position=(-600, 600),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 044: unmodelled alone: a walk to the north-west corner and a stand of 20 ticks between deliveries
scenario_s24_19 = ScenarioConfig(
    id="scenario_s24_19",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s24_19: script 044 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a walk to the north-west corner and a stand of 20 ticks between "
        "deliveries. Aspects: unmodelled: a walk elsewhere with a stand (20 ticks). Expectation: on against "
        "off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); no "
        "admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 200),
            scheduled_tasks=Script([
                deliver_item("item_53", table="kitting_table_0"),
                go_to_and_stand("corner_NW", "PT40S"),
                deliver_item("item_51", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_51", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_20 = ScenarioConfig(
    id="scenario_s24_20",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s24_20: script 044 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a walk to the north-west corner and a stand of 20 ticks between "
        "deliveries. Aspects: unmodelled: a walk elsewhere with a stand (20 ticks). Expectation: on against "
        "off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); no "
        "admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the "
        "walk. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 200),
            scheduled_tasks=Script([
                deliver_item("item_53", table="kitting_table_0"),
                go_to_and_stand("corner_NW", "PT40S"),
                deliver_item("item_51", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_51", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -600),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_21 = ScenarioConfig(
    id="scenario_s24_21",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 88),)),
    description=(
        "scenario_s24_21: script 044 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 88. Purpose: unmodelled alone: a walk "
        "to the north-west corner and a stand of 20 ticks between deliveries. Aspects: unmodelled: a walk "
        "elsewhere with a stand (20 ticks). Expectation: the delivery under break_time admitted later than "
        "with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis "
        "whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 200),
            scheduled_tasks=Script([
                deliver_item("item_53", table="kitting_table_0"),
                go_to_and_stand("corner_NW", "PT40S"),
                deliver_item("item_51", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_51", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_22 = ScenarioConfig(
    id="scenario_s24_22",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 88),)),
    description=(
        "scenario_s24_22: script 044 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 88. Purpose: unmodelled alone: a walk "
        "to the north-west corner and a stand of 20 ticks between deliveries. Aspects: unmodelled: a walk "
        "elsewhere with a stand (20 ticks). Expectation: the delivery under break_time admitted later than "
        "with no fact, near off; no admission during the stand or the walk elsewhere, except a hypothesis "
        "whose target lies on the walk. working robot: the decisions as off where no admission moves; an "
        "earlier admission of a delivery moves the response decision earlier or leaves it; under the window "
        "the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 200),
            scheduled_tasks=Script([
                deliver_item("item_53", table="kitting_table_0"),
                go_to_and_stand("corner_NW", "PT40S"),
                deliver_item("item_51", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_51", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -600),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_23 = ScenarioConfig(
    id="scenario_s24_23",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(ROOM_WARM, 0, 88),)),
    description=(
        "scenario_s24_23: script 044 of step 5e, the idle robot, its own timeline, room_warm over a delivery "
        "(the human works through it): room_warm from 0 to 88. Purpose: unmodelled alone: a walk to the "
        "north-west corner and a stand of 20 ticks between deliveries. Aspects: unmodelled: a walk elsewhere "
        "with a stand (20 ticks). Expectation: the delivery under room_warm admitted later than with no "
        "fact, by less than under break_time (raised 0.5 against 2)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 200),
            scheduled_tasks=Script([
                deliver_item("item_53", table="kitting_table_0"),
                go_to_and_stand("corner_NW", "PT40S"),
                deliver_item("item_51", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_51", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_24 = ScenarioConfig(
    id="scenario_s24_24",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(ROOM_WARM, 0, 88),)),
    description=(
        "scenario_s24_24: script 044 of step 5e, the working robot, its own timeline, room_warm over a "
        "delivery (the human works through it): room_warm from 0 to 88. Purpose: unmodelled alone: a walk to "
        "the north-west corner and a stand of 20 ticks between deliveries. Aspects: unmodelled: a walk "
        "elsewhere with a stand (20 ticks). Expectation: the delivery under room_warm admitted later than "
        "with no fact, by less than under break_time (raised 0.5 against 2). working robot: the decisions as "
        "off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 200),
            scheduled_tasks=Script([
                deliver_item("item_53", table="kitting_table_0"),
                go_to_and_stand("corner_NW", "PT40S"),
                deliver_item("item_51", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_53", table="kitting_table_0"),
                deliver_item("item_51", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -600),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 045: a coffee break and the A/C activation after the one delivery; the second delivery never started
scenario_s24_25 = ScenarioConfig(
    id="scenario_s24_25",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s24_25: script 045 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break and the A/C activation after the one delivery; the second delivery never "
        "started. Aspects: unmodelled: a never-started delivery; foreseeable: two of two kinds, at the end. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior); a coffee break admitted later than off (ordinary strength); the A/C activation "
        "rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the assigned "
        "tasks); the never-started delivery never admitted (no observation warrant)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, -200),
            scheduled_tasks=Script([
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_0"),
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
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_26 = ScenarioConfig(
    id="scenario_s24_26",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s24_26: script 045 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break and the A/C activation after the one delivery; the second delivery never "
        "started. Aspects: unmodelled: a never-started delivery; foreseeable: two of two kinds, at the end. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior); a coffee break admitted later than off (ordinary strength); the A/C activation "
        "rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the assigned "
        "tasks); the never-started delivery never admitted (no observation warrant). working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, -200),
            scheduled_tasks=Script([
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_0"),
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
            start_position=(-600, 600),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_27 = ScenarioConfig(
    id="scenario_s24_27",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 65, 125), window(ROOM_WARM, 125, 162),)),
    description=(
        "scenario_s24_27: script 045 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 65 to 125, room_warm from 125 to 162. Purpose: a coffee "
        "break and the A/C activation after the one delivery; the second delivery never started. Aspects: "
        "unmodelled: a never-started delivery; foreseeable: two of two kinds, at the end. Expectation: the "
        "coffee break (raised by break_time) admitted earlier than off and than on with no fact; the A/C "
        "activation's belief at arrival higher than with no fact (raised by room_warm); admission possible "
        "only where the movement evidence allows; a delivery inside a window admitted later than with no "
        "fact; the never-started delivery never admitted (no observation warrant)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, -200),
            scheduled_tasks=Script([
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_0"),
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
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_28 = ScenarioConfig(
    id="scenario_s24_28",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 65, 125), window(ROOM_WARM, 125, 162),)),
    description=(
        "scenario_s24_28: script 045 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 65 to 125, room_warm from 125 to 162. Purpose: a "
        "coffee break and the A/C activation after the one delivery; the second delivery never started. "
        "Aspects: unmodelled: a never-started delivery; foreseeable: two of two kinds, at the end. "
        "Expectation: the coffee break (raised by break_time) admitted earlier than off and than on with no "
        "fact; the A/C activation's belief at arrival higher than with no fact (raised by room_warm); "
        "admission possible only where the movement evidence allows; a delivery inside a window admitted "
        "later than with no fact; the never-started delivery never admitted (no observation warrant). "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it; the coffee break admitted earlier, the robot's "
        "decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, -200),
            scheduled_tasks=Script([
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_0"),
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
            start_position=(-600, 600),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_29 = ScenarioConfig(
    id="scenario_s24_29",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 65),)),
    description=(
        "scenario_s24_29: script 045 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 65. Purpose: a coffee break and the A/C "
        "activation after the one delivery; the second delivery never started. Aspects: unmodelled: a "
        "never-started delivery; foreseeable: two of two kinds, at the end. Expectation: the delivery under "
        "break_time admitted later than with no fact, near off; the never-started delivery never admitted "
        "(no observation warrant)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, -200),
            scheduled_tasks=Script([
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_0"),
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
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s24_30 = ScenarioConfig(
    id="scenario_s24_30",
    setup="env_setup_24",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 65),)),
    description=(
        "scenario_s24_30: script 045 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 65. Purpose: a coffee break and the A/C "
        "activation after the one delivery; the second delivery never started. Aspects: unmodelled: a "
        "never-started delivery; foreseeable: two of two kinds, at the end. Expectation: the delivery under "
        "break_time admitted later than with no fact, near off; the never-started delivery never admitted "
        "(no observation warrant). working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; under the window the "
        "delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, -200),
            scheduled_tasks=Script([
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_0"),
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
            start_position=(-600, 600),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)
