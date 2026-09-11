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

scenario_01 = ScenarioConfig(
    id="scenario_01",
    name="layout0_phase4_test",
    description=(
        "Minimal Phase 4 development scenario. force cross passing"
        "... "
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(450, 350),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item,bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-450, 350),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
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
        "Phase 4C B2/B3 fixture. The robot's cheapest task (item_4, cost 1032) is the conflicted "
        "one, so the t=0 pick lands on it by construction. The conflict comes from matched "
        "arrival times at the shared kitting table: both carry legs converge there with a small "
        "gap, giving a long near-by overlap (step 22: item_4 min_dist 15.5, under 50 cm for ~166 "
        "projection units). item_6 (cost 1372, min_dist ~185) is a clean alternative. "
        "Measured (leg-level recognizer, PYTHONHASHSEED=0): t=0 confidence is below theta in "
        "both conditions, so no projection is built at t=0. (1) assignment_prior off — theta "
        "crosses at the human's GRASP (step 22, 0.797), after the robot's move_to has completed. "
        "(2) assignment_prior on — theta crosses at step 11 (0.780) when the human enters "
        "zone_SW and ZONE_BOOST applies to item_3; the robot is roughly half-way to shelf_4 (its "
        "move_to completes at 21), a projection is built, item_4 min_dist 14.98 vs item_6 292. "
        "(3) t=0 most_likely is a tie-break on layout item order (TODO-42). No foreseeable "
        "tasks. Human plan is scripted/fixed."
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