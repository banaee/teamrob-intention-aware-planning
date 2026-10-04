#!/usr/bin/env python3
"""
moved5d.py — T-K part 1, step 5d: the admissions of a hypothesis that is not the true task (comparison.py's A2 rows,
every kind: during modelled tasks, on a pin tick, on the exit walk) that moved with the gate change, one line each.

    moved5d.py <before root>      the root holding the outputs before the gate change, laid out as analysis/kitting
                                  (the external copy: /home/hadi/teamrob_analysis_2026-10-04_gate/kitting)

Before: the recognition runs under <before root>/irb (step 4's tk2 and tk2/off, step 5b's tk5b, the reference sets tk1
and the s08/s09 folders); after: the same under analysis/kitting/irb. A row moved when it is absent, or its ticks differ,
on the other side. For each tick a row lost, the gate's answer after the change on that tick (actual.csv) is counted:
that answer is the cause (none(leader_outranked): AM68; none(leader_unwarranted): AM67).
"""
import csv
import importlib
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "analysis/kitting/mpb/tk5b"))
import comparison as C

NAME = "actual.csv"


def rows_of(d):
    lv = C.levels(d)
    return [dict(r, scen=d.name) for r in C.wrong_rows(d, lv)]


def gate_of(d):
    return {int(r["tick"]): r["gate"] for r in csv.DictReader(open(d / NAME)) if int(r["tick"]) >= 0}


RULING = {"none(leader_outranked)": "AM68", "none(leader_unwarranted)": "AM67"}


def klass(lost):
    """As expected by ruling when every lost tick is refused by one of the two rulings; otherwise to examine."""
    if lost and all(k in RULING for k in lost):
        return "as expected by ruling (" + ", ".join(sorted({RULING[k] for k in lost}, reverse=True)) + ")"
    return "to examine"


def main(before):
    C.S.SCHEMAS.update({s.name: s for s in importlib.import_module("domains.kitting.registry").domain_config["task_model"]})
    after = ROOT / "analysis/kitting/irb"
    before = Path(before) / "irb"
    sets = [("step 4, on", "tk2"), ("step 5b, on", "tk5b"), ("off (step 4's)", "tk2/off"), ("off (round 1)", "tk1"),
            ("off (s08, s09)", ".")]
    print("| side | scenario | kind | admitted | before: ticks (gate) | after | the gate after the change on the lost ticks | "
          "class |")
    print("|---|---|---|---|---|---|---|---|")
    for label, sub in sets:
        for d in sorted((after / sub).glob("scenario_*")):
            if not (d / NAME).exists():
                continue
            b, a, g = rows_of(before / sub / d.name), rows_of(d), gate_of(d)
            akeys = {(r["h"], r["a"], r["b"]) for r in a}
            for r in b:
                if (r["h"], r["a"], r["b"]) in akeys:
                    continue
                now = [x for x in a if x["h"] == r["h"] and x["a"] <= r["b"] and x["b"] >= r["a"]]
                kept = set().union(*[set(range(x["a"], x["b"] + 1)) for x in now]) if now else set()
                lost = Counter(g[t] for t in range(r["a"], r["b"] + 1) if t not in kept)
                aft = "; ".join(f"{x['a']}-{x['b']} ({x['gate']})" for x in now) or "absent"
                print(f"| {label} | {d.name.removeprefix('scenario_')} | {r['kind']} | {C.short(r['h'])} | "
                      f"{r['a']}-{r['b']} ({r['gate']}) | {aft} | "
                      f"{', '.join(f'{k} {v}' for k, v in sorted(lost.items()))} | {klass(lost)} |")
            bkeys = {(r["h"], r["a"], r["b"]) for r in b}
            for r in a:
                if (r["h"], r["a"], r["b"]) not in bkeys and not any(
                        x["h"] == r["h"] and x["a"] <= r["b"] and x["b"] >= r["a"] for x in b):
                    print(f"| {label} | {d.name.removeprefix('scenario_')} | {r['kind']} | {C.short(r['h'])} | absent | "
                          f"{r['a']}-{r['b']} ({r['gate']}) | new | to examine |")


if __name__ == "__main__":
    main(sys.argv[1])
