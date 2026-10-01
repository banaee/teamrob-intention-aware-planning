# domains/dock_loading/scenarios/scenarios_s03.py
"""
Dock_loading scenarios on env_setup_03 (T-G stage 1, kind 2, written for
env_layout_02; design_decisions.md, "T-G: the second domain's rulings", B14).
One module per setup.
"""

from shared.types import AgentConfig, ScenarioConfig, Script


# A viewing fixture: the scene loads and initialises; not a baseline, not an
# IR test-bed or MPB case.
scenario_s03_01 = ScenarioConfig(
    id="scenario_s03_01",
    setup="env_setup_03",
    reference_layouts=["env_layout_02"],
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
