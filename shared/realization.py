"""
shared/realization.py

PURPOSE:
    Realization: what the segments of a ProjectedPlan actually become, given
    the human.
    realize() takes a robot ProjectedPlan and the human's, and computes the
    holds the robot must take so that its plan keeps `min_separation` from the
    human's projected plan. The realized duration — walking plus the holds — is
    the candidate's cost. Conflict becomes cost by construction: a conflicted
    plan costs more because avoiding the human takes longer. No conflict
    weight, no exclusion threshold (design_decisions.md, "The robot can wait";
    the decisions taken at R1 after T1b).

    Hold-only, whole-trajectory minimal shift (R1, TODO-70), applied PER ENTRY
    (T-B Q2, T-B2c): before each entry ONE hold, taken where the robot then
    is — at the decision position for the first entry, where the previous
    entry ended for a later one — then the whole entry shifted. Entry k's
    CUMULATIVE SHIFT is the smallest WHOLE-TICK shift, not below entry k−1's,
    such that entry k's shifted segments have no violation within the
    assessed window; the HOLD before entry k is the difference of the two
    (docs/glossary.md keeps the two terms apart). Whole ticks (T3b): a hold
    is executed as whole ticks, so the plan that is checked and costed is the
    plan that is executed; see design_decisions.md, "Realization as built".
    With ONE entry this is one hold δ at the decision position and the whole
    plan shifted by δ, exactly as before T-B2c. It is NOT the per-segment
    policy R1 rejected: inside an entry every segment receives the same
    shift, and the only new place for a hold is before an entry's first
    segment. Why per entry and not one common shift: a common shift must lie
    outside the violating intervals of EVERY entry, so a conflict in a later
    entry would delay the earlier ones too, and could be pushed further by an
    earlier entry's interval that the later conflict never needed; per entry,
    each cumulative shift is no larger than the common one and the cost never
    higher (design_decisions.md, "One hold per entry").

    A violation is ROBOT-RESPONSIBLE (F1; design_decisions.md,
    "Robot-responsible separation"): min_separation binds the robot's motion,
    not the joint state. The robot violates at a moment when it is MOVING,
    strictly within `min_separation` of the human, and the distance is not
    strictly increasing — (a) its motion takes the distance from at least
    min_separation to below it, or (b) it moves within min_separation without
    the distance increasing. Standing still is never a violation, whatever
    the human does; moving so that the distance strictly increases never is.
    Consequences: a hold itself — a standing robot, wherever it is taken — is
    never checked and never violated, there is no hold cap, and a clearing
    shift ALWAYS exists for every entry (a
    shift past the last violating interval, at the latest past T_h), so
    realization is TOTAL: every plan has a cost. A standing robot may be in
    the human's way; the human's detour is a team-level cost (TODO-15), not
    priced here. Motion is continuous along segments; the computation is
    exact — closed-form shift intervals per segment pair, no sampling in
    time, and the integer δ read off them.

LAYERING (design_decisions.md, "The robot can wait"; one-way, no cycles):

    trajectory_algorithms.py   pure geometry   segments in -> violating shifts out
            |
    realization.py             realize()       "what would these segments become, given the human?"
            |
    projection.py              Projector       task + world -> a ProjectedPlan's segments
            |
    meta_planner.py            MetaPlanner     which candidate to pick

    This module reads ProjectedPlans and Segments and nothing else: it knows
    nothing of tasks, beliefs, or selection, and holds no simulator constant.
    `min_separation` is passed IN by the caller (MetaPlanner, T4/T10) — the
    single policy value — so no policy enters the geometry below, and this
    module decides nothing about which plan to run. Consumed by MetaPlanner's
    B2 `b2a` (T4) and by B3, which selects on RealizedPlan.cost (T10).

WHAT THIS MODULE DOES NOT DO:
    - Does NOT choose between candidates (meta_planner.py)
    - Does NOT project (projection.py) — it consumes projections
    - Does NOT assess anything beyond T_h, the end of the human's projection:
      the plan there is neither clear nor blocked (Property 2 as amended at
      R1); what happens there is the execution layer's ("Assumption:
      execution-time avoidance past T_h"), which is to apply the same
      robot-responsible rule (TODO-73)
    - Does NOT hold anywhere but where the robot is — at the decision
      position, or where an entry ended (a hold elsewhere is a detour, Phase
      4D) — nor partway along a segment or between two segments of one
      entry (TODO-70, deferred)
    - Does NOT import from mesa_sim/ or ros_sim/
"""

