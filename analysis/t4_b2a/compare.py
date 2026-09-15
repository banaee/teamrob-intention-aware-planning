#!/usr/bin/env python3
"""
compare.py — a gated sweep against its ungated reference, per condition (T4; reusable in T6).

Usage (repo root):
    python analysis/t4_b2a/compare.py <base_dir> <variant_dir> [cf_dir] [--sep 50] > comparison.md

<base_dir>, <variant_dir>: logs named <cond>.log (sweep.sh). [cf_dir]: cf_b3.py logs, same names.
Per condition in the variant dir:
  - every B2 verdict ([meta-b2], with the step of its [meta-trig] line);
  - the decision sequence (step:trigger:winner from [meta]) in both, and where it differs;
  - every executed hold ([hold] start/end);
  - actual separation: contiguous [sep] episodes below --sep (cm), both runs;
  - with cf_dir: B2 continues, those where B3 would have switched, single-task pools, and whether
    the cf log equals the variant log on the regression greps + [meta-b2] + [hold] (in order).
Only the line formats of run_mesa.py / meta_planner.py / executor.py are read; no simulator import.
"""
import re, sys
from pathlib import Path

args = [a for a in sys.argv[1:]]
sep_thr = 50.0
if "--sep" in args:
    i = args.index("--sep"); sep_thr = float(args[i + 1]); del args[i:i + 2]
base, var = Path(args[0]), Path(args[1])
cf = Path(args[2]) if len(args) > 2 else None

STRIP = re.compile(r"^\d{4}-\d\d-\d\d [\d:,]+ ")
CHECK = ("[meta]", "[meta-proj]", "[meta-pool]", "[IR] step=", "[IR-dist]", "[IR-complete]", "[sep]",
         "[meta-b2]", "[hold]")
ITEM = re.compile(r"deliver_item\(\?item=(item_\d+),\?kitting_table=kitting_table_0\)")

def lines(p): return [STRIP.sub("", l.rstrip("\n")) for l in open(p, errors="replace")]
def short(s): return ITEM.sub(r"\1", s)

def decisions(L):
    out = []
    for l in L:
        m = re.match(r"\[meta\] step=(\d+) trigger=(\S+) winner=\S+\{'\?item': '(item_\d+)'", l)
        if m: out.append((int(m[1]), m[2], m[3]))
        m = re.match(r"\[meta\] step=(\d+) all tasks complete", l)
        if m: out.append((int(m[1]), "done", "-"))
    return out

def b2(L):
    out, step = [], None
    for l in L:
        m = re.match(r"\[meta-trig\] step=(\d+) trigger=", l)
        if m: step = int(m[1])
        if l.startswith("[meta-b2]"): out.append((step, short(l[len("[meta-b2] "):])))
    return out

def episodes(L):
    d = {int(m[1]): float(m[2]) for m in (re.match(r"\[sep\] step=(\d+) \S+ dist=(\S+)", l) for l in L) if m}
    eps, cur = [], []
    for k in sorted(d):
        if d[k] < sep_thr: cur.append(k)
        elif cur: eps.append(cur); cur = []
    if cur: eps.append(cur)
    return "; ".join(f"{e[0]}–{e[-1]} ({len(e)} t, min {min(d[k] for k in e):.2f} @{min(e, key=d.get)})" for e in eps) or "none"

def order(seq):
    out = []
    for _, _, w in seq:
        if not out or out[-1] != w: out.append(w)
    return out

def fmt(seq): return " ".join(f"{s}:{t}:{w}" for s, t, w in seq)

print(f"# {var.name} against {base.name}\n")
print(f"Separation threshold {sep_thr:g} cm. Decision format step:trigger:winner.\n")
for vlog in sorted(var.glob("*.log")):
    c = vlog.stem
    V, B = lines(vlog), lines(base / f"{c}.log")
    print(f"## {c}\n")
    rows = b2(V)
    if rows:
        print("B2 verdicts:\n")
        for s, r in rows: print(f"- {s}: {r}")
        print()
    dv, db = decisions(V), decisions(B)
    print(f"Decisions {base.name}: {fmt(db)}  \nDecisions {var.name}: {fmt(dv)}  ")
    if dv == db:
        print("Decision sequence: identical\n")
    else:
        k = next((i for i, (x, y) in enumerate(zip(db, dv)) if x != y), min(len(db), len(dv)))
        print(f"Decision sequence: differs from entry {k} "
              f"({base.name} {db[k] if k < len(db) else '-'}, {var.name} {dv[k] if k < len(dv) else '-'}); "
              f"task order (consecutive repeats collapsed) {'identical' if order(db) == order(dv) else 'DIFFERS'}\n")
    holds = [l for l in V if l.startswith("[hold]")]
    if holds:
        print("Holds:\n")
        for h in holds: print(f"- `{h}`")
        print()
    print(f"[sep] < {sep_thr:g}: {base.name} {episodes(B)}  \n[sep] < {sep_thr:g}: {var.name} {episodes(V)}\n")
    if cf is not None and (cf / f"{c}.log").exists():
        C = lines(cf / f"{c}.log")
        cfl = [l for l in C if l.startswith("[cf-b3]")]
        same = [l for l in C if l.startswith(CHECK)] == [l for l in V if l.startswith(CHECK)]
        sw = [short(l) for l in cfl if "b3_would_switch=True" in l]
        print(f"Counterfactual B3: continues {len(cfl)}, B3 would switch {len(sw)}, "
              f"single-task pool {sum('pool=1 ' in l for l in cfl)}; cf log equals the run: {'yes' if same else 'NO'}")
        for l in sw: print(f"- `{l}`")
        print()
