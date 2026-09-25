# world/human_executor.py
"""
The human's executor (T-H, items 5 to 8; built in T-H2): the stack machine that
runs a Script, and the load-time check of a script against the sequential
expansion. World-side (world/): imports shared/ only, no body and no use case.

ONE MACHINE, TWO DRIVERS. StackMachine holds the stack (one level deep) and every
transition rule: which entry begins, which event fires on which anchor, what a
Start and a Drop do, how a suspended task resumes (the cut action first, then a
re-expansion in the resulting state), and which outcome a task gets. It expands
tasks with the planner on the tree and resolves anchors by schema identity. It
does not run actions: it hands the driver a Next (RunAction, ResumeAction, Idle)
and the driver reports back (action_done, cut, inject). Two drivers exist:
    - the body, at run time (mesa_sim/sim_agents.HumanAgent): one tick at a
      time, the shared Executor executing the microactions;
    - the symbolic replay, at load (check_script below): each action completes
      at once and the state advances by successor_state(), the derivation the
      robot's orderings are projected through.
So the run-time expansion IS the load-time one, by construction, for everything
the human decides; the two can differ only where the live world differs from
the symbolic state, i.e. by the robot's effects (an item it delivered or moved).
That divergence is recorded (Unfired, a COMPLETED resumption), never an error.

TICKS. `ticks_of` converts a DuringAction's physical time to the body's ticks; the
driver supplies it (the body converts, shared/ holds no unit). A during fires at
the start of the tick on which that many of the action's ticks are executed and
the action has ticks left; `at` fires when the action's completion has been
acknowledged. The machine never reads a clock: the driver hands it the tick for
the record.

THE RECORD. Every transition is written to the Record (shared/record.py) as it
happens; the driver writes the per-tick Snapshot. Nothing here reaches the
robot's mind.
"""

from dataclasses import dataclass, replace
from typing import Callable, List, Optional, Sequence, Tuple

from shared.planner import AdaptivePlanner, DecompositionError
from shared.projection import successor_state
from world.record import (
    Beginning, Boundary, Cut, Entered, Left, Outcome, Record, Refused, RefusalReason, Resumed, Snapshot, Started,
    Unfired, UnfiredReason, Where,
)
from shared.target_resolution import movement_target_position
from shared.types import (
    AfterAction, Decision, Drop, DuringAction, Event, GroundedAction, Now, Script, Start, TaskInstance, Trigger,
    WorldState, task_instance_key,
)


class ScriptError(ValueError):
    """The script cannot run as written: found by the load-time replay."""


class AnchorError(ValueError):
    """An anchor does not name one action of an expansion; carries why."""

    def __init__(self, reason: UnfiredReason, text: str):
        super().__init__(text)
        self.reason = reason


# =============================================================================
# anchors
# =============================================================================

def occurrence_of(actions: Sequence[GroundedAction], i: int) -> int:
    """The occurrence index of actions[i] among the actions of its schema."""
    return sum(1 for a in actions[:i] if a.schema is actions[i].schema)


def index_of(actions: Sequence[GroundedAction], action: GroundedAction) -> int:
    """The index of `action` in `actions`, by identity (the planner builds
    equal actions more than once: two walks to one table)."""
    return next(i for i, a in enumerate(actions) if a is action)


