#!/usr/bin/env python3
"""
comparison.py — context knowledge on against off over T-K part 1's kitting runs (steps 4, 5 and 5b): one overview,
read from existing outputs only (no run, nothing recomputed by the framework). Writes COMPARISON.md's tables to stdout.

    comparison.py            run from the repository root

The pairs (within one script: the on run and the off run of the same script):
- recognition: step 4 (analysis/kitting/irb/tk2/<scenario>, its off side in tk2/off or tk1, offon.py's pairing) and step
  5b (analysis/kitting/irb/tk5b/<scenario>, its off side analysis/kitting/irb/<scenario>); `actual.csv` on both sides;
- planning: step 5 (analysis/kitting/mpb/tk/<scenario>, its off side tk/off/ of the same script) and step 5b
  (analysis/kitting/mpb/tk5b/<scenario>, its off side analysis/kitting/mpb/<scenario>); single_task.

The readings reused: admission.py (true stretches, wrong admissions), g_reading.py (the trigger rule's record),
analysis/kitting/irb/tk5b/read5b.py (the pin-tick rows, the trigger rule's wrong ticks), sep_classes.py (F1's classes),
mpblib (the decisions). CAUSES holds the cause of each case below min_separation, read by hand from the case table
(the decision in force, its projection and the human's true task) and stated there.
"""
import csv
import importlib
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(ROOT / "analysis/instruments/irb"), str(ROOT / "analysis/kitting/irb/tk2"),
                str(ROOT / "analysis/kitting/irb/tk5b"), str(ROOT / "analysis/instruments/mpb"),
                str(ROOT / "analysis/instruments/common"), str(ROOT)]
import admission as A
import g_reading as G
import offon as O
import read5b as R
import summary as S
import logparse
from sep_classes import rule
from mpblib import load_decisions

THETA = 0.75
NAME = "actual.csv"
IRB = ROOT / "analysis/kitting/irb"
MPB = ROOT / "analysis/kitting/mpb"
G.NAME = NAME


# ---- recognition ----------------------------------------------------------------------------------------------------

def rec_pairs():
    out = []
    for d in sorted(p for p in (IRB / "tk2").iterdir() if p.is_dir() and (p / NAME).exists()):
        out.append(("step 4", d, O.off_dir_of(d, [IRB / "tk2/off", IRB / "tk1"], NAME)))
    for d in sorted(p for p in (IRB / "tk5b").iterdir() if p.is_dir() and (p / NAME).exists()):
        out.append(("step 5b", d, IRB / d.name))
    return out


def levels(d):
    """Per tick the levels column, parsed: {task: level}."""
    out = {}
    for r in csv.DictReader(open(d / NAME)):
        t = int(r["tick"])
        if t >= 0 and t not in out:
            out[t] = dict(x.split("=") for x in r["levels"].split()) if r["levels"] else {}
    return out


def raised(lv):
    return any(v == "raised" for v in lv.values())


def exit_start(d):
    """The first tick of the script's last entry, the exit walk (the authoring convention, docs/assumptions.md 1.1)."""
    acts = json.load(open(d / "trajectory.json"))["actions"]
    last = acts[-1]["task"]
    i = len(acts) - 1
    while i > 0 and acts[i - 1]["task"] == last:
        i -= 1
    return acts[i]["tick"]


def stats(xs):
    if not xs:
        return "-"
    return f"median {statistics.median(xs):g}, range {min(xs)} to {max(xs)}"


