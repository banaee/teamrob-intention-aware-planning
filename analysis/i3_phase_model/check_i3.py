#!/usr/bin/env python3
"""
analysis/i3_phase_model/check_i3.py — acceptance checks and measurements for I3 (the phase model).

Part 1, unit checks on synthetic domains (no simulator):
  U1  two hypotheses whose expected actions head for the same place from the same origin
      receive an identical likelihood, and the kernel runs once for both (criterion 5)
  U2  the expected action is derived by walking the guard-selected method; when the method
      flips under a hypothesis the walk finds the right action and no index is stored
  U3  a terminal completion that holds for one tick and then disappears retires the hypothesis
      for good (the latch TODO-50 needs: `waited` is visible for three ticks only)
  U4  the completion channel is judged on the action expected BEFORE the event, so pick_up's
      completion is HIGH at the grasp tick (the post-grasp walk has already moved on)
  U5  shared/recognizer.py names no predicate: `holding` is read only through grounded
      completion conditions (criterion 4) — a source grep

Part 2, instrumented runs (wrappers on the robot's live recognizer, I1/I2's technique; the
[IR]/[IR-dist]/[meta] lines are replicated so the instrumented log cmp's against run_mesa.py's):
  M1  expected action per hypothesis per tick (expected_actions.csv) and every phase advance
  M2  completion-channel firings: at every grasp/release, which hypotheses were judged on which
      predicate and what they received (completion_events.csv) — the first time this branch runs
  M3  terminal completions and their tick (completions.csv)
  M4  likelihood sharing: progress/completion calls vs kernel evaluations (criterion 5 in the sweep)
  M5  `waited(human_0, X)` ticks against the entity the executor's own wait_at was bound to
      (waited_ticks.csv) — s40 and, outside the sweep, s10 (coffee machine and AC switch 75 cm apart)
  M6  the rival's expected action during a carry (criterion 2): per carry, what deliver_item(Y≠X)
      expected while the human held X (rival_phase.csv)

Part 3, variants — analysis-only monkeypatches, NOT shipped code, each producing a log set:
  nopin     the terminal pin disabled (stage S3 of the replay: phase model without completion)
  ungated   the completion channel judged on every expected action at a discrete tick, not only
            on actions whose vocabulary contains the microaction (the other reading of step 4)
  ownshelf  rivals decomposed as if the observed agent held nothing (deliver_default →
            move_to(shelf_Y)) — the world the task's criterion 2 assumes; measures what it would give

    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/i3_phase_model/check_i3.py [--variants]
"""
import csv
import logging
import math
import re
import sys
from collections import Counter, defaultdict
from copy import copy
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "mesa_sim"))
HERE = Path(__file__).parent

from shared.types import (                                   # noqa: E402
    Var, Const, ConditionSchema, StepCall, MethodSchema, TaskSchema, ActionSchema,
    DomainModel, WorldState, AgentState, Observation, SpatialContext, ActionContext,
    Predicate,
)
from shared.domain_knowledge import DomainKnowledgeBase, ContextKnowledge   # noqa: E402
from shared.recognizer import IntentionRecognizer, HypothesisKey, UNKNOWN   # noqa: E402
from shared import likelihood_functions                                     # noqa: E402
from shared.likelihood_functions import HIGH_LIKELIHOOD, LOW_LIKELIHOOD, NEUTRAL_LIKELIHOOD  # noqa: E402
from domains.kitting.actions import move_to, pick_up, place, wait_at        # noqa: E402

CONDITIONS = [
    ("s00_off", "env_layout0", "scenario_00", 300, False),
    ("s00_on",  "env_layout0", "scenario_00", 300, True),
    ("s20_off", "env_layout2", "scenario_20", 200, False),
    ("s20_on",  "env_layout2", "scenario_20", 200, True),
    ("s30_off", "env_layout3", "scenario_30", 200, False),
    ("s30_on",  "env_layout3", "scenario_30", 200, True),
    ("s40_off", "env_layout4", "scenario_40", 400, False),
    ("s40_on",  "env_layout4", "scenario_40", 400, True),
]
# Outside the sweep (dropped, TODO-52): run only for M5, the `waited` attribution check.
WAITED_EXTRA = [("s10_off", "env_layout1", "scenario_10", 300, False)]


