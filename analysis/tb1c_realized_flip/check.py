#!/usr/bin/env python3
"""
check.py — T-B1c: scenario_83, the decision at which realized cost changes the head under full_reorder.

Runs scenario_83 (env_layout8) in process under --strategy full_reorder, cost_strategy realized and
plain, assignment prior off and on (gate none, stop off), and records the inputs of every B3 call
(the pool, the world, the belief, the human projection), as analysis/tb2c_per_entry_holds/check.py
does. Then, outside the run, for every B3 call of the realized runs, every ordering of the pool is
priced twice — plain (realize() against no human plan) and realized (against the admitted projection)
— and the call is THE DECISION when the head of the plain-cost winner and the head of the
realized-cost winner differ (R3). At that decision it prints:

  1. the plain-cost table of every ordering (R7, plain side) and, from the plain run's B3 call at the
     same step, the same pool and the same costs (the plain run's [meta-ord] lines carry them;
     permutation_costs.py prices only from the robot's start and is not used);
  2. the realized costs, the holds before each entry and the cumulative shifts (R7, realized side),
     the hold sent (RealizedPlan.delta of the winner, holds[0]; expected 0 under R4) and the hold
     before the head realized alone of the plain-cost winner (expected 0 under R4);
  3. the R5 numbers: the plain-cost gap between the plain-cost winner and the realized-cost winner
     against the cumulative shift of the plain-cost winner; the flip needs gap < shift;
  4. validity of the plain-cost winner's later hold by F1's independent sampling (tb2c's check 9: the
     realized segments and the human projection sampled at DT ticks over the assessed window; rule (a)
     a crossing into s while moving, rule (b) moving within s with d' <= 0; both must be 0) and its
     minimality (the same sampling with that entry's cumulative shift one tick smaller must violate);
     the realized-cost winner sampled the same way, at its realized plan (holds 0: must be clear);
  5. the geometry: the segments of the conflicting entry and of the human projection, and the
     violating shift intervals of that entry.

Then, per run, the decision sequence (step:trigger:winner), and, if sweep/ holds the run_mesa logs
(sweep.sh), the completion tick from the world fact (the robot's last release + 1, metrics.py's rule),
the human's releases, the executed holds and the [sep] ticks below min_separation.

Ends with a verdict and exits non-zero on a defect: no decision found in a realized run, more than
one, a decision whose trigger is task_committed (R2), a plain-cost winner whose first hold is not 0
(R4), a violating sample in either winner, or a later hold that is not minimal.

Usage (repo root):
    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/tb1c_realized_flip/check.py \
        > analysis/tb1c_realized_flip/checks.md
"""
import itertools, logging, math, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "mesa_sim"))
logging.disable(logging.CRITICAL)
import numpy as np
from mesa_sim.sim_model import SimModel
from domains.kitting.registry import domain_config
from shared.types import Var
from shared.realization import realize, _realized_segments
from shared.trajectory_algorithms import shift_violation_interval

DT = 0.001
LAYOUT, SCENARIO, STEPS = "env_layout8", "scenario_83", 340
HEAD_RE = re.compile(r"winner=deliver_item\(\?item=item_(\d)")
CONDS = [(cost, prior) for prior in (False, True) for cost in ("realized", "plain")]


def item(task):
    return task.bindings[Var("?item")].value.split("_")[-1]


def fmt(ordering):
    return " ".join(item(t) for t in ordering)


def seg_state(segments, t):
    """(pos, vel, moving) of a head-to-tail chain at t; None outside its span. (F1's validate.py)"""
    for sg in segments:
        if sg.start_step - 1e-12 <= t <= sg.end_step + 1e-12:
            L = sg.end_step - sg.start_step
            if L <= 0:
                return np.array(sg.start_pos, float), np.zeros(2), False
            f = (t - sg.start_step) / L
            p0, p1 = np.array(sg.start_pos, float), np.array(sg.end_pos, float)
            v = (p1 - p0) / L
            return p0 + f * (p1 - p0), v, bool(np.any(p1 != p0))
    return None


def sample(realized_segments, human_segments, s, t0, t_h):
    """(rule_a, rule_b, min distance while moving, samples) over the assessed window. (F1's validate.py)"""
    lo = max(t0, human_segments[0].start_step, realized_segments[0].start_step)
    hi = min(t_h, realized_segments[-1].end_step)
    if hi <= lo:
        return 0, 0, math.inf, 0
    a = b = n = 0; dmin = math.inf; prev_d = None
    for t in np.arange(lo, hi + DT / 2, DT):
        r = seg_state(realized_segments, t); h = seg_state(human_segments, t)
        if r is None or h is None:
            prev_d = None; continue
        (pr, vr, moving), (ph, vh, _) = r, h
        diff = pr - ph; d = float(np.hypot(*diff)); n += 1
        if moving:
            dmin = min(dmin, d)
            dd = float(diff @ (vr - vh)) / d if d > 0 else -1.0
            if d < s - 1e-9 and dd <= 1e-9: b += 1
            if prev_d is not None and prev_d >= s and d < s - 1e-9: a += 1
        prev_d = d
    return a, b, dmin, n


