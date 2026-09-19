#!/usr/bin/env python3
"""
analysis/g1_graded_evidence/check.py — the checks of the graded-evidence build (a stretch's odds against
`unknown` are L / u^f, f the fraction of the expected path it covered; docs/recognizer_handback.md §1.5).

  --run <cond> <out.json>   one condition in-process through mesa_sim.run_mesa.run_headless (the plain run,
                            same argv as the sweep scripts), with the recognizer wrapped: an INDEPENDENT
                            accumulator of the accounting invariant
                                E_t(k)/E_t(unknown) = Π_closed L_k(s)/u^f_k(s) · Π_events c_k(e)
                                                      · (v_k(t)/u^f_k(t) | 1 if the open stretch is empty)
                            driven by the recognizer's phase state and the likelihood functions only, and a
                            per-tick record of the evidence state (the data the deferred θ decision asks
                            for: the top hypothesis's odds against unknown, the ratio of the top two, the
                            live-set size). Prints the log it wrote.
  --final <base_dir> <new_dir>
                            runs the 16 conditions (subprocesses, PYTHONHASHSEED=0), copies each log to
                            logs_instrumented/, checks it against <new_dir>/<cond>.log (the plain sweep,
                            instrumentation neutrality) on the CLAUDE.md greps, and writes summary.md
                            (invariant, reveals old → new, crossings, meta-planner decisions that moved)
                            and crossings.md (the θ data, every crossing ± 2 ticks). <base_dir> holds the
                            pre-change sweep (same conditions, same step counts).

    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/g1_graded_evidence/check.py \\
        --final <base_dir> <new_dir>
"""
import json
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE.parent))

PY = os.path.expanduser("~/python-envs/teamrob-sp4-env/bin/python")
COND = {  # cond: (layout, scenario, steps) — the sweep scripts' step counts
    "s00": ("env_layout0", "scenario_00", 300), "s10": ("env_layout1", "scenario_10", 450),
    "s20": ("env_layout2", "scenario_20", 300), "s30": ("env_layout3", "scenario_30", 200),
    "s40": ("env_layout4", "scenario_40", 400), "s50": ("env_layout5", "scenario_50", 300),
    "s70": ("env_layout7", "scenario_70", 300), "s71": ("env_layout7", "scenario_71", 300),
}
ORDER = [f"{c}_{p}" for c in COND for p in ("off", "on")]
GREPS = ["[meta] ", "meta-cand", "[meta-proj]", "[meta-pool]", "[IR] step=", "[IR-dist]", "[IR-complete]",
         "[sep]", "[hold]", "[stop]"]
UNKNOWN = "unknown"
ITEM = re.compile(r"deliver_item\(\?item=(item_\d+),\?kitting_table=kitting_table_0\)")


def short(k):
    return ITEM.sub(r"\1", k).replace("?ac_switch=", "").replace("?coffee_machine=", "")


# ---------------------------------------------------------------------------
# --run: one condition, instrumented
# ---------------------------------------------------------------------------

