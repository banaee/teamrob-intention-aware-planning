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

import math
from typing import Dict, List, Optional, Tuple

from shared.types import (
    Observation, BeliefState, WorldState, Predicate, Const,
    TaskSchema, StepCall, Var,
)
from shared.domain_knowledge import DomainKnowledgeBase, ContextKnowledge


# =============================================================================
# Likelihood constants
# =============================================================================
HIGH_LIKELIHOOD    = 4.0   # strong directional alignment or confirmed grasp
LOW_LIKELIHOOD     = 0.1   # misaligned direction or wrong item grasped
NEUTRAL_LIKELIHOOD = 1.0   # uninformative observation

# ω_context boost multipliers
ZONE_BOOST         = 2.0   # human already in target zone
TEMPERATURE_BOOST  = 3.0   # high room temp → ac_activation more likely
FATIGUE_BOOST      = 2.5   # long shift → coffee_break more likely

# Thresholds for context boosts
HIGH_TEMP_THRESHOLD    = 26.0   # degrees C
LONG_SHIFT_THRESHOLD   = 500    # simulation steps

# Confidence threshold θ — above this meta_planner may act on belief
CONFIDENCE_THRESHOLD = 0.75

# Floor applied after normalization to prevent belief collapse to exact zero
BELIEF_FLOOR = 1e-3

# Unknown hypothesis key
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
def build_hypothesis_space(
    knowledge: DomainKnowledgeBase,
    known_item_ids: List[str],
) -> List[HypothesisKey]:
    """
    Build the full hypothesis space for IR.
    One HypothesisKey per (intention, parameter_binding) combination.

    For tasks with ?item parameter: one hypothesis per known item in workspace.
    For parameterless tasks (coffee_break, ac_activation): one hypothesis total.

    Called once at agent construction. Item IDs come from workspace layout —
    the robot observes all items exist, but not which are assigned to the human.
    """
    hypotheses = []
    for intention_name in knowledge.get_all_intentions():
        task_schema = knowledge.get_task_schema(intention_name)
        if task_schema is None:
            continue
        has_item_param = any(p.name == "?item" for p in task_schema.parameters)
        if has_item_param:
            for item_id in known_item_ids:
                hypotheses.append(HypothesisKey(
                    task_name=intention_name,
                    bindings={"?item": item_id},
                ))
        else:
            hypotheses.append(HypothesisKey(
                task_name=intention_name,
                bindings={},
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
        """
        self.knowledge = knowledge
        self.context = context
        self._hypotheses = hypotheses
        self._history: List[Observation] = []

        # Uniform prior over all hypotheses + unknown
        n = len(hypotheses) + 1
        self._uniform: Dict = {h: 1.0 / n for h in hypotheses}
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

        prior = prev_belief.distribution if prev_belief is not None else self._uniform

        # Compute unnormalized posterior
        unnorm: Dict = {}
        for hyp in self._hypotheses:
            key = repr(hyp)
            likelihood = self._likelihood(obs, world, hyp)
            omega = self._context_weight(obs, world, hyp)
            unnorm[key] = likelihood * omega * prior.get(key, self._uniform.get(hyp, 1.0 / (len(self._hypotheses) + 1)))

        # unknown: neutral likelihood, no context boost
        unnorm[UNKNOWN] = NEUTRAL_LIKELIHOOD * prior.get(UNKNOWN, self._uniform[UNKNOWN])

        # Normalize
        total = sum(unnorm.values()) or 1.0
        distribution = {k: v / total for k, v in unnorm.items()}

        # Apply floor to prevent belief collapse — zero-probability hypotheses
        # can never recover through multiplicative update without this.
        distribution = {k: max(v, BELIEF_FLOOR) for k, v in distribution.items()}
        floor_total = sum(distribution.values())
        distribution = {k: v / floor_total for k, v in distribution.items()}





        most_likely = max(distribution, key=distribution.get)
        confidence = distribution[most_likely]

        return BeliefState(
            timestamp=obs.timestamp,
            agent_id=obs.agent_id,
            distribution=distribution,
            most_likely=most_likely,
            confidence=confidence,
        )

    # -------------------------------------------------------------------------
    # Likelihood model
    # -------------------------------------------------------------------------

    def _likelihood(
        self,
        obs: Observation,
        world: WorldState,
        hyp: HypothesisKey,
    ) -> float:
        mu = obs.detected_microaction

        if mu == "grasp":
            return self._likelihood_grasp(obs, world, hyp)
        elif mu == "step":
            return self._likelihood_step(obs, world, hyp)
        else:
            return NEUTRAL_LIKELIHOOD

    def _likelihood_grasp(
        self,
        obs: Observation,
        world: WorldState,
        hyp: HypothesisKey,
    ) -> float:
        """
        Grasp is highly informative: holding τ's target item → HIGH, else → LOW.
        For tasks with no ?item binding (e.g. coffee_break): uninformative.
        """
        item_id = hyp.bindings.get("?item")
        if item_id is None:
            return NEUTRAL_LIKELIHOOD

        holding_pred = Predicate("holding", (Const(obs.agent_id), Const(item_id)))
        return HIGH_LIKELIHOOD if holding_pred in world.predicates else LOW_LIKELIHOOD

    def _likelihood_step(
        self,
        obs: Observation,
        world: WorldState,
        hyp: HypothesisKey,
    ) -> float:
        """
        Direction-based likelihood.
        Cosine similarity between movement vector and vector-to-target.
        Mapped linearly from [-1,1] to [LOW_LIKELIHOOD, HIGH_LIKELIHOOD].
        """
        if len(self._history) < 2:
            return NEUTRAL_LIKELIHOOD

        human_pos = obs.spatial_context.position
        prev_pos = self._history[-2].spatial_context.position

        move_vec = (human_pos[0] - prev_pos[0], human_pos[1] - prev_pos[1])
        move_norm = math.sqrt(move_vec[0]**2 + move_vec[1]**2)
        if move_norm < 1e-6:
            return NEUTRAL_LIKELIHOOD  # not moving

        expected_pos = self._get_expected_position(hyp, world, obs.agent_id)
        if expected_pos is None:
            return NEUTRAL_LIKELIHOOD

        to_target = (expected_pos[0] - human_pos[0], expected_pos[1] - human_pos[1])
        target_norm = math.sqrt(to_target[0]**2 + to_target[1]**2)
        if target_norm < 1e-6:
            return HIGH_LIKELIHOOD  # already at target

        cosine = (move_vec[0]*to_target[0] + move_vec[1]*to_target[1]) / (move_norm * target_norm)

        # Map [-1, 1] → [LOW, HIGH]
        return LOW_LIKELIHOOD + (cosine + 1.0) / 2.0 * (HIGH_LIKELIHOOD - LOW_LIKELIHOOD)

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
                                if hasattr(term, "value"):
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
                        if hasattr(term, "value"):
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
                        if hasattr(term, "value"):
                            return world.object_zones.get(term.value)
        return None
                        
        