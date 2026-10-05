# domains/kitting/scenarios/scenarios_s23.py
"""
Kitting scenarios on env_setup_23: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_07; the shift
env_setup_23: env_setup_05's shift, so the script of scenario_s05_01 and scenario_s05_02 has its copies here.
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

# ---- script 035: the script of scenario_s05_01 and scenario_s05_02 as it is: a coffee break at the start, the delivery from the shelf beside the machine, the A/C activation at the end; no exit walk
scenario_s23_01 = ScenarioConfig(
    id="scenario_s23_01",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s23_01: script 035 of step 5e (the script of scenario_s05_01 and scenario_s05_02, as it "
        "is), the idle robot, no timeline (the setup states none). Purpose: the script of scenario_s05_01 "
        "and scenario_s05_02 as it is: a coffee break at the start, the delivery from the shelf beside the "
        "machine, the A/C activation at the end; no exit walk. Aspects: foreseeable: at the start and at the "
        "end; existing (two robot sides). Expectation: on against off: each delivery admitted earlier or "
        "equal (the assigned tasks share most of the prior); a coffee break admitted later than off "
        "(ordinary strength); the A/C activation rarely admitted on or off; its belief at arrival lower on "
        "(ordinary 0.02 against the assigned tasks)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s23_02 = ScenarioConfig(
    id="scenario_s23_02",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 56), window(ROOM_WARM, 96, 143),)),
    description=(
        "scenario_s23_02: script 035 of step 5e (the script of scenario_s05_01 and scenario_s05_02, as it "
        "is), the idle robot, its own timeline, the raising fact over the foreseeable task (accord): "
        "break_time from 0 to 56, room_warm from 96 to 143. Purpose: the script of scenario_s05_01 and "
        "scenario_s05_02 as it is: a coffee break at the start, the delivery from the shelf beside the "
        "machine, the A/C activation at the end; no exit walk. Aspects: foreseeable: at the start and at the "
        "end; existing (two robot sides). Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; the A/C activation's belief at arrival higher than with "
        "no fact (raised by room_warm); admission possible only where the movement evidence allows; a "
        "delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s23_03 = ScenarioConfig(
    id="scenario_s23_03",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 56), window(ROOM_WARM, 96, 143),)),
    description=(
        "scenario_s23_03: script 035 of step 5e (the script of scenario_s05_01 and scenario_s05_02, as it "
        "is), the working robot, its own timeline, the raising fact over the foreseeable task (accord): "
        "break_time from 0 to 56, room_warm from 96 to 143. Purpose: the script of scenario_s05_01 and "
        "scenario_s05_02 as it is: a coffee break at the start, the delivery from the shelf beside the "
        "machine, the A/C activation at the end; no exit walk. Aspects: foreseeable: at the start and at the "
        "end; existing (two robot sides). Expectation: the coffee break (raised by break_time) admitted "
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
            start_position=(510, -550),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_04 = ScenarioConfig(
    id="scenario_s23_04",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 56), window(ROOM_WARM, 96, 143),)),
    description=(
        "scenario_s23_04: script 035 of step 5e (the script of scenario_s05_01 and scenario_s05_02, as it "
        "is), the working robot, its own timeline, the raising fact over the foreseeable task (accord): "
        "break_time from 0 to 56, room_warm from 96 to 143. Purpose: the script of scenario_s05_01 and "
        "scenario_s05_02 as it is: a coffee break at the start, the delivery from the shelf beside the "
        "machine, the A/C activation at the end; no exit walk. Aspects: foreseeable: at the start and at the "
        "end; existing (two robot sides). Expectation: the coffee break (raised by break_time) admitted "
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
            start_position=(510, -550),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_05 = ScenarioConfig(
    id="scenario_s23_05",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 56, 96),)),
    description=(
        "scenario_s23_05: script 035 of step 5e (the script of scenario_s05_01 and scenario_s05_02, as it "
        "is), the idle robot, its own timeline, break_time over a delivery (the human works through it): "
        "break_time from 56 to 96. Purpose: the script of scenario_s05_01 and scenario_s05_02 as it is: a "
        "coffee break at the start, the delivery from the shelf beside the machine, the A/C activation at "
        "the end; no exit walk. Aspects: foreseeable: at the start and at the end; existing (two robot "
        "sides). Expectation: the delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s23_06 = ScenarioConfig(
    id="scenario_s23_06",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 56, 96),)),
    description=(
        "scenario_s23_06: script 035 of step 5e (the script of scenario_s05_01 and scenario_s05_02, as it "
        "is), the working robot, its own timeline, break_time over a delivery (the human works through it): "
        "break_time from 56 to 96. Purpose: the script of scenario_s05_01 and scenario_s05_02 as it is: a "
        "coffee break at the start, the delivery from the shelf beside the machine, the A/C activation at "
        "the end; no exit walk. Aspects: foreseeable: at the start and at the end; existing (two robot "
        "sides). Expectation: the delivery under break_time admitted later than with no fact, near off. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it; under the window the delivery's admission and the "
        "robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_07 = ScenarioConfig(
    id="scenario_s23_07",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 56, 96),)),
    description=(
        "scenario_s23_07: script 035 of step 5e (the script of scenario_s05_01 and scenario_s05_02, as it "
        "is), the working robot, its own timeline, break_time over a delivery (the human works through it): "
        "break_time from 56 to 96. Purpose: the script of scenario_s05_01 and scenario_s05_02 as it is: a "
        "coffee break at the start, the delivery from the shelf beside the machine, the A/C activation at "
        "the end; no exit walk. Aspects: foreseeable: at the start and at the end; existing (two robot "
        "sides). Expectation: the delivery under break_time admitted later than with no fact, near off. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it; under the window the delivery's admission and the "
        "robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 036: deliveries only: the first approach heads straight at the coffee machine (shelf_5 beside it)
scenario_s23_08 = ScenarioConfig(
    id="scenario_s23_08",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s23_08: script 036 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: the first approach heads straight at the coffee machine (shelf_5 beside "
        "it). Aspects: deliveries: two; approach toward the machine; robot: scenario_s05_01's side, its "
        "first route past the machine. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s23_09 = ScenarioConfig(
    id="scenario_s23_09",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s23_09: script 036 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: the first approach heads straight at the coffee machine (shelf_5 beside "
        "it). Aspects: deliveries: two; approach toward the machine; robot: scenario_s05_01's side, its "
        "first route past the machine. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior). working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_10 = ScenarioConfig(
    id="scenario_s23_10",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 64),)),
    description=(
        "scenario_s23_10: script 036 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 64. Purpose: deliveries only: the first "
        "approach heads straight at the coffee machine (shelf_5 beside it). Aspects: deliveries: two; "
        "approach toward the machine; robot: scenario_s05_01's side, its first route past the machine. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off; a delivery "
        "whose walk heads toward the machine may lose its admission to the raised coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s23_11 = ScenarioConfig(
    id="scenario_s23_11",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 64),)),
    description=(
        "scenario_s23_11: script 036 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 64. Purpose: deliveries only: the first "
        "approach heads straight at the coffee machine (shelf_5 beside it). Aspects: deliveries: two; "
        "approach toward the machine; robot: scenario_s05_01's side, its first route past the machine. "
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
            start_position=(510, -550),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_12 = ScenarioConfig(
    id="scenario_s23_12",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(ROOM_WARM, 0, 64),)),
    description=(
        "scenario_s23_12: script 036 of step 5e, the idle robot, its own timeline, room_warm over a delivery "
        "(the human works through it): room_warm from 0 to 64. Purpose: deliveries only: the first approach "
        "heads straight at the coffee machine (shelf_5 beside it). Aspects: deliveries: two; approach toward "
        "the machine; robot: scenario_s05_01's side, its first route past the machine. Expectation: the "
        "delivery under room_warm admitted later than with no fact, by less than under break_time (raised "
        "0.5 against 2)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s23_13 = ScenarioConfig(
    id="scenario_s23_13",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(ROOM_WARM, 0, 64),)),
    description=(
        "scenario_s23_13: script 036 of step 5e, the working robot, its own timeline, room_warm over a "
        "delivery (the human works through it): room_warm from 0 to 64. Purpose: deliveries only: the first "
        "approach heads straight at the coffee machine (shelf_5 beside it). Aspects: deliveries: two; "
        "approach toward the machine; robot: scenario_s05_01's side, its first route past the machine. "
        "Expectation: the delivery under room_warm admitted later than with no fact, by less than under "
        "break_time (raised 0.5 against 2). working robot: the decisions as off where no admission moves; an "
        "earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 037: the A/C activation alone, at the start
scenario_s23_14 = ScenarioConfig(
    id="scenario_s23_14",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s23_14: script 037 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: the A/C activation alone, at the start. Aspects: foreseeable: the A/C alone, at the start; "
        "start: north-east of the table. Expectation: on against off: each delivery admitted earlier or "
        "equal (the assigned tasks share most of the prior); the A/C activation rarely admitted on or off; "
        "its belief at arrival lower on (ordinary 0.02 against the assigned tasks)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 300),
            scheduled_tasks=Script([
                ac_activation("ac_switch_0"),
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s23_15 = ScenarioConfig(
    id="scenario_s23_15",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s23_15: script 037 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: the A/C activation alone, at the start. Aspects: foreseeable: the A/C alone, at the start; "
        "start: north-east of the table. Expectation: on against off: each delivery admitted earlier or "
        "equal (the assigned tasks share most of the prior); the A/C activation rarely admitted on or off; "
        "its belief at arrival lower on (ordinary 0.02 against the assigned tasks). working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 300),
            scheduled_tasks=Script([
                ac_activation("ac_switch_0"),
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_16 = ScenarioConfig(
    id="scenario_s23_16",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(ROOM_WARM, 0, 49),)),
    description=(
        "scenario_s23_16: script 037 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): room_warm from 0 to 49. Purpose: the A/C activation alone, at the start. "
        "Aspects: foreseeable: the A/C alone, at the start; start: north-east of the table. Expectation: the "
        "A/C activation's belief at arrival higher than with no fact (raised by room_warm); admission "
        "possible only where the movement evidence allows; a delivery inside a window admitted later than "
        "with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 300),
            scheduled_tasks=Script([
                ac_activation("ac_switch_0"),
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s23_17 = ScenarioConfig(
    id="scenario_s23_17",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(ROOM_WARM, 0, 49),)),
    description=(
        "scenario_s23_17: script 037 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): room_warm from 0 to 49. Purpose: the A/C activation alone, at the "
        "start. Aspects: foreseeable: the A/C alone, at the start; start: north-east of the table. "
        "Expectation: the A/C activation's belief at arrival higher than with no fact (raised by room_warm); "
        "admission possible only where the movement evidence allows; a delivery inside a window admitted "
        "later than with no fact. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 300),
            scheduled_tasks=Script([
                ac_activation("ac_switch_0"),
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_18 = ScenarioConfig(
    id="scenario_s23_18",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 49, 123),)),
    description=(
        "scenario_s23_18: script 037 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 49 to 123. Purpose: the A/C activation "
        "alone, at the start. Aspects: foreseeable: the A/C alone, at the start; start: north-east of the "
        "table. Expectation: the delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 300),
            scheduled_tasks=Script([
                ac_activation("ac_switch_0"),
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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

scenario_s23_19 = ScenarioConfig(
    id="scenario_s23_19",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 49, 123),)),
    description=(
        "scenario_s23_19: script 037 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 49 to 123. Purpose: the A/C activation "
        "alone, at the start. Aspects: foreseeable: the A/C alone, at the start; start: north-east of the "
        "table. Expectation: the delivery under break_time admitted later than with no fact, near off. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it; under the window the delivery's admission and the "
        "robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 300),
            scheduled_tasks=Script([
                ac_activation("ac_switch_0"),
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("door"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 038: a coffee break inside a delivery: at shelf_5 before the grasp, at the machine beside it
scenario_s23_20 = ScenarioConfig(
    id="scenario_s23_20",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s23_20: script 038 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery: at shelf_5 before the grasp, at the machine beside it. "
        "Aspects: foreseeable: inside a delivery, before the grasp; approach toward the machine; robot: "
        "item_1 past the machine, crossing. Expectation: on against off: each delivery admitted earlier or "
        "equal (the assigned tasks share most of the prior); a coffee break admitted later than off "
        "(ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 400),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s23_21 = ScenarioConfig(
    id="scenario_s23_21",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s23_21: script 038 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery: at shelf_5 before the grasp, at the machine beside it. "
        "Aspects: foreseeable: inside a delivery, before the grasp; approach toward the machine; robot: "
        "item_1 past the machine, crossing. Expectation: on against off: each delivery admitted earlier or "
        "equal (the assigned tasks share most of the prior); a coffee break admitted later than off "
        "(ordinary strength). working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 400),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_22 = ScenarioConfig(
    id="scenario_s23_22",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 48, 84),)),
    description=(
        "scenario_s23_22: script 038 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 48 to 84. Purpose: a coffee break inside a delivery: at "
        "shelf_5 before the grasp, at the machine beside it. Aspects: foreseeable: inside a delivery, before "
        "the grasp; approach toward the machine; robot: item_1 past the machine, crossing. Expectation: the "
        "coffee break (raised by break_time) admitted earlier than off and than on with no fact; a delivery "
        "inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 400),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s23_23 = ScenarioConfig(
    id="scenario_s23_23",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 48, 84),)),
    description=(
        "scenario_s23_23: script 038 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 48 to 84. Purpose: a coffee break inside a delivery: "
        "at shelf_5 before the grasp, at the machine beside it. Aspects: foreseeable: inside a delivery, "
        "before the grasp; approach toward the machine; robot: item_1 past the machine, crossing. "
        "Expectation: the coffee break (raised by break_time) admitted earlier than off and than on with no "
        "fact; a delivery inside a window admitted later than with no fact. working robot: the decisions as "
        "off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 400),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_24 = ScenarioConfig(
    id="scenario_s23_24",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 122, 214),)),
    description=(
        "scenario_s23_24: script 038 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 122 to 214. Purpose: a coffee break inside a "
        "delivery: at shelf_5 before the grasp, at the machine beside it. Aspects: foreseeable: inside a "
        "delivery, before the grasp; approach toward the machine; robot: item_1 past the machine, crossing. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off; a delivery "
        "whose walk heads toward the machine may lose its admission to the raised coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 400),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
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

scenario_s23_25 = ScenarioConfig(
    id="scenario_s23_25",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 122, 214),)),
    description=(
        "scenario_s23_25: script 038 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 122 to 214. Purpose: a coffee break inside a "
        "delivery: at shelf_5 before the grasp, at the machine beside it. Aspects: foreseeable: inside a "
        "delivery, before the grasp; approach toward the machine; robot: item_1 past the machine, crossing. "
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
            start_position=(0, 400),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SW"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 039: unmodelled with a foreseeable task: a delivery abandoned after the grasp, then the A/C activation; the second delivery never started
scenario_s23_26 = ScenarioConfig(
    id="scenario_s23_26",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s23_26: script 039 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery abandoned after the grasp, then the A/C "
        "activation; the second delivery never started. Aspects: unmodelled: an abandoned delivery (after "
        "the grasp), a never-started delivery; foreseeable: the A/C after them. Expectation: on against off: "
        "each delivery admitted earlier or equal (the assigned tasks share most of the prior); the A/C "
        "activation rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the "
        "assigned tasks); the never-started delivery never admitted (no observation warrant); the abandoned "
        "delivery admitted while the human walks to it, then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, 0),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, drop),
                ac_activation("ac_switch_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s23_27 = ScenarioConfig(
    id="scenario_s23_27",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s23_27: script 039 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery abandoned after the grasp, then the A/C "
        "activation; the second delivery never started. Aspects: unmodelled: an abandoned delivery (after "
        "the grasp), a never-started delivery; foreseeable: the A/C after them. Expectation: on against off: "
        "each delivery admitted earlier or equal (the assigned tasks share most of the prior); the A/C "
        "activation rarely admitted on or off; its belief at arrival lower on (ordinary 0.02 against the "
        "assigned tasks); the never-started delivery never admitted (no observation warrant); the abandoned "
        "delivery admitted while the human walks to it, then retracted as the evidence turns. working robot: "
        "the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, 0),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, drop),
                ac_activation("ac_switch_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_28 = ScenarioConfig(
    id="scenario_s23_28",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(ROOM_WARM, 54, 138),)),
    description=(
        "scenario_s23_28: script 039 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): room_warm from 54 to 138. Purpose: unmodelled with a foreseeable task: a "
        "delivery abandoned after the grasp, then the A/C activation; the second delivery never started. "
        "Aspects: unmodelled: an abandoned delivery (after the grasp), a never-started delivery; "
        "foreseeable: the A/C after them. Expectation: the A/C activation's belief at arrival higher than "
        "with no fact (raised by room_warm); admission possible only where the movement evidence allows; a "
        "delivery inside a window admitted later than with no fact; the never-started delivery never "
        "admitted (no observation warrant); the abandoned delivery admitted while the human walks to it, "
        "then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, 0),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, drop),
                ac_activation("ac_switch_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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

scenario_s23_29 = ScenarioConfig(
    id="scenario_s23_29",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(ROOM_WARM, 54, 138),)),
    description=(
        "scenario_s23_29: script 039 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): room_warm from 54 to 138. Purpose: unmodelled with a foreseeable "
        "task: a delivery abandoned after the grasp, then the A/C activation; the second delivery never "
        "started. Aspects: unmodelled: an abandoned delivery (after the grasp), a never-started delivery; "
        "foreseeable: the A/C after them. Expectation: the A/C activation's belief at arrival higher than "
        "with no fact (raised by room_warm); admission possible only where the movement evidence allows; a "
        "delivery inside a window admitted later than with no fact; the never-started delivery never "
        "admitted (no observation warrant); the abandoned delivery admitted while the human walks to it, "
        "then retracted as the evidence turns. working robot: the decisions as off where no admission moves; "
        "an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, 0),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, drop),
                ac_activation("ac_switch_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 040: unmodelled alone: a stand of 30 ticks at the table between deliveries
scenario_s23_30 = ScenarioConfig(
    id="scenario_s23_30",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s23_30: script 040 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a stand of 30 ticks at the table between deliveries. Aspects: "
        "unmodelled: a stand (30 ticks), between deliveries. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); no admission during the "
        "stand or the walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                stand("PT60S"),
                deliver_item("item_5", table="kitting_table_0"),
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
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_31 = ScenarioConfig(
    id="scenario_s23_31",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s23_31: script 040 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a stand of 30 ticks at the table between deliveries. Aspects: "
        "unmodelled: a stand (30 ticks), between deliveries. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); no admission during the "
        "stand or the walk elsewhere, except a hypothesis whose target lies on the walk. working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                stand("PT60S"),
                deliver_item("item_5", table="kitting_table_0"),
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
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_32 = ScenarioConfig(
    id="scenario_s23_32",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 95),)),
    description=(
        "scenario_s23_32: script 040 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 95. Purpose: unmodelled alone: a stand "
        "of 30 ticks at the table between deliveries. Aspects: unmodelled: a stand (30 ticks), between "
        "deliveries. Expectation: the delivery under break_time admitted later than with no fact, near off; "
        "no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the "
        "walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                stand("PT60S"),
                deliver_item("item_5", table="kitting_table_0"),
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
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_33 = ScenarioConfig(
    id="scenario_s23_33",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 95),)),
    description=(
        "scenario_s23_33: script 040 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 95. Purpose: unmodelled alone: a stand "
        "of 30 ticks at the table between deliveries. Aspects: unmodelled: a stand (30 ticks), between "
        "deliveries. Expectation: the delivery under break_time admitted later than with no fact, near off; "
        "no admission during the stand or the walk elsewhere, except a hypothesis whose target lies on the "
        "walk. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                stand("PT60S"),
                deliver_item("item_5", table="kitting_table_0"),
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
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_34 = ScenarioConfig(
    id="scenario_s23_34",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(ROOM_WARM, 0, 95),)),
    description=(
        "scenario_s23_34: script 040 of step 5e, the idle robot, its own timeline, room_warm over a delivery "
        "(the human works through it): room_warm from 0 to 95. Purpose: unmodelled alone: a stand of 30 "
        "ticks at the table between deliveries. Aspects: unmodelled: a stand (30 ticks), between deliveries. "
        "Expectation: the delivery under room_warm admitted later than with no fact, by less than under "
        "break_time (raised 0.5 against 2)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                stand("PT60S"),
                deliver_item("item_5", table="kitting_table_0"),
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
            start_position=(-700, 500),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s23_35 = ScenarioConfig(
    id="scenario_s23_35",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(ROOM_WARM, 0, 95),)),
    description=(
        "scenario_s23_35: script 040 of step 5e, the working robot, its own timeline, room_warm over a "
        "delivery (the human works through it): room_warm from 0 to 95. Purpose: unmodelled alone: a stand "
        "of 30 ticks at the table between deliveries. Aspects: unmodelled: a stand (30 ticks), between "
        "deliveries. Expectation: the delivery under room_warm admitted later than with no fact, by less "
        "than under break_time (raised 0.5 against 2). working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                stand("PT60S"),
                deliver_item("item_5", table="kitting_table_0"),
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
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)


# T-F part 1, part 1b (5 October 2026): copies with a fact in force (analysis/kitting/tf1/make_copies.py; REPORT.md, "Part 1").
scenario_s23_36 = ScenarioConfig(
    id="scenario_s23_36",
    setup="env_setup_23",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(ROOM_WARM, 0, 54),)),
    description=(
        "T-F part 1, part 1b: scenario_s23_27's copy with a fact in force, not in accord: room_warm over ticks 0 to 54 (deliver_item(item_3,kitting_table_0)). "
        "Everything else is scenario_s23_27's (analysis/kitting/tf1/make_copies.py)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, 0),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, drop),
                ac_activation("ac_switch_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

