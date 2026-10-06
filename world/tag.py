"""
world/tag.py

PURPOSE:
    The tag per task (Hadi, 5 October 2026; design_records.md, "T-F part 1", THE TAG PER TASK; glossary §7): the one
    definition, read by the analyses (analysis/instruments/mpb/tag.py, from a run's log and record) and by the web-ui's
    piece (mesa_sim/webui_adapter.py, from the running model). Each task the human performs gets one tag by the facts in
    force at its first tick:
    - in accord: a fact holds, and the human performs the task the fact makes more likely;
    - not in accord: a fact holds, and the human performs another task;
    - no fact: no fact holds.
    A label of the world: it compares what the human does with what the facts suggest. The robot never has it.

THE RULE:
    "The task a fact makes more likely": the foreseeable tasks at the raised level of the domain's declared context
    knowledge (`ContextKnowledge.level`, AM36: the suppressing condition first, then the raising, else ordinary),
    evaluated on the world's facts at the task's first tick: the timeline facts in force (the run's windows) and the
    recency facts of the foreseeable tasks the human completed (its record: a completion's tick and the task's recency
    duration in ticks, half-open, the completion tick included, AM46, AM47). Object states are not read (no raising
    condition of kitting or dock_loading names one). The raised task comes from the declarations, never from a name.

    PROVISIONAL (ccode, 6 October 2026; TODO-185, for Hadi's confirmation; followed as preferred by Hadi, 6 October
    2026, T-viz 1a): a fact that lowers a task gives no tag. The tag reads the raised level only; a task that starts
    while only a lowering fact holds is tagged "no fact". The tasks at the suppressed level are returned beside the tag
    (`lowered`), so the case stays visible.

    A task the human performs: one stretch of one task on top of the human's stack (a task resumed after a cut is a new
    stretch, tagged at its resumption; the same top on consecutive ticks is one stretch; an empty stack ends one).

WHAT THIS MODULE DOES NOT DO:
    - It reads no log, no record and no model: its callers hand it the facts, the completions and the tops of the stack
    - Nothing of the robot's mind: the declared context knowledge is the domain's declaration, read as data
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence, Set, Tuple

from shared.knowledge import ContextKnowledge, StrengthLevel
from shared.types import Predicate, TaskSchema


class Tag(Enum):
    IN_ACCORD = "in accord"
    NOT_IN_ACCORD = "not in accord"
    NO_FACT = "no fact"


@dataclass(frozen=True)
class TaskTag:
    """A task's tag, and the foreseeable tasks at the raised and at the suppressed level at its first tick."""
    tag: Tag
    raised: Tuple[TaskSchema, ...]
    lowered: Tuple[TaskSchema, ...]


def recent_tasks(knowledge: ContextKnowledge, completions: Sequence[Tuple[int, TaskSchema]],
                 recency_ticks: Sequence[Tuple[TaskSchema, int]], tick: int) -> Tuple[TaskSchema, ...]:
    """The foreseeable tasks whose recency fact holds at `tick`: completed at a tick c with c <= tick < c + d, d the
    task's recency duration in ticks (the body's conversion of the declared duration). Matched by identity."""
    out = []
    for e in knowledge.entries():
        d = next((n for task, n in recency_ticks if task is e.task), None)
        if e.recency is None or d is None:
            continue
        if any(task is e.task and c <= tick < c + d for c, task in completions):
            out.append(e.task)
    return tuple(out)


def tag_at(knowledge: ContextKnowledge, performed: TaskSchema, facts: Set[Predicate],
           recent: Sequence[TaskSchema]) -> TaskTag:
    """The tag of the task `performed`, by the facts in force at its first tick: the timeline facts `facts` and the
    recency facts of `recent`."""
    levels = [(e.task, knowledge.level(e.task, facts, recent)) for e in knowledge.entries()]
    raised = tuple(t for t, level in levels if level is StrengthLevel.RAISED)
    lowered = tuple(t for t, level in levels if level is StrengthLevel.SUPPRESSED)
    if not raised:
        tag = Tag.NO_FACT
    elif any(performed is t for t in raised):
        tag = Tag.IN_ACCORD
    else:
        tag = Tag.NOT_IN_ACCORD
    return TaskTag(tag, raised, lowered)


class Stretches:
    """The stretches of the top of the human's stack, fed tick by tick in order: `at` gives the first tick of the
    stretch whose task is on top at the tick, None when the stack is empty. Two tops are the same task when their keys
    are equal (the record's label of the task instance, `shared.types.task_instance_key`)."""

    def __init__(self):
        self._top: Optional[str] = None
        self._start: Optional[int] = None

    def at(self, tick: int, top: Optional[str]) -> Optional[int]:
        if top is None:
            self._top = self._start = None
        elif top != self._top:
            self._top, self._start = top, tick
        return self._start
