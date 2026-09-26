# domains/kitting/scenarios/scenarios_s07.py
"""
Kitting scenarios on env_setup_07 — the scenarios of the old env_setup9.
One module per setup; scenario ids keep their old form until stage 3.
Every task instance is written in the kitting call form (domains/kitting/script.py),
a human's script as a Script of task instances with events (T-H; migrated in T-H3):
an event's anchor is an action schema of the task's decomposition.
A task's class (WorkTask, PersonalTask, HumanOnlyTask) is declared in tasks.py — not repeated here.
"""

from shared.types import AgentConfig, ScenarioConfig, Script, drop
from domains.kitting.actions import move_to, pick_up
from domains.kitting.script import deliver_item, go_to, stand, go_to_and_stand


# ===============================================================
# manually defined scenario, for only "env_layout_09" (two kitting tables against
# opposite walls; the realistic-placement variant of env_layout_08).
# scenario_s07_01 is for VIEWING env_layout_09 and running it: it is NOT a measured
# fixture, nothing is measured from it, and T-B does not use it. The measured
# two-table fixture is scenario_s06_01 / scenario_s06_02 on env_layout_08.
# ===============================================================
scenario_s07_01 = ScenarioConfig(
    id="scenario_s07_01",
    setup="env_setup_07",
    reference_layouts=["env_layout_09"],
    description=(
        "env_layout_09: kitting_table_0 against the north wall, kitting_table_1 against the south wall. "
        "The robot's pool is item_5 / item_4 / item_1 (to kitting_table_1) and item_6 (to kitting_table_0); "
        "the human fetches item_2 to kitting_table_0 and item_3 to kitting_table_1. Not a fixture."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-850, 250),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
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
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_s07_02 = ScenarioConfig(
    id="scenario_s07_02",
    setup="env_setup_07",
    reference_layouts=["env_layout_09"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human walks to item_3, turns without picking it up, delivers item_2."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-850, 250),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1").at(move_to, drop, occurrence=0),
                deliver_item("item_2", table="kitting_table_0"),
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
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# Script example (T-C2c play), not a measured fixture.
scenario_s07_03 = ScenarioConfig(
    id="scenario_s07_03",
    setup="env_setup_07",
    reference_layouts=["env_layout_09"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human delivers item_2 to kitting_table_1 instead of its table (kitting_table_0), then delivers item_3."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-850, 250),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_1"),
                deliver_item("item_3", table="kitting_table_1"),
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
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# Script example (T-C2c play), not a measured fixture.
scenario_s07_04 = ScenarioConfig(
    id="scenario_s07_04",
    setup="env_setup_07",
    reference_layouts=["env_layout_09"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human picks up item_2, walks to corner_NE with it and stays 30 ticks, finishes the delivery, then delivers item_3."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-850, 250),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(pick_up, go_to_and_stand("corner_NE", "PT60S")),
                deliver_item("item_3", table="kitting_table_1"),
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
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_s07_05 = ScenarioConfig(
    id="scenario_s07_05",
    setup="env_setup_07",
    reference_layouts=["env_layout_09"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human delivers item_2 and item_3, stays 40 ticks at kitting_table_1 while the robot converges on it, then walks to corner_SE."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-850, 250),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
                stand("PT80S"),
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
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

