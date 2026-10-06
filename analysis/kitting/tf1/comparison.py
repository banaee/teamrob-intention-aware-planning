#!/usr/bin/env python3
"""
comparison.py — the comparative statistics report of the measurement of T-F part 1, written for a reader outside the
repository (Hadi, 5 October 2026). Every number and table of the report comes from here; none is typed by hand.

    comparison.py            reads analysis/kitting/tf1/measurement/results.csv (the measurement's result table,
                             analysis/instruments/mpb/table.py), writes analysis/kitting/tf1/COMPARISON.md, the
                             self-contained analysis/kitting/tf1/comparison.html (the same text, the figures embedded) and
                             the figures in analysis/kitting/tf1/comparison/ (png, git-ignored); prints the cross-check
                             against the design chat's figures.

The data: the 128 scenarios run in all four conditions (run_001 to run_512); the 176 copies with a timeline, run in one
condition only, are left out (no comparison is possible on them). A scenario's measures are its run's row. A paired
change is the second condition's value minus the first's, per scenario: negative is earlier or fewer.
Statistics: descriptive and paired per scenario; the Wilcoxon signed-rank test over scenarios as an indication only
(it assumes independent scenarios, which they are not); beside it, the room as the unit (the scenarios of one room share
its layout and often its scripts): the mean change per room, and a 95% interval for the mean change per scenario from a
bootstrap that resamples rooms (10,000 resamples, seed 0).
"""
import base64
import csv
import json
import math
import re
import random
import statistics as st
import sys
from pathlib import Path

import markdown
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "measurement" / "results.csv"
FIG = HERE / "comparison"
CONDS = ["HU", "IU", "OFF", "ON"]
LONG = {"HU": "human-unaware", "IU": "intention-unaware", "OFF": "intention-aware, context knowledge off",
        "ON": "intention-aware, context knowledge on"}
STEPS = [("HU", "IU", "Step 1: planning against the observed human",
          "human-unaware → intention-unaware"),
         ("IU", "OFF", "Step 2: recognition of the human's task",
          "intention-unaware → intention-aware, context knowledge off"),
         ("OFF", "ON", "Step 3a: context knowledge with no timeline fact in force",
          "context knowledge off → on, the starting likelihoods alone")]
SETS = [("A", 1, 64, "the planning test-bed"), ("B", 65, 88, "the context-knowledge planning cases"),
        ("C", 89, 512, "the context-knowledge scenarios on six rooms")]
INK, MUTED, BAR = "#0b0b0b", "#8a8880", "#2a78d6"


def cond(r):
    on = lambda v: v in ("True", "on")
    if not on(r["human_aware"]):
        return "HU"
    if not on(r["intention_aware"]):
        return "IU"
    return "ON" if on(r["context_knowledge"]) else "OFF"


def load():
    rows = [r for r in csv.DictReader(open(RESULTS)) if int(r["run"][4:]) <= 512]
    by = {}
    for r in rows:
        n = int(r["run"][4:])
        r["set"] = next(s for s, lo, hi, _ in SETS if lo <= n <= hi)
        r["done"] = r["completion"] != "unfinished"
        for k in ("hold_ticks", "near_encounters", "viol", "recede", "stand_passing", "stand_beside", "decisions"):
            r[k] = int(r[k])
        r["completion"] = int(r["completion"]) if r["done"] else None
        r["sep_min"] = float(r["sep_min"])
        r["dir"] = HERE / "measurement" / r["scenario"] / r["run"]
        by.setdefault(r["scenario"], {})[cond(r)] = r
    assert all(len(v) == 4 for v in by.values()) and len(by) == 128, "128 scenarios in four conditions"
    return by


def f1(x):
    return "–" if x is None else f"{x:+.1f}" if isinstance(x, float) else f"{x:+d}"


def mean(xs):
    return st.mean(xs) if xs else None


def median(xs):
    return st.median(xs) if xs else None


def boot_rooms(pairs, seed=0, n=10000):
    """95% interval of the mean change per scenario, resampling rooms with replacement (each drawn room with all its
    scenarios)."""
    rooms = {}
    for room, d in pairs:
        rooms.setdefault(room, []).append(d)
    keys = sorted(rooms)
    rnd = random.Random(seed)
    means = []
    for _ in range(n):
        draw = [x for _ in keys for x in rooms[rnd.choice(keys)]]
        means.append(sum(draw) / len(draw))
    means.sort()
    return means[int(0.025 * n)], means[int(0.975 * n) - 1]


def wil(ds):
    nz = [d for d in ds if d != 0]
    if len(nz) < 6:
        return None
    return wilcoxon(nz).pvalue


def paired(by, a, b, key, scen):
    """Per scenario the change b - a of `key`, over the scenarios in `scen` where both values exist."""
    out = []
    for s in scen:
        x, y = by[s][a][key], by[s][b][key]
        if x is not None and y is not None:
            out.append((by[s][a]["layout"], s, y - x))
    return out


def summary(pairs):
    ds = [d for _, _, d in pairs]
    ch = [d for d in ds if d != 0]
    lo_hi = boot_rooms([(room, d) for room, _, d in pairs]) if pairs else (None, None)
    rooms = {}
    for room, _, d in pairs:
        rooms.setdefault(room, []).append(d)
    rm = [mean(v) for v in rooms.values()]
    return dict(n=len(ds), lower=sum(d < 0 for d in ds), equal=sum(d == 0 for d in ds), higher=sum(d > 0 for d in ds),
                mean=mean(ds), median=median(ds), changed=len(ch), ch_median=median(ch),
                ch_min=min(ch) if ch else None, ch_max=max(ch) if ch else None, total=sum(ds), p=wil(ds),
                ci=lo_hi, rooms=len(rooms), rooms_lower=sum(m < 0 for m in rm), rooms_equal=sum(m == 0 for m in rm),
                rooms_higher=sum(m > 0 for m in rm))


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def num(x, d=1):
    """A number with d decimals (d = 0: an integer count)."""
    if x is None:
        return "–"
    return str(x) if d == 0 else f"{float(x):.{d}f}"


def signed(x, d=1):
    return "–" if x is None else f"{float(x):+.{d}f}"


def pval(p):
    return "–" if p is None else ("< 0.001" if p < 0.001 else f"{p:.3f}")


def step_rows(by, scen, finished):
    """The rows of a step table: per step, completion, violation ticks and ticks below min_separation."""
    rows = []
    for a, b, title, _ in STEPS:
        for key, label, sc in (("completion", "completion (ticks)", finished), ("viol", "violation ticks", scen),
                               ("near_encounters", "ticks below min_separation", scen)):
            s = summary(paired(by, a, b, key, sc))
            word = ("earlier", "equal", "later") if key == "completion" else ("fewer", "equal", "more")
            rows.append([title.split(":")[0], label, s["n"],
                         f"{s['lower']} {word[0]} / {s['equal']} {word[1]} / {s['higher']} {word[2]}",
                         signed(s["mean"], 2), signed(s["median"]),
                         "–" if not s["changed"] else f"{s['changed']}: median {signed(s['ch_median'])}, "
                                                      f"{f1(s['ch_min'])} to {f1(s['ch_max'])}",
                         "–" if s["ci"][0] is None else f"{s['ci'][0]:+.2f} to {s['ci'][1]:+.2f}",
                         f"{s['rooms_lower']} / {s['rooms_equal']} / {s['rooms_higher']}", pval(s["p"])])
    return rows


