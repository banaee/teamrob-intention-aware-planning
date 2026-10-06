# domains/dock_loading/scenarios/scenarios_s09.py
"""
Dock_loading scenarios on env_setup_09 (T-G stage 1, kind 3 "pallets in the bays", written for env_layout_04;
design_records.md, "T-G: the second domain's rulings", THE MPB ON DOCK_LOADING: THE SET, its rulings and the build
plan's dispositions DL-P1 to DL-P9). One module per setup. The MPB on dock_loading: K1 to K9 as _01 to _09 (controlled),
M3 as _10 (mixed, independent of the robot, full expectations). Every authored duration and cut point is derived from
path lengths in analysis/dock_loading/mpb/authoring.md.
"""

from shared.types import AgentConfig, ScenarioConfig, Script
from domains.dock_loading.actions import move_to
from domains.dock_loading.script import (coffee_break, confirm_delivered_pallet, deliver_pallet, go_to, load_return,
                                         office_break, stand)
from shared.types import Timeline
from domains.dock_loading.script import window
from domains.dock_loading.facts import BREAK_TIME


scenario_s09_01 = ScenarioConfig(
    id="scenario_s09_01",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "MPB on dock_loading, K1, the control: the human scans pallet_0 in the dry bay; the robot delivers "
        "pallet_5 to the frozen bay, its one task (every human walk and stand keeps at least 248.3 cm from its "
        "route; no other pairing of this room keeps more than min_separation, DL-P3). Tests: no hold at any "
        "decision; completion and every position equal to the comparison run (the same setup, pool and start, the "
        "human removed). Controlled (THE SET; MPB-DL3): kind 3 \"pallets in the bays\", a script independent of "
        "the robot, the disjointness rule (MPB-DL7) checked before the runs, full expectations committed before "
        "the runs. The human starts at the standby place and closes at the desk (B13); the robot starts on the "
        "truck side; prior on."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_5"),
            ],
        ),
    ],
)


scenario_s09_02 = ScenarioConfig(
    id="scenario_s09_02",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "MPB on dock_loading, K2, admission and the admitted projection (meeting form 1): the human scans "
        "pallet_0, then pallet_2; the robot delivers pallet_4 and pallet_5 and returns pallet_6. Tests: the "
        "decision at the tick the gate clears, against the human's projected walk to the bay the robot delivers "
        "to; where the records predict no admission, decisions on the fallback projection. Controlled (THE SET; "
        "MPB-DL3): kind 3 \"pallets in the bays\", a script independent of the robot, the disjointness rule "
        "(MPB-DL7) checked before the runs, full expectations committed before the runs. The human starts at the "
        "standby place and closes at the desk (B13); the robot starts on the truck side; prior on."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_03 = ScenarioConfig(
    id="scenario_s09_03",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "MPB on dock_loading, K3, the stand at a bay with an alternative task (meeting form 2): the human scans "
        "pallet_0, then stands at the dry bay for 96 ticks (PT192S; authoring.md), unmodelled behaviour; the "
        "robot delivers pallet_4 and pallet_5 and returns pallet_6. Tests: decisions on the fallback projection "
        "of a standing human and the projection_expired cadence. The switch by cost is reported, not expected "
        "(DL-P2). Controlled (THE SET; MPB-DL3): kind 3 \"pallets in the bays\", a script independent of the "
        "robot, the disjointness rule (MPB-DL7) checked before the runs, full expectations committed before the "
        "runs. The human starts at the standby place and closes at the desk (B13); the robot starts on the truck "
        "side; prior on."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_04 = ScenarioConfig(
    id="scenario_s09_04",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "MPB on dock_loading, K4, the stand at a bay with no alternative: the human as K3; the robot's pool is "
        "the delivery of pallet_4 to the dry bay only. Tests: the robot holds; the holds lengthen at each expiry "
        "(evidence for TODO-132 (a), not a verified rule). Controlled (THE SET; MPB-DL3): kind 3 \"pallets in the "
        "bays\", a script independent of the robot, the disjointness rule (MPB-DL7) checked before the runs, full "
        "expectations committed before the runs. The human starts at the standby place and closes at the desk "
        "(B13); the robot starts on the truck side; prior on."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
            ],
        ),
    ],
)


