#!/usr/bin/env python3
"""
timing.py — projection vs execution, per placement (T9's premise check).

For every fired trigger in a T1b-style captures.json (fractional segments per candidate and for the
human projection), compares the PROJECTED placement — the last (stationary `place`) segment of the
logged winner, [start, end] relative to the trigger — with the tick at which the executor actually
executed the release, read from the matching headless log's per-tick lines. The same for the human:
the human projection's last segment vs the human's actual release, only where the projected
hypothesis is the human's actual task and is a delivery (a coffee/AC hypothesis ends in a wait whose
duration the projection does not model, TODO-32).

  lead = (trigger + projected place start) − actual release tick
  > 0 : the executor released BEFORE the projected placement began (execution ahead of projection)
  < 0 : after

A trigger's robot row is kept only if the robot's next release belongs to the winner selected at that
trigger and no later trigger selected a different task before it (continues are fine: they re-project
the same task from a later point, and are rows of their own).

Usage: python analysis/t9_arrival_radius/timing.py <captures.json> <log_dir> [label]
Writes nothing; prints a markdown table (paste into REPORT.md).
"""
import json, re, sys, statistics
from pathlib import Path

STEPLINE = re.compile(r"^  step: (\d+): \[(\w+)\] task=(\S+) action=(\S+) micro=(\S+) pos=")
META = re.compile(r"^\[meta\] step=(\d+) trigger=(\S+) winner=(\S+?)\{'\?item': '(\w+)'")

def parse_log(path):
    releases = {"robot_0": [], "human_0": []}
    winners = []          # (step, item)
    for ln in open(path):
        m = STEPLINE.match(ln)
        if m:
            step, agent, task, action, micro = int(m.group(1)), m.group(2), m.group(3), m.group(4), m.group(5)
            if micro == "release":
                releases[agent].append(step)
            continue
        m = META.match(ln)
        if m:
            winners.append((int(m.group(1)), m.group(4)))
    return releases, winners

def item_of(key):
    m = re.search(r"\?item=(\w+)", key)
    return m.group(1) if m else None

def main():
    cap = json.load(open(sys.argv[1]))["conditions"]
    log_dir = Path(sys.argv[2])
    label = sys.argv[3] if len(sys.argv) > 3 else ""
    rob_rows, hum_rows = [], []
    for cond in cap:
        name = cond["name"]
        releases, winners = parse_log(log_dir / f"{name}.log")
        wmap = dict(winners)
        for tr in cond["triggers"]:
            t = tr["step"]
            # ---- robot: the logged winner's projected placement vs the robot's next release
            witem = wmap.get(t)
            if witem is not None:
                cand = next((c for c in tr["candidates"] if item_of(c["task"]) == witem), None)
                nxt = next((r for r in releases["robot_0"] if r >= t), None)
                if cand is not None and nxt is not None:
                    later = [(s, it) for s, it in winners if t < s <= nxt]
                    if all(it == witem for _, it in later):
                        seg = cand["projection"]["segments"][-1]
                        nseg = len(cand["projection"]["segments"])
                        rob_rows.append((name, t, tr["trigger"], witem, nseg, t + seg["start_step"], nxt,
                                         t + seg["start_step"] - nxt))
            # ---- human: the projected hypothesis's placement vs the human's next release
            hp = tr.get("human_projection")
            if hp and tr.get("projection_reason") == "built":
                hyp = hp["task_queue"][0]
                if hyp == tr["human_actual_task"] and hyp.startswith("deliver_item"):
                    nxt = next((r for r in releases["human_0"] if r >= t), None)
                    if nxt is not None:
                        seg = hp["segments"][-1]
                        hum_rows.append((name, t, tr["trigger"], item_of(hyp), len(hp["segments"]),
                                         t + seg["start_step"], nxt, t + seg["start_step"] - nxt))
    def table(rows, who):
        print(f"\n### {who} placements {label}: projected place-segment start vs actual release tick ({len(rows)} rows)\n")
        print("| condition | trigger | reason | item | segs | projected place start | actual release | lead (ticks) |")
        print("|---|---|---|---|---|---|---|---|")
        for r in rows:
            print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]:.2f} | {r[6]} | {r[7]:+.2f} |")
        leads = [r[7] for r in rows]
        if leads:
            print(f"\nlead: min {min(leads):+.2f} / median {statistics.median(leads):+.2f} / max {max(leads):+.2f}; "
                  f"rows with lead > 0 (execution ahead): {sum(l > 0 for l in leads)} of {len(leads)}; "
                  f"|lead| ≤ 0.5: {sum(abs(l) <= 0.5 for l in leads)}")
    table(rob_rows, "Robot")
    table(hum_rows, "Human")

if __name__ == "__main__":
    main()