def run_one(cond, out_json):
    c, p = cond.split("_")
    lay, sc, st = COND[c]
    sys.argv = ["run_mesa.py", "--domain", "kitting", "--layout", lay, "--scenario", sc, "--steps", str(st),
                "--assignment_prior", "true" if p == "on" else "false",
                "--cost_strategy", "realized", "--gate_strategy", "none", "--separation_stop", "false"]
    from mesa_sim import run_mesa                  # first: it puts mesa_sim/ on the path (mesa_fork) and opens the log
    from shared import likelihood_functions as LF
    from shared import recognizer as R
    from shared.types import task_instance_key
    from shared.target_resolution import movement_target_position
    from mesa_sim import sim_model as SM

    model_ref = {}
    orig_model_init = SM.SimModel.__init__

    def model_init(self, *a, **kw):
        orig_model_init(self, *a, **kw)
        model_ref["m"] = self
    SM.SimModel.__init__ = model_init

    rows = []
    orig_rec_init = R.IntentionRecognizer.__init__

    def rec_init(rec, *a, **kw):
        orig_rec_init(rec, *a, **kw)
        acc = {}
        orig = rec.update

        def grade(action, origin, pos, world, arrived):
            """The accumulator's own reading of the grade: u^f, or u when the observation has no path."""
            if arrived or action is None or action.schema.progress_evaluator is None:
                return LF.UNKNOWN_LIKELIHOOD
            g = movement_target_position(action, world)
            if g is None:
                return LF.UNKNOWN_LIKELIHOOD
            expected = LF.straight_line_cost(origin, g)
            f = 0.0 if expected <= 0 else min(1.0, max(0.0, (expected - LF.straight_line_cost(pos, g)) / expected))
            return LF.UNKNOWN_LIKELIHOOD ** f

        def update(obs, world, prev_belief=None):
            before_e, before_o, before_oo = dict(rec._expected), dict(rec._origin), dict(rec._origin_odo)
            before_c = set(rec._completed)
            first = not before_e
            b = orig(obs, world, prev_belief)
            step = int(obs.timestamp); pos = obs.spatial_context.position; odo = rec._odometer[obs.agent_id]
            mu = (obs.detected_microaction or "").upper()
            for k in rec._completed - before_c:
                acc.pop(k, None)
            boundary = bool(rec._completed - before_c) and all(
                rec._origin_odo[k] == odo and rec._origin[k] == pos for k in rec._origin)
            if boundary:
                for k in rec._expected:
                    acc[k] = 1.0
            err_max = 0.0
            for k, a in rec._expected.items():
                if k not in before_e:
                    acc[k] = 1.0
                elif not boundary:
                    prev = before_e[k]
                    if prev is not None and rec._in_vocabulary(prev, mu):
                        acc[k] *= rec._completion_likelihood(prev, world, {})
                    if not rec._same_action(prev, a):
                        closing = rec._progress_likelihood(prev, before_o[k], odo - before_oo[k], pos, world, {})
                        if closing is not None:
                            arrived = prev.completion_predicate is not None and prev.completion_predicate in world.predicates
                            acc[k] *= closing / grade(prev, before_o[k], pos, world, arrived)
                v = rec._progress_likelihood(a, rec._origin[k], odo - rec._origin_odo[k], pos, world, {})
                odds = acc[k] * (1.0 if v is None else v / grade(a, rec._origin[k], pos, world, False))
                got = rec._evidence[k] / rec._evidence[UNKNOWN]
                err = abs(math.log(got) - math.log(odds)) if got > 0 and odds > 0 else float("inf")
                err_max = max(err_max, err)
            if first:
                return b            # the constructor's priming observation, before the clock (no belief logged)
            human = model_ref["m"].humans[obs.agent_id]
            ti = human.get_current_task_instance()
            truth = task_instance_key(ti) if (ti is not None and not human.finished) else UNKNOWN
            ev = {k: v / rec._evidence[UNKNOWN] for k, v in rec._evidence.items() if k != UNKNOWN}
            ranked = sorted(ev, key=lambda k: -ev[k])
            top = ranked[0] if ranked else None
            second = ranked[1] if len(ranked) > 1 else None
            rows.append(dict(step=step, truth=truth, most_likely=b.most_likely, confidence=b.confidence,
                             top=top, odds_top=ev.get(top), second=second, odds_second=ev.get(second),
                             live=len(ev), err=err_max, checks=len(rec._expected)))
            return b
        rec.update = update
    R.IntentionRecognizer.__init__ = rec_init

    run_mesa.run_headless()
    Path(out_json).write_text(json.dumps(rows))
    print(run_mesa.log_filename)


# ---------------------------------------------------------------------------
# --final
# ---------------------------------------------------------------------------

def grep(path, key):
    return [l for l in open(path, errors="replace") if l.startswith(key) or (key == "meta-cand" and "meta-cand" in l)]


def compare(a, b):
    """The CLAUDE.md greps of two logs: 'identical', or the greps that differ with the first differing step."""
    diffs = []
    for g in GREPS:
        la, lb = grep(a, g), grep(b, g)
        if la != lb:
            first = next((x for x, y in zip(la, lb) if x != y), None)
            first = first if first is not None else (la[len(lb)] if len(la) > len(lb) else lb[len(la)])
            m = re.search(r"step=(\d+)", first)
            diffs.append(f"{g.strip()}@{m[1] if m else '?'}")
    return "identical" if not diffs else ", ".join(diffs)


