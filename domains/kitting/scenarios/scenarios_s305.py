# domains/kitting/scenarios/scenarios_s305.py
"""
Kitting scenarios on env_setup_305, a copy of Hadi's env_setup_302 (T-pres, the deck's replays; design_records.md,
"T-pres, the talk", NEW SCENARIOS FOR THE REPLAYS): copies of Hadi's scenarios under new ids, his own files untouched;
outside every measured set. The room is env_layout_12.
_01: scenario_s302_02 with the robot starting at (300, 60) instead of (390, 160), so that its carry from shelf_5 to
kitting_table_3 meets her carry from shelf_1 to kitting_table_0 at the room's crossing: intention-unaware, the robot
holds against the projection from her motion (talk stage 2, the reactive robot). In scenario_s302_02 the two pass 60 cm
apart and no hold is decided. The robot's start was chosen from a grid of starts run with the override
scenario.robot_0.start_position (the longest hold of the grid); what the robot then does is the framework's own result.
"""

from shared.types import AgentConfig, ScenarioConfig, Script
from domains.kitting.script import deliver_item


scenario_s305_01 = ScenarioConfig(
    id="scenario_s305_01",
    setup="env_setup_305",
    reference_layouts=["env_layout_12"],
    description=(
        "scenario_s305_01: T-pres, talk stage 2: scenario_s302_02 with the robot's start moved to (300, 60), so that its "
        "carry meets hers at the crossing and the reactive robot holds."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(-240, 220),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(300, 60),
            assigned_tasks=[deliver_item("item_7", table="kitting_table_3")],
            observes=["human_0"],
        ),
    ],
)
