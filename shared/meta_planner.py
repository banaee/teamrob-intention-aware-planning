"""
shared/meta_planner.py

PURPOSE:
    Owns robot task scheduling: which task to do next (under the
    "full_reorder" strategy, chosen with the rest of the pool as lookahead;
    see STRATEGY). Sits above
    planner.py (decomposes one task) and replaces replanning.py (trigger-only).
    Called by sim_agents.py; projects each candidate task through the injected
    Projector (shared/projection.py), which decomposes via planner.py.

    See shared/io_contracts.md §2.2 for the authoritative interface contract.
    See design_decisions.md, "Cancellation is not a meta_planner cost term",
    for why the cost carries no carrying/cancellation logic.
    See design_decisions.md, DESIGN-16, for the single_task vs. full_reorder
    strategy decision and the receding-horizon reasoning behind defaulting to
    single_task.

WHAT THIS MODULE DOES:
    - Owns the robot's task queue internally (Q1) — never passed in or out except
      inside UpdateResult. The queue holds only tasks NOT currently executing;
      the in-progress task lives in ExecutorState.current_task, not the queue
      (see update()'s docstring, "queue invariant").
    - Decides WHETHER to re-evaluate (evaluate_triggers)
    - Decides WHICH task to do next (update); under "full_reorder" on the
      cost of the cheapest ordering that starts with it
    - Projects a candidate task — or, under "full_reorder", a candidate
      ordering — and the human's predicted task through Projector.project()
      / project_human(). Never decomposes tasks itself.
    - Realizes every candidate against the human's projection through
      realize() (shared/realization.py; T10) and selects on the realized
      cost T_r + δ: interference detection is INTERNAL to realization, on the
      projection side, and conflict is priced by construction as the hold
      that avoids it (design_decisions.md, "The robot can wait"). Since F1
      (robot-responsible separation) realization is total: every candidate
      has a cost, and nothing here excludes a candidate. This module
      supplies min_separation and consumes the RealizedPlan; it holds no
      geometry and no conflict weight. The batch interference profile that
      preceded it (_detect_interference, min_safe_distance) is gone.

WHAT THIS MODULE DOES NOT DO:
    - Does NOT decompose a task into actions (that is planner.py)
    - Does NOT compute cancellation cost as a separate term (resolved intrinsically
      by planner.py's guarded method selection on the task itself)
    - Does NOT search for alternate paths/detours to avoid a conflict, and does
      NOT compute holds itself — that is realization (hold-only first, in 4C;
      detour and an off-the-shelf planner in 4D, DESIGN-13), a service on the
      projection side. MetaPlanner only ever picks among the discrete candidate
      tasks it's given, on their realized costs, and passes the winner's holds
      on as an execution hint.
    - Does NOT know about Mesa steps or ROS callbacks — simulators decide WHEN to
      call evaluate_triggers()/update(); this module decides WHAT counts as a trigger
    - Does NOT import from mesa_sim/ or ros_sim/

BLOCK STRUCTURE OF update():
    0.    task pool = ([current_task] if not None else []) + self._queue,
          minus every task already complete in the WorldState (its terminal
          condition holds — whoever did it; see _is_complete()).
          Terminal return if empty.
    B1.5  current_task is None, or the pool has just dropped it as complete
          in the world → nothing to continue; go straight to B3.
          Not an algorithmic block. Task boundaries always re-decide freely.
    B2    _is_current_task_plausible() — a MID-TASK commitment gate. Continue
          the current task (with the hold its realization placed), or
          escalate to B3. Always escalates when self._gate_strategy == "none"
          (the default), in which case update() behaves exactly as it did
          before the block split. "b2a" (T4) realizes the current task alone
          and continues iff δ ≤ ρ × (T_h − now).
    B3    _replan_tasks() — selects the task assignment and commits.
    Both B2 and B3 consume realization: B2 `b2a` (built, T4) realizes the
    CURRENT task alone and judges its hold; B3 (built, T10) realizes EVERY
    candidate and takes the argmin of realized cost, carrying the winner's
    hold. B2's role is COMMITMENT (R1, TODO-36): it can only keep the current
    task where B3 might switch, never cause a switch.

TASK POOL vs. CANDIDATES:
    The pool assembled in update() is NOT a candidate set. Nothing competes at
    that level. Candidates come into existence only inside B3, and what they
    are depends on B3's strategy: an individual task under "single_task", a
    permuted ordering under "full_reorder". Forming them from the pool is B3's
    private business.

    Inside B3, current_task is an ordinary candidate and competes on identical
    terms — no WAIT/RESELECT branch there; continuation vs. reselection falls
    out of the argmin. The one explicit continuation branch in the design is
    B2, which decides whether B3 runs at all, not what B3 decides once it does.

STRATEGY (DESIGN-16):
    self._strategy selects what a CANDIDATE is inside B3 — an individual task,
    or one ordering of the pool. Neither strategy commits to an order: the
    queue carries none under either (see "TASK POOL vs. CANDIDATES" above).
        "single_task" (default, IMPLEMENTED) — receding-horizon selection.
            Score each candidate alone (a length-1 ordering, projected from
            the live WorldState); the argmin becomes the new current_task —
            every candidate has a cost and none is excluded, since F1 made
            realization total. The rest of the queue is left as an unordered
            pool with no ordering commitment.
        "full_reorder" (B3.B; BUILT, T-B2b / T-B2c; a run option, T-B2d) —
            each ordering of the pool is a candidate: projected as ONE
            chained ProjectedPlan, one entry per task (entry 1's segments,
            then entry 2's from where entry 1 ended, ...) and realized against
            the ONE human projection inside [trigger, T_h], one minimal-shift
            search and so one hold per entry (T-B Q2); the argmin ordering's
            HEAD becomes the new current_task, and the hold that goes out is
            the hold before the first entry (_replan_orderings()). The ordering past
            the head is a LOOKAHEAD for that choice, re-priced at the next
            trigger (recognition_changed, which passes through B2, or
            no_current_task, which bypasses it; task_committed is no trigger
            since D3) — not an order commitment; the
            queue's order carries none, as under single_task. It exists for
            tasks coupled by geometry (two-table kitting: a task's end
            position depends on its table, so later walks depend on the
            order); in one-table layouts it is expected to choose as
            single_task does. Projector.project() chains the entries
            (T-B2a): the next entry starts at the step and position the
            previous one ends at, and is decomposed against a hypothetical
            successor state derived from what the action schemas declare
            (retraction of facts a projected action ended, holding after
            place, and the location of an object it moved — the part of
            TODO-07 that applies). DESIGN-12 does not apply: nothing is
            priced past T_h. Brute permutation is acceptable at pools of 3 to
            5; there is no cap. DECIDED (T-B Q2, Q3): a hold that clears a
            conflict in a LATER entry is placed at the boundary before that
            entry, one hold per entry (realize(), T-B2c); B2 commits to
            the current task, not to an order (`b2a` unchanged). See
            design_decisions.md, "B3.B (`full_reorder`) is lookahead for the
            choice of the next task, built next".
    Rationale for defaulting to single_task: the human-prediction horizon H is
    already belief-bounded and uncertain beyond it — committing to a
    multi-task robot schedule optimized against that same uncertain horizon
    has a weaker justification than re-deciding at each trigger from fresh
    WorldState/belief. See design_decisions.md, DESIGN-16, for the full
    argument. It stands under B3.B, which re-decides at every trigger too.

STILL OPEN (do not resolve inline while implementing — see TODOS_AND_DEFERRED.md):
    DESIGN-08 is RESOLVED by realization (conflict is priced by construction as
    hold duration; no penalty formula — see _replan_tasks()), DESIGN-09
    (pre-RESELECT cheap filter — B2 realizing the current task alone is that
    filter; B2 survives as `b2a`, TODO-36), DESIGN-10 (interference geometry
    — realize() asks shift_violation_interval's closed form; the sampling
    algorithm discretized_time_sampling() was removed, TODO-83 — see
    shared/trajectory_algorithms.py), DESIGN-12
    (horizon-projected confidence — moot under single_task, and not needed by
    full_reorder as designed: nothing is priced past T_h), DESIGN-13 (partly pulled forward into 4C as the hold-only
    realization strategy; detour — obstacle_aware_path() — and an
    off-the-shelf planner remain 4D), DESIGN-16 (see STRATEGY above). None
    block the single_task implementation below.
"""

