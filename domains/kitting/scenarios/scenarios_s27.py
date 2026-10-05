# domains/kitting/scenarios/scenarios_s27.py
"""
Kitting scenarios on env_setup_27: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_19; the shift
env_setup_27: the near shift: every part goes to the near table (the west side to kitting_table_0, the east side to kitting_table_1); shelf_0 and shelf_3 hold two parts each.
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

# ---- script 066: deliveries only: two parts from one shelf
scenario_s27_01 = ScenarioConfig(
    id="scenario_s27_01",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_01: script 066 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: two parts from one shelf. Aspects: deliveries: two from shelf_0 to "
        "kitting_table_0; start: west wall; robot: east, apart. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -100),
            scheduled_tasks=Script([
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_38", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_38", table="kitting_table_0"),
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

scenario_s27_02 = ScenarioConfig(
    id="scenario_s27_02",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_02: script 066 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: two parts from one shelf. Aspects: deliveries: two from shelf_0 to "
        "kitting_table_0; start: west wall; robot: east, apart. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior). working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -100),
            scheduled_tasks=Script([
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_38", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_38", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, 200),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_35", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s27_03 = ScenarioConfig(
    id="scenario_s27_03",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 63),)),
    description=(
        "scenario_s27_03: script 066 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 63. Purpose: deliveries only: two parts "
        "from one shelf. Aspects: deliveries: two from shelf_0 to kitting_table_0; start: west wall; robot: "
        "east, apart. Expectation: the delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -100),
            scheduled_tasks=Script([
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_38", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_38", table="kitting_table_0"),
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

scenario_s27_04 = ScenarioConfig(
    id="scenario_s27_04",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 63),)),
    description=(
        "scenario_s27_04: script 066 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 63. Purpose: deliveries only: two parts "
        "from one shelf. Aspects: deliveries: two from shelf_0 to kitting_table_0; start: west wall; robot: "
        "east, apart. Expectation: the delivery under break_time admitted later than with no fact, near off. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it; under the window the delivery's admission and the "
        "robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -100),
            scheduled_tasks=Script([
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_38", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_38", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, 200),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_35", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 067: deliveries only: three to the east table
scenario_s27_05 = ScenarioConfig(
    id="scenario_s27_05",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_05: script 067 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: three to the east table. Aspects: deliveries: three to kitting_table_1; "
        "start: south-east corner; robot: west, apart. Expectation: on against off: each delivery admitted "
        "earlier or equal (the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -450),
            scheduled_tasks=Script([
                deliver_item("item_35", table="kitting_table_1"),
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_37", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_35", table="kitting_table_1"),
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_37", table="kitting_table_1"),
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

scenario_s27_06 = ScenarioConfig(
    id="scenario_s27_06",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_06: script 067 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: three to the east table. Aspects: deliveries: three to kitting_table_1; "
        "start: south-east corner; robot: west, apart. Expectation: on against off: each delivery admitted "
        "earlier or equal (the assigned tasks share most of the prior). working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -450),
            scheduled_tasks=Script([
                deliver_item("item_35", table="kitting_table_1"),
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_37", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_35", table="kitting_table_1"),
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_37", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 0),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s27_07 = ScenarioConfig(
    id="scenario_s27_07",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 40),)),
    description=(
        "scenario_s27_07: script 067 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 40. Purpose: deliveries only: three to "
        "the east table. Aspects: deliveries: three to kitting_table_1; start: south-east corner; robot: "
        "west, apart. Expectation: the delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -450),
            scheduled_tasks=Script([
                deliver_item("item_35", table="kitting_table_1"),
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_37", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_35", table="kitting_table_1"),
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_37", table="kitting_table_1"),
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

scenario_s27_08 = ScenarioConfig(
    id="scenario_s27_08",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 40),)),
    description=(
        "scenario_s27_08: script 067 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 40. Purpose: deliveries only: three to "
        "the east table. Aspects: deliveries: three to kitting_table_1; start: south-east corner; robot: "
        "west, apart. Expectation: the delivery under break_time admitted later than with no fact, near off. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it; under the window the delivery's admission and the "
        "robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, -450),
            scheduled_tasks=Script([
                deliver_item("item_35", table="kitting_table_1"),
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_37", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_35", table="kitting_table_1"),
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_37", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 0),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 068: deliveries only: the walk from kitting_table_0 to shelf_3 heads toward the coffee machine
scenario_s27_09 = ScenarioConfig(
    id="scenario_s27_09",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_09: script 068 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: the walk from kitting_table_0 to shelf_3 heads toward the coffee machine. "
        "Aspects: deliveries: three, both tables; approach toward the machine; robot: south start, crossing. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, -450),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_36", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_36", table="kitting_table_0"),
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

scenario_s27_10 = ScenarioConfig(
    id="scenario_s27_10",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_10: script 068 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: the walk from kitting_table_0 to shelf_3 heads toward the coffee machine. "
        "Aspects: deliveries: three, both tables; approach toward the machine; robot: south start, crossing. "
        "Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks share most "
        "of the prior). working robot: the decisions as off where no admission moves; an earlier admission "
        "of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, -450),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_36", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -450),
            assigned_tasks=[
                deliver_item("item_37", table="kitting_table_1"),
                deliver_item("item_31", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s27_11 = ScenarioConfig(
    id="scenario_s27_11",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 50),)),
    description=(
        "scenario_s27_11: script 068 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 50. Purpose: deliveries only: the walk "
        "from kitting_table_0 to shelf_3 heads toward the coffee machine. Aspects: deliveries: three, both "
        "tables; approach toward the machine; robot: south start, crossing. Expectation: the delivery under "
        "break_time admitted later than with no fact, near off; a delivery whose walk heads toward the "
        "machine may lose its admission to the raised coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, -450),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_36", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_36", table="kitting_table_0"),
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

scenario_s27_12 = ScenarioConfig(
    id="scenario_s27_12",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 50),)),
    description=(
        "scenario_s27_12: script 068 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 50. Purpose: deliveries only: the walk "
        "from kitting_table_0 to shelf_3 heads toward the coffee machine. Aspects: deliveries: three, both "
        "tables; approach toward the machine; robot: south start, crossing. Expectation: the delivery under "
        "break_time admitted later than with no fact, near off; a delivery whose walk heads toward the "
        "machine may lose its admission to the raised coffee break. working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it; under the window the delivery's admission and the robot's decision on it later than with "
        "no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, -450),
            scheduled_tasks=Script([
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_36", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_32", table="kitting_table_0"),
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -450),
            assigned_tasks=[
                deliver_item("item_37", table="kitting_table_1"),
                deliver_item("item_31", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 069: a coffee break between deliveries
scenario_s27_13 = ScenarioConfig(
    id="scenario_s27_13",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_13: script 069 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break between deliveries. Aspects: foreseeable: between deliveries; start: "
        "north-west. Expectation: on against off: each delivery admitted earlier or equal (the assigned "
        "tasks share most of the prior); a coffee break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 250),
            scheduled_tasks=Script([
                deliver_item("item_30", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_39", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_39", table="kitting_table_1"),
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

scenario_s27_14 = ScenarioConfig(
    id="scenario_s27_14",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_14: script 069 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break between deliveries. Aspects: foreseeable: between deliveries; start: "
        "north-west. Expectation: on against off: each delivery admitted earlier or equal (the assigned "
        "tasks share most of the prior); a coffee break admitted later than off (ordinary strength). working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 250),
            scheduled_tasks=Script([
                deliver_item("item_30", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_39", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_39", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -300),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_37", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s27_15 = ScenarioConfig(
    id="scenario_s27_15",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 44, 124),)),
    description=(
        "scenario_s27_15: script 069 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 44 to 124. Purpose: a coffee break between deliveries. "
        "Aspects: foreseeable: between deliveries; start: north-west. Expectation: the coffee break (raised "
        "by break_time) admitted earlier than off and than on with no fact; a delivery inside a window "
        "admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 250),
            scheduled_tasks=Script([
                deliver_item("item_30", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_39", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_39", table="kitting_table_1"),
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

scenario_s27_16 = ScenarioConfig(
    id="scenario_s27_16",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 44, 124),)),
    description=(
        "scenario_s27_16: script 069 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 44 to 124. Purpose: a coffee break between "
        "deliveries. Aspects: foreseeable: between deliveries; start: north-west. Expectation: the coffee "
        "break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside "
        "a window admitted later than with no fact. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it; the "
        "coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 250),
            scheduled_tasks=Script([
                deliver_item("item_30", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_39", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_39", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -300),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_37", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s27_17 = ScenarioConfig(
    id="scenario_s27_17",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 44),)),
    description=(
        "scenario_s27_17: script 069 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 44. Purpose: a coffee break between "
        "deliveries. Aspects: foreseeable: between deliveries; start: north-west. Expectation: the delivery "
        "under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 250),
            scheduled_tasks=Script([
                deliver_item("item_30", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_39", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_39", table="kitting_table_1"),
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

scenario_s27_18 = ScenarioConfig(
    id="scenario_s27_18",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 44),)),
    description=(
        "scenario_s27_18: script 069 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 44. Purpose: a coffee break between "
        "deliveries. Aspects: foreseeable: between deliveries; start: north-west. Expectation: the delivery "
        "under break_time admitted later than with no fact, near off. working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it; under the window the delivery's admission and the robot's decision on it later than with "
        "no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-950, 250),
            scheduled_tasks=Script([
                deliver_item("item_30", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_39", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_39", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -300),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_37", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 070: a coffee break inside a delivery, at shelf_3 before the grasp
scenario_s27_19 = ScenarioConfig(
    id="scenario_s27_19",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_19: script 070 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery, at shelf_3 before the grasp. Aspects: foreseeable: "
        "inside a delivery, before the grasp. Expectation: on against off: each delivery admitted earlier or "
        "equal (the assigned tasks share most of the prior); a coffee break admitted later than off "
        "(ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 0),
            scheduled_tasks=Script([
                deliver_item("item_33", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_32", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_32", table="kitting_table_0"),
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

scenario_s27_20 = ScenarioConfig(
    id="scenario_s27_20",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_20: script 070 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery, at shelf_3 before the grasp. Aspects: foreseeable: "
        "inside a delivery, before the grasp. Expectation: on against off: each delivery admitted earlier or "
        "equal (the assigned tasks share most of the prior); a coffee break admitted later than off "
        "(ordinary strength). working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 0),
            scheduled_tasks=Script([
                deliver_item("item_33", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_32", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_32", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, -200),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s27_21 = ScenarioConfig(
    id="scenario_s27_21",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 38, 116),)),
    description=(
        "scenario_s27_21: script 070 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 38 to 116. Purpose: a coffee break inside a delivery, at "
        "shelf_3 before the grasp. Aspects: foreseeable: inside a delivery, before the grasp. Expectation: "
        "the coffee break (raised by break_time) admitted earlier than off and than on with no fact; a "
        "delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 0),
            scheduled_tasks=Script([
                deliver_item("item_33", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_32", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_32", table="kitting_table_0"),
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

scenario_s27_22 = ScenarioConfig(
    id="scenario_s27_22",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 38, 116),)),
    description=(
        "scenario_s27_22: script 070 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 38 to 116. Purpose: a coffee break inside a "
        "delivery, at shelf_3 before the grasp. Aspects: foreseeable: inside a delivery, before the grasp. "
        "Expectation: the coffee break (raised by break_time) admitted earlier than off and than on with no "
        "fact; a delivery inside a window admitted later than with no fact. working robot: the decisions as "
        "off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 0),
            scheduled_tasks=Script([
                deliver_item("item_33", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_32", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_32", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, -200),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s27_23 = ScenarioConfig(
    id="scenario_s27_23",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 192, 296),)),
    description=(
        "scenario_s27_23: script 070 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 192 to 296. Purpose: a coffee break inside a "
        "delivery, at shelf_3 before the grasp. Aspects: foreseeable: inside a delivery, before the grasp. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 0),
            scheduled_tasks=Script([
                deliver_item("item_33", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_32", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_32", table="kitting_table_0"),
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

scenario_s27_24 = ScenarioConfig(
    id="scenario_s27_24",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 192, 296),)),
    description=(
        "scenario_s27_24: script 070 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 192 to 296. Purpose: a coffee break inside a "
        "delivery, at shelf_3 before the grasp. Aspects: foreseeable: inside a delivery, before the grasp. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; under the window the delivery's admission and the robot's "
        "decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 0),
            scheduled_tasks=Script([
                deliver_item("item_33", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_32", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_32", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, -200),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 071: unmodelled alone: a long stand, 60 ticks, at kitting_table_1
scenario_s27_25 = ScenarioConfig(
    id="scenario_s27_25",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_25: script 071 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a long stand, 60 ticks, at kitting_table_1. Aspects: unmodelled: a stand "
        "(60 ticks), between deliveries. Expectation: on against off: each delivery admitted earlier or "
        "equal (the assigned tasks share most of the prior); no admission during the stand or the walk "
        "elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, -200),
            scheduled_tasks=Script([
                deliver_item("item_34", table="kitting_table_1"),
                stand("PT120S"),
                deliver_item("item_35", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_35", table="kitting_table_1"),
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

scenario_s27_26 = ScenarioConfig(
    id="scenario_s27_26",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_26: script 071 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a long stand, 60 ticks, at kitting_table_1. Aspects: unmodelled: a stand "
        "(60 ticks), between deliveries. Expectation: on against off: each delivery admitted earlier or "
        "equal (the assigned tasks share most of the prior); no admission during the stand or the walk "
        "elsewhere, except a hypothesis whose target lies on the walk. working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, -200),
            scheduled_tasks=Script([
                deliver_item("item_34", table="kitting_table_1"),
                stand("PT120S"),
                deliver_item("item_35", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_35", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 100),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s27_27 = ScenarioConfig(
    id="scenario_s27_27",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 44),)),
    description=(
        "scenario_s27_27: script 071 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 44. Purpose: unmodelled alone: a long "
        "stand, 60 ticks, at kitting_table_1. Aspects: unmodelled: a stand (60 ticks), between deliveries. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off; no admission "
        "during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(500, -200),
            scheduled_tasks=Script([
                deliver_item("item_34", table="kitting_table_1"),
                stand("PT120S"),
                deliver_item("item_35", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_35", table="kitting_table_1"),
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

scenario_s27_28 = ScenarioConfig(
    id="scenario_s27_28",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 44),)),
    description=(
        "scenario_s27_28: script 071 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 44. Purpose: unmodelled alone: a long "
        "stand, 60 ticks, at kitting_table_1. Aspects: unmodelled: a stand (60 ticks), between deliveries. "
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
            start_position=(500, -200),
            scheduled_tasks=Script([
                deliver_item("item_34", table="kitting_table_1"),
                stand("PT120S"),
                deliver_item("item_35", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_35", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 100),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_36", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 072: unmodelled with a foreseeable task: a walk to corner_SE, then a coffee break
scenario_s27_29 = ScenarioConfig(
    id="scenario_s27_29",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_29: script 072 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a walk to corner_SE, then a coffee break. Aspects: "
        "unmodelled: a walk elsewhere (no stand); foreseeable: right after it; robot: two parts from "
        "shelf_3. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); a coffee break admitted later than off (ordinary strength); no admission "
        "during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, 0),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                go_to("corner_SE"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
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

scenario_s27_30 = ScenarioConfig(
    id="scenario_s27_30",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_30: script 072 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a walk to corner_SE, then a coffee break. Aspects: "
        "unmodelled: a walk elsewhere (no stand); foreseeable: right after it; robot: two parts from "
        "shelf_3. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); a coffee break admitted later than off (ordinary strength); no admission "
        "during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, 0),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                go_to("corner_SE"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, 300),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_39", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s27_31 = ScenarioConfig(
    id="scenario_s27_31",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 129, 225),)),
    description=(
        "scenario_s27_31: script 072 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 129 to 225. Purpose: unmodelled with a foreseeable task: "
        "a walk to corner_SE, then a coffee break. Aspects: unmodelled: a walk elsewhere (no stand); "
        "foreseeable: right after it; robot: two parts from shelf_3. Expectation: the coffee break (raised "
        "by break_time) admitted earlier than off and than on with no fact; a delivery inside a window "
        "admitted later than with no fact; no admission during the stand or the walk elsewhere, except a "
        "hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, 0),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                go_to("corner_SE"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
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

scenario_s27_32 = ScenarioConfig(
    id="scenario_s27_32",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 129, 225),)),
    description=(
        "scenario_s27_32: script 072 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 129 to 225. Purpose: unmodelled with a foreseeable "
        "task: a walk to corner_SE, then a coffee break. Aspects: unmodelled: a walk elsewhere (no stand); "
        "foreseeable: right after it; robot: two parts from shelf_3. Expectation: the coffee break (raised "
        "by break_time) admitted earlier than off and than on with no fact; a delivery inside a window "
        "admitted later than with no fact; no admission during the stand or the walk elsewhere, except a "
        "hypothesis whose target lies on the walk. working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it; the "
        "coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, 0),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                go_to("corner_SE"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, 300),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_39", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s27_33 = ScenarioConfig(
    id="scenario_s27_33",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 45),)),
    description=(
        "scenario_s27_33: script 072 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 45. Purpose: unmodelled with a "
        "foreseeable task: a walk to corner_SE, then a coffee break. Aspects: unmodelled: a walk elsewhere "
        "(no stand); foreseeable: right after it; robot: two parts from shelf_3. Expectation: the delivery "
        "under break_time admitted later than with no fact, near off; no admission during the stand or the "
        "walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-700, 0),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                go_to("corner_SE"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
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

scenario_s27_34 = ScenarioConfig(
    id="scenario_s27_34",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 45),)),
    description=(
        "scenario_s27_34: script 072 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 45. Purpose: unmodelled with a "
        "foreseeable task: a walk to corner_SE, then a coffee break. Aspects: unmodelled: a walk elsewhere "
        "(no stand); foreseeable: right after it; robot: two parts from shelf_3. Expectation: the delivery "
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
            start_position=(-700, 0),
            scheduled_tasks=Script([
                deliver_item("item_31", table="kitting_table_0"),
                go_to("corner_SE"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_31", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, 300),
            assigned_tasks=[
                deliver_item("item_33", table="kitting_table_1"),
                deliver_item("item_39", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 073: unmodelled with a foreseeable task: a delivery to the other table (item_37 to kitting_table_0), a coffee break at the end
scenario_s27_35 = ScenarioConfig(
    id="scenario_s27_35",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_35: script 073 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery to the other table (item_37 to "
        "kitting_table_0), a coffee break at the end. Aspects: unmodelled: a delivery to the other table; "
        "foreseeable: at the end; robot: two parts from shelf_0 to kitting_table_0, where the human "
        "delivers. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); a coffee break admitted later than off (ordinary strength); the delivery "
        "to the other table: admitted on the walk to the shelf, then its carry unexplained; no other "
        "hypothesis admitted there."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, -300),
            scheduled_tasks=Script([
                deliver_item("item_37", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_37", table="kitting_table_1"),
                deliver_item("item_32", table="kitting_table_0"),
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

scenario_s27_36 = ScenarioConfig(
    id="scenario_s27_36",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_36: script 073 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled with a foreseeable task: a delivery to the other table (item_37 to "
        "kitting_table_0), a coffee break at the end. Aspects: unmodelled: a delivery to the other table; "
        "foreseeable: at the end; robot: two parts from shelf_0 to kitting_table_0, where the human "
        "delivers. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); a coffee break admitted later than off (ordinary strength); the delivery "
        "to the other table: admitted on the walk to the shelf, then its carry unexplained; no other "
        "hypothesis admitted there. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, -300),
            scheduled_tasks=Script([
                deliver_item("item_37", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_37", table="kitting_table_1"),
                deliver_item("item_32", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 300),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_38", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s27_37 = ScenarioConfig(
    id="scenario_s27_37",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 103, 184),)),
    description=(
        "scenario_s27_37: script 073 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 103 to 184. Purpose: unmodelled with a foreseeable task: "
        "a delivery to the other table (item_37 to kitting_table_0), a coffee break at the end. Aspects: "
        "unmodelled: a delivery to the other table; foreseeable: at the end; robot: two parts from shelf_0 "
        "to kitting_table_0, where the human delivers. Expectation: the coffee break (raised by break_time) "
        "admitted earlier than off and than on with no fact; a delivery inside a window admitted later than "
        "with no fact; the delivery to the other table: admitted on the walk to the shelf, then its carry "
        "unexplained; no other hypothesis admitted there."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, -300),
            scheduled_tasks=Script([
                deliver_item("item_37", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_37", table="kitting_table_1"),
                deliver_item("item_32", table="kitting_table_0"),
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

scenario_s27_38 = ScenarioConfig(
    id="scenario_s27_38",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 103, 184),)),
    description=(
        "scenario_s27_38: script 073 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 103 to 184. Purpose: unmodelled with a foreseeable "
        "task: a delivery to the other table (item_37 to kitting_table_0), a coffee break at the end. "
        "Aspects: unmodelled: a delivery to the other table; foreseeable: at the end; robot: two parts from "
        "shelf_0 to kitting_table_0, where the human delivers. Expectation: the coffee break (raised by "
        "break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted "
        "later than with no fact; the delivery to the other table: admitted on the walk to the shelf, then "
        "its carry unexplained; no other hypothesis admitted there. working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, -300),
            scheduled_tasks=Script([
                deliver_item("item_37", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_37", table="kitting_table_1"),
                deliver_item("item_32", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 300),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_38", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s27_39 = ScenarioConfig(
    id="scenario_s27_39",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 63, 103),)),
    description=(
        "scenario_s27_39: script 073 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 63 to 103. Purpose: unmodelled with a "
        "foreseeable task: a delivery to the other table (item_37 to kitting_table_0), a coffee break at the "
        "end. Aspects: unmodelled: a delivery to the other table; foreseeable: at the end; robot: two parts "
        "from shelf_0 to kitting_table_0, where the human delivers. Expectation: the delivery under "
        "break_time admitted later than with no fact, near off; the delivery to the other table: admitted on "
        "the walk to the shelf, then its carry unexplained; no other hypothesis admitted there."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, -300),
            scheduled_tasks=Script([
                deliver_item("item_37", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_37", table="kitting_table_1"),
                deliver_item("item_32", table="kitting_table_0"),
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

scenario_s27_40 = ScenarioConfig(
    id="scenario_s27_40",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 63, 103),)),
    description=(
        "scenario_s27_40: script 073 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 63 to 103. Purpose: unmodelled with a "
        "foreseeable task: a delivery to the other table (item_37 to kitting_table_0), a coffee break at the "
        "end. Aspects: unmodelled: a delivery to the other table; foreseeable: at the end; robot: two parts "
        "from shelf_0 to kitting_table_0, where the human delivers. Expectation: the delivery under "
        "break_time admitted later than with no fact, near off; the delivery to the other table: admitted on "
        "the walk to the shelf, then its carry unexplained; no other hypothesis admitted there. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; under the window the delivery's admission and the robot's "
        "decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, -300),
            scheduled_tasks=Script([
                deliver_item("item_37", table="kitting_table_0"),
                deliver_item("item_32", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_37", table="kitting_table_1"),
                deliver_item("item_32", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-900, 300),
            assigned_tasks=[
                deliver_item("item_30", table="kitting_table_0"),
                deliver_item("item_38", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 074: unmodelled alone: a delivery abandoned after the grasp, the part carried away to the corner; the second delivery never started
scenario_s27_41 = ScenarioConfig(
    id="scenario_s27_41",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_41: script 074 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a delivery abandoned after the grasp, the part carried away to the "
        "corner; the second delivery never started. Aspects: unmodelled: an abandoned delivery, a walk "
        "elsewhere, a never-started delivery; no foreseeable task. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); the never-started "
        "delivery never admitted (no observation warrant); the abandoned delivery admitted while the human "
        "walks to it, then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -200),
            scheduled_tasks=Script([
                deliver_item("item_36", table="kitting_table_0").at(pick_up, drop),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_36", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_1"),
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

scenario_s27_42 = ScenarioConfig(
    id="scenario_s27_42",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_42: script 074 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a delivery abandoned after the grasp, the part carried away to the "
        "corner; the second delivery never started. Aspects: unmodelled: an abandoned delivery, a walk "
        "elsewhere, a never-started delivery; no foreseeable task. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); the never-started "
        "delivery never admitted (no observation warrant); the abandoned delivery admitted while the human "
        "walks to it, then retracted as the evidence turns. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -200),
            scheduled_tasks=Script([
                deliver_item("item_36", table="kitting_table_0").at(pick_up, drop),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_36", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(800, 100),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_37", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 075: a coffee break inside a delivery after the grasp, and a second soon after at the end
scenario_s27_43 = ScenarioConfig(
    id="scenario_s27_43",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_43: script 075 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery after the grasp, and a second soon after at the end. "
        "Aspects: foreseeable: two coffee breaks, inside a delivery and at the end. Expectation: on against "
        "off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee "
        "break admitted later than off (ordinary strength); the second under its recency fact (suppressed), "
        "later still."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, 150),
            scheduled_tasks=Script([
                deliver_item("item_35", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_33", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_35", table="kitting_table_1"),
                deliver_item("item_33", table="kitting_table_1"),
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

scenario_s27_44 = ScenarioConfig(
    id="scenario_s27_44",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s27_44: script 075 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery after the grasp, and a second soon after at the end. "
        "Aspects: foreseeable: two coffee breaks, inside a delivery and at the end. Expectation: on against "
        "off: each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee "
        "break admitted later than off (ordinary strength); the second under its recency fact (suppressed), "
        "later still. working robot: the decisions as off where no admission moves; an earlier admission of "
        "a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, 150),
            scheduled_tasks=Script([
                deliver_item("item_35", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_33", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_35", table="kitting_table_1"),
                deliver_item("item_33", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -400),
            assigned_tasks=[
                deliver_item("item_36", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s27_45 = ScenarioConfig(
    id="scenario_s27_45",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 10, 93), window(BREAK_TIME, 192, 266),)),
    description=(
        "scenario_s27_45: script 075 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 10 to 93, break_time from 192 to 266. Purpose: a coffee "
        "break inside a delivery after the grasp, and a second soon after at the end. Aspects: foreseeable: "
        "two coffee breaks, inside a delivery and at the end. Expectation: the coffee break (raised by "
        "break_time) admitted earlier than off and than on with no fact; the second one suppressed by its "
        "recency fact, the window gives it nothing; a delivery inside a window admitted later than with no "
        "fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, 150),
            scheduled_tasks=Script([
                deliver_item("item_35", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_33", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_35", table="kitting_table_1"),
                deliver_item("item_33", table="kitting_table_1"),
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

scenario_s27_46 = ScenarioConfig(
    id="scenario_s27_46",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 10, 93), window(BREAK_TIME, 192, 266),)),
    description=(
        "scenario_s27_46: script 075 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 10 to 93, break_time from 192 to 266. Purpose: a "
        "coffee break inside a delivery after the grasp, and a second soon after at the end. Aspects: "
        "foreseeable: two coffee breaks, inside a delivery and at the end. Expectation: the coffee break "
        "(raised by break_time) admitted earlier than off and than on with no fact; the second one "
        "suppressed by its recency fact, the window gives it nothing; a delivery inside a window admitted "
        "later than with no fact. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; the coffee break admitted "
        "earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, 150),
            scheduled_tasks=Script([
                deliver_item("item_35", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_33", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_35", table="kitting_table_1"),
                deliver_item("item_33", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -400),
            assigned_tasks=[
                deliver_item("item_36", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s27_47 = ScenarioConfig(
    id="scenario_s27_47",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 137, 192),)),
    description=(
        "scenario_s27_47: script 075 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 137 to 192. Purpose: a coffee break inside a "
        "delivery after the grasp, and a second soon after at the end. Aspects: foreseeable: two coffee "
        "breaks, inside a delivery and at the end. Expectation: the delivery under break_time admitted later "
        "than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, 150),
            scheduled_tasks=Script([
                deliver_item("item_35", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_33", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_35", table="kitting_table_1"),
                deliver_item("item_33", table="kitting_table_1"),
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

scenario_s27_48 = ScenarioConfig(
    id="scenario_s27_48",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 137, 192),)),
    description=(
        "scenario_s27_48: script 075 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 137 to 192. Purpose: a coffee break inside a "
        "delivery after the grasp, and a second soon after at the end. Aspects: foreseeable: two coffee "
        "breaks, inside a delivery and at the end. Expectation: the delivery under break_time admitted later "
        "than with no fact, near off. working robot: the decisions as off where no admission moves; an "
        "earlier admission of a delivery moves the response decision earlier or leaves it; under the window "
        "the delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(900, 150),
            scheduled_tasks=Script([
                deliver_item("item_35", table="kitting_table_1").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_33", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_35", table="kitting_table_1"),
                deliver_item("item_33", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, -400),
            assigned_tasks=[
                deliver_item("item_36", table="kitting_table_0"),
                deliver_item("item_31", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)


# T-F part 1, part 1b (5 October 2026): copies with a fact in force (analysis/kitting/tf1/make_copies.py; REPORT.md, "Part 1").
scenario_s27_49 = ScenarioConfig(
    id="scenario_s27_49",
    setup="env_setup_27",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 18),)),
    description=(
        "T-F part 1, part 1b: scenario_s27_42's copy with a fact in force, not in accord: break_time over ticks 0 to 18 (deliver_item(item_36,kitting_table_0)). "
        "Everything else is scenario_s27_42's (analysis/kitting/tf1/make_copies.py)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, -200),
            scheduled_tasks=Script([
                deliver_item("item_36", table="kitting_table_0").at(pick_up, drop),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_36", table="kitting_table_0"),
                deliver_item("item_35", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(800, 100),
            assigned_tasks=[
                deliver_item("item_34", table="kitting_table_1"),
                deliver_item("item_37", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

