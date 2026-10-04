#!/usr/bin/env python3
"""
g_reading.py — the reading for question G (T-K part 1, Hadi, 4 October 2026): admission and retraction under context
knowledge. Reporting only, read from step 4's outputs (`actual.csv` of this set, its off side in `off/` and round 1),
nothing run and nothing recomputed.

For every admission of a hypothesis that is not the true task, context knowledge on (admission.py's P8 rows; the
one-tick rows on a completion left out; the exit walk in its own table):
1. at the admission: the admitted hypothesis's belief over H (`belief_h`, the gate's value), its prior, its hypothesis
   adequacy and the warrant source. The admission is the first tick of the run of ticks on which the gate clears with
   that hypothesis leading (the idle robot's gate per tick, as admission.py reads it); where that run began while the
   hypothesis was the true task, the admission was right then, and the wrong ticks start where the human left it.
   Commitment warrant: the hypothesis is one of the human's assigned tasks (the run log's `[IR-assignment]` line);
   observation warrant: the `warrant` column;
2. over the admitted ticks (the gate's run): the ticks with observation warrant and the ticks adequate;
3. from the off run of the same script (equal prior, the ranking by the evidence alone), searched from the first tick
   on which the admitted hypothesis is not the true task: the first tick on which another live hypothesis has a
   strictly greater belief than the admitted one, and the first tick on which the true task has the strictly greatest
   belief; on each, the two leading values, their absolute difference and their ratio. Equality within 1e-9 (the
   instruments' agreement level) is a tie: a tie is reported with its first tick and length and gets no first tick;
4. what ended it: the gate's outcome on the next tick (admission.py's reading), and what the meta-planner's trigger
   rule would read against a record set at the admission (`evaluate_triggers`: the leader changes, an episode boundary,
   the recorded hypothesis inadequate; the gate is not asked for retention), the first such tick from the admission.
Then the two counts over the admissions of the true task (admission.py's stretches), on and off: how many rest on
commitment warrant with no observation warrant on the admission tick, and how many of those are lone deliveries (one
delivery live at the stretch's first tick, the report's reading).

    g_reading.py            run from the repository root; prints markdown
"""
import csv
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "analysis/instruments/irb"))
sys.path.insert(0, str(ROOT))
import admission as A
import offon as O
import summary as S

THETA = 0.75
TIE = 1e-9
NAME = "actual.csv"
ON = ROOT / "analysis/kitting/irb/tk2"
OFFS = [ON / "off", ROOT / "analysis/kitting/irb/tk1"]


def short(k):
    """A hypothesis key as the table names it: a delivery by its item, a foreseeable task by its schema."""
    if not k:
        return "-"
    m = re.match(r"(\w+)\((.*)\)$", S.short(k))
    return m[2] if m[1] == "deliver_item" else m[1]


class Run:
    def __init__(self, d, log=None):
        self.d, self.sid = d, d.name.removeprefix("scenario_")
        traj = json.load(open(d / "trajectory.json"))
        self.truth = {r["tick"]: (S.hypothesis_key(r["task"]) if r["task"] else None)
                      for r in traj["rows"] if r["tick"] >= 0}
        self.tick, self.hyp = {}, {}
        for r in csv.DictReader(open(d / NAME)):
            t = int(r["tick"])
            if t < 0:
                continue
            self.tick.setdefault(t, dict(leader=r["most_likely"], gate=r["gate"], boundary=r["boundary"] == "1",
                                         pins=r["pins"].split(";")))
            if r["key"]:
                self.hyp.setdefault(t, {})[r["key"]] = dict(b=float(r["belief_h"]), prior=float(r["prior"]) if r["prior"] else None,
                                                            adequacy=r["adequacy"], warrant=r["warrant"])
        self.assigned = set()
        if log is not None:
            for l in open(log):
                m = re.match(r"\[IR-assignment\] knowledge=on known=\[(.*)\]$", l)
                if m:
                    self.assigned = {S.hypothesis_key(k) for k in re.findall(r"'([^']+)'", m[1])}
        self.last = max(self.tick)

    def clears_for(self, t, h):
        return t in self.tick and self.tick[t]["gate"] == "clears" and self.tick[t]["leader"] == h

    def warrant(self, t, h):
        src = (["commitment"] if h in self.assigned else []) + \
              (["observation"] if self.hyp[t][h]["warrant"] == "observation" else [])
        return ",".join(src) or "none"

    def top2(self, t):
        v = sorted(self.hyp[t].items(), key=lambda kv: -kv[1]["b"])
        (k1, a1), (k2, a2) = v[0], (v[1] if len(v) > 1 else (None, dict(b=0.0)))
        return k1, a1["b"], k2, a2["b"]


