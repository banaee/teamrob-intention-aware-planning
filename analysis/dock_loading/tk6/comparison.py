#!/usr/bin/env python3
"""
comparison.py — the comparison report of T-K part 1's step 6 on dock_loading (Hadi, 6 October 2026; design_records.md,
"T-K", STEP 6), in the form of T-F part 1's (analysis/kitting/tf1/comparison.py). Every number and table of the report
comes from here; none is typed by hand.

    comparison.py     reads analysis/dock_loading/tk6/measurement/results.csv (analysis/instruments/mpb/table.py) and
                      tags.csv (analysis/instruments/mpb/tag.py), writes analysis/dock_loading/tk6/COMPARISON.md and the
                      self-contained comparison.html (the same text, the figure embedded; the figure in comparison/,
                      git-ignored by the rule for analysis/)

The data:
- The 74 planning scripts, each in the four conditions. These give the side-by-side table and the steps 1, 2 and 3a,
  paired per scenario.
- The 164 copies with break_time (context knowledge on). These give the tag per task: each copy is read against its
  base with context knowledge off, and against its base with it on and no fact.
- The 54 recognition scenarios, with context knowledge off and on.

The statistics are kitting's:
- descriptive and paired per scenario;
- the Wilcoxon signed-rank test as an indication only;
- the room as the unit: the mean change per room, and a 95% interval from a bootstrap that resamples rooms.
"""
import base64
import csv
import json
import random
import re
import statistics as st
import sys
from pathlib import Path

import markdown
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT), str(ROOT / "mesa_sim")]
M = HERE / "measurement"
FIG = HERE / "comparison"
CONDS = ["HU", "IU", "OFF", "ON"]
LONG = {"HU": "human-unaware", "IU": "intention-unaware", "OFF": "intention-aware, context knowledge off",
        "ON": "intention-aware, context knowledge on"}
STEPS = [("HU", "IU", "Step 1: planning against the observed human", "human-unaware → intention-unaware"),
         ("IU", "OFF", "Step 2: recognition of the human's task", "intention-unaware → intention-aware, context knowledge off"),
         ("OFF", "ON", "Step 3a: context knowledge with no timeline fact in force",
          "context knowledge off → on, the starting likelihoods and the recency facts alone")]
TAGS = ["in accord", "not in accord", "no fact"]
INK, MUTED, BAR = "#0b0b0b", "#8a8880", "#2a78d6"
COPY = re.compile(r"(scenario_s\d+_\d+)'s copy with break_time")


def cond(r):
    on = lambda v: v in ("True", "on")
    if not on(r["human_aware"]):
        return "HU"
    if not on(r["intention_aware"]):
        return "IU"
    return "ON" if on(r["context_knowledge"]) else "OFF"


def mean(xs):
    return st.mean(xs) if xs else None


def median(xs):
    return st.median(xs) if xs else None


def boot_rooms(pairs, seed=0, n=10000):
    rooms = {}
    for room, d in pairs:
        rooms.setdefault(room, []).append(d)
    keys = sorted(rooms)
    rnd = random.Random(seed)
    means = sorted(sum(draw) / len(draw) for draw in
                   ([x for _ in keys for x in rooms[rnd.choice(keys)]] for _ in range(n)))
    return means[int(0.025 * n)], means[int(0.975 * n) - 1]


def wil(ds):
    nz = [d for d in ds if d != 0]
    return None if len(nz) < 6 else wilcoxon(nz).pvalue


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    return "\n".join(out + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])


def num(x, d=1):
    return "–" if x is None else (str(x) if d == 0 else f"{float(x):.{d}f}")


def signed(x, d=1):
    return "–" if x is None else f"{float(x):+.{d}f}"


def pval(p):
    return "–" if p is None else ("< 0.001" if p < 0.001 else f"{p:.3f}")