def short(key):
    k = key.replace("deliver_item(?item=", "d(").replace(",?kitting_table=kitting_table_0)", ")")
    k = k.replace("coffee_break(?coffee_machine=coffee_machine_0)", "coffee")
    k = k.replace("ac_activation(?ac_switch=ac_switch_0)", "ac")
    return k


def act_str(a):
    if a is None:
        return "-"
    b = ",".join(f"{k}={v}" for k, v in sorted(a.bindings.items()) if k != "?agent")
    return f"{a.action_name}({b})"


# ---------------------------------------------------------------------------
# Part 1 — unit checks
# ---------------------------------------------------------------------------

def _obs(agent, pos, mu="step", t=0.0):
    return Observation(timestamp=t, agent_id=agent, detected_microaction=mu,
                       spatial_context=SpatialContext(position=pos, orientation=0.0, zone="z"),
                       action_context=ActionContext())


def _world(agent, pos, predicates=(), objects=None, locations=None, homes=None, holding=None, t=0.0):
    return WorldState(timestamp=t, agent_states={agent: AgentState(agent, "z", holding=holding)},
                      agent_positions={agent: pos}, predicates=set(predicates),
                      object_positions=dict(objects or {}), object_locations=dict(locations or {}),
                      object_zones={k: "z" for k in (objects or {})},
                      object_home_container=dict(homes if homes is not None else (locations or {})))


def _kitting_like_kb():
    from domains.kitting.tasks import deliver_item
    return DomainKnowledgeBase(DomainModel(
        tasks={"deliver_item": deliver_item},
        actions={"move_to": move_to, "pick_up": pick_up, "place": place},
        microactions=["STEP", "GRASP", "RELEASE"], intentions={"deliver_item"}))


class _KernelCounter:
    """Counts actual kernel evaluations by wrapping the registry entry."""
    def __init__(self):
        self.n = 0
        self._orig = likelihood_functions.PROGRESS_EVALUATORS["directional"]
    def __enter__(self):
        def counted(*a, **k):
            self.n += 1
            return self._orig(*a, **k)
        likelihood_functions.PROGRESS_EVALUATORS["directional"] = counted
        return self
    def __exit__(self, *exc):
        likelihood_functions.PROGRESS_EVALUATORS["directional"] = self._orig


