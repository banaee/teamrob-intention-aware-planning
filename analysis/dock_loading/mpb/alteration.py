#!/usr/bin/env python3
"""
alteration.py — dock_loading's single-rule alteration test (MPB-4; design_decisions.md, "T-G: the second domain's
rulings", THE MPB ON DOCK_LOADING, DL-P9): the shared engine and rules of analysis/instruments/mpb/alteration.py, with
dock_loading's B1 in its place and three rules of the IR oracle that dock_loading exercises (rules 24 to 26,
analysis/instruments/ir_testbed/README.md):
- B1, the admitted plan decomposed with the hall method always (the area guards ignored);
- E1, the human's area read as the hall on every tick (rule 24);
- E2, no episode boundary through a terminal action's completion other than a place or a wait (rule 26: a scan);
- E3, every support key live whatever its applicability (rule 25, T-G A4 switched off). On kind 3 every scan's pallet
  stands in its bay throughout, so no controlled scenario can show it; if undetected it is recorded as a property of the
  set with that reason (DL-P9).

    alteration.py <scratch dir> <scenario dir> [<scenario dir> ...]      (each: analysis/dock_loading/mpb/<scenario>/on_single_task)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "instruments" / "mpb"))
from alteration import SHARED, main

B1 = ("B1", "the admitted plan decomposed with the hall method always (the area guards ignored)", "mpb/mpb_oracle.py",
      ["actions = planner.decompose(space[leader], agent, world)"],
      ["actions = planner.decompose(space[leader], agent, world, method=space[leader].schema.name + '_hall')"])
E = [
    ("E1", "the human's area read as the hall on every tick (rule 24)", "ir_testbed/oracle.py",
     ['fact = area_fact(agent, (row["x"], row["y"]), areas)'], ['fact = area_fact(agent, (0.0, 0.0), areas)']),
    ("E2", "no boundary through a scan's completion (rule 26)", "ir_testbed/oracle.py",
     ["return any(self.completes(T, h, prev, now) for T in self.terminal)"], ["return False"]),
    ("E3", "every support key live whatever its applicability (rule 25, A4 off)", "ir_testbed/oracle.py",
     ["if A is None and k not in self.completed:     # T-G A4"],
     ["if False and A is None and k not in self.completed:     # T-G A4"]),
]

if __name__ == "__main__":
    main("dock_loading", SHARED[:5] + [B1] + SHARED[5:] + E)
