# domains/kitting/domain.py
"""
Assembles the kitting DomainModel from tasks and actions.
Entry point: build_kitting_domain()
Called once at startup by KnowledgeBase via sim_model.py.
"""

from shared.types import DomainModel
from domains.kitting.actions import move_to, pick_up, place, wait_at
from domains.kitting.tasks import deliver_item, coffee_break, ac_activation
from domains.kitting.scenarios import scenario_10

def register_kitting_domain() -> DomainModel:
    return DomainModel(
        tasks={
            "deliver_item":  deliver_item,
            "coffee_break":  coffee_break,
            "ac_activation": ac_activation,
        },
        actions={
            "move_to":   move_to,
            "pick_up":   pick_up,
            "place":     place,
            "wait_at":   wait_at,
        },
        microactions=["STEP", "GRASP", "RELEASE", "STAND"],
        intentions={"deliver_item", "coffee_break", "ac_activation"},
    )
    

domain_config = {
    "register_fn": register_kitting_domain,
    "layouts": {
        "env_layout1": {
            "path":      "domains/kitting/env_layout1.json",
            "scenarios": {
                "scenario_10": scenario_10,
            },
        },
    },
}