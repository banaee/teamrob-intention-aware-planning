#!/usr/bin/env python3
"""
properties.py — the meta-planner test-bed's part 4 (MPB-1, MPB-3): the properties a scenario declares, as booleans over
the logged robot state, and the measures reported for every run. The planner's logged decision values (the winner, its
hold, the candidates' [meta-cand] delta) are observed inputs to a property, never an input to a derivation of what
should hold. The instrument's own computations are F1's classes over the executed positions (analysis/tb1a_destination/
sep_classes.py, F1's execution rule) and the layout's path lengths; never a hold.

    properties.py <scenario> <dir> <run.log> <run file>

Writes properties.json and properties.md in <dir>.

For every run:
- completion (the world tick after the robot's last release on a task), holds, near-encounters and F1's classes;
- the decisions with their trigger, cause, gate, projection, winner and hold;
- two detectors, recorded and classified by hand:
  - TODO-134: a decision resting on a fallback stand whose first executed robot tick is an F1 violation;
  - the arrival-tick ray (the plan's objection 1; Hadi, point 5): a decision resting on a moving fallback whose ray
    starts inside a fixed object's arrival radius the human entered on that tick (the skip rule lets the ray run
    through the object). Class 3 under MPB-4 when it occurs.

The declared properties (the scenarios' descriptions; analysis/mpb/authoring.md):
- scenario_s10_02: P2a, at the decision admitting deliver_item(item_1) through recognition_changed with cause entered,
  the robot's task carries a positive hold; P2b, no F1 robot violation within that decision's assessed window.
- scenario_s10_03 (Hadi's addition, AD3; its "observation warrant lost from the cut" clause pending, see REPORT.md):
  P3a, no decision between the cut into the carry and the retraction; P3b, the decision record keeps
  deliver_item(item_1) on every tick of that interval (so the admitted projection is unchanged: admission is asked on a
  fired trigger only); P3c, the leader is deliver_item(item_1), an assigned task (commitment warrant), on every tick of
  it. The delivery's observation warrant over the interval is measured and reported.
- scenario_s11_01: P6.1, the winner switches to deliver_item(item_9) at a projection_expired decision, before the
  robot's first grasp of item_8, while the human stands where it started; P6.2 (single_task: the candidates' holds are
  logged), at that decision item_8's hold exceeds the layout's cost difference, and at every earlier decision it does
  not (the switch at the FIRST expiry whose hold exceeds it; T-D X, X1; the fallback stand ends at 1 + k, so the hold is
  at most k + 1).
- scenario_s10_06: P8a, no hold at any decision; P8b, the completion equals the reference run's; P8c, the robot's
  per-tick positions equal the reference run's.
- scenario_s11_02: evidence for TODO-132 (a), no property: the decisions on the stand, their holds, the tick the
  stand's persistence broke and the end of the projection the last of them rested on.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(HERE), str(ROOT), str(ROOT / "analysis"), str(ROOT / "analysis" / "tb1a_destination")]

import yaml
import logparse
from domains.kitting.registry import domain_config
from sep_classes import rule, summary
from mpblib import Mode, Room, Trigger, load_decisions, skipped_objects


def room_of(run_file, traj):
    cfg = yaml.safe_load(open(run_file))
    sc = domain_config["scenarios"][cfg["scenario"]]
    layout = json.load(open(ROOT / domain_config["layouts"][cfg.get("layout") or sc.reference_layouts[0]]))
    w, h = layout["space"]["width"], layout["space"]["height"]
    return Room(-w / 2, w / 2, -h / 2, h / 2, {o["id"]: tuple(o["position"]) for o in layout["env_objects"]},
                traj["params"]["proximity"])


def item_of(key):
    return None if key is None else key.split("?item=")[1].split(",")[0].split(")")[0]


def completion(agents):
    releases = [a["tick"] for a in agents if a["micro"] == "release" and a["task"] is not None]
    return releases[-1] + 1 if releases else None


def position_before(agents, t, start):
    """The robot's position at a decision on tick t: where it stood before its tick-t move."""
    return tuple(start) if t == 0 else tuple(agents[t - 1]["robot"])


def arrival(frm, to, radius):
    d = math.dist(frm, to)
    return tuple(frm) if d <= radius else (to[0] - (to[0] - frm[0]) * radius / d, to[1] - (to[1] - frm[1]) * radius / d)


def plain_difference(p, a, b, traj):
    """The layout's plain-cost difference, in ticks, of delivering item b rather than item a from p with an empty hand:
    the path lengths (to the shelf, the arrival radius short, then to the table) at the body's speed. The stationary
    structure of the two deliveries is the same (deliver_default), so it cancels."""
    r, v = traj["params"]["proximity"], traj["params"]["speed"]
    fixed = traj["fixed"]
    def path(item):
        shelf, table = fixed[traj["home"][item]], fixed[traj["dest"][item]]
        return math.dist(p, shelf) + math.dist(arrival(p, shelf, r), table)
    return (path(b) - path(a)) / v