def three(ds, words=("earlier", "equal", "later")):
    return f"{sum(d < 0 for d in ds)} {words[0]} / {sum(d == 0 for d in ds)} {words[1]} / {sum(d > 0 for d in ds)} {words[2]}"


def load():
    from domains.dock_loading.registry import domain_config
    rows = list(csv.DictReader(open(M / "results.csv")))
    by, byf = {}, {}                       # single_task; full_reorder (Hadi, 6 October 2026: the planning scripts only)
    for r in rows:
        r["done"] = r["completion"] != "unfinished"
        for k in ("hold_ticks", "near_encounters", "viol", "recede", "stand_passing", "stand_beside", "decisions"):
            r[k] = int(r[k])
        r["completion"] = int(r["completion"]) if r["done"] and r["completion"] not in ("None", "") else None
        r["sep_min"] = float(r["sep_min"]) if r["sep_min"] else None
        (byf if r["strategy"] == "full_reorder" else by).setdefault(r["scenario"], {})[cond(r)] = r
    desc = {s: domain_config["scenarios"][s].description for s in by}
    base_of = {s: COPY.search(desc[s])[1] for s in by if COPY.search(desc[s])}
    dep = {s for s in by if next(a for a in domain_config["scenarios"][s].agents if a.agent_type == "human")
           .scheduled_tasks.dependence.value == "on_robot"}
    plan = sorted(s for s in by if len(by[s]) == 4)
    recog = sorted(s for s in by if set(by[s]) == {"OFF", "ON"} and s not in base_of)
    tags = {}
    for t in csv.DictReader(open(M / "tags.csv")):
        tags.setdefault((t["scenario"], t["run"]), []).append(t)
    return rows, by, byf, plan, recog, base_of, dep, tags


def order(r):
    """The robot's executed order of tasks in a run: its task per tick (robot.json), consecutive repeats merged."""
    out = []
    for a in json.load(open(M / r["scenario"] / r["run"] / "robot.json")):
        if a["task"] is not None and (not out or out[-1] != a["task"]):
            out.append(a["task"])
    return [re.sub(r"\(\?pallet=(\w+)\)", r"(\1)", x).replace("deliver_pallet", "deliver").replace("load_return", "return")
            for x in out]


def run_tags(tags, by, s, c):
    r = by[s].get(c)
    return [] if r is None else tags.get((s, r["run"]), [])


def keyed(ts):
    """A run's stretches keyed by (task, its k-th occurrence): the same human stretch across runs of one script."""
    seen, out = {}, {}
    for t in ts:
        k = seen[t["task"]] = seen.get(t["task"], -1) + 1
        out[(t["task"], k)] = t
    return out


def adm(t, reading):
    v = t[f"adm_{reading}"]
    return None if v in ("", "never") else int(v)


def paired(by, a, b, key, scen):
    return [(by[s][a]["layout"], s, by[s][b][key] - by[s][a][key]) for s in scen
            if by[s][a][key] is not None and by[s][b][key] is not None]


def step_rows(by, scen, finished):
    rows = []
    for a, b, title, _ in STEPS:
        for key, label, sc in (("completion", "completion (ticks)", finished), ("viol", "violation ticks", scen),
                               ("near_encounters", "ticks below min_separation", scen), ("hold_ticks", "held ticks", scen)):
            ps = paired(by, a, b, key, sc)
            ds = [d for _, _, d in ps]
            rooms = {}
            for room, _, d in ps:
                rooms.setdefault(room, []).append(d)
            rm = [mean(v) for v in rooms.values()]
            ci = boot_rooms([(room, d) for room, _, d in ps]) if ps else (None, None)
            word = ("earlier", "equal", "later") if key == "completion" else ("fewer", "equal", "more")
            rows.append([title.split(":")[0], label, len(ds), three(ds, word), signed(mean(ds), 2), signed(median(ds)),
                         "–" if ci[0] is None else f"{ci[0]:+.2f} to {ci[1]:+.2f}",
                         f"{sum(m < 0 for m in rm)} / {sum(m == 0 for m in rm)} / {sum(m > 0 for m in rm)}",
                         pval(wil(ds))])
    return rows


