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

    Likelihood of the expected action a, all constants unchanged from before:
        - completion channel: the observed microaction is in a's declared
          discrete vocabulary (pick_up → GRASP, place → RELEASE, ...) → HIGH if
          a's grounded completion predicate holds in the world, else LOW. It is
          judged on the action the hypothesis expected BEFORE the event (the
          world after a grasp already satisfies pick_up's completion, so the
          derived action has moved on). An event is a fact at a moment: it
          MULTIPLIES onto the hypothesis's evidence.
        - progress channel: a has a progress_evaluator (move_to) → the cosine
          kernel on the CHORD from the hypothesis's origin to the agent's
          position, against the bearing from that origin to a's target (the
          object's current location, shared/target_resolution.py). One stretch
          of movement toward one target is one observation however many ticks
          it spans: the chord value REPLACES the previous tick's, it is not
          multiplied on it. When the expected action changes (phase advance,
          or regress — derived, so both happen), the closing action's final
          chord is folded into the evidence once and the origin moves to the
          agent's position.
        - neither (a stationary tick, a discrete action observing something
          outside its vocabulary, an action without target or evaluator, a
          hypothesis the planner cannot decompose here): NEUTRAL.
        - 'unknown': always NEUTRAL.
    Two hypotheses whose expected actions share evaluator, origin and target
    position receive the same value, computed once per tick.

    Completed tasks: judged on the TERMINAL action's completion condition
    directly (obj_at(item, table), waited(agent, machine)), whatever the phase
    walk did and whoever did it — the task is done and nobody can do it again.
    A completed hypothesis is skipped in the update (it accumulates no more
    evidence) AND pinned at BELIEF_FLOOR on output, for the rest of the run.

    Output belief = evidence × ω_context, with inadmissible and completed
    hypotheses pinned at BELIEF_FLOOR and the floor applied. ω_context is a fact
    about the current state, not an event: applied to the output only, never
    fed back. The distribution is over TASKS; the phase is internal.

    Context weight ω_context(τ, context, world):
        - TEMPERATURE_BOOST if room_temperature is high and τ is ac_activation
        - FATIGUE_BOOST if shift is long and τ is coffee_break
        - 1.0 otherwise

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
from shared.likelihood_functions import (
    HIGH_LIKELIHOOD, LOW_LIKELIHOOD, NEUTRAL_LIKELIHOOD,
)



# =============================================================================
# Recognizer-level constants
# (HIGH/LOW/NEUTRAL likelihood now live in likelihood_functions.py — single
#  source of truth, imported above rather than redefined here)
# =============================================================================

