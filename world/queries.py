"""
world/queries.py

PURPOSE:
    The typed queries on the human executor's record (T-H, item 7; built in
    T-H4): how the ground truth is read. Each answers one question the 24 Sept
    terminology had as a label: label A became `assigned` / `unperformed`,
    label B became `coverage`. Pure functions of the record and what the caller
    hands in; computed, never stored, never given to the robot.

        truth_at(record, tick)                          the stack at a tick
        switches(record)                                every applied Start
        resumptions(record)                             every resumption
        assigned(task, assigned_tasks, destinations)    the assigned task it pursues, and its departures
        unperformed(record, assigned_tasks, destinations)   assigned tasks never performed
        coverage(task, robot)                           COVERED | TASK_ABSENT | BINDING_ABSENT

    Task identity is `same_task` (shared/types.py): the same schema by identity
    and the same goal bindings; a stated determined binding that is not the
    station's is a `Departure`, the binding-level deviation.

WHERE THE ROBOT'S SIDE COMES FROM:
    `coverage` is judged against an ObservingRobot: the robot's task model, its
    hypothesis space and the station's destinations, built by the body at spawn
    (mesa_sim/sim_model.SimModel.observing) from the same objects the robot's
    mind is given. Data flows from the robot's side into the query, never back:
    shared/ never imports world/.

WHAT THIS MODULE DOES NOT DO:
    - It does not read the `.rec` stream back: the queries run on the in-memory
      Record (T-H4). Rebuilding task instances from key strings would be
      string parsing and a lookup by name.
    - It does not reach the robot's mind. truth_at enters it only through the
      oracle condition's explicit adapter (TODO-101, not built).
    - SIMULATION ONLY: a real human needs annotation of the same form.
"""

from dataclasses import dataclass
from typing import FrozenSet, List, Mapping, Optional, Sequence, Tuple

from shared.knowledge import TaskModel
from shared.recognizer import HypothesisKey
from shared.types import (
    DESTINATION_LOOKUP, Const, Departure, TaskInstance, TaskSchema, Var, destination_departures, goal_bindings,
    same_task, task_instance_key,
)
from world.record import Left, Outcome, Record, Resumed, Snapshot, Started


# =============================================================================
# the record alone
# =============================================================================

def truth_at(record: Record, tick: int) -> Snapshot:
    """The stack at `tick`, top first, with the action in hand and its
    progress: the tick's snapshot (the last one taken for it). The behaviour at
    the tick is `stack[0]`, or no task when the stack is empty."""
    snap = next((s for s in reversed(record.snapshots) if s.tick == tick), None)
    if snap is None:
        raise ValueError(f"the record has no snapshot at tick {tick}")
    return snap


def switches(record: Record) -> List[Started]:
    """Every applied Start, authored (at, during) or injected (Now), on a
    task or on the empty stack. A Drop is not a switch: it is Left(ABANDONED)."""
    return [t for t in record.transitions if isinstance(t, Started)]


def resumptions(record: Record) -> List[Resumed]:
    return [t for t in record.transitions if isinstance(t, Resumed)]


# =============================================================================
# label A: assigned, unperformed
# =============================================================================

@dataclass(frozen=True)
class Assignment:
    """
    The assigned task a task pursues: the same task (same_task: its schema and
    goal bindings). `departures` are its stated determined bindings that are not
    the station's, the bindings the assignment did not give (an assigned task's
    determined bindings are the station's, checked at load): () when the task IS
    the assigned task. deliver_item(item_1, table=kitting_table_2) against the
    assigned deliver_item(item_1): the assigned task, with one departure.
    """
    assigned: TaskInstance
    departures: Tuple[Departure, ...]

    def __repr__(self):
        return f"assigned:{task_instance_key(self.assigned)}{list(self.departures) if self.departures else ''}"


def assigned(task: TaskInstance, assigned_tasks: Sequence[TaskInstance],
             destinations: Mapping[str, str]) -> Optional[Assignment]:
    """The assigned task `task` pursues, with its departures; None when it is
    not assigned (a PersonalTask, a HumanOnlyTask, or a WorkTask instance of a
    goal the assigned tasks do not hold)."""
    match = next((a for a in assigned_tasks if same_task(a, task)), None)
    if match is None:
        return None
    return Assignment(match, _departures(task, destinations))


