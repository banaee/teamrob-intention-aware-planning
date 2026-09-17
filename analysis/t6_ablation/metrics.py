#!/usr/bin/env python3
"""
metrics.py — the T6 metrics per cell, from the logs alone (no simulator import).

Usage (repo root):
    python analysis/t6_ablation/metrics.py > analysis/t6_ablation/matrix.md

Reads core/<cell>/<fixture>_<prior>.log (the 2x2x2 cross of gate x cost x stop) and rho/rho<r>/ (the
rho sweep). Per run:
  - COMPLETION FROM THE WORLD FACT: the robot's pool is the first [meta] line's winner plus queue; the
    terminal condition obj_at(item, table) comes to hold on the tick the robot's release microaction
    executes (the per-tick line `action=place micro=release`), and is first observable on the next
    tick. The run is complete when the robot has released as many items as its pool holds; the
    completion tick is the last release + 1, the first tick on which the WorldState shows the fact.
    Where the recognizer pins the same item ([IR-complete], every robot item with the prior off, none
    with it on, since then the hypotheses are the human's pool) the pin is checked to be that tick;
    a mismatch is printed as a warning. The declared tick ([meta] ... all tasks complete, the
    empty-pool line) is shown next to it.
  - decision sequence (step:trigger:winner[selection,hold]) and its first divergence from the
    reference cell of the same fixture and prior (gate none, cost realized, stop off: the D2 baseline),
    and pairwise per question in the (a) / (b) / (c) tables.
  - trigger fires ([meta-trig] with a trigger) by kind; B2 verdicts ([meta-b2]).
  - holds: started, ticks executed, interrupted.
  - stop-on: blocked ticks, episodes, outcome (blocked.py's rule), refusals by window label, and the
    rule each refusal prevented ((a): the step started at or beyond s; (b): within).
  - robot violations on sequential motion (blocked.py / evaluate.py's acceptance check) split (a)/(b).
  - sub-s ticks: sampled [sep] dist below the run's min_separation, labelled against the assessed
    window of the decision in effect (F1's evaluate.py labelling: inside / edge / past T_h / other,
    where other is no projection, the offset tick, no decision, or the robot done).
  - human-borne proximity: blocked.py's stand < s split (stop / hold / own action / done).
min_separation (s) is read from each log's [run] header. The parsing functions are blocked.py's and F1
evaluate.py's, copied because neither is importable without running its main body; the (a)/(b) split
and the world-fact completion are the extensions.
"""
import re, sys, math
from pathlib import Path

HERE = Path(__file__).parent
TOL = 0.05

def num(x): return None if x in (None, "None") else float(x)

