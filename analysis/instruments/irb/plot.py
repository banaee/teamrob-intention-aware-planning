#!/usr/bin/env python3
"""
plot.py — one figure per scenario for the IRB (IRB.3b): the belief per hypothesis (since T-K part 1's gate stage the
belief over H, `belief_h`, the value the gate compares with θ; AM42) and S per hypothesis over
ticks (expected as lines, actual as markers every fifth tick), the finding and the lifecycle as a band, and the
script's action boundaries (trajectory.json) as thin vertical lines, the task starts labelled. Since G-build a fourth
panel: per hypothesis, the ticks it holds observation warrant (expected as a bar, actual as a dot every tick), and the
ticks the gate clears (the leader admissible: θ, adequate, warranted; T-D G), expected bar, actual dots. θ and α are read from
the run's [run] header; a hypothesis or task is labelled by its key without the parameter names. No id, coordinate or
tick is written here (IRB.4b).
Since T-F part 1 (the standing rule on figures, Hadi, 5 October 2026; design_records.md, "T-F part 1", THE FIGURES):
with context knowledge on (the run log holds `[IR-context]` lines), a panel directly under the belief shows, per tick,
the context facts in force as the mind read them (`facts=`: a timeline fact, labelled `timeline` when the run's
`[run_mesa] timeline` line names it, else an object state, labelled `state`) and the recency facts (`recent=`); with
context knowledge off the figure is as before. With no expected table (a planning run with no oracle: assignment
knowledge off, a script that depends on the robot) the actual values are drawn as lines, alone. A caller may add a
last panel on the same tick axis (`extra`, the planning test-bed's decision panel) and a line of settings to the title.

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


CTX = re.compile(r"^\[IR-context\] step=(-?\d+) facts=\[([^\]]*)\] recent=\[([^\]]*)\]")


def context(log):
    """Per tick the context facts in force and the recency facts the mind read ([IR-context]), and the run's timeline
    line; None with context knowledge off (no [IR-context] line)."""
    rows, timeline = {}, ""
    for l in open(log):
        if l.startswith("[run_mesa] timeline"):
            timeline = l
        m = CTX.match(l)
        if m:
            rows[int(m[1])] = (m[2].split(), m[3].split())
    return None if not rows else (rows, timeline)


def context_panel(ax, ctx, T):
    rows, timeline = ctx
    facts = sorted({f for fs, _ in rows.values() for f in fs})
    recent = sorted({r for _, rs in rows.values() for r in rs})
    label = lambda f: ("timeline " if f.split("(")[0] in timeline else "state ") + f.replace("()", "")
    lines = [(label(f), lambda t, f=f: f in rows.get(t, ((), ()))[0]) for f in facts] + \
            [("recent " + r, lambda t, r=r: r in rows.get(t, ((), ()))[1]) for r in recent]
    for i, (name, holds) in enumerate(lines):
        y = len(lines) - 1 - i
        on = [t for t in range(T + 1) if holds(t)]
        ax.broken_barh([(t - 0.5, 1) for t in on], (y - 0.3, 0.6), color=INK if name.startswith("timeline") else MUTED,
                       alpha=0.55, lw=0)
    ax.set_yticks(range(len(lines)))
    ax.set_yticklabels([n for n, _ in reversed(lines)], fontsize=7.5)
    ax.set_ylim(-0.6, max(len(lines), 1) - 0.4)
    if not lines:
        ax.text(0.01, 0.5, "context knowledge on: no context fact or recency fact held", transform=ax.transAxes,
                fontsize=8, color=MUTED, va="center")
    ax.set_ylabel("context", rotation=0, ha="right", va="center", color=INK)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


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


def main(d, log, extra=None, title=None):
    d = Path(d)
    THETA, alpha = header(log)
    exp, act = read(d / "expected.csv"), read(d / "actual.csv")
    traj = json.load(open(d / "trajectory.json"))
    ctx = context(log)
    every = sorted({r["key"] for r in (exp or act) if r["key"]})
    groups = [every[i:i + len(SERIES)] for i in range(0, len(every), len(SERIES))] or [[]]
    for n, keys in enumerate(groups):
        name = "figure.png" if n == 0 else f"figure_{n + 1}.png"
        part = "" if len(groups) == 1 else f" (hypotheses {n * len(SERIES) + 1} to {n * len(SERIES) + len(keys)} of {len(every)})"
        figure(d, exp, act, traj, THETA, alpha, keys, name, part, ctx, extra, title)


def figure(d, exp, act, traj, THETA, alpha, keys, name, part, ctx=None, extra=None, title=None):
    color = dict(zip(keys, SERIES))
    T = max(int(r["tick"]) for r in (exp or act))
    # the panels: the belief; the context (context knowledge on, T-F part 1); S; the finding; warrant and the gate; a
    # caller's last panel (the decisions)
    n_ctx = 0 if ctx is None else \
        max(len({f for fs, _ in ctx[0].values() for f in fs} | {r for _, rs in ctx[0].values() for r in rs}), 1)
    ratios = [3] + ([0.35 * n_ctx + 0.2] if ctx else []) + [3, 0.45, 1.3] + ([1.4] if extra else [])
    axes = plt.subplots(len(ratios), 1, figsize=(12, 8.6 + 0.3 * n_ctx + (1.9 if extra else 0)), sharex=True,
                        gridspec_kw=dict(height_ratios=ratios, hspace=0.08))[1]
    ax1, rest = axes[0], list(axes[1:])
    if ctx is not None:
        context_panel(rest.pop(0), ctx, T)
    ax2, ax3, ax4 = rest[:3]
    if extra is not None:
        extra(rest[3])
    for ax, col, ylabel in ((ax1, "belief_h", "belief over H"), (ax2, "S", "tail probability S")):
        e, a = series(exp, col), series(act, col)
        for k in keys:
            ts = range(T + 1)
            if exp:
                ys = [e.get(k, {}).get(t) for t in ts]
                ax.plot(list(ts), [float("nan") if y is None else y for y in ys], color=color[k], lw=2, label=short(k))
                at = [t for t in sorted(a.get(k, {})) if t % 5 == 0 and a[k][t] is not None]
                ax.plot(at, [a[k][t] for t in at], "o", ms=3.5, color=color[k], mec="white", mew=0.6)
            else:             # no expected table: the actual values alone, as lines
                ys = [a.get(k, {}).get(t) for t in ts]
                ax.plot(list(ts), [float("nan") if y is None else y for y in ys], color=color[k], lw=2, label=short(k))
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
               title="lines expected, dots actual" if exp else "actual (no oracle table)", title_fontsize=8)
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
    axes[-1].set_xlabel("tick")
    ax4.set_xlim(-1, T + 1)
    # the script's action boundaries; the task starts labelled
    last_task = None
    for b in traj["actions"]:
        for ax in (ax1, ax2):
            ax.axvline(b["tick"], color="#d9d8d2", lw=0.6, zorder=0)
        if b["task"] != last_task:
            ax1.text(b["tick"] + 1, 1.05, short(b["task"]), fontsize=7.5, color=INK, va="bottom", rotation=0)
            last_task = b["task"]
    if title is None:
        text = (f"{traj['scenario']} on {traj['layout']}, {'prior on' if exp else 'no oracle table'}{part}"
                + ("" if ctx is None else ", context knowledge on"))
    else:
        text = f"{traj['scenario']} on {traj['layout']}{part}{'' if exp else ', no oracle table'}\n{title}"
    fig = axes[0].figure
    fig.suptitle(text, x=0.06, ha="left", fontsize=11, color=INK)
    fig.savefig(d / name, dpi=130, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
