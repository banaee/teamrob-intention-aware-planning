#!/usr/bin/env python3
"""
analysis/l2_execution_lag/residual.py  (L2)

Attributes what is LEFT of TODO-77's lag after L2, row by row, instead of asserting a cause.

Two candidate residuals, both body facts the projection does not model and neither of which
L2 compensates for:

  STEP QUANTISATION (decided: not compensated). A walk of projected duration `dur` ticks is
  executed as ceil(dur) discrete steps — the executor stops on the first step that lands
  inside the arrival radius — so execution is ceil(dur) - dur ticks late per walk, always in
  [0, 1). Invariant to where in the walk the projection is taken: a partially-walked leg has
  an integer number of steps already behind it, which cancels.

  SKIPPED ACKNOWLEDGEMENT (robot only, 4-action plans). The projection charges one completion
  latency per action, but the robot re-plans at its own `task_committed` trigger, which fires
  on the tick that would have acknowledged the pick_up. The fresh `deliver_already_held` plan
  does not contain that pick_up, so continue_plan() loads from the start and the carry begins
  on that very tick: one of the four charged latencies is never spent. The projection is then
  1 tick LONG, in the opposite direction to quantisation.

predicted lead = -(sum of per-walk quantisation) + (1 if the row is a robot 4-action plan)

Usage: python analysis/l2_execution_lag/residual.py <captures.json> <log_dir>
"""
import json, math, re, statistics, sys
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


def item_of(k):
    m = re.search(r"\?item=(\w+)", k)
    return m.group(1) if m else None


def walk_quantisation(plan):
    """Sum of ceil(dur) - dur over the plan's MOVEMENT segments (those that cover ground)."""
    n_a, segs = plan["n_actions"], plan["segments"]
    stride = len(segs) // n_a
    total, per = 0.0, []
    for i in range(n_a):
        s = segs[stride * i]
        moved = (s["start_pos"][0] != s["end_pos"][0]) or (s["start_pos"][1] != s["end_pos"][1])
        if not moved:
            continue
        dur = s["end_step"] - s["start_step"]
        q = math.ceil(dur - 1e-9) - dur
        total += q
        per.append(q)
    return total, per, stride


def main():
    cap = json.load(open(sys.argv[1]))["conditions"]
    log_dir = Path(sys.argv[2])
    rows = []
    for cond in cap:
        releases, winners = parse_log(log_dir / f"{cond['name']}.log")
        wmap = dict(winners)
        for tr in cond["triggers"]:
            t = tr["step"]
            for who, plan, actual in (
                ("robot", None, None), ("human", None, None)):
                pass
            witem = wmap.get(t)
            if witem is not None:
                cand = next((c for c in tr["candidates"] if item_of(c["task"]) == witem), None)
                nxt = next((r for r in releases["robot_0"] if r >= t), None)
                if cand is not None and nxt is not None:
                    later = [(s, it) for s, it in winners if t < s <= nxt]
                    if all(it == witem for _, it in later):
                        p = cand["projection"]
                        q, per, stride = walk_quantisation(p)
                        seg = p["segments"][stride * (p["n_actions"] - 1)]
                        lead = t + seg["start_step"] - nxt
                        skipped = 1.0 if p["n_actions"] == 4 else 0.0
                        rows.append(("robot", cond["name"], t, p["n_actions"], q, skipped,
                                     -q + skipped, lead))
            hp = tr.get("human_projection")
            if hp and tr.get("projection_reason") == "built":
                hyp = hp["task_queue"][0]
                if hyp == tr["human_actual_task"] and hyp.startswith("deliver_item"):
                    nxt = next((r for r in releases["human_0"] if r >= t), None)
                    if nxt is not None:
                        q, per, stride = walk_quantisation(hp)
                        seg = hp["segments"][stride * (hp["n_actions"] - 1)]
                        lead = t + seg["start_step"] - nxt
                        rows.append(("human", cond["name"], t, hp["n_actions"], q, 0.0,
                                     -q, lead))

    print("| agent | actions | n | measured lead (min/med/max) | predicted (min/med/max) | residual after prediction (min/med/max) |")
    print("|---|---|---|---|---|---|")
    groups = {}
    for r in rows:
        groups.setdefault((r[0], r[3]), []).append(r)
    for k in sorted(groups):
        g = groups[k]
        meas = [r[7] for r in g]
        pred = [r[6] for r in g]
        diff = [r[7] - r[6] for r in g]
        f = lambda v: f"{min(v):+.2f} / {statistics.median(v):+.2f} / {max(v):+.2f}"
        print(f"| {k[0]} | {k[1]} | {len(g)} | {f(meas)} | {f(pred)} | {f(diff)} |")
    allv = [r[7] - r[6] for r in rows]
    print(f"\nall {len(rows)} rows, measured minus predicted: "
          f"min {min(allv):+.4f} / median {statistics.median(allv):+.4f} / max {max(allv):+.4f}; "
          f"|residual| <= 0.01 in {sum(abs(v) <= 0.01 for v in allv)} of {len(allv)}")


if __name__ == "__main__":
    main()


# =============================================================================
# Discrete-step forward model — attribution only, never a correction
# =============================================================================
#
# Replays the executor's DISCRETE stepping over the same plan the projection
# describes, to check that what is left of TODO-77's lag is step quantisation
# and nothing else. Uses no execution data: the targets are recovered from the
# projection's own segments (a walk ends arrival_radius short of its target, so
# target = end + radius * unit(end - start)).
#
# Per walk the executor takes k = ceil((d - radius) / speed) steps from wherever
# it actually stands and ends at distance d - k*speed from the target, which is
# inside the radius but not ON it. Two consequences, both left uncompensated by
# decision: the walk is ceil(dur) - dur ticks late, and the NEXT walk starts up
# to one step off the projected start, so it can be a whole step longer or
# shorter. The second is why a two-walk plan's residual can exceed one tick.

RADIUS, SPEED = 30.0, 20.0


def _unit(a, b):
    d = math.hypot(b[0] - a[0], b[1] - a[1])
    return None if d == 0 else ((b[0] - a[0]) / d, (b[1] - a[1]) / d)


def forward_release_tick(plan, start_step, latency=1.0):
    """Projected-time offset at which `place` would execute under discrete stepping."""
    n_a, segs = plan["n_actions"], plan["segments"]
    stride = len(segs) // n_a
    pos, t = tuple(segs[0]["start_pos"]), start_step
    for i in range(n_a):
        s = segs[stride * i]
        moved = s["start_pos"] != s["end_pos"]
        if i == n_a - 1:
            return t
        if moved:
            u = _unit(s["start_pos"], s["end_pos"])
            if u is None:
                return None
            target = (s["end_pos"][0] + RADIUS * u[0], s["end_pos"][1] + RADIUS * u[1])
            d = math.hypot(target[0] - pos[0], target[1] - pos[1])
            if d <= RADIUS:
                k = 0
            else:
                k = math.ceil((d - RADIUS) / SPEED - 1e-9)
                v = _unit(pos, target)
                pos = (pos[0] + k * SPEED * v[0], pos[1] + k * SPEED * v[1])
            t += k
        else:
            if any(segs[stride * j]["start_pos"] != segs[stride * j]["end_pos"] for j in range(i)):
                pass
            t += s["end_step"] - s["start_step"]
        t += latency
    return t