def crossings(rows, theta):
    """Ticks on which the belief first clears θ on a task hypothesis: (step, key, wrong)."""
    out = []
    prev = None
    for r in rows:
        cleared = r["most_likely"] != UNKNOWN and r["confidence"] >= theta
        if cleared and not (prev is not None and prev["most_likely"] == r["most_likely"] and prev["confidence"] >= theta):
            out.append((r["step"], r["most_likely"], r["most_likely"] != r["truth"]))
        prev = r
    return out


def crossings_from_log(path, truth_by_step, theta):
    rows = []
    for l in grep(path, "[IR] step="):
        m = re.match(r"\[IR\] step=(\d+) most_likely=(\S+) confidence=([\d.]+)", l)
        s = int(m[1])
        rows.append(dict(step=s, most_likely=m[2], confidence=float(m[3]), truth=truth_by_step.get(s, UNKNOWN)))
    return rows


def reveals(rows, theta):
    """Per human task episode (a run of ticks with one truth ≠ unknown): the first tick the truth is most_likely at
    ≥ θ, or '-'; the episode's last tick."""
    out = []
    cur = None
    for r in rows:
        t = r["truth"]
        if t == UNKNOWN:
            if cur:
                out.append(cur); cur = None
            continue
        if cur is None or cur["task"] != t:
            if cur:
                out.append(cur)
            cur = dict(task=t, start=r["step"], end=r["step"], reveal=None)
        cur["end"] = r["step"]
        if cur["reveal"] is None and r["most_likely"] == t and r["confidence"] >= theta:
            cur["reveal"] = r["step"]
    if cur:
        out.append(cur)
    return out


