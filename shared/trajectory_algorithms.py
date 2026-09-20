"""
shared/trajectory_algorithms.py

PURPOSE:
    Pure, simulator-agnostic functions that operate on Segment
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
       (shift_violation_interval; robot-responsible since F1: a standing
       robot never violates, a moving one must not be within min_separation
       without the distance increasing) — and runs the minimal-shift search
       over the intervals this module returns, for the smallest whole-tick
       shift that clears. min_separation is passed in; nothing here holds
       policy.

    No classes, no state, no imports from mesa_sim/ or ros_sim/ — same
    mind/body constraint as the rest of shared/.

WHAT'S IMPLEMENTED VS. PLACEHOLDER:
    straight_line_path()       — implemented, current default path realization.
    arrival_point()            — implemented (T9): where a walk stops when the
                                  walker halts a given radius short of its target.
    stationary_segment()       — implemented, for non-movement actions.
    shift_violation_interval() — implemented (T3, rewritten F1 for robot-
                                  responsible separation): the set of SHIFTS of
                                  one robot segment that violate a separation
                                  against one human segment, closed form. What
                                  realization (shared/realization.py) is built on.
    (first_approach_step()     — the hold-position check of T3; REMOVED at F1:
                                  a standing robot never violates.)
    obstacle_aware_path()      — NOT IMPLEMENTED. DESIGN-13 / TODO-09's future
                                  non-linear path realization; swap-in
                                  replacement for straight_line_path(), and the
                                  DETOUR strategy of realization (Phase 4D).

    (discretized_time_sampling() and closest_point_of_approach() — the batch
                                  interference sampler the pre-T10 B3 used and
                                  its unbuilt analytic alternative; REMOVED with
                                  ConflictPoint / InterferenceAssessment when
                                  nothing consumed them, TODO-83.
                                  shift_violation_interval() took the closed
                                  form's role.)

    The placeholder exists so the swap point is visible in code, not just in
    docs — implement when actually needed, not speculatively now.
"""

from typing import Optional, Tuple

