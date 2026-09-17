"""
mesa_sim/run_mesa.py

PURPOSE:
    Entry point for the Mesa simulation.
    Supports two modes:
        1. Headless — runs N steps, no visualization (for testing/experiments)
        2. Visualization — Solara + Plotly interactive interface

USAGE:
    # Headless (default, uses configs/experiment.yaml):
    python mesa_sim/run_mesa.py

    # Headless with domain override:
    python mesa_sim/run_mesa.py --domain dock_loading

    # Headless with full overrides:
    python mesa_sim/run_mesa.py --domain dock_loading --scenario scenario_11 --steps 400

    # Visualization (uses configs/experiment.yaml):
    solara run mesa_sim/run_mesa.py

    # Visualization with domain override:
    solara run mesa_sim/run_mesa.py -- --domain dock_loading

WHAT THIS MODULE DOES:
    - Loads configs/experiment.yaml as default run configuration
    - Accepts CLI args to override individual fields (domain, scenario, steps, etc.);
      an unknown flag or yaml key, or a value of the wrong kind, stops the run
    - Looks up domain registry to resolve string names to Python objects
    - Instantiates SimModel with chosen domain + scenario
    - Either runs headless loop or launches SolaraViz

WHAT THIS MODULE DOES NOT DO:
    - No simulation logic — all in sim_model.py and sim_agents.py
    - No visualization logic — that belongs in mesa_sim/viz/

ROS EQUIVALENT:
    ros_sim/run_ros.py — same experiment.yaml, different simulator instantiation.
"""

import argparse
import logging
import sys
import yaml
import numpy as np
from pathlib import Path

# Ensure project root is on path when run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

# makes mesa_fork importable directly
sys.path.insert(0, str(Path(__file__).parent))  

from mesa_sim.sim_model import SimModel
# from domains.kitting.registry import register_kitting_domain
# from domains.kitting.scenarios import scenario_11 as kitting_scenario_11
# from domains.dock_loading.registry import register_dock_loading_domain
# from domains.dock_loading.scenarios import scenario_10 as dock_scenario_10, scenario_11 as dock_scenario_11

from domains.kitting.registry import domain_config as kitting_config
from domains.dock_loading.registry import domain_config as dock_config

# ============================================================================
# Logging setup
# ============================================================================
import logging
from datetime import datetime
from pathlib import Path
Path("logs").mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"logs/run_{timestamp}.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler(log_filename, mode="w"),
        logging.StreamHandler(),  # still prints to terminal
    ]
)


# =============================================================================
# Domain registry
# Maps domain name strings (from experiment.yaml or CLI) to Python objects.
# Add one entry here when adding a new domain.
# =============================================================================


DOMAIN_REGISTRY = {
    "kitting":      kitting_config,
    "dock_loading": dock_config,
}


# =============================================================================
# Experiment config loader
# =============================================================================

EXPERIMENT_CONFIG_PATH = "configs/experiment.yaml"

GATE_STRATEGIES = ("none", "b2a", "b2b")
COST_STRATEGIES = ("realized", "plain")
BOOL_OPTIONS = ("assignment_prior", "separation_stop")

def load_experiment(experiment_path: str, overrides: dict) -> dict:
    """
    Load experiment.yaml and apply CLI overrides.
    CLI overrides take precedence over file values.
    `overrides` holds one entry per CLI flag (None when not given); the flags
    are the run options, so a yaml key that is not one of them is an error
    rather than a field nothing reads. File values are checked like the flags
    are: a strategy outside its choices, or a switch that is not a yaml
    boolean (`"false"` is a string, and bool("false") is True), stops the run.
    """
    with open(experiment_path, "r") as f:
        config = yaml.safe_load(f)
    unknown = sorted(set(config) - set(overrides))
    if unknown:
        raise ValueError(
            f"{experiment_path}: unknown keys {unknown}. "
            f"Run options: {sorted(overrides)}"
        )
    config.update({k: v for k, v in overrides.items() if v is not None})
    for key, choices in (("gate_strategy", GATE_STRATEGIES), ("cost_strategy", COST_STRATEGIES)):
        if key in config and config[key] not in choices:
            raise ValueError(f"{key}={config[key]!r}: expected one of {list(choices)}")
    for key in BOOL_OPTIONS:
        if key in config and not isinstance(config[key], bool):
            raise ValueError(f"{key}={config[key]!r}: expected true or false")
    return config


# =============================================================================
# CLI argument parser
# =============================================================================

