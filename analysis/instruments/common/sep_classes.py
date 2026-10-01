#!/usr/bin/env python3
"""
sep_classes.py <sweep dir> — per run log of a maintained baseline set (Track 2.5, docs/assumptions.md 4.6): the
completion tick, the [sep] minimum and F1's class counts of the ticks below min_separation. From the logs alone
(analysis/instruments/common/logparse.py; until the sort, 1 October 2026, this file was
analysis/tb1a_destination/sep_classes.py and the parser analysis/logparse.py); no simulator import. Used by the "2.5" sections of the four maintained READMEs.

- Completion (T6): the tick after the robot's last release, when the terminal fact is first observable. Only a
  release on a tick the robot has a task counts: after the pool empties the robot's per-tick line keeps its last
  action and micro (`task=None action=place micro=release`), which is no release.
- The [sep] minimum: of the tick-sampled `dist` and of the continuous `min` (TODO-79).
- F1's classes (analysis/f1_robot_responsible/evaluate.py, `rule`, copied here because that script runs at import),
  over the ticks whose continuous minimum lies below min_separation (read from the [run] header): "viol" when the
  robot moved during the tick and the continuous minimum lies below both min_separation and the tick's starting
  distance; "stand" when the robot did not move; "recede" when it moved with the distance increasing throughout.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import logparse


def rule(run, k, sep):
    """F1's rule at execution over tick k, on the continuous minimum (evaluate.py's `rule`, which='min')."""
    rp = run["rpos"]
    if k - 1 not in rp or k not in rp:
        return "?"
    if rp[k] == rp[k - 1]:
        return "stand"
    d_prev = run["sep"].get(k - 1, (None, None))[0]
    d_min = run["sep"][k][1]
    if d_prev is None:
        return "?"
    return "viol" if (d_min is not None and d_min < sep and d_min < d_prev - 1e-9) else "recede"


def summary(path):
    run = logparse.parse(path)
    sep = float(run["hdr"].get("min_separation", 50.0))
    releases = [k for k in run["releases"] if run["rtask"].get(k) not in (None, "None")]
    done = releases[-1] + 1 if run["pool"] and len(releases) >= len(run["pool"]) else None
    dist = min((v[0], k) for k, v in run["sep"].items())
    cont = min((v[1], k) for k, v in run["sep"].items() if v[1] is not None)
    counts = {"viol": 0, "stand": 0, "recede": 0, "?": 0}
    for k, (_, m) in run["sep"].items():
        if m is not None and m < sep:
            counts[rule(run, k, sep)] += 1
    return dict(log=Path(path).stem, done=done, steps=run["steps"], releases=len(releases), pool=len(run["pool"]),
                dist=dist, cont=cont, counts=counts)


if __name__ == "__main__":
    print("| log | completion | [sep] min dist (tick) | [sep] min continuous (tick) | viol | stand | recede |")
    print("|---|---|---|---|---|---|---|")
    for p in sorted(Path(sys.argv[1]).glob("*.log")):
        s = summary(p)
        done = s["done"] if s["done"] is not None else f"not complete in {s['steps']}"
        c = s["counts"]
        extra = f" ({c['?']} unclassified)" if c["?"] else ""
        print(f"| {s['log']} | {done} | {s['dist'][0]:.2f} ({s['dist'][1]}) | {s['cont'][0]:.2f} ({s['cont'][1]}) | "
              f"{c['viol']} | {c['stand']} | {c['recede']}{extra} |")
