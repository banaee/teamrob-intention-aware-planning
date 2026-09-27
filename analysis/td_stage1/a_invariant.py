#!/usr/bin/env python3
"""
A. The R6 invariant on every tick of the 48 post-build runs (and the four supplementary ones), from [IR-dist] / [IR].

Per tick t, with the space K = the key set of the run's first [IR-dist] line, the support = K (prior off) or the
[IR-prior] known tasks plus every hypothesis of a PersonalTask schema (coffee_break, ac_activation; prior on), and
pinned(t) = (K - support) plus every key with an [IR-complete] at or before t, live(t) = K - pinned(t):
  A1 the [IR-dist] key set is K on every tick, and no key `unknown`;
  A2 every pinned key reads exactly BELIEF_FLOOR (0.001);
  A3 the live keys sum to 1 - |pinned|·FLOOR, within the logged rounding (3 decimals: 0.0005 per live key);
  A4 a retired (completed or inadmissible) key never re-enters: never most_likely, never a member (in tails), and at
     the floor on every later tick; no key completes twice;
  A5 lifecycle is exhausted iff live(t) is empty, and then most_likely none, confidence 0, no finding;
  A6 most_likely is a live key with the largest P, and confidence equals its P;
  A7 (the adequacy accounting) every member is live, every S in [0, 1], and the logged finding equals the finding
     recomputed from the logged tails at the run's α = 0.05.
Prints one line per run and every violation.
"""
import sys
from tdlib import runs, parse, key_of, finding_at, FLOOR

PERSONAL = ("coffee_break(", "ac_activation(")


def check(r):
    log = parse(r["post"])
    steps = sorted(log["dist"])
    K = set(log["dist"][steps[0]])
    support = K if log["prior"] == "off" else {k for k in K if k.startswith(PERSONAL)} | {key_of(t) for t in log["known"]}
    inadmissible = K - support
    v = []
    maxres = 0.0
    if set(log["ir"]) != set(log["dist"]):
        v.append("A1 [IR] and [IR-dist] steps differ")
    pins = [l.split()[2] for l in open(r["post"]) if l.startswith("[IR-complete]")]
    for k in {k for k in pins if pins.count(k) > 1}:
        v.append(f"A4 {k} completes {pins.count(k)} times")
    for t in steps:
        d, ir = log["dist"][t], log["ir"][t]
        if set(d) != K or "unknown" in d:
            v.append(f"A1 t={t} key set {sorted(set(d) ^ K)}")
        completed = {k for k, c in log["complete"].items() if c <= t}
        pinned = inadmissible | completed
        live = K - pinned
        for k in pinned:
            if d.get(k) != FLOOR:
                v.append(f"A2 t={t} pinned {k}={d.get(k)}")
            if ir["ml"] == k:
                v.append(f"A4 t={t} retired {k} is most_likely")
            if k in ir["tails"]:
                v.append(f"A4 t={t} retired {k} is a member")
        if live:
            s = sum(d[k] for k in live)
            res = abs(s - (1 - len(pinned) * FLOOR))
            maxres = max(maxres, res)
            if res > 0.0005 * len(live) + 1e-9:
                v.append(f"A3 t={t} live sum {s:.3f} against {1 - len(pinned) * FLOOR:.3f}")
            if ir["lifecycle"] != "live":
                v.append(f"A5 t={t} live set {len(live)} but lifecycle {ir['lifecycle']}")
            if ir["ml"] not in live:
                v.append(f"A6 t={t} most_likely {ir['ml']} not live")
            elif d[ir["ml"]] != max(d[k] for k in live) or abs(ir["conf"] - d[ir["ml"]]) > 1e-9:
                v.append(f"A6 t={t} most_likely {ir['ml']} P={d[ir['ml']]} conf={ir['conf']}")
            for k, S in ir["tails"].items():
                if k not in live or not 0.0 <= S <= 1.0:
                    v.append(f"A7 t={t} member {k} S={S}")
            if ir["finding"] != finding_at(ir, 0.05):
                v.append(f"A7 t={t} logged {ir['finding']} recomputed {finding_at(ir, 0.05)} tails={ir['tails']}")
        else:
            if ir["lifecycle"] != "exhausted" or ir["ml"] != "none" or ir["conf"] != 0.0 or ir["finding"] or ir["tails"]:
                v.append(f"A5 t={t} empty live set: lifecycle={ir['lifecycle']} ml={ir['ml']} finding={ir['finding']}")
    return len(steps), len(K), len(inadmissible), maxres, v


def main():
    total = bad = 0
    for supp in (False, True):
        print("# supplementary (not among the 48)" if supp else "# the 48 maintained runs")
        print(f"{'run':62} ticks |K| |inadm| max|res| violations")
        for r in runs(supp):
            n, nk, ni, res, v = check(r)
            total += n
            bad += len(v)
            print(f"{r['set'] + '/' + r['name']:62} {n:5} {nk:3} {ni:6} {res:8.4f} {len(v)}")
            for x in v[:20]:
                print("   ", x)
    print(f"ticks checked: {total}; violations: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
