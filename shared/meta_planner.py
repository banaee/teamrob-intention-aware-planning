"""
shared/meta_planner.py

PURPOSE:
    Owns robot task scheduling: which tasks, in what order. Sits above planner.py
    (decomposes one task) and replaces replanning.py (trigger-only). Called by
    sim_agents.py; calls planner.py per candidate ordering to project execution.

    See shared/io_contracts.md §2.2 for the authoritative interface contract.
    See design_decisions.md, "Cancellation is not a meta_planner cost term",
    for why _cost() carries no carrying/cancellation logic.

WHAT THIS MODULE DOES:
    - Owns the robot's task queue internally (Q1) — never passed in or out except
      inside UpdateResult
    - Decides WHETHER to re-evaluate task order (evaluate_triggers)
    - Decides WHICH task to do next and in what order the rest follow (update)
    - Projects candidate orderings and the human's predicted task for interference
      checking, using planner.py per candidate — never decomposes tasks itself

WHAT THIS MODULE DOES NOT DO:
    - Does NOT decompose a task into actions (that is planner.py)
    - Does NOT compute cancellation cost as a separate term (resolved intrinsically
      by planner.py's guarded method selection on the task itself)
    - Does NOT know about Mesa steps or ROS callbacks — simulators decide WHEN to
      call evaluate_triggers()/update(); this module decides WHAT counts as a trigger
    - Does NOT import from mesa_sim/ or ros_sim/

CANDIDATE SET (settled design, see design_decisions.md):
    current_task competes as just another candidate — no special-case WAIT/RESELECT
    branch. Every update() call evaluates {current_task} ∪ remaining_tasks through
    the identical pipeline. Continuation vs. reselection falls out of cost
    comparison, not a separate decision.

STILL OPEN (do not resolve inline while implementing — see TODOS_AND_DEFERRED.md):
    DESIGN-09 (pre-RESELECT cheap filter), DESIGN-10 (interference sampling
    granularity), DESIGN-12 (horizon-projected confidence), DESIGN-13 (common
    path-realization estimator). None block this skeleton or the first real
    implementations.
"""

from typing import List, Optional

from shared.types import (
    BeliefState,
    WorldState,
    TaskInstance,
    AbstractPlan,
    ProjectedPlan,
    InterferenceAssessment,
    ExecutorState,
    TriggerDecision,
    UpdateResult,
)
from shared.domain_knowledge import DomainKnowledgeBase


