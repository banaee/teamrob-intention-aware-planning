#!/usr/bin/env python3
"""
X summary. Per run (prior on first): the declared completion tick N, the exposed span N+1..last, the ticks the moved
statistics gained there (unexplained at α = 0.05, exhausted, lone live hypothesis; definitions in x_moved.py), and the
lone live hypothesis in the exposed interval. Runs whose robot never completes print N = -.
"""
from x_moved import ticksets
from tdlib import runs, parse, label

rs = runs() + runs(True)
rs = [r for r in rs if r["prior"] == "on"] + [r for r in rs if r["prior"] == "off"]
print(f"{'run':52} {'N':>4} {'exposed':>9} {'ux@.05 +':>9} {'exh +':>6} {'lone +':>7}  lone live hypothesis (exposed)")
for r in rs:
    pre, done = ticksets(r["pre"], r["prerec"])
    post, _ = ticksets(r["post"], r["rec"])
    name = r["set"][:4] + "/" + label(r)
    if done is None:
        print(f"{name:52} {'-':>4} {'-':>9}")
        continue
    log = parse(r["post"])
    add = lambda k: len(post[k] - pre[k])
    lone = {log["ir"][t]["ml"] for t in post["lone"] - pre["lone"]}
    span = f"{done + 1}-{max(log['ir'])}"
    print(f"{name:52} {done:>4} {span:>9} {add('ux@0.05'):>9} {add('exh'):>6} {add('lone'):>7}  {','.join(sorted(lone)) or '-'}")
