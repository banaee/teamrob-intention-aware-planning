#!/usr/bin/env python3
"""
decision_panel.py — the decision panel of the planning test-bed's figures (the figures rule, Hadi, 5 October 2026;
design_records.md, "T-F part 1", THE FIGURES): what the robot did with what it believed, on the run's tick axis, the
same panel in every condition so the conditions compare by eye. From the run's own outputs (actual.py): the decisions
(actual_decisions.json), their winners and holds (selection.json), the robot's task per tick (robot.json).

Three rows:
- robot task: the robot's current task over the ticks (a band per task, named at its start), the decided holds over
  it (hatched, from the decision tick for the hold's length, labelled);
- projection: what each decision rested on: the admitted task (a filled mark, named where it differs from the last
  admitted task named), the fallback projection (an open
  mark and a bar to the fallback's end), or none (a cross);
- decision: each decision's tick, the mark by trigger (■ no_current_task, ● recognition_changed, ▲ projection_expired),
  the cause of a recognition_changed written above it; where the oracle's chain exists (expected_decisions.json), the
  expected decision ticks as thin green lines on the row (they were the old figure.png's, which the one figure of N
  replaces; the measurement of T-F part 1).

`settings_text(log)`: the run's settings from its [run] header (the effective values), for the figures' titles.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "irb"))
import plot as ir_plot                                  # analysis/instruments/irb/plot.py: the settings line

MARK = {"no_current_task": ("s", "tab:gray"), "recognition_changed": ("o", "tab:blue"),
        "projection_expired": ("^", "tab:orange")}
TASKS = ["#c9dcf3", "#f7d2c0", "#c6eadb", "#d8d2ee"]          # light bands for the robot's tasks, cycling
HOLD = "tab:orange"
INK, MUTED = "#0b0b0b", "#8a8880"


def short(key):
    """A key without its parameter names: deliver_item(?item=x,?kitting_table=t) -> deliver_item(x,t)."""
    return re.sub(r"\?\w+=", "", key or "")


def settings_text(log) -> str:
    """The run's settings, the strategy first, as its [run] header printed them (effective values)."""
    return ir_plot.settings_text(log)


def draw(ax, d, horizon):
    d = Path(d)
    decisions = [x for x in json.load(open(d / "actual_decisions.json")) if x["tick"] < horizon]
    sel = {s["tick"]: s for s in json.load(open(d / "selection.json"))}
    robot = [a for a in json.load(open(d / "robot.json")) if a["tick"] < horizon]
    # robot task: a band per stretch of one task
    stretches = []
    for a in robot:
        if stretches and stretches[-1][2] == a["task"] and a["tick"] == stretches[-1][1] + 1:
            stretches[-1][1] = a["tick"]
        else:
            stretches.append([a["tick"], a["tick"], a["task"]])
    colours = {}
    for t0, t1, task in stretches:
        if task is None:
            continue
        c = colours.setdefault(task, TASKS[len(colours) % len(TASKS)])
        ax.broken_barh([(t0 - 0.5, t1 - t0 + 1)], (1.7, 0.6), color=c, lw=0)
        ax.text(t0, 2.0, " " + short(task), fontsize=6.5, va="center", color=INK)
    for t, s in sel.items():
        if s.get("hold") and t < horizon:
            ax.broken_barh([(t - 0.5, s["hold"])], (1.72, 0.56), facecolor="none", edgecolor=HOLD, hatch="////", lw=0.8)
            ax.text(t + s["hold"], 2.36, f"hold {s['hold']}", fontsize=6.5, color=HOLD, ha="right")
    # the expected decisions (the oracle's chain), thin green lines on the decision row
    if (d / "expected_decisions.json").exists():
        for x in json.load(open(d / "expected_decisions.json")):
            if x["tick"] < horizon:
                ax.plot([x["tick"], x["tick"]], [-0.4, 0.4], color="tab:green", lw=0.8, alpha=0.7)
    # projection and decision; an admitted task is named where it differs from the last one named
    named = None
    for x in decisions:
        m, c = MARK[x["trigger"]]
        ax.scatter([x["tick"]], [0], marker=m, s=34, facecolors="none", edgecolors=c, lw=1.1)
        if x.get("cause"):
            ax.text(x["tick"], 0.28, x["cause"], fontsize=6, color=c, ha="center", rotation=90, va="bottom")
        if x.get("admitted"):
            ax.scatter([x["tick"]], [1], marker="o", s=30, color=INK)
            if x["admitted"]["key"] != named:
                ax.text(x["tick"] + 0.8, 1.12, short(x["admitted"]["key"]), fontsize=6.5, color=INK, va="bottom")
                named = x["admitted"]["key"]
        elif x.get("fallback"):
            ax.plot([x["tick"], x["fallback"]["end"]], [1, 1], color=MUTED, lw=3, alpha=0.45, solid_capstyle="butt")
            ax.scatter([x["tick"]], [1], marker="o", s=30, facecolors="white", edgecolors=MUTED, lw=1.1)
        else:
            ax.scatter([x["tick"]], [1], marker="x", s=26, color=MUTED, lw=1.1)
    ax.set_yticks([0, 1, 2], ["decision", "projection", "robot task"], fontsize=7.5)
    ax.set_ylim(-0.5, 2.7)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


# the panel's key, written under the figure by the builder (analysis/instruments/irb/plot.py, `draw`)
KEY = ("decision panel — projection: ● admitted (named)  ○ fallback (bar to its end)  × none;  decision: ■ no_current_task  "
       "● recognition_changed (cause above)  ▲ projection_expired;  green line: expected (the oracle);  hatched: hold")
