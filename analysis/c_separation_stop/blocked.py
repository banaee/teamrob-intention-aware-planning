#!/usr/bin/env python3
"""
blocked.py — blocked time and human-borne proximity as outcomes, from the logs alone (R2).

Usage (repo root):
    python analysis/c_separation_stop/blocked.py [dir ...] > analysis/c_separation_stop/blocked.md

Reads every <dir>/<cond>.log (default: stop_off/ and stop_on/, the C runs) and reports per run:
  - BLOCKED TIME, from the executor's [stop] lines: total blocked ticks, the episodes (contiguous
    ticks), and per episode the action and the place it was walking to. Completion is reported only
    when the run completes ([meta] ... all tasks complete); otherwise the run is "blocked by an
    occupying human" when its last stop episode runs to the step cap (with the blocked duration), or
    "not completed within the cap" when it does not.
  - HUMAN-BORNE PROXIMITY: ticks on which the robot did not move (the F1 evaluation's "stand" label)
    and the tick-sampled distance is below min_separation, split by what the robot was doing — a
    separation stop, a decided hold, its own stationary action (grasp / release / wait), or standing
    idle after its last task ("done"). Reported next to the ROBOT VIOLATIONS of the F1 rule on Mesa's
    sequential motion (evaluate.py's acceptance check), so that the two sides of one close moment are
    on one line: what the robot did, what the human did.
  - FOR D2: stops per blocked place (ticks and episodes), and the robot's walks — a walk is a maximal
    run of ticks executing one move_to — with how many contain a stop and how many END in one (the
    walk never resumed before the cap).
Only the line formats of run_mesa.py / meta_planner.py / executor.py are read; no simulator import.
"""
import re, sys, math
from pathlib import Path

HERE = Path(__file__).parent
SEP = 50.0
TOL = 0.05
DIRS = [Path(a) for a in sys.argv[1:]] or [HERE / "stop_off", HERE / "stop_on"]

def num(x): return None if x in (None, "None") else float(x)

def parse(path):
    step = None
    stops, sep, rpos, hpos, ract, rtask, holds, done, steps = [], {}, {}, {}, {}, {}, [], None, 0
    for l in open(path, errors="replace"):
        l = l.rstrip("\n")
        m = re.match(r"\[meta\] step=(\d+) all tasks complete", l)
        if m: done = int(m[1]); continue
        if l.startswith("[stop]"):
            d = dict(re.findall(r"(\w+)=(\S+)", l))
            m = re.search(r"action=(\w+)\(([^)]*)\)", l)
            d["step"] = int(d["step"]); d["action"] = m[1]
            args = m[2].split(",")
            d["place"] = args[-1] if len(args) > 1 else m[2]
            stops.append(d); continue
        m = re.match(r"\[hold\] step=(\d+) \S+ start planned=(\d+)", l)
        if m: holds.append([int(m[1]), None]); continue
        m = re.match(r"\[hold\] step=(\d+) \S+ end planned=\d+ executed=(\d+)", l)
        if m and holds and holds[-1][1] is None: holds[-1][1] = int(m[2]); continue
        m = re.match(r"\[sep\] step=(\d+) \S+ dist=(\S+)(?: min=(\S+))?", l)
        if m: sep[int(m[1])] = (float(m[2]), num(m[3])); steps = max(steps, int(m[1]) + 1); continue
        m = re.match(r"\s*step: (\d+): \[robot_\d+\] task=(\S+) action=(\S+) micro=\S+ pos=\[\s*(\S+)\s+(\S+)\s*\]", l)
        if m:
            k = int(m[1]); rtask[k] = m[2]; ract[k] = m[3]
            rpos[k] = (float(m[4]), float(m[5])); continue
        m = re.match(r"\s*step: (\d+): \[human_\d+\] .*pos=\[\s*(\S+)\s+(\S+)\s*\]", l)
        if m: hpos[int(m[1])] = (float(m[2]), float(m[3])); continue
    hold_ticks = set()
    for start, executed in holds:
        hold_ticks.update(range(start, start + (executed if executed is not None else 0)))
    return dict(stops=stops, sep=sep, rpos=rpos, hpos=hpos, ract=ract, rtask=rtask,
                hold_ticks=hold_ticks, done=done, steps=steps)

def episodes(ticks):
    eps, cur = [], []
    for k in ticks:
        if cur and k == cur[-1] + 1: cur.append(k)
        else:
            if cur: eps.append(cur)
            cur = [k]
    if cur: eps.append(cur)
    return eps

def sequential_violations(run):
    """evaluate.py's acceptance check: ticks on which the robot moved and its step broke the F1 rule."""
    out = []
    for k in sorted(run["rpos"]):
        if k - 1 not in run["rpos"] or k not in run["hpos"]: continue
        r0, r1, h = run["rpos"][k - 1], run["rpos"][k], run["hpos"][k]
        ex, ey = r1[0] - r0[0], r1[1] - r0[1]
        ee = ex * ex + ey * ey
        if ee == 0.0: continue
        dx, dy = r0[0] - h[0], r0[1] - h[1]
        t = -(dx * ex + dy * ey) / ee
        if t <= 0.0: continue
        t = min(1.0, t)
        if math.hypot(dx + t * ex, dy + t * ey) < SEP - TOL: out.append(k)
    return out

