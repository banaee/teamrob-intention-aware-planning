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
        "'waypoint' objects no task enumerates: wander_0 (356, -210) lies on the straight line "
        "from the coffee machine to shelf_6, so the human first heads toward a shelf it will "
        "deliver from later; wander_1 (230, -550) is >= 64 deg off every target seen from "
        "wander_0, so the turn is a retraction case. The two walks are scripted as "
        "ac_activation instances bound to the waypoints (move_to + a one-tick wait_at): the "
        "schema only supplies the walk; ac_activation's own hypothesis is bound to "
        "ac_switch_0, which is never visited. (4) deliver item_6 from shelf_6 (950, -150), so "
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
                TaskInstance(schema=ac_activation, bindings={Var("?ac_switch"): Const("wander_0")}),   # segment 3, leg 1: toward shelf_6
                TaskInstance(schema=ac_activation, bindings={Var("?ac_switch"): Const("wander_1")}),   # segment 3, leg 2: turn away
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

# ===============================================================
# manually defined scenarios, for only "env_layout5" (env_layout2 + rest_0).
# ===============================================================
scenario_50 = ScenarioConfig(
    id="scenario_50",
    name="layout5_end_state_steps_aside",
    description=(
        "End-state variant of scenario_20 (F47). Identical to scenario_20 in every task, position and "
        "pool; the one change is a third human task after its last delivery: coffee_break bound to "
        "rest_0, a waypoint 500 cm east of the table (env_layout5 = env_layout2 + rest_0). The human "
        "leaves the table for rest_0 instead of idling at it, stands there for the schema's PT60S and "
        "then idles THERE, so the robot's remaining table deliveries meet a free table. Measured (F47, "
    "stop on): identical to scenario_20 until tick 124 (the human's item_2 placement); the human "
    "walks off at 125, stands at (477, 399) on 149-179; the robot's item_6 delivery, refused from "
    "tick 144 to the cap in scenario_20, goes through and the run completes at 239 under both "
    "priors (prior-off keeps scenario_20's 2-tick stop at 57-58). Stop off: 237 / 239 (scenario_20: "
    "235 / 239). Reported next "
        "to scenario_20, not instead of it: 'stays at the place' and 'steps aside after its last task' "
        "are the two end-state conditions (design_decisions.md, 'After C'; TODO-47 (d)). The walk to "
        "rest_0 (bearing 0 deg from the table) is >= 51 deg off every shelf, so no delivery hypothesis "
        "fits it; 'waypoint' is enumerated by no task, as in scenario_40. No coffee machine on the "
        "layout: the schema supplies the walk and the stand, the entity is the waypoint."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(200, 50),
            scheduled_tasks=[
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_2"), Var("?kitting_table"): Const("kitting_table_0")}),
                TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("rest_0")}),   # steps aside; the schema only supplies the walk and the stand
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
# manually defined scenarios, for only "env_layout6" (mid-run blocking, F47).
# ===============================================================
_F47_DESCRIPTION = (
    "Mid-run blocking fixture (F47), for D2's evaluation; builds no D2 mechanism. The robot starts "
    "50 cm south of the table and its cheapest task is item_1 at shelf_1, 800 cm due south along "
    "x = 0. The human, assigned item_5 at shelf_5 (west end of the aisle y = -550), walks in from "
    "(510, -550) toward that shelf and STOPS on the robot's route at wander_0 (0, -550) for a "
    "coffee_break - the schema's PT60S, 30 ticks; no coffee machine exists, so no hypothesis "
    "explains the stop - then walks east to wander_1, rests there for another PT60S, and only then "
    "delivers item_5 (leaving the rest spot at ~124, reaching the table at ~241, after the robot's "
    "last placement at ~206 in the current runs; a slower policy would meet it idle at the table). "
    "Measured (F47; 20 cm/tick, arrival radius 30, min_separation 50, cost realized, gate none, "
    "stop on, PYTHONHASHSEED=0, 300 steps): the human stands at (30, -550) on ticks 25-55 and moves "
    "at 58; the robot's step south from (0, -500) is refused on ticks 25-56 prior-off (32 ticks) "
    "and 27-56 prior-on (30 ticks) - on its FIRST task, item_1, with the alternative still in the "
    "pool; then it completes at 203 (scenario_60) / 204 (scenario_61). Prior-on the recognizer has "
    "one admissible task and puts 0.906 on deliver_item(item_5) at tick 0 before the human has "
    "moved, so a projection is built at t=0 (T_h 109.5), the robot holds 2 ticks against the "
    "projected walk crossing its route, and the stop is labelled inside the window - the human "
    "deviated from its projected delivery. Prior-off shelf_2 (2 deg), shelf_5 (0 deg) and shelf_1 "
    "(21 deg) share the belief below theta and nothing is projected (outside(no_projection)). With "
    "the stop off the robot walks through the standing human twice (approach 25-27, carry back "
    "44-46; 6 violating steps) and completes at 171-174. Control, not a fixture: the same layout "
    "with a coffee machine at wander_0's position and the break bound to it (the occupation "
    "modelled) produces no stop at all - the crossing at tick 23 makes B3 switch to the alternative "
    "in the beside variant (item_2 80.15 vs item_1 + hold 32 = 89; done 185) and hold 32 ticks in "
    "the across variant (done 204 / 209): a foreseen occupation is absorbed by planning; D2's event "
    "arises only from an occupation the projection does not carry. THE ONE VARIABLE between "
    "scenario_60 and _61 is where the "
    "alternative shelf stands, at the SAME 900 cm from the table (identical task cost, identical "
    "t=0 choice): "
)
scenario_60 = ScenarioConfig(
    id="scenario_60",
    name="layout6_block_alternative_beside",
    description=_F47_DESCRIPTION + (
        "scenario_60 - shelf_2 BESIDE the blocked shelf (45 deg west of its bearing). Switching from "
        "the block point to item_2 and returning adds ~13 ticks of walking over doing item_2 from the "
        "table later, against ~32 ticks of remaining occupation: the occupation is LONG relative to "
        "the switch. Favours neither policy by construction: the occupation is the schema's and the "
        "alternative's own cost is the same as in scenario_61; only the geometry differs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=[
                TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("wander_0")}),   # stops on the robot's route; the schema supplies the walk and the PT60S stand
                TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("wander_1")}),   # steps aside and rests
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_5"), Var("?kitting_table"): Const("kitting_table_0")}),   # the assigned delivery, last: after the robot is done in the current runs
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

scenario_61 = ScenarioConfig(
    id="scenario_61",
    name="layout6_block_alternative_across",
    description=_F47_DESCRIPTION + (
        "scenario_61 - shelf_3 ACROSS the table (the opposite bearing). Switching from the block point "
        "to item_3 and returning adds ~53 ticks of walking (the robot passes the table twice more), "
        "against ~32 ticks of remaining occupation: the occupation is SHORT relative to the switch. "
        "Favours neither policy by construction, as scenario_60."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=[
                TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("wander_0")}),
                TaskInstance(schema=coffee_break, bindings={Var("?coffee_machine"): Const("wander_1")}),
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
                TaskInstance(schema=deliver_item, bindings={Var("?item"): Const("item_3"), Var("?kitting_table"): Const("kitting_table_0")}),
            ],
            observes=["human_0"],
        ),
    ],
)
