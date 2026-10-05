# domains/kitting/scenarios/scenarios_s28.py
"""
Kitting scenarios on env_setup_28: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_20; the shift
env_setup_28: env_setup_07's shift with item_7 (shelf_3 to kitting_table_0, along the north wall past the coffee machine) and item_8 (shelf_6 to kitting_table_1) added.
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

# ---- script 076: deliveries only: scenario_s07_01's two deliveries, then the exit walk
scenario_s28_01 = ScenarioConfig(
    id="scenario_s28_01",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_01: script 076 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: scenario_s07_01's two deliveries, then the exit walk. Aspects: "
        "deliveries: two, kitting_table_0 then kitting_table_1; start: west, first walk away from the "
        "machine; robot: scenario_s07_01's side without item_6, crossing at kitting_table_1. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-850, 250),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
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

scenario_s28_02 = ScenarioConfig(
    id="scenario_s28_02",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_02: script 076 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: scenario_s07_01's two deliveries, then the exit walk. Aspects: "
        "deliveries: two, kitting_table_0 then kitting_table_1; start: west, first walk away from the "
        "machine; robot: scenario_s07_01's side without item_6, crossing at kitting_table_1. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior). "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-850, 250),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s28_03 = ScenarioConfig(
    id="scenario_s28_03",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 35),)),
    description=(
        "scenario_s28_03: script 076 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 35. Purpose: deliveries only: "
        "scenario_s07_01's two deliveries, then the exit walk. Aspects: deliveries: two, kitting_table_0 "
        "then kitting_table_1; start: west, first walk away from the machine; robot: scenario_s07_01's side "
        "without item_6, crossing at kitting_table_1. Expectation: the delivery under break_time admitted "
        "later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-850, 250),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
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

scenario_s28_04 = ScenarioConfig(
    id="scenario_s28_04",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 35),)),
    description=(
        "scenario_s28_04: script 076 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 35. Purpose: deliveries only: "
        "scenario_s07_01's two deliveries, then the exit walk. Aspects: deliveries: two, kitting_table_0 "
        "then kitting_table_1; start: west, first walk away from the machine; robot: scenario_s07_01's side "
        "without item_6, crossing at kitting_table_1. Expectation: the delivery under break_time admitted "
        "later than with no fact, near off. working robot: the decisions as off where no admission moves; an "
        "earlier admission of a delivery moves the response decision earlier or leaves it; under the window "
        "the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-850, 250),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 077: deliveries only: the walk from kitting_table_0 to shelf_3 along the north wall heads straight at the coffee machine
scenario_s28_05 = ScenarioConfig(
    id="scenario_s28_05",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_05: script 077 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: the walk from kitting_table_0 to shelf_3 along the north wall heads "
        "straight at the coffee machine. Aspects: deliveries: two to kitting_table_0; approach toward the "
        "machine (the same bearing); robot: south-east, apart. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 350),
            scheduled_tasks=Script([
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
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

scenario_s28_06 = ScenarioConfig(
    id="scenario_s28_06",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_06: script 077 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: the walk from kitting_table_0 to shelf_3 along the north wall heads "
        "straight at the coffee machine. Aspects: deliveries: two to kitting_table_0; approach toward the "
        "machine (the same bearing); robot: south-east, apart. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior). working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 350),
            scheduled_tasks=Script([
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, -300),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s28_07 = ScenarioConfig(
    id="scenario_s28_07",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 123),)),
    description=(
        "scenario_s28_07: script 077 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 123. Purpose: deliveries only: the walk "
        "from kitting_table_0 to shelf_3 along the north wall heads straight at the coffee machine. Aspects: "
        "deliveries: two to kitting_table_0; approach toward the machine (the same bearing); robot: "
        "south-east, apart. Expectation: the delivery under break_time admitted later than with no fact, "
        "near off; a delivery whose walk heads toward the machine may lose its admission to the raised "
        "coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 350),
            scheduled_tasks=Script([
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
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

scenario_s28_08 = ScenarioConfig(
    id="scenario_s28_08",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 123),)),
    description=(
        "scenario_s28_08: script 077 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 123. Purpose: deliveries only: the walk "
        "from kitting_table_0 to shelf_3 along the north wall heads straight at the coffee machine. Aspects: "
        "deliveries: two to kitting_table_0; approach toward the machine (the same bearing); robot: "
        "south-east, apart. Expectation: the delivery under break_time admitted later than with no fact, "
        "near off; a delivery whose walk heads toward the machine may lose its admission to the raised "
        "coffee break. working robot: the decisions as off where no admission moves; an earlier admission of "
        "a delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 350),
            scheduled_tasks=Script([
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(500, -300),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_4", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 078: a coffee break at the start
scenario_s28_09 = ScenarioConfig(
    id="scenario_s28_09",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_09: script 078 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the start. Aspects: foreseeable: at the start; start: by "
        "kitting_table_0, first walk east toward the machine; deliveries: both tables. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "a coffee break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_1"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_1"),
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

scenario_s28_10 = ScenarioConfig(
    id="scenario_s28_10",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_10: script 078 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the start. Aspects: foreseeable: at the start; start: by "
        "kitting_table_0, first walk east toward the machine; deliveries: both tables. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "a coffee break admitted later than off (ordinary strength). working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_1"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(800, -200),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s28_11 = ScenarioConfig(
    id="scenario_s28_11",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 54),)),
    description=(
        "scenario_s28_11: script 078 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 0 to 54. Purpose: a coffee break at the start. Aspects: "
        "foreseeable: at the start; start: by kitting_table_0, first walk east toward the machine; "
        "deliveries: both tables. Expectation: the coffee break (raised by break_time) admitted earlier than "
        "off and than on with no fact; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_1"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_1"),
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

scenario_s28_12 = ScenarioConfig(
    id="scenario_s28_12",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 54),)),
    description=(
        "scenario_s28_12: script 078 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 0 to 54. Purpose: a coffee break at the start. "
        "Aspects: foreseeable: at the start; start: by kitting_table_0, first walk east toward the machine; "
        "deliveries: both tables. Expectation: the coffee break (raised by break_time) admitted earlier than "
        "off and than on with no fact; a delivery inside a window admitted later than with no fact. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; the coffee break admitted earlier, the robot's decision "
        "against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_1"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(800, -200),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s28_13 = ScenarioConfig(
    id="scenario_s28_13",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 54, 132),)),
    description=(
        "scenario_s28_13: script 078 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 54 to 132. Purpose: a coffee break at the "
        "start. Aspects: foreseeable: at the start; start: by kitting_table_0, first walk east toward the "
        "machine; deliveries: both tables. Expectation: the delivery under break_time admitted later than "
        "with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to "
        "the raised coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_1"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_1"),
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

scenario_s28_14 = ScenarioConfig(
    id="scenario_s28_14",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 54, 132),)),
    description=(
        "scenario_s28_14: script 078 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 54 to 132. Purpose: a coffee break at the "
        "start. Aspects: foreseeable: at the start; start: by kitting_table_0, first walk east toward the "
        "machine; deliveries: both tables. Expectation: the delivery under break_time admitted later than "
        "with no fact, near off; a delivery whose walk heads toward the machine may lose its admission to "
        "the raised coffee break. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; under the window the "
        "delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_1"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(800, -200),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 079: a coffee break between deliveries, the next delivery leaving from the machine
scenario_s28_15 = ScenarioConfig(
    id="scenario_s28_15",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_15: script 079 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break between deliveries, the next delivery leaving from the machine. Aspects: "
        "foreseeable: between deliveries; robot: centre start, item_1 across the room, crossing. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior); a coffee break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, -300),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
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

scenario_s28_16 = ScenarioConfig(
    id="scenario_s28_16",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_16: script 079 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break between deliveries, the next delivery leaving from the machine. Aspects: "
        "foreseeable: between deliveries; robot: centre start, item_1 across the room, crossing. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior); a coffee break admitted later than off (ordinary strength). working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, -300),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, -100),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_1", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s28_17 = ScenarioConfig(
    id="scenario_s28_17",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 58, 120),)),
    description=(
        "scenario_s28_17: script 079 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 58 to 120. Purpose: a coffee break between deliveries, "
        "the next delivery leaving from the machine. Aspects: foreseeable: between deliveries; robot: centre "
        "start, item_1 across the room, crossing. Expectation: the coffee break (raised by break_time) "
        "admitted earlier than off and than on with no fact; a delivery inside a window admitted later than "
        "with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, -300),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
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

scenario_s28_18 = ScenarioConfig(
    id="scenario_s28_18",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 58, 120),)),
    description=(
        "scenario_s28_18: script 079 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 58 to 120. Purpose: a coffee break between "
        "deliveries, the next delivery leaving from the machine. Aspects: foreseeable: between deliveries; "
        "robot: centre start, item_1 across the room, crossing. Expectation: the coffee break (raised by "
        "break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted "
        "later than with no fact. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; the coffee break admitted "
        "earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, -300),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, -100),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_1", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s28_19 = ScenarioConfig(
    id="scenario_s28_19",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 58),)),
    description=(
        "scenario_s28_19: script 079 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 58. Purpose: a coffee break between "
        "deliveries, the next delivery leaving from the machine. Aspects: foreseeable: between deliveries; "
        "robot: centre start, item_1 across the room, crossing. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, -300),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
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

scenario_s28_20 = ScenarioConfig(
    id="scenario_s28_20",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 58),)),
    description=(
        "scenario_s28_20: script 079 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 58. Purpose: a coffee break between "
        "deliveries, the next delivery leaving from the machine. Aspects: foreseeable: between deliveries; "
        "robot: centre start, item_1 across the room, crossing. Expectation: the delivery under break_time "
        "admitted later than with no fact, near off. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it; under "
        "the window the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, -300),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, -100),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_1", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 080: a coffee break inside a delivery after the grasp, at the machine along the wall from shelf_3
scenario_s28_21 = ScenarioConfig(
    id="scenario_s28_21",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_21: script 080 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery after the grasp, at the machine along the wall from "
        "shelf_3. Aspects: foreseeable: inside a delivery, after the grasp. Expectation: on against off: "
        "each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee "
        "break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, 100),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s28_22 = ScenarioConfig(
    id="scenario_s28_22",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_22: script 080 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery after the grasp, at the machine along the wall from "
        "shelf_3. Aspects: foreseeable: inside a delivery, after the grasp. Expectation: on against off: "
        "each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee "
        "break admitted later than off (ordinary strength). working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, 100),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, -100),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_8", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s28_23 = ScenarioConfig(
    id="scenario_s28_23",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 25, 84),)),
    description=(
        "scenario_s28_23: script 080 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 25 to 84. Purpose: a coffee break inside a delivery "
        "after the grasp, at the machine along the wall from shelf_3. Aspects: foreseeable: inside a "
        "delivery, after the grasp. Expectation: the coffee break (raised by break_time) admitted earlier "
        "than off and than on with no fact; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, 100),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s28_24 = ScenarioConfig(
    id="scenario_s28_24",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 25, 84),)),
    description=(
        "scenario_s28_24: script 080 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 25 to 84. Purpose: a coffee break inside a delivery "
        "after the grasp, at the machine along the wall from shelf_3. Aspects: foreseeable: inside a "
        "delivery, after the grasp. Expectation: the coffee break (raised by break_time) admitted earlier "
        "than off and than on with no fact; a delivery inside a window admitted later than with no fact. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it; the coffee break admitted earlier, the robot's "
        "decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, 100),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, -100),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_8", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s28_25 = ScenarioConfig(
    id="scenario_s28_25",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 134, 243),)),
    description=(
        "scenario_s28_25: script 080 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 134 to 243. Purpose: a coffee break inside a "
        "delivery after the grasp, at the machine along the wall from shelf_3. Aspects: foreseeable: inside "
        "a delivery, after the grasp. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, 100),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s28_26 = ScenarioConfig(
    id="scenario_s28_26",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 134, 243),)),
    description=(
        "scenario_s28_26: script 080 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 134 to 243. Purpose: a coffee break inside a "
        "delivery after the grasp, at the machine along the wall from shelf_3. Aspects: foreseeable: inside "
        "a delivery, after the grasp. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off. working robot: the decisions as off where no admission moves; an earlier admission "
        "of a delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, 100),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_NW"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, -100),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_8", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 081: a coffee break inside a delivery at the table before the release: from the south table back across the room to the machine
scenario_s28_27 = ScenarioConfig(
    id="scenario_s28_27",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_27: script 081 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery at the table before the release: from the south table "
        "back across the room to the machine. Aspects: foreseeable: inside a delivery, before the release; "
        "deliveries: one; robot: to kitting_table_1, where the human's part waits in hand. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "a coffee break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, 0),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=1),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_1"),
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

scenario_s28_28 = ScenarioConfig(
    id="scenario_s28_28",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_28: script 081 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery at the table before the release: from the south table "
        "back across the room to the machine. Aspects: foreseeable: inside a delivery, before the release; "
        "deliveries: one; robot: to kitting_table_1, where the human's part waits in hand. Expectation: on "
        "against off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); "
        "a coffee break admitted later than off (ordinary strength). working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, 0),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=1),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s28_29 = ScenarioConfig(
    id="scenario_s28_29",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 93, 172),)),
    description=(
        "scenario_s28_29: script 081 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 93 to 172. Purpose: a coffee break inside a delivery at "
        "the table before the release: from the south table back across the room to the machine. Aspects: "
        "foreseeable: inside a delivery, before the release; deliveries: one; robot: to kitting_table_1, "
        "where the human's part waits in hand. Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; a delivery inside a window admitted later than with no "
        "fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, 0),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=1),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_1"),
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

scenario_s28_30 = ScenarioConfig(
    id="scenario_s28_30",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 93, 172),)),
    description=(
        "scenario_s28_30: script 081 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 93 to 172. Purpose: a coffee break inside a delivery "
        "at the table before the release: from the south table back across the room to the machine. Aspects: "
        "foreseeable: inside a delivery, before the release; deliveries: one; robot: to kitting_table_1, "
        "where the human's part waits in hand. Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; a delivery inside a window admitted later than with no "
        "fact. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; the coffee break admitted earlier, the "
        "robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, 0),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=1),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 082: a second coffee break soon after the first
scenario_s28_31 = ScenarioConfig(
    id="scenario_s28_31",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_31: script 082 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a second coffee break soon after the first. Aspects: foreseeable: two coffee breaks, "
        "between and at the end; deliveries: kitting_table_1 then kitting_table_0. Expectation: on against "
        "off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee "
        "break admitted later than off (ordinary strength); the second under its recency fact (suppressed), "
        "later still."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -200),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_7", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_7", table="kitting_table_0"),
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

scenario_s28_32 = ScenarioConfig(
    id="scenario_s28_32",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_32: script 082 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a second coffee break soon after the first. Aspects: foreseeable: two coffee breaks, "
        "between and at the end; deliveries: kitting_table_1 then kitting_table_0. Expectation: on against "
        "off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee "
        "break admitted later than off (ordinary strength); the second under its recency fact (suppressed), "
        "later still. working robot: the decisions as off where no admission moves; an earlier admission of "
        "a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -200),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_7", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 0),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s28_33 = ScenarioConfig(
    id="scenario_s28_33",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 35, 115), window(BREAK_TIME, 206, 268),)),
    description=(
        "scenario_s28_33: script 082 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 35 to 115, break_time from 206 to 268. Purpose: a second "
        "coffee break soon after the first. Aspects: foreseeable: two coffee breaks, between and at the end; "
        "deliveries: kitting_table_1 then kitting_table_0. Expectation: the coffee break (raised by "
        "break_time) admitted earlier than off and than on with no fact; the second one suppressed by its "
        "recency fact, the window gives it nothing; a delivery inside a window admitted later than with no "
        "fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -200),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_7", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_7", table="kitting_table_0"),
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

scenario_s28_34 = ScenarioConfig(
    id="scenario_s28_34",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 35, 115), window(BREAK_TIME, 206, 268),)),
    description=(
        "scenario_s28_34: script 082 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 35 to 115, break_time from 206 to 268. Purpose: a "
        "second coffee break soon after the first. Aspects: foreseeable: two coffee breaks, between and at "
        "the end; deliveries: kitting_table_1 then kitting_table_0. Expectation: the coffee break (raised by "
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
            start_position=(900, -200),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_7", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 0),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s28_35 = ScenarioConfig(
    id="scenario_s28_35",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 35),)),
    description=(
        "scenario_s28_35: script 082 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 35. Purpose: a second coffee break soon "
        "after the first. Aspects: foreseeable: two coffee breaks, between and at the end; deliveries: "
        "kitting_table_1 then kitting_table_0. Expectation: the delivery under break_time admitted later "
        "than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -200),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_7", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_7", table="kitting_table_0"),
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

scenario_s28_36 = ScenarioConfig(
    id="scenario_s28_36",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 35),)),
    description=(
        "scenario_s28_36: script 082 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 35. Purpose: a second coffee break soon "
        "after the first. Aspects: foreseeable: two coffee breaks, between and at the end; deliveries: "
        "kitting_table_1 then kitting_table_0. Expectation: the delivery under break_time admitted later "
        "than with no fact, near off. working robot: the decisions as off where no admission moves; an "
        "earlier admission of a delivery moves the response decision earlier or leaves it; under the window "
        "the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -200),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_7", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_1"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, 0),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 083: unmodelled alone: a stand of 40 ticks at the start, at kitting_table_1
scenario_s28_37 = ScenarioConfig(
    id="scenario_s28_37",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_37: script 083 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a stand of 40 ticks at the start, at kitting_table_1. Aspects: "
        "unmodelled: a stand (40 ticks) at the start; deliveries: two to kitting_table_1; robot: to "
        "kitting_table_0, apart. Expectation: on against off: each delivery admitted earlier or equal (the "
        "assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, "
        "except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, -350),
            scheduled_tasks=Script([
                stand("PT80S"),
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_8", table="kitting_table_1"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_8", table="kitting_table_1"),
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

scenario_s28_38 = ScenarioConfig(
    id="scenario_s28_38",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_38: script 083 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a stand of 40 ticks at the start, at kitting_table_1. Aspects: "
        "unmodelled: a stand (40 ticks) at the start; deliveries: two to kitting_table_1; robot: to "
        "kitting_table_0, apart. Expectation: on against off: each delivery admitted earlier or equal (the "
        "assigned tasks share most of the prior); no admission during the stand or the walk elsewhere, "
        "except a hypothesis whose target lies on the walk. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, -350),
            scheduled_tasks=Script([
                stand("PT80S"),
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_8", table="kitting_table_1"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_8", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 300),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s28_39 = ScenarioConfig(
    id="scenario_s28_39",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 41, 99),)),
    description=(
        "scenario_s28_39: script 083 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 41 to 99. Purpose: unmodelled alone: a stand "
        "of 40 ticks at the start, at kitting_table_1. Aspects: unmodelled: a stand (40 ticks) at the start; "
        "deliveries: two to kitting_table_1; robot: to kitting_table_0, apart. Expectation: the delivery "
        "under break_time admitted later than with no fact, near off; no admission during the stand or the "
        "walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, -350),
            scheduled_tasks=Script([
                stand("PT80S"),
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_8", table="kitting_table_1"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_8", table="kitting_table_1"),
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

scenario_s28_40 = ScenarioConfig(
    id="scenario_s28_40",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 41, 99),)),
    description=(
        "scenario_s28_40: script 083 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 41 to 99. Purpose: unmodelled alone: a stand "
        "of 40 ticks at the start, at kitting_table_1. Aspects: unmodelled: a stand (40 ticks) at the start; "
        "deliveries: two to kitting_table_1; robot: to kitting_table_0, apart. Expectation: the delivery "
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
            start_position=(500, -350),
            scheduled_tasks=Script([
                stand("PT80S"),
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_8", table="kitting_table_1"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_8", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 300),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 084: unmodelled with a foreseeable task: a walk to corner_NW and a stand of 20 ticks, then a coffee break
scenario_s28_41 = ScenarioConfig(
    id="scenario_s28_41",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_41: script 084 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a walk to corner_NW and a stand of 20 ticks, then a "
        "coffee break. Aspects: unmodelled: a walk elsewhere with a stand (20 ticks); foreseeable: right "
        "after it. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); a coffee break admitted later than off (ordinary strength); no admission "
        "during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 100),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                go_to_and_stand("corner_NW", "PT40S"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
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

scenario_s28_42 = ScenarioConfig(
    id="scenario_s28_42",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_42: script 084 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a walk to corner_NW and a stand of 20 ticks, then a "
        "coffee break. Aspects: unmodelled: a walk elsewhere with a stand (20 ticks); foreseeable: right "
        "after it. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); a coffee break admitted later than off (ordinary strength); no admission "
        "during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 100),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                go_to_and_stand("corner_NW", "PT40S"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, -300),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_1"),
                deliver_item("item_8", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s28_43 = ScenarioConfig(
    id="scenario_s28_43",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 85, 169),)),
    description=(
        "scenario_s28_43: script 084 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 85 to 169. Purpose: unmodelled with a foreseeable task: "
        "a walk to corner_NW and a stand of 20 ticks, then a coffee break. Aspects: unmodelled: a walk "
        "elsewhere with a stand (20 ticks); foreseeable: right after it. Expectation: the coffee break "
        "(raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a "
        "window admitted later than with no fact; no admission during the stand or the walk elsewhere, "
        "except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 100),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                go_to_and_stand("corner_NW", "PT40S"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
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

scenario_s28_44 = ScenarioConfig(
    id="scenario_s28_44",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 85, 169),)),
    description=(
        "scenario_s28_44: script 084 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 85 to 169. Purpose: unmodelled with a foreseeable "
        "task: a walk to corner_NW and a stand of 20 ticks, then a coffee break. Aspects: unmodelled: a walk "
        "elsewhere with a stand (20 ticks); foreseeable: right after it. Expectation: the coffee break "
        "(raised by break_time) admitted earlier than off and than on with no fact; a delivery inside a "
        "window admitted later than with no fact; no admission during the stand or the walk elsewhere, "
        "except a hypothesis whose target lies on the walk. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 100),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                go_to_and_stand("corner_NW", "PT40S"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, -300),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_1"),
                deliver_item("item_8", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s28_45 = ScenarioConfig(
    id="scenario_s28_45",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 42),)),
    description=(
        "scenario_s28_45: script 084 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 42. Purpose: unmodelled with a "
        "foreseeable task: a walk to corner_NW and a stand of 20 ticks, then a coffee break. Aspects: "
        "unmodelled: a walk elsewhere with a stand (20 ticks); foreseeable: right after it. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off; no admission during the stand "
        "or the walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 100),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                go_to_and_stand("corner_NW", "PT40S"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
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

scenario_s28_46 = ScenarioConfig(
    id="scenario_s28_46",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 42),)),
    description=(
        "scenario_s28_46: script 084 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 42. Purpose: unmodelled with a "
        "foreseeable task: a walk to corner_NW and a stand of 20 ticks, then a coffee break. Aspects: "
        "unmodelled: a walk elsewhere with a stand (20 ticks); foreseeable: right after it. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off; no admission during the stand "
        "or the walk elsewhere, except a hypothesis whose target lies on the walk. working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it; under the window the delivery's admission and the robot's decision "
        "on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 100),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                go_to_and_stand("corner_NW", "PT40S"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, -300),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_1"),
                deliver_item("item_8", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 085: unmodelled alone: a delivery to the other table (item_6 to kitting_table_1) and a never-started delivery
scenario_s28_47 = ScenarioConfig(
    id="scenario_s28_47",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_47: script 085 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a delivery to the other table (item_6 to kitting_table_1) and a "
        "never-started delivery. Aspects: unmodelled: a delivery to the other table, a never-started "
        "delivery. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); the never-started delivery never admitted (no observation warrant); the "
        "delivery to the other table: admitted on the walk to the shelf, then its carry unexplained; no "
        "other hypothesis admitted there."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, -300),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_1"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
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

scenario_s28_48 = ScenarioConfig(
    id="scenario_s28_48",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    description=(
        "scenario_s28_48: script 085 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a delivery to the other table (item_6 to kitting_table_1) and a "
        "never-started delivery. Aspects: unmodelled: a delivery to the other table, a never-started "
        "delivery. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); the never-started delivery never admitted (no observation warrant); the "
        "delivery to the other table: admitted on the walk to the shelf, then its carry unexplained; no "
        "other hypothesis admitted there. working robot: the decisions as off where no admission moves; an "
        "earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, -300),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_1"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, 0),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)


# T-F part 1, part 1b (5 October 2026): copies with a fact in force (analysis/kitting/tf1/make_copies.py; REPORT.md, "Part 1").
scenario_s28_49 = ScenarioConfig(
    id="scenario_s28_49",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 93),)),
    description=(
        "T-F part 1, part 1b: scenario_s28_28's copy with a fact in force, not in accord: break_time over ticks 0 to 93 (deliver_item(item_1,kitting_table_1)). "
        "Everything else is scenario_s28_28's (analysis/kitting/tf1/make_copies.py)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, 0),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=1),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(900, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)


scenario_s28_50 = ScenarioConfig(
    id="scenario_s28_50",
    setup="env_setup_28",
    reference_layouts=["env_layout_20"],
    timeline=Timeline((window(BREAK_TIME, 0, 79),)),
    description=(
        "T-F part 1, part 1b: scenario_s28_48's copy with a fact in force, not in accord: break_time over ticks 0 to 79 (deliver_item(item_6,kitting_table_1)). "
        "Everything else is scenario_s28_48's (analysis/kitting/tf1/make_copies.py)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, -300),
            scheduled_tasks=Script([
                deliver_item("item_6", table="kitting_table_1"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, 0),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_1"),
                deliver_item("item_5", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