def parse(path):
    hdr = {}
    fires, b2, b3, cands = {}, None, None, []
    decisions, pins, holds, stops, sep, rpos, hpos, ract, rtask, releases = [], {}, [], [], {}, {}, {}, {}, {}, []
    declared, steps, pool = None, 0, None
    verdicts = {"continue": 0, "continue_hold": 0, "escalate": 0}
    for l in open(path, errors="replace"):
        l = l.rstrip("\n")
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
        if l.startswith("[meta-b3]"):
            b3 = dict(re.findall(r"(\w+)=(\S+)", l)); continue
        m = re.match(r"\[meta\] step=(\d+) trigger=(\S+) winner=\S+\{'\?item': '(item_\d+)'.*queue=(.*)$", l)
        if m:
            s, trig, w = int(m[1]), m[2], m[3]
            if pool is None: pool = [w] + re.findall(r"item_\d+", m[4])
            if b3 is not None:
                dec = dict(step=s, trigger=trig, winner=w, selection=b3["selection"], hold=int(b3["hold"]), T_h=num(b3["T_h"]))
            elif b2 is not None and b2.get("verdict", "").startswith("continue"):
                dec = dict(step=s, trigger=trig, winner=w, selection="b2_" + b2["verdict"], hold=int(b2.get("hold", 0)), T_h=num(b2.get("remaining")))
            else:
                dec = dict(step=s, trigger=trig, winner=w, selection="?", hold=0, T_h=None)
            decisions.append(dec); continue
        m = re.match(r"\[meta\] step=(\d+) all tasks complete", l)
        if m: declared = int(m[1]); decisions.append(dict(step=declared, trigger="done", winner="-", selection="done", hold=0, T_h=None)); continue
        m = re.match(r"\[IR-complete\] step=(\d+) deliver_item\(\?item=(item_\d+),", l)
        if m: pins.setdefault(m[2], int(m[1])); continue
        m = re.match(r"\[hold\] step=(\d+) \S+ start planned=(\d+)", l)
        if m: holds.append(dict(start=int(m[1]), planned=int(m[2]), executed=None, interrupted=None)); continue
        m = re.match(r"\[hold\] step=(\d+) \S+ end planned=\d+ executed=(\d+) interrupted=(\w+)", l)
        if m and holds and holds[-1]["executed"] is None:
            holds[-1]["executed"] = int(m[2]); holds[-1]["interrupted"] = m[3] == "True"; continue
        if l.startswith("[stop]"):
            d = dict(re.findall(r"(\w+)=(\S+)", l))
            m = re.search(r"action=(\w+)\(([^)]*)\)", l)
            d["step"] = int(d["step"]); d["action"] = m[1]
            args = m[2].split(",")
            d["place"] = args[-1] if len(args) > 1 else m[2]
            d["dist"] = float(d["dist"]); d["step_min"] = float(d["step_min"])
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
    sepv = float(hdr.get("min_separation", 50.0))
    pool = pool or []
    done_world = releases[-1] + 1 if pool and len(releases) >= len(pool) else None
    if len(releases) > len(pool):
        print(f"WARNING {path}: {len(releases)} releases for a pool of {len(pool)}", file=sys.stderr)
    if done_world is not None:
        robot_pins = [pins[i] for i in pool if i in pins]
        if robot_pins and max(robot_pins) != done_world:
            print(f"WARNING {path}: last pin {max(robot_pins)} != last release + 1 = {done_world}", file=sys.stderr)
    return dict(hdr=hdr, sep_v=sepv, fires=fires, verdicts=verdicts, decisions=decisions, pins=pins, pool=pool, releases=releases,
                done_world=done_world, declared=declared, holds=holds, hold_ticks=hold_ticks, stops=stops,
                sep=sep, rpos=rpos, hpos=hpos, ract=ract, rtask=rtask, steps=steps)

# ---- decisions -------------------------------------------------------------------------------------
def fmt_dec(d):
    tag = "" if d["selection"] == "done" else f"[{d['selection']}" + (f",hold={d['hold']}" if d["hold"] else "") + "]"
    return f"{d['step']}:{d['trigger']}:{d['winner']}{tag}"

def seq(run): return [(d["step"], d["trigger"], d["winner"]) for d in run["decisions"]]

def order(run):
    out = []
    for d in run["decisions"]:
        w = d["winner"]
        if w != "-" and (not out or out[-1] != w): out.append(w)
    return out

def diverge(a, b):
    """First entry at which the decision sequences differ: 'identical', or the step and both entries."""
    sa, sb = seq(a), seq(b)
    if sa == sb: return "identical"
    k = next((i for i, (x, y) in enumerate(zip(sa, sb)) if x != y), min(len(sa), len(sb)))
    ga = fmt_dec(a["decisions"][k]) if k < len(sa) else "-"
    gb = fmt_dec(b["decisions"][k]) if k < len(sb) else "-"
    oa, ob = order(a), order(b)
    return f"entry {k}: {ga} vs {gb}" + ("" if oa == ob else f"; ORDER {' '.join(oa)} vs {' '.join(ob)}")

# ---- windows (F1 evaluate.py) ----------------------------------------------------------------------
def in_effect(run, k):
    d = None
    for x in run["decisions"]:
        if x["step"] <= k: d = x
        else: break
    return d

def label(d, k):
    if d is None: return "other"
    if d["selection"] == "done": return "other"
    if d["T_h"] is None: return "other"
    end = k - d["step"] + 1; start = end - 1; T_h = d["T_h"]
    if start >= 1.0 and end <= T_h: return "inside"
    if start >= T_h: return "past"
    if end <= 1.0: return "other"
    return "edge"

