#!/usr/bin/env python3
"""
B. The recognizer's outputs per ground-truth case of the record, against the truth (no oracle IR: TODO-101 is not
built; the truth is the record's stack and the loader's [coverage] value per script entry).

Runs are grouped by identical recognizer output and record (tdlib.ir_groups); one representative per group, the
group's other runs named. Prior on first. Ticks are [IR] steps. Truth "raw" is the record at t, "lag" the record at
t + 2 (the task transitions land 2 ticks after the world fact the recognizer reads).

Cases (the record's): B1 a switch to a modelled task (every applied Start whose task is COVERED: in these scripts
each entry of the script, the first on the empty stack); B2 a switch outside the support; B3 TASK_ABSENT;
B4 BINDING_ABSENT; B5 no task on the stack; B6 an episode's first ticks (step 0 and every [IR-boundary]).
Finding letters: A adequate, U unresolved, X unexplained, E exhausted (lifecycle), at α = 0.05 unless a column
names the level. A disagreement is a tick where the finding (at any α) contradicts the truth: X on a COVERED task
with its expected binding, or anything but X on a BINDING_ABSENT / TASK_ABSENT tick after the shared prefix (C
states the prefix). Every disagreement is listed with its members and their S.
"""
from tdlib import (runs, parse, parse_rec, truth, finding_at, ir_groups, key_of, label, ALPHAS, THETA, LAG)

L = {"adequate": "A", "unresolved": "U", "unexplained": "X", "exhausted": "E"}


def sk(k):
    """Short key for tables: item_3, coffee_break, ac_switch_0."""
    if k in (None, "none"):
        return "none"
    if k.startswith("deliver_item"):
        return k.split("=")[1].split(",")[0].rstrip(")")
    if k.startswith("coffee_break"):
        return "coffee"
    return k.split("=")[1].rstrip(")")


def tails_str(ir):
    return " ".join(f"{sk(k)}={v:.4f}" for k, v in sorted(ir["tails"].items())) or "-"


def state(ir, alpha=0.05):
    f = finding_at(ir, alpha)
    return f"{sk(ir['ml'])}({ir['conf']:.3f}) {L[f]}"


def groups_by_prior(rs):
    gs = ir_groups(rs)
    return [g for g in gs if g[0]["prior"] == "on"] + [g for g in gs if g[0]["prior"] == "off"]


def others(g):
    return (" = " + ", ".join(label(x) for x in g[1:])) if len(g) > 1 else ""


def switches(log, rec):
    """(record tick, task) for every `entered:` in the record, and its coverage value."""
    out = []
    for t in sorted(rec):
        for e in rec[t]["events"]:
            if e.startswith("entered:"):
                task = e[len("entered:"):]
                out.append((t, task, log["coverage"].get(task, "?")))
    return out


