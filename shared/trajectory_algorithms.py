"""
shared/trajectory_algorithms.py

PURPOSE:
    Pure, simulator-agnostic functions that operate on Segment/ConflictPoint
    (shared/types.py). Two families, both deliberately pluggable — meta_planner.py
    holds a reference to whichever function it's using, never hardcodes a call:

    1. PATH REALIZATION — how a single action's motion is computed.
       Consumed by MetaPlanner._build_segments().
    2. INTERFERENCE DETECTION — given two agents' Segments, where/how close do
       they get. Consumed by MetaPlanner._detect_interference() today; under
       the Phase 4C wait-decision revision (design_decisions.md, "The robot can
       wait") the consumer becomes realize(), on the projection side, asking a
       narrower question — the EARLIEST VIOLATION of a given min_separation
       for one robot segment placed at a given start time — and holding until
       it clears. min_separation is passed in; nothing here holds policy.

    No classes, no state, no imports from mesa_sim/ or ros_sim/ — same
    mind/body constraint as the rest of shared/.

WHAT'S IMPLEMENTED VS. PLACEHOLDER:
    straight_line_path()       — implemented, current default path realization.
    arrival_point()            — implemented (T9): where a walk stops when the
                                  walker halts a given radius short of its target.
    stationary_segment()       — implemented, for non-movement actions.
    discretized_time_sampling()— implemented, current default interference algorithm.
    closest_point_of_approach()— NOT IMPLEMENTED. Documented analytic approach
                                  below; swap-in replacement for
                                  discretized_time_sampling(), same signature.
                                  Its closed form is what realization's
                                  earliest_violation needs (see its docstring).
    obstacle_aware_path()      — NOT IMPLEMENTED. DESIGN-13 / TODO-09's future
                                  non-linear path realization; swap-in
                                  replacement for straight_line_path(), and the
                                  DETOUR strategy of realization (Phase 4D).

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


def arrival_point(
    start_pos: Tuple[float, float],
    end_pos: Tuple[float, float],
    arrival_radius: float,
) -> Tuple[float, float]:
    """
    Where a straight-line walk from start_pos toward end_pos STOPS when the
    walker halts `arrival_radius` short of its target (T9): the point on the
    segment at that distance from end_pos, or start_pos itself when the walker
    is already within the radius (no motion at all — the executor's completion
    condition already holds). With arrival_radius == 0 this is end_pos.

    `arrival_radius` is in world units and is the caller's (Projector's), who
    got it from the embodiment: nothing here knows what distance a body stops
    at. Pure geometry, no policy.
    """
    if arrival_radius <= 0.0:
        return end_pos          # exactly, not start + 1.0 * delta in floating point
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    distance = (dx * dx + dy * dy) ** 0.5
    if distance <= arrival_radius:
        return start_pos
    frac = (distance - arrival_radius) / distance
    return (start_pos[0] + frac * dx, start_pos[1] + frac * dy)


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

    ROLE UNDER REALIZATION (Phase 4C wait-decision revision): the DETOUR
    strategy — go around the human rather than hold — as opposed to the
    hold-only strategy 4C builds first. Waiting somewhere other than where
    you are is a detour too. Needs a path planner and introduces iteration
    between trajectory and interference (a new path has new violations), which
    is why it stays Phase 4D with the off-the-shelf planner (PRIEST, ROS).
    """
    raise NotImplementedError(
        "trajectory_algorithms.obstacle_aware_path: not yet built — see "
        "roadmap.md DESIGN-13 and TODOS_AND_DEFERRED.md TODO-09. "
        "straight_line_path() is the current path realization for all actions."
    )


# =============================================================================
# INTERFERENCE DETECTION
# =============================================================================

def _speed(segment: Segment) -> float:
    """World units per step along `segment`; 0.0 for a stationary or zero-duration segment."""
    duration = segment.end_step - segment.start_step
    if duration <= 0.0:
        return 0.0
    return _distance(segment.start_pos, segment.end_pos) / duration


def discretized_time_sampling(
    segment_a: Segment,
    segment_b: Segment,
    interval: float = 1.0,
    *,
    max_spatial_step: float,
) -> list:
    """
    Default interference algorithm. Samples both segments at fixed step
    intervals across their overlapping step-time window and reports the
    geometric distance at each sample. Zero-length overlap (segments don't
    share any step-time) returns an empty list — not a conflict.

    interval: sampling spacing in steps (execution ticks). Coarser than 1.0 is
    cheaper but can miss a close pass between samples; finer catches more but
    costs more calls. Not tuned — same "placeholder default" status as
    assumed_speed.
    max_spatial_step: REQUIRED, keyword-only. Upper bound, in world units, on
    how far the faster of the two agents moves between consecutive samples.
    The effective spacing is min(interval, max_spatial_step / max(speed_a,
    speed_b)), with speed read off each Segment itself (distance / duration),
    so a projection built at 20 units per tick is sampled 20 times per tick
    when max_spatial_step is 1. It has no default on purpose: a value in world
    units is a unit-scale assumption (1 cm in Mesa, 1 m in ROS would not be
    the same resolution), and that is a fact about the body. The embodiment
    layer binds it — e.g. functools.partial(discretized_time_sampling,
    max_spatial_step=<from its config>) — and passes the bound callable to
    MetaPlanner as interference_algorithm. Calling this without it raises
    TypeError rather than sampling at an assumed scale.

    Returns List[ConflictPoint], one per sample in the overlap window,
    regardless of how close the sample is — MetaPlanner._detect_interference()
    is where a `distance` threshold turns these into a feasible/infeasible
    decision, not here. This function only measures, it doesn't judge.

    Under realization (design, not yet built) this is the FALLBACK for
    earliest_violation: the first sample below min_separation, not the
    minimum over all of them. It computes more than a hold needs — the
    closed form in closest_point_of_approach() is the intended answer.

    Symmetric in segment_a/segment_b — order doesn't affect the result.
    """
    overlap_start = max(segment_a.start_step, segment_b.start_step)
    overlap_end = min(segment_a.end_step, segment_b.end_step)
    if overlap_start >= overlap_end:
        return []

    max_speed = max(_speed(segment_a), _speed(segment_b))
    if max_speed > 0.0:
        interval = min(interval, max_spatial_step / max_speed)

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

    ROLE UNDER REALIZATION (Phase 4C wait-decision revision; design_decisions.md,
    "The robot can wait"): this is what the closed form was reserved for. The
    question realization asks is not "the minimum over the window" but the
    EARLIEST VIOLATION of a given min_separation for one robot segment placed
    at a given start time, against each time-overlapping human segment. Same
    quadratic: no real root of d²(t) = min_separation² inside the overlap
    window means no violation; the roots give the violation interval and
    hence the earliest clear time, which is where the robot holds until. No
    sampling, no resolution parameter, no world-unit constant in shared/ —
    min_separation is passed in. Whether it lands under this name or as an
    `earliest_violation` beside it is the implementer's; the interface is
    "earliest violation for this segment at this start time".
    """
    raise NotImplementedError(
        "trajectory_algorithms.closest_point_of_approach: not yet built — "
        "see the analytic approach documented in this function's docstring. "
        "discretized_time_sampling() is the current default interference "
        "algorithm."
    )
