#!/usr/bin/env python3
"""
plot.py — one figure per scenario for the IRB (IRB.3b): the belief per hypothesis and S per hypothesis over
ticks (expected as lines, actual as markers every fifth tick), the finding and the lifecycle as a band, and the
script's action boundaries (trajectory.json) as thin vertical lines, the task starts labelled. Since G-build a fourth
panel: per hypothesis, the ticks it holds observation warrant (expected as a bar, actual as a dot every tick), and the
ticks the gate clears (the leader admissible: θ, adequate, warranted; T-D G), expected bar, actual dots. θ and α are read from
the run's [run] header; a hypothesis or task is labelled by its key without the parameter names. No id, coordinate or
tick is written here (IRB.4b).

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

# categorical slots 1 to 4, fixed order by key; the four pass every check over all pairs (the dataviz validator, light;
# violet as slot 4, since the sort). More than four hypotheses: the figure is faceted, four per figure (figure.png,
# figure_2.png, ...), every hypothesis keeping its slot within its figure; a fifth slot fails the normal-vision floor.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"]
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
    every = sorted({r["key"] for r in exp if r["key"]})
    groups = [every[i:i + len(SERIES)] for i in range(0, len(every), len(SERIES))] or [[]]
    for n, keys in enumerate(groups):
        name = "figure.png" if n == 0 else f"figure_{n + 1}.png"
        part = "" if len(groups) == 1 else f" (hypotheses {n * len(SERIES) + 1} to {n * len(SERIES) + len(keys)} of {len(every)})"
        figure(d, exp, act, traj, THETA, alpha, keys, name, part)


def figure(d, exp, act, traj, THETA, alpha, keys, name, part):
    color = dict(zip(keys, SERIES))
    T = max(int(r["tick"]) for r in exp)
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 8.6), sharex=True,
                                             gridspec_kw=dict(height_ratios=[3, 3, 0.45, 1.3], hspace=0.08))
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
    # warrant per hypothesis and the gate's clearing (T-D G): expected bars, actual dots
    rows4 = keys + ["gate clears"]
    for i, k in enumerate(rows4):
        y = len(rows4) - 1 - i
        c = INK if k == "gate clears" else color[k]
        if k == "gate clears":
            e_on = sorted({int(r["tick"]) for r in exp if r["gate"] == "clears"})
            a_on = sorted({int(r["tick"]) for r in act if r["gate"] == "clears"})
        else:
            e_on = [int(r["tick"]) for r in exp if r["key"] == k and r["warrant"] == "observation"]
            a_on = [int(r["tick"]) for r in act if r["key"] == k and r["warrant"] == "observation"]
        ax4.broken_barh([(t - 0.5, 1) for t in e_on], (y - 0.3, 0.6), color=c, alpha=0.35, lw=0)
        ax4.plot(a_on, [y] * len(a_on), "|", ms=5, color=c)
    ax4.set_yticks(range(len(rows4)))
    ax4.set_yticklabels([("warrant " + short(k)) if k != "gate clears" else k for k in reversed(rows4)], fontsize=7.5)
    ax4.set_ylim(-0.6, len(rows4) - 0.4)
    for s in ("top", "right"):
        ax4.spines[s].set_visible(False)
    ax4.set_xlabel("tick")
    ax4.set_xlim(-1, T + 1)
    # the script's action boundaries; the task starts labelled
    last_task = None
    for b in traj["actions"]:
        for ax in (ax1, ax2):
            ax.axvline(b["tick"], color="#d9d8d2", lw=0.6, zorder=0)
        if b["task"] != last_task:
            ax1.text(b["tick"] + 1, 1.05, short(b["task"]), fontsize=7.5, color=INK, va="bottom", rotation=0)
            last_task = b["task"]
    fig.suptitle(f"{traj['scenario']} on {traj['layout']}, prior on{part}", x=0.06, ha="left", fontsize=11, color=INK)
    fig.savefig(d / name, dpi=130, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