def anchor_index(actions: Sequence[GroundedAction], trigger: Trigger) -> int:
    """
    The index in `actions` an AfterAction / DuringAction anchor names: the
    occurrences of the schema by identity; exactly one when no occurrence is
    given. Raises AnchorError otherwise (absent, ambiguous, out of range).
    """
    if not isinstance(trigger, (AfterAction, DuringAction)):
        raise TypeError(f"{trigger!r} names no action")
    hits = [i for i, a in enumerate(actions) if a.schema is trigger.action]
    listing = "[" + ", ".join(f"{i}: {a.action_name}" for i, a in enumerate(actions)) + "]"
    if not hits:
        raise AnchorError(UnfiredReason.ANCHOR_ABSENT,
                          f"anchor {trigger!r}: '{trigger.action.name}' is not in the expansion {listing}")
    if trigger.occurrence is None:
        if len(hits) > 1:
            raise AnchorError(UnfiredReason.ANCHOR_AMBIGUOUS,
                              f"anchor {trigger!r}: '{trigger.action.name}' occurs at {hits}; give an occurrence; "
                              f"expansion {listing}")
        return hits[0]
    if not 0 <= trigger.occurrence < len(hits):
        raise AnchorError(UnfiredReason.ANCHOR_OUT_OF_RANGE,
                          f"anchor {trigger!r}: '{trigger.action.name}' occurs {len(hits)} time(s), at {hits}; "
                          f"expansion {listing}")
    return hits[trigger.occurrence]


# =============================================================================
# the stack
# =============================================================================

@dataclass
class Pending:
    """An unfired event with its anchor resolved against the frame's expansion."""
    event: Event
    index: int


@dataclass
class Frame:
    """
    One task on the stack. `actions` is its expansion in the world it was
    (re-)expanded in, None when it is to be (re-)expanded; `index` the action
    in hand. `cut`: it was suspended inside that action; `finishing`: the cut
    action is being completed on resumption, before the re-expansion. `events`
    are the unfired authored events (a decision's task has none); `pending`
    the ones whose anchor resolved against `actions`.
    """
    task: TaskInstance
    events: List[Event]
    actions: Optional[List[GroundedAction]] = None
    index: int = 0
    pending: Optional[List[Pending]] = None
    cut: Optional[Cut] = None
    finishing: Optional[Cut] = None
    expansions: int = 0          # how often it was expanded: a re-expansion is a resumption

    def all_done(self) -> bool:
        return self.actions is not None and self.index >= len(self.actions)


@dataclass(frozen=True)
class Next:
    """What the driver runs next. Not constructed directly."""
    def __post_init__(self):
        if type(self) is Next:
            raise TypeError("Next is not constructed directly")


@dataclass(frozen=True)
class RunAction(Next):
    action: GroundedAction
    occurrence: int


@dataclass(frozen=True)
class ResumeAction(Next):
    """Complete the cut action with what remains of it."""
    cut: Cut


@dataclass(frozen=True)
class Idle(Next):
    """The stack is empty and the script has no entry left."""