STEP_HEAD = ["step", "measure", "scenarios", "per scenario: lower / equal / higher", "mean change", "median change",
             "95% interval of the mean (rooms resampled)", "rooms with mean change < 0 / = 0 / > 0",
             "Wilcoxon p (indication only)"]


def recognition_rows(tags, by, scen, a, b, reading):
    """Per stretch of a task with a hypothesis, a's run against b's: admitted in each, the change of the delay."""
    n = adm_a = adm_b = 0
    ds, da, db, wa, wb = [], [], [], 0, 0
    for s in scen:
        A, B = keyed(run_tags(tags, by, s, a)), keyed(run_tags(tags, by, s, b))
        for k, x in A.items():
            y = B.get(k)
            if y is None or not x["hypothesis"]:
                continue
            if reading == "record" and (int(x["counted"]) == 0 or int(y["counted"]) == 0):
                continue
            n += 1
            p, q = adm(x, reading), adm(y, reading)
            adm_a += p is not None
            adm_b += q is not None
            if p is not None:
                da.append(p)
            if q is not None:
                db.append(q)
            if p is not None and q is not None:
                ds.append(q - p)
        for x in A.values():
            wa += int(x[f"wrong_{reading}"])
        for y in B.values():
            wb += int(y[f"wrong_{reading}"])
    return dict(n=n, adm_a=adm_a, adm_b=adm_b, med_a=median(da), med_b=median(db), ds=ds, wrong_a=wa, wrong_b=wb)


def kind(task):
    name = task.split("(")[0]
    return {"confirm_delivered_pallet": "scan", "coffee_break": "coffee break", "office_break": "office break"}.get(
        name, "other (a walk to the standby place or the desk, a stand)")


