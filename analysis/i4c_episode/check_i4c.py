#!/usr/bin/env python3
"""
RETIRED (graded evidence, September 2026): the unit checks here encode the pre-grade values (a fitting stretch worth
1/u on its first step; unknown a constant per observation) and the sweep matrix describes the pre-grade HEAD.
They are the record of their report and no longer run at HEAD: `--unit` prints this note. The checks that survive
the grade are restated with graded expectations in analysis/g1_graded_evidence/unit_checks.py, which is the live
set.

analysis/i4c_episode/check_i4c.py — the I4c matrix on I4's harness (analysis/i4_evidence_model/check_i4.py):
the shipped code (both changes) against each change alone and against neither.

Variants (analysis-only monkeypatches; only `base` is shipped):
  base          change 1 (an empty stretch contributes no factor; unknown pays u only on a tick with an
                observation) + change 2 (the belief re-initialises to the prior at an episode boundary)
  empty_only    change 1 alone — the boundary moves origins only (I4b's mechanism), bases untouched
  episode_only  change 2 alone — an empty stretch scores the perfect fit and unknown pays u on every tick
                (I4b's scoring), including on the boundary tick
  neither       both reverted — must equal baseline/ (I4b's run_mesa.py logs at d040e6d) on the four greps

  --final    eight conditions × four variants: summary.md, metrics.csv, the per-tick CSVs (trace, excess,
             phase_advances, completions, completion_events), retention.csv (criterion 7), chains.md (criteria 2–4),
             region.md (criterion 6, closed form from the logged excess — no sweep)
  --unit     I4's U1–U6 re-run, I4c's U7–U9
    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/i4c_episode/check_i4c.py --final
"""
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "i4_evidence_model"))
import check_i4 as I4                                                          # noqa: E402
from check_i4 import ORDER, THETA, short, act_str, metrics, compare_logs, unit_checks   # noqa: E402
from shared import likelihood_functions as LF                                 # noqa: E402

I4.HERE = HERE


# ---------------------------------------------------------------------------
# Variants
# ---------------------------------------------------------------------------

def _instrument(rec):
    """Inner wrapper (installed before I4's outer one): per tick, every live hypothesis's walked distance since
    its origin (an empty stretch is walked == 0) and the factor unknown received (u, or 1 = none)."""
    rec._i4c = {"walked": {}, "ufactor": {}}
    orig = rec.update

    def update(obs, world, prev_belief=None):
        b = orig(obs, world, prev_belief)
        step = int(obs.timestamp); odo = rec._odometer[obs.agent_id]
        for k in rec._expected:
            rec._i4c["walked"][(step, k)] = odo - rec._origin_odo[k]
        bu = rec._base.get("unknown", 0.0)
        rec._i4c["ufactor"][step] = rec._evidence["unknown"] / bu if bu else float("nan")
        return b
    rec.update = update


def _origins_only(rec):
    """Revert change 2: I4b's boundary — origins move, bases and evidence untouched."""
    def begin(pos, odo):
        for k in rec._origin:
            rec._origin[k], rec._origin_odo[k] = pos, odo
    rec._begin_episode = begin


def _perfect_fit_on_empty(rec):
    """Revert change 1: an empty stretch takes the perfect-fit value (so unknown pays u on it, as in I4b)."""
    orig = rec._progress_likelihood

    def prog(action, origin, walked, pos, world, memo):
        v = orig(action, origin, walked, pos, world, memo)
        return LF.PERFECT_FIT_LIKELIHOOD if v is None else v
    rec._progress_likelihood = prog


def setup_base(rec, model, human):
    _instrument(rec)


def setup_empty_only(rec, model, human):
    _origins_only(rec)
    _instrument(rec)


def setup_episode_only(rec, model, human):
    _perfect_fit_on_empty(rec)
    orig_begin = rec._begin_episode

    def begin(pos, odo):
        # the re-initialisation, then I4b's scoring of the (empty) boundary tick: 1 for every task, u for unknown
        orig_begin(pos, odo)
        un = {k: v * (LF.UNKNOWN_LIKELIHOOD if k == "unknown" else 1.0) for k, v in rec._base.items()}
        tot = sum(un.values())
        for k in rec._base:
            rec._base[k] /= tot
        rec._evidence = {k: v / tot for k, v in un.items()}
    rec._begin_episode = begin
    _instrument(rec)


