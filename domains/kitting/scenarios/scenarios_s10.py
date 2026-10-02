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


scenario_s10_01 = ScenarioConfig(
    id="scenario_s10_01",
    setup="env_setup_10",
    reference_layouts=["env_layout_12"],
    description=_MPB + (
        "scenario_s10_01, MPB scenario 1, admission after theta: the human delivers item_1 and item_2 (assigned, never "
        "in an order), then exits; the first walk discriminates. Authored to expose the admission on the tick the gate "
        "first clears, through recognition_changed with cause entered (D2), for each delivery; the robot works its NE "
        "pool, away from the human, started so that none of its task completions coincides with those ticks. Modelled "
        "behaviour only, besides the exit walk."
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
        _robot((460, 480), _NE_POOL),
    ],
)

scenario_s10_02 = ScenarioConfig(
    id="scenario_s10_02",
    setup="env_setup_10",
    reference_layouts=["env_layout_12"],
    description=_MPB + (
        "scenario_s10_02, MPB scenario 2, the hold against an admitted projection: the human's script is "
        "scenario_s10_01's; the robot's one task carries item_7 from shelf_5 to kitting_table_3 along the perpendicular "
        "bisector of the human's diagonal kitting_table_0 - shelf_1, crossing it at its midpoint (-210, 0), and the robot "
        "starts where its planned passage of that point coincides with the human's carry back from shelf_1 (authoring "
        "check: both between ticks 44 and 45). Authored to expose the hold: at the decision that admits "
        "deliver_item(item_1) (entered), the admitted plan crosses the robot's route and the robot's task carries a "
        "hold. Declared property: that hold is positive, and no F1 robot violation occurs within the decision's "
        "assessed window. Modelled behaviour only, besides the exit walk."
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
        _robot((390, -573), [deliver_item("item_7", table="kitting_table_3")]),
    ],
)

scenario_s10_03 = ScenarioConfig(
    id="scenario_s10_03",
    setup="env_setup_10",
    reference_layouts=["env_layout_12"],
    description=_MPB + (
        "scenario_s10_03, MPB scenario 3, the planning side of the mid-action change (scenario_s09_13's script on this "
        "room): coffee_break cut into the carry of item_1 mid-walk (PT28S, 14 of the carry's 28 steps), the break, the "
        "resumed delivery, deliver item_2, exit. Authored to expose the chain: the admitted delivery retracted when its "
        "carry phase turns inadequate (recognition_changed, cause retraction), the fallback projection and its expiry, "
        "and re-admission at the next fitting phase (coffee_break at its advance to wait_at, cause entered). The robot "
        "works its NE pool from (-250, 560), a start the pre-run timing check chose so that none of its task "
        "completions falls within 3 ticks of that chain (analysis/mpb/authoring.md). Modelled behaviour only, besides "
        "the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 220),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").during(
                    move_to, "PT28S", coffee_break("coffee_machine_0"), occurrence=1),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=list(_TWO_DELIVERIES),
            observes=[],
        ),
        _robot((-250, 560), _NE_POOL),
    ],
)

scenario_s10_04 = ScenarioConfig(
    id="scenario_s10_04",
    setup="env_setup_10",
    reference_layouts=["env_layout_12"],
    description=_MPB + (
        "scenario_s10_04, MPB scenario 4, boundary re-admission on commitment (scenario_s09_02's script on this room): "
        "deliver item_1, coffee_break, deliver item_2, exit. Authored to expose the coffee break's own boundary b with "
        "one delivery left: coffee_break is retired while waited holds, so deliver_item(item_2) is the single live "
        "hypothesis at b + 1. At b the recorded hypothesis (coffee_break) is pinned and most_likely changes, so "
        "recognition_changed fires with cause replaced (boundary stays a possible cause when the recorded hypothesis "
        "remains the leader) and admission refuses (no observation on a boundary tick); at b + 1 deliver_item(item_2) is "
        "admitted on commitment warrant (cause entered). The robot works its NE pool. Modelled behaviour only, besides "
        "the exit walk."
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
        _robot((460, 480), _NE_POOL),
    ],
)