def final(base_dir, new_dir):
    import logparse
    from shared.meta_planner import DEFAULT_THETA as theta
    from shared import likelihood_functions as LF
    base_dir, new_dir = Path(base_dir), Path(new_dir)
    inst = HERE / "logs_instrumented"; inst.mkdir(exist_ok=True)
    data = HERE / "data"; data.mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONHASHSEED="0")
    S = [f"# Graded evidence — checks (generated by check.py; BETA={LF.BETA}, UNKNOWN_LIKELIHOOD={LF.UNKNOWN_LIKELIHOOD}, θ={theta})\n"]
    X = ["# Graded evidence — the θ data: every crossing of θ, ± 2 ticks\n",
         "A crossing is the first tick the belief clears θ on a task hypothesis (a new `most_likely`, or the same one",
         "back above θ). `odds` is the top task hypothesis's odds against `unknown` (the evidence state, before the",
         "output floor and pins); `ratio` its odds over the second task hypothesis's; `live` the number of live task",
         "hypotheses (`unknown` not counted). `wrong` marks a crossing whose `most_likely` is not the human's task.\n"]
    S.append("## Instrumentation and invariant\n\n| condition | log == plain sweep | invariant max |Δ log odds| (checks) |\n|---|---|---|")
    ok_all = True
    per = {}
    for cond in ORDER:
        js = data / f"{cond}.json"
        r = subprocess.run([PY, str(HERE / "check.py"), "--run", cond, str(js)], env=env, cwd=ROOT,
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stderr[-2000:]); raise SystemExit(f"{cond}: exit {r.returncode}")
        log = r.stdout.strip().splitlines()[-1]
        shutil.copy(ROOT / log, inst / f"{cond}.log")
        rows = json.loads(js.read_text())
        per[cond] = rows
        same = compare(inst / f"{cond}.log", new_dir / f"{cond}.log")
        errs = [x["err"] for x in rows]
        emax = max(errs) if errs else 0.0
        if same != "identical" or emax > 1e-9:
            ok_all = False
        S.append(f"| {cond} | {same} | {emax:.1e} ({sum(x['checks'] for x in rows)}) |")
    S.append("")

    # reveals old → new, crossings, wrong crossings
    S.append("## Reveals (first tick the human's task is `most_likely` at ≥ θ), old → new; crossings\n")
    S.append("| condition | task (ticks) | reveal old | reveal new | crossings old | crossings new |\n|---|---|---|---|---|---|")
    wrong_any = []
    for cond in ORDER:
        rows = per[cond]
        truth = {r["step"]: r["truth"] for r in rows}
        old_rows = crossings_from_log(base_dir / f"{cond}.log", truth, theta)
        # the human's script is fixed: the per-tick truth of the new run applies to the old log when the human's
        # own lines agree (checked here)
        hum = lambda p: [l for l in open(p, errors="replace") if "[human_0] task=" in l]
        assert hum(base_dir / f"{cond}.log") == hum(new_dir / f"{cond}.log"), f"{cond}: human lines differ"
        old_rev = {(e["task"], e["start"]): e["reveal"] for e in reveals(old_rows, theta)}
        new_rev = reveals(rows, theta)
        old_x = crossings(old_rows, theta); new_x = crossings(rows, theta)
        fx = lambda xs: ", ".join(f"{s} {short(k)}{' WRONG' if w else ''}" for s, k, w in xs) or "-"
        for i, e in enumerate(new_rev):
            S.append(f"| {cond if i == 0 else ''} | {short(e['task'])} ({e['start']}–{e['end']}) | "
                     f"{old_rev.get((e['task'], e['start']), '-') or '-'} | {e['reveal'] or '-'} | "
                     f"{fx(old_x) if i == 0 else ''} | {fx(new_x) if i == 0 else ''} |")
        if not new_rev:
            S.append(f"| {cond} | - | - | - | {fx(old_x)} | {fx(new_x)} |")
        wrong_any += [(cond, s, short(k)) for s, k, w in new_x if w]
        # crossings.md
        X.append(f"## {cond}\n")
        by = {r["step"]: r for r in rows}
        for s, k, w in new_x:
            X.append(f"### crossing at {s}: {short(k)}{' — WRONG (truth ' + short(by[s]['truth']) + ')' if w else ''}\n")
            X.append("| tick | truth | most_likely | confidence | top | odds | second | ratio | live |\n|---|---|---|---|---|---|---|---|---|")
            for t in range(s - 2, s + 3):
                r = by.get(t)
                if r is None:
                    continue
                ratio = (r["odds_top"] / r["odds_second"]) if r["odds_second"] else float("inf")
                X.append(f"| {t} | {short(r['truth'])} | {short(r['most_likely'])} | {r['confidence']:.3f} | {short(r['top'])} | "
                         f"{r['odds_top']:.3g} | {short(r['second']) if r['second'] else '-'} | {ratio:.3g} | {r['live']} |")
            X.append("")
    S.append("")
    S.append(f"Wrong-task crossings (new): {', '.join(f'{c} {s} {k}' for c, s, k in wrong_any) if wrong_any else 'none'}\n")

    # meta-planner decisions that moved
    S.append("## Meta-planner decisions, old → new (consequences, not judged)\n")
    S.append("| condition | greps that differ (first differing step) | decisions old | decisions new | completion old → new (world tick) |\n|---|---|---|---|---|")
    for cond in ORDER:
        a, b = logparse.parse(base_dir / f"{cond}.log"), logparse.parse(new_dir / f"{cond}.log")
        fd = lambda run: "; ".join(f"{d['step']} {d['trigger']}→{short(d['winner'])}" for d in run["decisions"])
        comp = lambda run: (run["releases"][-1] + 1) if run["releases"] and run["declared"] else "-"
        S.append(f"| {cond} | {compare(base_dir / f'{cond}.log', new_dir / f'{cond}.log')} | {fd(a)} | {fd(b)} | {comp(a)} → {comp(b)} |")
    S.append(f"\nOVERALL: {'PASS' if ok_all else 'FAIL'} (instrumentation neutral on every grep, invariant ≤ 1e-9)\n")
    (HERE / "summary.md").write_text("\n".join(S))
    (HERE / "crossings.md").write_text("\n".join(X))
    print("\n".join(S))
    return 0 if ok_all else 1


if __name__ == "__main__":
    if sys.argv[1] == "--run":
        run_one(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "--final":
        sys.exit(final(sys.argv[2], sys.argv[3]))