class StackMachine:

    def __init__(self, script: Script, planner: AdaptivePlanner, agent_id: str,
                 ticks_of: Callable[[str], int], record: Record):
        self.entries = list(script.entries)
        self.next_entry = 0
        self.planner = planner
        self.agent_id = agent_id
        self.ticks_of = ticks_of
        self.record = record
        self.stack: List[Frame] = []          # top last

    # ------------------------------------------------------------------
    # queries for the driver and the record
    # ------------------------------------------------------------------

    def stack_tasks(self) -> List[TaskInstance]:
        """The stack, top first."""
        return [f.task for f in reversed(self.stack)]

    def current(self) -> Optional[Tuple[GroundedAction, int]]:
        """The action in hand of the top frame with its occurrence: the cut
        action being finished, or the action at the cursor; None otherwise."""
        if not self.stack:
            return None
        top = self.stack[-1]
        if top.finishing is not None:
            return top.finishing.action, top.finishing.occurrence
        if top.actions is not None and top.index < len(top.actions):
            return top.actions[top.index], occurrence_of(top.actions, top.index)
        return None

    def cut_due(self, done: int) -> bool:
        """Whether a DuringAction on the action in hand fires at `done` executed ticks."""
        return bool(self._during_at(done))

    def refusal(self, decision: Decision) -> Optional[RefusalReason]:
        """Why `decision` would be refused now, or None. Asked by the driver
        before it stops the body for an injection."""
        if isinstance(decision, Start) and len(self.stack) >= 2:
            return RefusalReason.STACK_FULL
        if isinstance(decision, Drop) and not self.stack:
            return RefusalReason.EMPTY_STACK
        return None

    # ------------------------------------------------------------------
    # transitions
    # ------------------------------------------------------------------

    def next(self, world: WorldState, tick: int) -> Next:
        """What to run, with nothing in hand: begins entries, expands,
        resumes, completes, until an action is to run or nothing is left."""
        while True:
            if not self.stack:
                if self.next_entry >= len(self.entries):
                    return Idle()
                entry = self.entries[self.next_entry]
                self.next_entry += 1
                self.stack.append(Frame(entry.task, list(entry.events)))
                self.record.add(Entered(tick, entry.task))
                continue
            top = self.stack[-1]
            if top.finishing is not None:
                return ResumeAction(top.finishing)
            if top.actions is None:
                if not self._expand(top, world, tick):
                    continue
            if top.index < len(top.actions):
                return RunAction(top.actions[top.index], occurrence_of(top.actions, top.index))
            self._pop(top, Outcome.COMPLETED, tick)

    def action_done(self, world: WorldState, tick: int) -> None:
        """The action in hand completed and was acknowledged: fires the
        AfterAction events anchored on it, in authored order, after the frame
        is completed when it was the frame's last action (an entry's boundary
        is its last action; nothing is suspended that has nothing left)."""
        top = self.stack[-1]
        if top.finishing is not None:
            # the cut action is complete. Nothing left to do when it was the
            # last of the expansion: completed, a fact of the expansion (a
            # stand's process completion leaves no world fact to read).
            # Otherwise the task is re-expanded in the resulting state.
            last = index_of(top.actions, top.finishing.action) == len(top.actions) - 1
            top.finishing = None
            top.actions = None
            top.pending = None
            if last:
                self._pop(top, Outcome.COMPLETED, tick)
            return
        i = top.index
        action = top.actions[i]
        where = Boundary(action, occurrence_of(top.actions, i))
        top.index += 1
        batch = [p for p in top.pending if p.index == i and isinstance(p.event.trigger, AfterAction)]
        unfired = [p for p in top.pending if p.index == i and isinstance(p.event.trigger, DuringAction)]
        for p in unfired:
            self._forget(top, p)
            self.record.add(Unfired(tick, top.task, p.event, UnfiredReason.PAST_ACTION))
        for p in batch:
            self._forget(top, p)
        if top.all_done():
            self._pop(top, Outcome.COMPLETED, tick)
        for p in batch:
            self._apply(p.event, world, tick, where)

    def cut(self, world: WorldState, tick: int, done: int) -> None:
        """A DuringAction on the action in hand fires at `done` executed ticks:
        the driver has stopped the body. Applies every during event at that
        time, in authored order."""
        top = self.stack[-1]
        action, occurrence = self.current()
        where = Cut(action, occurrence, done)
        batch = self._during_at(done)
        for p in batch:
            self._forget(top, p)
        for p in batch:
            self._apply(p.event, world, tick, where)

    def inject(self, decision: Decision, world: WorldState, tick: int, done: int) -> None:
        """A live event (trigger Now). `done`: the executed ticks of the action
        in hand, 0 when none or none executed (then it is a boundary, so an
        exported replay lands on the same tick). The driver asks refusal()
        first and stops the body only for an accepted injection."""
        reason = self.refusal(decision)
        if reason is not None:
            self.record.add(Refused(tick, decision, reason))
            return
        where: Optional[Where] = None
        if self.stack:
            top = self.stack[-1]
            current = self.current()
            if done > 0 and current is not None:
                where = Cut(current[0], current[1], done)
            elif top.actions is not None and top.index > 0:
                where = Boundary(top.actions[top.index - 1], occurrence_of(top.actions, top.index - 1))
            else:
                where = Beginning()
        self._apply(Event(Now(), decision), world, tick, where)

    # ------------------------------------------------------------------
    # internals
    # ------------------------------------------------------------------

    def _during_at(self, done: int) -> List[Pending]:
        if not self.stack:
            return []
        top = self.stack[-1]
        if top.pending is None:
            return []
        if top.finishing is not None:
            i = index_of(top.actions, top.finishing.action)
        else:
            i = top.index
        return [p for p in top.pending
                if p.index == i and isinstance(p.event.trigger, DuringAction)
                and self.ticks_of(p.event.trigger.time) == done]

    def _forget(self, frame: Frame, pending: Pending) -> None:
        frame.pending.remove(pending)
        frame.events.remove(pending.event)

    def _expand(self, frame: Frame, world: WorldState, tick: int) -> bool:
        """(Re-)expand `frame` in `world`: infeasible pops it, and so does a
        resumption with nothing left to do (the task's terminal condition
        holds, whoever made it hold); else its actions and the anchors of its
        unfired events. A task's first expansion runs as written: the script
        says it is done, and the terminal condition is judged on a resumption
        only (T-H, item 6)."""
        try:
            actions = self.planner.decompose(frame.task, self.agent_id, world)
        except DecompositionError:
            self._pop(frame, Outcome.INFEASIBLE, tick)
            return False
        if frame.expansions > 0 and self.planner.is_complete(frame.task, self.agent_id, world):
            self._pop(frame, Outcome.COMPLETED, tick)
            return False
        frame.expansions += 1
        frame.actions = actions
        frame.index = 0
        frame.pending = []
        for event in list(frame.events):
            try:
                frame.pending.append(Pending(event, anchor_index(actions, event.trigger)))
            except AnchorError as e:
                frame.events.remove(event)
                self.record.add(Unfired(tick, frame.task, event, e.reason))
        return True

    def _pop(self, frame: Frame, outcome: Outcome, tick: int) -> None:
        """`frame` leaves the stack with `outcome`; its unfired events are
        recorded; the frame below, if any, is resumed."""
        assert self.stack[-1] is frame
        self.stack.pop()
        self.record.add(Left(tick, frame.task, outcome))
        for event in frame.events:
            self.record.add(Unfired(tick, frame.task, event, UnfiredReason.NEVER_REACHED))
        if self.stack:
            below = self.stack[-1]
            self.record.add(Resumed(tick, below.task))
            if below.cut is not None:
                below.finishing = below.cut
                below.cut = None
            else:
                below.actions = None
                below.pending = None

    def _apply(self, event: Event, world: WorldState, tick: int, where: Optional[Where]) -> None:
        decision = event.decision
        reason = self.refusal(decision)
        if reason is not None:
            self.record.add(Refused(tick, decision, reason))
            return
        if isinstance(decision, Start):
            if self.stack:
                top = self.stack[-1]
                self.record.add(Left(tick, top.task, Outcome.SUSPENDED))
                if isinstance(where, Cut):
                    top.cut = where
                    top.finishing = None
            self.stack.append(Frame(decision.task, []))
            self.record.add(Started(tick, decision.task, event.trigger, where))
            return
        if isinstance(decision, Drop):
            self._pop(self.stack[-1], Outcome.ABANDONED, tick)
            return
        raise TypeError(f"{decision!r} is neither a Start nor a Drop")


