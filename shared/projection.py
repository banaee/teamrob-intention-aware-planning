"""
shared/projection.py

PURPOSE:
    Turns a task into a predicted trajectory. Given a TaskInstance, an agent, and a
    WorldState, produces a ProjectedPlan: the decomposed AbstractPlan plus per-action
    Segments describing where that agent will be, and when.

    Agent-agnostic by construction — the same call projects a robot candidate or the
    human's predicted task. Nothing here knows about task *selection*; that is
    meta_planner.py's job.

WHY THIS IS ITS OWN MODULE:
    Projection was originally private to MetaPlanner (_project, _build_segments,
    _estimate_duration, plus inline human-projection code in update()). But turning a
    task into a trajectory is not selection logic — MetaPlanner merely consumes it.
    Several planned consumers want projection without wanting selection:
      - DESIGN-13's path-realization estimator (Phase 4D low-level planner)
      - visualization drawing predicted human/robot paths
      - Phase 5 evaluation measuring prediction quality against actual behaviour
    Under the old structure each would have had to reach into MetaPlanner's privates
    or duplicate the logic.

LAYERING (one-way, no cycles):
    trajectory_algorithms.py   pure geometry — Segment in, ConflictPoint/Segment out
            ↓
    projection.py              task + world → trajectory
            ↓
    meta_planner.py            which trajectory to pick

WHAT THIS MODULE DOES NOT DO:
    - Does NOT decide which task to do (meta_planner.py)
    - Does NOT detect interference or compute cost (meta_planner.py)
    - Does NOT update beliefs (recognizer.py)
    - Does NOT import from mesa_sim/ or ros_sim/
"""

from typing import List, Optional

from shared.types import (
    BeliefState,
    WorldState,
    TaskInstance,
    AbstractPlan,
    ProjectedPlan,
    ProjectedPlanEntry,
    Segment,
    Var,
    Const,
    task_instance_key,
)
from shared.domain_knowledge import DomainKnowledgeBase
from shared.planner import AdaptivePlanner
from shared.recognizer import IntentionRecognizer
from shared.trajectory_algorithms import straight_line_path, stationary_segment


