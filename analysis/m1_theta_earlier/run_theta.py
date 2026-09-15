#!/usr/bin/env python3
"""
analysis/m1_theta_earlier/run_theta.py  (M1 — exploratory, measurement only)

Runs mesa_sim/run_mesa.py's headless loop unchanged, with MetaPlanner's `theta`
forced to a value given on the command line. The patch is INSTANCE-LEVEL in the
sense that matters: it wraps MetaPlanner.__init__ in this process only, so
shared/ is untouched on disk and nothing is committed with a changed default
(the T1b pattern). theta has exactly one live home — MetaPlanner.__init__'s
`theta` parameter, read in evaluate_triggers() (the theta_crossed test) and in
update_human_projection() (projection admission) — and mesa_sim/sim_agents.py
does not pass it, so the default governs every run. recognizer.py's
CONFIDENCE_THRESHOLD = 0.75 is dead code (no reader in shared/ or mesa_sim/).

Delegates to run_mesa.run_headless() rather than re-implementing its loop, so
the log format — including T9's per-tick [sep] line — is the real one and a
theta=0.75 run is byte-comparable with the T9 baselines.

Usage (PYTHONHASHSEED=0 is mandatory, TODO-42):
    PYTHONHASHSEED=0 python analysis/m1_theta_earlier/run_theta.py <theta> \
        --domain kitting --layout env_layout3 --scenario scenario_30 \
        --steps 200 --assignment_prior false
The log lands in logs/run_<timestamp>.log as usual; stages.sh copies it.
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))   # makes mesa_fork importable, as run_mesa.py does

if os.environ.get("PYTHONHASHSEED") != "0":
    sys.exit("Run with PYTHONHASHSEED=0 (TODO-42: hypothesis order is otherwise nondeterministic).")

theta = float(sys.argv[1])
sys.argv = [str(ROOT / "mesa_sim" / "run_mesa.py")] + sys.argv[2:]

from shared.meta_planner import MetaPlanner          # noqa: E402

_orig_init = MetaPlanner.__init__


def _init(self, *args, **kwargs):
    # sim_agents.py constructs MetaPlanner with keyword arguments only; guard
    # against theta arriving positionally, which would make this silently wrong.
    assert len(args) <= 3, "MetaPlanner called with theta positionally — patch is unsafe"
    kwargs["theta"] = theta
    _orig_init(self, *args, **kwargs)


MetaPlanner.__init__ = _init

os.chdir(ROOT)                                   # run_mesa writes logs/ relative to cwd
from mesa_sim import run_mesa                    # noqa: E402  (module-level logging + SolaraViz)

model = run_mesa.run_headless()
mp = model.robots["robot_0"].meta_planner
assert mp._theta == theta, f"theta not applied: {mp._theta}"
print(f"[m1] theta applied: {mp._theta}")
