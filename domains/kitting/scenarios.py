# domains/kitting/scenarios.py
"""
Scenario definitions for the kitting domain.
Task assignments reference domain schemas directly — no string parsing,
no YAML, no ? prefix conventions.
is_foreseeable is declared on TaskSchema — not repeated here.
"""

from shared.types import Var, Const, TaskInstance, AgentConfig, ScenarioConfig
from domains.kitting.tasks import deliver_item, coffee_break, ac_activation



# ===============================================================
# manually defined scenario, for only "env_layout0".
# ===============================================================
scenario_00 = ScenarioConfig(
    id="scenario_00",
    name="layout0_phase4_collision_baseline",
    description=(
        "Minimal Phase 4 development scenario. Robot and human start symmetric, "
        "paths cross near center during first moveto (case 0.1 collision). "
        "Both converge on KT after picking (case 0.2 conflict). "
        "No foreseeable tasks. Human plan is scripted/fixed."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(350, 200),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item,bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-350, 200),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)


# ===============================================================
# manually defined scenarios, for only "env_layout1".
# ===============================================================
scenario_10 = ScenarioConfig(
    id="scenario_10",
    name="basic_kitting_with_coffee_break",
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
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=coffee_break,  bindings={Var("?coffee_machine"): Const("coffee_machine_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=ac_activation,  bindings={Var("?ac_switch"): Const("ac_switch_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(200, 200),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)

# ===============================================================
# manually defined scenarios, for only "env_layout2".
# ===============================================================
scenario_20 = ScenarioConfig(
    id="scenario_20",
    name="layout2_midapproach_sustained_conflict",
    description=(
        "Phase 4C B2/B3 fixture. The robot's cheapest task (item_4: 54 ticks at t=0, vs item_6 "
        "71 and item_7 103, at 20 cm/tick) is the conflicted one, so the t=0 pick lands on it by "
        "construction. The conflict comes from matched arrival times at the shared kitting "
        "table: the robot's approach + carry (447 + 583 cm) and the human's (449 + 617 cm) are "
        "within a tick of each other, so both carry legs converge into the table and both "
        "placements overlap there. item_6 (shelf_6, west) is the clean alternative; item_7 "
        "(shelf_7, far east) never competes. Measured conflict geometry, in the units of the "
        "day, lives in analysis/t1_conflict_measurement/REPORT.md and TODO-28/TODO-30, not "
        "here — those figures move whenever the meta-planner does. "
        "Recognizer behaviour (leg-level recognizer, PYTHONHASHSEED=0): t=0 confidence is "
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
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-500, 300),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
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
    name="layout3_midpath_crossing",
    description=(
        "Crossing fixture (TODO-47(c)). Mirror-symmetric approaches force a mid-path crossing "
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
        "(step 39) - the crossing itself is never seen by the meta-planner. Measured with "
        "PYTHONHASHSEED=0, assignment_prior on. No foreseeable tasks. Human plan is "
        "scripted/fixed. Geometry: env_layout3.json."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 300),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-300, 300),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)
