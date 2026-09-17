#!/usr/bin/env python3
"""
logparse.py — the run-log parser the analysis scripts share: C's evaluate.py and blocked.py
(analysis/c_separation_stop/), F1's evaluate.py (analysis/f1_robot_responsible/) and T6's metrics.py
(analysis/t6_ablation/). They held copies of one parser; this is the one.

parse(path) reads a headless run log in one pass and returns every field any of those scripts uses;
each script takes what it needs. The measures more than one script computes the same way on a parsed
run (episodes, the decision in effect, the sequential-motion check of the F1 rule) are here too; the
script-specific ones (window labels, outcomes, the stand-within split) stay in the scripts.
Only the line formats of run_mesa.py / sim_agents.py / meta_planner.py / executor.py are read; no
simulator import.

Import from a script one directory below analysis/:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1])); import logparse
"""
import math, re

TOL = 0.05   # positions in the per-tick lines are rounded to 0.01

ITEM = re.compile(r"deliver_item\(\?item=(item_\d+),\?kitting_table=kitting_table_0\)")

def short(s): return ITEM.sub(r"\1", s)
def num(x): return None if x in (None, "None") else float(x)

def parse(path):
    """
    One run log. Returns a dict:
      lines       every line, newline stripped
      hdr         the [run] header's key=value fields (strings)
      decisions   one dict per [meta] decision: step, trigger, winner, source (b3 | b2 | ? | done),
                  selection, hold, T_h, cands (the [meta-cand] fields of a B3 decision, task shortened);
                  the empty-pool line is a decision with trigger / source / selection "done", winner "-"
      declared    the step of the empty-pool line, or None
      pool        the first decision's winner plus its queue (items)
      fires       [meta-trig] fires by trigger (trigger none not counted)
      verdicts    [meta-b2] verdict counts: continue / continue_hold / escalate
      pins        [IR-complete]: item -> first pinned step
      hold_lines  every [hold] line, as logged
      holds       one dict per started hold: start, planned, executed, interrupted (None until its end line)
      hold_ticks  the ticks on which a hold was executing
      stops       one dict per [stop] line: its key=value fields as logged (strings) with step as int,
                  action (the action name), place (its last argument), call (name and arguments as
                  logged), rpos / hpos (robot and human position tuples)
      sep         [sep] step -> (dist, min or None); steps: the last [sep] step + 1
      rpos, hpos  per-tick robot / human position; ract, rtask: the robot's action and task per tick
      releases    the ticks on which the robot's place released
    """
    lines = [l.rstrip("\n") for l in open(path, errors="replace")]
    hdr = {}
    fires, verdicts = {}, {"continue": 0, "continue_hold": 0, "escalate": 0}
    b2 = b3 = None; cands = []
    decisions, pins, hold_lines, holds, stops = [], {}, [], [], []
    sep, rpos, hpos, ract, rtask, releases = {}, {}, {}, {}, {}, []
    declared, steps, pool = None, 0, None
    for l in lines:
        if l.startswith("[run] "):
            hdr = dict(re.findall(r"(\w+)=(\S+)", l)); continue
        m = re.match(r"\[meta-trig\] step=(\d+) trigger=(\S+)", l)
        if m:
            b2 = b3 = None; cands = []
            if m[2] != "none": fires[m[2]] = fires.get(m[2], 0) + 1
            continue
        if l.startswith("[meta-b2]"):
            b2 = dict(re.findall(r"(\w+)=(\S+)", l))
            v = b2.get("verdict")
            if v in verdicts: verdicts[v] += 1
            continue
        if l.startswith("[meta-cand]"):
            d = dict(re.findall(r"(\w+)=(\S+)", l)); d["task"] = short(l.split()[1]); cands.append(d); continue
        if l.startswith("[meta-b3]"):
            b3 = dict(re.findall(r"(\w+)=(\S+)", l)); continue
        m = re.match(r"\[meta\] step=(\d+) trigger=(\S+) winner=\S+\{'\?item': '(item_\d+)'", l)
        if m:
            s, trig, w = int(m[1]), m[2], m[3]
            q = re.search(r"queue=(.*)$", l)
            if pool is None and q: pool = [w] + re.findall(r"item_\d+", q[1])
            if b3 is not None:
                dec = dict(step=s, trigger=trig, winner=w, source="b3", selection=b3["selection"],
                           hold=int(b3["hold"]), T_h=num(b3["T_h"]), cands=cands)
            elif b2 is not None and b2.get("verdict", "").startswith("continue"):
                dec = dict(step=s, trigger=trig, winner=w, source="b2", selection="b2_" + b2["verdict"],
                           hold=int(b2.get("hold", 0)), T_h=num(b2.get("remaining")), cands=[])
            else:
                dec = dict(step=s, trigger=trig, winner=w, source="?", selection="?", hold=0, T_h=None, cands=[])
            decisions.append(dec); continue
        m = re.match(r"\[meta\] step=(\d+) all tasks complete", l)
        if m:
            declared = int(m[1])
            decisions.append(dict(step=declared, trigger="done", winner="-", source="done", selection="done", hold=0, T_h=None, cands=[]))
            continue
        m = re.match(r"\[IR-complete\] step=(\d+) deliver_item\(\?item=(item_\d+),", l)
        if m: pins.setdefault(m[2], int(m[1])); continue
        if l.startswith("[hold]"):
            hold_lines.append(l)
            m = re.match(r"\[hold\] step=(\d+) \S+ start planned=(\d+)", l)
            if m: holds.append(dict(start=int(m[1]), planned=int(m[2]), executed=None, interrupted=None)); continue
            m = re.match(r"\[hold\] step=(\d+) \S+ end planned=\d+ executed=(\d+) interrupted=(\w+)", l)
            if m and holds and holds[-1]["executed"] is None:
                holds[-1]["executed"] = int(m[2]); holds[-1]["interrupted"] = m[3] == "True"
            continue
        if l.startswith("[stop]"):
            d = dict(re.findall(r"(\w+)=(\S+)", l))
            d["step"] = int(d["step"])
            m = re.search(r"action=(\w+)\(([^)]*)\)", l)
            d["action"] = m[1]
            args = m[2].split(",")
            d["place"] = args[-1] if len(args) > 1 else m[2]
            d["call"] = re.search(r"action=(\S+)", l)[1]
            m = re.search(r"pos=\(([-\d.]+), ([-\d.]+)\) human_pos=\(([-\d.]+), ([-\d.]+)\)", l)
            if m: d["rpos"] = (float(m[1]), float(m[2])); d["hpos"] = (float(m[3]), float(m[4]))
            stops.append(d); continue
        m = re.match(r"\[sep\] step=(\d+) \S+ dist=(\S+)(?: min=(\S+))?", l)
        if m: sep[int(m[1])] = (float(m[2]), num(m[3])); steps = max(steps, int(m[1]) + 1); continue
        m = re.match(r"\s*step: (\d+): \[robot_\d+\] task=(\S+) action=(\S+) micro=\S+ pos=\[\s*(\S+)\s+(\S+)\s*\]", l)
        if m:
            k = int(m[1]); rtask[k] = m[2]; ract[k] = m[3]; rpos[k] = (float(m[4]), float(m[5]))
            if m[3] == "place" and "micro=release" in l: releases.append(k)
            continue
        m = re.match(r"\s*step: (\d+): \[human_\d+\] .*pos=\[\s*(\S+)\s+(\S+)\s*\]", l)
        if m: hpos[int(m[1])] = (float(m[2]), float(m[3])); continue
    hold_ticks = set()
    for h in holds:
        hold_ticks.update(range(h["start"], h["start"] + (h["executed"] or 0)))
    return dict(lines=lines, hdr=hdr, decisions=decisions, declared=declared, pool=pool or [], fires=fires,
                verdicts=verdicts, pins=pins, hold_lines=hold_lines, holds=holds, hold_ticks=hold_ticks,
                stops=stops, sep=sep, steps=steps, rpos=rpos, hpos=hpos, ract=ract, rtask=rtask, releases=releases)

