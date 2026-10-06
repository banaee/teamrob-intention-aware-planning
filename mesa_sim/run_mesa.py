"""
mesa_sim/run_mesa.py

PURPOSE:
    Entry point for the Mesa simulation: the starts.
    Supports two modes:
        1. Headless — runs N steps, no visualization (for testing/experiments)
        2. Visualization — the solara-ui, Solara + Plotly interactive interface

USAGE:
    # Headless (default, uses configs/experiment.yaml):
    python mesa_sim/run_mesa.py

    # Headless with domain override:
    python mesa_sim/run_mesa.py --domain dock_loading

    # Headless with full overrides:
    python mesa_sim/run_mesa.py --domain dock_loading --scenario scenario_s03_01 --steps 400

    # Another run file, and one override of a fact of the run's artefacts (T-L stage 4):
    python mesa_sim/run_mesa.py --run my_run.yaml --override layout.shelf_2.position=-300,-300

    # Visualization (uses configs/experiment.yaml):
    solara run mesa_sim/run_mesa.py

    # Visualization with domain override:
    solara run mesa_sim/run_mesa.py -- --domain dock_loading

WHAT THIS MODULE DOES:
    - Headless: reads the run configuration from configs/experiment.yaml (or the run file
      --run names) and the flags, starts one sim-run of it, steps it N times and ends it
    - Under solara: imports the solara-ui's page (mesa_sim/viz/solara_page.py), which solara
      finds here; a headless start imports no Solara and nothing of mesa_sim/viz/
    - Re-exports the names of mesa_sim/run_config.py its callers used before T-viz 0.2

WHAT THIS MODULE DOES NOT DO:
    - No reading or building logic — mesa_sim/run_config.py (one definition for every start)
    - No log set-up or run-level line — mesa_sim/sim_run.py (the log pair is a sim-run's)
    - No simulation logic — all in sim_model.py and sim_agents.py
    - No visualization logic — that belongs in mesa_sim/viz/

ROS EQUIVALENT:
    ros_sim/run_ros.py — same experiment.yaml, different simulator instantiation.
"""

import sys
from pathlib import Path

# Ensure project root is on path when run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

# makes mesa_fork importable directly
sys.path.insert(0, str(Path(__file__).parent))

from mesa_sim.run_config import (  # noqa: F401 — re-exported for the callers of this module
    BOOL_OPTIONS, COST_STRATEGIES, DOMAIN_REGISTRY, EXPERIMENT_CONFIG_PATH, GATE_STRATEGIES, RUN_OPTIONS,
    STRATEGIES, UNDER_SOLARA, build_model, load_experiment, load_user_config, parse_user_args,
    resolve_model_params, resolve_triple, run_configuration,
)
from mesa_sim.sim_run import start_sim_run


# =============================================================================
# Headless runner
# =============================================================================

def run_headless():
    """One sim-run of the command line's run configuration, stepped `steps` times and
    ended; a start that fails still writes its log pair (sim_run.start_sim_run)."""
    sim_run = start_sim_run(load_user_config)
    for _ in range(sim_run.config["steps"]):
        sim_run.step()
    sim_run.end()
    return sim_run.model


# =============================================================================
# Solara visualization entry point
# =============================================================================

# Solara needs the page at the top level of the module it runs, at load time;
# it is imported under solara only, so a headless start never loads Solara.
if UNDER_SOLARA:
    from mesa_sim.viz.solara_page import Page  # noqa: F401


# =============================================================================
# CLI entry point
# =============================================================================

if __name__ == "__main__":
    if not UNDER_SOLARA:
        run_headless()
