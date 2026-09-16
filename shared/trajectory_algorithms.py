"""
shared/trajectory_algorithms.py

PURPOSE:
    Pure, simulator-agnostic functions that operate on Segment/ConflictPoint
    (shared/types.py). Two families, both deliberately pluggable — meta_planner.py
    holds a reference to whichever function it's using, never hardcodes a call:

    1. PATH REALIZATION — how a single action's motion is computed.
       Consumed by MetaPlanner._build_segments().
    2. INTERFERENCE DETECTION — given two agents' Segments, where/how close do
       they get. The batch sampler's consumer, MetaPlanner._detect_interference(),
       was removed at T10; under the Phase 4C wait-decision revision
       (design_decisions.md, "The robot can wait") the consumer is realize()
       (shared/realization.py, T3), which asks
       a different question — for which SHIFTS of a robot segment is there a
       violation of a given min_separation against a human segment
       (shift_violation_interval), and when does the human first come within
       it of the robot's standing position (first_approach_step) — and takes
       the smallest shift that clears. min_separation is passed in; nothing
       here holds policy.

    No classes, no state, no imports from mesa_sim/ or ros_sim/ — same
    mind/body constraint as the rest of shared/.

WHAT'S IMPLEMENTED VS. PLACEHOLDER:
    straight_line_path()       — implemented, current default path realization.
    arrival_point()            — implemented (T9): where a walk stops when the
                                  walker halts a given radius short of its target.
    stationary_segment()       — implemented, for non-movement actions.
    discretized_time_sampling()— implemented, current default interference algorithm.
    shift_violation_interval() — implemented (T3): the set of SHIFTS of one robot
                                  segment that violate a separation against one
                                  human segment, closed form. What realization
                                  (shared/realization.py) is built on.
    first_approach_step()      — implemented (T3): when a moving human segment
                                  first comes within a separation of a fixed
                                  point — the hold-position check.
    closest_point_of_approach()— NOT IMPLEMENTED. Documented analytic approach
                                  below; swap-in replacement for
                                  discretized_time_sampling(), same signature.
                                  The role its closed form was reserved for is
                                  taken by shift_violation_interval().
    obstacle_aware_path()      — NOT IMPLEMENTED. DESIGN-13 / TODO-09's future
                                  non-linear path realization; swap-in
                                  replacement for straight_line_path(), and the
                                  DETOUR strategy of realization (Phase 4D).

    Both placeholders exist so the swap points are visible in code, not just in
    docs — implement when actually needed, not speculatively now.
"""

from typing import Optional, Tuple

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
    regardless of how close the sample is. This function only measures, it
    doesn't judge; the caller that thresholded `distance`
    (MetaPlanner._detect_interference()) was removed at T10, and nothing in
    the run path consumes this sampler now.

    Under realization this is at most a FALLBACK for the closed-form
    shift_violation_interval below: the first sample below min_separation,
    not the minimum over all of them. It computes more than a hold needs.

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


def _roots(a2: float, a1: float, a0: float) -> list:
    """
    Real roots of a2 t² + a1 t + a0 = 0, ascending. a2 == 0 returns [] — every
    caller's a2 is a squared speed, and a zero speed makes a1 zero as well, so
    the polynomial is then constant and has no isolated root. Evaluated in
    the numerically stable form (no cancellation between -a1 and the
    discriminant's root).
    """
    if a2 <= 0.0:
        return []
    disc = a1 * a1 - 4.0 * a2 * a0
    if disc < 0.0:
        return []
    sq = disc ** 0.5
    q = -0.5 * (a1 + sq) if a1 >= 0.0 else -0.5 * (a1 - sq)
    if q == 0.0:
        return [0.0, 0.0]
    r1, r2 = q / a2, a0 / q
    return [r1, r2] if r1 <= r2 else [r2, r1]