STEP_HEAD = ["step", "measure", "scenarios", "per scenario: lower / equal / higher", "mean change", "median change",
             "scenarios that change: how many, median and range of the change",
             "95% interval of the mean (rooms resampled)", "rooms with mean change < 0 / = 0 / > 0",
             "Wilcoxon p (indication only)"]


def figure(by, finished, scen, inter):
    from collections import Counter
    from matplotlib.ticker import MaxNLocator
    FIG.mkdir(exist_ok=True)
    for key, scset, label, name, width in (("completion", finished, "change in completion (ticks; negative is earlier)",
                                            "completion", 5),
                                           ("viol", scen, "change in violation ticks (negative is fewer)",
                                            "violations", 1)):
        fig, axes = plt.subplots(1, 3, figsize=(12, 3.6))
        lim = max(abs(d) for a, b, *_ in STEPS for _, _, d in paired(by, a, b, key, scset))
        top = width * math.ceil((lim + 1) / width)
        for ax, (a, b, title, sub) in zip(axes, STEPS):
            ds = [d for _, _, d in paired(by, a, b, key, scset)]
            ch = [d for d in ds if d != 0]
            if width == 1:             # one bar per integer value
                cnt = Counter(ch)
                ax.bar(list(cnt), list(cnt.values()), width=0.8, color=BAR)
            else:                      # bins of `width` ticks, edges at k * width + 0.5 (no bin spans zero)
                edges = [k * width + 0.5 for k in range(-int(top / width) - 1, int(top / width) + 1)]
                ax.hist(ch, bins=edges, color=BAR, edgecolor="white", linewidth=0.6)
            ax.set_xlim(-top, top)
            ax.axvline(0, color=MUTED, lw=0.8, ls="--")
            ax.set_title(f"{title.split(':')[0]}\n{sub}", fontsize=8.5, color=INK, loc="left")
            ax.text(0.98, 0.95, f"{len(ds)} scenarios\n{len(ds) - len(ch)} with no change (not drawn)\n"
                                f"{sum(d < 0 for d in ds)} lower, {sum(d > 0 for d in ds)} higher",
                    transform=ax.transAxes, ha="right", va="top", fontsize=7.5, color=INK)
            ax.set_xlabel(label, fontsize=8)
            ax.set_ylabel("scenarios", fontsize=8)
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            ax.tick_params(labelsize=7.5)
            for sp in ("top", "right"):
                ax.spines[sp].set_visible(False)
        fig.tight_layout()
        fig.savefig(FIG / f"{name}.png", dpi=130)
        plt.close(fig)
    # the trade of step 1, per interacting scenario; identical points drawn once, sized and labelled by their count
    pts = Counter((by[s]["HU"]["viol"] - by[s]["IU"]["viol"], by[s]["IU"]["completion"] - by[s]["HU"]["completion"])
                  for s in inter if s in finished)
    fig, ax = plt.subplots(figsize=(7, 4.4))
    for (x, y), n in pts.items():
        ax.scatter([x], [y], s=18 + 14 * n, color=BAR, edgecolor="white", linewidth=0.6, alpha=0.85)
        if n > 1:
            ax.annotate(f"{n}", (x, y), xytext=(6, 4), textcoords="offset points", fontsize=7.5, color=INK)
    ax.axhline(0, color=MUTED, lw=0.8, ls="--")
    ax.axvline(0, color=MUTED, lw=0.8, ls="--")
    ax.set_xlabel("violation ticks removed by step 1 (per scenario)", fontsize=8.5)
    ax.set_ylabel("completion delay added by step 1 (ticks)", fontsize=8.5)
    ax.set_title(f"Step 1, per scenario: delay against violation ticks removed\n{sum(pts.values())} scenarios in which "
                 "the human and the robot interact; a number beside a point counts the scenarios on it",
                 fontsize=8.5, loc="left", color=INK)
    ax.tick_params(labelsize=7.5)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "trade.png", dpi=130)
    plt.close(fig)


# ---- part 1: context knowledge with a fact in force (the last step of T-F part 1)
sys.path.insert(0, str(HERE))
import make_copies                                     # the copies, their base and class (the rule: REPORT.md, "Part 1")

MODELLED = re.compile(r"^(deliver_item|coffee_break|ac_activation)\(")


def _bind(key):
    name, args = key.split("(", 1)
    return name, dict(a.split("=", 1) for a in args.rstrip(")").split(",") if "=" in a)


def _hyp(task, keys):
    """The hypothesis key of a task the human performs, or None (a task with no hypothesis)."""
    if not MODELLED.match(task):
        return None
    name, b = _bind(task)
    for k in keys:
        kn, kb = _bind(k)
        if kn == name and all(b.get(x) == v for x, v in kb.items()):
            return k
    return None


def recognition(d):
    """The two recognition measures of a run (REPORT.md, "Part 1", 1c): per stretch of a modelled task the human
    performs, the ticks from its first tick to the first tick the decision record holds its hypothesis (None: not
    admitted within the stretch); the ticks on which the decision record holds a hypothesis other than the human's
    task. Over the ticks before the robot's terminal decision (the whole run when it has none)."""
    obs = json.load(open(d / "observed.json"))
    end = obs["terminal"] if obs["terminal"] is not None else obs["steps"]
    ticks = {t["tick"]: t for t in json.load(open(d / "actual_ticks.json")) if t["tick"] < end}
    keys = sorted({k for t in ticks.values() for k in (t.get("belief_h") or t["belief"])})
    st = make_copies.stretches(json.load(open(d / "trajectory.json")))
    lat, wrong = [], 0
    for task, a, b in st:
        h = _hyp(task, keys)
        if h is None or a >= end:
            continue
        hit = next((t for t in range(a, min(b, end)) if ticks.get(t, {}).get("record") == h), None)
        lat.append((task, a, None if hit is None else hit - a))
    for t, row in ticks.items():
        cur = next((task for task, a, b in st if a <= t < b), None)
        h = None if cur is None else _hyp(cur, keys)
        if row.get("record") is not None and row["record"] != h:
            wrong += 1
    return lat, wrong


def windows(d):
    """The timeline windows of a run, from its log's `[run_mesa] timeline` line: [(fact, first tick, end)]."""
    log = d / f"{d.name}.log"
    line = next(l for l in open(log) if l.startswith("[run_mesa] timeline"))
    return [(f, int(a), 10 ** 9 if b == "end" else int(b))          # "end": the window runs to the run's end
            for f, a, b in re.findall(r"(\w+) (\d+)\.\.(\d+|end)", line.split("windows=")[1])]


