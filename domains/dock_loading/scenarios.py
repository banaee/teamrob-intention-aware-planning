# domains/dock_loading/scenarios.py
"""
Scenario definitions for the dock_loading domain.
Task assignments reference domain schemas directly — no string parsing, no YAML.
is_foreseeable is declared on TaskSchema — not repeated here.
"""

from shared.types import Var, Const, TaskInstance, AgentConfig, ScenarioConfig
from domains.dock_loading.tasks import (
    deliver_pallet, load_return, scan_pallet_task, coffee_break
)


scenario_01 = ScenarioConfig(
    id="scenario_01",
    name="basic_dock_loading_with_coffee_break",
    description=(
        "Robot delivers 6 full pallets from truck to hall (3 dry, 3 frozen), "
        "then loads 4 empty pallets from bays back to truck. "
        "Human scans each delivered pallet. "
        "Human takes a coffee break after the 2nd scan (3rd task slot)."
    ),
    env_layout="env_layout1",
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            assigned_tasks=[
                TaskInstance(schema=coffee_break,     bindings={}),
                TaskInstance(schema=scan_pallet_task, bindings={Var("?pallet"): Const("pallet_0")}),
                TaskInstance(schema=scan_pallet_task, bindings={Var("?pallet"): Const("pallet_1")}),
                TaskInstance(schema=coffee_break,     bindings={}),
                TaskInstance(schema=scan_pallet_task, bindings={Var("?pallet"): Const("pallet_2")}),
                TaskInstance(schema=scan_pallet_task, bindings={Var("?pallet"): Const("pallet_3")}),
                TaskInstance(schema=scan_pallet_task, bindings={Var("?pallet"): Const("pallet_4")}),
                TaskInstance(schema=scan_pallet_task, bindings={Var("?pallet"): Const("pallet_5")}),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            assigned_tasks=[
                # Deliver full pallets: dry to dry_delivery_area
                TaskInstance(schema=deliver_pallet, bindings={Var("?pallet"): Const("pallet_0"), Var("?dest"): Const("dry_delivery_area")}),
                TaskInstance(schema=deliver_pallet, bindings={Var("?pallet"): Const("pallet_1"), Var("?dest"): Const("dry_delivery_area")}),
                # Deliver full pallets: frozen to frozen_delivery_area
                TaskInstance(schema=deliver_pallet, bindings={Var("?pallet"): Const("pallet_3"), Var("?dest"): Const("frozen_delivery_area")}),
                TaskInstance(schema=deliver_pallet, bindings={Var("?pallet"): Const("pallet_4"), Var("?dest"): Const("frozen_delivery_area")}),
                # Load empty pallets back to truck
                TaskInstance(schema=load_return, bindings={Var("?pallet"): Const("pallet_6")}),
                TaskInstance(schema=load_return, bindings={Var("?pallet"): Const("pallet_8")}),
            ],
            observes=["human_0"],
        ),
    ],
)
