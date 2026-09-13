#!/usr/bin/env python3
"""
analysis/i4b_boundary/check_i4b.py — the I4b matrix: the shipped boundary (A, phase-attributed) against
the rejected candidates and the readings of the principle, all as analysis-only monkeypatches on I4's
harness (analysis/i4_evidence_model/check_i4.py, reused).

Variants (none but `base` shipped):
  nobound    the boundary disabled — must equal I4 (baseline/)
  A_release  A with the RELEASE microaction as the attribution (the domain-assumption reading)
  B          after any retirement, the first tick at which any hypothesis's expected action changes
  C5         the observed agent's 5th consecutive stationary tick (N = 5 read from candidates.py)
  D          any tick at which any hypothesis's expected action changes
  fold       A, but every live hypothesis's open-stretch value is folded into its base before the origin
             moves ("keep the belief" read literally: the belief at the boundary tick is preserved exactly)
  ungated    A + the completion channel judged on every expected action at a discrete tick (Task 2)
  ownshelf   A + rivals decomposed as if nothing were held (TODO-55 (c), re-measured)

  --final [--variants]   eight conditions; summary.md, metrics.csv, the CSVs, logs_instrumented/<variant>/
  --sweep                the fine (β, u) grid under the shipped boundary (criterion 6)
    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/i4b_boundary/check_i4b.py --final --variants
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "i4_evidence_model"))
import check_i4 as I4                                   # noqa: E402
from check_i4 import ORDER, short, metrics, compare_logs, unit_checks   # noqa: E402
from shared import likelihood_functions as LF          # noqa: E402

I4.HERE = HERE      # sweeps and the run_mesa comparison read/write this directory


def _reset(rec, obs):
    pos = obs.spatial_context.position; odo = rec._odometer[obs.agent_id]
    for k in rec._origin:
        rec._origin[k], rec._origin_odo[k] = pos, odo


def setup_nobound(rec, model, human):
    rec._task_boundary = lambda previous, actions: False


def setup_A_release(rec, model, human):
    cell = {"mu": ""}
    rec._task_boundary = lambda previous, actions: cell["mu"] == "RELEASE"
    orig = rec.update
    def update(obs, world, prev_belief=None):
        cell["mu"] = (obs.detected_microaction or "").upper()
        return orig(obs, world, prev_belief)
    rec.update = update


def _wrapped(rec, decide):
    """Disable the shipped rule; `decide(rec, obs, before_expected, before_completed) -> bool` fires a reset
    after the tick's update."""
    rec._task_boundary = lambda previous, actions: False
    orig = rec.update
    def update(obs, world, prev_belief=None):
        before_e, before_c = dict(rec._expected), set(rec._completed)
        b = orig(obs, world, prev_belief)
        if decide(rec, obs, before_e, before_c):
            _reset(rec, obs)
        return b
    rec.update = update


def setup_B(rec, model, human):
    state = {"pending": False}
    def decide(rec, obs, before_e, before_c):
        if rec._completed - before_c:
            state["pending"] = True
        advanced = any(k in before_e and not rec._same_action(before_e[k], a) for k, a in rec._expected.items())
        if state["pending"] and advanced:
            state["pending"] = False
            return True
        return False
    _wrapped(rec, decide)


def setup_C5(rec, model, human):
    state = {"pos": None, "n": 0}
    def decide(rec, obs, before_e, before_c):
        p = obs.spatial_context.position
        state["n"] = state["n"] + 1 if p == state["pos"] else 1
        state["pos"] = p
        return state["n"] == 5
    _wrapped(rec, decide)


def setup_D(rec, model, human):
    def decide(rec, obs, before_e, before_c):
        return any(k in before_e and not rec._same_action(before_e[k], a) for k, a in rec._expected.items())
    _wrapped(rec, decide)


def setup_fold(rec, model, human):
    """A's criterion, with the open-stretch value folded into the base before the origin moves."""
    def decide(rec, obs, before_e, before_c):
        newly = rec._completed - before_c
        if not newly:
            return False
        # attribution as shipped: the retired hypothesis expected its terminal action on the previous tick
        fired = False
        for k in newly:
            acts = rec._tick_actions.get(k)
            if acts and rec._same_action(before_e.get(k), acts[-1]):
                fired = True
        if fired:
            for k in list(rec._origin):
                rec._base[k] = rec._evidence[k]        # base × open value → the belief at this tick, kept
        return fired
    _wrapped(rec, decide)


SETUPS = {"nobound": setup_nobound, "A_release": setup_A_release, "B": setup_B, "C5": setup_C5, "D": setup_D,
          "fold": setup_fold}
I4_VARIANTS = ["ungated", "ownshelf"]


