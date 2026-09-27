#!/usr/bin/env python3
"""
C. Finding statistics per run and aggregated, at each α in {0.01, 0.05, 0.1}, recomputed from the logged tails.

FALSE UNEXPLAINED: ticks where the truth is a task on the stack with coverage COVERED (a modelled task with its
expected binding) and the finding is unexplained. Per run and per phase of the truth (the record's action: move_to#0
the walk to the object, pick_up#0, move_to#1 the carry walk, place#0, wait_at#0), as ticks and as phase instances
(a phase instance = one (task, action) run of consecutive ticks in the record; counted once if any tick in it reads
unexplained; the per-phase unit of α). Raw truth (the record at t) and lag-corrected (the record at t + 2).
Denominators: the modelled ticks and phase instances.

MISSED UNEXPLAINED: ticks on TASK_ABSENT and outside-support tasks after the shared prefix where the finding is not
unexplained. Neither occurs in the 48 runs nor in the four supplementary ones (B2, B3). BINDING_ABSENT, the one
unmodelled case measured (the supplementary wrong-table runs), is reported in its place. SHARED PREFIX: the part of
the wrong-table task whose actions the modelled hypothesis of the same item (the item to its designated table) also
expects, with the same targets: its walk to the item and its pick_up (the record's move_to#0 and pick_up#0). The
prefix ends on the first tick of the record's move_to#1, the carry walk to the other table (actions are aligned with
the body at lag 0). Cross-check from the evidence: the tick the item hypothesis's S first falls below the one-tick
latency value 0.8629 (C prints both).

DETECTION DELAY: from the record's switch tick (the `entered:` of the unmodelled task) and from the prefix end, to the
first unexplained tick, per α.
"""
from collections import defaultdict
from tdlib import runs, parse, parse_rec, truth, finding_at, ir_groups, label, ALPHAS, LAG

PHASES = ["move_to#0", "pick_up#0", "move_to#1", "place#0", "wait_at#0"]


def instances(rec):
    """Record tick -> phase-instance id: consecutive ticks with the same (top task, action)."""
    out, n, prev = {}, 0, None
    for t in sorted(rec):
        cur = (rec[t]["top"], rec[t]["action"])
        if cur != prev:
            n += 1
            prev = cur
        out[t] = n
    return out


def false_unexplained(r):
    log, rec = parse(r["post"]), parse_rec(r["rec"])
    inst = instances(rec)
    last = max(rec)
    res = {}
    for lag in (0, LAG):
        ticks = defaultdict(int)          # (phase) -> modelled ticks
        insts = defaultdict(set)          # (phase) -> instance ids
        fx = {a: defaultdict(int) for a in ALPHAS}
        fxi = {a: defaultdict(set) for a in ALPHAS}
        for t, ir in log["ir"].items():
            tr = truth(log, rec, t, lag)
            if tr["cov"] != "covered":
                continue
            ph = tr["action"]
            iid = inst[min(t + lag, last)]
            ticks[ph] += 1
            insts[ph].add(iid)
            for a in ALPHAS:
                if finding_at(ir, a) == "unexplained":
                    fx[a][ph] += 1
                    fxi[a][ph].add(iid)
        res[lag] = (ticks, insts, fx, fxi)
    return res


