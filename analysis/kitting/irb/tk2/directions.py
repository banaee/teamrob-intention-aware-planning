#!/usr/bin/env python3
"""
directions.py — the directions of Hadi's point 5 (T-K part 1, step 4), read on the set's outputs (reporting only).

Sides (Hadi, stage 3): off (context knowledge off; the same script's run, round 1 or `off/`); on without the raising
fact for the case's foreseeable task; on with it. Kinds: "within" (one script: off against on, or the same script
under different timelines); "across" (different scripts), stated with what confounds it. A script is identified by
its human actions on its layout (offon.py's rule). Every number is read from `<csv>` (expected.csv before the runs,
actual.csv after them) through admission.py's readings and the per-tick columns (levels, belief_h, gate, pins).

    directions.py <csv name>        run from the repository root
"""
import csv
import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "analysis/instruments/irb"))
sys.path.insert(0, str(ROOT))
import admission as A
import offon as O
import summary as S

THETA = 0.75
ON = ROOT / "analysis/kitting/irb/tk2"
OFFS = [ON / "off", ROOT / "analysis/kitting/irb/tk1"]


class Run:
    def __init__(self, d, name):
        self.d, self.sid = d, d.name.removeprefix("scenario_")
        lay, acts = O.script_of(d)
        self.script = (lay, tuple(acts))
        _, _, st = A.stretches(d, name, THETA)
        self.stretches = {(r["key"], r["a"]): r for r in st}
        _, self.wrong = A.wrong_admissions(d, name)
        self.tick, self.belief = {}, {}
        for r in csv.DictReader(open(d / name)):
            t = int(r["tick"])
            if t < 0:
                continue
            self.tick.setdefault(t, dict(levels=dict(x.split("=") for x in r["levels"].split()), gate=r["gate"],
                                         leader=r["most_likely"], pins=r["pins"].split(";"), live=[]))
            if r["key"]:
                self.tick[t]["live"].append(r["key"])
                self.belief.setdefault(t, {})[r["key"]] = float(r["belief_h"])
        self.timeline = O.timeline_of(d)

    def live_deliveries(self, t):
        return sum(1 for k in self.tick[t]["live"] if k.startswith("deliver_item"))

    def level(self, t, task):
        return self.tick[t]["levels"].get(task) if t in self.tick else None

    def levels_over(self, a, b, task):
        return sorted({self.level(t, task) for t in range(a, b + 1) if t in self.tick and self.level(t, task)})


def fmt(t, a):
    return "never" if t is None else f"{t} ({t - a})"


