"""
shared/recognizer.py

PURPOSE:
    Bayesian intention recognizer.
    Maintains and updates P(τ | observations) over all known intentions T.

ALGORITHM:
    P(τ | obs_1..t) ∝ P(obs_t | τ) · ω_context(τ, context, world) · P(τ | obs_1..t-1)

    Likelihood P(obs_t | τ):
        - discrete microaction (grasp, release): the completion predicate of
          the matching action, as the planner grounded it, would be checked —
          but the first action of every method is a movement, whose branch
          answers first, so in practice a discrete tick is a zero-length chord
          and every hypothesis gets NEUTRAL (I1 audit 2.2; the per-hypothesis
          phase of I3 makes the completion branch reachable)
        - movement (no discrete vocabulary matches): direction-based — cosine
          similarity between the CHORD from the current leg's start to the
          agent's position and the vector from that leg start toward τ's target
          object. Mapped to [LOW_LIKELIHOOD, HIGH_LIKELIHOOD].
          τ's target is the target of the first movement action of the method
          the planner selects for τ against the current world — the observed
          agent's bindings, its guards (what it holds), its derived vars —
          resolved to a position by shared/target_resolution.py. No method is
          ever chosen by position in the schema, and no parameter is named
          here. A hypothesis no method applies to in this world (guards
          unsatisfiable, a derived var with no value) is scored NEUTRAL, not
          crashed on; the first such tick per hypothesis is logged.
        - other discrete microactions (release, stand): uninformative → NEUTRAL
        - 'unknown' hypothesis: always NEUTRAL (decays via normalization only)

    Evidence accounting — one leg is one observation:
        The recognizer keeps an EVIDENCE state (no context weights, no state
        refutations in it) and derives the output belief from it each tick.
        A discrete observation (its microaction is in some action schema's
        declared vocabulary: grasp, release, ...) is an EVENT: it multiplies
        onto the evidence state and closes the current movement leg.
        A moving observation is scored as one chord from the leg start, on top
        of the evidence the leg started from, REPLACING the leg's earlier chords
        rather than multiplying on them. A stationary observation changes
        nothing and closes the leg: a leg is a maximal run of moving
        observations. Consecutive steps of a straight walk are the same
        observation (heading varies ≤0.04° within a leg in the simulator);
        multiplying n copies of it gave 4ⁿ against 'unknown' and saturated
        belief in three steps. See design_decisions.md, "One leg is one
        observation".

    Output belief = evidence × ω_context, with state refutations pinned:
        ω_context and the held-item refutation below are facts about the current
        state, not events, so they are applied to the OUTPUT only and never fed
        back — otherwise every leg boundary would count them twice.

    Held-item refutation (hard):
        If the observed agent holds object X, every hypothesis bound to a
        different portable object is REFUTED — the intention is observed, not
        inferred — and pinned at BELIEF_FLOOR on output, the same treatment as
        an inadmissible hypothesis. Hypotheses bound to no portable object
        (coffee_break, ac_activation) and 'unknown' are never refuted by a
        grasp. This used to
        be a ×0.1 factor per step; under per-step multiplication that was de
        facto elimination, under one-observation-per-leg it would have been a
        one-shot nudge, which was never what the constraint claimed.

    Context weight ω_context(τ, context, world):
        - ZONE_BOOST if in_zone(human, zone) matches τ's target zone
        - TEMPERATURE_BOOST if room_temperature is high and τ is ac_activation
        - FATIGUE_BOOST if shift is long and τ is coffee_break
        - 1.0 otherwise (no boost)

    Prior:
        - Uniform at t=0
        - Previous posterior at t>0 (passed in as prev_belief)

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
        in it. With no assignment known, this whole mechanism is inert and the
        original code path runs unchanged.

    Normalization: posterior sums to 1.0 after each update.

HYPOTHESIS SPACE:
    One hypothesis per (task_name, param_bindings) pair derived from the domain
    schemas and the objects present in the workspace, plus 'unknown'.
    Hypotheses include both assigned and foreseeable tasks.

INPUTS:
    - Observation:      detected_microaction, spatial_context.position, spatial_context.zone
    - WorldState:       predicates (in_zone, holding), object_locations, object_positions
    - ContextKnowledge: shift_start_step, room_temperature
    - prev_belief:      previous BeliefState (None → initial prior)
    - assigned_tasks:   observed agent's work order (None/empty → restriction is off)

OUTPUTS:
    - BeliefState: distribution, most_likely, confidence
"""

