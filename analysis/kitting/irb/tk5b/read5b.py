#!/usr/bin/env python3
"""
read5b.py — T-K part 1, step 5b, the recognition set with context knowledge on (analysis/kitting/irb/tk5b/README.md):
the set's reader. Reporting only, read from existing outputs with admission.py's and g_reading.py's readings, nothing
recomputed.

The on side: every scenario folder of analysis/kitting/irb/tk5b; its off side: the folder of the same name in
analysis/kitting/irb (the set's reference, context knowledge off). Both read from the same <csv name>: expected.csv
(the oracle, before any run) or actual.csv (the recognizer, after the runs).

    read5b.py <csv name>            e.g. read5b.py expected.csv     run from the repository root; prints markdown
    read5b.py summary <csv name>    one row per scenario (REPORT.md's table)

Two tables:
1. per true stretch (admission.py): the first tick at θ and the admission, off and on, each with its delay from the
   stretch's first tick; the ticks after the admission on which the gate no longer clears for the true hypothesis;
2. every admission of a hypothesis that is not the true task (admission.py's P8 rows, the exit walk and the one-tick
   rows on a completion included and marked), off and on: the gate's run of ticks and its length, the true task on
   those ticks, how the gate's run ends, and how the meta-planner's trigger rule would hold it (g_reading.py's
   record_end: a record set on the first tick the gate clears for the hypothesis, kept until the rule fires: the
   leader changes, an episode boundary, or the recorded hypothesis inadequate; the gate is not asked for retention),
   with the record's first tick (before the gate's first wrong tick where the admission was right until the human
   left the task) and the wrong ticks it is kept, from the gate's first wrong tick to the tick before the rule fires.
   A one-tick admission on the tick the previous task is pinned, whose hypothesis the human starts on the next tick
   (the next task admitted one tick before its stretch), is listed as such, not as a wrong admission.
"""
import importlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / "analysis/instruments/irb"), str(ROOT / "analysis/kitting/irb/tk2"), str(ROOT)]
import admission as A
import g_reading as G
import summary as S

THETA = 0.75
ON = ROOT / "analysis/kitting/irb/tk5b"
OFF = ROOT / "analysis/kitting/irb"


def tick(r, k):
    return "never" if r[k] is None else f"{r[k]} ({r[k] - r['a']})"


def on_pin_tick(w):
    """A one-tick admission on the tick the previous task is pinned, whose hypothesis the human starts on the next
    tick: the next task admitted one tick before its stretch, not a wrong admission."""
    return w["end"].startswith("the human starts it") and all("complete: pinned" in p for p in w["true"].split(", "))


def held(run, w):
    """The trigger rule's hold of the wrong admission w: the record's first tick, the wrong ticks it is kept (from the
    gate's first wrong tick to the tick before the rule fires, or before the human starts the recorded task) with their
    number, and the firing tick and reason."""
    h, a = w["h"], w["a"]
    rec = G.record_end(run, a, h)                         # 'record from a0; fires <t> <reason>' or '... run's end'
    m = re.match(r"record from (\d+); fires (\d+) (.*)$", rec)
    if m is None:
        a0, f, why = int(re.match(r"record from (\d+)", rec)[1]), run.last + 1, "run's end"
    else:
        a0, f, why = int(m[1]), int(m[2]), f"{m[2]} {m[3]}"
    right = next((t for t in range(a, f) if run.truth.get(t) == h), None)
    if right is not None:
        return f"from {a0}; {a} to {right - 1} ({right - a}), right from {right}", why
    return f"from {a0}; {a} to {f - 1} ({f - a})", why


