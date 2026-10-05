#!/usr/bin/env python3
"""
plot.py — the per-tick figure of a run, one file (figure.png), every panel on one shared tick axis; the IRB's figure and
the builder the planning test-bed's figure calls (analysis/instruments/mpb/plot.py).

History: IRB.3b drew the belief per hypothesis (since T-K part 1's gate stage the belief over H, `belief_h`, the value
the gate compares with θ; AM42) and S per hypothesis (expected as lines, actual as markers every fifth tick), the
finding and the lifecycle as a band, the script's action boundaries (trajectory.json) as thin vertical lines with the
task starts labelled; G-build the observation-warrant panel and the gate's clearing; T-F part 1 (the standing rule on
figures, Hadi, 5 October 2026) the context panel under the belief, and the decision panel a caller adds.

Since the measurement of T-F part 1 (N, Hadi, 5 October 2026; design_records.md, "T-F part 1", THE MEASUREMENT): one
figure file per run, the panels from the top, each where the run has it:
- the belief over H per hypothesis; with more than four hypotheses one belief panel per four (the palette's four
  validated slots, every hypothesis keeping its slot within its panel), all in the same file;
- the context panel (context knowledge on: the run log's `[IR-context]` lines), directly under the belief (the earlier
  ruling's place: the facts it shows are what changes the prior);
- the tail probability S per hypothesis, one panel per four as the belief;
- the adequacy finding (the lifecycle when exhausted) as a band;
- the observation warrant per hypothesis, then the gate's answer per tick, one row per answer the run holds (clears or
  the refusal's reason: `none(below_theta)`, `none(leader_inadequate)`, ..., `none(intention_off)`): expected (the
  oracle's table) as a light bar, actual as a mark;
- the decision panel (a caller's: the planning test-bed's decisions, projections, robot tasks and holds);
- the robot–human distance: per tick the continuous minimum the `[sep]` line logs (the value the separation measure
  reads), on a scale of 0 to 4 × min_separation so the ticks near it are readable (larger values drawn at the top
  edge), min_separation dashed, and every tick below it shaded by F1's class (analysis/instruments/common/
  separation.py: a moving robot violating or receding, a standing robot with the human passing or beside it); the
  closest approach written.
A run in which the recognizer does not run (human-unaware, intention-unaware) has no recognition panel; its gate row is
drawn where the caller gives one (intention-unaware: `none(intention_off)` on every tick).
θ and α and min_separation are read from the run's [run] header; a hypothesis or task is labelled by its key without
the parameter names. No id, coordinate or tick is written here (IRB.4b).

    plot.py <scenario dir> <run.log>        the IRB: expected.csv, actual.csv, trajectory.json in the dir
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

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
import logparse
import separation

# categorical slots 1 to 4, fixed order by key; the four pass every check over all pairs (the dataviz validator, light;
# violet as slot 4, since the sort). More than four hypotheses: one panel per four, every hypothesis keeping its slot
# within its panel; a fifth slot fails the normal-vision floor.
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7"]
BAND = {"unresolved": "#cfcdc6", "adequate": "#eeede9", "unexplained": "#e34948", "exhausted": "#8a8880"}
INK, MUTED = "#0b0b0b", "#8a8880"
# F1's classes of a tick below min_separation (separation.counts)
SEP_CLASS = [("viol", "a moving robot, violating", "#e34948"), ("recede", "a moving robot, receding", "#eb6834"),
             ("passing", "a standing robot, the human passing", "#8a8880"),
             ("beside", "a standing robot, the human beside it", "#cfcdc6")]
SCALE = 4             # the distance panel's top, in multiples of min_separation


def header(log):
    """θ, α and min_separation from the run's [run] header."""
    for l in open(log):
        if l.startswith("[run] "):
            h = dict(re.findall(r"(\w+)=(\S+)", l))
            return float(h["theta"]), float(h["test_level"]), float(h.get("min_separation", 50.0))
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