def tag_section(w, tags, by, base_of):
    """The tag per task: each copy's stretches against its base's (context knowledge off; on with no fact)."""
    data = {g: [] for g in TAGS}
    for copy, base in sorted(base_of.items()):
        if base not in by or "ON" not in by[copy]:
            continue
        C = keyed(run_tags(tags, by, copy, "ON"))
        OFF, NOF = keyed(run_tags(tags, by, base, "OFF")), keyed(run_tags(tags, by, base, "ON"))
        for k, c in C.items():
            data[c["tag"]].append((copy, base, c, OFF.get(k), NOF.get(k)))
    w("## The tag per task")
    w("")
    w("Each task the human performs in a copy with break_time is tagged by the world's facts at its first tick (glossary "
      "§7; the reader `analysis/instruments/mpb/tag.py`): **in accord** (a fact holds and the human performs the task "
      "it makes more likely: break time, the coffee break), **not in accord** (a fact holds and the human performs "
      "another task), **no fact**. The task a fact makes more likely is the declared context knowledge's raised task. "
      "Provisional (TODO-185, for Hadi): a fact that lowers a task (a recency fact) gives no tag; a task that starts "
      "while only a lowering fact holds is *no fact*, and its lowered tasks are counted apart below.")
    w("")
    w("Each stretch of a copy (context knowledge on, its fact in force) is read against the same stretch of its base "
      "scenario with context knowledge off, and with context knowledge on and no fact. \"Admitted\" in two readings "
      "(Hadi, 6 October 2026): **gate**, the first tick the gate's answer clears for the task's hypothesis; **record**, "
      "the first tick the meta-planner's decision record holds it (before the robot's terminal decision). Delays are "
      "ticks from the stretch's first tick.")
    w("")
    cnt = []
    for g in TAGS:
        by_kind = {}
        for _, _, c, _, _ in data[g]:
            by_kind[kind(c["task"])] = by_kind.get(kind(c["task"]), 0) + 1
        cnt.append([g, len(data[g]), len({x[0] for x in data[g]}),
                    "; ".join(f"{k} {v}" for k, v in sorted(by_kind.items()))])
    w(table(["tag", "task stretches", "copies", "by kind of task"], cnt))
    w("")
    head = ["measure"] + [f"{g} ({len(data[g])})" for g in TAGS]
    rows = []
    for reading in ("gate", "record"):
        for ref, label in ((3, "off"), (4, "on, no fact")):
            def ds_of(g):
                out = []
                for x in data[g]:
                    c, b = x[2], x[ref]
                    if b is None or not c["hypothesis"]:
                        continue
                    if reading == "record" and (int(c["counted"]) == 0 or int(b["counted"]) == 0):
                        continue
                    out.append((adm(b, reading), adm(c, reading)))
                return out
            rows.append([f"{reading}: admitted, base {label} / copy"] + [
                (lambda ps: f"{sum(p is not None for p, _ in ps)} / {sum(q is not None for _, q in ps)} of {len(ps)}")(ds_of(g))
                for g in TAGS])
            rows.append([f"{reading}: delay median (admitted in both), base {label} / copy"] + [
                (lambda ps: "–" if not ps else f"{num(median([p for p, _ in ps]))} / {num(median([q for _, q in ps]))} ({len(ps)})")(
                    [(p, q) for p, q in ds_of(g) if p is not None and q is not None]) for g in TAGS])
            rows.append([f"{reading}: delay per stretch against base {label}"] + [
                three([q - p for p, q in ds_of(g) if p is not None and q is not None]) for g in TAGS])
        for ref, label in ((3, "off"), (4, "on, no fact")):
            rows.append([f"{reading}: wrong-admission ticks, base {label} → copy"] + [
                f"{sum(int(x[ref][f'wrong_{reading}']) for x in data[g] if x[ref] is not None)} → "
                f"{sum(int(x[2][f'wrong_{reading}']) for x in data[g] if x[ref] is not None)}" for g in TAGS])
    for key, label in (("viol", "violation ticks"), ("near", "ticks below min_separation")):
        for ref, rl in ((3, "off"), (4, "on, no fact")):
            rows.append([f"{label} inside the task, base {rl} → copy"] + [
                f"{sum(int(x[ref][key]) for x in data[g] if x[ref] is not None)} → "
                f"{sum(int(x[2][key]) for x in data[g] if x[ref] is not None)}" for g in TAGS])
    w(table(head, rows))
    w("")
    for g in TAGS[:2]:
        by_kind = {}
        for x in data[g]:
            if x[3] is None or not x[2]["hypothesis"]:
                continue
            p, q = adm(x[3], "gate"), adm(x[2], "gate")
            if p is not None and q is not None:
                by_kind.setdefault(kind(x[2]["task"]), []).append(q - p)
        w(f"- **{g}**, the gate's delay against context knowledge off, by kind of task: " + "; ".join(
            f"{k}: {three(v)}, median {signed(median(v))}" for k, v in sorted(by_kind.items())) + "." if by_kind else
          f"- **{g}**: no stretch admitted in both.")
    w("")
    low = [x for g in TAGS for x in data[g] if x[2]["lowered"]]
    performed = [x for x in low if x[2]["task"].split("(")[0] in x[2]["lowered"].split(";")]
    w(f"Lowered tasks (the provisional reading of TODO-185): {len(low)} of the copies' stretches start while a "
      f"foreseeable task is at its suppressed level; in {len(performed)} the human performs that task "
      f"({', '.join(sorted({x[0] for x in performed})) or 'none'}). Their tags as counted above: "
      + ", ".join(f"{g} {sum(x[2]['tag'] == g for x in low)}" for g in TAGS) + ".")
    w("")
    return data


