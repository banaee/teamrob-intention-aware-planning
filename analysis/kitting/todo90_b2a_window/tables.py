#!/usr/bin/env python3
"""tables.py <log> <capture.json> — (TODO-90) one row per fired decision of robot_0: tick, trigger, admitted hypothesis
(the [IR] most_likely of that tick) or the refusal reason, T_h, the assessed window, hold, B3 reached or B2 continued.
Assessed window (glossary; realize()): [decision step, T_h] ∩ the human projection's span (from the observation offset,
1 on the projection clock) ∩ the realized plan's span (to its end); tick k covers [k − t, k − t + 1] on the clock of the
decision at t (the executor's [stop] label, executor.py), so the window's ticks are those whose interval lies inside it,
up to the next fired decision."""
import json, math, re, sys
log, cap = sys.argv[1], json.load(open(sys.argv[2]))
ir, rows, cur = {}, [], None
for l in open(log):
    m = re.match(r"\[IR\] step=(\d+) most_likely=(\S+)", l)
    if m: ir[int(m[1])] = m[2]; continue
    m = re.match(r"\[meta-trig\] step=(\d+) trigger=(\S+)", l)
    if m and m[2] != "none": cur = dict(t=int(m[1]), trig=m[2]); rows.append(cur); continue
    if l.startswith("[meta-proj]"):
        p = re.search(r"projection=(\S+)", l)[1]
        cur["hyp"] = ir.get(cur["t"], "?") if p == "built" else p.replace("none(", "refused (").rstrip(")") + ")"
    elif l.startswith("[meta-b2]"):
        d = dict(re.findall(r"(\w+)=(\S+)", l)); cur["block"] = "B2 " + d["verdict"]; cur["hold"] = d.get("hold")
    elif l.startswith("[meta-b3]"):
        d = dict(re.findall(r"(\w+)=(\S+)", l)); cur["block"] = "B3"; cur["hold"] = d["hold"]; cur["win"] = d["winner"]
    elif re.match(r"\[meta\] step=\d+ all tasks complete", l):
        cur["block"] = "— (pool empty)"; cur["hold"] = "—"
print("| tick | trigger | admitted hypothesis / refusal | T_h | realized end | assessed window (clock) | ticks inside | hold | block |")
print("|---|---|---|---|---|---|---|---|---|")
for i, r in enumerate(rows):
    nxt = rows[i + 1]["t"] if i + 1 < len(rows) else 10**9
    c = [x for x in cap if x["step"] == r["t"] and x["T_h"] is not None
         and (r["block"] != "B3" or x["task"][0] == r.get("win"))]
    if c:
        th, end = c[0]["T_h"], c[0]["robot"][-1][3]; w = min(th, end)
        k0, k1 = r["t"] + 1, min(r["t"] + math.floor(w) - 1, nxt - 1)
        win, ticks, th_s, end_s = f"[1, {w:.2f}]", f"{k0}–{k1}", f"{th:.2f}", f"{end:.2f}"
    else:
        win = ticks = th_s = end_s = "—"
    print(f"| {r['t']} | {r['trig']} | {r.get('hyp','?')} | {th_s} | {end_s} | {win} | {ticks} | {r.get('hold','?')} | {r.get('block','?')} |")