from importlib.metadata import distribution
import itertools
import logging
import math
from typing import Dict, List, Optional, Set, Tuple

from shared.types import (
    Observation, BeliefState, WorldState, GroundedAction,
    TaskInstance, task_instance_key,
)
from shared.domain_knowledge import DomainKnowledgeBase, ContextKnowledge
from shared.planner import AdaptivePlanner, DecompositionError
from shared.target_resolution import movement_target_id, movement_target_position
from shared import likelihood_functions
from shared.likelihood_functions import (
    HIGH_LIKELIHOOD, LOW_LIKELIHOOD, NEUTRAL_LIKELIHOOD,
)



# =============================================================================
# Recognizer-level constants
# (HIGH/LOW/NEUTRAL likelihood now live in likelihood_functions.py — single
#  source of truth, imported above rather than redefined here)
# =============================================================================

# ω_context boost multipliers
ZONE_BOOST         = 2.0
TEMPERATURE_BOOST  = 3.0
FATIGUE_BOOST      = 2.5

HIGH_TEMP_THRESHOLD    = 26.0
LONG_SHIFT_THRESHOLD   = 500

CONFIDENCE_THRESHOLD = 0.75

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
        assigned_tasks: Optional[List[TaskInstance]] = None,
    ):
        """
        knowledge:      HTN domain knowledge
        context:        background context facts for ω_context weighting
        hypotheses:     list of (task_name, bindings) pairs for this scenario.
                        Built from the domain schemas and the workspace objects
                        at construction time in sim_agents.py.
        assigned_tasks: the OBSERVED agent's work order — which tasks it was
                        assigned, not in which order it will do them. None or
                        empty means the robot has no such knowledge: the
                        admissibility restriction is off and update() runs its
                        original unrestricted path over every hypothesis.

        _initial_prior is the t=0 prior over all hypotheses + unknown: uniform
        when the restriction is off; uniform over the admissible set, with the
        inadmissible pinned, when it is on.
        Keyed by repr(hyp) strings — same key space as BeliefState.distribution,
        so `prior` has one consistent type throughout update(), whether it
        comes from prev_belief.distribution or this fallback.
        """
        self.knowledge = knowledge
        self.context = context
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
        # not decomposable this tick). Cleared at the top of update(); both the
        # evidence pass and the output pass of one tick read it.
        self._tick_actions: Dict[str, Optional[List[GroundedAction]]] = {}
        # Keys already reported as undecomposable, so the log says it once per
        # episode rather than once per tick.
        self._undecomposable: Set[str] = set()

        # Microactions some action in the hypothesis space declares as a discrete
        # vocabulary (pick_up → ["GRASP"], place → ["RELEASE"], ...). Read from
        # the schemas, never from simulator string literals — the same membership
        # test _likelihood() dispatches on, asked once over the whole space. Used
        # by update() to tell an event from a movement observation.
        # Every method is consulted: deliver_item's first method is the guarded
        # deliver_already_held (move_to, place), which has no pick_up, so the
        # grasp vocabulary lives only in the other methods. (Per-tick dispatch
        # in _likelihood() uses the method the planner's guards select.)
        self._discrete_microactions: Set[str] = set()
        for hyp in self._hypotheses:
            task_schema = self.knowledge.get_task_schema(hyp.task_name)
            for method in (task_schema.methods if task_schema else []):
                for step in method.step_calls:
                    schema = self.knowledge.get_action_schema(step.action_name)
                    if schema is not None and isinstance(schema.microactions, list):
                        self._discrete_microactions.update(m.upper() for m in schema.microactions)
        # Evidence state — see update(). `_evidence` is the belief with no
        # context weights or state refutations in it; `_leg_base` is its value
        # at the start of the current movement leg, and `_leg_start_pos` where
        # that leg started. Movement observations are scored as ONE chord from
        # there, replacing the leg's earlier chords, not multiplying.
        self._evidence: Optional[Dict[str, float]] = None
        self._leg_base: Optional[Dict[str, float]] = None
        self._leg_start_pos: Optional[Tuple[float, float]] = None

        self._admissible: Optional[Set[str]] = self._build_admissible_keys(assigned_tasks)

        if self._admissible is None:
            # Uniform prior over all hypotheses + unknown
            n = len(self._hypotheses) + 1
            self._initial_prior: Dict[str, float] = {repr(h): 1.0 / n for h in self._hypotheses}
            self._initial_prior[UNKNOWN] = 1.0 / n
        else:
            # Uniform over the admissible set only, then pinned — the same shape
            # as every distribution update() produces, so prior and posterior
            # agree. Built in hypothesis order (then unknown), the order _weigh
            # produces, not in the admissible set's iteration order.
            n = len(self._admissible)
            live = {repr(h): 1.0 / n for h in self._hypotheses if repr(h) in self._admissible}
            live[UNKNOWN] = 1.0 / n
            self._initial_prior = self._pin(
                live,
                {k for k in self._by_key if k not in self._admissible},
            )
        # Keys pinned at BELIEF_FLOOR on every output because of the restriction.
        self._inadmissible: Set[str] = (
            set() if self._admissible is None
            else {k for k in self._by_key if k not in self._admissible}
        )
        self._evidence = self._initial_prior
        self._leg_base = self._initial_prior

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
        Used for inadmissible hypotheses (restriction) and for hypotheses
        refuted by the held item (state) alike.

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
        Bayesian update: P(τ|obs_1..t) ∝ P(obs_t|τ) · ω_context(τ) · P(τ|obs_1..t-1)

        Evidence accounting — three kinds of observation:

          discrete (microaction in some action schema's declared vocabulary —
              a domain fact, not a string literal): an EVENT. Multiplies onto
              the evidence state and closes the current movement leg.
          moving: scored as one chord from the leg start to the current
              position, on top of the evidence the leg started from —
              REPLACING the leg's earlier chords, never multiplying on them.
          stationary (no displacement since the previous observation): nothing
              new; closes the leg. A leg is a maximal run of moving
              observations, so a turn without a discrete event still starts a
              fresh chord from where the agent stopped.

        The evidence state carries neither ω_context nor the held-item
        refutation — both are facts about the current state and are applied to
        the output only (see _output()). The recognizer therefore owns its
        belief; `prev_belief` is accepted for contract compatibility and not
        consulted (its distribution already contains those output-only
        factors, so feeding it back would count them twice).
        """
        self._history.append(obs)
        self._tick_actions = {}
        current_pos = obs.spatial_context.position
        if self._leg_start_pos is None:
            self._leg_start_pos = current_pos   # the first observation opens the first leg

        mu = (obs.detected_microaction or "").upper()
        discrete = mu in self._discrete_microactions
        prev_pos = self._history[-2].spatial_context.position if len(self._history) >= 2 else None
        moving = (
            prev_pos is not None
            and math.hypot(current_pos[0] - prev_pos[0], current_pos[1] - prev_pos[1]) >= 1e-6
        )

        if discrete:
            self._evidence = self._finalize(self._weigh(obs, world, self._evidence, prev_pos))
            self._leg_base, self._leg_start_pos = self._evidence, current_pos
        elif moving:
            self._evidence = self._finalize(self._weigh(obs, world, self._leg_base, self._leg_start_pos))
        else:
            self._leg_base, self._leg_start_pos = self._evidence, current_pos

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

    def _weigh(
        self,
        obs: Observation,
        world: WorldState,
        prior: Dict[str, float],
        origin: Optional[Tuple[float, float]],
    ) -> Dict[str, float]:
        """
        Unnormalized evidence posterior: likelihood × prior over the admissible
        hypotheses plus 'unknown'. An inadmissible hypothesis is refuted, not
        down-weighted: skipped here, it neither accumulates evidence nor takes
        part in the normalization, and is pinned at BELIEF_FLOOR on output.
        With the restriction off (_admissible is None) nothing is skipped.
        `origin` is where the movement being scored began (see _progress_likelihood).
        """
        unnorm: Dict[str, float] = {}
        for hyp in self._hypotheses:
            key = repr(hyp)
            if self._admissible is not None and key not in self._admissible:
                continue
            default = self._initial_prior.get(key, 1.0 / (len(self._hypotheses) + 1))
            unnorm[key] = self._likelihood(obs, world, hyp, origin) * prior.get(key, default)
        # unknown: neutral likelihood
        unnorm[UNKNOWN] = NEUTRAL_LIKELIHOOD * prior.get(UNKNOWN, self._initial_prior[UNKNOWN])
        return unnorm

    def _output(self, obs: Observation, world: WorldState) -> Dict[str, float]:
        """
        The belief reported this tick: evidence × ω_context, with the
        hypotheses refuted by the held item pinned at BELIEF_FLOOR alongside the
        inadmissible ones. State factors only — nothing here is fed back.
        """
        refuted = self._refuted_by_holding(obs, world)
        unnorm: Dict[str, float] = {}
        for key, p in self._evidence.items():
            if key in self._inadmissible or key in refuted:
                continue
            hyp = self._by_key.get(key)
            omega = self._context_weight(obs, world, hyp) if hyp is not None else 1.0
            unnorm[key] = p * omega
        return self._finalize(unnorm, self._inadmissible | refuted)

    def _refuted_by_holding(self, obs: Observation, world: WorldState) -> Set[str]:
        """
        HELD-ITEM REFUTATION (see TODO-37): if the observed agent is holding an
        object, every hypothesis bound to a DIFFERENT portable object is
        refuted — the intention is observed, not inferred. Hypotheses bound to
        no portable object and 'unknown' are untouched. Returns the refuted
        keys; _output() pins them. Without this, a previously-delivered item
        sitting at the kitting table becomes a geometric decoy for every human
        carry leg (validated: scenario_00, run_20260904_131808, belief reached
        0.995 on an already-completed task).

        What the agent holds is read from its AgentState, a typed field, not
        by scanning predicates for a name. "Portable" is the world's own
        notion — an object that has a location (WorldState.object_locations
        is populated for exactly those) — so no parameter name is read: a
        hypothesis is refuted when any of its bindings names a portable object
        other than the held one. A rule of the evidence model; scheduled for
        removal in I3, kept exactly here.
        """
        agent_state = world.agent_states.get(obs.agent_id)
        held = agent_state.holding if agent_state is not None else None
        if held is None:
            return set()
        return {
            repr(h) for h in self._hypotheses
            if any(v != held and v in world.object_locations for v in h.bindings.values())
        }

    def _finalize(self, unnorm: Dict[str, float], pinned: Optional[Set[str]] = None) -> Dict[str, float]:
        """Normalize, floor, and pin an unnormalized posterior over the live
        keys. `pinned` defaults to the inadmissible set (the evidence state);
        _output() adds the held-item refutations."""
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
    # Likelihood model
    # -------------------------------------------------------------------------

    def _likelihood(
        self,
        obs: Observation,
        world: WorldState,
        hyp: HypothesisKey,
        origin: Optional[Tuple[float, float]] = None,
    ) -> float:
        """
        Schema-driven dispatch over the actions the observed agent would
        perform under hyp — the planner's decomposition of hyp against the
        current world (guard-selected method, every binding grounded), in
        order. For each grounded action:
          - if its schema declares a discrete microaction vocabulary (e.g.
            ["GRASP"], ["RELEASE"], ["TOUCH"]) and the observed microaction is
            a member of it → completion-predicate check against WorldState,
            using the predicate the planner already grounded
          - if the schema is continuous ("STEP*") and declares a
            progress_evaluator → delegate to the registered evaluator
            (shared/likelihood_functions.py) against that action's target
        The first action that answers decides (unchanged dispatch order; a
        per-hypothesis phase is I3's).

        No microaction string literals are compared against hardcoded values here.
        The only comparison is membership of obs.detected_microaction in each
        schema's OWN declared microactions list — domain knowledge, not simulator
        vocabulary. A new domain with a different microaction taxonomy needs zero
        changes here; it only needs correctly populated ActionSchema objects.

        A hypothesis the planner cannot decompose in this world (no method's
        guards hold, a derived var has no value) has no actions to dispatch
        over and is NEUTRAL.

        The held-item refutation is NOT applied here any more: it is a state
        fact, pinned on output by _refuted_by_holding() / _output(). Evidence
        for a refuted hypothesis still accumulates here so that it is live again,
        honestly weighted, once the item is released.
        """
        mu = (obs.detected_microaction or "").upper()

        actions = self._grounded_actions(hyp, obs.agent_id, world)
        if actions is None:
            return NEUTRAL_LIKELIHOOD

        for action in actions:
            spec = action.schema.microactions

            # Discrete completion-type action (pick_up, place, scan_it, ...)
            if isinstance(spec, list) and mu in (m.upper() for m in spec):
                predicate = action.completion_predicate
                if predicate is None:   # ProcessCompletion — nothing to observe
                    return NEUTRAL_LIKELIHOOD
                return likelihood_functions.completion_predicate_likelihood(
                    predicate, frozenset(world.predicates)
                )

            # Continuous progress-type action (move_to, ...)
            if spec == "STEP*" and action.schema.progress_evaluator:
                return self._progress_likelihood(obs, world, action, origin)

        return NEUTRAL_LIKELIHOOD

    def _progress_likelihood(
        self,
        obs: Observation,
        world: WorldState,
        action: GroundedAction,
        origin: Optional[Tuple[float, float]],
    ) -> float:
        """
        Delegate to the progress evaluator named by action.schema.progress_evaluator.
        Builds the plain-value inputs (move_vec, origin, target_pos) the evaluator
        needs — no geometry happens here, only assembly of inputs already
        available from the leg state and the action's resolved target.

        `origin` is where the movement being scored began: the leg start for a
        continuous observation (so move_vec is the leg's chord), the previous
        position for a discrete one (standing still → zero vector → NEUTRAL).
        The heading is compared against the bearing to the target FROM THE
        ORIGIN, not from the current position: a τ-walker would have gone
        straight from where the leg began. Measuring against the current
        position would let a passed target's swinging bearing re-import, one
        step at a time, the accumulation this design removes.

        The target is where the action's target object is NOW (a carried one
        is wherever its holder is) — shared/target_resolution.py, the lookup
        the projector uses for the same action.
        """
        if origin is None:
            return NEUTRAL_LIKELIHOOD

        evaluator = likelihood_functions.PROGRESS_EVALUATORS.get(action.schema.progress_evaluator)
        if evaluator is None:
            return NEUTRAL_LIKELIHOOD

        current_pos = obs.spatial_context.position
        move_vec = (current_pos[0] - origin[0], current_pos[1] - origin[1])

        target_pos = movement_target_position(action, world)
        if target_pos is None:
            return NEUTRAL_LIKELIHOOD

        return evaluator(move_vec, origin, target_pos)

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
        and the hypothesis is scored NEUTRAL; it is logged once per episode so
        that a hypothesis that can never be scored is visible in the log
        rather than indistinguishable from one that is merely uninformative.
        Schema errors (unbound variable, unknown lookup) propagate: a domain
        modelling mistake must not look like uncertainty.
        Memoised per tick: the evidence pass and the output pass read it.
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
                logging.warning("[recognizer] %s not decomposable for %s, scored NEUTRAL: %s",
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

        # Zone boost — human already in target zone. The observation carries
        # the agent's zone; the target zone is that of the object the
        # hypothesis's chord is scored against.
        target_zone = self._target_zone(hyp, obs.agent_id, world)
        if target_zone is not None and obs.spatial_context.zone == target_zone:
            weight *= ZONE_BOOST

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

    # -------------------------------------------------------------------------
    # Target resolution helpers
    # -------------------------------------------------------------------------

    def _target_zone(
        self,
        hyp: HypothesisKey,
        agent_id: str,
        world: WorldState,
    ) -> Optional[str]:
        """
        Zone of τ's target object, for ω_context zone boost: the target of the
        first movement action of the method the planner selects for τ in this
        world — the same object _progress_likelihood scores the chord against.
        WorldState.object_zones already places a carried object in its
        carrier's zone, consistent with target_resolution's position rule.
        None when τ has no movement action, is not decomposable here, or the
        object has no zone.
        """
        actions = self._grounded_actions(hyp, agent_id, world)
        for action in actions or []:
            target_id = movement_target_id(action)
            if target_id is not None:
                return world.object_zones.get(target_id)
        return None
