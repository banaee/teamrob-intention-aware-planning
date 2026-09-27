#!/usr/bin/env python3
"""
summary.py — the tables REPORT.md quotes, per scenario (TB.3b), printed as markdown: the expected-action table
(phases.json, from the oracle), the derived tick table of events, and the descriptive trends read from actual.csv
(the in-process BeliefState): each true hypothesis's first tick at or above θ, each rival's belief at the tick its S
falls below α and the v·D that took it there, the finding's transitions, the coffee boundary (scenario_s08_03 / _04),
the exit walk. v·D is recovered from the actual S (the inverse of E5's tail); its split into e and the standing
charge v·(s − s_exp) is read from expected.csv, whose every compared column equals actual.csv (diff.md).

The true hypothesis on a tick is the hypothesis key of the task the human's action on that tick belongs to
(trajectory.json: the task on top of the replay's stack for that action, its acknowledgement tick included); None
on the idle ticks and for the exit walk, which no hypothesis describes.

    summary.py <scenario dir>
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

THETA, ALPHA, BETA, V = 0.75, 0.05, 0.01, 20.0


def rows(path):
    return [r for r in csv.DictReader(open(path)) if int(r["tick"]) >= 0]


def key_of(task):
    if task is None or task.startswith("go_to"):
        return None
    return re.sub(r",\?kitting_table=kitting_table_\d+", "", task)


def short(k):
    return (k or "-").replace("deliver_item(?item=", "deliver ").replace(
        "coffee_break(?coffee_machine=coffee_machine_0)", "coffee_break").rstrip(")") if k else "-"


def vd_of(S):
    if S >= 1.0:
        return 0.0
    return -math.log(2.0 ** S - 1.0) / BETA


def main(d):
    d = Path(d)
    act, exp = rows(d / "actual.csv"), rows(d / "expected.csv")
    traj, ph = json.load(open(d / "trajectory.json")), json.load(open(d / "phases.json"))
    sid = traj["scenario"]
    by = {}
    for r in act:
        by.setdefault(int(r["tick"]), {})[r["key"]] = r
    ex = {(int(r["tick"]), r["key"]): r for r in exp}
    T = max(by)
    truth = {r["tick"]: key_of(r["task"]) for r in traj["rows"] if r["tick"] >= 0}
    tick0 = lambda t: next(iter(by[t].values()))
    out = [f"### {sid}", ""]

    # the script, per tick
    out += ["Script actions (replay expanded per tick; the first tick of each action):", "",
            "| tick | task | action | occurrence |", "|---|---|---|---|"]
    out += [f"| {b['tick']} | {short(key_of(b['task'])) if key_of(b['task']) else b['task']} | {b['action']} | "
            f"{b['occurrence']} |" for b in traj["actions"]]
    out += ["", f"Last acknowledgement tick {traj['last_ack']}; idle from {traj['last_ack'] + 1} to {T}.", ""]

    # the expected-action table
    out += ["Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before "
            "the clock starts; after the pin the hypothesis is retired):", "",
            "| hypothesis | expected action | ticks |", "|---|---|---|"]
    for k in ph["space"]:
        for lab, a, b in ph["phases"][k]:
            out.append(f"| {short(k)} | {lab} | {a} to {b} |")
    out.append("")

    # events
    pins = [(t, p) for t in sorted(by) for p in tick0(t)["pins"].split(";") if p]
    bounds = [t for t in sorted(by) if tick0(t)["boundary"] == "1"]
    exhausted = next((t for t in sorted(by) if tick0(t)["lifecycle"] == "exhausted"), None)
    out += ["Events (actual):", "", "| tick | event |", "|---|---|"]
    ev = [(t, f"pin {short(p)}") for t, p in pins] + [(t, "boundary") for t in bounds]
    if exhausted is not None:
        ev.append((exhausted, "exhausted (no live hypothesis) from here"))
    out += [f"| {t} | {e} |" for t, e in sorted(ev)]
    out.append("")

    # trends: the true hypothesis's first tick at or above theta, per stretch of ticks it is the truth
    out += ["True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its "
            "first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.", "",
            "| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |", "|---|---|---|---|---|---|"]
    stretches, cur = [], None
    for t in range(T + 1):
        k = truth.get(t)
        if cur and cur[0] == k:
            cur[2] = t
        else:
            cur = [k, t, t]
            stretches.append(cur)
    for k, a, b in stretches:
        if k is None:
            continue
        hit = next((t for t in range(a, b + 1) if k in by[t] and float(by[t][k]["belief"]) >= THETA), None)
        if hit is None:
            out.append(f"| {short(k)} | {a} to {b} | not reached | - | - | - |")
        else:
            r = by[hit][k]
            out.append(f"| {short(k)} | {a} to {b} | {hit} | {float(r['belief']):.4f} | "
                       f"{'yes' if r['most_likely'] == k else 'no'} | {r['adequacy']} |")
    out.append("")

    # trends: each S < alpha crossing (a member whose S falls below alpha, from >= alpha or from no observation)
    out += ["Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no "
            "observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from "
            "expected.csv; the truth on that tick.", "",
            "| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |",
            "|---|---|---|---|---|---|---|---|---|"]
    prev = {}
    for t in sorted(by):
        for k, r in by[t].items():
            if not k:
                continue
            below = r["S"] != "" and float(r["S"]) < ALPHA
            if below and not prev.get(k, False):
                S = float(r["S"])
                e = ex[(t, k)]
                stand = V * (float(e["s"]) - float(e["s_exp"]))
                out.append(f"| {t} | {short(k)} | {e['expected_action']} | {float(r['belief']):.4f} | {S:.4f} | "
                           f"{vd_of(S):.1f} | {float(e['e']):.1f} | {stand:.1f} | {short(truth.get(t))} |")
            prev[k] = below
    out.append("")

    # trends: the finding's transitions
    out += ["Finding transitions (actual; `exhausted` is the lifecycle state, no finding):", "",
            "| tick | from | to | truth |", "|---|---|---|---|"]
    last = None
    for t in sorted(by):
        r = tick0(t)
        s = r["finding"] if r["lifecycle"] == "live" else "exhausted"
        if s != last:
            out.append(f"| {t} | {last or '-'} | {s} | {short(truth.get(t))} |")
            last = s
    out.append("")

    # the coffee boundary (the coffee_break started inside a delivery)
    starts = [b for b in traj["actions"] if b["task"].startswith("coffee_break")]
    if starts and len(starts[0]["stack"]) > 1:
        c0 = starts[0]["tick"]
        cpin = next(t for t, p in pins if p.startswith("coffee_break"))
        resume = next(b["tick"] for b in traj["actions"] if b["tick"] > cpin)
        ticks = sorted({c0 - 2, c0 - 1, c0, c0 + 1, c0 + 2, cpin - 1, cpin, cpin + 1, cpin + 2, resume, resume + 1,
                        resume + 2})
        keys = ph["space"]
        out += [f"Across the coffee boundary (actual): the coffee_break starts at {c0} (its walk), is pinned at "
                f"{cpin} (the boundary), and the suspended delivery resumes at {resume}.", "",
                "| tick | human action | truth | " + " | ".join(f"{short(k)} belief / S" for k in keys)
                + " | finding |", "|---|---|---|" + "---|" * len(keys) + "---|"]
        trow = {r["tick"]: r for r in traj["rows"]}
        for t in ticks:
            cells = []
            for k in keys:
                r = by[t].get(k)
                cells.append("retired" if r is None else
                             f"{float(r['belief']):.4f} / {'-' if r['S'] == '' else format(float(r['S']), '.4f')}")
            r0 = tick0(t)
            out.append(f"| {t} | {trow[t]['action']} {trow[t]['micro'] or ''} | {short(truth.get(t))} | "
                       + " | ".join(cells) + f" | {r0['finding'] if r0['lifecycle'] == 'live' else 'exhausted'} |")
        out.append("")

    # the exit walk
    ex_start = next(b["tick"] for b in traj["actions"] if b["task"].startswith("go_to"))
    walk = [r for r in traj["rows"] if r["tick"] >= ex_start and r["action"] == "move_to"]
    last_step = max(r["tick"] for r in walk if r["micro"] == "step")
    live = sorted(k for k in by[ex_start] if k)
    out += [f"Exit walk (go_to corner_SE): first step {ex_start}, last step {last_step}, acknowledgement "
            f"{traj['last_ack']}; the idle human from {traj['last_ack'] + 1}. Live at its first tick: "
            f"{', '.join(short(k) for k in live) or 'none (exhausted)'}.", ""]
    for k in live:
        cross = next((t for t in range(ex_start, T + 1) if k in by[t] and by[t][k]["S"] != ""
                      and float(by[t][k]["S"]) < ALPHA), None)
        une = next((t for t in range(ex_start, T + 1) if tick0(t)["finding"] == "unexplained"), None)
        r = by[ex_start][k]
        out.append(f"- {short(k)}: belief {float(r['belief']):.4f} at {ex_start}; S < α from {cross}"
                   + (f" (belief {float(by[cross][k]['belief']):.4f}; v·D {vd_of(float(by[cross][k]['S'])):.1f} cm)"
                      if cross is not None else "")
                   + f"; the finding unexplained from {une}.")
        out.append("")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1])