def a1(pairs):
    """Admissions of the true task: on against off, per stretch, by category."""
    cats = {}
    for step, d, o in pairs:
        _, _, on = A.stretches(d, NAME, THETA)
        _, _, off = A.stretches(o, NAME, THETA)
        off = {(r["key"], r["a"]): r for r in off}
        lv = levels(d)
        for r in on:
            f = off[(r["key"], r["a"])]
            name = r["key"].split("(")[0]
            l0 = lv.get(r["a"], {})
            if name == "deliver_item":
                cat = "assigned delivery, a raising fact holding" if raised(l0) else "assigned delivery, no raising fact"
            else:
                own = l0.get(name, "ordinary")
                cat = f"{name}, its raising fact holding" if own == "raised" else f"{name}, no raising fact ({own})"
            cats.setdefault(cat, []).append((step, d.name, r, f))
    print("| category (the state on the stretch's first tick, on) | stretches | earlier | equal | later | difference on − off "
          "(ticks, both admitted) | ticks earlier, total | ticks later, total | admitted on only | off only | neither |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    order = ["assigned delivery, no raising fact", "assigned delivery, a raising fact holding",
             "coffee_break, its raising fact holding", "coffee_break, no raising fact (ordinary)",
             "coffee_break, no raising fact (suppressed)", "ac_activation, its raising fact holding",
             "ac_activation, no raising fact (ordinary)", "ac_activation, no raising fact (suppressed)"]
    rows = {}
    for cat in order + sorted(set(cats) - set(order)):
        xs = cats.get(cat)
        if not xs:
            continue
        both = [r["adm"] - f["adm"] for _, _, r, f in xs if r["adm"] is not None and f["adm"] is not None]
        on_only = sum(r["adm"] is not None and f["adm"] is None for _, _, r, f in xs)
        off_only = sum(r["adm"] is None and f["adm"] is not None for _, _, r, f in xs)
        neither = sum(r["adm"] is None and f["adm"] is None for _, _, r, f in xs)
        e, q, l = sum(x < 0 for x in both), sum(x == 0 for x in both), sum(x > 0 for x in both)
        rows[cat] = (len(xs), e, q, l, both, on_only, off_only)
        print(f"| {cat} | {len(xs)} | {e} | {q} | {l} | {stats(both)} | {-sum(x for x in both if x < 0)} | "
              f"{sum(x for x in both if x > 0)} | {on_only} | {off_only} | {neither} |")
    return rows


def classify(x, w):
    """A wrong admission's kind: 'pin' (the next task on the previous task's pin tick, the human starting it next),
    'exit' (from its first wrong tick on the exit walk, or on the last task's pinned ticks before it), 'main'."""
    if R.on_pin_tick(w):
        return "pin"
    es = exit_start(x)
    parts = [p for p in w["true"].split(", ")]
    if w["a"] >= es or all(p == "unmodelled" or "complete: pinned" in p for p in parts) and w["b"] >= es:
        return "exit"
    return "main"


def wrong_rows(x, lv=None):
    run = G.Run(x)
    _, rows = A.wrong_admissions(x, NAME)
    out = []
    for w in rows:
        k = classify(x, w)
        n = w["b"] - w["a"] + 1
        kept, _ = R.held(run, w)
        m = re.search(r"; \d+ to (?:\d+|the run's end) \((\d+)\)", kept)
        rule_n = int(m[1]) if m else n
        out.append(dict(kind=k, h=w["h"], a=w["a"], b=w["b"], gate=n, rule=rule_n,
                        raised=raised(lv.get(w["a"], {})) if lv is not None else None))
    return out


def a2(pairs):
    """Admissions of a hypothesis that is not the true task, off against on, per pair; the off run counted once per
    pair (one off run is the off side of several timelines in step 4) and once per script."""
    acc = {}
    seen_off = set()

    def add(key, r):
        acc.setdefault(key, []).append(r)
    for step, d, o in pairs:
        lv = levels(d)
        for r in wrong_rows(d, lv):
            add(("on", r["kind"]), r)
            if r["kind"] == "main":
                add(("on, a raising fact holding" if r["raised"] else "on, no raising fact", "main"), r)
        offr = wrong_rows(o)
        for r in offr:
            add(("off (per pair)", r["kind"]), r)
            if o not in seen_off:
                add(("off (each script once)", r["kind"]), r)
        seen_off.add(o)

    def line(side, kind):
        xs = acc.get((side, kind), [])
        if not xs:
            return f"| {side} | 0 | - | - | - | - | - | - |"
        g, rr = [x["gate"] for x in xs], [x["rule"] for x in xs]
        return (f"| {side} | {len(xs)} | {statistics.median(g):g} | {max(g)} | {sum(g)} | {statistics.median(rr):g} | "
                f"{max(rr)} | {sum(rr)} |")
    head = ("| side | count | gate: median | max | total ticks | trigger rule: median | max | total ticks |\n"
            "|---|---|---|---|---|---|---|---|")
    print("During modelled tasks (the exit walk and the one-tick rows on a completion left out):\n")
    print(head)
    for side in ("off (per pair)", "off (each script once)", "on", "on, no raising fact", "on, a raising fact holding"):
        print(line(side, "main"))
    print("\nThe exit walk:\n")
    print(head)
    for side in ("off (per pair)", "off (each script once)", "on"):
        print(line(side, "exit"))
    print("\nThe one-tick rows on a completion (the next delivery admitted on the previous task's pin tick; not wrong from "
          "the next tick):\n")
    print(head)
    for side in ("off (per pair)", "off (each script once)", "on"):
        print(line(side, "pin"))
    return acc