def unperformed(record: Record, assigned_tasks: Sequence[TaskInstance],
                destinations: Mapping[str, str]) -> List[TaskInstance]:
    """
    The assigned tasks, in assigned order, never performed: no task left the
    stack COMPLETED that is this assigned task with no departures. An abandoned
    one, one delivered elsewhere, one never begun and one the run ended in are
    unperformed; which of these is read from the record and from `assigned`.
    """
    performed: List[TaskInstance] = []
    for t in record.transitions:
        if isinstance(t, Left) and t.outcome is Outcome.COMPLETED:
            a = assigned(t.task, assigned_tasks, destinations)
            if a is not None and not a.departures:
                performed.append(a.assigned)
    return [a for a in assigned_tasks if not any(p is a for p in performed)]


# =============================================================================
# label B: coverage
# =============================================================================

@dataclass(frozen=True)
class ObservingRobot:
    """
    What coverage is judged against: an observing robot's task model and its
    hypothesis space (the whole space, not the support the assignment prior
    narrows: the prior is part of the belief, not of the model), and the
    station's destinations (object id -> its designated destination), the
    layout fact a hypothesis's determined parameters follow from. Built by the
    body at spawn from the objects the robot is given.
    """
    task_model: TaskModel
    hypotheses: FrozenSet[HypothesisKey]
    destinations: Mapping[str, str]


@dataclass(frozen=True)
class Coverage:
    """Of one task instance, against one robot. Not constructed directly."""
    def __post_init__(self):
        if type(self) is Coverage:
            raise TypeError("Coverage is not constructed directly: Covered, TaskAbsent or BindingAbsent")


@dataclass(frozen=True)
class Covered(Coverage):
    """A hypothesis of the robot's hypothesis space describes the task."""
    hypothesis: HypothesisKey

    def __repr__(self):
        return "covered"


@dataclass(frozen=True)
class TaskAbsent(Coverage):
    """The task's schema is not in the robot's task model."""
    schema: TaskSchema

    def __repr__(self):
        return "task_absent"


@dataclass(frozen=True)
class BindingAbsent(Coverage):
    """The schema is in the task model; this binding of the task is carried by
    no hypothesis."""
    var: Var
    value: Const

    def __repr__(self):
        return f"binding_absent({self.var.name}={self.value.value})"


def coverage(task: TaskInstance, robot: ObservingRobot) -> Coverage:
    """
    Whether the robot's tree contains the task's nodes, and if not at which
    level, judged per task instance (an interrupted task is judged on its own
    instance, its interruption on its own). In order:
      1. the schema is not in the task model: TaskAbsent;
      2. no hypothesis is the same task: BindingAbsent, carrying the first goal
         binding, in parameter order, that no hypothesis of the schema carries;
      3. a stated determined binding is not the station's: BindingAbsent,
         carrying it (a hypothesis carries the designated destination);
      4. Covered, with the hypothesis.
    """
    if not robot.task_model.holds(task.schema):
        return TaskAbsent(task.schema)
    hypothesis = next((h for h in robot.hypotheses if same_task(h.task_instance(), task)), None)
    if hypothesis is None:
        return _absent_goal_binding(task, robot.hypotheses)
    departures = _departures(task, robot.destinations)
    if departures:
        return BindingAbsent(departures[0].var, departures[0].stated)
    return Covered(hypothesis)


def _absent_goal_binding(task: TaskInstance, hypotheses: FrozenSet[HypothesisKey]) -> BindingAbsent:
    goal = goal_bindings(task)
    of_schema = [h for h in hypotheses if h.schema is task.schema]
    for var in task.schema.parameters:
        if var in goal and not any(h.bindings.get(var.name) == goal[var].value for h in of_schema):
            return BindingAbsent(var, goal[var])
    raise ValueError(f"{task_instance_key(task)}: no hypothesis is this task, yet every goal binding is carried by "
                     f"one: the task is not fully bound")


def _departures(task: TaskInstance, destinations: Mapping[str, str]) -> Tuple[Departure, ...]:
    """The task's departures from the station. A determined parameter follows
    only from the station's destinations here: a bound one with any other
    lookup cannot be judged, and is an error, never silently the station's."""
    for var, const in task.bindings.items():
        lookup = task.schema.determined_parameters.get(var.name)
        if lookup is not None and lookup[0] != DESTINATION_LOOKUP:
            raise TypeError(f"{task_instance_key(task)}: {var.name} is determined by '{lookup[0]}', which the "
                            f"queries cannot judge (only '{DESTINATION_LOOKUP}')")
    return destination_departures(task, destinations)
