#!/usr/bin/env python3
"""
X. Every moved number, tick by tick (IRB.2b; TODO-121). Per run (all 48 and the four supplementary runs, not grouped),
the tick sets of the statistics 1.5c reported, computed by the same code on PRE (the 1.5c logs) and POST (IRB.2b), and
their difference: the ticks present on one side only, each marked EXPOSED (after the run's declared completion tick N,
from the PRE log's `[meta] step=N all tasks complete`) or TRUNCATED (at or before N; none expected: the regeneration
criterion, `baseline_diff.txt`, has the [IR*] lines identical up to N). Runs whose robot never completes have no
exposed interval.

Statistics (truth lag-corrected, the record at t + 2, as in C and F; α ∈ {0.01, 0.05, 0.1}, the finding recomputed
from the logged tails):
  fx@α     false unexplained: the truth a COVERED task, the finding unexplained (C);
  ux@α     unexplained, whatever the truth (C's detections and false ones together);
  nonmem   the true hypothesis live (COVERED, not completed at or before t) and not a member (absent from the tails);
  unres    unresolved: lifecycle live, no member;
  abt@α    adequate-below-θ: the finding adequate, the true hypothesis a member with S = 1 and P below θ (F);
  bound    [IR-boundary] ticks;  pin  [IR-complete] ticks;
  exh      lifecycle exhausted;
  lone     lifecycle live with one live hypothesis (P > BELIEF_FLOOR in [IR-dist]), for TODO-117's case;
  admit    decisions whose [meta-proj] projection= is built (D).
Prints per run the per-statistic moved ticks (post-only +, pre-only -) as ranges with their class, then totals per
prior.
"""
from collections import defaultdict
from tdlib import runs, parse, parse_rec, truth, finding_at, label, ALPHAS, LAG, THETA, FLOOR

STATS = ([f"fx@{a}" for a in ALPHAS] + [f"ux@{a}" for a in ALPHAS] + ["nonmem", "unres"]
         + [f"abt@{a}" for a in ALPHAS] + ["bound", "pin", "exh", "lone", "admit"])


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
        if k is not None and live and log["complete"].get(k, 10 ** 9) > t and k not in ir["tails"]:
            s["nonmem"].add(t)
        if live and not ir["tails"]:
            s["unres"].add(t)
        if not live:
            s["exh"].add(t)
        if live and sum(1 for v in log["dist"][t].values() if v > FLOOR + 1e-9) == 1:
            s["lone"].add(t)
    s["bound"] = set(log["boundary"])
    s["pin"] = set(log["complete"].values())
    s["admit"] = {d["step"] for d in log["decisions"] if (d["proj"] or "").startswith("built")}
    return s, log["done"]


def main():
    print(__doc__)
    rs = runs() + runs(True)
    rs = [r for r in rs if r["prior"] == "on"] + [r for r in rs if r["prior"] == "off"]
    tot = {p: {k: [0, 0, 0] for k in STATS} for p in ("on", "off")}   # post-only exposed, post-only truncated, pre-only
    for r in rs:
        pre, done = ticksets(r["pre"], r["prerec"])
        post, _ = ticksets(r["post"], r["rec"])
        lines = []
        for k in STATS:
            plus, minus = post[k] - pre[k], pre[k] - post[k]
            exp = {t for t in plus if done is not None and t > done}
            trunc = plus - exp
            t_ = tot[r["prior"]][k]
            t_[0] += len(exp); t_[1] += len(trunc); t_[2] += len(minus)
            if plus or minus:
                parts = []
                if exp:
                    parts.append(f"+{len(exp)} EXPOSED {ranges(exp)}")
                if trunc:
                    parts.append(f"+{len(trunc)} TRUNCATED {ranges(trunc)}")
                if minus:
                    parts.append(f"-{len(minus)} {ranges(minus)}")
                lines.append(f"    {k:9} {len(pre[k]):4} -> {len(post[k]):4}   " + "; ".join(parts))
        n = f"N={done}" if done is not None else "N=- (never completes)"
        print(f"\n{r['set']}/{r['name']}  [{label(r)}]  {n}")
        print("\n".join(lines) if lines else "    no statistic moved")
    print("\n## totals: ticks added on POST in the exposed interval / added at or before N / removed")
    for p in ("on", "off"):
        print(f"  prior {p}:")
        for k in STATS:
            e, tr, m = tot[p][k]
            print(f"    {k:9} +{e} exposed   +{tr} truncated   -{m}")


if __name__ == "__main__":
    main()
