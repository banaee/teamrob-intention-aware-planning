#!/usr/bin/env python3
"""
stats.py — the statistics of the demo-day round of T-F (Hadi, 8 October 2026; README.md beside this file), from the
runner's outputs under runs/ (run_set.sh: results.csv, the per-run folders; tag.py: tags.csv). Writes COMPARISON.md
beside this file and runs/per_run.csv (one row per run, the measures below). Every number in COMPARISON.md is
generated here.

    stats.py

THE CONDITIONS (the seven runs of a scenario, make_runs.py), read from each run's effective settings (results.csv):
  HU          human-unaware (the separation stop off by R5)
  IU          intention-unaware                     IA-off      intention-aware, context knowledge off
  IA-on       intention-aware, context knowledge on
each of IU, IA-off and IA-on with the separation stop off and on. Two series, kept apart: stop off HU, IU, IA-off,
IA-on; stop on IU, IA-off, IA-on, with HU (which has no stop) as the series' first column for reference.

PER RUN: completion of the robot (the world tick after its last release; unfinished: no terminal decision within the
cap), of the human (the tick after the last tick its stack holds a task: its script, the exit walk included, done), of
both (the later of the two; unfinished if the robot's is); held ticks; stopped ticks (the `[stop]` lines); ticks below
min_separation (near_encounters) and by F1's class (viol: a moving robot; recede; stand_passing, stand_beside: a
standing robot), the continuous minimum distance.

LEAD AND STAY, PER ADMISSION (read from the logs and the record, no build): an admission is the first decision, within
one stretch of a task on top of the human's stack, whose projection admits that task's hypothesis (measures.json's
decisions; the stretch from the record, as tag.py reads it); admissions of a task the human is not performing are not
counted here (they are tag.py's wrong-admission ticks). "The place the robot's plan needs": a fixed object both the
robot's chosen task at that decision (the winner) and the admitted task visit (a delivery: its item's shelf and its
destination table; a coffee break: the machine); with the items disjoint this is a kitting table both deliver to, or
none (the admission is then counted as "no shared place"). Lead: ticks from the admission to the first tick, within the
stretch, the human is at the place (within the arrival radius, the trajectory's proximity, 30 cm, of its position; 0 if
already there); stay: the consecutive ticks from that arrival the human remains there. No arrival within the stretch:
counted as "no arrival".

THE TABLES: per group (a, b, c) and over all 50: per condition, the median and the range [min, max] over the scenarios.
An unfinished completion ranks above every finished one (shown as "unf"). The comparison is paired by scenario, for each
pair of neighbouring conditions in a series: the count of scenarios better, equal, worse on completion (the robot's),
held plus stopped ticks, and ticks below min_separation (fewer is better for each; an unfinished run is worse than a
finished one, two unfinished are equal). THE SENTENCE under each table follows a rule fixed here, before the numbers:
for the pair's added capability and a measure, with b better, w worse, e equal and p the two-sided sign test on b and w:
  helps                                         p < 0.05 and b > w;
  does not help (it makes it worse)             p < 0.05 and w > b;
  does not help (no difference in this set)     e >= 80% of the scenarios and p >= 0.05;
  cannot be told from this set                  otherwise.
GROUP B BY THE TAG: the coffee-break and delivery stretches of group b tagged in accord or not in accord (tag.py), per
stretch IA-off against IA-on (the stop off, and the stop on): ticks to the admission in the decision record's reading
(adm_record; "never" ranks above every number), ticks a wrong task is admitted (wrong_record), ticks below
min_separation inside the stretch (near); the same paired counts and sentence rule.
"""
import csv
import json
import math
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"
GROUP = {1: "a", 2: "a", 3: "b", 4: "b", 5: "b", 6: "b", 7: "c", 8: "c", 9: "c", 10: "c"}
SUBGROUP = {7: "c, the mix", 8: "c, the mix", 9: "c, unmodelled only", 10: "c, unmodelled only"}
OFF = ["HU", "IU", "IA-off", "IA-on"]
ON = ["HU", "IU+stop", "IA-off+stop", "IA-on+stop"]
LABEL = {"HU": "human-unaware", "IU": "intention-unaware", "IA-off": "intention-aware, ck off",
         "IA-on": "intention-aware, ck on", "IU+stop": "intention-unaware", "IA-off+stop": "intention-aware, ck off",
         "IA-on+stop": "intention-aware, ck on"}
