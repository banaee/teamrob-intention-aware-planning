"""
analysis/t1b_realization/realize.py  (T1b — measurement scaffolding, NOT the implementation)

A throwaway hold-only realizer over the Segment dicts in captures.json. Nothing
here is imported by shared/; nothing in shared/ changed.

Geometry (closed form). A robot segment placed at start time t has position
P0 + v (tau - t) on [t, t + D]; a human segment has Q0 + w (tau - c) on [c, d].
On the overlap window the relative position is A + B tau with
    A = (P0 - v t) - (Q0 - w c),   B = v - w,
so d^2(tau) is a quadratic; d^2 < s^2 has no real root => no violation, and the
roots bound the violation interval. No sampling anywhere in the realizers; the
sampled functions at the bottom exist only to cross-check the closed form.

Three realizations of the same hold-only policy are computed per row:

  greedy      the design entry's loop, literally (design_decisions.md, "The
              robot can wait"):
                  loop: v = earliest_violation(segment at t); if None break;
                        if v.clear_time beyond horizon: break;
                        hold += clear_time - t; t = clear_time
              with the two properties the task requires: the hold is a
              stationary segment at the segment's start position and is
              checked against the human like any other; and a violation that
              is still open when the human's projection ends is recorded as
              UNRESOLVED (status none:beyond_horizon), never as cleared.
              `clear_time` is the end of the merged violation interval of the
              segment AS PLACED (merged across abutting human segments). When
              that interval is cut by the robot segment's own end while still
              open (the robot would arrive inside s), clear_time is the
              segment end: the loop holds one segment duration and re-checks
              (flagged, counted). Extrapolating the root past the segment end
              would describe motion the robot never makes.
              mode="literal": the same loop but on "clear_time beyond the
              horizon" it BREAKS AND PLACES the segment (the pseudo-code's
              "# no human left") — the design text read without the task's
              rule. Reported alongside, never pooled.
  exact       the same per-segment policy (hold at the segment's start, then
              go), but the EARLIEST feasible start per segment found by a
              fine grid (0.01 tick) instead of the greedy's clear-time jump.
              Feasible = the hold at the start position is clear AND the
              segment is clear over the whole part of it inside the horizon.
              This is the check on the greedy: same policy, minimal hold.
  whole       T1's single shift: hold delta at the trigger position, then run
              the whole projected trajectory unshifted (c_pause_delay.csv),
              smallest delta on a 0.01-tick grid, strict horizon rule.

Strict horizon rule (all three): only [0, T_h] is assessed, T_h = end of the
human's last projected segment. A violation anywhere in [0, T_h] — including
one cut off by T_h — is a violation; nothing after T_h is assessed.
"""

import math
import numpy as np

EPS = 1e-9
GRID = 0.01   # tick; grid for `exact` and `whole` (resolution check in analyze.py)


class Seg:
    __slots__ = ("P0", "P1", "a", "b", "D", "v", "length")

    def __init__(self, d):
        self.P0 = np.array(d["start_pos"], float)
        self.P1 = np.array(d["end_pos"], float)
        self.a = float(d["start_step"])
        self.b = float(d["end_step"])
        self.D = self.b - self.a
        self.length = float(np.linalg.norm(self.P1 - self.P0))
        self.v = (self.P1 - self.P0) / self.D if self.D > EPS else np.zeros(2)


def segs(plan):
    return [Seg(s) for s in plan["segments"]]


def horizon(hsegs):
    return hsegs[-1].b


def pos_at(ss, tau):
    for s in ss:
        if s.a - EPS <= tau <= s.b + EPS:
            return s.P0 + s.v * (min(max(tau, s.a), s.b) - s.a)
    return None


def phase_at(plan, tau):
    """Phase label of the action whose segment contains tau (None past the end)."""
    for i, s in enumerate(plan["segments"]):
        if s["start_step"] - EPS <= tau <= s["end_step"] + EPS:
            return plan["actions"][i]["phase"]
    return None


# =============================================================================
# Closed-form pair test: robot (P0, v, duration D) placed at t vs human segment
# =============================================================================

