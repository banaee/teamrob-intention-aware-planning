"""
analysis/f47_fixtures/retired_scenarios_60_61.py — RECORD ONLY, not registered, not importable by the
registry. scenario_60 / scenario_61 (F47) bound coffee_break's ?coffee_machine to wander_0, a waypoint:
an ill-typed task instance (a coffee break in a world with no coffee machine) that ran only because
scheduled bindings were not type-checked. Since F47b `check_task_bindings()` (shared/types.py) refuses it
at spawn. The definitions are kept here as they were, with their measured descriptions, for the record;
env_layout6.json stays in domains/kitting/, unregistered. See README.md.
"""
from shared.types import TaskInstance, AgentConfig, ScenarioConfig, Var, Const
from domains.kitting.tasks import deliver_item, coffee_break

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
