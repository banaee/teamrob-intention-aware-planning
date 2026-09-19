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
    current world for the observed agent (I2), its actions are walked from the
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
        - progress channel: a has a progress_evaluator (move_to) → the
          excess-path likelihood: the distance the agent has walked since the
          hypothesis's origin (a per-agent odometer, read at the origin), plus
          the remaining cost to a's target, minus the direct cost from the
          origin — the path WASTED under the hypothesis — through a logistic.
          The target is the object's current location
          (shared/target_resolution.py). One stretch of movement toward one
          target is one observation however many ticks it spans: the value is
          recomputed from the origin and REPLACES the previous tick's, it is
          not multiplied on it. When the expected action changes (phase
          advance, or regress — derived, so both happen), the closing action's
          final value is folded into the evidence once and the origin (position
          and odometer reading) moves to the agent's.
        - no graded signal (an action without target or evaluator — pick_up,
          place, wait_at: the agent is within reach of where it happens — or a
          hypothesis the planner cannot decompose here): the perfect-fit value,
          nothing to charge. A stationary tick mid-stretch changes nothing:
          the excess is what it was.
        - an EMPTY stretch — nothing walked since the origin: the tick a
          hypothesis enters an action, the ticks after an episode boundary
          before the agent moves, t = 0 — is not an observation. The channel
          contributes NO FACTOR for it (not 1.0: zero excess is a perfectly
          efficient walk, and no walk is not that), and the belief carries
          forward unchanged.
        - 'unknown': a stated constant, UNKNOWN_LIKELIHOOD, per whole expected
          path covered — the reference every observation is scored against
          (I4d), GRADED by how much of the hypothesis's expected path the
          stretch covered (graded evidence): a stretch's likelihood under
          'unknown' is u^f, f the fraction of C(origin, target) closed so far
          (likelihood_functions.covered_fraction), or 1 by the world's own
          fact when the stretch has arrived (its action's completion holds at
          the fold). An observation with no path — a no-graded-signal action
          — is ungraded and pays u. A hypothesis's evidence is its ODDS
          against 'unknown': the product over its own observations of L/u^f,
          closed stretches and events in its base, the open stretch multiplied
          on top as v/u^f for this tick. A fold moves one factor from the open
          term to the base and changes nothing; 'unknown' itself takes no
          factor. The invariant, for every live hypothesis k and tick t within
          an episode:
              E_t(k)/E_t(unknown) = [π(k)/π(unknown)] · Π_closed L_k(s)/u^f_k(s)
                                    · Π_events c_k(e) · (v_k(t)/u^f_k(t) | 1 if empty)
          So a lone fitting task's ceiling is 1/(1+uⁿ) over n whole
          observations; a walk's odds rise with the path covered, from 1 on
          its first step toward 1/u at its arrival; and between two tasks of
          equal fit an extra closed stretch is worth 1/u: a phase advance is
          evidence.
    Normalisation is over every hypothesis AND 'unknown' together, never over
    the hypotheses alone. Two hypotheses whose expected actions share
    evaluator, origin, walked distance and target position receive the same
    value, computed once per tick.

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
    ends a STRETCH: the closing stretch's value folds into the evidence and is
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
    fed back. The distribution is over TASKS; the phase is internal.

    Context weight ω_context(τ, context, world):
        - TEMPERATURE_BOOST if room_temperature is high and τ is ac_activation
        - FATIGUE_BOOST if shift is long and τ is coffee_break
        - 1.0 otherwise

    Prior:
        - Uniform over the live hypotheses + unknown at t=0 and at every
          episode boundary (the admissible prior, over the current support)
        - The recognizer's own evidence state at t>0 (prev_belief is not
          consulted — see update())

    Admissibility restriction (optional, off by default):
        When the robot knows which tasks the observed agent is assigned — a work
        order, not a plan — that knowledge restricts the SUPPORT of the belief;
        it is not a magnitude. The admissible set is the assigned tasks, plus
        every foreseeable task (schema.is_foreseeable — a deviation is never part
        of a work order, and must stay recognizable), plus 'unknown'. Admissible
        hypotheses take the ordinary update above, normalized over admissible
        mass only; inadmissible ones are refuted — pinned at BELIEF_FLOOR, never
        accumulating evidence. No weight, no boost: confidence is then a function
        of the admissible set size and of the evidence, with no tunable magnitude
        in it. With no assignment known, this whole mechanism is inert.

    Normalization: posterior sums to 1.0 after each update.

