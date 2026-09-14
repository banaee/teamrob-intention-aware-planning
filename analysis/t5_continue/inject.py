#!/usr/bin/env python3
"""
inject.py — the continue-decision mechanism, isolated (T5 / TODO-43).

Runs one sweep condition headless and, on the chosen tick(s), makes evaluate_triggers()
report a fired trigger (reason "injected") if no real one fired. Everything downstream is
the real code path: update() re-decides from the live world, the planner re-decomposes,
the executor receives the plan. Nothing else is patched. The robot's per-tick
(action, microaction) is then printed for a window, so the tick on which the robot grasps,
releases or steps can be read against the same run with no injection.

Usage (from the repo root, PYTHONHASHSEED=0):
    python analysis/t5_continue/inject.py <layout> <scenario> <prior true|false> <steps> <window_lo> <window_hi> [inject_step ...]
e.g.
    PYTHONHASHSEED=0 python analysis/t5_continue/inject.py env_layout0 scenario_00 false 40 2 8 6
"""
import logging, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "mesa_sim"))  # the vendored fork imports as mesa_fork, as run_mesa.py arranges
from mesa_sim.sim_model import SimModel
from domains.kitting.registry import domain_config
from shared.meta_planner import MetaPlanner
from shared.types import TriggerDecision

layout, scenario, prior, steps, lo, hi = sys.argv[1], sys.argv[2], sys.argv[3] == "true", int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
inject = {int(s) for s in sys.argv[7:]}
tag = f"{scenario}_{'on' if prior else 'off'}_inject{'-'.join(str(s) for s in sorted(inject)) or 'none'}"
logging.basicConfig(level=logging.INFO, format="%(message)s",
                    handlers=[logging.FileHandler(Path(__file__).parent / f"{tag}.log", mode="w")])

lay = domain_config["layouts"][layout]
model = SimModel(scenario=lay["scenarios"][scenario], register_fn=domain_config["register_fn"],
                 env_layout_path=lay["path"], assignment_prior=prior)

_orig = MetaPlanner.evaluate_triggers
def _patched(self, belief, world, executor_state):
    d = _orig(self, belief, world, executor_state)
    if not d.fired and int(model.schedule.steps) in inject and executor_state.current_task is not None:
        return TriggerDecision(fired=True, reason="injected", score=1.0)
    return d
MetaPlanner.evaluate_triggers = _patched

rows = []
for step in range(steps):
    model.step()
    for aid, robot in model.robots.items():
        rows.append((step, robot.current_action, robot.current_microaction))
        logging.info(f"  step: {step}: [{aid}] action={robot.current_action} micro={robot.current_microaction} pos={robot.pos}")

print(f"== {tag}")
print("  " + "  ".join(f"{s}:{a}/{m}" for s, a, m in rows if lo <= s <= hi))
firsts = {}
for s, a, m in rows:
    if m in ("grasp", "release") and m not in firsts:
        firsts[m] = s
print(f"  first grasp tick={firsts.get('grasp')}  first release tick={firsts.get('release')}")
