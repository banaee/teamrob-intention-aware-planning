#!/usr/bin/env python3
"""
chain.py — the causal chain per tick for one hypothesis over one stretch of scenario_40, from
excess.csv and trace.csv (written by check_i4.py --final): excess path (cm), the movement likelihood
it produced, the hypothesis's evidence base and posterior, the strongest competitor, P(unknown).

  chain.py <condition-tag> <hypothesis> <first-step> <last-step> [--beta B]
  e.g. chain.py s40_on coffee 115 186 ; chain.py reset_boundary/s40_on d(item_6) 187 230
"""
import csv, math, sys
from pathlib import Path
HERE = Path(__file__).parent
tag, hyp, a, b = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
if "--dir" in sys.argv:                       # read another stage's excess.csv / trace.csv (I4b)
    HERE = Path(sys.argv[sys.argv.index("--dir") + 1]).resolve()
beta = float(sys.argv[sys.argv.index("--beta") + 1]) if "--beta" in sys.argv else None
if beta is None:
    sys.path.insert(0, str(HERE.parents[1]))
    from shared import likelihood_functions as LF
    beta = LF.BETA
ex = {}
for r in csv.DictReader(open(HERE / "excess.csv")):
    if r["condition"] == tag and a <= int(r["step"]) <= b:
        ex.setdefault(int(r["step"]), {})[r["hypothesis"]] = r
tr = {}
with open(HERE / "trace.csv") as f:
    rd = csv.reader(f); header = next(rd)
    for row in rd:
        if row[0] == tag and a <= int(row[1]) <= b:
            tr[int(row[1])] = row
# distribution columns: after the 9 fixed columns, in hypothesis order; recover the key order from excess.csv rows
hyp_order = None
print(f"| step | seg | human action | expected | excess cm | L | base | P({hyp}) | strongest other | P(unknown) |")
print("|---|---|---|---|---|---|---|---|---|---|")
prev = None
for s in sorted(tr):
    row = tr[s]; e = ex.get(s, {}).get(hyp)
    if e is None:
        continue
    exc = e["excess_cm"]
    L = f"{2.0 / (1.0 + math.exp(beta * float(exc))):.3f}" if exc != "" else "1 (no graded signal)"
    # strongest competitor: read all hypotheses' beliefs at this step from excess.csv (live keys) + unknown
    others = {k: float(r["belief"]) for k, r in ex[s].items() if k != hyp}
    # unknown is not in excess.csv (no expected action); the trace has confidence/most_likely only, so
    # read P(unknown) as 1 − Σ live beliefs − Σ pinned (0.001 each is implicit); approximate from trace's most_likely when unknown leads
    live_sum = sum(float(r["belief"]) for r in ex[s].values())
    p_unknown = max(0.0, 1.0 - live_sum)
    p_unknown_note = ""
    if others:
        k, v = max(others.items(), key=lambda kv: kv[1])
        comp = f"{k} {v:.3f}" if v > p_unknown else f"unknown {p_unknown:.3f}"
    else:
        comp = f"unknown {p_unknown:.3f}"
    print(f"| {s} | {row[2]} | {row[4]}/{row[5]} | {e['expected_action'][:22]} | {exc} | {L} | {float(e['base']):.2e} | {float(e['belief']):.3f} | {comp} | {p_unknown:.3f} |")
