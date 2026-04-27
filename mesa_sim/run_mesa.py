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
    python mesa_sim/run_mesa.py --domain dock_loading --scenario scenario_01 --steps 400

    # Visualization (uses configs/experiment.yaml):
    solara run mesa_sim/run_mesa.py

    # Visualization with domain override:
    solara run mesa_sim/run_mesa.py -- --domain dock_loading

WHAT THIS MODULE DOES:
    - Loads configs/experiment.yaml as default run configuration
    - Accepts CLI args to override individual fields (domain, scenario, steps, etc.)
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
from domains.kitting.registry import register_kitting_domain
from domains.kitting.scenarios import scenario_01 as kitting_scenario_01
from domains.dock_loading.registry import register_dock_loading_domain
from domains.dock_loading.scenarios import scenario_00 as dock_scenario_00, scenario_01 as dock_scenario_01


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
    "kitting": {
        "register_fn":  register_kitting_domain,
        "layout_path":  "domains/kitting/env_layout1.json",
        "scenarios":    {"scenario_01": kitting_scenario_01},
    },
    "dock_loading": {
        "register_fn":  register_dock_loading_domain,
        "layout_path":  "domains/dock_loading/env_layout1.json",
        "scenarios":    {
            "scenario_00": dock_scenario_00,
            "scenario_01": dock_scenario_01
            },
    },
}




# =============================================================================
# Experiment config loader
# =============================================================================

EXPERIMENT_CONFIG_PATH = "configs/experiment.yaml"

def load_experiment(experiment_path: str, overrides: dict) -> dict:
    """
    Load experiment.yaml and apply CLI overrides.
    CLI overrides take precedence over file values.
    """
    with open(experiment_path, "r") as f:
        config = yaml.safe_load(f)
    config.update({k: v for k, v in overrides.items() if v is not None})
    return config


# =============================================================================
# CLI argument parser
# =============================================================================

# def parse_user_args():
#     parser = argparse.ArgumentParser(description="Run TeamRob Mesa simulation")
#     parser.add_argument("--experiment",  type=str,  default=EXPERIMENT_CONFIG_PATH,
#                         help="Path to experiment YAML config (default: configs/experiment.yaml)")
#     parser.add_argument("--domain",      type=str,  default=None,
#                         help="Domain name override (e.g. kitting, dock_loading)")
#     parser.add_argument("--layout",      type=int,  default=None,
#                         help="Layout number override (default: 1)")
#     parser.add_argument("--scenario",    type=str,  default=None,
#                         help="Scenario ID override (e.g. scenario_01)")
#     parser.add_argument("--steps",       type=int,  default=None,
#                         help="Number of steps override for headless run")
#     parser.add_argument("--planner",     type=str,  default=None,
#                         help="Planner variant override (e.g. basic, intention_aware)")
#     parser.add_argument("--recognizer",  type=str,  default=None,
#                         help="Recognizer variant override (e.g. uniform, bayesian)")
#     return parser.parse_known_args()[0]

def parse_user_args():
    parser = argparse.ArgumentParser(description="Run TeamRob Mesa simulation")
    parser.add_argument("--experiment",  type=str,  default=EXPERIMENT_CONFIG_PATH)
    parser.add_argument("--domain",      type=str,  default=None, help="Domain name override (e.g. kitting, dock_loading)")
    parser.add_argument("--layout",      type=int,  default=None, help="Layout number override (default: 1)")
    parser.add_argument("--scenario",    type=str,  default=None, help="Scenario ID override (e.g. scenario_01)")
    parser.add_argument("--steps",       type=int,  default=None, help="Number of steps override for headless run")
    parser.add_argument("--planner",     type=str,  default=None, help="Planner variant override (e.g. basic, intention_aware)")
    parser.add_argument("--recognizer",  type=str,  default=None, help="Recognizer variant override (e.g. uniform, bayesian)")
    argv = [a for a in sys.argv[1:] if a != '--']  # strip '--' separator
    return parser.parse_known_args(argv)[0]



# =============================================================================
# Model factory — shared by headless and Solara
# =============================================================================

def _make_domain_model() -> SimModel:
    user_args = parse_user_args()
    user_config = load_experiment(user_args.experiment, {
        "domain":     user_args.domain,
        "layout":     user_args.layout,
        "scenario":   user_args.scenario,
        "steps":      user_args.steps,
        "planner":    user_args.planner,
        "recognizer": user_args.recognizer,
    })

    # --------- domain arguments from config/CLI ---------
    domain_name = user_config["domain"]
    if domain_name not in DOMAIN_REGISTRY:
        raise ValueError(
            f"Unknown domain '{domain_name}'. "
            f"Available: {list(DOMAIN_REGISTRY.keys())}"
        )
    domain = DOMAIN_REGISTRY[domain_name]
    
    # --------- scenario arguments from config/CLI ---------
    scenario_id = user_config["scenario"]
    if scenario_id not in domain["scenarios"]:
        raise ValueError(
            f"Unknown scenario '{scenario_id}' for domain '{domain_name}'. "
            f"Available: {list(domain['scenarios'].keys())}"
        )
    scenario = domain["scenarios"][scenario_id]
    
    # --------- layout arguments from config/CLI ---------
    # TODO: use config["layout"] number to select layout path when multiple layouts exist
    layout_path = domain["layout_path"]


    return SimModel(
        scenario=scenario,
        register_fn=domain["register_fn"],
        env_layout_path=layout_path,
    )


# =============================================================================
# Headless runner
# =============================================================================

def run_headless():
    
    
    user_args = parse_user_args()
    user_config = load_experiment(user_args.experiment, {
        "domain":     user_args.domain,
        "layout":     user_args.layout,
        "scenario":   user_args.scenario,
        "steps":      user_args.steps,
        "planner":    user_args.planner,
        "recognizer": user_args.recognizer,
    })

    n_steps = user_config["steps"]
    logging.info(f"[run_mesa] Starting headless run — "
          f"domain={user_config['domain']} scenario={user_config['scenario']} steps={n_steps}")

    model = _make_domain_model()

    for step in range(n_steps):
        model.step()
        if step % 10 == 0:
            for aid, human in model.humans.items():
                logging.info(f"  [{aid}] task={human.current_task} "
                      f"action={human.current_action} "
                      f"micro={human.current_microaction} "
                      f"pos={np.round(human.pos, 2)}")
            for aid, robot in model.robots.items():
                logging.info(f"  [{aid}] task={robot.current_task} "
                      f"action={robot.current_action} "
                      f"micro={robot.current_microaction} "
                      f"pos={np.round(robot.pos, 2)}")

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

_user_args = parse_user_args()  # already uses parse_known_args()[0]
_user_config = load_experiment(_user_args.experiment, {
    "domain":     _user_args.domain,
    "layout":     _user_args.layout,
    "scenario":   _user_args.scenario,
    "steps":      _user_args.steps,
    "planner":    _user_args.planner,
    "recognizer": _user_args.recognizer,
})
_domain_args = DOMAIN_REGISTRY[_user_config["domain"]]
_model_params = {
    "scenario":        _domain_args["scenarios"][_user_config["scenario"]],
    "register_fn":     _domain_args["register_fn"],
    "env_layout_path": _domain_args["layout_path"],
}

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
    if not any("solara" in arg for arg in sys.argv):
        run_headless()