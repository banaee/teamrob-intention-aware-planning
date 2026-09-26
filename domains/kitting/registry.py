# domains/kitting/registry.py
"""
Assembles the kitting tree of task schemas (T-H) from tasks and actions, and
declares the task model a robot is given.
Entry point: register_kitting_domain()
Called once at startup by sim_model.py.
"""

from pathlib import Path

from shared.knowledge import Tree
from domains.discovery import discover_files, discover_scenarios
from domains.kitting.actions import move_to, pick_up, place, wait_at, stand
from domains.kitting.tasks import deliver_item, coffee_break, ac_activation, go_to, stand_task, go_to_and_stand
import domains.kitting.scenarios as _scenarios

def register_kitting_domain() -> Tree:
    return Tree(
        tasks=[deliver_item, coffee_break, ac_activation, go_to, stand_task, go_to_and_stand],
        actions=[move_to, pick_up, place, wait_at, stand],
        microactions=["STEP", "GRASP", "RELEASE", "STAND"],
    )


_HERE = Path(__file__).parent

domain_config = {
    "register_fn": register_kitting_domain,
    # The task model every robot is given (T-H): every WorkTask and the
    # PersonalTasks it foresees; no HumanOnlyTask.
    "task_model":  [deliver_item, coffee_break, ac_activation],
    # The three artefacts of a run (T-L, stage 2): layouts and setups are
    # registered by the files in their folders, the scenarios by discovery
    # over the scenarios package (domains/discovery.py) — no hand-written
    # list, a duplicate scenario id is an error at import. env_layout6.json
    # and env_layout99.json stay at the domain root, unsplit and unregistered.
    "layouts":   discover_files(_HERE / "layouts"),
    "setups":    discover_files(_HERE / "setups"),
    "scenarios": discover_scenarios(_scenarios),
}
