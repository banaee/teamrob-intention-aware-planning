# domains/kitting/scenarios/scenarios_s25.py
"""
Kitting scenarios on env_setup_25: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_19; the shift
env_setup_25: env_setup_06's shift (item_0, item_1, item_4, item_6 to kitting_table_0; item_3, item_7 to kitting_table_1) with item_2 and item_5 added, both to kitting_table_1.
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

# ---- script 046: deliveries only: two, one to each table
scenario_s25_01 = ScenarioConfig(
    id="scenario_s25_01",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_01: script 046 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: two, one to each table. Aspects: deliveries: two, kitting_table_0 then "
        "kitting_table_1; start: west floor, first walk away from the machine; robot: south start, south "
        "shelves, both tables, crossing at kitting_table_0. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 100),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_02 = ScenarioConfig(
    id="scenario_s25_02",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_02: script 046 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: two, one to each table. Aspects: deliveries: two, kitting_table_0 then "
        "kitting_table_1; start: west floor, first walk away from the machine; robot: south start, south "
        "shelves, both tables, crossing at kitting_table_0. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior). working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 100),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_03 = ScenarioConfig(
    id="scenario_s25_03",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 61),)),
    description=(
        "scenario_s25_03: script 046 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 61. Purpose: deliveries only: two, one "
        "to each table. Aspects: deliveries: two, kitting_table_0 then kitting_table_1; start: west floor, "
        "first walk away from the machine; robot: south start, south shelves, both tables, crossing at "
        "kitting_table_0. Expectation: the delivery under break_time admitted later than with no fact, near "
        "off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 100),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_04 = ScenarioConfig(
    id="scenario_s25_04",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 61),)),
    description=(
        "scenario_s25_04: script 046 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 61. Purpose: deliveries only: two, one "
        "to each table. Aspects: deliveries: two, kitting_table_0 then kitting_table_1; start: west floor, "
        "first walk away from the machine; robot: south start, south shelves, both tables, crossing at "
        "kitting_table_0. Expectation: the delivery under break_time admitted later than with no fact, near "
        "off. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 100),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 047: deliveries only: three, two to the east table, the last across to the west table
scenario_s25_05 = ScenarioConfig(
    id="scenario_s25_05",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_05: script 047 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: three, two to the east table, the last across to the west table. Aspects: "
        "deliveries: three, kitting_table_1 twice then kitting_table_0; start: east floor; robot: south-west "
        "start, west shelves to kitting_table_0, crossing only at that table. Expectation: on against off: "
        "each delivery admitted earlier or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, 200),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_06 = ScenarioConfig(
    id="scenario_s25_06",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_06: script 047 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: three, two to the east table, the last across to the west table. Aspects: "
        "deliveries: three, kitting_table_1 twice then kitting_table_0; start: east floor; robot: south-west "
        "start, west shelves to kitting_table_0, crossing only at that table. Expectation: on against off: "
        "each delivery admitted earlier or equal (the assigned tasks share most of the prior). working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, 200),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, -400),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_07 = ScenarioConfig(
    id="scenario_s25_07",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 28),)),
    description=(
        "scenario_s25_07: script 047 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 28. Purpose: deliveries only: three, "
        "two to the east table, the last across to the west table. Aspects: deliveries: three, "
        "kitting_table_1 twice then kitting_table_0; start: east floor; robot: south-west start, west "
        "shelves to kitting_table_0, crossing only at that table. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, 200),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_08 = ScenarioConfig(
    id="scenario_s25_08",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 28),)),
    description=(
        "scenario_s25_08: script 047 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 28. Purpose: deliveries only: three, "
        "two to the east table, the last across to the west table. Aspects: deliveries: three, "
        "kitting_table_1 twice then kitting_table_0; start: east floor; robot: south-west start, west "
        "shelves to kitting_table_0, crossing only at that table. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it; under "
        "the window the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, 200),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, -400),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 048: a coffee break at the start
scenario_s25_09 = ScenarioConfig(
    id="scenario_s25_09",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_09: script 048 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the start. Aspects: foreseeable: at the start; start: floor centre, "
        "first walk toward the machine; deliveries: both tables; robot: south-east start. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "a coffee break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, -100),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_10 = ScenarioConfig(
    id="scenario_s25_10",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_10: script 048 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the start. Aspects: foreseeable: at the start; start: floor centre, "
        "first walk toward the machine; deliveries: both tables; robot: south-east start. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "a coffee break admitted later than off (ordinary strength). working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, -100),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -400),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_11 = ScenarioConfig(
    id="scenario_s25_11",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 60),)),
    description=(
        "scenario_s25_11: script 048 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 0 to 60. Purpose: a coffee break at the start. Aspects: "
        "foreseeable: at the start; start: floor centre, first walk toward the machine; deliveries: both "
        "tables; robot: south-east start. Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; a delivery inside a window admitted later than with no "
        "fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, -100),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_12 = ScenarioConfig(
    id="scenario_s25_12",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 60),)),
    description=(
        "scenario_s25_12: script 048 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 0 to 60. Purpose: a coffee break at the start. "
        "Aspects: foreseeable: at the start; start: floor centre, first walk toward the machine; deliveries: "
        "both tables; robot: south-east start. Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; a delivery inside a window admitted later than with no "
        "fact. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; the coffee break admitted earlier, the "
        "robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, -100),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -400),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_13 = ScenarioConfig(
    id="scenario_s25_13",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 60, 145),)),
    description=(
        "scenario_s25_13: script 048 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 60 to 145. Purpose: a coffee break at the "
        "start. Aspects: foreseeable: at the start; start: floor centre, first walk toward the machine; "
        "deliveries: both tables; robot: south-east start. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose "
        "its admission to the raised coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, -100),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_14 = ScenarioConfig(
    id="scenario_s25_14",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 60, 145),)),
    description=(
        "scenario_s25_14: script 048 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 60 to 145. Purpose: a coffee break at the "
        "start. Aspects: foreseeable: at the start; start: floor centre, first walk toward the machine; "
        "deliveries: both tables; robot: south-east start. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off; a delivery whose walk heads toward the machine may lose "
        "its admission to the raised coffee break. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it; under "
        "the window the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, -100),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -400),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 049: a coffee break between two deliveries, the first a carry across the room
scenario_s25_15 = ScenarioConfig(
    id="scenario_s25_15",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_15: script 049 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break between two deliveries, the first a carry across the room. Aspects: "
        "foreseeable: between deliveries; deliveries: kitting_table_1 then kitting_table_0; start: west; "
        "robot: north-east start, east shelves to kitting_table_1, crossing at it. Expectation: on against "
        "off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee "
        "break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, -100),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_1"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_16 = ScenarioConfig(
    id="scenario_s25_16",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_16: script 049 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break between two deliveries, the first a carry across the room. Aspects: "
        "foreseeable: between deliveries; deliveries: kitting_table_1 then kitting_table_0; start: west; "
        "robot: north-east start, east shelves to kitting_table_1, crossing at it. Expectation: on against "
        "off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee "
        "break admitted later than off (ordinary strength). working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, -100),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_1"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, 300),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_17 = ScenarioConfig(
    id="scenario_s25_17",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 95, 168),)),
    description=(
        "scenario_s25_17: script 049 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 95 to 168. Purpose: a coffee break between two "
        "deliveries, the first a carry across the room. Aspects: foreseeable: between deliveries; "
        "deliveries: kitting_table_1 then kitting_table_0; start: west; robot: north-east start, east "
        "shelves to kitting_table_1, crossing at it. Expectation: the coffee break (raised by break_time) "
        "admitted earlier than off and than on with no fact; a delivery inside a window admitted later than "
        "with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, -100),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_1"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_18 = ScenarioConfig(
    id="scenario_s25_18",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 95, 168),)),
    description=(
        "scenario_s25_18: script 049 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 95 to 168. Purpose: a coffee break between two "
        "deliveries, the first a carry across the room. Aspects: foreseeable: between deliveries; "
        "deliveries: kitting_table_1 then kitting_table_0; start: west; robot: north-east start, east "
        "shelves to kitting_table_1, crossing at it. Expectation: the coffee break (raised by break_time) "
        "admitted earlier than off and than on with no fact; a delivery inside a window admitted later than "
        "with no fact. working robot: the decisions as off where no admission moves; an earlier admission of "
        "a delivery moves the response decision earlier or leaves it; the coffee break admitted earlier, the "
        "robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, -100),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_1"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, 300),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_19 = ScenarioConfig(
    id="scenario_s25_19",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 95),)),
    description=(
        "scenario_s25_19: script 049 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 95. Purpose: a coffee break between two "
        "deliveries, the first a carry across the room. Aspects: foreseeable: between deliveries; "
        "deliveries: kitting_table_1 then kitting_table_0; start: west; robot: north-east start, east "
        "shelves to kitting_table_1, crossing at it. Expectation: the delivery under break_time admitted "
        "later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, -100),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_1"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_20 = ScenarioConfig(
    id="scenario_s25_20",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 95),)),
    description=(
        "scenario_s25_20: script 049 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 95. Purpose: a coffee break between two "
        "deliveries, the first a carry across the room. Aspects: foreseeable: between deliveries; "
        "deliveries: kitting_table_1 then kitting_table_0; start: west; robot: north-east start, east "
        "shelves to kitting_table_1, crossing at it. Expectation: the delivery under break_time admitted "
        "later than with no fact, near off. working robot: the decisions as off where no admission moves; an "
        "earlier admission of a delivery moves the response decision earlier or leaves it; under the window "
        "the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, -100),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_1"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, 300),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 050: a coffee break inside a delivery after the grasp: from shelf_3 along the north wall to the machine
scenario_s25_21 = ScenarioConfig(
    id="scenario_s25_21",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_21: script 050 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery after the grasp: from shelf_3 along the north wall to the "
        "machine. Aspects: foreseeable: inside a delivery, after the grasp; start: east floor; robot: south, "
        "apart. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); a coffee break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 0),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_0", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_0", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_22 = ScenarioConfig(
    id="scenario_s25_22",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_22: script 050 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery after the grasp: from shelf_3 along the north wall to the "
        "machine. Aspects: foreseeable: inside a delivery, after the grasp; start: east floor; robot: south, "
        "apart. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); a coffee break admitted later than off (ordinary strength). working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 0),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_0", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_0", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_23 = ScenarioConfig(
    id="scenario_s25_23",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 32, 110),)),
    description=(
        "scenario_s25_23: script 050 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 32 to 110. Purpose: a coffee break inside a delivery "
        "after the grasp: from shelf_3 along the north wall to the machine. Aspects: foreseeable: inside a "
        "delivery, after the grasp; start: east floor; robot: south, apart. Expectation: the coffee break "
        "(raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a "
        "window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 0),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_0", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_0", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_24 = ScenarioConfig(
    id="scenario_s25_24",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 32, 110),)),
    description=(
        "scenario_s25_24: script 050 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 32 to 110. Purpose: a coffee break inside a delivery "
        "after the grasp: from shelf_3 along the north wall to the machine. Aspects: foreseeable: inside a "
        "delivery, after the grasp; start: east floor; robot: south, apart. Expectation: the coffee break "
        "(raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a "
        "window admitted later than with no fact. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it; the "
        "coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 0),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_0", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_0", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_25 = ScenarioConfig(
    id="scenario_s25_25",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 154, 276),)),
    description=(
        "scenario_s25_25: script 050 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 154 to 276. Purpose: a coffee break inside a "
        "delivery after the grasp: from shelf_3 along the north wall to the machine. Aspects: foreseeable: "
        "inside a delivery, after the grasp; start: east floor; robot: south, apart. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 0),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_0", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_0", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_26 = ScenarioConfig(
    id="scenario_s25_26",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 154, 276),)),
    description=(
        "scenario_s25_26: script 050 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 154 to 276. Purpose: a coffee break inside a "
        "delivery after the grasp: from shelf_3 along the north wall to the machine. Aspects: foreseeable: "
        "inside a delivery, after the grasp; start: east floor; robot: south, apart. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off. working robot: the decisions "
        "as off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it; under the window the delivery's admission and the robot's decision on it "
        "later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 0),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_0", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_0", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 051: a second coffee break soon after the first
scenario_s25_27 = ScenarioConfig(
    id="scenario_s25_27",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_27: script 051 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a second coffee break soon after the first. Aspects: foreseeable: two coffee breaks, "
        "between and at the end; deliveries: both tables. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted "
        "later than off (ordinary strength); the second under its recency fact (suppressed), later still."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 300),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_28 = ScenarioConfig(
    id="scenario_s25_28",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_28: script 051 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a second coffee break soon after the first. Aspects: foreseeable: two coffee breaks, "
        "between and at the end; deliveries: both tables. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted "
        "later than off (ordinary strength); the second under its recency fact (suppressed), later still. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 300),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, -400),
            assigned_tasks=[
                deliver_item("item_7", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_29 = ScenarioConfig(
    id="scenario_s25_29",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 56, 136), window(BREAK_TIME, 274, 347),)),
    description=(
        "scenario_s25_29: script 051 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 56 to 136, break_time from 274 to 347. Purpose: a second "
        "coffee break soon after the first. Aspects: foreseeable: two coffee breaks, between and at the end; "
        "deliveries: both tables. Expectation: the coffee break (raised by break_time) admitted earlier than "
        "off and than on with no fact; the second one suppressed by its recency fact, the window gives it "
        "nothing; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 300),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_30 = ScenarioConfig(
    id="scenario_s25_30",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 56, 136), window(BREAK_TIME, 274, 347),)),
    description=(
        "scenario_s25_30: script 051 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 56 to 136, break_time from 274 to 347. Purpose: a "
        "second coffee break soon after the first. Aspects: foreseeable: two coffee breaks, between and at "
        "the end; deliveries: both tables. Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; the second one suppressed by its recency fact, the "
        "window gives it nothing; a delivery inside a window admitted later than with no fact. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; the coffee break admitted earlier, the robot's decision "
        "against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 300),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, -400),
            assigned_tasks=[
                deliver_item("item_7", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_31 = ScenarioConfig(
    id="scenario_s25_31",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 56),)),
    description=(
        "scenario_s25_31: script 051 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 56. Purpose: a second coffee break soon "
        "after the first. Aspects: foreseeable: two coffee breaks, between and at the end; deliveries: both "
        "tables. Expectation: the delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 300),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_32 = ScenarioConfig(
    id="scenario_s25_32",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 56),)),
    description=(
        "scenario_s25_32: script 051 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 56. Purpose: a second coffee break soon "
        "after the first. Aspects: foreseeable: two coffee breaks, between and at the end; deliveries: both "
        "tables. Expectation: the delivery under break_time admitted later than with no fact, near off. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it; under the window the delivery's admission and the "
        "robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 300),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, -400),
            assigned_tasks=[
                deliver_item("item_7", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 052: a coffee break at the end
scenario_s25_33 = ScenarioConfig(
    id="scenario_s25_33",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_33: script 052 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the end. Aspects: foreseeable: at the end; deliveries: kitting_table_0 "
        "(across) then kitting_table_1; robot: north-west start, item_2 across the room, crossing. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior); a coffee break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, -300),
            scheduled_tasks=Script([
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_34 = ScenarioConfig(
    id="scenario_s25_34",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_34: script 052 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the end. Aspects: foreseeable: at the end; deliveries: kitting_table_0 "
        "(across) then kitting_table_1; robot: north-west start, item_2 across the room, crossing. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior); a coffee break admitted later than off (ordinary strength). working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, -300),
            scheduled_tasks=Script([
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, 300),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_35 = ScenarioConfig(
    id="scenario_s25_35",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 194, 269),)),
    description=(
        "scenario_s25_35: script 052 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 194 to 269. Purpose: a coffee break at the end. Aspects: "
        "foreseeable: at the end; deliveries: kitting_table_0 (across) then kitting_table_1; robot: "
        "north-west start, item_2 across the room, crossing. Expectation: the coffee break (raised by "
        "break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted "
        "later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, -300),
            scheduled_tasks=Script([
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_36 = ScenarioConfig(
    id="scenario_s25_36",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 194, 269),)),
    description=(
        "scenario_s25_36: script 052 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 194 to 269. Purpose: a coffee break at the end. "
        "Aspects: foreseeable: at the end; deliveries: kitting_table_0 (across) then kitting_table_1; robot: "
        "north-west start, item_2 across the room, crossing. Expectation: the coffee break (raised by "
        "break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted "
        "later than with no fact. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; the coffee break admitted "
        "earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, -300),
            scheduled_tasks=Script([
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, 300),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_37 = ScenarioConfig(
    id="scenario_s25_37",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 97),)),
    description=(
        "scenario_s25_37: script 052 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 97. Purpose: a coffee break at the end. "
        "Aspects: foreseeable: at the end; deliveries: kitting_table_0 (across) then kitting_table_1; robot: "
        "north-west start, item_2 across the room, crossing. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, -300),
            scheduled_tasks=Script([
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_38 = ScenarioConfig(
    id="scenario_s25_38",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 97),)),
    description=(
        "scenario_s25_38: script 052 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 97. Purpose: a coffee break at the end. "
        "Aspects: foreseeable: at the end; deliveries: kitting_table_0 (across) then kitting_table_1; robot: "
        "north-west start, item_2 across the room, crossing. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it; under "
        "the window the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, -300),
            scheduled_tasks=Script([
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, 300),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 053: unmodelled alone: a stand of 40 ticks at kitting_table_1 between deliveries
scenario_s25_39 = ScenarioConfig(
    id="scenario_s25_39",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_39: script 053 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a stand of 40 ticks at kitting_table_1 between deliveries. Aspects: "
        "unmodelled: a stand (40 ticks), between deliveries; robot: south start, item_7 to kitting_table_1 "
        "while the human stands there. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, "
        "except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -150),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1"),
                stand("PT80S"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_40 = ScenarioConfig(
    id="scenario_s25_40",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_40: script 053 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a stand of 40 ticks at kitting_table_1 between deliveries. Aspects: "
        "unmodelled: a stand (40 ticks), between deliveries; robot: south start, item_7 to kitting_table_1 "
        "while the human stands there. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, "
        "except a hypothesis whose target lies on the walk. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -150),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1"),
                stand("PT80S"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_41 = ScenarioConfig(
    id="scenario_s25_41",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 57),)),
    description=(
        "scenario_s25_41: script 053 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 57. Purpose: unmodelled alone: a stand "
        "of 40 ticks at kitting_table_1 between deliveries. Aspects: unmodelled: a stand (40 ticks), between "
        "deliveries; robot: south start, item_7 to kitting_table_1 while the human stands there. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off; no admission "
        "during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -150),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1"),
                stand("PT80S"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_42 = ScenarioConfig(
    id="scenario_s25_42",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 57),)),
    description=(
        "scenario_s25_42: script 053 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 57. Purpose: unmodelled alone: a stand "
        "of 40 ticks at kitting_table_1 between deliveries. Aspects: unmodelled: a stand (40 ticks), between "
        "deliveries; robot: south start, item_7 to kitting_table_1 while the human stands there. "
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
            start_position=(900, -150),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1"),
                stand("PT80S"),
                deliver_item("item_4", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 054: unmodelled with a foreseeable task: a delivery abandoned at shelf_1 before the grasp, then a coffee break
scenario_s25_43 = ScenarioConfig(
    id="scenario_s25_43",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_43: script 054 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery abandoned at shelf_1 before the grasp, then "
        "a coffee break. Aspects: unmodelled: an abandoned delivery (before the grasp); foreseeable: right "
        "after; robot: north-east start, to kitting_table_1. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted "
        "later than off (ordinary strength); the abandoned delivery admitted while the human walks to it, "
        "then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 0),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_44 = ScenarioConfig(
    id="scenario_s25_44",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_44: script 054 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery abandoned at shelf_1 before the grasp, then "
        "a coffee break. Aspects: unmodelled: an abandoned delivery (before the grasp); foreseeable: right "
        "after; robot: north-east start, to kitting_table_1. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted "
        "later than off (ordinary strength); the abandoned delivery admitted while the human walks to it, "
        "then retracted as the evidence turns. working robot: the decisions as off where no admission moves; "
        "an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 0),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, 400),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_45 = ScenarioConfig(
    id="scenario_s25_45",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 32, 128),)),
    description=(
        "scenario_s25_45: script 054 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 32 to 128. Purpose: unmodelled with a foreseeable task: "
        "a delivery abandoned at shelf_1 before the grasp, then a coffee break. Aspects: unmodelled: an "
        "abandoned delivery (before the grasp); foreseeable: right after; robot: north-east start, to "
        "kitting_table_1. Expectation: the coffee break (raised by break_time) admitted earlier than off and "
        "than on with no fact; a delivery inside a window admitted later than with no fact; the abandoned "
        "delivery admitted while the human walks to it, then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 0),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_46 = ScenarioConfig(
    id="scenario_s25_46",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 32, 128),)),
    description=(
        "scenario_s25_46: script 054 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 32 to 128. Purpose: unmodelled with a foreseeable "
        "task: a delivery abandoned at shelf_1 before the grasp, then a coffee break. Aspects: unmodelled: "
        "an abandoned delivery (before the grasp); foreseeable: right after; robot: north-east start, to "
        "kitting_table_1. Expectation: the coffee break (raised by break_time) admitted earlier than off and "
        "than on with no fact; a delivery inside a window admitted later than with no fact; the abandoned "
        "delivery admitted while the human walks to it, then retracted as the evidence turns. working robot: "
        "the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; the coffee break admitted earlier, the robot's decision "
        "against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 0),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, 400),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_47 = ScenarioConfig(
    id="scenario_s25_47",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 128, 197),)),
    description=(
        "scenario_s25_47: script 054 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 128 to 197. Purpose: unmodelled with a "
        "foreseeable task: a delivery abandoned at shelf_1 before the grasp, then a coffee break. Aspects: "
        "unmodelled: an abandoned delivery (before the grasp); foreseeable: right after; robot: north-east "
        "start, to kitting_table_1. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off; the abandoned delivery admitted while the human walks to it, then retracted as the "
        "evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 0),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_48 = ScenarioConfig(
    id="scenario_s25_48",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 128, 197),)),
    description=(
        "scenario_s25_48: script 054 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 128 to 197. Purpose: unmodelled with a "
        "foreseeable task: a delivery abandoned at shelf_1 before the grasp, then a coffee break. Aspects: "
        "unmodelled: an abandoned delivery (before the grasp); foreseeable: right after; robot: north-east "
        "start, to kitting_table_1. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off; the abandoned delivery admitted while the human walks to it, then retracted as the "
        "evidence turns. working robot: the decisions as off where no admission moves; an earlier admission "
        "of a delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 0),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, 400),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 055: unmodelled alone: a delivery to the other table (item_6 to kitting_table_1, designated kitting_table_0), and a never-started delivery
scenario_s25_49 = ScenarioConfig(
    id="scenario_s25_49",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_49: script 055 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a delivery to the other table (item_6 to kitting_table_1, designated "
        "kitting_table_0), and a never-started delivery. Aspects: unmodelled: a delivery to the other table, "
        "a never-started delivery; robot: to kitting_table_1, where the human delivers twice. Expectation: "
        "on against off: each delivery admitted earlier or equal (the assigned tasks share most of the "
        "prior); the never-started delivery never admitted (no observation warrant); the delivery to the "
        "other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis "
        "admitted there."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -300),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_1"),
                deliver_item("item_2", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_1"),
                deliver_item("item_0", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_50 = ScenarioConfig(
    id="scenario_s25_50",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s25_50: script 055 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a delivery to the other table (item_6 to kitting_table_1, designated "
        "kitting_table_0), and a never-started delivery. Aspects: unmodelled: a delivery to the other table, "
        "a never-started delivery; robot: to kitting_table_1, where the human delivers twice. Expectation: "
        "on against off: each delivery admitted earlier or equal (the assigned tasks share most of the "
        "prior); the never-started delivery never admitted (no observation warrant); the delivery to the "
        "other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis "
        "admitted there. working robot: the decisions as off where no admission moves; an earlier admission "
        "of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -300),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_1"),
                deliver_item("item_2", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_1"),
                deliver_item("item_0", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(800, 300),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_51 = ScenarioConfig(
    id="scenario_s25_51",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 78, 246),)),
    description=(
        "scenario_s25_51: script 055 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 78 to 246. Purpose: unmodelled alone: a "
        "delivery to the other table (item_6 to kitting_table_1, designated kitting_table_0), and a "
        "never-started delivery. Aspects: unmodelled: a delivery to the other table, a never-started "
        "delivery; robot: to kitting_table_1, where the human delivers twice. Expectation: the delivery "
        "under break_time admitted later than with no fact, near off; the never-started delivery never "
        "admitted (no observation warrant); the delivery to the other table: admitted on the walk to the "
        "shelf, then its carry unexplained; no other hypothesis admitted there."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -300),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_1"),
                deliver_item("item_2", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_1"),
                deliver_item("item_0", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 250),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s25_52 = ScenarioConfig(
    id="scenario_s25_52",
    setup="env_setup_25",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 78, 246),)),
    description=(
        "scenario_s25_52: script 055 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 78 to 246. Purpose: unmodelled alone: a "
        "delivery to the other table (item_6 to kitting_table_1, designated kitting_table_0), and a "
        "never-started delivery. Aspects: unmodelled: a delivery to the other table, a never-started "
        "delivery; robot: to kitting_table_1, where the human delivers twice. Expectation: the delivery "
        "under break_time admitted later than with no fact, near off; the never-started delivery never "
        "admitted (no observation warrant); the delivery to the other table: admitted on the walk to the "
        "shelf, then its carry unexplained; no other hypothesis admitted there. working robot: the decisions "
        "as off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it; under the window the delivery's admission and the robot's decision on it "
        "later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -300),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_1"),
                deliver_item("item_2", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_1"),
                deliver_item("item_0", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(800, 300),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)