def evaluate(sid, d, log_path, run_file):
    obs = json.load(open(d / "observed.json"))
    sel = json.load(open(d / "selection.json"))
    agents = json.load(open(d / "robot.json"))
    ticks = json.load(open(d / "actual_ticks.json"))
    traj = json.load(open(d / "trajectory.json"))
    decisions = load_decisions(d / "actual_decisions.json")
    run = logparse.parse(log_path)
    sep = float(run["hdr"].get("min_separation", 50.0))
    sel_by = {s["tick"]: s for s in sel}
    rm = room_of(run_file, traj)
    human_rows = {r["tick"]: r for r in traj["rows"]}
    out = dict(scenario=sid, strategy=obs["strategy"], prior=obs["prior"], completion=completion(agents),
               terminal=obs["terminal"], horizon=obs["horizon"], properties=[], measures={}, detectors={})
    s = summary(log_path)
    out["measures"] = dict(sep_min_dist=s["dist"], sep_min_continuous=s["cont"], f1=s["counts"],
                           near_encounters=sum(1 for _, (_, m) in run["sep"].items() if m is not None and m < sep),
                           holds=[(x["tick"], x["hold"]) for x in sel if x["hold"]],
                           hold_ticks=sum(x["hold"] or 0 for x in sel))
    out["decisions"] = [dict(tick=x.tick, trigger=x.trigger.value, cause=x.cause and x.cause.value, gate=x.gate.value,
                             leader=x.leader, projection=("admitted " + x.admitted.key) if x.admitted else
                             (f"fallback {x.fallback.mode.value} k={x.fallback.k} end={x.fallback.end:.2f}"
                              if x.fallback else "none"),
                             winner=sel_by[x.tick]["winner"], hold=sel_by[x.tick]["hold"]) for x in decisions]
    # the detectors
    todo134, rays = [], []
    for x in decisions:
        if x.fallback is not None and x.fallback.mode is Mode.STANDING and rule(run, x.tick, sep) == "viol":
            todo134.append(x.tick)
        if x.fallback is not None and x.fallback.mode is Mode.MOVING:
            pos, prev = human_rows[x.tick], human_rows[x.tick - 1]
            now = skipped_objects((pos["x"], pos["y"]), rm)
            before = skipped_objects((prev["x"], prev["y"]), rm)
            entered = [o for o in now if o not in before]
            if entered:
                rays.append(dict(tick=x.tick, objects=entered, k=x.fallback.k, duration=x.fallback.duration,
                                 end=x.fallback.end))
    out["detectors"] = dict(todo134=todo134, arrival_tick_rays=rays)

    def prop(name, holds, detail):
        out["properties"].append(dict(name=name, holds=bool(holds), detail=detail))

    if sid == "scenario_s10_02":
        adm = next((x for x in decisions if x.trigger is Trigger.RECOGNITION_CHANGED and x.cause is not None
                    and x.cause.value == "entered" and x.admitted and item_of(x.admitted.key) == "item_1"), None)
        if adm is None:
            prop("P2a", False, "no entered decision admitting deliver_item(item_1)")
        else:
            s_ = sel_by[adm.tick]
            prop("P2a", s_["hold"] and s_["hold"] > 0, f"tick {adm.tick}: winner {s_['winner']}, hold {s_['hold']}")
            end = adm.tick + math.ceil(s_["horizon"]) if s_["horizon"] is not None else adm.tick
            viol = [k for k in range(adm.tick + 1, end + 1)
                    if k in run["sep"] and run["sep"][k][1] is not None and run["sep"][k][1] < sep
                    and rule(run, k, sep) == "viol"]
            prop("P2b", not viol, f"assessed window ticks {adm.tick + 1} to {end} (T_h {s_['horizon']}); "
                                  f"F1 violations {viol}")
    if sid == "scenario_s10_03":
        t_cut = next(a["tick"] for a in traj["actions"] if a["task"].startswith("coffee_break"))
        t_r = next((x.tick for x in decisions if x.cause is not None and x.cause.value == "retraction"), None)
        if t_r is None:
            prop("P3a", False, "no retraction")
        else:
            key = "deliver_item(?item=item_1)"
            span = [k for k in ticks if t_cut <= k["tick"] < t_r]
            prop("P3a", not [x.tick for x in decisions if t_cut <= x.tick < t_r],
                 f"interval {t_cut} to {t_r - 1}: decisions {[x.tick for x in decisions if t_cut <= x.tick < t_r]}")
            prop("P3b", all(k["record"] == key for k in span), f"record on the interval: "
                 f"{sorted(set(str(k['record']) for k in span))}")
            human = next(a for a in domain_config["scenarios"][sid].agents if a.agent_type == "human")
            assigned = {c.value for t in human.assigned_tasks for v, c in t.bindings.items() if v.name == "?item"}
            prop("P3c", all(k["leader"] == key for k in span) and "item_1" in assigned,
                 f"leaders on the interval: {sorted(set(str(k['leader']) for k in span))}; item_1 assigned")
            out["measures"]["ad3_observation_warrant"] = [(k["tick"], k["observation_warrant"].get(key)) for k in span]
    if sid == "scenario_s11_01":
        start = traj["rows"][0]
        standing = lambda t: (human_rows[t]["x"], human_rows[t]["y"]) == (start["x"], start["y"])
        grasp8 = next((a["tick"] for a in agents if a["carrying"] == "item_8"), None)
        sw = next((x for x in decisions if item_of(sel_by[x.tick]["winner"]) == "item_9"), None)
        before = [x for x in decisions if sw is None or x.tick < sw.tick]
        prop("P6.1", sw is not None and sw.trigger is Trigger.PROJECTION_EXPIRED
             and (grasp8 is None or sw.tick < grasp8) and standing(sw.tick)
             and all(item_of(sel_by[x.tick]["winner"]) == "item_8" for x in before),
             "no switch" if sw is None else f"switch at {sw.tick} ({sw.trigger.value}); first grasp of item_8: "
             f"{grasp8}; the human standing: {standing(sw.tick)}")
        if obs["strategy"] == "single_task" and sw is not None:
            rs = json.load(open(d / "robot.json"))
            robot_start = next(a for a in domain_config["scenarios"][sid].agents
                               if a.agent_type == "robot").start_position
            rows = []
            for x in before + [sw]:
                p = position_before(rs, x.tick, robot_start)
                dc = plain_difference(p, "item_8", "item_9", traj)
                h8 = next(c["delta"] for c in sel_by[x.tick]["candidates"] if item_of(c["task"]) == "item_8")
                rows.append((x.tick, round(dc, 3), h8))
            ok = rows[-1][2] > rows[-1][1] and all(h <= dc for _, dc, h in rows[:-1])
            prop("P6.2", ok, f"(tick, the layout's cost difference, item_8's hold): {rows}")
    if sid == "scenario_s10_06":
        ref = json.load(open(d / "reference.json"))
        prop("P8a", all(not x["hold"] for x in sel) and all(c["delta"] == 0 for x in sel for c in x["candidates"]),
             f"holds {[(x['tick'], x['hold']) for x in sel if x['hold']]}")
        prop("P8b", out["completion"] == ref["completion"],
             f"completion {out['completion']}, the reference's {ref['completion']}")
        diff = [a["tick"] for a, r in zip(agents, ref["ticks"]) if tuple(a["robot"]) != (r["x"], r["y"])]
        prop("P8c", not diff, f"ticks where the robot's positions differ: {diff[:10]}")
    if sid == "scenario_s11_02":
        stand = next(a["tick"] for a in traj["actions"] if a["action"] == "stand")
        rows = traj["rows"]
        brk = next(r["tick"] for p, r in zip(rows[:-1], rows[1:])
                   if r["tick"] > stand and (r["x"], r["y"]) != (p["x"], p["y"]))
        on = [x for x in decisions if stand <= x.tick < brk]
        out["measures"]["todo132a"] = dict(
            stand_first_tick=stand, persistence_broke=brk,
            decisions=[(x.tick, x.trigger.value, None if x.fallback is None else x.fallback.k,
                        None if x.fallback is None else round(x.fallback.end, 2), sel_by[x.tick]["hold"]) for x in on],
            last_projection_end=None if not on or on[-1].fallback is None else on[-1].fallback.end,
            holds_past_break=[(x.tick, sel_by[x.tick]["hold"]) for x in decisions
                              if sel_by[x.tick]["hold"] and x.tick + sel_by[x.tick]["hold"] > brk and x.tick < brk])
    return out


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
    for k in ("ad3_observation_warrant", "todo132a"):
        if k in m:
            lines += ["", f"## {k}", "", f"{m[k]}"]
    lines += ["", "## Decisions", "", "| tick | trigger | cause | gate | leader | projection | winner | hold |",
              "|---|---|---|---|---|---|---|---|"]
    lines += [f"| {x['tick']} | {x['trigger']} | {x['cause'] or ''} | {x['gate']} | {x['leader']} | {x['projection']} | "
              f"{x['winner']} | {x['hold']} |" for x in r["decisions"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sid, d, log_path, run_file = sys.argv[1], Path(sys.argv[2]), sys.argv[3], sys.argv[4]
    r = evaluate(sid, d, log_path, run_file)
    json.dump(r, open(d / "properties.json", "w"), indent=1)
    (d / "properties.md").write_text(markdown(r))
    held = [f"{p['name']}={'yes' if p['holds'] else 'NO'}" for p in r["properties"]]
    print(f"{sid} ({r['strategy']}): properties {held or 'none'}; detectors {r['detectors']}")