HYPOTHESIS SPACE:
    One hypothesis per (task_name, param_bindings) pair derived from the domain
    schemas and the objects present in the workspace, plus 'unknown'.
    Hypotheses include both assigned and foreseeable tasks.

INPUTS:
    - Observation:      detected_microaction, spatial_context.position
    - WorldState:       predicates (completion conditions), object_locations,
                        object_positions, agent_positions (target resolution)
    - ContextKnowledge: shift_start_step, room_temperature
    - prev_belief:      previous BeliefState (None → initial prior)
    - assigned_tasks:   observed agent's work order (None/empty → restriction is off)

OUTPUTS:
    - BeliefState: distribution, most_likely, confidence
"""

import itertools
import logging
from typing import Dict, List, Optional, Set, Tuple

from shared.types import (
    Observation, BeliefState, WorldState, GroundedAction,
    TaskInstance, task_instance_key,
)
from shared.domain_knowledge import DomainKnowledgeBase, ContextKnowledge
from shared.planner import AdaptivePlanner, DecompositionError
from shared.target_resolution import movement_target_position
from shared import likelihood_functions



# =============================================================================
# Recognizer-level constants
# (the likelihood constants — UNKNOWN_LIKELIHOOD, the detection rates — live
#  in likelihood_functions.py, single source of truth, read through the module
#  at call time rather than redefined here; the detour tolerance beta is the
#  embodiment's, passed to the constructor)
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

UNKNOWN = "unknown"


# =============================================================================
# HypothesisKey
# =============================================================================

class HypothesisKey:
    """
    Identifies one IR hypothesis: a task with specific parameter bindings.
    e.g. deliver_item(?item=item_3), coffee_break()
    """
    def __init__(self, task_name: str, bindings: Dict[str, str]):
        self.task_name = task_name
        self.bindings = bindings

    def __repr__(self):
        if self.bindings:
            params = ",".join(f"{k}={v}" for k, v in sorted(self.bindings.items()))
            return f"{self.task_name}({params})"
        return f"{self.task_name}()"

    def __eq__(self, other):
        return (isinstance(other, HypothesisKey)
                and self.task_name == other.task_name
                and self.bindings == other.bindings)

    def __hash__(self):
        return hash((self.task_name, tuple(sorted(self.bindings.items()))))

# ============================================================================
#  Functions
# ============================================================================ 
# def build_hypothesis_space(
#     knowledge: DomainKnowledgeBase,
#     known_item_ids: List[str],
# ) -> List[HypothesisKey]:
#     """
#     Build the full hypothesis space for IR.
#     One HypothesisKey per (intention, parameter_binding) combination.

#     For tasks with ?item parameter: one hypothesis per known item in workspace.
#     For parameterless tasks (coffee_break, ac_activation): one hypothesis total.

#     Called once at agent construction. Item IDs come from workspace layout —
#     the robot observes all items exist, but not which are assigned to the human.
#     """
#     hypotheses = []
#     for intention_name in knowledge.get_all_intentions():
#         task_schema = knowledge.get_task_schema(intention_name)
#         if task_schema is None:
#             continue
#         param_types = task_schema.parameter_types
#         if not param_types:
#             hypotheses.append(HypothesisKey(task_name=intention_name, bindings={}))
#             continue
#         var_names = list(param_types.keys())
#         candidate_lists = [knowledge.get_objects_by_type(param_types[v]) for v in var_names]
#         for combo in itertools.product(*candidate_lists):
#             hypotheses.append(HypothesisKey(
#                 task_name=intention_name,
#                 bindings=dict(zip(var_names, combo)),
#             ))
#     return hypotheses

def build_hypothesis_space(
    knowledge: DomainKnowledgeBase,
    known_objects_by_type: Dict[str, List[str]],   # was: known_item_ids: List[str]
) -> List[HypothesisKey]:
    hypotheses = []
    for intention_name in knowledge.get_all_intentions():
        task_schema = knowledge.get_task_schema(intention_name)
        if task_schema is None:
            continue
        param_types = task_schema.parameter_types
        if not param_types:
            hypotheses.append(HypothesisKey(task_name=intention_name, bindings={}))
            continue
        var_names = list(param_types.keys())
        candidate_lists = [known_objects_by_type.get(param_types[v], []) for v in var_names]
        for combo in itertools.product(*candidate_lists):
            hypotheses.append(HypothesisKey(
                task_name=intention_name,
                bindings=dict(zip(var_names, combo)),
            ))
    return hypotheses

# =============================================================================
# IntentionRecognizer
# =============================================================================