def unit_checks():
    out = []
    kb = _kitting_like_kb()
    # Two items on ONE shelf, the agent starts west of it and walks east.
    objs = {"shelf_0": (200.0, 0.0), "item_a": (200.0, 0.0), "item_b": (200.0, 0.0),
            "table_0": (0.0, 400.0)}
    locs = {"item_a": "shelf_0", "item_b": "shelf_0"}
    ha = HypothesisKey("deliver_item", {"?item": "item_a", "?kitting_table": "table_0"})
    hb = HypothesisKey("deliver_item", {"?item": "item_b", "?kitting_table": "table_0"})

    # U1 — identical likelihood, computed once
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    rec.update(_obs("h", (0.0, 0.0), t=0), _world("h", (0.0, 0.0), objects=objs, locations=locs, t=0))
    with _KernelCounter() as kc:
        b = rec.update(_obs("h", (20.0, 0.0), t=1), _world("h", (20.0, 0.0), objects=objs, locations=locs, t=1))
    same = abs(b.distribution[repr(ha)] - b.distribution[repr(hb)]) < 1e-12
    out.append(("U1 two hypotheses expecting move_to to the same place: identical likelihood",
                same, f"P(a)={b.distribution[repr(ha)]:.4f} P(b)={b.distribution[repr(hb)]:.4f}"))
    out.append(("U1 ... computed once (one kernel evaluation for two hypotheses)", kc.n == 1, f"{kc.n} kernel call(s)"))

    # U2 — method flips under a hypothesis; the walk still finds the action, nothing indexed
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    w0 = _world("h", (180.0, 0.0), predicates=[Predicate("at", (Const("h"), Const("shelf_0"))),
                                                Predicate("at", (Const("h"), Const("item_a"))),
                                                Predicate("at", (Const("h"), Const("item_b")))],
                objects=objs, locations=locs, t=0)
    rec.update(_obs("h", (180.0, 0.0), "stand", t=0), w0)
    exp0 = {k: act_str(a) for k, a in rec._expected.items()}
    # grasp item_a: holding(h, item_a) appears; item_a leaves the shelf
    locs1 = {"item_a": "h", "item_b": "shelf_0"}
    w1 = _world("h", (180.0, 0.0), predicates=[Predicate("at", (Const("h"), Const("shelf_0"))),
                                                Predicate("at", (Const("h"), Const("item_b"))),
                                                Predicate("holding", (Const("h"), Const("item_a")))],
                objects={**objs, "item_a": (180.0, 0.0)}, locations=locs1, homes=locs, holding="item_a", t=1)
    b1 = rec.update(_obs("h", (180.0, 0.0), "grasp", t=1), w1)
    exp1 = {k: act_str(a) for k, a in rec._expected.items()}
    ok2 = (exp0[repr(ha)] == "pick_up(?item=item_a)" and exp0[repr(hb)] == "pick_up(?item=item_b)"
           and exp1[repr(ha)] == "move_to(?target=table_0)"                 # deliver_already_held, index 0
           and exp1[repr(hb)] == "place(?item=item_a,?target=shelf_0)")   # deliver_with_return, index 1
    out.append(("U2 expected action derived through the re-selected method (2- and 6-action lists)",
                ok2, f"before grasp {exp0[repr(ha)]} / {exp0[repr(hb)]}; after {exp1[repr(ha)]} / {exp1[repr(hb)]}"))
    # Both hypotheses expected a grasp here (both items within reach), so both are judged:
    # holding(h, item_a) holds → HIGH for a; holding(h, item_b) does not → LOW for b: ratio 40.
    ratio = b1.distribution[repr(ha)] / b1.distribution[repr(hb)]
    out.append(("U4 completion channel judged on the action expected before the grasp: HIGH for item_a, LOW for item_b (×40)",
                b1.distribution[repr(ha)] > 0.75 and abs(ratio - HIGH_LIKELIHOOD / LOW_LIKELIHOOD) < 0.5,
                f"P(a)={b1.distribution[repr(ha)]:.3f} P(b)={b1.distribution[repr(hb)]:.3f} ratio {ratio:.1f}"))
    has_index = any(isinstance(v, int) for v in rec.__dict__.values()) or any(
        isinstance(v, dict) and any(isinstance(x, int) for x in v.values())
        for k, v in rec.__dict__.items() if k not in ("_base", "_evidence", "_initial_prior"))
    out.append(("U2 no integer phase index stored on the recognizer", not has_index, ""))

    # U3 — transient terminal completion latches
    _agent, _machine, _target, _entity = Var("?agent"), Var("?machine"), Var("?target"), Var("?entity")
    cb = TaskSchema(name="cb", parameters=[_machine], parameter_types={"?machine": "machine"}, is_foreseeable=True,
                    methods=[MethodSchema(name="m", parameters=[_machine], guards=[],
                                          step_calls=[StepCall("move_to", {_target: _machine}),
                                                      StepCall("wait_at", {_entity: _machine, Var("?duration"): Const("PT3S")})])])
    kb3 = DomainKnowledgeBase(DomainModel(tasks={"cb": cb}, actions={"move_to": move_to, "wait_at": wait_at},
                                          microactions=["STEP", "STAND"], intentions={"cb"}))
    hc = HypothesisKey("cb", {"?machine": "m_0"})
    rec3 = IntentionRecognizer(knowledge=kb3, context=ContextKnowledge.default(), hypotheses=[hc])
    o3 = {"m_0": (100.0, 0.0)}
    rec3.update(_obs("h", (0.0, 0.0), t=0), _world("h", (0.0, 0.0), objects=o3, t=0))
    rec3.update(_obs("h", (80.0, 0.0), t=1), _world("h", (80.0, 0.0), objects=o3, t=1))
    p_before = rec3.update(_obs("h", (80.0, 0.0), "stand", t=2), _world("h", (80.0, 0.0), objects=o3, t=2)).distribution[repr(hc)]
    waited = Predicate("waited", (Const("h"), Const("m_0")))
    p_at = rec3.update(_obs("h", (80.0, 0.0), "stand", t=3), _world("h", (80.0, 0.0), predicates=[waited], objects=o3, t=3)).distribution[repr(hc)]
    p_after = rec3.update(_obs("h", (60.0, 0.0), t=4), _world("h", (60.0, 0.0), objects=o3, t=4)).distribution[repr(hc)]
    out.append(("U3 terminal completion pins the hypothesis on the tick it holds and keeps it pinned after it clears",
                p_before > 0.5 and p_at == 0.001 and p_after == 0.001 and repr(hc) in rec3._completed,
                f"before {p_before:.3f}, at {p_at:.3f}, after {p_after:.3f}"))

    # U5 — source grep: no predicate name in the recognizer
    src = (ROOT / "shared" / "recognizer.py").read_text()
    code = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
    code_no_doc = re.sub(r'"""[\s\S]*?"""', "", code)
    bad = [w for w in ('"holding"', '"in_zone"', '"at"', '"obj_at"', '"waited"', '"?item"', '"move_to"', "ZONE_BOOST", "_refuted_by_holding")
           if w in code_no_doc]
    out.append(("U5 recognizer.py code names no predicate / parameter / action / removed mechanism", not bad, f"found: {bad}" if bad else ""))
    return out


