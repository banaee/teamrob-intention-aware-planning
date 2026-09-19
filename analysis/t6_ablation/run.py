"""
run.py — run_mesa headless with the MetaPlanner's two policy parameters that have no run option set
in-process (T6): rho (B2 `b2a`'s bound) and min_separation (in cm; since T-A1 the MetaPlanner takes
it in world units, where T6 converted it to the former ratio cm / assumed_speed). Nothing in the code base
changes; the wrapper replaces rho's keyword default at construction and the body's supply of
min_separation (sim_agents._get_min_separation), so the `[run]` header records the values actually used
and names T6_SEP_CM as the separation's source, and the separation stop (which reads
meta_planner.min_separation) follows the same s. Unset variables leave the defaults (rho 0.5, 50 cm from mesa_configs.yaml).

    T6_RHO=0.25 T6_SEP_CM=70 PYTHONHASHSEED=0 python analysis/t6_ablation/run.py --domain kitting \\
        --layout env_layout2 --scenario scenario_20 --steps 300 --assignment_prior false \\
        --gate_strategy b2a --cost_strategy realized --separation_stop true
"""
import os, sys
sys.path.insert(0, os.getcwd())
from shared import meta_planner as _mp
from mesa_sim import run_mesa                  # first: it puts mesa_fork on the path
from mesa_sim import sim_agents as _sa

_orig_init = _mp.MetaPlanner.__init__

def _init(self, *args, **kwargs):
    rho = os.environ.get("T6_RHO")
    if rho:
        kwargs["rho"] = float(rho)
    _orig_init(self, *args, **kwargs)

_mp.MetaPlanner.__init__ = _init

if os.environ.get("T6_SEP_CM"):
    _sa._get_min_separation = lambda model: (float(os.environ["T6_SEP_CM"]), "env:T6_SEP_CM(analysis/t6_ablation/run.py)")

run_mesa.run_headless()