def context_lines(ctx):
    rows, timeline = ctx
    facts = sorted({f for fs, _ in rows.values() for f in fs})
    recent = sorted({r for _, rs in rows.values() for r in rs})
    label = lambda f: ("timeline " if f.split("(")[0] in timeline else "state ") + f.replace("()", "")
    return [(label(f), lambda t, f=f: f in rows.get(t, ((), ()))[0]) for f in facts] + \
           [("recent " + r, lambda t, r=r: r in rows.get(t, ((), ()))[1]) for r in recent]


def context_panel(ax, ctx, T):
    lines = context_lines(ctx)
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


def settings_text(log) -> str:
    """The run's settings, the strategy first, as its [run] header printed them (effective values)."""
    h = dict(re.findall(r"(\w+)=(\S+)", next(l for l in open(log) if l.startswith("[run] "))))
    keys = ("human_aware", "intention_aware", "assignment_knowledge", "context_knowledge")
    return f"strategy {h['strategy']}; " + ", ".join(f"{k} {h[k]}" for k in keys if k in h)


def gate_of(rows):
    """The gate's answer per tick from a table of rows (one per tick and key)."""
    return {int(r["tick"]): r["gate"] for r in rows if r.get("gate")}


def short(k):
    """A key without its parameter names: deliver_item(?item=x) -> deliver_item(x)."""
    return re.sub(r"\?\w+=", "", k)


