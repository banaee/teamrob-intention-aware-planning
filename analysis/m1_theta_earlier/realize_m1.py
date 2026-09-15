#!/usr/bin/env python3
"""
analysis/m1_theta_earlier/realize_m1.py  (M1 — exploratory, measurement only)

Runs T1b's throwaway realizer (analysis/t1b_realization/realize.py, imported
unchanged) offline over M1's captures, at min_separation = 50 cm, on the
CURRENT projection (T9's arrival radius in place).

Policy applied is the one R1 decided (design_decisions.md, "The robot can
wait"): the WHOLE-TRAJECTORY MINIMAL SHIFT — realize.realize_whole() — plus
R1's HOLD CAP, which realize.py does not itself enforce: a shift that reaches
T_h is clearing by outlasting the assessment, so it is UNREALIZABLE, not a long
hold. realize_whole() reports that case as shift_past_horizon.

Per admitted trigger and candidate:
    realizable / why not, delta (hold, ticks), realized cost T_r + delta,
    unassessed share (T_r + delta - T_h)+ / (T_r + delta), and the winner by
    realized cost (argmin in pool order, the tie rule B3 uses today).
    T_r is the candidate's own projected duration (its last segment's end),
    T_h the end of the human's projection; both measured from the trigger tick.

This is measurement of what realization WOULD give. Nothing here is the
implementation (T3), and nothing in shared/ is touched or consulted.

Usage: python analysis/m1_theta_earlier/realize_m1.py [--sep 50] [--out DIR]
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis" / "t1b_realization"))

import realize as R          # noqa: E402  (T1b's realizer, unchanged)

SHORT = (lambda k: k.replace(",?kitting_table=kitting_table_0", "")
                    .replace("deliver_item(?item=", "").replace(")", ""))


def realize_candidate(cand, hplan, s):
    """R1's policy: whole-trajectory minimal shift, with the hold cap applied."""
    rplan = cand["projection"]
    T_r = rplan["segments"][-1]["end_step"]
    T_h = R.horizon(R.segs(hplan))
    res = R.realize_whole(rplan, hplan, s)
    out = {"candidate": SHORT(cand["task"]), "is_current_task": cand["is_current_task"],
           "T_r": T_r, "T_h": T_h, "cost_logged": cand["cost"],
           "logged_feasible": cand.get("logged_feasible"),
           "logged_min_dist": cand.get("logged_min_dist")}
    if res["status"] != "realized":
        out.update({"realizable": False, "why": res["status"], "delta": None,
                    "realized_cost": None, "unassessed": None})
        return out
    if res.get("shift_past_horizon"):
        out.update({"realizable": False, "why": "none:hold_reaches_horizon",
                    "delta": res["delta"], "realized_cost": None, "unassessed": None})
        return out
    d = res["delta"]
    cost = T_r + d
    out.update({"realizable": True, "why": None, "delta": d, "realized_cost": cost,
                "unassessed": max(0.0, cost - T_h) / cost if cost > 0 else 0.0})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sep", type=float, default=50.0)
    ap.add_argument("--out", default=str(Path(__file__).parent))
    args = ap.parse_args()
    out_dir = Path(args.out)
    caps = json.load(open(out_dir / "captures.json"))["conditions"]

    rows = []
    for cond in caps:
        for tr in cond["triggers"]:
            if tr["human_projection"] is None:
                continue                      # not admitted: realization is not called (by design)
            cands = [realize_candidate(c, tr["human_projection"], args.sep)
                     for c in tr["candidates"]]
            ok = [c for c in cands if c["realizable"]]
            if ok:
                win = min(ok, key=lambda c: c["realized_cost"])["candidate"]
                fallback = False
            else:                              # R1: all_unrealizable -> plain projected cost
                win = min(cands, key=lambda c: c["T_r"])["candidate"]
                fallback = True
            rows.append({
                "condition": cond["name"], "prior": cond["assignment_prior"],
                "theta": cond["theta"], "step": tr["step"], "trigger": tr["trigger"],
                "confidence": tr["confidence"],
                "hypothesis": SHORT(tr["most_likely"]),
                "human_actual": SHORT(tr["human_actual_task"]) if tr["human_actual_task"] else None,
                "hyp_matches_actual": tr["most_likely"] == tr["human_actual_task"],
                "robot_pos": tr["agent_positions"]["robot_0"],
                "human_pos": tr["agent_positions"]["human_0"],
                "robot_holding": tr["robot_holding"],
                "logged_winner": SHORT(tr["winner"]) if tr["winner"] else None,
                "realized_winner": win, "all_unrealizable": fallback,
                "candidates": cands,
            })

    with open(out_dir / "realization.json", "w") as f:
        json.dump({"min_separation": args.sep, "rows": rows}, f, indent=1)

    # ---- markdown table ----------------------------------------------------
    def fmt(x, nd=2):
        return "–" if x is None else f"{x:.{nd}f}"

    L = [f"Realization at min_separation = {args.sep:.0f} cm, whole-trajectory minimal shift with",
         "R1's hold cap. Admitted triggers only (no projection = realization is not called).",
         "T_r, T_h, delta and realized cost in ticks, measured from the trigger tick.", "",
         "| run | step | trigger | conf | hypothesis | cand | cur? | T_r | T_h | realizable | delta | realized cost | unassessed | logged win | realized win |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        for i, c in enumerate(r["candidates"]):
            first = (lambda v: v if i == 0 else "")
            status = "yes" if c["realizable"] else c["why"].replace("none:", "NO — ")
            win = r["realized_winner"] + (" (all unrealizable → plain cost)"
                                          if r["all_unrealizable"] else "")
            L.append(
                f"| {first(r['condition'])} | {first(r['step'])} | {first(r['trigger'])} "
                f"| {r['confidence']:.3f} | {first(r['hypothesis'])} | {c['candidate']} "
                f"| {'yes' if c['is_current_task'] else ''} "
                f"| {c['T_r']:.2f} | {c['T_h']:.2f} | {status} "
                f"| {fmt(c['delta'])} | {fmt(c['realized_cost'])} | {fmt(c['unassessed'])} "
                f"| {first(r['logged_winner'])} | {first(win)} |")
    open(out_dir / "realization.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
