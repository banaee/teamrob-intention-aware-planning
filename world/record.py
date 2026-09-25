"""
world/record.py

PURPOSE:
    The human executor's record (T-H, item 7; built in T-H2): the ground truth
    of what the human was doing at each tick, as a decision, not as a body
    position. Per tick a Snapshot: the stack (top first), the action in hand and
    its progress; and the transitions the stack made on that tick, each typed.
    Written by the embodiment's human driver (mesa_sim/sim_agents.HumanAgent)
    and by the load-time replay (domains/human_executor.check_script); streamed
    as one `[rec]` line per tick in a file beside the run log, diffed in the
    sweep. Its typed queries (switches, resumptions, assigned, unperformed,
    coverage, truth_at) are T-H4's and are not here.

WHAT THIS MODULE DOES NOT DO:
    - Nothing here reaches the robot's mind: world_state_builder and obs_builder
      read none of it (tests/test_th2_executor.py guards that). truth_at enters
      the mind only through the oracle condition's explicit adapter (TODO-101).
    - No body unit is interpreted: `done` and `total` are the body's ticks of the
      action as the body counts them; an exporter converts once (Phase 7).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Union

from shared.types import Decision, Event, GroundedAction, TaskInstance, Trigger, task_instance_key


class Outcome(Enum):
    """Of a task leaving the stack (or being pushed down): computed from what the
    stack did and the world, never authored."""
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    ABANDONED = "abandoned"
    INFEASIBLE = "infeasible"


class RefusalReason(Enum):
    STACK_FULL = "stack_full"      # a Start while a task is already suspended (one level, TODO-100)
    EMPTY_STACK = "empty_stack"    # a Drop with nothing on the stack


class UnfiredReason(Enum):
    """Why an authored event never fired: at load each is an error; at run time,
    recorded (the run may differ from the load-time replay by the robot's effects)."""
    ANCHOR_ABSENT = "anchor_absent"          # the action is not in the (re-)expansion
    ANCHOR_AMBIGUOUS = "anchor_ambiguous"    # the action occurs more than once and no occurrence was given
    ANCHOR_OUT_OF_RANGE = "anchor_out_of_range"
    NEVER_REACHED = "never_reached"          # the task left the stack before the anchor
    PAST_ACTION = "past_action"              # a during whose time is not inside the action


@dataclass(frozen=True)
class Where:
    """Where on an entry's expansion a decision was taken. Not constructed directly."""
    def __post_init__(self):
        if type(self) is Where:
            raise TypeError("Where is not constructed directly: write Boundary or Cut")


@dataclass(frozen=True)
class Boundary(Where):
    """After `action` (the k-th occurrence) completed."""
    action: GroundedAction
    occurrence: int

    def __repr__(self):
        return f"after({self.action.action_name}#{self.occurrence})"


@dataclass(frozen=True)
class Beginning(Where):
    """Before the task's first action (an injection on a task not yet begun)."""

    def __repr__(self):
        return "beginning"


@dataclass(frozen=True)
class Cut(Where):
    """Inside `action` (the k-th occurrence), `done` of the body's ticks of it
    executed. What an exporter needs to rewrite Now as during (Phase 7)."""
    action: GroundedAction
    occurrence: int
    done: int

    def __repr__(self):
        return f"in({self.action.action_name}#{self.occurrence},{self.done})"


@dataclass(frozen=True)
class Snapshot:
    """One tick: the stack top first; the action in hand (or the one being
    acknowledged) with its occurrence and progress; None and 0/0 when idle."""
    tick: int
    stack: List[TaskInstance]
    action: Optional[GroundedAction]
    occurrence: int
    done: int
    total: int


@dataclass(frozen=True)
class Transition:
    """A change of the stack on one tick. Not constructed directly."""
    tick: int

    def __post_init__(self):
        if type(self) is Transition:
            raise TypeError("Transition is not constructed directly")


@dataclass(frozen=True)
class Started(Transition):
    """`task` pushed on the stack by `trigger`; `where` on the task below it
    (None: pushed on an empty stack, a plain entry)."""
    task: TaskInstance
    trigger: Trigger
    where: Optional[Where]

    def __repr__(self):
        return f"started:{task_instance_key(self.task)}:{self.trigger!r}" + (f":{self.where!r}" if self.where else "")


@dataclass(frozen=True)
class Entered(Transition):
    """A script entry's task pushed on the empty stack, in script order."""
    task: TaskInstance

    def __repr__(self):
        return f"entered:{task_instance_key(self.task)}"


@dataclass(frozen=True)
class Resumed(Transition):
    task: TaskInstance

    def __repr__(self):
        return f"resumed:{task_instance_key(self.task)}"


@dataclass(frozen=True)
class Left(Transition):
    """`task` left the top of the stack (COMPLETED, ABANDONED, INFEASIBLE) or was
    pushed down (SUSPENDED)."""
    task: TaskInstance
    outcome: Outcome

    def __repr__(self):
        return f"{self.outcome.value}:{task_instance_key(self.task)}"


@dataclass(frozen=True)
class Refused(Transition):
    decision: Decision
    reason: RefusalReason

    def __repr__(self):
        return f"refused:{self.decision!r}:{self.reason.value}"


@dataclass(frozen=True)
class Unfired(Transition):
    task: TaskInstance
    event: Event
    reason: UnfiredReason

    def __repr__(self):
        return f"unfired:{task_instance_key(self.task)}:{self.event!r}:{self.reason.value}"


@dataclass
class Record:
    snapshots: List[Snapshot] = field(default_factory=list)
    transitions: List[Transition] = field(default_factory=list)

    def add(self, transition: Transition) -> None:
        self.transitions.append(transition)

    def snapshot(self, snap: Snapshot) -> None:
        self.snapshots.append(snap)

    def transitions_at(self, tick: int) -> List[Transition]:
        return [t for t in self.transitions if t.tick == tick]

    def line(self, tick: int) -> str:
        """The `[rec]` line of `tick`: its snapshot (the last taken for that
        tick) and its transitions, in order."""
        snap = next((s for s in reversed(self.snapshots) if s.tick == tick), None)
        stack = ";".join(task_instance_key(t) for t in snap.stack) if snap and snap.stack else "-"
        action = f"{snap.action.action_name}#{snap.occurrence}" if snap and snap.action is not None else "-"
        progress = f"{snap.done}/{snap.total}" if snap else "0/0"
        events = ",".join(repr(t) for t in self.transitions_at(tick)) or "-"
        return f"[rec] step={tick} stack={stack} action={action} progress={progress} events={events}"
