#!/usr/bin/env python3
"""
evaluate.py — C: the execution-time separation stop, off against on, from the logs alone.

Usage (repo root):
    python analysis/c_separation_stop/evaluate.py > analysis/c_separation_stop/comparison.md

Reads stop_off/ and stop_on/ (sweep.sh; cost realized, gate none) and the F1 realized baselines
(analysis/f1_robot_responsible/realized_none/). Per condition:
  - stop_off against the F1 baseline: byte-identical apart from the [run] header line, or not;
  - decision sequences off and on, where they differ, completion ticks;
  - every [stop] line (tick, positions, distance, step minimum, delayed action, window label), and the
    stop episodes (contiguous ticks) with their window labels;
  - ACCEPTANCE, sequential motion: for every tick on which the robot MOVED, the step from its previous
    position to its new one is checked against the human's position THAT tick (the human has already
    moved when the robot steps): a violation is a step whose distance to the human, convex along the
    step, is not increasing from the first instant and whose minimum is below min_separation. Count
    must be 0 with the stop on. Positions are read from the per-tick lines (rounded to 0.01), so a
    0.05 cm tolerance is applied.
  - the simultaneous-interpolation figure alongside: the F1 evaluation's label on `[sep] min=` (both
    agents moving in a straight line during the tick; "viol" when the robot moved and the continuous
    minimum lies below min_separation and below the tick's starting distance). Where it counts a moment
    the sequential check does not, the human's own motion during the tick is what closed the distance.
Only the line formats of run_mesa.py / meta_planner.py / executor.py are read; no simulator import.
"""
import re, sys, hashlib, math
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
F1 = ROOT / "analysis/f1_robot_responsible/realized_none"
CONFIGS = ["stop_off", "stop_on"]
SEP = 50.0
TOL = 0.05

def lines(p): return [l.rstrip("\n") for l in open(p, errors="replace")]
def num(x): return None if x in (None, "None") else float(x)

def parse(path):
    L = lines(path)
    step = None
    decisions, stops, sep, rpos, hpos, steps = [], [], {}, {}, {}, 0
    for l in L:
        m = re.match(r"\[meta-trig\] step=(\d+) trigger=", l)
        if m: step = int(m[1]); continue
        m = re.match(r"\[meta\] step=(\d+) trigger=(\S+) winner=\S+\{'\?item': '(item_\d+)'", l)
        if m: decisions.append((int(m[1]), m[2], m[3])); continue
        m = re.match(r"\[meta\] step=(\d+) all tasks complete", l)
        if m: decisions.append((int(m[1]), "done", "-")); continue
        if l.startswith("[stop]"):
            d = dict(re.findall(r"(\w+)=(\S+)", l))
            m = re.search(r"pos=\(([-\d.]+), ([-\d.]+)\) human_pos=\(([-\d.]+), ([-\d.]+)\)", l)
            d["rpos"] = (float(m[1]), float(m[2])); d["hpos"] = (float(m[3]), float(m[4]))
            d["action"] = re.search(r"action=(\S+)", l)[1]
            stops.append(d); continue
        m = re.match(r"\[sep\] step=(\d+) \S+ dist=(\S+)(?: min=(\S+))?", l)
        if m: sep[int(m[1])] = (float(m[2]), num(m[3])); steps = max(steps, int(m[1]) + 1); continue
        m = re.match(r"\s*step: (\d+): \[robot_\d+\] .*pos=\[\s*(\S+)\s+(\S+)\s*\]", l)
        if m: rpos[int(m[1])] = (float(m[2]), float(m[3])); continue
        m = re.match(r"\s*step: (\d+): \[human_\d+\] .*pos=\[\s*(\S+)\s+(\S+)\s*\]", l)
        if m: hpos[int(m[1])] = (float(m[2]), float(m[3])); continue
    return dict(lines=L, decisions=decisions, stops=stops, sep=sep, rpos=rpos, hpos=hpos, steps=steps)

def fmt(seq): return " ".join(f"{s}:{t}:{w}" for s, t, w in seq)

def diff_seq(a, b, na, nb):
    if a == b: return "identical"
    k = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    return f"differs from entry {k} ({na} {a[k] if k < len(a) else '-'}; {nb} {b[k] if k < len(b) else '-'})"

def sequential_violations(run):
    """Ticks on which the robot moved and its step broke the F1 rule against the human's position that tick."""
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
        if dmin < SEP - TOL: out.append((k, dmin, math.hypot(dx, dy)))
    return out

def simultaneous_viol(run):
    """The F1 evaluation's 'viol' ticks on [sep] min=: robot moved, continuous minimum below SEP and below the start distance."""
    out = []
    for k in sorted(run["sep"]):
        if k - 1 not in run["rpos"] or k not in run["rpos"] or k - 1 not in run["sep"]: continue
        if run["rpos"][k] == run["rpos"][k - 1]: continue
        d_prev = run["sep"][k - 1][0]; d_min = run["sep"][k][1]
        if d_min is not None and d_min < SEP and d_min < d_prev - 1e-9: out.append((k, d_min))
    return out