def part1(rows, by):
    """The section's lines: the copies by class against the base's run with context knowledge off."""
    run_of = {}
    for r in rows:
        run_of.setdefault(r["scenario"], {})[cond(r)] = r
    cls = make_copies.classes()
    pairs = {}
    for copy, c in sorted(cls.items()):
        if copy not in run_of or c["base"] not in by:
            continue
        on = run_of[copy]["ON"]
        pairs.setdefault(c["cls"], []).append((c["base"], copy, by[c["base"]]["OFF"], by[c["base"]]["ON"], on))
    out = []
    w = out.append
    w("## Step 3b: context knowledge with a timeline fact in force")
    w("")
    w("Step 3a compares context knowledge off and on in scenarios where, with three exceptions, no context fact "
      "is in force: it measures the starting likelihoods alone. Step 3b takes each *copy* of a scenario with a context fact in "
      "force over chosen ticks (a timeline: for example *break time* over some ticks) is run with context knowledge "
      "on, and compared with its base scenario run with context knowledge off. The human's script is the same in both; "
      "only the fact and the knowledge differ. The copies fall into two classes, by a rule fixed before the runs:")
    w("")
    w("- **in accord**: the fact holds over the ticks in which the human does the task the fact makes more likely "
      "(break time during the coffee break; room warm during the visit to the air-conditioning switch);")
    w("- **not in accord**: the fact holds while the human does another task, or the human never does that task.")
    w("")
    w("A set with facts only in accord would show a benefit by construction; the second class shows the cost of a fact "
      "that misleads. Three copies whose fact holds over the whole run are listed apart. Two recognition measures are "
      "added, because context knowledge acts on recognition first: the **admission delay** (for each task the human "
      "performs that the robot can recognise, the ticks from the task's start until the robot plans around that task; "
      "or never within the task) and the **wrong-admission ticks** (ticks on which the robot plans around a task the "
      "human is not doing). Both are counted over the ticks before the robot's work ends.")
    w("")
    names = [("in accord", "in accord"), ("not in accord", "not in accord"), ("whole run", "fact over the whole run")]
    data = {}
    for k, label in names:
        ps = pairs.get(k, [])
        rec = [(recognition(off["dir"]), recognition(on["dir"]), recognition(nof["dir"])) for _, _, off, nof, on in ps]
        data[k] = (ps, rec)
    head = ["measure"] + [f"{label} ({len(data[k][0])} copies, {len({p[0] for p in data[k][0]})} base scenarios)"
                          for k, label in names]
    rows_ = []
    rows_.append(["completion: earlier / equal / later than context knowledge off (scenarios finished in both)"] + [
        (lambda ds: f"{sum(x < 0 for x in ds)} / {sum(x == 0 for x in ds)} / {sum(x > 0 for x in ds)} ({len(ds)})")(
            [on["completion"] - off["completion"] for _, _, off, _, on in data[k][0]
             if off["completion"] is not None and on["completion"] is not None]) for k, _ in names])
    for key, label in (("completion", "completion, mean change (ticks)"), ("hold_ticks", "held ticks, mean change"),
                       ("viol", "violation ticks, mean change"),
                       ("near_encounters", "ticks below min_separation, mean change")):
        rows_.append([label] + [signed(mean([on[key] - off[key] for _, _, off, _, on in data[k][0]
                                             if off[key] is not None and on[key] is not None]), 2) for k, _ in names])
    for key, label in (("viol", "violation ticks, total: off → on with the fact"),
                       ("near_encounters", "ticks below min_separation, total: off → on with the fact"),
                       ("hold_ticks", "held ticks, total: off → on with the fact")):
        rows_.append([label] + [f"{sum(off[key] for _, _, off, _, on in data[k][0])} → "
                                f"{sum(on[key] for _, _, off, _, on in data[k][0])}" for k, _ in names])
    rows_.append(["unfinished runs: off / on with the fact"] + [
        f"{sum(off['completion'] is None for _, _, off, _, on in data[k][0])} / "
        f"{sum(on['completion'] is None for _, _, off, _, on in data[k][0])}" for k, _ in names])

    def lat_rows(k):
        st = [(o, n) for (lo, _), (ln, _), _ in data[k][1] for o, n in zip(lo, ln)]
        both = [(o[2], n[2]) for o, n in st if o[2] is not None and n[2] is not None]
        ds = [n - o for o, n in both]
        return st, both, ds
    rows_.append(["recognisable task stretches the human performs"] + [len(lat_rows(k)[0]) for k, _ in names])
    rows_.append(["of them admitted: off / on with the fact"] + [
        f"{sum(o[2] is not None for o, _ in lat_rows(k)[0])} / {sum(n[2] is not None for _, n in lat_rows(k)[0])}"
        for k, _ in names])
    rows_.append(["admission delay, median (ticks; stretches admitted in both): off / on with the fact"] + [
        (lambda st, both, ds: "–" if not both else
         f"{num(median([o for o, _ in both]))} / {num(median([n for _, n in both]))} ({len(both)})")(*lat_rows(k))
        for k, _ in names])
    rows_.append(["admission delay per stretch: earlier / equal / later with the fact"] + [
        (lambda st, both, ds: f"{sum(x < 0 for x in ds)} / {sum(x == 0 for x in ds)} / {sum(x > 0 for x in ds)}")(
            *lat_rows(k)) for k, _ in names])
    def split(k, inside):
        out_ = []
        for (b, copy, off, nof, on), ((lo, _), (ln, _), _) in zip(data[k][0], data[k][1]):
            ws = windows(on["dir"])
            for o, n in zip(lo, ln):
                if (any(a <= o[1] < e for _, a, e in ws)) == inside and o[2] is not None and n[2] is not None:
                    out_.append(n[2] - o[2])
        return out_
    for inside, label in ((True, "starting inside the fact's window"), (False, "starting outside it")):
        rows_.append([f"admission delay per stretch {label}: earlier / equal / later with the fact (stretches)"] + [
            (lambda ds: f"{sum(x < 0 for x in ds)} / {sum(x == 0 for x in ds)} / {sum(x > 0 for x in ds)} ({len(ds)})")(
                split(k, inside)) for k, _ in names])
    rows_.append(["wrong-admission ticks, total: off → on with the fact"] + [
        f"{sum(ro[1] for ro, rn, _ in data[k][1])} → {sum(rn[1] for ro, rn, _ in data[k][1])}" for k, _ in names])
    rows_.append(["wrong-admission ticks per copy: fewer / equal / more with the fact"] + [
        (lambda ds: f"{sum(x < 0 for x in ds)} / {sum(x == 0 for x in ds)} / {sum(x > 0 for x in ds)}")(
            [rn[1] - ro[1] for ro, rn, _ in data[k][1]]) for k, _ in names])
    w(table(head, rows_))
    w("")
    w("For reference, the same base scenarios with context knowledge on and **no** fact in force (the starting "
      "likelihoods alone), against context knowledge off:")
    w("")
    ref = []
    for k, label in names:
        ps, rec = data[k]
        seen, cs, vs, ws, ls = set(), [], [], [], []
        for (b, _, off, nof, on), (ro, rn, rnf) in zip(ps, rec):
            if b in seen:
                continue
            seen.add(b)
            if off["completion"] is not None and nof["completion"] is not None:
                cs.append(nof["completion"] - off["completion"])
            vs.append(nof["viol"] - off["viol"])
            ws.append(rnf[1] - ro[1])
            ls += [n[2] - o[2] for o, n in zip(ro[0], rnf[0]) if o[2] is not None and n[2] is not None]
        ref.append([f"{label}: its {len(seen)} base scenarios",
                    f"{sum(x < 0 for x in cs)} / {sum(x == 0 for x in cs)} / {sum(x > 0 for x in cs)}",
                    signed(mean(cs), 2), f"{sum(x < 0 for x in vs)} / {sum(x == 0 for x in vs)} / {sum(x > 0 for x in vs)}",
                    f"{sum(x < 0 for x in ws)} / {sum(x == 0 for x in ws)} / {sum(x > 0 for x in ws)}",
                    f"{sum(x < 0 for x in ls)} / {sum(x == 0 for x in ls)} / {sum(x > 0 for x in ls)} ({len(ls)})"])
    w(table(["base scenarios", "completion: earlier / equal / later", "completion: mean change",
             "violation ticks: fewer / equal / more", "wrong-admission ticks: fewer / equal / more",
             "admission delay per stretch: earlier / equal / later (stretches)"], ref))
    w("")
    # what the tables show, stated from the numbers
    for k, label in names[:2]:
        ps, rec = data[k]
        cs = [on["completion"] - off["completion"] for _, _, off, _, on in ps
              if off["completion"] is not None and on["completion"] is not None]
        wr = [rn[1] - ro[1] for ro, rn, _ in rec]
        st, both, ds = lat_rows(k)
        ins = split(k, True)
        w(f"- **{label}** ({len(ps)} copies): completion {sum(x < 0 for x in cs)} earlier, {sum(x > 0 for x in cs)} "
          f"later, {sum(x == 0 for x in cs)} equal, mean {signed(mean(cs), 2)} ticks; violation ticks "
          f"{sum(off['viol'] for _, _, off, _, on in ps)} → {sum(on['viol'] for _, _, off, _, on in ps)}; admission "
          f"delay earlier in {sum(x < 0 for x in ds)} task stretches and later in {sum(x > 0 for x in ds)} of "
          f"{len(both)}, of the {len(ins)} starting inside the fact's window earlier in {sum(x < 0 for x in ins)} and "
          f"later in {sum(x > 0 for x in ins)}; wrong-admission ticks {sum(ro[1] for ro, rn, _ in rec)} → "
          f"{sum(rn[1] for ro, rn, _ in rec)}.")
    w("")
    w("The admission delays compare a copy with context knowledge on against its base with it off, so they include "
      "what the starting likelihoods alone do (the reference table); the stretches starting inside the fact's window "
      "are those the fact acts on.")
    w("")
    summary_lines = []
    for k, label in names[:2]:
        ps, rec = data[k]
        ins = split(k, True)
        cs = [on["completion"] - off["completion"] for _, _, off, _, on in ps
              if off["completion"] is not None and on["completion"] is not None]
        summary_lines.append(
            f"{label} ({len(ps)} copies): of {len(ins)} task stretches starting while the fact holds, admitted earlier "
            f"in {sum(x < 0 for x in ins)} and later in {sum(x > 0 for x in ins)}; completion {sum(x < 0 for x in cs)} "
            f"earlier, {sum(x == 0 for x in cs)} equal, {sum(x > 0 for x in cs)} later; violation ticks "
            f"{sum(off['viol'] for _, _, off, _, on in ps)} → {sum(on['viol'] for _, _, off, _, on in ps)}")
    return out, summary_lines