def setup_neither(rec, model, human):
    _perfect_fit_on_empty(rec)
    _origins_only(rec)
    _instrument(rec)


SETUPS = {"base": setup_base, "empty_only": setup_empty_only, "episode_only": setup_episode_only,
          "neither": setup_neither}
REF = {"base": HERE / "new", "neither": HERE / "baseline"}


# ---------------------------------------------------------------------------
# Derived tables
# ---------------------------------------------------------------------------

def wrong_task_ranges(rows):
    """Ticks with confidence ≥ θ whose winner is a task other than the truth, as ranges per winner."""
    out, cur = [], None
    for r in rows:
        wrong = r["confidence"] >= THETA and r["most_likely"] not in (r["truth"], "unknown")
        if wrong and cur and cur[0] == r["most_likely"] and cur[2] == r["step"] - 1:
            cur[2] = r["step"]
        elif wrong:
            if cur:
                out.append(cur)
            cur = [r["most_likely"], r["step"], r["step"]]
        elif cur:
            out.append(cur); cur = None
    if cur:
        out.append(cur)
    return " ".join(f"{w}:{a}-{b}({b - a + 1})" for w, a, b in out)


def boundaries_of(log_path):
    return [int(l.split("step=")[1].split(" ")[0]) for l in open(log_path) if l.startswith("[IR-boundary]")]


def retention_rows(tag, bnds, st):
    """Criterion 7: at every boundary, each live hypothesis's advances during the ended episode, its base on the
    tick before and on the boundary tick. Uniform retention = every base on the boundary tick equal."""
    by_step = defaultdict(dict)
    for s, k, a, ex, base, p in st["excess"]:
        by_step[s][k] = base
    rows, prev = [], -1
    for b in bnds:
        live = by_step.get(b, {})
        bases = sorted(set(round(v, 9) for v in live.values()))
        for k in live:
            adv = sum(1 for s, kk, _, _ in st["advances"] if kk == k and prev < s <= b)
            rows.append((tag, b, short(k), adv, f"{by_step.get(b - 1, {}).get(k, float('nan')):.3e}",
                         f"{live[k]:.6f}", len(bases) == 1))
        prev = b
    return rows


