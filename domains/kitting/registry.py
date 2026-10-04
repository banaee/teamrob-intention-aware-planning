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
from domains.kitting.actions import move_to, pick_up, place, wait_at, switch_on, stand
from domains.kitting.facts import AC_ON, BREAK_TIME, ROOM_WARM
from domains.kitting.tasks import deliver_item, coffee_break, ac_activation, go_to, stand_task, go_to_and_stand
import domains.kitting.scenarios as _scenarios

def register_kitting_domain() -> Tree:
    return Tree(
        tasks=[deliver_item, coffee_break, ac_activation, go_to, stand_task, go_to_and_stand],
        actions=[move_to, pick_up, place, wait_at, switch_on, stand],
        microactions=["STEP", "GRASP", "RELEASE", "STAND"],
    )


_HERE = Path(__file__).parent

domain_config = {
    "register_fn": register_kitting_domain,
    # The task model every robot is given (T-H): every WorkTask and the
    # PersonalTasks it foresees; no HumanOnlyTask.
    "task_model":  [deliver_item, coffee_break, ac_activation],
    # The object states the domain declares (T-G A5): the A/C switch's (T-K part 1, AM18).
    "states":      [AC_ON],
    # The three artefacts of a run (T-L, stage 2): layouts and setups are
    # registered by the files in their folders, the scenarios by discovery
    # over the scenarios package (domains/discovery.py) — no hand-written
    # list, a duplicate scenario id is an error at import. env_layout6.json
    # and env_layout99.json stay at the domain root, unsplit and unregistered.
    # The timeline facts (T-K part 1; P3, X5): facts about no object that hold
    # only on the ticks of a window of the timeline in force (AM40); no condition
    # of a schema names one (the loader checks it).
    "timeline_facts": [BREAK_TIME, ROOM_WARM],
    "layouts":   discover_files(_HERE / "layouts"),
    "setups":    discover_files(_HERE / "setups"),
    "scenarios": discover_scenarios(_scenarios),
}
