#!/usr/bin/env python3
"""
summary.py — the tables REPORT.md quotes, per scenario (TB.3b; layout-independent since TB.4b), printed as markdown:
the script's actions, the expected-action table (phases.json, from the oracle), the derived tick table of events, and
the descriptive trends read from actual.csv (the in-process BeliefState): each true hypothesis's first tick at or
above θ, each hypothesis's belief at the tick its S falls below α and the v·D that took it there, the finding's
transitions, every task started by an event (its start, its pin, the resumption), and the script's last entry (the
exit walk by the authoring convention). v·D is recovered from the actual S (the inverse of E5's tail); its split into e
and the standing charge v·(s − s_exp) is read from expected.csv, whose every compared column equals actual.csv
(diff.md). θ, α, β and v are read from the run's [run] header; no id, coordinate or tick is written here.

The true hypothesis on a tick is the hypothesis key of the task the human's action on that tick belongs to
(trajectory.json: the task on top of the replay's stack for that action, its acknowledgement tick included) when the
loader's [coverage] line judges that task `covered`; none otherwise (an unmodelled task, the idle human). A covered
task's hypothesis outside the support is named as such.

    summary.py <scenario dir> <run.log>
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from domains.kitting.registry import domain_config


def rows(path):
    return [r for r in csv.DictReader(open(path)) if int(r["tick"]) >= 0]


def header(log):
    for l in open(log):
        if l.startswith("[run] "):
            h = dict(re.findall(r"(\w+)=(\S+)", l))
            return float(h["theta"]), float(h["test_level"]), float(h["beta"]), float(h["speed"])
    raise ValueError(f"{log}: no [run] header")


def coverage(log):
    """Task key -> coverage value, from the loader's [coverage] lines (the entries and the tasks their events start)."""
    out = {}
    for l in open(log):
        if l.startswith("[coverage]"):
            for tok in l.split()[4:]:
                task, value = tok.removeprefix("start:").rsplit(")=", 1)
                out[task + ")"] = value.split("(")[0]
    return out


SCHEMAS = {s.name: s for s in domain_config["task_model"]}


def hypothesis_key(task):
    """The hypothesis key of a task key: its schema and its enumerated bindings (determined parameters dropped)."""
    m = re.match(r"(\w+)\((.*)\)$", task)
    schema = SCHEMAS.get(m[1])
    if schema is None:
        return None
    det = schema.determined_parameters or {}
    kept = [b for b in m[2].split(",") if b and b.split("=")[0] not in det]
    return f"{m[1]}(" + ",".join(kept) + ")"


def short(k):
    return re.sub(r"\?\w+=", "", k) if k else "-"


