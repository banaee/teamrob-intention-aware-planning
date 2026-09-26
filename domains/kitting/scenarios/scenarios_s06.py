# domains/kitting/scenarios/scenarios_s06.py
"""
Kitting scenarios on env_setup_06 — the scenarios of the old env_setup8.
One module per setup; scenario ids keep their old form until stage 3.
Every task instance is written in the kitting call form (domains/kitting/script.py),
a human's script as a Script of task instances with events (T-H; migrated in T-H3):
an event's anchor is an action schema of the task's decomposition.
A task's class (WorkTask, PersonalTask, HumanOnlyTask) is declared in tasks.py — not repeated here.
"""

from shared.types import AgentConfig, ScenarioConfig, Script, drop
from domains.kitting.actions import move_to
from domains.kitting.script import deliver_item


# ===============================================================
# manually defined scenarios, for only "env_layout_08" (two kitting tables; T-B1b).
# scenario_s06_01 / scenario_s06_02 are the two-table fixture for B3.B: the cost
# argument and the baselines are in analysis/tb1b_two_tables/README.md.
# The robot's pool: item_6 and item_1 (short, beside kitting_table_0), item_4
# (far east, to kitting_table_0), item_7 (near the robot's start, to
# kitting_table_1). From the robot's start the cheapest single task is item_6,
# but the cheapest full ordering starts with item_7.
# ===============================================================
scenario_s06_01 = ScenarioConfig(
    id="scenario_s06_01",
    setup="env_setup_06",
    reference_layouts=["env_layout_08"],
    description=(
        "Two tables, ordering isolated: the robot's cheapest first task (item_6) is not the head of its "
        "cheapest full ordering (item_7 first). The human works the north shelves, uses both tables and "
        "stays clear of the robot's paths."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 400),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s06_02 = ScenarioConfig(
    id="scenario_s06_02",
    setup="env_setup_06",
    reference_layouts=["env_layout_08"],
    description=(
        "scenario_s06_01 with the human starting further from item_0: its first task spans the robot's two "
        "short tasks and ends at kitting_table_0 as the second of them does, so the conflict falls in the "
        "second task of the ordering (item_6, item_1), not in its head."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 200),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# scenario_s06_03 (T-B1c): the existence case in which realized cost changes the
# HEAD under full_reorder — a conflict in an entry after the head, which the
# head realized alone cannot see. The robot's side is scenario_s06_01's; only the
# human's differs. The human fetches item_3 first (a 66-tick walk along the
# north wall, then the carry to kitting_table_1) and then item_0, so that its
# carry of item_0 reaches kitting_table_0 while the robot, having delivered
# item_4 there, is on the second of its two short tasks: in the plain-cost
# ordering (item_6, item_1) the item_1 entry arrives at the table while the
# human stands there releasing item_0 (a 3-tick hold before that entry), in
# (item_1, item_6) the item_6 entry arrives after the human's projection ends.
# The start position sets that timing; the record is analysis/tb1c_realized_flip/.
scenario_s06_03 = ScenarioConfig(
    id="scenario_s06_03",
    setup="env_setup_06",
    reference_layouts=["env_layout_08"],
    description=(
        "scenario_s06_01 with the human working item_3 then item_0 from the north wall: its item_0 carry reaches "
        "kitting_table_0 as the second of the robot's two short tasks does, so under full_reorder the plain-cost "
        "ordering (item_6, item_1) carries a hold before item_1 and realized cost makes item_1 the head."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-430, 400),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_0", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_1"),
                deliver_item("item_0", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# scenario_s06_04 is for VIEWING env_layout_08 (the Solara viewer), one task each:
# it is not a fixture, nothing is measured from it, and T-B does not use it.
scenario_s06_04 = ScenarioConfig(
    id="scenario_s06_04",
    setup="env_setup_06",
    reference_layouts=["env_layout_08"],
    description=(
        "Minimal scenario for opening env_layout_08 in the viewer: one robot task and one human task. "
        "Not a fixture."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 400),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_s06_05 = ScenarioConfig(
    id="scenario_s06_05",
    setup="env_setup_06",
    reference_layouts=["env_layout_08"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human walks to item_3, turns without picking it up, delivers item_0."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 400),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_1").at(move_to, drop, occurrence=0),
                deliver_item("item_0", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

# Script example (T-C2c play), not a measured fixture.
scenario_s06_06 = ScenarioConfig(
    id="scenario_s06_06",
    setup="env_setup_06",
    reference_layouts=["env_layout_08"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human delivers item_0 to kitting_table_1 instead of its table (kitting_table_0), then delivers item_3."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 400),
            scheduled_tasks=Script([
                deliver_item("item_0", table="kitting_table_1"),
                deliver_item("item_3", table="kitting_table_1"),
            ]),
            assigned_tasks=[
                deliver_item("item_0", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_1"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)

