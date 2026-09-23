"""analysis/tc2c_scripts/play.py <n> [run_mesa flags...] — T-C2c play: runs play scenario n (1-22) of play.md.

The scripts are registered script examples in domains/kitting/scenarios.py (not measured fixtures); this only
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
    "7": ("env_layout9", "scenario_91"),   # change of mind before the pick-up, tables at the walls
    "8": ("env_layout9", "scenario_92"),   # wrong destination, tables at the walls
    "9": ("env_layout9", "scenario_93"),   # landmark walk and stay mid-carry, tables at the walls
    "10": ("env_layout4", "scenario_41"),  # coffee break, stay at the table, abandon after pick-up
    "11": ("env_layout2", "scenario_22"),  # landmark stay after pick-up
    "12": ("env_layout2", "scenario_23"),  # table stay, robot converging
    "13": ("env_layout2", "scenario_24"),  # change of mind before the pick-up
    "14": ("env_layout3", "scenario_31"),  # change of mind after the pick-up (the return)
    "15": ("env_layout3", "scenario_32"),  # free actions, then the deliveries
    "16": ("env_layout4", "scenario_42"),  # abandon after pick-up, to a corner holding the item
    "17": ("env_layout5", "scenario_51"),  # change of mind before the pick-up
    "18": ("env_layout5", "scenario_52"),  # landmark stay mid-carry
    "19": ("env_layout5", "scenario_53"),  # table stay after the deliveries, then coffee
    "20": ("env_layout7", "scenario_72"),  # coffee break, table stay, abandon
    "21": ("env_layout7", "scenario_73"),  # free actions, then the delivery
    "22": ("env_layout9", "scenario_94"),  # table stay, robot converging
}

layout, scenario = PLAY[sys.argv[1]]
sys.argv = ["run_mesa.py", "--domain", "kitting", "--layout", layout, "--scenario", scenario] + sys.argv[2:]
from mesa_sim.run_mesa import run_headless
run_headless()
