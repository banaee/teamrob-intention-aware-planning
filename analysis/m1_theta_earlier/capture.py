#!/usr/bin/env python3
"""
analysis/m1_theta_earlier/capture.py  (M1 — exploratory, measurement only)

T1b's instrumented capture (analysis/t1b_realization/measure.py, imported
unchanged) over the four M1 conditions: scenario_30 × assignment prior off/on ×
theta {0.75, 0.65}. Writes captures.json (every fired trigger with its belief,
admission reason, human projection and every candidate projection, all with
fractional Segments) plus a per-condition instrumented log in run_mesa's exact
format, so it can be diffed against the plain runs.

theta is forced the same way as in run_theta.py: MetaPlanner.__init__ wrapped in
this process, shared/ untouched.

Usage:  PYTHONHASHSEED=0 python analysis/m1_theta_earlier/capture.py [--out DIR]
"""

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))
sys.path.insert(0, str(ROOT / "analysis" / "t1b_realization"))

if os.environ.get("PYTHONHASHSEED") != "0":
    sys.exit("Run with PYTHONHASHSEED=0 (TODO-42).")

from shared.meta_planner import MetaPlanner          # noqa: E402

_orig_init = MetaPlanner.__init__
_theta = {"value": 0.75}


def _init(self, *args, **kwargs):
    assert len(args) <= 3, "MetaPlanner called with theta positionally — patch is unsafe"
    kwargs["theta"] = _theta["value"]
    _orig_init(self, *args, **kwargs)


MetaPlanner.__init__ = _init

import measure                                       # noqa: E402  (T1b's, unchanged)

# name, layout, scenario, steps, assignment_prior, theta
CONDITIONS = [
    ("s30_off_t075", "env_layout3", "scenario_30", 200, False, 0.75),
    ("s30_on_t075",  "env_layout3", "scenario_30", 200, True,  0.75),
    ("s30_off_t065", "env_layout3", "scenario_30", 200, False, 0.65),
    ("s30_on_t065",  "env_layout3", "scenario_30", 200, True,  0.65),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).parent))
    args = ap.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(ROOT)

    captures = {"conditions": []}
    for name, layout, scenario, steps, prior, theta in CONDITIONS:
        _theta["value"] = theta
        print(f"running {name} (theta={theta}) ...", flush=True)
        cond = measure.run_condition(name, layout, scenario, steps, prior, out_dir=out_dir)
        assert cond["config"]["theta"] == theta, f"theta not applied in {name}"
        cond["theta"] = theta
        captures["conditions"].append(cond)

    with open(out_dir / "captures.json", "w") as f:
        json.dump(captures, f, indent=1)
    print(f"wrote {out_dir / 'captures.json'}")


if __name__ == "__main__":
    main()