def main(d, log):
    d = Path(d)
    THETA, ALPHA, BETA, V = header(log)
    vd_of = lambda S: 0.0 if S >= 1.0 else -math.log(2.0 ** S - 1.0) / BETA
    act, exp = rows(d / "actual.csv"), rows(d / "expected.csv")
    traj, ph = json.load(open(d / "trajectory.json")), json.load(open(d / "phases.json"))
    admissible = ph["space"]
    cov = coverage(log)
    by = {}
    for r in act:
        by.setdefault(int(r["tick"]), {})[r["key"]] = r
    ex = {(int(r["tick"]), r["key"]): r for r in exp}
    T = max(by)
    task_of = {r["tick"]: r["task"] for r in traj["rows"] if r["tick"] >= 0}
    truth = {t: (hypothesis_key(k) if k and cov.get(k) == "covered" else None) for t, k in task_of.items()}
    tick0 = lambda t: next(iter(by[t].values()))
    state = lambda t: tick0(t)["finding"] if tick0(t)["lifecycle"] == "live" else "exhausted"
    out = [f"### {traj['scenario']}", ""]

    # the script, per tick
    out += ["Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the "
            "loader's [coverage] line):", "",
            "| tick | task | coverage | action | occurrence | stack depth |", "|---|---|---|---|---|---|"]
    out += [f"| {b['tick']} | {short(b['task'])} | {cov.get(b['task'], '?')} | {b['action']} | {b['occurrence']} | "
            f"{len(b['stack'])} |" for b in traj["actions"]]
    out += ["", f"Last acknowledgement tick {traj['last_ack']}; idle from {traj['last_ack'] + 1} to {T}. "
            f"The support (prior on): {', '.join(short(k) for k in admissible)}.", ""]

    # the expected-action table
    out += ["Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before "
            "the clock starts; after the pin the hypothesis is retired):", "",
            "| hypothesis | expected action | ticks |", "|---|---|---|"]
    for k in admissible:
        for lab, a, b in ph["phases"][k]:
            out.append(f"| {short(k)} | {short(lab)} | {a} to {b} |")
    out.append("")

    # events
    pins = [(t, p) for t in sorted(by) for p in tick0(t)["pins"].split(";") if p]
    bounds = [t for t in sorted(by) if tick0(t)["boundary"] == "1"]
    ev = [(t, f"pin {short(p)}") for t, p in pins] + [(t, "boundary") for t in bounds]
    last = None
    for t in sorted(by):
        s = state(t)
        if s == "unexplained" and last != "unexplained":
            ev.append((t, "finding turns unexplained"))
        if last == "unexplained" and s != "unexplained":
            ev.append((t, f"finding turns {s} (from unexplained)"))
        if s == "exhausted" and last != "exhausted":
            ev.append((t, "exhausted (no live hypothesis) from here"))
        last = s
    out += ["Events (actual):", "", "| tick | event |", "|---|---|"]
    out += [f"| {t} | {e} |" for t, e in sorted(ev)]
    never = [k for k in admissible if k not in {p for _, p in pins}]
    tail = len(traj["actions"]) - 1                  # the last entry: the final run of actions with its task
    while tail > 0 and traj["actions"][tail - 1]["task"] == traj["actions"][-1]["task"] \
            and len(traj["actions"][tail - 1]["stack"]) == 1:
        tail -= 1
    exit_start = traj["actions"][tail]["tick"]
    states = sorted({state(t) for t in range(exit_start, traj["last_ack"] + 1)})
    out += ["", f"Never pinned: {', '.join(short(k) for k in never) or 'none'}. At the last entry "
            f"({short(traj['actions'][-1]['task'])}, ticks {exit_start} to {traj['last_ack']}): lifecycle and finding "
            f"{', '.join(states)}; on the idle ticks after it: {', '.join(sorted({state(t) for t in range(traj['last_ack'] + 1, T + 1)})) or '-'}.", ""]

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
        if k not in admissible:
            out.append(f"| {short(k)} | {a} to {b} | outside the support (at the floor) | - | - | - |")
            continue
        hit = next((t for t in range(a, b + 1) if k in by[t] and float(by[t][k]["belief"]) >= THETA), None)
        if hit is None:
            out.append(f"| {short(k)} | {a} to {b} | not reached | - | - | - |")
        else:
            r = by[hit][k]
            out.append(f"| {short(k)} | {a} to {b} | {hit} | {float(r['belief']):.4f} | "
                       f"{'yes' if r['most_likely'] == k else 'no'} | {r['adequacy']} |")
    out.append("")

    # trends: each S < alpha crossing
    out += [f"Refutations (actual): each tick on which a hypothesis's S falls below α = {ALPHA:g} (from ≥ α or from no "
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
                out.append(f"| {t} | {short(k)} | {short(e['expected_action'])} | {float(r['belief']):.4f} | {S:.4f} | "
                           f"{vd_of(S):.1f} | {float(e['e']):.1f} | {stand:.1f} | {short(truth.get(t))} |")
            prev[k] = below
    out.append("")

    # trends: the finding's transitions
    out += ["Finding transitions (actual; `exhausted` is the lifecycle state, no finding):", "",
            "| tick | from | to | truth |", "|---|---|---|---|"]
    last = None
    for t in sorted(by):
        s = state(t)
        if s != last:
            out.append(f"| {t} | {last or '-'} | {s} | {short(truth.get(t))} |")
            last = s
    out.append("")

    # every task started by an event: its start, its pin (if its hypothesis is pinned), the resumption
    trow = {r["tick"]: r for r in traj["rows"]}
    started = []                                     # (task, its first tick on top of a suspended task)
    for b in traj["actions"]:
        if len(b["stack"]) > 1 and (not started or started[-1][0] != b["task"]):
            started.append((b["task"], b["tick"]))
    for task, s0 in started:
        s1 = s0                                      # the contiguous stretch it is on top
        while task_of.get(s1 + 1) == task:
            s1 += 1
        k = hypothesis_key(task) if cov.get(task) == "covered" else None
        pin = next((t for t, p in pins if k is not None and p == k), None)
        resume = next((b["tick"] for b in traj["actions"] if b["tick"] > s1), None)
        anchor = pin if pin is not None else s1
        ticks = sorted({x for x in (s0 - 2, s0 - 1, s0, s0 + 1, s0 + 2, anchor - 1, anchor, anchor + 1, anchor + 2)
                        + ((resume, resume + 1, resume + 2) if resume is not None else ()) if 0 <= x <= T})
        out += [f"Across the started task {short(task)} ({cov.get(task, '?')}; actual): on top of the stack from {s0} "
                f"to {s1}" + (f", its hypothesis pinned at {pin}" if pin is not None else ", no pin") +
                (f"; the suspended task resumes at {resume}." if resume is not None else "."), "",
                "| tick | human action | truth | " + " | ".join(f"{short(k)} belief / S" for k in admissible)
                + " | finding |", "|---|---|---|" + "---|" * len(admissible) + "---|"]
        for t in ticks:
            cells = []
            for h in admissible:
                r = by[t].get(h)
                cells.append("retired" if r is None else
                             f"{float(r['belief']):.4f} / {'-' if r['S'] == '' else format(float(r['S']), '.4f')}")
            out.append(f"| {t} | {trow[t]['action']} {trow[t]['micro'] or ''} | {short(truth.get(t))} | "
                       + " | ".join(cells) + f" | {state(t)} |")
        out.append("")

    # the script's last entry (the exit walk by the authoring convention)
    walk = [r for r in traj["rows"] if exit_start <= r["tick"] <= traj["last_ack"]]
    last_step = max(r["tick"] for r in walk if r["micro"] == "step")
    live = sorted(k for k in by[exit_start] if k)
    out += [f"The last entry ({short(traj['actions'][-1]['task'])}): first step {exit_start}, last step {last_step}, "
            f"acknowledgement {traj['last_ack']}; the idle human from {traj['last_ack'] + 1}. Live at its first tick: "
            f"{', '.join(short(k) for k in live) or 'none (exhausted)'}.", ""]
    for k in live:
        cross = next((t for t in range(exit_start, T + 1) if k in by[t] and by[t][k]["S"] != ""
                      and float(by[t][k]["S"]) < ALPHA), None)
        une = next((t for t in range(exit_start, T + 1) if state(t) == "unexplained"), None)
        r = by[exit_start][k]
        out.append(f"- {short(k)}: belief {float(r['belief']):.4f} at {exit_start}; S < α from {cross}"
                   + (f" (belief {float(by[cross][k]['belief']):.4f}; v·D {vd_of(float(by[cross][k]['S'])):.1f} cm)"
                      if cross is not None else "")
                   + f"; the finding unexplained from {une}.")
        out.append("")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