NEAR = 1.01      # the reporting threshold of a near-tie (a ratio of the evidence within 1 percent); not a design value


def a2_kinds(pairs):
    """Each admission of a hypothesis that is not the true task with context knowledge on (the exit walk and the
    pin-tick rows left out), classified from the evidence alone: the off run of the same script, whose belief is the
    evidence under the equal prior (the G reading's method). On each of the gate's wrong ticks, the ratio of the true
    task's belief to the admitted hypothesis's in the off run:
    (i) a tie or a near-tie, the movement not separating them: the ratio within [1/NEAR, NEAR];
    (ii) the evidence ranks the true task first and the prior overrules it: the ratio above NEAR, the true task first;
    (iii) the evidence itself ranks the admitted hypothesis above the true task: the ratio below 1/NEAR (the case the
         two kinds asked for do not cover; the off run is then mostly wrong there too);
    a tick with the ratio above NEAR and a third hypothesis first is counted apart, as (iv). A row takes the kind of most
    of its ticks (on a tie of counts the order (i), (ii), (iii)). No kind where the true task is no hypothesis
    (unmodelled, or outside the support)."""
    print("| step | scenario | admitted (on) | wrong ticks (gate) | true task | off ratio true / admitted: first wrong tick, last "
          "| ticks (i) / (ii) / (iii) | kind |")
    print("|---|---|---|---|---|---|---|---|")
    rows = {"(i)": [], "(ii)": [], "(iii)": [], "none": []}
    ticks = {"(i)": 0, "(ii)": 0, "(iii)": 0, "(iv)": 0}
    for step, d, o in pairs:
        lv = levels(d)
        on, off = G.Run(d), G.Run(o)
        for r in wrong_rows(d, lv):
            if r["kind"] != "main":
                continue
            h, rat, cls, trues = r["h"], [], {"(i)": 0, "(ii)": 0, "(iii)": 0, "(iv)": 0}, set()
            for t in range(r["a"], r["b"] + 1):
                k = on.truth.get(t)
                if k is None or t not in off.hyp or k not in off.hyp[t] or h not in off.hyp[t]:
                    continue
                trues.add(k)
                bk, bh = off.hyp[t][k]["b"], off.hyp[t][h]["b"]
                ratio = bk / bh if bh > 0 else float("inf")
                first = all(bk > v["b"] for kk, v in off.hyp[t].items() if kk != k)
                c = "(i)" if 1 / NEAR <= ratio <= NEAR else ("(ii)" if first else "(iv)") if ratio > NEAR else "(iii)"
                cls[c] += 1
                rat.append(ratio)
            if not rat:
                rows["none"].append(r)
                true = ", ".join(sorted({G.short(on.truth[t]) if on.truth.get(t) else "unmodelled"
                                         for t in range(r["a"], r["b"] + 1)}))
                print(f"| {step} | {d.name.removeprefix('scenario_')} | {G.short(h)} | {r['a']}-{r['b']} ({r['gate']}) | "
                      f"{true} | - | - | none (the true task is no hypothesis) |")
                continue
            for c, n in cls.items():
                ticks[c] += n
            kind = max(("(i)", "(ii)", "(iii)"), key=lambda c: (cls[c], -["(i)", "(ii)", "(iii)"].index(c)))
            rows[kind].append(r)
            iv = f" / (iv) {cls['(iv)']}" if cls["(iv)"] else ""
            print(f"| {step} | {d.name.removeprefix('scenario_')} | {G.short(h)} | {r['a']}-{r['b']} ({r['gate']}) | "
                  f"{', '.join(sorted(G.short(k) for k in trues))} | ×{rat[0]:.4f}, ×{rat[-1]:.4f} | "
                  f"{cls['(i)']} / {cls['(ii)']} / {cls['(iii)']}{iv} | {kind} |")
    print(f"\nRows: (i) {len(rows['(i)'])}, (ii) {len(rows['(ii)'])}, (iii) {len(rows['(iii)'])}, no kind {len(rows['none'])}. "
          f"Ticks: (i) {ticks['(i)']}, (ii) {ticks['(ii)']}, (iii) {ticks['(iii)']}, (iv) {ticks['(iv)']}. "
          f"Gate ticks per kind of row: " + ", ".join(f"{k} {sum(x['gate'] for x in v)}" for k, v in rows.items()) + ".")
    return rows, ticks


