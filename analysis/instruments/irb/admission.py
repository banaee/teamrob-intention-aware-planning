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
- θ: the first tick with the true hypothesis's belief over H (`belief_h`, the value the gate reads; T-K part 1, AM42)
  at or above θ, and its delay from the stretch's start;
- admitted: the first tick on which the gate clears with the true hypothesis leading (the idle robot asks admission at
  tick 0 only; the gate per tick is what admission would answer on that tick, as in summary.py's gate table);
- after admission: the ticks of the stretch, from the admission to the true hypothesis's pin (its task's completion,
  the `pins` column) or the stretch's end, on which the gate no longer clears for the true hypothesis (the retraction
  reading), each run of ticks with its outcome and leader;
- other admissions: the ticks of the stretch on which the gate clears with another hypothesis leading.
Since T-K part 1's build stage 6 (KT10, KT14), two columns: the state the case meets, read on the stretch's first tick
from the `levels` column (a foreseeable task's own level; for an assigned task the levels of its foreseeable rivals);
and, for an ac_activation stretch, the A/C hypothesis's belief over H (`belief_h`) at its arrival (its wait is one
tick, so admission is not the informative measure, KT10). The state reads "-" with context knowledge off (no levels).
CORRECTED (T-K part 1, step 4, 4 October 2026): the arrival is the tick before the first tick of its switch_on in the
trajectory, the move's last tick (Hadi's completion minus the wait); on switch_on's first tick the hypothesis is
already retired by its pin and has no belief. It is read with context knowledge off too.
ADDED (step 4, Hadi: P8 part of the measure): a second table, every admission of a hypothesis that is not the true
task, on any tick, the unmodelled ones (the exit walk) included: each run of consecutive ticks on which the gate
clears with the same hypothesis leading and that hypothesis is not the true one, the true task(s) on those ticks, and
how the run ends: "retraction at t (outcome)" when on the next tick the gate no longer clears for it and the human is
not doing it; "the human starts it at t" when the next tick's true task is that hypothesis; "then X" when the gate
clears for another hypothesis; "to the run's end". A true task pinned on or before the tick, within its stretch (its
terminal fact holds; the human still on the last action's ticks), is marked "(complete: pinned)".

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
            by.setdefault(t, {})[r["key"]] = float(r["belief_h"])     # the belief over H, the gate's value (AM42)
    # the arrival of each switch_on: the tick before the first tick of the action in the trajectory, per task (KT10;
    # on the switch_on's first tick the hypothesis is retired by its pin, step 4's correction)
    arrival = {}
    for b in traj["actions"]:
        if b["action"] == "switch_on":
            arrival.setdefault(b["task"], b["tick"] - 1)
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
        levels = dict(x.split("=") for x in tick_row[a].get("levels", "").split())
        name = k.split("(")[0]
        state = levels.get(name) if name in levels else " ".join(f"{n} {v}" for n, v in sorted(levels.items()))
        task_key = next((tk for tk in arrival if S.hypothesis_key(tk) == k), None)
        at_arrival = (f"{by[arrival[task_key]].get(k, float('nan')):.4f} at {arrival[task_key]}"
                      if task_key is not None and arrival[task_key] in by else None)
        out.append(dict(key=k, a=a, b=b, hit=hit, adm=adm, after=after, other=other, state=state or None,
                        at_arrival=at_arrival))
    return traj["scenario"], traj["layout"], sorted(out, key=lambda r: r["a"])


def wrong_admissions(d, name):
    """Every run of ticks on which the gate clears with a hypothesis leading that is not the true task (step 4, P8)."""
    traj = json.load(open(d / "trajectory.json"))
    truth = {r["tick"]: (S.hypothesis_key(r["task"]) if r["task"] else None) for r in traj["rows"] if r["tick"] >= 0}
    rows = {}
    for r in csv.DictReader(open(d / name)):
        t = int(r["tick"])
        if t >= 0:
            rows.setdefault(t, r)                       # gate and leader are per tick, repeated per hypothesis row
    wrong = lambda t: (t in rows and rows[t]["gate"] == "clears" and rows[t]["most_likely"] != truth.get(t))
    out, t, last = [], 0, max(rows)
    while t <= last:
        if not wrong(t):
            t += 1
            continue
        h, a = rows[t]["most_likely"], t
        while t + 1 <= last and wrong(t + 1) and rows[t + 1]["most_likely"] == h:
            t += 1
        b, nxt = t, t + 1
        if nxt > last:
            end = "to the run's end"
        elif truth.get(nxt) == h:
            end = f"the human starts it at {nxt}"
        elif rows[nxt]["gate"] == "clears":
            end = f"then {S.short(rows[nxt]['most_likely'])} at {nxt}"
        else:
            end = f"retraction at {nxt} ({rows[nxt]['gate']})"
        true = []
        for u in range(a, b + 1):
            k = S.short(truth.get(u)) if truth.get(u) else "unmodelled"
            if truth.get(u) and any(truth[u] in rows[p]["pins"].split(";") for p in range(u, -1, -1)
                                    if p in rows and all(truth.get(q) == truth[u] for q in range(p, u + 1))):
                k += " (complete: pinned)"     # pinned on or before the tick, the human still on its last action
            if not true or true[-1] != k:
                true.append(k)
        out.append(dict(h=h, a=a, b=b, true=", ".join(true), end=end))
        t += 1
    return traj["scenario"], out


def main(root, name, theta, domain="kitting"):
    root = Path(root)
    S.SCHEMAS.update({s.name: s for s in importlib.import_module(f"domains.{domain}.registry").domain_config["task_model"]})
    print(f"From `{name}`, θ = {theta:g}. Ticks inclusive; delay from the stretch's first tick in brackets.\n")
    print("| scenario | true hypothesis | ticks | first ≥ θ | admitted | after admission (not clearing for it) | other admissions | state at start (levels) | A/C belief at arrival |")
    print("|---|---|---|---|---|---|---|---|---|")
    for d in sorted(p for p in root.iterdir() if p.is_dir() and (p / name).exists()):
        sid, _, rows = stretches(d, name, theta)
        for r in rows:
            hit = "never" if r["hit"] is None else f"{r['hit']} ({r['hit'] - r['a']})"
            adm = "never" if r["adm"] is None else f"{r['adm']} ({r['adm'] - r['a']})"
            print(f"| {sid.removeprefix('scenario_')} | {S.short(r['key'])} | {r['a']} to {r['b']} | {hit} | {adm} | "
                  f"{fmt_runs(r['after'])} | {fmt_runs(r['other'])} | {r['state'] or '-'} | {r['at_arrival'] or '-'} |")
    print("\nAdmissions of a hypothesis that is not the true task (every tick, the unmodelled ones included).\n")
    print("| scenario | hypothesis admitted | ticks | true task on those ticks | how it ends |")
    print("|---|---|---|---|---|")
    for d in sorted(p for p in root.iterdir() if p.is_dir() and (p / name).exists()):
        sid, rows = wrong_admissions(d, name)
        for r in rows:
            ticks = f"{r['a']}" if r["a"] == r["b"] else f"{r['a']} to {r['b']}"
            print(f"| {sid.removeprefix('scenario_')} | {S.short(r['h'])} | {ticks} | "
                  f"{r['true']} | {r['end']} |")


if __name__ == "__main__":
    args, domain = sys.argv[1:], "kitting"
    if "--domain" in args:                 # T-K part 1, step 6: the run's domain (kitting by default)
        i = args.index("--domain"); domain = args[i + 1]; args = args[:i] + args[i + 2:]
    main(args[0], args[1], float(args[2]), domain)