def load_full_reorder():
    """The same 128 scenarios in the four conditions under full_reorder (run_721 to run_1232; Hadi, 6 October 2026;
    design_records.md, "T-F part 1", THE MEASUREMENT EXTENDED BY FULL_REORDER), keyed as `load` keys single_task."""
    by = {}
    for r in csv.DictReader(open(RESULTS)):
        if r["strategy"] != "full_reorder":
            continue
        r["done"] = r["completion"] != "unfinished"
        for k in ("hold_ticks", "near_encounters", "viol", "recede", "stand_passing", "stand_beside", "decisions"):
            r[k] = int(r[k])
        r["completion"] = int(r["completion"]) if r["done"] else None
        r["sep_min"] = float(r["sep_min"])
        r["dir"] = HERE / "measurement" / r["scenario"] / r["run"]
        by.setdefault(r["scenario"], {})[cond(r)] = r
    assert all(len(v) == 4 for v in by.values()) and len(by) == 128, "128 scenarios in four conditions"
    return by


def order(r):
    """The robot's executed order of tasks in a run: its task per tick (robot.json), consecutive repeats merged."""
    out = []
    for a in json.load(open(r["dir"] / "robot.json")):
        if a["task"] is not None and (not out or out[-1] != a["task"]):
            out.append(a["task"])
    return [re.sub(r"deliver_item\(\?item=(\w+)(,\?kitting_table=(\w+))?\)", r"\1", x) for x in out]


