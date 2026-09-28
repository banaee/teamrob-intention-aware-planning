"""
shared/projection.py

PURPOSE:
    Turns a task into a predicted plan. Given a TaskInstance, an agent, and a
    WorldState, produces a ProjectedPlan: the decomposed AbstractPlan plus per-action
    Segments describing where that agent will be, and when.

    Agent-agnostic by construction — the same call projects a robot candidate or the
    human's predicted task. Nothing here knows about task *selection*; that is
    meta_planner.py's job.

WHY THIS IS ITS OWN MODULE:
    Projection was originally private to MetaPlanner (_project, _build_segments,
    _estimate_duration, plus inline human-projection code in update()). But turning a
    task into a ProjectedPlan is not selection logic — MetaPlanner merely consumes it.
    Several consumers want projection without wanting selection:
      - realization (Phase 4C wait-decision revision; design_decisions.md, "The
        robot can wait"): shared/realization.py's realize(plan, human_plan,
        min_separation, decision_step) -> RealizedPlan, hold-only (T3) —
        DESIGN-13's estimator partly pulled forward; detour and an off-the-shelf
        planner stay Phase 4D. It belongs on THIS side of the layering, not in
        MetaPlanner, which supplies min_separation and consumes the result.
      - visualization drawing predicted human/robot paths
      - Phase 5 evaluation measuring prediction quality against actual behaviour
    Under the old structure each would have had to reach into MetaPlanner's privates
    or duplicate the logic.

LAYERING (one-way, no cycles; design_decisions.md, "The robot can wait"):
    trajectory_algorithms.py   pure geometry   segments in -> violating shifts / conflicts out
            |
    realization.py (hold-only) "what would these segments actually become, given the human?"
            |
    projection.py              Projector       task + world -> a ProjectedPlan's segments
            |
    meta_planner.py            MetaPlanner     which candidate to pick

WHAT THIS MODULE DOES NOT DO:
    - Does NOT decide which task to do (meta_planner.py)
    - Does NOT detect interference or compute cost: realize() in
      shared/realization.py asks the interference question on this side and
      returns the realized duration as the cost; meta_planner.py decides
      between candidates on that number (B2 `b2a` T4, B3 T10)
    - Does NOT update beliefs (recognizer.py)
    - Does NOT import from mesa_sim/ or ros_sim/
"""

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from typing import Callable, List, Optional, Sequence, Tuple

from shared.types import (
    BeliefState,
    WorldState,
    TaskInstance,
    AbstractPlan,
    GroundedAction,
    ProjectedPlan,
    ProjectedPlanEntry,
    RealizedPlan,
    Segment,
    Workspace,
    task_instance_key,
)
from shared.knowledge import TaskModel
from shared.planner import AdaptivePlanner
from shared.recognizer import IntentionRecognizer
from shared.target_resolution import movement_target_id, movement_target_position
from shared.trajectory_algorithms import straight_line_path, stationary_segment, arrival_point
from shared.realization import realize