def lead(run, t, h=None):
    """The two leading values on tick t, their absolute difference and their ratio; the admitted one's if not in them."""
    k1, v1, k2, v2 = run.top2(t)
    ratio = f"{v1 / v2:.4f}" if v2 > 0 else "∞"
    diff = f"{v1 - v2:.2g}" if v1 - v2 < 1e-3 else f"{v1 - v2:.4f}"
    own = (f"; admitted {run.hyp[t][h]['b']:.4f}" if h is not None and h not in (k1, k2) and h in run.hyp[t] else "")
    return f"{short(k1)} {v1:.4f} / {short(k2) if k2 else '-'} {v2:.4f} (Δ {diff}, ×{ratio}{own})"


def first_strict(run, a, cond):
    """cond(t) -> 'gt' | 'tie' | 'no' | 'stop'. The first tick from a with 'gt'; the ties met before it."""
    ties, t = [], a
    while t <= run.last:
        if t not in run.hyp:
            t += 1
            continue
        c = cond(t)
        if c == "stop":
            return None, ties, t
        if c == "tie":
            if ties and ties[-1][1] == t - 1:
                ties[-1][1] = t
            else:
                ties.append([t, t])
        if c == "gt":
            return t, ties, None
        t += 1
    return None, ties, None


def other_above(off, h):
    def cond(t):
        if h not in off.hyp[t]:
            return "stop"
        mine = off.hyp[t][h]["b"]
        rest = [v["b"] for k, v in off.hyp[t].items() if k != h]
        if not rest:
            return "no"
        m = max(rest)
        return "gt" if m > mine + TIE else ("tie" if abs(m - mine) <= TIE else "no")
    return cond


def true_greatest(off):
    def cond(t):
        k = off.truth.get(t)
        if k is None or k not in off.hyp[t]:
            return "no"
        mine = off.hyp[t][k]["b"]
        rest = [v["b"] for kk, v in off.hyp[t].items() if kk != k]
        if not rest:
            return "gt"
        m = max(rest)
        return "gt" if mine > m + TIE else ("tie" if abs(m - mine) <= TIE else "no")
    return cond


def fmt_first(off, a, found, ties, stop, held_before, h=None):
    tie = "; ".join(f"tie {x} ({y - x + 1} tick{'s' if y > x else ''})" for x, y in ties)
    if found is None:
        alone = h is not None and all(set(off.hyp[t]) == {h} for t in range(a, off.last + 1) if t in off.hyp)
        s = (f"none (the admitted hypothesis not live from {stop})" if stop is not None else
             "none: no other live hypothesis" if alone else "none to the run's end")
    else:
        s = f"{found} (+{found - a}{', held before' if found == a and held_before else ''}): {lead(off, found, h)}"
    return f"{tie}; {s}" if tie else s


def no_fire(run, t, h):
    """The trigger rule's recorded side fires nothing on tick t against a record of h."""
    return (run.tick[t]["leader"] == h and not run.tick[t]["boundary"]
            and run.hyp.get(t, {}).get(h, {}).get("adequacy") != "inadequate")


def record_end(run, a, h):
    """The record of h that holds on tick a (the gate clears for h there): its first tick (the first tick the gate
    clears for h after the last tick the rule would have fired) and the tick on which the rule fires against it."""
    s = a
    while (s - 1) in run.tick and run.tick[s - 1]["leader"] == h and no_fire(run, s, h):
        s -= 1
    a0 = next(t for t in range(s, a + 1) if run.clears_for(t, h))
    return f"record from {a0}; fires {fire(run, a0, h)}"


def fire(run, a0, h):
    """The first tick after a0 on which the trigger rule would fire against a record of h set at a0."""
    for t in range(a0 + 1, run.last + 1):
        if t not in run.tick:
            continue
        if run.tick[t]["leader"] != h:
            return f"{t} leader {short(run.tick[t]['leader']) if run.tick[t]['leader'] else 'none'}"
        if run.tick[t]["boundary"]:
            return f"{t} boundary"
        if run.hyp[t][h]["adequacy"] == "inadequate":
            return f"{t} inadequate"
    return "run's end"