def run(cost, prior):
    layout = domain_config["layouts"][LAYOUT]
    m = SimModel(layout["scenarios"][SCENARIO], domain_config["register_fn"], env_layout_path=layout["path"],
                 assignment_prior=prior, strategy="full_reorder", cost_strategy=cost, gate_strategy="none")
    robot = m.robots["robot_0"]; mp = robot.meta_planner
    calls = []
    inner = mp._replan_tasks

    def capture(**kw):
        result = inner(**kw)
        calls.append(dict(step=int(m.schedule.steps), trigger=mp._last_trigger_reason, pool=list(kw["task_pool"]),
                          belief=kw["belief"], world=kw["world"], against=kw["human_projection"], result=result,
                          robot_pos=(round(robot.pos[0], 1), round(robot.pos[1], 1))))
        return result
    mp._replan_tasks = capture
    for _ in range(STEPS):
        m.step()
    return robot, calls


def price(P, s, c):
    """Every ordering of the call's pool: (ordering, plan, plain RealizedPlan, realized RealizedPlan)."""
    rows = []
    for indices in itertools.permutations(range(len(c["pool"]))):
        ordering = [c["pool"][i] for i in indices]
        plan = P.project(ordering, c["world"], "robot_0", c["belief"], start_step=0.0)
        rows.append((ordering, plan, realize(plan, None, s, 0.0), realize(plan, c["against"], s, 0.0)))
    return rows


def winner(rows, key):
    """The first minimum in enumeration order (pool order), as _replan_orderings() keeps it."""
    best = None
    for row in rows:
        if best is None or key(row) < key(best):
            best = row
    return best


def segs(plan):
    return [sg for e in plan.entries for sg in e.segments]


def seg_line(sg):
    kind = "stand" if sg.start_pos == sg.end_pos else "move"
    return (f"{kind} [{sg.start_step:.2f}, {sg.end_step:.2f}] ({sg.start_pos[0]:.1f}, {sg.start_pos[1]:.1f})"
            f" -> ({sg.end_pos[0]:.1f}, {sg.end_pos[1]:.1f})")


def sweep_row(path):
    """Completion (world fact), the human's releases, executed holds, sub-s [sep] ticks, from a run_mesa log."""
    text = path.read_text().splitlines()
    s = float(re.search(r"min_separation=([0-9.]+)", next(l for l in text if l.startswith("[run]"))).group(1))
    rel = [int(re.search(r"step: (\d+)", l).group(1)) for l in text if "[robot_0]" in l and "action=place micro=release" in l]
    hrel = [int(re.search(r"step: (\d+)", l).group(1)) for l in text if "[human_0]" in l and "micro=release" in l]
    declared = [int(re.search(r"step=(\d+)", l).group(1)) for l in text if l.startswith("[meta] ") and "all tasks complete" in l]
    holds = sum(1 for l in text if l.startswith("[hold]"))
    seps = [(int(re.search(r"step=(\d+)", l).group(1)), float(re.search(r"dist=([0-9.]+)", l).group(1)))
            for l in text if l.startswith("[sep]")]
    sub = [(st, d) for st, d in seps if d < s]
    dmin = min(seps, key=lambda x: x[1]) if seps else None
    heads = []
    for l in text:
        if l.startswith("[meta-b3]"):
            h = HEAD_RE.search(l).group(1)
            if not heads or heads[-1] != h:
                heads.append(h)
    return dict(completion=rel[-1] + 1 if rel else None, declared=declared[0] if declared else None, human=hrel,
                holds=holds, sub=sub, dmin=dmin, heads=heads)


def sweep_line(r):
    """One line per log. The sub-s ticks are summarised: once both agents have finished they stand where they
    are, so a sub-s distance at the end of a run persists to the last step of the log."""
    before = [(st, d) for st, d in r["sub"] if st <= r["completion"]]
    after = [(st, d) for st, d in r["sub"] if st > r["completion"]]
    sub = ("none" if not r["sub"] else
           f"first {r['sub'][0][0]} ({r['sub'][0][1]:.1f} cm), {len(before)} up to completion, {len(after)} after it "
           f"(both agents done and standing)")
    return (f"completion {r['completion']} (world fact; declared {r['declared']}), heads {' '.join(r['heads'])}, "
            f"human releases {r['human']}, executed holds {r['holds']}, min [sep] {r['dmin'][1]:.2f} cm at step "
            f"{r['dmin'][0]}, [sep] ticks below min_separation: {sub}")


