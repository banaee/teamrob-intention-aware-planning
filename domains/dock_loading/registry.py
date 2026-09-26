# domains/dock_loading/registry.py
"""
Assembles the dock_loading tree of task schemas (T-H) from tasks and actions,
and declares the task model a robot is given.
Entry point: register_dock_loading_domain()
Called once at startup by sim_model.py.
"""

from pathlib import Path

from shared.knowledge import Tree
from domains.discovery import discover_files, discover_scenarios
from domains.dock_loading.actions import move_to, pick_up, place, wait_at, scan_it
from domains.dock_loading.tasks import deliver_pallet, load_return, confirm_delivered_pallet, coffee_break, office_break
import domains.dock_loading.scenarios as _scenarios

def register_dock_loading_domain() -> Tree:
    return Tree(
        tasks=[deliver_pallet, load_return, confirm_delivered_pallet, coffee_break, office_break],
        actions=[move_to, pick_up, place, wait_at, scan_it],
        microactions=["STEP", "GRASP", "RELEASE", "STAND", "TOUCH"],
    )


_HERE = Path(__file__).parent

domain_config = {
    "register_fn": register_dock_loading_domain,
    # The task model every robot is given (T-H).
    "task_model":  [deliver_pallet, load_return, confirm_delivered_pallet, coffee_break, office_break],
    # The three artefacts of a run (T-L, stage 2): layouts and setups are
    # registered by the files in their folders, the scenarios by discovery
    # over the scenarios package (domains/discovery.py) — no hand-written
    # list, a duplicate scenario id is an error at import.
    "layouts":   discover_files(_HERE / "layouts"),
    "setups":    discover_files(_HERE / "setups"),
    "scenarios": discover_scenarios(_scenarios),
}