def lone_early(x):
    """A lone assigned task (one delivery live) admitted while the human is not doing it: per run of the gate clearing
    for it, the ticks until the human starts it or the gate stops clearing for it (the retraction), and the ticks until
    the trigger rule fires against a record set there."""
    run = G.Run(x)
    out, t = [], 0
    while t <= run.last:
        tk = run.tick.get(t)
        if tk is None or tk["gate"] != "clears" or not (tk["leader"] or "").startswith("deliver_item"):
            t += 1
            continue
        h = tk["leader"]
        if run.truth.get(t) == h or (t - 1 in run.tick and run.clears_for(t - 1, h)):
            t += 1
            continue
        if sum(1 for k in run.hyp.get(t, {}) if k.startswith("deliver_item")) != 1:
            t += 1
            continue
        a, u = t, t
        while u <= run.last and run.truth.get(u) != h and run.clears_for(u, h):
            u += 1
        how = "started" if run.truth.get(u) == h else ("retracted" if u <= run.last else "run's end")
        out.append(dict(a=a, n=u - a, how=how))
        t = u + 1
    return out


def a3(pairs):
    acc, seen = {}, set()
    for step, d, o in pairs:
        for side, x in (("on", d), ("off", o)):
            if side == "off":
                if o in seen:
                    continue
                seen.add(o)
            for r in lone_early(x):
                acc.setdefault((side, r["how"], r["n"] == 1), []).append((step, x.name, r))
    print("| side | ends | count | ticks until it ends: median | range | total | where (scenario: first tick, ticks) |")
    print("|---|---|---|---|---|---|---|")
    for side in ("off", "on"):
        for how in ("started", "retracted", "run's end"):
            for one in (True, False):
                xs = acc.get((side, how, one), [])
                if not xs:
                    continue
                n = [r["n"] for _, _, r in xs]
                label = f"{how}{' on the next tick (1 tick)' if one and how == 'started' else ''}"
                where = "; ".join(f"{s.removeprefix('scenario_')}: {r['a']}, {r['n']}" for _, s, r in xs) \
                    if not (one and how == "started") else f"{len(xs)} runs"
                print(f"| {side}{' (each script once)' if side == 'off' else ' (per run)'} | {label} | {len(xs)} | {statistics.median(n):g} | {min(n)} to "
                      f"{max(n)} | {sum(n)} | {where} |")
    return acc


# ---- planning -------------------------------------------------------------------------------------------------------

def plan_pairs():
    import importlib.util
    spec = importlib.util.spec_from_file_location("mpb5b", ROOT / "analysis/kitting/mpb/tk5b/read5b.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    out = [("step 5", MPB / "tk" / s, MPB / "tk/off" / o)
           for s, o in (("scenario_s16_01", "scenario_s16_01"), ("scenario_s16_02", "scenario_s16_01"),
                        ("scenario_s16_03", "scenario_s16_03"), ("scenario_s16_04", "scenario_s16_03"),
                        ("scenario_s16_05", "scenario_s16_05"), ("scenario_s16_06", "scenario_s16_05"))]
    out += [("step 5b", MPB / "tk5b" / s, MPB / s) for s in m.SCENARIOS]
    return out


