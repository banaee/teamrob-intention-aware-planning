#!/usr/bin/env python3
"""
G. The Projector's actual priced standing for pick_up and place, read from its own output on a fixture.

Runs scenario_s01_01 on env_layout_01, assignment prior on, with the tb1a sweep's options (the run file's defaults
otherwise; no value changed), and records every human projection the meta-planner admits: the instance's
`update_human_projection` is wrapped here, in this script only, to keep its return value. For the first admitted
projection of each hypothesis it prints the entry's segments, paired with the plan's actions (build_segments emits
two per action when the body states an action-completion latency: the action's own, then the latency's stationary
segment), and beside each action the recognizer's s_exp for it. Cycle 1.5b (E9): s_exp is per phase, the latency
priced after the completion that opened it plus the action's own standing, so the script reads it from the
recognizer during the run (`IntentionRecognizer._priced_standing(key, action)` on every tick the hypothesis expects
that action; the first value seen) and prints beside it the attribution from the Projector's own segments (the
previous action's latency plus this action's own stationary segment). Then the body's observed stand at each
location, from the fixture's baseline log.

Run from the repo root: PYTHONHASHSEED=0 ~/python-envs/ir-nomesa-env/bin/python analysis/td_stage1b/g_priced_standing.py
"""
import logging, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "mesa_sim"))
sys.argv = ["run_mesa.py", "--domain", "kitting", "--layout", "env_layout_01", "--scenario", "scenario_s01_01",
            "--steps", "90", "--cost_strategy", "realized", "--gate_strategy", "none", "--separation_stop", "false",
            "--assignment_prior", "true"]
logging.disable(logging.CRITICAL)
import run_mesa  # noqa: E402

STEPS = 90


def main():
    model = run_mesa._make_domain_model()
    robot = next(iter(model.robots.values()))
    mp, rec = robot.meta_planner, robot.recognizer
    captured, tick = [], [0]
    orig = mp.update_human_projection

    def wrapped(belief, world):
        p = orig(belief, world)
        if p is not None:
            captured.append((tick[0], belief.most_likely, p))
        return p

    mp.update_human_projection = wrapped
    s_exp_seen = {}
    for s in range(STEPS):
        tick[0] = s
        model.step()
        for key, a in rec._expected.items():
            if a is not None and key in rec._entry_latency:
                s_exp_seen.setdefault((key, a.action_name, tuple(sorted(a.bindings.items()))),
                                      rec._priced_standing(key, a))

    seen = set()
    for s, ml, p in captured:
        if ml in seen:
            continue
        seen.add(ml)
        print(f"admitted at step {s}: {ml}")
        for e in p.entries:
            acts, segs = e.abstract_plan.actions, e.segments
            print(f"  entry start={e.estimated_start_step} duration={e.estimated_duration} "
                  f"actions={len(acts)} segments={len(segs)}")
            assert len(segs) == 2 * len(acts), "expected one latency segment per action"
            prev_lat = None
            for i, a in enumerate(acts):
                own, lat = segs[2 * i], segs[2 * i + 1]
                d_own, d_lat = own.end_step - own.start_step, lat.end_step - lat.start_step
                moving = own.start_pos != own.end_pos
                attributed = (prev_lat or 0.0) + (0.0 if moving else d_own)
                s_exp = s_exp_seen.get((ml, a.action_name, tuple(sorted(a.bindings.items()))))
                print(f"    {a.action_name:8} {'walk' if moving else 'stand':5} own={d_own:6.2f} "
                      f"latency(stand)={d_lat:4.2f} "
                      f"projected standing at its location={('%.2f' % (d_lat if moving else d_own + d_lat)):>5} "
                      f"E9 attribution (previous latency + own stationary)={attributed:.2f} "
                      f"recognizer s_exp={'-' if s_exp is None else '%.2f' % s_exp}")
                prev_lat = d_lat
    print()
    print("observed body (the fixture's baseline log, human_0): the stationary ticks at each location")
    log = ROOT / "analysis/tb1a_destination/sweep/env_layout_01_scenario_s01_01_on.log"
    rows = []
    for l in open(log):
        if "[human_0]" in l and l.lstrip().startswith("step:"):
            parts = l.split()
            rows.append((int(parts[1].rstrip(":")), parts[4].split("=")[1], parts[5].split("=")[1]))
    run = []
    for st, a, mu in rows:
        if mu == "step":
            if run:
                print(f"  steps {run[0][0]}-{run[-1][0]} ({len(run)} ticks): " + " ".join(f"{x[1]}/{x[2]}" for x in run))
                run = []
        else:
            run.append((st, a, mu))
        if st > 145:
            break
    counts()


def counts():
    """
    Over the 48 runs: the true hypothesis's S on the record's walking ticks (the body's micro=step) where it is a
    member, by the D it implies (ticks, from S inverted at β, v): D = 0 exactly (S = 1), D = 1 (S = 0.8629, one
    latency tick carried from the stationary action before the walk or from the boundary's place acknowledgement;
    under E9 that tick is priced to the walk), other. The truth is lag-corrected (the record at t + 2).
    """
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from tdlib import runs, parse, parse_rec, truth, vd_of, LAG, V
    from collections import Counter
    print()
    print("the true hypothesis's D on the human's walking ticks where it is a member (48 runs, lag-corrected truth)")
    for prior in ("on", "off"):
        c = Counter()
        for r in runs():
            if r["prior"] != prior:
                continue
            log, rec = parse(r["post"]), parse_rec(r["rec"])
            for t, ir in log["ir"].items():
                h = log["human"].get(t)
                tr = truth(log, rec, t, LAG)
                if h is None or h[1] != "step" or tr["key"] is None or tr["key"] not in ir["tails"]:
                    continue
                d = round(vd_of(ir["tails"][tr["key"]]) / V, 2)
                c["D=0" if d == 0 else "D=1" if d == 1.0 else "other"] += 1
        tot = sum(c.values())
        print(f"  prior {prior}: {tot} ticks: " + ", ".join(f"{k} {v} ({100 * v / tot:.1f}%)" for k, v in sorted(c.items())))


if __name__ == "__main__":
    main()
