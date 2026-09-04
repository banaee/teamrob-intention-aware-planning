"""
shared/trajectory_algorithms.py

PURPOSE:
    Pure, simulator-agnostic functions that operate on Segment/ConflictPoint
    (shared/types.py). Two families, both deliberately pluggable — meta_planner.py
    holds a reference to whichever function it's using, never hardcodes a call:

    1. PATH REALIZATION — how a single action's motion is computed.
       Consumed by MetaPlanner._build_segments().
    2. INTERFERENCE DETECTION — given two agents' Segments, where/how close do
       they get. Consumed by MetaPlanner._detect_interference().

    No classes, no state, no imports from mesa_sim/ or ros_sim/ — same
    mind/body constraint as the rest of shared/.

WHAT'S IMPLEMENTED VS. PLACEHOLDER:
    straight_line_path()       — implemented, current default path realization.
    stationary_segment()       — implemented, for non-movement actions.
    discretized_time_sampling()— implemented, current default interference algorithm.
    closest_point_of_approach()— NOT IMPLEMENTED. Documented analytic approach
                                  below; swap-in replacement for
                                  discretized_time_sampling(), same signature.
    obstacle_aware_path()      — NOT IMPLEMENTED. DESIGN-13 / TODO-09's future
                                  non-linear path realization; swap-in
                                  replacement for straight_line_path().

    Both placeholders exist so the swap points are visible in code, not just in
    docs — implement when actually needed, not speculatively now.
"""

from typing import Tuple

from shared.types import Segment, ConflictPoint


# =============================================================================
# Internal helpers
# =============================================================================

def _position_at(segment: Segment, step: float) -> Tuple[float, float]:
    """
    Linear-interpolated position of `segment` at `step`. Assumes straight-line,
    constant-speed motion within the segment (matches how every current
    Segment is built — see straight_line_path(), stationary_segment()).
    `step` is clamped to [segment.start_step, segment.end_step] — callers are
    expected to only query within a segment's own span (or an overlap window
    already intersected with it), clamping is just a safety net against
    floating-point edge steps.
    """
    if segment.end_step <= segment.start_step:
        return segment.start_pos
    t = (step - segment.start_step) / (segment.end_step - segment.start_step)
    t = max(0.0, min(1.0, t))
    x = segment.start_pos[0] + t * (segment.end_pos[0] - segment.start_pos[0])
    y = segment.start_pos[1] + t * (segment.end_pos[1] - segment.start_pos[1])
    return (x, y)


def _distance(pos_a: Tuple[float, float], pos_b: Tuple[float, float]) -> float:
    """Euclidean distance between two positions."""
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return (dx * dx + dy * dy) ** 0.5


def _midpoint(pos_a: Tuple[float, float], pos_b: Tuple[float, float]) -> Tuple[float, float]:
    """
    Representative position for a ConflictPoint involving two agents.
    Interference is symmetric (neither agent's position is more "the conflict"
    than the other's) — the midpoint is the least-arbitrary single point to
    report. Not used for any distance math, purely for ConflictPoint.position.
    """
    return ((pos_a[0] + pos_b[0]) / 2.0, (pos_a[1] + pos_b[1]) / 2.0)


# =============================================================================
# PATH REALIZATION
# =============================================================================

def straight_line_path(
    start_pos: Tuple[float, float],
    start_step: float,
    end_pos: Tuple[float, float],
    assumed_speed: float,
) -> Segment:
    """
    Default path realization: straight-line, constant-speed motion from
    start_pos to end_pos. Duration = distance / assumed_speed — same
    assumption MetaPlanner._estimate_duration() and Mesa's current
    steps_toward() already make.

    Called from MetaPlanner._build_segments() for each movement action.
    """
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    distance = (dx * dx + dy * dy) ** 0.5
    duration = distance / assumed_speed
    return Segment(
        start_pos=start_pos,
        start_step=start_step,
        end_pos=end_pos,
        end_step=start_step + duration,
    )


def stationary_segment(
    pos: Tuple[float, float],
    start_step: float,
    duration: float,
) -> Segment:
    """
    Segment for a non-movement action (grasp, place, wait_at) — the agent
    holds one position for `duration` steps. Still valid input to interference
    detection: a human passing close while the robot is stationary mid-pickup
    is a real conflict, not a non-event.

    `duration` is the caller's concern (MetaPlanner._build_segments(), via
    self._knowledge.get_cost() / self._default_action_cost) — this function
    has no knowledge-base access by design, same mind/body boundary as the
    rest of shared/.
    """
    return Segment(
        start_pos=pos,
        start_step=start_step,
        end_pos=pos,
        end_step=start_step + duration,
    )