# =============================================================================
# the load-time check: the symbolic replay
# =============================================================================

def advance(world: WorldState, actions: Sequence[GroundedAction], agent_id: str) -> WorldState:
    """The symbolic state `actions` leave `world` in for `agent_id`: the
    successor state, the agent at the target of its last walk. A new value."""
    end_pos = None
    for action in actions:
        if action.schema.movement_target_key is not None:
            end_pos = movement_target_position(action, world) or end_pos
    return successor_state(world, actions, agent_id, end_pos)


def action_ticks(action: GroundedAction, world: WorldState, agent_pos: Tuple[float, float],
                 ticks_of: Callable[[str], int],
                 walk: Callable[[Tuple[float, float], Tuple[float, float]], List[Tuple[float, float]]]) -> int:
    """
    The body's ticks of `action` from `agent_pos` in `world`, read from what the
    schema declares: a walk's step positions (`walk`, the body's), a duration
    (`ticks_of`, the body's), or the declared microaction list.
    """
    schema = action.schema
    if schema.movement_target_key is not None:
        target = movement_target_position(action, world)
        if target is None:
            raise ScriptError(f"{action.action_name}: its target has no position in the world")
        return len(walk(agent_pos, target))
    if schema.duration_key is not None:
        return ticks_of(action.bindings[schema.duration_key])
    if isinstance(schema.microactions, list):
        return len(schema.microactions)
    raise ScriptError(f"{action.action_name}: the body's tick count of '{schema.microactions}' is not known here")