UNF = math.inf


def condition(r):
    if r["human_aware"] == "False":
        return "HU"
    base = "IU" if r["intention_aware"] == "False" else ("IA-on" if r["context_knowledge"] == "True" else "IA-off")
    return base + ("+stop" if r["separation_stop"] == "on" else "")


def human_completion(rec):
    last = None
    for l in open(rec):
        m = re.match(r"\[rec\] step=(\d+) stack=(\S+)", l)
        if m and m[2] != "-":
            last = int(m[1])
    return None if last is None else last + 1


sys.path[:0] = [str(HERE.parents[1] / "instruments" / "mpb")]
import tag


def stretches(rec):
    """[(task, first tick, tick after the last)] of the top of the human's stack (tag.py's reading)."""
    return tag.record(rec)[0]


def places(key, traj):
    """The fixed objects a task visits, from its hypothesis or task key."""
    item = re.search(r"\?item=(item_\d+)", key)
    if item:
        return {traj["home"][item[1]], traj["dest"][item[1]]}
    machine = re.search(r"\?coffee_machine=(\w+)", key)
    return {machine[1]} if machine else set()


def lead_stay(d, traj, strs):
    m = json.load(open(d / "measures.json"))
    pos = {r["tick"]: (r["x"], r["y"]) for r in traj["rows"]}
    radius = traj["params"]["proximity"]
    seen, out = set(), []
    for x in m["decisions"]:
        if not x["projection"].startswith("admitted "):
            continue
        h, t = x["projection"][len("admitted "):], x["tick"]
        s = next((s for s in strs if s[1] <= t < s[2]), None)
        if s is None or tag.hypothesis_of(s[0], [h]) is None or (s, h) in seen:
            continue
        seen.add((s, h))
        shared = places(h, traj) & places(x["winner"], traj)
        if not shared:
            out.append(dict(tick=t, hypothesis=h, place=None, lead=None, stay=None))
            continue
        p = traj["fixed"][sorted(shared)[0]]
        at = lambda k: k in pos and math.dist(pos[k], p) <= radius
        arrive = next((k for k in range(t, s[2]) if at(k)), None)
        if arrive is None:
            out.append(dict(tick=t, hypothesis=h, place=sorted(shared)[0], lead=None, stay=None))
            continue
        k = arrive
        while at(k):
            k += 1
        out.append(dict(tick=t, hypothesis=h, place=sorted(shared)[0], lead=arrive - t, stay=k - arrive))
    return out


def per_run():
    rows = []
    for r in csv.DictReader(open(RUNS / "results.csv")):
        d = RUNS / r["scenario"] / r["run"]
        n = int(r["scenario"].rsplit("_", 1)[1])
        traj = json.load(open(d / "trajectory.json"))
        strs = stretches(d / f"{r['run']}.rec")
        robot = UNF if r["completion"] == "unfinished" else int(r["completion"])
        human = human_completion(d / f"{r['run']}.rec")
        rows.append(dict(
            run=r["run"], scenario=r["scenario"], group=GROUP[n], subgroup=SUBGROUP.get(n, GROUP[n]),
            condition=condition(r), robot=robot, human=human, both=max(robot, human),
            hold=int(r["hold_ticks"]), stop=int(r["stop_ticks"]), near=int(r["near_encounters"]), viol=int(r["viol"]),
            recede=int(r["recede"]), stand_passing=int(r["stand_passing"]), stand_beside=int(r["stand_beside"]),
            sep_min=float(r["sep_min"]) if r["sep_min"] else UNF, oracle=r["oracle"],
            disagreements=r["disagreements"], reference=r["reference"], admissions=lead_stay(d, traj, strs)))
    return rows


def fmt(v):
    return "unf" if v == UNF else (f"{v:.1f}" if isinstance(v, float) and v != int(v) else f"{int(v)}")


def cell(vals):
    vals = sorted(vals)
    if not vals:
        return "–"
    med = statistics.median_low(vals) if UNF in vals else statistics.median(vals)
    return f"{fmt(med)} [{fmt(vals[0])}–{fmt(vals[-1])}]"


def sign_p(b, w):
    n = b + w
    if n == 0:
        return 1.0
    k = min(b, w)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n * 2
    return min(1.0, p)