def episodes(stops):
    eps, cur = [], []
    for d in stops:
        k = int(d["step"])
        if cur and k == cur[-1] + 1: cur.append(k)
        else:
            if cur: eps.append(cur)
            cur = [k]
    if cur: eps.append(cur)
    return eps

runs = {c: {p.stem: parse(p) for p in sorted((HERE / c).glob("*.log"))} for c in CONFIGS}
base = {p.stem: parse(p) for p in sorted(F1.glob("*.log"))}
conds = sorted(runs["stop_on"])

print("# C — the execution-time separation stop: off against on\n")
print(f"Generated by `evaluate.py`. Cost realized, gate none; PYTHONHASHSEED=0; min_separation {SEP:g} cm. "
      "Decision format step:trigger:winner. Stop lines as logged by the executor; window: inside / edge / "
      "outside(past_T_h) / outside(no_projection) / outside(offset) of the decision in effect.\n")

print("## Summary\n")
print("| condition | off = F1 baseline (minus [run]) | done off | done on | stops on | stop episodes on | sequential violations off | on | simultaneous 'viol' off | on |")
print("|---|---|---|---|---|---|---|---|---|---|")
for c in conds:
    off, on = runs["stop_off"][c], runs["stop_on"][c]
    same = [l for l in off["lines"] if not l.startswith("[run]")] == [l for l in base[c]["lines"] if not l.startswith("[run]")]
    done_off = next((s for s, t, w in off["decisions"] if t == "done"), None)
    done_on = next((s for s, t, w in on["decisions"] if t == "done"), None)
    eps = episodes(on["stops"])
    done_on_s = str(done_on) if done_on is not None else "not within %d" % on["steps"]
    print(f"| {c} | {'yes' if same else 'NO'} | {done_off} | {done_on_s} | {len(on['stops'])} | "
          f"{'; '.join(f'{e[0]}–{e[-1]} ({len(e)})' for e in eps) or 'none'} | {len(sequential_violations(off))} | {len(sequential_violations(on))} | "
          f"{len(simultaneous_viol(off))} | {len(simultaneous_viol(on))} |")
print()

for c in conds:
    off, on = runs["stop_off"][c], runs["stop_on"][c]
    print(f"## {c}\n")
    print(f"Decisions off: {fmt(off['decisions'])}  \nDecisions on: {fmt(on['decisions'])}  ")
    print(f"Decision sequence: {diff_seq(off['decisions'], on['decisions'], 'off', 'on')}\n")
    if on["stops"]:
        print("Stops (on):\n")
        for e in episodes(on["stops"]):
            first = next(d for d in on["stops"] if int(d["step"]) == e[0])
            labels = {}
            for d in on["stops"]:
                if e[0] <= int(d["step"]) <= e[-1]: labels[d["window"]] = labels.get(d["window"], 0) + 1
            print(f"- ticks {e[0]}–{e[-1]} ({len(e)}): robot at {first['rpos']}, human at {first['hpos']}, dist {first['dist']}, "
                  f"step_min {first['step_min']}, delayed {first['action']}; window {', '.join(f'{v} {k}' for k, v in labels.items())}; "
                  f"decision {first['decision']} T_h {first['T_h']}")
        print()
    sv_off, sv_on = sequential_violations(off), sequential_violations(on)
    print(f"Acceptance, sequential motion: off {len(sv_off)} violating steps"
          + (f" ({'; '.join(f'{k}: min {d:.2f}' for k, d, _ in sv_off)})" if sv_off else "")
          + f"; on {len(sv_on)}" + (f" ({'; '.join(f'{k}: min {d:.2f}' for k, d, _ in sv_on)})" if sv_on else "") + "  ")
    si_off, si_on = simultaneous_viol(off), simultaneous_viol(on)
    print(f"Simultaneous interpolation ('viol' on [sep] min): off {len(si_off)}"
          + (f" ({'; '.join(f'{k}: {d:.2f}' for k, d in si_off)})" if si_off else "")
          + f"; on {len(si_on)}" + (f" ({'; '.join(f'{k}: {d:.2f}' for k, d in si_on)})" if si_on else "") + "\n")

print("## Baselines (md5)\n")
print("| condition | " + " | ".join(CONFIGS) + " |")
print("|---|" + "---|" * len(CONFIGS))
for c in conds:
    print(f"| {c} | " + " | ".join(hashlib.md5((HERE / cfg / f'{c}.log').read_bytes()).hexdigest() for cfg in CONFIGS) + " |")
