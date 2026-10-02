#!/usr/bin/env python3
"""
alteration.py — kitting's single-rule alteration test (MPB-4): the shared engine and rules of
analysis/instruments/mpb/alteration.py, with kitting's B1 (the method guards of deliver_item) in its place.

    alteration.py <scratch dir> <scenario dir> [<scenario dir> ...]      (each: analysis/kitting/mpb/<scenario>/on_single_task)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "instruments" / "mpb"))
from alteration import SHARED, main

B1 = ("B1", "the admitted plan decomposed without the method guards (deliver_default always)", "mpb/mpb_oracle.py",
      ["actions = planner.decompose(space[leader], agent, world)"],
      ["actions = planner.decompose(space[leader], agent, world, method='deliver_default') "
       "if space[leader].schema.name == 'deliver_item' else planner.decompose(space[leader], agent, world)"])

if __name__ == "__main__":
    main("kitting", SHARED[:5] + [B1] + SHARED[5:])
