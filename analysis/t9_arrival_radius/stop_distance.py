#!/usr/bin/env python3
"""
stop_distance.py — where does each agent actually stop? For every completed walk in a headless log
(the tick on which action=move_to shows micro=None: the executor acknowledging at(agent, target)),
the distance from the agent's position to the nearest task object (any non-obstacle, non-item object
or item position in the layout) — the executor's real stopping distance, per agent.
Usage: python stop_distance.py <layout.json> <log> [<log> ...]
"""
import json, math, re, sys, statistics
POS = re.compile(r"^  step: (\d+): \[(\w+)\] task=(\S+) action=move_to micro=None pos=\[\s*([-\d.]+)\s+([-\d.]+)\s*\]")
def targets(layout):
    d = json.load(open(layout)); pts = {}
    for o in d["env_objects"]:
        if o["type"] == "obstacle": continue
        if "position" in o: pts[o["id"]] = tuple(o["position"])
    for o in d["env_objects"]:
        if "initial_container" in o and o["initial_container"] in pts: pts[o["id"]] = pts[o["initial_container"]]
    return pts
def main():
    layout, logs = sys.argv[1], sys.argv[2:]
    pts = targets(layout)
    per = {}
    for lg in logs:
        prev = None
        for ln in open(lg):
            m = POS.match(ln)
            if m:
                agent, x, y = m.group(2), float(m.group(4)), float(m.group(5))
                key = (lg, agent, m.group(1))
                d = min(math.hypot(x - px, y - py) for px, py in pts.values())
                per.setdefault(agent, []).append(d)
    for agent, ds in sorted(per.items()):
        print(f"{agent}: {len(ds)} completed walks; stop distance to the nearest object: "
              f"min {min(ds):.1f} / median {statistics.median(ds):.1f} / max {max(ds):.1f} cm; "
              f"all ≤ 30: {all(d <= 30.0 for d in ds)}")
if __name__ == "__main__":
    main()