scenario_s09_05 = ScenarioConfig(
    id="scenario_s09_05",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "MPB on dock_loading, K5, the same motion: the human scans pallet_0, then pallet_1, both in the dry bay; "
        "the robot delivers pallet_4 and pallet_5 and returns pallet_6. Tests: the gate refuses during the walk; "
        "the robot decides on the fallback projection of a walking human. Controlled (THE SET; MPB-DL3): kind 3 "
        "\"pallets in the bays\", a script independent of the robot, the disjointness rule (MPB-DL7) checked "
        "before the runs, full expectations committed before the runs. The human starts at the standby place and "
        "closes at the desk (B13); the robot starts on the truck side; prior on."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_1"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_1"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_06 = ScenarioConfig(
    id="scenario_s09_06",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "MPB on dock_loading, K6, a foreseeable task between scans: the human scans pallet_0, takes a "
        "coffee_break (an ordinary entry, Q15), then scans pallet_2; the robot has its four tasks. Tests: "
        "admission on observation warrant during the break walk; the boundary and the re-admission after it. "
        "Controlled (THE SET; MPB-DL3): kind 3 \"pallets in the bays\", a script independent of the robot, the "
        "disjointness rule (MPB-DL7) checked before the runs, full expectations committed before the runs. The "
        "human starts at the standby place and closes at the desk (B13); the robot starts on the truck side; "
        "prior on."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_07 = ScenarioConfig(
    id="scenario_s09_07",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "MPB on dock_loading, K7, the office: the human scans pallet_0, takes an office_break (an ordinary "
        "entry), then scans pallet_2; the robot has its four tasks. Tests: the admitted projection through the "
        "office door; the robot's decisions while the human is in another area. Controlled (THE SET; MPB-DL3): "
        "kind 3 \"pallets in the bays\", a script independent of the robot, the disjointness rule (MPB-DL7) "
        "checked before the runs, full expectations committed before the runs. The human starts at the standby "
        "place and closes at the desk (B13); the robot starts on the truck side; prior on."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    office_break("office_chair"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_08 = ScenarioConfig(
    id="scenario_s09_08",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "MPB on dock_loading, K8, the change during an action: the human's walk to pallet_0 is cut on its last "
        "step (PT30S, 15 of its 16 steps; DL-P1) into a coffee_break, after which the scan resumes; then the "
        "human scans pallet_2; the robot delivers pallet_4 and pallet_5 and returns pallet_6. Tests: retraction, "
        "the fallback projection after it, re-admission, where the oracle derives them. Controlled (THE SET; "
        "MPB-DL3): kind 3 \"pallets in the bays\", a script independent of the robot, the disjointness rule "
        "(MPB-DL7) checked before the runs, full expectations committed before the runs. The human starts at the "
        "standby place and closes at the desk (B13); the robot starts on the truck side; prior on."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").during(move_to, "PT30S", coffee_break("coffee_machine_0"), occurrence=0),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_09 = ScenarioConfig(
    id="scenario_s09_09",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "MPB on dock_loading, K9, the admission that is wrong about the human: the human scans pallet_2 in the "
        "frozen bay, walks to the standby place (an ordinary entry) and stands there for 30 ticks (PT60S; "
        "authoring.md); assigned the scan only; the robot delivers pallet_4 and returns pallet_6. Tests: the walk "
        "to the standby place admitted as a break (expected so, by the records), the robot's decision against it, "
        "the retraction when the human stands. The wrong reading is a finding about the mind (MPB-DL1 (iv)), not "
        "a disagreement. Contains behaviour with no hypothesis: the walk to and the stand at the standby place. "
        "Controlled (THE SET; MPB-DL3): kind 3 \"pallets in the bays\", a script independent of the robot, the "
        "disjointness rule (MPB-DL7) checked before the runs, full expectations committed before the runs. The "
        "human starts at the standby place and closes at the desk (B13); the robot starts on the truck side; "
        "prior on."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    go_to("standby_place"),
                    stand("PT60S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_10 = ScenarioConfig(
    id="scenario_s09_10",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "MPB on dock_loading, M3, combined deviations (mixed; independent of the robot, kind 3, full "
        "expectations; read only against the controlled ones): the human walks to pallet_0 and takes a "
        "coffee_break on arrival, then scans pallet_0, pallet_1 and pallet_2 and stands at the frozen bay for 96 "
        "ticks (PT192S); the robot has its four tasks. Combines K5, K6 and K3. The human starts at the standby "
        "place and closes at the desk; the robot starts on the truck side; prior on."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                    confirm_delivered_pallet("pallet_1"),
                    confirm_delivered_pallet("pallet_2"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_1"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


# T-K part 1, step 6 (6 October 2026): the new scripts (analysis/dock_loading/tk6/make_set.py bases).
scenario_s09_11 = ScenarioConfig(
    id="scenario_s09_11",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "T-K part 1, step 6, script a (a coffee break first, before any scan), on env_layout_04: the human takes a "
        "coffee break, scans pallet_0, scans pallet_2, then the walk to the desk; the robot delivers pallet_4 and "
        "pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script independent of the robot, the disjointness "
        "rule (MPB-DL7). No timeline (no fact); its copies with break_time follow. No expectation derived by hand "
        "(Hadi, 6 October 2026); the oracle's tables are committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_12 = ScenarioConfig(
    id="scenario_s09_12",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "T-K part 1, step 6, script b (scans only, across both bays), on env_layout_04: the human scans pallet_0, "
        "scans pallet_2, scans pallet_1, scans pallet_3, then the walk to the desk; the robot delivers pallet_4 "
        "and pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script independent of the robot, the "
        "disjointness rule (MPB-DL7). No timeline (no fact); its copies with break_time follow. No expectation "
        "derived by hand (Hadi, 6 October 2026); the oracle's tables are committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                    confirm_delivered_pallet("pallet_1"),
                    confirm_delivered_pallet("pallet_3"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_1"),
                confirm_delivered_pallet("pallet_3"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_13 = ScenarioConfig(
    id="scenario_s09_13",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "T-K part 1, step 6, script c (an office break inside a scan, on arrival at the bay before the scan), on "
        "env_layout_04: the human scans pallet_0 with an office break on arrival at the bay, scans pallet_2, then "
        "the walk to the desk; the robot delivers pallet_4 and pallet_5 and returns pallet_6 and pallet_7. Kind 3, "
        "a script independent of the robot, the disjointness rule (MPB-DL7). No timeline (no fact); its copies "
        "with break_time follow. No expectation derived by hand (Hadi, 6 October 2026); the oracle's tables are "
        "committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").at(move_to, office_break("office_chair"), occurrence=0),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_14 = ScenarioConfig(
    id="scenario_s09_14",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "T-K part 1, step 6, script d (a second coffee break inside the first's recency), on env_layout_04: the "
        "human takes a coffee break, scans pallet_0, takes a coffee break, scans pallet_2, then the walk to the "
        "desk; the robot delivers pallet_4 and pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script "
        "independent of the robot, the disjointness rule (MPB-DL7). No timeline (no fact); its copies with "
        "break_time follow. No expectation derived by hand (Hadi, 6 October 2026); the oracle's tables are "
        "committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_15 = ScenarioConfig(
    id="scenario_s09_15",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "T-K part 1, step 6, script e (a coffee break, then an office break), on env_layout_04: the human scans "
        "pallet_0, takes a coffee break, takes an office break, scans pallet_2, then the walk to the desk; the "
        "robot delivers pallet_4 and pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script independent of "
        "the robot, the disjointness rule (MPB-DL7). No timeline (no fact); its copies with break_time follow. No "
        "expectation derived by hand (Hadi, 6 October 2026); the oracle's tables are committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    office_break("office_chair"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_16 = ScenarioConfig(
    id="scenario_s09_16",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "T-K part 1, step 6, script e' (an office break, then a coffee break), on env_layout_04: the human scans "
        "pallet_0, takes an office break, takes a coffee break, scans pallet_2, then the walk to the desk; the "
        "robot delivers pallet_4 and pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script independent of "
        "the robot, the disjointness rule (MPB-DL7). No timeline (no fact); its copies with break_time follow. No "
        "expectation derived by hand (Hadi, 6 October 2026); the oracle's tables are committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    office_break("office_chair"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_17 = ScenarioConfig(
    id="scenario_s09_17",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "T-K part 1, step 6, script f (one coffee break between two scans, for the three window edges), on "
        "env_layout_04: the human scans pallet_2, takes a coffee break, scans pallet_0, then the walk to the desk; "
        "the robot delivers pallet_4 and pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script independent "
        "of the robot, the disjointness rule (MPB-DL7). No timeline (no fact); its copies with break_time follow. "
        "No expectation derived by hand (Hadi, 6 October 2026); the oracle's tables are committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_18 = ScenarioConfig(
    id="scenario_s09_18",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    description=(
        "T-K part 1, step 6, script g (a coffee break once every scan is done (no assigned task live)), on "
        "env_layout_04: the human scans pallet_0, scans pallet_2, takes a coffee break, then the walk to the desk; "
        "the robot delivers pallet_4 and pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script independent "
        "of the robot, the disjointness rule (MPB-DL7). No timeline (no fact); its copies with break_time follow. "
        "No expectation derived by hand (Hadi, 6 October 2026); the oracle's tables are committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                    coffee_break("coffee_machine_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


# T-K part 1, step 6 (6 October 2026): the copies with break_time (analysis/dock_loading/tk6/make_set.py variants).
scenario_s09_19 = ScenarioConfig(
    id="scenario_s09_19",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 19),)),
    description=(
        "T-K part 1, step 6: scenario_s09_01's copy with break_time from 0 to 19 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_01's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_5"),
            ],
        ),
    ],
)


scenario_s09_20 = ScenarioConfig(
    id="scenario_s09_20",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 19, 55),)),
    description=(
        "T-K part 1, step 6: scenario_s09_01's copy with break_time from 19 to 55 (V2, over another task; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_01's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_5"),
            ],
        ),
    ],
)


