# domains/kitting/scenarios/scenarios_s11.py
"""
Kitting scenarios on env_setup_11 — the meta-planner test-bed (MPB; design_records.md, "The meta-planner test-bed
(MPB)"; analysis/mpb/), the fallback projection's scenarios. One module per setup; the kitting call form
(domains/kitting/script.py).
The room is env_layout_12; the shift env_setup_11: the robot's item_8 (shelf_3 -> kitting_table_2) and item_9
(shelf_6 -> kitting_table_4), the occupied target's pair; item_10 (shelf_4) and item_11 (shelf_7), both to
kitting_table_1, the NE route; and the human's item_12 (shelf_1 -> kitting_table_0).
The human is assigned deliver_item(item_12) and never performs it (re-authored in MPB part (iv), Hadi's ruling of 29
September 2026, from the first authoring's human with no assigned tasks, whose empty assignment switched the support
restriction off: shared/io_contracts.md §2.1). This is a different in-scope case, not "no assigned work": an assigned task
the human does not execute, carrying commitment warrant. With the restriction on, the live set is that delivery and
coffee_break; neither reaches theta while adequate (analysis/mpb/authoring.md, part (iv)), so every decision rests on the
fallback projection. Disjointness (MPB-3): the human's item_12 (shelf_1) against the robot's items 8 to 11 (shelves 3,
6, 4, 7).
_01 the occupied target with an alternative task (X1); _02 the fallback against a walker and a stander.
Added in MPB part (v) for coverage (Hadi, 29 September 2026; analysis/mpb/coverage.md, row D9): _03 the switch while
carrying.
"""

from shared.types import AgentConfig, ScenarioConfig, Script
from domains.kitting.script import deliver_item, go_to, go_to_and_stand, stand
from shared.types import Timeline
from domains.kitting.script import window
from domains.kitting.facts import BREAK_TIME, ROOM_WARM

# The human's assigned delivery, never performed (commitment warrant, never admitted: authoring.md, part (iv)).
_UNPERFORMED = [deliver_item("item_12", table="kitting_table_0")]


_MPB = (
    "Meta-planner test-bed (MPB), env_layout_12: the recognition-to-planning chain with a working robot, against an "
    "oracle that states the expected decision (trigger and cause, gate, projection) before the run (analysis/mpb/). "
    "The human is assigned deliver_item(item_12) and never performs it (an assigned task the human does not execute, "
    "carrying commitment warrant; re-authored in part (iv)). The live set is that delivery and coffee_break; neither "
    "reaches theta while adequate, so every decision rests on the fallback projection. "
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
            assigned_tasks=list(_UNPERFORMED),
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
            assigned_tasks=list(_UNPERFORMED),
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

scenario_s11_03 = ScenarioConfig(
    id="scenario_s11_03",
    setup="env_setup_11",
    reference_layouts=["env_layout_12"],
    description=_MPB + (
        "scenario_s11_03, the switch while carrying (MPB part (v), coverage row D9; T-D X, X1 with the return walk): "
        "scenario_s11_01's human script unchanged (the stand at kitting_table_2 from tick 0, unmodelled, declared here, "
        "then the exit); the robot's pool is scenario_s11_01's, and the robot starts 50 cm south of shelf_3, so it grasps "
        "item_8 before the first expiry whose hold can exceed the empty-handed cost difference (3.5 ticks). The "
        "experimental variable is the robot's carrying state at the decision, which puts the return walk "
        "(deliver_with_return: item_8 back to shelf_3) into the cost difference, not when the stand began. Authored to "
        "expose the switch by cost while carrying: at the first projection_expired decision whose hold on item_8 (at most "
        "k + 1, k the observed standing count) exceeds the cost difference with the return walk, the winner switches to "
        "item_9 and item_8 goes back to shelf_3 before item_9 is grasped."
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
            assigned_tasks=list(_UNPERFORMED),
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-420, 540),
            assigned_tasks=[
                deliver_item("item_8", table="kitting_table_2"),
                deliver_item("item_9", table="kitting_table_4"),
            ],
            observes=["human_0"],
        ),
    ],
)


# T-F part 1, part 1b (5 October 2026): copies with a fact in force (analysis/kitting/tf1/make_copies.py; REPORT.md, "Part 1").
scenario_s11_04 = ScenarioConfig(
    id="scenario_s11_04",
    setup="env_setup_11",
    reference_layouts=["env_layout_12"],
    timeline=Timeline((window(BREAK_TIME, 0, 61),)),
    description=(
        "T-F part 1, part 1b: scenario_s11_01's copy with a fact in force, not in accord: break_time over ticks 0 to 61 (stand(PT120S)). "
        "Everything else is scenario_s11_01's (analysis/kitting/tf1/make_copies.py)."
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
            assigned_tasks=list(_UNPERFORMED),
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


scenario_s11_05 = ScenarioConfig(
    id="scenario_s11_05",
    setup="env_setup_11",
    reference_layouts=["env_layout_12"],
    timeline=Timeline((window(BREAK_TIME, 0, 21),)),
    description=(
        "T-F part 1, part 1b: scenario_s11_02's copy with a fact in force, not in accord: break_time over ticks 0 to 21 (go_to(door_N)). "
        "Everything else is scenario_s11_02's (analysis/kitting/tf1/make_copies.py)."
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
            assigned_tasks=list(_UNPERFORMED),
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


scenario_s11_06 = ScenarioConfig(
    id="scenario_s11_06",
    setup="env_setup_11",
    reference_layouts=["env_layout_12"],
    timeline=Timeline((window(BREAK_TIME, 0, 61),)),
    description=(
        "T-F part 1, part 1b: scenario_s11_03's copy with a fact in force, not in accord: break_time over ticks 0 to 61 (stand(PT120S)). "
        "Everything else is scenario_s11_03's (analysis/kitting/tf1/make_copies.py)."
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
            assigned_tasks=list(_UNPERFORMED),
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-420, 540),
            assigned_tasks=[
                deliver_item("item_8", table="kitting_table_2"),
                deliver_item("item_9", table="kitting_table_4"),
            ],
            observes=["human_0"],
        ),
    ],
)