def full_reorder_sections(w, by, scen, finished):
    """The sections the measurement extended by full_reorder adds (Hadi, 6 October 2026); every number under
    single_task above is unchanged."""
    byf = load_full_reorder()
    finf = [s for s in scen if all(byf[s][c]["done"] for c in CONDS)]
    fin2 = [s for s in finished if s in finf]
    S = {"single_task": by, "full_reorder": byf}
    w("## The measurement under full_reorder")
    w("")
    w("Added on 6 October 2026 (Hadi; design_records.md, \"T-F part 1\", THE MEASUREMENT EXTENDED BY FULL_REORDER): the "
      "same 128 scenarios in the same four conditions under the strategy `full_reorder`, in which the robot orders its "
      "whole pool at each decision (run_721 to run_1232). Debugging, not T-F part 2's evaluation. Every comparison of "
      "conditions stays inside one strategy; every number above is the `single_task` measurement's, unchanged. "
      "`full_reorder` logs no per-candidate hold (TODO-141); no measure below needs one.")
    w("")
    w(f"### The four conditions under each strategy")
    w("")
    w(f"Completion over the {len(fin2)} scenarios finished in all eight runs; the other measures over all 128.")
    w("")
    head = ["measure"] + [f"{LONG[c]}, {st_}" for c in CONDS for st_ in S]
    rows = [["completion, mean (ticks)"] + [num(mean([S[st_][s][c]["completion"] for s in fin2])) for c in CONDS for st_ in S]]
    for key, label in (("viol", "violation ticks, total"), ("near_encounters", "ticks below min_separation, total"),
                       ("hold_ticks", "held ticks, total"), ("decisions", "decisions, total")):
        rows.append([label] + [sum(S[st_][s][c][key] for s in scen) for c in CONDS for st_ in S])
    rows.append(["runs that do not finish"] + [sum(not S[st_][s][c]["done"] for s in scen) for c in CONDS for st_ in S])
    w(table(head, rows))
    w("")
    w("### The three steps under full_reorder, paired per scenario")
    w("")
    w(f"Over the 128 scenarios under `full_reorder` ({len(finf)} finished in all four conditions, for completion); the "
      "same table under `single_task` is above. Negative is earlier or fewer.")
    w("")
    w(table(STEP_HEAD, step_rows(byf, scen, finf)))
    w("")
    w("### full_reorder against single_task, per condition")
    w("")
    w("Per scenario, the `full_reorder` run against the `single_task` run of the same condition; completion over the "
      "scenarios finished under both. Negative is earlier or fewer under `full_reorder`.")
    w("")
    rr = []
    for c in CONDS:
        fc = [s for s in scen if by[s][c]["done"] and byf[s][c]["done"]]
        for key, label, sc in (("completion", "completion (ticks)", fc), ("viol", "violation ticks", scen),
                               ("near_encounters", "ticks below min_separation", scen), ("hold_ticks", "held ticks", scen)):
            ds = [byf[s][c][key] - by[s][c][key] for s in sc]
            word = ("earlier", "equal", "later") if key == "completion" else ("fewer", "equal", "more")
            rr.append([LONG[c], label, len(ds), f"{sum(d < 0 for d in ds)} {word[0]} / {sum(d == 0 for d in ds)} "
                       f"{word[1]} / {sum(d > 0 for d in ds)} {word[2]}", signed(mean(ds), 2),
                       f"{sum(by[s][c][key] for s in sc)} → {sum(byf[s][c][key] for s in sc)}"])
    w(table(["condition", "measure", "scenarios", "per scenario: lower / equal / higher", "mean change",
             "total: single_task → full_reorder"], rr))
    w("")
    w("### Where recognition changes the robot's order of deliveries")
    w("")
    w("The robot's executed order of tasks (its task per tick, consecutive repeats merged; a task left and taken up "
      "again appears twice), compared between conditions of one strategy.")
    w("")
    cmp_rows, lists = [], {}
    for st_, b in S.items():
        for a, c in (("HU", "IU"), ("IU", "OFF"), ("OFF", "ON")):
            ch = [s for s in scen if order(b[s][a]) != order(b[s][c])]
            lists[(st_, a, c)] = ch
            cmp_rows.append([st_, f"{LONG[a]} → {LONG[c]}", len(scen), len(ch),
                             sum(order(b[s][a])[:1] != order(b[s][c])[:1] for s in scen)])
    w(table(["strategy", "conditions", "scenarios", "scenarios whose order differs", "of them the first task differs"],
            cmp_rows))
    w("")
    for st_, b in S.items():
        for a, c in (("IU", "OFF"), ("OFF", "ON")):
            ch = lists[(st_, a, c)]
            w(f"- {st_}, {LONG[a]} → {LONG[c]}: " + ("no scenario." if not ch else ""))
            for s in ch:
                w(f"  - {s} ({b[s][a]['layout']}): {', '.join(order(b[s][a]))} → {', '.join(order(b[s][c]))}; "
                  f"completion {b[s][a]['completion']} → {b[s][c]['completion']}, violation ticks {b[s][a]['viol']} → "
                  f"{b[s][c]['viol']}")
    w("")
    un = [(s, c) for s in scen for c in CONDS if not byf[s][c]["done"]]
    w("Runs that do not finish under `full_reorder`: " + ("none." if not un else
      "; ".join(f"{s} ({LONG[c]}, tick limit {json.load(open(byf[s][c]['dir'] / 'observed.json'))['steps']})"
                for s, c in un) + "."))
    w("")


