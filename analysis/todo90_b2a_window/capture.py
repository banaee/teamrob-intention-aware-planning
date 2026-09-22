"""capture.py <out.json> <run_mesa args...> — (TODO-90) runs mesa_sim/run_mesa.py unchanged, recording for every
realize() call made inside MetaPlanner.update() of robot_0: the tick, which block called it (B2 when the plan has
the executing task alone and the call comes from _is_current_task_plausible, else B3), the robot's realized
segments, the human projection's segments, δ and T_h, all on the decision's projection clock. Writes nothing to
the log."""
import json, runpy, sys, traceback
from pathlib import Path
REPO = Path.cwd()
sys.path.insert(0, str(REPO))
import shared.meta_planner as M

out, sys.argv = sys.argv[1], [str(REPO / "mesa_sim/run_mesa.py")] + sys.argv[2:]
rec, st = [], {"step": -1}

def segs(ss):
    return [[list(s.start_pos), list(s.end_pos), s.start_step, s.end_step] for s in ss]

_realize = M.realize
def realize(plan, human_plan, min_separation, decision_step):
    r = _realize(plan, human_plan, min_separation, decision_step)
    caller = "B2" if any(f.name == "_is_current_task_plausible" for f in traceback.extract_stack()) else "B3"
    hs = [s for e in human_plan.entries for s in e.segments] if human_plan is not None else []
    rec.append({"step": st["step"], "block": caller, "task": plan.task_queue, "delta": r.cumulative_shifts,
                "T_h": r.horizon, "robot": segs(r.segments), "human": segs(hs)})
    return r
M.realize = realize

_trig = M.MetaPlanner.evaluate_triggers
def evaluate_triggers(self, belief, world, executor_state):
    st["step"] += 1
    return _trig(self, belief, world, executor_state)
M.MetaPlanner.evaluate_triggers = evaluate_triggers

try:
    runpy.run_path(sys.argv[0], run_name="__main__")
finally:
    json.dump(rec, open(out, "w"))
