# domains/kitting/scenarios/scenarios_s22.py
"""
Kitting scenarios on env_setup_22: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_06; the shift
env_setup_22: a second shift: the human's parts on the east shelves (shelf_2, shelf_7) and shelf_6, the robot's on the two middle shelves.
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

# ---- script 030: deliveries only: three
scenario_s22_01 = ScenarioConfig(
    id="scenario_s22_01",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s22_01: script 030 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: three. Aspects: deliveries: three, east, south-east, south-west; robot: "
        "south-west start, the middle shelves. Expectation: on against off: each delivery admitted earlier "
        "or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 350),
            scheduled_tasks=Script([
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_42", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_42", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 100),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_02 = ScenarioConfig(
    id="scenario_s22_02",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s22_02: script 030 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: three. Aspects: deliveries: three, east, south-east, south-west; robot: "
        "south-west start, the middle shelves. Expectation: on against off: each delivery admitted earlier "
        "or equal (the assigned tasks share most of the prior). working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 350),
            scheduled_tasks=Script([
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_42", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_42", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, -400),
            assigned_tasks=[
                deliver_item("item_44", table="kitting_table_0"),
                deliver_item("item_45", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_03 = ScenarioConfig(
    id="scenario_s22_03",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 65),)),
    description=(
        "scenario_s22_03: script 030 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 65. Purpose: deliveries only: three. "
        "Aspects: deliveries: three, east, south-east, south-west; robot: south-west start, the middle "
        "shelves. Expectation: the delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 350),
            scheduled_tasks=Script([
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_42", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_42", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 100),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_04 = ScenarioConfig(
    id="scenario_s22_04",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 65),)),
    description=(
        "scenario_s22_04: script 030 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 65. Purpose: deliveries only: three. "
        "Aspects: deliveries: three, east, south-east, south-west; robot: south-west start, the middle "
        "shelves. Expectation: the delivery under break_time admitted later than with no fact, near off. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it; under the window the delivery's admission and the "
        "robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 350),
            scheduled_tasks=Script([
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_42", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_42", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, -400),
            assigned_tasks=[
                deliver_item("item_44", table="kitting_table_0"),
                deliver_item("item_45", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 031: a second coffee break soon after the first
scenario_s22_05 = ScenarioConfig(
    id="scenario_s22_05",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s22_05: script 031 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a second coffee break soon after the first. Aspects: foreseeable: two coffee breaks, "
        "between and at the end. Expectation: on against off: each delivery admitted earlier or equal (the "
        "assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength); the second under its recency fact (suppressed), later still."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_42", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_41", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_42", table="kitting_table_0"),
                deliver_item("item_41", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 100),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_06 = ScenarioConfig(
    id="scenario_s22_06",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s22_06: script 031 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a second coffee break soon after the first. Aspects: foreseeable: two coffee breaks, "
        "between and at the end. Expectation: on against off: each delivery admitted earlier or equal (the "
        "assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength); the second under its recency fact (suppressed), later still. working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_42", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_41", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_42", table="kitting_table_0"),
                deliver_item("item_41", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, -400),
            assigned_tasks=[
                deliver_item("item_44", table="kitting_table_0"),
                deliver_item("item_45", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_07 = ScenarioConfig(
    id="scenario_s22_07",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 97, 152), window(BREAK_TIME, 212, 267),)),
    description=(
        "scenario_s22_07: script 031 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 97 to 152, break_time from 212 to 267. Purpose: a second "
        "coffee break soon after the first. Aspects: foreseeable: two coffee breaks, between and at the end. "
        "Expectation: the coffee break (raised by break_time) admitted earlier than off and than on with no "
        "fact; the second one suppressed by its recency fact, the window gives it nothing; a delivery inside "
        "a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_42", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_41", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_42", table="kitting_table_0"),
                deliver_item("item_41", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 100),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_08 = ScenarioConfig(
    id="scenario_s22_08",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 97, 152), window(BREAK_TIME, 212, 267),)),
    description=(
        "scenario_s22_08: script 031 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 97 to 152, break_time from 212 to 267. Purpose: a "
        "second coffee break soon after the first. Aspects: foreseeable: two coffee breaks, between and at "
        "the end. Expectation: the coffee break (raised by break_time) admitted earlier than off and than on "
        "with no fact; the second one suppressed by its recency fact, the window gives it nothing; a "
        "delivery inside a window admitted later than with no fact. working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_42", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_41", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_42", table="kitting_table_0"),
                deliver_item("item_41", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, -400),
            assigned_tasks=[
                deliver_item("item_44", table="kitting_table_0"),
                deliver_item("item_45", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_09 = ScenarioConfig(
    id="scenario_s22_09",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 97),)),
    description=(
        "scenario_s22_09: script 031 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 97. Purpose: a second coffee break soon "
        "after the first. Aspects: foreseeable: two coffee breaks, between and at the end. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_42", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_41", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_42", table="kitting_table_0"),
                deliver_item("item_41", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 100),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_10 = ScenarioConfig(
    id="scenario_s22_10",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 97),)),
    description=(
        "scenario_s22_10: script 031 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 97. Purpose: a second coffee break soon "
        "after the first. Aspects: foreseeable: two coffee breaks, between and at the end. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off. working robot: the decisions "
        "as off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it; under the window the delivery's admission and the robot's decision on it "
        "later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_42", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_41", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_42", table="kitting_table_0"),
                deliver_item("item_41", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, -400),
            assigned_tasks=[
                deliver_item("item_44", table="kitting_table_0"),
                deliver_item("item_45", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 032: unmodelled with a foreseeable task: a delivery abandoned at shelf_6 before the grasp, then a coffee break
scenario_s22_11 = ScenarioConfig(
    id="scenario_s22_11",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s22_11: script 032 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery abandoned at shelf_6 before the grasp, then "
        "a coffee break. Aspects: unmodelled: an abandoned delivery (before the grasp); foreseeable: right "
        "after; robot: south-east start. Expectation: on against off: each delivery admitted earlier or "
        "equal (the assigned tasks share most of the prior); a coffee break admitted later than off "
        "(ordinary strength); the abandoned delivery admitted while the human walks to it, then retracted as "
        "the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, 200),
            scheduled_tasks=Script([
                deliver_item("item_43", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_41", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_43", table="kitting_table_0"),
                deliver_item("item_41", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 100),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_12 = ScenarioConfig(
    id="scenario_s22_12",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s22_12: script 032 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery abandoned at shelf_6 before the grasp, then "
        "a coffee break. Aspects: unmodelled: an abandoned delivery (before the grasp); foreseeable: right "
        "after; robot: south-east start. Expectation: on against off: each delivery admitted earlier or "
        "equal (the assigned tasks share most of the prior); a coffee break admitted later than off "
        "(ordinary strength); the abandoned delivery admitted while the human walks to it, then retracted as "
        "the evidence turns. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, 200),
            scheduled_tasks=Script([
                deliver_item("item_43", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_41", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_43", table="kitting_table_0"),
                deliver_item("item_41", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, -300),
            assigned_tasks=[
                deliver_item("item_44", table="kitting_table_0"),
                deliver_item("item_45", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_13 = ScenarioConfig(
    id="scenario_s22_13",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 23, 113),)),
    description=(
        "scenario_s22_13: script 032 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 23 to 113. Purpose: unmodelled with a foreseeable task: "
        "a delivery abandoned at shelf_6 before the grasp, then a coffee break. Aspects: unmodelled: an "
        "abandoned delivery (before the grasp); foreseeable: right after; robot: south-east start. "
        "Expectation: the coffee break (raised by break_time) admitted earlier than off and than on with no "
        "fact; a delivery inside a window admitted later than with no fact; the abandoned delivery admitted "
        "while the human walks to it, then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, 200),
            scheduled_tasks=Script([
                deliver_item("item_43", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_41", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_43", table="kitting_table_0"),
                deliver_item("item_41", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 100),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_14 = ScenarioConfig(
    id="scenario_s22_14",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 23, 113),)),
    description=(
        "scenario_s22_14: script 032 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 23 to 113. Purpose: unmodelled with a foreseeable "
        "task: a delivery abandoned at shelf_6 before the grasp, then a coffee break. Aspects: unmodelled: "
        "an abandoned delivery (before the grasp); foreseeable: right after; robot: south-east start. "
        "Expectation: the coffee break (raised by break_time) admitted earlier than off and than on with no "
        "fact; a delivery inside a window admitted later than with no fact; the abandoned delivery admitted "
        "while the human walks to it, then retracted as the evidence turns. working robot: the decisions as "
        "off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, 200),
            scheduled_tasks=Script([
                deliver_item("item_43", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_41", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_43", table="kitting_table_0"),
                deliver_item("item_41", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, -300),
            assigned_tasks=[
                deliver_item("item_44", table="kitting_table_0"),
                deliver_item("item_45", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_15 = ScenarioConfig(
    id="scenario_s22_15",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 113, 173),)),
    description=(
        "scenario_s22_15: script 032 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 113 to 173. Purpose: unmodelled with a "
        "foreseeable task: a delivery abandoned at shelf_6 before the grasp, then a coffee break. Aspects: "
        "unmodelled: an abandoned delivery (before the grasp); foreseeable: right after; robot: south-east "
        "start. Expectation: the delivery under break_time admitted later than with no fact, near off; the "
        "abandoned delivery admitted while the human walks to it, then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, 200),
            scheduled_tasks=Script([
                deliver_item("item_43", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_41", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_43", table="kitting_table_0"),
                deliver_item("item_41", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 100),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_16 = ScenarioConfig(
    id="scenario_s22_16",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 113, 173),)),
    description=(
        "scenario_s22_16: script 032 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 113 to 173. Purpose: unmodelled with a "
        "foreseeable task: a delivery abandoned at shelf_6 before the grasp, then a coffee break. Aspects: "
        "unmodelled: an abandoned delivery (before the grasp); foreseeable: right after; robot: south-east "
        "start. Expectation: the delivery under break_time admitted later than with no fact, near off; the "
        "abandoned delivery admitted while the human walks to it, then retracted as the evidence turns. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it; under the window the delivery's admission and the "
        "robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, 200),
            scheduled_tasks=Script([
                deliver_item("item_43", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_41", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_43", table="kitting_table_0"),
                deliver_item("item_41", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, -300),
            assigned_tasks=[
                deliver_item("item_44", table="kitting_table_0"),
                deliver_item("item_45", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 033: a stand of 20 ticks at the table, then a coffee break at the end
scenario_s22_17 = ScenarioConfig(
    id="scenario_s22_17",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s22_17: script 033 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a stand of 20 ticks at the table, then a coffee break at the end. Aspects: unmodelled: a "
        "stand (20 ticks); foreseeable: at the end, right after it. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength); no admission during the stand or the walk elsewhere, "
        "except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 350),
            scheduled_tasks=Script([
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
                stand("PT40S"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 100),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_18 = ScenarioConfig(
    id="scenario_s22_18",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s22_18: script 033 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a stand of 20 ticks at the table, then a coffee break at the end. Aspects: unmodelled: a "
        "stand (20 ticks); foreseeable: at the end, right after it. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength); no admission during the stand or the walk elsewhere, "
        "except a hypothesis whose target lies on the walk. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 350),
            scheduled_tasks=Script([
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
                stand("PT40S"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, -400),
            assigned_tasks=[
                deliver_item("item_44", table="kitting_table_0"),
                deliver_item("item_45", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_19 = ScenarioConfig(
    id="scenario_s22_19",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 171, 228),)),
    description=(
        "scenario_s22_19: script 033 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 171 to 228. Purpose: a stand of 20 ticks at the table, "
        "then a coffee break at the end. Aspects: unmodelled: a stand (20 ticks); foreseeable: at the end, "
        "right after it. Expectation: the coffee break (raised by break_time) admitted earlier than off and "
        "than on with no fact; a delivery inside a window admitted later than with no fact; no admission "
        "during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 350),
            scheduled_tasks=Script([
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
                stand("PT40S"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 100),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_20 = ScenarioConfig(
    id="scenario_s22_20",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 171, 228),)),
    description=(
        "scenario_s22_20: script 033 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 171 to 228. Purpose: a stand of 20 ticks at the "
        "table, then a coffee break at the end. Aspects: unmodelled: a stand (20 ticks); foreseeable: at the "
        "end, right after it. Expectation: the coffee break (raised by break_time) admitted earlier than off "
        "and than on with no fact; a delivery inside a window admitted later than with no fact; no admission "
        "during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; the coffee break admitted earlier, the robot's decision "
        "against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 350),
            scheduled_tasks=Script([
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
                stand("PT40S"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, -400),
            assigned_tasks=[
                deliver_item("item_44", table="kitting_table_0"),
                deliver_item("item_45", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_21 = ScenarioConfig(
    id="scenario_s22_21",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 65),)),
    description=(
        "scenario_s22_21: script 033 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 65. Purpose: a stand of 20 ticks at the "
        "table, then a coffee break at the end. Aspects: unmodelled: a stand (20 ticks); foreseeable: at the "
        "end, right after it. Expectation: the delivery under break_time admitted later than with no fact, "
        "near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target "
        "lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 350),
            scheduled_tasks=Script([
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
                stand("PT40S"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 100),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_22 = ScenarioConfig(
    id="scenario_s22_22",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 65),)),
    description=(
        "scenario_s22_22: script 033 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 65. Purpose: a stand of 20 ticks at the "
        "table, then a coffee break at the end. Aspects: unmodelled: a stand (20 ticks); foreseeable: at the "
        "end, right after it. Expectation: the delivery under break_time admitted later than with no fact, "
        "near off; no admission during the stand or the walk elsewhere, except a hypothesis whose target "
        "lies on the walk. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; under the window the "
        "delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 350),
            scheduled_tasks=Script([
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
                stand("PT40S"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, -400),
            assigned_tasks=[
                deliver_item("item_44", table="kitting_table_0"),
                deliver_item("item_45", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 034: deliveries only, the first approach heading toward the coffee machine: from the south-east, shelf_2 lies 7 deg off the machine's bearing
scenario_s22_23 = ScenarioConfig(
    id="scenario_s22_23",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s22_23: script 034 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only, the first approach heading toward the coffee machine: from the "
        "south-east, shelf_2 lies 7 deg off the machine's bearing. Aspects: deliveries: two; start: "
        "south-east, first walk toward the machine; robot: north-west start. Expectation: on against off: "
        "each delivery admitted earlier or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -350),
            scheduled_tasks=Script([
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 100),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_24 = ScenarioConfig(
    id="scenario_s22_24",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s22_24: script 034 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only, the first approach heading toward the coffee machine: from the "
        "south-east, shelf_2 lies 7 deg off the machine's bearing. Aspects: deliveries: two; start: "
        "south-east, first walk toward the machine; robot: north-west start. Expectation: on against off: "
        "each delivery admitted earlier or equal (the assigned tasks share most of the prior). working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -350),
            scheduled_tasks=Script([
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 400),
            assigned_tasks=[
                deliver_item("item_44", table="kitting_table_0"),
                deliver_item("item_45", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_25 = ScenarioConfig(
    id="scenario_s22_25",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 50),)),
    description=(
        "scenario_s22_25: script 034 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 50. Purpose: deliveries only, the first "
        "approach heading toward the coffee machine: from the south-east, shelf_2 lies 7 deg off the "
        "machine's bearing. Aspects: deliveries: two; start: south-east, first walk toward the machine; "
        "robot: north-west start. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised "
        "coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -350),
            scheduled_tasks=Script([
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 100),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s22_26 = ScenarioConfig(
    id="scenario_s22_26",
    setup="env_setup_22",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 50),)),
    description=(
        "scenario_s22_26: script 034 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 50. Purpose: deliveries only, the first "
        "approach heading toward the coffee machine: from the south-east, shelf_2 lies 7 deg off the "
        "machine's bearing. Aspects: deliveries: two; start: south-east, first walk toward the machine; "
        "robot: north-west start. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off; a delivery whose walk heads toward the machine may lose its admission to the raised "
        "coffee break. working robot: the decisions as off where no admission moves; an earlier admission of "
        "a delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -350),
            scheduled_tasks=Script([
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_41", table="kitting_table_0"),
                deliver_item("item_43", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-550, 400),
            assigned_tasks=[
                deliver_item("item_44", table="kitting_table_0"),
                deliver_item("item_45", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)
