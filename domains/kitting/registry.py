# domains/kitting/registry.py
"""
Assembles the kitting tree of task schemas (T-H) from tasks and actions, and
declares the task model a robot is given.
Entry point: register_kitting_domain()
Called once at startup by sim_model.py.
"""

from pathlib import Path

from shared.knowledge import (Condition, ContextKnowledge, ForeseeableKnowledge, ObjectState, RecencyDuration,
                              RecencyFact, Strength, TimelineFact, Tree)
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


# The declared context knowledge (T-K part 1, AM26, AM36 to AM38; docs/context_knowledge_method.md, section 4): the
# suppressed and the ordinary strength for every foreseeable task of the domain, and per foreseeable task its
# suppressing condition, its raising condition with its raised strength, and its recency duration (physical time, the
# body converts it). Each value is a modelling assumption with its source; none was chosen from a threshold or a
# scenario. Knowledge about the human at this kind of site: declared once here, never per setup or scenario.
_SOURCE = ("Modelling assumption, Hadi, 3 October 2026. A relative strength. Its order of magnitude is motivated by "
           "the proposed meaning of a strength (a ratio of counted task starts), which is not validated. (AM17, AM38)")
context_knowledge = ContextKnowledge(
    suppressed=Strength(0.005, _SOURCE),
    ordinary=Strength(0.02, _SOURCE),
    tasks=[
    ForeseeableKnowledge(
        task=coffee_break,
        suppressing=Condition((RecencyFact(coffee_break),)),          # just done (AM37)
        raising=Condition((TimelineFact(BREAK_TIME),)),               # the site's break time (AM37)
        raised=Strength(2.0, "Hadi, 3 October 2026 (AM38): break time favours the coffee break, more probable than an "
                             "assigned task, not as strongly as 3 stated (3 asserted 3 of 4 task starts); 2 of 3."),
        recency=RecencyDuration("PT180S", "3 times the task's declared wait (PT60S), counted from the observed "
                                          "completion (AM14, AM16): 90 ticks"),
    ),
    ForeseeableKnowledge(
        task=ac_activation,
        suppressing=Condition((ObjectState(AC_ON),)),                 # the A/C is on: pointless (AM37)
        raising=Condition((TimelineFact(ROOM_WARM),)),                # the room is warm (AM37)
        raised=Strength(0.5, "Hadi, 3 October 2026 (AM38): a warm room is a matter of comfort with no stated time, so "
                             "the human more often starts an assigned task first; the activation follows within about "
                             "3 task starts (0.2 asserted 6)."),
        recency=None,                                                  # ac_on covers it (AM37)
    ),
    ],
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
    # The declared context knowledge (T-K part 1, AM26), read by the recognizer's prior with context knowledge on.
    "context_knowledge": context_knowledge,
    "layouts":   discover_files(_HERE / "layouts"),
    "setups":    discover_files(_HERE / "setups"),
    "scenarios": discover_scenarios(_scenarios),
}