import math
from typing import List, Optional, Tuple

from shared.types import ProjectedPlan, RealizedPlan, Segment
from shared.trajectory_algorithms import (
    shift_violation_interval,
    stationary_segment,
)


# Floating-point slack on step comparisons (merging abutting shift intervals).
# Not a margin: the minimal shift has none by design, and this is nine orders
# of magnitude below a tick.
_EPS = 1e-9


def realize(
    plan: ProjectedPlan,
    human_plan: Optional[ProjectedPlan],
    min_separation: float,
    decision_step: float,
) -> RealizedPlan:
    """
    Realizes `plan` against `human_plan` under the hold-only, whole-trajectory
    minimal shift, one minimal-shift search per entry. Returns a RealizedPlan
    (shared/types.py) — always, with a cost: under robot-responsible
    separation (F1) a clearing shift exists for every entry.

    plan:            the robot's projection — one entry per task of whatever
                     ordering it holds, each entry starting where the previous
                     one ends. Its first segment starts at or after
                     `decision_step`, from where the robot is; the first hold
                     is taken there, a later entry's hold where the entry
                     before it ended.
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

    ONE SEARCH PER ENTRY, in the plan's order. Search k ranges over the
    violating shift intervals of entry k's OWN segments, with the cumulative
    shift of entry k−1 as its lower bound (0 for the first entry); its result
    is the cumulative shift of entry k (RealizedPlan.cumulative_shifts), and
    the hold before entry k is the difference (RealizedPlan.holds). An
    entry's intervals do not depend on the earlier shifts: its positions are
    unchanged and the human's projection is fixed. cost = T_r + the cumulative
    shift of the LAST entry. With one entry there is one search from 0, and
    δ below is both its shift and its hold.

    δ: the smallest WHOLE-TICK shift ≥ 0 that is outside every violating
    shift interval (trajectory_algorithms.shift_violation_interval, one per
    MOVING robot segment × human segment pair — a stationary robot segment
    never violates; each is one open interval by convexity, exact). THE
    MINIMAL-SHIFT SEARCH takes the intervals in order of their start: δ
    starts at 0 and, whenever an interval strictly contains it, jumps to the
    first whole tick at or after that interval's end. One pass suffices — δ
    never decreases, so an interval already passed cannot contain a later δ.
    Exact bad-shift intervals rather than a search over δ with a per-δ
    check, because the feasible set in δ is not monotone (a shift can clear
    one violation and run into the next): no bisection is valid, and for the
    same reason the whole-tick δ is NOT the fractional minimal shift rounded
    up — rounding up can land in a second interval; the search continues past
    it. Whole ticks (T3b, decided from the design, not the data): the hold
    reaches the body as STAND microactions, one per tick, so a fractional δ
    could not be executed as computed, and rounding at execution would
    either break the separation (down: the minimal shift has no margin) or
    leave the executed plan unchecked (up: non-monotone). T_r stays
    FRACTIONAL: it is the projection's continuous duration, execution
    quantises per walk (ceil per walk, L2: deliberately not compensated),
    and rounding the total would be a second quantisation that models
    nothing and can only turn an order into a tie. cost = T_r + δ is then
    ONE quantity — the projected duration of the RealizedPlan's segments, its
    hold in whole ticks because the hold is executed as ticks — and the
    plain cost a caller compares it with (no projection) must be the same
    T_r, `projected_duration`, not ProjectedPlan's integer-rounded
    `total_estimated_cost`.

    THE HOLD: stationary at the plan's start position over
    [decision_step, plan start + δ]; before a later entry, stationary where
    the previous entry ended, from its realized end to the entry's shifted
    start. A standing robot never violates (F1), so
    the hold is never checked and never bounds δ: the human may pass within
    `min_separation` of the standing robot, or through it. THERE IS NO HOLD
    CAP (F1 deleted the T_h cap): a hold may extend to or past T_h, in which
    case the shifted plan lies in the unassessed tail, exactly as any plan
    starting at or after T_h does. Every violating interval is bounded, so
    a clearing δ always exists.

    THE UNASSESSED SHARE counts the part of the realized plan beyond T_h
    only (it reaches 1.0 when the hold pushes the whole plan past T_h). The steps before the human projection's span — the observation
    offset, one tick in Mesa (L2) — are unassessed too but not counted: the
    share reports the tail the hold pushes past the horizon (TODO-69), and
    the offset is a property of the observation, the same for every
    candidate at a trigger.

    NO HUMAN PROJECTION (None, or one without segments): δ = 0, cost = T_r,
    unassessed share 1.0, reason "no_human_projection". The caller may treat
    this exactly as it treats an absent projection today — plain projected
    cost, no hold. The only other reason is "realized".

    Raises ValueError for a plan with no segments, or one whose first segment
    starts before `decision_step` (it would describe motion already past).
    """
    entry_segments: List[List[Segment]] = [list(entry.segments) for entry in plan.entries]
    robot_segments: List[Segment] = [seg for segments in entry_segments for seg in segments]
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
        no_shift = [0] * len(entry_segments)
        return RealizedPlan(
            holds=list(no_shift),
            cumulative_shifts=no_shift,
            cost=projected_duration,
            projected_duration=projected_duration,
            segments=_realized_segments(entry_segments, decision_step, no_shift),
            hold_position=hold_position,
            hold_start=decision_step,
            horizon=None,
            unassessed_share=1.0,
            reason="no_human_projection",
        )
    horizon = human_segments[-1].end_step

    # --- one minimal-shift search PER ENTRY, in the plan's order (T-B Q2) ---
    # Search k: the smallest whole tick >= the cumulative shift of entry k-1
    # (0 for the first entry) outside every violating shift interval of entry
    # k's OWN segments (stationary robot segments return None: a standing
    # robot never violates). An entry's intervals do not depend on the earlier
    # shifts — its positions are unchanged and the human's projection is fixed.
    cumulative_shifts: List[int] = []
    shift = 0
    for segments in entry_segments:
        intervals: List[Tuple[float, float]] = []
        for robot_seg in segments:
            for human_seg in human_segments:
                interval = shift_violation_interval(robot_seg, human_seg, min_separation)
                if interval is not None and interval[1] > 0.0:
                    intervals.append(interval)
        intervals.sort()
        for lo, hi in intervals:
            if lo + _EPS < shift < hi - _EPS:
                # Strictly inside a violating interval: the first whole tick at
                # or after its end. Its end itself is clear (the distance touches
                # min_separation there), hence the slack towards "clear".
                shift = math.ceil(hi - _EPS)
            elif lo > shift + _EPS:
                break
        cumulative_shifts.append(shift)
    holds = [now - before for now, before in zip(cumulative_shifts, [0] + cumulative_shifts[:-1])]

    realized_end = plan_end + cumulative_shifts[-1]
    span = realized_end - decision_step
    beyond = max(0.0, realized_end - horizon)
    unassessed_share = min(1.0, beyond / span) if span > 0.0 else 0.0

    return RealizedPlan(
        holds=holds,
        cumulative_shifts=cumulative_shifts,
        cost=projected_duration + cumulative_shifts[-1],
        projected_duration=projected_duration,
        segments=_realized_segments(entry_segments, decision_step, cumulative_shifts),
        hold_position=hold_position,
        hold_start=decision_step,
        horizon=horizon,
        unassessed_share=unassessed_share,
        reason="realized",
    )


def _realized_segments(
    entry_segments: List[List[Segment]],
    decision_step: float,
    cumulative_shifts: List[int],
) -> List[Segment]:
    """
    Per entry: the stationary stretch of its hold (when it has positive
    duration), taken at the entry's first segment's start — where the previous
    entry ended, or where the robot is at the decision step — then the entry's
    segments at its cumulative shift.
    """
    out: List[Segment] = []
    reached = decision_step  # the step the realized plan has reached so far
    for segments, shift in zip(entry_segments, cumulative_shifts):
        if not segments:
            continue
        shifted_start = segments[0].start_step + shift
        if shifted_start - reached > 0.0:
            out.append(stationary_segment(segments[0].start_pos, reached, shifted_start - reached))
        for seg in segments:
            out.append(Segment(
                start_pos=seg.start_pos,
                start_step=seg.start_step + shift,
                end_pos=seg.end_pos,
                end_step=seg.end_step + shift,
            ))
        reached = out[-1].end_step
    return out
