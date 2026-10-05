#!/usr/bin/env python3
"""
comp5e.py — T-K part 1, step 5e (analysis/kitting/tk5e/README.md): context knowledge on against off over the step's
runs, read from their outputs only (nothing recomputed by the framework), with step 5d's measures
(analysis/kitting/tk5d/REPORT.md; analysis/kitting/mpb/tk5b/comparison.py, whose readings are reused). Prints the
report's tables as markdown.

    comp5e.py            run from the repository root

The set is read from the registry: every scenario of env_setup_17 to _30, its description naming its script, its form
(the idle robot: recognition; the working robot: planning) and its setting (no timeline, accord, through, through_rw);
an existing script's working form with no timeline is the existing scenario (scenario_s02_01, s02_02, s04_01, s03_06,
s05_01, s05_02), matched by its human script and robot pool.

The pairs (within one script):
- recognition: tk5e/irb/on/<scenario> against tk5e/irb/off/<the script's idle form with no timeline>; `actual.csv`;
- planning: tk5e/mpb/on/<scenario>/on_single_task against tk5e/mpb/off/<the working form with no timeline and the same
  robot pool>/on_single_task.
Rooms in two groups: the four rooms (env_layout_02, _05, _06, _07) and the two new rooms (env_layout_19, _20).

Classes of a wrong admission (the gate clearing with a hypothesis leading that is not the true task):
- pin: a one-tick admission of the next task on the previous task's pin tick (step 5b's reading);
- exit: on the exit walk (the script's last entry a go_to), or on the last task's pinned ticks before it;
- unmodelled: on a tick the human's top task is a stand, a walk elsewhere or a walk-and-stand before the exit walk
  (no hypothesis is true there);
- main: during a modelled task.
CAUSES holds the cause of each planning case below min_separation, read by hand from the case table.
"""
import csv
import importlib
import importlib.util
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / "analysis/instruments/irb"), str(ROOT / "analysis/kitting/irb/tk2"),
                str(ROOT / "analysis/kitting/irb/tk5b"), str(ROOT / "analysis/instruments/mpb"),
                str(ROOT / "analysis/instruments/common"), str(ROOT)]
import admission as A
import g_reading as G
import read5b as R
import summary as S
from sep_classes import rule  # noqa: F401  (PRun uses it)

_spec = importlib.util.spec_from_file_location("cmp5b", ROOT / "analysis/kitting/mpb/tk5b/comparison.py")
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)

THETA = 0.75
NAME = "actual.csv"
G.NAME = NAME
T5E = ROOT / "analysis/kitting/tk5e"
FOUR = ("env_layout_02", "env_layout_05", "env_layout_06", "env_layout_07")
NEW = ("env_layout_19", "env_layout_20")
GROUPS = (("four rooms", FOUR), ("two new rooms", NEW))
SETTINGS = ("none", "accord", "through", "through_rw")
FORM = {"no timeline (the setup states none)": "none",
        "its own timeline, the raising fact over the foreseeable task (accord)": "accord",
        "its own timeline, break_time over a delivery (the human works through it)": "through",
        "its own timeline, room_warm over a delivery (the human works through it)": "through_rw"}
EXISTING = ("scenario_s02_01", "scenario_s02_02", "scenario_s04_01", "scenario_s03_06", "scenario_s05_01",
            "scenario_s05_02")


# ---- the set --------------------------------------------------------------------------------------------------------

def human(sc):
    return next(a for a in sc.agents if a.agent_type == "human")


def robot(sc):
    return next(a for a in sc.agents if a.agent_type == "robot")


def item_of(task):
    return next((c.value for v, c in task.bindings.items() if v.name == "?item"), None)


