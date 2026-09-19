"""
shared/likelihood_functions.py

PURPOSE:
    Pure, domain-agnostic likelihood functions for Bayesian intention recognition.
    No knowledge of tasks, items, zones, or simulators — only distances and
    predicate membership tests over plain symbolic inputs.

    recognizer.py resolves WHAT to check (which predicate, which target position,
    which evaluator) from domain knowledge (ActionSchema fields). This module only
    answers HOW LIKELY a given observation is, given already-resolved inputs.

THE EVIDENCE MODEL (I4):
    Every constant here has a physical meaning; nothing is a tuning knob without
    one. The recognizer's belief depends on exactly these, plus the world-state
    builder's proximity threshold (which decides when at(agent, object) holds,
    hence when phases advance — not a likelihood constant, but load-bearing).

    Movement — the excess-path likelihood (Masters & Sardina's costdif, IJCAI-18,
    with the logistic of Ramírez & Geffner's RG2). For a hypothesis whose
    expected action is located at g, measured from the ORIGIN where it began
    expecting that action:
        excess = walked + C(pos, g) - C(origin, g)
        L      = 2 / (1 + exp(BETA * excess))     — the logistic, normalised
                 so that L = 1 at zero excess (see PERFECT_FIT_LIKELIHOOD)
    `walked` is the odometer distance since the origin; C is a path cost —
    straight-line by default (Mesa agents walk through obstacles, so observed
    paths ARE straight lines), injectable for a domain that has something
    better. `excess` is the WASTED distance under the hypothesis: how much
    further the agent has walked than a perfectly efficient walk from the
    origin to g would have required. Walk straight at g and it stays at 0;
    walk away and it grows with every step — direction and distance in one
    quantity. It is recomputed from the origin every tick and REPLACES the
    previous value: twenty ticks of one walk are one observation, counted once.
    The `walked` term is kept deliberately (costdif2 drops it, preserving the
    ranking but not the values — and the meta-planner's θ gate reads values).
    The logistic is bounded and behaves when excess is negative (a moving
    target can produce it): (0, 2) after the normalisation, (0, 1] for any
    excess ≥ 0.

    BETA — detour tolerance, per cm: how much wasted path makes a target
    implausible. 1/BETA is the excess at which the likelihood has fallen to
    2/(1+e) ≈ 0.54 (from 1 at zero excess). Absolute units make it layout-scale
    dependent (the same defect recorded for min_separation, formerly
    min_safe_distance, TODO-28); the
    fractional form (excess as a fraction of C(origin, g)) was measured against
    it in the I4 sweep — see analysis/i4_evidence_model/REPORT.md.

    PERFECT_FIT_LIKELIHOOD — the value at zero excess, 1.0: the multiplicative
    identity, so that a phase with no wasted path folds NOTHING into the
    evidence when it closes and a phase advance is continuous (with the raw
    logistic, 0.5 at zero excess, every advance halved the evidence of a
    hypothesis that had done nothing wrong — measured as a 0.83 → 0.71 drop at
    the grasp tick of s40's positive control, I4 report §1). Also the value of a
    tick that offers nothing to charge: the expected action has no location or
    no graded signal (pick_up, place, wait_at: the agent is within reach of the
    action's location, or the walk would have regressed to the approach).

    UNKNOWN_LIKELIHOOD — the likelihood under `unknown` of an observation that
    covered one whole expected path. It is the threshold separating "fits
    badly enough to be called unexplained" from "fits well enough to be a real
    hypothesis": walk toward something no task targets, every hypothesis's
    excess grows and its likelihood falls, `unknown`'s does not move, and
    `unknown` wins. It also sets the CEILING on confidence — a lone hypothesis
    fitting perfectly over n whole observations reaches 1 / (1 + uⁿ), never 1.

    The grade (graded evidence, September 2026). A stretch's evidence against
    `unknown` is metered by how much of the hypothesis's expected path it
    covered: f = (C(origin, g) − C(pos, g)) / C(origin, g), the share of the
    direct cost from the origin that the agent has closed, clipped to [0, 1]
    (covered_fraction). The stretch's likelihood under `unknown` is u^f
    (graded_unknown_likelihood), so its odds are L / u^f: log-linear in f,
    evidence accrues at a constant rate per unit of expected path, and two
    stretches covering the halves of one path are worth the whole. A stretch
    that covered a whole path is worth L/u, as before the grade; one that
    covered nothing (a step away from the target: f = 0) pays L alone, so
    refutation by wasted path is untouched — the grade meters confirmation
    only. A stretch that has ARRIVED (its action's completion holds at the
    fold) is graded 1 by that fact, not by the distances: the world says the
    path is covered, and the arrival radius is the body's, not this layer's.
    Scale-free: a ratio of two costs. Observations with no path (an action
    without evaluator or target) are ungraded and stay at u.

    Completion — a detection-reliability model. The observed microaction is in
    the expected action's vocabulary (GRASP for pick_up), so the question is
    how much more likely that signal is when the action really completed than
    when it did not: P(signal | completed) = DETECTION_HIT_RATE,
    P(signal | not completed) = DETECTION_FALSE_ALARM_RATE. These describe a
    detector, not a preference. In Mesa the simulator's report IS the ground
    truth: every completion is reported (hit rate 1.0) and no signal arrives
    without one — the false-alarm rate is kept at a small non-zero value only
    so that a refuted hypothesis retains a recoverable base (the same reason
    BELIEF_FLOOR exists), and its exact value is not load-bearing in any
    measured condition (no two hypotheses ever expect a grasp at the same tick
    in the current layouts). A real cell's grasp detector misses and misfires;
    set these from its measured rates. A completion is an event at a moment: it
    MULTIPLIES onto the hypothesis's evidence, unlike the movement value.

DISPATCH:
    recognizer.py selects a progress evaluator by NAME (ActionSchema.progress_evaluator),
    never by inspecting raw microaction strings. PROGRESS_EVALUATORS is the registry
    mapping those names to functions here. Adding a new ongoing-action type means:
    write one function, register it below, name it in the relevant ActionSchema.
    Zero changes to recognizer.py's orchestration logic.
"""

