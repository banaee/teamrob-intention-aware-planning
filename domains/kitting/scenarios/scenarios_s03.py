# domains/kitting/scenarios/scenarios_s03.py
"""
Kitting scenarios on env_setup_03 — the scenarios of the old env_setup2 and
env_setup5 (content-identical, merged in T-L stage 2). One module per setup;
scenario ids keep their old form until stage 3.
Every task instance is written in the kitting call form (domains/kitting/script.py),
a human's script as a Script of task instances with events (T-H; migrated in T-H3):
an event's anchor is an action schema of the task's decomposition.
A task's class (WorkTask, PersonalTask, HumanOnlyTask) is declared in tasks.py — not repeated here.
"""

from shared.types import AgentConfig, ScenarioConfig, Script, drop
from domains.kitting.actions import move_to, pick_up
from domains.kitting.script import deliver_item, coffee_break, stand, go_to_and_stand


# ===============================================================
# manually defined scenarios, for only "env_layout_03".
# ===============================================================
scenario_s03_01 = ScenarioConfig(
    id="scenario_s03_01",
    setup="env_setup_03",
    reference_layouts=["env_layout_03"],
    description=(
        "Phase 4C B2/B3 fixture. The robot's cheapest task (item_4: 54 ticks at t=0, vs item_6 "
        "71 and item_7 103, at 20 cm/tick) is the conflicted one, so the t=0 pick lands on it by "
        "construction. The conflict comes from matched arrival times at the shared kitting "
        "table: the robot's approach + carry (447 + 583 cm) and the human's (449 + 617 cm) are "
        "within a tick of each other, so both carry walks converge into the table and both "
        "placements overlap there. item_6 (shelf_6, west) is the clean alternative; item_7 "
        "(shelf_7, far east) never competes. Measured conflict geometry, in the units of the "
        "day, lives in analysis/t1_conflict_measurement/REPORT.md and TODO-28/TODO-30, not "
        "here — those figures move whenever the meta-planner does. "
        "Recognizer behaviour (pre-I2 recognizer, PYTHONHASHSEED=0): t=0 confidence is "
        "below theta in both conditions, so no projection is built at t=0. (1) "
        "assignment_prior off — theta crosses at the human's GRASP (step 22, 0.797), after the "
        "robot's move_to has completed. (2) assignment_prior on — theta crosses at step 11 "
        "(0.780) when the human enters zone_SW and ZONE_BOOST applies to item_3; the robot is "
        "roughly half-way to shelf_4 (its move_to completes at 21), so a projection is built "
        "mid-approach. (3) t=0 most_likely is a tie-break on layout item order (TODO-42). No "
        "foreseeable tasks. Human plan is scripted/fixed."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
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
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_s03_02 = ScenarioConfig(
    id="scenario_s03_02",
    setup="env_setup_03",
    reference_layouts=["env_layout_03"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human picks up item_3, walks to corner_SE with it and stays 30 ticks, finishes the delivery, then delivers item_2."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, go_to_and_stand("corner_SE", "PT60S")),
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
            start_position=(-500, 300),
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
scenario_s03_03 = ScenarioConfig(
    id="scenario_s03_03",
    setup="env_setup_03",
    reference_layouts=["env_layout_03"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human delivers item_3, stays 40 ticks at the table while the robot converges on it, then delivers item_2."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                stand("PT80S"),
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
            start_position=(-500, 300),
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
scenario_s03_04 = ScenarioConfig(
    id="scenario_s03_04",
    setup="env_setup_03",
    reference_layouts=["env_layout_03"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human walks to item_3, turns without picking it up, delivers item_2."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(move_to, drop, occurrence=0),
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
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s03_05 = ScenarioConfig(
    id="scenario_s03_05",
    setup="env_setup_03",
    reference_layouts=["env_layout_03"],
    description=(
        "Phase 4C B2/B3 fixture. The robot's cheapest task (item_4: 54 ticks at t=0, vs item_6 "
        "71 and item_7 103, at 20 cm/tick) is the conflicted one, so the t=0 pick lands on it by "
        "construction. The conflict comes from matched arrival times at the shared kitting "
        "table: the robot's approach + carry (447 + 583 cm) and the human's (449 + 617 cm) are "
        "within a tick of each other, so both carry walks converge into the table and both "
        "placements overlap there. item_6 (shelf_6, west) is the clean alternative; item_7 "
        "(shelf_7, far east) never competes. Measured conflict geometry, in the units of the "
        "day, lives in analysis/t1_conflict_measurement/REPORT.md and TODO-28/TODO-30, not "
        "here — those figures move whenever the meta-planner does. "
        "Recognizer behaviour (pre-I2 recognizer, PYTHONHASHSEED=0): t=0 confidence is "
        "below theta in both conditions, so no projection is built at t=0. (1) "
        "assignment_prior off — theta crosses at the human's GRASP (step 22, 0.797), after the "
        "robot's move_to has completed. (2) assignment_prior on — theta crosses at step 11 "
        "(0.780) when the human enters zone_SW and ZONE_BOOST applies to item_3; the robot is "
        "roughly half-way to shelf_4 (its move_to completes at 21), so a projection is built "
        "mid-approach. (3) t=0 most_likely is a tie-break on layout item order (TODO-42). No "
        "foreseeable tasks. Human plan is scripted/fixed."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)


# ===============================================================
# manually defined scenarios, for only "env_layout_06" (env_layout_03 + rest_0).
# ===============================================================
scenario_s03_06 = ScenarioConfig(
    id="scenario_s03_06",
    setup="env_setup_03",
    reference_layouts=["env_layout_06"],
    description=(
        "End-state variant of scenario_s03_01 (F47, retyped F47b). Identical to scenario_s03_01 in every task, "
        "position and pool; the one change is a third human task after its last delivery: "
        "coffee_break at coffee_machine_0, a coffee machine 500 cm east of the table (env_layout_06 = "
        "env_layout_03 + the machine; until F47b it was a waypoint rest_0, an ill-typed binding). The human "
        "leaves the table for the machine instead of idling at it, stands there for the schema's PT60S and "
        "then idles THERE, so the robot's remaining table deliveries meet a free table. Because the "
        "machine exists, coffee_break(coffee_machine_0) is a hypothesis for the whole run (both priors), "
        "which scenario_s03_01 has not - the recognizer's live set differs from scenario_s03_01's from t=0: "
        "prior-on the first crossing moves from 6 to 8 (the hold of 8 with it, so the robot's whole "
        "timeline shifts 2 ticks and it now meets the departing human at 57-58 as prior-off does); "
        "prior-off an extra theta_crossed at 140 (coffee_break clears theta on the walk) re-confirms item_6. "
        "Measured (F47b, stop on): completes at 237 (prior off) / 239 (prior on) under both priors; "
        "scenario_s03_01 with the stop on is refused at the table from tick 144 to the cap. Stop off: "
        "235 / 237 (scenario_s03_01: 235 / 239). Earlier measurement with the waypoint (F47): "
    "stop on): identical to scenario_s03_01 until tick 124 (the human's item_2 placement); the human "
    "walks off at 125, stands at (477, 399) on 149-179; the robot's item_6 delivery, refused from "
    "tick 144 to the cap in scenario_s03_01, goes through and the run completes at 239 under both "
    "priors (prior-off keeps scenario_s03_01's 2-tick stop at 57-58). Stop off: 237 / 239 (scenario_s03_01: "
    "235 / 239). Reported next "
        "to scenario_s03_01, not instead of it: 'stays at the place' and 'steps aside after its last task' "
        "are the two end-state conditions (design_decisions.md, 'After C'; TODO-47 (d)). The walk to "
        "the machine (bearing 0 deg from the table) is >= 51 deg off every shelf, so no delivery "
        "hypothesis fits it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),   # steps aside: a coffee break at the machine east of the table
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
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_s03_07 = ScenarioConfig(
    id="scenario_s03_07",
    setup="env_setup_03",
    reference_layouts=["env_layout_06"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "One table, so no wrong destination: human walks to item_2, turns without picking it up, delivers item_3."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0").at(move_to, drop, occurrence=0),
                deliver_item("item_3", table="kitting_table_0"),
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
            start_position=(-500, 300),
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
scenario_s03_08 = ScenarioConfig(
    id="scenario_s03_08",
    setup="env_setup_03",
    reference_layouts=["env_layout_06"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human picks up item_3, walks to corner_NW with it and stays 30 ticks, finishes the delivery, then delivers item_2."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, go_to_and_stand("corner_NW", "PT60S")),
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
            start_position=(-500, 300),
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
scenario_s03_09 = ScenarioConfig(
    id="scenario_s03_09",
    setup="env_setup_03",
    reference_layouts=["env_layout_06"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human delivers item_3 and item_2, stays 40 ticks at the table, then takes a coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                stand("PT80S"),
                coffee_break("coffee_machine_0"),
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
            start_position=(-500, 300),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