def obstacle_aware_path(
    start_pos: Tuple[float, float],
    start_step: float,
    end_pos: Tuple[float, float],
    assumed_speed: float,
    # world: "WorldState",
) -> Segment:
    """
    NOT IMPLEMENTED. Future non-linear, static-obstacle-aware path realization
    — DESIGN-13 (roadmap.md, Phase 4D) / TODO-09 (replaces Mesa's straight-line
    steps_toward()). Intended as a drop-in replacement for straight_line_path()
    with the same call shape plus a WorldState for obstacle data; likely
    returns a path that Segment's straight-line start/end can't fully capture,
    so Segment itself may need to grow (e.g. an optional waypoint list) when
    this is actually built — not resolved now, flagging rather than guessing.
    """
    raise NotImplementedError(
        "trajectory_algorithms.obstacle_aware_path: not yet built — see "
        "roadmap.md DESIGN-13 and TODOS_AND_DEFERRED.md TODO-09. "
        "straight_line_path() is the current path realization for all actions."
    )


# =============================================================================
# INTERFERENCE DETECTION
# =============================================================================

def discretized_time_sampling(
    segment_a: Segment,
    segment_b: Segment,
    interval: float = 1.0,
) -> list:
    """
    Default interference algorithm. Samples both segments at fixed step
    intervals across their overlapping step-time window and reports the
    geometric distance at each sample. Zero-length overlap (segments don't
    share any step-time) returns an empty list — not a conflict.

    interval: sampling spacing in steps. Coarser than 1.0 is cheaper but can
    miss a close pass between samples; finer catches more but costs more
    calls. Not tuned — same "placeholder default" status as assumed_speed.

    Returns List[ConflictPoint], one per sample in the overlap window,
    regardless of how close the sample is — MetaPlanner._detect_interference()
    is where a `distance` threshold turns these into a feasible/infeasible
    decision, not here. This function only measures, it doesn't judge.

    Symmetric in segment_a/segment_b — order doesn't affect the result.
    """
    overlap_start = max(segment_a.start_step, segment_b.start_step)
    overlap_end = min(segment_a.end_step, segment_b.end_step)
    if overlap_start >= overlap_end:
        return []

    conflicts = []
    step = overlap_start
    while step < overlap_end:
        pos_a = _position_at(segment_a, step)
        pos_b = _position_at(segment_b, step)
        conflicts.append(ConflictPoint(
            step=step,
            position=_midpoint(pos_a, pos_b),
            distance=_distance(pos_a, pos_b),
        ))
        step += interval

    # Always include the overlap window's exact end point, even if the fixed
    # interval didn't land on it — otherwise a close pass right at the
    # boundary can be missed entirely depending on where sampling started.
    pos_a = _position_at(segment_a, overlap_end)
    pos_b = _position_at(segment_b, overlap_end)
    conflicts.append(ConflictPoint(
        step=overlap_end,
        position=_midpoint(pos_a, pos_b),
        distance=_distance(pos_a, pos_b),
    ))

    return conflicts


def closest_point_of_approach(
    segment_a: Segment,
    segment_b: Segment,
) -> list:
    """
    NOT IMPLEMENTED. Future analytic alternative to discretized_time_sampling()
    — same signature, same List[ConflictPoint] return shape, drop-in
    replacement via MetaPlanner's interference_algorithm constructor param.

    Approach (documented, not yet coded): within the two segments' overlapping
    step-time window, each agent's position is a linear function of step
    (straight-line/constant-speed, same assumption as straight_line_path()).
    The squared distance between the two agents is therefore a quadratic in
    step; its minimum has a closed-form solution (vertex of the parabola).
    That minimum must then be clamped to the actual overlap window, since the
    unconstrained analytic minimum can fall outside it — in that case the
    true closest approach is at whichever window boundary is nearer the
    unconstrained minimum. Returns a single ConflictPoint at that step
    (empty list if the segments don't overlap in step-time at all).

    Exact rather than sampled — no interval/resolution tradeoff — but has
    edge cases discretized_time_sampling() doesn't (near-zero relative
    velocity between the two agents makes the quadratic near-degenerate).
    Left unimplemented deliberately: discretized_time_sampling() is the
    working default until this is worth the edge-case care.
    """
    raise NotImplementedError(
        "trajectory_algorithms.closest_point_of_approach: not yet built — "
        "see the analytic approach documented in this function's docstring. "
        "discretized_time_sampling() is the current default interference "
        "algorithm."
    )
