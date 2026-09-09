"""
shared/meta_planner.py

PURPOSE:
    Owns robot task scheduling: which task to do next, and (under the not-yet-
    implemented "full_reorder" strategy) what order the rest follow. Sits above
    planner.py (decomposes one task) and replaces replanning.py (trigger-only).
    Called by sim_agents.py; calls planner.py per candidate task to project
    execution.

    See shared/io_contracts.md §2.2 for the authoritative interface contract.
    See design_decisions.md, "Cancellation is not a meta_planner cost term",
    for why _cost() carries no carrying/cancellation logic.
    See design_decisions.md, DESIGN-16, for the single_task vs. full_reorder
    strategy decision and the receding-horizon reasoning behind defaulting to
    single_task.

WHAT THIS MODULE DOES:
    - Owns the robot's task queue internally (Q1) — never passed in or out except
      inside UpdateResult. The queue holds only tasks NOT currently executing;
      the in-progress task lives in ExecutorState.current_task, not the queue
      (see update()'s docstring, "queue invariant").
    - Decides WHETHER to re-evaluate (evaluate_triggers)
    - Decides WHICH task to do next (update); under "full_reorder" (not yet
      implemented) would also decide what order the rest of the queue follows
    - Projects a candidate task — or, under "full_reorder", a candidate
      ordering — and the human's predicted task, for interference checking,
      using planner.py per candidate. Never decomposes tasks itself.
    - Detects interference by comparing straight-line Segments (see
      shared/trajectory_algorithms.py) between the robot's projection and the
      human's, via a swappable algorithm — no zone concept involved (see
      design_decisions.md on why zone-based proximity was rejected).

WHAT THIS MODULE DOES NOT DO:
    - Does NOT decompose a task into actions (that is planner.py)
    - Does NOT compute cancellation cost as a separate term (resolved intrinsically
      by planner.py's guarded method selection on the task itself)
    - Does NOT search for alternate paths/detours to avoid a conflict — that is
      Phase 4D's low-level path-realization estimator (DESIGN-13), driven by a
      conflict hint from _detect_interference(), not a meta_planner concern.
      MetaPlanner only ever picks among the discrete candidate tasks it's given.
    - Does NOT know about Mesa steps or ROS callbacks — simulators decide WHEN to
      call evaluate_triggers()/update(); this module decides WHAT counts as a trigger
    - Does NOT import from mesa_sim/ or ros_sim/

BLOCK STRUCTURE OF update():
    0.    task pool = ([current_task] if not None else []) + self._queue.
          Terminal return if empty.
    B1.5  current_task is None → nothing to continue; go straight to B3.
          Not an algorithmic block. Task boundaries always re-decide freely.
    B2    _is_current_task_plausible() — a MID-TASK commitment gate. Continue
          the current task, or escalate to B3. Skipped entirely when
          self._gate_strategy == "none" (the default), in which case update()
          behaves exactly as it did before the block split.
    B3    _replan_tasks() — selects the task assignment and commits.

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
    self._strategy controls how much of the queue a given update() call
    rewrites — it does NOT change what a candidate is:
        "single_task" (default, IMPLEMENTED) — receding-horizon selection.
            Score each candidate alone (a length-1 ordering, projected from
            the live WorldState); the argmin feasible candidate becomes the
            new current_task; the rest of the queue is left as an unordered
            pool with no ordering commitment.
        "full_reorder" (NOT IMPLEMENTED) — score every permutation of
            candidates; the argmin permutation becomes the entire new queue.
            _project() raises NotImplementedError for orderings longer than
            1, pending the WorldState-continuity design that multi-task
            projection depends on (guard/effects retraction semantics).
    Rationale for defaulting to single_task: the human-prediction horizon H is
    already belief-bounded and uncertain beyond it — committing to a
    multi-task robot schedule optimized against that same uncertain horizon
    has a weaker justification than re-deciding at each trigger from fresh
    WorldState/belief. See design_decisions.md, DESIGN-16, for the full
    argument.

STILL OPEN (do not resolve inline while implementing — see TODOS_AND_DEFERRED.md):
    DESIGN-08 (soft interference penalty in _cost() — hard-gate only for now,
    see _cost()'s docstring), DESIGN-09 (pre-RESELECT cheap filter — not
    implemented, every candidate is fully projected and checked), DESIGN-10
    (interference sampling — discretized_time_sampling() is the current
    default algorithm; closest_point_of_approach() is a documented,
    unimplemented alternative — see shared/trajectory_algorithms.py),
    DESIGN-12 (horizon-projected confidence — relevant only to full_reorder,
    moot under single_task), DESIGN-13 (obstacle-aware path realization —
    straight_line_path() is the current default; see
    shared/trajectory_algorithms.py), DESIGN-16 (see STRATEGY above). None
    block the single_task implementation below.
"""

