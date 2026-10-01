#!/usr/bin/env python3
"""
RETIRED (graded evidence, September 2026): the unit checks here encode the pre-grade values (a fitting stretch worth
1/u on its first step; unknown a constant per observation) and the sweep matrix describes the pre-grade HEAD.
They are the record of their report and no longer run at HEAD: `--unit` prints this note. The checks that survive
the grade are restated with graded expectations in analysis/g1_graded_evidence/unit_checks.py, which is the live
set.

analysis/i4d_fold_unknown/check_i4d.py — the I4d matrix on I4's harness through I4c's helpers: the shipped code
(unknown's contribution folds with the stretch, TODO-60) against the reversion.

Variants (analysis-only monkeypatches; only `base` is shipped):
  base     a stretch folds as odds L/u; the open observation is v/u; unknown takes no factor
  nofold   I4c's accounting — a stretch folds as L, unknown pays u on any tick with an observation;
           must equal baseline/ (I4c's run_mesa.py logs at ac240a8) on the four greps

Every `base` run carries an independent accumulator of the invariant
    E_t(k)/E_t(unknown) = Π_closed L_k(s)/u · Π_events c_k(e) · (v_k(t)/u | 1 if the open stretch is empty)
driven only by the recognizer's phase state and the likelihood functions; its largest deviation per condition
is reported (invariant.csv, one row per tick and hypothesis).

  --final    eight conditions × two variants: summary.md, metrics.csv, the per-tick CSVs, invariant.csv,
             retrigger.md (criterion 2), chains.md, region.md
  --unit     I4's U1–U3/U6, I4c's U7–U9, I4d's U5'' and U10 (U4 and U5 re-stated: the ceiling and the mixed tick changed)
    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/i4d_fold_unknown/check_i4d.py --final
"""
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "i4c_episode"))
sys.path.insert(0, str(HERE.parent / "i4_evidence_model"))
import check_i4c as C                                                          # noqa: E402
import check_i4 as I4                                                          # noqa: E402
from check_i4 import ORDER, THETA, short, act_str, metrics, compare_logs       # noqa: E402
from shared import likelihood_functions as LF                                 # noqa: E402

I4.HERE = HERE
UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Variants
# ---------------------------------------------------------------------------

def _invariant(rec):
    """Independent accumulator of each live hypothesis's closed odds; compares with the recognizer's evidence
    after every tick. Installed as an inner wrapper (before I4's outer one)."""
    # the constructor's priming update has already registered every hypothesis (an empty stretch, odds 1)
    rec._i4d = {"acc": {k: 1.0 for k in rec._expected}, "rows": []}
    orig = rec.update

    def update(obs, world, prev_belief=None):
        before_e, before_o, before_oo = dict(rec._expected), dict(rec._origin), dict(rec._origin_odo)
        before_c = set(rec._completed)
        b = orig(obs, world, prev_belief)
        step = int(obs.timestamp); pos = obs.spatial_context.position; odo = rec._odometer[obs.agent_id]
        mu = (obs.detected_microaction or "").upper(); u = LF.UNKNOWN_LIKELIHOOD
        acc = rec._i4d["acc"]
        for k in rec._completed - before_c:
            acc.pop(k, None)
        boundary = bool(rec._completed - before_c) and all(rec._origin_odo[k] == odo and rec._origin[k] == pos for k in rec._origin)
        if boundary:
            for k in rec._expected:
                acc[k] = 1.0
        for k, a in rec._expected.items():
            if k not in before_e:
                acc[k] = 1.0
            elif not boundary:
                prev = before_e[k]
                if prev is not None and rec._in_vocabulary(prev, mu):
                    acc[k] *= rec._completion_likelihood(prev, world, {})
                if not rec._same_action(prev, a):
                    closing = rec._progress_likelihood(prev, before_o[k], odo - before_oo[k], pos, world, {})
                    if closing is not None:
                        acc[k] *= closing / u
            v = rec._progress_likelihood(a, rec._origin[k], odo - rec._origin_odo[k], pos, world, {})
            odds = acc[k] * (1.0 if v is None else v / u)
            got = rec._evidence[k] / rec._evidence[UNKNOWN]
            err = abs(math.log(got) - math.log(odds)) if got > 0 and odds > 0 else float("inf")
            rec._i4d["rows"].append((step, k, f"{odds:.6e}", f"{got:.6e}", f"{err:.2e}"))
        return b
    rec.update = update