# ---------------------------------------------------------------------------
# Part 2 — instrumented runs
# ---------------------------------------------------------------------------

def run_condition(name, layout, scenario, steps, prior, variant="base"):
    from mesa_sim.sim_model import SimModel
    from mesa_sim.world_state_builder import build_world_state
    from domains.kitting.registry import domain_config
    lay = domain_config["layouts"][layout]
    scen = lay["scenarios"][scenario]
    log_path = HERE / "logs_instrumented" / variant / f"{name}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
    fh = logging.FileHandler(log_path, mode="w"); fh.setFormatter(logging.Formatter("%(message)s"))
    root.addHandler(fh); root.setLevel(logging.INFO)
    logging.info(f"[run_mesa] Starting headless run — domain=kitting scenario={scenario} steps={steps}")

    model = SimModel(scenario=scen, register_fn=domain_config["register_fn"],
                     env_layout_path=lay["path"], assignment_prior=prior)
    robot = model.robots["robot_0"]; human = model.humans["human_0"]
    rec = robot.recognizer

    stats = {"progress_calls": 0, "completion_calls": 0, "kernel_evals": 0, "completion_evals": 0,
             "expected": [], "advances": [], "events": [], "completions": [], "waited": [], "rival": []}
    tick = {"step": -1}
    # The priming observation (observe_initial) has already happened in SimModel.__init__;
    # record its expected actions as step -1.
    for k, a in rec._expected.items():
        stats["expected"].append((-1, k, act_str(a), rec._origin.get(k)))

    # --- variants ---------------------------------------------------------
    if variant == "nopin":
        rec._terminal_complete = lambda actions, world: False
    if variant == "ungated":
        discrete = {"GRASP", "RELEASE"}
        rec._in_vocabulary = lambda action, mu: mu in discrete
    if variant == "ownshelf":
        from shared.planner import DecompositionError
        def grounded(hyp, agent_id, world):
            key = repr(hyp)
            if key in rec._tick_actions:
                return rec._tick_actions[key]
            held = world.agent_states[agent_id].holding
            w = world
            if held is not None and held not in hyp.bindings.values():
                w = copy(world)
                w.predicates = {p for p in world.predicates
                                if not (p.name == "holding" and p.args[0].value == agent_id)}
            try:
                acts = rec._planner.decompose(hyp.task_name, hyp.bindings, agent_id, w)
            except DecompositionError:
                acts = None
            rec._tick_actions[key] = acts
            return acts
        rec._grounded_actions = grounded

    # --- M4: likelihood sharing -------------------------------------------
    orig_kernel = likelihood_functions.PROGRESS_EVALUATORS["directional"]
    def kernel(*a, **k):
        stats["kernel_evals"] += 1
        return orig_kernel(*a, **k)
    likelihood_functions.PROGRESS_EVALUATORS["directional"] = kernel
    orig_cpl = likelihood_functions.completion_predicate_likelihood
    def cpl(predicate, world_predicates):
        stats["completion_evals"] += 1
        return orig_cpl(predicate, world_predicates)
    likelihood_functions.completion_predicate_likelihood = cpl
    orig_prog = rec._progress_likelihood
    def prog(action, origin, pos, world, memo):
        stats["progress_calls"] += 1
        return orig_prog(action, origin, pos, world, memo)
    rec._progress_likelihood = prog
    orig_comp = rec._completion_likelihood
    def comp(action, world, memo):
        stats["completion_calls"] += 1
        v = orig_comp(action, world, memo)
        stats["_events_this_tick"].append((act_str(action), str(action.completion_predicate), v))
        return v
    rec._completion_likelihood = comp
    stats["_events_this_tick"] = []

    # --- M1/M2/M3: wrap update to snapshot phase state --------------------
    orig_update = rec.update
    def update(obs, world, prev_belief=None):
        before = dict(rec._expected)
        completed_before = set(rec._completed)
        stats["_events_this_tick"] = []
        b = orig_update(obs, world, prev_belief)
        step = int(obs.timestamp)
        mu = (obs.detected_microaction or "").upper()
        for k, a in rec._expected.items():
            stats["expected"].append((step, k, act_str(a), rec._origin.get(k)))
            if k in before and not rec._same_action(before[k], a):
                stats["advances"].append((step, k, act_str(before[k]), act_str(a)))
        for k in rec._completed - completed_before:
            stats["completions"].append((step, k, human.current_action, human.current_microaction))
        if stats["_events_this_tick"]:
            # which hypotheses expected each judged action before the event
            by_action = defaultdict(list)
            for k, a in before.items():
                by_action[act_str(a)].append(k)
            for astr, pred, v in stats["_events_this_tick"]:
                for k in by_action.get(astr, ["?"]):
                    stats["events"].append((step, mu, k, astr, pred, v, b.distribution.get(k)))
        # M6: rivals while the human holds something
        held = world.agent_states[obs.agent_id].holding
        if held is not None:
            for k, a in rec._expected.items():
                hyp = rec._by_key[k]
                if held not in hyp.bindings.values() and hyp.task_name == "deliver_item":
                    stats["rival"].append((step, held, k, act_str(a)))
        return b
    rec.update = update

    stats["aborted"] = None
    for step in range(steps):
        tick["step"] = step
        try:
            model.step()
        except RuntimeError as e:           # scenario_10's latent TODO-52 crash (outside the sweep)
            stats["aborted"] = (step, str(e).split(":")[0])
            logging.info(f"[check_i3] run aborted at step {step}: {e}")
            break
        for aid, h in model.humans.items():
            logging.info(f"  step: {step}: [{aid}] task={h.current_task} action={h.current_action} "
                         f"micro={h.current_microaction} pos={np.round(h.pos, 2)}")
        for aid, r in model.robots.items():
            logging.info(f"  step: {step}: [{aid}] task={r.current_task} action={r.current_action} "
                         f"micro={r.current_microaction} pos={np.round(r.pos, 2)}")
        # M5 — waited predicate vs the entity the executor's wait_at is bound to
        w = build_world_state(model)
        for p in w.predicates:
            if p.name == "waited" and p.args[0].value == "human_0":
                ex = human.executor
                plan = ex.current_plan
                bound = None
                if plan is not None:
                    idx = min(ex.action_index, len(plan.actions) - 1)
                    last_wait = [a for a in plan.actions[:idx + 1] if a.action_name == "wait_at"]
                    bound = last_wait[-1].bindings.get("?entity") if last_wait else None
                stats["waited"].append((step, p.args[1].value, bound, human.current_task, human.current_action))
    logging.info("[run_mesa] Headless run complete.")
    fh.flush(); root.removeHandler(fh)
    likelihood_functions.PROGRESS_EVALUATORS["directional"] = orig_kernel
    likelihood_functions.completion_predicate_likelihood = orig_cpl
    return stats