# ω_context boost multipliers
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
        #                   expected one — where its chord is measured from
        #   _base[key]      the hypothesis's evidence with every closed phase and
        #                   every event folded in, in one common scale across
        #                   keys (rescaled each tick so that Σ base·chord = 1);
        #                   the open phase's chord is recomputed from _origin
        #                   each tick and multiplied on top, never into it
        #   _completed      keys whose terminal completion condition has held:
        #                   skipped and pinned for the rest of the run
        self._expected: Dict[str, Optional[GroundedAction]] = {}
        self._origin: Dict[str, Tuple[float, float]] = {}
        self._base: Dict[str, float] = {}
        self._completed: Set[str] = set()
        # Normalized evidence over the live keys + unknown — the belief with no
        # context weights and no pins in it; _output() derives the report from it.
        self._evidence: Dict[str, float] = {}

        self._admissible: Optional[Set[str]] = self._build_admissible_keys(assigned_tasks)

        if self._admissible is None:
            # Uniform prior over all hypotheses + unknown
            n = len(self._hypotheses) + 1
            self._initial_prior: Dict[str, float] = {repr(h): 1.0 / n for h in self._hypotheses}
            self._initial_prior[UNKNOWN] = 1.0 / n
        else:
            # Uniform over the admissible set only, then pinned — the same shape
            # as every distribution update() produces, so prior and posterior
            # agree. Built in hypothesis order (then unknown), the order update()
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
        self._evidence = {k: v for k, v in self._initial_prior.items() if k not in self._inadmissible}
        self._base = dict(self._evidence)

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
             chord into the evidence once and move the origin to the agent's
             position (a phase advance — or regress; both are derived facts);
          5. the open action's chord from the origin multiplies on top of the
             evidence for this tick only (replaced next tick).
        Then normalize over the live keys + unknown.

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

        unnorm: Dict[str, float] = {}
        for hyp in self._hypotheses:
            key = repr(hyp)
            if key in self._inadmissible or key in self._completed:
                continue
            actions = self._grounded_actions(hyp, obs.agent_id, world)
            if actions is not None and self._terminal_complete(actions, world):
                self._completed.add(key)
                self._base.pop(key, None)
                self._expected.pop(key, None)
                self._origin.pop(key, None)
                logging.info("[IR-complete] step=%d %s completed: %s holds",
                             int(obs.timestamp), key, actions[-1].completion_predicate)
                continue
            current = self._expected_action(actions, world)

            if key not in self._expected:
                # First observation of this hypothesis: it enters its current
                # action here. No chord yet.
                self._expected[key], self._origin[key] = current, pos
                unnorm[key] = self._base[key]
                continue

            previous = self._expected[key]
            if previous is not None and self._in_vocabulary(previous, mu):
                self._base[key] *= self._completion_likelihood(previous, world, memo)
            if not self._same_action(previous, current):
                self._base[key] *= self._progress_likelihood(previous, self._origin[key], pos, world, memo)
                self._expected[key], self._origin[key] = current, pos
                chord = NEUTRAL_LIKELIHOOD
            else:
                chord = self._progress_likelihood(current, self._origin[key], pos, world, memo)
            unnorm[key] = self._base[key] * chord
        unnorm[UNKNOWN] = self._base[UNKNOWN] * NEUTRAL_LIKELIHOOD

        # One normalization, at the task layer. The bases are rescaled by the
        # same total so they stay in one scale with each other (ratios are
        # untouched) and so that evidence == base × open chord exactly.
        total = sum(unnorm.values()) or 1.0
        for key in self._base:
            self._base[key] /= total
        self._evidence = {k: v / total for k, v in unnorm.items()}

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
        predicate (the planner's) now holds — HIGH or LOW. No predicate
        (ProcessCompletion) → nothing to observe → NEUTRAL. Memoised by the
        predicate: two hypotheses expecting the same completion share one value.
        """
        predicate = action.completion_predicate
        if predicate is None:
            return NEUTRAL_LIKELIHOOD
        key = ("completion", predicate)
        if key not in memo:
            memo[key] = likelihood_functions.completion_predicate_likelihood(
                predicate, frozenset(world.predicates)
            )
        return memo[key]

    @staticmethod
    def _progress_likelihood(
        action: Optional[GroundedAction],
        origin: Tuple[float, float],
        pos: Tuple[float, float],
        world: WorldState,
        memo: Dict[tuple, float],
    ) -> float:
        """
        Progress channel: delegate to the evaluator named by
        action.schema.progress_evaluator with the chord from `origin` (where
        the hypothesis entered this action) to `pos`, against the target's
        current position (shared/target_resolution.py, the lookup the projector
        uses). The heading is compared with the bearing FROM THE ORIGIN, not
        from the current position: a τ-walker would have gone straight from
        where it began; a passed target's swinging bearing must not re-import
        accumulation one step at a time. A zero chord (the agent has not moved
        since the origin was set) is NEUTRAL inside the kernel.

        NEUTRAL when there is no action, no evaluator (pick_up, place, wait_at:
        no graded in-progress signal) or no resolvable target. Memoised by
        (evaluator, origin, target position): two hypotheses whose expected
        actions head for the same place from the same origin — two items on one
        shelf — share one value.
        """
        if action is None:
            return NEUTRAL_LIKELIHOOD
        evaluator = likelihood_functions.PROGRESS_EVALUATORS.get(action.schema.progress_evaluator)
        if evaluator is None:
            return NEUTRAL_LIKELIHOOD
        target_pos = movement_target_position(action, world)
        if target_pos is None:
            return NEUTRAL_LIKELIHOOD
        key = ("progress", action.schema.progress_evaluator, origin, target_pos)
        if key not in memo:
            move_vec = (pos[0] - origin[0], pos[1] - origin[1])
            memo[key] = evaluator(move_vec, origin, target_pos)
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
        and the hypothesis is scored NEUTRAL; it is logged once per episode so
        that a hypothesis that can never be scored is visible in the log
        rather than indistinguishable from one that is merely uninformative.
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
