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
    - Instantiates SimModel with chosen scenario
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
import numpy as np

# Ensure project root is on path when run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from mesa_sim.sim_model import SimModel
from domains.kitting.scenarios import scenario_01

# =============================================================================
# Default config
# =============================================================================

DEFAULT_STEPS = 600
DEFAULT_ENV_LAYOUT = "domains/kitting/env_layout1.json"

SCENARIOS = {
    "scenario_01": scenario_01,
} 
DEFAULT_SCENARIO_ID = "scenario_01"


# =============================================================================
# Headless runner
# =============================================================================

def run_headless(scenario_id: str, n_steps: int):
    """
    Run simulation without visualization.
    Useful for testing, debugging, and batch experiments.
    """
    print(f"[run_mesa] Starting headless run — scenario={scenario_id}, steps={n_steps}")

    scenario  = SCENARIOS.get(scenario_id)
    if scenario is None:
        print(f"[run_mesa] ERROR: unknown scenario '{scenario_id}'. "
              f"Available: {list(SCENARIOS.keys())}")
        return None

    model = SimModel(
        scenario=scenario,
        env_layout_path=DEFAULT_ENV_LAYOUT,
    )

    for step in range(n_steps):
        model.step()
        # print(f"  step {step + 1}/{n_steps} — schedule steps: {model.schedule.steps}")
        # only for diagnostic purposes — print agent states every 10 steps
        if step % 10 == 0:
            for aid, human in model.humans.items():
                print(f"  [{aid}] task={human.current_task} action={human.current_action} micro={human.current_microaction} pos={np.round(human.pos, 2)}")
            for aid, robot in model.robots.items():
                print(f"  [{aid}] task={robot.current_task} action={robot.current_action} micro={robot.current_microaction} pos={np.round(robot.pos, 2)}")

    print("[run_mesa] Headless run complete.")
    return model



# =============================================================================
# Solara visualization entry point
# =============================================================================

from mesa_sim.viz.space_drawer import space_drawer
from mesa_sim.viz.portrayal import agent_portrayal
from mesa_sim.mesa_fork.visualization import SolaraViz

page = SolaraViz(
    model_class=SimModel,
    model_params={"scenario": SCENARIOS[DEFAULT_SCENARIO_ID]},
    space_drawer=space_drawer,
    agent_portrayal=agent_portrayal,
    name="TeamRob Factory Simulation",
    # play_interval=150,  # means about 6 steps per second.
    play_interval=5,  # means about 6 steps per second.
)


# =============================================================================
# CLI entry point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Run TeamRob Mesa simulation")
    parser.add_argument(
        "--scenario", type=str, default=DEFAULT_SCENARIO_ID,
        help=f"Scenario ID to run (default: {DEFAULT_SCENARIO_ID}). Available: {list(SCENARIOS.keys())}"
    )
    parser.add_argument(
        "--steps", type=int, default=DEFAULT_STEPS,
        help=f"Number of steps to run in headless mode (default: {DEFAULT_STEPS})"
    )
    args = parser.parse_args()
    run_headless(scenario_id=args.scenario, n_steps=args.steps)


if __name__ == "__main__":
    import sys
    if not any("solara" in arg for arg in sys.argv):
        main()
        
        
