#!/usr/bin/env python3
"""
compare.py — the meta-planner test-bed's comparison (MPB-3, MPB-4): the expected per-tick table and chain against the
in-process actual (the primary source) and the log (the check), over the comparison horizon (observed.json, MPB-5).

    compare.py <scenario> <dir> [--no-oracle]

<dir> holds expected_ticks.json (mpb_oracle.py), expected_decisions.json (chain.py), actual_ticks.json,
actual_decisions.json, actual_log_decisions.json, observed.json (actual.py). Writes diff.md and diff.json (the counts
and every disagreement). The classification of each disagreement (MPB-4's five classes) is written by hand after
investigation, in diff.md's last section and in REPORT.md.

Compared, exactly unless stated:
- per tick (in-process): the leader, the boundary flag, the adequacy finding (added in part (iv)), the gate's outcome,
  every live hypothesis's hypothesis adequacy and observation warrant; on the ticks the robot evaluated its triggers, P4's perception facts (the displacement at
  absolute 1e-9, the run length and the standing count exactly);
- part 1: the set of (tick, trigger, cause) of the decisions that are not no_current_task (the no_current_task ticks are
  the run's, listed);
- part 2, at every decision: the gate's outcome, the leader, and when the gate clears the warrant sources;
- part 3, at every decision: the admitted projection's key and plan, or the fallback's mode, k (exactly), duration and
  end (relative 1e-9) and the tick its expiry fires;
- the log check, per logged decision: trigger and cause as in-process; its [meta-proj] text as the expected decision
  implies (`built warrant=...`, `fallback refused=<gate>`); the tick's [IR] leader.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mpblib import Gate, Trigger, load_decisions, load_ticks

TOL = 1e-9


def close(a, b):
    return math.isclose(a, b, rel_tol=TOL, abs_tol=1e-12)


def compare_ticks(exp, act, horizon):
    out, counts = [], {c: [0, 0] for c in ("leader", "boundary", "finding", "gate", "adequacy", "observation_warrant",
                                           "perception")}
    act = {a["tick"]: a for a in act}

    def check(col, t, e, a):
        counts[col][0] += 1
        if e != a:
            counts[col][1] += 1
            out.append((t, col, e, a))

    for e in exp:
        t = e.tick
        if t >= horizon or t not in act:
            continue
        a = act[t]
        check("leader", t, e.leader, a["leader"])
        check("boundary", t, e.boundary, a["boundary"])
        check("finding", t, e.finding, a["finding"])
        check("gate", t, e.gate.value, a["gate"])
        check("adequacy", t, dict(sorted(e.adequacy.items())), dict(sorted(a["adequacy"].items())))
        check("observation_warrant", t, dict(sorted(e.observation_warrant.items())),
              dict(sorted(a["observation_warrant"].items())))
        if a["evaluated"]:
            p, q = e.perception, a["perception"]
            same = (p is None and q is None) or (
                p is not None and q is not None and p.run_length == q["run_length"]
                and p.standing_count == q["standing_count"]
                and all(abs(x - y) <= TOL for x, y in zip(p.displacement, q["displacement"])))
            counts["perception"][0] += 1
            if not same:
                counts["perception"][1] += 1
                out.append((t, "perception",
                            None if p is None else [list(p.displacement), p.run_length, p.standing_count],
                            None if q is None else [q["displacement"], q["run_length"], q["standing_count"]]))
    return counts, out


def part(d):
    """A decision's parts: 1 (trigger, cause), 2 (gate, leader, warrant), 3 (the projection's identity)."""
    fb = d.fallback
    p3 = (None if d.admitted is None else (d.admitted.key, d.admitted.actions),
          None if fb is None else (fb.mode.value, fb.k, fb.duration, fb.end, fb.expiry_tick()))
    return (d.trigger.value, None if d.cause is None else d.cause.value), (d.gate.value, d.leader, d.warrant), p3


def same_p3(e, a):
    ea, ef = e
    aa, af = a
    if ea != aa or (ef is None) != (af is None):
        return False
    if ef is None:
        return True
    return ef[0] == af[0] and ef[1] == af[1] and close(ef[2], af[2]) and close(ef[3], af[3]) and ef[4] == af[4]


def compare_decisions(exp, act):
    out = []
    e_set = {(d.tick,) + part(d)[0] for d in exp if d.trigger is not Trigger.NO_CURRENT_TASK}
    a_set = {(d.tick,) + part(d)[0] for d in act if d.trigger is not Trigger.NO_CURRENT_TASK}
    for x in sorted(e_set - a_set):
        out.append((x[0], "part 1", f"expected {x[1]} {x[2] or ''}".strip(), "absent"))
    for x in sorted(a_set - e_set):
        out.append((x[0], "part 1", "absent", f"actual {x[1]} {x[2] or ''}".strip()))
    e_by, a_by = {d.tick: d for d in exp}, {d.tick: d for d in act}
    n2 = n3 = 0
    for t in sorted(set(e_by) & set(a_by)):
        (_, e2, e3), (_, a2, a3) = part(e_by[t]), part(a_by[t])
        n2 += 1
        n3 += 1
        if e2 != a2:
            out.append((t, "part 2", e2, a2))
        if not same_p3(e3, a3):
            out.append((t, "part 3", e3, a3))
    return dict(part1=[len(e_set), len(a_set)], part2=n2, part3=n3), out


def log_text(d):
    """The [meta-proj] projection text a decision implies (shared/io_contracts.md §2.2; T-D G AD4)."""
    if d.gate is Gate.CLEARS:
        return "built warrant=" + ",".join(d.warrant)
    return f"fallback refused={d.gate.value}" if d.fallback is not None else d.gate.value


def compare_log(act, log, exp_by_tick):
    out = []
    a_by = {d.tick: d for d in act}
    for l in log:
        t = l["tick"]
        a = a_by.get(t)
        if a is None:
            out.append((t, "log", "no in-process decision", l))
            continue
        if (l["trigger"], l["cause"]) != (a.trigger.value, None if a.cause is None else a.cause.value):
            out.append((t, "log trigger", (a.trigger.value, a.cause and a.cause.value), (l["trigger"], l["cause"])))
        if l["leader"] != a.leader:
            out.append((t, "log leader", a.leader, l["leader"]))
        e = exp_by_tick.get(t)
        if e is not None and l["projection"] != log_text(e):
            out.append((t, "log projection", log_text(e), l["projection"]))
    return out


if __name__ == "__main__":
    sid, d = sys.argv[1], Path(sys.argv[2])
    obs = json.load(open(d / "observed.json"))
    H = obs["horizon"]
    exp_t = load_ticks(d / "expected_ticks.json")
    exp_d = [x for x in load_decisions(d / "expected_decisions.json") if x.tick < H]
    act_t = json.load(open(d / "actual_ticks.json"))
    act_d = [x for x in load_decisions(d / "actual_decisions.json") if x.tick < H]
    log_d = [x for x in json.load(open(d / "actual_log_decisions.json")) if x["tick"] < H]
    tc, tb = compare_ticks(exp_t, act_t, H)
    dc, db = compare_decisions(exp_d, act_d)
    lb = compare_log(act_d, log_d, {x.tick: x for x in exp_d})
    bad = tb + db + lb
    lines = [f"# {sid}: expected against actual ({obs['strategy']}, prior {'on' if obs['prior'] else 'off'})", "",
             f"Horizon: ticks 0 to {H - 1} (the first observed completion point + 30, capped at the run's "
             f"{obs['steps']} steps; MPB-5). Terminal decision: {obs['terminal']}; the human's last acknowledgement: "
             f"{obs['last_ack']}. The run's no_current_task ticks: {obs['no_current_task']}.", "",
             "## Per tick (in-process)", "", "| column | compared | disagree |", "|---|---|---|"]
    lines += [f"| {c} | {n} | {k} |" for c, (n, k) in tc.items()]
    lines += ["", "## Decisions", "",
              f"Part 1, decisions other than no_current_task: {dc['part1'][0]} expected, {dc['part1'][1]} actual. "
              f"Parts 2 and 3 compared at {dc['part2']} decisions present on both sides. The log: {len(log_d)} "
              "decisions checked.", "", f"Disagreements: {len(bad)}", ""]
    if bad:
        lines += ["| tick | where | expected | actual |", "|---|---|---|---|"]
        lines += [f"| {t} | {w} | {e} | {a} |" for t, w, e, a in bad]
        lines.append("")
    lines += ["## Classification", "", "None to classify." if not bad else "(written after investigation)", ""]
    (d / "diff.md").write_text("\n".join(lines))
    json.dump(dict(ticks=tc, decisions=dc, disagreements=[list(map(str, b)) for b in bad]),
              open(d / "diff.json", "w"), indent=1)
    print(f"{sid} ({obs['strategy']}): {len(tb)} per-tick, {len(db)} decision, {len(lb)} log disagreements")