def crossings(log_path):
    out = []
    for line in open(log_path):
        if line.startswith("[meta]") and "theta_crossed" in line:
            s = re.search(r"step=(\d+)", line).group(1)
            out.append(int(s))
    return out


def ir_line(log_path, step):
    for line in open(log_path):
        if line.startswith(f"[IR] step={step} "):
            m = re.search(r"most_likely=(\S+) confidence=([\d.]+)", line)
            return short(m.group(1)), float(m.group(2))
    return None


def compare_logs(a, b):
    """Regression greps equal?"""
    def greps(p):
        return [l for l in open(p) if l.startswith(("[IR] ", "[IR-dist]", "[meta]", "[meta-cand]"))]
    return greps(a) == greps(b)


# ---------------------------------------------------------------------------
def main():
    variants = ["base", "nopin"] + (["ungated", "ownshelf"] if "--variants" in sys.argv else [])
    lines = ["# I3 checks — generated by check_i3.py\n"]
    lines.append("## Unit checks\n\n| check | result | detail |\n|---|---|---|")
    ok_all = True
    for name, ok, detail in unit_checks():
        ok_all &= ok
        lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} | {detail} |")
    lines.append("")

    csv_rows = defaultdict(list)
    lines.append("## Instrumented sweep (variant `base` = the shipped code)\n")
    lines.append("| condition | log == run_mesa | progress calls / kernel evals | completion calls / evals | "
                 "phase advances | completions (step:key) | θ crossings | waited ticks (step:object=bound) |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for variant in variants:
        for name, layout, scenario, steps, prior in CONDITIONS:
            st = run_condition(name, layout, scenario, steps, prior, variant)
            log = HERE / "logs_instrumented" / variant / f"{name}.log"
            if variant == "base":
                same = compare_logs(log, HERE / "new" / f"{name}.log") if (HERE / "new" / f"{name}.log").exists() else None
                comps = ", ".join(f"{s}:{short(k)}" for s, k, _, _ in st["completions"])
                waited = ", ".join(f"{s}:{o}={'ok' if o == b else b}" for s, o, b, _, _ in st["waited"])
                lines.append(f"| {name} | {same} | {st['progress_calls']} / {st['kernel_evals']} | "
                             f"{st['completion_calls']} / {st['completion_evals']} | {len(st['advances'])} | {comps} | "
                             f"{crossings(log)} | {waited or '-'} |")
                if same is False:
                    ok_all = False
                csv_rows["expected_actions"] += [(name, s, short(k), a, o) for s, k, a, o in st["expected"]]
                csv_rows["phase_advances"] += [(name, s, short(k), a, b) for s, k, a, b in st["advances"]]
                csv_rows["completion_events"] += [(name, s, mu, short(k), a, p, v, f"{out:.3f}" if out is not None else "")
                                                  for s, mu, k, a, p, v, out in st["events"]]
                csv_rows["completions"] += [(name, s, short(k), act, mu) for s, k, act, mu in st["completions"]]
                csv_rows["waited_ticks"] += [(name, s, o, b, t, a) for s, o, b, t, a in st["waited"]]
                # rival phases: compress to (held, key, action) -> step range
                rng = {}
                for s, held, k, a in st["rival"]:
                    rng.setdefault((held, k, a), [s, s])[1] = s
                csv_rows["rival_phase"] += [(name, held, short(k), a, r[0], r[1]) for (held, k, a), r in rng.items()]
            else:
                csv_rows[f"variant_{variant}"].append((name, str(crossings(log)), ", ".join(f"{s}:{short(k)}" for s, k, _, _ in st["completions"])))
    # M5 outside the sweep
    for name, layout, scenario, steps, prior in WAITED_EXTRA:
        st = run_condition(name, layout, scenario, steps, prior, "base")
        waited = ", ".join(f"{s}:{o}={'ok' if o == b else b}" for s, o, b, _, _ in st["waited"])
        note = f" — run aborted at step {st['aborted'][0]} ({st['aborted'][1]}, TODO-52)" if st["aborted"] else ""
        lines.append(f"| {name} (waited check only{note}) | - | - | - | - | - | - | {waited or '-'} |")
        csv_rows["waited_ticks"] += [(name, s, o, b, t, a) for s, o, b, t, a in st["waited"]]
    lines.append("")

    for variant in variants[1:]:
        lines.append(f"## Variant `{variant}` (analysis-only monkeypatch)\n\n| condition | θ crossings | completions |\n|---|---|---|")
        for name, cr, comps in csv_rows[f"variant_{variant}"]:
            lines.append(f"| {name} | {cr} | {comps} |")
        lines.append("")

    headers = {
        "expected_actions": ["condition", "step", "hypothesis", "expected_action", "origin"],
        "phase_advances": ["condition", "step", "hypothesis", "from", "to"],
        "completion_events": ["condition", "step", "microaction", "hypothesis", "judged_action", "predicate", "likelihood", "output_belief"],
        "completions": ["condition", "step", "hypothesis", "human_action", "human_micro"],
        "waited_ticks": ["condition", "step", "waited_object", "executor_bound_entity", "human_task", "human_action"],
        "rival_phase": ["condition", "held", "hypothesis", "expected_action", "from_step", "to_step"],
    }
    for fname, header in headers.items():
        with open(HERE / f"{fname}.csv", "w", newline="") as f:
            w = csv.writer(f); w.writerow(header); w.writerows(csv_rows[fname])
    lines.append(f"\nOVERALL: {'PASS' if ok_all else 'FAIL'}\n")
    (HERE / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
