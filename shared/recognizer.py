"""
shared/recognizer.py

PURPOSE:
    Bayesian intention recognizer.
    Maintains and updates P(τ | observations) over all known intentions T.

ALGORITHM:
    P(τ | obs_1..t) ∝ P(obs_t | τ) · ω_context(τ, context, world) · P(τ | obs_1..t-1)

    Likelihood P(obs_t | τ):
        - microaction is 'grasp': if observed agent is now holding τ's target item → HIGH,
          else → LOW
        - microaction is 'step': direction-based — cosine similarity between
          human's movement vector and vector from human toward τ's target object.
          Mapped to [LOW_LIKELIHOOD, HIGH_LIKELIHOOD].
        - other microactions (release, stand): uninformative → NEUTRAL
        - 'unknown' hypothesis: always NEUTRAL (decays via normalization only)

    Context weight ω_context(τ, context, world):
        - ZONE_BOOST if in_zone(human, zone) matches τ's target zone
        - TEMPERATURE_BOOST if room_temperature is high and τ is ac_activation
        - FATIGUE_BOOST if shift is long and τ is coffee_break
        - 1.0 otherwise (no boost)

    Prior:
        - Uniform at t=0
        - Previous posterior at t>0 (passed in as prev_belief)

    Normalization: posterior sums to 1.0 after each update.

HYPOTHESIS SPACE:
    One hypothesis per (task_name, param_bindings) pair derived from the
    human agent's scheduled_tasks at construction time, plus 'unknown'.
    Hypotheses include both assigned and foreseeable tasks.

INPUTS:
    - Observation:      detected_microaction, spatial_context.position, spatial_context.zone
    - WorldState:       predicates (in_zone, holding), object_locations, object_positions
    - ContextKnowledge: shift_start_step, room_temperature
    - prev_belief:      previous BeliefState (None → uniform prior)

OUTPUTS:
    - BeliefState: distribution, most_likely, confidence
"""

from importlib.metadata import distribution
import itertools
from typing import Dict, List, Optional, Tuple

