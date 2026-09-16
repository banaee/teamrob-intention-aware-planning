#!/usr/bin/env python3
"""
evaluate.py — T10's comparison of the three configurations, from their logs alone.

Usage (repo root):
    python analysis/t10_b3_realized/evaluate.py > analysis/t10_b3_realized/comparison.md

Reads plain_none/, realized_none/, realized_b2a/ (sweep.sh) and the L2 baselines
(analysis/l2_execution_lag/new/) and, per condition, reports:
  - the decision sequence of each configuration (step:trigger:winner, with B3's selection and
    the decided hold), and where plain vs realized and realized none vs b2a first differ;
  - every all_unrealizable event, with its candidates;
  - every hold ([hold] start/end: planned, executed, interrupted);
  - actual separation below --sep (cm): contiguous episodes of the tick-sampled `dist` and of the
    continuous `min` (TODO-79), each tick labelled against the assessed window of the decision in
    effect — inside: the tick's motion lies within [1, T_h] on that decision's projection clock
    (step 1 is the observation offset, L2); edge: it straddles the offset or T_h; outside: past
    T_h, or the decision had no projection (plain, no_projection), or the robot had finished;
    "(fallback)" marks a decision taken by the all_unrealizable fallback, whose window was not
    cleared by anyone;
  - how far the new baselines are from L2: first differing decision, and the first differing line
    per regression grep on the L2 step count ([meta-cand] changed format; [sep] compared on `dist`).
Only the line formats of run_mesa.py / meta_planner.py / executor.py are read; no simulator import.
"""
import re, sys, hashlib
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
L2 = ROOT / "analysis/l2_execution_lag/new"
CONFIGS = ["plain_none", "realized_none", "realized_b2a"]
SEP = 50.0
if "--sep" in sys.argv:
    SEP = float(sys.argv[sys.argv.index("--sep") + 1])

ITEM = re.compile(r"deliver_item\(\?item=(item_\d+),\?kitting_table=kitting_table_0\)")
GREPS = ["[meta] ", "[meta-proj]", "[meta-pool]", "[IR] step=", "[IR-dist]", "[IR-complete]", "[sep]"]

def short(s): return ITEM.sub(r"\1", s)
def lines(p): return [l.rstrip("\n") for l in open(p, errors="replace")]
def num(x): return None if x in (None, "None") else float(x)

def parse(path):
    L = lines(path)
    step, b2, b3, cands = None, None, None, []
    decisions, holds, sep, steps = [], [], {}, 0
    for l in L:
        m = re.match(r"\[meta-trig\] step=(\d+) trigger=", l)
        if m: step = int(m[1]); b2 = b3 = None; cands = []; continue
        if l.startswith("[meta-b2]"):
            d = dict(re.findall(r"(\w+)=(\S+)", l))
            b2 = d; continue
        if l.startswith("[meta-cand]"):
            d = dict(re.findall(r"(\w+)=(\S+)", l)); d["task"] = short(l.split()[1]); cands.append(d); continue
        if l.startswith("[meta-b3]"):
            b3 = dict(re.findall(r"(\w+)=(\S+)", l)); continue
        m = re.match(r"\[meta\] step=(\d+) trigger=(\S+) winner=\S+\{'\?item': '(item_\d+)'", l)
        if m:
            s, trig, w = int(m[1]), m[2], m[3]
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
        if m: decisions.append(dict(step=int(m[1]), trigger="done", winner="-", source="done", selection="done", hold=0, T_h=None, cands=[])); continue
        if l.startswith("[hold]"): holds.append(l); continue
        m = re.match(r"\[sep\] step=(\d+) \S+ dist=(\S+)(?: min=(\S+))?", l)
        if m: sep[int(m[1])] = (float(m[2]), num(m[3])); steps = max(steps, int(m[1]) + 1)
    return dict(lines=L, decisions=decisions, holds=holds, sep=sep, steps=steps)

def fmt_dec(d):
    tag = "" if d["source"] == "done" else f"[{d['selection']}" + (f",hold={d['hold']}" if d["hold"] else "") + "]"
    return f"{d['step']}:{d['trigger']}:{d['winner']}{tag}"

def seq(run): return [(d["step"], d["trigger"], d["winner"]) for d in run["decisions"]]
def order(sq):
    out = []
    for _, _, w in sq:
        if w != "-" and (not out or out[-1] != w): out.append(w)
    return out

