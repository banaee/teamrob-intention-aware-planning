"""
shared/completion_memory.py

PURPOSE:
    The memory of observed completions (T-K part 1, AM27, AM30, AM33, AM47): a
    component of the robot's mind, outside the recognizer, that records the tick
    of each observed completion of a foreseeable task that declares a recency
    duration. The recency facts the recognizer's prior reads are derived from
    it, on each run, as an input (AM30); the recognizer stores nothing of it.

WHAT AN OBSERVED COMPLETION IS (AM33, AM47):
    The task's terminal fact in the robot's world state, for example
    waited(agent, machine), read through the planner's decomposition of each of
    the task's hypotheses for the observed agent (the query the recognizer's pin
    uses): recorded at the tick on which the terminal fact holds after a tick
    on which it did not. One already holding at the robot's first observation
    is not recorded, nor is a fact whose previous tick could not be read (the
    hypothesis was not applicable then). Completion counts, not admission; a
    completion the robot does not observe, and a task cut before its
    completion, produce none. Whoever did it: the terminal fact is a fact of the
    world (the pin's reading, T-D L4).

THE RECENCY FACT (AM14, AM46, AM47):
    recent_f holds at tick t iff 0 <= t - t_f_obs < d_f, t_f_obs the tick of the
    last observed completion of f and d_f its recency duration in ticks, the
    body's conversion of the declared physical duration (passed in at
    construction: shared/ holds no unit-scale value).

USED BY:
    - mesa_sim/sim_agents.py (RobotAgent): observe() before the recognizer runs,
      recent() handed to IntentionRecognizer.update().
"""

from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Tuple

from shared.knowledge import TaskModel
from shared.planner import AdaptivePlanner, DecompositionError
from shared.types import PersonalTask, TaskInstance, WorldState


@dataclass
class _Hypothesis:
    """One hypothesis of a remembered task: its task instance, and whether its terminal fact held on the previous
    observed tick (None: not read, before the first observation or while not applicable)."""
    instance: TaskInstance
    held: Optional[bool] = None


@dataclass
class _Entry:
    """One remembered foreseeable task: its hypotheses, its recency duration in ticks, the tick of its last observed
    completion."""
    task: PersonalTask
    duration_ticks: int
    hypotheses: List[_Hypothesis] = field(default_factory=list)
    completed_at: Optional[int] = None


class ObservedCompletions:
    """
    Built per robot for its observed agent, with the robot's task model and, per foreseeable task that declares a
    recency duration, that duration in ticks and the task's hypotheses (as TaskInstances, the recognizer's
    HypothesisKey.task_instance()). Tasks are compared by identity.
    """

    def __init__(self, task_model: TaskModel,
                 remembered: Sequence[Tuple[PersonalTask, int, Sequence[TaskInstance]]]):
        self._planner = AdaptivePlanner(knowledge=task_model)
        self._entries: List[_Entry] = []
        for task, ticks, instances in remembered:
            if isinstance(ticks, bool) or not isinstance(ticks, int) or ticks <= 0:
                raise ValueError(f"'{task.name}': a recency duration in ticks is a positive integer, not {ticks!r}")
            if any(e.task is task for e in self._entries):
                raise ValueError(f"'{task.name}' is remembered twice")
            self._entries.append(_Entry(task, ticks, [_Hypothesis(i) for i in instances]))

    def observe(self, agent_id: str, world: WorldState) -> None:
        """Read the terminal fact of every remembered hypothesis for `agent_id` in `world` (one observation per tick,
        before the recognizer runs); record a completion at this tick where it newly holds (AM47)."""
        tick = int(world.timestamp)
        for entry in self._entries:
            for hyp in entry.hypotheses:
                try:
                    actions = self._planner.decompose(hyp.instance, agent_id, world)
                except DecompositionError:
                    hyp.held = None          # not applicable here: its fact cannot be read
                    continue
                predicate = actions[-1].completion_predicate
                holds = predicate is not None and predicate in world.predicates
                if holds and hyp.held is False:
                    entry.completed_at = tick
                hyp.held = holds

    def recent(self, tick: int) -> Tuple[PersonalTask, ...]:
        """The tasks whose recency fact holds at `tick`: a completion at t_obs with 0 <= tick - t_obs < d. A tuple
        in declaration order (a task schema is compared by identity, never hashed)."""
        return tuple(e.task for e in self._entries
                     if e.completed_at is not None and 0 <= tick - e.completed_at < e.duration_ticks)

    def completion_of(self, task: PersonalTask) -> Optional[int]:
        """The tick of the last observed completion of `task`, or None (for tests and the log)."""
        return next((e.completed_at for e in self._entries if e.task is task), None)