scenario_s09_21 = ScenarioConfig(
    id="scenario_s09_21",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 19),)),
    description=(
        "T-K part 1, step 6: scenario_s09_02's copy with break_time from 0 to 19 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_02's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_22 = ScenarioConfig(
    id="scenario_s09_22",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 19, 39),)),
    description=(
        "T-K part 1, step 6: scenario_s09_02's copy with break_time from 19 to 39 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_02's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_23 = ScenarioConfig(
    id="scenario_s09_23",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 19),)),
    description=(
        "T-K part 1, step 6: scenario_s09_03's copy with break_time from 0 to 19 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_03's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_24 = ScenarioConfig(
    id="scenario_s09_24",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 19, 116),)),
    description=(
        "T-K part 1, step 6: scenario_s09_03's copy with break_time from 19 to 116 (V2, over another task; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_03's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_25 = ScenarioConfig(
    id="scenario_s09_25",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 19),)),
    description=(
        "T-K part 1, step 6: scenario_s09_04's copy with break_time from 0 to 19 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_04's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
            ],
        ),
    ],
)


scenario_s09_26 = ScenarioConfig(
    id="scenario_s09_26",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 19, 116),)),
    description=(
        "T-K part 1, step 6: scenario_s09_04's copy with break_time from 19 to 116 (V2, over another task; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_04's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
            ],
        ),
    ],
)


