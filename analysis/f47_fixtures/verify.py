#!/usr/bin/env python3
"""verify.py <log>... — F47 conditions 1–3 from a stop-on log: every [stop] episode with the decision in
effect, the candidates it saw (alternatives = candidates minus the winner), whether the blocked task was the
robot's last (pool of one), the human's stand window at the place, and completion."""
import re, sys
from pathlib import Path
ITEM = re.compile(r"deliver_item\(\?item=(item_\d+),\?kitting_table=kitting_table_0\)")
def short(s): return ITEM.sub(r"\1", s)
for path in sys.argv[1:]:
    L = [l.rstrip("\n") for l in open(path, errors="replace")]
    decisions, cands, cur, stops, hstand, done, steps, holds = [], {}, [], [], {}, None, 0, []
    for l in L:
        m = re.match(r"\[meta-trig\] step=(\d+)", l)
        if m: cur = []; continue
        if l.startswith("[meta-cand]"): cur.append(short(l.split()[1])); continue
        m = re.match(r"\[meta\] step=(\d+) trigger=(\S+) winner=\S+\{'\?item': '(item_\d+)'", l)
        if m:
            decisions.append((int(m[1]), m[2], short(m[3]))); cands[int(m[1])] = list(cur); continue
        m = re.match(r"\[meta\] step=(\d+) all tasks complete", l)
        if m: done = int(m[1]); continue
        if l.startswith("[stop]"):
            d = dict(re.findall(r"(\w+)=(\S+)", l)); m = re.search(r"action=(\w+)\(([^)]*)\)", l)
            stops.append((int(d["step"]), m[1], m[2].split(",")[-1], d["window"], d["decision"], d["T_h"])); continue
        m = re.match(r"\[hold\] step=(\d+) \S+ start planned=(\d+)", l)
        if m: holds.append((int(m[1]), int(m[2]))); continue
        m = re.match(r"\s*step: (\d+): \[human_\d+\] task=(\S+) action=(\S+) micro=(\S+) pos=\[\s*(\S+)\s+(\S+)\s*\]", l)
        if m:
            k = int(m[1]); steps = max(steps, k + 1)
            if m[3] == "wait_at": hstand.setdefault(m[2] + "@" + f"({float(m[5]):.0f},{float(m[6]):.0f})", []).append(k)
    eps = []
    for s in stops:
        if eps and s[0] == eps[-1][-1][0] + 1: eps[-1].append(s)
        else: eps.append([s])
    print(f"## {Path(path).stem}  ({Path(path).parent.name})")
    print(f"decisions: " + " ".join(f"{s}:{t}:{w}" for s, t, w in decisions) + (f" done:{done}" if done is not None else f" NOT DONE in {steps}"))
    for k, v in hstand.items():
        print(f"human wait_at {k}: ticks {v[0]}–{v[-1]} ({len(v)})")
    if holds: print("holds: " + "; ".join(f"start {s} planned {p}" for s, p in holds))
    for e in eps:
        t0, act, place, win, dec, th = e[0]
        d = max((x for x in decisions if x[0] <= t0), key=lambda x: x[0], default=None)
        c = cands.get(d[0], []) if d else []
        alts = [x for x in c if x != d[2]] if d else []
        last = (len(c) == 1) if d else None
        print(f"STOP {t0}–{e[-1][0]} ({len(e)} ticks) {act}->{place}, window {win}, decision {dec} T_h {th}; "
              f"decision in effect {d[0] if d else '-'}:{d[2] if d else '-'} over {c}; alternatives {alts}; "
              f"{'LAST task' if last else 'not the last task'}")
    print()
