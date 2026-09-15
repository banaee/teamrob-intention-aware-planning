"""
analysis/i1_ir_audit/measure.py  (I1 — IR audit, measurement only)

Drives the headless Mesa simulation for the eight I1 conditions (s00/s10/s20/s30 ×
assignment_prior off/on) with the robot's IntentionRecognizer instrumented FROM
OUTSIDE: instance-level wrappers on the live object, `shared/` untouched, no
decision changed, no value altered. Every wrapper calls the original and records
what it received and what it returned. At every tick it captures:

  - the observation (microaction, position), the recognizer's own classification
    of it (discrete / moving / stationary, replicated from update()'s arithmetic on
    the same inputs), the leg state before and after the call
  - per hypothesis: which branch of _likelihood() answered (completion /
    progress / fallthrough), every helper's inputs and result (expected position
    and the branch that produced it, target zone, resolved completion predicate),
    the returned likelihood, the ω_context weight and which boost produced it
  - the held-item refutation set, the inadmissible set, the floor clamps in
    _finalize(), the evidence state and the output distribution
  - the human's actual state (script task, executor action index, action,
    microaction, holding — analysis-side ground truth the robot never sees) and
    the world predicates about the human
  - an EXTERNAL evaluation of every action's declared completion condition, for
    the human's live plan and for every hypothesis × method × step, against the
    same WorldState the recognizer saw — read-only, no effect on the run

Domain interpretation (what counts as a shelf, a table, a delivered item) lives
HERE, never in shared/.

Also writes an instrumented log per condition in run_mesa's exact format so it
can be diffed byte-for-byte against the baseline logs.

Usage (PYTHONHASHSEED=0 is mandatory, TODO-42):
    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/i1_ir_audit/measure.py [--out DIR]
"""

import argparse
import json
import logging
import math
import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))  # makes mesa_fork importable, as run_mesa.py does

from mesa_sim.sim_model import SimModel                                   # noqa: E402
from domains.kitting.registry import domain_config                        # noqa: E402
from shared.types import (                                                # noqa: E402
    task_instance_key, Predicate, Const, Var, ConditionSchema, ProcessCompletion,
)
from shared import recognizer as rec_mod                                  # noqa: E402
from shared import likelihood_functions as lf                             # noqa: E402


CONDITIONS = [
    # name,      layout,        scenario,      steps, assignment_prior
    ("s00_off", "env_layout0", "scenario_00", 300, False),
    ("s00_on",  "env_layout0", "scenario_00", 300, True),
    ("s10_off", "env_layout1", "scenario_10", 300, False),
    ("s10_on",  "env_layout1", "scenario_10", 300, True),
    ("s20_off", "env_layout2", "scenario_20", 200, False),
    ("s20_on",  "env_layout2", "scenario_20", 200, True),
    ("s30_off", "env_layout3", "scenario_30", 200, False),
    ("s30_on",  "env_layout3", "scenario_30", 200, True),
]


# =============================================================================
# Helpers (analysis-side only)
# =============================================================================

def pos_list(p):
    return None if p is None else [float(p[0]), float(p[1])]


def pred_str(p):
    return str(p)


def preds_about(world, agent_id):
    """Every world predicate whose first argument is agent_id, as strings, sorted."""
    return sorted(str(p) for p in world.predicates if p.args and p.args[0].value == agent_id)


