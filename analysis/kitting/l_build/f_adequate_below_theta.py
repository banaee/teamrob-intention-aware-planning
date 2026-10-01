#!/usr/bin/env python3
"""
F. The adequate-below-θ pattern: ticks where the finding is adequate, the true hypothesis (the lag-corrected truth's)
is a member with S = 1, and its belief is below θ (0.75). Per run (IR-identical runs once), at each α (the finding
is recomputed per α; the member condition does not depend on α), split by the phase the human is in (the record's
action at t: wait_at, pick_up, place, move_to), with the ticks as ranges and the rival that holds the belief.
"""
from collections import defaultdict
from tdlib import runs, parse, parse_rec, truth, finding_at, ir_groups, label, ALPHAS, THETA, LAG


def ranges(ts):
    out, start, prev = [], None, None
    for t in ts + [None]:
        if start is not None and (t is None or t != prev + 1):
            out.append(f"{start}-{prev}" if prev != start else f"{start}")
            start = None
        if t is not None and start is None:
            start = t
        prev = t
    return ",".join(out)


def main():
    print(__doc__)
    gs = ir_groups(runs())
    gs = [g for g in gs if g[0]["prior"] == "on"] + [g for g in gs if g[0]["prior"] == "off"]
    tot = {p: {a: defaultdict(int) for a in ALPHAS} for p in ("on", "off")}
    for g in gs:
        r = g[0]
        log, rec = parse(r["post"]), parse_rec(r["rec"])
        hits = {a: defaultdict(list) for a in ALPHAS}
        leaders = defaultdict(set)
        for t, ir in sorted(log["ir"].items()):
            k = truth(log, rec, t, LAG)["key"]
            if k is None or ir["tails"].get(k) != 1.0 or log["dist"][t].get(k, 0) >= THETA:
                continue
            ph = (rec[t]["action"] or "-").split("#")[0]
            for a in ALPHAS:
                if finding_at(ir, a) == "adequate":
                    hits[a][ph].append(t)
            if ir["ml"] != k:
                leaders[ph].add(ir["ml"].split("=")[-1].rstrip(")"))
        if not any(hits[a] for a in ALPHAS):
            continue
        print(f"\n{label(r)}" + (f"  [x{len(g)}]" if len(g) > 1 else ""))
        for ph in sorted(set().union(*[hits[a].keys() for a in ALPHAS])):
            n = [len(hits[a][ph]) for a in ALPHAS]
            for a, x in zip(ALPHAS, n):
                tot[r["prior"]][a][ph] += x * len(g)
            print(f"  {ph:8} ticks α=.01/.05/.10: {n[0]}/{n[1]}/{n[2]}  at {ranges(hits[0.05][ph])}"
                  + (f"  leader elsewhere: {','.join(sorted(leaders[ph]))}" if leaders[ph] else ""))
    print("\nTotals over the 48 runs (groups weighted by size), ticks by phase, α=.01/.05/.10:")
    for p in ("on", "off"):
        phs = sorted(set().union(*[tot[p][a].keys() for a in ALPHAS]))
        print(f"  prior {p}: " + "; ".join(f"{ph} {tot[p][0.01][ph]}/{tot[p][0.05][ph]}/{tot[p][0.1][ph]}" for ph in phs))


if __name__ == "__main__":
    main()
