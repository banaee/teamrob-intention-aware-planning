# domains/kitting/scenarios/scenarios_s10.py
"""
Kitting scenarios on env_setup_10 — the meta-planner test-bed (MPB; design_records.md, "The meta-planner test-bed
(MPB)"; analysis/mpb/). One module per setup. Every task instance is written in the kitting call form
(domains/kitting/script.py), a human's script as a Script of task instances with events (T-H).
The room is env_layout_12 (the 10/11 pattern translated by (0, -200), plus the robot's work areas); the shift
env_setup_10: the human's item_1 (shelf_1) and item_2 (shelf_2), both designated to kitting_table_0; the robot's
item_3 to item_6 on the NE shelves (shelf_4, shelf_7, shelf_8, shelf_9), designated to kitting_table_1; the robot's
item_7 on shelf_5, designated to kitting_table_3 (the crossing). The robot works (its own pool) and observes the human;
each scenario is authored to expose one decision of the recognition-to-planning chain, stated in its description; the
oracle states the expected decision before the run (analysis/mpb/). Prior ON in the primary set (configs/mpb/).
Disjointness (MPB-3): in every scenario the robot's items and shelves are disjoint from the human's.
Every human script ends with the exit walk to corner_SE. The coffee break's duration is the schema's.
_01 admission after theta; _02 the hold against an admitted projection; _03 the planning side of the mid-action change;
_04 boundary re-admission on commitment; _05 the lone foreseeable hypothesis after the assigned tasks; _06 the control.
Added in MPB part (iv) for coverage (Hadi, 29 September 2026; a coverage gap found in review, not a failed run): _07 the
sudden stand mid-carry; _08 the change of mind between assigned tasks; _09 the misdelivery.
Added in MPB part (v) for coverage (Hadi, 29 September 2026; analysis/mpb/coverage.md, rows E6 and A4): _10 a record
kept through a dip below theta; _11 the cause boundary, on env_layout_13 (env_layout_12 without the coffee machine).
"""

from shared.types import AgentConfig, ScenarioConfig, Script
from domains.kitting.actions import move_to, pick_up
from domains.kitting.script import deliver_item, coffee_break, go_to, stand
from shared.types import Timeline
from domains.kitting.script import window
from domains.kitting.facts import BREAK_TIME, ROOM_WARM


# ===============================================================
# the meta-planner test-bed, on "env_layout_12" (analysis/mpb/)
# ===============================================================
_MPB = (
    "Meta-planner test-bed (MPB), env_layout_12: the recognition-to-planning chain with a working robot, against an "
    "oracle that states the expected decision (trigger and cause, gate, projection) before the run (analysis/mpb/). "
)
_NE_POOL = [
    deliver_item("item_3", table="kitting_table_1"),
    deliver_item("item_4", table="kitting_table_1"),
    deliver_item("item_5", table="kitting_table_1"),
    deliver_item("item_6", table="kitting_table_1"),
]
_TWO_DELIVERIES = [
    deliver_item("item_1", table="kitting_table_0"),
    deliver_item("item_2", table="kitting_table_0"),
]


def _robot(start, pool):
    return AgentConfig(
        agent_id="robot_0",
        agent_type="robot",
        start_position=start,
        assigned_tasks=list(pool),
        observes=["human_0"],
    )




scenario_s302_02 = ScenarioConfig(
    id="scenario_s302_02",
    setup="env_setup_302",
    reference_layouts=["env_layout_12"],
    description= "stage2 of slides",
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-240, 220),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0"),
            ]),
            assigned_tasks=list(_TWO_DELIVERIES),
            observes=[],
        ),
        _robot((390, 160), [deliver_item("item_7", table="kitting_table_3")]),
    ],
)
