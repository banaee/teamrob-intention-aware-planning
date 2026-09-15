#!/usr/bin/env python3
"""
analysis/m1_theta_earlier/why.py  (M1 — diagnostic for the report)

Decomposes each admitted trigger's realization outcome into the two quantities
that decide it under R1's whole-trajectory minimal shift:

  hold budget   the latest time a hold at the robot's trigger position may run
                to: the START of the first violation of that STATIONARY hold
                against the human's projection (inf = the human never comes
                within min_separation of where the robot stands). Property 1 —
                a hold is a position, checked like any other segment — makes
                this an upper bound on delta.
  shift needed  the smallest d >= 0 at which every SHIFTED segment is clear,
                ignoring the hold-position rule. The lower bound on delta.

Realizable iff shift needed <= hold budget (and, by R1's cap, delta < T_h).
Also: each candidate's unheld minimum distance to the human's projection and
WHEN it occurs, which says which conflict the hold is being asked to fix.

Usage: python analysis/m1_theta_earlier/why.py [--sep 50]
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis" / "t1b_realization"))
import realize as R   # noqa: E402

GRID = 0.01
SHORT = (lambda k: k.replace(",?kitting_table=kitting_table_0", "").replace("deliver_item(?item=", "").replace(")", ""))


def hold_budget(P, hs, s, T_h):
    """Latest end for a stationary hold at P: start of its first violation, else inf."""
    v = R.earliest_violation(np.asarray(P, float), np.zeros(2), 0.0, T_h, hs, s)
    return np.inf if v is None else v["start"]


def shift_needed(rplan, hs, s, T_h):
    """Smallest d >= 0 clearing every shifted segment, hold-position rule ignored."""
    rs = R.segs(rplan)
    ds = np.arange(0.0, T_h + GRID, GRID)
    ok = np.ones_like(ds, bool)
    for r in rs:
        ok &= R.segment_clear(r.P0, r.v, r.a + ds, r.D, hs, s)
    idx = np.flatnonzero(ok)
    return float(ds[idx[0]]) if len(idx) else None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--sep", type=float, default=50.0)
    a = ap.parse_args()
    caps = json.load(open(Path(__file__).parent / "captures.json"))["conditions"]
    out = [f"min_separation = {a.sep:.0f} cm. Times are ticks from the trigger.", "",
           "| run | step | conf | robot pos | human pos | cand | unheld min dist (when) | shift needed | hold budget | outcome |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for cond in caps:
        for tr in cond["triggers"]:
            hp = tr["human_projection"]
            if hp is None:
                continue
            hs = R.segs(hp); T_h = R.horizon(hs)
            P = tr["agent_positions"]["robot_0"]; H = tr["agent_positions"]["human_0"]
            budget = hold_budget(P, hs, a.sep, T_h)
            for i, c in enumerate(tr["candidates"]):
                rs = R.segs(c["projection"])
                md, mt = R.sampled_min_distance(rs, hs, T_h)
                need = shift_needed(c["projection"], hs, a.sep, T_h)
                if need is None:
                    outcome = "NO — no shift clears"
                elif need > budget + 1e-9:
                    outcome = "NO — hold blocked (human reaches the robot's spot first)"
                elif need >= T_h - 1e-6:
                    outcome = "NO — hold reaches T_h"
                else:
                    outcome = f"realizable, delta {need:.2f}"
                f = (lambda v: v if i == 0 else "")
                out.append(f"| {f(cond['name'])} | {f(tr['step'])} | {tr['confidence']:.3f} "
                           f"| {f(f'({P[0]:.0f}, {P[1]:.0f})')} | {f(f'({H[0]:.0f}, {H[1]:.0f})')} "
                           f"| {SHORT(c['task'])} | {md:.1f} (t+{mt:.1f}) "
                           f"| {'none clears' if need is None else f'{need:.2f}'} "
                           f"| {'inf' if np.isinf(budget) else f'{budget:.2f}'} | {outcome} |")
    txt = "\n".join(out) + "\n"
    open(Path(__file__).parent / "why.md", "w").write(txt)
    print(txt)


if __name__ == "__main__":
    main()
