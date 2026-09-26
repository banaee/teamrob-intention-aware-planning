"""
mesa_sim/list_scenarios.py

Lists every registered kitting scenario with its composition and its scenario
coverage (world/composition.scenario_composition), one line per human and
observing robot, on the layout it is registered under and the domain's
declared task model. Each scenario is loaded as a run loads it (SimModel: the
bindings check, the load-time replay, the robot's ObservingRobot); nothing is
stepped and no log is written.

Usage (from the repo root):
    PYTHONHASHSEED=0 python mesa_sim/list_scenarios.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))   # makes mesa_fork importable directly

from mesa_sim.sim_model import SimModel
from domains.kitting.registry import domain_config
from world.composition import scenario_composition


def main():
    for layout_name, layout in domain_config["layouts"].items():
        for scenario_id, scenario in layout["scenarios"].items():
            model = SimModel(scenario=scenario, register_fn=domain_config["register_fn"],
                             task_model_schemas=domain_config["task_model"], env_layout_path=layout["path"])
            pairs = [(h, r) for r in scenario.agents if r.agent_type == "robot"
                     for h in scenario.agents if h.agent_type == "human" and h.agent_id in r.observes]
            if not pairs:
                print(f"{scenario_id} {layout_name} no robot observes a human")
            for human_cfg, robot_cfg in pairs:
                composition, scenario_coverage = scenario_composition(human_cfg.scheduled_tasks,
                                                                      model.observing[robot_cfg.agent_id])
                print(f"{scenario_id} {layout_name} {human_cfg.agent_id} {robot_cfg.agent_id} "
                      f"scenario_coverage={scenario_coverage.value} {composition!r}")


if __name__ == "__main__":
    main()
