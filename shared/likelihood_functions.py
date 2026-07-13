"""
shared/likelihood_functions.py

PURPOSE:
    Pure, domain-agnostic likelihood functions for Bayesian intention recognition.
    No knowledge of tasks, items, zones, or simulators — only vector math and
    predicate membership tests over plain symbolic inputs.

    recognizer.py resolves WHAT to check (which predicate, which target position,
    which evaluator) from domain knowledge (ActionSchema fields). This module only
    answers HOW LIKELY a given observation is, given already-resolved inputs.

DISPATCH:
    recognizer.py selects a progress evaluator by NAME (ActionSchema.progress_evaluator),
    never by inspecting raw microaction strings. PROGRESS_EVALUATORS is the registry
    mapping those names to functions here. Adding a new ongoing-action type means:
    write one function, register it below, name it in the relevant ActionSchema.
    Zero changes to recognizer.py's orchestration logic.
"""

import math
from typing import Dict, Optional, Tuple

from shared.types import Predicate


# =============================================================================
# Likelihood constants
# (single source of truth — recognizer.py imports these, does not redefine them)
# =============================================================================
HIGH_LIKELIHOOD    = 4.0   # strong directional alignment or confirmed completion
LOW_LIKELIHOOD     = 0.1   # misaligned direction or completion predicate absent
NEUTRAL_LIKELIHOOD = 1.0   # uninformative observation


# =============================================================================
# Completion-predicate likelihood
# =============================================================================

def completion_predicate_likelihood(
    predicate: Predicate,
    world_predicates: frozenset,
) -> float:
    """
    Generic completion check: does the given (already-resolved) predicate
    currently hold in the world?

    Used for any action whose ActionSchema.completion is a ConditionSchema
    (pick_up → holding, place → obj_at, scan_it → scanned, ...). The caller
    (recognizer) is responsible for resolving the schema's completion
    ConditionSchema into a concrete Predicate using the hypothesis's bindings —
    this function only tests set membership.
    """
    return HIGH_LIKELIHOOD if predicate in world_predicates else LOW_LIKELIHOOD


# =============================================================================
# Directional (movement) progress likelihood
# =============================================================================

def direction_consistency_likelihood(
    move_vec: Tuple[float, float],
    current_pos: Tuple[float, float],
    target_pos: Tuple[float, float],
) -> float:
    """
    Cosine-similarity trajectory-consistency check.

    Scores how consistent an observed movement vector is with heading toward
    target_pos from current_pos. Mapped linearly from cosine similarity
    [-1, 1] to [LOW_LIKELIHOOD, HIGH_LIKELIHOOD].

    Registered as "directional" in PROGRESS_EVALUATORS. Applies to any action
    schema with progress_evaluator="directional" (currently: move_to).

    Returns NEUTRAL_LIKELIHOOD if the agent isn't moving (move_vec ~ 0) —
    no directional evidence available. Returns HIGH_LIKELIHOOD if already
    at the target (target_vec ~ 0) — trivially consistent.
    """
    move_norm = math.sqrt(move_vec[0] ** 2 + move_vec[1] ** 2)
    if move_norm < 1e-6:
        return NEUTRAL_LIKELIHOOD  # not moving — no directional evidence

    to_target = (target_pos[0] - current_pos[0], target_pos[1] - current_pos[1])
    target_norm = math.sqrt(to_target[0] ** 2 + to_target[1] ** 2)
    if target_norm < 1e-6:
        return HIGH_LIKELIHOOD  # already at target

    cosine = (move_vec[0] * to_target[0] + move_vec[1] * to_target[1]) / (move_norm * target_norm)

    return LOW_LIKELIHOOD + (cosine + 1.0) / 2.0 * (HIGH_LIKELIHOOD - LOW_LIKELIHOOD)


# =============================================================================
# Registry — dispatch key is ActionSchema.progress_evaluator, never a mu string
# =============================================================================

PROGRESS_EVALUATORS: Dict[str, callable] = {
    "directional": direction_consistency_likelihood,
    # Future: "duration": duration_consistency_likelihood,  (for wait_at-style actions)
}