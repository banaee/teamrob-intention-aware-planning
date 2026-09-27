#!/usr/bin/env python3
"""
The clip (E10, decision 3 of the 1.5b plan step): the ticks, prior off, on which the belief's value for a live
hypothesis's walk is changed by the clip of L(v·D) at v·D <= 0 where 1.3b read L(e) with a negative excess e (a
moving target: an item the robot carries resolves through its holder). 1.3b's value there was L(e) > 1; now it is
L(v·D) (1 when v·D <= 0).

One run of the simulator per call, with the run options given on the command line (the sweep's); the robot's
recognizer's _phase_likelihood is wrapped here, in this script only, to note every call on a walk with walked
path > 0 and e < 0 (the fold and the open phase alike): the tick, the hypothesis, e, the 1.3b value L(e) and the
1.5b value. Prints ranges per hypothesis. Nothing else is changed.

Run from the repo root, e.g.
  PYTHONHASHSEED=0 ~/python-envs/ir-nomesa-env/bin/python analysis/l_build/clip_ticks.py 300 --domain kitting \
      --layout env_layout_01 --scenario scenario_s01_01 --cost_strategy realized --gate_strategy none \
      --separation_stop false --assignment_prior false
"""
import logging, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "mesa_sim"))
STEPS = int(sys.argv[1])
sys.argv = ["run_mesa.py", "--steps", str(STEPS)] + sys.argv[2:]
logging.disable(logging.CRITICAL)
import run_mesa  # noqa: E402
from shared import likelihood_functions as LF  # noqa: E402
from shared.recognizer import IntentionRecognizer  # noqa: E402


def main():
    model = run_mesa._make_domain_model()
    rec = next(iter(model.robots.values())).recognizer
    notes = []
    orig = IntentionRecognizer._phase_likelihood

    def wrapped(self, key, action, pos, odo, still, world, memo):
        value = orig(self, key, action, pos, odo, still, world, memo)
        if self is rec and action is not None and action.schema.progress_evaluator is not None:
            walked = odo - self._origin_odo[key]
            e = self._excess(action, self._origin[key], walked, pos, world, memo)
            if walked > 0.0 and e < 0.0:
                notes.append((int(self._history[-1].timestamp), key, e, LF.logistic_of_excess(e, self._beta), value))
        return value

    IntentionRecognizer._phase_likelihood = wrapped
    for _ in range(STEPS):
        if model.running is False:
            break
        model.step()
    by = {}
    for t, k, e, old, new in notes:
        by.setdefault(k, []).append((t, e, old, new))
    if not by:
        print("  no tick with e < 0 on a walk")
    for k, xs in by.items():
        ticks = sorted({t for t, *_ in xs})
        ranges, start = [], ticks[0]
        for a, b in zip(ticks, ticks[1:] + [None]):
            if b != a + 1:
                ranges.append(f"{start}-{a}" if a != start else f"{a}")
                start = b
        emin = min(e for _, e, _, _ in xs)
        oldmax = max(o for _, _, o, _ in xs)
        print(f"  {k}: {len(ticks)} ticks at {','.join(ranges)}; min e {emin:.2e} cm; 1.3b L(e) up to 1 + {oldmax - 1:.1e}, "
              f"1.5b value {min(n for *_, n in xs):.3f}-{max(n for *_, n in xs):.3f}")


if __name__ == "__main__":
    main()
