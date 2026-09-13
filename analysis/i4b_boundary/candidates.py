#!/usr/bin/env python3
"""
candidates.py — where each boundary definition would fire, from I4's existing CSVs and logs
(analysis/i4_evidence_model/, shipped code, no boundary). No simulator runs.

  A_phase   a retirement whose hypothesis expected its TERMINAL action on the previous tick
            (the observed agent's own derived phase had reached the completing action)
  A_release a retirement on a tick where the observed agent's microaction is RELEASE
  B         after any retirement, the first tick at which any hypothesis's expected action changes
  C(N)      the N-th consecutive stationary tick of the observed agent (fires once per stop)
  D         any tick at which any hypothesis's expected action changes

For each firing: is it a behavioural boundary in fact (the human's task/segment changes within ±2
ticks), and what it would drop — the excess (cm) every live non-truth hypothesis has accumulated on
its open stretch at that tick (the discrimination a reset without a fold forgives).
"""
import csv, re, sys
from collections import defaultdict
from pathlib import Path
I4 = Path(__file__).resolve().parents[1] / "i4_evidence_model"
CONDS = ["s00_off", "s00_on", "s20_off", "s20_on", "s30_off", "s30_on", "s40_off", "s40_on"]

def load(name):
    return [r for r in csv.DictReader(open(I4 / f"{name}.csv"))]

completions = [r for r in load("completions") if "/" not in r["condition"]]
advances = [r for r in load("phase_advances") if "/" not in r["condition"]]
expected = defaultdict(dict)      # (cond, step) -> {hyp: action}
for r in csv.DictReader(open(I4 / "expected_actions.csv")):
    if "/" not in r["condition"]:
        expected[(r["condition"], int(r["step"]))][r["hypothesis"]] = r["expected_action"]
excess = defaultdict(dict)        # (cond, step) -> {hyp: excess}
for r in csv.DictReader(open(I4 / "excess.csv")):
    if "/" not in r["condition"]:
        excess[(r["condition"], int(r["step"]))][r["hypothesis"]] = float(r["excess_cm"]) if r["excess_cm"] else 0.0
trace = defaultdict(dict)         # cond -> step -> row
with open(I4 / "trace.csv") as f:
    rd = csv.reader(f); next(rd)
    for row in rd:
        if "/" not in row[0]:
            trace[row[0]][int(row[1])] = {"segment": row[2], "truth": row[3], "action": row[4], "micro": row[5]}
STEP = re.compile(r"^\s+step: (\d+): \[human_0\] task=(\S+) action=(\S+) micro=(\S+) pos=\[\s*(-?[\d.]+)\s+(-?[\d.]+)\]")
positions = defaultdict(dict)
for c in CONDS:
    for line in open(I4 / "new" / f"{c}.log"):
        m = STEP.match(line)
        if m:
            positions[c][int(m.group(1))] = (float(m.group(5)), float(m.group(6)), m.group(2), m.group(3), m.group(4))

def is_terminal(action):
    return action.startswith("wait_at(") or (action.startswith("place(") and "kitting_table" in action)

def truth_boundaries(c):
    """Ticks where the human's task (or s40 segment) changes; plus the first idle tick."""
    b = []
    prev = None
    for s in sorted(trace[c]):
        key = (trace[c][s]["truth"], trace[c][s]["segment"])
        if prev is not None and key != prev:
            b.append(s)
        prev = key
    return b

def stops(c):
    """Runs of consecutive ticks with an unchanged human position: (start, end, action at start)."""
    out, run = [], None
    steps = sorted(positions[c])
    for i, s in enumerate(steps):
        if i > 0 and positions[c][s][:2] == positions[c][steps[i - 1]][:2]:
            if run is None:
                run = [steps[i - 1], s]
            else:
                run[1] = s
        else:
            if run is not None:
                out.append((run[0], run[1], positions[c][run[0]][3], positions[c][run[0]][4]))
            run = None
    if run is not None:
        out.append((run[0], run[1], positions[c][run[0]][3], positions[c][run[0]][4]))
    return out

def forgiven(c, step):
    """Σ excess of live non-truth hypotheses at `step` (what a reset-without-fold there drops)."""
    truth = trace[c].get(step, {}).get("truth")
    return sum(v for h, v in excess.get((c, step), {}).items() if h != truth)

def fires(c):
    out = {}
    ret = [(int(r["step"]), r["hypothesis"], r["human_micro"]) for r in completions if r["condition"] == c]
    out["A_phase"] = [s for s, h, mu in ret if is_terminal(expected[(c, s - 1)].get(h, ""))]
    out["A_release"] = [s for s, h, mu in ret if mu == "release"]
    adv_ticks = sorted({int(r["step"]) for r in advances if r["condition"] == c})
    out["B"] = sorted({next((a for a in adv_ticks if a >= s), None) for s, _, _ in ret} - {None})
    out["D"] = adv_ticks
    st = stops(c)
    out["stops"] = st
    for n in (2, 3, 5):
        out[f"C({n})"] = [a + n - 1 for a, b, _, _ in st if b - a + 1 >= n]
    out["retirements"] = ret
    return out

def main():
    grand = defaultdict(lambda: [0, 0, 0.0])
    for c in CONDS:
        f = fires(c); tb = truth_boundaries(c)
        print(f"\n## {c}  truth boundaries (task/segment change, first tick of the new one): {tb}")
        print("   retirements (step:hyp/micro): " + ", ".join(f"{s}:{h}/{mu or 'idle'}" for s, h, mu in f["retirements"]))
        print("   stops (start–end, length, human action/micro at start): " +
              ", ".join(f"{a}–{b} ({b - a + 1}, {act}/{mu})" for a, b, act, mu in f["stops"]))
        for cand in ("A_phase", "A_release", "B", "C(2)", "C(3)", "C(5)", "D"):
            ticks = f[cand]
            rows = []
            for t in ticks:
                near = any(abs(t - b) <= 2 for b in tb)
                fg = forgiven(c, t)
                rows.append((t, near, fg))
                grand[cand][0] += 1; grand[cand][1] += near; grand[cand][2] += 0 if near else fg
            desc = " ".join(f"{t}{'' if near else '✗'}({fg:.0f})" for t, near, fg in rows)
            print(f"   {cand:9s} n={len(ticks):3d} at-boundary={sum(1 for _, n, _ in rows if n):3d}  {desc}")
    print("\n## totals over the eight conditions: firings, at a boundary, excess (cm) forgiven by the off-boundary firings")
    for cand, (n, nb, fg) in grand.items():
        print(f"   {cand:9s} {n:4d} {nb:4d} {fg:10.0f}")

if __name__ == "__main__":
    main()
