#!/usr/bin/env python3
"""
tk5.py — T-K part 1, step 5, the planning cases (analysis/kitting/mpb/tk/README.md): the set's own reader.

    tk5.py expect      the expected chain per run before any run: the MPB chain (analysis/instruments/mpb/chain.py)
                       assembled from the oracle's per-tick table (expected_ticks.json) with the robot's one
                       no_current_task tick known before the run, tick 0; valid up to the robot's completion, whose
                       no_current_task tick only the run gives (the decisions after it are listed and marked)
    tk5.py report      per scenario and side, from the runs: the decisions with their projection and hold, the
                       admissions as the meta-planner held them (the decision record: from a decision that admits to
                       the next decision), the completion, the separation in the case's window and over the run

The sides: off is analysis/kitting/mpb/tk/off/<scenario>, on is analysis/kitting/mpb/tk/<scenario>; one strategy,
single_task. Nothing here derives an expectation from a run.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / "analysis" / "instruments" / "mpb"), str(ROOT / "analysis" / "instruments" / "common"),
                 str(ROOT)]

from chain import assemble
from mpblib import load_ticks, load_decisions

VAR = "on_single_task"
# (scenario, side, the case(s) it serves, the case's window of ticks)
RUNS = [("scenario_s16_01", "off", "3, 2 (reference)", (40, 60)), ("scenario_s16_01", "on", "3", (40, 60)),
        ("scenario_s16_02", "on", "2", (40, 60)),
        ("scenario_s16_03", "off", "1, 4 (reference)", (38, 75)), ("scenario_s16_03", "on", "4", (38, 75)),
        ("scenario_s16_04", "on", "1", (38, 75)),
        ("scenario_s16_05", "off", "5 (reference)", (15, 35)), ("scenario_s16_05", "on", "5", (15, 35)),
        ("scenario_s16_06", "on", "5, the A/C raised", (15, 35))]
SIDE = {("scenario_s16_01", "off"): "off", ("scenario_s16_01", "on"): "on, no fact", ("scenario_s16_02", "on"): "on, break_time",
        ("scenario_s16_03", "off"): "off", ("scenario_s16_03", "on"): "on, no fact", ("scenario_s16_04", "on"): "on, break_time",
        ("scenario_s16_05", "off"): "off", ("scenario_s16_05", "on"): "on, no fact", ("scenario_s16_06", "on"): "on, room_warm"}


def folder(sid, side):
    return (HERE / "off" if side == "off" else HERE) / sid / VAR


def short(key):
    if key is None:
        return "-"
    return key.split("(")[0] + ("(" + key.split("?item=")[1].split(")")[0].split(",")[0] + ")" if "?item=" in key else "")


def proj(d):
    if d.admitted is not None:
        return "admitted " + short(d.admitted.key)
    return "none" if d.fallback is None else f"fallback {d.fallback.mode.value} k={d.fallback.k} end={d.fallback.end:.0f}"


def expect():
    print("| scenario | side | case | expected decisions before the robot's completion (tick trigger/cause: projection) |")
    print("|---|---|---|---|")
    for sid, side, case, _ in RUNS:
        ticks = load_ticks(folder(sid, side) / "expected_ticks.json")
        chain = assemble(ticks, {0}, None, 130)
        cells = [f"{d.tick} {d.trigger.value.replace('recognition_changed', 'rc').replace('projection_expired', 'pe').replace('no_current_task', 'nct')}"
                 f"{'/' + d.cause.value if d.cause else ''}: {proj(d)}" for d in chain]
        print(f"| {sid} | {SIDE[(sid, side)]} | {case} | {'; '.join(cells)} |")


def held(decisions, last):
    """The admissions as the meta-planner held them: from a decision that admits to the tick before the next decision."""
    out = []
    for i, d in enumerate(decisions):
        if d.admitted is None:
            continue
        end = decisions[i + 1].tick - 1 if i + 1 < len(decisions) else last
        out.append(f"{short(d.admitted.key)} {d.tick}-{end}")
    return out


def report():
    import logparse
    from sep_classes import summary, rule
    print("| scenario | side | case | decisions (tick trigger/cause: projection, hold) | held admissions | completion | "
          "window: min separation (tick), F1 violations | run: min separation (tick) |")
    print("|---|---|---|---|---|---|---|---|")
    for sid, side, case, (a, b) in RUNS:
        d = folder(sid, side)
        decisions = load_decisions(d / "actual_decisions.json")
        sel = {s["tick"]: s for s in json.load(open(d / "selection.json"))}
        props = json.load(open(d / "properties.json"))
        log = next((HERE / ("off" if side == "off" else "") / "runs").glob(f"*_{sid}_{VAR}.log"))
        run = logparse.parse(str(log))
        sep = float(run["hdr"].get("min_separation", 50.0))
        win = [(run["sep"][k][1], k) for k in range(a, b + 1) if k in run["sep"] and run["sep"][k][1] is not None]
        mn = min(win)
        viol = [k for k in range(a, b + 1) if k in run["sep"] and run["sep"][k][1] is not None
                and run["sep"][k][1] < sep and rule(run, k, sep) == "viol"]
        s = summary(str(log))
        cells = [f"{x.tick} {x.trigger.value.replace('recognition_changed', 'rc').replace('projection_expired', 'pe').replace('no_current_task', 'nct')}"
                 f"{'/' + x.cause.value if x.cause else ''}: {proj(x)}, {sel[x.tick]['hold'] or 0}" for x in decisions]
        print(f"| {sid} | {SIDE[(sid, side)]} | {case} | {'; '.join(cells)} | {', '.join(held(decisions, props['horizon']))} | "
              f"{props['completion']} | {mn[0]:.1f} ({mn[1]}), {viol or 'none'} | {s['cont'][0]:.1f} ({s['cont'][1]}) |")


if __name__ == "__main__":
    {"expect": expect, "report": report}[sys.argv[1]]()