def _bool_arg(value: str) -> bool:
    """argparse type for the true/false override flags. Needed because bool('false')
    is True — argparse would otherwise accept any string as True."""
    if value.lower() in ("true", "1", "yes"):
        return True
    if value.lower() in ("false", "0", "no"):
        return False
    raise argparse.ArgumentTypeError(f"expected true/false, got '{value}'")


# `solara run mesa_sim/run_mesa.py -- --domain ...`: solara's own arguments come
# first in sys.argv, this script's follow the '--'.
_UNDER_SOLARA = "solara" in Path(sys.argv[0]).parts


def _script_argv() -> list:
    """The command-line arguments meant for this script: everything after the
    script name headless (a bare '--' dropped), only what follows '--' under
    solara (nothing when there is none)."""
    argv = sys.argv[1:]
    if _UNDER_SOLARA:
        return argv[argv.index("--") + 1:] if "--" in argv else []
    return [a for a in argv if a != "--"]


def parse_user_args():
    """Strict: an unknown or misspelled flag exits with an error, so a run never
    falls back silently to the yaml value of the option it meant to set."""
    parser = argparse.ArgumentParser(description="Run TeamRob Mesa simulation")
    parser.add_argument("--experiment",  type=str,  default=EXPERIMENT_CONFIG_PATH)
    parser.add_argument("--domain",      type=str,  default=None, help="Domain name override (e.g. kitting, dock_loading)")
    parser.add_argument("--layout", type=str, default=None, help="Layout name override (e.g. env_layout1)")
    parser.add_argument("--scenario",    type=str,  default=None, help="Scenario ID override (e.g. scenario_11)")
    parser.add_argument("--steps",       type=int,  default=None, help="Number of steps override for headless run")
    parser.add_argument("--assignment_prior", type=_bool_arg, default=None, help="Assignment-prior override: true/false")
    parser.add_argument("--gate_strategy", type=str, default=None, choices=GATE_STRATEGIES, help="MetaPlanner B2 gate strategy override")
    parser.add_argument("--cost_strategy", type=str, default=None, choices=COST_STRATEGIES, help="MetaPlanner B3 cost strategy override")
    parser.add_argument("--separation_stop", type=_bool_arg, default=None, help="Execution-time separation stop override: true/false")
    return parser.parse_args(_script_argv())


def load_user_config() -> dict:
    """The run configuration: the experiment file the CLI names, every flag given overriding it."""
    user_args = parse_user_args()
    overrides = {k: v for k, v in vars(user_args).items() if k != "experiment"}
    return load_experiment(user_args.experiment, overrides)



# =============================================================================
# Model factory — shared by headless and Solara
# =============================================================================
def resolve_model_params(user_config: dict) -> dict:
    '''
    Resolves user config to domain, layout, and scenario objects, and returns
    SimModel's keyword arguments. Used by both the headless factory and the
    Solara page, so a name the registry does not have fails the same way on both.
    Steps:
        1. Look up domain in DOMAIN_REGISTRY
        2. Look up layout in domain["layouts"]
        3. Look up scenario in layout["scenarios"]
    '''
    # --------- domain ---------
    domain_name = user_config["domain"]
    if domain_name not in DOMAIN_REGISTRY:
        raise ValueError(
            f"Unknown domain '{domain_name}'. "
            f"Available: {list(DOMAIN_REGISTRY.keys())}"
        )
    domain = DOMAIN_REGISTRY[domain_name]

    # --------- layout ---------
    layout_name = user_config["layout"]
    if layout_name not in domain["layouts"]:
        raise ValueError(
            f"Unknown layout '{layout_name}' for domain '{domain_name}'. "
            f"Available: {list(domain['layouts'].keys())}"
        )
    layout = domain["layouts"][layout_name]

    # --------- scenario ---------
    scenario_id = user_config["scenario"]
    if scenario_id not in layout["scenarios"]:
        raise ValueError(
            f"Unknown scenario '{scenario_id}' for layout '{layout_name}'. "
            f"Available: {list(layout['scenarios'].keys())}"
        )
    scenario = layout["scenarios"][scenario_id]

    return {
        "scenario":         scenario,
        "register_fn":      domain["register_fn"],
        "env_layout_path":  layout["path"],
        "assignment_prior": bool(user_config.get("assignment_prior", False)),
        "gate_strategy":    user_config.get("gate_strategy", "none"),
        "cost_strategy":    user_config.get("cost_strategy", "realized"),
        "separation_stop":  bool(user_config.get("separation_stop", False)),
    }


