#!/usr/bin/env python3
"""measure.py <sweep_dir> — the table of the task_committed ablation, one row per run, from <tag>.log and the
<tag>.json capture.py wrote beside it.

  completion  the world fact: the robot's last `action=place micro=release` + 1.
  decisions   fired triggers, and their count per trigger (nc = no_current_task, rc = recognition_changed,
              tc = task_committed).
  holds       executed `[hold] ... end`: start tick (ticks executed).
  sep         `[sep]` against the assessed window of the decision in effect (the last fired trigger at or
              before the tick), T10's convention (analysis/t10_b3_realized/evaluate.py): tick k is the instant
              k − t + 1 on the projection clock of the decision at t, inside when 1 ≤ it ≤ T_h; T_h from
              `[meta-b3]`, or `remaining` of a `[meta-b2]` that continued; None (no projection) has no window.
              in<50: inside ticks with `dist` below min_separation; min_in: the smallest `dist` inside any
              window; out<50: sub-min_separation ticks outside every window (information).
  b2          b2a rows: `[meta-b2]` lines (B2 reached) and how many continued.
  residual    per robot delivery: release tick − (t + hold executed from t + head's projected place start) of the
              decision in effect at the release, i.e. the last fired trigger strictly before the release tick (a
              decision on the release tick itself projects a place the executor performs that same tick); `*` when
              that decision projected nothing (B2 continuing without an admitted projection) and the last decision
              on the same task that did project is used.
"""
import json, re, sys
from pathlib import Path

SEP = 50.0
REL = re.compile(r"^  step: (\d+): \[robot_0\] task=\S+ action=place micro=release")


def parse(log):
    decs, holds, sep, b2 = [], [], {}, []
    step, pend = None, {}
    for l in open(log):
        m = re.match(r"\[meta-trig\] step=(\d+) trigger=(\S+)", l)
        if m:
            step = int(m[1])
            if m[2] != "none":
                decs.append(dict(step=step, trigger=m[2], T_h=None)); pend = decs[-1]
            continue
        if l.startswith("[meta-b3]"):
            d = dict(re.findall(r"(\w+)=(\S+)", l))
            pend["T_h"] = None if d["T_h"] == "None" else float(d["T_h"]); continue
        if l.startswith("[meta-b2]"):
            d = dict(re.findall(r"(\w+)=(\S+)", l)); b2.append(d["verdict"])
            if d["verdict"].startswith("continue") and d.get("remaining"):
                pend["T_h"] = float(d["remaining"])
            continue
        if re.match(r"\[meta\] step=\d+ all tasks complete", l):
            pend["T_h"] = None; pend["done"] = True; continue
        m = re.match(r"\[hold\] step=(\d+) \S+ end planned=(\d+) executed=(\d+) interrupted=(\S+)", l)
        if m:
            holds.append((int(m[1]) - int(m[3]) + 1, int(m[3]), m[4])); continue
        m = re.match(r"\[sep\] step=(\d+) \S+ dist=(\S+)", l)
        if m: sep[int(m[1])] = float(m[2]); continue
    rels = [int(m[1]) for m in (REL.match(l) for l in open(log)) if m]
    return decs, holds, sep, b2, rels


def in_effect(decs, k):
    d = None
    for x in decs:
        if x["step"] <= k: d = x
        else: break
    return d


def row(sweep, tag):
    decs, holds, sep, b2, rels = parse(sweep / f"{tag}.log")
    cap = json.load(open(sweep / f"{tag}.json"))
    by = {"no_current_task": 0, "recognition_changed": 0, "task_committed": 0}
    for d in decs:
        if not d.get("done"): by[d["trigger"]] += 1
    n_in, min_in, out = 0, None, []
    for k, v in sorted(sep.items()):
        d = in_effect(decs, k)
        inside = d is not None and d["T_h"] is not None and 1.0 <= k - d["step"] + 1 <= d["T_h"]
        if inside:
            min_in = v if min_in is None else min(min_in, v)
            n_in += v < SEP
        elif v < SEP and (not rels or k < rels[-1] + 1):
            out.append(k)
    executed = {s: n for s, n, _ in holds}
    res = []
    for r in rels:
        c = [x for x in cap if x["step"] < r][-1]
        if c["place_start"] is not None:
            res.append(f"{r - (c['step'] + executed.get(c['step'], 0) + c['place_start']):+.2f}")
        else:
            p = [x for x in cap if x["step"] < r and x["winner"] == c["winner"] and x["place_start"] is not None][-1]
            res.append(f"{r - (p['step'] + executed.get(p['step'], 0) + p['place_start']):+.2f}*")
    return dict(completion=rels[-1] + 1 if rels else None, n=sum(by.values()),
                trig=f"{by['no_current_task']}/{by['recognition_changed']}/{by['task_committed']}",
                holds=", ".join(f"{s} ({n})" + ("i" if i == "True" else "") for s, n, i in holds) or "—",
                n_in=n_in, min_in=f"{min_in:.2f}" if min_in is not None else "—",
                out=spans(out), b2=f"{len(b2)} ({sum(v.startswith('continue') for v in b2)} cont.)",
                res=" ".join(res))


def spans(ks):
    if not ks: return "—"
    out, a = [], ks[0]
    for x, y in zip(ks, ks[1:] + [None]):
        if y != x + 1: out.append(f"{a}" if a == x else f"{a}–{x}"); a = y
    return ", ".join(out)


def main():
    sweep = Path(sys.argv[1])
    conds = [(c, s, "none") for c in ("s80", "s81", "s83", "s20", "s70") for s in ("single_task", "full_reorder")]
    conds += [(c, "b2a", "b2a") for c in ("s10", "s20", "s30")]
    print("| run | prior | trigger | completion | decisions (nc/rc/tc) | holds executed | in<50 | min in window "
          "| <50 outside window (to completion) | B2 reached | release residual per delivery |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for c, s, g in conds:
        for p in ("off", "on"):
            for t in ("with", "without"):
                r = row(sweep, f"{c}_{s}_{p}_{t}")
                name = f"{c} {'ST' if s == 'single_task' else 'FR' if s == 'full_reorder' else 'b2a ST'}"
                print(f"| {name} | {p} | {t} | {r['completion']} | {r['n']} ({r['trig']}) | {r['holds']} | "
                      f"{r['n_in']} | {r['min_in']} | {r['out']} | {r['b2'] if g == 'b2a' else '—'} | {r['res']} |")


if __name__ == "__main__":
    main()