def setup_base(rec, model, human):
    _invariant(rec)
    C._instrument(rec)


def setup_nofold(rec, model, human):
    """I4c's accounting: the stretch folds as L (v·u/u), the open term is v (v·u/u), and unknown pays u on any
    tick with an observation — applied after the tick as a second normalisation, which is algebraically I4c's
    update. Skipped on a boundary tick (I4c's _begin_episode reports the bare prior)."""
    orig_prog = rec._progress_likelihood

    def prog(action, origin, walked, pos, world, memo):
        v = orig_prog(action, origin, walked, pos, world, memo)
        return None if v is None else v * LF.UNKNOWN_LIKELIHOOD
    rec._progress_likelihood = prog
    orig = rec.update

    def update(obs, world, prev_belief=None):
        before_c = set(rec._completed)
        b = orig(obs, world, prev_belief)
        pos = obs.spatial_context.position; odo = rec._odometer[obs.agent_id]
        boundary = bool(rec._completed - before_c) and all(rec._origin_odo[k] == odo and rec._origin[k] == pos for k in rec._origin)
        observed = any(orig_prog(a, rec._origin[k], odo - rec._origin_odo[k], pos, world, {}) is not None
                       for k, a in rec._expected.items())
        if observed and not boundary:
            ev = dict(rec._evidence); ev[UNKNOWN] *= LF.UNKNOWN_LIKELIHOOD
            z = sum(ev.values())
            rec._evidence = {k: v / z for k, v in ev.items()}
            for k in rec._base:
                rec._base[k] /= z
            d = rec._output(obs, world)
            from shared.types import BeliefState
            ml = max(d, key=lambda k: d[k])
            b = BeliefState(timestamp=obs.timestamp, agent_id=obs.agent_id, distribution=d, most_likely=ml, confidence=d[ml])
        return b
    rec.update = update
    C._instrument(rec)


SETUPS = {"base": setup_base, "nofold": setup_nofold}
REF = {"base": HERE / "new", "nofold": HERE / "baseline"}
RETRIGGER = {"s00_on": (106, 116), "s20_on": (84, 94), "s30_on": (93, 103)}


# ---------------------------------------------------------------------------
# Unit checks
# ---------------------------------------------------------------------------

