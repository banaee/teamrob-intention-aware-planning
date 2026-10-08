# domains/kitting/scenarios/scenarios_s24.py
"""
Kitting scenarios on env_setup_24: T-K part 1, step 5e (context knowledge on kitting's rooms 02, 05, 06, 07 and the copies
of 08 and 09 with a coffee machine; analysis/kitting/tk5e/README.md). One module per setup. The room is env_layout_07; the shift
env_setup_24: a second shift: the human's parts on shelf_1 (behind the coffee machine), shelf_5 (beside it) and shelf_3 (across the table); the robot's on shelf_2, shelf_3 and shelf_1.
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



scenario_s304_14 = ScenarioConfig(
    id="scenario_s304_14",
    setup="env_setup_304",
    reference_layouts=["env_layout_07"],
    description=(
        "scenario_s304_14: script 043 of step 5e, the working robot, no timeline (the setup states none). "
        "Purpose: a second coffee break soon after the first, at the start and after the first delivery. "
        "Aspects: foreseeable: two coffee breaks, at the start and between. Expectation: on against off: "
        "each delivery admitted earlier or equal (the assigned tasks share most of the prior); a coffee "
        "break admitted later than off (ordinary strength); the second under its recency fact (suppressed), "
        "later still. working robot: the decisions as off where no admission moves; an earlier admission of "
        "a delivery moves the response decision earlier or leaves it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -300),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_53", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_52", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-750, 400),
            assigned_tasks=[
                deliver_item("item_54", table="kitting_table_0"),
                deliver_item("item_55", table="kitting_table_0"),
                deliver_item("item_56", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s304_15 = ScenarioConfig(
    id="scenario_s304_15",
    setup="env_setup_304",
    reference_layouts=["env_layout_07"],
    timeline=Timeline((window(BREAK_TIME, 0, 51), window(BREAK_TIME, 90, 150),)),
    description=(
        "scenario_s304_15: script 043 of step 5e, the idle robot, its own timeline, the raising fact over the "
        "foreseeable task (accord): break_time from 0 to 51, break_time from 90 to 150. Purpose: a second "
        "coffee break soon after the first, at the start and after the first delivery. Aspects: foreseeable: "
        "two coffee breaks, at the start and between. Expectation: the coffee break (raised by break_time) "
        "admitted earlier than off and than on with no fact; the second one suppressed by its recency fact, "
        "the window gives it nothing; a delivery inside a window admitted later than with no fact."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, -300),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_52", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_53", table="kitting_table_0"),
                go_to("corner_NE"),
            ]),
            assigned_tasks=[
                deliver_item("item_52", table="kitting_table_0"),
                deliver_item("item_53", table="kitting_table_0"),
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

