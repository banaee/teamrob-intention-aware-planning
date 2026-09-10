"""
analysis/t1_conflict_measurement/measure.py  (T1 — measurement only)

Drives the headless Mesa simulation for the six T1 conditions with the robot's
MetaPlanner and Projector instrumented FROM OUTSIDE: instance-level wrappers
on the live objects, `shared/` untouched, no decision changed. At every fired
trigger it records what MetaPlanner received and produced:

  - the trigger decision, belief, executor state, world positions/holdings
  - the human projection (segments + actions) and its admission reason
  - every candidate projection B3 built (segments + actions), its cost,
    feasibility and logged min_dist, plus a cross-check of the analysis-side
    distance function against the ConflictPoints _detect_interference produced
  - a COUNTERFACTUAL human projection for triggers rejected as
    none(below_theta), built after update() returned (side-effect free by
    construction: Projector.project only reads world/belief; verified by the
    byte-identical log diff, see REPORT.md §Verification)
  - the human's actual scripted task at that tick (read from the HumanAgent —
    analysis-side ground truth the robot never sees)

Domain interpretation (which action is an approach / carry / placement /
return) lives HERE, never in shared/.

Also writes an instrumented log per condition in run_mesa's exact format so it
can be diffed byte-for-byte against the baseline, and a per-tick table
(belief, trigger, robot task/holding) parsed from that log for the θ-flip scan.

Usage (PYTHONHASHSEED=0 is mandatory, TODO-42):
    PYTHONHASHSEED=0 python analysis/t1_conflict_measurement/measure.py [--out DIR]
"""

import argparse
import json
import logging
import math
import os
import re
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


