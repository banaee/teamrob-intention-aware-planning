# domains/kitting/scenarios/scenarios_s02.py
"""
Kitting scenarios on env_setup_02 — the scenarios of the old env_setup1.
One module per setup; scenario ids keep their old form until stage 3.
Every task instance is written in the kitting call form (domains/kitting/script.py),
a human's script as a Script of task instances with events (T-H; migrated in T-H3):
an event's anchor is an action schema of the task's decomposition.
A task's class (WorkTask, PersonalTask, HumanOnlyTask) is declared in tasks.py — not repeated here.
"""

from shared.types import AgentConfig, ScenarioConfig, Script, drop
from domains.kitting.actions import pick_up
from domains.kitting.script import deliver_item, coffee_break, ac_activation, stand


# ===============================================================
# manually defined scenarios, for only "env_layout1".
# ===============================================================
scenario_10 = ScenarioConfig(
    id="scenario_10",
    setup="env_setup_02",
    reference_layouts=["env_layout1"],
    description=(
        "Human and robot each deliver items to the kitting table. "
        "Human deviates to a coffee break after completing their first delivery. "
        "Robot must recognize the deviation and replan accordingly."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
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
            start_position=(200, 0),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c scenario A, interrupted delivery: a fixture, not a baseline (analysis/tc2c_scripts/).
# The human picks item_2, walks away from the table to the coffee machine with it,
# waits, then resumes the delivery; item_5 follows so the assigned tasks are s10's.
scenario_11 = ScenarioConfig(
    id="scenario_11",
    setup="env_setup_02",
    reference_layouts=["env_layout1"],
    description=(
        "T-C2c scenario A. deliver(item_2).at(pick_up, coffee_break): suspended for the coffee break, then resumed; "
        "then deliver(item_5). Robot side and assigned tasks as scenario_10."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_5", table="kitting_table_0"),
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
            start_position=(200, 0),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_12 = ScenarioConfig(
    id="scenario_12",
    setup="env_setup_02",
    reference_layouts=["env_layout1"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human takes a coffee break with item_2 in hand, delivers it, stays 20 at the table, then picks up item_5 and abandons it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                stand("PT40S"),
                deliver_item("item_5", table="kitting_table_0").at(pick_up, drop),
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
            start_position=(200, 0),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

