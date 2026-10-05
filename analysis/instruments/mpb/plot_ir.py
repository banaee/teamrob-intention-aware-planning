#!/usr/bin/env python3
"""
plot_ir.py — the recognition rows of a planning run for its figure: per tick and hypothesis the belief, the belief over
H (`belief_h`), S, the finding, the lifecycle, the gate's answer and the observation warrant, from the oracle's table
(expected_ticks.json) or the in-process actual (actual_ticks.json), in the columns the IRB's builder reads
(analysis/instruments/irb/plot.py).

Until the measurement of T-F part 1 it drew the IRB's figure of an MPB run as figure_ir.png (added at the MPB close-out;
since T-F part 1's figures rule with the decision panel and, with no oracle table, the actual alone). Since N (Hadi,
5 October 2026: one figure file per run, every panel on one shared tick axis) plot.py draws that one figure,
figure.png, and calls `rows` here; no runner calls this file.

The hypotheses drawn are the support's, the expected table's keys. The belief carries the output floor of the setup's
robot items (held outside the support, each at the floor), so the support's shares sum to slightly less than 1, on the
expected side and the actual side alike; the figure draws the belief over H (`belief_h`, the value the gate compares
with θ, without the floor and the pins, AM42), recorded on both sides.
"""
import csv

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
