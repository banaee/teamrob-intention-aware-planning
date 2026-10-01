# domains/dock_loading/scenarios/scenarios_s02.py
"""
Dock_loading scenarios on env_setup_02 (T-G stage 1, kind 1, written for
env_layout_02; design_decisions.md, "T-G: the second domain's rulings", B14).
One module per setup.
"""

from shared.types import AgentConfig, ScenarioConfig, Script


# A viewing fixture: the scene loads and initialises; not a baseline, not an
# IR test-bed or MPB case.
scenario_s02_01 = ScenarioConfig(
    id="scenario_s02_01",
    setup="env_setup_02",
    reference_layouts=["env_layout_02"],
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