def main():
    by = load()
    scen = sorted(by)
    finished = [s for s in scen if all(by[s][c]["done"] for c in CONDS)]
    unfinished = [(s, c) for s in scen for c in CONDS if not by[s][c]["done"]]
    inter = [s for s in scen if by[s]["HU"]["near_encounters"] > 0]
    rooms = sorted({by[s]["HU"]["layout"] for s in scen})
    sets = {k: [s for s in scen if by[s]["HU"]["set"] == k] for k, *_ in SETS}
    out = []
    w = out.append

    # ---- cross-check against the design chat's figures (stdout)
    print("cross-check (the design chat's figures from REPORT.md):")
    print("  violation ticks, 128 scenarios:", [sum(by[s][c]["viol"] for s in scen) for c in CONDS], "expected [137, 14, 17, 23]")
    print("  held ticks:", [sum(by[s][c]["hold_ticks"] for s in scen) for c in CONDS], "expected [0, 1155, 1415, 1517]")
    for (a, b, *_), exp in zip(STEPS, ("0/91/36 +5.8", "15/101/11 -0.8", "8/112/7 -0.3")):
        s = summary(paired(by, a, b, "completion", finished))
        print(f"  {a}->{b} completion on {s['n']}: {s['lower']}/{s['equal']}/{s['higher']} mean {s['mean']:+.2f}; expected {exp}")

    total_hold = {c: sum(by[s][c]["hold_ticks"] for s in scen) for c in CONDS}

    # ---- step 3b (part 1): computed first, placed after the step tables
    allrows = [r for r in csv.DictReader(open(RESULTS)) if r["strategy"] == "single_task"]   # full_reorder: its own sections
    for r in allrows:
        r["done"] = r["completion"] != "unfinished"
        for k in ("hold_ticks", "near_encounters", "viol"):
            r[k] = int(r[k])
        r["completion"] = int(r["completion"]) if r["done"] else None
        r["dir"] = HERE / "measurement" / r["scenario"] / r["run"]
    p1, p1_summary = part1(allrows, by)
    with_fact = sorted(s for s in scen if windows(by[s]["ON"]["dir"]))
    nofact = len(scen) - len(with_fact)
    wf = ", ".join(with_fact)

    # ---- the document
    w("# What recognising the human's intention adds to a robot's planning: a comparison in simulation")
    w("")
    w("A measurement of the framework *intention-aware human–robot teaming* (kitting, simulated), 5 October 2026. "
      "Every number below is generated by `analysis/kitting/tf1/comparison.py` from the measurement's result table; "
      "none is typed by hand.")
    w("")
    w("## The question")
    w("")
    w("A robot and a human work in the same room. The robot delivers parts from shelves to tables; the human does "
      "the same with other parts, and also takes breaks, switches on the air conditioning, or does things the robot "
      "has no model of. The robot should finish its deliveries without coming too close to the human. The framework "
      "gives the robot three abilities, added one at a time. This report asks what each one changes, on two things: "
      "how long the robot needs for its deliveries, and how often it comes too close to the human.")
    w("")
    w("1. What does planning against the observed human add over a robot that ignores the human?")
    w("2. What does recognising the human's task add over planning against the observed motion alone?")
    w("3. What does context knowledge add to that recognition: (a) with no context fact in force, and (b) with a context "
      "fact in force over chosen ticks?")
    w("")
    w("## Terms")
    w("")
    w("- **Tick.** One step of the simulation. One tick stands for 2 seconds. The robot and the human move at most "
      "20 cm per tick. All durations below are in ticks.")
    w("- **Scenario.** One room, the parts on its shelves, the robot's deliveries, and a script for the human: the "
      "tasks the human performs, in order, with their timing. The human follows the script and does not react to "
      "the robot. The human and the robot are points in the room; the measure between them is their distance.")
    w("- **The four conditions.** The same robot with one ability added at each step:")
    w("  - **human-unaware**: the robot plans and moves as if the room were empty. It never waits for the human.")
    w("  - **intention-unaware**: the robot observes the human's position and motion. It projects that motion a "
      "short time ahead (the human keeps walking straight, or keeps standing, for as long as it has so far) and "
      "plans its route and its waiting around that projection. This short projection is called the *fallback "
      "projection*.")
    w("  - **intention-aware, context knowledge off**: the robot also infers which task the human is doing, from the "
      "human's motion and from the list of tasks the human is assigned. When it is confident enough in one task "
      "(a fixed threshold, with further checks), it plans around the projected course of that whole task instead of "
      "the short projection.")
    w("  - **intention-aware, context knowledge on**: the inference also starts from what the robot knows of the "
      "situation: for example whether it is break time, whether the room is warm, whether the human has just had a "
      "break. These facts change how likely each task is before any motion is seen.")
    w("- **Step.** The change from one condition to the next: step 1 is human-unaware → intention-unaware, step 2 is "
      "intention-unaware → intention-aware with context knowledge off, step 3 is context knowledge off → on: step 3a "
      "with no timeline fact in force (the starting likelihoods alone), step 3b with a timeline fact in force.")
    w("- **Timeline fact.** A context fact stated to hold over chosen ticks of a run, for example *break time* from "
      "tick 77 to tick 155. With context knowledge on, a fact in force makes the task it belongs to (here the coffee "
      "break) more likely before any motion is seen.")
    w("- **min_separation.** The distance the robot's planning tries to keep from the human: 50 cm.")
    w("- **Tick below min_separation.** A tick in which the smallest distance between robot and human during the tick "
      "is below 50 cm. Each such tick is put into one class:")
    w("  - **violation**: the robot moved during the tick, and the distance fell below 50 cm and below the distance "
      "at the start of the tick. The robot moved closer to the human.")
    w("  - **receding**: the robot moved during the tick, and the distance grew.")
    w("  - **passing** / **beside**: the robot stood still, and the human walked past it (passing) or stood next to it "
      "(beside). A standing robot is not counted as violating.")
    w("- **Hold.** The robot deliberately waits in place for a decided number of ticks before going on, so that its "
      "route stays clear of the human's projected route.")
    w("- **Completion.** The tick at which the robot's last delivery is done. A run that does not complete its "
      "deliveries within its tick limit is **unfinished**; it has no completion tick and is reported apart, never "
      "averaged. The tick limit is fixed per scenario before the run: the robot's deliveries along their plain "
      "length, plus the length of the human's script, plus 30 ticks.")
    w("")
    w("## In short")
    w("")
    w(f"Over {len(finished)} scenarios that finish in all four conditions (completion) and {len(scen)} scenarios "
      "(distance), each step compared with the one before it in the same scenarios:")
    w("")
    for a, b, title, sub in STEPS:
        c = summary(paired(by, a, b, "completion", finished))
        v = summary(paired(by, a, b, "viol", scen))
        va, vb = sum(by[x][a]["viol"] for x in scen), sum(by[x][b]["viol"] for x in scen)
        flat = lambda z: z["ci"][0] <= 0 <= z["ci"][1]
        line = (f"- **{title}** ({sub}): violation ticks {va} → {vb} "
                f"({v['lower']} scenarios fewer, {v['higher']} more, {v['equal']} equal); completion "
                f"{c['higher']} scenarios later, {c['lower']} earlier, {c['equal']} equal, mean change "
                f"{signed(c['mean'], 2)} ticks.")
        if b == "ON":
            line += (f" No timeline fact is in force in {nofact} of these {len(scen)} scenarios: this step measures "
                     "the starting likelihoods alone, not context knowledge with a fact in force (step 3b).")
        if flat(c) and flat(v):
            line += (" Individual scenarios change in both directions; neither mean change is distinguishable from "
                     "zero in this set (the room-resampled intervals of both include zero).")
        w(line)
    w("- **Step 3b: context knowledge with a timeline fact in force** (copies of the scenarios with a fact over chosen "
      "ticks, context knowledge on, against the base scenario with context knowledge off): " + "; ".join(p1_summary)
      + ". The fact in accord with the human's task speeds the recognition of that task, the fact not in accord "
      "delays it; completion and violation ticks change in few copies.")
    w("")
    w("## What was run")
    w("")
    w(f"- **{len(scen)} scenarios**, each run in **all four conditions**: {4 * len(scen)} runs. Every comparison "
      "below is paired: the same scenario in two conditions.")
    w(f"- **{len(rooms)} rooms** (simulated kitting cells with shelves, kitting tables, a coffee machine, in some an "
      "air-conditioning switch).")
    w("- The scenarios come from three sets written earlier for testing the framework:")
    for k, lo, hi, name in SETS:
        rs = sorted({by[s]["HU"]["layout"] for s in sets[k]})
        w(f"  - **set {k}**, {name}: {len(sets[k])} scenarios in {len(rs)} room(s).")
    w("  Set A was written to make every decision path of the planner occur. Sets B and C were written to test "
      "context knowledge; set C places the human's breaks, air-conditioning visits, unplanned stops and walks, and "
      "abandoned deliveries at many points of the work.")
    w("- In every run the robot decides one delivery at a time (the strategy *single_task*). Its planner, its "
      "thresholds and every parameter are the same in all runs; only the condition changes.")
    allrows = [r for s in scen for r in by[s].values()]
    dis = sum(int(r["disagreements"] or 0) for r in allrows)
    checked = sum(1 for r in allrows if r["oracle"] == "compared")
    ref_eq = sum(1 for s in scen if by[s]["HU"]["reference"] == "equal")
    w(f"- Every run was checked against an independent re-computation of what the robot should decide on every tick "
      f"(the test-bed's oracle): {checked} of {len(allrows)} runs checked, {dis} disagreements. In {ref_eq} of "
      f"{len(scen)} scenarios the human-unaware robot moves exactly as the robot does in the same room with no human.")
    copies = sum(1 for r in csv.DictReader(open(RESULTS)) if int(r["run"][4:]) > 512 and r["strategy"] == "single_task")
    w(f"- {copies} further runs, copies of these scenarios with a context fact in force over chosen ticks, run with "
      "context knowledge on only, are compared with their base scenarios in the section *Context knowledge with a fact "
      "in force*; the four-condition tables leave them out.")
    w(f"- {len(by) * 4 - len(unfinished)} of {len(by) * 4} runs finish. The {len(unfinished)} unfinished runs are "
      "reported in their own section. The completion comparisons use the "
      f"{len(finished)} scenarios that finish in all four conditions; the distance measures use all {len(scen)}.")
    w("")

    # ---- conditions side by side
    w("## The four conditions side by side")
    w("")
    w(f"Completion over the {len(finished)} scenarios that finish in all four conditions; every other measure over all "
      f"{len(scen)} scenarios. In the last column no timeline fact is in force in {nofact} of the {len(scen)} scenarios "
      f"(a fact holds over the whole run in {wf}): it shows context knowledge with the starting likelihoods alone. "
      "Context knowledge with a fact in force is step 3b.")
    w("")
    head = ["measure"] + [LONG[c] for c in CONDS[:3]] + [f"{LONG['ON']}, no timeline fact in force in {nofact} of {len(scen)}"]
    rows = []
    comp = {c: [by[s][c]["completion"] for s in finished] for c in CONDS}
    rows.append(["completion, mean (ticks)"] + [num(mean(comp[c])) for c in CONDS])
    rows.append(["completion, median (ticks)"] + [num(median(comp[c]), 0) for c in CONDS])
    rows.append(["unfinished runs"] + [sum(1 for s in scen if not by[s][c]["done"]) for c in CONDS])
    rows.append(["held ticks, total"] + [total_hold[c] for c in CONDS])
    rows.append(["scenarios with a hold"] + [sum(1 for s in scen if by[s][c]["hold_ticks"] > 0) for c in CONDS])
    for key, label, one in (("viol", "violation ticks", "violation tick"), ("recede", "receding ticks", None),
                            ("stand_passing", "passing ticks (robot standing)", None),
                            ("stand_beside", "beside ticks (robot standing)", None),
                            ("near_encounters", "ticks below min_separation, all classes",
                             "tick below min_separation")):
        rows.append([f"{label}, total"] + [sum(by[s][c][key] for s in scen) for c in CONDS])
        if one:
            rows.append([f"scenarios with at least one {one}"] +
                        [sum(1 for s in scen if by[s][c][key] > 0) for c in CONDS])
    rows.append(["smallest distance, median over scenarios (cm)"] + [num(median([by[s][c]["sep_min"] for s in scen]))
                                                                     for c in CONDS])
    rows.append(["smallest distance, lowest scenario (cm)"] + [num(min(by[s][c]["sep_min"] for s in scen))
                                                              for c in CONDS])
    w(table(head, rows))
    w("")

    # ---- the steps, all scenarios
    w("## The three steps, paired per scenario")
    w("")
    w(f"Step 3a is context knowledge with no timeline fact in force in {nofact} of the {len(scen)} scenarios: the "
      "starting likelihoods alone. Step 3b, with a fact in force, has its own section after these tables.")
    w("")
    w("A change is the second condition's value minus the first's, in the same scenario: negative means earlier "
      "completion or fewer ticks. The interval and the room counts treat the room as the unit (see *Statistics*). "
      "The Wilcoxon signed-rank p-value is given as an indication only; it assumes independent scenarios.")
    w("")
    w(f"### All scenarios ({len(finished)} for completion, {len(scen)} for the distance measures)")
    w("")
    w(table(STEP_HEAD, step_rows(by, scen, finished)))
    w("")
    fin_inter = [s for s in inter if s in finished]
    w(f"### The scenarios in which the human and the robot interact ({len(fin_inter)} for completion, {len(inter)} "
      "for the distance measures)")
    w("")
    w(f"A scenario counts as interacting when the human-unaware robot has at least one tick below min_separation. In "
      f"the other {len(scen) - len(inter)} scenarios the robot ignoring the human never comes within 50 cm of the "
      "human, and the four conditions differ in completion in "
      f"{sum(1 for s in scen if s not in inter and s in finished and len({by[s][c]['completion'] for c in CONDS}) > 1)}"
      " of them.")
    w("")
    w(table(STEP_HEAD, step_rows(by, inter, fin_inter)))
    w("")

    # ---- step 3b
    out.extend(p1)

    # ---- the trade of step 1
    w("## The trade of step 1: delay against violations")
    w("")
    d_tot = sum(by[s]["IU"]["completion"] - by[s]["HU"]["completion"] for s in finished)
    d_int = sum(by[s]["IU"]["completion"] - by[s]["HU"]["completion"] for s in fin_inter)
    v_rem = sum(by[s]["HU"]["viol"] - by[s]["IU"]["viol"] for s in finished)
    v_rem_all = sum(by[s]["HU"]["viol"] - by[s]["IU"]["viol"] for s in scen)
    b_rem = sum(by[s]["HU"]["near_encounters"] - by[s]["IU"]["near_encounters"] for s in finished)
    rows = [["completion delay added, total (ticks)", d_tot, d_int],
            ["held ticks added, total", sum(by[s]["IU"]["hold_ticks"] for s in finished),
             sum(by[s]["IU"]["hold_ticks"] for s in fin_inter)],
            ["violation ticks removed, total", v_rem, sum(by[s]["HU"]["viol"] - by[s]["IU"]["viol"] for s in fin_inter)],
            ["ticks below min_separation removed, total", b_rem,
             sum(by[s]["HU"]["near_encounters"] - by[s]["IU"]["near_encounters"] for s in fin_inter)],
            ["ticks of delay per violation tick removed", num(d_tot / v_rem, 2) if v_rem else "–",
             num(d_int / sum(by[s]["HU"]["viol"] - by[s]["IU"]["viol"] for s in fin_inter), 2)],
            ["scenarios with a delay", sum(1 for s in finished if by[s]["IU"]["completion"] > by[s]["HU"]["completion"]),
             sum(1 for s in fin_inter if by[s]["IU"]["completion"] > by[s]["HU"]["completion"])],
            ["scenarios with a delay and no violation removed",
             sum(1 for s in finished if by[s]["IU"]["completion"] > by[s]["HU"]["completion"]
                 and by[s]["HU"]["viol"] <= by[s]["IU"]["viol"]),
             sum(1 for s in fin_inter if by[s]["IU"]["completion"] > by[s]["HU"]["completion"]
                 and by[s]["HU"]["viol"] <= by[s]["IU"]["viol"])]]
    w(table(["", f"all {len(finished)} finished scenarios", f"the {len(fin_inter)} interacting ones"], rows))
    w("")
    w(f"Over all {len(scen)} scenarios, unfinished runs included, step 1 removes {v_rem_all} violation ticks.")
    w("")
    w("![Step 1 per scenario](comparison/trade.png)")
    w("")

    # ---- per set
    w("## Per set of scenarios")
    w("")
    rows = []
    for k, lo, hi, name in SETS:
        sc = sets[k]
        fin = [s for s in sc if s in finished]
        for a, b, title, _ in STEPS:
            s1 = summary(paired(by, a, b, "completion", fin))
            s2 = summary(paired(by, a, b, "viol", sc))
            rows.append([f"{k} ({len(sc)})", title.split(":")[0],
                         f"{s1['lower']} / {s1['equal']} / {s1['higher']}", signed(s1["mean"], 2),
                         f"{s2['lower']} / {s2['equal']} / {s2['higher']}",
                         f"{sum(by[s][a]['viol'] for s in sc)} → {sum(by[s][b]['viol'] for s in sc)}"])
    w(table(["set (scenarios)", "step", "completion: earlier / equal / later", "completion: mean change",
             "violation ticks: fewer / equal / more", "violation ticks, total"], rows))
    w("")

    # ---- unfinished
    w("## Runs that do not finish")
    w("")
    for s in sorted({s for s, _ in unfinished}):
        cs = [c for c in CONDS if not by[s][c]["done"]]
        done = [c for c in CONDS if by[s][c]["done"]]
        fin_text = "; ".join(f"*{LONG[c]}* at tick {by[s][c]['completion']}" for c in done)
        w(f"- **{s}**: unfinished in " + "; ".join(f"*{LONG[c]}*" for c in cs) + f". Finished in {fin_text}.")
        for c in cs:
            obs = json.load(open(by[s][c]["dir"] / "observed.json"))
            log = by[s][c]["dir"] / f"{by[s][c]['run']}.log"
            holds = [(int(m[1]), int(m[2])) for m in
                     (re.match(r"\[hold\] step=(\d+) \S+ start planned=(\d+)", l) for l in open(log)) if m]
            late = [h for h in holds if h[0] > obs["last_ack"]]
            w(f"  - {LONG[c]}: tick limit {obs['steps']}; the human's script ends at tick {obs['last_ack']}; after it "
              f"the robot starts {len(late)} holds, of "
              + ", ".join(f"{p} ticks at tick {t}" for t, p in late) + f"; held ticks in all {by[s][c]['hold_ticks']}.")
    w("")
    w("At the end of its script the human stands still beside the robot's remaining target and stays there to the "
      "end of the run. The robots that observe the human wait for the standing human to move; each wait is as long "
      "as the human has stood so far, so the waits double. The human-unaware robot walks to its target and finishes. "
      "This scenario is left out of every completion figure above; in the distance measures it is included, each "
      "run counted over its whole length.")
    w("")

    full_reorder_sections(w, by, scen, finished)

    # ---- figures
    w("## The change per scenario")
    w("")
    w("Each panel shows, for one step, how many scenarios change by how much. Scenarios with no change are counted "
      "in the panel's text and not drawn.")
    w("")
    w("![Change in completion per step](comparison/completion.png)")
    w("")
    w("![Change in violation ticks per step](comparison/violations.png)")
    w("")

    # ---- statistics
    sizes = [sum(1 for s in scen if by[s]["HU"]["layout"] == room) for room in rooms]
    w("## Statistics")
    w("")
    w("- The tables are descriptive. Every comparison is paired per scenario, because the scenarios differ far more "
      "from each other than the conditions do.")
    w("- The scenarios are not independent samples. They were written by hand to place particular situations; "
      f"several share a human script or are copies of each other with one detail changed; and they share {len(rooms)} "
      "rooms. A test over scenarios therefore overstates the evidence. The Wilcoxon signed-rank p-value over "
      "scenarios (zero changes left out) is given only as an indication.")
    w("- To respect the dependence within a room, the room is also used as the unit: the tables give how many rooms "
      "have a negative, zero or positive mean change, and a 95% interval for the mean change per scenario from a "
      "bootstrap that resamples whole rooms (10,000 resamples). With "
      f"{len(rooms)} rooms of very unequal size ({min(sizes)} to {max(sizes)} scenarios) this interval is coarse.")
    w("")

    # ---- limits
    w("## What these numbers do not show")
    w("")
    w("- One planning strategy only: the robot decides one delivery at a time. A robot that reorders all its "
      "deliveries could use recognition differently; it was not measured here.")
    w("- The scenarios are authored to test the framework, not drawn at random from real work. The counts say how "
      "often something happened in this set, not how often it would happen on a shop floor.")
    w("- The human is scripted and does not react to the robot. A real person would step aside, wait, or change the "
      "order of work.")
    w("- One domain (kitting) in simulation, with point agents and a fixed speed.")
    w("- Recognition itself is measured only in step 3b, by two counts (the admission delay and the wrong-admission "
      "ticks); elsewhere only what recognition changes in the robot's deliveries and distance, in this set.")
    w(f"- The scenarios of steps 1 to 3a have no timeline fact in force in {nofact} of {len(scen)}, so step 3a "
      "measures context knowledge with the starting likelihoods alone. What context knowledge does when a fact is in "
      "force is step 3b alone.")
    w("- The timeline facts of step 3b are placed by a fixed rule on chosen ticks of each script (REPORT.md, \"Part "
      "1\"); they are not a sample of real shifts. Both classes exist for every script that allows them, but their "
      "counts differ (in accord fewer than not in accord).")
    w("- Step 3b compares each copy with context knowledge on against its base with context knowledge off, so its "
      "admission delays include what the starting likelihoods alone do (its reference table).")
    w("")
    text = "\n".join(out) + "\n"
    (HERE / "COMPARISON.md").write_text(text)

    # ---- figures, then the self-contained html (the same text, the figures embedded)
    figure(by, finished, scen, inter)
    html = markdown.markdown(text, extensions=["tables"])
    for p in sorted(FIG.glob("*.png")):
        data = base64.b64encode(p.read_bytes()).decode()
        html = html.replace(f'src="comparison/{p.name}"', f'src="data:image/png;base64,{data}"')
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Recognition and planning: comparison</title>
<style>
body {{ font-family: system-ui, -apple-system, "Segoe UI", sans-serif; color: #0b0b0b; background: #ffffff;
       max-width: 1100px; margin: 2em auto; padding: 0 16px; line-height: 1.5; font-size: 15px; }}
h1 {{ font-size: 1.6em; }} h2 {{ margin-top: 2em; border-bottom: 1px solid #e6e5e0; padding-bottom: 0.2em; }}
table {{ border-collapse: collapse; margin: 1em 0; font-size: 13px; display: block; overflow-x: auto; }}
th, td {{ border: 1px solid #e6e5e0; padding: 4px 8px; text-align: left; vertical-align: top; }}
th {{ background: #f6f5f1; }}
img {{ max-width: 100%; }}
code {{ background: #f6f5f1; padding: 0 3px; }}
@media print {{ body {{ max-width: none; }} table {{ display: table; }} }}
</style></head><body>
{html}
</body></html>
"""
    (HERE / "comparison.html").write_text(page)
    print(f"written: {HERE / 'COMPARISON.md'}, {HERE / 'comparison.html'}, figures in {FIG}")


if __name__ == "__main__":
    main()