def diff_seq(a, b, na, nb):
    sa, sb = seq(a), seq(b)
    if sa == sb: return "identical"
    k = next((i for i, (x, y) in enumerate(zip(sa, sb)) if x != y), min(len(sa), len(sb)))
    ga = fmt_dec(a["decisions"][k]) if k < len(sa) else "-"
    gb = fmt_dec(b["decisions"][k]) if k < len(sb) else "-"
    return (f"differs from entry {k} ({na} {ga}; {nb} {gb}); task order "
            f"{'identical' if order(sa) == order(sb) else 'DIFFERS: ' + ' '.join(order(sa)) + ' vs ' + ' '.join(order(sb))}")

def in_effect(run, k):
    d = None
    for x in run["decisions"]:
        if x["step"] <= k: d = x
        else: break
    return d

def label(d, k, interval):
    if d is None: return "outside(no_decision)"
    if d["source"] == "done": return "outside(robot_done)"
    if d["T_h"] is None: return "outside(no_projection)"
    suffix = "(fallback)" if d["selection"] == "all_unrealizable" else ""
    end = k - d["step"] + 1            # the sampled instant on the decision's projection clock
    start = end - 1
    T_h = d["T_h"]
    if interval:
        if start >= 1.0 and end <= T_h: lab = "inside"
        elif start >= T_h or end <= 1.0: lab = "outside(past_T_h)" if start >= T_h else "outside(offset)"
        else: lab = "edge"
    else:
        lab = "inside" if 1.0 <= end <= T_h else ("outside(past_T_h)" if end > T_h else "outside(offset)")
    return lab + suffix

def episodes(run, which):
    idx = 0 if which == "dist" else 1
    vals = {k: v[idx] for k, v in run["sep"].items() if v[idx] is not None}
    eps, cur = [], []
    for k in sorted(vals):
        if vals[k] < SEP: cur.append(k)
        elif cur: eps.append(cur); cur = []
    if cur: eps.append(cur)
    out = []
    for e in eps:
        labs = {}
        for k in e:
            lab = label(in_effect(run, k), k, which == "min")
            labs[lab] = labs.get(lab, 0) + 1
        kmin = min(e, key=vals.get)
        out.append(f"{e[0]}–{e[-1]} ({len(e)} t, min {vals[kmin]:.2f} @{kmin}; "
                   + ", ".join(f"{v} {k}" for k, v in labs.items()) + ")")
    return out or ["none"]

def grep_diff(new, base, nsteps):
    """First differing line per regression grep, the new log cut at the baseline's step count."""
    out = []
    for g in GREPS:
        A = [l for l in base["lines"] if l.startswith(g)]
        B = [l for l in new["lines"] if l.startswith(g)]
        if g in ("[sep]", "[IR] step=", "[IR-dist]", "[IR-complete]", "[meta] "):
            def stp(l):
                m = re.search(r"step=(\d+)", l); return int(m[1]) if m else -1
            B = [l for l in B if stp(l) < nsteps]
        if g == "[sep]":
            B = [re.sub(r" min=\S+", "", l) for l in B]
        if A == B: continue
        k = next((i for i, (x, y) in enumerate(zip(A, B)) if x != y), min(len(A), len(B)))
        m = re.search(r"step=(\d+)", (A + B)[k] if k < max(len(A), len(B)) else "")
        out.append(f"{g.strip()} first differs at line {k}" + (f" (step {m[1]})" if m else "") + f"; lines {len(A)} → {len(B)}")
    return out or ["byte-identical on every grep"]

runs = {c: {p.stem: parse(p) for p in sorted((HERE / c).glob("*.log"))} for c in CONFIGS}
base = {p.stem: parse(p) for p in sorted(L2.glob("*.log"))}
conds = sorted(runs["plain_none"])  # the four fixtures run under every configuration

print(f"# T10 — B3 on realized cost: plain vs realized, none vs b2a\n")
print(f"Generated by `evaluate.py`. PYTHONHASHSEED=0. Separation threshold {SEP:g} cm (min_separation). "
      f"Decision format step:trigger:winner[selection,hold]; selections: plain, no_projection, realized, "
      f"all_unrealizable (B3), b2_continue / b2_continue_hold (B2). Ticks below the threshold are labelled "
      f"against the assessed window of the decision in effect (see the script docstring).\n")

