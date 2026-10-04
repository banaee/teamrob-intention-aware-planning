#!/usr/bin/env python3
"""
plot_ir.py — the IRB's figure for an MPB run (added at the MPB close-out): the same panels as
analysis/irb/plot.py (the belief per hypothesis, the tail probability S per hypothesis, the finding band, the
observation-warrant bands and the gate's clearing; expected as lines, actual as dots; θ and α marked), drawn by that
script, imported unchanged, on the MPB's oracle table (expected_ticks.json) and in-process actual (actual_ticks.json).
Saved as figure_ir.png beside figure.png, which stays the MPB's decisions-and-distance figure (plot.py).

    plot_ir.py <scenario dir>/<prior>_<strategy> <run.log>

The hypotheses drawn are the support's, the expected table's keys. The belief carries the output floor of the setup's
robot items (held outside the support, each at the floor), so the support's shares sum to slightly less than 1, on the
expected side and the actual side alike. Since T-K part 1's gate stage (AM42) the belief panel draws the belief over
H (`belief_h`, the value the gate compares with θ, without the floor and the pins), recorded on both sides. Prior on
only: prior off has no oracle table (MPB-6).
"""
import csv
import json
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "irb"))
import plot as ir_plot                                  # analysis/irb/plot.py, unchanged

COLUMNS = ["tick", "key", "belief", "belief_h", "S", "finding", "lifecycle", "gate", "warrant"]


def rows(ticks, keys, belief_of, s_of):
    out = []
    for t in ticks:
        for k in keys:
            s = s_of(t).get(k)
            out.append(dict(tick=t["tick"], key=k, belief=belief_of(t).get(k, ""),
                            belief_h=t.get("belief_h", {}).get(k, ""), S="" if s is None else s,
                            finding=t["finding"] or "", lifecycle=t["lifecycle"], gate=t["gate"],
                            warrant=t["observation_warrant"].get(k, "none")))
    return out


def write(path, table):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(table)


def main(d, log):
    d = Path(d)
    exp = json.load(open(d / "expected_ticks.json"))
    act = json.load(open(d / "actual_ticks.json"))
    horizon = json.load(open(d / "observed.json"))["horizon"]
    exp = [t for t in exp if t["tick"] < horizon]
    act = [t for t in act if t["tick"] < horizon]
    keys = sorted({k for t in exp for k in t["belief"]})
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        write(tmp / "expected.csv", rows(exp, keys, lambda t: t["belief"], lambda t: t["S"]))
        write(tmp / "actual.csv", rows(act, keys, lambda t: t["belief"], lambda t: t["S"]))
        traj = json.load(open(d / "trajectory.json"))
        traj["actions"] = [a for a in traj["actions"] if a["tick"] < horizon]
        json.dump(traj, open(tmp / "trajectory.json", "w"))
        ir_plot.main(tmp, log)
        shutil.copy(tmp / "figure.png", d / "figure_ir.png")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
