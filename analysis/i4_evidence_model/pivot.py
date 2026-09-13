#!/usr/bin/env python3
"""pivot.py sweep_<tag>.csv — derived tables from a sweep: one grid per metric, beta down, unknown across."""
import csv, sys
from collections import defaultdict
path = sys.argv[1]
rows = list(csv.DictReader(open(path)))
betas = sorted({float(r["beta"]) for r in rows}); us = sorted({float(r["unknown"]) for r in rows})
by = {(float(r["beta"]), float(r["unknown"]), r["condition"]): r for r in rows}
conds = sorted({r["condition"] for r in rows})
def grid(title, cond, metric, fmt=lambda v: v):
    print(f"\n### {title}  [{cond}: {metric}]\n")
    print("| beta \\ u | " + " | ".join(f"{u:g}" for u in us) + " |")
    print("|---|" + "---|" * len(us))
    for b in betas:
        cells = []
        for u in us:
            r = by.get((b, u, cond))
            cells.append(fmt(r[metric]) if r else "·")
        print(f"| {b:g} | " + " | ".join(cells) + " |")
sel = sys.argv[2:] or ["all"]
if "all" in sel or "s40" in sel:
    grid("coffee max in segment 2 (criterion 1: ≥ 0.75)", "s40_on", "coffee_max_seg2")
    grid("deliver_item max in segment 2 (criterion 2: < 0.75)", "s40_on", "deliver_max_seg2")
    grid("item_6 at end of 3a / start→end of 3b (criterion 3: falls)", "s40_on", "item6_3b_start_end")
    grid("max task belief in segment 3 (truth: unknown)", "s40_on", "max_task_seg3")
    grid("ac most_likely ticks in 184–271 (criterion 4: 0)", "s40_on", "ac_most_likely_ticks_184_271")
    grid("belief at 272 (item_6 grasp)", "s40_on", "at_272")
    grid("wrong-θ ticks (task ≠ truth, excluding unknown)", "s40_on", "wrong_theta_task_ticks")
    grid("reveals", "s40_on", "reveals")
if "all" in sel or "s30" in sel:
    grid("s30_on reveals (criterion 5: item_3 pre-grasp; grasp at 39)", "s30_on", "reveals")
    grid("s30_on crossings", "s30_on", "crossings")
    grid("s30_on wrong-θ ticks (task)", "s30_on", "wrong_theta_task_ticks")
if "all" in sel or "s00" in sel:
    grid("s00_on reveals", "s00_on", "reveals")
    grid("s00_on crossings", "s00_on", "crossings")
    grid("s00_on wrong-θ ticks (task)", "s00_on", "wrong_theta_task_ticks")
if "all" in sel or "max" in sel:
    for c in conds:
        grid(f"max confidence (criterion 8)", c, "max_conf")