def shift_violation_interval(
    robot_segment: Segment,
    human_segment: Segment,
    min_separation: float,
) -> Optional[Tuple[float, float]]:
    """
    The shifts d for which `robot_segment`, delayed by d — the same path,
    occupying [start_step + d, end_step + d] — comes within `min_separation` of
    `human_segment` at some moment both exist. Closed form, exact: no sampling
    in time and none in d.

    Returns (lo, hi), the open interval of violating shifts (a violation is a
    STRICT inequality, distance < min_separation, so the endpoints themselves
    are clear: the distance touches min_separation there), or None when no
    shift violates. Either segment of zero duration contributes nothing — its
    instant is the boundary of its neighbours, which are checked.

    Geometry. With u the robot's time into its segment (0 ≤ u ≤ L) and d the
    shift, both agents move at constant velocity, so the relative position is
    affine in (u, d):
        R − Q  =  C + B u − w d,    C = P0 − Q0 − w (a − c),  B = v − w
    (P0, v: the robot segment's start and velocity; Q0, w: the human's; a, c:
    their start steps). The moments both exist are a parallelogram in (u, d):
    0 ≤ u ≤ L and c − a ≤ u + d ≤ d_h − a. The violating set |R − Q|² < s² is
    the preimage of an open disc under an affine map, hence convex (an ellipse
    interior, or a strip when the map is rank-deficient: parallel or equal
    velocities, a stationary agent). Its intersection with the parallelogram
    is convex, so its projection onto the d axis is ONE interval, whose
    endpoints are the extreme d over the closure of that intersection. Those
    extremes lie at one of: the ellipse's own d-extrema (when inside the
    parallelogram); a crossing of the ellipse boundary with a parallelogram
    edge; a parallelogram vertex inside the disc. All are enumerated; the
    interval is their d-range. Empty enumeration, or a range of zero width
    (a tangency), means no shift violates.

    `min_separation` is the caller's; nothing here decides what distance is
    unsafe. Tolerances below are floating-point slack on the enumeration
    (1e-9 relative), not a safety margin — the minimal shift has none by
    design (design_decisions.md, "The robot can wait").
    """
    a, b = robot_segment.start_step, robot_segment.end_step
    c, d_h = human_segment.start_step, human_segment.end_step
    L = b - a
    Dh = d_h - c
    if L <= 0.0 or Dh <= 0.0:
        return None

    P0, P1 = robot_segment.start_pos, robot_segment.end_pos
    Q0, Q1 = human_segment.start_pos, human_segment.end_pos
    vx, vy = (P1[0] - P0[0]) / L, (P1[1] - P0[1]) / L
    wx, wy = (Q1[0] - Q0[0]) / Dh, (Q1[1] - Q0[1]) / Dh
    Cx = P0[0] - Q0[0] - wx * (a - c)
    Cy = P0[1] - Q0[1] - wy * (a - c)
    Bx, By = vx - wx, vy - wy
    k1, k2 = c - a, d_h - a
    s2 = min_separation * min_separation

    tol_q = 1e-9 * max(s2, 1.0)                 # on squared distance
    tol_t = 1e-9 * max(L, Dh, 1.0)              # on u and d
    shifts = []

    def q(u: float, d: float) -> float:
        x = Cx + Bx * u - wx * d
        y = Cy + By * u - wy * d
        return x * x + y * y

    # Parallelogram vertices inside the disc.
    for u, d in ((0.0, k1), (0.0, k2), (L, k1 - L), (L, k2 - L)):
        if q(u, d) <= s2 + tol_q:
            shifts.append(d)

    # Edges u = 0 and u = L: |(C + B u) − w d|² = s², a quadratic in d.
    ww = wx * wx + wy * wy
    for u in (0.0, L):
        ex, ey = Cx + Bx * u, Cy + By * u
        for r in _roots(ww, -2.0 * (ex * wx + ey * wy), ex * ex + ey * ey - s2):
            if k1 - u - tol_t <= r <= k2 - u + tol_t:
                shifts.append(r)

    # Edges u + d = k (the human segment's start and end): with d = k − u,
    # R − Q = (C − w k) + v u, a quadratic in u.
    vv = vx * vx + vy * vy
    for k in (k1, k2):
        ex, ey = Cx - wx * k, Cy - wy * k
        for r in _roots(vv, 2.0 * (ex * vx + ey * vy), ex * ex + ey * ey - s2):
            if -tol_t <= r <= L + tol_t:
                shifts.append(k - r)

    # The ellipse's own d-extrema, when the affine map (u, d) -> R − Q has full
    # rank: M = [[Bx, -wx], [By, -wy]]. d = l · (x − C) over the circle
    # |x| = s, with l the second row of M⁻¹; extreme at x = ± s l / |l|.
    det = By * wx - Bx * wy
    if abs(det) > 1e-12 * (Bx * Bx + By * By + ww):
        lx, ly = -By / det, Bx / det
        ln = (lx * lx + ly * ly) ** 0.5
        for sign in (1.0, -1.0):
            x = sign * min_separation * lx / ln - Cx
            y = sign * min_separation * ly / ln - Cy
            d = lx * x + ly * y
            u = (-wy * x + wx * y) / det
            if -tol_t <= u <= L + tol_t and k1 - tol_t <= u + d <= k2 + tol_t:
                shifts.append(d)

    if not shifts:
        return None
    lo, hi = min(shifts), max(shifts)
    if hi - lo <= tol_t:
        return None
    return (lo, hi)


def first_approach_step(
    pos: Tuple[float, float],
    human_segment: Segment,
    min_separation: float,
    from_step: float,
) -> Optional[float]:
    """
    The first step, at or after `from_step` and within `human_segment`'s span,
    at which the human is STRICTLY within `min_separation` of the fixed point
    `pos`; None if it never is on this segment. Closed form: the squared
    distance of a constant-velocity point to a fixed one is a quadratic in
    step, and the first violation is either the window's start (already
    inside) or the quadratic's smaller root.

    This is the hold-position check of realization: a hold is a position, and
    the moment the human first comes within the separation of it bounds how
    long the robot may stand there. A zero-duration segment contributes
    nothing (its instant belongs to its neighbours).
    """
    c, d_h = human_segment.start_step, human_segment.end_step
    Dh = d_h - c
    lo, hi = max(c, from_step), d_h
    if Dh <= 0.0 or hi - lo <= 0.0:
        return None
    Q0, Q1 = human_segment.start_pos, human_segment.end_pos
    wx, wy = (Q1[0] - Q0[0]) / Dh, (Q1[1] - Q0[1]) / Dh
    # Q(t) − pos = A + w t
    Ax = Q0[0] - pos[0] - wx * c
    Ay = Q0[1] - pos[1] - wy * c
    s2 = min_separation * min_separation
    tol_q = 1e-9 * max(s2, 1.0)
    tol_t = 1e-9 * max(Dh, 1.0)

    x, y = Ax + wx * lo, Ay + wy * lo
    if x * x + y * y < s2 - tol_q:
        return lo
    roots = _roots(wx * wx + wy * wy, 2.0 * (Ax * wx + Ay * wy), Ax * Ax + Ay * Ay - s2)
    if not roots:
        return None
    r1, r2 = roots
    # The window starts outside the disc, so a violation inside it begins at r1
    # (r2 ≤ lo means the approach is already over).
    if r2 - r1 <= tol_t or r1 < lo - tol_t or r1 >= hi - tol_t:
        return None
    return max(r1, lo)


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