import math
from typing import Callable, Dict, Optional, Tuple

from shared.types import Predicate

Position = Tuple[float, float]
PathCost = Callable[[Position, Position], float]


# =============================================================================
# The parameter set (single source of truth — recognizer.py reads these through
# the module, never redefines them)
# =============================================================================
BETA                       = 0.01    # detour tolerance, 1/cm (excess of 100 cm → L ≈ 0.54)
UNKNOWN_LIKELIHOOD         = 0.1     # likelihood under `unknown` per whole expected path covered; ceiling 1/(1+uⁿ)
DETECTION_HIT_RATE         = 1.0     # P(signal | completed): Mesa reports every completion
DETECTION_FALSE_ALARM_RATE = 1e-3    # P(signal | not completed): none in Mesa; non-zero for recoverability


# =============================================================================
# Path cost — straight-line default, injectable
# =============================================================================

def straight_line_cost(a: Position, b: Position) -> float:
    """Euclidean distance. The default C(a, b): a distance, not a path."""
    return math.hypot(b[0] - a[0], b[1] - a[1])


# =============================================================================
# Movement — excess-path likelihood
# =============================================================================

def logistic_of_excess(excess: float, beta: Optional[float] = None) -> float:
    """2 / (1 + exp(beta · excess)): 1 at zero excess, → 0 as the excess
    grows, → 2 for a (moving-target) negative excess."""
    b = BETA if beta is None else beta
    x = b * excess
    if x > 700.0:                      # exp overflow guard; the value is 0 to double precision
        return 0.0
    return 2.0 / (1.0 + math.exp(x))


PERFECT_FIT_LIKELIHOOD = logistic_of_excess(0.0)    # 1.0: nothing to charge


def excess_path_likelihood(
    walked: float,
    origin: Position,
    pos: Position,
    target_pos: Position,
    cost: PathCost = straight_line_cost,
) -> float:
    """
    Excess-path likelihood of the movement observed since `origin` under an
    action located at `target_pos`: the agent has walked `walked` (odometer
    since the origin) and is now at `pos`; a perfectly efficient walk would
    have cost C(origin, target). Registered as "excess_path"; applies to any
    action schema with progress_evaluator="excess_path" (currently: move_to).
    """
    excess = walked + cost(pos, target_pos) - cost(origin, target_pos)
    return logistic_of_excess(excess)


# =============================================================================
# The grade — how much of an expected path a stretch covered (graded evidence)
# =============================================================================

def covered_fraction(
    origin: Position,
    pos: Position,
    target_pos: Position,
    cost: PathCost = straight_line_cost,
) -> float:
    """
    The fraction of the expected path C(origin, target) that the stretch has
    covered by `pos`: the direct cost from the origin less what is still left,
    over the direct cost. 1 at the target, 0 at the origin and anywhere no
    nearer to the target than the origin (a step away covers nothing; the
    excess charges it), clipped to [0, 1]. 0 when the expected path is empty
    (the origin is at the target). A ratio of two costs: scale-free.
    """
    expected = cost(origin, target_pos)
    if expected <= 0.0:
        return 0.0
    return min(1.0, max(0.0, (expected - cost(pos, target_pos)) / expected))


def graded_unknown_likelihood(fraction: float) -> float:
    """
    The likelihood of a stretch under `unknown`, graded by the fraction of the
    expected path it covered: u^fraction — u for a whole path, 1 for none.
    Log-linear, so the odds L / u^fraction accrue at a constant rate per unit
    of expected path and compose across a path's stretches.
    """
    return UNKNOWN_LIKELIHOOD ** fraction


# =============================================================================
# Completion — detection reliability
# =============================================================================

def completion_predicate_likelihood(
    predicate: Predicate,
    world_predicates: frozenset,
) -> float:
    """
    Likelihood of the observed completion signal: the detector's hit rate if
    the action's (already-resolved) completion predicate holds in the world,
    its false-alarm rate if it does not. The caller (recognizer) resolves the
    schema's completion ConditionSchema into a concrete Predicate through the
    planner — this function only tests set membership.
    """
    return DETECTION_HIT_RATE if predicate in world_predicates else DETECTION_FALSE_ALARM_RATE


# =============================================================================
# Registry — dispatch key is ActionSchema.progress_evaluator, never a mu string
# =============================================================================

PROGRESS_EVALUATORS: Dict[str, Callable[..., float]] = {
    "excess_path": excess_path_likelihood,
    # Future: "duration": duration_consistency_likelihood,  (for wait_at-style actions)
}