def pair_violation(P0, v, t, D, h, s):
    """
    Violation interval of the robot segment placed at t against human segment h,
    inside their overlap window. Returns None or (lo, hi, open_at_hi):
    open_at_hi is True when the violation is still going on at hi (the window
    end cut it, not a root).
    """
    lo = max(t, h.a)
    hi = min(t + D, h.b)
    if hi - lo <= EPS:
        return None
    A = (P0 - v * t) - (h.P0 - h.v * h.a)
    B = v - h.v
    bb = float(B @ B)
    ab = float(A @ B)
    aa = float(A @ A)
    if bb < 1e-12:
        if aa < s * s - EPS:
            return (lo, hi, True)
        return None
    disc = ab * ab - bb * (aa - s * s)
    if disc <= 0.0:
        return None
    sq = math.sqrt(disc)
    r1 = (-ab - sq) / bb
    r2 = (-ab + sq) / bb
    vlo = max(r1, lo)
    vhi = min(r2, hi)
    if vhi - vlo <= EPS:
        return None
    return (vlo, vhi, r2 > hi + EPS)


def earliest_violation(P0, v, t, D, hsegs, s):
    """
    Earliest violation of the robot segment placed at t against the whole human
    projection: merged across abutting human segments. Returns None or a dict
    {start, clear, open, at_horizon, at_segment_end}.
    """
    ivs = [iv for iv in (pair_violation(P0, v, t, D, h, s) for h in hsegs) if iv is not None]
    if not ivs:
        return None
    ivs.sort()
    lo, hi, op = ivs[0]
    for (l2, h2, o2) in ivs[1:]:
        if l2 <= hi + 1e-6:
            if h2 > hi:
                hi, op = h2, o2
        else:
            break
    T_h = horizon(hsegs)
    return {
        "start": lo, "clear": hi, "open": op,
        "at_horizon": op and hi >= T_h - 1e-6,
        "at_segment_end": op and hi >= t + D - 1e-6 and hi < T_h - 1e-6,
    }


def hold_violation(P0, t0, t1, hsegs, s):
    """The stationary hold at P0 over [t0, t1], checked like any other segment."""
    if t1 - t0 <= EPS:
        return None
    return earliest_violation(P0, np.zeros(2), t0, t1 - t0, hsegs, s)


# =============================================================================
# 1. greedy — the design entry's loop
# =============================================================================

def realize_greedy(rplan, hplan, s, mode="strict", trace=None, t_max=None):
    """t_max: latest time a hold may end (default: the horizon). Used by the
    held-at-end variant: the human is extended past its horizon, but a hold that
    ends after the ORIGINAL horizon is clearing by outlasting it -> unresolved."""
    rs, hs = segs(rplan), segs(hplan)
    T_h = horizon(hs)
    if t_max is None:
        t_max = T_h
    t = 0.0
    total_hold = 0.0
    holds = []           # (segment index, hold ticks, hold position, hold start, hold end)
    placed = []          # (segment index, placed start, placed end)
    n_iter = 0
    n_segment_end = 0
    first_violation = None
    status = "realized"
    outlasts = False
    fail_seg = None
    for i, r in enumerate(rs):
        while True:
            v = earliest_violation(r.P0, r.v, t, r.D, hs, s)
            if v is None:
                break
            if trace is not None:
                trace.append({"segment": i, "t": t, "start": v["start"], "clear": v["clear"],
                              "P0": r.P0, "v": r.v, "D": r.D})
            if first_violation is None:
                first_violation = {"segment": i, "t": v["start"], "placed_start": t}
            if v["at_horizon"]:
                outlasts = True
                if mode == "strict":
                    status = "none:beyond_horizon"
                    fail_seg = i
                break
            n_iter += 1
            if v["at_segment_end"]:
                n_segment_end += 1
            t_new = v["clear"]
            if t_new > t_max + 1e-9:
                outlasts = True
                if mode == "strict":
                    status = "none:beyond_horizon"
                    fail_seg = i
                break
            hv = hold_violation(r.P0, t, t_new, hs, s)
            if hv is not None:
                status = "none:hold_position_violated"
                fail_seg = i
                holds.append((i, t_new - t, r.P0.tolist(), t, t_new))
                break
            holds.append((i, t_new - t, r.P0.tolist(), t, t_new))
            total_hold += t_new - t
            t = t_new
            if n_iter > 10000:
                raise RuntimeError("greedy did not terminate")
        if status != "realized":
            break
        placed.append((i, t, t + r.D))
        t += r.D
    return {
        "status": status, "delta": total_hold if status == "realized" else None,
        "delta_partial": total_hold, "holds": holds, "placed": placed,
        "n_iter": n_iter, "n_segment_end_truncations": n_segment_end,
        "first_violation": first_violation, "outlasts_horizon": outlasts,
        "fail_segment": fail_seg, "T_h": T_h,
        "end": t if status == "realized" else None,
    }


