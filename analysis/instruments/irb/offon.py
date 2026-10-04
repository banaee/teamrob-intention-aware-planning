#!/usr/bin/env python3
"""
offon.py — context knowledge off against on, per case (T-K part 1, step 4, 4 October 2026; KT14: each case labelled by
the state the script meets). Reporting only, read from existing outputs with admission.py's readings, nothing
recomputed.

The on side: every scenario folder of <on dir> with <csv name>. Its off side: the scenario folder, in the off dirs in
the order given, whose trajectory has the same human actions on the same layout (the same script; the timeline acts on
the robot's mind only, R1, so the off run of the script is the off side of every timeline it is run under), read from
the same <csv name>. Per scenario: the timeline in force, read from the trajectory's facts (each timeline fact's runs
of ticks). Per true stretch: the state on its first tick (on), the first tick at θ and the admission off and on, the
ticks after the admission on which the gate no longer clears for it (the retraction reading) off and on, and for an
A/C activation its belief at arrival off and on. Then every admission of a hypothesis that is not the true task, off
and on (P8, part of the measure by Hadi's ruling of 4 October 2026).

    offon.py <on dir> <csv name> <theta> <off dir> [<off dir> ...]
    e.g. offon.py analysis/kitting/irb/tk2 expected.csv 0.75 analysis/kitting/irb/tk2/off analysis/kitting/irb/tk1
"""
import importlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import admission as A
import summary as S


def script_of(d):
    t = json.load(open(d / "trajectory.json"))
    return t["layout"], [(a["tick"], a["action"], a["occurrence"], a["task"]) for a in t["actions"]]


def timeline_of(d):
    """The timeline facts' runs of ticks, from the trajectory's facts (the environment's resolved timeline)."""
    rows = json.load(open(d / "trajectory.json"))["rows"]
    held = {}
    for r in rows:
        if r["tick"] >= 0:
            for f in r["facts"]:
                if len(f) == 1:
                    held.setdefault(f[0], []).append(r["tick"])
    last = max(r["tick"] for r in rows)
    out = []
    for name, ticks in sorted(held.items()):
        for a, b in A.runs_of(ticks):
            out.append(f"{name} {a} to {'end' if b == last else b + 1}")
    return "; ".join(out) or "none"


def off_dir_of(d, offs, name):
    key = script_of(d)
    for root in offs:
        for o in sorted(p for p in root.iterdir() if p.is_dir() and (p / name).exists()):
            if script_of(o) == key:
                return o
    return None


def tick(r, k):
    return "never" if r[k] is None else f"{r[k]} ({r[k] - r['a']})"


def main(on_root, name, theta, offs):
    on_root, offs = Path(on_root), [Path(p) for p in offs]
    S.SCHEMAS.update({s.name: s for s in importlib.import_module("domains.kitting.registry").domain_config["task_model"]})
    cases = []
    for d in sorted(p for p in on_root.iterdir() if p.is_dir() and (p / name).exists()):
        o = off_dir_of(d, offs, name)
        if o is None:
            sys.exit(f"{d.name}: no off run of the same script in {', '.join(map(str, offs))}")
        cases.append((d, o))
    print(f"From `{name}`, θ = {theta:g}; off: the same script's run in the off folder named. Ticks inclusive; delay "
          f"from the stretch's first tick in brackets. \"after admission\": ticks from the admission to the pin on "
          f"which the gate no longer clears for the true hypothesis (the retraction reading).\n")
    print("| scenario | timeline in force (on) | off from | true hypothesis | ticks | state at start (on) | first ≥ θ off | "
          "on | admitted off | on | after admission off | on | A/C belief at arrival off | on |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for d, o in cases:
        sid, _, on = A.stretches(d, name, theta)
        _, _, off = A.stretches(o, name, theta)
        off = {(r["key"], r["a"]): r for r in off}
        tl, src = timeline_of(d), f"{o.parent.name}/{o.name.removeprefix('scenario_')}"
        for r in on:
            f = off[(r["key"], r["a"])]
            print(f"| {sid.removeprefix('scenario_')} | {tl} | {src} | {S.short(r['key'])} | {r['a']} to {r['b']} | "
                  f"{r['state'] or '-'} | {tick(f, 'hit')} | {tick(r, 'hit')} | {tick(f, 'adm')} | {tick(r, 'adm')} | "
                  f"{A.fmt_runs(f['after'])} | {A.fmt_runs(r['after'])} | {f['at_arrival'] or '-'} | "
                  f"{r['at_arrival'] or '-'} |")
            tl = src = "〃"
    print("\nAdmissions of a hypothesis that is not the true task (every tick, the unmodelled ones included), off and "
          "on.\n")
    print("| scenario | side | hypothesis admitted | ticks | true task on those ticks | how it ends |")
    print("|---|---|---|---|---|---|")
    for d, o in cases:
        for side, x in (("off", o), ("on", d)):
            _, rows = A.wrong_admissions(x, name)
            for r in rows or [None]:
                if r is None:
                    print(f"| {d.name.removeprefix('scenario_')} | {side} | none | - | - | - |")
                    continue
                ticks = f"{r['a']}" if r["a"] == r["b"] else f"{r['a']} to {r['b']}"
                print(f"| {d.name.removeprefix('scenario_')} | {side} | {S.short(r['h'])} | {ticks} | {r['true']} | "
                      f"{r['end']} |")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4:])
