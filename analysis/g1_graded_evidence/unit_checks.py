#!/usr/bin/env python3
"""
analysis/g1_graded_evidence/unit_checks.py — the recognizer's unit checks under graded evidence.

The I4 / I4c / I4d harnesses (analysis/i4_evidence_model/check_i4.py, i4c_episode/check_i4c.py,
i4d_fold_unknown/check_i4d.py, `--unit`) encoded the pre-grade values (a fitting stretch worth 1/u on its first
step). They are retired as records of their reports; the checks that survive the grade are restated here with
the graded expectations, and this is the file that runs at HEAD. Same toy world as I4's: shelf_a at (400, 0),
shelf_b at (0, 400), table_0 at (0, −400), β = 0.01, u = 0.1.

    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/g1_graded_evidence/unit_checks.py

G0   the grade functions: covered_fraction clips to [0, 1] and is 0 on an empty path; u^f composes (half + half = whole)
G1   (I4 U1) straight walk 200 of 400 cm: a:u = u^−0.5; b, walked away from, pays L(excess) alone (f = 0)
G2   (I4 U2) stationary ticks change nothing
G3   (I4 U3) out 200 and back: the target's excess is 400 cm and the stretch covered nothing — a:u = L(400)
G4   (I4 U4, I4d U10) the arrival: u^−0.9 one step before, 100 at the fold (f = 1 by the completion fact × open pick_up)
G5   (I4d U5'') the grasp: base a:b 1000 (the event), evidence a:b 100, a:u 1/u before and after
G6   (I4 U6) recognizer.py names no predicate / parameter / action / removed mechanism / old constant
G7   (I4c U7) t = 0 and a stationary tick report the prior exactly; the first 20 cm step scores a at u^−0.05
G8   (I4c U8) the episode boundary re-initialises uniformly; the first step after it is graded from the new origin
G9   (I4c U9) a completion the agent's phase did not reach pins and is no boundary; a:u stays on its graded walk
G10  (I4d U10) the fold keeps unknown's graded contribution: 100 on the grasp tick, 100 · u^−1/28 one carry step later
"""
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

from shared import likelihood_functions as LF                                 # noqa: E402

UNKNOWN = "unknown"


def act_str(a):
    return "None" if a is None else f"{a.action_name}({','.join(f'{k}={v}' for k, v in sorted(a.bindings.items()))})"


