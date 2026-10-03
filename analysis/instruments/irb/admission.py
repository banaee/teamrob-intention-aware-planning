#!/usr/bin/env python3
"""
admission.py — per true stretch, when the true hypothesis reaches the threshold and when the gate admits it, and what
follows (reporting only; 3 October 2026, T-K part 1's round without context knowledge: the measure of
design_records.md, "T-K", CONTENT POINT 3, KT3). Read from a scenario's existing outputs, nothing recomputed: either
`expected.csv` (the oracle, before the run) or `actual.csv` (the recognizer, after it); both carry per tick the
leader (`most_likely`), the gate's outcome (`gate`) and per hypothesis the belief.

A true stretch is a contiguous run of ticks on which the human's action belongs to one task of the robot's task model
(the trajectory's task, as a hypothesis key); the exit walk and the idle human have none. The scripts this is written
for hold modelled tasks only, so this is summary.py's stretch without its [coverage] reading, and it needs no run log.
Per stretch:
- θ: the first tick with the true hypothesis's belief at or above θ, and its delay from the stretch's start;
- admitted: the first tick on which the gate clears with the true hypothesis leading (the idle robot asks admission at
  tick 0 only; the gate per tick is what admission would answer on that tick, as in summary.py's gate table);
- after admission: the ticks of the stretch, from the admission to the true hypothesis's pin (its task's completion,
  the `pins` column) or the stretch's end, on which the gate no longer clears for the true hypothesis (the retraction
  reading), each run of ticks with its outcome and leader;
- other admissions: the ticks of the stretch on which the gate clears with another hypothesis leading.

    admission.py <set dir> <csv name> <theta>      e.g. admission.py analysis/kitting/irb/tk1 expected.csv 0.75
"""
import csv
import importlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import summary as S


def runs_of(ticks):
    """Contiguous runs of a sorted tick list, as (first, last)."""
    out = []
    for t in ticks:
        if out and out[-1][1] == t - 1:
            out[-1][1] = t
        else:
            out.append([t, t])
    return out


def fmt_runs(items):
    """items: [(tick, label)] -> 'a to b label; ...', merging equal labels on consecutive ticks."""
    out = []
    for t, lab in items:
        if out and out[-1][1] == t - 1 and out[-1][2] == lab:
            out[-1][1] = t
        else:
            out.append([t, t, lab])
    return "; ".join(f"{a}{'' if a == b else f' to {b}'} {lab}" for a, b, lab in out) or "-"


def stretches(d, name, theta):
    traj = json.load(open(d / "trajectory.json"))
    by, tick_row = {}, {}
    for r in csv.DictReader(open(d / name)):
        t = int(r["tick"])
        if t < 0:
            continue
        tick_row[t] = r
        if r["key"]:
            by.setdefault(t, {})[r["key"]] = float(r["belief"])
    truth = {r["tick"]: (S.hypothesis_key(r["task"]) if r["task"] else None) for r in traj["rows"] if r["tick"] >= 0}
    out = []
    for k, (a, b) in ((k, ab) for k in set(truth.values()) if k
                      for ab in runs_of(sorted(t for t, v in truth.items() if v == k))):
        span = [t for t in range(a, b + 1) if t in tick_row]
        hit = next((t for t in span if by.get(t, {}).get(k, 0.0) >= theta), None)
        adm = next((t for t in span if tick_row[t]["gate"] == "clears" and tick_row[t]["most_likely"] == k), None)
        pin = next((t for t in span if k in tick_row[t]["pins"].split(";")), b + 1)
        after = [] if adm is None else [
            (t, f"{tick_row[t]['gate']} ({S.short(tick_row[t]['most_likely'])})") for t in span
            if adm < t < pin and not (tick_row[t]["gate"] == "clears" and tick_row[t]["most_likely"] == k)]
        other = [(t, S.short(tick_row[t]["most_likely"])) for t in span
                 if tick_row[t]["gate"] == "clears" and tick_row[t]["most_likely"] != k]
        out.append(dict(key=k, a=a, b=b, hit=hit, adm=adm, after=after, other=other))
    return traj["scenario"], traj["layout"], sorted(out, key=lambda r: r["a"])


def main(root, name, theta):
    root = Path(root)
    S.SCHEMAS.update({s.name: s for s in importlib.import_module("domains.kitting.registry").domain_config["task_model"]})
    print(f"From `{name}`, θ = {theta:g}. Ticks inclusive; delay from the stretch's first tick in brackets.\n")
    print("| scenario | true hypothesis | ticks | first ≥ θ | admitted | after admission (not clearing for it) | other admissions |")
    print("|---|---|---|---|---|---|---|")
    for d in sorted(p for p in root.iterdir() if p.is_dir() and (p / name).exists()):
        sid, _, rows = stretches(d, name, theta)
        for r in rows:
            hit = "never" if r["hit"] is None else f"{r['hit']} ({r['hit'] - r['a']})"
            adm = "never" if r["adm"] is None else f"{r['adm']} ({r['adm'] - r['a']})"
            print(f"| {sid.removeprefix('scenario_')} | {S.short(r['key'])} | {r['a']} to {r['b']} | {hit} | {adm} | "
                  f"{fmt_runs(r['after'])} | {fmt_runs(r['other'])} |")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]))