def unit_checks_i4d():
    from shared.types import Const, DomainModel, WorldState, AgentState, Observation, SpatialContext, ActionContext, Predicate
    from shared.domain_knowledge import DomainKnowledgeBase, ContextKnowledge
    from shared.recognizer import IntentionRecognizer, HypothesisKey
    from domains.kitting.actions import move_to, pick_up, place
    from domains.kitting.tasks import deliver_item
    I4.apply_constants(0.01, 0.1)
    u = LF.UNKNOWN_LIKELIHOOD

    def _obs(agent, pos, mu="step", t=0.0):
        return Observation(timestamp=t, agent_id=agent, detected_microaction=mu,
                           spatial_context=SpatialContext(position=pos, orientation=0.0, zone="z"), action_context=ActionContext())

    def _world(agent, pos, predicates=(), objects=None, locations=None, holding=None, t=0.0, home=None):
        return WorldState(timestamp=t, agent_states={agent: AgentState(agent, "z", holding=holding)}, agent_positions={agent: pos},
                          predicates=set(predicates), object_positions=dict(objects or {}), object_locations=dict(locations or {}),
                          object_zones={k: "z" for k in (objects or {})}, object_home_container=dict(home if home is not None else (locations or {})))
    kb = DomainKnowledgeBase(DomainModel(tasks={"deliver_item": deliver_item}, actions={"move_to": move_to, "pick_up": pick_up, "place": place},
                                         microactions=["STEP", "GRASP", "RELEASE"], intentions={"deliver_item"}))
    objs = {"shelf_a": (400.0, 0.0), "item_a": (400.0, 0.0), "shelf_b": (0.0, 400.0), "item_b": (0.0, 400.0), "table_0": (0.0, -400.0)}
    locs = {"item_a": "shelf_a", "item_b": "shelf_b"}
    ha = HypothesisKey("deliver_item", {"?item": "item_a", "?kitting_table": "table_0"})
    hb = HypothesisKey("deliver_item", {"?item": "item_b", "?kitting_table": "table_0"})
    P = lambda name, *args: Predicate(name, tuple(Const(a) for a in args))
    out = []

    # U10 — the fold keeps unknown's contribution: a walks to shelf_a (excess 0); at the arrival its move_to folds
    # and pick_up opens (no graded signal). a:unknown is 1/u on the walk, 1/u² from the arrival (closed 1/u ×
    # open 1/u), 1/u² on the grasp tick (pick_up folds, move_to(table) is empty: no factor), 1/u³ on the first
    # step of the carry. b:unknown is L(excess_b)/u throughout, unchanged by a's advances; a:b gains 1/u per
    # observation of a.
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    rec.update(_obs("h", (0.0, 0.0), "stand", t=0), _world("h", (0.0, 0.0), objects=objs, locations=locs, t=0))
    r = {}
    for i in range(1, 20):
        p = (20.0 * i, 0.0)
        preds = [P("at", "h", "shelf_a"), P("at", "h", "item_a")] if 400 - 20 * i <= 30 else []
        b = rec.update(_obs("h", p, t=i), _world("h", p, predicates=preds, objects=objs, locations=locs, t=i))
        if i in (18, 19):
            r[i] = (rec._evidence[repr(ha)] / rec._evidence[UNKNOWN], rec._evidence[repr(hb)] / rec._evidence[UNKNOWN])
    p = (380.0, 0.0)
    b20 = rec.update(_obs("h", p, "grasp", t=20), _world("h", p, predicates=[P("at", "h", "shelf_a"), P("holding", "h", "item_a")],
                                                        objects={**objs, "item_a": p}, locations={**locs, "item_a": "h"}, holding="item_a", t=20, home=locs))
    e20 = dict(rec._evidence)
    p21 = (380.0 - 380 / 28, -400 / 28)                                   # one step straight at the table
    b21 = rec.update(_obs("h", p21, t=21), _world("h", p21, predicates=[P("holding", "h", "item_a")],
                                                 objects={**objs, "item_a": p21}, locations={**locs, "item_a": "h"}, holding="item_a", t=21, home=locs))
    ex_b = lambda x: x + math.hypot(x, 400) - 400                          # b's excess after walking x east
    a18, b18 = r[18]; a19, b19 = r[19]
    a20 = e20[repr(ha)] / e20[UNKNOWN]; a21 = rec._evidence[repr(ha)] / rec._evidence[UNKNOWN]
    ok = (abs(a18 - 1 / u) < 1e-9 and abs(a19 - 1 / u ** 2) < 1e-9 and abs(a20 - 1 / u ** 2) < 1e-9 and abs(a21 - 1 / u ** 3) < 1e-6
          and abs(b18 - LF.logistic_of_excess(ex_b(360)) / u) < 1e-9 and abs(b19 - LF.logistic_of_excess(ex_b(380)) / u) < 1e-9
          and act_str(rec._expected[repr(ha)]).startswith("move_to"))
    out.append(("U10 fold keeps unknown's contribution: a:unknown 1/u on the walk, 1/u² at the arrival (closed 1/u × open pick_up 1/u), "
                "1/u² on the grasp tick (no dip: pick_up folds, the new stretch is empty), 1/u³ one step into the carry; b:unknown "
                "= L(excess)/u throughout (evidence state: the output floor sits at 1e-3)", ok,
                f"a:u {a18:.1f} → {a19:.1f} → {a20:.1f} → {a21:.1f}; b:u {b18:.4f} → {b19:.4f} (expected {LF.logistic_of_excess(ex_b(360))/u:.4f} → "
                f"{LF.logistic_of_excess(ex_b(380))/u:.4f}); P(a) at the grasp {b20.distribution[repr(ha)]:.3f}"))

    # U5'' — I4's U5 under the accounting: the grasped item's hypothesis keeps its evidence (hit 1.0) and the rival that
    # also expected the grasp is charged the false-alarm rate — the BASE ratio a:b is 1000. The EVIDENCE ratio is 100:
    # on the grasp tick a's new stretch (move_to the table) is empty, no observation, while b's new phase — place(item_a)
    # back on shelf_0 under deliver_with_return, no graded signal — is one, and pays 1/u. a:unknown stays 1/u (the
    # closed pick_up phase keeps its u).
    objs2 = {"shelf_0": (200.0, 0.0), "item_a": (200.0, 0.0), "item_b": (200.0, 0.0), "table_0": (0.0, 400.0)}
    locs2 = {"item_a": "shelf_0", "item_b": "shelf_0"}
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    at = [P("at", "h", "shelf_0"), P("at", "h", "item_a"), P("at", "h", "item_b")]
    rec.update(_obs("h", (180.0, 0.0), "stand", t=0), _world("h", (180.0, 0.0), predicates=at, objects=objs2, locations=locs2, t=0))
    rec.update(_obs("h", (180.0, 0.0), "stand", t=1), _world("h", (180.0, 0.0), predicates=at, objects=objs2, locations=locs2, t=1))
    r1 = rec._evidence[repr(ha)] / rec._evidence[UNKNOWN]
    w1 = _world("h", (180.0, 0.0), predicates=at[:1] + at[2:] + [P("holding", "h", "item_a")], objects={**objs2, "item_a": (180.0, 0.0)},
                locations={"item_a": "h", "item_b": "shelf_0"}, holding="item_a", t=2, home=locs2)
    b2 = rec.update(_obs("h", (180.0, 0.0), "grasp", t=2), w1)
    ev = rec._evidence
    ok = (abs(rec._base[repr(ha)] / rec._base[repr(hb)] - 1000.0) < 1e-6 and abs(ev[repr(ha)] / ev[repr(hb)] - 1000.0 * u) < 1e-6
          and abs(r1 - 1 / u) < 1e-9 and abs(ev[repr(ha)] / ev[UNKNOWN] - 1 / u) < 1e-9
          and act_str(rec._expected[repr(hb)]).startswith("place"))
    out.append(("U5'' grasp under the accounting: base ratio a:b 1000 (the event); evidence ratio a:b 100 — a's new stretch is empty, b's "
                "new place phase (no graded signal) is an observation and pays 1/u; a:unknown 1/u before and after", ok,
                f"base a:b {rec._base[repr(ha)]/rec._base[repr(hb)]:.1f}, evidence a:b {ev[repr(ha)]/ev[repr(hb)]:.1f}, a:u {r1:.1f} → "
                f"{ev[repr(ha)]/ev[UNKNOWN]:.1f}, b expects {act_str(rec._expected[repr(hb)])}, output P(b)={b2.distribution[repr(hb)]:.3f}"))
    return out


