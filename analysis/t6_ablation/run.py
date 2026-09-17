"""
run.py — run_mesa headless with the MetaPlanner's two policy parameters that have no run option set
in-process (T6): rho (B2 `b2a`'s bound) and min_separation (in cm, converted to the ratio the
MetaPlanner takes, min_separation_in_motion_ticks = cm / assumed_speed). Nothing in the code base
changes; the wrapper replaces the keyword defaults at construction, so the `[run]` header records the
values actually used, and the separation stop (which reads meta_planner.min_separation) follows the
same s. Unset variables leave the defaults (rho 0.5, 2.5 ticks = 50 cm).

    T6_RHO=0.25 T6_SEP_CM=70 PYTHONHASHSEED=0 python analysis/t6_ablation/run.py --domain kitting \\
        --layout env_layout2 --scenario scenario_20 --steps 300 --assignment_prior false \\
        --gate_strategy b2a --cost_strategy realized --separation_stop true
"""
import os, sys
sys.path.insert(0, os.getcwd())
from shared import meta_planner as _mp

_orig_init = _mp.MetaPlanner.__init__

def _init(self, *args, **kwargs):
    rho = os.environ.get("T6_RHO")
    sep_cm = os.environ.get("T6_SEP_CM")
    if rho:
        kwargs["rho"] = float(rho)
    if sep_cm:
        projector = kwargs["projector"] if "projector" in kwargs else args[1]
        kwargs["min_separation_in_motion_ticks"] = float(sep_cm) / projector.assumed_speed
    _orig_init(self, *args, **kwargs)

_mp.MetaPlanner.__init__ = _init

from mesa_sim import run_mesa
run_mesa.run_headless()