class Projector:
    """
    Builds ProjectedPlans. Owns its own AdaptivePlanner — projection always
    decomposes from scratch against the live WorldState, never resumes a
    partially-executed plan (see design_decisions.md, "Plans are re-decomposed
    from scratch; the world state is the execution cursor").
    """

    def __init__(
        self,
        task_model: TaskModel,
        assumed_speed: float = 1.0,
        default_action_cost: float = 1.0,
        arrival_radius: float = 0.0,
        action_completion_latency: float = 0.0,
        task_completion_latency: float = 0.0,
        observed_task_completion_latency: float = 0.0,
        observation_offset: float = 0.0,
        duration_to_steps: Optional[Callable[[str], float]] = None,
    ):
        """
        task_model:           the robot's task model (T-H), passed through to planner.py
                              calls and used for per-action cost lookup.
        assumed_speed:        world units the agent moves per execution step, so a
                              movement action lasts distance / assumed_speed steps.
                              Supplied by the embodiment layer (Mesa: its step_size,
                              see mesa_sim/sim_agents.py; ROS would supply its own).
                              The 1.0 default is a unit-less placeholder, not a value
                              shared/ knows to be right.
        default_action_cost:  duration, in execution steps, of a non-movement action
                              when task_model.get_cost(action_name) has no costs.yaml
                              entry. Mesa executes one microaction per tick, so 1.0 is
                              exact for pick_up/place there. An action whose schema
                              names a duration binding (wait_at) is priced through
                              duration_to_steps instead (TODO-32).
        arrival_radius:       world units short of a movement target at which the
                              body's executor STOPS — the distance at which its
                              at(agent, object) predicate holds, so the walk is
                              complete. A projected walk ends there, not at the
                              target point, and the next action is projected from
                              there (T9; design_decisions.md, "Projected walks end
                              where the executor stops"). Supplied by the embodiment
                              exactly as assumed_speed is (Mesa: the same
                              PROXIMITY_THRESHOLD its world-state builder emits `at`
                              with; ROS its own). The 0.0 default is a unit-less
                              placeholder (walk to the point), not a value shared/
                              knows to be right.
        action_completion_latency:
                              execution steps the body spends LEARNING that an action
                              finished, after its last microaction and before the next
                              action starts. Charged once per action, as a stationary
                              stretch at the position the action ended at — the agent is
                              standing still, not moving. Supplied by the embodiment as the
                              other three are (Mesa: one tick, the step its executor
                              spends seeing the completion predicate and advancing its
                              cursor without executing anything —
                              mesa_sim/executor.ACTION_COMPLETION_LATENCY; ROS its
                              own). The 0.0 default is a unit-less placeholder (an
                              instantaneous body), not a value shared/ knows to be
                              right. See design_decisions.md, "Projection time
                              includes what the body spends finishing an action" (L2).
        task_completion_latency:
                              execution steps the body spends COMPLETING a task, after
                              its last action's acknowledgement and before the next
                              task's first microaction. Charged once per projected
                              task, as a stationary segment at the position the task
                              ended at (project(), after build_segments()). Supplied by the
                              embodiment as action_completion_latency is (Mesa: one
                              tick, the step its executor spends in
                              _on_task_complete() — mesa_sim/executor.TASK_COMPLETION_LATENCY;
                              ROS its own). The 0.0 default is a unit-less placeholder,
                              not a value shared/ knows to be right. Applies to this
                              agent's own projections (the robot's candidates). See
                              design_decisions.md, "Robot-responsible separation" (the
                              completion tick).
        observed_task_completion_latency:
                              the same, for the OBSERVED agent's body: charged per task
                              of the human's projection (project_human()). Each body
                              states its own (T-C2b): the human's executor is
                              action-level, tracks no task and spends no per-task tick,
                              so Mesa's human reports 0 (mesa_sim/sim_agents.py). Its
                              per-action acknowledgement is the same executor's, and
                              action_completion_latency applies to both.
        observation_offset:   execution steps between this agent's own "now" — the
                              start of a projection, step 0 — and the time the
                              OBSERVED agent's state was true. project_human() starts
                              the human's projection there instead of at 0, so both
                              projections lie on one clock. Supplied by the
                              embodiment (Mesa: one tick, because the observed human
                              moves before the robot observes it within a tick, so its
                              observed position is the position it will hold at step 1
                              of the robot's projection, not at step 0 —
                              mesa_sim/sim_agents.OBSERVATION_OFFSET; ROS would derive
                              it from its own timestamps). The 0.0 default means
                              "observed at this agent's now". Consequence, deliberately
                              not papered over: the human's projection says nothing
                              about [0, observation_offset), because nothing was
                              observed of the human at this agent's now — the interval
                              is simply outside its span, and interference geometry
                              intersects windows.
        duration_to_steps:    converts the duration bound on a grounded action (the
                              value under ActionSchema.duration_key, an ISO-8601
                              string in the kitting domain) into execution steps.
                              Both halves — the string's parser and the seconds one
                              step lasts — are body facts, so the embodiment hands
                              the callable in as it hands in assumed_speed and the
                              latencies (Mesa: action_decomposer._parse_duration_to_steps
                              over mesa_configs.yaml's seconds_per_step — the same
                              function its executor's STAND* expansion uses, so the
                              projected wait and the executed wait are one number by
                              construction; ROS its own). shared/ calls it and holds
                              neither the parser nor the constant. None (the default)
                              means the body supplied no conversion: such an action
                              falls back to the cost lookup / default_action_cost, the
                              pre-TODO-32 behaviour — a placeholder, not a value
                              shared/ knows to be right. The robot's known duration
                              is the schema's; the human's actual duration comes from
                              the same schema through the same executor, so the two
                              match for now (design_decisions.md, "The human's wait
                              duration in the projection").
        """
        self._task_model = task_model
        self._planner = AdaptivePlanner(knowledge=task_model)
        self._assumed_speed = assumed_speed
        self._default_action_cost = default_action_cost
        self._arrival_radius = arrival_radius
        self._action_completion_latency = action_completion_latency
        self._task_completion_latency = task_completion_latency
        self._observed_task_completion_latency = observed_task_completion_latency
        self._observation_offset = observation_offset
        self._duration_to_steps = duration_to_steps

    # =========================================================================
    # Public
    # =========================================================================

    @property
    def assumed_speed(self) -> float:
        """The body-supplied motion per execution step (read by the embodiment
        for its run header)."""
        return self._assumed_speed

    def project(
        self,
        ordering: List[TaskInstance],
        world: WorldState,
        agent_id: str,
        belief: BeliefState,
        start_step: float = 0.0,
        task_completion_latency: Optional[float] = None,
    ) -> ProjectedPlan:
        """
        Builds a ProjectedPlan for `ordering`: one entry per task, in the
        ordering's order. `task_completion_latency` is the projected agent's
        body's per-task tick; omitted, this agent's own (project_human() passes
        the observed agent's).

        The first entry is decomposed via planner.plan() against the WorldState
        the caller passes — the live one — so a partially-executed task is
        projected from where the agent actually is, not from scratch. `belief`
        is forwarded to planner.plan() as-is (required, no default on that
        signature); callers always have a real belief available, unlike the
        human script path in sim_agents.py which fabricates a dummy one because
        it has no IR at all.

        Entry k+1 (len(ordering) > 1 — MetaPlanner's "full_reorder", T-B2a)
        follows from entry k: it starts at the step and the position entry k's
        last segment ends at, and is decomposed against the SUCCESSOR STATE of
        entry k (successor_state()) — the world as entry k's actions declare
        they leave it. That is what a later entry reads: the start position
        (build_segments(): world.agent_positions), the predicates guards match,
        and where objects are (target_resolution). Without it a fact the
        earlier task ended stays true for the later one (after a delivery the
        agent would still hold the delivered object, and the next task would be
        decomposed as if it had to put it back). design_decisions.md, "B3.B
        (`full_reorder`) is lookahead for the choice of the next task, built
        next", (a)-(c).

        The successor state is HYPOTHETICAL: a new WorldState value, built
        here between two entries and dropped when this call returns. The
        WorldState passed in is only read, never written, and no successor
        state is stored on the Projector or returned — a ProjectedPlan holds
        plans and segments, no WorldState. An ordering of one task builds none,
        and is projected exactly as it was before orderings were.

        Agent-agnostic: the same call projects a robot candidate or the human's
        predicted task (see project_human()).
        """
        if task_completion_latency is None:
            task_completion_latency = self._task_completion_latency
        task_queue: List[str] = []
        entries: List[ProjectedPlanEntry] = []
        entry_start = start_step

        for index, task in enumerate(ordering):
            abstract_plan = self._planner.plan(
                task=task,
                agent_id=agent_id,
                belief=belief,
                world=world,
            )

            segments = self.build_segments(abstract_plan, world, agent_id, entry_start)
            # What the body spends completing the task (F1): a stationary segment at
            # the position the task ended at, once per task — a task-level cost, not per action,
            # so it is placed here and not in build_segments(). Omitted at 0.0.
            if segments and task_completion_latency > 0.0:
                segments.append(stationary_segment(
                    segments[-1].end_pos, segments[-1].end_step, task_completion_latency
                ))
            entry_end = segments[-1].end_step if segments else entry_start
            duration = int(round(entry_end - entry_start))

            task_queue.append(task_instance_key(task))
            entries.append(ProjectedPlanEntry(
                abstract_plan=abstract_plan,
                estimated_start_step=int(entry_start),
                estimated_duration=duration,
                segments=segments,
            ))

            # The next entry follows from this one. `world` is rebound to a new
            # value; the caller's WorldState is not touched.
            if index + 1 < len(ordering):
                end_pos = segments[-1].end_pos if segments else world.agent_positions.get(agent_id)
                world = successor_state(world, abstract_plan.actions, agent_id, end_pos)
            entry_start = entry_end

        return ProjectedPlan(
            task_queue=task_queue,
            entries=entries,
            total_estimated_cost=int(round(entry_start - start_step)),
        )

    def project_human(
        self,
        belief: BeliefState,
        world: WorldState,
        human_agent_id: Optional[str],
        recognizer: IntentionRecognizer,
    ) -> Optional[ProjectedPlan]:
        """
        Builds the human's predicted plan from the current belief.

        Resolves belief.most_likely back to its HypothesisKey via
        recognizer.get_hypothesis(), rebuilds it as a TaskInstance, and projects it
        exactly as a robot candidate would be — project() is agent-agnostic, so
        there is no separate human projection path.

        Called once per fired cognitive-clock trigger — not per tick, and not per
        candidate. The human's predicted plan is a fact about the world at
        this event, independent of which robot task is being evaluated.

        Returns None in two distinct cases, both normal rather than errors:
          - no human is observed (human_agent_id is None)
          - get_hypothesis() cannot resolve belief.most_likely (e.g. "unknown")
        A hypothesis holds a schema of the task model (T-H1), so its task is
        always one this projector's planner decomposes.
        A None projection means the caller runs no interference check that call —
        a routine mid-run state, since the belief re-initialises at every human
        task boundary (I4c). MetaPlanner.update_human_projection() also refuses
        `unknown` before calling this (T8).
        """
        if human_agent_id is None:
            return None

        hypothesis = recognizer.get_hypothesis(belief.most_likely)
        if hypothesis is None:
            return None

        human_task = hypothesis.task_instance()
        # Starts at observation_offset, not 0: the projection begins where the
        # observed agent's state was TRUE, which need not be the projecting
        # agent's own now (L2). Its duration is unchanged — project() measures
        # from start_step — but its segments, and so its end, sit on the
        # projecting agent's clock.
        return self.project(
            [human_task], world, human_agent_id, belief,
            start_step=self._observation_offset,
            task_completion_latency=self._observed_task_completion_latency,
        )

    def project_fallback(
        self,
        world: WorldState,
        human_agent_id: str,
    ) -> Optional["FallbackProjection"]:
        """
        The fallback projection (T-D P): what the world model holds of the
        observed human — its position, true at the observation offset (L2), as
        project_human() starts there; its last one-tick displacement, absent
        before a second observation — with the room it moves in: the workspace,
        the fixed objects, and this projector's arrival radius (T9, the radius
        a projected walk stops at). Its end is each candidate's own
        (FallbackProjection.for_candidate()), so nothing here sets a horizon.

        Returns None when the world holds no position for `human_agent_id`:
        no human observed, nothing to build it from.
        """
        position = world.agent_positions.get(human_agent_id)
        if position is None:
            return None
        return FallbackProjection(
            position=position,
            displacement=world.agent_displacements.get(human_agent_id),
            start_step=self._observation_offset,
            workspace=world.workspace,
            fixed_objects=tuple(world.fixed_object_positions.values()),
            arrival_radius=self._arrival_radius,
        )

    def build_segments(
        self,
        plan: AbstractPlan,
        world: WorldState,
        agent_id: str,
        start_step: float = 0.0,
    ) -> List[Segment]:
        """
        Per-action Segments for `plan` — a straight-line motion or a stationary
        stretch each — starting from the
        agent's live position at `start_step`. Single geometry pass, chained
        head-to-tail in both position and step-time.

        Movement actions (schema.movement_target_key is not None): the target
        position comes from shared/target_resolution.py — the same lookup the
        recognizer scores chords against — and the path from
        trajectory_algorithms.straight_line_path(), the current default path
        realization, ending at trajectory_algorithms.arrival_point(): the
        body's arrival_radius short of the target, where its executor stops
        (T9). The stationary action that follows, and the next walk, are
        projected from that point. What is still not modelled: the residual
        of at most one execution step between the exact radius and the
        discrete step the executor stops on, and the tick an executor spends
        acknowledging a completed action. Only movement_target_type == "object" is handled; "zone"
        targets were removed from the live domain (see domains/kitting/actions.py),
        and this raises explicitly rather than silently mis-estimating if one
        reappears. Obstacle-aware, non-linear realization is DESIGN-13 / TODO-09
        (Phase 4D) — see trajectory_algorithms.obstacle_aware_path(). Holds
        against the human (Phase 4C realization) are placed AFTER this pass, on
        the segments it returns; this builds the unheld segments only.

        Every action, movement or not, is then followed by a stationary
        segment of `action_completion_latency` steps at the position it ended
        at: the body does not learn an action is finished the instant it is
        (L2). Omitted entirely when the latency is 0, so a Projector built
        without one produces exactly the segments it did before. One
        consequence for consumers: there are then TWO segments per action, not
        one — read the count off the segments, never off the plan's actions.

        Non-movement actions: trajectory_algorithms.stationary_segment(), held for
        the action's stated duration when its schema names a duration binding
        (schema.duration_key, wait_at's ?duration) and the body supplied
        duration_to_steps — the grounded action's bound value, converted by the
        body (TODO-32); otherwise for task_model.get_cost(action_name) steps,
        falling back to default_action_cost.
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
                target_pos = movement_target_position(action, world)
                if target_pos is None:
                    raise ValueError(
                        f"Projector.build_segments: no position for target "
                        f"'{movement_target_id(action)}' of action "
                        f"'{action.action_name}'"
                    )
                stop_pos = arrival_point(current_pos, target_pos, self._arrival_radius)
                segment = straight_line_path(current_pos, current_step, stop_pos, self._assumed_speed)
                current_pos = stop_pos
            else:
                duration = self._stated_duration(action)
                if duration is None:
                    cost = self._task_model.get_cost(action.action_name)
                    duration = cost if cost is not None else self._default_action_cost
                segment = stationary_segment(current_pos, current_step, duration)

            segments.append(segment)
            current_step = segment.end_step

            # What the body spends learning the action finished: a stationary
            # stretch at the position it ended at, checked like any other segment.
            if self._action_completion_latency > 0.0:
                latency_segment = stationary_segment(
                    current_pos, current_step, self._action_completion_latency
                )
                segments.append(latency_segment)
                current_step = latency_segment.end_step

        return segments

    def _stated_duration(self, action) -> Optional[float]:
        """
        The duration the domain states for `action`, in execution steps, or None
        when there is none to read: the schema names no duration binding, the
        grounded action does not carry it, or the body supplied no
        duration_to_steps (TODO-32). The key is the schema's, never a literal.
        """
        key = action.schema.duration_key
        if key is None or self._duration_to_steps is None:
            return None
        value = action.bindings.get(key)
        if value is None:
            return None
        return float(self._duration_to_steps(value))

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


# =============================================================================
# The human projection a candidate is realized against (T-D P)
# =============================================================================

class HumanProjection(ABC):
    """
    What admission (MetaPlanner.update_human_projection()) hands update(): the
    human's plan a candidate is realized against, one per fired trigger, and
    whether a candidate so realized is realizable under it. Two kinds (T-D P,
    design_decisions.md, "T-D P: the fallback projection"):
      AdmittedProjection   the admitted hypothesis's projection, the same
                           ProjectedPlan for every candidate; F1's semantics:
                           every candidate realizes, its hold priced as cost.
      FallbackProjection   admission refused with a human observed: the human
                           where it was observed and as it moved last (P2),
                           over each candidate's own span; a candidate whose
                           violation is cleared only by the projection's end
                           is not realizable (P1).
    realize() is not told which it is given: it reads the ProjectedPlan.
    """

    @abstractmethod
    def for_candidate(self, candidate: ProjectedPlan) -> ProjectedPlan:
        """The human's ProjectedPlan to realize `candidate` against."""

    @abstractmethod
    def realizable(self, candidate: ProjectedPlan, realized: RealizedPlan, min_separation: float) -> bool:
        """Whether `realized` — `candidate` realized against
        for_candidate(candidate) at `min_separation` — is realizable under this
        projection."""


