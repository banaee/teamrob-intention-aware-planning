# domains/kitting/scenarios/scenarios_s20.py
"""
Kitting scenarios on env_setup_20: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_05; the shift
env_setup_20: a second shift: two parts on shelf_3 (one the human's, one the robot's), the human's others on the south-east and east shelves.
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

# ---- script 019: deliveries only: three, the robot's first part on the human's first shelf
scenario_s20_01 = ScenarioConfig(
    id="scenario_s20_01",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s20_01: script 019 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: three, the robot's first part on the human's first shelf. Aspects: "
        "deliveries: three; robot: west start, its first part on the human's shelf_3, crossing. Expectation: "
        "on against off: each delivery admitted earlier or equal (the assigned tasks share most of the "
        "prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 300),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_02 = ScenarioConfig(
    id="scenario_s20_02",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s20_02: script 019 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: three, the robot's first part on the human's first shelf. Aspects: "
        "deliveries: three; robot: west start, its first part on the human's shelf_3, crossing. Expectation: "
        "on against off: each delivery admitted earlier or equal (the assigned tasks share most of the "
        "prior). working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 300),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, 0),
            assigned_tasks=[
                deliver_item("item_36", table="kitting_table_0"),
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_03 = ScenarioConfig(
    id="scenario_s20_03",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 109),)),
    description=(
        "scenario_s20_03: script 019 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 109. Purpose: deliveries only: three, "
        "the robot's first part on the human's first shelf. Aspects: deliveries: three; robot: west start, "
        "its first part on the human's shelf_3, crossing. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 300),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_04 = ScenarioConfig(
    id="scenario_s20_04",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 109),)),
    description=(
        "scenario_s20_04: script 019 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 109. Purpose: deliveries only: three, "
        "the robot's first part on the human's first shelf. Aspects: deliveries: three; robot: west start, "
        "its first part on the human's shelf_3, crossing. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it; under "
        "the window the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 300),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, 0),
            assigned_tasks=[
                deliver_item("item_36", table="kitting_table_0"),
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_05 = ScenarioConfig(
    id="scenario_s20_05",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(ROOM_WARM, 0, 109),)),
    description=(
        "scenario_s20_05: script 019 of step 5e, the idle robot, its own timeline, room_warm over a delivery "
        "(the human works through it): room_warm from 0 to 109. Purpose: deliveries only: three, the robot's "
        "first part on the human's first shelf. Aspects: deliveries: three; robot: west start, its first "
        "part on the human's shelf_3, crossing. Expectation: the delivery under room_warm admitted later "
        "than with no fact, by less than under break_time (raised 0.5 against 2)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 300),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_06 = ScenarioConfig(
    id="scenario_s20_06",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(ROOM_WARM, 0, 109),)),
    description=(
        "scenario_s20_06: script 019 of step 5e, the working robot, its own timeline, room_warm over a "
        "delivery (the human works through it): room_warm from 0 to 109. Purpose: deliveries only: three, "
        "the robot's first part on the human's first shelf. Aspects: deliveries: three; robot: west start, "
        "its first part on the human's shelf_3, crossing. Expectation: the delivery under room_warm admitted "
        "later than with no fact, by less than under break_time (raised 0.5 against 2). working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 300),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, 0),
            assigned_tasks=[
                deliver_item("item_36", table="kitting_table_0"),
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 020: a coffee break at the end
scenario_s20_07 = ScenarioConfig(
    id="scenario_s20_07",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s20_07: script 020 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the end. Aspects: foreseeable: at the end; start: north-east; robot: "
        "south-west start. Expectation: on against off: each delivery admitted earlier or equal (the "
        "assigned tasks share most of the prior); a coffee break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(600, 500),
            scheduled_tasks=Script([
                deliver_item("item_33", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_08 = ScenarioConfig(
    id="scenario_s20_08",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s20_08: script 020 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the end. Aspects: foreseeable: at the end; start: north-east; robot: "
        "south-west start. Expectation: on against off: each delivery admitted earlier or equal (the "
        "assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength). working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(600, 500),
            scheduled_tasks=Script([
                deliver_item("item_33", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, -400),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_09 = ScenarioConfig(
    id="scenario_s20_09",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 211, 279),)),
    description=(
        "scenario_s20_09: script 020 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 211 to 279. Purpose: a coffee break at the end. Aspects: "
        "foreseeable: at the end; start: north-east; robot: south-west start. Expectation: the coffee break "
        "(raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a "
        "window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(600, 500),
            scheduled_tasks=Script([
                deliver_item("item_33", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_10 = ScenarioConfig(
    id="scenario_s20_10",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 211, 279),)),
    description=(
        "scenario_s20_10: script 020 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 211 to 279. Purpose: a coffee break at the end. "
        "Aspects: foreseeable: at the end; start: north-east; robot: south-west start. Expectation: the "
        "coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery "
        "inside a window admitted later than with no fact. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(600, 500),
            scheduled_tasks=Script([
                deliver_item("item_33", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, -400),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_11 = ScenarioConfig(
    id="scenario_s20_11",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 98),)),
    description=(
        "scenario_s20_11: script 020 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 98. Purpose: a coffee break at the end. "
        "Aspects: foreseeable: at the end; start: north-east; robot: south-west start. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(600, 500),
            scheduled_tasks=Script([
                deliver_item("item_33", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_12 = ScenarioConfig(
    id="scenario_s20_12",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 98),)),
    description=(
        "scenario_s20_12: script 020 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 98. Purpose: a coffee break at the end. "
        "Aspects: foreseeable: at the end; start: north-east; robot: south-west start. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off. working robot: the decisions "
        "as off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it; under the window the delivery's admission and the robot's decision on it "
        "later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(600, 500),
            scheduled_tasks=Script([
                deliver_item("item_33", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, -400),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 021: a coffee break and the A/C activation together between deliveries
scenario_s20_13 = ScenarioConfig(
    id="scenario_s20_13",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s20_13: script 021 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break and the A/C activation together between deliveries. Aspects: foreseeable: "
        "two of two kinds in a row, between deliveries. Expectation: on against off: each delivery admitted "
        "earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than "
        "off (ordinary strength); the A/C activation rarely admitted on or off; its belief at arrival lower "
        "on (ordinary 0.02 against the assigned tasks)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 400),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_1"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_14 = ScenarioConfig(
    id="scenario_s20_14",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s20_14: script 021 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break and the A/C activation together between deliveries. Aspects: foreseeable: "
        "two of two kinds in a row, between deliveries. Expectation: on against off: each delivery admitted "
        "earlier or equal (the assigned tasks share most of the prior); a coffee break admitted later than "
        "off (ordinary strength); the A/C activation rarely admitted on or off; its belief at arrival lower "
        "on (ordinary 0.02 against the assigned tasks). working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 400),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_1"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 400),
            assigned_tasks=[
                deliver_item("item_36", table="kitting_table_0"),
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_15 = ScenarioConfig(
    id="scenario_s20_15",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 130, 198), window(ROOM_WARM, 198, 220),)),
    description=(
        "scenario_s20_15: script 021 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 130 to 198, room_warm from 198 to 220. Purpose: a coffee "
        "break and the A/C activation together between deliveries. Aspects: foreseeable: two of two kinds in "
        "a row, between deliveries. Expectation: the coffee break (raised by break_time) admitted earlier "
        "than off and than on with no fact; the A/C activation's belief at arrival higher than with no fact "
        "(raised by room_warm); admission possible only where the movement evidence allows; a delivery "
        "inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 400),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_1"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_16 = ScenarioConfig(
    id="scenario_s20_16",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 130, 198), window(ROOM_WARM, 198, 220),)),
    description=(
        "scenario_s20_16: script 021 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 130 to 198, room_warm from 198 to 220. Purpose: a "
        "coffee break and the A/C activation together between deliveries. Aspects: foreseeable: two of two "
        "kinds in a row, between deliveries. Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; the A/C activation's belief at arrival higher than with "
        "no fact (raised by room_warm); admission possible only where the movement evidence allows; a "
        "delivery inside a window admitted later than with no fact. working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 400),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_1"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 400),
            assigned_tasks=[
                deliver_item("item_36", table="kitting_table_0"),
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_17 = ScenarioConfig(
    id="scenario_s20_17",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 130),)),
    description=(
        "scenario_s20_17: script 021 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 130. Purpose: a coffee break and the "
        "A/C activation together between deliveries. Aspects: foreseeable: two of two kinds in a row, "
        "between deliveries. Expectation: the delivery under break_time admitted later than with no fact, "
        "near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 400),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_1"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_18 = ScenarioConfig(
    id="scenario_s20_18",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 130),)),
    description=(
        "scenario_s20_18: script 021 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 130. Purpose: a coffee break and the "
        "A/C activation together between deliveries. Aspects: foreseeable: two of two kinds in a row, "
        "between deliveries. Expectation: the delivery under break_time admitted later than with no fact, "
        "near off. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 400),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_1"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 400),
            assigned_tasks=[
                deliver_item("item_36", table="kitting_table_0"),
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 022: unmodelled alone: a stand of 30 ticks at the table between deliveries
scenario_s20_19 = ScenarioConfig(
    id="scenario_s20_19",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s20_19: script 022 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a stand of 30 ticks at the table between deliveries. Aspects: "
        "unmodelled: a stand (30 ticks), between deliveries; robot: east start, its last part on the human's "
        "shelf_3. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis "
        "whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 500),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                stand("PT60S"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_20 = ScenarioConfig(
    id="scenario_s20_20",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s20_20: script 022 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a stand of 30 ticks at the table between deliveries. Aspects: "
        "unmodelled: a stand (30 ticks), between deliveries; robot: east start, its last part on the human's "
        "shelf_3. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis "
        "whose target lies on the walk. working robot: the decisions as off where no admission moves; an "
        "earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 500),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                stand("PT60S"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, 0),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_21 = ScenarioConfig(
    id="scenario_s20_21",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 105),)),
    description=(
        "scenario_s20_21: script 022 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 105. Purpose: unmodelled alone: a stand "
        "of 30 ticks at the table between deliveries. Aspects: unmodelled: a stand (30 ticks), between "
        "deliveries; robot: east start, its last part on the human's shelf_3. Expectation: the delivery "
        "under break_time admitted later than with no fact, near off; no admission during the stand or the "
        "walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 500),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                stand("PT60S"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_22 = ScenarioConfig(
    id="scenario_s20_22",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 105),)),
    description=(
        "scenario_s20_22: script 022 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 105. Purpose: unmodelled alone: a stand "
        "of 30 ticks at the table between deliveries. Aspects: unmodelled: a stand (30 ticks), between "
        "deliveries; robot: east start, its last part on the human's shelf_3. Expectation: the delivery "
        "under break_time admitted later than with no fact, near off; no admission during the stand or the "
        "walk elsewhere, except a hypothesis whose target lies on the walk. working robot: the decisions as "
        "off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it; under the window the delivery's admission and the robot's decision on it "
        "later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 500),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                stand("PT60S"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, 0),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_23 = ScenarioConfig(
    id="scenario_s20_23",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(ROOM_WARM, 0, 105),)),
    description=(
        "scenario_s20_23: script 022 of step 5e, the idle robot, its own timeline, room_warm over a delivery "
        "(the human works through it): room_warm from 0 to 105. Purpose: unmodelled alone: a stand of 30 "
        "ticks at the table between deliveries. Aspects: unmodelled: a stand (30 ticks), between deliveries; "
        "robot: east start, its last part on the human's shelf_3. Expectation: the delivery under room_warm "
        "admitted later than with no fact, by less than under break_time (raised 0.5 against 2)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 500),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                stand("PT60S"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_24 = ScenarioConfig(
    id="scenario_s20_24",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(ROOM_WARM, 0, 105),)),
    description=(
        "scenario_s20_24: script 022 of step 5e, the working robot, its own timeline, room_warm over a "
        "delivery (the human works through it): room_warm from 0 to 105. Purpose: unmodelled alone: a stand "
        "of 30 ticks at the table between deliveries. Aspects: unmodelled: a stand (30 ticks), between "
        "deliveries; robot: east start, its last part on the human's shelf_3. Expectation: the delivery "
        "under room_warm admitted later than with no fact, by less than under break_time (raised 0.5 against "
        "2). working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 500),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                stand("PT60S"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, 0),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 023: unmodelled with a foreseeable task: a walk to the south-west corner and a stand of 20 ticks, then a coffee break
scenario_s20_25 = ScenarioConfig(
    id="scenario_s20_25",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s20_25: script 023 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a walk to the south-west corner and a stand of 20 "
        "ticks, then a coffee break. Aspects: unmodelled: a walk elsewhere with a stand (20 ticks); "
        "foreseeable: right after it. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength); no admission during the stand or the walk elsewhere, except a hypothesis whose target "
        "lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 0),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                go_to_and_stand("corner_SW", "PT40S"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_26 = ScenarioConfig(
    id="scenario_s20_26",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s20_26: script 023 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a walk to the south-west corner and a stand of 20 "
        "ticks, then a coffee break. Aspects: unmodelled: a walk elsewhere with a stand (20 ticks); "
        "foreseeable: right after it. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength); no admission during the stand or the walk elsewhere, except a hypothesis whose target "
        "lies on the walk. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 0),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                go_to_and_stand("corner_SW", "PT40S"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 500),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_27 = ScenarioConfig(
    id="scenario_s20_27",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 190, 268),)),
    description=(
        "scenario_s20_27: script 023 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 190 to 268. Purpose: unmodelled with a foreseeable task: "
        "a walk to the south-west corner and a stand of 20 ticks, then a coffee break. Aspects: unmodelled: "
        "a walk elsewhere with a stand (20 ticks); foreseeable: right after it. Expectation: the coffee "
        "break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside "
        "a window admitted later than with no fact; no admission during the stand or the walk elsewhere, "
        "except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 0),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                go_to_and_stand("corner_SW", "PT40S"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_28 = ScenarioConfig(
    id="scenario_s20_28",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 190, 268),)),
    description=(
        "scenario_s20_28: script 023 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 190 to 268. Purpose: unmodelled with a foreseeable "
        "task: a walk to the south-west corner and a stand of 20 ticks, then a coffee break. Aspects: "
        "unmodelled: a walk elsewhere with a stand (20 ticks); foreseeable: right after it. Expectation: the "
        "coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery "
        "inside a window admitted later than with no fact; no admission during the stand or the walk "
        "elsewhere, except a hypothesis whose target lies on the walk. working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 0),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                go_to_and_stand("corner_SW", "PT40S"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 500),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_29 = ScenarioConfig(
    id="scenario_s20_29",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 98),)),
    description=(
        "scenario_s20_29: script 023 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 98. Purpose: unmodelled with a "
        "foreseeable task: a walk to the south-west corner and a stand of 20 ticks, then a coffee break. "
        "Aspects: unmodelled: a walk elsewhere with a stand (20 ticks); foreseeable: right after it. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off; no admission "
        "during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, 0),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                go_to_and_stand("corner_SW", "PT40S"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 300),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s20_30 = ScenarioConfig(
    id="scenario_s20_30",
    setup="env_setup_20",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 98),)),
    description=(
        "scenario_s20_30: script 023 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 98. Purpose: unmodelled with a "
        "foreseeable task: a walk to the south-west corner and a stand of 20 ticks, then a coffee break. "
        "Aspects: unmodelled: a walk elsewhere with a stand (20 ticks); foreseeable: right after it. "
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
            start_position=(500, 0),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                go_to_and_stand("corner_SW", "PT40S"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_33", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 500),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)