print("# T-B1c checks: scenario_83, realized cost changes the head under full_reorder\n")
print(f"Generated by `check.py`. {SCENARIO} on {LAYOUT}, full_reorder; cost realized and plain; gate none, stop off; "
      f"assignment prior off and on; PYTHONHASHSEED=0; sampling step {DT} tick.\n")

DEFECTS = []
runs = {}
for cost, prior in CONDS:
    runs[(cost, prior)] = run(cost, prior)

for prior in (False, True):
    tag = "on" if prior else "off"
    robot, calls = runs[("realized", prior)]
    _, plain_calls = runs[("plain", prior)]
    P, s = robot.projector, robot.meta_planner.min_separation
    print(f"## Prior {tag}: the decision (realized run)\n")
    decisions = []
    for c in calls:
        rows = price(P, s, c)
        pw = winner(rows, lambda r: r[2].cost)
        rw = winner(rows, lambda r: r[3].cost)
        if pw[0][0] is not rw[0][0]:
            decisions.append((c, rows, pw, rw))
    if len(decisions) != 1:
        DEFECTS.append(f"prior {tag}: {len(decisions)} decisions with different heads under plain and realized cost (expected 1)")
    for c, rows, pw, rw in decisions:
        against = c["against"]
        T_h = rw[3].horizon
        print(f"- step {c['step']}, trigger `{c['trigger']}`, pool {[item(t) for t in c['pool']]}, robot at {c['robot_pos']}, "
              f"projection admitted (T_h {T_h:.2f} on the projection clock, {c['step'] + T_h:.2f} absolute), "
              f"belief {c['belief'].most_likely} {c['belief'].confidence:.3f}")
        if c["trigger"] == "task_committed":
            DEFECTS.append(f"prior {tag}: the decision's trigger is task_committed (R2)")
        if item(rw[0][0]) != item(c["result"].current_task):
            DEFECTS.append(f"prior {tag}: the script's realized winner is not the run's")
        print(f"- head under plain cost: item_{item(pw[0][0])} (ordering {fmt(pw[0])}); head under realized cost: "
              f"item_{item(rw[0][0])} (ordering {fmt(rw[0])}); the run's winner: item_{item(c['result'].current_task)}, "
              f"hold sent {c['result'].hold}\n")
        # 1 + 2: the table
        print("| ordering | plain cost | realized cost | holds per entry | cumulative shifts | T_r | share past T_h |")
        print("|---|---|---|---|---|---|---|")
        for ordering, plan, plain, real in sorted(rows, key=lambda r: r[2].cost):
            print(f"| {fmt(ordering)} | {plain.cost:.2f} | {real.cost:.2f} | {real.holds} | {real.cumulative_shifts} | "
                  f"{real.projected_duration:.2f} | {real.unassessed_share:.2f} |")
        # the plain run's call at the same step
        same = [pc for pc in plain_calls if pc["step"] == c["step"]]
        if same:
            pc = same[0]
            prow = price(P, s, pc)
            agree = ([item(t) for t in pc["pool"]] == [item(t) for t in c["pool"]] and pc["trigger"] == c["trigger"]
                     and all(abs(a[2].cost - b[2].cost) < 1e-9 for a, b in zip(sorted(prow, key=lambda r: fmt(r[0])),
                                                                              sorted(rows, key=lambda r: fmt(r[0])))))
            print(f"\nThe plain run's B3 call at step {c['step']}: trigger `{pc['trigger']}`, pool {[item(t) for t in pc['pool']]}, "
                  f"winner item_{item(pc['result'].current_task)}; same pool, trigger and plain costs as above: {agree}. "
                  f"Its [meta-ord] lines carry these plain costs per head.")
            if not agree:
                DEFECTS.append(f"prior {tag}: the plain run's call at step {c['step']} does not agree with the realized run's")
        else:
            print(f"\nThe plain run has no B3 call at step {c['step']}.")
            DEFECTS.append(f"prior {tag}: no plain-run call at the decision step")
        # R4: the plain winner's head realized alone
        alone = realize(P.project(pw[0][:1], c["world"], "robot_0", c["belief"], start_step=0.0), against, s, 0.0)
        print(f"\n- R4: plain-cost winner {fmt(pw[0])}: holds {pw[3].holds}; its head item_{item(pw[0][0])} realized alone: "
              f"hold {alone.delta}; the winner's hold sent (holds[0] of {fmt(rw[0])}): {rw[3].holds[0]}")
        if pw[3].holds[0] != 0 or alone.delta != 0:
            DEFECTS.append(f"prior {tag}: the plain-cost winner's first hold is not 0 (R4)")
        if not any(h > 0 for h in pw[3].holds[1:]):
            DEFECTS.append(f"prior {tag}: the plain-cost winner carries no hold before a later entry (R4)")
        # R5
        gap = rw[2].cost - pw[2].cost
        shift = pw[3].cumulative_shifts[-1]
        print(f"- R5: plain-cost gap (realized winner {fmt(rw[0])} {rw[2].cost:.2f} − plain winner {fmt(pw[0])} {pw[2].cost:.2f}) = "
              f"{gap:.2f}; cumulative shift of the plain winner = {shift}; gap < shift: {gap < shift}")
        if not gap < shift:
            DEFECTS.append(f"prior {tag}: R5 fails (gap {gap:.2f}, shift {shift})")
        # 4: validity and minimality
        human = segs(against)
        for label, (ordering, plan, plain, real) in (("plain-cost winner", pw), ("realized-cost winner", rw)):
            a, b, dmin, n = sample(real.segments, human, s, 0.0, real.horizon)
            print(f"- sampled, {label} {fmt(ordering)} at its realized plan: rule a {a}, rule b {b}, min distance while moving "
                  f"{dmin:.2f} cm, {n} samples")
            if a or b:
                DEFECTS.append(f"prior {tag}: the {label} has a violating sample")
            entries = [list(e.segments) for e in plan.entries]
            for k, hold in enumerate(real.holds):
                if hold > 0:
                    shifts = list(real.cumulative_shifts); shifts[k] -= 1
                    ma, mb, mdmin, _ = sample(_realized_segments(entries, 0.0, shifts), human, s, 0.0, real.horizon)
                    print(f"  - minimality, entry {k + 1} at its cumulative shift − 1 ({shifts[k]}): rule a {ma}, rule b {mb}, "
                          f"min distance while moving {mdmin:.2f} cm: {'violates' if ma + mb else 'NO VIOLATION FOUND'}")
                    if not (ma + mb):
                        DEFECTS.append(f"prior {tag}: the hold before entry {k + 1} of {fmt(ordering)} is not minimal")
        # 5: geometry
        k = next(i for i, h in enumerate(pw[3].holds) if h > 0)
        entry = pw[1].entries[k]
        print(f"\nThe conflicting entry of {fmt(pw[0])}: entry {k + 1}, item_{item(pw[0][k])}, projected segments "
              f"(projection clock, the trigger at 0):\n")
        for sg in entry.segments:
            print(f"- {seg_line(sg)}")
        print("\nThe human projection's segments:\n")
        for sg in human:
            print(f"- {seg_line(sg)}")
        ivs = sorted((round(iv[0], 2), round(iv[1], 2)) for sg in entry.segments for h in human
                     if (iv := shift_violation_interval(sg, h, s)) is not None and iv[1] > 0.0)
        print(f"\nViolating shift intervals of entry {k + 1} against the human projection: {ivs}; the entry inherits "
              f"{pw[3].cumulative_shifts[k - 1] if k else 0} and the minimal-shift search returns {pw[3].cumulative_shifts[k]}.\n")
        # where each ordering's entry k ends against where the human's projection stands at its end
        stand = np.array(human[-1].end_pos, float)
        print(f"Where the human projection ends (its stand point): ({stand[0]:.1f}, {stand[1]:.1f}). The last move segment of "
              f"entry {k + 1} of each ordering, its end point and that point's distance from the stand point "
              f"(min_separation {s:.0f} cm):\n")
        for ordering, plan, plain, real in sorted(rows, key=lambda r: r[2].cost):
            last = [sg for sg in plan.entries[k].segments if sg.start_pos != sg.end_pos][-1]
            end = np.array(last.end_pos, float)
            print(f"- {fmt(ordering)}: entry {k + 1} item_{item(ordering[k])}, {seg_line(last)}, "
                  f"{float(np.hypot(*(end - stand))):.2f} cm from the stand point")
        print()

print("## Decision sequences (step:trigger:winner[hold]) and the executed runs\n")
for cost, prior in CONDS:
    robot, calls = runs[(cost, prior)]
    tag = f"s83_{cost}_{'on' if prior else 'off'}"
    seq = " ".join(f"{c['step']}:{c['trigger']}:{item(c['result'].current_task)}[{c['result'].hold}]" for c in calls)
    print(f"- {tag}: {seq}")
    log = HERE / "sweep" / f"{tag}.log"
    if log.exists():
        print("  - log: " + sweep_line(sweep_row(log)))
for prior in ("off", "on"):
    for cost in ("realized", "plain"):
        log = HERE / "sweep" / f"s80_{cost}_{prior}.log"
        if log.exists():
            print(f"- s80_{cost}_{prior} (log only): " + sweep_line(sweep_row(log)))

print("\n## Verdict\n")
print("- " + ("; ".join(DEFECTS) if DEFECTS else "no defect: one decision per prior, its trigger not task_committed, the "
             "plain-cost winner's first hold 0 and a later hold > 0, gap < shift, both winners valid by sampling, the later "
             "hold minimal"))
if DEFECTS:
    sys.exit(1)
