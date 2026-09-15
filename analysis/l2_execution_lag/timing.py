#!/usr/bin/env python3
"""
analysis/l2_execution_lag/timing.py  (L2)

TODO-77's measurement, re-run so that before and after are produced by the same code.
For every fired trigger in a T1b-style captures.json, compares the PROJECTED placement —
the `place` action's segment, [start, end] relative to the trigger — with the tick on which
the executor actually executed the release, read from the matching headless log.

  lead = (trigger + projected place start) − actual release tick
  > 0 : the executor released BEFORE the projected placement began (execution ahead)
  < 0 : after (execution behind projection — TODO-77's lag)

Since L2 the projection carries a completion-latency hold after every action, so there are
two segments per action, not one. The place segment is located by stride
(n_segments // n_actions), which is 1 in pre-L2 captures and 2 after — the same script
therefore reads both.

Rows are kept on the same rule as T9: the robot's next release must belong to the winner
selected at that trigger with no different winner in between; the human's projected
hypothesis must be its actual task and a delivery (a coffee/AC hypothesis ends in a wait
whose duration the projection does not model, TODO-32).

Usage: python analysis/l2_execution_lag/timing.py <captures.json> <log_dir> [label]
"""
import json, re, sys, statistics
from pathlib import Path

STEPLINE = re.compile(r"^  step: (\d+): \[(\w+)\] task=(\S+) action=(\S+) micro=(\S+) pos=")
META = re.compile(r"^\[meta\] step=(\d+) trigger=(\S+) winner=(\S+?)\{'\?item': '(\w+)'")


def parse_log(path):
    releases = {"robot_0": [], "human_0": []}
    winners = []
    for ln in open(path):
        m = STEPLINE.match(ln)
        if m:
            if m.group(5) == "release":
                releases[m.group(2)].append(int(m.group(1)))
            continue
        m = META.match(ln)
        if m:
            winners.append((int(m.group(1)), m.group(4)))
    return releases, winners


def item_of(key):
    m = re.search(r"\?item=(\w+)", key)
    return m.group(1) if m else None


def place_segment(plan):
    """The segment of the LAST action, whatever the per-action segment stride is."""
    n_a, segs = plan["n_actions"], plan["segments"]
    stride = len(segs) // n_a
    return segs[stride * (n_a - 1)], stride


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
            witem = wmap.get(t)
            if witem is not None:
                cand = next((c for c in tr["candidates"] if item_of(c["task"]) == witem), None)
                nxt = next((r for r in releases["robot_0"] if r >= t), None)
                if cand is not None and nxt is not None:
                    later = [(s, it) for s, it in winners if t < s <= nxt]
                    if all(it == witem for _, it in later):
                        seg, stride = place_segment(cand["projection"])
                        rob_rows.append((name, t, tr["trigger"], witem,
                                         cand["projection"]["n_actions"], stride,
                                         t + seg["start_step"], nxt,
                                         t + seg["start_step"] - nxt))
            hp = tr.get("human_projection")
            if hp and tr.get("projection_reason") == "built":
                hyp = hp["task_queue"][0]
                if hyp == tr["human_actual_task"] and hyp.startswith("deliver_item"):
                    nxt = next((r for r in releases["human_0"] if r >= t), None)
                    if nxt is not None:
                        seg, stride = place_segment(hp)
                        hum_rows.append((name, t, tr["trigger"], item_of(hyp),
                                         hp["n_actions"], stride,
                                         t + seg["start_step"], nxt,
                                         t + seg["start_step"] - nxt))

    def table(rows, who):
        print(f"\n### {who} placements {label}: projected place start vs actual release tick ({len(rows)} rows)\n")
        print("| condition | trigger | reason | item | actions | seg/action | projected place start | actual release | lead |")
        print("|---|---|---|---|---|---|---|---|---|")
        for r in rows:
            print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]:.2f} | {r[7]} | {r[8]:+.2f} |")
        leads = [r[8] for r in rows]
        if leads:
            print(f"\nlead: min {min(leads):+.2f} / median {statistics.median(leads):+.2f} / max {max(leads):+.2f}; "
                  f"ahead of projection: {sum(l > 0 for l in leads)} of {len(leads)}")
            by = {}
            for r in rows:
                by.setdefault(r[4], []).append(r[8])
            for n_a in sorted(by):
                v = by[n_a]
                print(f"  {n_a}-action plans: n={len(v)} min {min(v):+.2f} / median {statistics.median(v):+.2f} / max {max(v):+.2f}")

    table(rob_rows, "Robot")
    table(hum_rows, "Human")


if __name__ == "__main__":
    main()
