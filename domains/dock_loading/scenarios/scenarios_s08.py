# domains/dock_loading/scenarios/scenarios_s08.py
"""
Dock_loading scenarios on env_setup_08 (T-G stage 1, kind 3 "pallets in the bays", written for env_layout_03;
design_records.md, "T-G: the second domain's rulings", THE MPB ON DOCK_LOADING: THE SET, its rulings and the build
plan's dispositions DL-P1 to DL-P9). One module per setup. The MPB on dock_loading: K1 to K9 as _01 to _09 (controlled),
M3 as _10 (mixed, independent of the robot, full expectations). Every authored duration and cut point is derived from
path lengths in analysis/dock_loading/mpb/authoring.md.
"""

from shared.types import AgentConfig, ScenarioConfig, Script
from domains.dock_loading.actions import move_to
from domains.dock_loading.script import (coffee_break, confirm_delivered_pallet, deliver_pallet, go_to, load_return,
                                         office_break, stand)


scenario_s08_01 = ScenarioConfig(
    id="scenario_s08_01",
    setup="env_setup_08",
    reference_layouts=["env_layout_03"],
    description=(
        "MPB on dock_loading, K1, the control: the human scans pallet_2 in the frozen bay; the robot delivers "
        "pallet_4 to the dry bay and returns pallet_6 (every human walk and stand keeps at least 225.6 cm from "
        "every robot route, in every order of the pool). Tests: no hold at any decision; completion and every "
        "position equal to the comparison run (the same setup, pool and start, the human removed). Controlled "
        "(THE SET; MPB-DL3): kind 3 \"pallets in the bays\", a script independent of the robot, the disjointness "
        "rule (MPB-DL7) checked before the runs, full expectations committed before the runs. The human starts at "
        "the standby place and closes at the desk (B13); the robot starts on the truck side; prior on."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
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


scenario_s08_02 = ScenarioConfig(
    id="scenario_s08_02",
    setup="env_setup_08",
    reference_layouts=["env_layout_03"],
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


scenario_s08_03 = ScenarioConfig(
    id="scenario_s08_03",
    setup="env_setup_08",
    reference_layouts=["env_layout_03"],
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


scenario_s08_04 = ScenarioConfig(
    id="scenario_s08_04",
    setup="env_setup_08",
    reference_layouts=["env_layout_03"],
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


scenario_s08_05 = ScenarioConfig(
    id="scenario_s08_05",
    setup="env_setup_08",
    reference_layouts=["env_layout_03"],
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


scenario_s08_06 = ScenarioConfig(
    id="scenario_s08_06",
    setup="env_setup_08",
    reference_layouts=["env_layout_03"],
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


scenario_s08_07 = ScenarioConfig(
    id="scenario_s08_07",
    setup="env_setup_08",
    reference_layouts=["env_layout_03"],
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


scenario_s08_08 = ScenarioConfig(
    id="scenario_s08_08",
    setup="env_setup_08",
    reference_layouts=["env_layout_03"],
    description=(
        "MPB on dock_loading, K8, the change during an action: the human's walk to pallet_0 is cut on its last "
        "step (PT52S, 26 of its 27 steps; DL-P1) into a coffee_break, after which the scan resumes; then the "
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
                    confirm_delivered_pallet("pallet_0").during(move_to, "PT52S", coffee_break("coffee_machine_0"), occurrence=0),
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


scenario_s08_09 = ScenarioConfig(
    id="scenario_s08_09",
    setup="env_setup_08",
    reference_layouts=["env_layout_03"],
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


scenario_s08_10 = ScenarioConfig(
    id="scenario_s08_10",
    setup="env_setup_08",
    reference_layouts=["env_layout_03"],
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
