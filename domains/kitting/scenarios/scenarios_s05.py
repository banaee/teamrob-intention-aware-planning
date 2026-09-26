# domains/kitting/scenarios/scenarios_s05.py
"""
Kitting scenarios on env_setup_05 — the scenarios of the old env_setup7.
One module per setup; scenario ids keep their old form until stage 3.
Every task instance is written in the kitting call form (domains/kitting/script.py),
a human's script as a Script of task instances with events (T-H; migrated in T-H3):
an event's anchor is an action schema of the task's decomposition.
A task's class (WorkTask, PersonalTask, HumanOnlyTask) is declared in tasks.py — not repeated here.
"""

from shared.types import AgentConfig, ScenarioConfig, Script, drop
from domains.kitting.actions import pick_up
from domains.kitting.script import deliver_item, coffee_break, ac_activation, go_to, stand


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
    setup="env_setup_05",
    reference_layouts=["env_layout7"],
    description=_F47B_DESCRIPTION + (
        "scenario_70 - shelf_2 BESIDE the blocked shelf (45 deg west of its bearing): switching from a "
        "block at (0, -500) to item_2 and returning adds ~13 ticks of walking over doing item_2 from "
        "the table later; the occupation would be LONG relative to the switch."
        " Purpose (label C, docs/glossary.md §7): the script ends at the AC switch "
        "(ac_activation completes), then no task on the stack to the end of the run."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_71 = ScenarioConfig(
    id="scenario_71",
    setup="env_setup_05",
    reference_layouts=["env_layout7"],
    description=_F47B_DESCRIPTION + (
        "scenario_71 - shelf_3 ACROSS the table (the opposite bearing): switching from a block at "
        "(0, -500) to item_3 and returning adds ~53 ticks of walking; the occupation would be SHORT "
        "relative to the switch."
        " Purpose (label C, docs/glossary.md §7): the script ends at the AC switch "
        "(ac_activation completes), then no task on the stack to the end of the run."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=Script([
                coffee_break("coffee_machine_0"),
                deliver_item("item_5", table="kitting_table_0"),
                ac_activation("ac_switch_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
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
    setup="env_setup_05",
    reference_layouts=["env_layout7"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human takes a coffee break with item_5 in hand, delivers it, stays 20 at the table, then picks up item_3 and abandons it (item_3 assigned to the human here, not in scenario_70)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=Script([
                deliver_item("item_5", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                stand("PT40S"),
                deliver_item("item_3", table="kitting_table_0").at(pick_up, drop),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

# Script example (T-C2c play), not a measured fixture.
scenario_73 = ScenarioConfig(
    id="scenario_73",
    setup="env_setup_05",
    reference_layouts=["env_layout7"],
    description=(
        "Script example (T-C2c play), not a measured fixture: nothing is recorded from it. "
        "Human walks to the door, stays 20, walks to corner_NW, then delivers item_5, its one assigned task."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(510, -550),
            scheduled_tasks=Script([
                go_to("door"),
                stand("PT40S"),
                go_to("corner_NW"),
                deliver_item("item_5", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_5", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, 0),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=["human_0"],
        ),
    ],
)

