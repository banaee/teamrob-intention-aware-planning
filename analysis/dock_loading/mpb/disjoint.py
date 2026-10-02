#!/usr/bin/env python3
"""
disjoint.py — the disjointness rule of the MPB on dock_loading (MPB-DL7; design_decisions.md, "T-G: the second domain's
rulings", THE MPB ON DOCK_LOADING): an authoring constraint of the controlled scenarios (and of M3, the mixed scenario
with full expectations), checked per scenario before its runs: no pallet is named both by the robot's pool and by an
assigned scan of the human. Reads the registered scenario literals; prints one line per scenario and exits 1 on a breach.

    disjoint.py <scenario id> [<scenario id> ...]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from domains.dock_loading.registry import domain_config


def pallets(tasks):
    return sorted({c.value for t in tasks for v, c in t.bindings.items() if v.name == "?pallet"})


bad = 0
for sid in sys.argv[1:]:
    sc = domain_config["scenarios"][sid]
    human = next(a for a in sc.agents if a.agent_type == "human")
    robot = next(a for a in sc.agents if a.agent_type == "robot")
    h, r = pallets(human.assigned_tasks), pallets(robot.assigned_tasks)
    both = sorted(set(h) & set(r))
    bad += bool(both)
    print(f"{sid}: the human's assigned scans {h}; the robot's pool {r}; named by both: {both or 'none'}")
sys.exit(1 if bad else 0)
