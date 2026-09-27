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
        L      = 2 / (1 + exp(beta * excess))     — the logistic, normalised
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

    beta — detour tolerance, per unit of length: how much wasted path makes a
    target implausible. 1/beta is the excess at which the likelihood has fallen
    to 2/(1+e) ≈ 0.54 (from 1 at zero excess). A physical tolerance about how
    people walk, in the body's length units, so it is NOT held here: the
    embodiment supplies it to IntentionRecognizer (Mesa: 0.01 /cm,
    mesa_configs.yaml), as it supplies min_separation to the MetaPlanner
    (T-A1; TODO-58). One fixed value per embodiment, decided on IR grounds, not
    per layout. The fractional form (excess as a fraction of C(origin, g)) was
    measured against it in the I4 sweep — see analysis/i4_evidence_model/REPORT.md.

    PERFECT_FIT_LIKELIHOOD — the value at zero excess, 1.0: the multiplicative
    identity, so that a phase with no wasted path folds NOTHING into the
    evidence when it closes and a phase advance is continuous (with the raw
    logistic, 0.5 at zero excess, every advance halved the evidence of a
    hypothesis that had done nothing wrong — measured as a 0.83 → 0.71 drop at
    the grasp tick of s40's positive control, I4 report §1). Also the value of a
    tick that offers nothing to charge: the expected action has no location or
    no graded signal (pick_up, place, wait_at: the agent is within reach of the
    action's location, or the walk would have regressed to the approach).

    The belief has no reference hypothesis (T-D R1, 27 September 2026): each live
    hypothesis pays its own likelihood per stretch, and the recognizer
    normalises over the live hypothesis set H only. The absolute question —
    whether the best of the robot's models is wrong — is not the belief's; it is
    the adequacy finding's (below, and shared/recognizer.py).

    Adequacy — the tail probability (T-D E5). The same logistic read as a
    density on x >= 0, p(x) = beta·L(x) / (2 ln 2), is the reference
    distribution the adequacy test reads a hypothesis's projected completion
    delay against, in length units (x = v·D, v the body's speed):
        S(x) = ln(1 + exp(-beta·x)) / ln 2   for x > 0,   S = 1 for x <= 0.
    A modelling assumption, stated as one: it criticises the model the belief
    uses, and its empirical adequacy is open. beta gains here its second
    meaning, the scale of the reference distribution; it is not retuned for
    adequacy. The test level alpha is the recognizer's run option, not held
    here.

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
from typing import Callable, Dict, Tuple

from shared.types import Predicate

Position = Tuple[float, float]
PathCost = Callable[[Position, Position], float]


# =============================================================================
# The parameter set (single source of truth — recognizer.py reads these through
# the module, never redefines them). The detour tolerance beta is not here: it
# carries the body's length unit, so the embodiment supplies it (T-A1).
# =============================================================================
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

def logistic_of_excess(excess: float, beta: float) -> float:
    """2 / (1 + exp(beta · excess)): 1 at zero excess, → 0 as the excess
    grows, → 2 for a (moving-target) negative excess."""
    x = beta * excess
    if x > 700.0:                      # exp overflow guard; the value is 0 to double precision
        return 0.0
    return 2.0 / (1.0 + math.exp(x))


PERFECT_FIT_LIKELIHOOD = 1.0    # the logistic at zero excess, for any beta: nothing to charge


def excess_path_likelihood(
    walked: float,
    origin: Position,
    pos: Position,
    target_pos: Position,
    cost: PathCost,
    beta: float,
) -> float:
    """
    Excess-path likelihood of the movement observed since `origin` under an
    action located at `target_pos`: the agent has walked `walked` (odometer
    since the origin) and is now at `pos`; a perfectly efficient walk would
    have cost C(origin, target). `beta` is the embodiment's detour tolerance,
    in the units of the positions. Registered as "excess_path"; applies to any
    action schema with progress_evaluator="excess_path" (currently: move_to).
    """
    return logistic_of_excess(excess_path(walked, origin, pos, target_pos, cost), beta)


def excess_path(
    walked: float,
    origin: Position,
    pos: Position,
    target_pos: Position,
    cost: PathCost,
) -> float:
    """
    The wasted path since `origin` under an action located at `target_pos`:
    walked + C(pos, target) - C(origin, target). The one computation the
    excess-path likelihood and the adequacy test's projected completion delay
    both read (T-D E2: "the excess path from the origin as computed today").
    """
    return walked + cost(pos, target_pos) - cost(origin, target_pos)


# =============================================================================
# Adequacy — the tail of the reference distribution (T-D E5)
# =============================================================================

def tail_probability(x: float, beta: float) -> float:
    """
    S(x) = ln(1 + exp(-beta·x)) / ln 2 for x > 0, and 1 for x <= 0: the tail of
    the reference distribution p(x) = beta·L(x) / (2 ln 2) at x = v·D, the
    projected completion delay in the body's length units. 1 at x = 0,
    decreasing to 0. beta is the excess-path likelihood's own tolerance.
    """
    if x <= 0.0:
        return 1.0
    return math.log1p(math.exp(-beta * x)) / math.log(2.0)


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
}

# The excess each registered evaluator's likelihood is a function of, under the
# same name: what the adequacy test reads as e (T-D E2). Time is not an
# evaluator: it enters adequacy only, never the belief's likelihood (T-D E3).
EXCESS_MEASURES: Dict[str, Callable[[float, Position, Position, Position, PathCost], float]] = {
    "excess_path": excess_path,
}
