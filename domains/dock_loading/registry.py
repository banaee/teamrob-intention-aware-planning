# domains/dock_loading/registry.py
"""
Assembles the dock_loading DomainModel from tasks and actions.
Entry point: register_dock_loading_domain()
Called once at startup by DomainKnowledgeBase via sim_model.py.
"""

from shared.types import DomainModel
from domains.dock_loading.actionOperators import move_to, pick_up, place, wait_at, scan_pallet
from domains.dock_loading.tasks import deliver_pallet, load_return, scan_pallet_task, coffee_break


def register_dock_loading_domain() -> DomainModel:
    return DomainModel(
        tasks={
            "deliver_pallet": deliver_pallet,
            "load_return":    load_return,
            "scan_pallet":    scan_pallet_task,
            "coffee_break":   coffee_break,
        },
        actions={
            "move_to":      move_to,
            "pick_up":      pick_up,
            "place":        place,
            "wait_at":      wait_at,
            "scan_pallet":  scan_pallet,
        },
        microactions=["STEP", "GRASP", "RELEASE", "STAND", "TOUCH"],
        intentions={"deliver_pallet", "load_return", "scan_pallet", "coffee_break"},
    )