def all_unit_checks():
    # I4's U4 asserts a:unknown unchanged across a zero-excess advance and U5 an evidence ratio a:b of exactly 1000 at the
    # grasp — both false by design now (a closed stretch keeps its 1/u; an open no-graded-signal phase is an observation);
    # U10 and U5'' state the new expectations. I4c's U7–U9 hold as written.
    checks = [c for c in I4.unit_checks() if not c[0].startswith(("U4", "U5"))]
    return checks + C.unit_checks_i4c() + unit_checks_i4d()


# ---------------------------------------------------------------------------
# Final matrix
# ---------------------------------------------------------------------------

def retrigger(name, rows, log_path):
    lo, hi = RETRIGGER[name]
    meta = [l.strip() for l in open(log_path) if l.startswith("[meta] step=") and lo <= int(l.split("step=")[1].split(" ")[0]) <= hi]
    out = [f"### {name}, ticks {lo}–{hi}\n", "| tick | human | most_likely | confidence |", "|---|---|---|---|"]
    for r in rows:
        if lo <= r["step"] <= hi:
            out.append(f"| {r['step']} | {r['human_action']}/{r['human_micro']} | {r['most_likely']} | {r['confidence']:.3f} |")
    out.append("\n`[meta]` lines in the window: " + ("; ".join(f"`{m}`" for m in meta) if meta else "none") + "\n")
    return "\n".join(out)


