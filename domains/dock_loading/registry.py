# domains/dock_loading/registry.py
"""
Assembles the dock_loading DomainModel from tasks and actions.
Entry point: register_dock_loading_domain()
Called once at startup by DomainKnowledgeBase via sim_model.py.
"""

from shared.types import DomainModel
from domains.dock_loading.actionOperators import move_to, pick_up, place, wait_at, scan_it
from domains.dock_loading.tasks import deliver_pallet, load_return, confirm_delivered_pallet, coffee_break, go_to_office


def register_dock_loading_domain() -> DomainModel:
    return DomainModel(
        tasks={
            "deliver_pallet": deliver_pallet,
            "load_return":    load_return,
            "confirm_delivered_pallet": confirm_delivered_pallet,
            "coffee_break":   coffee_break,
            "go_to_office":   go_to_office,
        },
        actions={
            "move_to":      move_to,
            "pick_up":      pick_up,
            "place":        place,
            "wait_at":      wait_at,
            "scan_it":      scan_it,
        },
        microactions=["STEP", "GRASP", "RELEASE", "STAND", "TOUCH"],
        intentions={"deliver_pallet", "load_return", "confirm_delivered_pallet", "coffee_break", "go_to_office"},
    )