def unit_checks():
    from shared.types import (Const, DomainModel, WorldState, AgentState, Observation, SpatialContext, ActionContext,
                              Predicate)
    from shared.domain_knowledge import DomainKnowledgeBase, ContextKnowledge
    from shared.recognizer import IntentionRecognizer, HypothesisKey
    from domains.kitting.actions import move_to, pick_up, place
    from domains.kitting.tasks import deliver_item
    assert LF.BETA == 0.01 and LF.UNKNOWN_LIKELIHOOD == 0.1, "the expectations below are for β = 0.01, u = 0.1"
    u = LF.UNKNOWN_LIKELIHOOD
    out = []

    def _obs(agent, pos, mu="step", t=0.0):
        return Observation(timestamp=t, agent_id=agent, detected_microaction=mu,
                           spatial_context=SpatialContext(position=pos, orientation=0.0, zone="z"),
                           action_context=ActionContext())

    def _world(agent, pos, predicates=(), objects=None, locations=None, holding=None, t=0.0, home=None):
        return WorldState(timestamp=t, agent_states={agent: AgentState(agent, "z", holding=holding)},
                          agent_positions={agent: pos}, predicates=set(predicates),
                          object_positions=dict(objects or {}), object_locations=dict(locations or {}),
                          object_zones={k: "z" for k in (objects or {})},
                          object_home_container=dict(home if home is not None else (locations or {})))

    kb = DomainKnowledgeBase(DomainModel(tasks={"deliver_item": deliver_item},
                                         actions={"move_to": move_to, "pick_up": pick_up, "place": place},
                                         microactions=["STEP", "GRASP", "RELEASE"], intentions={"deliver_item"}))
    objs = {"shelf_a": (400.0, 0.0), "item_a": (400.0, 0.0), "shelf_b": (0.0, 400.0), "item_b": (0.0, 400.0),
            "table_0": (0.0, -400.0)}
    locs = {"item_a": "shelf_a", "item_b": "shelf_b"}
    ha = HypothesisKey("deliver_item", {"?item": "item_a", "?kitting_table": "table_0"})
    hb = HypothesisKey("deliver_item", {"?item": "item_b", "?kitting_table": "table_0"})
    P = lambda name, *args: Predicate(name, tuple(Const(a) for a in args))
    odds = lambda d, k: d[k] / d[UNKNOWN]
    near = lambda x, y, tol=1e-9: abs(x - y) < tol
    ex_b = lambda x: x + math.hypot(x, 400) - 400            # b's excess after walking x east from (0, 0)

    # G0 — the grade functions
    cf = LF.covered_fraction
    ok = (near(cf((0, 0), (200, 0), (400, 0)), 0.5) and cf((0, 0), (0, 0), (400, 0)) == 0.0
          and cf((0, 0), (-100, 0), (400, 0)) == 0.0 and cf((0, 0), (400, 0), (400, 0)) == 1.0
          and cf((400, 0), (200, 0), (400, 0)) == 0.0
          and near(LF.graded_unknown_likelihood(0.5) ** 2, LF.graded_unknown_likelihood(1.0))
          and LF.graded_unknown_likelihood(0.0) == 1.0 and LF.graded_unknown_likelihood(1.0) == u)
    out.append(("G0 covered_fraction: 0.5 half-way, 0 at the origin, 0 walked away, 1 at the target, 0 on an empty path; "
                "u^f: 1 at 0, u at 1, and (u^0.5)² = u", ok, ""))

    # G1 — straight walk 200 cm east
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    rec.update(_obs("h", (0.0, 0.0), t=0), _world("h", (0.0, 0.0), objects=objs, locations=locs, t=0))
    for i in range(1, 11):
        b = rec.update(_obs("h", (20.0 * i, 0.0), t=i), _world("h", (20.0 * i, 0.0), objects=objs, locations=locs, t=i))
    d = b.distribution
    ok = near(odds(d, repr(ha)), u ** -0.5) and near(odds(d, repr(hb)), LF.logistic_of_excess(ex_b(200)))
    out.append(("G1 straight walk 200 of 400 cm: a:u = u^−0.5 (zero excess, half the path); b (walked away from, f = 0) "
                "pays L(excess) alone", ok, f"a:u {odds(d, repr(ha)):.4f} (expected {u ** -0.5:.4f}), b:u {odds(d, repr(hb)):.4f} "
                f"(expected {LF.logistic_of_excess(ex_b(200)):.4f})"))

    # G2 — stationary ticks
    b0 = dict(d)
    for i in range(11, 31):
        b = rec.update(_obs("h", (200.0, 0.0), "stand", t=i), _world("h", (200.0, 0.0), objects=objs, locations=locs, t=i))
    out.append(("G2 twenty stationary ticks leave the belief unchanged (replace, not multiply)",
                all(abs(b.distribution[k] - b0[k]) < 1e-12 for k in b0), ""))

    # G3 — out and back
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    rec.update(_obs("h", (0.0, 0.0), t=0), _world("h", (0.0, 0.0), objects=objs, locations=locs, t=0))
    path = [(20.0 * i, 0.0) for i in range(1, 11)] + [(200.0 - 20.0 * i, 0.0) for i in range(1, 11)]
    for i, p in enumerate(path, 1):
        b = rec.update(_obs("h", p, t=i), _world("h", p, objects=objs, locations=locs, t=i))
    ok = near(odds(b.distribution, repr(ha)), LF.logistic_of_excess(400.0))
    out.append(("G3 out 200 cm and back: excess 400 cm and nothing covered (f = 0) — a:u = L(400), the refutation in full, "
                "no confirmation", ok, f"a:u {odds(b.distribution, repr(ha)):.4f} (expected {LF.logistic_of_excess(400.0):.4f})"))

    # G4 / G10 — the walk to shelf_a, the arrival, the grasp, one carry step
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    rec.update(_obs("h", (0.0, 0.0), "stand", t=0), _world("h", (0.0, 0.0), objects=objs, locations=locs, t=0))
    r = {}
    for i in range(1, 20):
        p = (20.0 * i, 0.0)
        preds = [P("at", "h", "shelf_a"), P("at", "h", "item_a")] if 400 - 20 * i <= 30 else []
        b = rec.update(_obs("h", p, t=i), _world("h", p, predicates=preds, objects=objs, locations=locs, t=i))
        r[i] = (odds(rec._evidence, repr(ha)), odds(rec._evidence, repr(hb)))
    ok = (near(r[18][0], u ** -0.9) and near(r[19][0], u ** -2) and act_str(rec._expected[repr(ha)]).startswith("pick_up")
          and near(r[18][1], LF.logistic_of_excess(ex_b(360))) and near(r[19][1], LF.logistic_of_excess(ex_b(380))))
    out.append(("G4 the arrival: a:u = u^−0.9 at 360 cm, 100 at 380 cm — the fold at f = 1 by the completion fact (1/u) × the "
                "open pick_up (1/u, ungraded); b:u = L(excess) throughout (f = 0)", ok,
                f"a:u {r[18][0]:.4f} → {r[19][0]:.2f}; b:u {r[18][1]:.4f} → {r[19][1]:.4f}; a expects {act_str(rec._expected[repr(ha)])}"))
    p = (380.0, 0.0)
    rec.update(_obs("h", p, "grasp", t=20), _world("h", p, predicates=[P("at", "h", "shelf_a"), P("holding", "h", "item_a")],
                                                  objects={**objs, "item_a": p}, locations={**locs, "item_a": "h"}, holding="item_a", t=20, home=locs))
    a20 = odds(rec._evidence, repr(ha))
    step = math.hypot(380, 400) / 28
    p21 = (380.0 - 380 / 28, -400 / 28)                                    # one step straight at the table
    rec.update(_obs("h", p21, t=21), _world("h", p21, predicates=[P("holding", "h", "item_a")],
                                            objects={**objs, "item_a": p21}, locations={**locs, "item_a": "h"}, holding="item_a", t=21, home=locs))
    a21 = odds(rec._evidence, repr(ha))
    ok = near(a20, u ** -2) and near(a21, u ** -(2 + 1 / 28), 1e-6) and act_str(rec._expected[repr(ha)]).startswith("move_to")
    out.append(("G10 the fold keeps unknown's graded contribution: 100 on the grasp tick (pick_up folds ungraded, the carry stretch is "
                "empty), 100 · u^−1/28 one step into the 552 cm carry", ok, f"a:u {a20:.2f} → {a21:.2f} (expected {u ** -(2 + 1 / 28):.2f})"))

    # G5 — the grasp with a rival at the same shelf (I4d's U5'')
    objs2 = {"shelf_0": (200.0, 0.0), "item_a": (200.0, 0.0), "item_b": (200.0, 0.0), "table_0": (0.0, 400.0)}
    locs2 = {"item_a": "shelf_0", "item_b": "shelf_0"}
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    at = [P("at", "h", "shelf_0"), P("at", "h", "item_a"), P("at", "h", "item_b")]
    rec.update(_obs("h", (180.0, 0.0), "stand", t=0), _world("h", (180.0, 0.0), predicates=at, objects=objs2, locations=locs2, t=0))
    rec.update(_obs("h", (180.0, 0.0), "stand", t=1), _world("h", (180.0, 0.0), predicates=at, objects=objs2, locations=locs2, t=1))
    r1 = odds(rec._evidence, repr(ha))
    w1 = _world("h", (180.0, 0.0), predicates=at[:1] + at[2:] + [P("holding", "h", "item_a")], objects={**objs2, "item_a": (180.0, 0.0)},
                locations={"item_a": "h", "item_b": "shelf_0"}, holding="item_a", t=2, home=locs2)
    rec.update(_obs("h", (180.0, 0.0), "grasp", t=2), w1)
    ev = rec._evidence
    ok = (near(rec._base[repr(ha)] / rec._base[repr(hb)], 1000.0, 1e-6) and near(ev[repr(ha)] / ev[repr(hb)], 1000.0 * u, 1e-6)
          and near(r1, 1 / u) and near(odds(ev, repr(ha)), 1 / u) and act_str(rec._expected[repr(hb)]).startswith("place"))
    out.append(("G5 the grasp: base a:b 1000 (hit / false alarm), evidence a:b 100 (b's new place phase is one ungraded observation, "
                "a's carry stretch is empty); a:u 1/u before and after (a stationary pick_up phase, ungraded)", ok,
                f"base a:b {rec._base[repr(ha)] / rec._base[repr(hb)]:.1f}, evidence a:b {ev[repr(ha)] / ev[repr(hb)]:.1f}, a:u {r1:.1f} → {odds(ev, repr(ha)):.1f}"))

    # G6 — source grep
    src = (ROOT / "shared" / "recognizer.py").read_text()
    code = "\n".join(l for l in src.splitlines() if not l.strip().startswith("#"))
    code_no_doc = re.sub(r'"""[\s\S]*?"""', "", code)
    bad = [w for w in ('"holding"', '"in_zone"', '"at"', '"obj_at"', '"waited"', '"?item"', '"move_to"', "ZONE_BOOST",
                       "_refuted_by_holding", "HIGH_LIKELIHOOD", "LOW_LIKELIHOOD", "NEUTRAL_LIKELIHOOD", "CONFIDENCE_THRESHOLD")
           if w in code_no_doc]
    out.append(("G6 recognizer.py code names no predicate / parameter / action / removed mechanism / old constant", not bad,
                f"found: {bad}" if bad else ""))

    # G7 — t = 0, a stationary tick, the first step
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    d0 = rec.update(_obs("h", (0.0, 0.0), "stand", t=0), _world("h", (0.0, 0.0), objects=objs, locations=locs, t=0)).distribution
    d1 = rec.update(_obs("h", (0.0, 0.0), "stand", t=1), _world("h", (0.0, 0.0), objects=objs, locations=locs, t=1)).distribution
    d2 = rec.update(_obs("h", (20.0, 0.0), t=2), _world("h", (20.0, 0.0), objects=objs, locations=locs, t=2)).distribution
    ok = (all(abs(v - 1 / 3) < 1e-12 for v in d0.values()) and d1 == d0
          and near(odds(d2, repr(ha)), u ** -0.05) and near(odds(d2, repr(hb)), LF.logistic_of_excess(ex_b(20))))
    out.append(("G7 t = 0 and a stationary tick report the prior exactly (1/3 each: no factor); the first 20 cm step scores a at "
                "u^−0.05 = 1.122 (one twentieth of its path) and b at L(excess) (f = 0)", ok,
                f"t=0 {tuple(round(v, 4) for v in d0.values())}, t=1 same={d1 == d0}, t=2 a:u {odds(d2, repr(ha)):.3f} b:u {odds(d2, repr(hb)):.4f}"))

    # G8 — the episode boundary
    hc = HypothesisKey("deliver_item", {"?item": "item_c", "?kitting_table": "table_0"})
    objs3 = {**objs, "item_c": (400.0, 0.0)}
    locs3 = {**locs, "item_c": "shelf_a"}
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb, hc])
    rec.update(_obs("h", (0.0, 0.0), "stand", t=0), _world("h", (0.0, 0.0), objects=objs3, locations=locs3, t=0))
    t = 0
    for i in range(1, 20):
        t += 1; p = (20.0 * i, 0.0)
        preds = [P("at", "h", "shelf_a"), P("at", "h", "item_a"), P("at", "h", "item_c")] if 400 - 20 * i <= 30 else []
        rec.update(_obs("h", p, t=t), _world("h", p, predicates=preds, objects=objs3, locations=locs3, t=t))
    t += 1; p = (380.0, 0.0)
    preds = [P("at", "h", "shelf_a"), P("at", "h", "item_c"), P("holding", "h", "item_a")]
    rec.update(_obs("h", p, "grasp", t=t), _world("h", p, predicates=preds, objects={**objs3, "item_a": p},
                                                  locations={**locs3, "item_a": "h"}, holding="item_a", t=t, home=locs3))
    for i in range(1, 21):
        t += 1; p = (380.0 - 19.0 * i, -20.0 * i)
        preds = [P("holding", "h", "item_a")] + ([P("at", "h", "table_0")] if i == 20 else [])
        rec.update(_obs("h", p, t=t), _world("h", p, predicates=preds, objects={**objs3, "item_a": p},
                                             locations={**locs3, "item_a": "h"}, holding="item_a", t=t, home=locs3))
    base_before = dict(rec._base)
    t += 1; p = (0.0, -400.0)
    preds = [P("at", "h", "table_0"), P("obj_at", "item_a", "table_0")]
    br = rec.update(_obs("h", p, "release", t=t), _world("h", p, predicates=preds, objects={**objs3, "item_a": p},
                                                         locations={**locs3, "item_a": "table_0"}, t=t, home=locs3))
    base_after = dict(rec._base)
    exp_out = rec._pin({repr(hb): 1 / 3, repr(hc): 1 / 3, UNKNOWN: 1 / 3}, {repr(ha)})
    t += 1
    bs = rec.update(_obs("h", p, "stand", t=t), _world("h", p, predicates=preds, objects={**objs3, "item_a": p},
                                                       locations={**locs3, "item_a": "table_0"}, t=t, home=locs3))
    t += 1; p2 = (0.0, -380.0)
    bw = rec.update(_obs("h", p2, t=t), _world("h", p2, predicates=[P("obj_at", "item_a", "table_0")], objects={**objs3, "item_a": p},
                                               locations={**locs3, "item_a": "table_0"}, t=t, home=locs3))
    f_b = 20 / 800                                                          # shelf_b is 800 cm north of the table
    f_c = (math.hypot(400, 400) - math.hypot(400, 380)) / math.hypot(400, 400)
    ex_c = 20 + math.hypot(400, 380) - math.hypot(400, 400)
    differed = abs(base_before[repr(hb)] - base_before[repr(hc)]) > 1e-12
    uniform = all(abs(base_after[k] - 1 / 3) < 1e-12 for k in (repr(hb), repr(hc), UNKNOWN))
    reported = all(abs(br.distribution[k] - exp_out[k]) < 1e-12 for k in exp_out) and bs.distribution == br.distribution
    scored = near(odds(bw.distribution, repr(hb)), u ** -f_b) and near(odds(bw.distribution, repr(hc)), LF.logistic_of_excess(ex_c) * u ** -f_c)
    ok = repr(ha) in rec._completed and differed and uniform and reported and scored and all(rec._origin[k] == p for k in rec._origin)
    out.append(("G8 episode boundary: b and c hold different bases before it; on the boundary tick every live base is 1/3, the output is "
                "the pinned prior and a stationary tick keeps it; one 20 cm step north then scores b at u^−(20/800) and c at "
                "L(excess) · u^−f_c from the new origin", ok,
                f"before b {base_before[repr(hb)]:.3e} c {base_before[repr(hc)]:.3e}; after {base_after[repr(hb)]:.4f} / {base_after[repr(hc)]:.4f} / "
                f"{base_after[UNKNOWN]:.4f}; step b:u {odds(bw.distribution, repr(hb)):.4f} (expected {u ** -f_b:.4f}) c:u "
                f"{odds(bw.distribution, repr(hc)):.4f} (expected {LF.logistic_of_excess(ex_c) * u ** -f_c:.4f})"))

    # G9 — the pin without the boundary
    rec = IntentionRecognizer(knowledge=kb, context=ContextKnowledge.default(), hypotheses=[ha, hb])
    rec.update(_obs("h", (0.0, 0.0), "stand", t=0), _world("h", (0.0, 0.0), objects=objs, locations=locs, t=0))
    for i in range(1, 6):
        b5 = rec.update(_obs("h", (20.0 * i, 0.0), t=i), _world("h", (20.0 * i, 0.0), objects=objs, locations=locs, t=i))
    p = (120.0, 0.0)
    b6 = rec.update(_obs("h", p, t=6), _world("h", p, predicates=[P("obj_at", "item_b", "table_0")],
                                             objects={**objs, "item_b": (0.0, -400.0)}, locations={"item_a": "shelf_a", "item_b": "table_0"}, t=6, home=locs))
    ok = (repr(hb) in rec._completed and rec._origin[repr(ha)] == (0.0, 0.0)
          and near(odds(b5.distribution, repr(ha)), u ** -0.25) and near(odds(b6.distribution, repr(ha)), u ** -0.3)
          and b6.distribution[repr(hb)] == 0.001)
    out.append(("G9 a completion the agent's phase did not reach (item_b delivered elsewhere mid-walk) pins b and is no boundary: a's "
                "origin stays, a:u continues its graded walk (u^−0.25 → u^−0.3), nothing re-initialises", ok,
                f"b pinned {b6.distribution[repr(hb)]}, a origin {rec._origin[repr(ha)]}, a:u {odds(b5.distribution, repr(ha)):.3f} → {odds(b6.distribution, repr(ha)):.3f}"))
    return out


if __name__ == "__main__":
    checks = unit_checks()
    for n, ok, d in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {n}  {d}")
    print("OVERALL:", "PASS" if all(ok for _, ok, _ in checks) else "FAIL")
    sys.exit(0 if all(ok for _, ok, _ in checks) else 1)