@dataclass(frozen=True)
class AdmittedProjection(HumanProjection):
    """The admitted hypothesis's projection (Projector.project_human())."""
    plan: ProjectedPlan

    def for_candidate(self, candidate: ProjectedPlan) -> ProjectedPlan:
        return self.plan

    def realizable(self, candidate: ProjectedPlan, realized: RealizedPlan, min_separation: float) -> bool:
        # F1: realization is total; a hold is priced as cost, never refused.
        return True


@dataclass(frozen=True)
class FallbackProjection(HumanProjection):
    """
    The fallback projection (T-D P): a short-term physical projection of the
    observed human, from what was observed, claiming nothing about intention.
    Built by Projector.project_fallback(). One mechanism, two cases, read from
    `displacement`, the human's last observed one-tick displacement (P2 (1)):
      STANDING (a zero displacement; or none observed yet, the initialisation
        convention): stationary at `position`;
      MOVING: a straight continuation from `position` along the displacement
        at its length per tick, until the ray meets the workspace boundary or
        enters the arrival radius of the first fixed object along it (an
        object whose radius contains the ray's start is skipped), then
        stationary there (P2 (2)).
    Over [start_step, the candidate's end] — start_step the observation offset
    (L2), the end the candidate's last segment's end, its own T_r on the
    decision's projection clock (under full_reorder the candidate is the
    ordering; P2 (3)). One entry, which has no task (abstract_plan None).
    Known errors, recorded and not fixed: a human passing an object on the way
    elsewhere is projected to stop there; an acknowledgement tick reads as
    standing for a decision on that tick.

    REALIZABLE (P1, rule 5) iff the candidate's violation is cleared by the
    projected motion within the horizon, not only by the projection's end (a
    stationary segment ending, or the moving segment cut by the horizon). Exact
    form: the shifts realize() found are checked by a second realize() against
    this projection rebuilt over the realized plan's own span (the candidate's
    end plus the last entry's cumulative shift); differing shifts refuse it.
    The rebuilt projection only extends the first one, so its violating
    intervals contain the first's and its shifts are never smaller: equal
    shifts mean the realized plan is clear of the human over its whole span. A
    consistency check; nothing iterates.
    """
    position: Tuple[float, float]
    displacement: Optional[Tuple[float, float]]
    start_step: float
    workspace: Optional[Workspace]
    fixed_objects: Tuple[Tuple[float, float], ...]
    arrival_radius: float

    def for_candidate(self, candidate: ProjectedPlan) -> ProjectedPlan:
        return self._over(_end_of(candidate))

    def realizable(self, candidate: ProjectedPlan, realized: RealizedPlan, min_separation: float) -> bool:
        realized_end = _end_of(candidate) + realized.cumulative_shifts[-1]
        again = realize(candidate, self._over(realized_end), min_separation, decision_step=realized.hold_start)
        return again.cumulative_shifts == realized.cumulative_shifts

    def _over(self, end: float) -> ProjectedPlan:
        """The projection over [start_step, end]: the continued walk, cut at
        `end` if it has not stopped by then, then the stand to `end`."""
        if end < self.start_step:
            raise ValueError(
                f"FallbackProjection: the span ends at step {end}, before the observation offset {self.start_step}"
            )
        segments: List[Segment] = []
        position, step = self.position, self.start_step
        if self.displacement is not None and self.displacement != (0.0, 0.0):
            length = math.hypot(*self.displacement)
            direction = (self.displacement[0] / length, self.displacement[1] / length)
            step = min(self.start_step + self._reach(direction) / length, end)
            travelled = (step - self.start_step) * length
            stop = (position[0] + direction[0] * travelled, position[1] + direction[1] * travelled)
            if step > self.start_step:
                segments.append(Segment(start_pos=position, start_step=self.start_step, end_pos=stop, end_step=step))
            position = stop
        if end > step or not segments:
            segments.append(stationary_segment(position, step, end - step))
        duration = end - self.start_step
        return ProjectedPlan(
            task_queue=[],
            entries=[ProjectedPlanEntry(
                abstract_plan=None,
                estimated_start_step=int(self.start_step),
                estimated_duration=int(round(duration)),
                segments=segments,
            )],
            total_estimated_cost=int(round(duration)),
        )

    def _reach(self, direction: Tuple[float, float]) -> float:
        """Distance along the ray from `position` in `direction` (a unit
        vector) to where the continued walk stops: the nearer of the
        workspace boundary and the entry into the first fixed object's arrival
        radius (an object whose radius contains the start skipped)."""
        if self.workspace is None:
            raise ValueError("FallbackProjection: a moving human needs the workspace, and the world holds none")
        px, py = self.position
        dx, dy = direction
        ws = self.workspace
        reach = math.inf
        if dx > 0.0:
            reach = min(reach, (ws.x_max - px) / dx)
        elif dx < 0.0:
            reach = min(reach, (ws.x_min - px) / dx)
        if dy > 0.0:
            reach = min(reach, (ws.y_max - py) / dy)
        elif dy < 0.0:
            reach = min(reach, (ws.y_min - py) / dy)
        reach = max(0.0, reach)
        r = self.arrival_radius
        for cx, cy in self.fixed_objects:
            wx, wy = px - cx, py - cy
            c = wx * wx + wy * wy - r * r
            if c <= 0.0:
                continue   # the ray starts inside this object's arrival radius
            b = wx * dx + wy * dy
            disc = b * b - c
            if disc < 0.0 or b >= 0.0:
                continue   # the ray misses the disc, or points away from it
            reach = min(reach, -b - math.sqrt(disc))
        return reach


