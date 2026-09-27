"""
shared/recognizer.py

PURPOSE:
    Bayesian intention recognizer.
    Maintains and updates P(τ | observations) over all known intentions T.

ALGORITHM:
    P(τ | obs_1..t) ∝ P(obs_t | τ) · ω_context(τ, context, world) · P(τ | obs_1..t-1)

    P(obs_t | τ) = P(obs_t | a_φ(τ)) — a task's likelihood IS the likelihood of
    the action it expects now (the phase model, I3). The phase is DERIVED every
    tick, never stored: the planner selects τ's method by guards against the
    current world for the observed agent (I2), its actions are scanned from the
    start, and the expected action is the first whose completion condition does
    not yet hold. A hypothesis remembers which action it expected last tick and
    where the agent was when it began expecting it (its ORIGIN); it never stores
    an index into an action list, because method selection genuinely flips
    under it (deliver_item(Y) becomes deliver_with_return while X is carried).

    Likelihood of the expected action a — the evidence model (I4), every
    constant of which lives in shared/likelihood_functions.py with its meaning:
        - completion channel: the observed microaction is in a's declared
          discrete vocabulary (pick_up → GRASP, place → RELEASE, ...) → the
          detector's hit rate if a's grounded completion predicate holds in
          the world, its false-alarm rate if not. It is judged on the action
          the hypothesis expected BEFORE the event (the world after a grasp
          already satisfies pick_up's completion, so the derived action has
          moved on). An event is a fact at a moment: it MULTIPLIES onto the
          hypothesis's evidence.
        - phase channel (T-D E10, 1.5 rulings, 27 September 2026): the
          phase's projected completion delay, in ticks,
              D = e/v + (s − s_exp)
          through the logistic, L(v·D) = 2 / (1 + exp(beta·v·D)), and 1 for
          v·D <= 0 (the clip). e is the path WASTED under the hypothesis: the
          distance the agent has walked since the hypothesis's origin (a
          per-agent odometer, read at the origin), plus the remaining cost to
          a's target, minus the direct cost from the origin — for an action
          with a progress_evaluator (move_to), 0 otherwise. The target is the
          object's current location (shared/target_resolution.py). s is the
          ticks the agent stood since the origin (a per-agent standing clock),
          s_exp the standing the Projector prices within the phase (E9: the
          latency after the completion that opened the phase, plus the
          action's own stationary duration). One phase is one observation
          however many ticks it spans: the value is recomputed from the
          origin and REPLACES the previous tick's, it is not multiplied on
          it. When the expected action changes (phase advance, or regress —
          derived, so both happen), the closing phase's final value is folded
          into the evidence once and the origin (position, odometer and
          standing-clock readings) moves to the agent's. For a walk with no
          standing beyond its s_exp, v·D = e and the value is the excess-path
          likelihood; standing beyond s_exp is charged v per tick, as excess
          path is; a stationary tick within the priced standing is not a
          charge (I4c narrowed), nor is a phase with nothing walked and no
          standing (D <= 0: the value 1, the belief carries forward).
        - a hypothesis the planner cannot decompose here has no phase: the
          perfect-fit value, nothing to charge.
    There is no reference hypothesis (T-D R1, 27 September 2026): each live
    hypothesis pays its own likelihood per phase — its closed phases and
    events in its base, the open phase's value multiplied on top for this
    tick — and the evidence is normalised over the live hypothesis set H
    only. The invariant (R6): on every tick the normalised evidence sums to 1
    over exactly H, and a retired or inadmissible hypothesis is never in H.
    The belief is therefore RELATIVE: a lone live hypothesis reads 1.0 on no
    evidence, two rivals start at 0.5; there is no ceiling below 1. Whether
    the best of the models is wrong is the adequacy finding's question
    (below), not the belief's. Two hypotheses whose expected actions share
    evaluator, origin, walked distance and target position share one excess,
    computed once per tick.

    Completed tasks: judged on the TERMINAL action's completion condition
    directly (obj_at(item, table), waited(agent, machine)), whatever the phase
    walk did and whoever did it — the task is done and nobody can do it again.
    A completed hypothesis is skipped in the update (it accumulates no more
    evidence) AND pinned at BELIEF_FLOOR on output, for the rest of the run.

    Episodes (I4b, I4c): the recognizer estimates the intention of the
    observed agent's CURRENT BEHAVIOURAL EPISODE — deliver_item(item_3) means
    "this is the task being executed now", not a disposition or a belief
    about later tasks; there is no representation here in which "the agent
    seems uninterested in shelf_9" could live. Within a task, a phase advance
    ends a PHASE: the closing phase's value folds into the evidence and is
    retained, so a task grows more likely as more of its actions verifiably
    complete (prefix accumulation). A task boundary ends the EPISODE: when a
    completion retires a hypothesis whose expected action on the previous tick
    WAS its terminal action — the observed agent's own derived phase had
    reached the completing action — the observed agent has finished a task,
    and the belief re-initialises to the prior over the hypotheses still live,
    uniformly, with no dependence on any hypothesis's fold history; every
    origin moves to the agent's current position; completed tasks stay
    pinned. Nothing crosses the boundary, and no persistence layer carries
    anything across it: cross-episode information is outside the
    task-hypothesis model by decision, and would need its own representation.
    The pin and the boundary answer different questions and deliberately do
    not share a criterion: the pin asks whether the task is complete in the
    world (whoever did it — the normalisation set shrinks, the belief does
    not re-initialise); the boundary asks whether the observed agent changed
    episode, and another agent completing a task is not such a moment. The
    attribution is the recognizer's own phase state — no authorship in the
    world state, no microaction vocabulary — and it assumes that an agent
    whose derived phase reached the terminal action is the one who completed
    it.

    Output belief = evidence × ω_context, with inadmissible and completed
    hypotheses pinned at BELIEF_FLOOR and the floor applied. ω_context is a fact
    about the current state, not an event: applied to the output only, never
    fed back. The distribution is over TASKS; the phase is internal. The R6
    invariant holds at two levels: the normalised evidence sums to 1 over
    exactly H (before the floor); the returned distribution sums to 1 with the
    pinned keys at exactly BELIEF_FLOOR and the live keys carrying the rest.
    When no hypothesis is live (lifecycle EXHAUSTED) the belief over H has no
    members: the distribution holds the pins alone (the output convention, not
    belief mass), most_likely is None and confidence 0.0.

    Adequacy (T-D E1 to E9, G1): the recognizer's second output, independent
    of the belief, over the same statistic. Per live hypothesis, per DERIVED
    PHASE (from its origin to its phase advance — the unit, no window), the
    projected completion delay D = e/v + (s − s_exp) above, in ticks: e the
    excess path (0 for a phase with no evaluator or no resolvable target), v
    the body's speed, s the ticks without movement since the origin, s_exp
    the Projector's priced stationary ticks within the phase's span (E9),
    read from the Projector's own sequence and source — per action its own
    segment (0 for a walk; the bound duration for an action whose schema
    names one, through the body's duration_to_steps; otherwise the task
    model's cost for the action, else the body's default_action_cost), then
    the body's action latency, which falls in the phase the completion
    opens (and at an episode boundary with it the observed agent's task
    latency). In kitting: 2 for pick_up and place, 1 for a walk entered from
    a completion (the first walk after a boundary included), 0 for the
    initial walk. D is non-decreasing within a phase. Its tail probability
    S = likelihood_functions.tail_probability(v·D, beta). A live hypothesis is
    a MEMBER of the test on a tick iff it has a derived phase this tick (an
    expected action) and that phase holds an observation: walked path since
    its origin, or standing beyond s_exp, or, in a stationary phase (pick_up,
    place, wait_at), a stationary tick within the priced duration (D <= 0,
    S = 1; E6 amended 27 Sept 2026), or its expected action completed on
    this tick (a member with S = 1 whatever phase it advances into, E8; not
    on a boundary tick). A walk with nothing walked and no standing beyond
    s_exp is not one. The finding: unresolved iff there is no member;
    unexplained iff every member has S < alpha (intersection-union); adequate
    otherwise. A non-member contributes no S. Beside it, every live
    hypothesis's hypothesis adequacy (G1): adequate (a member with
    S >= alpha), inadequate (a member with S < alpha), no observation (not a
    member); the finding is adequate exactly when some hypothesis's is.
    Computed from scratch every tick, with no memory beyond each
    hypothesis's current phase: an unexplained finding clears when a member
    reaches S ≥ alpha or a phase advance or episode boundary empties the
    membership. alpha, the test level, is a run option the embodiment passes
    in. The recognizer decides nothing about action with the finding (R5);
    the meta-planner reads the leader's hypothesis adequacy at its gate.

    Context weight ω_context(τ, context, world):
        - TEMPERATURE_BOOST if room_temperature is high and τ is ac_activation
        - FATIGUE_BOOST if shift is long and τ is coffee_break
        - 1.0 otherwise

    Prior:
        - Uniform over the live hypotheses at t=0 and at every episode
          boundary (the admissible prior, over the current support)
        - The recognizer's own evidence state at t>0 (prev_belief is not
          consulted — see update())

    Admissibility restriction (optional, off by default):
        When the robot knows which tasks the observed agent is assigned — its
        assigned tasks, not a plan — that knowledge restricts the SUPPORT of the
        belief; it is not a magnitude. The admissible set is the hypotheses of
        the assigned WorkTask instances, plus every hypothesis of a PersonalTask
        in the task model (a foreseeable task: never assigned, and must stay
        recognizable); compared as HypothesisKey values (T-H). Admissible
        hypotheses take the ordinary update above, normalized over admissible
        mass only; inadmissible ones are refuted — pinned at BELIEF_FLOOR, never
        accumulating evidence. No weight, no boost: confidence is then a function
        of the admissible set size and of the evidence, with no tunable magnitude
        in it. With no assignment known, this whole mechanism is inert.

    Normalization: the evidence sums to 1.0 over H after each update.

HYPOTHESIS SPACE:
    One hypothesis per (task_name, param_bindings) pair derived from the robot's
    task model and the objects present in the workspace. No residual
    hypothesis (T-D R1).
    Hypotheses include both WorkTasks and the PersonalTasks the model holds.

INPUTS:
    - Observation:      detected_microaction, spatial_context.position
    - WorldState:       predicates (completion conditions), object_locations,
                        object_positions, agent_positions (target resolution)
    - ContextKnowledge: shift_start_step, room_temperature
    - prev_belief:      previous BeliefState (None → initial prior)
    - assigned_tasks:   observed agent's assigned tasks (None/empty → restriction is off)

OUTPUTS:
    - BeliefState: distribution, most_likely, confidence (the belief over H);
      finding, lifecycle, tails, hypothesis_adequacy (the adequacy finding,
      the lifecycle state, the members' tail probabilities, every live
      hypothesis's hypothesis adequacy)
"""

