# domains/kitting/scenarios/scenarios_s21.py
"""
Kitting scenarios on env_setup_21: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_06; the shift
env_setup_21: env_setup_03's shift, so scenario_s03_06's script has its copies here.
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

# ---- script 024: scenario_s03_06's script as it is: a coffee break at the end, east of the table; no exit walk
scenario_s21_01 = ScenarioConfig(
    id="scenario_s21_01",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s21_01: script 024 of step 5e (the script of scenario_s03_06, as it is), the idle robot, "
        "no timeline (the setup states none). Purpose: scenario_s03_06's script as it is: a coffee break at "
        "the end, east of the table; no exit walk. Aspects: foreseeable: at the end; existing. Expectation: "
        "on against off: each delivery admitted earlier or equal (the assigned tasks share most of the "
        "prior); a coffee break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s21_02 = ScenarioConfig(
    id="scenario_s21_02",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 123, 178),)),
    description=(
        "scenario_s21_02: script 024 of step 5e (the script of scenario_s03_06, as it is), the idle robot, "
        "its own timeline, the raising fact over the foreseeable task (accord): break_time from 123 to 178. "
        "Purpose: scenario_s03_06's script as it is: a coffee break at the end, east of the table; no exit "
        "walk. Aspects: foreseeable: at the end; existing. Expectation: the coffee break (raised by "
        "break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted "
        "later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s21_03 = ScenarioConfig(
    id="scenario_s21_03",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 123, 178),)),
    description=(
        "scenario_s21_03: script 024 of step 5e (the script of scenario_s03_06, as it is), the working "
        "robot, its own timeline, the raising fact over the foreseeable task (accord): break_time from 123 "
        "to 178. Purpose: scenario_s03_06's script as it is: a coffee break at the end, east of the table; "
        "no exit walk. Aspects: foreseeable: at the end; existing. Expectation: the coffee break (raised by "
        "break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted "
        "later than with no fact. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; the coffee break admitted "
        "earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s21_04 = ScenarioConfig(
    id="scenario_s21_04",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 56),)),
    description=(
        "scenario_s21_04: script 024 of step 5e (the script of scenario_s03_06, as it is), the idle robot, "
        "its own timeline, break_time over a delivery (the human works through it): break_time from 0 to 56. "
        "Purpose: scenario_s03_06's script as it is: a coffee break at the end, east of the table; no exit "
        "walk. Aspects: foreseeable: at the end; existing. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s21_05 = ScenarioConfig(
    id="scenario_s21_05",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 56),)),
    description=(
        "scenario_s21_05: script 024 of step 5e (the script of scenario_s03_06, as it is), the working "
        "robot, its own timeline, break_time over a delivery (the human works through it): break_time from 0 "
        "to 56. Purpose: scenario_s03_06's script as it is: a coffee break at the end, east of the table; no "
        "exit walk. Aspects: foreseeable: at the end; existing. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it; under "
        "the window the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 025: deliveries only: scenario_s03_06's two deliveries, then the exit walk
scenario_s21_06 = ScenarioConfig(
    id="scenario_s21_06",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s21_06: script 025 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: scenario_s03_06's two deliveries, then the exit walk. Aspects: "
        "deliveries: two; robot: scenario_s03_06's side, crossing at shelf_3 and the table. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s21_07 = ScenarioConfig(
    id="scenario_s21_07",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s21_07: script 025 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: scenario_s03_06's two deliveries, then the exit walk. Aspects: "
        "deliveries: two; robot: scenario_s03_06's side, crossing at shelf_3 and the table. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s21_08 = ScenarioConfig(
    id="scenario_s21_08",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 56),)),
    description=(
        "scenario_s21_08: script 025 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 56. Purpose: deliveries only: "
        "scenario_s03_06's two deliveries, then the exit walk. Aspects: deliveries: two; robot: "
        "scenario_s03_06's side, crossing at shelf_3 and the table. Expectation: the delivery under "
        "break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s21_09 = ScenarioConfig(
    id="scenario_s21_09",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 56),)),
    description=(
        "scenario_s21_09: script 025 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 56. Purpose: deliveries only: "
        "scenario_s03_06's two deliveries, then the exit walk. Aspects: deliveries: two; robot: "
        "scenario_s03_06's side, crossing at shelf_3 and the table. Expectation: the delivery under "
        "break_time admitted later than with no fact, near off. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it; under the window the delivery's admission and the robot's decision on it later than with no "
        "fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 026: a coffee break at the start
scenario_s21_10 = ScenarioConfig(
    id="scenario_s21_10",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s21_10: script 026 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the start. Aspects: foreseeable: at the start; start: east of the table, "
        "first walk toward the machine. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 250),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s21_11 = ScenarioConfig(
    id="scenario_s21_11",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s21_11: script 026 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the start. Aspects: foreseeable: at the start; start: east of the table, "
        "first walk toward the machine. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength). working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 250),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s21_12 = ScenarioConfig(
    id="scenario_s21_12",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 43),)),
    description=(
        "scenario_s21_12: script 026 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 0 to 43. Purpose: a coffee break at the start. Aspects: "
        "foreseeable: at the start; start: east of the table, first walk toward the machine. Expectation: "
        "the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a "
        "delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 250),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s21_13 = ScenarioConfig(
    id="scenario_s21_13",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 43),)),
    description=(
        "scenario_s21_13: script 026 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 0 to 43. Purpose: a coffee break at the start. "
        "Aspects: foreseeable: at the start; start: east of the table, first walk toward the machine. "
        "Expectation: the coffee break (raised by break_time) admitted earlier than off and than on with no "
        "fact; a delivery inside a window admitted later than with no fact. working robot: the decisions as "
        "off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 250),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s21_14 = ScenarioConfig(
    id="scenario_s21_14",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 43, 121),)),
    description=(
        "scenario_s21_14: script 026 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 43 to 121. Purpose: a coffee break at the "
        "start. Aspects: foreseeable: at the start; start: east of the table, first walk toward the machine. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off; a delivery "
        "whose walk heads toward the machine may lose its admission to the raised coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 250),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s21_15 = ScenarioConfig(
    id="scenario_s21_15",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 43, 121),)),
    description=(
        "scenario_s21_15: script 026 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 43 to 121. Purpose: a coffee break at the "
        "start. Aspects: foreseeable: at the start; start: east of the table, first walk toward the machine. "
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
            start_position=(300, 250),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 027: a coffee break inside a delivery, after the grasp: the carry diverted to the machine
scenario_s21_16 = ScenarioConfig(
    id="scenario_s21_16",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s21_16: script 027 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery, after the grasp: the carry diverted to the machine. "
        "Aspects: foreseeable: inside a delivery, after the grasp. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s21_17 = ScenarioConfig(
    id="scenario_s21_17",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s21_17: script 027 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery, after the grasp: the carry diverted to the machine. "
        "Aspects: foreseeable: inside a delivery, after the grasp. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength). working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s21_18 = ScenarioConfig(
    id="scenario_s21_18",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 14, 70),)),
    description=(
        "scenario_s21_18: script 027 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 14 to 70. Purpose: a coffee break inside a delivery, "
        "after the grasp: the carry diverted to the machine. Aspects: foreseeable: inside a delivery, after "
        "the grasp. Expectation: the coffee break (raised by break_time) admitted earlier than off and than "
        "on with no fact; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s21_19 = ScenarioConfig(
    id="scenario_s21_19",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 14, 70),)),
    description=(
        "scenario_s21_19: script 027 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 14 to 70. Purpose: a coffee break inside a delivery, "
        "after the grasp: the carry diverted to the machine. Aspects: foreseeable: inside a delivery, after "
        "the grasp. Expectation: the coffee break (raised by break_time) admitted earlier than off and than "
        "on with no fact; a delivery inside a window admitted later than with no fact. working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it; the coffee break admitted earlier, the robot's decision against it "
        "earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s21_20 = ScenarioConfig(
    id="scenario_s21_20",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 97, 162),)),
    description=(
        "scenario_s21_20: script 027 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 97 to 162. Purpose: a coffee break inside a "
        "delivery, after the grasp: the carry diverted to the machine. Aspects: foreseeable: inside a "
        "delivery, after the grasp. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s21_21 = ScenarioConfig(
    id="scenario_s21_21",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 97, 162),)),
    description=(
        "scenario_s21_21: script 027 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 97 to 162. Purpose: a coffee break inside a "
        "delivery, after the grasp: the carry diverted to the machine. Aspects: foreseeable: inside a "
        "delivery, after the grasp. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off. working robot: the decisions as off where no admission moves; an earlier admission "
        "of a delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 028: a never-started delivery with a coffee break after the one delivery
scenario_s21_22 = ScenarioConfig(
    id="scenario_s21_22",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s21_22: script 028 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a never-started delivery with a coffee break after the one delivery. Aspects: unmodelled: "
        "a never-started delivery; foreseeable: between (the last delivery never comes). Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "a coffee break admitted later than off (ordinary strength); the never-started delivery never "
        "admitted (no observation warrant)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s21_23 = ScenarioConfig(
    id="scenario_s21_23",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s21_23: script 028 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a never-started delivery with a coffee break after the one delivery. Aspects: unmodelled: "
        "a never-started delivery; foreseeable: between (the last delivery never comes). Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "a coffee break admitted later than off (ordinary strength); the never-started delivery never "
        "admitted (no observation warrant). working robot: the decisions as off where no admission moves; an "
        "earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, -300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s21_24 = ScenarioConfig(
    id="scenario_s21_24",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 59, 115),)),
    description=(
        "scenario_s21_24: script 028 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 59 to 115. Purpose: a never-started delivery with a "
        "coffee break after the one delivery. Aspects: unmodelled: a never-started delivery; foreseeable: "
        "between (the last delivery never comes). Expectation: the coffee break (raised by break_time) "
        "admitted earlier than off and than on with no fact; a delivery inside a window admitted later than "
        "with no fact; the never-started delivery never admitted (no observation warrant)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s21_25 = ScenarioConfig(
    id="scenario_s21_25",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 59, 115),)),
    description=(
        "scenario_s21_25: script 028 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 59 to 115. Purpose: a never-started delivery with a "
        "coffee break after the one delivery. Aspects: unmodelled: a never-started delivery; foreseeable: "
        "between (the last delivery never comes). Expectation: the coffee break (raised by break_time) "
        "admitted earlier than off and than on with no fact; a delivery inside a window admitted later than "
        "with no fact; the never-started delivery never admitted (no observation warrant). working robot: "
        "the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; the coffee break admitted earlier, the robot's decision "
        "against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, -300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s21_26 = ScenarioConfig(
    id="scenario_s21_26",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 59),)),
    description=(
        "scenario_s21_26: script 028 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 59. Purpose: a never-started delivery "
        "with a coffee break after the one delivery. Aspects: unmodelled: a never-started delivery; "
        "foreseeable: between (the last delivery never comes). Expectation: the delivery under break_time "
        "admitted later than with no fact, near off; the never-started delivery never admitted (no "
        "observation warrant)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s21_27 = ScenarioConfig(
    id="scenario_s21_27",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 59),)),
    description=(
        "scenario_s21_27: script 028 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 59. Purpose: a never-started delivery "
        "with a coffee break after the one delivery. Aspects: unmodelled: a never-started delivery; "
        "foreseeable: between (the last delivery never comes). Expectation: the delivery under break_time "
        "admitted later than with no fact, near off; the never-started delivery never admitted (no "
        "observation warrant). working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; under the window the "
        "delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 300),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, -300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 029: unmodelled alone: a walk to corner_NE, 50 cm from the coffee machine, and a stand of 20 ticks there, which looks like a coffee break and is none
scenario_s21_28 = ScenarioConfig(
    id="scenario_s21_28",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s21_28: script 029 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a walk to corner_NE, 50 cm from the coffee machine, and a stand of 20 "
        "ticks there, which looks like a coffee break and is none. Aspects: unmodelled: a walk elsewhere "
        "toward the machine with a stand (20 ticks). Expectation: on against off: each delivery admitted "
        "earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the "
        "walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                go_to_and_stand("corner_NE", "PT40S"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s21_29 = ScenarioConfig(
    id="scenario_s21_29",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    description=(
        "scenario_s21_29: script 029 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a walk to corner_NE, 50 cm from the coffee machine, and a stand of 20 "
        "ticks there, which looks like a coffee break and is none. Aspects: unmodelled: a walk elsewhere "
        "toward the machine with a stand (20 ticks). Expectation: on against off: each delivery admitted "
        "earlier or equal (the assigned tasks share most of the prior); no admission during the stand or the "
        "walk elsewhere, except a hypothesis whose target lies on the walk. working robot: the decisions as "
        "off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                go_to_and_stand("corner_NE", "PT40S"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s21_30 = ScenarioConfig(
    id="scenario_s21_30",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 47),)),
    description=(
        "scenario_s21_30: script 029 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 47. Purpose: unmodelled alone: a walk "
        "to corner_NE, 50 cm from the coffee machine, and a stand of 20 ticks there, which looks like a "
        "coffee break and is none. Aspects: unmodelled: a walk elsewhere toward the machine with a stand (20 "
        "ticks). Expectation: the delivery under break_time admitted later than with no fact, near off; a "
        "delivery whose walk heads toward the machine may lose its admission to the raised coffee break; no "
        "admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                go_to_and_stand("corner_NE", "PT40S"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s21_31 = ScenarioConfig(
    id="scenario_s21_31",
    setup="env_setup_21",
    reference_layouts=["env_layout_06"],
    timeline=Timeline((window(BREAK_TIME, 0, 47),)),
    description=(
        "scenario_s21_31: script 029 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 47. Purpose: unmodelled alone: a walk "
        "to corner_NE, 50 cm from the coffee machine, and a stand of 20 ticks there, which looks like a "
        "coffee break and is none. Aspects: unmodelled: a walk elsewhere toward the machine with a stand (20 "
        "ticks). Expectation: the delivery under break_time admitted later than with no fact, near off; a "
        "delivery whose walk heads toward the machine may lose its admission to the raised coffee break; no "
        "admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the "
        "walk. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                go_to_and_stand("corner_NE", "PT40S"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)