def stand_within(run):
    """Ticks on which the robot did not move and the sampled distance is below SEP, by what it was doing."""
    stop_ticks = {d["step"] for d in run["stops"]}
    out = {"stop": [], "hold": [], "own_action": [], "done": []}
    for k in sorted(run["sep"]):
        if k - 1 not in run["rpos"] or k not in run["rpos"]: continue
        if run["rpos"][k] != run["rpos"][k - 1] or run["sep"][k][0] >= SEP: continue
        if k in stop_ticks: out["stop"].append(k)
        elif k in run["hold_ticks"]: out["hold"].append(k)
        elif run["done"] is not None and k >= run["done"]: out["done"].append(k)
        else: out["own_action"].append(k)
    return out

def walks(run):
    """Maximal runs of ticks executing one move_to (the robot's own task in flight)."""
    ticks = [k for k in sorted(run["ract"]) if run["ract"][k] == "move_to" and run["rtask"][k] != "None"]
    return episodes(ticks)

def fmt_eps(eps): return "; ".join(f"{e[0]}–{e[-1]} ({len(e)})" for e in eps) or "none"

runs = {d.name: {p.stem: parse(p) for p in sorted(d.glob("*.log"))} for d in DIRS}

print("# Blocked time and human-borne proximity (R2)\n")
print(f"Generated by `blocked.py` over {', '.join(d.name for d in DIRS)}. min_separation {SEP:g} cm; "
      "PYTHONHASHSEED=0. Blocked ticks are the executor's [stop] refusals; \"stand < s\" ticks are those on "
      "which the robot did not move and the sampled distance was below min_separation (the human's side of "
      "a close moment: a separation stop, a decided hold, the robot's own grasp / release / wait, or standing "
      "idle after its last task); robot violations are evaluate.py's acceptance count (the F1 rule on the "
      "robot's own steps, sequential motion).\n")

for dname, conds in runs.items():
    print(f"## {dname}\n")
    print("| run | outcome | blocked ticks | stop episodes (place) | robot violations | stand < s: stop / hold / own action / done | walks | with a stop | ending in a stop |")
    print("|---|---|---|---|---|---|---|---|---|")
    for c, run in conds.items():
        st = run["stops"]; ticks = [d["step"] for d in st]; eps = episodes(ticks)
        by_tick = {d["step"]: d for d in st}
        last = run["steps"] - 1
        if run["done"] is not None:
            outcome = f"completed at {run['done']}"
        elif eps and eps[-1][-1] == last:
            e = eps[-1]; d = by_tick[e[0]]
            outcome = f"blocked by an occupying human: {d['action']} to {d['place']} refused {len(e)} ticks ({e[0]}–{last})"
        else:
            outcome = f"not completed within {run['steps']}"
        ep_s = "; ".join(f"{e[0]}–{e[-1]} ({len(e)}, {by_tick[e[0]]['action']}→{by_tick[e[0]]['place']})" for e in eps) or "none"
        sw = stand_within(run)
        ws = walks(run)
        stop_set = set(ticks)
        with_stop = sum(1 for w in ws if stop_set & set(w))
        end_stop = sum(1 for w in ws if w[-1] in stop_set)
        viol = sequential_violations(run)
        print(f"| {c} | {outcome} | {len(ticks)} | {ep_s} | {len(viol)}"
              + (f" ({', '.join(map(str, viol))})" if viol else "")
              + f" | {len(sw['stop'])} / {len(sw['hold'])} / {len(sw['own_action'])} / {len(sw['done'])} | {len(ws)} | {with_stop} | {end_stop} |")
    print()
    # Per-place table for D2.
    places = {}
    for c, run in conds.items():
        for e in episodes([d["step"] for d in run["stops"]]):
            d = next(x for x in run["stops"] if x["step"] == e[0])
            key = (c, d["place"])
            places.setdefault(key, [0, 0]); places[key][0] += len(e); places[key][1] += 1
    if places:
        print("Stops per blocked place (ticks, episodes):\n")
        print("| run | place | blocked ticks | episodes |")
        print("|---|---|---|---|")
        for (c, place), (t, n) in sorted(places.items()):
            print(f"| {c} | {place} | {t} | {n} |")
        print()
    # Detail of the stand-within ticks, so the human-borne moments are locatable.
    print("Stand < s ticks (episodes):\n")
    for c, run in conds.items():
        sw = stand_within(run)
        parts = [f"{k} {fmt_eps(episodes(v))}" for k, v in sw.items() if v]
        print(f"- {c}: " + ("; ".join(parts) if parts else "none"))
    print()
