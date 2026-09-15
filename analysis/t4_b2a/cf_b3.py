#!/usr/bin/env python3
"""
cf_b3.py — the B3 counterfactual at every B2 continue (T4).

Runs one condition headless under a B2 gate strategy (default b2a). Whenever B2 CONTINUES the
current task, B3 (`_replan_tasks`) is also run on the same inputs with logging disabled and the
queue restored afterwards, and one line is logged:
    [cf-b3] step=<t> current=<task> b3_winner=<task> pool=<n> b3_would_switch=<bool>
Nothing else is patched: the decision taken is B2's, so the run is the ordinary gated run plus
those lines. stages.sh checks that (the regression greps plus [meta-b2] and [hold], in order,
identical to the plain run's log).

Usage (repo root, PYTHONHASHSEED=0):
    python analysis/t4_b2a/cf_b3.py <layout> <scenario> <prior true|false> <steps> <out.log> [gate_strategy]
"""
import logging, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))  # the vendored fork imports as mesa_fork, as run_mesa.py arranges
import numpy as np
from mesa_sim.sim_model import SimModel
from domains.kitting.registry import domain_config
from shared.meta_planner import MetaPlanner
from shared.types import task_instance_key

layout, scenario, prior, steps, out = sys.argv[1], sys.argv[2], sys.argv[3] == "true", int(sys.argv[4]), sys.argv[5]
gate = sys.argv[6] if len(sys.argv) > 6 else "b2a"
logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[logging.FileHandler(out, mode="w")])

lay = domain_config["layouts"][layout]
model = SimModel(scenario=lay["scenarios"][scenario], register_fn=domain_config["register_fn"],
                 env_layout_path=lay["path"], assignment_prior=prior, gate_strategy=gate)

_orig = MetaPlanner._is_current_task_plausible
def _patched(self, belief, world, executor_state, human_projection, task_pool):
    hold = _orig(self, belief, world, executor_state, human_projection, task_pool)
    if hold is not None:
        saved = list(self._queue)
        logging.disable(logging.CRITICAL)
        try:
            winner = task_instance_key(self._replan_tasks(
                task_pool=task_pool, belief=belief, world=world,
                executor_state=executor_state, human_projection=human_projection).current_task)
        except RuntimeError:
            winner = "RuntimeError"
        finally:
            logging.disable(logging.NOTSET)
            self._queue = saved
        current = task_instance_key(executor_state.current_task)
        logging.info(f"[cf-b3] step={int(model.schedule.steps)} current={current} b3_winner={winner} "
                     f"pool={len(task_pool)} b3_would_switch={winner != current}")
    return hold
MetaPlanner._is_current_task_plausible = _patched

for step in range(steps):
    model.step()
    # the same [sep] measure run_mesa.py logs, so the check below can include it
    for rid, robot in model.robots.items():
        for hid, human in model.humans.items():
            sep = float(np.hypot(robot.pos[0] - human.pos[0], robot.pos[1] - human.pos[1]))
            logging.info(f"[sep] step={step} {rid}-{hid} dist={sep:.2f}")
