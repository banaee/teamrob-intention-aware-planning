# domains/kitting/scenarios/scenarios_s12.py
"""
Kitting scenarios on env_setup_12 — the meta-planner test-bed (MPB; design_records.md, "The meta-planner test-bed
(MPB)"; analysis/mpb/), part (v): two of the five reachable decision paths the coverage matrix found without an instance
(analysis/mpb/coverage.md, rows D8 and C2; Hadi's rulings of 29 September 2026). One module per setup; the kitting call
form (domains/kitting/script.py).
The room is env_layout_14: env_layout_12's human side unchanged, plus shelf_11 and kitting_table_5 (cell D8) and
shelf_10 and kitting_table_6 (cell C2). The shift env_setup_12: env_setup_10's items (the human's item_1 on shelf_1 and
item_2 on shelf_2, to kitting_table_0; the robot's item_3 to item_6 on the NE shelves, to kitting_table_1; item_7 on
shelf_5, to kitting_table_3, the crossing), plus the robot's item_13 (shelf_11 -> kitting_table_5) and item_14
(shelf_10 -> kitting_table_6). Disjointness (MPB-3): the human's shelves 1 and 2 against the robot's shelves 4, 5, 7, 8,
9, 10 and 11. Every human script ends with the exit walk to corner_SE.
_01 the switch against an admitted projection (D8); _02 the hold against an admitted standing segment (C2).
"""

from shared.types import AgentConfig, ScenarioConfig, Script
from domains.kitting.script import deliver_item, coffee_break, go_to
from shared.types import Timeline
from domains.kitting.script import window
from domains.kitting.facts import BREAK_TIME, ROOM_WARM


_MPB = (
    "Meta-planner test-bed (MPB), env_layout_14, part (v): the recognition-to-planning chain with a working robot, "
    "against an oracle that states the expected decision (trigger and cause, gate, projection) before the run "
    "(analysis/mpb/). "
)
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


scenario_s301_01 = ScenarioConfig(
    id="scenario_s301_01",
    setup="env_setup_301",
    reference_layouts=["env_layout_14"],
    description= "stage 1 of slides",
    agents=[
        _robot((-300, 400), [
            deliver_item("item_1", table="kitting_table_0"),
            deliver_item("item_2", table="kitting_table_6"),
        ]),
    ],
)


