# domains/kitting/scenarios/scenarios_s08.py
"""
Kitting scenarios on env_setup_08 — the IR test-bed (TB; design_records.md, "The IR test-bed").
One module per setup. Every task instance is written in the kitting call form (domains/kitting/script.py),
a human's script as a Script of task instances with events (T-H): an event's anchor is an action schema of
the task's decomposition.
The recognizer is tested in isolation: the robot has an empty task pool and only observes; the human starts at
the kitting table, is assigned both deliveries (never in an order) and ends every script with the exit walk to
corner_SE. Prior ON in every run (configs/ir_testbed/). The coffee break's duration is the schema's.
"""

from shared.types import AgentConfig, ScenarioConfig, Script
from domains.kitting.actions import move_to, pick_up
from domains.kitting.script import deliver_item, coffee_break, go_to


# ===============================================================
# the IR test-bed, on "env_layout_10" (analysis/ir_testbed/)
# ===============================================================
_TB = (
    "IR test-bed (TB): the recognizer in isolation, against expectations derived from the records before the run "
    "(analysis/ir_testbed/). The robot at (0.10 W, 0.10 H) with an empty task pool, observing only; the human starts "
    "at the kitting table, assigned deliver_item(item_1) and deliver_item(item_2), and ends with the exit walk to "
    "corner_SE. Prior on. "
)


scenario_s08_01 = ScenarioConfig(
    id="scenario_s08_01",
    setup="env_setup_08",
    reference_layouts=["env_layout_10"],
    description=_TB + (
        "scenario_s08_01, two deliveries: deliver item_1, deliver item_2, exit. After both deliveries coffee_break "
        "is the lone live hypothesis (1.0 by normalisation) and the exit walk is charged against its walk to the "
        "machine (TODO-117's case)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s08_02 = ScenarioConfig(
    id="scenario_s08_02",
    setup="env_setup_08",
    reference_layouts=["env_layout_10"],
    description=_TB + (
        "scenario_s08_02, coffee between: deliver item_1, coffee_break, deliver item_2, exit. coffee_break is "
        "retired once waited holds, so no hypothesis is live after the second delivery: exhausted on the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s08_03 = ScenarioConfig(
    id="scenario_s08_03",
    setup="env_setup_08",
    reference_layouts=["env_layout_10"],
    description=_TB + (
        "scenario_s08_03, coffee after the pick-up: coffee_break started at the boundary after item_1's pick_up "
        "(the item in hand during the break; the resumption re-expands the carry), then deliver item_2, exit. "
        "A suspended task state, L's subject: the expectations are mechanical from the current records, and the "
        "test-bed does not resolve L."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s08_04 = ScenarioConfig(
    id="scenario_s08_04",
    setup="env_setup_08",
    reference_layouts=["env_layout_10"],
    description=_TB + (
        "scenario_s08_04, coffee before the pick-up: coffee_break started at the boundary after item_1's first "
        "move_to (empty-handed at the shelf; the resumption re-expands the walk back to the shelf, then the "
        "pick-up), then deliver item_2, exit. A suspended task state, L's subject: the expectations are mechanical "
        "from the current records, and the test-bed does not resolve L."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)
