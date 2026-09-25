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

from dataclasses import replace
from typing import Callable, List, Optional, Sequence, Tuple

from shared.types import (
    BeliefState,
    WorldState,
    TaskInstance,
    AbstractPlan,
    GroundedAction,
    ProjectedPlan,
    ProjectedPlanEntry,
    Segment,
    task_instance_key,
)
from shared.knowledge import TaskModel
from shared.planner import AdaptivePlanner
from shared.recognizer import IntentionRecognizer
from shared.target_resolution import movement_target_id, movement_target_position
from shared.trajectory_algorithms import straight_line_path, stationary_segment, arrival_point


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
    and the human action script's resolution at load (domains/script.py,
    resolve_script(), T-C2b), each task expanded against the state the
    elements before it leave behind. A module function so that both read one
    successor state, not two.

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
