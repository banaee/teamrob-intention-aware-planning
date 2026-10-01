"""capture.py <out.json> <run_mesa args...> — (ablation_task_committed) runs mesa_sim/run_mesa.py unchanged, recording per fired
decision of robot_0: step, trigger, winner key, hold, and the head entry's place-segment start (relative to
the decision step), from the robot projection of the winner's head made during that update(). Writes nothing
to the log."""
import json, runpy, sys
from pathlib import Path
REPO = Path.cwd()
sys.path.insert(0, str(REPO))
import shared.projection as P
import shared.meta_planner as M
from shared.types import task_instance_key

out, sys.argv = sys.argv[1], [str(REPO / "mesa_sim/run_mesa.py")] + sys.argv[2:]
rec, st = [], {"step": -1, "trig": None, "plans": []}

_proj = P.Projector.project
def project(self, ordering, world, agent_id, belief, start_step=0.0):
    plan = _proj(self, ordering, world, agent_id, belief, start_step)
    if agent_id.startswith("robot") and plan.entries:
        segs, n_a = plan.entries[0].segments, len(plan.entries[0].abstract_plan.actions)
        acts = [a.schema.name for a in plan.entries[0].abstract_plan.actions]
        stride = 2  # action + acknowledgement latency (L2), then one task-completion segment
        st["plans"].append((plan.task_queue[0], start_step, segs[stride * (n_a - 1)].start_step, acts))
    return plan
P.Projector.project = project

_trig = M.MetaPlanner.evaluate_triggers
def evaluate_triggers(self, belief, world, executor_state):
    d = _trig(self, belief, world, executor_state)
    st["step"] += 1; st["trig"] = d.reason; st["plans"] = []
    return d
M.MetaPlanner.evaluate_triggers = evaluate_triggers

_upd = M.MetaPlanner.update
def update(self, *a, **k):
    r = _upd(self, *a, **k)
    w = task_instance_key(r.current_task) if r.current_task is not None else None
    heads = [p for p in st["plans"] if p[0] == w]
    rec.append({"step": st["step"], "trigger": st["trig"], "winner": w, "hold": r.hold,
                "place_start": heads[0][2] - heads[0][1] if heads else None,
                "place_starts": sorted({round(p[2] - p[1], 6) for p in heads}),
                "actions": heads[0][3] if heads else None})
    return r
M.MetaPlanner.update = update

try:
    runpy.run_path(sys.argv[0], run_name="__main__")
finally:
    json.dump(rec, open(out, "w"), indent=0)
