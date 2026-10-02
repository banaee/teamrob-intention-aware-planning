#!/usr/bin/env python3
"""
properties.py — dock_loading's part 4 of the MPB (MPB-1, MPB-3; design_decisions.md, "T-G: the second domain's rulings",
THE MPB ON DOCK_LOADING: THE SET, its rulings and DL-P1 to DL-P9): the properties the scenarios declare, as booleans over
the logged robot state, and the measures some of them report. The shared part (the run's outputs read once, the
measures every run reports, the detectors, the markdown) is analysis/instruments/mpb/measures.py. The planner's logged
decision values (the winner, its hold, the candidates' [meta-cand] delta) are observed inputs, never an input to a
derivation of what should hold.

    properties.py <scenario> <dir> <run.log> <run file>

Declared properties (each scenario's description; authoring.md):
- K1, the control (scenario_s08_01, scenario_s09_01; CONTROLS): P1a, no hold at any decision (every decision's hold and
  every candidate's delta 0); P1b, the completion equals the comparison run's; P1c, the robot's position on every tick
  equals the comparison run's (reference.py: the same setup, pool and start, the human removed).
- M1, M2, M4 (scenario_s05_04 to _06, scenario_s07_04 to _06; mixed, kind 2, the script dependent on the robot):
  (i) every robot task completes (the terminal decision, the pool empty, within the cap); (ii) every ordinary entry of
  the script closes (completed, abandoned or infeasible) and the closing part completes (the record's end statement:
  no entry still open); (iii)
  no F1 violation with a moving robot; (iv) each scan of a delivered pallet enters the live set on the tick its
  delivery is first observable, the tick after the robot's release of that pallet (CLAUDE.md, "Regression checking":
  the world fact is first observable on the tick after the release), and not before.
Reported, not declared:
- K3 (DL-P2): whether the switch by cost occurred: a decision whose winner leaves deliver_pallet(pallet_4) while that
  task is not complete and the human stands at the dry bay; per decision on the stand, every candidate's hold.
- K4: TODO-132 (a)'s evidence: the decisions on the stand, their fallback k and end, the holds, the tick the stand's
  persistence broke, the holds that outlast it.
- K9: the admission on the walk to the standby place (the entered decision, its key, the winner and its hold) and the
  retraction, or the no_current_task tick that masks it (DL-P4).
- M2: whether two scans of one bay were live on one tick, and whether a decision fell while the human stood at the bay
  of the winner's delivery (within the arrival radius of it).
"""
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT), str(ROOT / "analysis" / "instruments" / "common"),
                 str(ROOT / "analysis" / "instruments" / "mpb")]

from measures import Part4, main

# The control scenarios: run.sh runs the reference (reference.py) for each (MPB-2, scenario 8; THE SET, K1).
CONTROLS = ("scenario_s08_01", "scenario_s09_01")
K3 = ("scenario_s08_03", "scenario_s09_03")
K4 = ("scenario_s08_04", "scenario_s09_04")
K9 = ("scenario_s08_09", "scenario_s09_09")
MIXED_DEPENDENT = ("scenario_s05_04", "scenario_s05_05", "scenario_s05_06",
                   "scenario_s07_04", "scenario_s07_05", "scenario_s07_06")
M2 = ("scenario_s05_05", "scenario_s07_05")


def pallet_of(key):
    return None if key is None else key.split("?pallet=")[1].split(",")[0].split(")")[0]


def stand_interval(traj):
    """The human's stand: its first tick and the tick the persistence broke (the first move after it)."""
    stand = next(a["tick"] for a in traj["actions"] if a["action"] == "stand")
    rows = traj["rows"]
    brk = next((r["tick"] for p, r in zip(rows[:-1], rows[1:])
                if r["tick"] > stand and (r["x"], r["y"]) != (p["x"], p["y"])), None)
    return stand, brk


