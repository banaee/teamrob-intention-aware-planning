#!/usr/bin/env python3
"""
separation.py <run.log> — the separation counts of one run, printed as markdown (the sort's preparation of the
instruments, 1 October 2026; plan approved by Hadi, question 5). From the log alone; no simulator import.

The measure (design_decisions.md, "T-G", the findings of the milestone): the ticks on which the human comes closer to
a standing robot than the minimum separation are reported apart from the violations by a moving robot; a standing
robot does not violate (F1). Per tick whose continuous [sep] minimum lies below min_separation (the [run] header),
F1's execution class (sep_classes.rule, the one definition): "viol", the robot moved with the distance falling below
both min_separation and the tick's starting distance; "recede", it moved with the distance increasing; "stand", the
robot did not move. A "stand" tick is split by the human's own displacement on that tick (the per-tick human lines):
the human moved (passing) or stood (standing beside the robot); "?" where the previous position is not logged.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import logparse
from sep_classes import rule


def stretches(ticks):
    return ", ".join(f"{e[0]}" if len(e) == 1 else f"{e[0]} to {e[-1]}" for e in logparse.episodes(sorted(ticks)))


def counts(path):
    run = logparse.parse(path)
    sep = float(run["hdr"].get("min_separation", 50.0))
    by = {"viol": [], "recede": [], "stand": [], "?": []}
    passing, beside, unknown = [], [], []
    for k, (_, m) in sorted(run["sep"].items()):
        if m is None or m >= sep:
            continue
        c = rule(run, k, sep)
        by[c].append(k)
        if c == "stand":
            h0, h1 = run["hpos"].get(k - 1), run["hpos"].get(k)
            (unknown if h0 is None or h1 is None else passing if h0 != h1 else beside).append(k)
    dist = min(((v[0], k) for k, v in run["sep"].items()), default=None)
    cont = min(((v[1], k) for k, v in run["sep"].items() if v[1] is not None), default=None)
    return sep, by, passing, beside, unknown, dist, cont


def main(path):
    sep, by, passing, beside, unknown, dist, cont = counts(path)
    out = [f"Separation ({Path(path).stem}; min_separation {sep:g} cm, from the [run] header): the ticks whose "
           "continuous [sep] minimum lies below it, by F1's execution class (sep_classes.rule).", "",
           "| class | ticks | stretches |", "|---|---|---|",
           f"| a moving robot, violating (viol) | {len(by['viol'])} | {stretches(by['viol']) or '-'} |",
           f"| a moving robot, receding (recede) | {len(by['recede'])} | {stretches(by['recede']) or '-'} |",
           f"| a standing robot, the human passing (moved on the tick) | {len(passing)} | {stretches(passing) or '-'} |",
           f"| a standing robot, the human standing beside it | {len(beside)} | {stretches(beside) or '-'} |"]
    if unknown or by["?"]:
        out.append(f"| unclassified (a position not logged) | {len(unknown) + len(by['?'])} | "
                   f"{stretches(unknown + by['?'])} |")
    out += ["", "The [sep] minimum: " + ("-" if dist is None else f"{dist[0]:.2f} cm at tick {dist[1]} (sampled)")
            + ("" if cont is None else f", {cont[0]:.2f} cm at tick {cont[1]} (continuous)") + "."]
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1])
