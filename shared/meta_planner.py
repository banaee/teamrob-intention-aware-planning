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

CANDIDATE SET (settled design, see design_decisions.md):
    "Candidate" always means an individual task — never an ordering. The
    candidate set for every update() call is {current_task} ∪ remaining_tasks.
    current_task competes as just another candidate — no special-case
    WAIT/RESELECT branch. Continuation vs. reselection falls out of cost
    comparison, not a separate decision — there is no distinct "go for
    reselect" step; an infeasible or costlier current_task is simply excluded
    or outscored like any other candidate would be.

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
        assumed_speed:           forwarded to Projector — world-units per estimation-unit
                                 for movement actions. Uncalibrated placeholder (TODO-28).
        default_action_cost:     forwarded to Projector — fallback duration for
                                 non-movement actions with no costs.yaml entry. Also a
                                 placeholder.
        min_safe_distance:       distance threshold below which a ConflictPoint makes a
                                 candidate infeasible (see _detect_interference()).
                                 Placeholder default, same "needs calibration" status as
                                 assumed_speed — not derived from any domain config yet.
        strategy:                "single_task" (default, implemented) or "full_reorder"
                                 (not yet functional) — see module docstring, DESIGN-16.
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
        Main entry point when evaluate_triggers() fires.

        Queue invariant (settled this session): self._queue holds only tasks
        NOT currently executing. The in-progress task, if any, lives solely in
        executor_state.current_task — it is not also a member of self._queue.
        Candidates = ([executor_state.current_task] if not None else []) +
        self._queue. On a winner: if it's the same object as current_task,
        the queue is untouched (continuation); if different, the winner is
        removed from the candidate list to form the new queue and the
        abandoned current_task (if any) is implicitly back in the pool via
        that same list. No special-case branch for either outcome — both fall
        out of the identical argmin.

        single_task strategy (the only implemented path):
            1. `human_projection` is supplied by the caller, built once per fired
               trigger via update_human_projection(). Not rebuilt here, not
               recomputed per candidate. None means no human observed or the
               hypothesis was unresolvable — every candidate is then scored
               without an interference check, not treated as always-conflicting.
            2. For each candidate: _project([task], ...) alone, then
               _detect_interference() against the human's projection (if
               built). Infeasible candidates are dropped before cost is even
               computed.
            3. argmin _cost() over the feasible survivors becomes the new
               current_task; the queue is every other candidate, in whatever
               order they happened to iterate — order carries no commitment
               under this strategy, it will be re-decided next trigger.

        full_reorder strategy: NOT YET IMPLEMENTED — raises NotImplementedError.
        _project() itself already refuses orderings longer than 1 (DESIGN-16).

        TERMINAL STATE: returns UpdateResult(current_task=None, queue=[]) when
        no candidates remain (queue empty and nothing executing) — all assigned
        tasks are complete. This is a normal return, not an exception; callers
        check `result.current_task is None`. The remaining RuntimeError in this
        method (every candidate excluded by _detect_interference()) is a genuine
        anomaly and stays an exception, deliberately distinguishable from this.
        """
        candidates: List[TaskInstance] = list(self._queue)
        if executor_state.current_task is not None:
            candidates = [executor_state.current_task] + candidates

        if not candidates:
            # Terminal state, not an error: all assigned tasks are complete.
            # Returned rather than raised so the embodiment layer learns this
            # from the contract instead of catching an exception — see
            # design_decisions.md, mind/body separation.
            return UpdateResult(current_task=None, queue=[])

        if self._strategy == "full_reorder":
            raise NotImplementedError(
                "MetaPlanner.update: 'full_reorder' strategy is not yet "
                "implemented — see design_decisions.md, DESIGN-16. "
                "_project() raises NotImplementedError for orderings longer "
                "than 1, which this strategy would require."
            )
        if self._strategy != "single_task":
            raise ValueError(f"MetaPlanner: unknown strategy '{self._strategy}'")


        scored: List[tuple] = []
        for task in candidates:
            projection = self._projector.project([task], world, executor_state.agent_id, belief, start_step=0.0)
            if human_projection is not None:
                assessment = self._detect_interference(projection, human_projection)
            else:
                assessment = InterferenceAssessment(feasible=True, conflicts=[])
            
            logging.info(
            # f"[meta-cand] {task_instance_key(task)} "
            f"cost={projection.total_estimated_cost} "
            f"feasible={assessment.feasible} "
            f"conflicts={len(assessment.conflicts)} "
            f"min_dist={min((c.distance for c in assessment.conflicts), default=None)}"
        )
            if assessment.feasible:
                scored.append((self._cost(projection, assessment), task))

        if not scored:
            raise RuntimeError(
                "MetaPlanner.update: no feasible candidate task this trigger "
                "(every candidate excluded by _detect_interference())."
            )

        _, winner = min(scored, key=lambda pair: pair[0])
        new_queue = [t for t in candidates if t is not winner]
        self._queue = new_queue
        return UpdateResult(current_task=winner, queue=list(new_queue))

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

    def _build_segments(
        self,
        plan: AbstractPlan,
        world: WorldState,
        agent_id: str,
        start_step: float,
    ) -> List[Segment]:
        """
        Per-action straight-line motion/hold Segments for `plan`, starting from
        the agent's live position at `start_step`. Single geometry pass, reused
        by _project() (attaches segments to ProjectedPlanEntry for interference
        detection) and available to _estimate_duration() (sums segment spans) —
        one implementation, not two independent walks.

        Movement actions (schema.movement_target_key is not None): resolved via
        trajectory_algorithms.straight_line_path() — the current default path
        realization (see module docstring, DESIGN-13). Only
        movement_target_type == "object" is handled — "zone" targets were
        removed from the live domain (see actions.py); this raises explicitly
        rather than silently mis-estimating if one reappears.

        Non-movement actions: trajectory_algorithms.stationary_segment(), held
        for self._knowledge.get_cost(action_name) steps, falling back to
        self._default_action_cost if costs.yaml has no entry. This includes
        wait_at — its real ISO-8601 ?duration binding is a
        mesa_sim/action_decomposer.py concern shared/ has no access to; known
        simplification (does not distinguish a long wait from a short one),
        not a considered design decision. Worth revisiting if scenario_00
        validation shows it producing bad orderings around foreseeable tasks.
        """
        current_pos = world.agent_positions.get(agent_id)
        if current_pos is None:
            raise ValueError(
                f"MetaPlanner._build_segments: no position for agent "
                f"'{agent_id}' in world.agent_positions"
            )

        segments: List[Segment] = []
        current_step = start_step

        for action in plan.actions:
            schema = action.schema

            if schema.movement_target_key is not None:
                if schema.movement_target_type != "object":
                    raise ValueError(
                        f"MetaPlanner._build_segments: unsupported "
                        f"movement_target_type '{schema.movement_target_type}' "
                        f"for action '{action.action_name}' — only 'object' is "
                        f"handled (zone targets removed from live domain)"
                    )
                target_id = action.bindings.get(schema.movement_target_key)
                target_pos = world.object_positions.get(target_id)
                if target_pos is None:
                    raise ValueError(
                        f"MetaPlanner._build_segments: no position for target "
                        f"'{target_id}' in world.object_positions "
                        f"(action '{action.action_name}')"
                    )
                segment = straight_line_path(current_pos, current_step, target_pos, self._assumed_speed)
                current_pos = target_pos
            else:
                cost = self._knowledge.get_cost(action.action_name)
                duration = cost if cost is not None else self._default_action_cost
                segment = stationary_segment(current_pos, current_step, duration)

            segments.append(segment)

            logging.info(
                f"[meta-seg] {agent_id} {action.action_name} "
                f"{segment.start_pos}@{segment.start_step:.1f} -> "
                f"{segment.end_pos}@{segment.end_step:.1f}"
            )
            
            current_step = segment.end_step

        return segments

    def _estimate_duration(
        self,
        plan: AbstractPlan,
        world: WorldState,
        agent_id: str,
        start_step: float = 0.0,
    ) -> int:
        """
        Total estimated steps to complete `plan` — sum of _build_segments()'s
        per-action spans. Thin convenience wrapper; _project() does NOT call
        this, since it needs the segments themselves (for ProjectedPlanEntry)
        and would otherwise trigger a second, redundant _build_segments() call
        — it computes duration directly from the segments it already builds.
        Kept as its own method for any caller that only wants the number.

        Signature changed from the original (plan, world) — agent_id and
        start_step are now explicit params rather than agent_id being derived
        from plan.actions[0].bindings.get("?agent"). _project() always has
        both values on hand already; re-deriving agent_id from bindings was a
        workaround for not having it, not a considered design choice worth
        preserving now that every caller can just pass it through. Private
        method, not part of io_contracts.md, so this is a safe signature change.
        """
        segments = self._build_segments(plan, world, agent_id, start_step)
        if not segments:
            return 0
        return int(round(segments[-1].end_step - segments[0].start_step))

    def _project(
        self,
        ordering: List[TaskInstance],
        world: WorldState,
        agent_id: str,
        belief: BeliefState,
        start_step: float,
    ) -> ProjectedPlan:
        """
        Builds a ProjectedPlan for `ordering`.

        len(ordering) == 1 — the only path the "single_task" strategy uses,
        and the only one implemented:
            Decomposes the one task via self._planner.plan(), starting from
            the live WorldState — so a partially-executed current_task is
            projected from where the agent actually is, not from scratch.
            No cross-task WorldState chaining involved. `belief` is forwarded
            to planner.plan() as-is (required, no default on that signature) —
            _project() always has a real belief available, unlike the human
            script path in sim_agents.py, which fabricates a dummy one because
            it has no IR at all.

        len(ordering) > 1 — only reachable under "full_reorder":
            NOT YET IMPLEMENTED, and deliberately so. For task 2+ in an
            ordering, the WorldState passed to planner.plan() would need to
            reflect the world as if every prior task in the ordering already
            completed — blocked on a WorldState-continuity design question
            (guard/effects retraction semantics; see design_decisions.md,
            DESIGN-16). Not solved with a narrow stopgap here, since
            full_reorder is not the active strategy.

        Also used for the human's predicted single-task "projection" (agent-
        agnostic, not robot-specific) — wired in from update() via
        get_hypothesis().
        """
        if len(ordering) > 1:
            raise NotImplementedError(
                "MetaPlanner._project: multi-task ordering projection requires "
                "resolving cross-task WorldState continuity — see "
                "design_decisions.md, DESIGN-16. Not needed while "
                "self._strategy == 'single_task'."
            )

        task = ordering[0]
        task_params = {var.name: const.value for var, const in task.bindings.items()}

        abstract_plan = self._planner.plan(
            my_intention=task.schema.name,
            task_params=task_params,
            agent_id=agent_id,
            belief=belief,
            world=world,
        )

        segments = self._build_segments(abstract_plan, world, agent_id, start_step)
        duration = int(round(segments[-1].end_step - start_step)) if segments else 0

        entry = ProjectedPlanEntry(
            abstract_plan=abstract_plan,
            estimated_start_step=int(start_step),
            estimated_duration=duration,
            segments=segments,
        )

        return ProjectedPlan(
            task_queue=[task_instance_key(task)],
            entries=[entry],
            total_estimated_cost=duration,
        )

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
