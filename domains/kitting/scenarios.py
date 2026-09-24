# domains/kitting/scenarios.py
"""
Scenario definitions for the kitting domain.
Task assignments reference domain schemas directly — no string parsing,
no YAML, no ? prefix conventions.
is_foreseeable is declared on TaskSchema — not repeated here.
"""

from shared.types import Var, Const, TaskInstance, AgentConfig, ScenarioConfig
from domains.kitting.tasks import deliver_item, coffee_break, ac_activation
from domains.kitting.script import MoveTo, Stay, interrupt, deviate, abandon



# ===============================================================
# manually defined scenario, for only "env_layout0".
# ===============================================================
scenario_00 = ScenarioConfig(
    id="scenario_00",
    name="layout0_phase4_collision_baseline",
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

# T-C2c scenario B, declared stay: a fixture, not a baseline (analysis/tc2c_scripts/).
# The human delivers item_3 and stays at the table 40 ticks; the robot's one
# delivery goes to that table. The stay is not projected (TODO-85).
scenario_01 = ScenarioConfig(
    id="scenario_01",
    name="layout0_declared_stay",
    description=(
        "T-C2c scenario B. Human delivers item_3, then Stay(40) at kitting_table_0. "
        "The robot's one task delivers item_4 to the same table."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(350, 200),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                Stay(40),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-350, 200),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
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
    name="layout0_change_of_mind_after_pickup",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human picks up item_3, abandons it (the return to its shelf is inserted by sequential expansion), delivers item_2."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(350, 200),
            scheduled_tasks=[
                *abandon(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                    after="pick_up",
                    then=[TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")})],
                ),
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

scenario_03 = ScenarioConfig(
    id="scenario_03",
    name="layout0_landmark_stay_mid_carry",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human picks up item_3, walks to corner_NE with it and stays 30 ticks, finishes the delivery, then delivers item_2."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(350, 200),
            scheduled_tasks=[
                *interrupt(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                    after="pick_up",
                    with_=[MoveTo("corner_NE"), Stay(30)],
                ),
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

scenario_04 = ScenarioConfig(
    id="scenario_04",
    name="layout0_free_actions_then_delivery",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human walks to the door, stays 20, walks to corner_SW, then delivers item_3, its one assigned task."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(350, 200),
            scheduled_tasks=[
                MoveTo("door"),
                Stay(20),
                MoveTo("corner_SW"),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
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
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=ac_activation,  bindings={Var("?ac_switch"): Const("ac_switch_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(200, 0),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c scenario A, interrupted delivery: a fixture, not a baseline (analysis/tc2c_scripts/).
# The human picks item_2, walks away from the table to the coffee machine with it,
# waits, then resumes the delivery; item_5 follows so the work order is s10's.
scenario_11 = ScenarioConfig(
    id="scenario_11",
    name="layout1_interrupted_delivery",
    description=(
        "T-C2c scenario A. interrupt(deliver(item_2), after=pick_up, with_=[coffee_break]), "
        "then deliver(item_5). Robot side and assigned tasks as scenario_10."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=[
                *interrupt(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                    after="pick_up",
                    with_=[TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("coffee_machine_0")})],
                ),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(200, 0),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
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
    name="layout1_coffee_stay_abandon",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human takes a coffee break with item_2 in hand, delivers it, stays 20 at the table, then picks up item_5 and abandons it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-400, -300),
            scheduled_tasks=[
                *interrupt(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                    after="pick_up",
                    with_=[TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("coffee_machine_0")})],
                ),
                Stay(20),
                *abandon(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
                    after="pick_up",
                ),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(200, 0),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
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

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_22 = ScenarioConfig(
    id="scenario_22",
    name="layout2_landmark_stay_after_pickup",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human picks up item_3, walks to corner_SE with it and stays 30 ticks, finishes the delivery, then delivers item_2."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=[
                *interrupt(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                    after="pick_up",
                    with_=[MoveTo("corner_SE"), Stay(30)],
                ),
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

scenario_23 = ScenarioConfig(
    id="scenario_23",
    name="layout2_table_stay_robot_converging",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human delivers item_3, stays 40 ticks at the table while the robot converges on it, then delivers item_2."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                Stay(40),
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

scenario_24 = ScenarioConfig(
    id="scenario_24",
    name="layout2_change_of_mind_before_pickup",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human walks to item_3, turns without picking it up, delivers item_2."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=[
                *abandon(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                    before="pick_up",
                ),
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

scenario_21 = ScenarioConfig(
    id="scenario_21",
    name="layout2_midapproach_sustained_conflict",
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
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
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

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_31 = ScenarioConfig(
    id="scenario_31",
    name="layout3_change_of_mind_after_pickup",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human picks up item_3, abandons it (the return to its shelf is inserted by sequential expansion), delivers item_7."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 300),
            scheduled_tasks=[
                *abandon(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                    after="pick_up",
                    then=[TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")})],
                ),
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

scenario_32 = ScenarioConfig(
    id="scenario_32",
    name="layout3_free_actions_then_deliveries",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human walks to the door, stays 20, walks to corner_SW, then delivers item_3 and item_7."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 300),
            scheduled_tasks=[
                MoveTo("door"),
                Stay(20),
                MoveTo("corner_SW"),
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

# ===============================================================================
# manually defined scenario, for only "env_layout4".
# ===============================================================================
scenario_40 = ScenarioConfig(
    id="scenario_40",
    name="layout4_foreseeable_and_unmodelled",
    description=(
        "Foreseeable-task fixture (I1 follow-up; baseline for I3/I4). One human run in four "
        "segments. (1) deliver item_3 from shelf_3 (-950, -50): 1209 cm approach from "
        "(100, 550), every other target >= 50 deg off the heading - the positive control. "
        "(2) coffee_break at coffee_machine_0 (-40, -250): scheduled, not assigned; from the "
        "kitting table the coffee bearing is >= 49.6 deg off every task target. (3) walk to two "
        "AC switches: ac_switch_1 (356, -210) lies on the straight line from the coffee machine to "
        "shelf_6, so the human first heads toward a shelf it will deliver from later; ac_switch_2 "
        "(230, -550) is >= 64 deg off every delivery target seen from ac_switch_1, so the turn is a "
        "retraction case. The two walks are ac_activation instances (move_to + a one-tick wait_at). "
        "F47b: until then the two targets were 'waypoint' objects wander_0 / wander_1 that no task "
        "enumerates, bound to ac_activation anyway - an ill-typed script; they were retyped as AC "
        "switches at the same coordinates, so ac_activation now has three hypotheses (ac_switch_0, "
        "never visited, plus these two) and the IR lines of this fixture changed (baseline "
        "regenerated, analysis/f47_fixtures/). (4) deliver item_6 from shelf_6 (950, -150), so "
        "the assigned pool is exactly the deliveries; shelf_5 (robot, undelivered then) is "
        "17 deg off this last approach - a prior-off decoy, inadmissible prior-on. Robot: "
        "item_4, item_7, item_5 from a SW start, ~375 ticks of work so the IR keeps observing "
        "until the human's script ends (~330 ticks). Run with --steps 400. Measured baselines: "
        "analysis/f1_foreseeable_fixture/REPORT.md."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("coffee_machine_0")}),
                TaskInstance(schema=ac_activation, bindings={Var("?ac_switch"): Const("ac_switch_1")}),   # script part 3, walk 1: toward shelf_6 (an AC switch since F47b; was the waypoint wander_0)
                TaskInstance(schema=ac_activation, bindings={Var("?ac_switch"): Const("ac_switch_2")}),   # script part 3, walk 2: turn away
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_41 = ScenarioConfig(
    id="scenario_41",
    name="layout4_coffee_stay_abandon",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human takes a coffee break with item_3 in hand, delivers it, stays 20 at the table, then picks up item_6 and abandons it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=[
                *interrupt(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                    after="pick_up",
                    with_=[TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("coffee_machine_0")})],
                ),
                Stay(20),
                *abandon(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
                    after="pick_up",
                ),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_42 = ScenarioConfig(
    id="scenario_42",
    name="layout4_abandon_to_corner_holding",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human delivers item_3, then picks up item_6, abandons it and walks to corner_SE holding it, where it stands."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                *abandon(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
                    after="pick_up",
                    then=[MoveTo("corner_SE")],
                ),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)

# ===============================================================
# manually defined scenarios, for only "env_layout5" (env_layout2 + rest_0).
# ===============================================================
scenario_50 = ScenarioConfig(
    id="scenario_50",
    name="layout5_end_state_steps_aside",
    description=(
        "End-state variant of scenario_20 (F47, retyped F47b). Identical to scenario_20 in every task, "
        "position and pool; the one change is a third human task after its last delivery: "
        "coffee_break at coffee_machine_0, a coffee machine 500 cm east of the table (env_layout5 = "
        "env_layout2 + the machine; until F47b it was a waypoint rest_0, an ill-typed binding). The human "
        "leaves the table for the machine instead of idling at it, stands there for the schema's PT60S and "
        "then idles THERE, so the robot's remaining table deliveries meet a free table. Because the "
        "machine exists, coffee_break(coffee_machine_0) is a hypothesis for the whole run (both priors), "
        "which scenario_20 has not - the recognizer's live set differs from scenario_20's from t=0: "
        "prior-on the first crossing moves from 6 to 8 (the hold of 8 with it, so the robot's whole "
        "timeline shifts 2 ticks and it now meets the departing human at 57-58 as prior-off does); "
        "prior-off an extra theta_crossed at 140 (coffee_break clears theta on the walk) re-confirms item_6. "
        "Measured (F47b, stop on): completes at 237 (prior off) / 239 (prior on) under both priors; "
        "scenario_20 with the stop on is refused at the table from tick 144 to the cap. Stop off: "
        "235 / 237 (scenario_20: 235 / 239). Earlier measurement with the waypoint (F47): "
    "stop on): identical to scenario_20 until tick 124 (the human's item_2 placement); the human "
    "walks off at 125, stands at (477, 399) on 149-179; the robot's item_6 delivery, refused from "
    "tick 144 to the cap in scenario_20, goes through and the run completes at 239 under both "
    "priors (prior-off keeps scenario_20's 2-tick stop at 57-58). Stop off: 237 / 239 (scenario_20: "
    "235 / 239). Reported next "
        "to scenario_20, not instead of it: 'stays at the place' and 'steps aside after its last task' "
        "are the two end-state conditions (design_decisions.md, 'After C'; TODO-47 (d)). The walk to "
        "the machine (bearing 0 deg from the table) is >= 51 deg off every shelf, so no delivery "
        "hypothesis fits it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("coffee_machine_0")}),   # steps aside: a coffee break at the machine east of the table
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

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_51 = ScenarioConfig(
    id="scenario_51",
    name="layout5_change_of_mind_before_pickup",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "One table, so no wrong destination: human walks to item_2, turns without picking it up, delivers item_3."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=[
                *abandon(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                    before="pick_up",
                ),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
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

scenario_52 = ScenarioConfig(
    id="scenario_52",
    name="layout5_landmark_stay_mid_carry",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human picks up item_3, walks to corner_NW with it and stays 30 ticks, finishes the delivery, then delivers item_2."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=[
                *interrupt(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                    after="pick_up",
                    with_=[MoveTo("corner_NW"), Stay(30)],
                ),
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

scenario_53 = ScenarioConfig(
    id="scenario_53",
    name="layout5_table_stay_after_delivery",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human delivers item_3 and item_2, stays 40 ticks at the table, then takes a coffee break."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                Stay(40),
                TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("coffee_machine_0")}),
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
# manually defined scenarios, for only "env_layout7" (mid-run stay with a real coffee machine, F47b).
# ===============================================================
_F47B_DESCRIPTION = (
    "Mid-run stay fixture (F47b), for D2's evaluation; builds no D2 mechanism; every scheduled task "
    "well typed. The robot starts 50 cm south of the table and its cheapest task is item_1 at "
    "shelf_1, 800 cm due south along x = 0. coffee_machine_0 stands ON that route at (0, -550) with "
    "the human's shelf_5 beside it (100 cm west). The human walks in from (510, -550) along the "
    "aisle, takes a coffee break at the machine (the schema's PT60S, 30 ticks), delivers item_5 from "
    "the shelf beside it, then switches on the AC by the east wall and stays there. The natural "
    "configuration, not tuned for the recognizer: whether the stay's hypothesis is admitted before the robot "
    "reaches it, and so absorbed by realization, is what the fixture measures. MEASURED (F47b; cost "
    "realized, gate none, stop off and on, both priors, PYTHONHASHSEED=0; analysis/f47_fixtures/): "
    "coffee_break crosses theta at tick 23 (0.796 prior-off, 0.897 prior-on), two ticks before the "
    "human stands at (30, -550) on 25-55, and B3 re-decides on the projected 30-tick wait (T_h 34): "
    "no mid-run block occurs in either scenario. scenario_70 switches to item_2 (80.15 vs item_1 + "
    "hold 32 = 89), returns to item_1 at 105 after the human has left, completes at 187, no [stop]. "
    "scenario_71 holds 32 ticks at (0, -40) (item_1 + hold 89 vs item_3 118), walks, and meets the "
    "human LEAVING the machine: 3 refused steps at 57-59 past T_h, then completes at 207 (204 with "
    "the stop off). The finding for D2: with well-typed fixtures the stay's hypothesis is admitted before it "
    "begins and realization absorbs it as a switch or a hold; the separation stop, and so the "
    "blocked event, is exercised only past T_h, on the human's departure. THE ONE VARIABLE "
    "between scenario_70 and _71 is where the alternative shelf stands, at the SAME 900 cm from the "
    "table (identical task cost, identical t=0 choice): "
)
scenario_70 = ScenarioConfig(
    id="scenario_70",
    name="layout7_stay_alternative_beside",
    description=_F47B_DESCRIPTION + (
        "scenario_70 - shelf_2 BESIDE the blocked shelf (45 deg west of its bearing): switching from a "
        "block at (0, -500) to item_2 and returning adds ~13 ticks of walking over doing item_2 from "
        "the table later; the occupation would be LONG relative to the switch."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=[
                TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("coffee_machine_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=ac_activation, bindings={Var("?ac_switch"): Const("ac_switch_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_71 = ScenarioConfig(
    id="scenario_71",
    name="layout7_stay_alternative_across",
    description=_F47B_DESCRIPTION + (
        "scenario_71 - shelf_3 ACROSS the table (the opposite bearing): switching from a block at "
        "(0, -500) to item_3 and returning adds ~53 ticks of walking; the occupation would be SHORT "
        "relative to the switch."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=[
                TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("coffee_machine_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=ac_activation, bindings={Var("?ac_switch"): Const("ac_switch_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_72 = ScenarioConfig(
    id="scenario_72",
    name="layout7_coffee_stay_abandon",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human takes a coffee break with item_5 in hand, delivers it, stays 20 at the table, then picks up item_3 and abandons it (item_3 assigned to the human here, not in scenario_70)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=[
                *interrupt(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
                    after="pick_up",
                    with_=[TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("coffee_machine_0")})],
                ),
                Stay(20),
                *abandon(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                    after="pick_up",
                ),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_73 = ScenarioConfig(
    id="scenario_73",
    name="layout7_free_actions_then_delivery",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human walks to the door, stays 20, walks to corner_NW, then delivers item_5, its one assigned task."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=[
                MoveTo("door"),
                Stay(20),
                MoveTo("corner_NW"),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)


# ===============================================================
# manually defined scenarios, for only "env_layout8" (two kitting tables; T-B1b).
# scenario_80 / scenario_81 are the two-table fixture for B3.B: the cost
# argument and the baselines are in analysis/tb1b_two_tables/README.md.
# The robot's pool: item_6 and item_1 (short, beside kitting_table_0), item_4
# (far east, to kitting_table_0), item_7 (near the robot's start, to
# kitting_table_1). From the robot's start the cheapest single task is item_6,
# but the cheapest full ordering starts with item_7.
# ===============================================================
scenario_80 = ScenarioConfig(
    id="scenario_80",
    name="layout8_two_tables_plain_order",
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
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_0"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_0"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_81 = ScenarioConfig(
    id="scenario_81",
    name="layout8_two_tables_conflict_past_head",
    description=(
        "scenario_80 with the human starting further from item_0: its first task spans the robot's two "
        "short tasks and ends at kitting_table_0 as the second of them does, so the conflict falls in the "
        "second task of the ordering (item_6, item_1), not in its head."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-300, 200),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_0"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_0"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=["human_0"],
        ),
    ],
)

# scenario_83 (T-B1c): the existence case in which realized cost changes the
# HEAD under full_reorder — a conflict in an entry after the head, which the
# head realized alone cannot see. The robot's side is scenario_80's; only the
# human's differs. The human fetches item_3 first (a 66-tick walk along the
# north wall, then the carry to kitting_table_1) and then item_0, so that its
# carry of item_0 reaches kitting_table_0 while the robot, having delivered
# item_4 there, is on the second of its two short tasks: in the plain-cost
# ordering (item_6, item_1) the item_1 entry arrives at the table while the
# human stands there releasing item_0 (a 3-tick hold before that entry), in
# (item_1, item_6) the item_6 entry arrives after the human's projection ends.
# The start position sets that timing; the record is analysis/tb1c_realized_flip/.
scenario_83 = ScenarioConfig(
    id="scenario_83",
    name="layout8_two_tables_realized_flip",
    description=(
        "scenario_80 with the human working item_3 then item_0 from the north wall: its item_0 carry reaches "
        "kitting_table_0 as the second of the robot's two short tasks does, so under full_reorder the plain-cost "
        "ordering (item_6, item_1) carries a hold before item_1 and realized cost makes item_1 the head."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-430, 400),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_0"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_0"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=["human_0"],
        ),
    ],
)

# scenario_82 is for VIEWING env_layout8 (the Solara viewer), one task each:
# it is not a fixture, nothing is measured from it, and T-B does not use it.
scenario_82 = ScenarioConfig(
    id="scenario_82",
    name="layout8_view",
    description=(
        "Minimal scenario for opening env_layout8 in the viewer: one robot task and one human task. "
        "Not a fixture."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 400),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_0"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_0"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_84 = ScenarioConfig(
    id="scenario_84",
    name="layout8_change_of_mind_before_pickup",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human walks to item_3, turns without picking it up, delivers item_0."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 400),
            scheduled_tasks=[
                *abandon(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
                    before="pick_up",
                ),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_0"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_0"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_85 = ScenarioConfig(
    id="scenario_85",
    name="layout8_wrong_destination",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human delivers item_0 to kitting_table_1 instead of its table (kitting_table_0), then delivers item_3."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-600, 400),
            scheduled_tasks=[
                *deviate(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_0"), Var("?kitting_table"): Const("kitting_table_0")}),
                    destination="kitting_table_1",
                ),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_0"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, -400),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_7"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=["human_0"],
        ),
    ],
)


# ===============================================================
# manually defined scenario, for only "env_layout9" (two kitting tables against
# opposite walls; the realistic-placement variant of env_layout8).
# scenario_90 is for VIEWING env_layout9 and running it: it is NOT a measured
# fixture, nothing is measured from it, and T-B does not use it. The measured
# two-table fixture is scenario_80 / scenario_81 on env_layout8.
# ===============================================================
scenario_90 = ScenarioConfig(
    id="scenario_90",
    name="layout9_two_tables_at_the_walls",
    description=(
        "env_layout9: kitting_table_0 against the north wall, kitting_table_1 against the south wall. "
        "The robot's pool is item_5 / item_4 / item_1 (to kitting_table_1) and item_6 (to kitting_table_0); "
        "the human fetches item_2 to kitting_table_0 and item_3 to kitting_table_1. Not a fixture."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-850, 250),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_91 = ScenarioConfig(
    id="scenario_91",
    name="layout9_change_of_mind_before_pickup",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human walks to item_3, turns without picking it up, delivers item_2."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-850, 250),
            scheduled_tasks=[
                *abandon(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
                    before="pick_up",
                ),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_92 = ScenarioConfig(
    id="scenario_92",
    name="layout9_wrong_destination",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human delivers item_2 to kitting_table_1 instead of its table (kitting_table_0), then delivers item_3."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-850, 250),
            scheduled_tasks=[
                *deviate(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                    destination="kitting_table_1",
                ),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_93 = ScenarioConfig(
    id="scenario_93",
    name="layout9_landmark_stay_mid_carry",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human picks up item_2, walks to corner_NE with it and stays 30 ticks, finishes the delivery, then delivers item_3."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-850, 250),
            scheduled_tasks=[
                *interrupt(
                    TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                    after="pick_up",
                    with_=[MoveTo("corner_NE"), Stay(30)],
                ),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_94 = ScenarioConfig(
    id="scenario_94",
    name="layout9_table_stay_robot_converging",
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human delivers item_2 and item_3, stays 40 ticks at kitting_table_1 while the robot converges on it, then walks to corner_SE."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-850, 250),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
                Stay(40),
                MoveTo("corner_SE"),
            ],
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_1")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_1"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_4"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_1")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_6"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)