import logging
from typing import Callable, List, Literal, Optional

from shared.types import (
    BeliefState,
    WorldState,
    TaskInstance,
    ProjectedPlan,
    InterferenceAssessment,
    ExecutorState,
    TriggerDecision,
    UpdateResult,
    Segment,
    ConflictPoint,
    task_instance_key,
)


from shared.domain_knowledge import DomainKnowledgeBase
from shared.recognizer import IntentionRecognizer
from shared.projection import Projector
from shared.trajectory_algorithms import discretized_time_sampling

class MetaPlanner:
    """
    See shared/io_contracts.md §2.2 for the interface contract this class implements.
    """

    def __init__(
        self,
        knowledge: DomainKnowledgeBase,
        projector: Projector,
        recognizer: IntentionRecognizer,
        theta: float = 0.75,
        min_safe_distance: float = 1.0,
        strategy: Literal["single_task", "full_reorder"] = "single_task",
        gate_strategy: Literal["none", "b2a", "b2b"] = "none",
        interference_algorithm: Callable[[Segment, Segment], List[ConflictPoint]] = discretized_time_sampling,
        human_agent_id: Optional[str] = None,
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
                                 only — never fed into _cost() as a magnitude.
        min_safe_distance:       distance threshold below which a ConflictPoint makes a
                                 candidate infeasible (see _detect_interference()).
                                 Placeholder default, same "needs calibration" status as
                                 assumed_speed — not derived from any domain config yet.
        strategy:                B3's strategy — "single_task" (default, implemented) or
                                 "full_reorder" (not yet functional). Selects what a
                                 candidate is inside _replan_tasks(): an individual task,
                                 or a permuted ordering. See module docstring, DESIGN-16. DESIGN-16.
        gate_strategy:           B2, the mid-task plausibility gate. "none" (default)
                                 skips B2 entirely — update() then behaves exactly as it
                                 did before the block split. "b2a" (assess current task in
                                 isolation) and "b2b" (compare current against other tasks
                                 individually) are not yet implemented. Independent of
                                 `strategy`; all combinations are intended to be runnable.
        interference_algorithm:  function(Segment, Segment) -> List[ConflictPoint].
                                 Defaults to trajectory_algorithms.discretized_time_sampling.
                                 closest_point_of_approach is a documented, unimplemented
                                 drop-in alternative — same signature, swap here when built.
        human_agent_id:          agent_id of the human this robot observes, for building
                                 the human's predicted projection in update(). Mirrors
                                 RobotAgent.observed_agent_id's existing optionality —
                                 None means no human projection is built and every
                                 candidate is scored without an interference check
                                 (treated as feasible by default), matching how
                                 RobotAgent already tolerates no observed human.
        """
        self._knowledge = knowledge
        self._recognizer = recognizer
        self._projector = projector
        self._theta = theta
        self._min_safe_distance = min_safe_distance
        self._strategy = strategy
        self._gate_strategy = gate_strategy
        self._interference_algorithm = interference_algorithm
        self._human_agent_id = human_agent_id
        self._queue: List[TaskInstance] = []  # owned internally per Q1; populated by seed_tasks()
        # Tick-to-tick comparison state for evaluate_triggers()'s theta_crossed and
        # task_commit checks. evaluate_triggers() has no prev_belief/prev_executor_state
        # params (unlike replanning.py's should_replan()) — this is owned internally,
        # same as the queue.
        self._prev_belief: Optional[BeliefState] = None
        self._prev_executor_state: Optional[ExecutorState] = None

        
    # =========================================================================
    # Public interface (shared/io_contracts.md §2.2)
    # =========================================================================

    def evaluate_triggers(
        self,
        belief: BeliefState,
        world: WorldState,
        executor_state: ExecutorState,
    ) -> TriggerDecision:
        """
        Replaces replanning.py's should_replan(). Event-driven only.

        Three real triggers:
            - no_current_task: executor_state.current_task is None. Covers BOTH
              t=0 (see seed_tasks()) AND ordinary task completion — this assumes
              whoever builds ExecutorState (sim_agents.py, step 9) clears
              current_task to None once a task's plan finishes, mirroring the
              existing current_plan=None pattern in RobotAgent.step(). If that
              wiring choice changes, a separate task_completed check would need
              to be reintroduced here.
            - theta_crossed: belief.confidence crosses self._theta from below to
              at/above it (DESIGN-07: single threshold, no hysteresis — this is a
              crossing event, not "confidence >= theta" every tick, or it would
              refire continuously while confidence stays high).
            - task_commit: executor_state.holding transitions from None to
              not-None (robot just picked something up).

        Confidence is a gate here (via theta_crossed), never a magnitude fed into
        _cost().
        """
        if executor_state.current_task is None:
            decision = TriggerDecision(fired=True, reason="no_current_task", score=1.0)
        else:
            theta_crossed = (
                self._prev_belief is not None
                and self._prev_belief.confidence < self._theta <= belief.confidence
            )
            task_committed = (
                self._prev_executor_state is not None
                and self._prev_executor_state.holding is None
                and executor_state.holding is not None
            )

            if theta_crossed:
                decision = TriggerDecision(fired=True, reason="theta_crossed", score=belief.confidence)
            elif task_committed:
                decision = TriggerDecision(fired=True, reason="task_committed", score=1.0)
            else:
                decision = TriggerDecision(fired=False, reason="none", score=0.0)

        self._prev_belief = belief
        self._prev_executor_state = executor_state
        return decision


    def update_human_projection(
        self,
        belief: BeliefState,
        world: WorldState,
    ) -> Optional[ProjectedPlan]:
        """
        Thin wrapper over Projector.project_human(), supplying the recognizer and
        human_agent_id this MetaPlanner was constructed with. Call once per fired
        trigger, between evaluate_triggers() and update(); pass the result to
        update() as its human_projection argument.

        Returns None if no human is observed or the hypothesis cannot be resolved
        — update() then treats every candidate as feasible and runs no
        interference check that call.
        """
        return self._projector.project_human(
            belief=belief,
            world=world,
            human_agent_id=self._human_agent_id,
            recognizer=self._recognizer,
        )
    
    
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
        ([current_task] if not None else []) + self._queue.

        Note the pool is NOT called "candidates". Candidates come into
        existence only inside B3, and what they are depends on B3's strategy —
        individual tasks under single_task, permuted orderings under
        full_reorder. Nothing is competing for anything at this level.

        BLOCK STRUCTURE:
            0.    assemble the task pool; terminal return if empty
            B1.5  no current task → nothing to continue, go straight to B3
            B2    _is_current_task_plausible() — continue, or escalate to B3
            B3    _replan_tasks() — select and commit

        `human_projection` is supplied by the caller, built once per fired
        trigger via update_human_projection(). Not rebuilt here, not recomputed
        per candidate. None means no human observed or the hypothesis was
        unresolvable — every candidate is then scored without an interference
        check, not treated as always-conflicting.

        TERMINAL STATE: returns UpdateResult(current_task=None, queue=[]) when
        the pool is empty (queue empty and nothing executing) — all assigned
        tasks are complete. A normal return, not an exception; callers check
        `result.current_task is None`.
        """
        task_pool: List[TaskInstance] = list(self._queue)
        if executor_state.current_task is not None:
            task_pool = [executor_state.current_task] + task_pool

        if not task_pool:
            # Terminal state, not an error: all assigned tasks are complete.
            # Returned rather than raised so the embodiment layer learns this
            # from the contract instead of catching an exception — see
            # design_decisions.md, mind/body separation.
            return UpdateResult(current_task=None, queue=[])

        # ---- B1.5: no current task, so there is nothing to continue --------
        # Not an algorithmic block. Task boundaries always re-decide freely;
        # B2 is specifically a MID-TASK commitment mechanism.
        if executor_state.current_task is not None:
            # ---- B2: plausibility gate on the current task ------------------
            if self._is_current_task_plausible(
                belief=belief,
                world=world,
                executor_state=executor_state,
                human_projection=human_projection,
                task_pool=task_pool,
            ):
                # Continuation: queue untouched, current task keeps executing.
                return UpdateResult(
                    current_task=executor_state.current_task,
                    queue=list(self._queue),
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
    ) -> bool:
        """
        SKELETON — not yet implemented (TODO-36).

        Decides whether the currently-executing task should keep executing, or
        whether the situation warrants escalating to B3. Called only when
        executor_state.current_task is not None (see update()'s B1.5).

        This is a WORTHINESS check, not a feasibility check. The current task
        may remain perfectly doable but only via a long pause or detour;
        "doable" is not the question. Naming reflects that — "feasible" and
        "should_continue" were both rejected as implying a bare collision test.

        Returns True to continue the current task, False to escalate to B3.

        Strategies (self._gate_strategy):
            "none" (default) — no gate; always escalate. update() then behaves
                exactly as it did before the block split.
            "b2a"  — assess the current task in isolation. Needs a scalar
                worthiness score derived from the current task's projection
                against human_projection. NOT IMPLEMENTED.
            "b2b"  — compare the current task against the other tasks in
                task_pool individually; continue only if it wins by a clear
                margin. Redundant with B3 under single_task by construction —
                a redundancy control for ablation, not a fourth policy.
                NOT IMPLEMENTED.

        `task_pool` is unused under "b2a" and is present only so the signature
        does not change when "b2b" is filled in.
        """
        if self._gate_strategy == "none":
            return False

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
            full_reorder — each permutation of the pool is a candidate.
                           NOT IMPLEMENTED; _project() also refuses orderings
                           longer than 1 (DESIGN-16).

        single_task detail: each candidate is projected alone from the live
        WorldState, interference-checked against human_projection if one was
        built, infeasible candidates dropped before cost is computed. The
        argmin over survivors becomes current_task; the rest form the queue in
        whatever order they happened to iterate — order carries no commitment
        under this strategy, it is re-decided next trigger.

        current_task, if any, is an ordinary member of task_pool and competes
        on identical terms. Continuation vs. reselection falls out of the
        argmin; there is no branch for either outcome here. (The one explicit
        continuation branch in the design lives in update()'s B2, which decides
        whether this method runs at all — not what it decides once it does.)

        The RuntimeError below (every candidate excluded by
        _detect_interference()) is a genuine anomaly and stays an exception,
        deliberately distinguishable from update()'s terminal return.
        """
        if self._strategy == "full_reorder":
            raise NotImplementedError(
                "MetaPlanner._replan_tasks: 'full_reorder' strategy is not yet "
                "implemented — see design_decisions.md, DESIGN-16. "
                "_project() raises NotImplementedError for orderings longer "
                "than 1, which this strategy would require."
            )
        if self._strategy != "single_task":
            raise ValueError(f"MetaPlanner: unknown strategy '{self._strategy}'")

        scored: List[tuple] = []
        for task in task_pool:
            projection = self._projector.project([task], world, executor_state.agent_id, belief, start_step=0.0)
            if human_projection is not None:
                assessment = self._detect_interference(projection, human_projection)
            else:
                assessment = InterferenceAssessment(feasible=True, conflicts=[])

            logging.info(
                f"[meta-cand] {task_instance_key(task)} "
                f"cost={projection.total_estimated_cost} "
                f"feasible={assessment.feasible} "
                f"conflicts={len(assessment.conflicts)} "
                f"min_dist={min((c.distance for c in assessment.conflicts), default=None)}"
            )
            if assessment.feasible:
                scored.append((self._cost(projection, assessment), task))

        if not scored:
            raise RuntimeError(
                "MetaPlanner._replan_tasks: no feasible candidate task this "
                "trigger (every candidate excluded by _detect_interference())."
            )

        _, winner = min(scored, key=lambda pair: pair[0])
        new_queue = [t for t in task_pool if t is not winner]
        self._queue = new_queue
        return UpdateResult(current_task=winner, queue=list(new_queue))
    
    
    def _detect_interference(
        self,
        robot_projection: ProjectedPlan,
        human_projection: ProjectedPlan,
    ) -> InterferenceAssessment:
        """
        Compares every Segment in robot_projection against every Segment in
        human_projection via self._interference_algorithm (default:
        trajectory_algorithms.discretized_time_sampling — swap to
        closest_point_of_approach or another algorithm via the constructor's
        interference_algorithm param once one is implemented). Segment pairs
        with no step-time overlap contribute no ConflictPoints — the
        algorithm functions handle that themselves.

        feasible = no returned ConflictPoint has distance below
        self._min_safe_distance (hard exclusion only — DESIGN-08's soft
        penalty is not applied here, see _cost()).

        Operates on ProjectedPlan/ProjectedPlanEntry generically via
        entry.segments — unchanged by the single_task vs. full_reorder
        decision; a single_task ProjectedPlan is just a 1-entry instance of
        the same structure this was already designed to consume.
        """
        robot_segments = [seg for entry in robot_projection.entries for seg in entry.segments]
        human_segments = [seg for entry in human_projection.entries for seg in entry.segments]

        conflicts: List[ConflictPoint] = []
        for robot_seg in robot_segments:
            for human_seg in human_segments:
                conflicts.extend(self._interference_algorithm(robot_seg, human_seg))

        feasible = not any(cp.distance < self._min_safe_distance for cp in conflicts)

        return InterferenceAssessment(feasible=feasible, conflicts=conflicts)

    def _cost(
        self,
        projection: ProjectedPlan,
        assessment: InterferenceAssessment,
    ) -> int:
        """
        Hard-gate only, for now (DESIGN-08 — soft interference penalty
        deferred, see module docstring and TODOS_AND_DEFERRED.md).
        assessment.feasible already excludes a candidate before this is even
        called (see update()) — this returns execution cost only.
        assessment.conflicts is available here but deliberately unused until
        DESIGN-08 is revisited with an actual penalty formula.

        No carrying parameter, no cancellation branch — cancellation cost is
        already reflected in projection's step count via planner.py's guarded
        method selection (see design_decisions.md).
        """
    
        return projection.total_estimated_cost
