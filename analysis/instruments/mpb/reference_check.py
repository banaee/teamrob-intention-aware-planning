#!/usr/bin/env python3
"""
reference_check.py <out dir> — the human-unaware check against the robot-alone reference run, for a script that depends
on the robot (T-K part 1, step 6, point 2; design_records.md, "T-K", STEP 6): such a script has no oracle table before
the run (MPB-DL3, G), so compare.py does not run on it; its human-unaware run is still checked here as compare.py checks
an independent one (`compare.human_unaware_checks`: the hold 0 at every decision, the robot's positions against the
reference run's). Applied as a check, not as G's finding: in dock_loading's stage 1 no robot task reads a fact the
human's tasks change (the scan's is_scanned), so a human-unaware robot moves as the robot alone; measured on the twelve
dependent scripts before the step's runs. Writes <out dir>/reference_check.json: the disagreements and the ticks compared.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compare import human_unaware_checks

if __name__ == "__main__":
    d = Path(sys.argv[1])
    horizon = json.load(open(d / "observed.json"))["horizon"]
    out, _, compared = human_unaware_checks(d, horizon, separate=True)
    json.dump(dict(disagreements=out, compared=compared), open(d / "reference_check.json", "w"), indent=1)
    print(f"{d.name}: reference check on {compared} ticks, {len(out)} disagreements")