def load_set():
    dc = importlib.import_module("domains.kitting.registry").domain_config
    S.SCHEMAS.update({s.name: s for s in dc["task_model"]})
    scen = dc["scenarios"]
    scripts = {}
    for sid, sc in scen.items():
        m = re.match(r"scenario_s(\d+)_\d+$", sid)
        if not m or not 17 <= int(m[1]) <= 30:
            continue
        d = re.match(r"\S+: script (\d+) of step 5e(?: \(([^)]*)\))?, the (idle|working) robot, (.*?)(?:: [^.]*)?\. Purpose",
                     sc.description)
        n, origin, form, words = int(d[1]), d[2], d[3], d[4]
        setting = FORM[words]
        e = scripts.setdefault(n, dict(n=n, layout=sc.reference_layouts[0], setup=sc.setup, idle={}, working=defaultdict(list),
                                       origin=origin, aspects=sc.description.split("Aspects: ")[1].split(". Expectation")[0],
                                       script=sc))
        (e["idle"].__setitem__(setting, sid) if form == "idle" else e["working"][setting].append(sid))
    for n, e in scripts.items():
        if e["origin"]:
            ids = re.findall(r"scenario_s\d+_\d+", e["origin"])
            ids += ["scenario_s05_02"] if "scenario_s05_01" in ids else []
            e["working"]["none"] = [x for x in EXISTING if x in ids]
        h = human(e["script"])
        e["assigned"] = [item_of(t) for t in h.assigned_tasks]
        e["never"] = None     # filled from the trajectory (items assigned and never handled)
    return scen, scripts


def pool(sc):
    return tuple(sorted(item_of(t) for t in robot(sc).assigned_tasks))


# ---- recognition ----------------------------------------------------------------------------------------------------

def rec_pairs(scen, scripts):
    out = []
    for n, e in sorted(scripts.items()):
        off = T5E / "irb/off" / e["idle"]["none"]
        for st, sid in e["idle"].items():
            on = T5E / "irb/on" / sid
            if (on / NAME).exists() and (off / NAME).exists():
                out.append(dict(n=n, layout=e["layout"], setting=st, on=on, off=off, e=e))
    return out


def group_of(layout):
    return "four rooms" if layout in FOUR else "two new rooms"


def levels(d):
    out = {}
    for r in csv.DictReader(open(d / NAME)):
        t = int(r["tick"])
        if t >= 0 and t not in out:
            out[t] = dict(x.split("=") for x in r["levels"].split()) if r["levels"] else {}
    return out


def category(key, lv):
    name = key.split("(")[0]
    if name == "deliver_item":
        return "delivery, a raising fact holding" if any(v == "raised" for v in lv.values()) else "delivery, no raising fact"
    own = lv.get(name, "ordinary")
    return f"{name}, {own}"


CAT_ORDER = ["delivery, no raising fact", "delivery, a raising fact holding", "coffee_break, raised",
             "coffee_break, ordinary", "coffee_break, suppressed", "ac_activation, raised", "ac_activation, ordinary",
             "ac_activation, suppressed"]


def stats(xs):
    return "-" if not xs else f"median {statistics.median(xs):g}, range {min(xs)} to {max(xs)}"


def true_rows(pairs):
    """Per true stretch of every on run, the on and off admissions (and the on run with no fact, for the copies)."""
    none_of = {(p["n"]): p for p in pairs if p["setting"] == "none"}
    rows = []
    for p in pairs:
        _, _, on = A.stretches(p["on"], NAME, THETA)
        _, _, off = A.stretches(p["off"], NAME, THETA)
        offd = {(r["key"], r["a"]): r for r in off}
        base = None
        if p["setting"] != "none" and p["n"] in none_of:
            _, _, b = A.stretches(none_of[p["n"]]["on"], NAME, THETA)
            base = {(r["key"], r["a"]): r for r in b}
        lv = levels(p["on"])
        for r in on:
            f = offd[(r["key"], r["a"])]
            rows.append(dict(p=p, r=r, f=f, cat=category(r["key"], lv.get(r["a"], {})),
                             none=None if base is None else base[(r["key"], r["a"])]))
    return rows


def cmp_line(label, xs, a="adm", b="adm", side=("r", "f")):
    both = [x[side[0]][a] - x[side[1]][b] for x in xs if x[side[0]][a] is not None and x[side[1]][b] is not None]
    on_only = sum(x[side[0]][a] is not None and x[side[1]][b] is None for x in xs)
    off_only = sum(x[side[0]][a] is None and x[side[1]][b] is not None for x in xs)
    neither = sum(x[side[0]][a] is None and x[side[1]][b] is None for x in xs)
    e, q, l = sum(v < 0 for v in both), sum(v == 0 for v in both), sum(v > 0 for v in both)
    return (f"| {label} | {len(xs)} | {e} / {q} / {l} | {on_only} / {off_only} / {neither} | {stats(both)} | "
            f"{-sum(v for v in both if v < 0)} / {sum(v for v in both if v > 0)} |")