class MetaPlanner:
    """
    See shared/io_contracts.md §2.2 for the interface contract this class implements.
    """

    def __init__(
        self,
        knowledge: DomainKnowledgeBase,
        theta: float = 0.75,
        assumed_speed: float = 1.0,
        default_action_cost: float = 1.0,
    ):
        """
        knowledge:           HTN domain knowledge, passed through to planner.py calls.
        theta:                cognitive-clock confidence threshold (DESIGN-07). Gate
                              only — never fed into _cost() as a magnitude.
        assumed_speed:        world-units per estimation-unit for movement actions
                              (Q3: distance / assumed_speed). Placeholder default —
                              needs calibration against Mesa's real step counts during
                              scenario_00 validation, not a tuned value yet.
        default_action_cost:  fallback cost for non-movement actions when
                              knowledge.get_cost(action_name) has no entry in
                              costs.yaml. Also a placeholder default.
        """
        self._knowledge = knowledge
        self._theta = theta
        self._assumed_speed = assumed_speed
        self._default_action_cost = default_action_cost
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

        Two real triggers:
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
            decision = TriggerDecision(replan=True, reason="no_current_task", score=1.0)
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
                decision = TriggerDecision(replan=True, reason="theta_crossed", score=belief.confidence)
            elif task_committed:
                decision = TriggerDecision(replan=True, reason="task_committed", score=1.0)
            else:
                decision = TriggerDecision(replan=False, reason="none", score=0.0)

        self._prev_belief = belief
        self._prev_executor_state = executor_state
        return decision

    def update(
        self,
        belief: BeliefState,
        world: WorldState,
        executor_state: ExecutorState,
    ) -> UpdateResult:
        """
        Main entry point when evaluate_triggers() fires. Orchestrates:
            1. Build the human's predicted ProjectedPlan once (via _project(),
               using recognizer.get_hypothesis() to resolve belief.most_likely —
               see Q2) — candidate-independent, computed once per call, not
               per candidate.
            2. Enumerate candidate orderings over {current_task} ∪ remaining_tasks.
            3. For each candidate: _project() the robot's ordering, run
               _detect_interference() against the human's projection (from step 1),
               and if feasible, _cost() it.
            4. Select the minimum-cost feasible candidate; update self._queue.

        current_task competes as just another candidate — no special-case branch.
        """
        raise NotImplementedError

    # =========================================================================
    # Internal (not part of io_contracts.md — private to this class)
    # =========================================================================

    def initialize_queue(
        self,
        tasks: List[TaskInstance],
        world: WorldState,
        agent_id: str,
    ) -> List[TaskInstance]:
        """
        Called once at t=0, before any belief exists. Produces Q0 via a base-cost
        heuristic (nearest-item-first or similar) over the unordered assigned_tasks
        set. No IR dependency.
        """
        raise NotImplementedError

    def _project(
        self,
        ordering: List[TaskInstance],
        world: WorldState,
        agent_id: str,
        start_step: int,
    ) -> ProjectedPlan:
        """
        Builds a ProjectedPlan for a full candidate ordering — not a single task in
        isolation. Required to catch downstream interference (e.g. a predicted
        collision at queue position 2 while position 1 is still executing).

        Decomposes each task in `ordering` via planner.py (AdaptivePlanner.plan()),
        starting from the live WorldState — so a partially-executed current_task is
        projected from where the agent actually is, not from scratch.

        Also used for the human's predicted single-task "ordering" (via
        get_hypothesis()) — this method is agent-agnostic, not robot-specific.
        """
        raise NotImplementedError

    def _estimate_duration(
        self,
        plan: AbstractPlan,
        world: WorldState,
    ) -> int:
        """
        Self-contained geometric estimate (distance / assumed_speed) — no simulator
        step-size dependency (Q3).

        Movement actions (schema.movement_target_key is not None): distance from
        current position to target / self._assumed_speed. Current position starts
        at world.agent_positions[agent_id] and advances to each movement action's
        target as the walk proceeds — later actions in the plan are estimated from
        where the agent will be, not from world's current snapshot position.

        Non-movement actions: self._knowledge.get_cost(action_name), falling back
        to self._default_action_cost if costs.yaml has no entry. This includes
        wait_at — its real ISO-8601 ?duration binding is a mesa_sim/action_decomposer.py
        concern shared/ has no access to; this is a known simplification (does not
        distinguish a long wait from a short one), not a considered design decision.
        Worth revisiting if scenario_00 validation shows it producing bad orderings
        around foreseeable tasks.

        Only movement_target_type == "object" is handled — "zone" targets were
        removed from the live domain (see actions.py), but this raises explicitly
        rather than silently mis-estimating if one reappears.
        """
        if not plan.actions:
            return 0

        agent_id = plan.actions[0].bindings.get("?agent")
        if agent_id is None:
            raise ValueError(
                f"MetaPlanner._estimate_duration: no '?agent' binding on first "
                f"action of plan for '{plan.goal_intention}'"
            )
        current_pos = world.agent_positions.get(agent_id)
        if current_pos is None:
            raise ValueError(
                f"MetaPlanner._estimate_duration: no position for agent "
                f"'{agent_id}' in world.agent_positions"
            )

        total = 0.0
        for action in plan.actions:
            schema = action.schema

            if schema.movement_target_key is not None:
                if schema.movement_target_type != "object":
                    raise ValueError(
                        f"MetaPlanner._estimate_duration: unsupported "
                        f"movement_target_type '{schema.movement_target_type}' "
                        f"for action '{action.action_name}' — only 'object' is "
                        f"handled (zone targets removed from live domain)"
                    )
                target_id = action.bindings.get(schema.movement_target_key)
                target_pos = world.object_positions.get(target_id)
                if target_pos is None:
                    raise ValueError(
                        f"MetaPlanner._estimate_duration: no position for target "
                        f"'{target_id}' in world.object_positions "
                        f"(action '{action.action_name}')"
                    )
                dx = target_pos[0] - current_pos[0]
                dy = target_pos[1] - current_pos[1]
                distance = (dx * dx + dy * dy) ** 0.5
                total += distance / self._assumed_speed
                current_pos = target_pos
            else:
                cost = self._knowledge.get_cost(action.action_name)
                total += cost if cost is not None else self._default_action_cost

        return int(round(total))

    def _detect_interference(
        self,
        robot_projection: ProjectedPlan,
        human_projection: ProjectedPlan,
    ) -> InterferenceAssessment:
        """
        Compares the robot's projected trajectory against the human's predicted
        trajectory. Returns feasible (hard exclusion — required resource occupied
        by predicted human position) and conflicts (all observed overlap points,
        feasible or not) — observation only. _cost() is the sole place these
        become a numeric penalty (see InterferenceAssessment docstring, DESIGN-08).
        """
        raise NotImplementedError

    def _cost(
        self,
        projection: ProjectedPlan,
        assessment: InterferenceAssessment,
    ) -> int:
        """
        execution_cost + interference_penalty for a feasible candidate. No
        carrying parameter, no cancellation branch — cancellation cost is already
        reflected in projection's step count via planner.py's guarded method
        selection (see design_decisions.md).
        """
        raise NotImplementedError