def ground_completion(schema, hyp_bindings, agent_id, step):
    """
    Analysis-side grounding of one action's completion condition, using exactly
    the two sources the recognizer's _resolve_term_value() uses (hyp bindings and
    the step call's own Const bindings) plus the step call's Var bindings resolved
    through the hypothesis — i.e. what a task-level binding lookup would give.
    Returns (Predicate | None, reason).
    """
    if isinstance(schema.completion, ProcessCompletion):
        return None, "process_completion"
    if not isinstance(schema.completion, ConditionSchema):
        return None, "no_completion"
    # action-parameter -> value, from the step call
    step_vals = {}
    for pvar, term in step.bindings.items():
        if isinstance(term, Const):
            step_vals[pvar.name] = term.value
        elif isinstance(term, Var):
            if term.name in hyp_bindings:
                step_vals[pvar.name] = hyp_bindings[term.name]
            else:
                step_vals[pvar.name] = None  # derived var or otherwise unbound
    args = []
    for t in schema.completion.args:
        if isinstance(t, Const):
            args.append(t.value)
        elif t.name == "?agent":
            args.append(agent_id)
        elif t.name in step_vals and step_vals[t.name] is not None:
            args.append(step_vals[t.name])
        elif t.name in hyp_bindings:
            args.append(hyp_bindings[t.name])
        else:
            return None, f"unbound:{t.name}"
    return Predicate(schema.completion.name, tuple(Const(a) for a in args)), "grounded"


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
    rec = robot.recognizer
    mp = robot.meta_planner
    human_id = robot.observed_agent_id
    human = model.humans[human_id]
    knowledge = model.knowledge

    hyp_keys = [repr(h) for h in rec._hypotheses]
    condition = {
        "name": name, "layout": layout, "scenario": scenario, "steps": steps,
        "assignment_prior": prior,
        "constants": {
            "HIGH_LIKELIHOOD": lf.HIGH_LIKELIHOOD, "LOW_LIKELIHOOD": lf.LOW_LIKELIHOOD,
            "NEUTRAL_LIKELIHOOD": lf.NEUTRAL_LIKELIHOOD,
            "ZONE_BOOST": rec_mod.ZONE_BOOST, "TEMPERATURE_BOOST": rec_mod.TEMPERATURE_BOOST,
            "FATIGUE_BOOST": rec_mod.FATIGUE_BOOST, "HIGH_TEMP_THRESHOLD": rec_mod.HIGH_TEMP_THRESHOLD,
            "LONG_SHIFT_THRESHOLD": rec_mod.LONG_SHIFT_THRESHOLD,
            # recognizer.CONFIDENCE_THRESHOLD was deleted in September 2026 (it had no
            # reader; theta's one home is meta_planner.DEFAULT_THETA). The literal is the
            # value that stood in recognizer.py when these I1 logs were produced, kept so
            # this record still describes that run — as the other analysis scripts keep
            # their own hardcoded 0.75. The live gate was, and is, theta_meta_planner below.
            "CONFIDENCE_THRESHOLD": 0.75, "BELIEF_FLOOR": rec_mod.BELIEF_FLOOR,
            "theta_meta_planner": mp._theta,
            "context_room_temperature": rec.context.room_temperature,
            "context_shift_start_step": rec.context.shift_start_step,
        },
        "hypotheses": [{"key": repr(h), "task": h.task_name, "bindings": dict(h.bindings)}
                       for h in rec._hypotheses],
        "discrete_microactions": sorted(rec._discrete_microactions),
        "admissible": sorted(rec._admissible) if rec._admissible is not None else None,
        "inadmissible": sorted(rec._inadmissible),
        "initial_prior": dict(rec._initial_prior),
        "object_types": {oid: o.type for oid, o in model.objects.items()},
        "object_positions": {oid: list(o.position) for oid, o in model.objects.items()},
        "human_script": [task_instance_key(t) for t in human.script],
        "robot_pool": [task_instance_key(t) for t in robot.assigned_tasks],
        "method_table": [],   # static: per task, per method, per step: action, completion grounding reason
        "ticks": [],
        "crash": None,
    }

    # static method table for every hypothesis (what a phase tracker would walk)
    for h in rec._hypotheses:
        ts = knowledge.get_task_schema(h.task_name)
        for mi, m in enumerate(ts.methods):
            for si, step in enumerate(m.step_calls):
                schema = knowledge.get_action_schema(step.action_name)
                pred, reason = ground_completion(schema, h.bindings, human_id, step)
                condition["method_table"].append({
                    "hyp": repr(h), "method_index": mi, "method": m.name,
                    "guards": [str(g.name) + str(tuple(str(a) for a in g.args)) for g in m.guards],
                    "step_index": si, "action": step.action_name,
                    "microactions": schema.microactions,
                    "completion_type": type(schema.completion).__name__,
                    "completion_grounded": pred_str(pred) if pred is not None else None,
                    "grounding": reason,
                })

    # ---- instance-level wrappers on the live recognizer ------------------
    state = {"tick": None, "hyp": None, "in_output": False}

    orig_update = rec.update
    orig_weigh = rec._weigh
    orig_output = rec._output
    orig_refuted = rec._refuted_by_holding
    orig_finalize = rec._finalize
    orig_likelihood = rec._likelihood
    orig_progress = rec._progress_likelihood
    orig_relevant = rec._get_relevant_action_schemas
    orig_resolve_cp = rec._resolve_completion_predicate
    orig_resolve_term = rec._resolve_term_value
    orig_context_weight = rec._context_weight
    orig_expected_pos = rec._get_expected_position
    orig_target_zone = rec._get_target_zone

    def update(obs, world, prev_belief=None):
        step = int(model.schedule.steps)
        mu = (obs.detected_microaction or "").upper()
        cur_pos = obs.spatial_context.position
        prev_pos = rec._history[-1].spatial_context.position if rec._history else None
        discrete = mu in rec._discrete_microactions
        moving = (prev_pos is not None
                  and math.hypot(cur_pos[0] - prev_pos[0], cur_pos[1] - prev_pos[1]) >= 1e-6)
        kind = "discrete" if discrete else ("moving" if moving else "stationary")
        held = world.agent_states[human_id].holding
        plan = human.current_plan
        ex = human.executor
        plan_completion = None
        if plan is not None and ex.current_plan is plan:
            plan_completion = []
            for ai, a in enumerate(plan.actions):
                cp = a.completion_predicate
                plan_completion.append({
                    "index": ai, "action": a.action_name,
                    "completion": pred_str(cp) if cp is not None else None,
                    "holds": (cp in world.predicates) if cp is not None else None,
                    "is_current": ai == ex.action_index,
                })
        # external evaluation of every hypothesis × method × step completion
        hyp_completion_true = []
        for row in condition["method_table"]:
            if row["completion_grounded"] is None:
                continue
            # rebuild the predicate cheaply from the static table
            h = rec._by_key[row["hyp"]]
            ts = knowledge.get_task_schema(h.task_name)
            step_call = ts.methods[row["method_index"]].step_calls[row["step_index"]]
            schema = knowledge.get_action_schema(step_call.action_name)
            pred, _ = ground_completion(schema, h.bindings, human_id, step_call)
            if pred in world.predicates:
                hyp_completion_true.append([row["hyp"], row["method_index"], row["step_index"]])

        tick = {
            "step": step,
            "obs_microaction": obs.detected_microaction,
            "obs_pos": pos_list(cur_pos),
            "obs_zone": obs.spatial_context.zone,
            "prev_pos": pos_list(prev_pos),
            "kind": kind,
            "leg_start_before": pos_list(rec._leg_start_pos),
            "evidence_before": dict(rec._evidence),
            "human_actual_task": (task_instance_key(human.get_current_task_instance())
                                  if human.get_current_task_instance() is not None else None),
            "human_script_index": human.script_index,
            "human_action": human.current_action,
            "human_action_index": ex.action_index,
            "human_microaction": human.current_microaction,
            "human_holding": held,
            "human_finished": human.finished,
            "human_predicates": preds_about(world, human_id),
            "obj_at": sorted(str(p) for p in world.predicates if p.name == "obj_at"),
            "object_locations": dict(world.object_locations),
            "robot_holding": world.agent_states[robot.unique_id].holding,
            "robot_pos": pos_list(world.agent_positions.get(robot.unique_id)),
            "plan_completion": plan_completion,
            "hyp_completion_true": hyp_completion_true,
            "weigh": None,
            "likelihoods": [],
            "refuted": None,
            "held_item_seen": None,
            "omega": {},
            "finalize": [],
        }
        state["tick"] = tick
        belief = orig_update(obs, world, prev_belief)
        tick["leg_start_after"] = pos_list(rec._leg_start_pos)
        tick["evidence_after"] = dict(rec._evidence)
        tick["distribution"] = dict(belief.distribution)
        tick["most_likely"] = belief.most_likely
        tick["confidence"] = belief.confidence
        condition["ticks"].append(tick)
        return belief

    def _weigh(obs, world, prior, origin):
        tick = state["tick"]
        tick["weigh"] = {"origin": pos_list(origin), "prior_is_evidence": prior is rec._evidence,
                         "prior_is_leg_base": prior is rec._leg_base}
        out = orig_weigh(obs, world, prior, origin)
        tick["weigh"]["live_keys"] = sorted(out.keys())
        tick["weigh"]["unnorm"] = dict(out)
        return out

    def _likelihood(obs, world, hyp, origin=None):
        rec_h = {"hyp": repr(hyp), "task": hyp.task_name, "branch": "fallthrough",
                 "schemas_scanned": None, "origin": pos_list(origin)}
        state["hyp"] = rec_h
        val = orig_likelihood(obs, world, hyp, origin)
        rec_h["value"] = val
        state["tick"]["likelihoods"].append(rec_h)
        state["hyp"] = None
        return val

    def _get_relevant_action_schemas(hyp):
        out = orig_relevant(hyp)
        if state["hyp"] is not None:
            ts = knowledge.get_task_schema(hyp.task_name)
            state["hyp"]["schemas_scanned"] = [s.name for s in out]
            state["hyp"]["method_used"] = ts.methods[0].name if ts and ts.methods else None
        return out

    def _resolve_completion_predicate(schema, hyp, obs):
        pred = orig_resolve_cp(schema, hyp, obs)
        if state["hyp"] is not None:
            state["hyp"]["branch"] = "completion" if pred is not None else "completion_unresolved"
            state["hyp"]["completion_schema"] = schema.name
            state["hyp"]["completion_predicate"] = pred_str(pred) if pred is not None else None
        return pred

    def _resolve_term_value(term, hyp, obs, task_schema, action_name):
        v = orig_resolve_term(term, hyp, obs, task_schema, action_name)
        if state["hyp"] is not None:
            state["hyp"].setdefault("term_resolutions", []).append(
                {"term": str(term), "action": action_name, "value": v})
        return v

    def _progress_likelihood(obs, world, hyp, schema, origin):
        h = state["hyp"]
        if h is not None:
            h["branch"] = "progress"
            h["progress_schema"] = schema.name
            h["evaluator"] = schema.progress_evaluator
            h["evaluator_registered"] = schema.progress_evaluator in lf.PROGRESS_EVALUATORS
            h["origin_none"] = origin is None
        val = orig_progress(obs, world, hyp, schema, origin)
        if h is not None and origin is not None and h.get("target_pos") is not None:
            cur = obs.spatial_context.position
            mv = (cur[0] - origin[0], cur[1] - origin[1])
            tt = (h["target_pos"][0] - origin[0], h["target_pos"][1] - origin[1])
            mn, tn = math.hypot(*mv), math.hypot(*tt)
            h["move_norm"] = mn
            h["target_dist_from_origin"] = tn
            h["cosine"] = (mv[0] * tt[0] + mv[1] * tt[1]) / (mn * tn) if mn > 1e-6 and tn > 1e-6 else None
        return val

    def _get_expected_position(hyp, world, agent_id):
        pos = orig_expected_pos(hyp, world, agent_id)
        h = state["hyp"]
        if h is not None:
            # replicate the branch labels of the original (analysis-side, read-only)
            item_id = hyp.bindings.get("?item")
            label, container = "no_item_binding", None
            if item_id is not None:
                held = Predicate("holding", (Const(agent_id), Const(item_id))) in world.predicates
                if held:
                    label = "phase2_last_move_to"
                else:
                    container = world.object_locations.get(item_id)
                    if container and world.object_positions.get(container):
                        ctype = model.objects[container].type if container in model.objects else "agent"
                        label = f"phase1_container:{ctype}"
                    elif container:
                        label = "phase1_container_unpositioned_fallback_item_pos"
                    else:
                        label = "phase1_item_pos"
            h["expected_branch"] = label
            h["container"] = container
            h["target_pos"] = pos_list(pos)
            h["target_none"] = pos is None
        return pos

    def _context_weight(obs, world, hyp):
        w = orig_context_weight(obs, world, hyp)
        tick = state["tick"]
        tz = state.get("last_target_zone")
        in_zone = (tz is not None and
                   Predicate("in_zone", (Const(obs.agent_id), Const(tz))) in world.predicates)
        temp = (hyp.task_name == "ac_activation" and rec.context.room_temperature is not None
                and rec.context.room_temperature >= rec_mod.HIGH_TEMP_THRESHOLD)
        fat = (hyp.task_name == "coffee_break"
               and rec.context.shift_duration(int(obs.timestamp)) >= rec_mod.LONG_SHIFT_THRESHOLD)
        tick["omega"][repr(hyp)] = {"weight": w, "target_zone": tz, "zone_fired": in_zone,
                                    "temp_fired": temp, "fatigue_fired": fat}
        state["last_target_zone"] = None
        return w

    def _get_target_zone(hyp, world):
        z = orig_target_zone(hyp, world)
        state["last_target_zone"] = z
        return z

    def _refuted_by_holding(obs, world):
        s = orig_refuted(obs, world)
        tick = state["tick"]
        tick["refuted"] = sorted(s)
        tick["held_item_seen"] = next(
            (p.args[1].value for p in world.predicates
             if p.name == "holding" and len(p.args) == 2 and p.args[0].value == obs.agent_id), None)
        return s

    def _output(obs, world):
        state["in_output"] = True
        try:
            return orig_output(obs, world)
        finally:
            state["in_output"] = False

    def _finalize(unnorm, pinned=None):
        total = sum(unnorm.values()) or 1.0
        below = [k for k, v in unnorm.items() if v / total < rec_mod.BELIEF_FLOOR]
        out = orig_finalize(unnorm, pinned)
        p = rec._inadmissible if pinned is None else pinned
        state["tick"]["finalize"].append({
            "where": "output" if state["in_output"] else "evidence",
            "n_live": len(unnorm), "clamped_to_floor": sorted(below),
            "n_pinned": len(p), "sum": sum(out.values()),
        })
        return out

    rec.update = update
    rec._weigh = _weigh
    rec._likelihood = _likelihood
    rec._get_relevant_action_schemas = _get_relevant_action_schemas
    rec._resolve_completion_predicate = _resolve_completion_predicate
    rec._resolve_term_value = _resolve_term_value
    rec._progress_likelihood = _progress_likelihood
    rec._get_expected_position = _get_expected_position
    rec._context_weight = _context_weight
    rec._get_target_zone = _get_target_zone
    rec._refuted_by_holding = _refuted_by_holding
    rec._output = _output
    rec._finalize = _finalize

    # ---- run ---------------------------------------------------------------
    completed = True
    for step in range(steps):
        try:
            model.step()
        except RuntimeError as e:
            # scenario_10 ends this way at step 257 in the unmodified baseline too
            # (MetaPlanner: no feasible candidate). Record and stop, as run_mesa does.
            condition["crash"] = {"step": step, "error": str(e).splitlines()[0]}
            completed = False
            break
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
    if completed:
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

    captures = {}
    for name, layout, scenario, steps, prior in CONDITIONS:
        captures[name] = run_condition(name, layout, scenario, steps, prior, out_dir)
        print(f"{name}: {len(captures[name]['ticks'])} ticks captured"
              f"{' (crash at step %d)' % captures[name]['crash']['step'] if captures[name]['crash'] else ''}",
              file=sys.stderr)
    with open(out_dir / "captures.json", "w") as f:
        json.dump(captures, f)
    print(f"wrote {out_dir / 'captures.json'}", file=sys.stderr)


if __name__ == "__main__":
    main()