def r1(rows):
    head = ("| category | stretches | earlier / equal / later | admitted on only / off only / neither | difference "
            "(ticks, both admitted) | ticks earlier / later |\n|---|---|---|---|---|---|")
    for gname, lays in GROUPS:
        print(f"\n**{gname}: on against off, by setting and by the state on the stretch's first tick**\n")
        print(head)
        for st in SETTINGS:
            for cat in CAT_ORDER:
                xs = [x for x in rows if x["p"]["layout"] in lays and x["p"]["setting"] == st and x["cat"] == cat]
                if xs:
                    print(cmp_line(f"{st}: {cat}", xs))
        xs = [x for x in rows if x["p"]["layout"] in lays and x["p"]["setting"] == "none"]
        print(cmp_line("none: all", xs))
    print("\n**The window against no fact (on with the window against on with no timeline, the same stretch)**\n")
    print(head.replace("admitted on only / off only", "admitted with the window only / with no fact only"))
    for gname, lays in GROUPS:
        for st in SETTINGS[1:]:
            for cat in CAT_ORDER:
                xs = [x for x in rows if x["p"]["layout"] in lays and x["p"]["setting"] == st and x["cat"] == cat
                      and x["none"] is not None]
                if xs:
                    print(cmp_line(f"{gname}, {st}: {cat}", xs, side=("r", "none")))
    print("\n**Per room, setting none, all stretches (on against off)**\n")
    print(head)
    for lay in FOUR + NEW:
        xs = [x for x in rows if x["p"]["layout"] == lay and x["p"]["setting"] == "none"]
        if xs:
            print(cmp_line(lay, xs))


def ac_rows(rows):
    print("| room | script | setting | stretch | admitted on / off | belief at arrival on / off |")
    print("|---|---|---|---|---|---|")
    for x in rows:
        if not x["r"]["key"].startswith("ac_activation"):
            continue
        p = x["p"]
        ad = lambda r: "never" if r["adm"] is None else f"{r['adm']} ({r['adm'] - r['a']})"
        print(f"| {p['layout'][-2:]} | {p['n']:03d} | {p['setting']} | {x['r']['a']} to {x['r']['b']} | {ad(x['r'])} / {ad(x['f'])} | "
              f"{x['r']['at_arrival'] or '-'} / {x['f']['at_arrival'] or '-'} |")


def traj_tasks(d):
    t = json.load(open(d / "trajectory.json"))
    return {r["tick"]: r["task"] for r in t["rows"] if r["tick"] >= 0}, t


def handled_items(traj):
    return {a["task"].split("?item=")[1].split(",")[0] for a in traj["actions"] if "?item=" in a["task"]}


def classify(d, w, tasks, exit_from):
    if R.on_pin_tick(w):
        return "pin"
    if exit_from is not None and (w["a"] >= exit_from or all(p == "unmodelled" or "complete: pinned" in p
                                                             for p in w["true"].split(", ")) and w["b"] >= exit_from):
        return "exit"
    top = tasks.get(w["a"]) or ""
    if top.split("(")[0] in ("stand", "go_to", "go_to_and_stand"):
        return "unmodelled"
    return "main"


def wrong_rows(d, e):
    tasks, traj = traj_tasks(d)
    acts = traj["actions"]
    exit_from = None
    if acts and acts[-1]["task"].startswith("go_to("):
        i = len(acts) - 1
        while i > 0 and acts[i - 1]["task"] == acts[-1]["task"]:
            i -= 1
        exit_from = acts[i]["tick"]
    never = set(e["assigned"]) - handled_items(traj)
    run = G.Run(d)
    _, rows = A.wrong_admissions(d, NAME)
    out = []
    for w in rows:
        k = classify(d, w, tasks, exit_from)
        kept, _ = R.held(run, w)
        m = re.search(r"; \d+ to (?:\d+|the run's end) \((\d+)\)", kept)
        it = w["h"].split("?item=")[1].rstrip(")") if "?item=" in w["h"] else None
        top = (tasks.get(w["a"]) or "").split("(")[0]
        out.append(dict(kind=k, h=w["h"], a=w["a"], b=w["b"], gate=w["b"] - w["a"] + 1,
                        rule=int(m[1]) if m else w["b"] - w["a"] + 1, never=it in never, top=top, true=w["true"]))
    return out


