# domains/kitting/scenarios/scenarios_s01.py
"""
Kitting scenarios on env_setup_01 — the scenarios of the old env_setup0 and
env_setup3 (content-identical, merged in T-L stage 2). One module per setup;
scenario ids keep their old form until stage 3.
Every task instance is written in the kitting call form (domains/kitting/script.py),
a human's script as a Script of task instances with events (T-H; migrated in T-H3):
an event's anchor is an action schema of the task's decomposition.
A task's class (WorkTask, PersonalTask, HumanOnlyTask) is declared in tasks.py — not repeated here.
"""

from shared.types import AgentConfig, ScenarioConfig, Script, drop
from domains.kitting.actions import pick_up
from domains.kitting.script import deliver_item, go_to, stand, go_to_and_stand


# ===============================================================
# manually defined scenario, for only "env_layout0".
# ===============================================================
scenario_00 = ScenarioConfig(
    id="scenario_00",
    setup="env_setup_01",
    reference_layouts=["env_layout0"],
    description=(
        "Minimal Phase 4 development scenario. Robot and human start symmetric, "
        "paths intersect near center during first moveto (case 0.1 collision). "
        "Both converge on KT after picking (case 0.2 conflict). "
        "No foreseeable tasks. Human plan is scripted/fixed."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(350, 200),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-350, 200),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c scenario B, declared stay: a fixture, not a baseline (analysis/tc2c_scripts/).
# The human delivers item_3 and stays at the table 40 ticks; the robot's one
# delivery goes to that table. The stay is not projected (TODO-85).
scenario_01 = ScenarioConfig(
    id="scenario_01",
    setup="env_setup_01",
    reference_layouts=["env_layout0"],
    description=(
        "T-C2c scenario B. Human delivers item_3, then stands 40 ticks at kitting_table_0 (stand PT80S). "
        "The robot's one task delivers item_4 to the same table."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(350, 200),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                stand("PT80S"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-350, 200),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_02 = ScenarioConfig(
    id="scenario_02",
    setup="env_setup_01",
    reference_layouts=["env_layout0"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human picks up item_3, abandons it (the next delivery returns it to its shelf first, deliver_with_return), delivers item_2."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(350, 200),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, drop),
                deliver_item("item_2", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-350, 200),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# Script example (T-C2c play), not a measured fixture.
scenario_03 = ScenarioConfig(
    id="scenario_03",
    setup="env_setup_01",
    reference_layouts=["env_layout0"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human picks up item_3, walks to corner_NE with it and stays 30 ticks, finishes the delivery, then delivers item_2."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(350, 200),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, go_to_and_stand("corner_NE", "PT60S")),
                deliver_item("item_2", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-350, 200),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# Script example (T-C2c play), not a measured fixture.
scenario_04 = ScenarioConfig(
    id="scenario_04",
    setup="env_setup_01",
    reference_layouts=["env_layout0"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human walks to the door, stays 20, walks to corner_SW, then delivers item_3, its one assigned task."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(350, 200),
            scheduled_tasks=Script([
                go_to("door"),
                stand("PT40S"),
                go_to("corner_SW"),
                deliver_item("item_3", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-350, 200),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)


# ===============================================================
# manually defined scenarios, for only "env_layout3".
# ===============================================================
scenario_30 = ScenarioConfig(
    id="scenario_30",
    setup="env_setup_01",
    reference_layouts=["env_layout3"],
    description=(
        "Intersecting-paths fixture (TODO-47(c)). Mirror-symmetric approaches make the two paths intersect "
        "on the robot's CURRENT task: the human starts at (300, 300) and walks to shelf_3 at "
        "(-200, -300) for item_3; the robot starts at (-300, 300) and walks to shelf_4 at "
        "(200, -300) for item_4, its cheapest task, so the t=0 pick lands on it. The two "
        "straight approaches are mirror images across x = 0 and pass through each other at "
        "the centre line (step 22, 11 cm apart) while both agents are still in move_to. The "
        "human hypothesis is correct throughout (item_3 is the human's first scripted task) "
        "and no distractor item sits between the human and item_3: the only other pool item, "
        "item_7 at shelf_7 (-400, 200), lies 42 deg off the human's heading, behind and to the "
        "side. Under the current linear chord kernel that is still close enough to take most "
        "of the chord credit (TODO-38), so during the approach item_3 holds 0.471, doubles to "
        "0.640 on zone_SW entry at step 23 (ZONE_BOOST), and reaches theta only at the grasp "
        "(step 39) - the path intersection itself is never seen by the meta-planner. Measured with "
        "PYTHONHASHSEED=0, assignment_prior on. No foreseeable tasks. Human plan is "
        "scripted/fixed. Geometry: env_layout3.json."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 300),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-300, 300),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_31 = ScenarioConfig(
    id="scenario_31",
    setup="env_setup_01",
    reference_layouts=["env_layout3"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human picks up item_3, abandons it (the next delivery returns it to its shelf first, deliver_with_return), delivers item_7."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 300),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, drop),
                deliver_item("item_7", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-300, 300),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# Script example (T-C2c play), not a measured fixture.
scenario_32 = ScenarioConfig(
    id="scenario_32",
    setup="env_setup_01",
    reference_layouts=["env_layout3"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human walks to the door, stays 20, walks to corner_SW, then delivers item_3 and item_7."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 300),
            scheduled_tasks=Script([
                go_to("door"),
                stand("PT40S"),
                go_to("corner_SW"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-300, 300),
            assigned_tasks=[
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_4", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

