"""
analysis/t1b_realization/measure.py  (T1b — measurement only)

Drives the headless Mesa simulation for the eight sweep conditions (s00, s20,
s30, s40 × assignment prior off/on; scenario_10 stays dropped, TODO-52) with
the robot's MetaPlanner and Projector instrumented FROM OUTSIDE: instance-level
wrappers on the live objects, `shared/` untouched, no decision changed. The
wrappers are T1's (analysis/t1_conflict_measurement/measure.py), minus the
ConflictPoint cross-check. At every fired trigger it records:

  - the trigger decision, belief, executor state, world positions / holdings
  - the human projection (segments + phase-labelled actions) and its
    admission reason
  - every candidate projection B3 built (segments + actions), its cost, and
    the logged feasible / min_dist
  - a COUNTERFACTUAL human projection for triggers whose projection was NOT
    admitted (none(below_theta) / none(unknown)), built after update()
    returned — side-effect free (Projector.project reads world/belief only;
    verified by the byte-identical instrumented log, see REPORT.md)
  - the human's actual scripted task at that tick (analysis-side ground truth
    the robot never sees)

Realization is NOT done here — realize.py / analyze.py consume captures.json.
Domain interpretation (approach / pick-up / carry / placement / return) lives
in this analysis directory, never in shared/.

Also writes an instrumented log per condition in run_mesa's exact format so it
can be diffed byte-for-byte against the T5 baselines.

Usage (PYTHONHASHSEED=0 is mandatory, TODO-42):
    PYTHONHASHSEED=0 python analysis/t1b_realization/measure.py [--out DIR]
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))  # makes mesa_fork importable, as run_mesa.py does

from mesa_sim.sim_model import SimModel                     # noqa: E402
from domains.kitting.registry import domain_config          # noqa: E402
from shared.types import task_instance_key                  # noqa: E402
from shared.recognizer import UNKNOWN                       # noqa: E402


CONDITIONS = [
    # name,      layout,        scenario,      steps, assignment_prior   (analysis/i3_phase_model/sweep.sh)
    ("s00_off", "env_layout0", "scenario_00", 300, False),
    ("s00_on",  "env_layout0", "scenario_00", 300, True),
    ("s20_off", "env_layout2", "scenario_20", 200, False),
    ("s20_on",  "env_layout2", "scenario_20", 200, True),
    ("s30_off", "env_layout3", "scenario_30", 200, False),
    ("s30_on",  "env_layout3", "scenario_30", 200, True),
    ("s40_off", "env_layout4", "scenario_40", 400, False),
    ("s40_on",  "env_layout4", "scenario_40", 400, True),
]


# =============================================================================
# Helpers: serialization and domain interpretation (analysis-side only)
# =============================================================================

def seg_to_dict(seg):
    return {
        "start_pos": [float(seg.start_pos[0]), float(seg.start_pos[1])],
        "start_step": float(seg.start_step),
        "end_pos": [float(seg.end_pos[0]), float(seg.end_pos[1])],
        "end_step": float(seg.end_step),
    }


def phase_labels(actions, model, holding_at_start):
    """
    Domain interpretation for the kitting domain, applied in the analysis
    script: label every planned action with a phase. Sequence-aware: a move_to
    a shelf while holding an item is the return leg of deliver_with_return.
    """
    labels = []
    held = holding_at_start
    for a in actions:
        name = a.action_name
        b = a.bindings
        target = b.get("?target")
        ttype = model.objects[target].type if target in model.objects else None
        if name == "move_to":
            if ttype == "item":
                lab = "approach_shelf"
            elif ttype == "kitting_table":
                lab = "carry_to_table" if held else "move_to_table_empty"
            elif ttype == "shelf":
                lab = "return_held_item" if held else "move_to_shelf_empty"
            else:
                lab = f"approach_{ttype}"
        elif name == "pick_up":
            lab = "pick_up"
            held = b.get("?item")
        elif name == "place":
            lab = "placement" if ttype == "kitting_table" else "return_placement"
            held = None
        elif name == "wait_at":
            lab = "wait"
        else:
            lab = name
        labels.append({"action": name, "target": target, "target_type": ttype,
                       "item": b.get("?item"), "phase": lab})
    return labels


def plan_to_dict(projection, model, holding_at_start):
    """One ProjectedPlan (single entry under single_task) → plain dict."""
    assert len(projection.entries) == 1, "single_task: exactly one entry expected"
    entry = projection.entries[0]
    actions = entry.abstract_plan.actions
    segs = entry.segments
    return {
        "task_queue": list(projection.task_queue),
        "total_estimated_cost": int(projection.total_estimated_cost),
        "estimated_duration": int(entry.estimated_duration),
        "n_actions": len(actions),
        "n_segments": len(segs),
        "one_segment_per_action": len(actions) == len(segs),
        "actions": phase_labels(actions, model, holding_at_start),
        "segments": [seg_to_dict(s) for s in segs],
    }


# =============================================================================
# One condition
# =============================================================================

def run_condition(name, layout, scenario, steps, prior, out_dir):
    domain = domain_config
    lay = domain["layouts"][layout]
    scen = lay["scenarios"][scenario]

    # ---- logging in run_mesa's exact format, to a per-condition file ------
    log_path = out_dir / "logs_instrumented" / f"{name}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    fh = logging.FileHandler(log_path, mode="w")
    fh.setFormatter(logging.Formatter("%(message)s"))
    root.addHandler(fh)
    root.setLevel(logging.INFO)
    logging.info(f"[run_mesa] Starting headless run — domain=kitting scenario={scenario} steps={steps}")

    model = SimModel(scenario=scen, register_fn=domain["register_fn"],
                     env_layout_path=lay["path"], assignment_prior=prior)
    robot = model.robots["robot_0"]
    mp = robot.meta_planner
    proj = robot.projector
    human_id = mp._human_agent_id
    human = model.humans[human_id]

    with open(ROOT / "mesa_sim" / "mesa_configs.yaml") as f:
        mesa_cfg = yaml.safe_load(f)["simulation"]
    with open(ROOT / lay["path"]) as f:
        layout_json = json.load(f)

    condition = {
        "name": name, "layout": layout, "scenario": scenario, "steps": steps,
        "assignment_prior": prior,
        "config": {
            "theta": mp._theta,
            "min_safe_distance": mp._min_safe_distance,
            "assumed_speed": proj._assumed_speed,
            "default_action_cost": proj._default_action_cost,
            "mesa_step_size": mesa_cfg["step_size"],
            "mesa_seconds_per_step": mesa_cfg["seconds_per_step"],
            "interference_spatial_resolution": mesa_cfg["interference_spatial_resolution"],
            "strategy": mp._strategy, "gate_strategy": mp._gate_strategy,
        },
        "layout_space": layout_json["space"],
        "object_positions": {oid: list(o.position) for oid, o in model.objects.items()},
        "object_types": {oid: o.type for oid, o in model.objects.items()},
        "human_script": [task_instance_key(t) for t in human.script],
        "robot_pool": [task_instance_key(t) for t in robot.assigned_tasks],
        "triggers": [],
        "wrapper_checks": {"projections_outside_update": 0},
    }

    # ---- instance-level wrappers (T1's) ------------------------------------
    state = {"cur": None, "in_update": False}

    orig_eval = mp.evaluate_triggers
    orig_uhp = mp.update_human_projection
    orig_update = mp.update
    orig_replan = mp._replan_tasks
    orig_detect = mp._detect_interference
    orig_project = proj.project

    def evaluate_triggers(belief, world, executor_state):
        dec = orig_eval(belief=belief, world=world, executor_state=executor_state)
        state["cur"] = {
            "step": int(model.schedule.steps),
            "trigger": dec.reason, "fired": dec.fired, "score": dec.score,
        }
        return dec

    def update_human_projection(belief, world):
        cur = state["cur"]
        result = orig_uhp(belief=belief, world=world)
        if belief.confidence < mp._theta:
            reason = "none(below_theta)"
        elif human_id is None:
            reason = "none(no_human)"
        elif belief.most_likely == UNKNOWN:
            reason = "none(unknown)"
        else:
            reason = "built" if result is not None else "none(unresolved)"
        cur.update({
            "confidence": belief.confidence,
            "most_likely": belief.most_likely,
            "distribution": dict(belief.distribution),
            "projection_reason": reason,
            "agent_positions": {a: list(p) for a, p in world.agent_positions.items()},
            "agent_holding": {a: st.holding for a, st in world.agent_states.items()},
            "human_actual_task": (task_instance_key(human.get_current_task_instance())
                                  if human.get_current_task_instance() is not None else None),
            "human_actual_action": human.current_action,
            "human_actual_micro": human.current_microaction,
            "human_script_index": human.script_index,
        })
        cur["_belief"] = belief
        cur["_world"] = world
        cur["human_projection"] = (plan_to_dict(result, model, world.agent_states[human_id].holding)
                                   if result is not None else None)
        return result

    def update(belief, world, executor_state, human_projection):
        cur = state["cur"]
        cur["robot_current_task"] = (task_instance_key(executor_state.current_task)
                                     if executor_state.current_task is not None else None)
        cur["robot_holding"] = executor_state.holding
        cur["candidates"] = []
        state["in_update"] = True
        try:
            result = orig_update(belief=belief, world=world, executor_state=executor_state,
                                 human_projection=human_projection)
        finally:
            state["in_update"] = False
        cur["winner"] = (task_instance_key(result.current_task)
                         if result.current_task is not None else None)
        cur["result_queue"] = [task_instance_key(t) for t in result.queue]
        return result

    def _replan_tasks(task_pool, belief, world, executor_state, human_projection):
        state["cur"]["task_pool"] = [task_instance_key(t) for t in task_pool]
        return orig_replan(task_pool=task_pool, belief=belief, world=world,
                           executor_state=executor_state, human_projection=human_projection)

    def project(ordering, world, agent_id, belief, start_step=0.0):
        p = orig_project(ordering, world, agent_id, belief, start_step=start_step)
        if state["in_update"] and agent_id == robot.unique_id:
            cur = state["cur"]
            cur["candidates"].append({
                "task": task_instance_key(ordering[0]),
                "is_current_task": cur["robot_current_task"] == task_instance_key(ordering[0]),
                "cost": int(p.total_estimated_cost),
                "projection": plan_to_dict(p, model, world.agent_states[agent_id].holding),
                "_obj": p,
            })
        elif not state["in_update"]:
            condition["wrapper_checks"]["projections_outside_update"] += 1
        return p

    def _detect_interference(robot_projection, human_projection):
        a = orig_detect(robot_projection, human_projection)
        cur = state["cur"]
        cand = next(c for c in reversed(cur["candidates"]) if c["_obj"] is robot_projection)
        cand["logged_feasible"] = bool(a.feasible)
        cand["logged_min_dist"] = min((c.distance for c in a.conflicts), default=None)
        return a

    mp.evaluate_triggers = evaluate_triggers
    mp.update_human_projection = update_human_projection
    mp.update = update
    mp._replan_tasks = _replan_tasks
    mp._detect_interference = _detect_interference
    proj.project = project

    # ---- run ---------------------------------------------------------------
    for step in range(steps):
        state["cur"] = None
        model.step()

        # replicate run_mesa.run_headless()'s per-step lines exactly
        for aid, h in model.humans.items():
            logging.info(f"  step: {step}: [{aid}] task={h.current_task} "
                         f"action={h.current_action} "
                         f"micro={h.current_microaction} "
                         f"pos={np.round(h.pos, 2)}")
        for aid, r in model.robots.items():
            logging.info(f"  step: {step}: [{aid}] task={r.current_task} "
                         f"action={r.current_action} "
                         f"micro={r.current_microaction} "
                         f"pos={np.round(r.pos, 2)}")

        cur = state["cur"]
        if cur and cur["fired"]:
            # counterfactual projection for NOT-admitted triggers — AFTER update()
            cur["counterfactual_human_projection"] = None
            cur["counterfactual_reason"] = None
            if cur.get("projection_reason", "").startswith("none(") and cur.get("_belief") is not None:
                b = cur["_belief"]
                if b.most_likely != UNKNOWN:
                    cf = proj.project_human(belief=b, world=cur["_world"],
                                            human_agent_id=human_id, recognizer=mp._recognizer)
                    if cf is not None:
                        cur["counterfactual_human_projection"] = plan_to_dict(
                            cf, model, cur["_world"].agent_states[human_id].holding)
                        cur["counterfactual_reason"] = "built_from_below_theta_most_likely"
                    else:
                        cur["counterfactual_reason"] = "unresolved"
                else:
                    cur["counterfactual_reason"] = "most_likely_is_unknown"
            for c in cur.get("candidates", []):
                c.pop("_obj", None)
            for k in ("_belief", "_world"):
                cur.pop(k, None)
            condition["triggers"].append(cur)

    logging.info("[run_mesa] Headless run complete.")
    fh.flush()
    return condition


def main():
    if os.environ.get("PYTHONHASHSEED") != "0":
        sys.exit("Run with PYTHONHASHSEED=0 (TODO-42: hypothesis order is otherwise nondeterministic).")
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).parent))
    args = ap.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    captures = {"conditions": []}
    for cond in CONDITIONS:
        print(f"running {cond[0]} ...", flush=True)
        captures["conditions"].append(run_condition(*cond, out_dir=out_dir))

    with open(out_dir / "captures.json", "w") as f:
        json.dump(captures, f, indent=1)
    print(f"wrote {out_dir / 'captures.json'}")


if __name__ == "__main__":
    main()
