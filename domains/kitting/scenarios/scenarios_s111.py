from shared.types import AgentConfig, ScenarioConfig, Script
from domains.kitting.script import deliver_item, go_to, go_to_and_stand, stand
from shared.types import Timeline
from domains.kitting.script import window
from domains.kitting.facts import BREAK_TIME, ROOM_WARM

_UNPERFORMED = [deliver_item("item_12", table="kitting_table_0")]


scenario_s111_01 = ScenarioConfig(
    id="scenario_s111_01",
    setup="env_setup_111",
    reference_layouts=["env_layout_12"],
    description="",
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
                deliver_item("item_8"),
                deliver_item("item_9"),
            ],
            observes=["human_0"],
        ),
    ],
)


scenario_s111_02 = ScenarioConfig(
    id="scenario_s111_02",
    setup="env_setup_111",
    reference_layouts=["env_layout_12"],
    description="",
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
                deliver_item("item_10"),
                deliver_item("item_11"),
            ],
            observes=["human_0"],
        ),
    ],
)


scenario_s111_03 = ScenarioConfig(
    id="scenario_s111_03",
    setup="env_setup_111",
    reference_layouts=["env_layout_12"],
    description="",
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
                deliver_item("item_8"),
                deliver_item("item_9"),
            ],
            observes=["human_0"],
        ),
    ],
)


scenario_s111_04 = ScenarioConfig(
    id="scenario_s111_04",
    setup="env_setup_111",
    reference_layouts=["env_layout_12"],
    timeline=Timeline((window(BREAK_TIME, 0, 61),)),
    description="",
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
                deliver_item("item_8"),
                deliver_item("item_9"),
            ],
            observes=["human_0"],
        ),
    ],
)


scenario_s111_05 = ScenarioConfig(
    id="scenario_s111_05",
    setup="env_setup_111",
    reference_layouts=["env_layout_12"],
    timeline=Timeline((window(BREAK_TIME, 0, 21),)),
    description="",
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
                deliver_item("item_10"),
                deliver_item("item_11"),
            ],
            observes=["human_0"],
        ),
    ],
)


scenario_s111_06 = ScenarioConfig(
    id="scenario_s111_06",
    setup="env_setup_111",
    reference_layouts=["env_layout_12"],
    timeline=Timeline((window(BREAK_TIME, 0, 61),)),
    description="",
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
                deliver_item("item_8"),
                deliver_item("item_9"),
            ],
            observes=["human_0"],
        ),
    ],
)