import itertools
import logging
from typing import Callable, Dict, List, Optional, Set, Tuple

from shared.types import (
    Observation, BeliefState, WorldState, GroundedAction,
    TaskInstance, TaskSchema, Var, Const, task_instance_key, PersonalTask, same_task,
    AdequacyFinding, RecognizerLifecycle, HypothesisAdequacy,
)
from shared.knowledge import TaskModel, ContextKnowledge
from shared.planner import AdaptivePlanner, DecompositionError
from shared.target_resolution import movement_target_position
from shared import likelihood_functions



# =============================================================================
# Recognizer-level constants
# (the likelihood constants — the detection rates — live in
#  likelihood_functions.py, single source of truth, read through the module
#  at call time rather than redefined here; the detour tolerance beta, the
#  body's speed and duration conversion, the priced standing and the test
#  level alpha are the embodiment's, passed to the constructor)
# =============================================================================

# ω_context boost multipliers
TEMPERATURE_BOOST  = 3.0
FATIGUE_BOOST      = 2.5

HIGH_TEMP_THRESHOLD    = 26.0
LONG_SHIFT_THRESHOLD   = 500

# theta is NOT here. The confidence gate is the meta-planner's decision, not a
# likelihood parameter (recognizer_handback.md §2) — this module produces the
# belief and never judges it. A CONFIDENCE_THRESHOLD = 0.75 sat here until
# September 2026 with no reader in shared/ or mesa_sim/; editing it looked
# authoritative and did nothing. The single definition is
# shared/meta_planner.py's DEFAULT_THETA (design_decisions.md, "theta has one
# home: the meta-planner owns the gate").

# Floor applied after normalization — prevents belief collapse to exact zero,
# which otherwise cannot recover through multiplicative Bayesian update.
BELIEF_FLOOR = 1e-3


# =============================================================================
# HypothesisKey
# =============================================================================

