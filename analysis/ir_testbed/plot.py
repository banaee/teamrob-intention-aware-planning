#!/usr/bin/env python3
"""
plot.py — one figure per scenario for the IR test-bed (TB.3b): the belief per hypothesis and S per hypothesis over
ticks (expected as lines, actual as markers every fifth tick), the finding and the lifecycle as a band, and the
script's action boundaries (trajectory.json) as thin vertical lines, the task starts labelled. θ and α are read from
the run's [run] header; a hypothesis or task is labelled by its key without the parameter names. No id, coordinate or
tick is written here (TB.4b).

    plot.py <scenario dir> <run.log>
"""
import csv
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]          # categorical slots 1 to 3 (all-pairs valid), fixed order by key
BAND = {"unresolved": "#cfcdc6", "adequate": "#eeede9", "unexplained": "#e34948", "exhausted": "#8a8880"}
INK, MUTED = "#0b0b0b", "#8a8880"


def header(log):
    """θ and α from the run's [run] header."""
    for l in open(log):
        if l.startswith("[run] "):
            h = dict(re.findall(r"(\w+)=(\S+)", l))
            return float(h["theta"]), float(h["test_level"])
    raise ValueError(f"{log}: no [run] header")


def read(path):
    return [r for r in csv.DictReader(open(path)) if int(r["tick"]) >= 0]


def series(rows, col):
    out = {}
    for r in rows:
        if r["key"]:
            out.setdefault(r["key"], {})[int(r["tick"])] = float(r[col]) if r[col] != "" else None
    return out


def short(k):
    """A key without its parameter names: deliver_item(?item=x) -> deliver_item(x)."""
    return re.sub(r"\?\w+=", "", k)


def main(d, log):
    d = Path(d)
    THETA, alpha = header(log)
    exp, act = read(d / "expected.csv"), read(d / "actual.csv")
    traj = json.load(open(d / "trajectory.json"))
    keys = sorted({r["key"] for r in exp if r["key"]})
    assert len(keys) <= len(SERIES), f"{len(keys)} hypotheses; the palette validates {len(SERIES)} all-pairs"
    color = dict(zip(keys, SERIES))
    T = max(int(r["tick"]) for r in exp)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 7.2), sharex=True,
                                        gridspec_kw=dict(height_ratios=[3, 3, 0.45], hspace=0.08))
    for ax, col, ylabel in ((ax1, "belief", "belief"), (ax2, "S", "tail probability S")):
        e, a = series(exp, col), series(act, col)
        for k in keys:
            ts = range(T + 1)
            ys = [e.get(k, {}).get(t) for t in ts]
            ax.plot(list(ts), [float("nan") if y is None else y for y in ys], color=color[k], lw=2, label=short(k))
            at = [t for t in sorted(a.get(k, {})) if t % 5 == 0 and a[k][t] is not None]
            ax.plot(at, [a[k][t] for t in at], "o", ms=3.5, color=color[k], mec="white", mew=0.6)
        ax.set_ylabel(ylabel, color=INK)
        ax.set_ylim(-0.03, 1.05)
        ax.grid(axis="y", color="#e6e5e0", lw=0.6)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    ax1.axhline(THETA, color=MUTED, lw=0.8, ls="--")
    ax1.text(T, THETA + 0.015, f"θ = {THETA:g}", ha="right", va="bottom", fontsize=8, color=MUTED)
    ax2.axhline(alpha, color=MUTED, lw=0.8, ls="--")
    ax2.text(T, alpha + 0.015, f"α = {alpha:g}", ha="right", va="bottom", fontsize=8, color=MUTED)
    ax1.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), frameon=False, fontsize=9,
               title="lines expected, dots actual", title_fontsize=8)
    # the band: the finding, or the lifecycle when exhausted
    state = {}
    for r in act:
        state[int(r["tick"])] = r["finding"] if r["lifecycle"] == "live" else "exhausted"
    for t, s in state.items():
        ax3.axvspan(t - 0.5, t + 0.5, color=BAND[s], lw=0)
    ax3.set_yticks([])
    ax3.set_ylabel("finding", rotation=0, ha="right", va="center", color=INK)
    ax3.legend(handles=[Patch(color=BAND[s], label=s) for s in BAND], loc="upper left", bbox_to_anchor=(1.0, 1.6),
               frameon=False, fontsize=8)
    ax3.set_xlabel("tick")
    ax3.set_xlim(-1, T + 1)
    # the script's action boundaries; the task starts labelled
    last_task = None
    for b in traj["actions"]:
        for ax in (ax1, ax2):
            ax.axvline(b["tick"], color="#d9d8d2", lw=0.6, zorder=0)
        if b["task"] != last_task:
            ax1.text(b["tick"] + 1, 1.05, short(b["task"]), fontsize=7.5, color=INK, va="bottom", rotation=0)
            last_task = b["task"]
    fig.suptitle(f"{traj['scenario']} on {traj['layout']}, prior on", x=0.06, ha="left", fontsize=11, color=INK)
    fig.savefig(d / "figure.png", dpi=130, bbox_inches="tight")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