import itertools
import logging
from math import factorial
from typing import Dict, List, Literal, Optional, Tuple

from shared.types import (
    BeliefState,
    WorldState,
    TaskInstance,
    ProjectedPlan,
    RealizedPlan,
    ExecutorState,
    TriggerDecision,
    UpdateResult,
    task_instance_key,
)


from shared.domain_knowledge import DomainKnowledgeBase
from shared.recognizer import IntentionRecognizer, UNKNOWN
from shared.planner import AdaptivePlanner
from shared.projection import Projector
from shared.realization import realize


# =============================================================================
# The cognitive-clock confidence gate (DESIGN-07)
# =============================================================================

DEFAULT_THETA = 0.75
"""
The single definition of theta. The gate is the META-PLANNER's decision — the
recognizer produces the belief and never judges it (recognizer_handback.md §2)
— so the value lives beside the one method that applies it, _clears_gate().

Importable by name (`from shared.meta_planner import DEFAULT_THETA`) for
visualization or evaluation code that wants to draw or report the bar without
constructing a MetaPlanner. Per-instance overrides go through the constructor's
`theta` parameter; no call site passes one today — mesa_sim/sim_agents.py is the
only place a MetaPlanner is constructed, and ros_sim/ (paused) constructs none —
so this default governs every run.

NOT a settled constant — see _clears_gate() for the two open directions
(TODO-64, TODO-65) and why they touch only that method.
"""


