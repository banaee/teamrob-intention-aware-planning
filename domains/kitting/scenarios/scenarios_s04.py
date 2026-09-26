# domains/kitting/scenarios/scenarios_s04.py
"""
Kitting scenarios on env_setup_04 — the scenarios of the old env_setup4.
One module per setup; scenario ids keep their old form until stage 3.
Every task instance is written in the kitting call form (domains/kitting/script.py),
a human's script as a Script of task instances with events (T-H; migrated in T-H3):
an event's anchor is an action schema of the task's decomposition.
A task's class (WorkTask, PersonalTask, HumanOnlyTask) is declared in tasks.py — not repeated here.
"""

from shared.types import AgentConfig, ScenarioConfig, Script, drop
from domains.kitting.actions import pick_up
from domains.kitting.script import deliver_item, coffee_break, ac_activation, go_to, stand


# ===============================================================================
# manually defined scenario, for only "env_layout4".
# ===============================================================================
scenario_40 = ScenarioConfig(
    id="scenario_40",
    setup="env_setup_04",
    reference_layouts=["env_layout4"],
    description=(
        "Foreseeable-task fixture (I1 follow-up; baseline for I3/I4). One human run in four "
        "script parts. (1) deliver item_3 from shelf_3 (-950, -50): 1209 cm approach from "
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
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_1"),   # script part 3, walk 1: toward shelf_6 (an AC switch since F47b; was the waypoint wander_0)
                ac_activation("ac_switch_2"),   # script part 3, walk 2: turn away
                deliver_item("item_6", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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
    setup="env_setup_04",
    reference_layouts=["env_layout4"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human takes a coffee break with item_3 in hand, delivers it, stays 20 at the table, then picks up item_6 and abandons it."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                stand("PT40S"),
                deliver_item("item_6", table="kitting_table_0").at(pick_up, drop),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
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
    setup="env_setup_04",
    reference_layouts=["env_layout4"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human delivers item_3, then picks up item_6, abandons it and walks to corner_SE holding it, where it stands."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0").at(pick_up, drop),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_6", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-950, -550),
            assigned_tasks=[
                deliver_item("item_4", table="kitting_table_0"),
                deliver_item("item_7", table="kitting_table_0"),
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

