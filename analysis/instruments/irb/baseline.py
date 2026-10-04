#!/usr/bin/env python3
"""
baseline.py — the delay to the threshold, per true stretch, over a domain's IRB set (reporting only; 2 October
2026, the mixed step of the IRB on dock_loading). From the existing outputs of each scenario (trajectory.json,
actual.csv, its run log); nothing is recomputed.

A true stretch is summary.py's: a contiguous run of ticks on which the human's action belongs to one task whose
[coverage] value is `covered`, the truth being that task's hypothesis key (unmodelled tasks and the idle human have
none). Per stretch: its length in ticks; the live hypotheses at its first tick (the keys actual.csv holds there); and
the delay, ticks from its first tick to the first on which the true hypothesis's belief over H (`belief_h`, the value
the gate reads; T-K part 1, AM42) is at or above θ (from the run's [run] header), or "never" within the stretch; a
truth outside the support is marked so.

    baseline.py <set dir> [<set dir> ...]       prints one markdown table per room, then the summary counts
"""
import csv
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import summary as S


def stretches(d, log):
    d = Path(d)
    S.SCHEMAS.update(S.schemas_of(log))
    THETA = S.header(log)[0]
    traj = json.load(open(d / "trajectory.json"))
    act = [r for r in csv.DictReader(open(d / "actual.csv")) if int(r["tick"]) >= 0]
    by = {}
    for r in act:
        by.setdefault(int(r["tick"]), {})[r["key"]] = r
    support = json.load(open(d / "phases.json"))["space"]
    cov = S.coverage(log)
    task_of = {r["tick"]: r["task"] for r in traj["rows"] if r["tick"] >= 0}
    truth = {t: (S.hypothesis_key(k) if k and cov.get(k) == "covered" else None) for t, k in task_of.items()}
    out, cur = [], None
    for t in sorted(by):
        k = truth.get(t)
        if cur and cur[0] == k and cur[2] == t - 1:
            cur[2] = t
        else:
            cur = [k, t, t]
            out.append(cur)
    rows = []
    for k, a, b in out:
        if k is None:
            continue
        live = len([x for x in by[a] if x])
        if k not in support:
            rows.append(dict(key=k, start=a, length=b - a + 1, live=live, delay="outside the support"))
            continue
        hit = next((t for t in range(a, b + 1) if k in by[t] and float(by[t][k]["belief_h"]) >= THETA), None)   # AM42
        rows.append(dict(key=k, start=a, length=b - a + 1, live=live, delay="never" if hit is None else hit - a))
    return traj["layout"], traj["scenario"], rows


def main(dirs):
    per_room, allrows = {}, []
    for root in dirs:
        root = Path(root)
        for d in sorted(p for p in root.iterdir() if p.is_dir() and (p / "actual.csv").exists()):
            log = next((root / "runs").glob(f"*_{d.name}_on.log"))
            layout, sid, rows = stretches(d, log)
            per_room.setdefault(layout, []).append((sid, rows))
            allrows += rows
    for layout in sorted(per_room):
        print(f"### {layout}\n")
        print("| scenario | true stretch (start) | length | live at its start | ticks to θ |")
        print("|---|---|---|---|---|")
        for sid, rows in per_room[layout]:
            for r in rows:
                print(f"| {sid} | {S.short(r['key'])} ({r['start']}) | {r['length']} | {r['live']} | {r['delay']} |")
        print()
    scored = [r for r in allrows if r["delay"] != "outside the support"]
    hits = [r["delay"] for r in scored if r["delay"] != "never"]
    print(f"Stretches: {len(allrows)}; in the support {len(scored)}; at θ within the stretch {len(hits)}; "
          f"never {len(scored) - len(hits)}; outside the support {len(allrows) - len(scored)}. Delay to θ: median "
          f"{statistics.median(hits) if hits else '-'}, min {min(hits) if hits else '-'}, max {max(hits) if hits else '-'}.")


if __name__ == "__main__":
    main(sys.argv[1:])
