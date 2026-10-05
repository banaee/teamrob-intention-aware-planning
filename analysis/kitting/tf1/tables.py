#!/usr/bin/env python3
"""
tables.py <measurement root> — the tables of the measurement of T-F part 1's report (D; Hadi, 5 October 2026), from the
result table run_set.sh wrote (<root>/results.csv), printed as markdown.

The sets, by serial (make_runs.py): run_001 to _064 the planning test-bed's 16, run_065 to _088 step 5's 6, run_089 to
_512 step 5e's 106 (each four conditions), run_513 to _688 step 5e's 176 copies with a timeline (intention-aware with
context knowledge on only). The condition from the row's effective settings (the [run] header): human_aware off
human-unaware (HU); intention_aware off intention-unaware (IU); else intention-aware with context knowledge off (IA-off)
or on (IA-on).

Per set, a table per condition: per scenario completion (the world tick after the robot's last release, where the pool
completed: the run has a terminal decision; "-" the pool not completed within the cap, whatever releases came before), held ticks, the ticks below min_separation (near-encounters: the tick's continuous [sep] minimum below it) and
F1's classes (viol, recede: a moving robot; passing, beside: a standing robot, the human passing or beside it), the
continuous [sep] minimum, the decisions, the oracle's disagreements. Per pair of conditions and set, the scenarios
better, equal and worse in the second condition than in the first: on completion (earlier is better; none within the
cap is worse than any completion), on the ticks below min_separation and on the ticks of F1's class viol (fewer is
better). No claim beyond the counts.
"""
import csv
import sys
from pathlib import Path

SETS = [("the planning test-bed (16)", 1, 64), ("step 5's planning cases (6)", 65, 88),
        ("step 5e's planning scenarios, no timeline (106)", 89, 512),
        ("step 5e's copies with a timeline (176; IA-on only)", 513, 688)]
CONDS = ["HU", "IU", "IA-off", "IA-on"]
NAMES = {"HU": "human-unaware", "IU": "intention-unaware", "IA-off": "intention-aware, context knowledge off",
         "IA-on": "intention-aware, context knowledge on"}


def on(v):
    return v in ("True", "on")


def cond(r):
    if not on(r["human_aware"]):
        return "HU"
    if not on(r["intention_aware"]):
        return "IU"
    return "IA-on" if on(r["context_knowledge"]) else "IA-off"


def num(x):
    return None if x in ("", "None") else int(x)


def cmp(a, b, lower_better=True):
    """-1 b better, 0 equal, 1 b worse; None (no completion) worst."""
    if a == b:
        return 0
    if a is None:
        return -1
    if b is None:
        return 1
    return -1 if b < a else 1


def main(root):
    rows = list(csv.DictReader(open(Path(root) / "results.csv")))
    for r in rows:
        r["n"], r["cond"] = int(r["run"].split("_")[1]), cond(r)
        if r["terminal"] in ("", "None"):           # the pool not completed within the cap
            r["completion"] = ""
    out = []
    compared = [r for r in rows if r["oracle"] == "compared"]
    dis = sum(int(r["disagreements"]) for r in compared)
    out += [f"Rows {len(rows)}; the oracle compared on {len(compared)} ({dis} disagreements); none derivable on "
            f"{len(rows) - len(compared)}; settings disagreeing with R5's reading: "
            f"{sum(1 for r in rows if r['settings_agree'] != 'True')}; human-unaware rows against the reference run: "
            + ", ".join(f"{v} {sum(1 for r in rows if r['cond'] == 'HU' and r['reference'] == v)}"
                        for v in sorted({r['reference'] for r in rows if r['cond'] == 'HU'})) + ".", ""]
    for title, lo, hi in SETS:
        sub = [r for r in rows if lo <= r["n"] <= hi]
        out += [f"## {title}", ""]
        conds = [c for c in CONDS if any(r["cond"] == c for r in sub)]
        for c in conds:
            rs = sorted((r for r in sub if r["cond"] == c), key=lambda r: r["scenario"])
            comp = [num(r["completion"]) for r in rs]
            out += [f"### {NAMES[c]} ({c}): {len(rs)} runs, completed within the cap {sum(x is not None for x in comp)}, "
                    f"held ticks {sum(int(r['hold_ticks']) for r in rs)}, ticks below min_separation "
                    f"{sum(int(r['near_encounters']) for r in rs)} (viol {sum(int(r['viol']) for r in rs)}, recede "
                    f"{sum(int(r['recede']) for r in rs)}, passing {sum(int(r['stand_passing']) for r in rs)}, beside "
                    f"{sum(int(r['stand_beside']) for r in rs)}), scenarios with a tick below "
                    f"{sum(1 for r in rs if int(r['near_encounters']) > 0)}", "",
                    "| scenario | run | completion | held | below | viol | recede | passing | beside | sep_min | decisions "
                    "| oracle |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
            out += [f"| {r['scenario']} | {r['run']} | {r['completion'] or '-'} | {r['hold_ticks']} | "
                    f"{r['near_encounters']} | {r['viol']} | {r['recede']} | {r['stand_passing']} | {r['stand_beside']} | "
                    f"{r['sep_min']} | {r['decisions']} | "
                    f"{'-' if r['oracle'] != 'compared' else r['disagreements']} |" for r in rs]
            out.append("")
        if len(conds) > 1:
            by = {(r["scenario"], r["cond"]): r for r in sub}
            scen = sorted({r["scenario"] for r in sub})
            out += ["### Pairs of conditions (the second against the first): scenarios better / equal / worse", "",
                    "| first | second | completion | ticks below min_separation | viol ticks |", "|---|---|---|---|---|"]
            for i, a in enumerate(conds):
                for b in conds[i + 1:]:
                    cells = []
                    for key in ("completion", "near_encounters", "viol"):
                        cs = [cmp(num(by[s, a][key]), num(by[s, b][key])) for s in scen]
                        cells.append(f"{cs.count(-1)} / {cs.count(0)} / {cs.count(1)}")
                    out.append(f"| {a} | {b} | " + " | ".join(cells) + " |")
            out.append("")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1])
