#!/usr/bin/env python3
"""
make_runs.py — writes the run files of the measurement of T-F part 1 (L, K; Hadi, 5 October 2026; design_records.md,
"T-F part 1", THE MEASUREMENT) into configs/kitting/tf1/measurement/<scenario>/run_NNN.yaml.

The scenarios (L): the planning test-bed's 16 (configs/kitting/mpb/*.yaml), step 5's 6 planning cases
(configs/kitting/mpb/tk/*.yaml) and step 5e's 106 planning scenarios in the form with no timeline fact
(configs/kitting/tk5e/mpb/off/*.yaml), 128 in all, each in the four conditions; then step 5e's 176 copies with a timeline
of their own (configs/kitting/tk5e/mpb/on/*.yaml not among the 106), intention-aware with context knowledge on only.
Each run file takes its source's room, setup, scenario and steps (the runner recomputes the cap) and states the default
settings, the condition's one option changed (R5's override sets the rest off at load):
  1 human-unaware                              human_aware: false
  2 intention-unaware                          intention_aware: false
  3 intention-aware, context knowledge off     context_knowledge: false
  4 intention-aware, context knowledge on      (the defaults)
Serials (K): run_001 onward, the four conditions of a scenario consecutive in the order above, the scenarios in the order
above (each set sorted by id); no setting in a name.
"""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
CFG = ROOT / "configs" / "kitting"
OUT = CFG / "tf1" / "measurement"
CONDITIONS = [("human-unaware", dict(human_aware=False)), ("intention-unaware", dict(intention_aware=False)),
              ("intention-aware, context knowledge off", dict(context_knowledge=False)),
              ("intention-aware, context knowledge on", {})]


def source(p):
    c = yaml.safe_load(open(p))
    return {k: c[k] for k in ("domain", "layout", "setup", "scenario", "steps")}


def write(n, src, origin, label, change):
    run = dict(src, human_aware=True, intention_aware=True, assignment_knowledge=True, context_knowledge=True,
               strategy="single_task", gate_strategy="none", cost_strategy="realized", separation_stop=False,
               test_level=0.05)
    run.update(change)
    d = OUT / src["scenario"]
    d.mkdir(parents=True, exist_ok=True)
    text = (f"# The measurement of T-F part 1 (not a baseline): {src['scenario']}, {label}. From {origin}.\n"
            f"# Run: analysis/instruments/mpb/run_set.sh kitting -o analysis/kitting/tf1/measurement <this file>\n\n"
            + yaml.safe_dump(run, sort_keys=False))
    (d / f"run_{n:03d}.yaml").write_text(text)


if __name__ == "__main__":
    four = sorted((CFG / "mpb").glob("*.yaml")) + sorted((CFG / "mpb" / "tk").glob("*.yaml")) + \
        sorted((CFG / "tk5e" / "mpb" / "off").glob("*.yaml"))
    plain = {p.name for p in (CFG / "tk5e" / "mpb" / "off").glob("*.yaml")}
    copies = sorted(p for p in (CFG / "tk5e" / "mpb" / "on").glob("*.yaml") if p.name not in plain)
    assert (len(four), len(copies)) == (128, 176), (len(four), len(copies))
    n = 0
    for p in four:
        for label, change in CONDITIONS:
            n += 1
            write(n, source(p), p.relative_to(ROOT), label, change)
    for p in copies:
        n += 1
        write(n, source(p), p.relative_to(ROOT), CONDITIONS[3][0], CONDITIONS[3][1])
    print(f"{n} run files in {OUT.relative_to(ROOT)}")