def verdict(b, e, w):
    p = sign_p(b, w)
    if p < 0.05:
        return "helps" if b > w else "makes it worse"
    if e >= 0.8 * (b + e + w):
        return "no difference"
    return "cannot be told"


def paired(by, a, c, key):
    b = e = w = 0
    for s in by:
        if a not in by[s] or c not in by[s]:
            continue
        x, y = key(by[s][a]), key(by[s][c])
        if y < x:
            b += 1
        elif y > x:
            w += 1
        else:
            e += 1
    return b, e, w


MEASURES = [("robot", "completion, robot"), ("human", "completion, human"), ("both", "completion, both"),
            ("hold", "held ticks"), ("stop", "stopped ticks"), ("near", "ticks below min_separation"),
            ("viol", "  of which viol (moving robot)"), ("recede", "  of which recede"),
            ("stand_passing", "  of which stand_passing"), ("stand_beside", "  of which stand_beside"),
            ("sep_min", "minimum distance (cm)")]
PAIRED = [("completion", lambda r: r["robot"]), ("held + stopped ticks", lambda r: r["hold"] + r["stop"]),
          ("ticks below min_separation", lambda r: r["near"])]
ADDED = {("HU", "IU"): "planning against the observed human", ("IU", "IA-off"): "recognition of the human's task",
         ("IA-off", "IA-on"): "context knowledge", ("HU", "IU+stop"): "planning against the observed human (stop on)",
         ("IU+stop", "IA-off+stop"): "recognition of the human's task",
         ("IA-off+stop", "IA-on+stop"): "context knowledge"}


def table(rows, title):
    by = defaultdict(dict)
    for r in rows:
        by[r["scenario"]][r["condition"]] = r
    n = len(by)
    out = [f"### {title} ({n} scenarios)", ""]
    for series, name in ((OFF, "separation stop off"), (ON, "separation stop on")):
        out += [f"**{name}** (median [min–max] over the scenarios)", "",
                "| measure | " + " | ".join(f"{c} ({LABEL[c]})" for c in series) + " |",
                "|---|" + "---|" * len(series)]
        for k, label in MEASURES:
            out.append(f"| {label} | " + " | ".join(cell([by[s][c][k] for s in by if c in by[s]]) for c in series)
                       + " |")
        out += ["", "Paired by scenario, better / equal / worse:", "",
                "| added capability | " + " | ".join(m for m, _ in PAIRED) + " |", "|---|" + "---|" * len(PAIRED)]
        sentences = []
        for a, c in zip(series, series[1:]):
            counts = [paired(by, a, c, f) for _, f in PAIRED]
            out.append(f"| {ADDED[(a, c)]} ({a} → {c}) | " + " | ".join(f"{b} / {e} / {w}" for b, e, w in counts)
                       + " |")
            v = [verdict(*x) for x in counts]
            sentences.append(f"{ADDED[(a, c)][0].upper() + ADDED[(a, c)][1:]}: on completion it {say(v[0])}; on held "
                             f"and stopped ticks it {say(v[1])}; on ticks below min_separation it {say(v[2])}.")
        out += [""] + [f"- {x}" for x in sentences] + [""]
    return out


def say(v):
    return {"helps": "helps", "makes it worse": "does not help (it makes it worse)",
            "no difference": "does not help (no difference in this set)",
            "cannot be told": "cannot be told from this set"}[v]


def lead_table(rows):
    out = ["| condition | admissions of the task performed | with a shared place | arrived | lead median [min–max] | "
           "stay median [min–max] |", "|---|---|---|---|---|---|"]
    for c in ("IA-off", "IA-on", "IA-off+stop", "IA-on+stop"):
        adm = [a for r in rows if r["condition"] == c for a in r["admissions"]]
        shared = [a for a in adm if a["place"] is not None]
        arrived = [a for a in shared if a["lead"] is not None]
        out.append(f"| {c} | {len(adm)} | {len(shared)} | {len(arrived)} | {cell([a['lead'] for a in arrived])} | "
                   f"{cell([a['stay'] for a in arrived])} |")
    return out