scenario_s09_27 = ScenarioConfig(
    id="scenario_s09_27",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 19),)),
    description=(
        "T-K part 1, step 6: scenario_s09_05's copy with break_time from 0 to 19 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_05's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_1"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_1"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_28 = ScenarioConfig(
    id="scenario_s09_28",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 19, 22),)),
    description=(
        "T-K part 1, step 6: scenario_s09_05's copy with break_time from 19 to 22 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_05's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_1"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_1"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_29 = ScenarioConfig(
    id="scenario_s09_29",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 19, 73),)),
    description=(
        "T-K part 1, step 6: scenario_s09_06's copy with break_time from 19 to 73 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_06's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_30 = ScenarioConfig(
    id="scenario_s09_30",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 19),)),
    description=(
        "T-K part 1, step 6: scenario_s09_06's copy with break_time from 0 to 19 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_06's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_31 = ScenarioConfig(
    id="scenario_s09_31",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 19, 86),)),
    description=(
        "T-K part 1, step 6: scenario_s09_07's copy with break_time from 19 to 86 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_07's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    office_break("office_chair"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_32 = ScenarioConfig(
    id="scenario_s09_32",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 19),)),
    description=(
        "T-K part 1, step 6: scenario_s09_07's copy with break_time from 0 to 19 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_07's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    office_break("office_chair"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_33 = ScenarioConfig(
    id="scenario_s09_33",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 15, 69),)),
    description=(
        "T-K part 1, step 6: scenario_s09_08's copy with break_time from 15 to 69 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_08's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").during(move_to, "PT30S", coffee_break("coffee_machine_0"), occurrence=0),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_34 = ScenarioConfig(
    id="scenario_s09_34",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 15),)),
    description=(
        "T-K part 1, step 6: scenario_s09_08's copy with break_time from 0 to 15 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_08's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").during(move_to, "PT30S", coffee_break("coffee_machine_0"), occurrence=0),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_35 = ScenarioConfig(
    id="scenario_s09_35",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 28),)),
    description=(
        "T-K part 1, step 6: scenario_s09_09's copy with break_time from 0 to 28 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_09's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    go_to("standby_place"),
                    stand("PT60S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_36 = ScenarioConfig(
    id="scenario_s09_36",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 28, 53),)),
    description=(
        "T-K part 1, step 6: scenario_s09_09's copy with break_time from 28 to 53 (V2, over another task; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_09's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    go_to("standby_place"),
                    stand("PT60S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s09_37 = ScenarioConfig(
    id="scenario_s09_37",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 17, 71),)),
    description=(
        "T-K part 1, step 6: scenario_s09_10's copy with break_time from 17 to 71 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_10's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                    confirm_delivered_pallet("pallet_1"),
                    confirm_delivered_pallet("pallet_2"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_1"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_38 = ScenarioConfig(
    id="scenario_s09_38",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 17),)),
    description=(
        "T-K part 1, step 6: scenario_s09_10's copy with break_time from 0 to 17 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_10's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                    confirm_delivered_pallet("pallet_1"),
                    confirm_delivered_pallet("pallet_2"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_1"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_39 = ScenarioConfig(
    id="scenario_s09_39",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 54),)),
    description=(
        "T-K part 1, step 6: scenario_s09_11's copy with break_time from 0 to 54 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_11's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_40 = ScenarioConfig(
    id="scenario_s09_40",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 54, 79),)),
    description=(
        "T-K part 1, step 6: scenario_s09_11's copy with break_time from 54 to 79 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_11's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_41 = ScenarioConfig(
    id="scenario_s09_41",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 19),)),
    description=(
        "T-K part 1, step 6: scenario_s09_12's copy with break_time from 0 to 19 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_12's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                    confirm_delivered_pallet("pallet_1"),
                    confirm_delivered_pallet("pallet_3"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_1"),
                confirm_delivered_pallet("pallet_3"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_42 = ScenarioConfig(
    id="scenario_s09_42",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 19, 39),)),
    description=(
        "T-K part 1, step 6: scenario_s09_12's copy with break_time from 19 to 39 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_12's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                    confirm_delivered_pallet("pallet_1"),
                    confirm_delivered_pallet("pallet_3"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_1"),
                confirm_delivered_pallet("pallet_3"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_43 = ScenarioConfig(
    id="scenario_s09_43",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 17, 84),)),
    description=(
        "T-K part 1, step 6: scenario_s09_13's copy with break_time from 17 to 84 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_13's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").at(move_to, office_break("office_chair"), occurrence=0),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_44 = ScenarioConfig(
    id="scenario_s09_44",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 17),)),
    description=(
        "T-K part 1, step 6: scenario_s09_13's copy with break_time from 0 to 17 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_13's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").at(move_to, office_break("office_chair"), occurrence=0),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_45 = ScenarioConfig(
    id="scenario_s09_45",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 54),)),
    description=(
        "T-K part 1, step 6: scenario_s09_14's copy with break_time from 0 to 54 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_14's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_46 = ScenarioConfig(
    id="scenario_s09_46",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 54, 79),)),
    description=(
        "T-K part 1, step 6: scenario_s09_14's copy with break_time from 54 to 79 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_14's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_47 = ScenarioConfig(
    id="scenario_s09_47",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 54), window(BREAK_TIME, 79, 133),)),
    description=(
        "T-K part 1, step 6: scenario_s09_14's copy with break_time from 0 to 54 and from 79 to 133 (V3, over both "
        "breaks; the rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_14's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_48 = ScenarioConfig(
    id="scenario_s09_48",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 19, 73),)),
    description=(
        "T-K part 1, step 6: scenario_s09_15's copy with break_time from 19 to 73 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_15's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    office_break("office_chair"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_49 = ScenarioConfig(
    id="scenario_s09_49",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 19),)),
    description=(
        "T-K part 1, step 6: scenario_s09_15's copy with break_time from 0 to 19 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_15's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    office_break("office_chair"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_50 = ScenarioConfig(
    id="scenario_s09_50",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 19, 73), window(BREAK_TIME, 73, 159),)),
    description=(
        "T-K part 1, step 6: scenario_s09_15's copy with break_time from 19 to 73 and from 73 to 159 (V3, over "
        "both breaks; the rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is "
        "scenario_s09_15's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    office_break("office_chair"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_51 = ScenarioConfig(
    id="scenario_s09_51",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 19, 86),)),
    description=(
        "T-K part 1, step 6: scenario_s09_16's copy with break_time from 19 to 86 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_16's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    office_break("office_chair"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_52 = ScenarioConfig(
    id="scenario_s09_52",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 19),)),
    description=(
        "T-K part 1, step 6: scenario_s09_16's copy with break_time from 0 to 19 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_16's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    office_break("office_chair"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_53 = ScenarioConfig(
    id="scenario_s09_53",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 19, 86), window(BREAK_TIME, 86, 157),)),
    description=(
        "T-K part 1, step 6: scenario_s09_16's copy with break_time from 19 to 86 and from 86 to 157 (V3, over "
        "both breaks; the rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is "
        "scenario_s09_16's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    office_break("office_chair"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_54 = ScenarioConfig(
    id="scenario_s09_54",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 18, 70),)),
    description=(
        "T-K part 1, step 6: scenario_s09_17's copy with break_time from 18 to 70 (edge before the human leaves; "
        "the rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_17's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_55 = ScenarioConfig(
    id="scenario_s09_55",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 33, 70),)),
    description=(
        "T-K part 1, step 6: scenario_s09_17's copy with break_time from 33 to 70 (edge in the walk; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_17's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_56 = ScenarioConfig(
    id="scenario_s09_56",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 39, 70),)),
    description=(
        "T-K part 1, step 6: scenario_s09_17's copy with break_time from 39 to 70 (edge at the arrival; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_17's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_57 = ScenarioConfig(
    id="scenario_s09_57",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 39, 82),)),
    description=(
        "T-K part 1, step 6: scenario_s09_18's copy with break_time from 39 to 82 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_18's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                    coffee_break("coffee_machine_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s09_58 = ScenarioConfig(
    id="scenario_s09_58",
    setup="env_setup_09",
    reference_layouts=["env_layout_04"],
    timeline=Timeline((window(BREAK_TIME, 0, 19),)),
    description=(
        "T-K part 1, step 6: scenario_s09_18's copy with break_time from 0 to 19 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s09_18's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                    coffee_break("coffee_machine_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)
