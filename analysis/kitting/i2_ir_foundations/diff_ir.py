#!/usr/bin/env python3
"""
diff_ir.py — attribute belief differences between two run logs, tick by tick.

usage: diff_ir.py BASE.log NEW.log [--eps 0.0005]

Parses [IR-dist] lines (full distribution per tick) and the per-step human
state lines run_mesa.py writes, and prints:
  1. t=0 winner and distribution in both logs;
  2. every tick where most_likely differs;
  3. episodes: maximal runs of consecutive ticks whose set of keys with
     |new - base| > eps is the same, with the human's action/microaction/
     holding at the episode start and the largest change per key;
  4. [meta] / [meta-proj] / [meta-cand] line diffs.
Pure text; no simulator import. Used for the I2 report (REPORT.md).
"""
import re, sys
from collections import OrderedDict

DIST = re.compile(r"^\[IR-dist\] step=(\d+) most_likely=(\S+) confidence=([\d.]+) dist=\[(.*)\]$")
STEP = re.compile(r"^\s+step: (\d+): \[(\w+)\] task=(\S+) action=(\S+) micro=(\S+) pos=\[(.*?)\]")
HOLD = re.compile(r"holding\(human_0, (\S+)\)")

def parse(path):
    dists, human, holding, meta = {}, {}, {}, []
    for line in open(path):
        m = DIST.match(line)
        if m:
            step = int(m.group(1))
            d = OrderedDict()
            for kv in m.group(4).split("  "):
                k, v = kv.rsplit("=", 1)
                d[k] = float(v)
            dists[step] = (m.group(2), float(m.group(3)), d)
            continue
        m = STEP.match(line)
        if m and m.group(2) == "human_0":
            human[int(m.group(1))] = (m.group(3), m.group(4), m.group(5))
            continue
        if line.startswith("[meta]") or line.startswith("[meta-proj]") or line.startswith("[meta-cand]"):
            meta.append(line.rstrip())
    return dists, human, meta

def short(k):
    k = k.replace("deliver_item(?item=", "d(").replace(",?kitting_table=kitting_table_0)", ")")
    k = k.replace("coffee_break(?coffee_machine=coffee_machine_0)", "coffee")
    k = k.replace("ac_activation(?ac_switch=ac_switch_0)", "ac")
    return k

def main():
    eps = 0.0005
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--eps" in sys.argv:
        eps = float(sys.argv[sys.argv.index("--eps") + 1])
    base, human_b, meta_b = parse(args[0])
    new, human_n, meta_n = parse(args[1])
    steps = sorted(set(base) | set(new))
    print(f"ticks: base {len(base)} new {len(new)}  eps={eps}")
    if human_b != human_n:
        print("HUMAN STATE LINES DIFFER between runs (sim side changed)")
    for s in [steps[0]]:
        for tag, src in (("base", base), ("new", new)):
            ml, conf, d = src[s]
            print(f"t={s} {tag}: most_likely={short(ml)} conf={conf:.3f} dist=" +
                  " ".join(f"{short(k)}={v:.3f}" for k, v in d.items()))
    print("\n== most_likely differences ==")
    ml_diff = [s for s in steps if s in base and s in new and base[s][0] != new[s][0]]
    for s in ml_diff:
        hb = human_n.get(s, ("?", "?", "?"))
        print(f"  t={s:3d} base={short(base[s][0])}({base[s][1]:.3f}) new={short(new[s][0])}({new[s][1]:.3f})  human: {hb[0]}/{hb[1]}/{hb[2]}")
    if not ml_diff:
        print("  none")
    print("\n== changed-key episodes (|new-base| > eps) ==")
    episodes = []
    cur = None
    for s in steps:
        if s not in base or s not in new:
            continue
        db, dn = base[s][2], new[s][2]
        changed = tuple(sorted(k for k in set(db) | set(dn) if abs(dn.get(k, 0) - db.get(k, 0)) > eps))
        if cur and cur["keys"] == changed and cur["end"] == s - 1:
            cur["end"] = s
            for k in changed:
                delta = dn.get(k, 0) - db.get(k, 0)
                if abs(delta) > abs(cur["max"][k][0]):
                    cur["max"][k] = (delta, s, db.get(k, 0), dn.get(k, 0))
        else:
            if cur:
                episodes.append(cur)
            cur = {"start": s, "end": s, "keys": changed,
                   "max": {k: (dn.get(k, 0) - db.get(k, 0), s, db.get(k, 0), dn.get(k, 0)) for k in changed},
                   "human": human_n.get(s, ("?", "?", "?"))}
    if cur:
        episodes.append(cur)
    for e in episodes:
        if not e["keys"]:
            print(f"  t={e['start']}-{e['end']}: identical")
            continue
        h = e["human"]
        print(f"  t={e['start']}-{e['end']} human@start {h[0]}/{h[1]}/{h[2]}:")
        for k in e["keys"]:
            delta, s, vb, vn = e["max"][k]
            print(f"      {short(k):<12} max Δ={delta:+.3f} at t={s} ({vb:.3f} → {vn:.3f})")
    print("\n== meta lines ==")
    if meta_b == meta_n:
        print("  identical")
    else:
        import difflib
        for line in difflib.unified_diff(meta_b, meta_n, lineterm="", n=0):
            if line.startswith(("---", "+++", "@@")):
                continue
            print("  " + line)

if __name__ == "__main__":
    main()
