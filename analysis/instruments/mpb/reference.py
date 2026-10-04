#!/usr/bin/env python3
"""
reference.py — the meta-planner test-bed's reference run (MPB-2, scenario 8; design_decisions.md, "The meta-planner
test-bed (MPB)"): the same setup, the same robot and pool as a scenario, without the human. A reference run, not a
scenario: it is not registered; the ScenarioConfig is built here from the scenario's own literal with the human agent
removed and the robot's `observes` emptied (no agent to observe), as analysis/irb/trajectory.py builds a
human-only one. It runs through the same SimModel, in-process, with the run file's options.

    reference.py <run file> <steps> <out.log> <out.json> [--strategy single_task|full_reorder]

The log holds every line the model emits (the run header, the robot's decisions) plus, per tick, the robot's line in
run_mesa.py's headless form, so the reference can be read as a run log is. out.json: per tick the robot's position and
microaction, the decision ticks ([meta] lines), the terminal tick and the completion tick (the world tick: the tick
after the robot's last release, when the terminal fact is first observable; CLAUDE.md, "Regression checking").

Why it loads and runs with no code change (the plan's control fact, confirmed by running it here):
shared/types.py ScenarioConfig.__post_init__ needs reference layouts only; mesa_sim/sim_model.py _spawn_agents gives
observed_id None for an empty `observes`, and _load_human_scripts skips non-humans; RobotAgent.observe_initial returns
with no human, step() builds no observation and hands the meta-planner the dummy belief; MetaPlanner.
update_human_projection refuses (below theta) and, with no human_agent_id, builds no fallback.
"""
import dataclasses
import json
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / "mesa_sim")]

import numpy as np
import yaml
from shared.types import ScenarioConfig
import importlib
from mesa_sim.sim_model import SimModel


class Collect(logging.Handler):
    def __init__(self):
        super().__init__()
        self.lines = []

    def emit(self, record):
        self.lines.append(record.getMessage())


def reference_scenario(scenario: ScenarioConfig) -> ScenarioConfig:
    """The scenario's robot alone: the human agent removed, the robot's `observes` emptied."""
    robots = [dataclasses.replace(a, observes=[]) for a in scenario.agents if a.agent_type == "robot"]
    return ScenarioConfig(id=scenario.id, description=f"reference run of {scenario.id}: its robot alone",
                          agents=robots, setup=scenario.setup, reference_layouts=scenario.reference_layouts)


def run(run_file, steps, strategy):
    cfg = yaml.safe_load(open(run_file))
    domain_config = importlib.import_module(f"domains.{cfg['domain']}.registry").domain_config   # since the sort
    scenario = domain_config["scenarios"][cfg["scenario"]]
    layout = cfg.get("layout") or scenario.reference_layouts[0]
    collect = Collect()
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(collect)
    logging.getLogger("rec").propagate = False
    m = SimModel(scenario=reference_scenario(scenario), register_fn=domain_config["register_fn"],
                 state_declarations=domain_config["states"],
                 task_model_schemas=domain_config["task_model"], layout_path=domain_config["layouts"][layout],
                 setup_path=domain_config["setups"][scenario.setup],
                 assignment_knowledge=bool(cfg["assignment_knowledge"]), strategy=strategy,
                 gate_strategy=cfg["gate_strategy"], cost_strategy=cfg["cost_strategy"],
                 separation_stop=bool(cfg["separation_stop"]), test_level=float(cfg["test_level"]),
                 context_knowledge=bool(cfg["context_knowledge"]))
    robot = next(iter(m.robots.values()))
    ticks = []
    for t in range(steps):
        m.step()
        logging.info(f"  step: {t}: [{robot.unique_id}] task={robot.current_task} action={robot.current_action} "
                     f"micro={robot.current_microaction} pos={np.round(robot.pos, 2)}")
        ticks.append(dict(tick=t, x=float(robot.pos[0]), y=float(robot.pos[1]), micro=robot.current_microaction))
    root.removeHandler(collect)
    releases = [r["tick"] for r in ticks if r["micro"] == "release"]
    decisions = [int(l.split("step=")[1].split()[0]) for l in collect.lines if l.startswith("[meta] step=")]
    terminal = next((int(l.split("step=")[1].split()[0]) for l in collect.lines
                     if l.startswith("[meta] step=") and l.endswith("all tasks complete")), None)
    return collect.lines, dict(scenario=scenario.id, layout=layout, strategy=strategy, steps=steps, ticks=ticks,
                               decisions=decisions, terminal=terminal,
                               completion=None if not releases or terminal is None else releases[-1] + 1)


if __name__ == "__main__":
    run_file, steps, out_log, out_json = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    strategy = sys.argv[sys.argv.index("--strategy") + 1] if "--strategy" in sys.argv else "single_task"
    lines, result = run(run_file, steps, strategy)
    Path(out_log).write_text("\n".join(lines) + "\n")
    json.dump(result, open(out_json, "w"))
    print(f"{result['scenario']} reference ({strategy}): terminal {result['terminal']}, completion (world tick) "
          f"{result['completion']}, decisions {result['decisions']}")
