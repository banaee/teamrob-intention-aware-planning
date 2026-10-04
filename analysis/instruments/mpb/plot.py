#!/usr/bin/env python3
"""
plot.py <scenario> <dir> — the meta-planner test-bed's figure: over the comparison horizon, (top) the gate's outcome per
tick with the leader's changes, the expected decisions (thin lines, prior on only) and the actual ones (marks, by
trigger); (bottom) the robot–human distance per tick with min_separation, and the holds the decisions sent (bars from
the decision tick for the hold's length).
"""
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

GATES = ["clears", "none(below_theta)", "none(leader_no_observation)", "none(leader_inadequate)",
         "none(leader_unwarranted)", "none(leader_outranked)"]
MARK = {"no_current_task": ("s", "tab:gray"), "recognition_changed": ("o", "tab:blue"),
        "projection_expired": ("^", "tab:orange")}

if __name__ == "__main__":
    sid, d = sys.argv[1], Path(sys.argv[2])
    obs = json.load(open(d / "observed.json"))
    H = obs["horizon"]
    ticks = [t for t in json.load(open(d / "actual_ticks.json")) if t["tick"] < H]
    agents = [a for a in json.load(open(d / "robot.json")) if a["tick"] < H]
    act = [x for x in json.load(open(d / "actual_decisions.json")) if x["tick"] < H]
    sel = {s["tick"]: s for s in json.load(open(d / "selection.json"))}
    exp = [x for x in json.load(open(d / "expected_decisions.json")) if x["tick"] < H] \
        if (d / "expected_decisions.json").exists() else []
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True, gridspec_kw=dict(height_ratios=[1, 1]))
    a1.scatter([t["tick"] for t in ticks], [GATES.index(t["gate"]) for t in ticks], s=4, c="k")
    a1.set_yticks(range(len(GATES)), GATES, fontsize=7)
    for x in exp:
        a1.axvline(x["tick"], color="tab:green", lw=0.6, alpha=0.6)
    for x in act:
        m, c = MARK[x["trigger"]]
        a1.scatter([x["tick"]], [GATES.index(x["gate"])], marker=m, s=40, facecolors="none", edgecolors=c)
    changes = [t for p, t in zip(ticks[:-1], ticks[1:]) if t["leader"] != p["leader"]]
    for t in changes:
        a1.annotate((t["leader"] or "none").split("(")[0] + "(" + (t["leader"] or "").split("=")[-1],
                    (t["tick"], len(GATES) - 0.6), fontsize=6, rotation=45)
    a1.set_title(f"{sid} ({obs['strategy']}, prior {'on' if obs['prior'] else 'off'}): gate per tick; decisions "
                 "(expected: green lines; actual: ■ no_current_task, ● recognition_changed, ▲ projection_expired)",
                 fontsize=8)
    dist = [math.dist(a["robot"], a["human"]) for a in agents]
    a2.plot([a["tick"] for a in agents], dist, lw=0.8)
    a2.axhline(50, color="r", lw=0.6, ls="--")
    for t, s in sel.items():
        if s["hold"] and t < H:
            a2.barh(0, s["hold"], left=t, height=15, color="tab:orange", alpha=0.6)
    a2.set_ylabel("robot–human distance (cm)", fontsize=8)
    a2.set_xlabel("tick")
    a2.set_ylim(bottom=0)
    fig.tight_layout()
    fig.savefig(d / "figure.png", dpi=110)