scenario_s10_05 = ScenarioConfig(
    id="scenario_s10_05",
    setup="env_setup_10",
    reference_layouts=["env_layout_12"],
    description=_MPB + (
        "scenario_s10_05, MPB scenario 5, the lone foreseeable hypothesis after the assigned tasks: deliver item_1, "
        "deliver item_2, a ten-tick stand at the table (stand PT10S, unmodelled, declared here), coffee_break, exit. At "
        "the last delivery's boundary the recorded delivery is pinned and most_likely changes (cause replaced; boundary "
        "stays a possible cause when the recorded hypothesis remains the leader), and coffee_break is then the lone live "
        "hypothesis. The stand is authored so that a decision (the fallback's expiry) falls on standing: there "
        "coffee_break is refused unwarranted (none(leader_unwarranted)); on the first step toward the machine it is "
        "warranted and admitted through recognition_changed with cause entered. The robot works its NE pool."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 220),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                stand("PT10S"),
                coffee_break("coffee_machine_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=list(_TWO_DELIVERIES),
            observes=[],
        ),
        _robot((460, 480), _NE_POOL),
    ],
)

scenario_s10_06 = ScenarioConfig(
    id="scenario_s10_06",
    setup="env_setup_10",
    reference_layouts=["env_layout_12"],
    description=_MPB + (
        "scenario_s10_06, MPB scenario 8, the control: the human delivers item_2 only (assigned; the east shelf) and "
        "exits, working away from every robot route (every human path, admitted plan and fallback segment at least "
        "280 cm from the robot's NE routes, analysis/mpb/authoring.md). Declared properties: no hold at any decision, "
        "and the robot's completion (and its per-tick positions) identical to the reference run, the same setup and "
        "robot run without the human (analysis/mpb/reference.py; a reference run, not a scenario). Modelled behaviour "
        "only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 220),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[deliver_item("item_2", table="kitting_table_0")],
            observes=[],
        ),
        _robot((460, 480), _NE_POOL),
    ],
)

scenario_s10_07 = ScenarioConfig(
    id="scenario_s10_07",
    setup="env_setup_10",
    reference_layouts=["env_layout_12"],
    description=_MPB + (
        "scenario_s10_07, the sudden stand mid-carry (MPB part (iv), coverage): a stand of 60 ticks (stand PT120S, "
        "unmodelled, declared here) cut into the carry of item_1 mid-walk (PT28S, 14 of the carry's 28 steps, as "
        "scenario_s09_13 cuts it), then the carry resumed, deliver item_2, exit. Authored to expose: the admitted "
        "delivery retracted about 17 standing ticks into the stand (s_exp = 0 for the walk; recognition_changed, cause "
        "retraction), a standing fallback doubling at each expiry, the resumed walk as a moving fallback, no "
        "re-admission of the delivery before its place (within a phase D cannot fall; T-D L, L2), then the boundary "
        "at the place and item_2's admission on commitment. The stand's length is derived so that one expiry falls "
        "within the stand and the next within the resumed walk (analysis/mpb/authoring.md, part (iv))."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 220),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").during(
                    move_to, "PT28S", stand("PT120S"), occurrence=1),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=list(_TWO_DELIVERIES),
            observes=[],
        ),
        _robot((460, 480), _NE_POOL),
    ],
)

scenario_s10_08 = ScenarioConfig(
    id="scenario_s10_08",
    setup="env_setup_10",
    reference_layouts=["env_layout_12"],
    description=_MPB + (
        "scenario_s10_08, the change of mind between assigned tasks (MPB part (iv), coverage; scenario_s09_07's "
        "script on this room): the human picks up item_1 and changes to deliver_item(item_2), returning item_1 to "
        "shelf_1 first (deliver_with_return), then delivers item_2 and item_1, exit. Authored to expose: no "
        "retraction; at the return's place (a terminal place, a boundary: T-D L, L1) the recorded delivery of item_1 is "
        "no longer the leader, which after the boundary is coffee_break on the prior's tie order, so "
        "recognition_changed fires with cause replaced and admission refuses (below theta, a fallback); item_2 is then "
        "admitted when it clears theta (entered, commitment and observation). The human's change from delivery 1 to "
        "delivery 2 passes through the coffee hypothesis in the recognizer's chain. The robot starts at (-165, 490), the "
        "start the pre-run timing check chose for both strategies (analysis/mpb/authoring.md, part (iv)). Modelled "
        "behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 220),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(
                    pick_up, deliver_item("item_2", table="kitting_table_0")),
                go_to("corner_SE"),
            ]),
            assigned_tasks=list(_TWO_DELIVERIES),
            observes=[],
        ),
        _robot((-165, 490), _NE_POOL),
    ],
)