class HypothesisKey:
    """
    Identifies one IR hypothesis: a task schema of the robot's task model with
    specific parameter bindings (the enumerated ones).
    e.g. deliver_item(?item=item_3), coffee_break()
    Holds the schema OBJECT (T-H1): equal keys have the same schema by identity
    and equal bindings. `task_name` is the schema's name, for the key's string.
    """
    def __init__(self, schema: TaskSchema, bindings: Dict[str, str]):
        self.schema = schema
        self.bindings = bindings

    @property
    def task_name(self) -> str:
        return self.schema.name

    def task_instance(self) -> TaskInstance:
        """The task this hypothesis names, as a TaskInstance of its schema (its
        determined parameters unbound: the planner resolves them)."""
        return TaskInstance(schema=self.schema,
                            bindings={Var(k): Const(v) for k, v in self.bindings.items()})

    def __repr__(self):
        if self.bindings:
            params = ",".join(f"{k}={v}" for k, v in sorted(self.bindings.items()))
            return f"{self.task_name}({params})"
        return f"{self.task_name}()"

    def __eq__(self, other):
        return (isinstance(other, HypothesisKey)
                and self.schema is other.schema
                and self.bindings == other.bindings)

    def __hash__(self):
        return hash((self.task_name, tuple(sorted(self.bindings.items()))))

# ============================================================================
#  Functions
# ============================================================================ 
def build_hypothesis_space(
    task_model: TaskModel,
    known_objects_by_type: Dict[str, List[str]],
) -> List[HypothesisKey]:
    """
    One HypothesisKey per task schema of the robot's task model and each
    combination of workspace objects for its enumerated parameters.
    """
    hypotheses = []
    for task_schema in task_model.task_schemas():
        param_types = task_schema.parameter_types
        if not param_types:
            hypotheses.append(HypothesisKey(schema=task_schema, bindings={}))
            continue
        # A parameter another parameter determines (the item's table) is not
        # free: enumerating it would split one intention into indistinguishable
        # hypotheses. The planner resolves it per hypothesis.
        var_names = [v for v in param_types if v not in task_schema.determined_parameters]
        candidate_lists = [known_objects_by_type.get(param_types[v], []) for v in var_names]
        for combo in itertools.product(*candidate_lists):
            hypotheses.append(HypothesisKey(
                schema=task_schema,
                bindings=dict(zip(var_names, combo)),
            ))
    return hypotheses

# =============================================================================
# IntentionRecognizer
# =============================================================================

