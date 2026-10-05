# domains/kitting/scenarios/scenarios_s17.py
"""
Kitting scenarios on env_setup_17: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_02; the shift
env_setup_17: env_setup_02's shift (item_k on shelf_k, all to kitting_table_0), so the measured scripts of env_layout_02 have their copies here.
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

# ---- script 001: scenario_s02_01's script as it is: a coffee break after the first delivery, the A/C activation after the second
scenario_s17_01 = ScenarioConfig(
    id="scenario_s17_01",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s17_01: script 001 of step 5e (the script of scenario_s02_01, as it is), the idle robot, "
        "no timeline (the setup states none). Purpose: scenario_s02_01's script as it is: a coffee break "
        "after the first delivery, the A/C activation after the second. Aspects: foreseeable: between "
        "deliveries, two of two kinds; existing. Expectation: on against off: each delivery admitted earlier "
        "or equal (the assigned tasks share most of the prior); a coffee break admitted later than off "
        "(ordinary strength); the A/C activation rarely admitted on or off; its belief at arrival lower on "
        "(ordinary 0.02 against the assigned tasks)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s17_02 = ScenarioConfig(
    id="scenario_s17_02",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 77, 155), window(ROOM_WARM, 311, 364),)),
    description=(
        "scenario_s17_02: script 001 of step 5e (the script of scenario_s02_01, as it is), the idle robot, "
        "its own timeline, the raising fact over the foreseeable task (accord): break_time from 77 to 155, "
        "room_warm from 311 to 364. Purpose: scenario_s02_01's script as it is: a coffee break after the "
        "first delivery, the A/C activation after the second. Aspects: foreseeable: between deliveries, two "
        "of two kinds; existing. Expectation: the coffee break (raised by break_time) admitted earlier than "
        "off and than on with no fact; the A/C activation's belief at arrival higher than with no fact "
        "(raised by room_warm); admission possible only where the movement evidence allows; a delivery "
        "inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s17_03 = ScenarioConfig(
    id="scenario_s17_03",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 77, 155), window(ROOM_WARM, 311, 364),)),
    description=(
        "scenario_s17_03: script 001 of step 5e (the script of scenario_s02_01, as it is), the working "
        "robot, its own timeline, the raising fact over the foreseeable task (accord): break_time from 77 to "
        "155, room_warm from 311 to 364. Purpose: scenario_s02_01's script as it is: a coffee break after "
        "the first delivery, the A/C activation after the second. Aspects: foreseeable: between deliveries, "
        "two of two kinds; existing. Expectation: the coffee break (raised by break_time) admitted earlier "
        "than off and than on with no fact; the A/C activation's belief at arrival higher than with no fact "
        "(raised by room_warm); admission possible only where the movement evidence allows; a delivery "
        "inside a window admitted later than with no fact. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(200, 0),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s17_04 = ScenarioConfig(
    id="scenario_s17_04",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 77),)),
    description=(
        "scenario_s17_04: script 001 of step 5e (the script of scenario_s02_01, as it is), the idle robot, "
        "its own timeline, break_time over a delivery (the human works through it): break_time from 0 to 77. "
        "Purpose: scenario_s02_01's script as it is: a coffee break after the first delivery, the A/C "
        "activation after the second. Aspects: foreseeable: between deliveries, two of two kinds; existing. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s17_05 = ScenarioConfig(
    id="scenario_s17_05",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 77),)),
    description=(
        "scenario_s17_05: script 001 of step 5e (the script of scenario_s02_01, as it is), the working "
        "robot, its own timeline, break_time over a delivery (the human works through it): break_time from 0 "
        "to 77. Purpose: scenario_s02_01's script as it is: a coffee break after the first delivery, the A/C "
        "activation after the second. Aspects: foreseeable: between deliveries, two of two kinds; existing. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; under the window the delivery's admission and the robot's "
        "decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(200, 0),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 002: scenario_s02_02's script as it is: a coffee break inside the first delivery, after the grasp (T-C2c scenario A); no exit walk
scenario_s17_06 = ScenarioConfig(
    id="scenario_s17_06",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s17_06: script 002 of step 5e (the script of scenario_s02_02, as it is), the idle robot, "
        "no timeline (the setup states none). Purpose: scenario_s02_02's script as it is: a coffee break "
        "inside the first delivery, after the grasp (T-C2c scenario A); no exit walk. Aspects: foreseeable: "
        "inside a delivery; existing. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_5", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s17_07 = ScenarioConfig(
    id="scenario_s17_07",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 33, 77),)),
    description=(
        "scenario_s17_07: script 002 of step 5e (the script of scenario_s02_02, as it is), the idle robot, "
        "its own timeline, the raising fact over the foreseeable task (accord): break_time from 33 to 77. "
        "Purpose: scenario_s02_02's script as it is: a coffee break inside the first delivery, after the "
        "grasp (T-C2c scenario A); no exit walk. Aspects: foreseeable: inside a delivery; existing. "
        "Expectation: the coffee break (raised by break_time) admitted earlier than off and than on with no "
        "fact; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_5", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s17_08 = ScenarioConfig(
    id="scenario_s17_08",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 33, 77),)),
    description=(
        "scenario_s17_08: script 002 of step 5e (the script of scenario_s02_02, as it is), the working "
        "robot, its own timeline, the raising fact over the foreseeable task (accord): break_time from 33 to "
        "77. Purpose: scenario_s02_02's script as it is: a coffee break inside the first delivery, after the "
        "grasp (T-C2c scenario A); no exit walk. Aspects: foreseeable: inside a delivery; existing. "
        "Expectation: the coffee break (raised by break_time) admitted earlier than off and than on with no "
        "fact; a delivery inside a window admitted later than with no fact. working robot: the decisions as "
        "off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_5", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(200, 0),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s17_09 = ScenarioConfig(
    id="scenario_s17_09",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 126, 251),)),
    description=(
        "scenario_s17_09: script 002 of step 5e (the script of scenario_s02_02, as it is), the idle robot, "
        "its own timeline, break_time over a delivery (the human works through it): break_time from 126 to "
        "251. Purpose: scenario_s02_02's script as it is: a coffee break inside the first delivery, after "
        "the grasp (T-C2c scenario A); no exit walk. Aspects: foreseeable: inside a delivery; existing. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_5", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s17_10 = ScenarioConfig(
    id="scenario_s17_10",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 126, 251),)),
    description=(
        "scenario_s17_10: script 002 of step 5e (the script of scenario_s02_02, as it is), the working "
        "robot, its own timeline, break_time over a delivery (the human works through it): break_time from "
        "126 to 251. Purpose: scenario_s02_02's script as it is: a coffee break inside the first delivery, "
        "after the grasp (T-C2c scenario A); no exit walk. Aspects: foreseeable: inside a delivery; "
        "existing. Expectation: the delivery under break_time admitted later than with no fact, near off. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it; under the window the delivery's admission and the "
        "robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_5", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(200, 0),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 003: deliveries only: three deliveries from the east, west and east walls
scenario_s17_11 = ScenarioConfig(
    id="scenario_s17_11",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s17_11: script 003 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: three deliveries from the east, west and east walls. Aspects: deliveries: "
        "three, order east-west-east; start: south-east floor, first walk away from the break corner; robot: "
        "south-west start, the south and west shelves, crossing the human at the table. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -100),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s17_12 = ScenarioConfig(
    id="scenario_s17_12",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s17_12: script 003 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: three deliveries from the east, west and east walls. Aspects: deliveries: "
        "three, order east-west-east; start: south-east floor, first walk away from the break corner; robot: "
        "south-west start, the south and west shelves, crossing the human at the table. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -100),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -200),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s17_13 = ScenarioConfig(
    id="scenario_s17_13",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 97),)),
    description=(
        "scenario_s17_13: script 003 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 97. Purpose: deliveries only: three "
        "deliveries from the east, west and east walls. Aspects: deliveries: three, order east-west-east; "
        "start: south-east floor, first walk away from the break corner; robot: south-west start, the south "
        "and west shelves, crossing the human at the table. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -100),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s17_14 = ScenarioConfig(
    id="scenario_s17_14",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 97),)),
    description=(
        "scenario_s17_14: script 003 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 97. Purpose: deliveries only: three "
        "deliveries from the east, west and east walls. Aspects: deliveries: three, order east-west-east; "
        "start: south-east floor, first walk away from the break corner; robot: south-west start, the south "
        "and west shelves, crossing the human at the table. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it; under "
        "the window the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -100),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -200),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s17_15 = ScenarioConfig(
    id="scenario_s17_15",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(ROOM_WARM, 0, 97),)),
    description=(
        "scenario_s17_15: script 003 of step 5e, the idle robot, its own timeline, room_warm over a delivery "
        "(the human works through it): room_warm from 0 to 97. Purpose: deliveries only: three deliveries "
        "from the east, west and east walls. Aspects: deliveries: three, order east-west-east; start: "
        "south-east floor, first walk away from the break corner; robot: south-west start, the south and "
        "west shelves, crossing the human at the table. Expectation: the delivery under room_warm admitted "
        "later than with no fact, by less than under break_time (raised 0.5 against 2)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -100),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s17_16 = ScenarioConfig(
    id="scenario_s17_16",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(ROOM_WARM, 0, 97),)),
    description=(
        "scenario_s17_16: script 003 of step 5e, the working robot, its own timeline, room_warm over a "
        "delivery (the human works through it): room_warm from 0 to 97. Purpose: deliveries only: three "
        "deliveries from the east, west and east walls. Aspects: deliveries: three, order east-west-east; "
        "start: south-east floor, first walk away from the break corner; robot: south-west start, the south "
        "and west shelves, crossing the human at the table. Expectation: the delivery under room_warm "
        "admitted later than with no fact, by less than under break_time (raised 0.5 against 2). working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -100),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -200),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 004: a coffee break at the start, then two deliveries
scenario_s17_17 = ScenarioConfig(
    id="scenario_s17_17",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s17_17: script 004 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the start, then two deliveries. Aspects: foreseeable: at the start; "
        "start: floor centre, first walk toward the coffee machine; robot: east start, east shelves, its "
        "routes apart from the human's. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
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

scenario_s17_18 = ScenarioConfig(
    id="scenario_s17_18",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s17_18: script 004 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the start, then two deliveries. Aspects: foreseeable: at the start; "
        "start: floor centre, first walk toward the coffee machine; robot: east start, east shelves, its "
        "routes apart from the human's. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength). working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, 300),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s17_19 = ScenarioConfig(
    id="scenario_s17_19",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 75),)),
    description=(
        "scenario_s17_19: script 004 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 0 to 75. Purpose: a coffee break at the start, then two "
        "deliveries. Aspects: foreseeable: at the start; start: floor centre, first walk toward the coffee "
        "machine; robot: east start, east shelves, its routes apart from the human's. Expectation: the "
        "coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery "
        "inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
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

scenario_s17_20 = ScenarioConfig(
    id="scenario_s17_20",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 75),)),
    description=(
        "scenario_s17_20: script 004 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 0 to 75. Purpose: a coffee break at the start, then "
        "two deliveries. Aspects: foreseeable: at the start; start: floor centre, first walk toward the "
        "coffee machine; robot: east start, east shelves, its routes apart from the human's. Expectation: "
        "the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a "
        "delivery inside a window admitted later than with no fact. working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, 300),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s17_21 = ScenarioConfig(
    id="scenario_s17_21",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 75, 136),)),
    description=(
        "scenario_s17_21: script 004 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 75 to 136. Purpose: a coffee break at the "
        "start, then two deliveries. Aspects: foreseeable: at the start; start: floor centre, first walk "
        "toward the coffee machine; robot: east start, east shelves, its routes apart from the human's. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off; a delivery "
        "whose walk heads toward the machine may lose its admission to the raised coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
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

scenario_s17_22 = ScenarioConfig(
    id="scenario_s17_22",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 75, 136),)),
    description=(
        "scenario_s17_22: script 004 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 75 to 136. Purpose: a coffee break at the "
        "start, then two deliveries. Aspects: foreseeable: at the start; start: floor centre, first walk "
        "toward the coffee machine; robot: east start, east shelves, its routes apart from the human's. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off; a delivery "
        "whose walk heads toward the machine may lose its admission to the raised coffee break. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; under the window the delivery's admission and the robot's "
        "decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, 300),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 005: the A/C activation alone, between two deliveries
scenario_s17_23 = ScenarioConfig(
    id="scenario_s17_23",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s17_23: script 005 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: the A/C activation alone, between two deliveries. Aspects: foreseeable: the A/C alone, "
        "between deliveries; start: beside the table; robot: south-east start, south and east shelves. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior); the A/C activation rarely admitted on or off; its belief at arrival lower on "
        "(ordinary 0.02 against the assigned tasks)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                deliver_item("item_5", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s17_24 = ScenarioConfig(
    id="scenario_s17_24",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s17_24: script 005 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: the A/C activation alone, between two deliveries. Aspects: foreseeable: the A/C alone, "
        "between deliveries; start: beside the table; robot: south-east start, south and east shelves. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior); the A/C activation rarely admitted on or off; its belief at arrival lower on "
        "(ordinary 0.02 against the assigned tasks). working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                deliver_item("item_5", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, -300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s17_25 = ScenarioConfig(
    id="scenario_s17_25",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(ROOM_WARM, 74, 126),)),
    description=(
        "scenario_s17_25: script 005 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): room_warm from 74 to 126. Purpose: the A/C activation alone, between two "
        "deliveries. Aspects: foreseeable: the A/C alone, between deliveries; start: beside the table; "
        "robot: south-east start, south and east shelves. Expectation: the A/C activation's belief at "
        "arrival higher than with no fact (raised by room_warm); admission possible only where the movement "
        "evidence allows; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                deliver_item("item_5", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s17_26 = ScenarioConfig(
    id="scenario_s17_26",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(ROOM_WARM, 74, 126),)),
    description=(
        "scenario_s17_26: script 005 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): room_warm from 74 to 126. Purpose: the A/C activation alone, between "
        "two deliveries. Aspects: foreseeable: the A/C alone, between deliveries; start: beside the table; "
        "robot: south-east start, south and east shelves. Expectation: the A/C activation's belief at "
        "arrival higher than with no fact (raised by room_warm); admission possible only where the movement "
        "evidence allows; a delivery inside a window admitted later than with no fact. working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                deliver_item("item_5", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, -300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s17_27 = ScenarioConfig(
    id="scenario_s17_27",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 74),)),
    description=(
        "scenario_s17_27: script 005 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 74. Purpose: the A/C activation alone, "
        "between two deliveries. Aspects: foreseeable: the A/C alone, between deliveries; start: beside the "
        "table; robot: south-east start, south and east shelves. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                deliver_item("item_5", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s17_28 = ScenarioConfig(
    id="scenario_s17_28",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 74),)),
    description=(
        "scenario_s17_28: script 005 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 74. Purpose: the A/C activation alone, "
        "between two deliveries. Aspects: foreseeable: the A/C alone, between deliveries; start: beside the "
        "table; robot: south-east start, south and east shelves. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it; under "
        "the window the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
                deliver_item("item_5", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, -300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 006: a coffee break inside a delivery whose approach heads toward the coffee machine: item_1 on shelf_1, 3.6 deg off the machine's bearing from the table
scenario_s17_29 = ScenarioConfig(
    id="scenario_s17_29",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s17_29: script 006 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery whose approach heads toward the coffee machine: item_1 on "
        "shelf_1, 3.6 deg off the machine's bearing from the table. Aspects: foreseeable: inside a delivery, "
        "after the grasp; approach toward the machine; robot: east, apart. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 100),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s17_30 = ScenarioConfig(
    id="scenario_s17_30",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s17_30: script 006 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery whose approach heads toward the coffee machine: item_1 on "
        "shelf_1, 3.6 deg off the machine's bearing from the table. Aspects: foreseeable: inside a delivery, "
        "after the grasp; approach toward the machine; robot: east, apart. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength). working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 100),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, -300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s17_31 = ScenarioConfig(
    id="scenario_s17_31",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 38, 78),)),
    description=(
        "scenario_s17_31: script 006 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 38 to 78. Purpose: a coffee break inside a delivery "
        "whose approach heads toward the coffee machine: item_1 on shelf_1, 3.6 deg off the machine's "
        "bearing from the table. Aspects: foreseeable: inside a delivery, after the grasp; approach toward "
        "the machine; robot: east, apart. Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; a delivery inside a window admitted later than with no "
        "fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 100),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s17_32 = ScenarioConfig(
    id="scenario_s17_32",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 38, 78),)),
    description=(
        "scenario_s17_32: script 006 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 38 to 78. Purpose: a coffee break inside a delivery "
        "whose approach heads toward the coffee machine: item_1 on shelf_1, 3.6 deg off the machine's "
        "bearing from the table. Aspects: foreseeable: inside a delivery, after the grasp; approach toward "
        "the machine; robot: east, apart. Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; a delivery inside a window admitted later than with no "
        "fact. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; the coffee break admitted earlier, the "
        "robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 100),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, -300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s17_33 = ScenarioConfig(
    id="scenario_s17_33",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 129, 248),)),
    description=(
        "scenario_s17_33: script 006 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 129 to 248. Purpose: a coffee break inside a "
        "delivery whose approach heads toward the coffee machine: item_1 on shelf_1, 3.6 deg off the "
        "machine's bearing from the table. Aspects: foreseeable: inside a delivery, after the grasp; "
        "approach toward the machine; robot: east, apart. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose "
        "its admission to the raised coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 100),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s17_34 = ScenarioConfig(
    id="scenario_s17_34",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 129, 248),)),
    description=(
        "scenario_s17_34: script 006 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 129 to 248. Purpose: a coffee break inside a "
        "delivery whose approach heads toward the coffee machine: item_1 on shelf_1, 3.6 deg off the "
        "machine's bearing from the table. Aspects: foreseeable: inside a delivery, after the grasp; "
        "approach toward the machine; robot: east, apart. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose "
        "its admission to the raised coffee break. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it; under "
        "the window the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 100),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, -300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 007: unmodelled alone: a stand of 20 ticks at the table after the one delivery, a second assigned delivery never started
scenario_s17_35 = ScenarioConfig(
    id="scenario_s17_35",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s17_35: script 007 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a stand of 20 ticks at the table after the one delivery, a second "
        "assigned delivery never started. Aspects: unmodelled: a stand (20 ticks) and a never-started "
        "delivery; no foreseeable task. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior); the never-started delivery never admitted (no "
        "observation warrant); no admission during the stand or the walk elsewhere, except a hypothesis "
        "whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                stand("PT40S"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s17_36 = ScenarioConfig(
    id="scenario_s17_36",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    description=(
        "scenario_s17_36: script 007 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a stand of 20 ticks at the table after the one delivery, a second "
        "assigned delivery never started. Aspects: unmodelled: a stand (20 ticks) and a never-started "
        "delivery; no foreseeable task. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior); the never-started delivery never admitted (no "
        "observation warrant); no admission during the stand or the walk elsewhere, except a hypothesis "
        "whose target lies on the walk. working robot: the decisions as off where no admission moves; an "
        "earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                stand("PT40S"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -100),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s17_37 = ScenarioConfig(
    id="scenario_s17_37",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 85),)),
    description=(
        "scenario_s17_37: script 007 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 85. Purpose: unmodelled alone: a stand "
        "of 20 ticks at the table after the one delivery, a second assigned delivery never started. Aspects: "
        "unmodelled: a stand (20 ticks) and a never-started delivery; no foreseeable task. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off; the never-started delivery "
        "never admitted (no observation warrant); no admission during the stand or the walk elsewhere, "
        "except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                stand("PT40S"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s17_38 = ScenarioConfig(
    id="scenario_s17_38",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 85),)),
    description=(
        "scenario_s17_38: script 007 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 85. Purpose: unmodelled alone: a stand "
        "of 20 ticks at the table after the one delivery, a second assigned delivery never started. Aspects: "
        "unmodelled: a stand (20 ticks) and a never-started delivery; no foreseeable task. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off; the never-started delivery "
        "never admitted (no observation warrant); no admission during the stand or the walk elsewhere, "
        "except a hypothesis whose target lies on the walk. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it; under the window the delivery's admission and the robot's decision on it later than with no "
        "fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                stand("PT40S"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -100),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s17_39 = ScenarioConfig(
    id="scenario_s17_39",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(ROOM_WARM, 0, 85),)),
    description=(
        "scenario_s17_39: script 007 of step 5e, the idle robot, its own timeline, room_warm over a delivery "
        "(the human works through it): room_warm from 0 to 85. Purpose: unmodelled alone: a stand of 20 "
        "ticks at the table after the one delivery, a second assigned delivery never started. Aspects: "
        "unmodelled: a stand (20 ticks) and a never-started delivery; no foreseeable task. Expectation: the "
        "delivery under room_warm admitted later than with no fact, by less than under break_time (raised "
        "0.5 against 2)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                stand("PT40S"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s17_40 = ScenarioConfig(
    id="scenario_s17_40",
    setup="env_setup_17",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(ROOM_WARM, 0, 85),)),
    description=(
        "scenario_s17_40: script 007 of step 5e, the working robot, its own timeline, room_warm over a "
        "delivery (the human works through it): room_warm from 0 to 85. Purpose: unmodelled alone: a stand "
        "of 20 ticks at the table after the one delivery, a second assigned delivery never started. Aspects: "
        "unmodelled: a stand (20 ticks) and a never-started delivery; no foreseeable task. Expectation: the "
        "delivery under room_warm admitted later than with no fact, by less than under break_time (raised "
        "0.5 against 2). working robot: the decisions as off where no admission moves; an earlier admission "
        "of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                stand("PT40S"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -100),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)
