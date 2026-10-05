# domains/kitting/scenarios/scenarios_s29.py
"""
Kitting scenarios on env_setup_29: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_20; the shift
env_setup_29: the cross shift: the north-west shelf_2 and the south-west shelf_6 to the south table, the others to the north table (shelf_3's carry along the north wall past the coffee machine).
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

# ---- script 086: deliveries only: one carry along the north wall past the coffee machine
scenario_s29_01 = ScenarioConfig(
    id="scenario_s29_01",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_01: script 086 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: one carry along the north wall past the coffee machine. Aspects: "
        "deliveries: one; start: near the machine, first walk away from it; robot: west, apart. Expectation: "
        "on against off: each delivery admitted earlier or equal (the assigned tasks share most of the "
        "prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 200),
            scheduled_tasks=Script([
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
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

scenario_s29_02 = ScenarioConfig(
    id="scenario_s29_02",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_02: script 086 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: one carry along the north wall past the coffee machine. Aspects: "
        "deliveries: one; start: near the machine, first walk away from it; robot: west, apart. Expectation: "
        "on against off: each delivery admitted earlier or equal (the assigned tasks share most of the "
        "prior). working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 200),
            scheduled_tasks=Script([
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, -200),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_03 = ScenarioConfig(
    id="scenario_s29_03",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 88),)),
    description=(
        "scenario_s29_03: script 086 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 88. Purpose: deliveries only: one carry "
        "along the north wall past the coffee machine. Aspects: deliveries: one; start: near the machine, "
        "first walk away from it; robot: west, apart. Expectation: the delivery under break_time admitted "
        "later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 200),
            scheduled_tasks=Script([
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
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

scenario_s29_04 = ScenarioConfig(
    id="scenario_s29_04",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 88),)),
    description=(
        "scenario_s29_04: script 086 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 88. Purpose: deliveries only: one carry "
        "along the north wall past the coffee machine. Aspects: deliveries: one; start: near the machine, "
        "first walk away from it; robot: west, apart. Expectation: the delivery under break_time admitted "
        "later than with no fact, near off. working robot: the decisions as off where no admission moves; an "
        "earlier admission of a delivery moves the response decision earlier or leaves it; under the window "
        "the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 200),
            scheduled_tasks=Script([
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, -200),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 087: deliveries only: three, alternating tables
scenario_s29_05 = ScenarioConfig(
    id="scenario_s29_05",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_05: script 087 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: three, alternating tables. Aspects: deliveries: three, alternating; "
        "robot: north-east start, to kitting_table_0, crossing. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, 0),
            scheduled_tasks=Script([
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
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

scenario_s29_06 = ScenarioConfig(
    id="scenario_s29_06",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_06: script 087 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: three, alternating tables. Aspects: deliveries: three, alternating; "
        "robot: north-east start, to kitting_table_0, crossing. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior). working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, 0),
            scheduled_tasks=Script([
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(800, 300),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_07 = ScenarioConfig(
    id="scenario_s29_07",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 108),)),
    description=(
        "scenario_s29_07: script 087 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 108. Purpose: deliveries only: three, "
        "alternating tables. Aspects: deliveries: three, alternating; robot: north-east start, to "
        "kitting_table_0, crossing. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, 0),
            scheduled_tasks=Script([
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
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

scenario_s29_08 = ScenarioConfig(
    id="scenario_s29_08",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 108),)),
    description=(
        "scenario_s29_08: script 087 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 108. Purpose: deliveries only: three, "
        "alternating tables. Aspects: deliveries: three, alternating; robot: north-east start, to "
        "kitting_table_0, crossing. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off. working robot: the decisions as off where no admission moves; an earlier admission "
        "of a delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, 0),
            scheduled_tasks=Script([
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(800, 300),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 088: a coffee break at the end, after two deliveries to the north table
scenario_s29_09 = ScenarioConfig(
    id="scenario_s29_09",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_09: script 088 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the end, after two deliveries to the north table. Aspects: foreseeable: "
        "at the end; start: west wall. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, -100),
            scheduled_tasks=Script([
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
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

scenario_s29_10 = ScenarioConfig(
    id="scenario_s29_10",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_10: script 088 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the end, after two deliveries to the north table. Aspects: foreseeable: "
        "at the end; start: west wall. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior); a coffee break admitted later than off (ordinary "
        "strength). working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, -100),
            scheduled_tasks=Script([
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(400, 0),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_11 = ScenarioConfig(
    id="scenario_s29_11",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 230, 291),)),
    description=(
        "scenario_s29_11: script 088 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 230 to 291. Purpose: a coffee break at the end, after "
        "two deliveries to the north table. Aspects: foreseeable: at the end; start: west wall. Expectation: "
        "the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a "
        "delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, -100),
            scheduled_tasks=Script([
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
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

scenario_s29_12 = ScenarioConfig(
    id="scenario_s29_12",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 230, 291),)),
    description=(
        "scenario_s29_12: script 088 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 230 to 291. Purpose: a coffee break at the end, "
        "after two deliveries to the north table. Aspects: foreseeable: at the end; start: west wall. "
        "Expectation: the coffee break (raised by break_time) admitted earlier than off and than on with no "
        "fact; a delivery inside a window admitted later than with no fact. working robot: the decisions as "
        "off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, -100),
            scheduled_tasks=Script([
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(400, 0),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_13 = ScenarioConfig(
    id="scenario_s29_13",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 61),)),
    description=(
        "scenario_s29_13: script 088 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 61. Purpose: a coffee break at the end, "
        "after two deliveries to the north table. Aspects: foreseeable: at the end; start: west wall. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, -100),
            scheduled_tasks=Script([
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
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

scenario_s29_14 = ScenarioConfig(
    id="scenario_s29_14",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 61),)),
    description=(
        "scenario_s29_14: script 088 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 61. Purpose: a coffee break at the end, "
        "after two deliveries to the north table. Aspects: foreseeable: at the end; start: west wall. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; under the window the delivery's admission and the robot's "
        "decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, -100),
            scheduled_tasks=Script([
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(400, 0),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 089: a coffee break between two deliveries to the south table
scenario_s29_15 = ScenarioConfig(
    id="scenario_s29_15",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_15: script 089 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break between two deliveries to the south table. Aspects: foreseeable: between "
        "deliveries; start: by the door, first walk west. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted "
        "later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -300),
            scheduled_tasks=Script([
                deliver_item("item_66", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_62", table="kitting_table_1"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_66", table="kitting_table_1"),
                deliver_item("item_62", table="kitting_table_1"),
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

scenario_s29_16 = ScenarioConfig(
    id="scenario_s29_16",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_16: script 089 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break between two deliveries to the south table. Aspects: foreseeable: between "
        "deliveries; start: by the door, first walk west. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted "
        "later than off (ordinary strength). working robot: the decisions as off where no admission moves; "
        "an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -300),
            scheduled_tasks=Script([
                deliver_item("item_66", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_62", table="kitting_table_1"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_66", table="kitting_table_1"),
                deliver_item("item_62", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, 0),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
                deliver_item("item_64", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_17 = ScenarioConfig(
    id="scenario_s29_17",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 89, 168),)),
    description=(
        "scenario_s29_17: script 089 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 89 to 168. Purpose: a coffee break between two "
        "deliveries to the south table. Aspects: foreseeable: between deliveries; start: by the door, first "
        "walk west. Expectation: the coffee break (raised by break_time) admitted earlier than off and than "
        "on with no fact; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -300),
            scheduled_tasks=Script([
                deliver_item("item_66", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_62", table="kitting_table_1"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_66", table="kitting_table_1"),
                deliver_item("item_62", table="kitting_table_1"),
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

scenario_s29_18 = ScenarioConfig(
    id="scenario_s29_18",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 89, 168),)),
    description=(
        "scenario_s29_18: script 089 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 89 to 168. Purpose: a coffee break between two "
        "deliveries to the south table. Aspects: foreseeable: between deliveries; start: by the door, first "
        "walk west. Expectation: the coffee break (raised by break_time) admitted earlier than off and than "
        "on with no fact; a delivery inside a window admitted later than with no fact. working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it; the coffee break admitted earlier, the robot's decision against it "
        "earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -300),
            scheduled_tasks=Script([
                deliver_item("item_66", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_62", table="kitting_table_1"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_66", table="kitting_table_1"),
                deliver_item("item_62", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, 0),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
                deliver_item("item_64", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_19 = ScenarioConfig(
    id="scenario_s29_19",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 89),)),
    description=(
        "scenario_s29_19: script 089 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 89. Purpose: a coffee break between two "
        "deliveries to the south table. Aspects: foreseeable: between deliveries; start: by the door, first "
        "walk west. Expectation: the delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -300),
            scheduled_tasks=Script([
                deliver_item("item_66", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_62", table="kitting_table_1"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_66", table="kitting_table_1"),
                deliver_item("item_62", table="kitting_table_1"),
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

scenario_s29_20 = ScenarioConfig(
    id="scenario_s29_20",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 89),)),
    description=(
        "scenario_s29_20: script 089 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 89. Purpose: a coffee break between two "
        "deliveries to the south table. Aspects: foreseeable: between deliveries; start: by the door, first "
        "walk west. Expectation: the delivery under break_time admitted later than with no fact, near off. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it; under the window the delivery's admission and the "
        "robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -300),
            scheduled_tasks=Script([
                deliver_item("item_66", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_62", table="kitting_table_1"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_66", table="kitting_table_1"),
                deliver_item("item_62", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, 0),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
                deliver_item("item_64", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 090: a coffee break inside a delivery, at shelf_4 before the grasp
scenario_s29_21 = ScenarioConfig(
    id="scenario_s29_21",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_21: script 090 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery, at shelf_4 before the grasp. Aspects: foreseeable: "
        "inside a delivery, before the grasp; robot: west start, crossing. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(600, -200),
            scheduled_tasks=Script([
                deliver_item("item_64", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_61", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_61", table="kitting_table_0"),
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

scenario_s29_22 = ScenarioConfig(
    id="scenario_s29_22",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_22: script 090 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery, at shelf_4 before the grasp. Aspects: foreseeable: "
        "inside a delivery, before the grasp; robot: west start, crossing. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength). working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(600, -200),
            scheduled_tasks=Script([
                deliver_item("item_64", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_61", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_61", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, 100),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_66", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_23 = ScenarioConfig(
    id="scenario_s29_23",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 18, 98),)),
    description=(
        "scenario_s29_23: script 090 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 18 to 98. Purpose: a coffee break inside a delivery, at "
        "shelf_4 before the grasp. Aspects: foreseeable: inside a delivery, before the grasp; robot: west "
        "start, crossing. Expectation: the coffee break (raised by break_time) admitted earlier than off and "
        "than on with no fact; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(600, -200),
            scheduled_tasks=Script([
                deliver_item("item_64", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_61", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_61", table="kitting_table_0"),
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

scenario_s29_24 = ScenarioConfig(
    id="scenario_s29_24",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 18, 98),)),
    description=(
        "scenario_s29_24: script 090 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 18 to 98. Purpose: a coffee break inside a delivery, "
        "at shelf_4 before the grasp. Aspects: foreseeable: inside a delivery, before the grasp; robot: west "
        "start, crossing. Expectation: the coffee break (raised by break_time) admitted earlier than off and "
        "than on with no fact; a delivery inside a window admitted later than with no fact. working robot: "
        "the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; the coffee break admitted earlier, the robot's decision "
        "against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(600, -200),
            scheduled_tasks=Script([
                deliver_item("item_64", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_61", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_61", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, 100),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_66", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_25 = ScenarioConfig(
    id="scenario_s29_25",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 228, 323),)),
    description=(
        "scenario_s29_25: script 090 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 228 to 323. Purpose: a coffee break inside a "
        "delivery, at shelf_4 before the grasp. Aspects: foreseeable: inside a delivery, before the grasp; "
        "robot: west start, crossing. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(600, -200),
            scheduled_tasks=Script([
                deliver_item("item_64", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_61", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_61", table="kitting_table_0"),
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

scenario_s29_26 = ScenarioConfig(
    id="scenario_s29_26",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 228, 323),)),
    description=(
        "scenario_s29_26: script 090 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 228 to 323. Purpose: a coffee break inside a "
        "delivery, at shelf_4 before the grasp. Aspects: foreseeable: inside a delivery, before the grasp; "
        "robot: west start, crossing. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off. working robot: the decisions as off where no admission moves; an earlier admission "
        "of a delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(600, -200),
            scheduled_tasks=Script([
                deliver_item("item_64", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_61", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_61", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, 100),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_66", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 091: a coffee break at the start, a long first walk toward the machine from the south table
scenario_s29_27 = ScenarioConfig(
    id="scenario_s29_27",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_27: script 091 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the start, a long first walk toward the machine from the south table. "
        "Aspects: foreseeable: at the start; start: kitting_table_1, the longest first walk toward the "
        "machine; deliveries: one, past the machine again. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted "
        "later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, -400),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
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

scenario_s29_28 = ScenarioConfig(
    id="scenario_s29_28",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_28: script 091 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the start, a long first walk toward the machine from the south table. "
        "Aspects: foreseeable: at the start; start: kitting_table_1, the longest first walk toward the "
        "machine; deliveries: one, past the machine again. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted "
        "later than off (ordinary strength). working robot: the decisions as off where no admission moves; "
        "an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, -400),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, -200),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_29 = ScenarioConfig(
    id="scenario_s29_29",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 77),)),
    description=(
        "scenario_s29_29: script 091 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 0 to 77. Purpose: a coffee break at the start, a long "
        "first walk toward the machine from the south table. Aspects: foreseeable: at the start; start: "
        "kitting_table_1, the longest first walk toward the machine; deliveries: one, past the machine "
        "again. Expectation: the coffee break (raised by break_time) admitted earlier than off and than on "
        "with no fact; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, -400),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
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

scenario_s29_30 = ScenarioConfig(
    id="scenario_s29_30",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 77),)),
    description=(
        "scenario_s29_30: script 091 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 0 to 77. Purpose: a coffee break at the start, a "
        "long first walk toward the machine from the south table. Aspects: foreseeable: at the start; start: "
        "kitting_table_1, the longest first walk toward the machine; deliveries: one, past the machine "
        "again. Expectation: the coffee break (raised by break_time) admitted earlier than off and than on "
        "with no fact; a delivery inside a window admitted later than with no fact. working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it; the coffee break admitted earlier, the robot's decision against it "
        "earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, -400),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, -200),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_31 = ScenarioConfig(
    id="scenario_s29_31",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 77, 168),)),
    description=(
        "scenario_s29_31: script 091 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 77 to 168. Purpose: a coffee break at the "
        "start, a long first walk toward the machine from the south table. Aspects: foreseeable: at the "
        "start; start: kitting_table_1, the longest first walk toward the machine; deliveries: one, past the "
        "machine again. Expectation: the delivery under break_time admitted later than with no fact, near "
        "off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee "
        "break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, -400),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
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

scenario_s29_32 = ScenarioConfig(
    id="scenario_s29_32",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 77, 168),)),
    description=(
        "scenario_s29_32: script 091 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 77 to 168. Purpose: a coffee break at the "
        "start, a long first walk toward the machine from the south table. Aspects: foreseeable: at the "
        "start; start: kitting_table_1, the longest first walk toward the machine; deliveries: one, past the "
        "machine again. Expectation: the delivery under break_time admitted later than with no fact, near "
        "off; a delivery whose walk heads toward the machine may lose its admission to the raised coffee "
        "break. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, -400),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, -200),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 092: unmodelled with a foreseeable task: a delivery abandoned at shelf_5 before the grasp, then a coffee break
scenario_s29_33 = ScenarioConfig(
    id="scenario_s29_33",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_33: script 092 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery abandoned at shelf_5 before the grasp, then "
        "a coffee break. Aspects: unmodelled: an abandoned delivery (before the grasp); foreseeable: right "
        "after. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); a coffee break admitted later than off (ordinary strength); the abandoned "
        "delivery admitted while the human walks to it, then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, 0),
            scheduled_tasks=Script([
                deliver_item("item_65", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_65", table="kitting_table_0"),
                deliver_item("item_63", table="kitting_table_0"),
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

scenario_s29_34 = ScenarioConfig(
    id="scenario_s29_34",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_34: script 092 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery abandoned at shelf_5 before the grasp, then "
        "a coffee break. Aspects: unmodelled: an abandoned delivery (before the grasp); foreseeable: right "
        "after. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); a coffee break admitted later than off (ordinary strength); the abandoned "
        "delivery admitted while the human walks to it, then retracted as the evidence turns. working robot: "
        "the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, 0),
            scheduled_tasks=Script([
                deliver_item("item_65", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_65", table="kitting_table_0"),
                deliver_item("item_63", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, -200),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_62", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_35 = ScenarioConfig(
    id="scenario_s29_35",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 22, 110),)),
    description=(
        "scenario_s29_35: script 092 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 22 to 110. Purpose: unmodelled with a foreseeable task: "
        "a delivery abandoned at shelf_5 before the grasp, then a coffee break. Aspects: unmodelled: an "
        "abandoned delivery (before the grasp); foreseeable: right after. Expectation: the coffee break "
        "(raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a "
        "window admitted later than with no fact; the abandoned delivery admitted while the human walks to "
        "it, then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, 0),
            scheduled_tasks=Script([
                deliver_item("item_65", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_65", table="kitting_table_0"),
                deliver_item("item_63", table="kitting_table_0"),
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

scenario_s29_36 = ScenarioConfig(
    id="scenario_s29_36",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 22, 110),)),
    description=(
        "scenario_s29_36: script 092 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 22 to 110. Purpose: unmodelled with a foreseeable "
        "task: a delivery abandoned at shelf_5 before the grasp, then a coffee break. Aspects: unmodelled: "
        "an abandoned delivery (before the grasp); foreseeable: right after. Expectation: the coffee break "
        "(raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a "
        "window admitted later than with no fact; the abandoned delivery admitted while the human walks to "
        "it, then retracted as the evidence turns. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it; the "
        "coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, 0),
            scheduled_tasks=Script([
                deliver_item("item_65", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_65", table="kitting_table_0"),
                deliver_item("item_63", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, -200),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_62", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_37 = ScenarioConfig(
    id="scenario_s29_37",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 110, 201),)),
    description=(
        "scenario_s29_37: script 092 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 110 to 201. Purpose: unmodelled with a "
        "foreseeable task: a delivery abandoned at shelf_5 before the grasp, then a coffee break. Aspects: "
        "unmodelled: an abandoned delivery (before the grasp); foreseeable: right after. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off; the abandoned delivery "
        "admitted while the human walks to it, then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, 0),
            scheduled_tasks=Script([
                deliver_item("item_65", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_65", table="kitting_table_0"),
                deliver_item("item_63", table="kitting_table_0"),
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

scenario_s29_38 = ScenarioConfig(
    id="scenario_s29_38",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 110, 201),)),
    description=(
        "scenario_s29_38: script 092 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 110 to 201. Purpose: unmodelled with a "
        "foreseeable task: a delivery abandoned at shelf_5 before the grasp, then a coffee break. Aspects: "
        "unmodelled: an abandoned delivery (before the grasp); foreseeable: right after. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off; the abandoned delivery "
        "admitted while the human walks to it, then retracted as the evidence turns. working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it; under the window the delivery's admission and the robot's decision "
        "on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, 0),
            scheduled_tasks=Script([
                deliver_item("item_65", table="kitting_table_0").at(move_to, drop, occurrence=0),
                coffee_break("coffee_machine_0"),
                deliver_item("item_63", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_65", table="kitting_table_0"),
                deliver_item("item_63", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, -200),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_62", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 093: unmodelled alone: a stand of 20 ticks at the south table, then a walk to corner_SE, before the next delivery
scenario_s29_39 = ScenarioConfig(
    id="scenario_s29_39",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_39: script 093 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a stand of 20 ticks at the south table, then a walk to corner_SE, before "
        "the next delivery. Aspects: unmodelled: two in a row, a stand (20 ticks) and a walk elsewhere. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior); no admission during the stand or the walk elsewhere, except a hypothesis whose "
        "target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 200),
            scheduled_tasks=Script([
                deliver_item("item_62", table="kitting_table_1"),
                stand("PT40S"),
                go_to("corner_SE"),
                deliver_item("item_65", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_65", table="kitting_table_0"),
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

scenario_s29_40 = ScenarioConfig(
    id="scenario_s29_40",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_40: script 093 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a stand of 20 ticks at the south table, then a walk to corner_SE, before "
        "the next delivery. Aspects: unmodelled: two in a row, a stand (20 ticks) and a walk elsewhere. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior); no admission during the stand or the walk elsewhere, except a hypothesis whose "
        "target lies on the walk. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 200),
            scheduled_tasks=Script([
                deliver_item("item_62", table="kitting_table_1"),
                stand("PT40S"),
                go_to("corner_SE"),
                deliver_item("item_65", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_65", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(200, 300),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
                deliver_item("item_61", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_41 = ScenarioConfig(
    id="scenario_s29_41",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 107),)),
    description=(
        "scenario_s29_41: script 093 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 107. Purpose: unmodelled alone: a stand "
        "of 20 ticks at the south table, then a walk to corner_SE, before the next delivery. Aspects: "
        "unmodelled: two in a row, a stand (20 ticks) and a walk elsewhere. Expectation: the delivery under "
        "break_time admitted later than with no fact, near off; no admission during the stand or the walk "
        "elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 200),
            scheduled_tasks=Script([
                deliver_item("item_62", table="kitting_table_1"),
                stand("PT40S"),
                go_to("corner_SE"),
                deliver_item("item_65", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_65", table="kitting_table_0"),
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

scenario_s29_42 = ScenarioConfig(
    id="scenario_s29_42",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 107),)),
    description=(
        "scenario_s29_42: script 093 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 107. Purpose: unmodelled alone: a stand "
        "of 20 ticks at the south table, then a walk to corner_SE, before the next delivery. Aspects: "
        "unmodelled: two in a row, a stand (20 ticks) and a walk elsewhere. Expectation: the delivery under "
        "break_time admitted later than with no fact, near off; no admission during the stand or the walk "
        "elsewhere, except a hypothesis whose target lies on the walk. working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it; under the window the delivery's admission and the robot's decision on it later than with "
        "no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 200),
            scheduled_tasks=Script([
                deliver_item("item_62", table="kitting_table_1"),
                stand("PT40S"),
                go_to("corner_SE"),
                deliver_item("item_65", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_65", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(200, 300),
            assigned_tasks=[
                deliver_item("item_63", table="kitting_table_0"),
                deliver_item("item_61", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 094: unmodelled alone: a never-started delivery among two performed
scenario_s29_43 = ScenarioConfig(
    id="scenario_s29_43",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_43: script 094 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a never-started delivery among two performed. Aspects: unmodelled: a "
        "never-started delivery; deliveries: two, both tables. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); the never-started delivery "
        "never admitted (no observation warrant)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -450),
            scheduled_tasks=Script([
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
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

scenario_s29_44 = ScenarioConfig(
    id="scenario_s29_44",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_44: script 094 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a never-started delivery among two performed. Aspects: unmodelled: a "
        "never-started delivery; deliveries: two, both tables. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); the never-started delivery "
        "never admitted (no observation warrant). working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -450),
            scheduled_tasks=Script([
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, -250),
            assigned_tasks=[
                deliver_item("item_65", table="kitting_table_0"),
                deliver_item("item_63", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_45 = ScenarioConfig(
    id="scenario_s29_45",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 83),)),
    description=(
        "scenario_s29_45: script 094 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 83. Purpose: unmodelled alone: a "
        "never-started delivery among two performed. Aspects: unmodelled: a never-started delivery; "
        "deliveries: two, both tables. Expectation: the delivery under break_time admitted later than with "
        "no fact, near off; the never-started delivery never admitted (no observation warrant)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -450),
            scheduled_tasks=Script([
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
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

scenario_s29_46 = ScenarioConfig(
    id="scenario_s29_46",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 83),)),
    description=(
        "scenario_s29_46: script 094 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 83. Purpose: unmodelled alone: a "
        "never-started delivery among two performed. Aspects: unmodelled: a never-started delivery; "
        "deliveries: two, both tables. Expectation: the delivery under break_time admitted later than with "
        "no fact, near off; the never-started delivery never admitted (no observation warrant). working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; under the window the delivery's admission and the robot's "
        "decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -450),
            scheduled_tasks=Script([
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_61", table="kitting_table_0"),
                deliver_item("item_66", table="kitting_table_1"),
                deliver_item("item_64", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, -250),
            assigned_tasks=[
                deliver_item("item_65", table="kitting_table_0"),
                deliver_item("item_63", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 095: unmodelled with a foreseeable task: a delivery to the other table (item_62 to kitting_table_0), then a coffee break inside the next delivery after the grasp
scenario_s29_47 = ScenarioConfig(
    id="scenario_s29_47",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_47: script 095 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery to the other table (item_62 to "
        "kitting_table_0), then a coffee break inside the next delivery after the grasp. Aspects: "
        "unmodelled: a delivery to the other table; foreseeable: inside the next delivery, after the grasp. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior); a coffee break admitted later than off (ordinary strength); the delivery to the "
        "other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis "
        "admitted there."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 250),
            scheduled_tasks=Script([
                deliver_item("item_62", table="kitting_table_0"),
                deliver_item("item_63", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_63", table="kitting_table_0"),
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

scenario_s29_48 = ScenarioConfig(
    id="scenario_s29_48",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s29_48: script 095 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery to the other table (item_62 to "
        "kitting_table_0), then a coffee break inside the next delivery after the grasp. Aspects: "
        "unmodelled: a delivery to the other table; foreseeable: inside the next delivery, after the grasp. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior); a coffee break admitted later than off (ordinary strength); the delivery to the "
        "other table: admitted on the walk to the shelf, then its carry unexplained; no other hypothesis "
        "admitted there. working robot: the decisions as off where no admission moves; an earlier admission "
        "of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 250),
            scheduled_tasks=Script([
                deliver_item("item_62", table="kitting_table_0"),
                deliver_item("item_63", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_63", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -200),
            assigned_tasks=[
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s29_49 = ScenarioConfig(
    id="scenario_s29_49",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 97, 156),)),
    description=(
        "scenario_s29_49: script 095 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 97 to 156. Purpose: unmodelled with a foreseeable task: "
        "a delivery to the other table (item_62 to kitting_table_0), then a coffee break inside the next "
        "delivery after the grasp. Aspects: unmodelled: a delivery to the other table; foreseeable: inside "
        "the next delivery, after the grasp. Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; a delivery inside a window admitted later than with no "
        "fact; the delivery to the other table: admitted on the walk to the shelf, then its carry "
        "unexplained; no other hypothesis admitted there."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 250),
            scheduled_tasks=Script([
                deliver_item("item_62", table="kitting_table_0"),
                deliver_item("item_63", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_63", table="kitting_table_0"),
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

scenario_s29_50 = ScenarioConfig(
    id="scenario_s29_50",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 97, 156),)),
    description=(
        "scenario_s29_50: script 095 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 97 to 156. Purpose: unmodelled with a foreseeable "
        "task: a delivery to the other table (item_62 to kitting_table_0), then a coffee break inside the "
        "next delivery after the grasp. Aspects: unmodelled: a delivery to the other table; foreseeable: "
        "inside the next delivery, after the grasp. Expectation: the coffee break (raised by break_time) "
        "admitted earlier than off and than on with no fact; a delivery inside a window admitted later than "
        "with no fact; the delivery to the other table: admitted on the walk to the shelf, then its carry "
        "unexplained; no other hypothesis admitted there. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 250),
            scheduled_tasks=Script([
                deliver_item("item_62", table="kitting_table_0"),
                deliver_item("item_63", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_63", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -200),
            assigned_tasks=[
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)


# T-F part 1, part 1b (5 October 2026): copies with a fact in force (analysis/kitting/tf1/make_copies.py; REPORT.md, "Part 1").
scenario_s29_51 = ScenarioConfig(
    id="scenario_s29_51",
    setup="env_setup_29",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 34),)),
    description=(
        "T-F part 1, part 1b: scenario_s29_48's copy with a fact in force, not in accord: break_time over ticks 0 to 34 (deliver_item(item_62,kitting_table_0)). "
        "Everything else is scenario_s29_48's (analysis/kitting/tf1/make_copies.py)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 250),
            scheduled_tasks=Script([
                deliver_item("item_62", table="kitting_table_0"),
                deliver_item("item_63", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_62", table="kitting_table_1"),
                deliver_item("item_63", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -200),
            assigned_tasks=[
                deliver_item("item_64", table="kitting_table_0"),
                deliver_item("item_65", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