def main(name):
    G.NAME = name
    S.SCHEMAS.update({s.name: s for s in importlib.import_module("domains.kitting.registry").domain_config["task_model"]})
    dirs = sorted(p for p in ON.iterdir() if p.is_dir() and (p / name).exists())
    print(f"From `{name}`, θ = {THETA:g}; off: analysis/kitting/irb/<scenario> (context knowledge off), on: "
          f"analysis/kitting/irb/tk5b/<scenario>. Ticks inclusive; delay from the stretch's first tick in brackets.\n")
    print("### 1. The true task, per stretch\n")
    print("| scenario | true hypothesis | ticks | first ≥ θ off | on | admitted off | on | after admission off | on |")
    print("|---|---|---|---|---|---|---|---|---|")
    for d in dirs:
        o = OFF / d.name
        sid, _, on = A.stretches(d, name, THETA)
        _, _, off = A.stretches(o, name, THETA)
        off = {(r["key"], r["a"]): r for r in off}
        for r in on:
            f = off[(r["key"], r["a"])]
            print(f"| {sid.removeprefix('scenario_')} | {S.short(r['key'])} | {r['a']} to {r['b']} | {tick(f, 'hit')} | "
                  f"{tick(r, 'hit')} | {tick(f, 'adm')} | {tick(r, 'adm')} | {A.fmt_runs(f['after'])} | "
                  f"{A.fmt_runs(r['after'])} |")
    print("\n### 2. Admissions of a hypothesis that is not the true task\n")
    print("The gate: the run of ticks on which it clears with that hypothesis leading (its length in brackets), and "
          "how it ends. The trigger rule: the record set on the first tick of the gate's run that clears for it, the "
          "ticks it is kept (length in brackets), and the tick and reason the rule fires.\n")
    print("| scenario | side | hypothesis admitted | gate: ticks (n) | true task on those ticks | gate: how it ends | "
          "trigger rule: record from; wrong ticks kept (n) | trigger rule: fires |")
    print("|---|---|---|---|---|---|---|---|")
    for d in dirs:
        for side, x in (("off", OFF / d.name), ("on", d)):
            run = G.Run(x)
            _, rows = A.wrong_admissions(x, name)
            for w in rows or [None]:
                if w is None:
                    print(f"| {d.name.removeprefix('scenario_')} | {side} | none | - | - | - | - | - |")
                    continue
                n = w["b"] - w["a"] + 1
                ticks = f"{w['a']}" if n == 1 else f"{w['a']} to {w['b']}"
                if on_pin_tick(w):
                    print(f"| {d.name.removeprefix('scenario_')} | {side} | {S.short(w['h'])} | {ticks} ({n}) | {w['true']} | "
                          f"{w['end']}: the next task admitted on the pin tick, not wrong | - | - |")
                    continue
                kept, fires = held(run, w)
                print(f"| {d.name.removeprefix('scenario_')} | {side} | {S.short(w['h'])} | {ticks} ({n}) | {w['true']} | "
                      f"{w['end']} | {kept} | {fires} |")


def short(k):
    return G.short(k)


def rows_of(x, name):
    """The wrong admissions of one side, compact: 'h a-b (gate n / rule n)', the unmodelled ones and the pin-tick rows apart."""
    run = G.Run(x)
    _, rows = A.wrong_admissions(x, name)
    main_, exit_ = [], []
    for w in rows:
        if on_pin_tick(w):
            continue
        n = w["b"] - w["a"] + 1
        kept, _ = held(run, w)
        m = re.search(r"\((\d+)\)", kept.split(";")[1])
        cell = f"{short(w['h'])} {w['a']}-{w['b']} ({n}/{m[1] if m else 'end'})"
        (exit_ if w["true"] == "unmodelled" else main_).append(cell)
    return main_, exit_


def summary(name):
    """One row per scenario: the true task's admission delays off -> on, the wrong admissions off and on (gate ticks /
    the trigger rule's wrong ticks), those on unmodelled actions (the exit walk, s09_05's corner walk, s09_06's stand)
    apart."""
    G.NAME = name
    S.SCHEMAS.update({s.name: s for s in importlib.import_module("domains.kitting.registry").domain_config["task_model"]})
    print("| scenario | the true task admitted, delay off → on | wrong admissions off (gate / rule ticks) | on | "
          "on unmodelled actions off | on |")
    print("|---|---|---|---|---|---|")
    for d in sorted(p for p in ON.iterdir() if p.is_dir() and (p / name).exists()):
        o = OFF / d.name
        _, _, on = A.stretches(d, name, THETA)
        _, _, off = A.stretches(o, name, THETA)
        off = {(r["key"], r["a"]): r for r in off}
        f = lambda r: "never" if r["adm"] is None else str(r["adm"] - r["a"])
        adm = ", ".join(f"{short(r['key'])} {f(off[(r['key'], r['a'])])} → {f(r)}" for r in on)
        (mo, eo), (mn, en) = rows_of(o, name), rows_of(d, name)
        print(f"| {d.name.removeprefix('scenario_')} | {adm} | {'; '.join(mo) or 'none'} | {'; '.join(mn) or 'none'} | "
              f"{'; '.join(eo) or 'none'} | {'; '.join(en) or 'none'} |")


if __name__ == "__main__":
    if sys.argv[1] == "summary":
        summary(sys.argv[2])
    else:
        main(sys.argv[1])