class Projector:
    """
    Builds ProjectedPlans. Owns its own AdaptivePlanner — projection always
    decomposes from scratch against the live WorldState, never resumes a
    partially-executed plan (see design_decisions.md, "Plans are re-decomposed
    from scratch; the world state is the execution cursor").
    """

    def __init__(
        self,
        knowledge: DomainKnowledgeBase,
        assumed_speed: float = 1.0,
        default_action_cost: float = 1.0,
    ):
        """
        knowledge:            HTN domain knowledge, passed through to planner.py calls
                              and used for per-action cost lookup.
        assumed_speed:        world-units per estimation-unit for movement actions
                              (distance / assumed_speed). Placeholder default — needs
                              calibration against the simulator's real step scale
                              (TODO-28), not a tuned value.
        default_action_cost:  fallback duration for non-movement actions when
                              knowledge.get_cost(action_name) has no costs.yaml entry.
                              Also a placeholder.
        """
        self._knowledge = knowledge
        self._planner = AdaptivePlanner(knowledge=knowledge)
        self._assumed_speed = assumed_speed
        self._default_action_cost = default_action_cost

    # =========================================================================
    # Public
    # =========================================================================

    def project(
        self,
        ordering: List[TaskInstance],
        world: WorldState,
        agent_id: str,
        belief: BeliefState,
        start_step: float = 0.0,
    ) -> ProjectedPlan:
        """
        Builds a ProjectedPlan for `ordering`.

        len(ordering) == 1 — the only implemented path:
            Decomposes the one task via planner.plan(), starting from the live
            WorldState — so a partially-executed task is projected from where the
            agent actually is, not from scratch. No cross-task WorldState chaining
            involved. `belief` is forwarded to planner.plan() as-is (required, no
            default on that signature); callers always have a real belief available,
            unlike the human script path in sim_agents.py which fabricates a dummy
            one because it has no IR at all.

        len(ordering) > 1 — only reachable under MetaPlanner's "full_reorder"
        strategy:
            NOT YET IMPLEMENTED, and deliberately so. For task 2+ in an ordering,
            the WorldState passed to planner.plan() would need to reflect the world
            as if every prior task in the ordering already completed — blocked on a
            WorldState-continuity design question (guard/effects retraction
            semantics; see TODO-07 and design_decisions.md, DESIGN-16). Not solved
            with a narrow position/holding stopgap here, which would silently fail
            for any guard depending on a different predicate.

        Agent-agnostic: the same call projects a robot candidate or the human's
        predicted task (see project_human()).
        """
        if len(ordering) > 1:
            raise NotImplementedError(
                "Projector.project: multi-task ordering projection requires "
                "resolving cross-task WorldState continuity — see TODO-07 and "
                "design_decisions.md, DESIGN-16. Not needed while MetaPlanner's "
                "strategy is 'single_task'."
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

        segments = self.build_segments(abstract_plan, world, agent_id, start_step)
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

    def project_human(
        self,
        belief: BeliefState,
        world: WorldState,
        human_agent_id: Optional[str],
        recognizer: IntentionRecognizer,
    ) -> Optional[ProjectedPlan]:
        """
        Builds the human's predicted trajectory from the current belief.

        Resolves belief.most_likely back to its HypothesisKey via
        recognizer.get_hypothesis(), rebuilds it as a TaskInstance, and projects it
        exactly as a robot candidate would be — project() is agent-agnostic, so
        there is no separate human projection path.

        Called once per fired cognitive-clock trigger — not per tick, and not per
        candidate. The human's predicted trajectory is a fact about the world at
        this event, independent of which robot task is being evaluated.

        Returns None in three distinct cases, all normal rather than errors:
          - no human is observed (human_agent_id is None)
          - get_hypothesis() cannot resolve belief.most_likely (e.g. "unknown")
          - the resolved task name is not in the domain's task schemas
        A None projection means the caller runs no interference check that call.
        """
        if human_agent_id is None:
            return None

        hypothesis = recognizer.get_hypothesis(belief.most_likely)
        if hypothesis is None:
            return None

        human_task_schema = self._knowledge.get_task_schema(hypothesis.task_name)
        if human_task_schema is None:
            return None

        human_task = TaskInstance(
            schema=human_task_schema,
            bindings={Var(k): Const(v) for k, v in hypothesis.bindings.items()},
        )
        return self.project(
            [human_task], world, human_agent_id, belief, start_step=0.0
        )

    def build_segments(
        self,
        plan: AbstractPlan,
        world: WorldState,
        agent_id: str,
        start_step: float = 0.0,
    ) -> List[Segment]:
        """
        Per-action straight-line motion/hold Segments for `plan`, starting from the
        agent's live position at `start_step`. Single geometry pass, chained
        head-to-tail in both position and step-time.

        Movement actions (schema.movement_target_key is not None): resolved via
        trajectory_algorithms.straight_line_path() — the current default path
        realization. Only movement_target_type == "object" is handled; "zone"
        targets were removed from the live domain (see domains/kitting/actions.py),
        and this raises explicitly rather than silently mis-estimating if one
        reappears. Obstacle-aware, non-linear realization is DESIGN-13 / TODO-09
        (Phase 4D) — see trajectory_algorithms.obstacle_aware_path().

        Non-movement actions: trajectory_algorithms.stationary_segment(), held for
        knowledge.get_cost(action_name) steps, falling back to default_action_cost.
        This includes wait_at — its real ISO-8601 ?duration binding is parsed in
        mesa_sim/action_decomposer.py, which shared/ cannot import, so a 60-second
        coffee break and a 2-second toggle currently cost the same (TODO-32). Known
        simplification, not a considered design decision.
        """
        current_pos = world.agent_positions.get(agent_id)
        if current_pos is None:
            raise ValueError(
                f"Projector.build_segments: no position for agent "
                f"'{agent_id}' in world.agent_positions"
            )

        segments: List[Segment] = []
        current_step = start_step

        for action in plan.actions:
            schema = action.schema

            if schema.movement_target_key is not None:
                if schema.movement_target_type != "object":
                    raise ValueError(
                        f"Projector.build_segments: unsupported "
                        f"movement_target_type '{schema.movement_target_type}' "
                        f"for action '{action.action_name}' — only 'object' is "
                        f"handled (zone targets removed from live domain)"
                    )
                target_id = action.bindings.get(schema.movement_target_key)
                target_pos = world.object_positions.get(target_id)
                if target_pos is None:
                    raise ValueError(
                        f"Projector.build_segments: no position for target "
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
            current_step = segment.end_step

        return segments

    def estimate_duration(
        self,
        plan: AbstractPlan,
        world: WorldState,
        agent_id: str,
        start_step: float = 0.0,
    ) -> int:
        """
        Total estimated steps to complete `plan` — the span of build_segments()'s
        output. Convenience wrapper for callers that want only the number.

        project() does NOT call this: it needs the Segments themselves for the
        ProjectedPlanEntry, and calling this would trigger a second, redundant
        geometry pass. Currently unused (TODO-31) — kept because it is the natural
        entry point for a caller wanting duration without a full projection.
        """
        segments = self.build_segments(plan, world, agent_id, start_step)
        if not segments:
            return 0
        return int(round(segments[-1].end_step - segments[0].start_step))
