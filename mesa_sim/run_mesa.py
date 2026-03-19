"""
mesa_sim/run_mesa.py

PURPOSE:
    Entry point for the Mesa simulation.
    Supports two modes:
        1. Headless — runs N steps, no visualization (for testing/experiments)
        2. Visualization — Solara + Plotly interactive interface

USAGE:
    # Headless (default):
    python mesa_sim/run_mesa.py

    # Headless with options:
    python mesa_sim/run_mesa.py --scenario scenario_01 --steps 200 --headless

    # Visualization:
    solara run mesa_sim/run_mesa.py

WHAT THIS MODULE DOES:
    - Parses CLI arguments
    - Instantiates FactoryModel with chosen scenario
    - Either runs headless loop or launches SolaraViz

WHAT THIS MODULE DOES NOT DO:
    - No simulation logic here — all in model.py and agents.py
    - No visualization logic here — that belongs in a future
      mesa_sim/visualization/ module (space drawer, agent portrayal)

VISUALIZATION (stub):
    SolaraViz wiring is stubbed — space_drawer and agent_portrayal
    are placeholders until mesa_sim/visualization/ is built.
    TODO: implement factory_space_drawer and factory_agent_portrayal
    mirroring the old factory_space_drawer.py + factory_portrayal.py

ROS EQUIVALENT:
    ros_sim/run_ros.py — launches the ROS node instead of Mesa loop.
    Both entry points instantiate the same shared cognitive components
    but drive them through different simulation loops.
"""

import argparse
import sys
from pathlib import Path

# Ensure project root is on path when run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from mesa_sim.sim_model import FactoryModel


# =============================================================================
# Default config
# =============================================================================

DEFAULT_SCENARIO = "scenario_01"
DEFAULT_STEPS = 100
DEFAULT_DOMAIN = "configs/domain1.json"
DEFAULT_SCENARIOS = "configs/scenarios.yaml"


# =============================================================================
# Headless runner
# =============================================================================

def run_headless(scenario_id: str, n_steps: int):
    """
    Run simulation without visualization.
    Useful for testing, debugging, and batch experiments.
    """
    print(f"[run_mesa] Starting headless run — scenario={scenario_id}, steps={n_steps}")

    model = FactoryModel(
        scenario_id=scenario_id,
        domain_path=DEFAULT_DOMAIN,
        scenarios_path=DEFAULT_SCENARIOS,
    )

    for step in range(n_steps):
        model.step()
        print(f"  step {step + 1}/{n_steps} — schedule steps: {model.schedule.steps}")

    print("[run_mesa] Headless run complete.")
    return model


# =============================================================================
# Solara visualization entry point
# =============================================================================

# These will be implemented in mesa_sim/visualization/ when that module exists
# TODO: implement factory_agent_portrayal
def _agent_portrayal_stub(agent):
    return {"color": "blue", "size": 10}


# TODO: implement factory_space_drawer using Plotly
# mirrors old visualization/factory_space_drawer.py
_space_drawer_stub = None


def _make_model():
    """Factory function for SolaraViz — creates fresh model instance."""
    return FactoryModel(
        scenario_id=DEFAULT_SCENARIO,
        domain_path=DEFAULT_DOMAIN,
        scenarios_path=DEFAULT_SCENARIOS,
    )


# Solara viz page — only instantiated when loaded by `solara run`, not by direct python execution
if __name__ != "__main__":
    try:
        from mesa_sim.viz.space_drawer import space_drawer
        from mesa_sim.viz.portrayal import agent_portrayal
        from mesa_sim.mesa_fork.visualization import SolaraViz

        page = SolaraViz(
            model_class=FactoryModel,
            model_params={"scenario_id": DEFAULT_SCENARIO},
            space_drawer=space_drawer,
            agent_portrayal=agent_portrayal,
            name="TeamRob Factory Simulation",
            play_interval=0.001,
        )
    except ImportError:
        page = None


# =============================================================================
# CLI entry point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Run TeamRob Mesa simulation")
    parser.add_argument(
        "--scenario", type=str, default=DEFAULT_SCENARIO,
        help=f"Scenario ID from scenarios.yaml (default: {DEFAULT_SCENARIO})"
    )
    parser.add_argument(
        "--steps", type=int, default=DEFAULT_STEPS,
        help=f"Number of steps to run in headless mode (default: {DEFAULT_STEPS})"
    )
    parser.add_argument(
        "--headless", action="store_true", default=True,
        help="Run without visualization (default: True)"
    )

    args = parser.parse_args()

    if args.headless:
        run_headless(scenario_id=args.scenario, n_steps=args.steps)
    else:
        print("[run_mesa] Visualization mode not yet implemented — run with solara.")
        print("  solara run mesa_sim/run_mesa.py")


if __name__ == "__main__":
    main()
