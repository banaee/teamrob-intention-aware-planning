#!/usr/bin/env python3
"""
measures.py — the meta-planner test-bed's part 4, the part every domain shares (MPB-1, MPB-3; design_decisions.md, "The
meta-planner test-bed (MPB)"): the run's outputs read once, the measures reported for every run, the two detectors,
X5's ground (1), the property record and the markdown. A domain's declared properties are its own, in
analysis/<domain>/mpb/properties.py, which builds on `Part4` and calls `main`. Moved here from kitting's properties.py
when dock_loading's MPB was built (T-G stage 1, 2 October 2026); kitting's outputs are byte-identical.

The planner's logged decision values (the winner, its hold, the candidates' [meta-cand] delta) are observed inputs to a
property, never an input to a derivation of what should hold. The instrument's own computations are F1's classes over
the executed positions (analysis/instruments/common/sep_classes.py, F1's execution rule) and the layout's path
lengths; never a hold.

For every run:
- completion (the world tick after the robot's last release on a task), holds, near-encounters and F1's classes;
- the decisions with their trigger, cause, gate, projection, winner and hold;
- two detectors, recorded and classified by hand:
  - TODO-134: a decision resting on a fallback stand whose first executed robot tick is an F1 violation;
  - the arrival-tick ray (the plan's objection 1; Hadi, point 5): a decision resting on a moving fallback whose ray
    starts inside a fixed object's arrival radius the human entered on that tick (the skip rule lets the ray run
    through the object). Class 3 under MPB-4 when it occurs.
"""
import importlib
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT), str(ROOT / "analysis" / "instruments" / "common")]

import yaml
import logparse
from sep_classes import rule, summary
from mpblib import Mode, Room, load_decisions, skipped_objects


def domain_of(run_file):
    """The run file's domain's registry (domains/<domain>/registry.py)."""
    return importlib.import_module(f"domains.{yaml.safe_load(open(run_file))['domain']}.registry").domain_config


def room_of(run_file, traj):
    domain_config = domain_of(run_file)
    cfg = yaml.safe_load(open(run_file))
    sc = domain_config["scenarios"][cfg["scenario"]]
    layout = json.load(open(ROOT / domain_config["layouts"][cfg.get("layout") or sc.reference_layouts[0]]))
    w, h = layout["space"]["width"], layout["space"]["height"]
    return Room(-w / 2, w / 2, -h / 2, h / 2, {o["id"]: tuple(o["position"]) for o in layout["env_objects"]},
                traj["params"]["proximity"])


def completion(agents):
    releases = [a["tick"] for a in agents if a["micro"] == "release" and a["task"] is not None]
    return releases[-1] + 1 if releases else None


def position_before(agents, t, start):
    """The robot's position at a decision on tick t: where it stood before its tick-t move."""
    return tuple(start) if t == 0 else tuple(agents[t - 1]["robot"])


def arrival(frm, to, radius):
    d = math.dist(frm, to)
    return tuple(frm) if d <= radius else (to[0] - (to[0] - frm[0]) * radius / d, to[1] - (to[1] - frm[1]) * radius / d)


def x5_ground1(ticks, decisions):
    """X5's ground (1), reconstructed: the stretches of consecutive ticks with the finding unexplained; in each, the
    decisions (a trigger fired) whose admission refused; and the first tick of the stretch after such a decision, where the
    finding has outlived a re-decision. A measurement over the run's own outputs."""
    out, stretch = [], []
    for t in sorted(ticks, key=lambda x: x["tick"]) + [None]:
        if t is not None and t["finding"] == "unexplained" and (not stretch or t["tick"] == stretch[-1] + 1):
            stretch.append(t["tick"])
            continue
        if stretch:
            refused = [x.tick for x in decisions if stretch[0] <= x.tick <= stretch[-1] and x.admitted is None]
            outlived = next((k for k in stretch if refused and k > refused[0]), None)
            out.append(dict(first=stretch[0], last=stretch[-1], refused_decisions=refused, ground1_from=outlived))
        stretch = [t["tick"]] if t is not None and t["finding"] == "unexplained" else []
    return out