def tag_tables(rows):
    tags = list(csv.DictReader(open(RUNS / "tags.csv")))
    cond = {r["run"]: r["condition"] for r in rows}
    grp = {r["run"]: r["group"] for r in rows}
    out = []
    for series in (("IA-off", "IA-on"), ("IA-off+stop", "IA-on+stop")):
        for tagname in ("in accord", "not in accord"):
            st = defaultdict(dict)
            for t in tags:
                if grp[t["run"]] != "b" or t["tag"] != tagname or cond[t["run"]] not in series or not t["hypothesis"]:
                    continue
                st[(t["scenario"], t["task"], t["start"])][cond[t["run"]]] = t
            num = lambda v: UNF if v == "never" else int(v)
            ms = [("ticks to admission", lambda t: num(t["adm_record"])),
                  ("wrong-admission ticks", lambda t: int(t["wrong_record"])),
                  ("ticks below min_separation", lambda t: int(t["near"]))]
            tasks = defaultdict(int)
            for k in st:
                tasks[k[1].split("(")[0]] += 1
            out += [f"**{tagname}**, {series[0]} → {series[1]}: {len(st)} stretches ("
                    + ", ".join(f"{v} {k}" for k, v in sorted(tasks.items())) + ")", "",
                    "| measure | " + " | ".join(series) + " | better / equal / worse |", "|---|---|---|---|"]
            sentences = []
            for name, f in ms:
                vals = [[f(st[k][c]) for k in st if c in st[k]] for c in series]
                b, e, w = paired(st, series[0], series[1], f)
                out.append(f"| {name} | {cell(vals[0])} | {cell(vals[1])} | {b} / {e} / {w} |")
                sentences.append(f"{name}: context knowledge {say(verdict(b, e, w))}")
            out += ["", "- " + "; ".join(sentences) + ".", ""]
    return out


def main():
    rows = per_run()
    with open(RUNS / "per_run.csv", "w", newline="") as f:
        cols = [k for k in rows[0] if k != "admissions"] + ["admissions"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({**r, "admissions": json.dumps(r["admissions"]),
                        **{k: ("unfinished" if r[k] == UNF else r[k]) for k in ("robot", "both", "sep_min")}})
    unf = [r for r in rows if r["robot"] == UNF]
    compared = [r for r in rows if r["oracle"] == "compared"]
    dis = sum(int(r["disagreements"]) for r in compared)
    humans = defaultdict(set)
    for r in rows:
        humans[r["scenario"]].add(r["human"])
    lines = ["# The demo-day round of T-F: comparison", "",
             "Generated by analysis/kitting/tf_demo/stats.py from the runs under runs/ (README.md: the decisions, the "
             "seed, the definitions). Durations in ticks.", "",
             f"- Runs: {len(rows)}; finished {len(rows) - len(unf)}, unfinished {len(unf)}"
             + (": " + ", ".join(f"{r['run']} ({r['scenario']}, {r['condition']})" for r in unf) if unf else "") + ".",
             f"- The oracle: compared on {len(compared)} runs, {dis} disagreements; not derivable on "
             f"{len(rows) - len(compared)}. The human-unaware runs' check includes the robot-alone reference run "
             f"(results.csv, `reference`: {sum(1 for r in rows if r['condition'] == 'HU' and r['reference'] == 'equal')} "
             f"of {sum(1 for r in rows if r['condition'] == 'HU')} equal).",
             f"- The human's completion is the same in every run of a scenario in "
             f"{sum(len(v) == 1 for v in humans.values())} of {len(humans)} scenarios (the human does not react to the "
             f"robot).", ""]
    lines += ["## All 50 scenarios", ""] + table(rows, "all")
    for g, title in (("a", "Group a: the assigned deliveries only"), ("b", "Group b: one coffee break"),
                     ("c", "Group c: switch, coffee break and unmodelled behaviour")):
        lines += [f"## {title}", ""] + table([r for r in rows if r["group"] == g], title)
    for sg in ("c, the mix", "c, unmodelled only"):
        lines += [f"## Group {sg}", ""] + table([r for r in rows if r["subgroup"] == sg], f"group {sg}")
    lines += ["## Group b by the tag", ""] + tag_tables(rows)
    lines += ["## Lead and stay per admission (all 50 scenarios)", ""] + lead_table(rows) + [""]
    for g in ("a", "b", "c"):
        lines += [f"Group {g}:", ""] + lead_table([r for r in rows if r["group"] == g]) + [""]
    (HERE / "COMPARISON.md").write_text("\n".join(lines) + "\n")
    print(f"{len(rows)} runs, unfinished {len(unf)}, oracle compared {len(compared)} with {dis} disagreements")


if __name__ == "__main__":
    main()