class PRun:
    def __init__(self, base):
        self.base = base
        d = base / "on_single_task"
        self.d = d
        self.props = json.load(open(d / "properties.json"))
        self.dec = load_decisions(d / "actual_decisions.json")
        self.sel = {s["tick"]: s for s in json.load(open(d / "selection.json"))}
        traj = json.load(open(d / "trajectory.json"))
        self.truth = {r["tick"]: (S.hypothesis_key(r["task"]) if r["task"] else None) for r in traj["rows"]}
        log = next((base.parent / "runs").glob(f"*_{base.name}_on_single_task.log"))
        self.run = logparse.parse(str(log))
        self.sep = float(self.run["hdr"].get("min_separation", 50.0))
        self.below = {}
        for k, (_, mn) in sorted(self.run["sep"].items()):
            if mn is not None and mn < self.sep:
                self.below[k] = (mn, rule(self.run, k, self.sep))

    def response(self):
        """The robot's response decision: the first decision with a positive hold or a switch (the winner other than
        the task held, that task still in the pool)."""
        held = None
        for d in self.dec:
            s = self.sel[d.tick]
            pool = [c["task"] for c in s["candidates"]]
            if (s["hold"] or 0) > 0:
                return d.tick, f"hold {s['hold']}"
            if held is not None and s["winner"] is not None and s["winner"] != held and held in pool \
                    and d.trigger.value != "no_current_task":
                return d.tick, "switch"
            held = s["winner"]
        return None, "none"

    def cases(self):
        """The contiguous runs of ticks below min_separation."""
        out = []
        for k in sorted(self.below):
            if out and out[-1][-1] == k - 1:
                out[-1].append(k)
            else:
                out.append([k])
        return out

    def in_force(self, t):
        return max((d for d in self.dec if d.tick <= t), key=lambda d: d.tick, default=None)


def short(k):
    return R.short(k) if k else "-"


def proj(d):
    if d is None:
        return "-"
    if d.admitted is not None:
        return f"{d.tick}: admitted {G.short(d.admitted.key)}"
    return f"{d.tick}: fallback {d.fallback.mode.value} k={d.fallback.k}" if d.fallback else f"{d.tick}: none"


# The cause of each case below min_separation: (step, scenario, side, first tick) -> cause. Read from the case table.
CAUSES = {
    ("step 5", "scenario_s16_01", "off", 44): ("other", "no projection past the human's arrival at shelf_4 (the moving fallback runs to 44); the robot arrives beside the turn and holds there, standing"),
    ("step 5", "scenario_s16_01", "on", 49): ("turn (TODO-146)", "the admitted plan about one tick and 18 cm ahead of the executed human at the turn"),
    ("step 5", "scenario_s16_02", "on", 48): ("turn (TODO-146)", "the admitted plan about one tick and 18 cm ahead of the executed human at the turn"),
    ("step 5", "scenario_s16_05", "on", 22): ("wrong admission", "deliver_item(item_4) admitted while the human walks to the A/C switch; no hold"),
    ("step 5b", "scenario_s11_03", "on", 11): ("wrong admission", "deliver_item(item_12), assigned and never performed, admitted at 0 while the human stands at the occupied table; no hold, item_8 released beside the human"),
    ("step 5b", "scenario_s12_02", "off", 138): ("other", "the human, leaving the coffee machine, walks past the robot standing in its hold (decided at 137 on a moving fallback); the robot moves off at 140"),
    ("step 5b", "scenario_s12_02", "on", 138): ("other", "the human, leaving the coffee machine, walks past the robot standing in its hold (decided at 135 on the admitted deliver_item(item_2), the true task; 134 before the gate change); the robot moves off at 141"),
}


