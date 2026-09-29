# domains/kitting/scenarios/scenarios_s11.py
"""
Kitting scenarios on env_setup_11 — the meta-planner test-bed (MPB; design_decisions.md, "The meta-planner test-bed
(MPB)"; analysis/mpb/), the fallback projection's scenarios. One module per setup; the kitting call form
(domains/kitting/script.py).
The room is env_layout_12; the shift env_setup_11 holds robot items only: item_8 (shelf_3 -> kitting_table_2) and
item_9 (shelf_6 -> kitting_table_4), the occupied target's pair; item_10 (shelf_4) and item_11 (shelf_7), both to
kitting_table_1, the NE route. The human has no assigned tasks (an authoring choice, stated per scenario): with the
prior on, coffee_break is the lone live hypothesis, refused throughout (unwarranted, then inadequate), so every
decision rests on the fallback projection. Disjointness (MPB-3) holds trivially: the human has no items.
_01 the occupied target with an alternative task (X1); _02 the fallback against a walker and a stander.
"""

from shared.types import AgentConfig, ScenarioConfig, Script
from domains.kitting.script import deliver_item, go_to, go_to_and_stand, stand


_MPB = (
    "Meta-planner test-bed (MPB), env_layout_12: the recognition-to-planning chain with a working robot, against an "
    "oracle that states the expected decision (trigger and cause, gate, projection) before the run (analysis/mpb/). "
    "The human has no assigned tasks (authoring choice): coffee_break is the lone live hypothesis and is refused "
    "throughout, so every decision rests on the fallback projection. "
)

scenario_s11_01 = ScenarioConfig(
    id="scenario_s11_01",
    setup="env_setup_11",
    reference_layouts=["env_layout_12"],
    description=_MPB + (
        "scenario_s11_01, MPB scenario 6, the occupied target with an alternative task (T-D X, X1): the human stands at "
        "kitting_table_2 from tick 0 (stand PT120S, unmodelled, declared here), then exits. The robot's pool: "
        "deliver_item(item_8) to kitting_table_2, the occupied table, and deliver_item(item_9) to kitting_table_4, 3.5 "
        "ticks dearer on plain cost at every point of the robot's walk north (the layout's path lengths, "
        "analysis/mpb/authoring.md). Authored to expose the switch by cost: under the fallback stand, which ends at "
        "1 + k ticks from the decision (k the observed standing count), item_8's hold is at most k + 1; the alternative "
        "is expected to win at the first expiry whose hold exceeds the cost difference (tick 14 by the authoring check, "
        "hold 7 > 3.5), before the robot carries item_8. After it the robot meets the occupied target with no "
        "alternative (holds lengthening, an evaluation observation)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-270, 620),
            scheduled_tasks=Script([
                stand("PT120S"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-420, 280),
            assigned_tasks=[
                deliver_item("item_8", table="kitting_table_2"),
                deliver_item("item_9", table="kitting_table_4"),
            ],
            observes=["human_0"],
        ),
    ],
)

scenario_s11_02 = ScenarioConfig(
    id="scenario_s11_02",
    setup="env_setup_11",
    reference_layouts=["env_layout_12"],
    description=_MPB + (
        "scenario_s11_02, MPB scenario 7, the fallback against a walker and a stander: the human walks straight north "
        "to door_N across the robot's route (y = 640, shelf_4 -> kitting_table_1), then walks to spot_E, 30 cm below "
        "that route, and stands there 30 ticks (go_to_and_stand PT60S, unmodelled, declared here), then exits. Authored "
        "to expose the expiry cadence of the fallback projection (a straight run of k ticks projects k ticks, a stand "
        "of k ticks k ticks, cut at the first fixed object's arrival radius), and a stand that ends before its "
        "projection: the re-decision ticks, the holds and the tick the persistence broke are recorded as evidence for "
        "TODO-132 (a), not verified. The robot delivers item_10 and item_11 to kitting_table_1."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(300, 260),
            scheduled_tasks=Script([
                go_to("door_N"),
                go_to_and_stand("spot_E", "PT60S"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-100, 600),
            assigned_tasks=[
                deliver_item("item_10", table="kitting_table_1"),
                deliver_item("item_11", table="kitting_table_1"),
            ],
            observes=["human_0"],
        ),
    ],
)