# ---- decisions -------------------------------------------------------------------------------------
def fmt_dec(d):
    tag = "" if d["source"] == "done" else f"[{d['selection']}" + (f",hold={d['hold']}" if d["hold"] else "") + "]"
    return f"{d['step']}:{d['trigger']}:{d['winner']}{tag}"

def seq(run): return [(d["step"], d["trigger"], d["winner"]) for d in run["decisions"]]

def in_effect(run, k):
    """The decision in effect on tick k: the last one taken at or before it."""
    d = None
    for x in run["decisions"]:
        if x["step"] <= k: d = x
        else: break
    return d

# ---- ticks and motion ------------------------------------------------------------------------------
def episodes(ticks):
    """Contiguous runs of ascending ticks."""
    eps, cur = [], []
    for k in ticks:
        if cur and k == cur[-1] + 1: cur.append(k)
        else:
            if cur: eps.append(cur)
            cur = [k]
    if cur: eps.append(cur)
    return eps

def sequential_violations(run, s):
    """
    The F1 rule on Mesa's sequential motion: every tick on which the robot MOVED, its step from the
    previous position to the new one checked against the human's position that tick (the human has
    already moved when the robot steps). A violation is a step whose distance to the human, convex
    along the step, is not increasing from the first instant and whose minimum is below s (less TOL).
    Returns (tick, minimum, distance at the step's start) per violating tick.
    """
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
        dmin = math.hypot(dx + t * ex, dy + t * ey)
        if dmin < s - TOL: out.append((k, dmin, math.hypot(dx, dy)))
    return out
