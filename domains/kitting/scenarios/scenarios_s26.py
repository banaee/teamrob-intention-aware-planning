# domains/kitting/scenarios/scenarios_s26.py
"""
Kitting scenarios on env_setup_26: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_19; the shift
env_setup_26: the cross shift: every part goes to the far table (the west and south-west shelves to kitting_table_1, the east and south-east shelves to kitting_table_0), so the carries cross the room's middle in front of the coffee machine.
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

# ---- script 056: deliveries only: one long carry across the room, past the front of the coffee machine
scenario_s26_01 = ScenarioConfig(
    id="scenario_s26_01",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_01: script 056 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: one long carry across the room, past the front of the coffee machine. "
        "Aspects: deliveries: one, across; robot: south-centre start, two carries the other way, crossing in "
        "the middle. Expectation: on against off: each delivery admitted earlier or equal (the assigned "
        "tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 200),
            scheduled_tasks=Script([
                deliver_item("item_20", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_20", table="kitting_table_1"),
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

scenario_s26_02 = ScenarioConfig(
    id="scenario_s26_02",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_02: script 056 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: one long carry across the room, past the front of the coffee machine. "
        "Aspects: deliveries: one, across; robot: south-centre start, two carries the other way, crossing in "
        "the middle. Expectation: on against off: each delivery admitted earlier or equal (the assigned "
        "tasks share most of the prior). working robot: the decisions as off where no admission moves; an "
        "earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 200),
            scheduled_tasks=Script([
                deliver_item("item_20", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_20", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, -300),
            assigned_tasks=[
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_27", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_03 = ScenarioConfig(
    id="scenario_s26_03",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 114),)),
    description=(
        "scenario_s26_03: script 056 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 114. Purpose: deliveries only: one long "
        "carry across the room, past the front of the coffee machine. Aspects: deliveries: one, across; "
        "robot: south-centre start, two carries the other way, crossing in the middle. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 200),
            scheduled_tasks=Script([
                deliver_item("item_20", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_20", table="kitting_table_1"),
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

scenario_s26_04 = ScenarioConfig(
    id="scenario_s26_04",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 114),)),
    description=(
        "scenario_s26_04: script 056 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 114. Purpose: deliveries only: one long "
        "carry across the room, past the front of the coffee machine. Aspects: deliveries: one, across; "
        "robot: south-centre start, two carries the other way, crossing in the middle. Expectation: the "
        "delivery under break_time admitted later than with no fact, near off. working robot: the decisions "
        "as off where no admission moves; an earlier admission of a delivery moves the response decision "
        "earlier or leaves it; under the window the delivery's admission and the robot's decision on it "
        "later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-500, 200),
            scheduled_tasks=Script([
                deliver_item("item_20", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_20", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, -300),
            assigned_tasks=[
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_27", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 057: deliveries only: four, alternating tables
scenario_s26_05 = ScenarioConfig(
    id="scenario_s26_05",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_05: script 057 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: deliveries only: four, alternating tables. Aspects: deliveries: four, alternating tables; "
        "robot: centre start, crossing. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -200),
            scheduled_tasks=Script([
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_22", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_22", table="kitting_table_1"),
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

scenario_s26_06 = ScenarioConfig(
    id="scenario_s26_06",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_06: script 057 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: deliveries only: four, alternating tables. Aspects: deliveries: four, alternating tables; "
        "robot: centre start, crossing. Expectation: on against off: each delivery admitted earlier or equal "
        "(the assigned tasks share most of the prior). working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -200),
            scheduled_tasks=Script([
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_22", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_22", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_26", table="kitting_table_1"),
                deliver_item("item_27", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_07 = ScenarioConfig(
    id="scenario_s26_07",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 136),)),
    description=(
        "scenario_s26_07: script 057 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 136. Purpose: deliveries only: four, "
        "alternating tables. Aspects: deliveries: four, alternating tables; robot: centre start, crossing. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -200),
            scheduled_tasks=Script([
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_22", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_22", table="kitting_table_1"),
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

scenario_s26_08 = ScenarioConfig(
    id="scenario_s26_08",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 136),)),
    description=(
        "scenario_s26_08: script 057 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 136. Purpose: deliveries only: four, "
        "alternating tables. Aspects: deliveries: four, alternating tables; robot: centre start, crossing. "
        "Expectation: the delivery under break_time admitted later than with no fact, near off. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; under the window the delivery's admission and the robot's "
        "decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -200),
            scheduled_tasks=Script([
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_22", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_22", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_26", table="kitting_table_1"),
                deliver_item("item_27", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 058: a coffee break between deliveries, after the second
scenario_s26_09 = ScenarioConfig(
    id="scenario_s26_09",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_09: script 058 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break between deliveries, after the second. Aspects: foreseeable: between, after "
        "two deliveries; start: south-east corner, first walk north. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, -400),
            scheduled_tasks=Script([
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_23", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
                deliver_item("item_23", table="kitting_table_0"),
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

scenario_s26_10 = ScenarioConfig(
    id="scenario_s26_10",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_10: script 058 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break between deliveries, after the second. Aspects: foreseeable: between, after "
        "two deliveries; start: south-east corner, first walk north. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength). working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, -400),
            scheduled_tasks=Script([
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_23", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
                deliver_item("item_23", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, -300),
            assigned_tasks=[
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_20", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_11 = ScenarioConfig(
    id="scenario_s26_11",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 190, 264),)),
    description=(
        "scenario_s26_11: script 058 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 190 to 264. Purpose: a coffee break between deliveries, "
        "after the second. Aspects: foreseeable: between, after two deliveries; start: south-east corner, "
        "first walk north. Expectation: the coffee break (raised by break_time) admitted earlier than off "
        "and than on with no fact; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, -400),
            scheduled_tasks=Script([
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_23", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
                deliver_item("item_23", table="kitting_table_0"),
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

scenario_s26_12 = ScenarioConfig(
    id="scenario_s26_12",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 190, 264),)),
    description=(
        "scenario_s26_12: script 058 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 190 to 264. Purpose: a coffee break between "
        "deliveries, after the second. Aspects: foreseeable: between, after two deliveries; start: "
        "south-east corner, first walk north. Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; a delivery inside a window admitted later than with no "
        "fact. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; the coffee break admitted earlier, the "
        "robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, -400),
            scheduled_tasks=Script([
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_23", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
                deliver_item("item_23", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, -300),
            assigned_tasks=[
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_20", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_13 = ScenarioConfig(
    id="scenario_s26_13",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 108),)),
    description=(
        "scenario_s26_13: script 058 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 108. Purpose: a coffee break between "
        "deliveries, after the second. Aspects: foreseeable: between, after two deliveries; start: "
        "south-east corner, first walk north. Expectation: the delivery under break_time admitted later than "
        "with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, -400),
            scheduled_tasks=Script([
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_23", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
                deliver_item("item_23", table="kitting_table_0"),
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

scenario_s26_14 = ScenarioConfig(
    id="scenario_s26_14",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 108),)),
    description=(
        "scenario_s26_14: script 058 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 108. Purpose: a coffee break between "
        "deliveries, after the second. Aspects: foreseeable: between, after two deliveries; start: "
        "south-east corner, first walk north. Expectation: the delivery under break_time admitted later than "
        "with no fact, near off. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; under the window the "
        "delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(800, -400),
            scheduled_tasks=Script([
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_23", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
                deliver_item("item_23", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, -300),
            assigned_tasks=[
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_20", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 059: a coffee break inside a delivery at the table, before the release (the part still in hand)
scenario_s26_15 = ScenarioConfig(
    id="scenario_s26_15",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_15: script 059 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery at the table, before the release (the part still in "
        "hand). Aspects: foreseeable: inside a delivery, before the release; robot: north-east start, "
        "crossing. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); a coffee break admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -200),
            scheduled_tasks=Script([
                deliver_item("item_22", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=1),
                deliver_item("item_27", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_22", table="kitting_table_1"),
                deliver_item("item_27", table="kitting_table_0"),
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

scenario_s26_16 = ScenarioConfig(
    id="scenario_s26_16",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_16: script 059 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break inside a delivery at the table, before the release (the part still in "
        "hand). Aspects: foreseeable: inside a delivery, before the release; robot: north-east start, "
        "crossing. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); a coffee break admitted later than off (ordinary strength). working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -200),
            scheduled_tasks=Script([
                deliver_item("item_22", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=1),
                deliver_item("item_27", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_22", table="kitting_table_1"),
                deliver_item("item_27", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, 300),
            assigned_tasks=[
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_25", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_17 = ScenarioConfig(
    id="scenario_s26_17",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 94, 167),)),
    description=(
        "scenario_s26_17: script 059 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 94 to 167. Purpose: a coffee break inside a delivery at "
        "the table, before the release (the part still in hand). Aspects: foreseeable: inside a delivery, "
        "before the release; robot: north-east start, crossing. Expectation: the coffee break (raised by "
        "break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted "
        "later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -200),
            scheduled_tasks=Script([
                deliver_item("item_22", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=1),
                deliver_item("item_27", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_22", table="kitting_table_1"),
                deliver_item("item_27", table="kitting_table_0"),
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

scenario_s26_18 = ScenarioConfig(
    id="scenario_s26_18",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 94, 167),)),
    description=(
        "scenario_s26_18: script 059 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 94 to 167. Purpose: a coffee break inside a delivery "
        "at the table, before the release (the part still in hand). Aspects: foreseeable: inside a delivery, "
        "before the release; robot: north-east start, crossing. Expectation: the coffee break (raised by "
        "break_time) admitted earlier than off and than on with no fact; a delivery inside a window admitted "
        "later than with no fact. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; the coffee break admitted "
        "earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -200),
            scheduled_tasks=Script([
                deliver_item("item_22", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=1),
                deliver_item("item_27", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_22", table="kitting_table_1"),
                deliver_item("item_27", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, 300),
            assigned_tasks=[
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_25", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_19 = ScenarioConfig(
    id="scenario_s26_19",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 211, 295),)),
    description=(
        "scenario_s26_19: script 059 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 211 to 295. Purpose: a coffee break inside a "
        "delivery at the table, before the release (the part still in hand). Aspects: foreseeable: inside a "
        "delivery, before the release; robot: north-east start, crossing. Expectation: the delivery under "
        "break_time admitted later than with no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -200),
            scheduled_tasks=Script([
                deliver_item("item_22", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=1),
                deliver_item("item_27", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_22", table="kitting_table_1"),
                deliver_item("item_27", table="kitting_table_0"),
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

scenario_s26_20 = ScenarioConfig(
    id="scenario_s26_20",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 211, 295),)),
    description=(
        "scenario_s26_20: script 059 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 211 to 295. Purpose: a coffee break inside a "
        "delivery at the table, before the release (the part still in hand). Aspects: foreseeable: inside a "
        "delivery, before the release; robot: north-east start, crossing. Expectation: the delivery under "
        "break_time admitted later than with no fact, near off. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it; under the window the delivery's admission and the robot's decision on it later than with no "
        "fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-900, -200),
            scheduled_tasks=Script([
                deliver_item("item_22", table="kitting_table_1").at(move_to, coffee_break("coffee_machine_0"), occurrence=1),
                deliver_item("item_27", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_22", table="kitting_table_1"),
                deliver_item("item_27", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, 300),
            assigned_tasks=[
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_25", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 060: a coffee break at the start, the machine a short walk away
scenario_s26_21 = ScenarioConfig(
    id="scenario_s26_21",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_21: script 060 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the start, the machine a short walk away. Aspects: foreseeable: at the "
        "start; start: near the machine, a short first walk toward it. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 100),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_20", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_20", table="kitting_table_1"),
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

scenario_s26_22 = ScenarioConfig(
    id="scenario_s26_22",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_22: script 060 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break at the start, the machine a short walk away. Aspects: foreseeable: at the "
        "start; start: near the machine, a short first walk toward it. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength). working robot: the decisions as off where no admission "
        "moves; an earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 100),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_20", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_20", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, -450),
            assigned_tasks=[
                deliver_item("item_26", table="kitting_table_1"),
                deliver_item("item_21", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_23 = ScenarioConfig(
    id="scenario_s26_23",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 54),)),
    description=(
        "scenario_s26_23: script 060 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 0 to 54. Purpose: a coffee break at the start, the "
        "machine a short walk away. Aspects: foreseeable: at the start; start: near the machine, a short "
        "first walk toward it. Expectation: the coffee break (raised by break_time) admitted earlier than "
        "off and than on with no fact; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 100),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_20", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_20", table="kitting_table_1"),
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

scenario_s26_24 = ScenarioConfig(
    id="scenario_s26_24",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 54),)),
    description=(
        "scenario_s26_24: script 060 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 0 to 54. Purpose: a coffee break at the start, the "
        "machine a short walk away. Aspects: foreseeable: at the start; start: near the machine, a short "
        "first walk toward it. Expectation: the coffee break (raised by break_time) admitted earlier than "
        "off and than on with no fact; a delivery inside a window admitted later than with no fact. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; the coffee break admitted earlier, the robot's decision "
        "against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 100),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_20", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_20", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, -450),
            assigned_tasks=[
                deliver_item("item_26", table="kitting_table_1"),
                deliver_item("item_21", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_25 = ScenarioConfig(
    id="scenario_s26_25",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 54, 198),)),
    description=(
        "scenario_s26_25: script 060 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 54 to 198. Purpose: a coffee break at the "
        "start, the machine a short walk away. Aspects: foreseeable: at the start; start: near the machine, "
        "a short first walk toward it. Expectation: the delivery under break_time admitted later than with "
        "no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the "
        "raised coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 100),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_20", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_20", table="kitting_table_1"),
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

scenario_s26_26 = ScenarioConfig(
    id="scenario_s26_26",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 54, 198),)),
    description=(
        "scenario_s26_26: script 060 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 54 to 198. Purpose: a coffee break at the "
        "start, the machine a short walk away. Aspects: foreseeable: at the start; start: near the machine, "
        "a short first walk toward it. Expectation: the delivery under break_time admitted later than with "
        "no fact, near off; a delivery whose walk heads toward the machine may lose its admission to the "
        "raised coffee break. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; under the window the "
        "delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 100),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_20", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_24", table="kitting_table_0"),
                deliver_item("item_20", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-700, -450),
            assigned_tasks=[
                deliver_item("item_26", table="kitting_table_1"),
                deliver_item("item_21", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 061: unmodelled alone: a walk to corner_SE and a stand of 20 ticks between deliveries
scenario_s26_27 = ScenarioConfig(
    id="scenario_s26_27",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_27: script 061 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a walk to corner_SE and a stand of 20 ticks between deliveries. Aspects: "
        "unmodelled: a walk elsewhere with a stand (20 ticks); start: south floor, first walk away from the "
        "machine. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis "
        "whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -300),
            scheduled_tasks=Script([
                deliver_item("item_27", table="kitting_table_0"),
                go_to_and_stand("corner_SE", "PT40S"),
                deliver_item("item_25", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_27", table="kitting_table_0"),
                deliver_item("item_25", table="kitting_table_0"),
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

scenario_s26_28 = ScenarioConfig(
    id="scenario_s26_28",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_28: script 061 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a walk to corner_SE and a stand of 20 ticks between deliveries. Aspects: "
        "unmodelled: a walk elsewhere with a stand (20 ticks); start: south floor, first walk away from the "
        "machine. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); no admission during the stand or the walk elsewhere, except a hypothesis "
        "whose target lies on the walk. working robot: the decisions as off where no admission moves; an "
        "earlier admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -300),
            scheduled_tasks=Script([
                deliver_item("item_27", table="kitting_table_0"),
                go_to_and_stand("corner_SE", "PT40S"),
                deliver_item("item_25", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_27", table="kitting_table_0"),
                deliver_item("item_25", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, 300),
            assigned_tasks=[
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_22", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_29 = ScenarioConfig(
    id="scenario_s26_29",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 71),)),
    description=(
        "scenario_s26_29: script 061 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 71. Purpose: unmodelled alone: a walk "
        "to corner_SE and a stand of 20 ticks between deliveries. Aspects: unmodelled: a walk elsewhere with "
        "a stand (20 ticks); start: south floor, first walk away from the machine. Expectation: the delivery "
        "under break_time admitted later than with no fact, near off; no admission during the stand or the "
        "walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, -300),
            scheduled_tasks=Script([
                deliver_item("item_27", table="kitting_table_0"),
                go_to_and_stand("corner_SE", "PT40S"),
                deliver_item("item_25", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_27", table="kitting_table_0"),
                deliver_item("item_25", table="kitting_table_0"),
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

scenario_s26_30 = ScenarioConfig(
    id="scenario_s26_30",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 71),)),
    description=(
        "scenario_s26_30: script 061 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 71. Purpose: unmodelled alone: a walk "
        "to corner_SE and a stand of 20 ticks between deliveries. Aspects: unmodelled: a walk elsewhere with "
        "a stand (20 ticks); start: south floor, first walk away from the machine. Expectation: the delivery "
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
            start_position=(0, -300),
            scheduled_tasks=Script([
                deliver_item("item_27", table="kitting_table_0"),
                go_to_and_stand("corner_SE", "PT40S"),
                deliver_item("item_25", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_27", table="kitting_table_0"),
                deliver_item("item_25", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-600, 300),
            assigned_tasks=[
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_22", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 062: a coffee break after the one delivery; the second delivery never started
scenario_s26_31 = ScenarioConfig(
    id="scenario_s26_31",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_31: script 062 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a coffee break after the one delivery; the second delivery never started. Aspects: "
        "unmodelled: a never-started delivery; foreseeable: at the end. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength); the never-started delivery never admitted (no "
        "observation warrant)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, -450),
            scheduled_tasks=Script([
                deliver_item("item_21", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
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

scenario_s26_32 = ScenarioConfig(
    id="scenario_s26_32",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_32: script 062 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a coffee break after the one delivery; the second delivery never started. Aspects: "
        "unmodelled: a never-started delivery; foreseeable: at the end. Expectation: on against off: each "
        "delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee break "
        "admitted later than off (ordinary strength); the never-started delivery never admitted (no "
        "observation warrant). working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, -450),
            scheduled_tasks=Script([
                deliver_item("item_21", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, 300),
            assigned_tasks=[
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_25", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_33 = ScenarioConfig(
    id="scenario_s26_33",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 94, 167),)),
    description=(
        "scenario_s26_33: script 062 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 94 to 167. Purpose: a coffee break after the one "
        "delivery; the second delivery never started. Aspects: unmodelled: a never-started delivery; "
        "foreseeable: at the end. Expectation: the coffee break (raised by break_time) admitted earlier than "
        "off and than on with no fact; a delivery inside a window admitted later than with no fact; the "
        "never-started delivery never admitted (no observation warrant)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, -450),
            scheduled_tasks=Script([
                deliver_item("item_21", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
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

scenario_s26_34 = ScenarioConfig(
    id="scenario_s26_34",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 94, 167),)),
    description=(
        "scenario_s26_34: script 062 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 94 to 167. Purpose: a coffee break after the one "
        "delivery; the second delivery never started. Aspects: unmodelled: a never-started delivery; "
        "foreseeable: at the end. Expectation: the coffee break (raised by break_time) admitted earlier than "
        "off and than on with no fact; a delivery inside a window admitted later than with no fact; the "
        "never-started delivery never admitted (no observation warrant). working robot: the decisions as off "
        "where no admission moves; an earlier admission of a delivery moves the response decision earlier or "
        "leaves it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, -450),
            scheduled_tasks=Script([
                deliver_item("item_21", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, 300),
            assigned_tasks=[
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_25", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_35 = ScenarioConfig(
    id="scenario_s26_35",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 94),)),
    description=(
        "scenario_s26_35: script 062 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 94. Purpose: a coffee break after the "
        "one delivery; the second delivery never started. Aspects: unmodelled: a never-started delivery; "
        "foreseeable: at the end. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off; the never-started delivery never admitted (no observation warrant)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, -450),
            scheduled_tasks=Script([
                deliver_item("item_21", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
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

scenario_s26_36 = ScenarioConfig(
    id="scenario_s26_36",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 94),)),
    description=(
        "scenario_s26_36: script 062 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 0 to 94. Purpose: a coffee break after the "
        "one delivery; the second delivery never started. Aspects: unmodelled: a never-started delivery; "
        "foreseeable: at the end. Expectation: the delivery under break_time admitted later than with no "
        "fact, near off; the never-started delivery never admitted (no observation warrant). working robot: "
        "the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; under the window the delivery's admission and the robot's "
        "decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-800, -450),
            scheduled_tasks=Script([
                deliver_item("item_21", table="kitting_table_1"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(700, 300),
            assigned_tasks=[
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_25", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 063: unmodelled alone: a delivery abandoned after the grasp; the next delivery first returns the part to its shelf
scenario_s26_37 = ScenarioConfig(
    id="scenario_s26_37",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_37: script 063 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a delivery abandoned after the grasp; the next delivery first returns "
        "the part to its shelf. Aspects: unmodelled: an abandoned delivery (after the grasp) followed by a "
        "return; start: near the machine, first walk away. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); the abandoned delivery "
        "admitted while the human walks to it, then retracted as the evidence turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, 300),
            scheduled_tasks=Script([
                deliver_item("item_23", table="kitting_table_0").at(pick_up, drop),
                deliver_item("item_26", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
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

scenario_s26_38 = ScenarioConfig(
    id="scenario_s26_38",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_38: script 063 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: unmodelled alone: a delivery abandoned after the grasp; the next delivery first returns "
        "the part to its shelf. Aspects: unmodelled: an abandoned delivery (after the grasp) followed by a "
        "return; start: near the machine, first walk away. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); the abandoned delivery "
        "admitted while the human walks to it, then retracted as the evidence turns. working robot: the "
        "decisions as off where no admission moves; an earlier admission of a delivery moves the response "
        "decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, 300),
            scheduled_tasks=Script([
                deliver_item("item_23", table="kitting_table_0").at(pick_up, drop),
                deliver_item("item_26", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-300, -100),
            assigned_tasks=[
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_27", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_39 = ScenarioConfig(
    id="scenario_s26_39",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 30, 182),)),
    description=(
        "scenario_s26_39: script 063 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 30 to 182. Purpose: unmodelled alone: a "
        "delivery abandoned after the grasp; the next delivery first returns the part to its shelf. Aspects: "
        "unmodelled: an abandoned delivery (after the grasp) followed by a return; start: near the machine, "
        "first walk away. Expectation: the delivery under break_time admitted later than with no fact, near "
        "off; the abandoned delivery admitted while the human walks to it, then retracted as the evidence "
        "turns."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, 300),
            scheduled_tasks=Script([
                deliver_item("item_23", table="kitting_table_0").at(pick_up, drop),
                deliver_item("item_26", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
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

scenario_s26_40 = ScenarioConfig(
    id="scenario_s26_40",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 30, 182),)),
    description=(
        "scenario_s26_40: script 063 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 30 to 182. Purpose: unmodelled alone: a "
        "delivery abandoned after the grasp; the next delivery first returns the part to its shelf. Aspects: "
        "unmodelled: an abandoned delivery (after the grasp) followed by a return; start: near the machine, "
        "first walk away. Expectation: the delivery under break_time admitted later than with no fact, near "
        "off; the abandoned delivery admitted while the human walks to it, then retracted as the evidence "
        "turns. working robot: the decisions as off where no admission moves; an earlier admission of a "
        "delivery moves the response decision earlier or leaves it; under the window the delivery's "
        "admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(400, 300),
            scheduled_tasks=Script([
                deliver_item("item_23", table="kitting_table_0").at(pick_up, drop),
                deliver_item("item_26", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_23", table="kitting_table_0"),
                deliver_item("item_26", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-300, -100),
            assigned_tasks=[
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_27", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 064: a stand of 20 ticks at the start, then a coffee break inside a delivery before the grasp
scenario_s26_41 = ScenarioConfig(
    id="scenario_s26_41",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_41: script 064 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: a stand of 20 ticks at the start, then a coffee break inside a delivery before the grasp. "
        "Aspects: unmodelled: a stand (20 ticks) at the start; foreseeable: inside a delivery, before the "
        "grasp. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); a coffee break admitted later than off (ordinary strength); no admission "
        "during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, 150),
            scheduled_tasks=Script([
                stand("PT40S"),
                deliver_item("item_25", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_22", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_22", table="kitting_table_1"),
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

scenario_s26_42 = ScenarioConfig(
    id="scenario_s26_42",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_42: script 064 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a stand of 20 ticks at the start, then a coffee break inside a delivery before the grasp. "
        "Aspects: unmodelled: a stand (20 ticks) at the start; foreseeable: inside a delivery, before the "
        "grasp. Expectation: on against off: each delivery admitted earlier or equal (the assigned tasks "
        "share most of the prior); a coffee break admitted later than off (ordinary strength); no admission "
        "during the stand or the walk elsewhere, except a hypothesis whose target lies on the walk. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, 150),
            scheduled_tasks=Script([
                stand("PT40S"),
                deliver_item("item_25", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_22", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_22", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, 0),
            assigned_tasks=[
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_26", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_43 = ScenarioConfig(
    id="scenario_s26_43",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 36, 119),)),
    description=(
        "scenario_s26_43: script 064 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 36 to 119. Purpose: a stand of 20 ticks at the start, "
        "then a coffee break inside a delivery before the grasp. Aspects: unmodelled: a stand (20 ticks) at "
        "the start; foreseeable: inside a delivery, before the grasp. Expectation: the coffee break (raised "
        "by break_time) admitted earlier than off and than on with no fact; a delivery inside a window "
        "admitted later than with no fact; no admission during the stand or the walk elsewhere, except a "
        "hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, 150),
            scheduled_tasks=Script([
                stand("PT40S"),
                deliver_item("item_25", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_22", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_22", table="kitting_table_1"),
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

scenario_s26_44 = ScenarioConfig(
    id="scenario_s26_44",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 36, 119),)),
    description=(
        "scenario_s26_44: script 064 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 36 to 119. Purpose: a stand of 20 ticks at the "
        "start, then a coffee break inside a delivery before the grasp. Aspects: unmodelled: a stand (20 "
        "ticks) at the start; foreseeable: inside a delivery, before the grasp. Expectation: the coffee "
        "break (raised by break_time) admitted earlier than off and than on with no fact; a delivery inside "
        "a window admitted later than with no fact; no admission during the stand or the walk elsewhere, "
        "except a hypothesis whose target lies on the walk. working robot: the decisions as off where no "
        "admission moves; an earlier admission of a delivery moves the response decision earlier or leaves "
        "it; the coffee break admitted earlier, the robot's decision against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, 150),
            scheduled_tasks=Script([
                stand("PT40S"),
                deliver_item("item_25", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_22", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_22", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, 0),
            assigned_tasks=[
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_26", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_45 = ScenarioConfig(
    id="scenario_s26_45",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 258, 362),)),
    description=(
        "scenario_s26_45: script 064 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 258 to 362. Purpose: a stand of 20 ticks at "
        "the start, then a coffee break inside a delivery before the grasp. Aspects: unmodelled: a stand (20 "
        "ticks) at the start; foreseeable: inside a delivery, before the grasp. Expectation: the delivery "
        "under break_time admitted later than with no fact, near off; no admission during the stand or the "
        "walk elsewhere, except a hypothesis whose target lies on the walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(700, 150),
            scheduled_tasks=Script([
                stand("PT40S"),
                deliver_item("item_25", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_22", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_22", table="kitting_table_1"),
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

scenario_s26_46 = ScenarioConfig(
    id="scenario_s26_46",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 258, 362),)),
    description=(
        "scenario_s26_46: script 064 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 258 to 362. Purpose: a stand of 20 ticks at "
        "the start, then a coffee break inside a delivery before the grasp. Aspects: unmodelled: a stand (20 "
        "ticks) at the start; foreseeable: inside a delivery, before the grasp. Expectation: the delivery "
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
            start_position=(700, 150),
            scheduled_tasks=Script([
                stand("PT40S"),
                deliver_item("item_25", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_22", table="kitting_table_1"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_25", table="kitting_table_0"),
                deliver_item("item_22", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-800, 0),
            assigned_tasks=[
                deliver_item("item_21", table="kitting_table_1"),
                deliver_item("item_26", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# ---- script 065: two coffee breaks, at the start and at the end, far apart
scenario_s26_47 = ScenarioConfig(
    id="scenario_s26_47",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_47: script 065 of step 5e, the idle robot, no timeline (the setup states none). "
        "Purpose: two coffee breaks, at the start and at the end, far apart. Aspects: foreseeable: two, at "
        "the start and at the end; deliveries: two long carries. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted "
        "later than off (ordinary strength); the second under its recency fact (suppressed), later still."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
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

scenario_s26_48 = ScenarioConfig(
    id="scenario_s26_48",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    description=(
        "scenario_s26_48: script 065 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: two coffee breaks, at the start and at the end, far apart. Aspects: foreseeable: two, at "
        "the start and at the end; deliveries: two long carries. Expectation: on against off: each delivery "
        "admitted earlier or equal (the assigned tasks share most of the prior); a coffee break admitted "
        "later than off (ordinary strength); the second under its recency fact (suppressed), later still. "
        "working robot: the decisions as off where no admission moves; an earlier admission of a delivery "
        "moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -400),
            assigned_tasks=[
                deliver_item("item_27", table="kitting_table_0"),
                deliver_item("item_25", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_49 = ScenarioConfig(
    id="scenario_s26_49",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 47), window(BREAK_TIME, 287, 367),)),
    description=(
        "scenario_s26_49: script 065 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 0 to 47, break_time from 287 to 367. Purpose: two coffee "
        "breaks, at the start and at the end, far apart. Aspects: foreseeable: two, at the start and at the "
        "end; deliveries: two long carries. Expectation: the coffee break (raised by break_time) admitted "
        "earlier than off and than on with no fact; the second one suppressed by its recency fact, the "
        "window gives it nothing; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
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

scenario_s26_50 = ScenarioConfig(
    id="scenario_s26_50",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 0, 47), window(BREAK_TIME, 287, 367),)),
    description=(
        "scenario_s26_50: script 065 of step 5e, the working robot, its own timeline, the raising fact over "
        "the foreseeable task (accord): break_time from 0 to 47, break_time from 287 to 367. Purpose: two "
        "coffee breaks, at the start and at the end, far apart. Aspects: foreseeable: two, at the start and "
        "at the end; deliveries: two long carries. Expectation: the coffee break (raised by break_time) "
        "admitted earlier than off and than on with no fact; the second one suppressed by its recency fact, "
        "the window gives it nothing; a delivery inside a window admitted later than with no fact. working "
        "robot: the decisions as off where no admission moves; an earlier admission of a delivery moves the "
        "response decision earlier or leaves it; the coffee break admitted earlier, the robot's decision "
        "against it earlier."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -400),
            assigned_tasks=[
                deliver_item("item_27", table="kitting_table_0"),
                deliver_item("item_25", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s26_51 = ScenarioConfig(
    id="scenario_s26_51",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 47, 183),)),
    description=(
        "scenario_s26_51: script 065 of step 5e, the idle robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 47 to 183. Purpose: two coffee breaks, at "
        "the start and at the end, far apart. Aspects: foreseeable: two, at the start and at the end; "
        "deliveries: two long carries. Expectation: the delivery under break_time admitted later than with "
        "no fact, near off."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
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

scenario_s26_52 = ScenarioConfig(
    id="scenario_s26_52",
    setup="env_setup_26",
    reference_layouts=["env_layout_19"],
    timeline=Timeline((window(BREAK_TIME, 47, 183),)),
    description=(
        "scenario_s26_52: script 065 of step 5e, the working robot, its own timeline, break_time over a "
        "delivery (the human works through it): break_time from 47 to 183. Purpose: two coffee breaks, at "
        "the start and at the end, far apart. Aspects: foreseeable: two, at the start and at the end; "
        "deliveries: two long carries. Expectation: the delivery under break_time admitted later than with "
        "no fact, near off. working robot: the decisions as off where no admission moves; an earlier "
        "admission of a delivery moves the response decision earlier or leaves it; under the window the "
        "delivery's admission and the robot's decision on it later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-200, 200),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_20", table="kitting_table_1"),
                deliver_item("item_24", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(600, -400),
            assigned_tasks=[
                deliver_item("item_27", table="kitting_table_0"),
                deliver_item("item_25", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)