def b(pairs):
    print("| step | scenario | side | completion | Δ to off | response decision (tick: what) | Δ to off | min separation (tick) | "
          "ticks below: standing robot | moving robot (F1 viol / recede) | cases below (first-last: min) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    case_rows, summary = [], dict(gain=[], loss=[], better=0, equal=0, worse=0)
    done_off = set()
    for step, on, off in pairs:
        sides = [("off", off), ("on", on)]
        runs = {s: PRun(x) for s, x in sides}
        c0, r0 = runs["off"].props["completion"], runs["off"].response()
        for side, x in sides:
            if side == "off" and (step, off.name) in done_off:
                continue
            p = runs[side]
            c, (rt, rw) = p.props["completion"], p.response()
            st = sum(1 for v in p.below.values() if v[1] == "stand")
            vi = sum(1 for v in p.below.values() if v[1] == "viol")
            rc = sum(1 for v in p.below.values() if v[1] == "recede")
            cs = "; ".join(f"{k[0]}-{k[-1]}: {min(p.below[t][0] for t in k):.1f}" for k in p.cases()) or "none"
            m = p.props["measures"]["sep_min_continuous"]
            dc = "-" if side == "off" else f"{c - c0:+d}"
            dr = "-" if side == "off" or rt is None or r0[0] is None else f"{rt - r0[0]:+d}"
            print(f"| {step} | {on.name if side == 'on' else off.name} | {side} | {c} | {dc} | "
                  f"{rt if rt is not None else '-'}: {rw} | {dr} | {m[0]:.1f} ({m[1]}) | {st} | {vi + rc} ({vi} / {rc}) | {cs} |")
            if side == "on":
                (summary["gain"] if c < c0 else summary["loss"]).append(c - c0) if c != c0 else None
                summary["better" if c < c0 else "worse" if c > c0 else "equal"] += 1
            for k in p.cases():
                d = p.in_force(k[0])
                mn = min(p.below[t][0] for t in k)
                cls = {c_: sum(1 for t in k if p.below[t][1] == c_) for c_ in ("stand", "viol", "recede")}
                truth = p.truth.get(k[0])
                wrong = d is not None and d.admitted is not None and G.short(d.admitted.key) != (G.short(truth) if truth else None)
                other = runs["on" if side == "off" else "off"]
                near = [t for t in other.below if k[0] - 5 <= t <= k[-1] + 5]
                case_rows.append(dict(step=step, scen=on.name if side == "on" else off.name, side=side, a=k[0], b=k[-1],
                                      mn=mn, cls=cls, proj=proj(d), truth=G.short(truth) if truth else "unmodelled",
                                      wrong=wrong, other=f"{min(near)}-{max(near)}" if near else "none"))
        done_off.add((step, off.name))
    return case_rows, summary


def b3(case_rows):
    print("| step | scenario | side | ticks | min | standing / viol / recede | decision in force: projection | human's true "
          "task | cause | the same span below min_separation on the other side (±5 ticks) |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    tally = {}
    for r in case_rows:
        key = (r["step"], r["scen"], r["side"], r["a"])
        cause = CAUSES.get(key)
        if cause is None:
            if r["cls"]["viol"] == 0 and r["cls"]["recede"] == 0:
                cause = ("standing", "the robot standing (not robot-responsible under F1)")
            else:
                cause = ("unclassified", "NOT CLASSIFIED")
        tally.setdefault((r["side"], cause[0]), []).append(key)
        c = r["cls"]
        print(f"| {r['step']} | {r['scen']} | {r['side']} | {r['a']}-{r['b']} | {r['mn']:.1f} | {c['stand']} / {c['viol']} / "
              f"{c['recede']} | {r['proj']} | {r['truth']} | {cause[0]}: {cause[1]} | {r['other']} |")
    return tally


def main():
    S.SCHEMAS.update({s.name: s for s in importlib.import_module("domains.kitting.registry").domain_config["task_model"]})
    pairs = rec_pairs()
    print(f"## A. Recognition ({sum(p[0] == 'step 4' for p in pairs)} pairs of step 4, "
          f"{sum(p[0] == 'step 5b' for p in pairs)} of step 5b)\n")
    print("### A1. Admissions of the true task, on against off\n")
    a1(pairs)
    print("\n### A2. Admissions of a hypothesis that is not the true task\n")
    a2(pairs)
    print("\n### A2, the kinds: what the evidence alone said (the off run)\n")
    a2_kinds(pairs)
    print("\n### A3. A lone assigned task admitted before the human starts it\n")
    a3(pairs)
    pp = plan_pairs()
    print(f"\n## B. Planning ({sum(p[0] == 'step 5' for p in pp)} on runs of step 5, "
          f"{sum(p[0] == 'step 5b' for p in pp)} of step 5b)\n")
    print("### B1 and B2. Completion, the response decision, the separation\n")
    rows, summ = b(pp)
    print("\n### B3. Every case below min_separation, with its cause\n")
    tally = b3(rows)
    print("\n### Planning tallies\n")
    print(f"- completion, on against off: better {summ['better']}, equal {summ['equal']}, worse {summ['worse']}; ticks "
          f"gained {-sum(summ['gain'])} over {len(summ['gain'])} runs ({sorted(summ['gain'])}), ticks lost "
          f"{sum(summ['loss'])} over {len(summ['loss'])} runs ({sorted(summ['loss'])})")
    for (side, cause), keys in sorted(tally.items()):
        print(f"- cases below min_separation, {side}, {cause}: {len(keys)} "
              f"({', '.join(k[1].removeprefix('scenario_') + ' ' + str(k[3]) for k in keys)})")


if __name__ == "__main__":
    main()
