"""analysis/tc2c_scripts/play.py <n> [run_mesa flags...] — T-C2c play: runs play scenario n (1-6) of play.md.

The six scripts are registered script examples in domains/kitting/scenarios.py (not measured fixtures); this only
maps play.md's numbering to them and calls the normal headless runner. Run from the repo root, e.g.

    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/tc2c_scripts/play.py 1 --steps 340 \\
        --assignment_prior true --strategy single_task --cost_strategy realized --gate_strategy none --separation_stop false

which is the same as run_mesa.py with --layout env_layout8 --scenario scenario_84.
"""
import sys
sys.path.insert(0, ".")

PLAY = {
    "1": ("env_layout8", "scenario_84"),   # change of mind before the pick-up
    "2": ("env_layout0", "scenario_02"),   # change of mind after the pick-up (the return)
    "3": ("env_layout8", "scenario_85"),   # wrong destination
    "4": ("env_layout0", "scenario_03"),   # landmark walk and stay mid-carry
    "5": ("env_layout1", "scenario_12"),   # coffee break, stay at the table, abandon after pick-up
    "6": ("env_layout0", "scenario_04"),   # free actions, then the one delivery
}

layout, scenario = PLAY[sys.argv[1]]
sys.argv = ["run_mesa.py", "--domain", "kitting", "--layout", layout, "--scenario", scenario] + sys.argv[2:]
from mesa_sim.run_mesa import run_headless
run_headless()
