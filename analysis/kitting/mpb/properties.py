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
- scenario_s10_03 (single_task; relabelled in part (iv): D2's retention by identity through a deviation, until its
  retraction, T-D L2 (ii); AD3 is not exercisable in the MPB set, design_decisions.md, "T-D G", AD3): P3a, no decision
  between the cut into the carry and the retraction; P3b, the decision record keeps deliver_item(item_1) on every tick of
  that interval (so the admitted projection is unchanged: admission is asked on a fired trigger only); P3c, the leader
  is deliver_item(item_1), an assigned task (commitment warrant), on every tick of it. The delivery's observation
  warrant over the interval is measured and reported (entry-warranted: it persists).
- scenario_s11_01: P6.1, the winner switches to deliver_item(item_9) at a projection_expired decision, before the
  robot's first grasp of item_8, while the human stands where it started; P6.2 (single_task: the candidates' holds are
  logged), at that decision item_8's hold exceeds the layout's cost difference, and at every earlier decision it does
  not (the switch at the FIRST expiry whose hold exceeds it; T-D X, X1; the fallback stand ends at 1 + k, so the hold is
  at most k + 1).
- scenario_s10_06: P8a, no hold at any decision; P8b, the completion equals the reference run's; P8c, the robot's
  per-tick positions equal the reference run's.
- scenario_s11_02: evidence for TODO-132 (a), no property: the decisions on the stand, their holds, the tick the
  stand's persistence broke and the end of the projection the last of them rested on.
- scenario_s10_09 (part (iv)): X5's ground (1), measured, not a mechanism (design_decisions.md, "T-D X", X5): per
  stretch of ticks on which the adequacy finding is unexplained, the decisions inside it whose admission refused, and the
  first tick on which the finding is still unexplained after such a decision (the finding has outlived a re-decision).
Part (v) (analysis/mpb/coverage.md, the five claimed cells; authoring.md, part (v)):
- scenario_s12_01 (row D8): P12.1a, the decisions before the one admitting deliver_item(item_1) (entered) all select
  item_7; that decision selects item_13 with hold 0, before item_7 is grasped (the switch caused by the admitted
  projection); P12.1b (single_task), at that decision item_7's hold exceeds the layout's plain-cost difference of item_13
  over item_7 (2.5 ticks, the authored parameter) and at every earlier decision it does not, the difference positive.