from shared.types import Segment


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
    occupying [start_step + d, end_step + d] — VIOLATES robot-responsible
    separation against `human_segment` at some moment both exist. Closed
    form, exact: no sampling in time and none in d.

    THE VIOLATION (F1; design_decisions.md, "Robot-responsible separation"):
    min_separation binds the robot's MOTION, not the joint state. The robot
    violates at a moment when it is moving, the distance to the human is
    strictly below `min_separation`, and the distance is not strictly
    increasing — this covers both (a) the robot's motion taking the distance
    from at least min_separation to below it (the instant after the
    crossing) and (b) the robot moving while within min_separation without
    the distance increasing. Standing still is never a violation, whatever
    the human does; moving so that the distance strictly increases is never
    a violation. A robot segment of zero velocity (a hold, a grasp, a latency)
    therefore contributes nothing and returns None at once.

    Returns (lo, hi), the open interval of violating shifts (the endpoints
    are the moments the violating set is touched, not entered: clear), or
    None when no shift violates. Either segment of zero duration contributes
    nothing — its instant is the boundary of its neighbours, which are checked.

    Geometry. With u the robot's time into its segment (0 ≤ u ≤ L) and d the
    shift, both agents move at constant velocity, so the relative position is
    affine in (u, d):
        X = R − Q  =  C + B u − w d,    C = P0 − Q0 − w (a − c),  B = v − w
    (P0, v: the robot segment's start and velocity; Q0, w: the human's; a, c:
    their start steps). The moments both exist are the parallelogram P:
    0 ≤ u ≤ L and c − a ≤ u + d ≤ d_h − a. "Within min_separation" is the
    open set E: |X|² < s², the preimage of a disc under an affine map, hence
    convex (an ellipse interior, or a strip when the map is rank-deficient).
    "Not strictly increasing" is d|X|²/du = 2 X · B ≤ 0, a CLOSED HALF-PLANE H
    in (u, d) — linear, since X is affine — and the whole plane when B = 0
    (equal velocities: the distance is constant, so a robot moving within
    min_separation violates throughout). The violating set is E ∩ H ∩ P: an
    intersection of convex sets, so convex, so its projection onto the d
    axis is ONE interval, whose endpoints are the extreme d over its closure.
    Those extremes lie at one of: a vertex of the convex polygon H ∩ P inside
    the disc; a crossing of the ellipse boundary with an edge of H ∩ P; the
    ellipse's own d-extrema when inside H ∩ P. H ∩ P is built by clipping the
    parallelogram against the half-plane (at most five vertices); every edge
    is a straight segment along which |X|² is a quadratic, so each crossing is
    a root. All are enumerated; the interval is their d-range. Empty
    enumeration, or a range of zero width (a tangency), means no shift
    violates.

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
    if vx == 0.0 and vy == 0.0:
        return None  # a standing robot never violates
    wx, wy = (Q1[0] - Q0[0]) / Dh, (Q1[1] - Q0[1]) / Dh
    Cx = P0[0] - Q0[0] - wx * (a - c)
    Cy = P0[1] - Q0[1] - wy * (a - c)
    Bx, By = vx - wx, vy - wy
    k1, k2 = c - a, d_h - a
    s2 = min_separation * min_separation

    tol_q = 1e-9 * max(s2, 1.0)                 # on squared distance
    tol_t = 1e-9 * max(L, Dh, 1.0)              # on u and d

    def X(u: float, d: float) -> Tuple[float, float]:
        return (Cx + Bx * u - wx * d, Cy + By * u - wy * d)

    def q(u: float, d: float) -> float:
        x, y = X(u, d)
        return x * x + y * y

    # The half-plane H: g(u, d) = X · B ≤ 0, linear in (u, d).
    BB = Bx * Bx + By * By
    gC, gU, gD = Cx * Bx + Cy * By, BB, -(wx * Bx + wy * By)
    tol_g = 1e-9 * max(1.0, abs(gC), gU * L, abs(gD) * max(abs(k1), abs(k2), 1.0))

    def g(u: float, d: float) -> float:
        return gC + gU * u + gD * d

    # The parallelogram P, vertices in cyclic order, clipped against H.
    poly = [(0.0, k1), (0.0, k2), (L, k2 - L), (L, k1 - L)]
    if BB > 0.0:
        clipped = []
        n = len(poly)
        for i in range(n):
            A, Bv = poly[i], poly[(i + 1) % n]
            gA, gB = g(*A), g(*Bv)
            inA, inB = gA <= tol_g, gB <= tol_g
            if inA:
                clipped.append(A)
            if inA != inB:
                t = gA / (gA - gB)
                clipped.append((A[0] + t * (Bv[0] - A[0]), A[1] + t * (Bv[1] - A[1])))
        poly = clipped
    if not poly:
        return None

    shifts = []

    # Vertices of H ∩ P inside the disc.
    for u, d in poly:
        if q(u, d) <= s2 + tol_q:
            shifts.append(d)

    # Edges of H ∩ P: along A + τ (B − A), |X|² is a quadratic in τ.
    n = len(poly)
    for i in range(n):
        (u0, d0), (u1, d1) = poly[i], poly[(i + 1) % n]
        x0, y0 = X(u0, d0)
        x1, y1 = X(u1, d1)
        ex, ey = x1 - x0, y1 - y0
        for r in _roots(ex * ex + ey * ey, 2.0 * (x0 * ex + y0 * ey), x0 * x0 + y0 * y0 - s2):
            if -tol_t <= r <= 1.0 + tol_t:
                shifts.append(d0 + r * (d1 - d0))

    # The ellipse's own d-extrema, when the affine map (u, d) -> X has full
    # rank: M = [[Bx, -wx], [By, -wy]]. d = l · (x − C) over the circle
    # |x| = s, with l the second row of M⁻¹; extreme at x = ± s l / |l|.
    ww = wx * wx + wy * wy
    det = By * wx - Bx * wy
    if abs(det) > 1e-12 * (BB + ww):
        lx, ly = -By / det, Bx / det
        ln = (lx * lx + ly * ly) ** 0.5
        for sign in (1.0, -1.0):
            x = sign * min_separation * lx / ln - Cx
            y = sign * min_separation * ly / ln - Cy
            d = lx * x + ly * y
            u = (-wy * x + wx * y) / det
            if (-tol_t <= u <= L + tol_t and k1 - tol_t <= u + d <= k2 + tol_t
                    and g(u, d) <= tol_g):
                shifts.append(d)

    if not shifts:
        return None
    lo, hi = min(shifts), max(shifts)
    if hi - lo <= tol_t:
        return None
    return (lo, hi)