def chain(tag, hyp, a, b, rows, st, walked):
    ex = defaultdict(dict)
    for s, k, act, e, base, p in st["excess"]:
        ex[s][short(k)] = (act, e, base, p)
    out = [f"### {tag} — {hyp}, ticks {a}–{b}\n",
           "| step | seg | human | expected | excess cm | factor | base | P(hyp) | strongest other | P(unknown) | u paid |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        s = r["step"]
        if not (a <= s <= b) or hyp not in ex.get(s, {}):
            continue
        act, e, base, p = ex[s][hyp]
        w = walked.get((s, hyp), None)
        if e == "":
            factor = "1 (no graded signal)"
        elif w is not None and w <= 0.0:
            factor = "none (empty)"
        else:
            factor = f"{LF.logistic_of_excess(float(e)):.3f}"
        others = {k: v for k, v in r["dist"].items() if k not in (hyp, "unknown")}
        ko, vo = max(others.items(), key=lambda kv: kv[1]) if others else ("-", 0.0)
        pu = r["dist"]["unknown"]
        comp = f"{ko} {vo:.3f}" if vo > pu else f"unknown {pu:.3f}"
        u = st["_ufactor"].get(s, float("nan"))
        out.append(f"| {s} | {r['segment']} | {r['human_action']}/{r['human_micro']} | {act[:24]} | {e} | {factor} | "
                   f"{base:.2e} | {r['dist'][hyp]:.3f} | {comp} | {pu:.3f} | {'u' if abs(u - LF.UNKNOWN_LIKELIHOOD) < 1e-12 else '—'} |")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# Criterion 6 — the working region, in closed form from the logged excess (no sweep)
# ---------------------------------------------------------------------------

def region(st_by_cond, rows_by_cond):
    """After a boundary every live base is 1/n and, while no live hypothesis advances, the posterior at each tick is
    L_β(excess_k) / (Σ_j L_β(excess_j) + u) — a closed form in (β, u) over the logged excess trajectories, which do
    not depend on β or u (the human is scripted). Evaluated on I4b's fine grid for s40's segment 2 (coffee) and
    segment 3 (ac / item_6 / unknown), and for the first task by construction (t ≥ 1 identical to I4b)."""
    grid = I4.GRID_ABS_FINE
    lines = ["# Criterion 6 — the working region under I4c, closed form (no simulator run)\n",
             "Within a window with no phase advance and no event, P_t(k) = L_β(e_k(t)) / (Σ_j L_β(e_j(t)) + u) from the "
             "uniform base a boundary leaves. Excess trajectories from the shipped run's excess.csv (s40_on).\n"]
    for cond in ("s40_on", "s40_off"):
        st = st_by_cond[cond]; rows = rows_by_cond[cond]
        ex = defaultdict(dict)
        for s, k, act, e, base, p in st["excess"]:
            ex[s][short(k)] = e
        seg = {r["step"]: r["segment"] for r in rows}
        adv = defaultdict(list)
        for s, k, a, b in st["advances"]:
            adv[s].append(short(k))
        for (name, lo, hi, truth) in (("segment 2: coffee", 115, 183, "coffee"), ("segment 3: ac / item_6 vs unknown", 184, 271, None)):
            steps = [s for s in range(lo, hi + 1) if s in ex]
            advs = {s: adv[s] for s in steps if adv.get(s)}
            lines.append(f"## {cond}, {name} (ticks {lo}–{hi}; advances inside the window: {advs or 'none'})\n")
            lines.append("| β \\ u | " + " | ".join(str(u) for u in grid["unknown"]) + " |")
            lines.append("|---|" + "---|" * len(grid["unknown"]))
            for beta in grid["beta"]:
                cells = []
                for u in grid["unknown"]:
                    cross, peak, wrong = None, 0.0, 0
                    for s in steps:
                        live = {k: e for k, e in ex[s].items()}
                        L = {k: (1.0 if e == "" else LF.logistic_of_excess(float(e), beta)) for k, e in live.items()}
                        tot = sum(L.values()) + u
                        post = {k: v / tot for k, v in L.items()}; post["unknown"] = u / tot
                        w = max(post, key=lambda k: post[k])
                        if truth:
                            if post[truth] > peak:
                                peak = post[truth]
                            if cross is None and post[truth] >= THETA:
                                cross = s
                        else:
                            if post[w] >= THETA and w != "unknown":
                                wrong += 1
                    cells.append(f"{cross or '—'} ({peak:.2f})" if truth else f"{wrong}")
                lines.append(f"| {beta} | " + " | ".join(cells) + " |")
            lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Unit checks
# ---------------------------------------------------------------------------

def unit_checks_i4c():
    from shared.types import (Const, DomainModel, WorldState, AgentState, Observation, SpatialContext, ActionContext,
                              Predicate)
    from shared.domain_knowledge import DomainKnowledgeBase, ContextKnowledge
    from shared.recognizer import IntentionRecognizer, HypothesisKey, BELIEF_FLOOR
    from domains.kitting.actions import move_to, pick_up, place
    from domains.kitting.tasks import deliver_item
    I4.apply_constants(0.01, 0.1)
    u = LF.UNKNOWN_LIKELIHOOD
    out = []

    def _obs(agent, pos, mu="step", t=0.0):
        return Observation(timestamp=t, agent_id=agent, detected_microaction=mu,
                           spatial_context=SpatialContext(position=pos, orientation=0.0, zone="z"),
                           action_context=ActionContext())

    def _world(agent, pos, predicates=(), objects=None, locations=None, holding=None, t=0.0, home=None):
        w = WorldState(timestamp=t, agent_states={agent: AgentState(agent, "z", holding=holding)},
                       agent_positions={agent: pos}, predicates=set(predicates),
                       object_positions=dict(objects or {}), object_locations=dict(locations or {}),
                       object_zones={k: "z" for k in (objects or {})},
                       object_home_container=dict(home if home is not None else (locations or {})))
        return w

    kb = DomainKnowledgeBase(DomainModel(tasks={"deliver_item": deliver_item},
                                         actions={"move_to": move_to, "pick_up": pick_up, "place": place},
                                         microactions=["STEP", "GRASP", "RELEASE"], intentions={"deliver_item"}))
    objs = {"shelf_a": (400.0, 0.0), "item_a": (400.0, 0.0), "shelf_b": (0.0, 400.0), "item_b": (0.0, 400.0),
            "table_0": (0.0, -400.0)}
    locs = {"item_a": "shelf_a", "item_b": "shelf_b"}
    ha = HypothesisKey("deliver_item", {"?item": "item_a", "?kitting_table": "table_0"})
    hb = HypothesisKey("deliver_item", {"?item": "item_b", "?kitting_table": "table_0"})
    P = lambda name, *args: Predicate(name, tuple(Const(a) for a in args))

    # U7 — t = 0 and a stationary tick report the prior exactly; the first step scores everyone
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    d0 = rec.update(_obs("h", (0.0, 0.0), "stand", t=0), _world("h", (0.0, 0.0), objects=objs, locations=locs, t=0)).distribution
    d1 = rec.update(_obs("h", (0.0, 0.0), "stand", t=1), _world("h", (0.0, 0.0), objects=objs, locations=locs, t=1)).distribution
    d2 = rec.update(_obs("h", (20.0, 0.0), t=2), _world("h", (20.0, 0.0), objects=objs, locations=locs, t=2)).distribution
    ex_b = 20 + math.hypot(20, 400) - 400.0
    ok = (all(abs(v - 1 / 3) < 1e-12 for v in d0.values()) and d1 == d0
          and abs(d2[repr(ha)] / d2["unknown"] - 1 / u) < 1e-9
          and abs(d2[repr(hb)] / d2["unknown"] - LF.logistic_of_excess(ex_b) / u) < 1e-9)
    out.append(("U7 t = 0 and a stationary tick after it report the prior exactly (1/3, 1/3, 1/3: no factor, unknown pays "
                "nothing); the first step scores a at 1/u and b at L(excess)/u", ok,
                f"t=0 {tuple(round(v, 4) for v in d0.values())}, t=1 same={d1 == d0}, t=2 a:u={d2[repr(ha)]/d2['unknown']:.3f} "
                f"b:u={d2[repr(hb)]/d2['unknown']:.4f} (expected {LF.logistic_of_excess(ex_b)/u:.4f})"))

    # U8 — the episode boundary: uniform re-initialisation regardless of phase history
    hc = HypothesisKey("deliver_item", {"?item": "item_c", "?kitting_table": "table_0"})
    objs3 = {**objs, "item_c": (400.0, 0.0)}
    locs3 = {**locs, "item_c": "shelf_a"}
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb, hc])
    rec.update(_obs("h", (0.0, 0.0), "stand", t=0), _world("h", (0.0, 0.0), objects=objs3, locations=locs3, t=0))
    t = 0
    for i in range(1, 20):                         # walk east to (380, 0): at(shelf_a) holds from 380 (dist 20 ≤ 30)
        t += 1; p = (20.0 * i, 0.0)
        preds = [P("at", "h", "shelf_a"), P("at", "h", "item_a"), P("at", "h", "item_c")] if 400 - 20 * i <= 30 else []
        rec.update(_obs("h", p, t=t), _world("h", p, predicates=preds, objects=objs3, locations=locs3, t=t))
    adv_before = {repr(ha): act_str(rec._expected[repr(ha)]), repr(hb): act_str(rec._expected[repr(hb)]), repr(hc): act_str(rec._expected[repr(hc)])}
    t += 1                                         # grasp item_a at (380, 0)
    p = (380.0, 0.0)
    preds = [P("at", "h", "shelf_a"), P("at", "h", "item_c"), P("holding", "h", "item_a")]
    rec.update(_obs("h", p, "grasp", t=t), _world("h", p, predicates=preds, objects={**objs3, "item_a": p},
                                                  locations={**locs3, "item_a": "h"}, holding="item_a", t=t, home=locs3))
    for i in range(1, 21):                         # carry to the table (0, -400), arriving at i = 20
        t += 1; p = (380.0 - 19.0 * i, -20.0 * i)
        preds = [P("holding", "h", "item_a")] + ([P("at", "h", "table_0")] if i == 20 else [])
        rec.update(_obs("h", p, t=t), _world("h", p, predicates=preds, objects={**objs3, "item_a": p},
                                             locations={**locs3, "item_a": "h"}, holding="item_a", t=t, home=locs3))
    base_before = {k: rec._base[k] for k in rec._base}
    adv_hist = {k: act_str(rec._expected[k]) for k in rec._expected}
    t += 1                                         # release: obj_at(item_a, table_0) — ha's terminal, expected on the previous tick
    p = (0.0, -400.0)
    preds = [P("at", "h", "table_0"), P("obj_at", "item_a", "table_0")]
    br = rec.update(_obs("h", p, "release", t=t), _world("h", p, predicates=preds, objects={**objs3, "item_a": p},
                                                         locations={**locs3, "item_a": "table_0"}, t=t, home=locs3))
    base_after = dict(rec._base)
    exp_out = rec._pin({repr(hb): 1 / 3, repr(hc): 1 / 3, "unknown": 1 / 3}, {repr(ha)})
    t += 1
    bs = rec.update(_obs("h", p, "stand", t=t), _world("h", p, predicates=preds, objects={**objs3, "item_a": p},
                                                       locations={**locs3, "item_a": "table_0"}, t=t, home=locs3))
    t += 1                                         # one step toward shelf_b
    p2 = (0.0, -380.0)
    bw = rec.update(_obs("h", p2, t=t), _world("h", p2, predicates=[P("obj_at", "item_a", "table_0")], objects={**objs3, "item_a": p},
                                               locations={**locs3, "item_a": "table_0"}, t=t, home=locs3))
    ex_c = 20 + math.hypot(400, 380) - math.hypot(400, 400)
    differed = abs(base_before[repr(hb)] - base_before[repr(hc)]) > 1e-12
    uniform = abs(base_after[repr(hb)] - 1 / 3) < 1e-12 and abs(base_after[repr(hc)] - 1 / 3) < 1e-12 and abs(base_after["unknown"] - 1 / 3) < 1e-12
    reported = all(abs(br.distribution[k] - exp_out[k]) < 1e-12 for k in exp_out) and bs.distribution == br.distribution
    scored = (abs(bw.distribution[repr(hb)] / bw.distribution["unknown"] - 1 / u) < 1e-9
              and abs(bw.distribution[repr(hc)] / bw.distribution["unknown"] - LF.logistic_of_excess(ex_c) / u) < 1e-9)
    ok = repr(ha) in rec._completed and differed and uniform and reported and scored and all(rec._origin[k] == p for k in rec._origin)
    out.append(("U8 episode boundary: before it b (one method flip at the grasp) and c (advanced at the shelf, false alarm at the grasp, "
                "flipped) hold different bases; on the boundary tick both are 1/3 with unknown, the output is the pinned prior, a "
                "stationary tick keeps it, and one step toward shelf_b scores b at 1/u and c at L(excess)/u from the new origin", ok,
                f"before: b {base_before[repr(hb)]:.3e} c {base_before[repr(hc)]:.3e} (expected {adv_hist[repr(hb)]} / {adv_hist[repr(hc)]}); "
                f"after: b {base_after[repr(hb)]:.4f} c {base_after[repr(hc)]:.4f} u {base_after['unknown']:.4f}; "
                f"boundary tick P(b)={br.distribution[repr(hb)]:.4f} P(a)={br.distribution[repr(ha)]:.3f}; step: b:u {bw.distribution[repr(hb)]/bw.distribution['unknown']:.2f}"))

    # U9 — the pin without the boundary: another agent completes item_b while h walks toward shelf_a
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    rec.update(_obs("h", (0.0, 0.0), "stand", t=0), _world("h", (0.0, 0.0), objects=objs, locations=locs, t=0))
    for i in range(1, 6):
        b5 = rec.update(_obs("h", (20.0 * i, 0.0), t=i), _world("h", (20.0 * i, 0.0), objects=objs, locations=locs, t=i))
    p = (120.0, 0.0)
    b6 = rec.update(_obs("h", p, t=6), _world("h", p, predicates=[P("obj_at", "item_b", "table_0")],
                                             objects={**objs, "item_b": (0.0, -400.0)}, locations={"item_a": "shelf_a", "item_b": "table_0"}, t=6, home=locs))
    ok = (repr(hb) in rec._completed and rec._origin[repr(ha)] == (0.0, 0.0)
          and abs(b6.distribution[repr(ha)] / b6.distribution["unknown"] - 1 / u) < 1e-9
          and abs(b5.distribution[repr(ha)] / b5.distribution["unknown"] - 1 / u) < 1e-9
          and b6.distribution[repr(hb)] == BELIEF_FLOOR)
    out.append(("U9 a completion the observed agent's phase did not reach (item_b delivered by someone else mid-walk) pins b and is "
                "no boundary: a's origin stays, a:unknown stays 1/u, nothing re-initialises", ok,
                f"b pinned {b6.distribution[repr(hb)]:.3f}, a origin {rec._origin[repr(ha)]}, a:u {b6.distribution[repr(ha)]/b6.distribution['unknown']:.2f}"))
    return out