- scenario_s12_02 (row C2): P12.2a, at the decision admitting coffee_break (entered) the robot's task carries a positive
  hold; P12.2b, the robot comes within min_separation of the human's waiting point (the wait_at position) only after the
  human has left it (the tick after the wait's last); P12.2c, no F1 robot violation within that decision's assessed
  window. The hold after the coffee break's boundary (a fallback stand) is TODO-132 (a)'s, recorded, not a property.
- scenario_s11_03 (row D9): P11.3a, the winner switches to deliver_item(item_9) at a projection_expired decision while
  the robot carries item_8 (grasped before it), every earlier decision selecting item_8; P11.3b, item_8 is released at
  shelf_3 (within the arrival radius) before item_9 is grasped; P11.3c (single_task), at that decision item_8's hold
  exceeds the return difference and at every earlier decision while carrying it does not. The return difference
  (X1, deliver_with_return), from the robot's position p: the path lengths, each walk ending the arrival radius short,
  of p -> shelf_3, -> shelf_6, -> kitting_table_4 against p -> kitting_table_2, at the body's speed, plus the priced
  stationary ticks the switch adds (T-D R and E, E9: 2 per pick_up and per place, 1 per walk entered from a completion:
  the return place 2, the walk to shelf_6 1, the grasp 2, the carry 1, the place 2, against the continued place 2: 6).
- scenario_s10_10 (row E6): P10.10, from the decision admitting deliver_item(item_1) (entered) to the tick before the
  next decision, the decision record is deliver_item(item_1) on every tick and no decision falls; on at least one of
  those ticks item_1 leads with its share below theta (the gate none(below_theta)), and on every such tick it is
  adequate (D2's retention by identity, no inadequacy and no trigger in the dip).
- scenario_s10_11 (row A4): no property; the cause boundary is part 1, compared exactly.
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT), str(ROOT / "analysis" / "instruments" / "common"),
                 str(ROOT / "analysis" / "instruments" / "mpb")]

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
            out["measures"]["retention_observation_warrant"] = [(k["tick"], k["observation_warrant"].get(key)) for k in span]
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
    if sid == "scenario_s10_09":
        out["measures"]["x5_ground1"] = [s_ for s_ in x5_ground1([t for t in ticks if t["tick"] < obs["horizon"]],
                                                                decisions) if s_["refused_decisions"]]
    if sid == "scenario_s12_01":
        adm = next((x for x in decisions if x.cause is not None and x.cause.value == "entered" and x.admitted
                    and item_of(x.admitted.key) == "item_1"), None)
        if adm is None:
            prop("P12.1a", False, "no entered decision admitting deliver_item(item_1)")
        else:
            grasp7 = next((a["tick"] for a in agents if a["carrying"] == "item_7"), None)
            before = [x for x in decisions if x.tick < adm.tick]
            s_ = sel_by[adm.tick]
            prop("P12.1a", all(item_of(sel_by[x.tick]["winner"]) == "item_7" for x in before)
                 and item_of(s_["winner"]) == "item_13" and s_["hold"] == 0 and (grasp7 is None or grasp7 > adm.tick),
                 f"winners before {adm.tick}: {sorted(set(item_of(sel_by[x.tick]['winner']) for x in before))}; at "
                 f"{adm.tick}: {s_['winner']}, hold {s_['hold']}; first grasp of item_7: {grasp7}")
            if obs["strategy"] == "single_task":
                robot_start = next(a for a in domain_config["scenarios"][sid].agents
                                   if a.agent_type == "robot").start_position
                rows = []
                for x in before + [adm]:
                    p = position_before(agents, x.tick, robot_start)
                    dc = plain_difference(p, "item_7", "item_13", traj)
                    h7 = next(c["delta"] for c in sel_by[x.tick]["candidates"] if item_of(c["task"]) == "item_7")
                    rows.append((x.tick, round(dc, 3), h7))
                prop("P12.1b", rows[-1][2] > rows[-1][1] and all(0 < dc and h <= dc for _, dc, h in rows[:-1]),
                     f"(tick, the layout's cost difference, item_7's hold): {rows}")
    if sid == "scenario_s12_02":
        adm = next((x for x in decisions if x.cause is not None and x.cause.value == "entered" and x.admitted
                    and x.admitted.key.startswith("coffee_break")), None)
        if adm is None:
            prop("P12.2a", False, "no entered decision admitting coffee_break")
        else:
            s_ = sel_by[adm.tick]
            prop("P12.2a", s_["hold"] and s_["hold"] > 0, f"tick {adm.tick}: winner {s_['winner']}, hold {s_['hold']}")
            waits = [r for r in traj["rows"] if r["action"] == "wait_at"]
            wp, left = (waits[0]["x"], waits[0]["y"]), waits[-1]["tick"] + 1
            near = [a["tick"] for a in agents if math.dist(tuple(a["robot"]), wp) < sep]
            prop("P12.2b", bool(near) and near[0] >= left,
                 f"waiting point ({wp[0]:.1f}, {wp[1]:.1f}), the human there {waits[0]['tick']} to {waits[-1]['tick']}; "
                 f"the robot within {sep:g} cm of it on ticks {near[:1]} to {near[-1:]}")
            end = adm.tick + math.ceil(s_["horizon"]) if s_["horizon"] is not None else adm.tick
            viol = [k for k in range(adm.tick + 1, end + 1)
                    if k in run["sep"] and run["sep"][k][1] is not None and run["sep"][k][1] < sep
                    and rule(run, k, sep) == "viol"]
            prop("P12.2c", not viol, f"assessed window ticks {adm.tick + 1} to {end} (T_h {s_['horizon']}); "
                                     f"F1 violations {viol}")
    if sid == "scenario_s11_03":
        grasp8 = next((a["tick"] for a in agents if a["carrying"] == "item_8"), None)
        sw = next((x for x in decisions if item_of(sel_by[x.tick]["winner"]) == "item_9"), None)
        before = [x for x in decisions if sw is None or x.tick < sw.tick]
        carrying = sw is not None and sw.tick > 0 and agents[sw.tick - 1]["carrying"] == "item_8"
        prop("P11.3a", sw is not None and sw.trigger is Trigger.PROJECTION_EXPIRED and carrying
             and grasp8 is not None and grasp8 < sw.tick
             and all(item_of(sel_by[x.tick]["winner"]) == "item_8" for x in before),
             "no switch" if sw is None else f"switch at {sw.tick} ({sw.trigger.value}); first grasp of item_8 "
             f"{grasp8}; carrying item_8 on the tick before: {carrying}")
        rel8 = next((a for a in agents if sw is not None and a["tick"] >= sw.tick and a["micro"] == "release"
                     and agents[a["tick"] - 1]["carrying"] == "item_8"), None)
        grasp9 = next((a["tick"] for a in agents if a["carrying"] == "item_9"), None)
        shelf3 = traj["fixed"]["shelf_3"]
        prop("P11.3b", rel8 is not None and grasp9 is not None and rel8["tick"] < grasp9
             and math.dist(tuple(rel8["robot"]), tuple(shelf3)) <= traj["params"]["proximity"] + 1e-9,
             "no release of item_8 after the switch" if rel8 is None else
             f"item_8 released at {rel8['tick']}, {math.dist(tuple(rel8['robot']), tuple(shelf3)):.1f} cm from "
             f"shelf_3; first grasp of item_9 {grasp9}")
        if obs["strategy"] == "single_task" and sw is not None:
            r, v, fixed = traj["params"]["proximity"], traj["params"]["speed"], traj["fixed"]
            def walks(p, targets):
                total, at = 0.0, tuple(p)
                for tgt in targets:
                    d = math.dist(at, fixed[tgt])
                    total += max(0.0, d - r)
                    at = arrival(at, fixed[tgt], r)
                return total
            robot_start = next(a for a in domain_config["scenarios"][sid].agents
                               if a.agent_type == "robot").start_position
            rows = []
            for x in before + [sw]:
                if x.tick == 0 or agents[x.tick - 1]["carrying"] != "item_8":
                    continue
                p = position_before(agents, x.tick, robot_start)
                dr = (walks(p, ["shelf_3", "shelf_6", "kitting_table_4"]) - walks(p, ["kitting_table_2"])) / v + 6
                h8 = next(c["delta"] for c in sel_by[x.tick]["candidates"] if item_of(c["task"]) == "item_8")
                rows.append((x.tick, round(dr, 3), h8))
            prop("P11.3c", bool(rows) and rows[-1][0] == sw.tick and rows[-1][2] > rows[-1][1]
                 and all(h <= dr for _, dr, h in rows[:-1]),
                 f"(tick, the return difference, item_8's hold), decisions while carrying: {rows}")
    if sid == "scenario_s10_10":
        adm = next((x for x in decisions if x.cause is not None and x.cause.value == "entered" and x.admitted
                    and item_of(x.admitted.key) == "item_1"), None)
        if adm is None:
            prop("P10.10", False, "no entered decision admitting deliver_item(item_1)")
        else:
            key = "deliver_item(?item=item_1)"
            nxt = next((x.tick for x in decisions if x.tick > adm.tick), obs["horizon"])
            span = [k for k in ticks if adm.tick < k["tick"] < nxt]
            dip = [k for k in span if k["leader"] == key and k["gate"] == "none(below_theta)"]
            prop("P10.10", bool(dip) and all(k["record"] == key for k in span)
                 and all(k["adequacy"].get(key) == "adequate" for k in dip),
                 f"admitted at {adm.tick}, next decision {nxt}; records {sorted(set(str(k['record']) for k in span))}; "
                 f"dip ticks {[k['tick'] for k in dip]}, item_1's adequacy there "
                 f"{sorted(set(k['adequacy'].get(key) for k in dip))}")
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
    for k in ("retention_observation_warrant", "todo132a", "x5_ground1"):
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
