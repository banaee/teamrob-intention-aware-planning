# domains/dock_loading/scenarios.py
"""
Scenario definitions for the dock_loading domain.
Task assignments reference domain schemas directly — no string parsing, no YAML.
is_foreseeable is declared on TaskSchema — not repeated here.
"""

from shared.types import Var, Const, TaskInstance, AgentConfig, ScenarioConfig
from domains.dock_loading.tasks import (
    deliver_pallet, load_return, confirm_delivered_pallet, coffee_break, office_break
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
                TaskInstance(schema=office_break, bindings={}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            scheduled_tasks=[
                TaskInstance(schema=deliver_pallet, bindings={Var("?pallet"): Const("pallet_3"), Var("?delivery_bay"): Const("frozen_delivery_bay_0")}),            
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
                TaskInstance(schema=office_break, bindings={Var("?office_chair"): Const("office_chair")}),
                TaskInstance(schema=confirm_delivered_pallet, bindings={Var("?pallet"): Const("pallet_0"), Var("?delivery_bay"): Const("dry_delivery_bay_0")}),
                TaskInstance(schema=coffee_break,     bindings={Var("?coffee_machine"): Const("coffee_machine_0")}),
                TaskInstance(schema=confirm_delivered_pallet, bindings={Var("?pallet"): Const("pallet_3"), Var("?delivery_bay"): Const("frozen_delivery_bay_0")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            scheduled_tasks=[
                # Deliver full pallets: dry to dry_delivery_area
                TaskInstance(schema=deliver_pallet, bindings={Var("?pallet"): Const("pallet_0"), Var("?delivery_bay"): Const("dry_delivery_bay_0")}),
                # TaskInstance(schema=deliver_pallet, bindings={Var("?pallet"): Const("pallet_1"), Var("?delivery_bay"): Const("dry_delivery_bay_0")}),
                # Deliver full pallets: frozen to frozen_delivery_area
                TaskInstance(schema=deliver_pallet, bindings={Var("?pallet"): Const("pallet_3"), Var("?delivery_bay"): Const("frozen_delivery_bay_0")}),
                # TaskInstance(schema=deliver_pallet, bindings={Var("?pallet"): Const("pallet_4"), Var("?delivery_bay"): Const("frozen_delivery_bay_0")}),
                # Load empty pallets back to truck
                TaskInstance(schema=load_return, bindings={Var("?pallet"): Const("pallet_6")}), # 6 is innitially empty ib empty_bay_dry
                TaskInstance(schema=load_return, bindings={Var("?pallet"): Const("pallet_8")}), # 8 is innitially empty in empty_bay_frozen
            ],
            observes=["human_0"],
        ),
    ],
)