print("## Summary\n")
tot = {c: dict(au=0, holds=0, held_ticks=0, interrupted=0) for c in CONFIGS}
rows = []
for cond in conds:
    r = {c: runs[c][cond] for c in CONFIGS if cond in runs[c]}
    for c, run in r.items():
        tot[c]["au"] += sum(d["selection"] == "all_unrealizable" for d in run["decisions"])
        tot[c]["holds"] += sum(" start " in h for h in run["holds"])
        tot[c]["held_ticks"] += sum(int(re.search(r"executed=(\d+)", h)[1]) for h in run["holds"] if " end " in h)
        tot[c]["interrupted"] += sum("interrupted=True" in h for h in run["holds"])
    done = {c: next((d["step"] for d in run["decisions"] if d["source"] == "done"), None) for c, run in r.items()}
    rows.append((cond, done))
print("| condition | done plain_none | done realized_none | done realized_b2a | plain vs realized | realized none vs b2a |")
print("|---|---|---|---|---|---|")
for cond, done in rows:
    a, b, c = (runs[x][cond] for x in CONFIGS)
    print(f"| {cond} | {done['plain_none']} | {done['realized_none']} | {done['realized_b2a']} | "
          f"{diff_seq(a, b, 'plain', 'realized').split(';')[0]} | {diff_seq(b, c, 'none', 'b2a').split(';')[0]} |")
print()
for c in CONFIGS:
    t = tot[c]
    print(f"- {c}: all_unrealizable events {t['au']}; holds started {t['holds']}, ticks held {t['held_ticks']}, interrupted {t['interrupted']}")
print()

for cond in conds:
    print(f"## {cond}\n")
    r = {c: runs[c][cond] for c in CONFIGS if cond in runs[c]}
    for c, run in r.items():
        print(f"Decisions {c}: " + " ".join(fmt_dec(d) for d in run["decisions"]) + "  ")
    print()
    if len(r) == 3:
        a, b, c3 = r["plain_none"], r["realized_none"], r["realized_b2a"]
        print(f"- plain vs realized (gate none): {diff_seq(a, b, 'plain', 'realized')}")
        print(f"- realized: gate none vs b2a: {diff_seq(b, c3, 'none', 'b2a')}")
        print()
    au = [(c, d) for c, run in r.items() for d in run["decisions"] if d["selection"] == "all_unrealizable"]
    if au:
        print("all_unrealizable:\n")
        for c, d in au:
            print(f"- {c} step {d['step']} {d['trigger']}: T_h={d['T_h']}; winner {d['winner']} on plain cost; candidates: "
                  + "; ".join(f"{x['task']} {x['reason']} T_r={x['T_r']}" for x in d["cands"]))
        print()
    for c, run in r.items():
        if run["holds"]:
            print(f"Holds {c}:\n")
            for h in run["holds"]: print(f"- `{h}`")
            print()
    print(f"Separation below {SEP:g} cm (tick-sampled `dist` / continuous `min`):\n")
    for c, run in r.items():
        print(f"- {c} dist: " + "; ".join(episodes(run, "dist")))
        print(f"- {c} min: " + "; ".join(episodes(run, "min")))
    print()
    if cond in base:
        nsteps = base[cond]["steps"]
        for c in ("plain_none", "realized_none"):
            if c in r:
                print(f"- {c} vs L2 ({nsteps} steps): decisions {diff_seq(r[c], base[cond], c, 'L2').split(';')[0]}; "
                      + "; ".join(grep_diff(r[c], base[cond], nsteps)))
        print()

# s40: regression sweep only (realized_none)
for cond in sorted(runs["realized_none"]):
    if cond in conds or cond not in base: continue
    run, b = runs["realized_none"][cond], base[cond]
    print(f"## {cond} (regression sweep only)\n")
    print(f"Decisions realized_none: " + " ".join(fmt_dec(d) for d in run["decisions"]) + "  \n")
    print(f"- realized_none vs L2: decisions {diff_seq(run, b, 'realized', 'L2').split(';')[0]}; " + "; ".join(grep_diff(run, b, b['steps'])))
    print(f"- realized_none min: " + "; ".join(episodes(run, "min")))
    print()

print("## Baselines (md5)\n")
print("| condition | " + " | ".join(CONFIGS) + " |")
print("|---|" + "---|" * len(CONFIGS))
for cond in sorted(runs["realized_none"]):
    cells = []
    for c in CONFIGS:
        p = HERE / c / f"{cond}.log"
        cells.append(hashlib.md5(p.read_bytes()).hexdigest() if p.exists() else "-")
    print(f"| {cond} | " + " | ".join(cells) + " |")
