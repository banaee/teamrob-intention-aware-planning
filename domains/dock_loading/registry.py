# domains/dock_loading/registry.py
"""
Assembles the dock_loading tree of task schemas (T-H) from tasks and actions,
and declares the task model a robot is given.
Entry point: register_dock_loading_domain()
Called once at startup by sim_model.py.
"""

from pathlib import Path

from shared.knowledge import StateDeclaration, Tree
from domains.discovery import discover_files, discover_scenarios
from domains.dock_loading.actions import move_to, pick_up, place, wait_at, scan_it, stand
from domains.dock_loading.tasks import (deliver_pallet, load_return, confirm_delivered_pallet, coffee_break,
                                        office_break, go_to, stand_task, go_to_and_stand)
import domains.dock_loading.scenarios as _scenarios

def register_dock_loading_domain() -> Tree:
    return Tree(
        tasks=[deliver_pallet, load_return, confirm_delivered_pallet, coffee_break, office_break,
               go_to, stand_task, go_to_and_stand],
        actions=[move_to, pick_up, place, wait_at, stand, scan_it],
        microactions=["STEP", "GRASP", "RELEASE", "STAND", "TOUCH"],
    )


_HERE = Path(__file__).parent

domain_config = {
    "register_fn": register_dock_loading_domain,
    # The task model every robot is given (T-H): every WorkTask and the
    # PersonalTasks it foresees; no HumanOnlyTask.
    "task_model":  [deliver_pallet, load_return, confirm_delivered_pallet, coffee_break, office_break],
    # The object states the domain declares (T-G A5); the setup's "states"
    # block states which hold at the start, the environment holds them.
    "states":      [StateDeclaration("is_empty", "pallet"), StateDeclaration("is_scanned", "pallet"),
                    StateDeclaration("is_open", "gate")],
    # The three artefacts of a run (T-L, stage 2): layouts and setups are
    # registered by the files in their folders, the scenarios by discovery
    # over the scenarios package (domains/discovery.py) — no hand-written
    # list, a duplicate scenario id is an error at import.
    # The timeline facts (T-K part 1; P3, X5): facts about no object that hold
    # only on the ticks of a window of the timeline in force (AM40); no condition
    # of a schema names one (the loader checks it).
    "timeline_facts": [],
    "layouts":   discover_files(_HERE / "layouts"),
    "setups":    discover_files(_HERE / "setups"),
    "scenarios": discover_scenarios(_scenarios),
}