def evaluate(sid, d, log_path, run_file):
    p4 = Part4(sid, d, log_path, run_file)
    obs, sel, agents, ticks, traj, decisions = p4.obs, p4.sel, p4.agents, p4.ticks, p4.traj, p4.decisions
    sel_by, out, prop = p4.sel_by, p4.out, p4.prop
    if sid in CONTROLS:
        ref = json.load(open(d / "reference.json"))
        prop("P1a", all(not x["hold"] for x in sel) and all(c["delta"] == 0 for x in sel for c in x["candidates"]),
             f"holds {[(x['tick'], x['hold']) for x in sel if x['hold']]}")
        prop("P1b", out["completion"] == ref["completion"],
             f"completion {out['completion']}, the reference's {ref['completion']}")
        diff = [a["tick"] for a, r in zip(agents, ref["ticks"]) if tuple(a["robot"]) != (r["x"], r["y"])]
        prop("P1c", not diff and len(agents) == len(ref["ticks"]), f"ticks where the robot's positions differ: {diff[:10]}")
    if sid in K3 + K4:
        stand, brk = stand_interval(traj)
        dry = traj["fixed"]["dry_delivery_bay_0"]
        released4 = next((a["tick"] for a in agents if a["micro"] == "release" and a["tick"] > 0
                          and agents[a["tick"] - 1]["carrying"] == "pallet_4"), None)
        on = [x for x in decisions if stand <= x.tick < (brk if brk is not None else obs["horizon"])]
        rows = [dict(tick=x.tick, trigger=x.trigger.value, mode=None if x.fallback is None else x.fallback.mode.value,
                     k=None if x.fallback is None else x.fallback.k,
                     end=None if x.fallback is None else round(x.fallback.end, 2),
                     winner=sel_by[x.tick]["winner"], hold=sel_by[x.tick]["hold"],
                     holds={c["task"]: c["delta"] for c in sel_by[x.tick]["candidates"]}) for x in on]
        out["measures"]["stand"] = dict(stand_first_tick=stand, persistence_broke=brk, pallet_4_released=released4,
                                        human_at=[round(traj["rows"][stand + 1]["x"], 2),
                                                  round(traj["rows"][stand + 1]["y"], 2)],
                                        dry_bay=list(dry), decisions=rows,
                                        holds_past_break=[(x.tick, sel_by[x.tick]["hold"]) for x in decisions
                                                          if brk is not None and sel_by[x.tick]["hold"]
                                                          and x.tick < brk < x.tick + sel_by[x.tick]["hold"]])
        if sid in K3:
            seq = [(x.tick, pallet_of(sel_by[x.tick]["winner"])) for x in decisions]
            switch = next((t for (t0, w0), (t, w) in zip(seq[:-1], seq[1:])
                           if w0 == "pallet_4" and w != "pallet_4" and stand <= t < (brk or obs["horizon"])
                           and (released4 is None or t < released4)), None)
            out["measures"]["k3_switch"] = dict(occurred=switch is not None, tick=switch)
    if sid in K9:
        adm = next((x for x in decisions if x.cause is not None and x.cause.value == "entered" and x.admitted
                    and x.tick >= next(a["tick"] for a in traj["actions"] if a["task"].startswith("go_to"))), None)
        retr = next((x.tick for x in decisions if x.cause is not None and x.cause.value == "retraction"), None)
        inadequate = None
        if adm is not None:
            inadequate = next((t["tick"] for t in ticks if t["tick"] > adm.tick
                               and t["adequacy"].get(adm.admitted.key) == "inadequate"), None)
        masked = inadequate is not None and inadequate in obs["no_current_task"] and retr != inadequate
        out["measures"]["k9"] = dict(
            admission=None if adm is None else dict(tick=adm.tick, key=adm.admitted.key,
                                                   winner=sel_by[adm.tick]["winner"], hold=sel_by[adm.tick]["hold"]),
            recorded_hypothesis_inadequate_from=inadequate, retraction=retr, masked_by_no_current_task=masked)
    if sid in MIXED_DEPENDENT:
        prop("M(i)", obs["terminal"] is not None, f"the terminal decision {obs['terminal']}")
        # the run's end statement of a script that depends on the robot: one [human] line per entry still open,
        # ordinary or closing (world/record.py, StillOpen; run_mesa.py); none when every entry closed
        still = [l.split(" open:", 1)[1].strip() for l in open(log_path) if l.startswith("[human] ") and " open:" in l]
        prop("M(ii)", not still, f"entries still open at the run's end: {still}")
        f1 = out["measures"]["f1"]
        prop("M(iii)", f1["viol"] == 0, f"F1 classes {f1}")
        rows = []
        for a in agents:
            if a["micro"] == "release" and a["tick"] > 0 and agents[a["tick"] - 1]["carrying"] is not None:
                p = agents[a["tick"] - 1]["carrying"]
                key = f"confirm_delivered_pallet(?pallet={p})"
                live = [t["tick"] for t in ticks if key in t["adequacy"]]
                if traj["dest"].get(p, "").endswith("delivery_bay_0"):
                    rows.append((p, a["tick"] + 1, live[0] if live else None))
        prop("M(iv)", all(first == obs_t for _, obs_t, first in rows),
             f"(pallet, the tick its delivery is first observable, the scan's first live tick): {rows}")
    if sid in M2:
        bays = traj["dest"]
        two = [t["tick"] for t in ticks
               if any(sum(1 for k in t["adequacy"] if k.startswith("confirm_delivered_pallet")
                          and bays[pallet_of(k)] == b) >= 2 for b in set(bays.values()))]
        occupied = []
        for x in decisions:
            p = pallet_of(sel_by[x.tick]["winner"])
            if p is None or not sel_by[x.tick]["winner"].startswith("deliver_pallet"):
                continue
            bay = traj["fixed"][bays[p]]
            h = p4.human_rows[x.tick]
            if math.dist((h["x"], h["y"]), bay) <= traj["params"]["proximity"]:
                occupied.append(x.tick)
        out["measures"]["m2"] = dict(two_scans_live_in_one_bay=two[:1] + two[-1:] if two else [],
                                     decisions_at_an_occupied_bay=occupied)
    out["extra_measures"] = ["stand", "k3_switch", "k9", "m2"]
    return out


if __name__ == "__main__":
    main(evaluate)
