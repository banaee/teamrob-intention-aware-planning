# domains/kitting/scenarios/scenarios_s12.py
"""
Kitting scenarios on env_setup_12 — the meta-planner test-bed (MPB; design_decisions.md, "The meta-planner test-bed
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


scenario_s12_01 = ScenarioConfig(
    id="scenario_s12_01",
    setup="env_setup_12",
    reference_layouts=["env_layout_14"],
    description=_MPB + (
        "scenario_s12_01, the switch against an admitted projection (coverage row D8): scenario_s10_02's human script and "
        "robot start; the robot's pool is item_7's crossing delivery (shelf_5 -> kitting_table_3, crossing the human's "
        "diagonal kitting_table_0 - shelf_1 at its midpoint) and item_13 (shelf_11 -> kitting_table_5), whose route stays "
        "clear of the human's first delivery and which is 2.5 ticks dearer on plain cost at the robot's position at the "
        "admission (an authored parameter, the midpoint of (0, hold), fixed before any run). Authored to expose the "
        "switch caused by the admitted projection: before the admission every decision rests on a fallback and selects "
        "item_7 (both tasks hold 0, item_7 cheaper); at the decision admitting deliver_item(item_1) (entered) item_7's "
        "carry through the crossing carries a hold above the difference and item_13 wins with hold 0, before item_7 is "
        "grasped. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 220),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=list(_TWO_DELIVERIES),
            observes=[],
        ),
        _robot((390, -573), [
            deliver_item("item_7", table="kitting_table_3"),
            deliver_item("item_13", table="kitting_table_5"),
        ]),
    ],
)

scenario_s12_02 = ScenarioConfig(
    id="scenario_s12_02",
    setup="env_setup_12",
    reference_layouts=["env_layout_14"],
    description=_MPB + (
        "scenario_s12_02, the hold against an admitted standing segment (coverage row C2): scenario_s10_04's human script "
        "(deliver item_1, a coffee break, deliver item_2, exit). The robot delivers item_3 in the NE area, then item_14, "
        "whose carry along y = -550 passes 30 cm from the human's waiting point at the coffee machine, inside the "
        "admitted coffee_break's wait. Authored to expose the hold against the admitted plan's stationary segment (the "
        "human's wait_at), not against a fallback stand: at the decision admitting coffee_break (entered) the robot's "
        "item_14 carries a positive hold. Declared property: that hold is positive; the robot comes within "
        "min_separation of the waiting point only after the human has left it; no F1 robot violation in the decision's "
        "assessed window. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 220),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=list(_TWO_DELIVERIES),
            observes=[],
        ),
        _robot((460, 480), [
            deliver_item("item_3", table="kitting_table_1"),
            deliver_item("item_14", table="kitting_table_6"),
        ]),
    ],
)
