# domains/dock_loading/scenarios/scenarios_s05.py
"""
Dock_loading scenarios on env_setup_05 (T-G stage 1, kind 2, written for
env_layout_03; design_decisions.md, "T-G: the second domain's rulings", B14).
One module per setup.
"""

from shared.types import AgentConfig, RepeatableEntry, ScenarioConfig, Script, ScriptDependence
from domains.dock_loading.script import confirm_delivered_pallet, deliver_pallet, go_to, load_return


# A viewing fixture: the scene loads and initialises; not a baseline, not an
# IR test-bed or MPB case.
scenario_s05_01 = ScenarioConfig(
    id="scenario_s05_01",
    setup="env_setup_05",
    reference_layouts=["env_layout_03"],
    description=(
        "A viewing fixture (T-G stage 1, B14), written so that the scene loads and initialises; not a baseline, "
        "not an IR test-bed or MPB case. Setup kind 2, the MPB's: the robot on the truck side; the human at the standby place. The human has "
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
            start_position=(0, -370),
            observes=["human_0"],
        ),
    ],
)


# The milestone (T-G stage 1, step 8; plan_T-G_stage1.md, answer 8): one simple
# scenario per room runs from start to end. Not a baseline; it measures nothing.
scenario_s05_02 = ScenarioConfig(
    id="scenario_s05_02",
    setup="env_setup_05",
    reference_layouts=["env_layout_03"],
    description=(
        "The milestone of T-G stage 1 (plan_T-G_stage1.md, answer 8): the first evidence that the room, the five "
        "mechanisms (the rename, A9 with R2, A4, A5, A3) and the domain's tasks work together; it measures nothing. "
        "The robot delivers pallet_0 to its bay and returns the empty pallet_4 to the truck; the human scans "
        "pallet_0 once it stands in its bay and closes at the desk. The script is declared dependent on the robot "
        "(the scan waits for the delivery). The standby entry is written; the human starts at the standby place, "
        "where go_to(standby_place) is complete, so until the scan is applicable the machine waits there (the skip "
        "rule), and after the scan the priority list is finished: the standby walk is not taken in this scenario. "
        "Contains behaviour with no hypothesis in the robot's task model: the stay at the standby place and the "
        "walk to the desk (unmodelled behaviour)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [confirm_delivered_pallet("pallet_0"), RepeatableEntry(go_to("standby_place"))],
                closing=[go_to("desk")],
                dependence=ScriptDependence.ON_ROBOT,
            ),
            observes=[],
            assigned_tasks=[confirm_delivered_pallet("pallet_0")],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[deliver_pallet("pallet_0"), load_return("pallet_4")],
        ),
    ],
)


# The second milestone scenario (T-G stage 1; design_decisions.md, "T-G: the
# second domain's rulings", FINDINGS OF THE MILESTONE: a second simple scenario
# per room). Not a baseline; it measures nothing.
scenario_s05_03 = ScenarioConfig(
    id="scenario_s05_03",
    setup="env_setup_05",
    reference_layouts=["env_layout_03"],
    description=(
        "The second milestone scenario of T-G stage 1, one per room, identical in content in the three rooms: it "
        "exercises what the first milestone (scenario_s05_02) did not: the human's walk to the standby place between "
        "scans, the robot arriving with a pallet at a bay where the human stands, two scans possible at once in one "
        "bay, and the frozen bay, which makes the three rooms differ. It measures nothing. "
        "The robot delivers pallet_0 and pallet_1 to the dry bay and pallet_2 to the frozen bay, and returns the "
        "empty pallet_4 to the truck; the human scans the three delivered pallets (the script lists the two of the "
        "dry bay first; an entry is taken when applicable), takes the standby entry whenever no scan is applicable, "
        "and closes at the desk. The script is declared dependent on the robot (each scan waits for its delivery). "
        "Contains behaviour with no hypothesis in the robot's task model: the walk to and the stay at the standby "
        "place, and the walk to the desk (unmodelled behaviour)."
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
                    confirm_delivered_pallet("pallet_2"),
                    RepeatableEntry(go_to("standby_place")),
                ],
                closing=[go_to("desk")],
                dependence=ScriptDependence.ON_ROBOT,
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
                deliver_pallet("pallet_0"),
                deliver_pallet("pallet_1"),
                deliver_pallet("pallet_2"),
                load_return("pallet_4"),
            ],
        ),
    ],
)
