#!/usr/bin/env python3
"""
evaluate.py — F1's comparison of the three configurations, from their logs alone.

Usage (repo root):
    python analysis/f1_robot_responsible/evaluate.py > analysis/f1_robot_responsible/comparison.md

Reads plain_none/, realized_none/, realized_b2a/ (sweep.sh) and the T10 baselines
(analysis/t10_b3_realized/<config>/) and, per condition, reports:
  - the decision sequence of each configuration (step:trigger:winner, with B3's selection and
    the decided hold), and where plain vs realized and realized none vs b2a first differ;
  - (there is no all_unrealizable event since F1; the counter stays as a check that none appears);
  - every hold ([hold] start/end: planned, executed, interrupted);
  - actual separation below --sep (cm): contiguous episodes of the tick-sampled `dist` and of the
    continuous `min` (TODO-79), each tick labelled against the assessed window of the decision in
    effect — inside: the tick's motion lies within [1, T_h] on that decision's projection clock
    (step 1 is the observation offset, L2); edge: it straddles the offset or T_h; outside: past
    T_h, or the decision had no projection (plain, no_projection), or the robot had finished;
    each tick below the threshold is ALSO classified against the F1 rule at execution: "viol" when
    the robot moved during the tick and the continuous minimum lies below both the threshold and
    the tick's starting distance (the distance decreased within min_separation while the robot
    moved: rule (a) or (b)); "stand" when the robot did not move; "recede" when it moved with the
    distance increasing throughout. For the tick-sampled `dist` the same with the end-of-tick
    distance against the previous one;
  - how far the new baselines are from the T10 baselines, per configuration: first differing
    decision, and the first differing line per regression grep ([meta-cand] changed format; [sep] compared on `dist`).
Only the line formats of run_mesa.py / meta_planner.py / executor.py are read (analysis/logparse.py); no simulator import.
"""
import re, sys, hashlib
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE.parent))
import logparse
from logparse import fmt_dec, seq, in_effect
T10 = ROOT / "analysis/t10_b3_realized"
CONFIGS = ["plain_none", "realized_none", "realized_b2a"]
SEP = 50.0
if "--sep" in sys.argv:
    SEP = float(sys.argv[sys.argv.index("--sep") + 1])

GREPS = ["[meta] ", "[meta-proj]", "[meta-pool]", "[IR] step=", "[IR-dist]", "[IR-complete]", "[sep]"]

def parse(path):
    run = logparse.parse(path)
    run["holds"] = run["hold_lines"]
    return run

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

def rule(run, k, which):
    """F1 rule at execution over tick k: viol | stand | recede (see the docstring)."""
    rp = run["rpos"]
    if k - 1 not in rp or k not in rp: return "?"
    moved = rp[k] != rp[k - 1]
    if not moved: return "stand"
    d_prev = run["sep"].get(k - 1, (None, None))[0]
    d_end, d_min = run["sep"][k]
    if d_prev is None: return "?"
    if which == "min":
        return "viol" if (d_min is not None and d_min < SEP and d_min < d_prev - 1e-9) else "recede"
    return "viol" if (d_end < SEP and d_end <= d_prev) else "recede"

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
            lab = rule(run, k, which) + " " + label(in_effect(run, k), k, which == "min")
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
            A = [re.sub(r" min=\S+", "", l) for l in A]
            B = [re.sub(r" min=\S+", "", l) for l in B]
        if A == B: continue
        k = next((i for i, (x, y) in enumerate(zip(A, B)) if x != y), min(len(A), len(B)))
        m = re.search(r"step=(\d+)", (A + B)[k] if k < max(len(A), len(B)) else "")
        out.append(f"{g.strip()} first differs at line {k}" + (f" (step {m[1]})" if m else "") + f"; lines {len(A)} → {len(B)}")
    return out or ["byte-identical on every grep"]

runs = {c: {p.stem: parse(p) for p in sorted((HERE / c).glob("*.log"))} for c in CONFIGS}
base = {c: {p.stem: parse(p) for p in sorted((T10 / c).glob("*.log"))} for c in CONFIGS}
conds = sorted(runs["plain_none"])  # the four fixtures run under every configuration

print(f"# F1 — robot-responsible separation: plain vs realized, none vs b2a, and against T10\n")
print(f"Generated by `evaluate.py`. PYTHONHASHSEED=0. Separation threshold {SEP:g} cm (min_separation). "
      f"Decision format step:trigger:winner[selection,hold]; selections: plain, no_projection, realized, "
      f"b2_continue / b2_continue_hold (B2). Ticks below the threshold are labelled with the F1 rule at execution "
      f"(viol | stand | recede) and against the assessed window of the decision in effect (see the script docstring).\n")

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
    for c in CONFIGS:
        if c in r and cond in base[c]:
            b = base[c][cond]
            print(f"- {c} vs T10 {c}: decisions {diff_seq(r[c], b, 'F1', 'T10')}; "
                  + "; ".join(grep_diff(r[c], b, b["steps"])))
    print()

# s40: regression sweep only (realized_none)
for cond in sorted(runs["realized_none"]):
    if cond in conds or cond not in base["realized_none"]: continue
    run, b = runs["realized_none"][cond], base["realized_none"][cond]
    print(f"## {cond} (regression sweep only)\n")
    print(f"Decisions realized_none: " + " ".join(fmt_dec(d) for d in run["decisions"]) + "  \n")
    print(f"- realized_none vs T10: decisions {diff_seq(run, b, 'F1', 'T10').split(';')[0]}; " + "; ".join(grep_diff(run, b, b['steps'])))
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
