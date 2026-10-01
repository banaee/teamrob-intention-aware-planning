#!/usr/bin/env python3
"""
The baseline diff of cycle 1.5b (the regeneration, item 1g): per maintained set and prior, the runs whose [IR] lines
changed, the runs whose world lines changed (the agents' per-tick lines: position, task, action, microaction), and
the robot's completion (T6: the world tick after its last release) before and after. PRE: the 1.3b baselines
(pre/<set>/), POST: the regenerated sets (analysis/<set>/sweep/).
"""
import re
from tdlib import runs, parse, robot_completion

WORLD = re.compile(r"^\s*step: \d+: \[(human|robot)_\d+\]")


def lines(path, pred):
    return [l for l in open(path, errors="replace") if pred(l)]


def main():
    print(__doc__)
    rows = {}
    for r in runs():
        ir = lines(r["pre"], lambda l: l.startswith("[IR]")) != lines(r["post"], lambda l: l.startswith("[IR]"))
        world = lines(r["pre"], WORLD.match) != lines(r["post"], WORLD.match)
        lp, lq = parse(r["pre"]), parse(r["post"])
        # a run whose robot never declares its pool empty did not complete: its last release is marked '(incomplete)'
        mark = lambda lg: f"{robot_completion(lg)}" + ("" if lg["done"] is not None else "(incomplete)")
        c = (mark(lp), mark(lq))
        rows.setdefault((r["set"], r["prior"]), []).append((r["name"], ir, world, c))
    print(f"{'set':20} {'prior':5} {'runs':>4} {'[IR] changed':>12} {'world changed':>13}  completion pre->post (changed only)")
    for (s, p), rs in sorted(rows.items(), key=lambda x: (x[0][0], x[0][1] != "on")):
        ch = [f"{n.replace('env_layout_', 'L').replace('scenario_', '')} {c[0]}->{c[1]}" for n, i, w, c in rs if c[0] != c[1]]
        print(f"{s:20} {p:5} {len(rs):4} {sum(i for _, i, _, _ in rs):12} {sum(w for _, _, w, _ in rs):13}  {'; '.join(ch) or '-'}")
    print("\nper run (world changed: first differing world tick)")
    for r in runs():
        a, b = lines(r["pre"], WORLD.match), lines(r["post"], WORLD.match)
        first = next((re.search(r"step: (\d+)", x)[1] for x, y in zip(a, b) if x != y), None)
        print(f"  {r['set']}/{r['name']}: world first differs at {first}")


if __name__ == "__main__":
    main()