def _make_domain_model() -> SimModel:
    '''Parses the CLI, loads experiment.yaml, and instantiates SimModel from the resolved config.'''
    return SimModel(**resolve_model_params(load_user_config()))

# =============================================================================
# Headless runner
# =============================================================================

def _min_separation_over_tick(r0, r1, h0, h1) -> float:
    """
    The minimum robot–human distance over one tick when the robot moves in a
    straight line from r0 to r1 and the human from h0 to h1, simultaneously.
    The difference D(t) = (r0 − h0) + t ((r1 − h1) − (r0 − h0)) is affine in
    t ∈ [0, 1], so |D| is minimised at the clamped projection of the origin
    onto that segment — closed form, no sampling. A measure (TODO-79), not a
    behaviour: nothing reads it back.
    """
    dx0, dy0 = r0[0] - h0[0], r0[1] - h0[1]
    ex, ey = (r1[0] - h1[0]) - dx0, (r1[1] - h1[1]) - dy0
    ee = ex * ex + ey * ey
    t = 0.0 if ee == 0.0 else min(1.0, max(0.0, -(dx0 * ex + dy0 * ey) / ee))
    return float(np.hypot(dx0 + t * ex, dy0 + t * ey))


def run_headless():
    config = load_user_config()

    n_steps = config["steps"]
    logging.info(f"[run_mesa] Starting headless run — "
          f"domain={config['domain']} layout={config['layout']} scenario={config['scenario']} steps={n_steps}")

    model = _make_domain_model()

    # Positions at the end of the previous tick, for the continuous minimum of
    # the [sep] measure below (TODO-79); the initial positions before step 0.
    prev_pos = {
        (rid, hid): (tuple(map(float, robot.pos)), tuple(map(float, human.pos)))
        for rid, robot in model.robots.items() for hid, human in model.humans.items()
    }

    for step in range(n_steps):
        model.step()
    
    # -----------------------
    # logging  
    # -------------------
        if step % 1 == 0: # keep logging every 2 steps to avoid log bloat
            for aid, human in model.humans.items():
                logging.info(f"  step: {step}: [{aid}] task={human.current_task} "
                      f"action={human.current_action} "
                      f"micro={human.current_microaction} "
                      f"pos={np.round(human.pos, 2)}")
            for aid, robot in model.robots.items():
                logging.info(f"  step: {step}: [{aid}] task={robot.current_task} "
                      f"action={robot.current_action} "
                      f"micro={robot.current_microaction} "
                      f"pos={np.round(robot.pos, 2)}")
            # Actual robot–human separation (T9): a measure only, so later tasks
            # can report how often and by how much execution falls below
            # min_separation. Nothing here reacts to this number; Mesa's
            # execution-time layer is the executor's separation stop (C, a run
            # option, default off), which reads the human's actual position
            # itself. `dist` samples the end-of-tick
            # positions; `min` (T10, TODO-79) is the continuous minimum over the
            # tick with both agents moving in a straight line from their
            # previous positions to these — the motion model realization
            # assumes — so a close pass between two samples is read at its
            # minimum, not at the nearer sample.
            for rid, robot in model.robots.items():
                for hid, human in model.humans.items():
                    r1 = tuple(map(float, robot.pos)); h1 = tuple(map(float, human.pos))
                    r0, h0 = prev_pos[(rid, hid)]
                    sep = float(np.hypot(r1[0] - h1[0], r1[1] - h1[1]))
                    logging.info(f"[sep] step={step} {rid}-{hid} dist={sep:.2f} "
                                 f"min={_min_separation_over_tick(r0, r1, h0, h1):.2f}")
                    prev_pos[(rid, hid)] = (r1, h1)

    logging.info("[run_mesa] Headless run complete.")
    
    return model


# =============================================================================
# Solara visualization entry point
# =============================================================================

# NOTE: solara cannot be wrapped in a run_solara() function 
# because it needs to be at the top level, module load time to properly register the page.

from mesa_sim.viz.space_drawer import space_drawer
from mesa_sim.viz.portrayal import agent_portrayal
from mesa_sim.mesa_fork.visualization import SolaraViz

_model_params = resolve_model_params(load_user_config())

# print(f"_model_params: {_model_params}")

page = SolaraViz(
    model_class=SimModel,
    model_params=_model_params,
    space_drawer=space_drawer,
    agent_portrayal=agent_portrayal,
    name="TeamRob Simulation",
    play_interval=5,
)



# =============================================================================
# CLI entry point
# =============================================================================

if __name__ == "__main__":
    if not _UNDER_SOLARA:
        run_headless()