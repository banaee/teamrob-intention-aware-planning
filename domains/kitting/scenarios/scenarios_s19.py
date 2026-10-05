# domains/kitting/scenarios/scenarios_s19.py
"""
Kitting scenarios on env_setup_19: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_05; the shift
env_setup_19: env_setup_04's shift, so scenario_s04_01's script has its copies here.
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

# ---- script 013: scenario_s04_01's script as it is: a coffee break, then the A/C activation on the line toward the next shelf
scenario_s19_01 = ScenarioConfig(
    id="scenario_s19_01",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s19_01: script 013 of step 5e (the script of scenario_s04_01, as it is), the idle robot, "
        "no timeline (the setup states none). Purpose: scenario_s04_01's script as it is: a coffee break, "
        "then the A/C activation on the line toward the next shelf. Aspects: foreseeable: two of two kinds "
        "between deliveries; existing. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength); the A/C activation rarely admitted on or off; its belief at arrival lower on (ordinary "
        "0.02 against the assigned tasks)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_1"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
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

scenario_s19_02 = ScenarioConfig(
    id="scenario_s19_02",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 117, 185), window(ROOM_WARM, 185, 207),)),
    description=(
        "scenario_s19_02: script 013 of step 5e (the script of scenario_s04_01, as it is), the idle robot, "
        "its own timeline, the raising fact over the foreseeable task (accord): break_time from 117 to 185, "
        "room_warm from 185 to 207. Purpose: scenario_s04_01's script as it is: a coffee break, then the A/C "
        "activation on the line toward the next shelf. Aspects: foreseeable: two of two kinds between "
        "deliveries; existing. Expectation: the coffee break (raised by break_time) admitted earlier than "
        "off and than on with no fact; the A/C activation's belief at arrival higher than with no fact "
        "(raised by room_warm); admission possible only where the movement evidence allows; a delivery "
        "inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_1"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
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

scenario_s19_03 = ScenarioConfig(
    id="scenario_s19_03",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 117, 185), window(ROOM_WARM, 185, 207),)),
    description=(
        "scenario_s19_03: script 013 of step 5e (the script of scenario_s04_01, as it is), the working "
        "robot, its own timeline, the raising fact over the foreseeable task (accord): break_time from 117 "
        "to 185, room_warm from 185 to 207. Purpose: scenario_s04_01's script as it is: a coffee break, then "
        "the A/C activation on the line toward the next shelf. Aspects: foreseeable: two of two kinds "
        "between deliveries; existing. Expectation: the coffee break (raised by break_time) admitted earlier "
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
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_1"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s19_04 = ScenarioConfig(
    id="scenario_s19_04",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 117),)),
    description=(
        "scenario_s19_04: script 013 of step 5e (the script of scenario_s04_01, as it is), the idle robot, "
        "its own timeline, break_time over a delivery (the human works through it): break_time from 0 to "
        "117. Purpose: scenario_s04_01's script as it is: a coffee break, then the A/C activation on the "
        "line toward the next shelf. Aspects: foreseeable: two of two kinds between deliveries; existing. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_1"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
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

scenario_s19_05 = ScenarioConfig(
    id="scenario_s19_05",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 117),)),
    description=(
        "scenario_s19_05: script 013 of step 5e (the script of scenario_s04_01, as it is), the working "
        "robot, its own timeline, break_time over a delivery (the human works through it): break_time from 0 "
        "to 117. Purpose: scenario_s04_01's script as it is: a coffee break, then the A/C activation on the "
        "line toward the next shelf. Aspects: foreseeable: two of two kinds between deliveries; existing. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; under the window the delivery's admission and the robot's "
        "decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_1"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 014: deliveries only: the two deliveries of scenario_s04_01 without its foreseeable tasks
scenario_s19_06 = ScenarioConfig(
    id="scenario_s19_06",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s19_06: script 014 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: the two deliveries of scenario_s04_01 without its foreseeable tasks. "
        "Aspects: deliveries: two; robot: scenario_s04_01's side. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
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

scenario_s19_07 = ScenarioConfig(
    id="scenario_s19_07",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s19_07: script 014 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: the two deliveries of scenario_s04_01 without its foreseeable tasks. "
        "Aspects: deliveries: two; robot: scenario_s04_01's side. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior). working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s19_08 = ScenarioConfig(
    id="scenario_s19_08",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 117),)),
    description=(
        "scenario_s19_08: script 014 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 117. Purpose: deliveries only: the two "
        "deliveries of scenario_s04_01 without its foreseeable tasks. Aspects: deliveries: two; robot: "
        "scenario_s04_01's side. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
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

scenario_s19_09 = ScenarioConfig(
    id="scenario_s19_09",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 117),)),
    description=(
        "scenario_s19_09: script 014 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 117. Purpose: deliveries only: the two "
        "deliveries of scenario_s04_01 without its foreseeable tasks. Aspects: deliveries: two; robot: "
        "scenario_s04_01's side. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off. working robot: the decisions as off where no admission moves; an earlier admission "
        "of a delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s19_10 = ScenarioConfig(
    id="scenario_s19_10",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(ROOM_WARM, 0, 117),)),
    description=(
        "scenario_s19_10: script 014 of step 5e, the idle robot, its own timeline, room_warm over a delivery "
        "(the human works through it): room_warm from 0 to 117. Purpose: deliveries only: the two deliveries "
        "of scenario_s04_01 without its foreseeable tasks. Aspects: deliveries: two; robot: "
        "scenario_s04_01's side. Expectation: the delivery under room_warm admitted later than with no fact, "
        "by less than under break_time (raised 0.5 against 2)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
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

scenario_s19_11 = ScenarioConfig(
    id="scenario_s19_11",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(ROOM_WARM, 0, 117),)),
    description=(
        "scenario_s19_11: script 014 of step 5e, the working robot, its own timeline, room_warm over a "
        "delivery (the human works through it): room_warm from 0 to 117. Purpose: deliveries only: the two "
        "deliveries of scenario_s04_01 without its foreseeable tasks. Aspects: deliveries: two; robot: "
        "scenario_s04_01's side. Expectation: the delivery under room_warm admitted later than with no fact, "
        "by less than under break_time (raised 0.5 against 2). working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 015: the A/C activation alone, at the start
scenario_s19_12 = ScenarioConfig(
    id="scenario_s19_12",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s19_12: script 015 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: the A/C activation alone, at the start. Aspects: foreseeable: the A/C alone, at the start; "
        "start: east of the table, first walk south toward the switch. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); the A/C activation "
        "rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the assigned "
        "tasks)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 400),
            scheduled_tasks=Script([
                ac_activation("ac_switch_1"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
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

scenario_s19_13 = ScenarioConfig(
    id="scenario_s19_13",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s19_13: script 015 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: the A/C activation alone, at the start. Aspects: foreseeable: the A/C alone, at the start; "
        "start: east of the table, first walk south toward the switch. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); the A/C activation "
        "rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the assigned "
        "tasks). working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 400),
            scheduled_tasks=Script([
                ac_activation("ac_switch_1"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s19_14 = ScenarioConfig(
    id="scenario_s19_14",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(ROOM_WARM, 0, 33),)),
    description=(
        "scenario_s19_14: script 015 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): room_warm from 0 to 33. Purpose: the A/C activation alone, at the start. "
        "Aspects: foreseeable: the A/C alone, at the start; start: east of the table, first walk south "
        "toward the switch. Expectation: the A/C activation's belief at arrival higher than with no fact "
        "(raised by room_warm); admission possible only where the movement evidence allows; a delivery "
        "inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 400),
            scheduled_tasks=Script([
                ac_activation("ac_switch_1"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
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

scenario_s19_15 = ScenarioConfig(
    id="scenario_s19_15",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(ROOM_WARM, 0, 33),)),
    description=(
        "scenario_s19_15: script 015 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): room_warm from 0 to 33. Purpose: the A/C activation alone, at the "
        "start. Aspects: foreseeable: the A/C alone, at the start; start: east of the table, first walk "
        "south toward the switch. Expectation: the A/C activation's belief at arrival higher than with no "
        "fact (raised by room_warm); admission possible only where the movement evidence allows; a delivery "
        "inside a window admitted later than with no fact. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 400),
            scheduled_tasks=Script([
                ac_activation("ac_switch_1"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s19_16 = ScenarioConfig(
    id="scenario_s19_16",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 33, 157),)),
    description=(
        "scenario_s19_16: script 015 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 33 to 157. Purpose: the A/C activation "
        "alone, at the start. Aspects: foreseeable: the A/C alone, at the start; start: east of the table, "
        "first walk south toward the switch. Expectation: the delivery under break_time admitted later than "
        "with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to "
        "the raised coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 400),
            scheduled_tasks=Script([
                ac_activation("ac_switch_1"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
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

scenario_s19_17 = ScenarioConfig(
    id="scenario_s19_17",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 33, 157),)),
    description=(
        "scenario_s19_17: script 015 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 33 to 157. Purpose: the A/C activation "
        "alone, at the start. Aspects: foreseeable: the A/C alone, at the start; start: east of the table, "
        "first walk south toward the switch. Expectation: the delivery under break_time admitted later than "
        "with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to "
        "the raised coffee break. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; under the window the "
        "delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 400),
            scheduled_tasks=Script([
                ac_activation("ac_switch_1"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 016: a coffee break between deliveries
scenario_s19_18 = ScenarioConfig(
    id="scenario_s19_18",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s19_18: script 016 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break between deliveries. Aspects: foreseeable: between deliveries; start: west "
        "floor; robot: north-east start, east shelves, crossing at the table. Expectation: on against off: "
        "each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee "
        "break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 0),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s19_19 = ScenarioConfig(
    id="scenario_s19_19",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s19_19: script 016 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break between deliveries. Aspects: foreseeable: between deliveries; start: west "
        "floor; robot: north-east start, east shelves, crossing at the table. Expectation: on against off: "
        "each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee "
        "break admitted later than off (ordinary strength). working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 0),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, 500),
            assigned_tasks=[
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s19_20 = ScenarioConfig(
    id="scenario_s19_20",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 124, 192),)),
    description=(
        "scenario_s19_20: script 016 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 124 to 192. Purpose: a coffee break between deliveries. "
        "Aspects: foreseeable: between deliveries; start: west floor; robot: north-east start, east shelves, "
        "crossing at the table. Expectation: the coffee break (raised by break_time) admitted earlier than "
        "off and than on with no fact; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 0),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s19_21 = ScenarioConfig(
    id="scenario_s19_21",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 124, 192),)),
    description=(
        "scenario_s19_21: script 016 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 124 to 192. Purpose: a coffee break between "
        "deliveries. Aspects: foreseeable: between deliveries; start: west floor; robot: north-east start, "
        "east shelves, crossing at the table. Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; a delivery inside a window admitted later than with no "
        "fact. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; the coffee break admitted earlier, the "
        "robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 0),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, 500),
            assigned_tasks=[
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s19_22 = ScenarioConfig(
    id="scenario_s19_22",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 124),)),
    description=(
        "scenario_s19_22: script 016 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 124. Purpose: a coffee break between "
        "deliveries. Aspects: foreseeable: between deliveries; start: west floor; robot: north-east start, "
        "east shelves, crossing at the table. Expectation: the delivery under break_time admitted later than "
        "with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 0),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s19_23 = ScenarioConfig(
    id="scenario_s19_23",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 124),)),
    description=(
        "scenario_s19_23: script 016 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 124. Purpose: a coffee break between "
        "deliveries. Aspects: foreseeable: between deliveries; start: west floor; robot: north-east start, "
        "east shelves, crossing at the table. Expectation: the delivery under break_time admitted later than "
        "with no fact, near off. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; under the window the "
        "delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 0),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, 500),
            assigned_tasks=[
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 017: the A/C activation inside a delivery: at shelf_6, before the grasp, the human walks back to the switch
scenario_s19_24 = ScenarioConfig(
    id="scenario_s19_24",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s19_24: script 017 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: the A/C activation inside a delivery: at shelf_6, before the grasp, the human walks back "
        "to the switch. Aspects: foreseeable: the A/C inside a delivery, before the grasp. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "the A/C activation rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against "
        "the assigned tasks)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0").at(move_to, ac_activation("ac_switch_1"), occurrence=0),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s19_25 = ScenarioConfig(
    id="scenario_s19_25",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s19_25: script 017 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: the A/C activation inside a delivery: at shelf_6, before the grasp, the human walks back "
        "to the switch. Aspects: foreseeable: the A/C inside a delivery, before the grasp. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "the A/C activation rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against "
        "the assigned tasks). working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0").at(move_to, ac_activation("ac_switch_1"), occurrence=0),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s19_26 = ScenarioConfig(
    id="scenario_s19_26",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(ROOM_WARM, 55, 86),)),
    description=(
        "scenario_s19_26: script 017 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): room_warm from 55 to 86. Purpose: the A/C activation inside a delivery: "
        "at shelf_6, before the grasp, the human walks back to the switch. Aspects: foreseeable: the A/C "
        "inside a delivery, before the grasp. Expectation: the A/C activation's belief at arrival higher "
        "than with no fact (raised by room_warm); admission possible only where the movement evidence "
        "allows; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0").at(move_to, ac_activation("ac_switch_1"), occurrence=0),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s19_27 = ScenarioConfig(
    id="scenario_s19_27",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(ROOM_WARM, 55, 86),)),
    description=(
        "scenario_s19_27: script 017 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): room_warm from 55 to 86. Purpose: the A/C activation inside a "
        "delivery: at shelf_6, before the grasp, the human walks back to the switch. Aspects: foreseeable: "
        "the A/C inside a delivery, before the grasp. Expectation: the A/C activation's belief at arrival "
        "higher than with no fact (raised by room_warm); admission possible only where the movement evidence "
        "allows; a delivery inside a window admitted later than with no fact. working robot: the decisions "
        "as off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0").at(move_to, ac_activation("ac_switch_1"), occurrence=0),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s19_28 = ScenarioConfig(
    id="scenario_s19_28",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 176, 289),)),
    description=(
        "scenario_s19_28: script 017 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 176 to 289. Purpose: the A/C activation "
        "inside a delivery: at shelf_6, before the grasp, the human walks back to the switch. Aspects: "
        "foreseeable: the A/C inside a delivery, before the grasp. Expectation: the delivery under "
        "break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0").at(move_to, ac_activation("ac_switch_1"), occurrence=0),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s19_29 = ScenarioConfig(
    id="scenario_s19_29",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 176, 289),)),
    description=(
        "scenario_s19_29: script 017 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 176 to 289. Purpose: the A/C activation "
        "inside a delivery: at shelf_6, before the grasp, the human walks back to the switch. Aspects: "
        "foreseeable: the A/C inside a delivery, before the grasp. Expectation: the delivery under "
        "break_time admitted later than with no fact, near off. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it; under the window the delivery's admission and the robot's decision on it later than with no "
        "fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0").at(move_to, ac_activation("ac_switch_1"), occurrence=0),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 018: unmodelled with a foreseeable task: a delivery abandoned after the grasp (the part still in hand), a coffee break, the second delivery never started
scenario_s19_30 = ScenarioConfig(
    id="scenario_s19_30",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s19_30: script 018 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery abandoned after the grasp (the part still "
        "in hand), a coffee break, the second delivery never started. Aspects: unmodelled: an abandoned "
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
            start_position=(-500, 400),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, drop),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
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

scenario_s19_31 = ScenarioConfig(
    id="scenario_s19_31",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    description=(
        "scenario_s19_31: script 018 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery abandoned after the grasp (the part still "
        "in hand), a coffee break, the second delivery never started. Aspects: unmodelled: an abandoned "
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
            start_position=(-500, 400),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, drop),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, 500),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s19_32 = ScenarioConfig(
    id="scenario_s19_32",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 34, 111),)),
    description=(
        "scenario_s19_32: script 018 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 34 to 111. Purpose: unmodelled with a foreseeable task: "
        "a delivery abandoned after the grasp (the part still in hand), a coffee break, the second delivery "
        "never started. Aspects: unmodelled: an abandoned delivery (after the grasp), a never-started "
        "delivery; foreseeable: after them. Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; a delivery inside a window admitted later than with no "
        "fact; the never-started delivery never admitted (no observation warrant); the abandoned delivery "
        "admitted while the human walks to it, then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 400),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, drop),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
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

scenario_s19_33 = ScenarioConfig(
    id="scenario_s19_33",
    setup="env_setup_19",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 34, 111),)),
    description=(
        "scenario_s19_33: script 018 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 34 to 111. Purpose: unmodelled with a foreseeable "
        "task: a delivery abandoned after the grasp (the part still in hand), a coffee break, the second "
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
            start_position=(-500, 400),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, drop),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, 500),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)