class IntentionRecognizer:

    def __init__(
        self,
        knowledge: DomainKnowledgeBase,
        context: ContextKnowledge,
        hypotheses: List[HypothesisKey],
        beta: float,
        assigned_tasks: Optional[List[TaskInstance]] = None,
        path_cost: Optional[likelihood_functions.PathCost] = None,
    ):
        """
        knowledge:      HTN domain knowledge
        context:        background context facts for ω_context weighting
        hypotheses:     list of (task_name, bindings) pairs for this scenario.
                        Built from the domain schemas and the workspace objects
                        at construction time in sim_agents.py.
        beta:           the excess-path likelihood's detour tolerance, per unit
                        of the body's length (Mesa: 0.01 /cm). Supplied by the
                        embodiment, no default: it carries the body's units,
                        and shared/ holds none (T-A1; TODO-58).
        assigned_tasks: the OBSERVED agent's work order — which tasks it was
                        assigned, not in which order it will do them. None or
                        empty means the robot has no such knowledge: the
                        admissibility restriction is off and update() runs its
                        original unrestricted path over every hypothesis.
        path_cost:      C(a, b), the cost of the walk between two positions the
                        excess-path likelihood is measured against. Straight-line
                        distance by default (Mesa agents walk through obstacles);
                        a domain with a better model injects it here.

        _initial_prior is the t=0 prior over all hypotheses + unknown: uniform
        when the restriction is off; uniform over the admissible set, with the
        inadmissible pinned, when it is on.
        Keyed by repr(hyp) strings — same key space as BeliefState.distribution,
        so `prior` has one consistent type throughout update(), whether it
        comes from prev_belief.distribution or this fallback.
        """
        self.knowledge = knowledge
        self.context = context
        self._path_cost = path_cost or likelihood_functions.straight_line_cost
        self._beta = beta
        # A schema naming an evaluator the registry does not have is a domain
        # modelling error, and must not look like uncertainty: without this
        # check every movement under it would silently score the perfect fit.
        for schema in knowledge.get_all_actions():
            name = schema.progress_evaluator
            if name is not None and name not in likelihood_functions.PROGRESS_EVALUATORS:
                raise ValueError(
                    f"action '{schema.name}' names progress_evaluator '{name}', which is not "
                    f"registered in likelihood_functions.PROGRESS_EVALUATORS "
                    f"({sorted(likelihood_functions.PROGRESS_EVALUATORS)})")
        # Sorted by key so that every order-dependent step downstream — the
        # insertion order of the evidence and output dicts, hence max()'s
        # tie-break for most_likely and the order of tied entries in the log —
        # is a function of the hypothesis space alone, not of the order the
        # caller enumerated it in (which followed DomainModel.intentions, a
        # set, hence the process's hash seed; TODO-42).
        self._hypotheses = sorted(hypotheses, key=repr)
        self._history: List[Observation] = []
        self._by_key: Dict[str, HypothesisKey] = {repr(h): h for h in self._hypotheses}  # this is used to look up HypothesisKey by string repr in update()

        # The same method selection the executor's plans come from. A
        # hypothesis is grounded through it every tick against the live world:
        # which method its guards admit for the observed agent, and what each
        # step then targets. Held privately for the same reason the projector
        # holds one — decomposition is stateless and world-driven.
        self._planner = AdaptivePlanner(knowledge=knowledge)
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
        #   _base[key]      the hypothesis's closed ODDS against unknown: every
        #                   closed phase (as L/u^f) and every event of the CURRENT
        #                   EPISODE folded in, in one common scale across keys
        #                   (rescaled each tick so that Σ base·open = 1); the
        #                   open phase's v/u^f is recomputed from _origin each tick
        #                   and multiplied on top, never into it; re-initialised
        #                   to the prior at every episode boundary.
        #                   _base[UNKNOWN] is the reference and only rescales.
        #   _completed      keys whose terminal completion condition has held:
        #                   skipped and pinned for the rest of the run
        self._expected: Dict[str, Optional[GroundedAction]] = {}
        self._origin: Dict[str, Tuple[float, float]] = {}
        self._origin_odo: Dict[str, float] = {}
        self._base: Dict[str, float] = {}
        self._completed: Set[str] = set()
        # Per observed agent: total path length walked since its first
        # observation (the sum of straight-line steps between consecutive
        # observed positions) and the position that total was last advanced to.
        self._odometer: Dict[str, float] = {}
        self._last_pos: Dict[str, Tuple[float, float]] = {}
        # Normalized evidence over the live keys + unknown — the belief with no
        # context weights and no pins in it; _output() derives the report from it.
        self._evidence: Dict[str, float] = {}

        self._admissible: Optional[Set[str]] = self._build_admissible_keys(assigned_tasks)

        if self._admissible is None:
            # Uniform prior over all hypotheses + unknown
            self._initial_prior: Dict[str, float] = self._prior([repr(h) for h in self._hypotheses])
        else:
            # Uniform over the admissible set only, then pinned — the same shape
            # as every distribution update() produces, so prior and posterior
            # agree. Built in hypothesis order (then unknown), the order update()
            # produces, not in the admissible set's iteration order.
            self._initial_prior = self._pin(
                self._prior([repr(h) for h in self._hypotheses if repr(h) in self._admissible]),
                {k for k in self._by_key if k not in self._admissible},
            )
        # Keys pinned at BELIEF_FLOOR on every output because of the restriction.
        self._inadmissible: Set[str] = (
            set() if self._admissible is None
            else {k for k in self._by_key if k not in self._admissible}
        )
        self._evidence = {k: v for k, v in self._initial_prior.items() if k not in self._inadmissible}
        self._base = dict(self._evidence)

    @staticmethod
    def _prior(live: List[str]) -> Dict[str, float]:
        """
        The prior over the hypotheses in `live` (keys, in hypothesis order)
        and 'unknown': uniform. The one prior the recognizer has — used at
        construction over the admissible set and at every episode boundary
        over the hypotheses still live. Nothing else is stored to re-start
        from.
        """
        n = len(live) + 1
        out = {k: 1.0 / n for k in live}
        out[UNKNOWN] = 1.0 / n
        return out

    def _begin_episode(self, pos: Tuple[float, float], odo: float) -> None:
        """
        An episode boundary: the observed agent has completed a task, and the
        intention the recognizer estimates — the task of the CURRENT
        behavioural episode — is a new question. The ended episode's evidence
        (every fold, every event) is discarded uniformly: every live
        hypothesis's base becomes the prior over the hypotheses still live,
        whatever its phase history was, and every origin moves to the agent's
        position. Every stretch is now empty, so the belief IS the prior until
        the agent moves. Completed hypotheses are not live and stay pinned.
        Nothing crosses the boundary: a task hypothesis says which task is
        being executed now, not what the agent is disposed to do next, and
        there is no representation here for the latter.
        """
        self._base = self._prior([k for k in self._base if k != UNKNOWN])
        self._evidence = dict(self._base)
        for key in self._origin:
            self._origin[key], self._origin_odo[key] = pos, odo

    def _build_admissible_keys(
        self,
        assigned_tasks: Optional[List[TaskInstance]],
    ) -> Optional[Set[str]]:
        """
        The set of hypothesis keys the observed agent's intention may lie in:
        its assigned tasks, plus every foreseeable task, plus 'unknown'. Returns
        None when nothing is known, which switches the mechanism off entirely
        rather than admitting everything explicitly — equivalent in effect, but
        None keeps update() on its original, unrestricted path.

        Foreseeable tasks and 'unknown' are admissible by construction. A
        foreseeable task is a deviation, and deviations are exactly what a work
        order does not list — identified by schema.is_foreseeable, so no task
        name is named here. 'unknown' is the escape hatch for behaviour outside
        the model. Restricting either away would make a deviation unrecognizable
        at the very moment it happens.

        Assignment identity crosses the layer boundary as task_instance_key(),
        which produces the same string as HypothesisKey.__repr__ by design.
        """
        if not assigned_tasks:
            return None

        admissible: Set[str] = {UNKNOWN}
        for hyp in self._hypotheses:
            schema = self.knowledge.get_task_schema(hyp.task_name)
            if schema is not None and schema.is_foreseeable:
                admissible.add(repr(hyp))

        for key in (task_instance_key(t) for t in assigned_tasks):
            if key in self._by_key:
                admissible.add(key)
            else:
                logging.warning(
                    "[recognizer] assigned task %s matches no hypothesis — ignored", key
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
          4. if the expected action changed, fold the closing action's final
             excess-path value, as odds L/u^f against unknown — f the fraction
             of the expected path the stretch covered, 1 if the action's
             completion holds (_unknown_likelihood) — into the evidence once
             (nothing, if its stretch was empty) and move the origin (position
             and odometer reading) to the agent's (a phase advance — or
             regress; both are derived facts);
          5. the open action's excess-path value from the origin, as v/u^f,
             multiplies on top of the evidence for this tick only (replaced
             next tick) — or no factor at all if the stretch is empty (nothing
             walked since the origin: not an observation).
        `unknown` is the reference and takes no factor. Then normalize over the
        live keys + unknown together. If a retirement this tick was the observed agent's
        own (step 2, terminal action expected on the previous tick), the
        episode ends: the belief re-initialises to the prior over the live
        keys + unknown and every origin moves to the agent's position
        (_begin_episode); this tick reports the re-initialised belief.

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
        agent = obs.agent_id
        if agent in self._last_pos:
            self._odometer[agent] += likelihood_functions.straight_line_cost(self._last_pos[agent], pos)
        else:
            self._odometer[agent] = 0.0
        self._last_pos[agent] = pos
        odo = self._odometer[agent]

        unnorm: Dict[str, float] = {}
        boundary = False
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
                logging.info("[IR-complete] step=%d %s completed: %s holds",
                             int(obs.timestamp), key, actions[-1].completion_predicate)
                continue
            current = self._expected_action(actions, world)

            if key not in self._expected:
                # First observation of this hypothesis: it enters its current
                # action here. Its stretch is empty: no observation, no factor.
                self._expected[key], self._origin[key], self._origin_odo[key] = current, pos, odo
                unnorm[key] = self._base[key]
                continue

            previous = self._expected[key]
            if previous is not None and self._in_vocabulary(previous, mu):
                self._base[key] *= self._completion_likelihood(previous, world, memo)
            if not self._same_action(previous, current):
                # The closing stretch's final value folds into the evidence
                # once — nothing folds if the stretch was empty. The new
                # action's stretch begins here, empty: no factor this tick
                # unless the action has no graded signal (then, as on every
                # tick, the perfect-fit value: nothing to charge).
                closing = self._progress_likelihood(
                    previous, self._origin[key], odo - self._origin_odo[key], pos, world, memo)
                if closing is not None:
                    # The stretch was one observation: its likelihood under
                    # the hypothesis AND under `unknown` fold together, as the
                    # odds L/u^f the open term already held (I4d), `unknown`'s
                    # graded by the path the stretch covered — the whole of
                    # it, if the action it served is complete.
                    self._base[key] *= closing / self._unknown_likelihood(
                        previous, self._origin[key], pos, world, arrived=self._completion_holds(previous, world))
                self._expected[key], self._origin[key], self._origin_odo[key] = current, pos, odo
                value = self._progress_likelihood(current, pos, 0.0, pos, world, memo)
            else:
                value = self._progress_likelihood(
                    current, self._origin[key], odo - self._origin_odo[key], pos, world, memo)
            # The open observation, if there is one, as odds against `unknown`.
            unnorm[key] = (self._base[key] if value is None
                           else self._base[key] * value / self._unknown_likelihood(
                               current, self._origin[key], pos, world))
        # `unknown` is the reference: every observation is scored against it
        # inside the hypothesis's own odds, so it takes no factor of its own.
        unnorm[UNKNOWN] = self._base[UNKNOWN]

        # One normalization, at the task layer, over the live keys AND unknown.
        # The bases are rescaled by the same total so they stay in one scale
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
            self._begin_episode(pos, odo)
            logging.info("[IR-boundary] step=%d %s completed a task: belief re-initialised to the "
                         "prior over %d hypotheses + unknown, origins reset",
                         int(obs.timestamp), agent, len(self._origin))

        distribution = self._output(obs, world)
        most_likely = max(distribution, key=lambda k: distribution[k])
        confidence = distribution[most_likely]

        return BeliefState(
            timestamp=obs.timestamp,
            agent_id=obs.agent_id,
            distribution=distribution,
            most_likely=most_likely,
            confidence=confidence,
        )

    def _output(self, obs: Observation, world: WorldState) -> Dict[str, float]:
        """
        The belief reported this tick: evidence × ω_context, with the
        inadmissible and the completed hypotheses pinned at BELIEF_FLOOR and the
        floor applied. State factors only — nothing here is fed back.
        """
        unnorm: Dict[str, float] = {}
        for key, p in self._evidence.items():
            hyp = self._by_key.get(key)
            omega = self._context_weight(obs, world, hyp) if hyp is not None else 1.0
            unnorm[key] = p * omega
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
        walk the planner's grounded list from the start and return the first
        whose completion condition does not hold in the world. Derived from the
        world every tick, never stored as an index — the method may have been
        re-selected since the last tick, and the same position in a different
        method is a different action. None when the hypothesis is not
        decomposable here or every completion already holds (the caller has
        then retired it on the terminal condition).
        An action with no completion predicate (ProcessCompletion) never reads
        as complete, so a walk stops at it.
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
    def _completion_holds(action: Optional[GroundedAction], world: WorldState) -> bool:
        """Whether `action`'s grounded completion predicate holds in the world:
        the stretch that served it has arrived. False for no action and for a
        ProcessCompletion (no predicate: never observably complete)."""
        if action is None:
            return False
        predicate = action.completion_predicate
        return predicate is not None and predicate in world.predicates

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

    def _progress_likelihood(
        self,
        action: Optional[GroundedAction],
        origin: Tuple[float, float],
        walked: float,
        pos: Tuple[float, float],
        world: WorldState,
        memo: Dict[tuple, float],
    ) -> Optional[float]:
        """
        Progress channel: delegate to the evaluator named by
        action.schema.progress_evaluator with the distance `walked` since
        `origin` (where the hypothesis entered this action), the agent's
        position, the target's current position (shared/target_resolution.py,
        the lookup the projector uses) and the injected path cost. The excess
        is measured FROM THE ORIGIN, not tick to tick: a τ-walker would have
        gone straight from where it began, and a passed target must not
        re-import accumulation one step at a time.

        None when the stretch is EMPTY — nothing walked since the origin. An
        empty stretch is not an observation: it is not a perfectly efficient
        walk (zero excess), it is no walk, and the channel has nothing to say.
        The caller applies no factor for it. (Stationarity as evidence AGAINST
        an action that predicts movement would be a different observation
        channel; it is not this one.)

        The perfect-fit value when there is no action, no evaluator (pick_up,
        place, wait_at: no graded in-progress signal) or no resolvable target.
        Memoised by (evaluator, origin, walked, target position): two
        hypotheses whose expected actions head for the same place from the
        same origin at the same odometer reading — two items on one shelf —
        share one value; two that share a position but not the reading do not.
        """
        if action is None:
            return likelihood_functions.PERFECT_FIT_LIKELIHOOD
        evaluator = likelihood_functions.PROGRESS_EVALUATORS.get(action.schema.progress_evaluator)
        if evaluator is None:
            return likelihood_functions.PERFECT_FIT_LIKELIHOOD
        target_pos = movement_target_position(action, world)
        if target_pos is None:
            return likelihood_functions.PERFECT_FIT_LIKELIHOOD
        if walked <= 0.0:
            return None
        key = ("progress", action.schema.progress_evaluator, origin, walked, target_pos)
        if key not in memo:
            memo[key] = evaluator(walked, origin, pos, target_pos, self._path_cost, self._beta)
        return memo[key]

    def _unknown_likelihood(
        self,
        action: Optional[GroundedAction],
        origin: Tuple[float, float],
        pos: Tuple[float, float],
        world: WorldState,
        arrived: bool = False,
    ) -> float:
        """
        The likelihood under `unknown` of the observation the open or closing
        stretch of `action` is — the reference the hypothesis's own value is
        scored against — GRADED by how much of the hypothesis's expected path
        the stretch covered (graded evidence): u^f, with f the fraction of
        C(origin, target) closed by `pos` (likelihood_functions.covered_fraction,
        the same origin, target and path cost the excess is measured against),
        or f = 1 when the stretch has `arrived` — the action's completion
        holds at the fold, so the world itself says the path is covered,
        whatever the arrival radius (the body's, not this layer's). Ungraded,
        u, for an observation with no path to grade: no action, no evaluator
        (pick_up, place, wait_at) or no resolvable target — one whole
        observation, as before the grade. A step away from the target covers
        nothing (f = 0, u^0 = 1): such a stretch pays its L alone, so the
        grade meters confirmation and leaves refutation to the excess.
        """
        if arrived:
            return likelihood_functions.UNKNOWN_LIKELIHOOD
        if action is None or action.schema.progress_evaluator is None:
            return likelihood_functions.UNKNOWN_LIKELIHOOD
        target_pos = movement_target_position(action, world)
        if target_pos is None:
            return likelihood_functions.UNKNOWN_LIKELIHOOD
        return likelihood_functions.graded_unknown_likelihood(
            likelihood_functions.covered_fraction(origin, pos, target_pos, self._path_cost))

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
        charge: one ungraded observation, 1/u, per tick it stays so); it is
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
            actions = self._planner.decompose(hyp.task_name, hyp.bindings, agent_id, world)
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