def all_unit_checks():
    return unit_checks() + unit_checks_i4c()


# ---------------------------------------------------------------------------
# Final matrix
# ---------------------------------------------------------------------------

def final():
    beta, unknown = LF.BETA, LF.UNKNOWN_LIKELIHOOD
    lines = [f"# I4c checks — generated by check_i4c.py (BETA={beta}, UNKNOWN_LIKELIHOOD={unknown})\n"]
    lines.append("## Unit checks\n\n| check | result | detail |\n|---|---|---|")
    ok_all = True
    for n, ok, d in all_unit_checks():
        ok_all &= ok
        lines.append(f"| {n} | {'PASS' if ok else 'FAIL'} | {d} |")
    lines.append("")
    csv_rows = defaultdict(list); all_metrics = []; retention = []; chains = []
    st_base, rows_base = {}, {}
    for variant in SETUPS:
        title = {"base": "Instrumented sweep (variant `base` = the shipped code: both changes)"}.get(
            variant, f"Variant `{variant}` (analysis-only monkeypatch)")
        lines.append(f"## {title}\n")
        lines.append("| condition | log == ref | boundaries | completions | θ crossings (`!` = winner ≠ truth) | reveals | wrong-θ ticks (task) | wrong-task ranges | max conf | unknown when idle |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|")
        for name in ORDER:
            log_dir = HERE / f"logs_instrumented/{variant}"
            rows, st = I4.run_condition(name, beta, unknown, log_dir=log_dir, collect=True, setup=SETUPS[variant])
            # the inner instrumentation lives on the recognizer; fetch it back through the model's robot
            from mesa_sim.sim_model import SimModel  # noqa: F401  (already imported by run_condition)
            m = metrics(name, rows); m["variant"] = variant; m["wrong_task_ranges"] = wrong_task_ranges(rows)
            all_metrics.append(m)
            same = ""
            ref = REF.get(variant)
            if ref is not None:
                same = compare_logs(log_dir / f"{name}.log", ref / f"{name}.log") if (ref / f"{name}.log").exists() else "n/a"
                if same is False:
                    ok_all = False
            bnd = boundaries_of(log_dir / f"{name}.log")
            comps = ", ".join(f"{s}:{short(k)}" for s, k, _, _ in st["completions"])
            if st["aborted"]:
                comps += f" — ABORTED at step {st['aborted'][0]} ({st['aborted'][1]}, TODO-52)"
            lines.append(f"| {name} | {same} | {' '.join(map(str, bnd)) or '-'} | {comps} | {m['crossings'] or '-'} | {m['reveals']} | "
                         f"{m['wrong_theta_ticks']} ({m['wrong_theta_task_ticks']}) | {m['wrong_task_ranges'] or '-'} | {m['max_conf']} | {m['unknown_when_idle']} |")
            if name.startswith("s40"):
                s40 = "; ".join(f"{k}={m[k]}" for k in ("coffee_max_seg2", "coffee_theta_ticks_seg2", "deliver_max_seg2", "item6_3a_end",
                                                        "item6_3b_start_end", "max_task_seg3", "unknown_end_seg3", "ac_max_184_271",
                                                        "ac_most_likely_ticks_184_271", "at_272"))
                lines.append(f"| ↳ s40 | {s40} | | | | | | | | |")
            tag = name if variant == "base" else f"{variant}/{name}"
            retention += retention_rows(tag, bnd, st)
            csv_rows["completions"] += [(tag, s, short(k), act, mu) for s, k, act, mu in st["completions"]]
            csv_rows["completion_events"] += [(tag, s, mu, short(k), a, p, v, f"{o:.3f}" if o is not None else "") for s, mu, k, a, p, v, o in st["events"]]
            csv_rows["phase_advances"] += [(tag, s, short(k), a, b) for s, k, a, b in st["advances"]]
            csv_rows["excess"] += [(tag, s, short(k), a, ex, base, p, f"{st['_walked'].get((s, k), float('nan')):.1f}") for s, k, a, ex, base, p in st["excess"]]
            csv_rows["trace"] += [(tag, r["step"], r["segment"], r["truth"], r["human_action"], r["human_micro"], r["human_holding"],
                                   r["most_likely"], round(r["confidence"], 4), st["_ufactor"].get(r["step"], "")) + tuple(round(v, 4) for v in r["dist"].values()) for r in rows]
            if variant == "base":
                st_base[name] = st; rows_base[name] = rows
            if name.startswith("s40") and variant in ("base", "empty_only", "episode_only"):
                walked = {(s, short(k)): w for (s, k), w in st["_walked"].items()}
                chains.append(chain(tag, "coffee", 113, 160, rows, st, walked))
                chains.append(chain(tag, "d(item_6)", 183, 275, rows, st, walked))
                chains.append(chain(tag, "ac", 183, 215, rows, st, walked))
                chains.append(chain(tag, "ac", 329, 380, rows, st, walked))
        lines.append("")
    headers = {
        "completions": ["condition", "step", "hypothesis", "human_action", "human_micro"],
        "completion_events": ["condition", "step", "microaction", "hypothesis", "judged_action", "predicate", "likelihood", "output_belief"],
        "phase_advances": ["condition", "step", "hypothesis", "from", "to"],
        "excess": ["condition", "step", "hypothesis", "expected_action", "excess_cm", "base", "belief", "walked_cm"],
        "trace": ["condition", "step", "segment", "truth", "human_action", "human_micro", "human_holding", "most_likely", "confidence", "u_factor", "dist..."],
    }
    for fname, header in headers.items():
        with open(HERE / f"{fname}.csv", "w", newline="") as f:
            w = csv.writer(f); w.writerow(header); w.writerows(csv_rows[fname])
    with open(HERE / "retention.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["condition", "boundary", "hypothesis", "advances_in_ended_episode", "base_tick_before", "base_at_boundary", "all_live_bases_equal"])
        w.writerows(retention)
    with open(HERE / "metrics.csv", "w", newline="") as f:
        keys = sorted({k for m in all_metrics for k in m}, key=lambda k: (k not in ("variant", "condition"), k))
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(all_metrics)
    (HERE / "chains.md").write_text("# Causal chains (from the instrumented runs)\n\n" + "\n".join(chains))
    (HERE / "region.md").write_text(region(st_base, rows_base))
    lines.append(f"\nOVERALL: {'PASS' if ok_all else 'FAIL'}\n")
    (HERE / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return 0 if ok_all else 1


# I4's run_condition keeps the recognizer private; expose the inner instrumentation through the stats dict.
_orig_run = I4.run_condition


def _run_condition(name, beta, unknown, frac=False, variant="base", log_dir=None, collect=False, setup=None):
    holder = {}

    def setup2(rec, model, human):
        setup(rec, model, human)
        holder["rec"] = rec
    rows, st = _orig_run(name, beta, unknown, frac, variant, log_dir, collect, setup2)
    rec = holder["rec"]
    st["_walked"] = rec._i4c["walked"]; st["_ufactor"] = rec._i4c["ufactor"]
    return rows, st


I4.run_condition = _run_condition


if __name__ == "__main__":
    if "--unit" in sys.argv:
        print("RETIRED: the I4c unit checks encode the pre-grade evidence model; run analysis/g1_graded_evidence/unit_checks.py")
        sys.exit(0)
        for n, ok, d in all_unit_checks():
            print(f"{'PASS' if ok else 'FAIL'}  {n}  {d}")
    else:
        sys.exit(final())