def r2(pairs):
    acc = defaultdict(list)
    seen = set()
    for p in pairs:
        g = group_of(p["layout"])
        for r in wrong_rows(p["on"], p["e"]):
            acc[(g, p["setting"], r["kind"])].append((p, r))
        if p["off"] not in seen:
            seen.add(p["off"])
            for r in wrong_rows(p["off"], p["e"]):
                acc[(g, "off", r["kind"])].append((p, r))
    print("| group | side | kind | count | gate ticks | trigger-rule ticks | of them a never-started delivery (count) |")
    print("|---|---|---|---|---|---|---|")
    for g, _ in GROUPS:
        for side in ("off",) + SETTINGS:
            for kind in ("main", "unmodelled", "exit", "pin"):
                xs = acc.get((g, side, kind), [])
                if xs:
                    print(f"| {g} | {side} | {kind} | {len(xs)} | {sum(r['gate'] for _, r in xs)} | "
                          f"{sum(r['rule'] for _, r in xs)} | {sum(r['never'] for _, r in xs)} |")
    return acc


def r2_list(acc, kinds=("main", "unmodelled")):
    print("| group | side | room | script | setting | admitted | ticks (gate) | trigger rule | true task / human's top task | never-started |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for (g, side, kind), xs in sorted(acc.items()):
        if kind not in kinds:
            continue
        for p, r in xs:
            print(f"| {g} | {side} | {p['layout'][-2:]} | {p['n']:03d} | {kind} | {G.short(r['h'])} | {r['a']}-{r['b']} ({r['gate']}) | "
                  f"{r['rule']} | {r['true']} / {r['top']} | {'yes' if r['never'] else ''} |")


def r2_kinds(pairs):
    """The kinds of the main wrong admissions with context knowledge on, from the evidence alone (the off run's belief),
    as step 5d's: (i) near-tie, (ii) the true task first and the prior overruling it, (iii) the evidence ranking the
    admitted one first; none where the true task is no hypothesis."""
    tally = defaultdict(lambda: [0, 0])
    for p in pairs:
        if p["setting"] == "none" and False:
            continue
        on, off = G.Run(p["on"]), G.Run(p["off"])
        for r in wrong_rows(p["on"], p["e"]):
            if r["kind"] != "main":
                continue
            cls = {"(i)": 0, "(ii)": 0, "(iii)": 0, "(iv)": 0}
            for t in range(r["a"], r["b"] + 1):
                k = on.truth.get(t)
                if k is None or t not in off.hyp or k not in off.hyp[t] or r["h"] not in off.hyp[t]:
                    continue
                bk, bh = off.hyp[t][k]["b"], off.hyp[t][r["h"]]["b"]
                ratio = bk / bh if bh > 0 else float("inf")
                first = all(bk > v["b"] for kk, v in off.hyp[t].items() if kk != k)
                c = "(i)" if 1 / C.NEAR <= ratio <= C.NEAR else ("(ii)" if first else "(iv)") if ratio > C.NEAR else "(iii)"
                cls[c] += 1
            kind = "none" if not sum(cls.values()) else max(("(i)", "(ii)", "(iii)"), key=lambda c: (cls[c], -["(i)", "(ii)", "(iii)"].index(c)))
            key = (group_of(p["layout"]), p["setting"], kind)
            tally[key][0] += 1
            tally[key][1] += r["gate"]
    print("| group | setting | (i) near-tie | (ii) the prior overruling | (iii) the evidence ranking it first | no true hypothesis |")
    print("|---|---|---|---|---|---|")
    for g, _ in GROUPS:
        for st in SETTINGS:
            cells = [tally.get((g, st, k), [0, 0]) for k in ("(i)", "(ii)", "(iii)", "none")]
            if any(c[0] for c in cells):
                print(f"| {g} | {st} | " + " | ".join(f"{c[0]} ({c[1]} ticks)" for c in cells) + " |")


def r3_gate(pairs):
    """The gate's refusals on the true stretches with the true task leading at or above θ (what the rulings refuse of
    the true task), and on every tick with another hypothesis leading at or above θ (what they refuse of a wrong one),
    on and off (off once per script)."""
    acc = defaultdict(int)
    seen = set()

    def tally(d, g, side):
        run = G.Run(d)
        for t, tk in run.tick.items():
            if tk["gate"] in ("clears", "none(below_theta)") or tk["leader"] not in run.hyp.get(t, {}):
                continue
            if run.hyp[t][tk["leader"]]["b"] < THETA:
                continue
            whose = "true task" if run.truth.get(t) == tk["leader"] else (
                "unmodelled tick" if run.truth.get(t) is None else "another task")
            acc[(g, side, whose, tk["gate"])] += 1
    for p in pairs:
        g = group_of(p["layout"])
        tally(p["on"], g, p["setting"])
        if p["off"] not in seen:
            seen.add(p["off"])
            tally(p["off"], g, "off")
    gates = sorted({k[3] for k in acc})
    print("| group | side | leader (≥ θ) | " + " | ".join(gates) + " |")
    print("|---|---|---|" + "---|" * len(gates))
    for g, _ in GROUPS:
        for side in ("off",) + SETTINGS:
            for whose in ("true task", "another task", "unmodelled tick"):
                cells = [acc.get((g, side, whose, x), 0) for x in gates]
                if any(cells):
                    print(f"| {g} | {side} | {whose} | " + " | ".join(str(c) for c in cells) + " |")
    return acc


def r3_true_refused(pairs):
    """Each run of ticks on a true stretch where the true task leads at or above θ and the gate refuses it outranked
    (AM68) or unwarranted (AM67), on, with the setting; the off run's gate on the same ticks."""
    print("| group | room | script | setting | true task | ticks | refusal | off: the gate on those ticks |")
    print("|---|---|---|---|---|---|---|---|")
    for p in pairs:
        run, off = G.Run(p["on"]), G.Run(p["off"])
        cur = None
        items = []
        for t in sorted(run.tick):
            tk = run.tick[t]
            ok = (run.truth.get(t) == tk["leader"] and tk["gate"] in ("none(leader_outranked)", "none(leader_unwarranted)")
                  and run.hyp.get(t, {}).get(tk["leader"], {}).get("b", 0) >= THETA)
            if ok and cur and cur[1] == t - 1 and cur[2] == tk["gate"] and cur[3] == tk["leader"]:
                cur[1] = t
            elif ok:
                cur = [t, t, tk["gate"], tk["leader"]]
                items.append(cur)
        for a, b, gt, k in items:
            og = sorted({off.tick[t]["gate"] for t in range(a, b + 1) if t in off.tick})
            print(f"| {group_of(p['layout'])} | {p['layout'][-2:]} | {p['n']:03d} | {p['setting']} | {G.short(k)} | {a}-{b} | "
                  f"{gt} | {', '.join(og)} |")


# ---- planning -------------------------------------------------------------------------------------------------------

def plan_pairs(scen, scripts):
    out = []
    for n, e in sorted(scripts.items()):
        bases = {pool(scen[b]): b for b in e["working"]["none"]}
        for st, sids in e["working"].items():
            for sid in sids:
                b = bases[pool(scen[sid])]
                on, off = T5E / "mpb/on" / sid, T5E / "mpb/off" / b
                if (on / "on_single_task/properties.json").exists() and (off / "on_single_task/properties.json").exists():
                    out.append(dict(n=n, layout=e["layout"], setting=st, on=on, off=off, e=e))
    return out


def wrong_records(p):
    """Decision records holding a hypothesis that is not the true task, before the robot's completion: count, ticks."""
    comp = p.props["completion"]
    end = comp if comp is not None else max(p.truth) + 1
    n, ticks = 0, 0
    dec = [d for d in p.dec if d.tick < end]
    for i, d in enumerate(dec):
        if d.admitted is None:
            continue
        stop = dec[i + 1].tick if i + 1 < len(dec) else end
        w = [t for t in range(d.tick, stop) if (S.short(p.truth[t]) if p.truth.get(t) else None) != S.short(d.admitted.key)]
        if w:
            n += 1
            ticks += len(w)
    return n, ticks


# The causes of the cases that differ between the sides, read by hand from the logs (decisions, holds, [sep]); keyed by
# (script number, first tick): every on run of the script with that case shares it. A case with the same ticks and
# minimum on both sides is not a context effect and takes its class from the decision in force (rule below).
CAUSES = {
    (35, 27): ("wrong admission (limitation, docs/assumptions.md 6.4)", "deliver_item(item_5) admitted at 0 while the human walks to the coffee machine, which stands 100 cm short of shelf_5 on the same bearing (a near-tie for 24 ticks; the prior picks the assigned delivery); the robot, its plan resting on the delivery, walks down x = 0 and passes the human standing at the machine (off: fallbacks, a hold at 24, 58 cm)"),
    (38, 52): ("limitation (an admitted task cut by a foreseeable task inside it)", "deliver_item(item_5) admitted at 36, rightly (the human walks to shelf_5; off still below θ); at the shelf the human steps to the coffee machine beside it, onto the robot's route, and the robot's plan still rests on the delivery (the record kept until the trigger rule fires: question G's reading)"),
    (15, 51): ("fallback under the window", "under break_time the delivery of item_3 is admitted at 59 (no fact: 37; off: 55); at 51 the robot rests on a moving fallback (k = 19) and passes the human"),
    (24, 57): ("off only (a gain on)", "scenario_s03_06's recorded meeting with the departing human on a moving fallback; on, the earlier admission of the deliveries shifts the robot's timeline and the case does not form"),
    (25, 57): ("off only (a gain on)", "as script 024: the robot meets the departing human on a moving fallback; on, the case does not form"),
    (25, 133): ("the same case on both sides, a tick apart", "the exit walk passes the robot resting on a moving fallback"),
    (25, 134): ("the same case on both sides, a tick apart", "the exit walk passes the robot resting on a moving fallback"),
    (34, 54): ("the same case on both sides, a tick apart", "the human passes the robot standing at kitting_table_0 (one receding tick)"),
    (34, 55): ("the same case on both sides, a tick apart", "the human passes the robot standing at kitting_table_0 (one receding tick)"),
    (41, 151): ("the same case on both sides, six ticks apart", "the human at shelf_3, the robot standing there for its item_55 (one receding tick)"),
    (41, 157): ("the same case on both sides, six ticks apart", "the human at shelf_3, the robot standing there for its item_55 (one receding tick)"),
    (42, 147): ("the same case on both sides, a tick apart", "the human arrives at the coffee machine beside the robot standing on its route (one receding tick)"),
    (42, 148): ("the same case on both sides, a tick apart", "the human arrives at the coffee machine beside the robot standing on its route (one receding tick)"),
    (43, 268): ("off only (a gain on)", "the robot moving past the human at kitting_table_0 on the admitted item_53; on, the robot's earlier decisions differ and the case does not form"),
    (65, 180): ("other, deeper on", "the human arrives at kitting_table_1 beside the robot holding there (both sides); on, a recognition_changed at 183 ends the hold a tick early and the robot moves off past the human (23.1 cm; off 32.0 cm, the hold completed)"),
}


def p1(pairs):
    runs = {}

    def prun(x):
        if x not in runs:
            runs[x] = C.PRun(x)
        return runs[x]
    print("| room | script | setting | scenario | completion off → on (Δ) | response decision off → on | wrong records off → on (count; ticks) | min separation off → on | cases below on (first-last: min) |")
    print("|---|---|---|---|---|---|---|---|---|")
    tallies = defaultdict(lambda: dict(better=0, equal=0, worse=0, gain=0, loss=0, resp_e=0, resp_l=0, resp_q=0))
    cases = []
    done_off = set()
    for p in pairs:
        on, off = prun(p["on"]), prun(p["off"])
        c1, c0 = on.props["completion"], off.props["completion"]
        (r1t, r1w), (r0t, r0w) = on.response(), off.response()
        w1, w0 = wrong_records(on), wrong_records(off)
        m1, m0 = on.props["measures"]["sep_min_continuous"], off.props["measures"]["sep_min_continuous"]
        cs = "; ".join(f"{k[0]}-{k[-1]}: {min(on.below[t][0] for t in k):.1f}" for k in on.cases()) or "none"
        d = None if c1 is None or c0 is None else c1 - c0
        print(f"| {p['layout'][-2:]} | {p['n']:03d} | {p['setting']} | {p['on'].name.removeprefix('scenario_')} | {c0} → {c1} "
              f"({'-' if d is None else f'{d:+d}'}) | {r0t}: {r0w} → {r1t}: {r1w} | {w0[0]}; {w0[1]} → {w1[0]}; {w1[1]} | "
              f"{m0[0]:.1f} → {m1[0]:.1f} | {cs} |")
        key = (group_of(p["layout"]), p["setting"])
        t = tallies[key]
        if d is not None:
            t["better" if d < 0 else "worse" if d > 0 else "equal"] += 1
            t["gain" if d < 0 else "loss"] += abs(d)
        if r1t is not None and r0t is not None:
            t["resp_e" if r1t < r0t else "resp_l" if r1t > r0t else "resp_q"] += 1
        t.setdefault("wrong_on", [0, 0]); t.setdefault("wrong_off", [0, 0])
        t["wrong_on"][0] += w1[0]; t["wrong_on"][1] += w1[1]; t["wrong_off"][0] += w0[0]; t["wrong_off"][1] += w0[1]
        for side, pr, x in (("on", on, p["on"]),) + ((("off", off, p["off"]),) if p["off"] not in done_off else ()):
            for k in pr.cases():
                dd = pr.in_force(k[0])
                truth = pr.truth.get(k[0])
                cls = {c_: sum(1 for tt in k if pr.below[tt][1] == c_) for c_ in ("stand", "viol", "recede")}
                cases.append(dict(p=p, side=side, scen=x.name, a=k[0], b=k[-1], mn=min(pr.below[tt][0] for tt in k), cls=cls,
                                  proj=C.proj(dd), truth=G.short(truth) if truth else "unmodelled",
                                  wrong=dd is not None and dd.admitted is not None and G.short(dd.admitted.key) != (G.short(truth) if truth else None)))
        done_off.add(p["off"])
    print("\n**Tallies (on against off)**\n")
    print("| group | setting | runs | completion better / equal / worse (ticks gained / lost) | response earlier / equal / later | wrong records off → on (count; ticks) |")
    print("|---|---|---|---|---|---|")
    for (g, st), t in sorted(tallies.items(), key=lambda kv: (kv[0][0], SETTINGS.index(kv[0][1]))):
        n = t["better"] + t["equal"] + t["worse"]
        print(f"| {g} | {st} | {n} | {t['better']} / {t['equal']} / {t['worse']} ({t['gain']} / {t['loss']}) | "
              f"{t['resp_e']} / {t['resp_q']} / {t['resp_l']} | {t['wrong_off'][0]}; {t['wrong_off'][1]} → {t['wrong_on'][0]}; {t['wrong_on'][1]} |")
    print("\n**Every case below min_separation, with its cause**\n")
    print("| room | script | setting | side | scenario | ticks | min | standing / viol / recede | decision in force | human's true task | wrong admission in force | cause |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for c in cases:
        cause = CAUSES.get((c["p"]["n"], c["a"]))
        other = [x for x in cases if x is not c and x["p"]["n"] == c["p"]["n"] and x["side"] != c["side"]
                 and (x["a"], x["b"], round(x["mn"], 1)) == (c["a"], c["b"], round(c["mn"], 1))]
        if cause is None and other and (c["cls"]["viol"] or c["cls"]["recede"]):
            d = c["proj"].split(": ", 1)[-1]
            cause = ("the same on both sides", "not a context effect; decision in force: " +
                     ("a wrong admission" if c["wrong"] else "the true task admitted" if d.startswith("admitted") else
                      "a fallback"))
        if cause is None:
            cause = ("standing", "the robot standing (not robot-responsible under F1)") if not c["cls"]["viol"] and not c["cls"]["recede"] \
                else ("unclassified", "NOT CLASSIFIED")
        k = c["cls"]
        print(f"| {c['p']['layout'][-2:]} | {c['p']['n']:03d} | {c['p']['setting']} | {c['side']} | {c['scen'].removeprefix('scenario_')} | "
              f"{c['a']}-{c['b']} | {c['mn']:.1f} | {k['stand']} / {k['viol']} / {k['recede']} | {c['proj']} | {c['truth']} | "
              f"{'yes' if c['wrong'] else ''} | {cause[0]}: {cause[1]} |")
    return cases


def checks():
    """The runs' own checks: the comparison's result per run (diff.md for the IRB, the chain's compare for the MPB)."""
    out = defaultdict(list)
    for side in ("on", "off"):
        for d in sorted(x for x in (T5E / "irb" / side).glob("scenario_*") if x.is_dir()):
            f = d / "diff.md"
            if not f.exists():
                out[f"irb {side}: no output"].append(d.name)
                continue
            txt = (d.parent / f"{d.name}.run.txt").read_text() if (d.parent / f"{d.name}.run.txt").exists() else ""
            m = re.search(r"(\d+) disagreements against actual.csv, (\d+) against actual_log.csv, (\d+) unmatched rows; "
                          r"undetermined \(skipped\) rank (\d+), gate (\d+)", txt)
            dis = [int(x) for x in re.findall(r"^Disagreements: (\d+)", f.read_text(), re.M)]   # diff.md: the last comparison
            out[f"irb {side}: " + ("0 disagreements" if dis and not any(dis) else "DISAGREEMENT or unread")].append(d.name)
            if m and (m[4] != "0" or m[5] != "0"):
                out[f"irb {side}: undetermined rank {m[4]}, gate {m[5]}"].append(d.name)
        for d in sorted(x for x in (T5E / "mpb" / side).glob("scenario_*") if x.is_dir()):
            txt = (d.parent / f"{d.name}.run.txt").read_text() if (d.parent / f"{d.name}.run.txt").exists() else ""
            m = re.search(r"\(single_task\): (\d+) per-tick, (\d+) decision, (\d+) log disagreements", txt)
            if "no chain" in txt:
                out[f"mpb {side}: no chain (an undetermined gate at a decision)"].append(d.name)
            elif m:
                out[f"mpb {side}: " + ("0 disagreements" if m.group(1, 2, 3) == ("0", "0", "0") else "DISAGREEMENT")].append(d.name)
            else:
                out[f"mpb {side}: no comparison read"].append(d.name)
    for k, v in sorted(out.items()):
        print(f"- {k}: {len(v)}" + ("" if "0 disagreements" in k else f" ({', '.join(x.removeprefix('scenario_') for x in v)})"))


def main():
    scen, scripts = load_set()
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("all", "checks"):
        print("## 0. The runs' checks\n")
        checks()
    pairs = rec_pairs(scen, scripts)
    if what in ("all", "rec"):
        print(f"\n## A. Recognition ({len(pairs)} on runs against their off run)\n")
        print("### A1. Admissions of the true task")
        rows = true_rows(pairs)
        r1(rows)
        print("\n### A2. The A/C activation, every stretch\n")
        ac_rows(rows)
        print("\n### A3. Admissions of a hypothesis that is not the true task\n")
        acc = r2(pairs)
        print("\n### A3, the kinds from the evidence alone (main, on)\n")
        r2_kinds(pairs)
        print("\n### A3, every main and unmodelled row\n")
        r2_list(acc)
        print("\n### A4. The gate's outcome with a leader at or above θ (ticks)\n")
        r3_gate(pairs)
        print("\n### A4, the true task refused by AM67 or AM68 (on)\n")
        r3_true_refused(pairs)
    if what in ("all", "plan"):
        pp = plan_pairs(scen, scripts)
        print(f"\n## B. Planning ({len(pp)} on runs against their off run)\n")
        p1(pp)


if __name__ == "__main__":
    main()