class MetaPlanner:
    """
    See shared/io_contracts.md §2.2 for the interface contract this class implements.
    """

    def __init__(
        self,
        knowledge: DomainKnowledgeBase,
        projector: Projector,
        recognizer: IntentionRecognizer,
        min_separation: float,
        theta: float = DEFAULT_THETA,
        strategy: Literal["single_task", "full_reorder"] = "single_task",
        gate_strategy: Literal["none", "b2a", "b2b"] = "none",
        cost_strategy: Literal["realized", "plain"] = "realized",
        human_agent_id: Optional[str] = None,
        rho: float = 0.5,
    ):
        """
        knowledge:              HTN domain knowledge, passed through to planner.py calls.
        recognizer:              the SAME live IntentionRecognizer instance the owning
                                 RobotAgent already constructed and calls .update() on —
                                 not a second instance built here. get_hypothesis() is
                                 stateless with respect to belief (it's a static lookup
                                 built once from the hypothesis space at recognizer
                                 construction), so holding this reference carries no
                                 staleness risk; it just avoids constructor bloat
                                 (context/hypotheses) and a redundant, unused _history
                                 list that constructing a second instance would add.
        theta:                   cognitive-clock confidence threshold (DESIGN-07). Gate
                                 only — never fed into a cost as a magnitude.
                                 Defaults to DEFAULT_THETA (module level, the single
                                 definition). Applied in exactly one place,
                                 _clears_gate(); do not compare against self._theta
                                 anywhere else.
        strategy:                B3's strategy — "single_task" (default) or
                                 "full_reorder" (B3.B, T-B2b / T-B2c).
                                 Selects what a candidate is inside _replan_tasks(): an
                                 individual task, or one ordering of the pool. A run
                                 option (T-B2d). See module docstring, DESIGN-16.
        gate_strategy:           B2, the mid-task plausibility gate. "none" (default)
                                 always escalates — update() then behaves exactly as it
                                 did before the block split. "b2a" (T4) realizes the
                                 current task alone and judges its hold against rho.
                                 "b2b" (realize current and each other task; margin —
                                 redundant with B3) is a documented stub. Independent of
                                 `strategy` and `cost_strategy`; all combinations are
                                 intended to be runnable.
        cost_strategy:           what B3 selects on (T10). "realized" (default): every
                                 candidate is realized against the human projection
                                 (realize(), this planner's min_separation) and the
                                 argmin of the realized cost T_r + δ wins, its δ carried
                                 as the decision's hold. "plain": the argmin of the projected
                                 duration T_r alone — no human consideration, no hold, no
                                 filter — for comparison and the T6 ablation. Both use
                                 the same quantity for T_r (RealizedPlan.projected_duration,
                                 the fractional segment span), so their difference is
                                 realization's effect and nothing else.
        human_agent_id:          agent_id of the human this robot observes, for building
                                 the human's predicted projection in update(). Mirrors
                                 RobotAgent.observed_agent_id's existing optionality —
                                 None means no human projection is built and every
                                 candidate realizes with δ = 0 at its plain projected
                                 duration, matching how RobotAgent already tolerates no
                                 observed human.
        min_separation:          the clearance realization must achieve, in world
                                 units, supplied by the body (TODO-28; Mesa: 50 cm,
                                 mesa_configs.yaml). A standard sets a distance, so it
                                 is set outside the planner and not derived here from
                                 the body's speed; no default, since shared/ holds no
                                 unit-scale value. The one value both B2 `b2a` (T4) and
                                 B3 (T10) hand to realize().
        rho:                     B2 `b2a`'s policy parameter (R1, TODO-36): continue the
                                 current task iff its realized hold δ ≤ rho × (T_h − now),
                                 the human's remaining projected duration at the trigger.
                                 0.5 is a STATED ASSUMPTION to be varied in T6, not a
                                 calibrated value.
        """
        self._knowledge = knowledge
        self._recognizer = recognizer
        self._projector = projector
        self._theta = theta
        self._strategy = strategy
        self._gate_strategy = gate_strategy
        self._cost_strategy = cost_strategy
        self._human_agent_id = human_agent_id
        self._min_separation = min_separation
        self._rho = rho
        # For the pool's completion test only (_is_complete()). Decomposition
        # for projection stays inside Projector; this never plans.
        self._planner = AdaptivePlanner(knowledge=knowledge)
        self._queue: List[TaskInstance] = []  # owned internally per Q1; populated by seed_tasks()
        # The decision record (D2): the hypothesis the last fired trigger's
        # decision was projected against — belief.most_likely on the tick
        # update_human_projection() built a projection; None when admission
        # refused (nothing was projected, so no decision rests on a hypothesis)
        # or before any trigger has fired. One field, because one reader:
        # evaluate_triggers()'s recognition_changed. Set in
        # update_human_projection(), read nowhere else.
        self._projected_hypothesis: Optional[str] = None
        # The reason of the latest evaluate_triggers() decision, for B2's log
        # line only; update()'s signature carries no trigger, and nothing
        # decides on this.
        self._last_trigger_reason: Optional[str] = None

        
    # =========================================================================
    # Public interface (shared/io_contracts.md §2.2)
    # =========================================================================

    # The policy values a run was produced under, read-only, so the embodiment
    # can write them into the run's log header (TODO-78). Reading them decides
    # nothing: theta is still applied only in _clears_gate().
    @property
    def theta(self) -> float:
        return self._theta

    @property
    def rho(self) -> float:
        return self._rho

    @property
    def min_separation(self) -> float:
        """World units, as the body supplied it."""
        return self._min_separation

    @property
    def strategy(self) -> str:
        return self._strategy

    @property
    def gate_strategy(self) -> str:
        return self._gate_strategy

    @property
    def cost_strategy(self) -> str:
        return self._cost_strategy

    def evaluate_triggers(
        self,
        belief: BeliefState,
        world: WorldState,
        executor_state: ExecutorState,
    ) -> TriggerDecision:
        """
        Replaces replanning.py's should_replan(). Event-driven only.

        Two real triggers (DESIGN-07; the second replaced in D2, the third,
        task_committed, removed in D3: the robot's own grasp was in the plan
        the last decision priced, not a change in what it rested on):
            - no_current_task: executor_state.current_task is None. Covers BOTH
              t=0 (see seed_tasks()) AND ordinary task completion — this assumes
              whoever builds ExecutorState (sim_agents.py, step 9) clears
              current_task to None once a task's plan finishes, mirroring the
              existing current_plan=None pattern in RobotAgent.step(). If that
              wiring choice changes, a separate task_completed check would need
              to be reintroduced here.
            - recognition_changed (D2): the belief no longer points at the
              hypothesis the last decision was projected against. ONE condition
              read from two sides, against the decision record
              `_projected_hypothesis`:
                * a hypothesis is recorded and belief.most_likely is no longer
                  it: replaced by another (TODO-48), the human's task ended and
                  the belief re-initialised (the recognizer's [IR-boundary]
                  tick), or `unknown` took over after a pin (TODO-54). What is
                  projected next is admission's answer, possibly nothing;
                * none is recorded and the belief clears _clears_gate() on a
                  task hypothesis — not `unknown`, which is no task hypothesis
                  and has no projection (admission refuses it). The first
                  time a task hypothesis clears the gate, as `theta_crossed`
                  fired it.
              The gate is asked at admission, never for retention: a recorded
              hypothesis that dips below theta while staying most likely fires
              nothing (TODO-68's repeated crossings) and keeps its projection
              until it is replaced, ends, or the human stops. That consequence
              is accepted and recorded (design_decisions.md, D2); a margin or a
              duration on the dip would be a second threshold, which DESIGN-07
              rules out. Supersedes `theta_crossed`, the crossing of the gate
              from below: it fired on every re-crossing and never on a change
              of hypothesis. The bar itself is _clears_gate()'s business,
              never compared here.

        When both hold on one tick the order is no_current_task, then
        recognition_changed — arbitrary, as before: only the reported reason
        and score differ, update() runs the same.

        Confidence is a gate here (via _clears_gate(), on the entering side of
        recognition_changed), never a magnitude fed into a cost.
        """
        if executor_state.current_task is None:
            decision = TriggerDecision(fired=True, reason="no_current_task", score=1.0)
        else:
            recorded = self._projected_hypothesis
            if recorded is not None:
                recognition_changed = belief.most_likely != recorded
            else:
                recognition_changed = (
                    self._clears_gate(belief) and belief.most_likely != UNKNOWN
                )

            if recognition_changed:
                decision = TriggerDecision(fired=True, reason="recognition_changed", score=belief.confidence)
            else:
                decision = TriggerDecision(fired=False, reason="none", score=0.0)

        self._last_trigger_reason = decision.reason
        return decision


    def update_human_projection(
        self,
        belief: BeliefState,
        world: WorldState,
    ) -> Optional[ProjectedPlan]:
        """
        Projection admission, then a thin wrapper over Projector.project_human(),
        supplying the recognizer and human_agent_id this MetaPlanner was
        constructed with. Call once per fired trigger, between
        evaluate_triggers() and update(); pass the result to update() as its
        human_projection argument.

        Admission is a MetaPlanner decision — Projector holds no policy. A
        projection is admitted only when the belief clears the confidence gate
        (_clears_gate(), the single place theta is applied): below the bar the
        most-likely hypothesis is not evidence, and a realization against it
        would be a realization against noise. The same gate
        evaluate_triggers() asks on the entering side of recognition_changed
        (DESIGN-07) — never fed into a cost.

        Also sets the decision record (D2): `_projected_hypothesis` becomes
        belief.most_likely when a projection is built, None when admission
        refuses. Cleared rather than kept on a refusal because nothing was
        projected, so no decision rests on the old hypothesis; a stale record
        would make recognition_changed fire on every later tick the belief
        points elsewhere, against a hypothesis no decision used.

        Returns None, in this order, when
          - the belief does not clear the gate (_clears_gate(); the projector is
            not called),
          - no human is observed,
          - belief.most_likely is the recognizer's `unknown` (the projector is
            not called): mass on `unknown` above theta is not admitted —
            the human's behaviour is unmodelled, or no task hypothesis is
            left live and the mass is `unknown`'s by normalisation — and
            there is nothing to project. Reachable since the completion pin:
            a hypothesis retired by the robot's own delivery hands its mass
            to `unknown` (TODO-54),
          - the hypothesis cannot be resolved (project_human() returned None).
        update() then realizes every candidate against no human plan: δ = 0,
        plain projected cost.

        Logs one [meta-proj] line per call. No step or trigger field: step
        counts are a simulator concept, and the TriggerDecision belongs to the
        caller. Both are recoverable by adjacency — this is called only on a
        fired trigger, so the [meta-trig] line of the same tick precedes it.
        """
        if not self._clears_gate(belief):
            reason = "none(below_theta)"
            projection = None
        elif self._human_agent_id is None:
            reason = "none(no_human)"
            projection = None
        elif belief.most_likely == UNKNOWN:
            reason = "none(unknown)"
            projection = None
        else:
            projection = self._projector.project_human(
                belief=belief,
                world=world,
                human_agent_id=self._human_agent_id,
                recognizer=self._recognizer,
            )
            reason = "built" if projection is not None else "none(unresolved)"

        self._projected_hypothesis = belief.most_likely if projection is not None else None

        logging.info(
            f"[meta-proj] confidence={belief.confidence:.3f} "
            f"theta={self._theta:.3f} projection={reason}"
        )
        return projection
    
    
    def update(
        self,
        belief: BeliefState,
        world: WorldState,
        executor_state: ExecutorState,
        human_projection: Optional[ProjectedPlan]
    ) -> UpdateResult:
        """
        Main entry point when evaluate_triggers() fires. Dispatch only — the
        decision logic lives in the blocks below.

        Queue invariant: self._queue holds only tasks NOT currently executing.
        The in-progress task, if any, lives solely in
        executor_state.current_task. The task pool for this call is
        ([current_task] if not None else []) + self._queue, minus every task
        already complete in `world` (see _is_complete()). Completion is a
        WORLD fact and is read from the world on every call, never recorded
        here: the executor's bookkeeping learns of its own task's completion
        up to two ticks after the terminal condition holds, and a queued task
        may be finished by someone else — neither owner is consulted.

        Note the pool is NOT called "candidates". Candidates come into
        existence only inside B3, and what they are depends on B3's strategy —
        individual tasks under single_task, permuted orderings under
        full_reorder. Nothing is competing for anything at this level.

        BLOCK STRUCTURE:
            0.    assemble the task pool; terminal return if empty
            B1.5  no current task, or the pool dropped it as complete →
                  nothing to continue, go straight to B3
            B2    _is_current_task_plausible() — continue, or escalate to B3
            B3    _replan_tasks() — select and commit

        `human_projection` is supplied by the caller, built once per fired
        trigger via update_human_projection(). Not rebuilt here, not recomputed
        per candidate. None means the projection was not admitted: belief
        confidence below theta, no human observed, `unknown`, or the hypothesis
        was unresolvable — every candidate then realizes with δ = 0 at its
        plain projected duration (realize() with no human plan), never as
        always-conflicting. A ROUTINE mid-run state, not an edge case: the
        belief re-initialises at every human task boundary (I4c).

        TERMINAL STATE: returns UpdateResult(current_task=None, queue=[]) when
        the pool is empty (nothing left to do: queue empty and nothing
        executing, or everything remaining is already complete in the world)
        — all assigned tasks are complete. A normal return, not an exception;
        callers check `result.current_task is None`.
        """
        current = executor_state.current_task
        task_pool: List[TaskInstance] = list(self._queue)
        if current is not None:
            task_pool = [current] + task_pool

        remaining: List[TaskInstance] = []
        current_dropped = False
        for task in task_pool:
            if self._is_complete(task, world, executor_state.agent_id):
                logging.info(f"[meta-pool] {task_instance_key(task)} complete in world: dropped from the pool")
                if task is current:
                    current_dropped = True
            else:
                remaining.append(task)
        task_pool = remaining

        if not task_pool:
            # Terminal state, not an error: all assigned tasks are complete.
            # Returned rather than raised so the embodiment layer learns this
            # from the contract instead of catching an exception — see
            # design_decisions.md, mind/body separation.
            return UpdateResult(current_task=None, queue=[])

        # ---- B1.5: no current task, so there is nothing to continue --------
        # Not an algorithmic block. Task boundaries always re-decide freely;
        # B2 is specifically a MID-TASK commitment mechanism. A current task
        # the pool has just dropped as complete in the world is over, whatever
        # the executor's bookkeeping still holds: there is nothing to continue
        # either (one fact, one owner — this decision reads completion from
        # the pool alone, never from executor_state.current_task).
        if current is not None and not current_dropped:
            # ---- B2: plausibility gate on the current task ------------------
            hold = self._is_current_task_plausible(
                belief=belief,
                world=world,
                executor_state=executor_state,
                human_projection=human_projection,
                task_pool=task_pool,
            )
            if hold is not None:
                # Continuation: queue untouched, current task keeps executing,
                # with the hold its realization placed (0: none).
                return UpdateResult(
                    current_task=executor_state.current_task,
                    queue=list(self._queue),
                    hold=hold,
                )

        # ---- B3: replan the task assignment ---------------------------------
        return self._replan_tasks(
            task_pool=task_pool,
            belief=belief,
            world=world,
            executor_state=executor_state,
            human_projection=human_projection,
        )
        
        
        
    # =========================================================================
    # Internal (not part of io_contracts.md — private to this class)
    # =========================================================================

    def _clears_gate(self, belief: BeliefState) -> bool:
        """
        THE confidence gate (DESIGN-07): has this belief cleared the bar the
        meta-planner is willing to act on? The ONLY place theta is applied.
        Both consumers ask this question and neither compares numbers itself:
          - evaluate_triggers(): `recognition_changed` asks it on its
            entering side only — a task hypothesis clears the gate while no
            projected hypothesis is recorded. Retention is by identity, not
            by this predicate (D2), so it is not asked per tick;
          - update_human_projection(): admission, this predicate on the
            current belief.
        Kept as one method deliberately. The gate is a decision the
        meta-planner makes FROM the belief, not a comparison welded into its
        call sites, because two open directions would change how the bar is
        computed without changing where it is asked (neither is implemented,
        and nothing here should be read as favouring either):
          - theta DERIVED rather than fixed (TODO-64): a function of the live
            hypothesis set, of layout geometry, or both. A fixed 0.75 is a
            different evidential bar over a three-hypothesis live set than an
            eight-hypothesis one, since the reachable ceiling is 1/(1 + u^n).
          - a MARGIN or likelihood-ratio gate replacing the absolute test
            (TODO-65): fire when the leading hypothesis is far enough ahead of
            the runner-up, of `unknown`, or of the rest of the field. 0.5
            against a field of 0.1s is a stronger signal than 0.6 against a
            field of 0.2s, and an absolute threshold cannot see the difference.
        `belief` alone already carries what both need except layout geometry:
        belief.distribution holds the live set and every rival's mass. A
        geometry-derived theta would add a `world` argument HERE, and the two
        call sites above already hold a WorldState to pass.

        Returns True when the belief clears the bar. Deliberately says nothing
        about what clearing MEANS: whether a decision still rests on a
        hypothesis is the decision record's question (`recognition_changed`,
        D2), not this predicate's, and that reading must not be built into
        this name.
        """
        return belief.confidence >= self._theta

    def seed_tasks(self, tasks: List[TaskInstance]) -> None:
        """
        Loads the initial task pool. Does NOT order it — Q0 (the real initial
        ordering) is produced by the first update() call, triggered by
        evaluate_triggers()'s no_current_task condition, through the identical
        pipeline used for every later re-evaluation. See design_decisions.md,
        "Robot's scheduled_tasks order is a scenario-authoring convenience, not
        a schedule."

        NOTE: called externally by sim_agents.py at agent construction, so this
        may belong in the "Public interface" section above and in
        io_contracts.md §2.2 rather than here — flagging, not resolving, since
        that placement wasn't part of any session's discussion.
        """
        self._queue = list(tasks)

    def _is_complete(
        self,
        task: TaskInstance,
        world: WorldState,
        agent_id: str,
    ) -> bool:
        """
        Whether `task` is already done in `world`, by the planner's generic
        test (AdaptivePlanner.is_complete: the terminal action's completion
        condition of the task's decomposition for `agent_id` holds). The same
        criterion the recognizer retires a hypothesis on, and equally
        indifferent to who did it. Derived from the task's own schema through
        the decomposition — no predicate name is known here.
        """
        task_params = {var.name: const.value for var, const in task.bindings.items()}
        return self._planner.is_complete(task.schema.name, task_params, agent_id, world)


    # =========================================================================
    # B2 — plausibility gate on the current task
    # =========================================================================

    def _is_current_task_plausible(
        self,
        belief: BeliefState,
        world: WorldState,
        executor_state: ExecutorState,
        human_projection: Optional[ProjectedPlan],
        task_pool: List[TaskInstance],
    ) -> Optional[int]:
        """
        Decides whether the currently-executing task should keep executing, or
        whether the situation warrants escalating to B3. Called only when
        executor_state.current_task is not None and not complete in the world
        (see update()'s B1.5).

        This is a WORTHINESS check, not a feasibility check. The current task
        may remain perfectly doable but only via a long pause or detour;
        "doable" is not the question. Naming reflects that — "feasible" and
        "should_continue" were both rejected as implying a bare collision test.

        Returns the hold (whole ticks, ≥ 0) to CONTINUE the current task with,
        or None to ESCALATE to B3. B2's role is COMMITMENT (R1, TODO-36): it
        can only keep the current task where B3 might switch; it never selects
        another task, and the hold it returns is realization's, not its own.

        Strategies (self._gate_strategy):
            "none" (default) — no gate; always escalate. update() then behaves
                exactly as it did before the block split.
            "b2a"  (T4) — realize the CURRENT TASK ALONE against
                human_projection (realize(), decision step 0, this planner's
                min_separation) and judge its hold δ against the human's
                remaining projected duration at the trigger, T_h − 0:
                  human_projection is None     → continue, no hold (0)
                  δ ≤ ρ × T_h                  → continue, with hold δ
                  δ above that bound           → escalate (None)
                (realization is total since F1: there is no unrealizable
                current task to escalate on)
                ρ is self._rho, a stated assumption (T6 varies it).
            "b2b"  — realize the current task and each other task in
                task_pool individually; continue only if it wins by a clear
                margin. Redundant with B3 under single_task by construction —
                a redundancy control for ablation, not a fourth policy.
                NOT IMPLEMENTED (documented stub).

        `task_pool` is unused under "b2a" and is present only so the signature
        does not change when "b2b" is filled in.

        When `human_projection` is None — not admitted by
        update_human_projection() (below theta, no human, `unknown`,
        unresolvable) — b2a continues with no hold. B2 escalates on evidence
        AGAINST the current task; no projection means no evidence, and no
        reason to interrupt committed work.

        Logs one [meta-b2] line per call under "b2a" (nothing under "none"):
        trigger, current task, projection admitted or not, reason, δ, T_r,
        the human's remaining projected duration, the bound, verdict
        (continue_hold | continue | escalate). No step field, as [meta-proj].
        """
        if self._gate_strategy == "none":
            return None

        if self._gate_strategy == "b2a":
            current = executor_state.current_task
            head = (f"[meta-b2] trigger={self._last_trigger_reason} "
                    f"current={task_instance_key(current)}")
            if human_projection is None:
                logging.info(f"{head} projection=none verdict=continue hold=0")
                return 0
            now = 0.0  # the trigger, on the projection clock
            projection = self._projector.project(
                [current], world, executor_state.agent_id, belief, start_step=now
            )
            realized = realize(projection, human_projection, self._min_separation, decision_step=now)
            if realized.horizon is None:
                # An admitted projection without segments: realize() reads it
                # as no projection, and so does B2.
                logging.info(f"{head} projection=admitted reason={realized.reason} verdict=continue hold=0")
                return 0
            remaining = realized.horizon - now
            bound = self._rho * remaining
            if realized.delta <= bound:
                hold = realized.delta
                verdict = "continue_hold" if hold > 0 else "continue"
            else:
                hold = None
                verdict = "escalate"
            logging.info(
                f"{head} projection=admitted "
                f"reason={realized.reason} delta={realized.delta} "
                f"T_r={realized.projected_duration:.2f} remaining={remaining:.2f} "
                f"rho={self._rho} bound={bound:.2f} verdict={verdict}"
                + (f" hold={hold}" if hold is not None else "")
            )
            return hold

        raise NotImplementedError(
            f"MetaPlanner._is_current_task_plausible: gate_strategy "
            f"'{self._gate_strategy}' is not yet implemented — see "
            f"TODOS_AND_DEFERRED.md, TODO-36."
        )

    # =========================================================================
    # B3 — task-level replanning
    # =========================================================================

    def _replan_tasks(
        self,
        task_pool: List[TaskInstance],
        belief: BeliefState,
        world: WorldState,
        executor_state: ExecutorState,
        human_projection: Optional[ProjectedPlan],
    ) -> UpdateResult:
        """
        Selects the task assignment: which task executes now, and what remains
        queued. "Replan" here is TASK-level — distinct from planner.plan()'s
        HTN decomposition, which is action-level.

        Forming candidates from task_pool is this block's private business:
            single_task  — each task in the pool is a candidate; argmin wins.
            full_reorder — each ordering of the pool is a candidate; the
                           head of the cheapest becomes the current task:
                           _replan_orderings() (T-B2b, T-B2c).

        single_task (B3.A with realized cost, T10): each candidate is projected
        alone from the live WorldState at decision step 0 (the trigger, on the
        projection clock) and realized — realize(projection, human_projection,
        min_separation, 0) — under the whole-trajectory minimal shift. Its cost
        is RealizedPlan.cost = T_r + δ: T_r the FRACTIONAL projected duration
        (the segment span), δ the hold in whole ticks. Realization is TOTAL
        (F1, robot-responsible separation: a standing robot never violates and
        there is no hold cap), so every candidate has a cost and none is
        excluded. The winner is the argmin over all candidates, ties resolved
        by pool order (min() keeps the first; TODO-42 — unchanged), and ITS δ
        goes out as UpdateResult.hold,
        whether the winner is the current task or another. The rest form the
        queue in whatever order they happened to iterate — order carries no
        commitment under this strategy, it is re-decided next trigger.
        "Continue, paying a 2-tick hold" and "switch, paying 19 ticks of
        walking" compare on one number, and conflict is priced by construction
        (design_decisions.md, "The robot can wait").

        No human projection (None, or one without segments): realize() reports
        `no_human_projection` for every candidate — δ = 0, cost = T_r — so B3
        is then an argmin over projected durations. The plain cost is the same
        T_r, RealizedPlan.projected_duration, never ProjectedPlan's integer
        total_estimated_cost (T3b). There is no all-unrealizable case any more
        (F1 removed it, and the RuntimeError before it went at T10).

        cost_strategy "plain": every candidate is realized against NO human
        plan, whatever was admitted — the argmin of T_r, no hold, no filter. A
        comparison condition (T6), not a policy; it shares T_r's quantity with
        "realized" so the two differ by realization alone.

        current_task, if any, is an ordinary member of task_pool and competes
        on identical terms. Continuation vs. reselection falls out of the
        argmin; there is no branch for either outcome here. (The one explicit
        continuation branch in the design lives in update()'s B2, which decides
        whether this method runs at all — not what it decides once it does.)

        Logs one [meta-cand] line per candidate (reason, T_r, δ, cost,
        unassessed share) and one [meta-b3] line per call (trigger,
        cost_strategy, selection ∈ realized | no_projection | plain, winner,
        cost, hold, T_h, candidate count). No step field, as [meta-proj] and
        [meta-b2]: the [meta-trig] line of the same tick precedes them.
        """
        if self._strategy not in ("single_task", "full_reorder"):
            raise ValueError(f"MetaPlanner: unknown strategy '{self._strategy}'")
        if self._cost_strategy not in ("realized", "plain"):
            raise ValueError(f"MetaPlanner: unknown cost_strategy '{self._cost_strategy}'")

        now = 0.0  # the trigger, on the projection clock
        against = human_projection if self._cost_strategy == "realized" else None
        if self._strategy == "full_reorder":
            return self._replan_orderings(task_pool, belief, world, executor_state, against)
        rows: List[Tuple[TaskInstance, RealizedPlan]] = []
        for task in task_pool:
            projection = self._projector.project([task], world, executor_state.agent_id, belief, start_step=now)
            realized = realize(projection, against, self._min_separation, decision_step=now)
            rows.append((task, realized))
            logging.info(
                f"[meta-cand] {task_instance_key(task)} reason={realized.reason} "
                f"T_r={realized.projected_duration:.2f} delta={realized.delta} "
                f"cost={realized.cost:.2f} share={realized.unassessed_share:.2f}"
            )

        winner, chosen = min(rows, key=lambda row: row[1].cost)
        hold = chosen.delta
        if self._cost_strategy == "plain":
            selection = "plain"
        elif chosen.horizon is None:
            selection = "no_projection"
        else:
            selection = "realized"

        logging.info(
            f"[meta-b3] trigger={self._last_trigger_reason} cost_strategy={self._cost_strategy} "
            f"selection={selection} winner={task_instance_key(winner)} cost={chosen.cost:.2f} hold={hold} "
            f"T_h={_fmt(rows[0][1].horizon)} candidates={len(rows)}"
        )

        new_queue = [t for t in task_pool if t is not winner]
        self._queue = new_queue
        return UpdateResult(current_task=winner, queue=list(new_queue), hold=hold)

    def _replan_orderings(
        self,
        task_pool: List[TaskInstance],
        belief: BeliefState,
        world: WorldState,
        executor_state: ExecutorState,
        against: Optional[ProjectedPlan],
    ) -> UpdateResult:
        """
        B3.B, "full_reorder" (T-B2b, T-B2c): a candidate is one ordering of the
        pool — the same pool single_task ranks, the current task included when
        there is one — and the HEAD of the cheapest ordering becomes the
        current task. Everything is computed here, at the trigger, on
        projections; nothing is executed and `world` is only read.

        THE COST OF AN ORDERING: the ordering is projected as one chained
        ProjectedPlan (Projector.project(), T-B2a) and realized against
        `against` — the ONE human projection under cost_strategy "realized",
        none under "plain" — by realize(), which runs one minimal-shift search
        per entry (T-B Q2). Its cost is RealizedPlan.cost: the sum of the
        entries' T_r plus the cumulative shift of the last entry. A conflict
        may lie in a later entry; it is then cleared by a hold before THAT
        entry, where the previous one ended, and the earlier entries are not
        delayed for it. Nothing past T_h is assessed or charged. With no human
        plan (not admitted, or "plain") every hold is 0 and the cost is the
        plain one, the sum of the entries' T_r.

        ENUMERATION AND TIES: every permutation, in pool order (the pool's own
        order first, then by position), and the first minimum wins — so on a
        tie between orderings with different heads, the head is the one
        earlier in the pool, the task single_task's rule would pick (TODO-42,
        unchanged). No cap on the pool and no depth limit: nothing in the
        design sets one (n! projections of n entries; pools are 3 to 5).
        Orderings with a common prefix do NOT share work: sharing the prefix's
        projection would need a successor state that outlives a project()
        call, which T-B2a rules out, and the measured cost of a call does not
        ask for it.

        THE HOLD that goes out is the hold before the FIRST entry of the
        winning ordering's RealizedPlan (RealizedPlan.delta). It is the hold
        single_task would send for the same head: search 1 ranges over the
        first entry's own intervals with lower bound 0, and the first entry is
        the head projected from the live world — the head realized alone. The
        holds before later entries are lookahead: they are priced, never sent.

        THE TAIL CARRIES NO COMMITMENT (T-B Q3: B2 commits to the current
        task, `b2a` unchanged). The winning ordering is not stored: self._queue
        becomes the pool without the head IN POOL ORDER, exactly as
        single_task leaves it, so the ordering cannot reach the next call
        through the pool's order and its tie-breaks. UpdateResult.queue lists
        the tail in the ordering's order, as information only.

        Logs, per call: one [meta-ord] line per possible head, in pool order
        (the cheapest ordering that starts with it, its cost, how many
        orderings start with it); one [meta-win] line for the winning ordering
        (reason, T_r, the hold before each entry, the cumulative shift of the
        last entry, cost, unassessed share); and the [meta-b3] line as under
        single_task (selection ∈ realized | no_projection | plain; cost the
        winning ordering's; hold the one sent; candidates the number of
        orderings), with `ordering=` appended.
        """
        now = 0.0  # the trigger, on the projection clock
        agent_id = executor_state.agent_id

        # head's index in the pool -> (realized ordering, ordering as pool
        # indices); filled in enumeration order, a strict < keeping the first
        # minimum per head
        cheapest: Dict[int, Tuple[RealizedPlan, Tuple[int, ...]]] = {}
        for indices in itertools.permutations(range(len(task_pool))):
            projection = self._projector.project(
                [task_pool[i] for i in indices], world, agent_id, belief, start_step=now
            )
            realized = realize(projection, against, self._min_separation, decision_step=now)
            if indices[0] not in cheapest or realized.cost < cheapest[indices[0]][0].cost:
                cheapest[indices[0]] = (realized, indices)

        per_head = factorial(len(task_pool) - 1)
        for head_index, (realized, indices) in cheapest.items():
            logging.info(
                f"[meta-ord] head={task_instance_key(task_pool[head_index])} cost={realized.cost:.2f} "
                f"orderings={per_head} ordering={_fmt_ordering(task_pool[i] for i in indices)}"
            )

        # min() keeps the first: heads are in pool order
        chosen, indices = min(cheapest.values(), key=lambda row: row[0].cost)
        ordering = [task_pool[i] for i in indices]
        head = ordering[0]
        hold = chosen.delta  # the hold before the first entry
        if self._cost_strategy == "plain":
            selection = "plain"
        elif chosen.horizon is None:
            selection = "no_projection"
        else:
            selection = "realized"

        logging.info(
            f"[meta-win] reason={chosen.reason} T_r={chosen.projected_duration:.2f} "
            f"holds={','.join(str(h) for h in chosen.holds)} shift={chosen.cumulative_shifts[-1]} "
            f"cost={chosen.cost:.2f} share={chosen.unassessed_share:.2f}"
        )
        logging.info(
            f"[meta-b3] trigger={self._last_trigger_reason} cost_strategy={self._cost_strategy} "
            f"selection={selection} winner={task_instance_key(head)} cost={chosen.cost:.2f} hold={hold} "
            f"T_h={_fmt(chosen.horizon)} candidates={per_head * len(task_pool)} "
            f"ordering={_fmt_ordering(ordering)}"
        )

        self._queue = [t for t in task_pool if t is not head]
        return UpdateResult(current_task=head, queue=ordering[1:], hold=hold)


def _fmt_ordering(ordering) -> str:
    """An ordering for the log lines above: its task instance keys, head first."""
    return " > ".join(task_instance_key(task) for task in ordering)


def _fmt(value: Optional[float]) -> str:
    """Two decimals, or None, for the log lines above."""
    return "None" if value is None else f"{value:.2f}"