from shared.types import (
    Observation, BeliefState, WorldState, Predicate, Const,
    TaskSchema, StepCall, Var, ConditionSchema,
)
from shared.domain_knowledge import DomainKnowledgeBase, ContextKnowledge
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
    ):
        """
        knowledge:   HTN domain knowledge
        context:     background context facts for ω_context weighting
        hypotheses:  list of (task_name, bindings) pairs for this scenario.
                     Derived from the human agent's scheduled_tasks at
                     construction time in sim_agents.py.
                     
        Uniform prior over all hypotheses + unknown.
        Keyed by repr(hyp) strings — same key space as BeliefState.distribution,
        so `prior` has one consistent type throughout update(), whether it
        comes from prev_belief.distribution or this fallback.
        """
        self.knowledge = knowledge
        self.context = context
        self._hypotheses = hypotheses
        self._history: List[Observation] = []
        self._by_key: Dict[str, HypothesisKey] = {repr(h): h for h in hypotheses}  # this is used to look up HypothesisKey by string repr in update()

        # Uniform prior over all hypotheses + unknown
        n = len(hypotheses) + 1
        self._uniform: Dict[str, float] = {repr(h): 1.0 / n for h in hypotheses}
        self._uniform[UNKNOWN] = 1.0 / n

    def update(
        self,
        obs: Observation,
        world: WorldState,
        prev_belief: Optional[BeliefState] = None,
    ) -> BeliefState:
        """
        Bayesian update: P(τ|obs_1..t) ∝ P(obs_t|τ) · ω_context(τ) · P(τ|obs_1..t-1)
        """
        self._history.append(obs)

        prior: Dict[str, float] = prev_belief.distribution if prev_belief is not None else self._uniform
    
        # Compute unnormalized posterior
        unnorm: Dict[str, float] = {}
        for hyp in self._hypotheses:
            key = repr(hyp)
            likelihood = self._likelihood(obs, world, hyp)
            omega = self._context_weight(obs, world, hyp)
            default = self._uniform.get(key, 1.0 / (len(self._hypotheses) + 1))
            unnorm[key] = likelihood * omega * prior.get(key, default)

        # unknown: neutral likelihood, no context boost
        unnorm[UNKNOWN] = NEUTRAL_LIKELIHOOD * prior.get(UNKNOWN, self._uniform[UNKNOWN])

        # Normalize
        total = sum(unnorm.values()) or 1.0
        distribution = {k: v / total for k, v in unnorm.items()}

        # Apply floor — no hypothesis may fall to exact zero, or it can never
        # recover through multiplicative update (see design_decisions.md).
        distribution = {k: max(v, BELIEF_FLOOR) for k, v in distribution.items()}
        floor_total = sum(distribution.values())
        distribution = {k: v / floor_total for k, v in distribution.items()}

        most_likely = max(distribution, key=lambda k: distribution[k])
        confidence = distribution[most_likely]

        return BeliefState(
            timestamp=obs.timestamp,
            agent_id=obs.agent_id,
            distribution=distribution,
            most_likely=most_likely,
            confidence=confidence,
        )

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
    ) -> float:
        """
        Schema-driven dispatch. For each action schema in hyp's task decomposition:
          - if the schema declares a discrete microaction vocabulary (e.g. ["GRASP"],
            ["RELEASE"], ["TOUCH"]) and the observed microaction is a member of it
            → completion-predicate check against WorldState
          - if the schema is continuous ("STEP*") and declares a progress_evaluator
            → delegate to the registered evaluator (shared/likelihood_functions.py)

        No microaction string literals are compared against hardcoded values here.
        The only comparison is membership of obs.detected_microaction in each
        schema's OWN declared microactions list — domain knowledge, not simulator
        vocabulary. A new domain with a different microaction taxonomy needs zero
        changes here; it only needs correctly populated ActionSchema objects.
        """
        mu = (obs.detected_microaction or "").upper()

        for schema in self._get_relevant_action_schemas(hyp):
            spec = schema.microactions

            # Discrete completion-type action (pick_up, place, scan_it, ...)
            if isinstance(spec, list) and mu in (m.upper() for m in spec):
                predicate = self._resolve_completion_predicate(schema, hyp, obs)
                if predicate is None:
                    return NEUTRAL_LIKELIHOOD
                return likelihood_functions.completion_predicate_likelihood(
                    predicate, frozenset(world.predicates)
                )

            # Continuous progress-type action (move_to, ...)
            if spec == "STEP*" and schema.progress_evaluator:
                return self._progress_likelihood(obs, world, hyp, schema)

        return NEUTRAL_LIKELIHOOD

    def _progress_likelihood(
        self,
        obs: Observation,
        world: WorldState,
        hyp: HypothesisKey,
        schema,
    ) -> float:
        """
        Delegate to the progress evaluator named by schema.progress_evaluator.
        Builds the plain-value inputs (move_vec, current_pos, target_pos) the
        evaluator needs — no geometry happens here, only assembly of inputs
        already available from Observation history and _get_expected_position.
        """
        if len(self._history) < 2:
            return NEUTRAL_LIKELIHOOD

        evaluator = likelihood_functions.PROGRESS_EVALUATORS.get(schema.progress_evaluator)
        if evaluator is None:
            return NEUTRAL_LIKELIHOOD

        current_pos = obs.spatial_context.position
        prev_pos = self._history[-2].spatial_context.position
        move_vec = (current_pos[0] - prev_pos[0], current_pos[1] - prev_pos[1])

        target_pos = self._get_expected_position(hyp, world, obs.agent_id)
        if target_pos is None:
            return NEUTRAL_LIKELIHOOD

        return evaluator(move_vec, current_pos, target_pos)

    def _get_relevant_action_schemas(self, hyp: HypothesisKey) -> List:
        """
        Return the (deduplicated) ActionSchema objects for all actions in
        hyp's task decomposition, in first-appearance order.
        """
        task_schema = self.knowledge.get_task_schema(hyp.task_name)
        if not task_schema or not task_schema.methods:
            return []
        seen = set()
        schemas = []
        for step in task_schema.methods[0].step_calls:
            if step.action_name in seen:
                continue
            seen.add(step.action_name)
            schema = self.knowledge.get_action_schema(step.action_name)
            if schema is not None:
                schemas.append(schema)
        return schemas

    def _resolve_completion_predicate(
        self,
        schema,
        hyp: HypothesisKey,
        obs: Observation,
    ) -> Optional[Predicate]:
        """
        Resolve schema.completion (a ConditionSchema over Vars/Consts) into a
        fully-grounded Predicate, using hyp's bindings and this action's own
        step_call bindings. Returns None if schema.completion is a
        ProcessCompletion (no predicate to check, e.g. wait_at) or if any
        term can't be resolved.
        """
        if not isinstance(schema.completion, ConditionSchema):
            return None

        task_schema = self.knowledge.get_task_schema(hyp.task_name)
        values = tuple(
            self._resolve_term_value(term, hyp, obs, task_schema, schema.name)
            for term in schema.completion.args
        )
        if any(v is None for v in values):
            return None
        return Predicate(
            schema.completion.name, 
            tuple(Const(v) for v in values if v is not None)
        )

    def _resolve_term_value(
        self,
        term,
        hyp: HypothesisKey,
        obs: Observation,
        task_schema: Optional[TaskSchema],
        action_name: str,
    ) -> Optional[str]:
        """
        Resolve a single Var/Const term to a concrete value string.
        Same "hasattr(term, 'value')" idiom already used in
        _get_expected_position / _get_target_zone, kept consistent.
        We changed "hasattr(term, 'value')" to "isinstance(term, Const)" to avoid false positives on Var objects that have a 'value' attribute.
        """
        if isinstance(term, Const):
            return term.value  # Const — already concrete

        var_name = term.name  # Var
        if var_name == "?agent":
            return obs.agent_id
        if var_name in hyp.bindings:
            return hyp.bindings[var_name]

        # Fall back: look up this action's own step_call binding for var_name
        if task_schema and task_schema.methods:
            for step in task_schema.methods[0].step_calls:
                if step.action_name == action_name:
                    for k, v in step.bindings.items():
                        if getattr(k, "name", None) == var_name and isinstance(v, Const):
                            return v.value
        return None


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

        # Zone boost — human already in target zone
        target_zone = self._get_target_zone(hyp, world)
        if target_zone is not None:
            in_zone_pred = Predicate("in_zone", (Const(obs.agent_id), Const(target_zone)))
            if in_zone_pred in world.predicates:
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
    def _get_expected_position(
        self,
        hyp: HypothesisKey,
        world: WorldState,
        agent_id: str,
    ) -> Optional[Tuple[float, float]]:
        """
        Return (x, y) of the position the human is expected to be moving toward
        given hypothesis τ and current world state.

        For deliver_item(?item=X):
            - Phase 1 (not holding item): expected position is item's container (shelf)
            - Phase 2 (holding item): expected position is delivery destination
            (last move_to target in task schema, e.g. kitting_table)
        For foreseeable tasks with no ?item (coffee_break, ac_activation):
            inspect first move_to step_call in task schema → position of its target object.
        """
        item_id = hyp.bindings.get("?item")
        if item_id is not None:
            holding_pred = Predicate("holding", (Const(agent_id), Const(item_id)))
            if holding_pred in world.predicates:
                # Phase 2: item is held — expected position is delivery destination
                task_schema = self.knowledge.get_task_schema(hyp.task_name)
                if task_schema and task_schema.methods:
                    for step in reversed(task_schema.methods[0].step_calls):
                        if step.action_name == "move_to":
                            for param_var, term in step.bindings.items():
                                if isinstance(term, Const):
                                    return world.object_positions.get(term.value)
            else:
                # Phase 1: item not yet held — expected position is item's container (shelf)
                container = world.object_locations.get(item_id)
                if container:
                    pos = world.object_positions.get(container)
                    if pos:
                        return pos
                return world.object_positions.get(item_id)

        # No ?item — foreseeable task: use first move_to step_call target
        task_schema = self.knowledge.get_task_schema(hyp.task_name)
        if task_schema and task_schema.methods:
            for step in task_schema.methods[0].step_calls:
                if step.action_name == "move_to":
                    for param_var, term in step.bindings.items():
                        if isinstance(term, Const):
                            return world.object_positions.get(term.value)
        return None


    def _get_target_zone(
        self,
        hyp: HypothesisKey,
        world: WorldState,
    ) -> Optional[str]:
        """
        Return the zone of τ's target object, for ω_context zone boost.
        """
        item_id = hyp.bindings.get("?item")
        if item_id is not None:
            container = world.object_locations.get(item_id)
            if container:
                return world.object_zones.get(container)
            return world.object_zones.get(item_id)

        # Foreseeable task — get zone of first move_to target
        task_schema = self.knowledge.get_task_schema(hyp.task_name)
        if task_schema and task_schema.methods:
            for step in task_schema.methods[0].step_calls:
                if step.action_name == "move_to":
                    for param_var, term in step.bindings.items():
                        if isinstance(term, Const):
                            return world.object_zones.get(term.value)
        return None
                        
        