# =============================================================================
# Vectorised feasibility on a grid of start times (for `exact` and `whole`)
# =============================================================================

def _pair_min_d2(P0, v, tp, D, h):
    """
    For an array of placed starts tp: min over the overlap window of d^2 between
    the robot segment (P0, v, D) placed at tp and human segment h. +inf where
    the two do not overlap in time.
    """
    lo = np.maximum(tp, h.a)
    hi = np.minimum(tp + D, h.b)
    valid = hi - lo > EPS
    A = (P0[None, :] - np.outer(tp, v)) - (h.P0 - h.v * h.a)[None, :]
    B = v - h.v
    bb = float(B @ B)
    if bb < 1e-12:
        d2 = (A * A).sum(1)
    else:
        ts = -(A @ B) / bb
        ts = np.clip(ts, lo, hi)
        R = A + np.outer(ts, B)
        d2 = (R * R).sum(1)
    return np.where(valid, d2, np.inf)


def segment_clear(P0, v, tp, D, hs, s):
    ok = np.ones_like(tp, bool)
    for h in hs:
        ok &= _pair_min_d2(P0, v, tp, D, h) >= s * s - 1e-7
    return ok


def hold_clear(P0, t0, tp, hs, s):
    """Stationary hold at P0 over [t0, tp] for an array tp >= t0."""
    D = tp - t0
    ok = np.ones_like(tp, bool)
    for h in hs:
        lo = np.maximum(t0, h.a)
        hi = np.minimum(tp, h.b)
        valid = hi - lo > EPS
        # human position relative to P0 over [lo, hi]: closest approach of a
        # moving point to a fixed point
        A = (h.P0 - h.v * h.a) - P0
        bb = float(h.v @ h.v)
        if bb < 1e-12:
            d2 = np.full_like(tp, float(A @ A))
        else:
            ts = np.clip(-(A @ h.v) / bb, lo, hi)
            R = A[None, :] + np.outer(ts, h.v)
            d2 = (R * R).sum(1)
        ok &= ~valid | (d2 >= s * s - 1e-7)
    return ok


# =============================================================================
# 2. exact — earliest feasible start per segment on a grid
# =============================================================================

def realize_exact(rplan, hplan, s, grid=GRID, t_max=None):
    rs, hs = segs(rplan), segs(hplan)
    T_h = horizon(hs)
    upper = T_h if t_max is None else min(T_h, t_max)
    t = 0.0
    total_hold = 0.0
    holds, placed = [], []
    status = "realized"
    fail_seg = None
    for i, r in enumerate(rs):
        if t >= T_h - EPS:
            placed.append((i, t, t + r.D))
            t += r.D
            continue
        if t >= upper - EPS:
            tp = np.array([t])          # no hold may end past t_max: the segment as is, or nothing
        else:
            tp = np.arange(t, upper + grid, grid)
            tp[0] = t
        ok = segment_clear(r.P0, r.v, tp, r.D, hs, s) & hold_clear(r.P0, t, tp, hs, s)
        idx = np.flatnonzero(ok)
        if len(idx) == 0:
            status = "none:no_feasible_start"
            fail_seg = i
            break
        t_new = float(tp[idx[0]])
        if t_new - t > EPS:
            holds.append((i, t_new - t, r.P0.tolist(), t, t_new))
            total_hold += t_new - t
        t = t_new
        placed.append((i, t, t + r.D))
        t += r.D
    return {"status": status, "delta": total_hold if status == "realized" else None,
            "holds": holds, "placed": placed, "fail_segment": fail_seg, "T_h": T_h,
            "end": t if status == "realized" else None}