def final():
    beta, unknown = LF.BETA, LF.UNKNOWN_LIKELIHOOD
    lines = [f"# I4d checks — generated by check_i4d.py (BETA={beta}, UNKNOWN_LIKELIHOOD={unknown})\n"]
    lines.append("## Unit checks\n\n| check | result | detail |\n|---|---|---|")
    ok_all = True
    for n, ok, d in all_unit_checks():
        ok_all &= ok
        lines.append(f"| {n} | {'PASS' if ok else 'FAIL'} | {d} |")
    lines.append("")
    csv_rows = defaultdict(list); all_metrics = []; inv_rows = []; retention = []; chains = []; retrig = []
    st_base, rows_base = {}, {}
    for variant in SETUPS:
        title = {"base": "Instrumented sweep (variant `base` = the shipped code)"}.get(variant, f"Variant `{variant}` (analysis-only monkeypatch)")
        lines.append(f"## {title}\n")
        lines.append("| condition | log == ref | invariant max |Δlog odds| | boundaries | completions | θ crossings (`!` = winner ≠ truth) | reveals | wrong-θ ticks (task) | wrong-task ranges | max conf | unknown when idle |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for name in ORDER:
            log_dir = HERE / f"logs_instrumented/{variant}"
            holder = {}
            def setup(rec, model, human, _s=SETUPS[variant]):
                _s(rec, model, human); holder["rec"] = rec
            rows, st = I4.run_condition(name, beta, unknown, log_dir=log_dir, collect=True, setup=setup)
            rec = holder["rec"]
            m = metrics(name, rows); m["variant"] = variant; m["wrong_task_ranges"] = C.wrong_task_ranges(rows)
            inv = ""
            if variant == "base":
                errs = [float(r[4]) for r in rec._i4d["rows"]]
                m["invariant_max_err"] = max(errs) if errs else 0.0
                inv = f"{m['invariant_max_err']:.1e} ({len(errs)} checks)"
                if m["invariant_max_err"] > 1e-9:
                    ok_all = False
                inv_rows += [(name,) + r for r in rec._i4d["rows"]]
            all_metrics.append(m)
            same = ""
            ref = REF.get(variant)
            if ref is not None:
                same = compare_logs(log_dir / f"{name}.log", ref / f"{name}.log") if (ref / f"{name}.log").exists() else "n/a"
                if same is False:
                    ok_all = False
            bnd = C.boundaries_of(log_dir / f"{name}.log")
            comps = ", ".join(f"{s}:{short(k)}" for s, k, _, _ in st["completions"])
            if st["aborted"]:
                comps += f" — ABORTED at step {st['aborted'][0]} ({st['aborted'][1]}, TODO-52)"
            lines.append(f"| {name} | {same} | {inv} | {' '.join(map(str, bnd)) or '-'} | {comps} | {m['crossings'] or '-'} | {m['reveals']} | "
                         f"{m['wrong_theta_ticks']} ({m['wrong_theta_task_ticks']}) | {m['wrong_task_ranges'] or '-'} | {m['max_conf']} | {m['unknown_when_idle']} |")
            if name.startswith("s40"):
                s40 = "; ".join(f"{k}={m[k]}" for k in ("coffee_max_seg2", "coffee_theta_ticks_seg2", "deliver_max_seg2", "item6_3a_end",
                                                        "item6_3b_start_end", "max_task_seg3", "unknown_end_seg3", "ac_max_184_271",
                                                        "ac_most_likely_ticks_184_271", "at_272"))
                lines.append(f"| ↳ s40 | {s40} | | | | | | | | | | |")
            tag = name if variant == "base" else f"{variant}/{name}"
            retention += C.retention_rows(tag, bnd, st)
            csv_rows["completions"] += [(tag, s, short(k), act, mu) for s, k, act, mu in st["completions"]]
            csv_rows["completion_events"] += [(tag, s, mu, short(k), a, p, v, f"{o:.3f}" if o is not None else "") for s, mu, k, a, p, v, o in st["events"]]
            csv_rows["phase_advances"] += [(tag, s, short(k), a, b) for s, k, a, b in st["advances"]]
            csv_rows["excess"] += [(tag, s, short(k), a, ex, base, p, f"{st['_walked'].get((s, k), float('nan')):.1f}") for s, k, a, ex, base, p in st["excess"]]
            csv_rows["trace"] += [(tag, r["step"], r["segment"], r["truth"], r["human_action"], r["human_micro"], r["human_holding"],
                                   r["most_likely"], round(r["confidence"], 4)) + tuple(round(v, 4) for v in r["dist"].values()) for r in rows]
            if variant == "base":
                st_base[name] = st; rows_base[name] = rows
                if name in RETRIGGER:
                    retrig.append(retrigger(name, rows, log_dir / f"{name}.log"))
            if name.startswith("s40"):
                walked = {(s, short(k)): w for (s, k), w in st["_walked"].items()}
                chains.append(C.chain(tag, "coffee", 113, 160, rows, st, walked))
                chains.append(C.chain(tag, "d(item_6)", 183, 280, rows, st, walked))
        lines.append("")
    headers = {
        "completions": ["condition", "step", "hypothesis", "human_action", "human_micro"],
        "completion_events": ["condition", "step", "microaction", "hypothesis", "judged_action", "predicate", "likelihood", "output_belief"],
        "phase_advances": ["condition", "step", "hypothesis", "from", "to"],
        "excess": ["condition", "step", "hypothesis", "expected_action", "excess_cm", "base", "belief", "walked_cm"],
        "trace": ["condition", "step", "segment", "truth", "human_action", "human_micro", "human_holding", "most_likely", "confidence", "dist..."],
    }
    for fname, header in headers.items():
        with open(HERE / f"{fname}.csv", "w", newline="") as f:
            w = csv.writer(f); w.writerow(header); w.writerows(csv_rows[fname])
    with open(HERE / "invariant.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["condition", "step", "hypothesis", "odds_accumulated", "odds_recognizer", "abs_log_error"]); w.writerows(inv_rows)
    with open(HERE / "retention.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["condition", "boundary", "hypothesis", "advances_in_ended_episode", "base_tick_before", "base_at_boundary", "all_live_bases_equal"])
        w.writerows(retention)
    with open(HERE / "metrics.csv", "w", newline="") as f:
        keys = sorted({k for m in all_metrics for k in m}, key=lambda k: (k not in ("variant", "condition"), k))
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(all_metrics)
    (HERE / "chains.md").write_text("# Causal chains (from the instrumented runs)\n\n" + "\n".join(chains))
    (HERE / "retrigger.md").write_text("# Criterion 2 — the three re-trigger cases under the shipped code\n\n" + "\n".join(retrig))
    (HERE / "region.md").write_text(C.region(st_base, rows_base))
    lines.append(f"\nOVERALL: {'PASS' if ok_all else 'FAIL'}\n")
    (HERE / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return 0 if ok_all else 1


if __name__ == "__main__":
    if "--unit" in sys.argv:
        print("RETIRED: the I4d unit checks encode the pre-grade evidence model; run analysis/g1_graded_evidence/unit_checks.py")
        sys.exit(0)
        for n, ok, d in all_unit_checks():
            print(f"{'PASS' if ok else 'FAIL'}  {n}  {d}")
    else:
        sys.exit(final())