scenario_s10_09 = ScenarioConfig(
    id="scenario_s10_09",
    setup="env_setup_10",
    reference_layouts=["env_layout_12"],
    description=_MPB + (
        "scenario_s10_09, the misdelivery (MPB part (iv), coverage; scenario_s09_08's script on this room): item_1 "
        "delivered to kitting_table_2 (a departure from its designated kitting_table_0; the robot does not use that "
        "table here), then deliver item_2, exit. Authored to expose: the admitted delivery retracted as its carry "
        "heads away from kitting_table_0 (cause retraction), the fallback, no re-admission (the delivery's terminal "
        "fact never holds); and the unexplained interval before the place at the wrong table, chosen for its length "
        "(analysis/mpb/authoring.md, part (iv)), which exposes X5's ground (1) (the finding unexplained and outliving at "
        "least one re-decision), measured from the run, not a mechanism."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 220),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_2"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=list(_TWO_DELIVERIES),
            observes=[],
        ),
        _robot((460, 480), _NE_POOL),
    ],
)

scenario_s10_10 = ScenarioConfig(
    id="scenario_s10_10",
    setup="env_setup_10",
    reference_layouts=["env_layout_12"],
    description=_MPB + (
        "scenario_s10_10, a record kept through a dip below theta (MPB part (v), coverage row E6; D2's retention by "
        "identity): scenario_s09_04's script on this room (the IR test-bed's coffee before the pick-up): coffee_break "
        "started at the boundary after item_1's first walk, empty-handed at shelf_1, then deliver item_2, exit. Modelled "
        "behaviour only, besides the exit walk. Authored to expose the retention: after deliver_item(item_1) is admitted "
        "(entered), the human's walk toward the machine lowers its share below theta while it stays the leader and "
        "adequate, so no trigger fires and the decision record keeps it through the dip, until coffee_break overtakes "
        "(replaced). The robot works its NE pool, started so that none of its decisions falls between the admission and "
        "the end of the dip (analysis/mpb/authoring.md, part (v))."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 220),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(
                    move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=list(_TWO_DELIVERIES),
            observes=[],
        ),
        _robot((-250, 480), _NE_POOL),
    ],
)

scenario_s10_11 = ScenarioConfig(
    id="scenario_s10_11",
    setup="env_setup_10",
    reference_layouts=["env_layout_13"],
    description=_MPB + (
        "scenario_s10_11, the cause boundary (MPB part (v), coverage row A4), on env_layout_13, env_layout_12 without the "
        "coffee machine: with no coffee_break hypothesis the live set is the two assigned deliveries. The human delivers "
        "item_1 to kitting_table_3 (a departure from its designated kitting_table_0; the robot does not use that table "
        "here), then item_2, then exits. Authored to expose recognition_changed with cause boundary: the admitted "
        "deliver_item(item_1) stays adequate up to the place at the wrong table (margin read from the oracle's table "
        "before any run), the place is a terminal action and ends the episode (T-D L, L1) without item_1's terminal fact, "
        "so item_1 stays live, and after the reset to the prior it is the first live hypothesis in the recognizer's order "
        "and remains the leader. The robot works its NE pool, started so that no decision of its own clears the record "
        "before the place."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 220),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_3"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=list(_TWO_DELIVERIES),
            observes=[],
        ),
        _robot((460, 480), _NE_POOL),
    ],
)