CONDITIONS = [
    # name,      layout,        scenario,      steps, assignment_prior
    ("s00_off", "env_layout0", "scenario_00", 300, False),
    ("s00_on",  "env_layout0", "scenario_00", 300, True),
    ("s10_off", "env_layout1", "scenario_10", 300, False),
    ("s10_on",  "env_layout1", "scenario_10", 300, True),
    ("s20_off", "env_layout2", "scenario_20", 200, False),
    ("s20_on",  "env_layout2", "scenario_20", 200, True),
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


def pos_at(segments, t):
    """Analysis-side position lookup on a head-to-tail Segment chain at step t."""
    for s in segments:
        if s.start_step <= t <= s.end_step:
            if s.end_step <= s.start_step:
                return s.start_pos
            f = (t - s.start_step) / (s.end_step - s.start_step)
            return (s.start_pos[0] + f * (s.end_pos[0] - s.start_pos[0]),
                    s.start_pos[1] + f * (s.end_pos[1] - s.start_pos[1]))
    return None


def crosscheck(robot_proj, human_proj, conflicts):
    """
    Compare the analysis-side distance function against the ConflictPoints the
    live _detect_interference() produced for this row:
      - evaluated AT the ConflictPoint sample steps, distances must agree exactly
      - min over integer steps vs. logged min_dist: differ only by sampling
    """
    rs = [s for e in robot_proj.entries for s in e.segments]
    hs = [s for e in human_proj.entries for s in e.segments]
    max_abs = 0.0
    n = 0
    for cp in conflicts:
        pr = pos_at(rs, cp.step)
        ph = pos_at(hs, cp.step)
        if pr is None or ph is None:
            continue
        d = math.hypot(pr[0] - ph[0], pr[1] - ph[1])
        max_abs = max(max_abs, abs(d - cp.distance))
        n += 1
    T = min(rs[-1].end_step, hs[-1].end_step)
    ints = []
    for t in range(0, int(math.floor(T)) + 1):
        pr, ph = pos_at(rs, t), pos_at(hs, t)
        ints.append(math.hypot(pr[0] - ph[0], pr[1] - ph[1]))
    logged_min = min((c.distance for c in conflicts), default=None)
    logged_argmin = min(conflicts, key=lambda c: c.distance).step if conflicts else None
    return {
        "n_conflict_points": len(conflicts),
        "n_points_compared": n,
        "max_abs_diff_at_cp_steps": max_abs,
        "logged_min_dist": logged_min,
        "logged_argmin_step": logged_argmin,
        "integer_step_min_d": min(ints) if ints else None,
        "integer_step_argmin": int(np.argmin(ints)) if ints else None,
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
            "strategy": mp._strategy, "gate_strategy": mp._gate_strategy,
        },
        "layout_space": layout_json["space"],
        "object_positions": {oid: list(o.position) for oid, o in model.objects.items()},
        "object_types": {oid: o.type for oid, o in model.objects.items()},
        "human_script": [task_instance_key(t) for t in human.script],
        "robot_pool": [task_instance_key(t) for t in robot.assigned_tasks],
        "triggers": [],
        "ticks": [],
        "wrapper_checks": {"projections_outside_update": 0},
    }

    # ---- instance-level wrappers -----------------------------------------
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
        cur["_human_projection_obj"] = result
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
        elif state["in_update"]:
            pass  # human projection is built before update(); nothing else expected here
        else:
            condition["wrapper_checks"]["projections_outside_update"] += 1
        return p

    def _detect_interference(robot_projection, human_projection):
        a = orig_detect(robot_projection, human_projection)
        cur = state["cur"]
        cand = next(c for c in reversed(cur["candidates"]) if c["_obj"] is robot_projection)
        cand["feasible"] = bool(a.feasible)
        cand["n_conflicts"] = len(a.conflicts)
        cand["logged_min_dist"] = min((c.distance for c in a.conflicts), default=None)
        cand["crosscheck"] = crosscheck(robot_projection, human_projection, a.conflicts)
        return a

    mp.evaluate_triggers = evaluate_triggers
    mp.update_human_projection = update_human_projection
    mp.update = update
    mp._replan_tasks = _replan_tasks
    mp._detect_interference = _detect_interference
    proj.project = project

    # ---- run ---------------------------------------------------------------
    for step in range(steps):
        pre_task = (task_instance_key(robot.current_task_instance)
                    if robot.current_task_instance is not None else None)
        pre_hold = robot.carrying
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
        tick = {
            "step": step,
            "trigger": cur["trigger"] if cur else None,
            "pre_task": pre_task, "pre_holding": pre_hold,
            "post_task": (task_instance_key(robot.current_task_instance)
                          if robot.current_task_instance is not None else None),
            "post_holding": robot.carrying,
            "human_actual_task": (task_instance_key(human.get_current_task_instance())
                                  if human.get_current_task_instance() is not None else None),
            "belief_most_likely": robot.belief.most_likely if robot.belief else None,
            "belief_confidence": robot.belief.confidence if robot.belief else None,
        }
        condition["ticks"].append(tick)

        if cur and cur["fired"]:
            # counterfactual projection for below-theta rejections — AFTER update()
            cur["counterfactual_human_projection"] = None
            if cur["projection_reason"] == "none(below_theta)":
                cf = proj.project_human(belief=cur["_belief"], world=cur["_world"],
                                        human_agent_id=human_id, recognizer=mp._recognizer)
                if cf is not None:
                    cur["counterfactual_human_projection"] = plan_to_dict(
                        cf, model, cur["_world"].agent_states[human_id].holding)
                    # same cross-check against the counterfactual, per candidate
                    for c in cur["candidates"]:
                        a = orig_detect(c["_obj"], cf)
                        c["counterfactual_logged_min_dist"] = min((x.distance for x in a.conflicts), default=None)
                        c["counterfactual_crosscheck"] = crosscheck(c["_obj"], cf, a.conflicts)
            for c in cur["candidates"]:
                c.pop("_obj", None)
            for k in ("_belief", "_world", "_human_projection_obj"):
                cur.pop(k, None)
            condition["triggers"].append(cur)

    logging.info("[run_mesa] Headless run complete.")
    fh.flush()

    # ---- per-tick belief series from the [IR] step= lines --------------------
    ir = {}
    with open(log_path) as f:
        for line in f:
            m = re.match(r"\[IR\] step=(\d+) most_likely=(\S+) confidence=([0-9.]+)", line)
            if m:
                ir[int(m.group(1))] = (m.group(2), float(m.group(3)))
    for t in condition["ticks"]:
        if t["step"] in ir:
            t["ir_most_likely"], t["ir_confidence"] = ir[t["step"]]
        else:
            t["ir_most_likely"], t["ir_confidence"] = None, None
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
