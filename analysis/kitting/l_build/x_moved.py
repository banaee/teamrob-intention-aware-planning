#!/usr/bin/env python3
"""
X. Every moved number, tick by tick (L-build; TB.2b's script, its EXPOSED / TRUNCATED classes dropped: the L-build
changes are not confined to an interval). Per run (all 48 and the four supplementary runs, not grouped), the tick sets
of the statistics 1.5c and TB.2b reported, computed by the same code on PRE (the TB.2b logs) and POST (L-build), and
their difference: the ticks present on one side only. The cause of each moved set is read beside l_events.txt (the
run's L events: boundaries without a pin, L1; re-entries, L4; retractions and boundary fires, L2 (ii) and L5 B).

Statistics (truth lag-corrected, the record at t + 2, as in C and F; α ∈ {0.01, 0.05, 0.1}, the finding recomputed
from the logged tails):
  fx@α     false unexplained: the truth a COVERED task, the finding unexplained (C);
  ux@α     unexplained, whatever the truth (C's detections and false ones together);
  nonmem   the true hypothesis live (COVERED, not retired on t) and not a member (absent from the tails);
  unres    unresolved: lifecycle live, no member;
  abt@α    adequate-below-θ: the finding adequate, the true hypothesis a member with S = 1 and P below θ (F);
  bound    [IR-boundary] ticks;  pin  [IR-complete] ticks;  reent  [IR-reentry] ticks;
  exh      lifecycle exhausted;
  lone     lifecycle live with one live hypothesis (P > BELIEF_FLOOR in [IR-dist]), for TODO-117's case;
  admit    decisions whose [meta-proj] projection= is built (D).
Prints per run the per-statistic moved ticks (post-only +, pre-only -) as ranges with their class, then totals per
prior.
"""
from collections import defaultdict
from tdlib import runs, parse, parse_rec, truth, finding_at, label, retired, ALPHAS, LAG, THETA, FLOOR

STATS = ([f"fx@{a}" for a in ALPHAS] + [f"ux@{a}" for a in ALPHAS] + ["nonmem", "unres"]
         + [f"abt@{a}" for a in ALPHAS] + ["bound", "pin", "reent", "exh", "lone", "admit"])


def ranges(ts):
    out, start, prev = [], None, None
    for t in sorted(ts) + [None]:
        if start is not None and (t is None or t != prev + 1):
            out.append(f"{start}-{prev}" if prev != start else f"{start}")
            start = None
        if t is not None and start is None:
            start = t
        prev = t
    return ",".join(out)


def ticksets(path, recpath):
    log, rec = parse(path), parse_rec(recpath)
    s = {k: set() for k in STATS}
    for t, ir in log["ir"].items():
        tr = truth(log, rec, t, LAG)
        k = tr["key"]
        live = ir["lifecycle"] != "exhausted"
        for a in ALPHAS:
            f = finding_at(ir, a)
            if f == "unexplained":
                s[f"ux@{a}"].add(t)
                if tr["cov"] == "covered":
                    s[f"fx@{a}"].add(t)
            if (f == "adequate" and k is not None and ir["tails"].get(k) == 1.0
                    and log["dist"][t].get(k, 0) < THETA):
                s[f"abt@{a}"].add(t)
        if k is not None and live and not retired(log, k, t) and k not in ir["tails"]:
            s["nonmem"].add(t)
        if live and not ir["tails"]:
            s["unres"].add(t)
        if not live:
            s["exh"].add(t)
        if live and sum(1 for v in log["dist"][t].values() if v > FLOOR + 1e-9) == 1:
            s["lone"].add(t)
    s["bound"] = set(log["boundary"])
    s["pin"] = {st for st, _ in log["pins"]}
    s["reent"] = {st for st, _ in log["reentries"]}
    s["admit"] = {d["step"] for d in log["decisions"] if (d["proj"] or "").startswith("built")}
    return s, log["done"]


def main():
    print(__doc__)
    rs = runs() + runs(True)
    rs = [r for r in rs if r["prior"] == "on"] + [r for r in rs if r["prior"] == "off"]
    tot = {p: {k: [0, 0] for k in STATS} for p in ("on", "off")}   # post-only, pre-only
    for r in rs:
        pre, done = ticksets(r["pre"], r["prerec"])
        post, done_post = ticksets(r["post"], r["rec"])
        lines = []
        for k in STATS:
            plus, minus = post[k] - pre[k], pre[k] - post[k]
            t_ = tot[r["prior"]][k]
            t_[0] += len(plus); t_[1] += len(minus)
            if plus or minus:
                parts = []
                if plus:
                    parts.append(f"+{len(plus)} {ranges(plus)}")
                if minus:
                    parts.append(f"-{len(minus)} {ranges(minus)}")
                lines.append(f"    {k:9} {len(pre[k]):4} -> {len(post[k]):4}   " + "; ".join(parts))
        n = f"N={done}->{done_post}" if done != done_post else f"N={done if done is not None else '-'}"
        print(f"\n{r['set']}/{r['name']}  [{label(r)}]  {n} (declared)")
        print("\n".join(lines) if lines else "    no statistic moved")
    print("\n## totals: ticks added on POST / removed")
    for p in ("on", "off"):
        print(f"  prior {p}:")
        for k in STATS:
            a, m = tot[p][k]
            print(f"    {k:9} +{a}   -{m}")


if __name__ == "__main__":
    main()