class IntentionRecognizer:

    def __init__(
        self,
        task_model: TaskModel,
        context: ContextKnowledge,
        hypotheses: List[HypothesisKey],
        beta: float,
        speed: float,
        duration_to_steps: Callable[[str], float],
        default_action_cost: float,
        action_completion_latency: float,
        observed_task_completion_latency: float,
        alpha: float,
        assigned_tasks: Optional[List[TaskInstance]] = None,
        path_cost: Optional[likelihood_functions.PathCost] = None,
    ):
        """
        task_model:     the robot's task model (T-H): its HTN knowledge
        context:        background context facts for ω_context weighting
        hypotheses:     list of (task_name, bindings) pairs for this scenario.
                        Built from the domain schemas and the workspace objects
                        at construction time in sim_agents.py.
        beta:           the phase likelihood's detour tolerance, per unit
                        of the body's length (Mesa: 0.01 /cm). Supplied by the
                        embodiment, no default: it carries the body's units,
                        and shared/ holds none (T-A1; TODO-58). Also the scale
                        of the adequacy test's reference distribution (T-D E5).
        speed:          v, the body's motion per tick, in its length units: the
                        value the embodiment hands the Projector as
                        assumed_speed. Converts between the excess path and
                        ticks in the projected completion delay (T-D E2).
        duration_to_steps: the body's conversion of a duration binding (wait_at's
                        ?duration) to ticks, the callable the Projector
                        receives. Prices the standing of such a phase.
        default_action_cost: the standing, in ticks, the Projector prices for a
                        stationary action with no stated duration and no task-
                        model cost (pick_up, place): the same value the body
                        hands the Projector (one source; ruled 27 Sept 2026).
        action_completion_latency: the ticks the Projector prices after every
                        action, standing where it ended (the body's value, the
                        one it hands the Projector). Attributed to the phase the
                        completion opens (T-D E9): a phase entered from a
                        completion is priced this much standing beside its own.
        observed_task_completion_latency: the ticks the Projector prices after
                        the observed agent's last action of a task (the body's
                        value for the observed agent, the one it hands the
                        Projector; Mesa's human: 0). Attributed with the action
                        latency to the phases a boundary opens (T-D E9).
        alpha:          the adequacy test's level, per derived phase (T-D E5): a
                        run option, no default here, never chosen from a
                        scenario.
        assigned_tasks: the OBSERVED agent's assigned tasks — which tasks it was
                        assigned, not in which order it will do them. None or
                        empty means the robot has no such knowledge: the
                        admissibility restriction is off and update() runs its
                        original unrestricted path over every hypothesis.
        path_cost:      C(a, b), the cost of the walk between two positions the
                        excess-path likelihood is measured against. Straight-line
                        distance by default (Mesa agents walk through obstacles);
                        a domain with a better model injects it here.

        _initial_prior is the t=0 prior over all hypotheses: uniform
        when the restriction is off; uniform over the admissible set, with the
        inadmissible pinned, when it is on.
        Keyed by repr(hyp) strings — same key space as BeliefState.distribution,
        so `prior` has one consistent type throughout update(), whether it
        comes from prev_belief.distribution or this fallback.
        """
        self.task_model = task_model
        self.context = context
        self._path_cost = path_cost or likelihood_functions.straight_line_cost
        self._beta = beta
        self._speed = speed
        self._duration_to_steps = duration_to_steps
        self._default_action_cost = default_action_cost
        self._action_completion_latency = action_completion_latency
        self._observed_task_completion_latency = observed_task_completion_latency
        self._alpha = alpha
        # A schema naming an evaluator the registry does not have is a domain
        # modelling error, and must not look like uncertainty: without this
        # check every movement under it would silently score the perfect fit.
        for schema in task_model.get_all_actions():
            name = schema.progress_evaluator
            if name is not None and name not in likelihood_functions.EXCESS_MEASURES:
                raise ValueError(
                    f"action '{schema.name}' names progress_evaluator '{name}', which is not "
                    f"registered in likelihood_functions.EXCESS_MEASURES "
                    f"({sorted(likelihood_functions.EXCESS_MEASURES)})")
        # Sorted by key so that every order-dependent step downstream — the
        # insertion order of the evidence and output dicts, hence max()'s
        # tie-break for most_likely and the order of tied entries in the log —
        # is a function of the hypothesis space alone, not of the order the
        # caller enumerated it in (which once followed a set of task names,
        # hence the process's hash seed; TODO-42).
        self._hypotheses = sorted(hypotheses, key=repr)
        self._history: List[Observation] = []
        self._by_key: Dict[str, HypothesisKey] = {repr(h): h for h in self._hypotheses}  # this is used to look up HypothesisKey by string repr in update()

        # The same method selection the executor's plans come from. A
        # hypothesis is grounded through it every tick against the live world:
        # which method its guards admit for the observed agent, and what each
        # step then targets. Held privately for the same reason the projector
        # holds one — decomposition is stateless and world-driven.
        self._planner = AdaptivePlanner(knowledge=task_model)
        # Per-tick memo of the grounded action list per hypothesis key (None =
        # not decomposable this tick). Cleared at the top of update().
        self._tick_actions: Dict[str, Optional[List[GroundedAction]]] = {}
        # Keys already reported as undecomposable, so the log says it once per
        # episode rather than once per tick.
        self._undecomposable: Set[str] = set()

        # Per-hypothesis phase state (see update()). Nothing here is an index
        # into an action list, and nothing is shared across hypotheses.
        #   _expected[key]  the GroundedAction the hypothesis expected on the
        #                   previous tick (None = not decomposable then); a key
        #                   absent from the dict has not been observed yet
        #   _origin[key]    the agent's position when that action became the
        #                   expected one — where its excess path is measured from
        #   _origin_odo[key] the agent's odometer reading at that moment, so
        #                   that walked = odometer − _origin_odo[key]
        #   _origin_still[key] the agent's count of ticks without movement at
        #                   that moment, so that s = _still − _origin_still[key]
        #                   (the standing in the phase's delay D)
        #   _entry_latency[key] the standing the Projector prices after the
        #                   completion that opened the phase (T-D E9): the
        #                   action latency if the phase was entered from a
        #                   completion, plus the observed agent's task latency
        #                   at an episode boundary; 0 for the phase a hypothesis
        #                   is first observed in, and after a regress
        #   _base[key]      the hypothesis's closed evidence: every closed phase
        #                   (as L) and every event of the CURRENT EPISODE folded
        #                   in, in one common scale across keys (rescaled each
        #                   tick so that Σ base·open = 1 over H); the open
        #                   phase's value is recomputed from _origin each tick
        #                   and multiplied on top, never into it; re-initialised
        #                   to the prior at every episode boundary.
        #   _completed      keys whose terminal completion condition has held:
        #                   skipped and pinned for the rest of the run
        self._expected: Dict[str, Optional[GroundedAction]] = {}
        self._origin: Dict[str, Tuple[float, float]] = {}
        self._origin_odo: Dict[str, float] = {}
        self._origin_still: Dict[str, int] = {}
        self._entry_latency: Dict[str, float] = {}
        self._base: Dict[str, float] = {}
        self._completed: Set[str] = set()
        # Per observed agent: total path length walked since its first
        # observation (the sum of straight-line steps between consecutive
        # observed positions) and the position that total was last advanced to.
        self._odometer: Dict[str, float] = {}
        # Per observed agent: the count of observed ticks on which it did not
        # move (a zero step), since its first observation — the standing clock
        # the adequacy test reads, as the odometer is the walking one.
        self._still: Dict[str, int] = {}
        self._last_pos: Dict[str, Tuple[float, float]] = {}
        # Normalized evidence over the live hypothesis set H — the belief with no
        # context weights and no pins in it; _output() derives the report from it.
        # Its keys ARE H.
        self._evidence: Dict[str, float] = {}

        self._admissible: Optional[Set[HypothesisKey]] = self._build_admissible(assigned_tasks)

        if self._admissible is None:
            # Uniform prior over all hypotheses
            self._initial_prior: Dict[str, float] = self._prior([repr(h) for h in self._hypotheses])
        else:
            # Uniform over the admissible set only, then pinned — the same shape
            # as every distribution update() produces, so prior and posterior
            # agree. Built in hypothesis order, the order update()
            # produces, not in the admissible set's iteration order.
            self._initial_prior = self._pin(
                self._prior([repr(h) for h in self._hypotheses if h in self._admissible]),
                {repr(h) for h in self._hypotheses if h not in self._admissible},
            )
        # Keys pinned at BELIEF_FLOOR on every output because of the restriction.
        self._inadmissible: Set[str] = (
            set() if self._admissible is None
            else {repr(h) for h in self._hypotheses if h not in self._admissible}
        )
        self._evidence = {k: v for k, v in self._initial_prior.items() if k not in self._inadmissible}
        self._base = dict(self._evidence)

    @staticmethod
    def _prior(live: List[str]) -> Dict[str, float]:
        """
        The prior over the hypotheses in `live` (keys, in hypothesis order):
        uniform. The one prior the recognizer has — used at
        construction over the admissible set and at every episode boundary
        over the hypotheses still live. Nothing else is stored to re-start
        from.
        """
        return {k: 1.0 / len(live) for k in live}

    def _begin_episode(self, pos: Tuple[float, float], odo: float, still: int) -> None:
        """
        An episode boundary: the observed agent has completed a task, and the
        intention the recognizer estimates — the task of the CURRENT
        behavioural episode — is a new question. The ended episode's evidence
        (every fold, every event) is discarded uniformly: every live
        hypothesis's base becomes the prior over the hypotheses still live,
        whatever its phase history was, and every origin moves to the agent's
        position. Every phase is now entered from the observed agent's
        completion, so each is priced the standing the Projector attributes to
        it (the action latency and the observed agent's task latency, T-D E9).
        Every phase is empty, so the belief IS the prior until the agent moves,
        and no walk holds an observation for the adequacy test (the finding is
        unresolved, or the lifecycle exhausted). Completed hypotheses are not
        live and stay pinned.
        Nothing crosses the boundary: a task hypothesis says which task is
        being executed now, not what the agent is disposed to do next, and
        there is no representation here for the latter.
        """
        self._base = self._prior(list(self._base))
        self._evidence = dict(self._base)
        for key in self._origin:
            self._origin[key], self._origin_odo[key], self._origin_still[key] = pos, odo, still
            self._entry_latency[key] = self._action_completion_latency + self._observed_task_completion_latency

    def _build_admissible(
        self,
        assigned_tasks: Optional[List[TaskInstance]],
    ) -> Optional[Set[HypothesisKey]]:
        """
        The support restriction (T-H, item 3): the hypotheses the observed
        agent's intention may lie in,
            admissible = { hypotheses of the WorkTask instances in the assigned tasks }
                       ∪ { every hypothesis of a PersonalTask in the task model }
        compared as HypothesisKey values. Every assigned task is a WorkTask instance (checked
        at load, AgentConfig). Returns None when nothing is known, which switches
        the mechanism off entirely rather than admitting everything explicitly —
        equivalent in effect, but None keeps update() on its original,
        unrestricted path.

        A PersonalTask in the task model is a foreseeable task: never assigned,
        so it must stay recognizable when the human switches to it. This is the
        one place the recognizer reads a
        schema's class.

        An assigned task is matched to the hypothesis space by task equality
        (same_task, T-H4): the hypothesis that is the same task, on the goal
        bindings (its bindings minus the schema's determined and duration
        parameters; T-B1a follow-up 2). A hypothesis has no determined
        parameter, its table is resolved from the station when grounded.
        Whether a determined binding agrees with the station is the
        embodiment's load-time conformance check (check_task_destinations),
        not a matter for this match.
        """
        if not assigned_tasks:
            return None

        admissible: Set[HypothesisKey] = {
            hyp for hyp in self._hypotheses
            if isinstance(hyp.schema, PersonalTask)
        }

        for task in assigned_tasks:
            key = next((hyp for hyp in self._hypotheses if same_task(hyp.task_instance(), task)), None)
            if key is not None:
                admissible.add(key)
            else:
                logging.warning(
                    "[recognizer] assigned task %s matches no hypothesis — ignored",
                    task_instance_key(task)
                )
        return admissible

    def _pin(self, distribution: Dict[str, float], pinned: Set[str]) -> Dict[str, float]:
        """
        Pin every key in `pinned` at BELIEF_FLOOR and rescale the live mass to
        fill what is left, so the result spans the full hypothesis space and
        still sums to 1.0. `distribution` holds the live keys only, normalized.
        Used for inadmissible hypotheses (restriction) and for completed
        hypotheses (the terminal pin) alike.

        Pinned at the floor rather than at zero for the reason the floor exists
        at all: a hypothesis at exact zero can never recover through
        multiplicative update. Note the log cannot tell a pinned hypothesis from
        a live one refuted by evidence — both read BELIEF_FLOOR.
        """
        live_mass = 1.0 - len(pinned) * BELIEF_FLOOR
        out = {k: v * live_mass for k, v in distribution.items()}
        out.update({k: BELIEF_FLOOR for k in sorted(pinned)})   # sets have no stable order
        return out

    def update(
        self,
        obs: Observation,
        world: WorldState,
        prev_belief: Optional[BeliefState] = None,
    ) -> BeliefState:
        """
        Bayesian update: P(τ|obs_1..t) ∝ P(obs_t|τ) · ω_context(τ) · P(τ|obs_1..t-1),
        with P(obs_t|τ) the likelihood of the action τ expects now.

        Per live hypothesis, in this order:
          1. derive the expected action against the current world (planner's
             guard-selected method, walked from the start to the first action
             whose completion condition does not hold);
          2. if the TERMINAL action's completion holds, the task is complete:
             retire the hypothesis (skipped here, pinned in _output) for good;
          3. if the observed microaction is in the vocabulary of the action the
             hypothesis expected on the previous tick, that action's completion
             check multiplies onto its evidence (an event);
          4. if the expected action changed, fold the closing phase's final
             value L(v·D) into the evidence once (1, if its delay was not
             positive) and move the origin (position, odometer and
             standing-clock readings) to the agent's (a phase advance — or
             regress; both are derived facts). A phase entered from the
             completion of the previous expected action (its completion
             predicate holds now) is priced the action latency beside its own
             standing (T-D E9), and the completing hypothesis is a member of
             the adequacy test with S = 1 on this tick (E8);
          5. the open phase's value L(v·D), D its projected completion delay
             from the origin (T-D E10), multiplies on top of the evidence for
             this tick only (replaced next tick): 1 while D <= 0 (nothing
             walked and no standing beyond the priced standing — not a
             charge).
        Then normalize over the live hypothesis set H (T-D R1, R6). If a
        retirement this tick was the observed agent's own (step 2, terminal
        action expected on the previous tick), the episode ends: the belief
        re-initialises to the prior over H and every origin moves to the
        agent's position (_begin_episode); this tick reports the re-initialised
        belief. Last, the adequacy finding and the lifecycle state are read
        from the phase state as it stands (_adequacy).

        ω_context is applied to the output only (see _output()). The recognizer
        therefore owns its belief; `prev_belief` is accepted for contract
        compatibility and not consulted (its distribution already contains the
        output-only factors, so feeding it back would count them twice).
        """
        self._history.append(obs)
        self._tick_actions = {}
        memo: Dict[tuple, float] = {}          # likelihood computations this tick, by inputs
        pos = obs.spatial_context.position
        mu = (obs.detected_microaction or "").upper()
        # Advance the observed agent's odometer by the step just observed.
        # A zero step advances the standing clock instead.
        agent = obs.agent_id
        if agent in self._last_pos:
            step = likelihood_functions.straight_line_cost(self._last_pos[agent], pos)
            self._odometer[agent] += step
            if step <= 0.0:
                self._still[agent] += 1
        else:
            self._odometer[agent] = 0.0
            self._still[agent] = 0
        self._last_pos[agent] = pos
        odo = self._odometer[agent]
        still = self._still[agent]

        unnorm: Dict[str, float] = {}
        boundary = False
        # The hypotheses whose expected action completed on this tick (E8).
        advanced: Set[str] = set()
        for hyp in self._hypotheses:
            key = repr(hyp)
            if key in self._inadmissible or key in self._completed:
                continue
            actions = self._grounded_actions(hyp, obs.agent_id, world)
            if actions is not None and self._terminal_complete(actions, world):
                if self._task_boundary(self._expected.get(key), actions):
                    boundary = True
                self._completed.add(key)
                self._base.pop(key, None)
                self._expected.pop(key, None)
                self._origin.pop(key, None)
                self._origin_odo.pop(key, None)
                self._origin_still.pop(key, None)
                self._entry_latency.pop(key, None)
                logging.info("[IR-complete] step=%d %s completed: %s holds",
                             int(obs.timestamp), key, actions[-1].completion_predicate)
                continue
            current = self._expected_action(actions, world)

            if key not in self._expected:
                # First observation of this hypothesis: it enters its current
                # action here, from no completion (E9: nothing priced before
                # its own standing). Its phase is empty: D <= 0, no charge.
                self._expected[key], self._origin[key], self._origin_odo[key] = current, pos, odo
                self._origin_still[key] = still
                self._entry_latency[key] = 0.0
                unnorm[key] = self._base[key]
                continue

            previous = self._expected[key]
            if previous is not None and self._in_vocabulary(previous, mu):
                self._base[key] *= self._completion_likelihood(previous, world, memo)
            if not self._same_action(previous, current):
                # The closing phase was one observation: its final value
                # L(v·D) folds into the evidence once (1 if its delay was not
                # positive). The new phase begins here, empty.
                self._base[key] *= self._phase_likelihood(key, previous, pos, odo, still, world, memo)
                self._expected[key], self._origin[key], self._origin_odo[key] = current, pos, odo
                self._origin_still[key] = still
                # Entered from a completion — the previous expected action's
                # completion predicate holds now — the phase is priced the
                # action latency the Projector charges after that action (E9),
                # and the completing hypothesis is a member of the adequacy
                # test with S = 1 on this tick (E8). A regress, or a method
                # flip that completed nothing, prices none.
                completed = (previous is not None and previous.completion_predicate is not None
                             and previous.completion_predicate in world.predicates)
                self._entry_latency[key] = self._action_completion_latency if completed else 0.0
                if completed:
                    advanced.add(key)
            # The open phase's value (E10): 1 while its delay is not positive.
            unnorm[key] = self._base[key] * self._phase_likelihood(key, current, pos, odo, still, world, memo)

        # One normalization, at the task layer, over the live hypothesis set H
        # (T-D R1): the keys of unnorm are exactly H. The bases are rescaled by the same total so they stay in one scale
        # with each other (ratios are untouched) and so that
        # evidence == base × open value exactly.
        total = sum(unnorm.values()) or 1.0
        for key in self._base:
            self._base[key] /= total
        self._evidence = {k: v / total for k, v in unnorm.items()}

        if boundary:
            # The observed agent's task boundary ends the behavioural episode:
            # the next one's inference starts from the prior, here, and this
            # tick already reports it (the ended episode's closing values are
            # not a belief the model holds any more).
            self._begin_episode(pos, odo, still)
            # The boundary is unchanged by E8: the hypotheses entering the new
            # episode hold no observation on this tick.
            advanced = set()
            logging.info("[IR-boundary] step=%d %s completed a task: belief re-initialised to the "
                         "prior over %d hypotheses, origins reset",
                         int(obs.timestamp), agent, len(self._origin))

        distribution = self._output(obs, world)
        if self._evidence:
            # The argmax over H, in the distribution's order (the live keys
            # first, in hypothesis order: the tie-break as before).
            most_likely = max((k for k in distribution if k in self._evidence),
                              key=lambda k: distribution[k])
            confidence = distribution[most_likely]
        else:
            # Exhausted: the belief over H has no members; the pins are the
            # output convention, not belief mass (T-D R4).
            most_likely, confidence = None, 0.0
        finding, lifecycle, tails, hypothesis_adequacy = self._adequacy(pos, odo, still, world, advanced, memo)

        return BeliefState(
            timestamp=obs.timestamp,
            agent_id=obs.agent_id,
            distribution=distribution,
            most_likely=most_likely,
            confidence=confidence,
            finding=finding,
            lifecycle=lifecycle,
            tails=tails,
            hypothesis_adequacy=hypothesis_adequacy,
        )

    # -------------------------------------------------------------------------
    # Adequacy (T-D E1 to E7, E8, G1)
    # -------------------------------------------------------------------------

    def _adequacy(
        self,
        pos: Tuple[float, float],
        odo: float,
        still: int,
        world: WorldState,
        advanced: Set[str],
        memo: Dict[tuple, float],
    ) -> Tuple[Optional[AdequacyFinding], RecognizerLifecycle, Dict[str, float],
               Dict[str, HypothesisAdequacy]]:
        """
        The adequacy finding, the lifecycle state, the members' tail
        probabilities and every live hypothesis's hypothesis adequacy, read
        from scratch from the phase state after this tick's update (and
        boundary): no memory beyond each live hypothesis's current derived
        phase (E7).

        H empty: EXHAUSTED, no finding, no tails, no hypothesis adequacy (R4).
        Otherwise, per live hypothesis in hypothesis order: a MEMBER iff it has
        a derived phase this tick (an expected action) and that phase holds an
        observation (E6 as amended, the complete membership rule) — walked
        path since its origin, standing beyond the priced standing s_exp, or a
        stationary tick within s_exp in a stationary phase (then D <= 0 and
        S = 1) — or its expected action completed on this tick (`advanced`,
        E8: a member with S = 1, whatever phase it advanced into; empty on a
        boundary tick). A member's tail S = tail_probability(v·D, beta) (E2,
        E5). Unresolved iff there is no member; unexplained iff every member
        has S < alpha (E4); adequate otherwise. A non-member contributes no S.
        Hypothesis adequacy (G1): ADEQUATE for a member with S >= alpha,
        INADEQUATE for a member with S < alpha, NO_OBSERVATION for a
        non-member; the finding is adequate exactly when some live
        hypothesis's is ADEQUATE.
        """
        live = [repr(h) for h in self._hypotheses if repr(h) in self._evidence]
        if not live:
            return None, RecognizerLifecycle.EXHAUSTED, {}, {}
        tails: Dict[str, float] = {}
        for key in live:
            action = self._expected.get(key)
            if action is None:
                continue                    # no derived phase this tick
            if key in advanced:
                tails[key] = 1.0            # the completion is an observation consistent with it (E8)
                continue
            walked = odo - self._origin_odo[key]
            s = still - self._origin_still[key]
            s_exp = self._priced_standing(key, action)
            # A stationary phase (no movement target: pick_up, place, wait_at)
            # is derived only at its location; a stationary tick in it within
            # the priced duration is an observation with D <= 0 (E6, amended
            # 27 Sept 2026). Its entry tick counts: the arrival step belongs
            # to the closing walk's stretch.
            stationary_phase = action.schema.movement_target_key is None
            if not (walked > 0.0 or s > s_exp or (stationary_phase and s <= s_exp)):
                continue                    # the phase holds no observation
            tails[key] = likelihood_functions.tail_probability(
                self._delay_length(key, action, pos, odo, still, world, memo), self._beta)
        hypothesis_adequacy = {
            key: (HypothesisAdequacy.NO_OBSERVATION if key not in tails
                  else HypothesisAdequacy.INADEQUATE if tails[key] < self._alpha
                  else HypothesisAdequacy.ADEQUATE)
            for key in live
        }
        if not tails:
            finding = AdequacyFinding.UNRESOLVED
        elif all(v < self._alpha for v in tails.values()):
            finding = AdequacyFinding.UNEXPLAINED
        else:
            finding = AdequacyFinding.ADEQUATE
        return finding, RecognizerLifecycle.LIVE, tails, hypothesis_adequacy

    # -------------------------------------------------------------------------
    # The phase's projected completion delay D (T-D E2, E9, E10)
    # -------------------------------------------------------------------------

    def _phase_likelihood(
        self,
        key: str,
        action: Optional[GroundedAction],
        pos: Tuple[float, float],
        odo: float,
        still: int,
        world: WorldState,
        memo: Dict[tuple, float],
    ) -> float:
        """
        The belief's evidence for `key`'s phase of `action`, from its origin
        (T-D E10): L(v·D), 1 for v·D <= 0 (likelihood_functions.
        delay_likelihood). For a walk with no standing beyond its priced
        standing v·D is the excess and this is the excess-path likelihood;
        standing beyond it is charged as excess path is; standing within it
        is no charge (I4c narrowed). No expected action (not decomposable
        here): the perfect-fit value, nothing to charge.
        """
        if action is None:
            return likelihood_functions.PERFECT_FIT_LIKELIHOOD
        return likelihood_functions.delay_likelihood(
            self._delay_length(key, action, pos, odo, still, world, memo), self._beta)

    def _delay_length(
        self,
        key: str,
        action: GroundedAction,
        pos: Tuple[float, float],
        odo: float,
        still: int,
        world: WorldState,
        memo: Dict[tuple, float],
    ) -> float:
        """
        v·D, the projected completion delay of `key`'s phase of `action` in
        the body's length units (E2):
            v·D = e + v·(s − s_exp)
        e the excess path from the origin (_excess), s the ticks without
        movement since the origin, s_exp the priced standing of the phase
        (_priced_standing). The one statistic the belief (L, E10) and the
        adequacy test (S, E5) read. Non-decreasing within a phase for a
        static target.
        """
        walked = odo - self._origin_odo[key]
        s = still - self._origin_still[key]
        e = self._excess(action, self._origin[key], walked, pos, world, memo)
        return e + self._speed * (s - self._priced_standing(key, action))

    def _priced_standing(self, key: str, action: GroundedAction) -> float:
        """
        s_exp: the Projector's priced stationary ticks that fall within
        `key`'s current phase of `action` (T-D E9), from the Projector's own
        sequence — per action its own segment, then the action latency:
        the latency priced after the completion that opened the phase
        (_entry_latency: the action latency when entered from a completion,
        with the observed agent's task latency at a boundary; 0 for the
        phase first observed, and after a regress), plus the action's own
        stationary duration (_action_duration). In kitting: 2 for pick_up and
        place after their walk, 1 for a walk entered from a completion, 0
        for the initial walk.
        """
        return self._entry_latency[key] + self._action_duration(action)

    def _action_duration(self, action: GroundedAction) -> float:
        """
        The stationary ticks the Projector prices for `action`'s own segment,
        by its own rule and source: 0 for a walk (the schema names a movement
        target: priced by distance, not by standing); the bound duration,
        through the body's duration_to_steps, when the schema names a
        duration binding (wait_at); otherwise the task model's cost for the
        action, and failing that the body's default_action_cost (pick_up,
        place).
        """
        schema = action.schema
        if schema.movement_target_key is not None:
            return 0.0
        if schema.duration_key is not None:
            value = action.bindings.get(schema.duration_key)
            if value is not None:
                return float(self._duration_to_steps(value))
        cost = self.task_model.get_cost(action.action_name)
        return cost if cost is not None else self._default_action_cost

    def _excess(
        self,
        action: GroundedAction,
        origin: Tuple[float, float],
        walked: float,
        pos: Tuple[float, float],
        world: WorldState,
        memo: Dict[tuple, float],
    ) -> float:
        """
        e: the excess path from `origin` under `action`
        (likelihood_functions.EXCESS_MEASURES, under the name the schema's
        progress_evaluator gives): the distance `walked` since the origin plus
        the remaining cost to the action's target (its current position,
        shared/target_resolution.py, the lookup the projector uses) minus the
        direct cost from the origin, with the injected path cost. Measured
        FROM THE ORIGIN, not tick to tick: a τ-walker would have gone straight
        from where it began, and a passed target must not re-import
        accumulation one step at a time. 0 for a phase with no excess to
        charge: no evaluator (pick_up, place, wait_at), no resolvable target,
        or nothing walked since the origin (then the agent is at the origin).
        Memoised by (evaluator, origin, walked, target position): two
        hypotheses whose expected actions head for the same place from the
        same origin at the same odometer reading — two items on one shelf —
        share one value.
        """
        name = action.schema.progress_evaluator
        if name is None:
            return 0.0
        target_pos = movement_target_position(action, world)
        if target_pos is None or walked <= 0.0:
            return 0.0
        memo_key = ("excess", name, origin, walked, target_pos)
        if memo_key not in memo:
            memo[memo_key] = likelihood_functions.EXCESS_MEASURES[name](
                walked, origin, pos, target_pos, self._path_cost)
        return memo[memo_key]

    def _output(self, obs: Observation, world: WorldState) -> Dict[str, float]:
        """
        The belief reported this tick: evidence × ω_context, with the
        inadmissible and the completed hypotheses pinned at BELIEF_FLOOR and the
        floor applied. State factors only — nothing here is fed back.
        """
        unnorm: Dict[str, float] = {}
        for key, p in self._evidence.items():
            unnorm[key] = p * self._context_weight(obs, world, self._by_key[key])
        return self._finalize(unnorm, self._inadmissible | self._completed)

    def _finalize(self, unnorm: Dict[str, float], pinned: Optional[Set[str]] = None) -> Dict[str, float]:
        """Normalize, floor, and pin an unnormalized posterior over the live
        keys — the output step. `pinned` defaults to the inadmissible set;
        _output() adds the completed hypotheses."""
        total = sum(unnorm.values()) or 1.0
        distribution = {k: v / total for k, v in unnorm.items()}

        # Apply floor — no hypothesis may fall to exact zero, or it can never
        # recover through multiplicative update (see design_decisions.md).
        distribution = {k: max(v, BELIEF_FLOOR) for k, v in distribution.items()}
        floor_total = sum(distribution.values())
        distribution = {k: v / floor_total for k, v in distribution.items()}

        # Restore the pinned hypotheses so the distribution spans the full
        # hypothesis space again and still sums to 1.0.
        pinned = self._inadmissible if pinned is None else pinned
        return self._pin(distribution, pinned) if pinned else distribution

    def get_hypothesis(self, key: str) -> Optional[HypothesisKey]:
        """
        Resolve a distribution/most_likely string key back to its HypothesisKey
        (task_name + bindings). Used by meta_planner to ground the predicted
        human task without re-parsing the repr string.
        meta_planner.py calls recognizer.get_hypothesis(belief.most_likely) when it needs the binding.
        """
        return self._by_key.get(key)
    
    
    
    # -------------------------------------------------------------------------
    # Phase derivation
    # -------------------------------------------------------------------------

    @staticmethod
    def _expected_action(
        actions: Optional[List[GroundedAction]],
        world: WorldState,
    ) -> Optional[GroundedAction]:
        """
        The action the observed agent would be on if it held this intention:
        scan the planner's grounded list from the start and return the first
        whose completion condition does not hold in the world. Derived from the
        world every tick, never stored as an index — the method may have been
        re-selected since the last tick, and the same position in a different
        method is a different action. None when the hypothesis is not
        decomposable here or every completion already holds (the caller has
        then retired it on the terminal condition).
        An action with no completion predicate (ProcessCompletion) never reads
        as complete, so the scan stops at it.
        """
        for action in actions or []:
            predicate = action.completion_predicate
            if predicate is None or predicate not in world.predicates:
                return action
        return None

    @staticmethod
    def _terminal_complete(actions: List[GroundedAction], world: WorldState) -> bool:
        """
        Whether the task is done: its terminal action's completion condition
        holds, judged directly and independently of how the phases advanced.
        Deliberately indifferent to who did it — obj_at(item, table) is true
        when the robot delivered the item, and that is exactly the signal
        wanted: the task cannot be done again. A terminal ProcessCompletion
        (no predicate) can never be observed complete.
        """
        predicate = actions[-1].completion_predicate
        return predicate is not None and predicate in world.predicates

    @staticmethod
    def _task_boundary(previous: Optional[GroundedAction], actions: List[GroundedAction]) -> bool:
        """
        Whether a retirement is the OBSERVED AGENT's task boundary: the
        hypothesis expected the terminal action on the previous tick, i.e. the
        agent's own derived phase had reached the action whose completion now
        holds. A completion that arrives while the hypothesis still expected an
        earlier action (another agent delivered the item; the agent was never
        there) retires the hypothesis (the pin) but is nobody's boundary here.
        Assumes an agent whose phase reached the terminal action is the one
        who completed it — the recognizer's own evidence, not authorship in
        the world state (I1 finding 5: there is none).
        """
        return IntentionRecognizer._same_action(previous, actions[-1])

    @staticmethod
    def _same_action(a: Optional[GroundedAction], b: Optional[GroundedAction]) -> bool:
        """Identity of an expected action: name and grounded bindings — the
        decision, not its position in whichever method produced it."""
        if a is None or b is None:
            return a is b
        return a.action_name == b.action_name and a.bindings == b.bindings

    @staticmethod
    def _in_vocabulary(action: GroundedAction, mu: str) -> bool:
        """Whether `mu` is one of the discrete microactions the action's schema
        declares (pick_up → ["GRASP"], ...). Membership in the schema's own
        list — domain knowledge, never a literal compared here. A continuous
        action ("STEP*", "STAND*") declares no such list."""
        spec = action.schema.microactions
        return isinstance(spec, list) and mu in (m.upper() for m in spec)

    # -------------------------------------------------------------------------
    # Likelihood model — one value per distinct set of inputs per tick
    # -------------------------------------------------------------------------

    @staticmethod
    def _completion_likelihood(
        action: GroundedAction,
        world: WorldState,
        memo: Dict[tuple, float],
    ) -> float:
        """
        Completion channel: the observed microaction is in `action`'s
        vocabulary, so the question is whether the action's grounded completion
        predicate (the planner's) now holds — the detector's hit rate or its
        false-alarm rate. No predicate (ProcessCompletion) → nothing to judge →
        the multiplicative identity. Memoised by the predicate: two hypotheses
        expecting the same completion share one value.
        """
        predicate = action.completion_predicate
        if predicate is None:
            return 1.0
        key = ("completion", predicate)
        if key not in memo:
            memo[key] = likelihood_functions.completion_predicate_likelihood(
                predicate, frozenset(world.predicates)
            )
        return memo[key]

    def _grounded_actions(
        self,
        hyp: HypothesisKey,
        agent_id: str,
        world: WorldState,
    ) -> Optional[List[GroundedAction]]:
        """
        The actions the observed agent would perform under hyp, grounded
        against the current world by the planner: the method whose guards
        hold for that agent (what it holds decides between deliver_default,
        deliver_already_held and deliver_with_return), its derived vars, and
        every step binding. Re-selected every tick — the world is the cursor.

        None when the planner cannot decompose hyp here (DecompositionError:
        no applicable method, a derived var without a value). That is a fact
        about this hypothesis in this world, not an error in the recognizer,
        and the hypothesis is scored at the perfect-fit value (nothing to
        charge); it has no derived phase, so it is never a member of the
        adequacy test while it stays so; it is
        logged once, until the hypothesis decomposes again, so that a
        hypothesis that can never be scored is visible in the log rather than
        indistinguishable from one that is merely uninformative.
        Schema errors (unbound variable, unknown lookup) propagate: a domain
        modelling mistake must not look like uncertainty.
        Memoised per tick (cleared at the top of update()).
        """
        key = repr(hyp)
        if key in self._tick_actions:
            return self._tick_actions[key]
        try:
            actions = self._planner.decompose(hyp.task_instance(), agent_id, world)
            self._undecomposable.discard(key)
        except DecompositionError as e:
            actions = None
            if key not in self._undecomposable:
                self._undecomposable.add(key)
                logging.warning("[recognizer] %s not decomposable for %s, scored perfect-fit: %s",
                                key, agent_id, e)
        self._tick_actions[key] = actions
        return actions

    # -------------------------------------------------------------------------
    # Context weight ω_context
    # -------------------------------------------------------------------------

    def _context_weight(
        self,
        obs: Observation,
        world: WorldState,
        hyp: HypothesisKey,
    ) -> float:
        """
        Combines multiple context signals multiplicatively.
        Each signal contributes an independent boost factor.
        """
        weight = 1.0

        # Temperature boost — high temp makes ac_activation more likely
        if hyp.task_name == "ac_activation":
            if (self.context.room_temperature is not None
                    and self.context.room_temperature >= HIGH_TEMP_THRESHOLD):
                weight *= TEMPERATURE_BOOST

        # Fatigue boost — long shift makes coffee_break more likely
        if hyp.task_name == "coffee_break":
            current_step = int(obs.timestamp)
            if self.context.shift_duration(current_step) >= LONG_SHIFT_THRESHOLD:
                weight *= FATIGUE_BOOST

        return weight
