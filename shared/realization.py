"""
shared/realization.py

PURPOSE:
    Realization: what a projected trajectory actually is, given the human.
    realize() takes a robot ProjectedPlan and the human's, and computes the
    hold the robot must take so that its plan keeps `min_separation` from the
    human's projected plan. The realized duration — walking plus the hold — is
    the candidate's cost. Conflict becomes cost by construction: a conflicted
    plan costs more because avoiding the human takes longer. No conflict
    weight, no exclusion threshold (design_decisions.md, "The robot can wait";
    the decisions taken at R1 after T1b).

    Hold-only, whole-trajectory minimal shift (R1, TODO-70): ONE hold δ at the
    robot's position at the decision step, then the whole plan shifted by δ.
    δ is the smallest WHOLE-TICK shift ≥ 0 such that the shifted trajectory —
    including the stationary hold at the decision position during the hold —
    has no violation within the assessed window (T3b: the hold is executed as
    whole ticks, so the plan that is checked and costed is the plan that is
    executed; see design_decisions.md, "Realization as built"). A violation
    is a distance: agents are points, and any moment at which they are
    strictly closer than `min_separation` is one — a single instant exactly
    at `min_separation` is not (head-on, same-line and "the human walks past
    the standing robot" conflicts need no special case; they come out
    unrealizable through the hold-position check). Motion is continuous along
    segments; the computation is exact — closed-form shift intervals per
    segment pair, no sampling in time, and the integer δ read off them.

LAYERING (design_decisions.md, "The robot can wait"; one-way, no cycles):

    trajectory_algorithms.py   pure geometry   segments in -> violating shifts out
            |
    realization.py             realize()       "what would this trajectory be, given the human?"
            |
    projection.py              Projector       task + world -> predicted trajectory
            |
    meta_planner.py            MetaPlanner     which trajectory to pick

    This module reads ProjectedPlans and Segments and nothing else: it knows
    nothing of tasks, beliefs, or selection, and holds no simulator constant.
    `min_separation` is passed IN by the caller (MetaPlanner, T4/T10) — the
    single policy value — so no policy enters the geometry below, and this
    module decides nothing about which plan to run. Consumed by MetaPlanner's
    B2 `b2a` (T4); B3 is to consume it at T10.

WHAT THIS MODULE DOES NOT DO:
    - Does NOT choose between candidates (meta_planner.py)
    - Does NOT project (projection.py) — it consumes projections
    - Does NOT assess anything beyond T_h, the end of the human's projection:
      the plan there is neither clear nor blocked (Property 2 as amended at
      R1); what happens there is the execution layer's ("Assumption:
      execution-time avoidance past T_h")
    - Does NOT hold anywhere but where the robot is (a hold elsewhere is a
      detour, Phase 4D), nor partway along a segment (TODO-70, deferred)
    - Does NOT import from mesa_sim/ or ros_sim/
"""

import math
from typing import List, Optional, Tuple

from shared.types import ProjectedPlan, RealizedPlan, Segment
from shared.trajectory_algorithms import (
    first_approach_step,
    shift_violation_interval,
    stationary_segment,
)


# Floating-point slack on step comparisons (merging abutting shift intervals,
# the hold cap). Not a margin: the minimal shift has none by design, and this
# is nine orders of magnitude below a tick.
_EPS = 1e-9