# =============================================================================
# 3. whole — T1's single shift from the trigger position
# =============================================================================

def realize_whole(rplan, hplan, s, grid=GRID, t_max=None):
    rs, hs = segs(rplan), segs(hplan)
    T_h = horizon(hs)
    upper = T_h if t_max is None else min(T_h, t_max)
    deltas = np.arange(0.0, upper + grid, grid)
    ok = hold_clear(rs[0].P0, 0.0, deltas, hs, s)
    for r in rs:
        ok &= segment_clear(r.P0, r.v, r.a + deltas, r.D, hs, s)
    idx = np.flatnonzero(ok)
    if len(idx) == 0:
        return {"status": "none:no_feasible_shift", "delta": None, "T_h": T_h}
    d = float(deltas[idx[0]])
    return {"status": "realized", "delta": d, "T_h": T_h,
            "end": rs[-1].b + d, "shift_past_horizon": d >= T_h - 1e-6}


# =============================================================================
# Realized trajectory and sampled cross-checks
# =============================================================================

def realized_trajectory(rplan, res):
    """Head-to-tail Segment list of the realized plan: holds as stationary segments."""
    rs = segs(rplan)
    out = []
    holds_by_seg = {}
    for (i, dt, P, t0, t1) in res.get("holds", []):
        holds_by_seg.setdefault(i, []).append((t0, t1))
    for (i, t0, t1) in res["placed"]:
        for (h0, h1) in holds_by_seg.get(i, []):
            out.append(Seg({"start_pos": rs[i].P0.tolist(), "end_pos": rs[i].P0.tolist(),
                            "start_step": h0, "end_step": h1}))
        out.append(Seg({"start_pos": rs[i].P0.tolist(), "end_pos": rs[i].P1.tolist(),
                        "start_step": t0, "end_step": t1}))
    return out


def chain_positions(chain, taus):
    """Vectorised position lookup on a head-to-tail chain; NaN outside its span."""
    starts = np.array([c.a for c in chain])
    ends = np.array([c.b for c in chain])
    idx = np.clip(np.searchsorted(starts, taus, side="right") - 1, 0, len(chain) - 1)
    out = np.full((len(taus), 2), np.nan)
    for i, c in enumerate(chain):
        m = idx == i
        if not m.any():
            continue
        tt = np.clip(taus[m], c.a, c.b)
        out[m] = c.P0[None, :] + np.outer(tt - c.a, c.v)
    inside = (taus >= starts[0] - EPS) & (taus <= ends[-1] + EPS)
    out[~inside] = np.nan
    return out


def sampled_min_distance(traj, hs, t_end, dt=0.01):
    """Min sampled distance over [0, t_end] between two head-to-tail chains."""
    taus = np.arange(0.0, t_end + dt / 2, dt)
    pr = chain_positions(traj, taus)
    ph = chain_positions(hs, taus)
    d = np.linalg.norm(pr - ph, axis=1)
    if np.all(np.isnan(d)):
        return (math.inf, None)
    k = int(np.nanargmin(d))
    return (float(d[k]), float(taus[k]))


def sampled_first_violation(P0, v, t, D, hs, s, dt=0.01):
    """Sampled counterpart of earliest_violation(): first sample with d < s."""
    T_h = horizon(hs)
    taus = np.arange(t, min(t + D, T_h) + dt / 2, dt)
    if len(taus) == 0:
        return None
    ph = chain_positions(hs, taus)
    pr = P0[None, :] + np.outer(taus - t, v)
    d = np.linalg.norm(pr - ph, axis=1)
    hit = np.flatnonzero(d < s)
    return float(taus[hit[0]]) if len(hit) else None