class Part4:
    """One run's outputs, read once, and the record every domain's properties write into (`out`)."""

    def __init__(self, sid, d, log_path, run_file):
        self.sid, self.d, self.run_file = sid, d, run_file
        self.domain_config = domain_of(run_file)
        self.obs = json.load(open(d / "observed.json"))
        self.sel = json.load(open(d / "selection.json"))
        self.agents = json.load(open(d / "robot.json"))
        self.ticks = json.load(open(d / "actual_ticks.json"))
        self.traj = json.load(open(d / "trajectory.json"))
        self.decisions = load_decisions(d / "actual_decisions.json")
        self.run = logparse.parse(log_path)
        self.sep = float(self.run["hdr"].get("min_separation", 50.0))
        self.sel_by = {s["tick"]: s for s in self.sel}
        self.rm = room_of(run_file, self.traj)
        self.human_rows = {r["tick"]: r for r in self.traj["rows"]}
        obs, sel, run, sep = self.obs, self.sel, self.run, self.sep
        out = dict(scenario=sid, strategy=obs["strategy"], prior=obs["prior"], completion=completion(self.agents),
                   terminal=obs["terminal"], horizon=obs["horizon"], properties=[], measures={}, detectors={})
        s = summary(log_path)
        out["measures"] = dict(sep_min_dist=s["dist"], sep_min_continuous=s["cont"], f1=s["counts"],
                               near_encounters=sum(1 for _, (_, m) in run["sep"].items() if m is not None and m < sep),
                               holds=[(x["tick"], x["hold"]) for x in sel if x["hold"]],
                               hold_ticks=sum(x["hold"] or 0 for x in sel))
        out["decisions"] = [dict(tick=x.tick, trigger=x.trigger.value, cause=x.cause and x.cause.value,
                                 gate=x.gate.value, leader=x.leader,
                                 projection=("admitted " + x.admitted.key) if x.admitted else
                                 (f"fallback {x.fallback.mode.value} k={x.fallback.k} end={x.fallback.end:.2f}"
                                  if x.fallback else "none"),
                                 winner=self.sel_by[x.tick]["winner"], hold=self.sel_by[x.tick]["hold"])
                            for x in self.decisions]
        # the detectors
        todo134, rays = [], []
        for x in self.decisions:
            if x.fallback is not None and x.fallback.mode is Mode.STANDING and rule(run, x.tick, sep) == "viol":
                todo134.append(x.tick)
            if x.fallback is not None and x.fallback.mode is Mode.MOVING:
                pos, prev = self.human_rows[x.tick], self.human_rows[x.tick - 1]
                now = skipped_objects((pos["x"], pos["y"]), self.rm)
                before = skipped_objects((prev["x"], prev["y"]), self.rm)
                entered = [o for o in now if o not in before]
                if entered:
                    rays.append(dict(tick=x.tick, objects=entered, k=x.fallback.k, duration=x.fallback.duration,
                                     end=x.fallback.end))
        out["detectors"] = dict(todo134=todo134, arrival_tick_rays=rays)
        self.out = out

    def prop(self, name, holds, detail):
        self.out["properties"].append(dict(name=name, holds=bool(holds), detail=detail))

    def violations(self, first, last):
        """F1 robot violations (the continuous minimum below min_separation with a moving robot) on ticks first..last."""
        run, sep = self.run, self.sep
        return [k for k in range(first, last + 1)
                if k in run["sep"] and run["sep"][k][1] is not None and run["sep"][k][1] < sep
                and rule(run, k, sep) == "viol"]


def markdown(r):
    m = r["measures"]
    lines = [f"# {r['scenario']}: part 4 and the measures ({r['strategy']}, prior {'on' if r['prior'] else 'off'})", "",
             f"Completion (world tick) {r['completion']}; terminal decision {r['terminal']}. [sep] minimum "
             f"{m['sep_min_dist'][0]:.2f} ({m['sep_min_dist'][1]}), continuous {m['sep_min_continuous'][0]:.2f} "
             f"({m['sep_min_continuous'][1]}); near-encounters {m['near_encounters']} ticks; F1 classes {m['f1']}; "
             f"holds {m['holds']} ({m['hold_ticks']} ticks).", "", "## Declared properties", ""]
    lines += [f"- **{p['name']}**: {'holds' if p['holds'] else 'DOES NOT HOLD'}. {p['detail']}"
              for p in r["properties"]] or ["None declared."]
    lines += ["", "## Detectors", "", f"- TODO-134 (a decision on a fallback stand whose first robot tick violates): "
              f"{r['detectors']['todo134'] or 'none'}", f"- The arrival-tick ray: "
              f"{r['detectors']['arrival_tick_rays'] or 'none'}"]
    for k in ("retention_observation_warrant", "todo132a", "x5_ground1") + tuple(r.get("extra_measures", ())):
        if k in m:
            lines += ["", f"## {k}", "", f"{m[k]}"]
    lines += ["", "## Decisions", "", "| tick | trigger | cause | gate | leader | projection | winner | hold |",
              "|---|---|---|---|---|---|---|---|"]
    lines += [f"| {x['tick']} | {x['trigger']} | {x['cause'] or ''} | {x['gate']} | {x['leader']} | {x['projection']} | "
              f"{x['winner']} | {x['hold']} |" for x in r["decisions"]]
    return "\n".join(lines) + "\n"


def main(evaluate):
    """properties.py <scenario> <dir> <run.log> <run file>: writes properties.json and properties.md in <dir>."""
    sid, d, log_path, run_file = sys.argv[1], Path(sys.argv[2]), sys.argv[3], sys.argv[4]
    r = evaluate(sid, d, log_path, run_file)
    json.dump(r, open(d / "properties.json", "w"), indent=1)
    (d / "properties.md").write_text(markdown(r))
    held = [f"{p['name']}={'yes' if p['holds'] else 'NO'}" for p in r["properties"]]
    print(f"{sid} ({r['strategy']}): properties {held or 'none'}; detectors {r['detectors']}")
