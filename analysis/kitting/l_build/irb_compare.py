#!/usr/bin/env python3
"""
The IRB's sixteen scenarios, L-build against the IRB at ec155f3 ("TB" in the code and its table; the actual.csv
committed at ec155f3, before L-build): per
scenario the first tick on which the recognizer's public output differs (most_likely, confidence, finding, lifecycle,
or any live hypothesis's belief, S or adequacy), the number of such ticks, the exhausted and unexplained tick counts
before and after, and the ticks at which the tracked hypotheses first reach θ in each contiguous stretch after the
first difference. Run from the repo root: ~/python-envs/ir-nomesa-env/bin/python analysis/l_build/irb_compare.py
"""
import csv, io, subprocess
from pathlib import Path

THETA, TB = 0.75, "ec155f3"
SCEN = [f"scenario_s08_0{i}" for i in range(1, 5)] + [f"scenario_s09_{i:02d}" for i in range(1, 13)]


def load(text):
    by = {}
    for r in csv.DictReader(io.StringIO(text)):
        t = int(r["tick"])
        if t >= 0:
            by.setdefault(t, {})[r["key"]] = r
    return by


def sig(rows):
    r0 = next(iter(rows.values()))
    return (r0["most_likely"], r0["confidence"], r0["finding"], r0["lifecycle"],
            tuple(sorted((k, r["belief"], r["S"], r["adequacy"]) for k, r in rows.items() if k)))


def count(by, pred):
    return sum(1 for t in by if pred(next(iter(by[t].values()))))


def theta_ticks(by):
    """(key, first tick >= θ) per contiguous stretch of ticks on which the key is most_likely at >= θ."""
    out, prev = [], None
    for t in sorted(by):
        r0 = next(iter(by[t].values()))
        cur = r0["most_likely"] if r0["confidence"] and float(r0["confidence"]) >= THETA else None
        if cur and cur != prev:
            out.append((t, cur.replace("deliver_item(?item=", "").replace("coffee_break(?coffee_machine=", "coffee:").rstrip(")")))
        prev = cur
    return out


print("| scenario | first moved tick | moved ticks | exhausted TB → L | unexplained TB → L | leaders at θ, TB | leaders at θ, L |")
print("|---|---|---|---|---|---|---|")
for s in SCEN:
    old = load(subprocess.run(["git", "show", f"{TB}:analysis/ir_testbed/{s}/actual.csv"], capture_output=True,
                              text=True, check=True).stdout)
    new = load(Path(f"analysis/ir_testbed/{s}/actual.csv").read_text())
    moved = [t for t in sorted(set(old) | set(new)) if t not in old or t not in new or sig(old[t]) != sig(new[t])]
    ex = lambda by: count(by, lambda r: r["lifecycle"] == "exhausted")
    ux = lambda by: count(by, lambda r: r["finding"] == "unexplained")
    fmt = lambda xs: ", ".join(f"{t} {k}" for t, k in xs)
    first = moved[0] if moved else None
    to = [x for x in theta_ticks(old) if first is not None and x[0] >= first]
    tn = [x for x in theta_ticks(new) if first is not None and x[0] >= first]
    print(f"| {s} | {first if moved else '-'} | {len(moved)} | {ex(old)} → {ex(new)} | {ux(old)} → {ux(new)} | "
          f"{fmt(to) or '-'} | {fmt(tn) or '-'} |")
