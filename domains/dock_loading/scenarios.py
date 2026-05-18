# domains/dock_loading/scenarios.py
"""
Scenario definitions for the dock_loading domain.
Task assignments reference domain schemas directly — no string parsing, no YAML.
is_foreseeable is declared on TaskSchema — not repeated here.
"""

from shared.types import Var, Const, TaskInstance, AgentConfig, ScenarioConfig
from domains.dock_loading.tasks import (
    deliver_pallet, load_return, confirm_delivered_pallet, coffee_break, go_to_office
)


# ===============================================================
# manually defined scenarios, for only "env_layout1".
# ===============================================================
scenario_10 = ScenarioConfig(
    id="scenario_10",
    name="minimal_debug",
    description="Human goes to office. Robot delivers one pallet.",
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=[
                TaskInstance(schema=go_to_office, bindings={}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            scheduled_tasks=[
                TaskInstance(schema=deliver_pallet, bindings={Var("?item"): Const("pallet_0"), Var("?dest"): Const("dry_delivery_area")}),
            ],
            observes=["human_0"],
        ),
    ],
)


# ===============================================================
# manually defined scenarios, for only "env_layout1".
# ===============================================================
scenario_11 = ScenarioConfig(
    id="scenario_11",
    name="basic_dock_loading_with_coffee_break",
    description=(
        "Robot delivers 6 full pallets from truck to hall (3 dry, 3 frozen), "
        "then loads 4 empty pallets from bays back to truck. "
        "Human scans each delivered pallet. "
        "Human takes a coffee break after the 2nd scan (3rd task slot)."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=[
                TaskInstance(schema=go_to_office, bindings={}),
                TaskInstance(schema=confirm_delivered_pallet, bindings={Var("?item"): Const("pallet_0")}),
                TaskInstance(schema=coffee_break,     bindings={}),
                TaskInstance(schema=confirm_delivered_pallet, bindings={Var("?item"): Const("pallet_3")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            scheduled_tasks=[
                # Deliver full pallets: dry to dry_delivery_area
                TaskInstance(schema=deliver_pallet, bindings={Var("?item"): Const("pallet_0"), Var("?dest"): Const("dry_delivery_area")}),
                # TaskInstance(schema=deliver_pallet, bindings={Var("?item"): Const("pallet_1"), Var("?dest"): Const("dry_delivery_area")}),
                # Deliver full pallets: frozen to frozen_delivery_area
                TaskInstance(schema=deliver_pallet, bindings={Var("?item"): Const("pallet_3"), Var("?dest"): Const("frozen_delivery_area")}),
                # TaskInstance(schema=deliver_pallet, bindings={Var("?item"): Const("pallet_4"), Var("?dest"): Const("frozen_delivery_area")}),
                # Load empty pallets back to truck
                TaskInstance(schema=load_return, bindings={Var("?item"): Const("pallet_6")}), # 6 is innitially empty ib empty_bay_dry
                TaskInstance(schema=load_return, bindings={Var("?item"): Const("pallet_8")}), # 8 is innitially empty in empty_bay_frozen
            ],
            observes=["human_0"],
        ),
    ],
)