def spines(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def distance_panel(ax, log, T, sep):
    """The robot–human distance per tick (the [sep] line's continuous minimum, else its sampled distance) on 0 to
    SCALE × min_separation; the ticks below min_separation shaded by F1's class; the closest approach written."""
    run = logparse.parse(log)
    ks = [k for k in sorted(run["sep"]) if k <= T]
    top = SCALE * sep
    ys = [run["sep"][k][1] if run["sep"][k][1] is not None else run["sep"][k][0] for k in ks]
    _, by, passing, beside, _, _, cont = separation.counts(log)
    ticks = dict(viol=by["viol"], recede=by["recede"], passing=passing, beside=beside)
    for name, _, colour in SEP_CLASS:
        for k in ticks[name]:
            if k <= T:
                ax.axvspan(k - 0.5, k + 0.5, color=colour, alpha=0.55, lw=0)
    ax.plot(ks, [min(y, top) for y in ys], color=INK, lw=1.0)
    ax.axhline(sep, color="#e34948", lw=0.8, ls="--")
    ax.text(T, sep, f"min_separation {sep:g} cm", ha="right", va="bottom", fontsize=7.5, color="#e34948")
    below = sum(1 for name, _, _ in SEP_CLASS for k in ticks[name] if k <= T)
    closest = min(((y, k) for y, k in zip(ys, ks)), default=None)
    note = ("" if closest is None else f"closest {closest[0]:.1f} cm at tick {closest[1]}") + \
           f"; ticks below min_separation: {below}; above {top:g} cm drawn at the top edge"
    ax.text(0.0, 1.02, note, transform=ax.transAxes, fontsize=7.5, color=INK, ha="left", va="bottom")
    ax.set_ylim(0, top * 1.04)
    ax.set_ylabel("robot–human\ndistance (cm)", color=INK)
    ax.grid(axis="y", color="#e6e5e0", lw=0.6)
    present = [Patch(color=c, alpha=0.55, label=lab) for name, lab, c in SEP_CLASS if any(k <= T for k in ticks[name])]
    if present:
        ax.legend(handles=present, loc="upper left", bbox_to_anchor=(1.0, 1.0), frameon=False, fontsize=7.5,
                  title="below min_separation", title_fontsize=7.5)
    spines(ax)


def draw(path, *, log, T, title, recog=None, traj=None, gate=None, decisions=None, key=None):
    """The one figure of a run, written to `path`.

    recog: the recognition tables, dict(exp=rows, act=rows) (rows of the IRB's columns: tick, key, belief_h, S,
        finding, lifecycle, gate, warrant; `exp` empty with no oracle table), or None where the recognizer does not
        run;
    traj: trajectory.json (the script's action boundaries), or None;
    gate: where `recog` is None, the gate's answer per tick, dict(exp={tick: answer}, act={tick: answer}), or None
        (no gate asked: human-unaware);
    decisions: a callable drawing the decision panel on the axis it is given, or None (an idle robot);
    key: a line written under the figure (the decision panel's key), or None."""
    THETA, alpha, sep = header(log)
    ctx = context(log)
    exp, act = (recog["exp"], recog["act"]) if recog else ([], [])
    every = sorted({r["key"] for r in (exp or act) if r["key"]}) if recog else []
    groups = [every[i:i + len(SERIES)] for i in range(0, len(every), len(SERIES))] if recog else []
    if recog and not groups:
        groups = [[]]
    if recog:
        gate = dict(exp=gate_of(exp), act=gate_of(act))
    answers = [] if gate is None else sorted(set(gate["exp"].values()) | set(gate["act"].values()),
                                             key=lambda g: (g != "clears", g))
    n_ctx = 0 if ctx is None else max(len(context_lines(ctx)), 1)
    panels = [("belief", g) for g in groups] + ([("context", None)] if ctx and recog else []) + \
             [("S", g) for g in groups] + ([("finding", None)] if recog else []) + \
             ([("rows", None)] if (every or answers) else []) + ([("decisions", None)] if decisions else []) + \
             [("distance", None)]
    tall = 2.6 if len(groups) <= 1 else 2.0
    size = dict(belief=tall, context=0.3 * n_ctx + 0.25, S=tall, finding=0.4,
                rows=0.26 * (len(every) + len(answers)) + 0.3, decisions=1.4, distance=1.7)
    ratios = [size[k] for k, _ in panels]
    fig, axes = plt.subplots(len(panels), 1, figsize=(12, 0.95 * sum(ratios) + 1.2), sharex=True, squeeze=False,
                             gridspec_kw=dict(height_ratios=ratios, hspace=0.12))
    axes = list(axes[:, 0])
    ax_of = {}
    for (kind, g), ax in zip(panels, axes):
        ax_of.setdefault(kind, []).append((g, ax))
    # the belief and S, one panel per four hypotheses
    for kind, col, ylabel, line, mark in (("belief", "belief_h", "belief over H", THETA, "θ"),
                                          ("S", "S", "tail probability S", alpha, "α")):
        e, a = series(exp, col), series(act, col)
        for keys, ax in ax_of.get(kind, []):
            color = dict(zip(keys, SERIES))
            ts = range(T + 1)
            for k in keys:
                if exp:
                    ys = [e.get(k, {}).get(t) for t in ts]
                    ax.plot(list(ts), [float("nan") if y is None else y for y in ys], color=color[k], lw=2,
                            label=short(k))
                    at = [t for t in sorted(a.get(k, {})) if t % 5 == 0 and a[k][t] is not None and t <= T]
                    ax.plot(at, [a[k][t] for t in at], "o", ms=3.5, color=color[k], mec="white", mew=0.6)
                else:             # no expected table: the actual values alone, as lines
                    ys = [a.get(k, {}).get(t) for t in ts]
                    ax.plot(list(ts), [float("nan") if y is None else y for y in ys], color=color[k], lw=2,
                            label=short(k))
            ax.set_ylabel(ylabel, color=INK)
            ax.set_ylim(-0.03, 1.05)
            ax.grid(axis="y", color="#e6e5e0", lw=0.6)
            spines(ax)
            ax.axhline(line, color=MUTED, lw=0.8, ls="--")
            ax.text(T, line + 0.015, f"{mark} = {line:g}", ha="right", va="bottom", fontsize=8, color=MUTED)
            if kind == "belief":
                ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), frameon=False, fontsize=9,
                          title="lines expected, dots actual" if exp else "actual (no oracle table)",
                          title_fontsize=8)
    if ctx and recog:
        context_panel(ax_of["context"][0][1], ctx, T)
    if recog:
        ax3 = ax_of["finding"][0][1]
        state = {}
        for r in act:
            state[int(r["tick"])] = r["finding"] if r["lifecycle"] == "live" else "exhausted"
        for t, s in state.items():
            if t <= T:
                ax3.axvspan(t - 0.5, t + 0.5, color=BAND[s], lw=0)
        ax3.set_yticks([])
        ax3.set_ylabel("finding", rotation=0, ha="right", va="center", color=INK)
        ax3.legend(handles=[Patch(color=BAND[s], label=s) for s in BAND], loc="upper left", bbox_to_anchor=(1.0, 1.6),
                   frameon=False, fontsize=8)
    # warrant per hypothesis, then the gate's answer per tick, one row per answer: expected bars, actual marks
    if "rows" in ax_of:
        ax4 = ax_of["rows"][0][1]
        slot = {k: SERIES[i % len(SERIES)] for i, k in enumerate(every)}
        rows4 = [("warrant", k) for k in every] + [("gate", g) for g in answers]
        for i, (kind, k) in enumerate(rows4):
            y = len(rows4) - 1 - i
            if kind == "gate":
                c = INK if k == "clears" else MUTED
                e_on = [t for t, g in gate["exp"].items() if g == k and t <= T]
                a_on = [t for t, g in gate["act"].items() if g == k and t <= T]
            else:
                c = slot[k]
                e_on = [int(r["tick"]) for r in exp if r["key"] == k and r["warrant"] == "observation"]
                a_on = [int(r["tick"]) for r in act if r["key"] == k and r["warrant"] == "observation"
                        and int(r["tick"]) <= T]
            ax4.broken_barh([(t - 0.5, 1) for t in e_on], (y - 0.3, 0.6), color=c, alpha=0.35, lw=0)
            ax4.plot(a_on, [y] * len(a_on), "|", ms=5, color=c)
        ax4.set_yticks(range(len(rows4)))
        ax4.set_yticklabels([("warrant " + short(k)) if kind == "warrant" else f"gate {k}"
                             for kind, k in reversed(rows4)], fontsize=7.5)
        ax4.set_ylim(-0.6, len(rows4) - 0.4)
        spines(ax4)
    if decisions:
        decisions(ax_of["decisions"][0][1])
    distance_panel(ax_of["distance"][0][1], log, T, sep)
    axes[-1].set_xlabel("tick")
    axes[-1].set_xlim(-1, T + 1)
    # the script's action boundaries; the human's task starts labelled above the top panel
    if traj is not None:
        last_task = None
        lined = [ax for k in ("belief", "S") for _, ax in ax_of.get(k, [])] + [ax_of["distance"][0][1]]
        for b in traj["actions"]:
            if b["tick"] > T:
                continue
            for ax in lined:
                ax.axvline(b["tick"], color="#d9d8d2", lw=0.6, zorder=0)
            if b["task"] != last_task:
                axes[0].text(b["tick"] + 1, 1.0, short(b["task"]), fontsize=7.5, color=INK, va="bottom",
                             transform=axes[0].get_xaxis_transform())
                last_task = b["task"]
    # the title above the top panel, clear of the human's task labels
    axes[0].annotate(title, xy=(0, 1), xycoords="axes fraction", xytext=(-40, 16), textcoords="offset points",
                     ha="left", va="bottom", fontsize=11, color=INK)
    if key:
        axes[-1].annotate(key, xy=(0, 0), xycoords="axes fraction", xytext=(-40, -34), textcoords="offset points",
                          ha="left", va="top", fontsize=7, color=MUTED)
    fig.savefig(path, dpi=110, bbox_inches="tight")
    plt.close(fig)


def main(d, log):
    """The IRB's figure: the oracle's table (expected.csv) and the actual (actual.csv) of the scenario dir."""
    d = Path(d)
    exp, act = read(d / "expected.csv"), read(d / "actual.csv")
    traj = json.load(open(d / "trajectory.json"))
    T = max(int(r["tick"]) for r in (exp or act))
    title = f"{traj['scenario']} on {traj['layout']}{'' if exp else ', no oracle table'}\n{settings_text(log)}"
    draw(d / "figure.png", log=log, T=T, title=title, recog=dict(exp=exp, act=act), traj=traj)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
