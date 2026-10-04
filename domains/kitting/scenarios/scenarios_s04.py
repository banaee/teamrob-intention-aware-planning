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
# manually defined scenario, for only "env_layout_05".
# ===============================================================================
scenario_s04_01 = ScenarioConfig(
    id="scenario_s04_01",
    setup="env_setup_04",
    reference_layouts=["env_layout_05"],
    description=(
        "Foreseeable-task fixture (I1 follow-up; baseline for I3/I4). One human run in five "
        "script parts. (1) deliver item_3 from shelf_3 (-950, -50): 1209 cm approach from "
        "(100, 550), every other target >= 50 deg off the heading - the positive control. "
        "(2) coffee_break at coffee_machine_0 (-40, -250): scheduled, not assigned; from the "
        "kitting table the coffee bearing is >= 49.6 deg off every task target. (3) walk to the "
        "A/C switch ac_switch_1 (356, -210), an ac_activation instance (move_to + a one-tick "
        "wait_at); it lies on the straight line from the coffee machine to shelf_6, so the human "
        "first heads toward a shelf it will deliver from later. (4) deliver item_6 from shelf_6 "
        "(950, -150), so the assigned pool is exactly the deliveries; shelf_5 (robot, undelivered "
        "then) is 17 deg off this last approach - a prior-off decoy, inadmissible prior-on. "
        "(5) the exit walk to corner_SE (docs/assumptions.md 1.1; added in Track 2.5: the terminal "
        "stand is not this fixture's purpose). Robot: item_4, item_7, item_5 from a SW start, "
        "complete at tick 379 prior on and 392 prior off (the world tick). The human's script ends "
        "at tick 369, when the exit walk completes. Run with --steps 400. "
        "Baselines: analysis/kitting/tb1a_destination/. "
        "One A/C switch since 4 October 2026 (T-K part 1, AM18, AM19): the layout's ac_switch_0 "
        "(never visited) and ac_switch_2 (the second walk of part 3, a turn away from every delivery "
        "target) were removed with that walk; the earlier records (analysis/kitting/ before that "
        "date, F47b's retyping of the waypoints wander_0 / wander_1 among them) describe three "
        "A/C switches and two activations."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(100, 550),
            scheduled_tasks=Script([
                deliver_item("item_3", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                ac_activation("ac_switch_1"),   # script part 3: toward shelf_6 (an AC switch since F47b; was the waypoint wander_0)
                deliver_item("item_6", table="kitting_table_0"),
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

# T-C2c play: script examples in the author form, not measured fixtures (analysis/tc2c_scripts/play.md).
# Convention for NEW scripts (23 Sept 2026): end with the human leaving (door or a corner); these predate it.
# The robot side is the layout's base scenario's.
scenario_s04_02 = ScenarioConfig(
    id="scenario_s04_02",
    setup="env_setup_04",
    reference_layouts=["env_layout_05"],
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
scenario_s04_03 = ScenarioConfig(
    id="scenario_s04_03",
    setup="env_setup_04",
    reference_layouts=["env_layout_05"],
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

