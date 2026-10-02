# domains/dock_loading/scenarios/scenarios_s06.py
"""
Dock_loading scenarios on env_setup_06 (T-G stage 1, kind 1, written for
env_layout_04; design_records.md, "T-G: the second domain's rulings", B14).
One module per setup.
"""

from shared.types import AgentConfig, RepeatableEntry, ScenarioConfig, Script, ScriptDependence, drop
from domains.dock_loading.actions import move_to
from domains.dock_loading.script import coffee_break, confirm_delivered_pallet, go_to, office_break, stand


# A viewing fixture: the scene loads and initialises; not a baseline, not an
# IR test-bed or MPB case.
scenario_s06_01 = ScenarioConfig(
    id="scenario_s06_01",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "A viewing fixture (T-G stage 1, B14), written so that the scene loads and initialises; not a baseline, "
        "not an IR test-bed or MPB case. Setup kind 1, the IR test-bed's: the robot idle on the gate's centre point; the human at the standby place. The human has "
        "no script and no assigned task, the robot no assigned task."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script([]),
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


# The IR test-bed on dock_loading (design_records.md, "T-G: the second domain's rulings", T-G Q16's block: the
# set, 14 controlled scenarios C1 to C14 as _02 to _15 and 4 mixed M1 to M4 as _16 to _19, each in the three rooms).
# The robot is idle; expectations are derived from the records before the runs (analysis/dock_loading/ir_testbed/).
scenario_s06_02 = ScenarioConfig(
    id="scenario_s06_02",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row C1: assigned work in two bays: scan 0, then scan 2. Controlled; "
        "the room's IR setup (kind 1 of B14), the robot idle on the gate's centre point with no task, the human starting "
        "at the standby place; prior on; the closing part is the walk to the desk (B13). Contains behaviour with no "
        "hypothesis in the robot's task model: the walk to the desk. The script is independent of the robot."
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
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_03 = ScenarioConfig(
    id="scenario_s06_03",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row C2: the order: scan 2, then scan 0 (C1 reversed). Controlled; "
        "the room's IR setup (kind 1 of B14), the robot idle on the gate's centre point with no task, the human starting "
        "at the standby place; prior on; the closing part is the walk to the desk (B13). Contains behaviour with no "
        "hypothesis in the robot's task model: the walk to the desk. The script is independent of the robot."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    confirm_delivered_pallet("pallet_0"),
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
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_04 = ScenarioConfig(
    id="scenario_s06_04",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row C3: two scans with the same motion: scan 0, then scan 1, both "
        "in the dry bay (C5 of the T-G entry: the two hypotheses share the first walk; pallet_0 and pallet_1 stand on one "
        "point, so scan 1 has no walk). Controlled; the room's IR setup (kind 1 of B14), the robot idle on the gate's "
        "centre point with no task, the human starting at the standby place; prior on; the closing part is the walk to "
        "the desk (B13). Contains behaviour with no hypothesis in the robot's task model: the walk to the desk. The "
        "script is independent of the robot."
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
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_05 = ScenarioConfig(
    id="scenario_s06_05",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row C4: the lifecycle over many episodes: scan 0, 2, 1, 3. "
        "Controlled; the room's IR setup (kind 1 of B14), the robot idle on the gate's centre point with no task, the "
        "human starting at the standby place; prior on; the closing part is the walk to the desk (B13). Contains "
        "behaviour with no hypothesis in the robot's task model: the walk to the desk. The script is independent of the "
        "robot."
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
                confirm_delivered_pallet("pallet_1"),
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_3"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_06 = ScenarioConfig(
    id="scenario_s06_06",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row C5: a foreseeable task between scans: scan 0, coffee_break, "
        "scan 2. Controlled; the room's IR setup (kind 1 of B14), the robot idle on the gate's centre point with no task, "
        "the human starting at the standby place; prior on; the closing part is the walk to the desk (B13). Contains "
        "behaviour with no hypothesis in the robot's task model: the walk to the desk. The script is independent of the "
        "robot."
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
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_07 = ScenarioConfig(
    id="scenario_s06_07",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row C6: the office and its door: scan 0, office_break (90 seconds), "
        "scan 2 (from the office, through the door). Controlled; the room's IR setup (kind 1 of B14), the robot idle on "
        "the gate's centre point with no task, the human starting at the standby place; prior on; the closing part is the "
        "walk to the desk (B13). Contains behaviour with no hypothesis in the robot's task model: the walk to the desk. "
        "The script is independent of the robot."
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
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_08 = ScenarioConfig(
    id="scenario_s06_08",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row C7: a foreseeable task inside a scan: coffee_break started on "
        "the arrival at pallet_0 (after the scan's move_to, before scan_it), the scan resumed; then scan 2. Controlled; "
        "the room's IR setup (kind 1 of B14), the robot idle on the gate's centre point with no task, the human starting "
        "at the standby place; prior on; the closing part is the walk to the desk (B13). Contains behaviour with no "
        "hypothesis in the robot's task model: the walk to the desk. The script is independent of the robot."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
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
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_09 = ScenarioConfig(
    id="scenario_s06_09",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row C8: an interruption inside a walk: coffee_break cut into the "
        "walk to pallet_0 (T-H's during, PT28S: 14 ticks, the value of kitting's mid-action cut, scenario_s09_13), the "
        "scan resumed; then scan 2. Controlled; the room's IR setup (kind 1 of B14), the robot idle on the gate's centre "
        "point with no task, the human starting at the standby place; prior on; the closing part is the walk to the desk "
        "(B13). Contains behaviour with no hypothesis in the robot's task model: the walk to the desk. The script is "
        "independent of the robot."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").during(move_to, "PT28S", coffee_break("coffee_machine_0"), occurrence=0),
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
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_10 = ScenarioConfig(
    id="scenario_s06_10",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row C9: a dropped scan: scan 0 dropped during its walk (PT28S); "
        "then scan 2. Controlled; the room's IR setup (kind 1 of B14), the robot idle on the gate's centre point with no "
        "task, the human starting at the standby place; prior on; the closing part is the walk to the desk (B13). "
        "Contains behaviour with no hypothesis in the robot's task model: the walk to the desk. The script is independent "
        "of the robot."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").during(move_to, "PT28S", drop, occurrence=0),
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
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_11 = ScenarioConfig(
    id="scenario_s06_11",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row C10: an authored retry (T-G Q12): scan 0 dropped during its "
        "walk (PT28S); scan 2; scan 0 as a second entry. Controlled; the room's IR setup (kind 1 of B14), the robot idle "
        "on the gate's centre point with no task, the human starting at the standby place; prior on; the closing part is "
        "the walk to the desk (B13). Contains behaviour with no hypothesis in the robot's task model: the walk to the "
        "desk. The script is independent of the robot."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").during(move_to, "PT28S", drop, occurrence=0),
                    confirm_delivered_pallet("pallet_2"),
                    confirm_delivered_pallet("pallet_0"),
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
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_12 = ScenarioConfig(
    id="scenario_s06_12",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row C11: the long stand: scan 0; a stand at the dry bay where the "
        "human has just scanned (stand(PT80S), 40 ticks, the duration of kitting's long-stand scenario scenario_s09_06; "
        "Hadi, 1 October 2026); scan 2. Controlled; the room's IR setup (kind 1 of B14), the robot idle on the gate's "
        "centre point with no task, the human starting at the standby place; prior on; the closing part is the walk to "
        "the desk (B13). Contains behaviour with no hypothesis in the robot's task model: the stand and the walk to the "
        "desk. The script is independent of the robot."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    stand("PT80S"),
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
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_13 = ScenarioConfig(
    id="scenario_s06_13",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row C12: a scan outside the assigned set: assigned the scans of "
        "pallet_0 and pallet_2; the script scans pallet_1, then pallet_2. Controlled; the room's IR setup (kind 1 of "
        "B14), the robot idle on the gate's centre point with no task, the human starting at the standby place; prior on; "
        "the closing part is the walk to the desk (B13). Contains behaviour with no hypothesis in the robot's task model: "
        "the walk to the desk; the scan of pallet_1 is outside the support under the prior. The script is independent of "
        "the robot."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_1"),
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
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_14 = ScenarioConfig(
    id="scenario_s06_14",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row C13: a diagnostic row (T-G Q16): the standby walk from the dry "
        "bay, and a hypothesis never live. Assigned the scans of pallet_0 and pallet_4; pallet_4 stays in the truck (the "
        "robot is idle), so its scan never becomes applicable, its entry stays open, the priority list is never finished "
        "and the closing part, the walk to the desk, is not taken (intended; Hadi, 1 October 2026); the record states the "
        "entries still open at the run's end. Controlled; the room's IR setup (kind 1 of B14), the robot idle on the "
        "gate's centre point with no task, the human starting at the standby place; prior on; the closing part is the "
        "walk to the desk (B13). Contains behaviour with no hypothesis in the robot's task model: the walk to and the "
        "stay at the standby place. The script is declared dependent on the robot (the scan of pallet_4 waits for a "
        "delivery that never comes)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_4"),
                    RepeatableEntry(go_to("standby_place")),
                ],
                closing=[go_to("desk")],
                dependence=ScriptDependence.ON_ROBOT,
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_4"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_15 = ScenarioConfig(
    id="scenario_s06_15",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row C14: a diagnostic row (T-G Q16): the standby walk from the "
        "frozen bay. Assigned the scans of pallet_2 and pallet_4; as C13, the scan of pallet_4 never becomes applicable, "
        "its entry stays open and the walk to the desk is not taken (intended; Hadi, 1 October 2026). Controlled; the "
        "room's IR setup (kind 1 of B14), the robot idle on the gate's centre point with no task, the human starting at "
        "the standby place; prior on; the closing part is the walk to the desk (B13). Contains behaviour with no "
        "hypothesis in the robot's task model: the walk to and the stay at the standby place. The script is declared "
        "dependent on the robot (the scan of pallet_4 waits for a delivery that never comes)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    confirm_delivered_pallet("pallet_4"),
                    RepeatableEntry(go_to("standby_place")),
                ],
                closing=[go_to("desk")],
                dependence=ScriptDependence.ON_ROBOT,
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_4"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_16 = ScenarioConfig(
    id="scenario_s06_16",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row M1: mixed: scan 0 with coffee_break started on the arrival at "
        "pallet_0; office_break; scan 2. Mixed; the room's IR setup (kind 1 of B14), the robot idle on the gate's centre "
        "point with no task, the human starting at the standby place; prior on; the closing part is the walk to the desk "
        "(B13). Contains behaviour with no hypothesis in the robot's task model: the walk to the desk. The script is "
        "independent of the robot."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
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
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_17 = ScenarioConfig(
    id="scenario_s06_17",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row M2: mixed: scan 0 dropped during its walk (PT28S); "
        "coffee_break; scan 2; scan 0 as a second entry. Mixed; the room's IR setup (kind 1 of B14), the robot idle on "
        "the gate's centre point with no task, the human starting at the standby place; prior on; the closing part is the "
        "walk to the desk (B13). Contains behaviour with no hypothesis in the robot's task model: the walk to the desk. "
        "The script is independent of the robot."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").during(move_to, "PT28S", drop, occurrence=0),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                    confirm_delivered_pallet("pallet_0"),
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
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_18 = ScenarioConfig(
    id="scenario_s06_18",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row M3: mixed: scan 0; the stand at the dry bay (stand(PT80S)); "
        "scan 2 with coffee_break cut into its walk (PT28S). As approved by Hadi (1 October 2026), scan 2 in place of the "
        "set's scan 1, whose walk has no step after the stand at the same bay. Mixed; the room's IR setup (kind 1 of "
        "B14), the robot idle on the gate's centre point with no task, the human starting at the standby place; prior on; "
        "the closing part is the walk to the desk (B13). Contains behaviour with no hypothesis in the robot's task model: "
        "the stand and the walk to the desk. The script is independent of the robot."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    stand("PT80S"),
                    confirm_delivered_pallet("pallet_2").during(move_to, "PT28S", coffee_break("coffee_machine_0"), occurrence=0),
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
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)


scenario_s06_19 = ScenarioConfig(
    id="scenario_s06_19",
    setup="env_setup_06",
    reference_layouts=["env_layout_04"],
    description=(
        "IR test-bed on dock_loading (T-G Q16's set), row M4: mixed, a diagnostic row (T-G Q16): assigned the scans of "
        "pallet_0, pallet_2 and pallet_4; the script scans pallet_1 (outside the support), takes office_break, scans "
        "pallet_2, then the scan of pallet_4, which never becomes applicable, so the standby entry is taken; the walk to "
        "the desk is not taken (intended; Hadi, 1 October 2026). Mixed; the room's IR setup (kind 1 of B14), the robot "
        "idle on the gate's centre point with no task, the human starting at the standby place; prior on; the closing "
        "part is the walk to the desk (B13). Contains behaviour with no hypothesis in the robot's task model: the walk to "
        "and the stay at the standby place; the scan of pallet_1 is outside the support under the prior. The script is "
        "declared dependent on the robot (the scan of pallet_4 waits for a delivery that never comes)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_1"),
                    office_break("office_chair"),
                    confirm_delivered_pallet("pallet_2"),
                    confirm_delivered_pallet("pallet_4"),
                    RepeatableEntry(go_to("standby_place")),
                ],
                closing=[go_to("desk")],
                dependence=ScriptDependence.ON_ROBOT,
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_4"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -300),
            observes=["human_0"],
        ),
    ],
)

