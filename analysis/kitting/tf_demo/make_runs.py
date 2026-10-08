#!/usr/bin/env python3
"""
make_runs.py — writes the run files of the demo-day round of T-F (Hadi, 8 October 2026; README.md beside this file) into
configs/kitting/tf_demo/<scenario>/run_NNN.yaml: the 50 scenarios of env_setup_100 to env_setup_104 (generate.py), each
in seven runs, the conditions in the order below, the scenarios in id order; serials run_001 onward, no setting in a
name (decision 6). Fixed in every run: single_task, the default θ and min_separation (the body's), assignment knowledge
at its default (on), steps 2000 (the cap of decision 5; the runner is given it with -s).
  1 human-unaware                                       human_aware: false (R5 sets the stop off)
  2 intention-unaware, separation stop off              intention_aware: false
  3 intention-unaware, separation stop on               intention_aware: false, separation_stop: true
  4 intention-aware, context knowledge off, stop off    context_knowledge: false
  5 intention-aware, context knowledge off, stop on     context_knowledge: false, separation_stop: true
  6 intention-aware, context knowledge on, stop off     (the defaults)
  7 intention-aware, context knowledge on, stop on      separation_stop: true
"""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "configs" / "kitting" / "tf_demo"
STEPS = 2000
CONDITIONS = [
    ("human-unaware", dict(human_aware=False)),
    ("intention-unaware, separation stop off", dict(intention_aware=False)),
    ("intention-unaware, separation stop on", dict(intention_aware=False, separation_stop=True)),
    ("intention-aware, context knowledge off, separation stop off", dict(context_knowledge=False)),
    ("intention-aware, context knowledge off, separation stop on", dict(context_knowledge=False, separation_stop=True)),
    ("intention-aware, context knowledge on, separation stop off", {}),
    ("intention-aware, context knowledge on, separation stop on", dict(separation_stop=True)),
]


if __name__ == "__main__":
    n = 0
    for setup in range(100, 105):
        for j in range(1, 11):
            sid = f"scenario_s{setup}_{j:02d}"
            d = OUT / sid
            d.mkdir(parents=True, exist_ok=True)
            for label, change in CONDITIONS:
                n += 1
                run = dict(domain="kitting", layout="env_layout_100", setup=f"env_setup_{setup}", scenario=sid,
                           steps=STEPS, human_aware=True, intention_aware=True, assignment_knowledge=True,
                           context_knowledge=True, strategy="single_task", gate_strategy="none",
                           cost_strategy="realized", separation_stop=False, test_level=0.05)
                run.update(change)
                text = (f"# The demo-day round of T-F (not a baseline): {sid}, {label}.\n"
                        f"# Run: analysis/instruments/mpb/run_set.sh kitting -s {STEPS} -o analysis/kitting/tf_demo/runs "
                        f"<this file>\n\n" + yaml.safe_dump(run, sort_keys=False))
                (d / f"run_{n:03d}.yaml").write_text(text)
    print(f"{n} run files in {OUT.relative_to(ROOT)}")