def main():
    rows, by, byf, plan, recog, base_of, dep, tags = load()
    planf = sorted(s for s in byf if len(byf[s]) == 4)
    finf = [s for s in planf if all(byf[s][c]["done"] for c in CONDS)]
    indep = [s for s in plan if s not in dep]
    finished = [s for s in plan if all(by[s][c]["done"] for c in CONDS)]
    rooms = sorted({by[s]["OFF"]["layout"] for s in plan})
    out = []
    w = out.append
    w("# dock_loading's stage 1 under the present gate: a comparison in simulation")
    w("")
    w("T-K part 1, step 6 (Hadi, 6 October 2026; design_records.md, \"T-K\", STEP 6). Debugging, not the evaluation: "
      "the set covers various situations roughly; nothing was adjusted to a result. Generated by `comparison.py` from "
      "`measurement/results.csv` and `measurement/tags.csv`; the set and its rules: `README.md`.")
    w("")
    w("## What was run")
    w("")
    oracle_rows = [r for r in rows if r["oracle"] == "compared"]
    dis = sum(int(r["disagreements"]) for r in oracle_rows)
    ref = [r for r in rows if r["reference"] != "none"]
    w(f"- {len(rows)} runs ({sum(r['strategy'] == 'single_task' for r in rows)} `single_task`, {sum(r['strategy'] == 'full_reorder' for r in rows)} `full_reorder`), assignment knowledge on, rooms {', '.join(rooms)}.")
    w(f"- {len(plan)} planning scripts in the four conditions ({len(indep)} independent of the robot, {len(plan) - len(indep)} "
      f"that depend on it); {len(base_of)} copies with break_time, context knowledge on; {len(recog)} recognition "
      "scenarios (the robot idle) with context knowledge off and on; under `full_reorder`, "
      f"{len(planf)} planning scripts in the four conditions (Hadi, 6 October 2026). Every comparison of conditions "
      "stays inside one strategy.")
    w(f"- The oracle compared on {len(oracle_rows)} runs: {dis} disagreements. The reference check (human-unaware "
      f"against the robot alone) on {len(ref)} runs: " + ", ".join(
          f"{v} {sum(r['reference'] == v for r in ref)}" for v in sorted({r['reference'] for r in ref})) + ".")
    w(f"- Settings as stated in every run: {sum(r['settings_agree'] == 'True' for r in rows)} of {len(rows)}.")
    w("")
    w("## The four conditions side by side (the planning scripts)")
    w("")
    head = ["measure"] + [LONG[c] for c in CONDS]
    tr = []
    tr.append(["runs that finish"] + [f"{sum(by[s][c]['done'] for s in plan)} of {len(plan)}" for c in CONDS])
    tr.append([f"completion, mean (ticks; the {len(finished)} scripts finished in all four)"] +
              [num(mean([by[s][c]['completion'] for s in finished])) for c in CONDS])
    for key, label in (("hold_ticks", "held ticks, total"), ("decisions", "decisions, total"),
                       ("near_encounters", "ticks below min_separation, total"), ("viol", "of them violation ticks (a moving robot)"),
                       ("recede", "of them a moving robot receding"), ("stand_passing", "of them a standing robot, the human passing"),
                       ("stand_beside", "of them a standing robot, the human beside it")):
        tr.append([label] + [sum(by[s][c][key] for s in plan) for c in CONDS])
    tr.append(["scripts with a violation tick"] + [sum(by[s][c]["viol"] > 0 for s in plan) for c in CONDS])
    tr.append(["closest distance, median of the scripts (cm)"] +
              [num(median([by[s][c]["sep_min"] for s in plan if by[s][c]["sep_min"] is not None])) for c in CONDS])
    w(table(head, tr))
    w("")
    w("The same for the scripts that depend on the robot alone (the human's timing follows the robot's deliveries, so "
      "a human-unaware run meets a different human trajectory):")
    w("")
    dp = [s for s in plan if s in dep]
    w(table(head, [["runs that finish"] + [f"{sum(by[s][c]['done'] for s in dp)} of {len(dp)}" for c in CONDS]] +
            [[label] + [sum(by[s][c][key] for s in dp) for c in CONDS] for key, label in
             (("near_encounters", "ticks below min_separation, total"), ("viol", "violation ticks"),
              ("hold_ticks", "held ticks"))]))
    w("")
    w("## The three steps, paired per scenario")
    w("")
    w(f"Over the {len(plan)} planning scripts ({len(finished)} for completion). Negative is earlier or fewer.")
    w("")
    w(table(STEP_HEAD, step_rows(by, plan, finished)))
    w("")
    w("Per room, the mean change per script (completion; violation ticks):")
    w("")
    pr = []
    for room in rooms:
        sc = [s for s in plan if by[s]["OFF"]["layout"] == room]
        fi = [s for s in finished if s in sc]
        pr.append([room, len(sc)] + [f"{signed(mean([d for _, _, d in paired(by, a, b, 'completion', fi)]), 2)}; "
                                     f"{signed(mean([d for _, _, d in paired(by, a, b, 'viol', sc)]), 2)}"
                                     for a, b, _, _ in STEPS])
    w(table(["room", "scripts"] + [t.split(":")[0] for _, _, t, _ in STEPS], pr))
    w("")
    full_reorder_sections(w, by, byf, plan, planf, finished, finf)
    w("## Recognition: context knowledge off against on, with no timeline fact in force")
    w("")
    w("Per stretch of a task the robot has a hypothesis for, the same stretch in the two runs. The recognition set has "
      "an idle robot whose pool is empty from the start, so its decision record holds nothing: only the gate's reading "
      "applies there.")
    w("")
    rr = []
    for label, scen in (("planning scripts", plan), ("recognition set (robot idle)", recog)):
        for reading in ("gate", "record"):
            x = recognition_rows(tags, by, scen, "OFF", "ON", reading)
            if x["n"] == 0:
                continue
            rr.append([label, reading, x["n"], f"{x['adm_a']} / {x['adm_b']}", f"{num(x['med_a'])} / {num(x['med_b'])}",
                       three(x["ds"]), f"{x['wrong_a']} → {x['wrong_b']}"])
    w(table(["set", "reading", "task stretches", "admitted: off / on", "delay median: off / on",
             "delay per stretch, on against off", "wrong-admission ticks: off → on"], rr))
    w("")
    w("The re-measurement of stage 1 (context knowledge off, the present gate), per room, the recognition set: task "
      "stretches with a hypothesis, admitted by the gate within the stretch, median delay.")
    w("")
    sr = []
    for room in sorted({by[s]["OFF"]["layout"] for s in recog}):
        for c in ("OFF", "ON"):
            st_ = [t for s in recog if by[s]["OFF"]["layout"] == room for t in run_tags(tags, by, s, c) if t["hypothesis"]]
            ad = [adm(t, "gate") for t in st_ if adm(t, "gate") is not None]
            ks = {}
            for t in st_:
                ks.setdefault(kind(t["task"]), [0, 0])
                ks[kind(t["task"])][0] += 1
                ks[kind(t["task"])][1] += adm(t, "gate") is not None
            sr.append([room, LONG[c], len(st_), len(ad), num(median(ad)),
                       "; ".join(f"{k} {a} of {n}" for k, (n, a) in sorted(ks.items()))])
    w(table(["room", "condition", "task stretches", "admitted", "delay median", "admitted by kind"], sr))
    w("")
    data = tag_section(w, tags, by, base_of)
    w("## Runs that do not finish")
    w("")
    un = [(s, c, st_) for st_, b in (("single_task", by), ("full_reorder", byf)) for s in sorted(b) for c in b[s]
          if not b[s][c]["done"] and s not in recog]
    w("None." if not un else "; ".join(f"{s} ({LONG[c]}, {st_})" for s, c, st_ in un) + ".")
    w("")
    w("## What these numbers do not show")
    w("")
    w("- Debugging, not the evaluation: the scripts and the windows are authored to make situations occur, not drawn "
      "from real work. The counts say how often something happened in this set.")
    w("- Two strategies for the planning scripts, `single_task` (every part) and `full_reorder` (the four conditions "
      "only: no copies, no recognition set); `full_reorder` logs no per-candidate hold (TODO-141). Assignment knowledge "
      "on, a scripted human who does not react to the robot, full observation, point agents at a fixed speed.")
    w("- Four rooms that share one hall; the room bootstrap over four rooms is coarse.")
    w("- In the scripts that depend on the robot the human's timing follows the robot's, so the conditions meet "
      "different human trajectories; the oracle does not run on them.")
    w("- The tag is provisional for a fact that lowers a task (TODO-185).")
    w("- No A/C switch in these rooms: ac_activation has no hypothesis, room_warm has no use, and only break_time is "
      "placed.")
    w("")
    text = "\n".join(out) + "\n"
    (HERE / "COMPARISON.md").write_text(text)
    figure(data)
    html = markdown.markdown(text + "\n![The gate's admission delay per tag](comparison/tags.png)\n", extensions=["tables"])
    for p in sorted(FIG.glob("*.png")):
        html = html.replace(f'src="comparison/{p.name}"',
                            f'src="data:image/png;base64,{base64.b64encode(p.read_bytes()).decode()}"')
    (HERE / "comparison.html").write_text(
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" "
        "content=\"width=device-width, initial-scale=1\"><title>dock_loading stage 1 comparison</title><style>"
        "body { font-family: system-ui, sans-serif; color: #0b0b0b; background: #ffffff; max-width: 1100px; "
        "margin: 2em auto; padding: 0 16px; line-height: 1.5; font-size: 15px; } table { border-collapse: collapse; "
        "margin: 1em 0; font-size: 13px; display: block; overflow-x: auto; } th, td { border: 1px solid #e6e5e0; "
        "padding: 4px 8px; text-align: left; vertical-align: top; } th { background: #f6f5f1; } img { max-width: 100%; }"
        "</style></head><body>\n" + html + "\n</body></html>\n")
    print(f"written: {HERE / 'COMPARISON.md'}, {HERE / 'comparison.html'}")