def check_script(script: Script, planner: AdaptivePlanner, world: WorldState, agent_id: str,
                 ticks_of: Callable[[str], int],
                 walk: Callable[[Tuple[float, float], Tuple[float, float]], List[Tuple[float, float]]]) -> Record:
    """
    The load-time replay: drives the StackMachine through the whole script with
    a symbolic body. Each action completes at once, the state advancing by
    successor_state(); a DuringAction on the action in hand is honoured as a cut
    at its tick when that tick lies inside the action (the body's count:
    `walk` from the symbolic position for a walk, `ticks_of` for a duration),
    the agent placed where the walk has got to. Every anchor of every event is
    thereby checked against the sequential expansion, events and resumptions
    included. An event that cannot fire (an anchor absent, ambiguous or out of
    range, a during outside its action, an anchor never reached, a Drop with
    nothing to drop, a Start refused) and a task infeasible in the symbolic
    state are a ScriptError. Returns the record of
    the replay, one snapshot per instruction.
    """
    record = Record()
    machine = StackMachine(script, planner, agent_id, ticks_of, record)
    step = 0
    while True:
        nxt = machine.next(world, step)
        if isinstance(nxt, Idle):
            break
        if isinstance(nxt, RunAction):
            action, occurrence, done = nxt.action, nxt.occurrence, 0
        else:
            action, occurrence, done = nxt.cut.action, nxt.cut.occurrence, nxt.cut.done
        pos = world.agent_positions[agent_id]
        # the body's ticks of the action: a walk's remainder is re-expanded from
        # where the agent stands (done ticks behind it); a stand's remainder is
        # what is left of its duration
        full = action_ticks(action, world, pos, ticks_of, walk)
        total = done + full if action.schema.movement_target_key is not None else full
        record.snapshot(Snapshot(step, machine.stack_tasks(), action, occurrence, done, total))
        # the earliest during inside what remains of the action, if any
        top = machine.stack[-1]
        i = index_of(top.actions, action)
        times = sorted({ticks_of(p.event.trigger.time) for p in top.pending
                        if p.index == i and isinstance(p.event.trigger, DuringAction)
                        and done < ticks_of(p.event.trigger.time) < total})
        if times:
            n = times[0]
            cut_world = world
            if action.schema.movement_target_key is not None:
                positions = walk(pos, movement_target_position(action, world))
                cut_world = replace(world, agent_positions={**world.agent_positions, agent_id: positions[n - done - 1]})
            machine.cut(cut_world, step, n)
            world = cut_world
        else:
            world = advance(world, [action], agent_id)
            machine.action_done(world, step)
        step += 1
    problems = [t for t in record.transitions
                if isinstance(t, (Unfired, Refused)) or (isinstance(t, Left) and t.outcome is Outcome.INFEASIBLE)]
    if problems:
        raise ScriptError("the script cannot run as written: " + "; ".join(repr(t) for t in problems))
    return record