def final(with_variants):
    beta, unknown = LF.BETA, LF.UNKNOWN_LIKELIHOOD
    lines = [f"# I4b checks — generated by check_i4b.py (BETA={beta}, UNKNOWN_LIKELIHOOD={unknown})\n"]
    lines.append("## Unit checks (I4's, re-run)\n\n| check | result | detail |\n|---|---|---|")
    ok_all = True
    for n, ok, d in unit_checks():
        ok_all &= ok
        lines.append(f"| {n} | {'PASS' if ok else 'FAIL'} | {d} |")
    lines.append("")
    variants = ["base"] + (list(SETUPS) + I4_VARIANTS if with_variants else [])
    csv_rows = defaultdict(list); all_metrics = []
    for variant in variants:
        title = ("Instrumented sweep (variant `base` = the shipped code: boundary A)" if variant == "base"
                 else f"Variant `{variant}` (analysis-only monkeypatch)")
        lines.append(f"## {title}\n")
        lines.append("| condition | log == ref | boundaries (step) | completions | θ crossings (`!` = winner ≠ truth) | reveals | wrong-θ ticks (task) | max conf | unknown when idle |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for name in ORDER:
            log_dir = HERE / f"logs_instrumented/{variant}"
            kw = {"variant": variant} if variant in I4_VARIANTS else {"setup": SETUPS.get(variant)}
            rows, st = I4.run_condition(name, beta, unknown, log_dir=log_dir, collect=True, **kw)
            m = metrics(name, rows); m["variant"] = variant; all_metrics.append(m)
            same = ""
            ref = {"base": HERE / "new", "nobound": HERE / "baseline"}.get(variant)
            if ref is not None:
                same = compare_logs(log_dir / f"{name}.log", ref / f"{name}.log") if (ref / f"{name}.log").exists() else "n/a"
                if same is False and variant == "base":
                    ok_all = False
            bnd = [l.split("step=")[1].split(" ")[0] for l in open(log_dir / f"{name}.log") if l.startswith("[IR-boundary]")]
            comps = ", ".join(f"{s}:{short(k)}" for s, k, _, _ in st["completions"])
            if st["aborted"]:
                comps += f" — ABORTED at step {st['aborted'][0]} ({st['aborted'][1]}, TODO-52)"
            lines.append(f"| {name} | {same} | {' '.join(bnd) or '-'} | {comps} | {m['crossings'] or '-'} | {m['reveals']} | "
                         f"{m['wrong_theta_ticks']} ({m['wrong_theta_task_ticks']}) | {m['max_conf']} | {m['unknown_when_idle']} |")
            if name.startswith("s40"):
                s40 = "; ".join(f"{k}={m[k]}" for k in ("coffee_max_seg2", "coffee_theta_ticks_seg2", "deliver_max_seg2", "item6_3a_end",
                                                        "item6_3b_start_end", "max_task_seg3", "unknown_end_seg3", "ac_max_184_271",
                                                        "ac_most_likely_ticks_184_271", "at_272"))
                lines.append(f"| ↳ s40 | {s40} | | | | | | | |")
            tag = name if variant == "base" else f"{variant}/{name}"
            big = variant == "base" or name.startswith("s40")
            csv_rows["completions"] += [(tag, s, short(k), act, mu) for s, k, act, mu in st["completions"]]
            csv_rows["completion_events"] += [(tag, s, mu, short(k), a, p, v, f"{o:.3f}" if o is not None else "") for s, mu, k, a, p, v, o in st["events"]]
            if big:
                csv_rows["phase_advances"] += [(tag, s, short(k), a, b) for s, k, a, b in st["advances"]]
                csv_rows["excess"] += [(tag, s, short(k), a, ex, base, p) for s, k, a, ex, base, p in st["excess"]]
                csv_rows["trace"] += [(tag, r["step"], r["segment"], r["truth"], r["human_action"], r["human_micro"], r["human_holding"],
                                       r["most_likely"], round(r["confidence"], 4)) + tuple(round(v, 4) for v in r["dist"].values()) for r in rows]
        lines.append("")
    headers = {
        "completions": ["condition", "step", "hypothesis", "human_action", "human_micro"],
        "completion_events": ["condition", "step", "microaction", "hypothesis", "judged_action", "predicate", "likelihood", "output_belief"],
        "phase_advances": ["condition", "step", "hypothesis", "from", "to"],
        "excess": ["condition", "step", "hypothesis", "expected_action", "excess_cm", "base", "belief"],
        "trace": ["condition", "step", "segment", "truth", "human_action", "human_micro", "human_holding", "most_likely", "confidence", "dist..."],
    }
    for fname, header in headers.items():
        with open(HERE / f"{fname}.csv", "w", newline="") as f:
            w = csv.writer(f); w.writerow(header); w.writerows(csv_rows[fname])
    with open(HERE / "metrics.csv", "w", newline="") as f:
        keys = sorted({k for m in all_metrics for k in m}, key=lambda k: (k not in ("variant", "condition"), k))
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(all_metrics)
    lines.append(f"\nOVERALL: {'PASS' if ok_all else 'FAIL'}\n")
    (HERE / "summary.md").write_text("\n".join(lines))
    print("\n".join(lines))
    return 0 if ok_all else 1


if __name__ == "__main__":
    if "--sweep" in sys.argv:
        I4.sweep(frac=False, fine=True)
    else:
        sys.exit(final("--variants" in sys.argv))