def main(name):
    S.SCHEMAS.update({s.name: s for s in importlib.import_module("domains.kitting.registry").domain_config["task_model"]})
    ons = [Run(d, name) for d in sorted(p for p in ON.iterdir() if p.is_dir() and p.name.startswith("scenario_"))]
    off_name = name
    offs = {}
    for r in ons:
        o = O.off_dir_of(r.d, OFFS, off_name)
        offs[r.sid] = Run(o, off_name)
    groups = {}
    for r in ons:
        groups.setdefault(r.script, []).append(r)

    out = []
    p = out.append

    # ---------------------------------------------------------------- per true stretch: off and every on side
    p("## Per true stretch, off and every on side of the same script (within one script)\n")
    p("Side: the level of the case's foreseeable task (a foreseeable stretch: its own; a delivery: its rivals') on "
      "the ticks from the stretch's start to the later of the two admissions. `live`: deliveries live at the start.\n")
    p("| script (off from) | true hypothesis | ticks | live | off: θ / admitted | on, per scenario: side → θ / admitted |")
    p("|---|---|---|---|---|---|")
    for script, runs in groups.items():
        off = offs[runs[0].sid]
        for (key, a), f in sorted(off.stretches.items(), key=lambda x: x[0][1]):
            cells = []
            for r in runs:
                s = r.stretches[(key, a)]
                end = max(x for x in (s["adm"], f["adm"], s["hit"], f["hit"], a) if x is not None)
                task = key.split("(")[0]
                lv = (r.levels_over(a, end, task) if not task.startswith("deliver")
                      else [f"{n} {'/'.join(r.levels_over(a, end, n))}" for n in ("coffee_break", "ac_activation")
                            if r.levels_over(a, end, n)])
                cells.append(f"{r.sid} [{', '.join(lv)}] → {fmt(s['hit'], a)} / {fmt(s['adm'], a)}")
            p(f"| {off.sid} | {S.short(key)} | {a} to {f['b']} | {off.live_deliveries(a)} | "
              f"{fmt(f['hit'], a)} / {fmt(f['adm'], a)} | {'; '.join(cells)} |")

    # ---------------------------------------------------------------- the A/C at arrival
    p("\n## The A/C activation's belief at its arrival (within one script)\n")
    p("| script (off) | arrival | live | off | on, per scenario: level at arrival → belief |")
    p("|---|---|---|---|---|")
    for script, runs in groups.items():
        off = offs[runs[0].sid]
        for (key, a), f in off.stretches.items():
            if not key.startswith("ac_activation") or not f["at_arrival"]:
                continue
            t = int(f["at_arrival"].split(" at ")[1])
            cells = [f"{r.sid} [{r.level(t, 'ac_activation')}; coffee {r.level(t, 'coffee_break')}] → "
                     f"{r.stretches[(key, a)]['at_arrival'].split(' at ')[0]}" for r in runs]
            p(f"| {off.sid} | {t} | {off.live_deliveries(t)} | {f['at_arrival'].split(' at ')[0]} | {'; '.join(cells)} |")

    # ---------------------------------------------------------------- the prior alone at a coffee break's start
    p("\n## The coffee break on its stretch's first observed ticks (the prior alone, direction 2)\n")
    p("The evidence restarts equal at the episode's boundary, so the belief on the stretch's first tick is the prior "
      "over the live hypotheses. `first clears`: the first tick on which the gate clears for it.\n")
    p("| scenario | stretch | live | level | belief at start | gate at start | first ≥ θ | first clears |")
    p("|---|---|---|---|---|---|---|---|")
    for r in ons:
        for (key, a), s in sorted(r.stretches.items(), key=lambda x: x[0][1]):
            if key.startswith("coffee_break"):
                b = r.belief.get(a, {}).get(key)
                p(f"| {r.sid} | {a} to {s['b']} | {r.live_deliveries(a)} | {r.level(a, 'coffee_break')} | "
                  f"{'-' if b is None else f'{b:.4f}'} | {r.tick[a]['gate']} | {fmt(s['hit'], a)} | {fmt(s['adm'], a)} |")

    # ---------------------------------------------------------------- the recency fact
    p("\n## The recency fact after an observed coffee break (direction 4)\n")
    p("Per completion: the ticks on which the coffee break is live and suppressed, those of them inside break_time, "
      "and its level on the first tick after the 90.\n")
    p("| scenario | completion | suppressed on (live ticks) | of them inside break_time | level after |")
    p("|---|---|---|---|---|")
    for r in ons:
        traj = json.load(open(r.d / "trajectory.json"))
        bt = {row["tick"] for row in traj["rows"] if ["break_time"] in row["facts"]}
        comp = [t for t in sorted(r.tick) if any(k.startswith("coffee_break") for k in r.tick[t]["pins"])]
        for c in comp:
            sup = [t for t in range(c, c + 90) if r.level(t, "coffee_break") == "suppressed"]
            live = [t for t in range(c, c + 90) if r.level(t, "coffee_break")]
            after = r.level(c + 90, "coffee_break") if c + 90 in r.tick else "run ended"
            p(f"| {r.sid} | {c} | {len(sup)} of {len(live)} | {len([t for t in sup if t in bt])} | {after} |")

    # ---------------------------------------------------------------- the edges inside an episode
    p("\n## A level changing inside an episode (direction 5)\n")
    p("Every tick on which a foreseeable task's level changes while it stays live, inside a true stretch: the true "
      "hypothesis's belief before and on that tick, and the gate for it before and on that tick.\n")
    p("| scenario | tick | change | true task | belief before → on | gate before → on |")
    p("|---|---|---|---|---|---|")
    for r in ons:
        traj = json.load(open(r.d / "trajectory.json"))
        truth = {row["tick"]: (S.hypothesis_key(row["task"]) if row["task"] else None) for row in traj["rows"]}
        for t in sorted(r.tick):
            if t - 1 not in r.tick:
                continue
            ch = [f"{n} {r.level(t - 1, n)}→{r.level(t, n)}" for n in ("coffee_break", "ac_activation")
                  if r.level(t - 1, n) and r.level(t, n) and r.level(t - 1, n) != r.level(t, n)]
            k = truth.get(t)
            if not ch or not k or truth.get(t - 1) != k:
                continue
            b0, b1 = r.belief.get(t - 1, {}).get(k), r.belief.get(t, {}).get(k)
            g = lambda u: "clears" if r.tick[u]["gate"] == "clears" and r.tick[u]["leader"] == k else (
                f"{r.tick[u]['gate']} ({S.short(r.tick[u]['leader'])})")
            p(f"| {r.sid} | {t} | {'; '.join(ch)} | {S.short(k)} | "
              f"{'-' if b0 is None else f'{b0:.4f}'} → {'-' if b1 is None else f'{b1:.4f}'} | {g(t - 1)} → {g(t)} |")

    # ---------------------------------------------------------------- admissions of a hypothesis not the true task
    p("\n## Admissions of a hypothesis that is not the true task, off against on (P8)\n")
    p("Excluding the one-tick rows on a true task's completion tick (\"complete: pinned\"; the next task leads on its "
      "last action's ticks), counted separately. Exit walk: the unmodelled ticks.\n")
    p("| scenario | off: exit walk | off: other | on: exit walk | on: other | on: one-tick on a completion |")
    p("|---|---|---|---|---|---|")
    fw = lambda rows, f: [x for x in rows if f(x)]
    show = lambda x: f"{S.short(x['h'])} {x['a']}{'' if x['a'] == x['b'] else f' to {x[chr(98)]}'} ({x['end']})"
    for r in ons:
        o = offs[r.sid]
        cell = []
        for rows in (o.wrong, r.wrong):
            ex = fw(rows, lambda x: x["true"] == "unmodelled")
            pinned_only = lambda x: all("complete: pinned" in part for part in x["true"].split(", "))
            ot = fw(rows, lambda x: x["true"] != "unmodelled" and not pinned_only(x))
            cell += ["; ".join(map(show, ex)) or "none", "; ".join(f"{show(x)} while {x['true']}" for x in ot) or "none"]
        pin = fw(r.wrong, lambda x: all("complete: pinned" in part for part in x["true"].split(", ")))
        p(f"| {r.sid} | {cell[0]} | {cell[1]} | {cell[2]} | {cell[3]} | {len(pin)} |")
    # ---------------------------------------------------------------- the stretches sorted by direction and side
    p("\n## The stretches sorted by direction and side (within one script: off against on, the same tick span)\n")
    p("Delay: admitted tick minus the stretch's first tick; `never` sorts last. A rival's side is the set of its levels "
      "from the stretch's start to the later admission.\n")
    NEVER = 10 ** 6
    rows = []
    for script, runs in groups.items():
        off = offs[runs[0].sid]
        for (key, a), f in off.stretches.items():
            n = off.live_deliveries(a)
            for r in runs:
                s = r.stretches[(key, a)]
                end = max(x for x in (s["adm"], f["adm"], a) if x is not None)
                own = key.split("(")[0]
                rivals = {t: set(r.levels_over(a, end, t)) for t in ("coffee_break", "ac_activation") if t != own}
                rows.append(dict(sid=r.sid, off=off.sid, key=key, a=a, n=n, own=own,
                                 own_levels=set(r.levels_over(a, end, own)), rivals=rivals,
                                 on=NEVER if s["adm"] is None else s["adm"] - a,
                                 offd=NEVER if f["adm"] is None else f["adm"] - a))
    d = lambda x: "never" if x == NEVER else str(x)

    def side(x):
        """'with': the raising fact's level throughout the span (a delivery: one rival raised throughout, no other
        rival raised; a foreseeable stretch: its own level raised throughout); 'without': no raised level in the span;
        'edge': a level changes to or from raised inside the span (direction 5's)."""
        if x["own"] == "deliver_item":
            r = [v for v in x["rivals"].values() if "raised" in v]
            return "without" if not r else "with" if len(r) == 1 and r[0] == {"raised"} else "edge"
        return "without" if "raised" not in x["own_levels"] else "with" if x["own_levels"] == {"raised"} else "edge"

    for x in rows:
        x["side"] = side(x)
    stretch = {}
    for x in rows:
        stretch.setdefault((x["off"], x["key"], x["a"]), []).append(x)

    def verdict(title, own, side_, better):
        """Within one script: each on stretch of side `side_` against off, and against the same stretch's on sides
        'without' in other scenarios of the script (for side_ 'with')."""
        xs = [x for x in rows if x["own"] == own and x["side"] == side_]
        tally = {}
        for x in xs:
            k = "as stated" if better(x["on"], x["offd"]) else "equal" if x["on"] == x["offd"] else "against"
            tally.setdefault(x["n"], {}).setdefault(k, []).append(x)
        p(f"- {title}, against off: {len(xs)} stretches; " + "; ".join(
            f"{n} live: " + ", ".join(f"{k} {len(v)}" for k, v in sorted(t.items())) + " (on's delays "
            + ", ".join(f"{dl}: {c}" for dl, c in sorted(__import__("collections").Counter(
                d(x["on"]) for v in t.values() for x in v).items(), key=lambda z: (len(z[0]), z[0]))) + ")"
            for n, t in sorted(tally.items())))
        for n, t in sorted(tally.items()):
            for x in t.get("against", []) + t.get("equal", []):
                p(f"  - {'against' if x in t.get('against', []) else 'equal'}: {x['sid']} {S.short(x['key'])} from "
                  f"{x['a']} ({n} live): off {d(x['offd'])}, on {d(x['on'])}")
        if side_ != "with":
            return
        pairs = [(x, y) for x in xs for y in stretch[(x["off"], x["key"], x["a"])] if y["side"] == "without"]
        p(f"- {title}, against on without the raising fact (the same script): {len(pairs)} pairs")
        for x, y in pairs:
            k = "as stated" if better(x["on"], y["on"]) else "equal" if x["on"] == y["on"] else "against"
            p(f"  - {k}: {S.short(x['key'])} from {x['a']} ({x['n']} live): {x['sid']} with {d(x['on'])}, "
              f"{y['sid']} without {d(y['on'])}, off {d(x['offd'])}")
        lacking = [f"{x['sid']} {S.short(x['key'])} from {x['a']} ({x['n']} live)" for x in xs
                   if not any(y["side"] == "without" for y in stretch[(x["off"], x["key"], x["a"])])]
        p(f"  - no on side without the raising fact in the set for: {'; '.join(lacking) or 'none'}")

    verdict("1, a delivery, no rival raised (on: ordinary or suppressed), admitted earlier on than off",
            "deliver_item", "without", lambda on, off: on < off)
    verdict("1, the coffee break never raised, admitted later on than off", "coffee_break", "without",
            lambda on, off: on > off)
    verdict("2, the coffee break raised throughout, admitted earlier", "coffee_break", "with", lambda a, b: a < b)
    verdict("2, a delivery with a rival raised throughout, admitted later", "deliver_item", "with", lambda a, b: a > b)
    edges = [x for x in rows if x["side"] == "edge"]
    p(f"- 5, stretches with a level changing to or from raised inside the span (read in the section on edges): "
      f"{len(edges)}: " + ", ".join(f"{x['sid']} {S.short(x['key'])}" for x in edges))
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1])