def sub_s(run):
    out = {"inside": 0, "edge": 0, "past": 0, "other": 0}
    for k in sorted(run["sep"]):
        if run["sep"][k][0] < run["sep_v"]:
            out[label(in_effect(run, k), k)] += 1
    return out

def stop_windows(run):
    out = {"inside": 0, "edge": 0, "past": 0, "other": 0}
    for d in run["stops"]:
        w = d["window"]
        out["inside" if w == "inside" else "edge" if w == "edge" else "past" if w == "outside(past_T_h)" else "other"] += 1
    return out

# ---- motion checks (blocked.py) ---------------------------------------------------------------------
def sequential_violations(run):
    """Ticks on which the robot moved and its step broke the F1 rule; (a) started at or beyond s, (b) within."""
    a, b, s = [], [], run["sep_v"]
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
        if math.hypot(dx + t * ex, dy + t * ey) < s - TOL:
            (a if math.hypot(dx, dy) >= s - TOL else b).append(k)
    return a, b

def episodes(ticks):
    eps, cur = [], []
    for k in ticks:
        if cur and k == cur[-1] + 1: cur.append(k)
        else:
            if cur: eps.append(cur)
            cur = [k]
    if cur: eps.append(cur)
    return eps

def stand_within(run):
    stop_ticks = {d["step"] for d in run["stops"]}
    out = {"stop": 0, "hold": 0, "own": 0, "done": 0}
    done = run["done_world"]
    for k in sorted(run["sep"]):
        if k - 1 not in run["rpos"] or k not in run["rpos"]: continue
        if run["rpos"][k] != run["rpos"][k - 1] or run["sep"][k][0] >= run["sep_v"]: continue
        if k in stop_ticks: out["stop"] += 1
        elif k in run["hold_ticks"]: out["hold"] += 1
        elif done is not None and k > done: out["done"] += 1
        else: out["own"] += 1
    return out

def outcome(run):
    st = run["stops"]; ticks = [d["step"] for d in st]; eps = episodes(ticks)
    last = run["steps"] - 1
    if run["done_world"] is not None: return f"done {run['done_world']}"
    if eps and eps[-1][-1] == last:
        e = eps[-1]; d = next(x for x in st if x["step"] == e[0])
        return f"blocked to cap: {d['action']}→{d['place']} {len(e)} ticks ({e[0]}–{last})"
    return f"not done in {run['steps']}"

def stop_rules(run):
    a = sum(1 for d in run["stops"] if d["dist"] >= run["sep_v"] - TOL)
    return a, len(run["stops"]) - a

def fires(run):
    f = run["fires"]
    return f"{f.get('no_current_task', 0)}/{f.get('recognition_changed', 0)}/{f.get('task_committed', 0)}"

def holds(run):
    h = run["holds"]
    return f"{len(h)}/{sum(x['executed'] or 0 for x in h)}/{sum(1 for x in h if x['interrupted'])}"

def row(run, ref):
    sw = sub_s(run); stw = stop_windows(run); va, vb = sequential_violations(run); sa, sb = stop_rules(run); hb = stand_within(run)
    done = run["done_world"]
    v = run["verdicts"]
    return (f"{done if done is not None else 'no (' + str(len(run['releases'])) + '/' + str(len(run['pool'])) + ')'} | "
            f"{run['declared'] if run['declared'] is not None else '-'} | "
            f"{'-' if ref is None else diverge(run, ref)} | {len(run['decisions']) - (1 if run['declared'] is not None else 0)} | {fires(run)} | "
            f"{v['continue']}/{v['continue_hold']}/{v['escalate']} | {holds(run)} | "
            f"{len(run['stops'])} | {outcome(run) if run['stops'] or done is None else '-'} | {stw['inside']}/{stw['edge']}/{stw['past']}/{stw['other']} | {sa}/{sb} | "
            f"{len(va)}/{len(vb)} | {sw['inside']}/{sw['edge']}/{sw['past']}/{sw['other']} | {hb['stop']}/{hb['hold']}/{hb['own']}/{hb['done']}")

HEAD = ("| run | done (world) | declared | vs reference (first divergence) | decisions | fires nct/rc/tc | B2 c/ch/esc | holds n/ticks/int | "
        "blocked ticks | outcome | refusals in/edge/past/other | refused (a)/(b) | robot viol (a)/(b) | sub-s ticks in/edge/past/other | stand<s stop/hold/own/done |")
