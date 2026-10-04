#!/usr/bin/env python3
"""
compare.py — expected.csv against actual.csv (full precision, the in-process BeliefState) and against actual_log.csv
(the run log, print precision), per (tick, hypothesis), for the IRB (IRB.3b). Writes diff.md: per column the
count compared and the count that disagrees, then every disagreement with its tick. Tick -1 (the observation before
the clock starts, RobotAgent.observe_initial) has no log line and is not compared (reading R4).

Since the gate rulings' build (stage 4): `rank`, the evidence rank per hypothesis, against both files; a cell the
generator marks undetermined (D3) is skipped and counted, never compared.
Categorical columns exactly (since G-build also `warrant`, the observation warrant per hypothesis, against both files,
and `gate`, the gate's outcome per tick, against actual.csv only: the log carries no per-tick gate; since T-K part 1's
gate stage `belief_h`, the belief over H per hypothesis, against actual.csv only; since its stage 6 `prior` per
hypothesis and `levels` and `recent` per tick, against both files, the log's `[IR-context]` line printing the prior to
4 decimals; all three empty on both sides with context knowledge off); numeric columns against actual.csv at relative tolerance 1e-9 (absolute 1e-12 near
zero), against actual_log.csv at half a unit of the printed digit (belief and confidence 5e-4, S 5e-5, position
5e-3). The columns the recognizer does not output (expected_action, origin_x, origin_y, e, s, s_exp, D, L,
evidence) are empty in both actual files and skipped.

The classification of each disagreement (the generator misread the records; the recognizer disagrees with the
records; the records do not determine the value) is written by hand after investigating it, under "Classification".

    compare.py <scenario> <expected.csv> <actual.csv> <actual_log.csv> <diff.md>
"""
import csv
import math
import sys

TICK = ["human_x", "human_y", "micro", "holding", "waited", "obj_at", "at", "most_likely", "confidence", "finding",
        "lifecycle", "pins", "reentries", "boundary", "gate", "levels", "recent"]
HYP = ["prior", "belief", "belief_h", "S", "member", "adequacy", "warrant", "rank"]
NUMERIC = {"human_x", "human_y", "confidence", "prior", "belief", "belief_h", "S"}
PRINTED = {"human_x": 5e-3, "human_y": 5e-3, "confidence": 5e-4, "prior": 5e-5, "belief": 5e-4, "S": 5e-5}
LOG_COLUMNS = ["human_x", "human_y", "micro", "most_likely", "confidence", "finding", "lifecycle", "pins", "reentries",
               "boundary", "levels", "recent",
               "prior", "belief", "S", "member", "adequacy", "warrant", "rank"]
# D3 (the gate rulings' build): where the generator marks `rank` or `gate` undetermined (its evidence agrees with the
# recognizer's to 1e-9, not bit for bit, and the exact rule turns on a closer difference), the cell is skipped and
# counted, never compared
UNDETERMINED = "undetermined"
SKIPPED = ["expected_action", "origin_x", "origin_y", "e", "s", "s_exp", "D", "L", "evidence"]


def read(path):
    rows = {}
    for r in csv.DictReader(open(path)):
        t = int(r["tick"])
        if t >= 0:
            rows[(t, r["key"])] = r
    return rows


def equal(col, a, b, printed):
    if a == b:
        return True
    if col not in NUMERIC or a == "" or b == "":
        return False
    x, y = float(a), float(b)
    if printed:
        return abs(x - y) <= PRINTED[col] + 1e-12
    return math.isclose(x, y, rel_tol=1e-9, abs_tol=1e-12)


def compare(exp, act, columns, printed):
    counts = {c: [0, 0] for c in columns}
    bad, skipped = [], {}
    rowset = sorted(set(exp) ^ set(act))
    for k in sorted(set(exp) & set(act)):
        for c in columns:
            if c in HYP and k[1] == "":
                continue
            if c in TICK and k[1] != sorted(x for (t, x) in exp if t == k[0])[0]:
                continue                                   # per-tick columns once per tick
            if exp[k][c] == UNDETERMINED:
                skipped[c] = skipped.get(c, 0) + 1
                continue
            counts[c][0] += 1
            if not equal(c, exp[k][c], act[k][c], printed):
                counts[c][1] += 1
                bad.append((k[0], k[1], c, exp[k][c], act[k][c]))
    return counts, bad, rowset, skipped


def section(title, counts, bad, rowset, skipped):
    out = [f"## {title}", "",
           f"Rows (tick, live hypothesis) present on one side only: {len(rowset)}"
           + (f" (first: {rowset[:5]})" if rowset else ""), "",
           "| column | compared | disagree |", "|---|---|---|"]
    out += [f"| {c} | {n} | {d} |" for c, (n, d) in counts.items()]
    out += ["", "Undetermined (D3; skipped, not compared): "
            + (", ".join(f"{c} {n}" for c, n in sorted(skipped.items())) if skipped else "none"), ""]
    out += [f"Disagreements: {len(bad)}", ""]
    if bad:
        out += ["| tick | hypothesis | column | expected | actual |", "|---|---|---|---|---|"]
        out += [f"| {t} | {k or '-'} | {c} | {e} | {a} |" for t, k, c, e, a in bad]
        out.append("")
    return out


if __name__ == "__main__":
    sid, e_path, a_path, l_path, out = sys.argv[1:6]
    exp, act, log = read(e_path), read(a_path), read(l_path)
    c1, b1, r1, u1 = compare(exp, act, TICK + HYP, printed=False)
    c2, b2, r2, u2 = compare(exp, log, LOG_COLUMNS, printed=True)
    lines = [f"# {sid}: expected against actual", "",
             "expected.csv (oracle.py) against actual.csv (the in-process BeliefState, full precision; its [IR*] lines "
             "byte-identical to the logged run's) and against actual_log.csv (the run log, print precision). Ticks "
             f"0 to {max(t for t, _ in exp)}. Not compared (the recognizer does not output them): "
             + ", ".join(SKIPPED) + ".", ""]
    lines += section("Against actual.csv (relative tolerance 1e-9)", c1, b1, r1, u1)
    lines += section("Against actual_log.csv (print precision)", c2, b2, r2, u2)
    lines += ["## Classification", "",
              "None to classify." if not (b1 or b2 or r1 or r2) else "(written after investigation)", ""]
    open(out, "w").write("\n".join(lines))
    print(f"{sid}: {len(b1)} disagreements against actual.csv, {len(b2)} against actual_log.csv, "
          f"{len(r1) + len(r2)} unmatched rows; undetermined (skipped) rank {u1.get('rank', 0)}, gate {u1.get('gate', 0)}")