def main():
    print(__doc__)
    all48 = runs()
    gs = ir_groups(all48)
    gs = [g for g in gs if g[0]["prior"] == "on"] + [g for g in gs if g[0]["prior"] == "off"]

    for lag in (LAG, 0):
        print(f"\n## false unexplained per run, truth {'lag-corrected (t + 2)' if lag else 'raw (t)'}")
        print("   modelled ticks / phase instances; then per α: unexplained ticks / instances, and the phases they fall in")
        agg = {p: {a: [0, 0, 0, 0] for a in ALPHAS} for p in ("on", "off")}  # ticks, inst, fx ticks, fx inst
        for g in gs:
            r = g[0]
            ticks, insts, fx, fxi = false_unexplained(r)[lag]
            nt, ni = sum(ticks.values()), sum(len(v) for v in insts.values())
            cells = []
            for a in ALPHAS:
                ft, fi = sum(fx[a].values()), sum(len(v) for v in fxi[a].values())
                where = ",".join(f"{p}:{fx[a][p]}" for p in PHASES if fx[a][p])
                cells.append(f"α={a}: {ft}/{fi}" + (f" ({where})" if where else ""))
                for x in g:  # every run of the group counts in the aggregate
                    s = agg[r["prior"]][a]
                    s[0] += nt; s[1] += ni; s[2] += ft; s[3] += fi
            more = f"  [x{len(g)}]" if len(g) > 1 else ""
            print(f"  {label(r):34} {nt:4}/{ni:3}  " + "   ".join(cells) + more)
        print("  aggregate over the 48 runs (groups weighted by their size):")
        for p in ("on", "off"):
            print(f"    prior {p}: " + "   ".join(
                f"α={a}: {s[2]}/{s[0]} ticks ({100 * s[2] / s[0]:.2f}%), {s[3]}/{s[1]} instances ({100 * s[3] / s[1]:.2f}%)"
                for a, s in agg[p].items()))

    # per phase, aggregated over the 48 (lag-corrected)
    print("\n## false unexplained per phase, aggregated over the 48 runs, lag-corrected truth: ticks / instances")
    for p in ("on", "off"):
        tot = {ph: [0, 0] for ph in PHASES}
        fx = {a: {ph: [0, 0] for ph in PHASES} for a in ALPHAS}
        for r in all48:
            if r["prior"] != p:
                continue
            ticks, insts, f, fi = false_unexplained(r)[LAG]
            for ph in PHASES:
                tot[ph][0] += ticks[ph]; tot[ph][1] += len(insts[ph])
                for a in ALPHAS:
                    fx[a][ph][0] += f[a][ph]; fx[a][ph][1] += len(fi[a][ph])
        print(f"  prior {p}:")
        for ph in PHASES:
            print(f"    {ph:10} {tot[ph][0]:6} ticks {tot[ph][1]:4} instances   " +
                  "   ".join(f"α={a}: {fx[a][ph][0]}/{fx[a][ph][1]}" for a in ALPHAS))

    # missed unexplained and detection delay: BINDING_ABSENT, supplementary runs
    print("\n## missed unexplained and detection delay: TASK_ABSENT and outside-support ticks: none (B2, B3).")
    print("   BINDING_ABSENT in its place (the supplementary wrong-table runs), lag-corrected truth for the task span")
    for r in runs(True):
        log, rec = parse(r["post"]), parse_rec(r["rec"])
        ba = [t for t in sorted(rec) if rec[t]["top"] and log["coverage"].get(rec[t]["top"], "").startswith("binding_absent")]
        task = rec[ba[0]]["top"]
        switch = next(t for t in sorted(rec) if f"entered:{task}" in rec[t]["events"])
        prefix_end = next(t for t in ba if rec[t]["action"] == "move_to#1")
        item_key = "deliver_item(?item=" + task.split("?item=")[1].split(",")[0] + ")"
        ev_end = next((t for t in sorted(log["ir"]) if t >= prefix_end - 2
                       and log["ir"][t]["tails"].get(item_key, 1.0) < 0.8629), None)
        span = [t for t in sorted(log["ir"]) if truth(log, rec, t, LAG)["cov"].startswith("binding_absent")]
        after = [t for t in span if t >= prefix_end]
        print(f"  {label(r)}: task {task}; switch (record) {switch}; prefix end {prefix_end} (record move_to#1), "
              f"evidence cross-check {ev_end}; unmodelled span after the prefix {after[0]}-{after[-1]} ({len(after)} ticks)")
        for a in ALPHAS:
            missed = [t for t in after if finding_at(log["ir"][t], a) != "unexplained"]
            first = next((t for t in after if finding_at(log["ir"][t], a) == "unexplained"), None)
            print(f"    α={a}: missed {len(missed)}/{len(after)} ({100 * len(missed) / len(after):.1f}%); first unexplained "
                  f"{first}; delay from switch {first - switch if first is not None else '-'}, "
                  f"from prefix end {first - prefix_end if first is not None else '-'}")


if __name__ == "__main__":
    main()