RULE = "|" + "---|" * 15

def load(d): return {p.stem: parse(p) for p in sorted(d.glob("*.log"))}

core = {d.name: load(d) for d in sorted((HERE / "core").glob("g*"))}
REF = "gnone_crealized_soff"
ref = core.get(REF, {})
FIX = ["s00", "s10", "s20", "s30", "s40", "s50", "s70", "s71"]

print("# T6 — run matrix and per-cell metrics\n")
print("Generated by `metrics.py`. PYTHONHASHSEED=0. Columns: done (world) = the tick after the robot's last release, when "
      "the pool is delivered (no (k/m) = k of m pool items released), checked against the [IR-complete] pins where the "
      "recognizer has them; declared = the empty-pool line; vs reference = first differing decision "
      "against gate none / cost realized / stop off of the same fixture and prior; fires = [meta-trig] no_current_task / "
      "recognition_changed / task_committed; B2 = b2a verdicts continue / continue_hold / escalate; holds = started / ticks "
      "executed / interrupted; refusals by the [stop] window label; refused (a)/(b) = the rule each refusal prevented; robot "
      "viol = sequential-motion violations of the F1 rule by the robot's own steps, (a)/(b); sub-s ticks = sampled distance "
      "below s by the assessed window of the decision in effect; stand<s = human-borne proximity by what the robot was doing.\n")

print("## Core cross\n")
for cell, runs in core.items():
    print(f"### {cell}\n"); print(HEAD); print(RULE)
    for c in sorted(runs):
        print(f"| {c} | " + row(runs[c], None if cell == REF else ref.get(c)) + " |")
    print()

def pair_table(title, question, keyf, left, right, cells):
    print(f"## {title}\n")
    print(f"{question}\n")
    print(f"| fixture | prior | cell pair | {left} done | {right} done | first divergence ({left} vs {right}) | {left} holds | {right} holds | {left} blocked | {right} blocked |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for ca, cb in cells:
        if ca not in core or cb not in core: continue
        for f in FIX:
            for p in ("off", "on"):
                k = f"{f}_{p}"
                a, b = core[ca].get(k), core[cb].get(k)
                if a is None or b is None: continue
                da = a["done_world"] if a["done_world"] is not None else "no"
                db = b["done_world"] if b["done_world"] is not None else "no"
                print(f"| {f} | {p} | {keyf(ca, cb)} | {da} | {db} | {diverge(a, b)} | {holds(a)} | {holds(b)} | {len(a['stops'])} | {len(b['stops'])} |")
    print()

pair_table("(a) plain vs realized", "Within each gate x stop x prior: cost plain against cost realized.",
           lambda a, b: a.replace("_cplain", ""), "plain", "realized",
           [(f"g{g}_cplain_s{s}", f"g{g}_crealized_s{s}") for g in ("none", "b2a") for s in ("off", "on")])
pair_table("(b) none vs b2a", "Within each cost x stop x prior: gate none against gate b2a (rho 0.5).",
           lambda a, b: a.replace("gnone_", ""), "none", "b2a",
           [(f"gnone_c{c}_s{s}", f"gb2a_c{c}_s{s}") for c in ("plain", "realized") for s in ("off", "on")])
pair_table("(c) stop off vs on", "Within each gate x cost x prior: separation stop off against on.",
           lambda a, b: a.replace("_soff", ""), "off", "on",
           [(f"g{g}_c{c}_soff", f"g{g}_c{c}_son") for g in ("none", "b2a") for c in ("plain", "realized")])

for sweep, base in (("rho", "gb2a_crealized_soff"),):
    d = HERE / sweep
    if not d.exists(): continue
    print(f"## {sweep} sweep (reference: core/{base})\n")
    for sd in sorted(d.iterdir(), key=lambda p: float(re.sub(r'[^0-9.]', '', p.name))):
        runs = load(sd)
        print(f"### {sd.name}\n"); print(HEAD); print(RULE)
        for c in sorted(runs):
            print(f"| {c} | " + row(runs[c], core.get(base, {}).get(c)) + " |")
        print()