def full_reorder_sections(w, by, byf, plan, planf, finished, finf):
    S = {"single_task": (by, plan, finished), "full_reorder": (byf, planf, finf)}
    both = [s for s in plan if s in planf]
    fin2 = [s for s in both if all(by[s][c]["done"] and byf[s][c]["done"] for c in CONDS)]
    w("## The four conditions under each strategy (the planning scripts)")
    w("")
    w(f"The {len(both)} planning scripts run under both strategies; completion over the {len(fin2)} finished in all eight "
      "runs. Each column's condition is compared only with the same strategy's columns.")
    w("")
    head = ["measure"] + [f"{LONG[c]}, {st_}" for c in CONDS for st_ in S]
    rows = [["completion, mean (ticks)"] + [num(mean([S[st_][0][s][c]["completion"] for s in fin2])) for c in CONDS for st_ in S]]
    for key, label in (("viol", "violation ticks, total"), ("near_encounters", "ticks below min_separation, total"),
                       ("hold_ticks", "held ticks, total"), ("decisions", "decisions, total")):
        rows.append([label] + [sum(S[st_][0][s][c][key] for s in both) for c in CONDS for st_ in S])
    rows.append(["scripts with a violation tick"] + [sum(S[st_][0][s][c]["viol"] > 0 for s in both) for c in CONDS for st_ in S])
    w(table(head, rows))
    w("")
    w("## The three steps under full_reorder, paired per scenario")
    w("")
    w(f"Over the {len(planf)} planning scripts under `full_reorder` ({len(finf)} for completion); the same table under "
      "`single_task` is above. Negative is earlier or fewer.")
    w("")
    w(table(STEP_HEAD, step_rows(byf, planf, finf)))
    w("")
    w("## full_reorder against single_task, per condition")
    w("")
    w("Per script, the `full_reorder` run against the `single_task` run of the same condition. Negative is earlier or "
      "fewer under `full_reorder`.")
    w("")
    rr = []
    for c in CONDS:
        for key, label, sc in (("completion", "completion (ticks)", fin2), ("viol", "violation ticks", both),
                               ("near_encounters", "ticks below min_separation", both), ("hold_ticks", "held ticks", both)):
            ds = [byf[s][c][key] - by[s][c][key] for s in sc]
            word = ("earlier", "equal", "later") if key == "completion" else ("fewer", "equal", "more")
            rr.append([LONG[c], label, len(ds), three(ds, word), signed(mean(ds), 2),
                       f"{sum(by[s][c][key] for s in sc)} → {sum(byf[s][c][key] for s in sc)}"])
    w(table(["condition", "measure", "scripts", "per script: lower / equal / higher", "mean change",
             "total: single_task → full_reorder"], rr))
    w("")
    w("## Where recognition changes the robot's order of tasks")
    w("")
    w("The robot's executed order of tasks (its task per tick, consecutive repeats merged; a task left and taken up "
      "again appears twice) compared between conditions of one strategy. The intention-unaware robot plans against the "
      "observed motion only; a different order in an intention-aware run is a change that recognition (the admissions, "
      "or their absence) brought about.")
    w("")
    cmp_rows, lists = [], {}
    for st_, (b, sc, _) in S.items():
        for a, c in (("HU", "IU"), ("IU", "OFF"), ("OFF", "ON")):
            ch = [s for s in sc if order(b[s][a]) != order(b[s][c])]
            lists[(st_, a, c)] = ch
            cmp_rows.append([st_, f"{LONG[a]} → {LONG[c]}", len(sc), len(ch),
                             sum(order(b[s][a])[:1] != order(b[s][c])[:1] for s in sc)])
    w(table(["strategy", "conditions", "scripts", "scripts whose order differs", "of them the first task differs"], cmp_rows))
    w("")
    for st_, (b, sc, _) in S.items():
        for a, c in (("IU", "OFF"), ("OFF", "ON")):
            ch = lists[(st_, a, c)]
            if not ch:
                w(f"- {st_}, {LONG[a]} → {LONG[c]}: no script.")
                continue
            w(f"- {st_}, {LONG[a]} → {LONG[c]}:")
            for s in ch:
                w(f"  - {s} ({b[s][a]['layout']}): {', '.join(order(b[s][a]))} → {', '.join(order(b[s][c]))}; "
                  f"completion {b[s][a]['completion']} → {b[s][c]['completion']}, violation ticks {b[s][a]['viol']} → "
                  f"{b[s][c]['viol']}")
    w("")


def figure(data):
    FIG.mkdir(exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
    for ax, g in zip(axes, TAGS[:2]):
        ds = [adm(x[2], "gate") - adm(x[3], "gate") for x in data[g] if x[3] is not None and x[2]["hypothesis"]
              and adm(x[2], "gate") is not None and adm(x[3], "gate") is not None]
        ch = [d for d in ds if d != 0]
        if ch:
            ax.hist(ch, bins=range(min(ch) - 1, max(ch) + 2), color=BAR, edgecolor="white")
        ax.axvline(0, color=MUTED, lw=0.8, ls="--")
        ax.set_title(f"{g}: the gate's admission delay, copy (on, fact) − base (off)\n{len(ds)} stretches admitted in "
                     f"both, {len(ds) - len(ch)} unchanged (not drawn)", fontsize=8.5, loc="left", color=INK)
        ax.set_xlabel("change in ticks (negative is earlier)", fontsize=8)
        ax.set_ylabel("task stretches", fontsize=8)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIG / "tags.png", dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    main()