def reading(run, off, w):
    h, a, b = w["h"], w["a"], w["b"]
    a0 = a
    while run.clears_for(a0 - 1, h):
        a0 -= 1
    x = run.hyp[a0][h]
    at = (f"{a0}{'' if a0 == a else ' (right until ' + str(a - 1) + ')'}: b {x['b']:.3f}, prior {x['prior']:.3f}, "
          f"{x['adequacy']}, {run.warrant(a0, h)}")
    span = range(a0, b + 1)
    obs = sum(run.hyp[t][h]["warrant"] == "observation" for t in span)
    obs_w = sum(run.hyp[t][h]["warrant"] == "observation" for t in range(a, b + 1))
    adq = sum(run.hyp[t][h]["adequacy"] == "adequate" for t in span)
    over = (f"{len(span)} ticks: obs. warrant {obs}, adequate {adq}"
            + ("" if a0 == a else f"; of the {b - a + 1} wrong: obs. warrant {obs_w}"))
    oc = other_above(off, h)
    f1, t1, s1 = first_strict(off, a, oc)
    held1 = f1 == a and (a - 1) in off.hyp and oc(a - 1) == "gt"
    tc = true_greatest(off)
    f2, t2, s2 = first_strict(off, a, tc)
    held2 = f2 == a and (a - 1) in off.hyp and tc(a - 1) == "gt"
    nxt = b + 1
    gate_end = (f"{nxt} {off_gate(run, nxt)}" if nxt <= run.last else "run's end")
    meta = dict(commitment_only=run.warrant(a0, h) == "commitment",
                lone=sum(1 for k in run.hyp[a0] if k.startswith("deliver_item")) == 1 and h.startswith("deliver_item"))
    true = re.sub(r"(\w+)\(([^()]*)\)", lambda m: m[2] if m[1] == "deliver_item" else m[1], w["true"])
    return meta, [short(h), f"{a} to {b}" if a != b else f"{a}", true, at, over,
            fmt_first(off, a, f1, t1, s1, held1, h), fmt_first(off, a, f2, t2, s2, held2) if w["true"] != "unmodelled"
            else "- (unmodelled)", gate_end, record_end(run, a, h)]


def off_gate(run, t):
    g, l = run.tick[t]["gate"], run.tick[t]["leader"]
    return f"{g}" + (f" ({short(l)})" if g == "clears" or g == "none(below_theta)" else "")


def counts(run):
    """Admissions of the true task: (total, commitment only at the admission tick, of those lone deliveries). The
    admission tick is the first tick of the gate's run that reaches the stretch's admission."""
    _, _, st = A.stretches(run.d, NAME, THETA)
    tot = comm = lone = 0
    for s in st:
        if s["adm"] is None:
            continue
        tot += 1
        a0 = s["adm"]
        while run.clears_for(a0 - 1, s["key"]):
            a0 -= 1                                       # the gate's run may begin on the previous task's pin tick
        if run.warrant(a0, s["key"]) == "commitment":
            comm += 1
            n = sum(1 for k in run.hyp[s["a"]] if k.startswith("deliver_item")) if s["a"] in run.hyp else None
            lone += n == 1
    return tot, comm, lone


def main():
    S.SCHEMAS.update({s.name: s for s in importlib.import_module("domains.kitting.registry").domain_config["task_model"]})
    head = ("| scenario | admitted | wrong ticks | true task | 1. at the admission: belief, prior, adequacy, warrant | "
            "2. over the admitted ticks | 3a. off: another strictly above it (top two) | "
            "3b. off: the true task strictly greatest (top two) | 4. gate's end | 4. the trigger rule's end |")
    rule = "|---|---|---|---|---|---|---|---|---|---|"
    main_rows, exit_rows, cnt_on, cnt_off, seen = [], [], [0, 0, 0], [0, 0, 0], set()
    wrong_comm = [0, 0, 0]
    for d in sorted(p for p in ON.iterdir() if p.is_dir() and (p / NAME).exists()):
        traj = json.load(open(d / "trajectory.json"))
        log = ON / "runs" / f"{traj['layout']}_{d.name}_on.log"
        run = Run(d, log)
        o = O.off_dir_of(d, OFFS, NAME)
        off = Run(o, None)
        off.assigned = run.assigned                       # the same assigned tasks; the off side's log is not read
        _, wrong = A.wrong_admissions(d, NAME)
        for w in wrong:
            if all("complete: pinned" in part for part in w["true"].split(", ")):
                continue
            meta, cells = reading(run, off, w)
            (exit_rows if w["true"] == "unmodelled" else main_rows).append([run.sid] + cells)
            if w["true"] != "unmodelled":
                wrong_comm[0] += 1
                wrong_comm[1] += meta["commitment_only"]
                wrong_comm[2] += meta["commitment_only"] and meta["lone"]
        for c, r in ((cnt_on, run), (cnt_off, off)):
            if r is off and o in seen:
                continue                                  # one off run is the off side of several timelines
            seen.add(o) if r is off else None
            for i, v in enumerate(counts(r)):
                c[i] += v
    print("### During modelled tasks\n")
    print(head)
    print(rule)
    for r in main_rows:
        print("| " + " | ".join(r) + " |")
    print("\n### The exit walk (unmodelled)\n")
    print(head)
    print(rule)
    for r in exit_rows:
        print("| " + " | ".join(r) + " |")
    print(f"\n### Admissions of the true task resting on commitment warrant alone on the admission tick\n")
    print(f"- on: {cnt_on[1]} of {cnt_on[0]} admissions of the true task; lone deliveries among them: {cnt_on[2]}")
    print(f"- the rows of the first table (on, a hypothesis not the true task): {wrong_comm[1]} of {wrong_comm[0]}; "
          f"lone deliveries among them (one delivery live on the admission tick): {wrong_comm[2]}")
    print(f"- off (each script's off run once): {cnt_off[1]} of {cnt_off[0]}; lone deliveries among them: {cnt_off[2]}")


if __name__ == "__main__":
    main()