def main():
    all48 = runs()
    supp = runs(True)
    print(__doc__)

    # ---- B1: switches to a modelled task ----
    print("\n## B1 a switch to a modelled task: the window around each switch, world tick w = record tick - 2")
    print("columns: ticks w-1 .. w+3, each 'leader(confidence) finding'; the truth raw / lag at w and w+2")
    for g in groups_by_prior(all48):
        r = g[0]
        log, rec = parse(r["post"]), parse_rec(r["rec"])
        print(f"\n### {label(r)}{others(g)}")
        for rt, task, cov in switches(log, rec):
            if cov != "covered":
                continue
            w = max(rt - LAG, 0)
            cells = []
            for t in range(w - 1, w + 4):
                if t in log["ir"]:
                    cells.append(f"{t}:{state(log['ir'][t])}")
            tr_raw, tr_lag = truth(log, rec, w, 0), truth(log, rec, w, LAG)
            print(f"  switch rec={rt} -> {sk(key_of(task))}; at w={w} truth raw={sk(tr_raw['key'])}/{tr_raw['action']} "
                  f"lag={sk(tr_lag['key'])}/{tr_lag['action']}; boundary at w: {w in log['boundary']}")
            print("     " + " | ".join(cells))

    # ---- B2, B3 ----
    print("\n## B2 a switch outside the support, B3 TASK_ABSENT")
    n_out = n_ta = 0
    for r in all48 + supp:
        log = parse(r["post"])
        n_ta += sum(1 for v in log["coverage"].values() if v.startswith("task_absent"))
        if log["prior"] == "on":
            support = {key_of(t) for t in log["known"]}
            n_out += sum(1 for t, v in log["coverage"].items()
                         if v == "covered" and key_of(t) not in support
                         and not t.startswith(("coffee_break", "ac_activation")))
    print(f"  script entries outside the support (prior on, COVERED, neither assigned nor foreseeable): {n_out}")
    print(f"  script entries TASK_ABSENT: {n_ta}  (over the 48 runs and the four supplementary ones)")

    # ---- B4: BINDING_ABSENT (supplementary runs only) ----
    print("\n## B4 BINDING_ABSENT (the supplementary runs; none among the 48)")
    for r in supp:
        log, rec = parse(r["post"]), parse_rec(r["rec"])
        print(f"\n### {label(r)} ({r['layout']})")
        rows = []
        for t in sorted(log["ir"]):
            tr = truth(log, rec, t, LAG)
            if not tr["cov"].startswith("binding_absent"):
                continue
            ir = log["ir"][t]
            rows.append((t, rec[t]["action"], sk(ir["ml"]), ir["conf"],
                         "".join(L[finding_at(ir, a)] for a in ALPHAS), tails_str(ir)))
        _ranges(rows)

    # ---- B5: no task on the stack ----
    print("\n## B5 no task on the stack (lag-corrected: the record at t + 2 has an empty stack)")
    print(f"{'run':44} {'ticks':>5} {'first':>5} lifecycle         leader(s)                    finding @.01/.05/.10")
    for g in groups_by_prior(all48) + [[x] for x in supp]:
        r = g[0]
        log, rec = parse(r["post"]), parse_rec(r["rec"])
        ts = [t for t in sorted(log["ir"]) if truth(log, rec, t, LAG)["cov"] == "no_task"]
        if not ts:
            print(f"{label(r):44} {0:5}")
            continue
        lc = {}
        ml = {}
        fs = {a: {} for a in ALPHAS}
        for t in ts:
            ir = log["ir"][t]
            lc[ir["lifecycle"]] = lc.get(ir["lifecycle"], 0) + 1
            ml[sk(ir["ml"])] = ml.get(sk(ir["ml"]), 0) + 1
            for a in ALPHAS:
                f = L[finding_at(ir, a)]
                fs[a][f] = fs[a].get(f, 0) + 1
        print(f"{label(r):44} {len(ts):5} {ts[0]:5} {_d(lc):17} {_d(ml):28} "
              + " / ".join(_d(fs[a]) for a in ALPHAS) + (f"   [{others(g)[3:]}]" if len(g) > 1 else ""))
        # the tick the idle stand first reads unexplained, per α
        firsts = [next((t for t in ts if finding_at(log["ir"][t], a) == "unexplained"), None) for a in ALPHAS]
        if any(firsts):
            print(f"{'':44} first X at α=.01/.05/.10: " + " / ".join(str(x) if x is not None else "-" for x in firsts)
                  + f"  (stack empty in the record from {ts[0] + LAG})")

    # ---- B6: an episode's first ticks ----
    print("\n## B6 an episode's first ticks (step 0 and each [IR-boundary] b): finding letters b .. b+5, members at the")
    print("   first resolved tick, the leader at b; 'true' = the lag-corrected truth's hypothesis")
    for g in groups_by_prior(all48):
        r = g[0]
        log, rec = parse(r["post"]), parse_rec(r["rec"])
        print(f"\n### {label(r)}{others(g)}")
        for b in [min(log["ir"])] + log["boundary"]:
            seq = "".join(L[finding_at(log["ir"][t], 0.05)] for t in range(b, b + 6) if t in log["ir"])
            first = next((t for t in range(b, b + 40) if t in log["ir"] and log["ir"][t]["tails"]), None)
            tr = truth(log, rec, b, LAG)
            ir = log["ir"][b]
            print(f"  b={b:3} true={sk(tr['key']):12} leader {sk(ir['ml'])}({ir['conf']:.3f}) {ir['lifecycle']:9} "
                  f"seq={seq:6} first member at {first}: "
                  + (tails_str(log["ir"][first]) if first is not None else "-"))

    # ---- disagreements on modelled ticks ----
    print("\n## disagreements on COVERED ticks: unexplained (any α) while the truth is a modelled task with its binding")
    for g in groups_by_prior(all48):
        r = g[0]
        log, rec = parse(r["post"]), parse_rec(r["rec"])
        for t in sorted(log["ir"]):
            ir = log["ir"][t]
            if finding_at(ir, max(ALPHAS)) != "unexplained":
                continue
            raw, lag = truth(log, rec, t, 0), truth(log, rec, t, LAG)
            if "covered" not in (raw["cov"], lag["cov"]):
                continue
            print(f"  {label(r)}{others(g)} t={t} truth raw={sk(raw['key'])}/{raw['action']} "
                  f"lag={sk(lag['key'])}/{lag['action']} leader={sk(ir['ml'])}({ir['conf']:.3f}) "
                  f"finding .01/.05/.10={''.join(L[finding_at(ir, a)] for a in ALPHAS)} members: {tails_str(ir)}; "
                  f"true hypothesis a member: {lag['key'] in ir['tails']}; human {log['human'][t][0]}/{log['human'][t][1]}")


def _d(d):
    return ",".join(f"{k}:{v}" for k, v in sorted(d.items(), key=lambda kv: -kv[1]))


def _ranges(rows):
    """Consecutive ticks with the same action, leader, findings and member set, collapsed into one line."""
    start = prev = None
    for row in rows + [None]:
        sig = None if row is None else (row[1], row[2], row[4], tuple(x.split("=")[0] for x in row[5].split()))
        if start is not None and (row is None or sig != psig or row[0] != prev[0] + 1):
            print(f"  {start[0]:3}-{prev[0]:3} {start[1]:10} leader {start[2]}({start[3]:.3f}..{prev[3]:.3f}) "
                  f"finding .01/.05/.10={start[4]} members {start[5]} .. {prev[5]}")
            start = None
        if row is not None and start is None:
            start = row
        if row is not None:
            prev, psig = row, sig


if __name__ == "__main__":
    main()