def _end_of(candidate: ProjectedPlan) -> float:
    """The candidate's end: its last segment's end step."""
    segments = [seg for entry in candidate.entries for seg in entry.segments]
    if not segments:
        raise ValueError("FallbackProjection: the candidate has no segments")
    return segments[-1].end_step


def successor_state(
    world: WorldState,
    actions: Sequence[GroundedAction],
    agent_id: str,
    end_pos: Optional[Tuple[float, float]],
) -> WorldState:
    """
    The WorldState `actions` declare they leave behind, as a NEW
    value: `world` is read and never written, and every container that
    differs is a copy. Hypothetical — nothing has been executed. Two readers:
    Projector.project(), between two entries of one call and no longer (T-B2a);
    and the load-time replay of the human's script (world/human_executor.py,
    check_script(), T-H2), each action advancing the symbolic state the
    script's tasks are expanded against. A module function so that both read
    one successor state, not two.

    Derived from the action schemas only, action by action in plan order,
    with each grounded action's own bindings — no predicate, parameter or
    task name appears here:
      - ActionSchema.retracts: the grounded fact is no longer true;
      - ActionSchema.effects:  the grounded fact is true (retract first,
        then add, so an action may replace a fact);
      - moved_object_key / moved_to_key: the moved object is where the
        action put it — object_locations names the agent or object it is
        now at, and object_positions follows, read at the END of the plan
        (an object an agent still holds is where the agent ends).
    The agent's own position is geometry, not a schema fact: `end_pos`, the
    end of the entry's last segment (None: left where it is).

    What it does NOT carry, because no schema declares it: anything the
    body's world-state builder derives and no action states (zones, a fact
    a later action of another kind ends), and the observed agent's own
    projected effects — the limitation a single task has too. The part of
    TODO-07 projection needs; the planner's forward chaining and
    precondition checking are not this.
    """
    predicates = set(world.predicates)
    object_locations = dict(world.object_locations)
    object_positions = dict(world.object_positions)
    agent_positions = dict(world.agent_positions)
    if end_pos is not None:
        agent_positions[agent_id] = end_pos

    moved: List[str] = []
    for action in actions:
        schema = action.schema
        for condition in schema.retracts:
            predicates.discard(condition.to_predicate(action.bindings))
        for condition in schema.effects:
            predicates.add(condition.to_predicate(action.bindings))
        if schema.moved_object_key is not None:
            obj_id = action.bindings[schema.moved_object_key]
            object_locations[obj_id] = action.bindings[schema.moved_to_key]
            moved.append(obj_id)

    for obj_id in moved:
        place_id = object_locations[obj_id]
        position = agent_positions.get(place_id, object_positions.get(place_id))
        if position is not None:
            object_positions[obj_id] = position

    return replace(
        world,
        agent_positions=agent_positions,
        object_locations=object_locations,
        object_positions=object_positions,
        predicates=predicates,
    )