def realize(
    plan: ProjectedPlan,
    human_plan: Optional[ProjectedPlan],
    min_separation: float,
    decision_step: float,
) -> RealizedPlan:
    """
    Realizes `plan` against `human_plan` under the hold-only, whole-trajectory
    minimal shift. Returns a RealizedPlan (shared/types.py) — never None: an
    unrealizable plan is reported as such, with its reason.

    plan:            the robot's projection — the segments of whatever ordering
                     it holds (every entry's segments, in order; not assumed to
                     be one task). Its first segment starts at or after
                     `decision_step`, from where the robot is; the hold is
                     taken there.
    human_plan:      the human's projection, or None when none was admitted.
                     Its segments start at the observation offset (L2), so the
                     steps before that are outside its span and are not
                     assessed; T_h is its last segment's end.
    min_separation:  the clearance the realization must achieve, in world
                     units. The caller's policy value; nothing here decides it.
    decision_step:   the robot's own now, on the projection clock (0.0 for a
                     projection started at the trigger tick).

    THE ASSESSED WINDOW: the steps at which both the realized plan and the
    human's projection exist, i.e. [decision_step, T_h] intersected with the
    human's span and the realized plan's. Nothing past T_h is assessed or
    charged; nothing before the human's span is assessed either (nothing was
    observed of the human there).

    δ: the smallest WHOLE-TICK shift ≥ 0 that is outside every violating
    shift interval (trajectory_algorithms.shift_violation_interval, one per
    robot segment × human segment pair; each is one open interval by
    convexity, exact). The intervals are walked in order of their start: δ
    starts at 0 and, whenever an interval strictly contains it, jumps to the
    first whole tick at or after that interval's end. One pass suffices — δ
    never decreases, so an interval already passed cannot contain a later δ.
    Exact bad-shift intervals rather than a search over δ with a per-δ
    check, because the feasible set in δ is not monotone (a shift can clear
    one crossing and walk into the next): no bisection is valid, and for the
    same reason the whole-tick δ is NOT the fractional minimal shift rounded
    up — rounding up can land in a second interval; the walk continues past
    it. Whole ticks (T3b, decided from the design, not the data): the hold
    reaches the body as STAND microactions, one per tick, so a fractional δ
    could not be executed as computed, and rounding at execution would
    either break the separation (down: the minimal shift has no margin) or
    leave the executed plan unchecked (up: non-monotone). T_r stays
    FRACTIONAL: it is the projection's continuous duration, execution
    quantises per walk (ceil per walk, L2: deliberately not compensated),
    and rounding the total would be a second quantisation that models
    nothing and can only turn an order into a tie. cost = T_r + δ is then
    ONE quantity — the projected duration of the realized trajectory, its
    hold in whole ticks because the hold is executed as ticks — and the
    plain cost a caller compares it with (no projection; all unrealizable)
    must be the same T_r, `projected_duration`, not ProjectedPlan's
    integer-rounded `total_estimated_cost`.

    THE HOLD: stationary at the plan's start position over
    [decision_step, plan start + δ]. It is a position and is checked like any
    segment: the human's projection must not come strictly within
    `min_separation` of it during the hold. Since the hold only grows with δ,
    the first step at which the human comes within the separation of the
    hold position (trajectory_algorithms.first_approach_step) bounds δ from
    above; a smallest clearing δ beyond that bound means NO shift clears, and
    the plan is unrealizable ("hold_position_violated"). The hold may end at
    that step exactly (the human then touches `min_separation`, which is
    not a violation).

    THE HOLD CAP: a hold (δ > 0) may not extend to T_h. If the smallest
    clearing δ satisfies plan start + δ ≥ T_h, the plan is unrealizable
    ("hold_reaches_horizon"): it would clear by outlasting the assessment,
    not by avoiding anything within it. δ = 0 is never a hold and is not
    capped — a plan that starts at or after T_h is realizable and fully
    unassessed.

    THE UNASSESSED SHARE counts the part of the realized plan beyond T_h
    only. The steps before the human projection's span — the observation
    offset, one tick in Mesa (L2) — are unassessed too but not counted: the
    share reports the tail the hold pushes past the horizon (TODO-69), and
    the offset is a property of the observation, the same for every
    candidate at a trigger.

    NO HUMAN PROJECTION (None, or one without segments): realizable, δ = 0,
    cost = T_r, unassessed share 1.0, reason "no_human_projection". The
    caller may treat this exactly as it treats an absent projection today —
    plain projected cost, no hold.

    Raises ValueError for a plan with no segments, or one whose first segment
    starts before `decision_step` (it would describe motion already past).
    """
    robot_segments: List[Segment] = [seg for entry in plan.entries for seg in entry.segments]
    if not robot_segments:
        raise ValueError("realize: the robot plan has no segments")
    plan_start = robot_segments[0].start_step
    plan_end = robot_segments[-1].end_step
    if plan_start < decision_step - _EPS:
        raise ValueError(
            f"realize: the plan starts at step {plan_start}, before the "
            f"decision step {decision_step}"
        )
    hold_position = robot_segments[0].start_pos
    projected_duration = plan_end - plan_start

    human_segments: List[Segment] = (
        [seg for entry in human_plan.entries for seg in entry.segments]
        if human_plan is not None else []
    )
    if not human_segments:
        return RealizedPlan(
            realizable=True,
            delta=0,
            cost=projected_duration,
            projected_duration=projected_duration,
            segments=_realized_segments(robot_segments, hold_position, decision_step, 0),
            hold_position=hold_position,
            hold_start=decision_step,
            horizon=None,
            unassessed_share=1.0,
            reason="no_human_projection",
        )
    horizon = human_segments[-1].end_step

    # --- the smallest shift outside every violating shift interval ----------
    intervals: List[Tuple[float, float]] = []
    for robot_seg in robot_segments:
        for human_seg in human_segments:
            interval = shift_violation_interval(robot_seg, human_seg, min_separation)
            if interval is not None and interval[1] > 0.0:
                intervals.append(interval)
    intervals.sort()
    delta = 0
    for lo, hi in intervals:
        if lo + _EPS < delta < hi - _EPS:
            # Strictly inside a violating interval: the first whole tick at
            # or after its end. Its end itself is clear (the distance touches
            # min_separation there), hence the slack towards "clear".
            delta = math.ceil(hi - _EPS)
        elif lo > delta + _EPS:
            break

    # --- the hold is a position: the human must not pass within the ---------
    # separation of it while the robot stands there
    first_approach: Optional[float] = None
    for human_seg in human_segments:
        first_approach = first_approach_step(hold_position, human_seg, min_separation, decision_step)
        if first_approach is not None:
            break
    if first_approach is not None and plan_start + delta > first_approach + _EPS:
        return _unrealizable(projected_duration, hold_position, decision_step, horizon,
                             "hold_position_violated")

    # --- the hold cap: a hold may not extend to T_h -------------------------
    if delta > 0 and plan_start + delta >= horizon - _EPS:
        return _unrealizable(projected_duration, hold_position, decision_step, horizon,
                             "hold_reaches_horizon")

    realized_end = plan_end + delta
    span = realized_end - decision_step
    beyond = max(0.0, realized_end - horizon)
    unassessed_share = min(1.0, beyond / span) if span > 0.0 else 0.0

    return RealizedPlan(
        realizable=True,
        delta=delta,
        cost=projected_duration + delta,
        projected_duration=projected_duration,
        segments=_realized_segments(robot_segments, hold_position, decision_step, delta),
        hold_position=hold_position,
        hold_start=decision_step,
        horizon=horizon,
        unassessed_share=unassessed_share,
        reason="realized",
    )


def _realized_segments(
    robot_segments: List[Segment],
    hold_position: Tuple[float, float],
    decision_step: float,
    delta: int,
) -> List[Segment]:
    """The hold (when it has positive duration), then every segment shifted by delta."""
    shifted_start = robot_segments[0].start_step + delta
    out: List[Segment] = []
    if shifted_start - decision_step > 0.0:
        out.append(stationary_segment(hold_position, decision_step, shifted_start - decision_step))
    for seg in robot_segments:
        out.append(Segment(
            start_pos=seg.start_pos,
            start_step=seg.start_step + delta,
            end_pos=seg.end_pos,
            end_step=seg.end_step + delta,
        ))
    return out


def _unrealizable(
    projected_duration: float,
    hold_position: Tuple[float, float],
    decision_step: float,
    horizon: float,
    reason: str,
) -> RealizedPlan:
    return RealizedPlan(
        realizable=False,
        delta=None,
        cost=None,
        projected_duration=projected_duration,
        segments=[],
        hold_position=hold_position,
        hold_start=decision_step,
        horizon=horizon,
        unassessed_share=None,
        reason=reason,
    )
