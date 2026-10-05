#!/usr/bin/env python3
"""
plot.py <scenario> <dir> <run.log> — the planning test-bed's figure of a run: one file, figure.png, every panel on one
shared tick axis over the comparison horizon (observed.json), drawn by the IRB's builder (analysis/instruments/irb/
plot.py, `draw`).

Since the measurement of T-F part 1 (N, Hadi, 5 October 2026; design_records.md, "T-F part 1", THE MEASUREMENT): the
two figures of a run (figure.png, the gate and the distance; figure_ir.png, the recognition and the decision panel,
faceted into figure_ir_2.png, ... beyond four hypotheses) are replaced by this one. The panels, each where the run has
it: the belief over H; the context panel (context knowledge on); the tail probability S; the adequacy finding; the
observation warrant per hypothesis and the gate's answer per tick, one row per answer (clears or the refusal's reason);
the decision panel (decision_panel.py: the robot's task and the holds, the projection each decision rested on, the
decisions by trigger and cause, the oracle's expected decisions); the robot–human distance on a scale readable near
min_separation, the ticks below it shaded by F1's class. Expected values (the oracle's table, expected_ticks.json) as
lines and bars, actual (actual.py's actual_ticks.json) as dots and marks; with no oracle table the actual alone.
The condition is read from the run's [run] header (its effective values): human-unaware, no recognition panel and no
gate row (admission refuses with none(no_human) before the gate is asked); intention-unaware, no recognition panel, the
gate's answer per tick (none(intention_off)); intention-aware, every panel. The title: the scenario and layout, the
condition, the run's settings (the strategy first).
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import decision_panel                                  # the decision panel (T-F part 1); imports irb/plot.py as `plot`
import plot_ir                                         # the recognition rows from the per-tick tables
ir_plot = decision_panel.ir_plot


def condition(log):
    h = dict(re.findall(r"(\w+)=(\S+)", next(l for l in open(log) if l.startswith("[run] "))))
    return "human-unaware" if h.get("human_aware") == "off" else \
        "intention-unaware" if h.get("intention_aware") == "off" else "intention-aware"


def main(sid, d, log):
    d = Path(d)
    H = json.load(open(d / "observed.json"))["horizon"]
    exp = [t for t in json.load(open(d / "expected_ticks.json")) if t["tick"] < H] \
        if (d / "expected_ticks.json").exists() else []
    act = [t for t in json.load(open(d / "actual_ticks.json")) if t["tick"] < H]
    traj = json.load(open(d / "trajectory.json"))
    cond = condition(log)
    recog = gate = None
    if cond == "intention-aware":
        # the hypotheses of H (the belief over H's keys over the run), not the robot's items the reported belief holds
        # at the output floor
        keys = sorted({k for t in (exp or act) for k in t.get("belief_h") or t["belief"]})
        recog = dict(exp=plot_ir.rows(exp, keys, lambda t: t["belief"], lambda t: t["S"]),
                     act=plot_ir.rows(act, keys, lambda t: t["belief"], lambda t: t["S"]))
    elif cond == "intention-unaware":
        gate = dict(exp={t["tick"]: t["gate"] for t in exp}, act={t["tick"]: t["gate"] for t in act})
    title = (f"{sid} on {traj['layout']} ({cond}){'' if exp or cond != 'intention-aware' else ', no oracle table'}\n"
             f"{decision_panel.settings_text(log)}"
             + ("" if cond == "intention-aware" else "; no belief, the recognizer does not run"))
    ir_plot.draw(d / "figure.png", log=log, T=H - 1, title=title, recog=recog, traj=traj, gate=gate,
                 decisions=lambda ax: decision_panel.draw(ax, d, H), key=decision_panel.KEY)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
