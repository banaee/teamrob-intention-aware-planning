# domains/dock_loading/registry.py
"""
Assembles the dock_loading tree of task schemas (T-H) from tasks and actions,
and declares the task model a robot is given.
Entry point: register_dock_loading_domain()
Called once at startup by sim_model.py.
"""

from shared.knowledge import Tree
from domains.dock_loading.actions import move_to, pick_up, place, wait_at, scan_it
from domains.dock_loading.tasks import deliver_pallet, load_return, confirm_delivered_pallet, coffee_break, office_break
from domains.dock_loading.scenarios import scenario_10, scenario_11

def register_dock_loading_domain() -> Tree:
    return Tree(
        tasks=[deliver_pallet, load_return, confirm_delivered_pallet, coffee_break, office_break],
        actions=[move_to, pick_up, place, wait_at, scan_it],
        microactions=["STEP", "GRASP", "RELEASE", "STAND", "TOUCH"],
    )


domain_config = {
    "register_fn": register_dock_loading_domain,
    # The task model every robot is given (T-H).
    "task_model":  [deliver_pallet, load_return, confirm_delivered_pallet, coffee_break, office_break],
    # The three artefacts of a run (T-L, stage 1): layouts and setups by id and
    # file; the scenarios flat — each declares its setup and reference layouts.
    "layouts": {
        "env_layout1": "domains/dock_loading/env_layout1.json",
    },
    "setups": {
        "env_setup1": "domains/dock_loading/env_setup1.json",
    },
    "scenarios": {
        "scenario_10": scenario_10,
        "scenario_11": scenario_11,
    },
}