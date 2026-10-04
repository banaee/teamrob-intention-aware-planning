#!/usr/bin/env python3
"""
whatif.py — two what-if readings on T-K part 1's recorded gate answers (Hadi, 4 October 2026), and the ratios behind
docs/assumptions.md 6.4. Filters on recorded answers, not runs: a changed admission would change later ticks (the
decisions, the projection, a planning robot's path), which a filter cannot show. Nothing is run or recomputed by the
framework; the pairs and readings are comparison.py's.

    whatif.py            run from the repository root; prints markdown (WHATIF.md's tables)

The filters, applied on each tick to the recorded answer with context knowledge on (the gate clears, leader h):
- X: h is admissible only if the evidence alone (the off run of the same script, the equal prior) ranks no other live
  hypothesis strictly above it (by more than 1e-9, the instruments' agreement level);
- Y: h is admissible only with observation warrant on the tick (commitment warrant alone does not admit);
- X and Y together.
"""
import csv
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import comparison as C          # sets the paths; its main() runs only as a script

A, G, S = C.A, C.G, C.S
TIE = 1e-9
FILTERS = ("X", "Y", "X and Y")


def x_ok(off, t, h):
    if t not in off.hyp or h not in off.hyp[t]:
        return False
    mine = off.hyp[t][h]["b"]
    return all(v["b"] <= mine + TIE for k, v in off.hyp[t].items() if k != h)


def y_ok(on, t, h):
    return on.hyp.get(t, {}).get(h, {}).get("warrant") == "observation"


def passes(f, on, off, t, h):
    return {"X": lambda: x_ok(off, t, h), "Y": lambda: y_ok(on, t, h),
            "X and Y": lambda: x_ok(off, t, h) and y_ok(on, t, h)}[f]()


def admits(f, on, off, t, h):
    """The filtered answer on tick t for h: the recorded gate clears for h, and the filter lets it."""
    return on.clears_for(t, h) and (f is None or passes(f, on, off, t, h))


def runs(ticks):
    out = []
    for t in ticks:
        if out and out[-1][1] == t - 1:
            out[-1][1] = t
        else:
            out.append([t, t])
    return ", ".join(f"{a}" if a == b else f"{a}-{b}" for a, b in out) or "none"


def pairs():
    out = []
    for step, d, o in C.rec_pairs():
        on, off = G.Run(d), G.Run(o)
        out.append((step, d, o, on, off))
    return out


# ---- 6.4: the ratios ------------------------------------------------------------------------------------------------

def ratios(P):
    """Over the admissions of a hypothesis that is not the true task during modelled tasks (comparison.py's main rows)
    with a true hypothesis: per tick, the evidence ratio true / admitted in the off run."""
    per_tick, rows = [], []
    for step, d, o, on, off in P:
        lv = C.levels(d)
        for r in C.wrong_rows(d, lv):
            if r["kind"] != "main":
                continue
            h, rs, trues = r["h"], [], set()
            for t in range(r["a"], r["b"] + 1):
                k = on.truth.get(t)
                if k is None or t not in off.hyp or k not in off.hyp[t] or h not in off.hyp[t]:
                    continue
                trues.add(G.short(k))
                bk, bh = off.hyp[t][k]["b"], off.hyp[t][h]["b"]
                first = all(bk > v["b"] + TIE for kk, v in off.hyp[t].items() if kk != k)
                rs.append((t, bk / bh if bh > 0 else float("inf"), abs(bk - bh) <= TIE, first))
            if rs:
                per_tick += rs
                rows.append((step, d.name, r, rs, ", ".join(sorted(trues))))
    tie = [x for x in per_tick if x[2]]
    above = [x for x in per_tick if not x[2] and x[1] > 1 and x[3]]
    above3 = [x for x in per_tick if not x[2] and x[1] > 1 and not x[3]]
    below = [x for x in per_tick if not x[2] and x[1] < 1]
    q = lambda xs: (f"min ×{min(xs):.4f}, quartiles ×{statistics.quantiles(xs, n=4)[0]:.4f} / "
                    f"×{statistics.median(xs):.4f} / ×{statistics.quantiles(xs, n=4)[2]:.4f}, max ×{max(xs):.4f}") if len(xs) > 1 else "-"
    print(f"Wrong ticks with a true hypothesis: {len(per_tick)} (in {len(rows)} admissions).\n")
    print("| the evidence alone on the tick (the off run) | ticks | the ratio true / admitted |")
    print("|---|---|---|")
    print(f"| a tie (equal within 1e-9) | {len(tie)} | ×1 |")
    print(f"| the true task first | {len(above)} | {q([x[1] for x in above])} |")
    print(f"| the true task above the admitted one, a third hypothesis first | {len(above3)} | {q([x[1] for x in above3])} |")
    print(f"| the admitted one above the true task | {len(below)} | {q([x[1] for x in below])} |")
    print("\nPer admission whose ticks end with the true task first: the ratio on its first and its last wrong tick.\n")
    print("| step | scenario | admitted | wrong ticks | true task | ratio, first wrong tick | ratio, last wrong tick | ties |")
    print("|---|---|---|---|---|---|---|---|")
    for step, s, r, rs, true in rows:
        if not (rs[-1][1] > 1 and rs[-1][3]):
            continue
        print(f"| {step} | {s.removeprefix('scenario_')} | {G.short(r['h'])} | {r['a']}-{r['b']} ({r['gate']}) | {true} | "
              f"×{rs[0][1]:.4f} | ×{rs[-1][1]:.4f} | {sum(x[2] for x in rs)} |")


# ---- the lone assigned task admitted before the human starts it ----------------------------------------------------

def concentration(P):
    """How much of the true task's earlier admission, and of the wrong gate ticks, comes from a lone assigned task
    admitted before the human starts it (comparison.py's lone_early)."""
    lone_gain = other_gain = 0
    for step, d, o, on, off in P:
        _, _, st_on = A.stretches(d, C.NAME, C.THETA)
        _, _, st_off = A.stretches(o, C.NAME, C.THETA)
        st_off = {(r["key"], r["a"]): r for r in st_off}
        for r in st_on:
            f = st_off[(r["key"], r["a"])]
            if r["adm"] is None or f["adm"] is None or r["adm"] >= f["adm"]:
                continue
            a0 = r["adm"]
            while on.clears_for(a0 - 1, r["key"]):
                a0 -= 1
            lone = (a0 < r["a"] and r["key"].startswith("deliver_item")
                    and sum(1 for k in on.hyp.get(a0, {}) if k.startswith("deliver_item")) == 1)
            if lone:
                lone_gain += f["adm"] - r["adm"]
            else:
                other_gain += f["adm"] - r["adm"]
    wrong_lone = wrong_all = 0
    for step, d, o, on, off in P:
        early = {(x["a"]) for x in C.lone_early(d) if x["how"] == "retracted"}
        for r in C.wrong_rows(d, C.levels(d)):
            if r["kind"] != "main":
                continue
            wrong_all += r["gate"]
            if r["a"] in early or (r["a"] - 1) in early:
                wrong_lone += r["gate"]
    print(f"- the true task's admission earlier than off, ticks gained in total: {lone_gain + other_gain}; of them by a lone "
          f"assigned task admitted on the previous task's completion tick: {lone_gain}")
    print(f"- wrong gate ticks during modelled tasks: {wrong_all}; of them a lone assigned task admitted before the human "
          f"starts it and retracted: {wrong_lone}")


# ---- 2: the filters -------------------------------------------------------------------------------------------------

def earlier(P):
    """The admissions of the true task that are earlier on than off: their tick under each filter."""
    cases = []
    for step, d, o, on, off in P:
        _, _, st_on = A.stretches(d, C.NAME, C.THETA)
        _, _, st_off = A.stretches(o, C.NAME, C.THETA)
        st_off = {(r["key"], r["a"]): r for r in st_off}
        lv = C.levels(d)
        for r in st_on:
            f = st_off[(r["key"], r["a"])]
            if r["adm"] is None or (f["adm"] is not None and r["adm"] >= f["adm"]):
                continue
            k = r["key"]
            a0 = r["adm"]
            while on.clears_for(a0 - 1, k):
                a0 -= 1
            name = k.split("(")[0]
            if name == "deliver_item":
                lone = a0 < r["a"] and sum(1 for x in on.hyp.get(a0, {}) if x.startswith("deliver_item")) == 1
                cat = "a lone assigned task admitted before the human starts it" if lone else "assigned delivery"
            else:
                own = lv.get(r["a"], {}).get(name, "ordinary")
                cat = "foreseeable task, its raising fact holding" if own == "raised" else "foreseeable task, no raising fact"
            res = {}
            for fl in FILTERS:
                t = next((u for u in range(a0, r["b"] + 1) if admits(fl, on, off, u, k)), None)
                res[fl] = t
            cases.append(dict(cat=cat, a0=a0, off=f["adm"], res=res))
    cats = ["assigned delivery", "a lone assigned task admitted before the human starts it",
            "foreseeable task, its raising fact holding", "foreseeable task, no raising fact"]
    print("| filter | category | earlier on than off | keep their tick | delayed: count | delay in ticks (median, range) | "
          "still earlier than off | never admitted in the stretch |")
    print("|---|---|---|---|---|---|---|---|")
    for fl in FILTERS:
        for cat in cats:
            xs = [c for c in cases if c["cat"] == cat]
            if not xs:
                continue
            keep = sum(c["res"][fl] == c["a0"] for c in xs)
            dl = [c["res"][fl] - c["a0"] for c in xs if c["res"][fl] is not None and c["res"][fl] > c["a0"]]
            never = sum(c["res"][fl] is None for c in xs)
            still = sum(c["res"][fl] is not None and (c["off"] is None or c["res"][fl] < c["off"]) for c in xs)
            print(f"| {fl} | {cat} | {len(xs)} | {keep} | {len(dl)} | {C.stats(dl)} | {still} | {never} |")


def row_kind(on, off, r):
    cls = {"(i)": 0, "(ii)": 0, "(iii)": 0}
    h = r["h"]
    for t in range(r["a"], r["b"] + 1):
        k = on.truth.get(t)
        if k is None or t not in off.hyp or k not in off.hyp[t] or h not in off.hyp[t]:
            continue
        bk, bh = off.hyp[t][k]["b"], off.hyp[t][h]["b"]
        ratio = bk / bh if bh > 0 else float("inf")
        first = all(bk > v["b"] for kk, v in off.hyp[t].items() if kk != k)
        c = "(i)" if 1 / C.NEAR <= ratio <= C.NEAR else ("(ii)" if first else "(iv)") if ratio > C.NEAR else "(iii)"
        if c in cls:
            cls[c] += 1
    if not any(cls.values()):
        return "no true hypothesis"
    return max(("(i)", "(ii)", "(iii)"), key=lambda c: (cls[c], -["(i)", "(ii)", "(iii)"].index(c)))


def wrong(P):
    rows = []
    for step, d, o, on, off in P:
        for r in C.wrong_rows(d, C.levels(d)):
            kind = row_kind(on, off, r) if r["kind"] == "main" else {"exit": "the exit walk", "pin": "pin tick"}[r["kind"]]
            rem = {fl: [t for t in range(r["a"], r["b"] + 1) if admits(fl, on, off, t, r["h"])] for fl in FILTERS}
            rows.append(dict(step=step, s=d.name.removeprefix("scenario_"), r=r, kind=kind, rem=rem))
    kinds = ["(ii)", "(iii)", "no true hypothesis", "the exit walk", "pin tick"]
    print("| filter | kind (COMPARISON.md) | admissions | gate ticks | disappear | remain | ticks remaining |")
    print("|---|---|---|---|---|---|---|")
    for fl in FILTERS:
        for kd in kinds:
            xs = [x for x in rows if x["kind"] == kd]
            if not xs:
                continue
            gone = sum(not x["rem"][fl] for x in xs)
            print(f"| {fl} | {kd} | {len(xs)} | {sum(x['r']['gate'] for x in xs)} | {gone} | {len(xs) - gone} | "
                  f"{sum(len(x['rem'][fl]) for x in xs)} |")
    print("\nEvery admission of a hypothesis that is not the true task during modelled tasks, the ticks remaining under "
          "each filter:\n")
    print("| step | scenario | admitted | wrong ticks (gate) | kind | X | Y | X and Y |")
    print("|---|---|---|---|---|---|---|---|")
    for x in rows:
        if x["kind"] in ("the exit walk", "pin tick"):
            continue
        r = x["r"]
        print(f"| {x['step']} | {x['s']} | {G.short(r['h'])} | {r['a']}-{r['b']} ({r['gate']}) | {x['kind']} | "
              + " | ".join(runs(x["rem"][fl]) for fl in FILTERS) + " |")


def planning():
    """The two planning cases caused by a wrong admission: the filters on the ticks before the robot's pass, from the
    MPB's per-tick tables (belief_h, observation_warrant), off run as the evidence."""
    cases = [("step 5", "scenario_s16_05", C.MPB / "tk/scenario_s16_05", C.MPB / "tk/off/scenario_s16_05", 22),
             ("step 5b", "scenario_s11_03", C.MPB / "tk5b/scenario_s11_03", C.MPB / "scenario_s11_03", 11)]
    print("| step | scenario | the pass from | ticks before it on which the recorded gate clears (leader) | X refuses | "
          "Y refuses | X and Y refuse | the decision ticks before the pass: recorded, X, Y |")
    print("|---|---|---|---|---|---|---|---|")
    for step, sid, on_d, off_d, p in cases:
        on = {r["tick"]: r for r in json.load(open(on_d / "on_single_task/actual_ticks.json"))}
        off = {r["tick"]: r for r in json.load(open(off_d / "on_single_task/actual_ticks.json"))}
        dec = [d.tick for d in C.load_decisions(on_d / "on_single_task/actual_decisions.json") if d.tick < p]
        clears = [t for t in range(0, p) if on[t]["gate"] == "clears"]
        lead = {on[t]["leader"] for t in clears}

        def xok(t):
            h, b = on[t]["leader"], off[t]["belief_h"]
            return h in b and all(v <= b[h] + TIE for k, v in b.items() if k != h)

        def yok(t):
            return on[t]["observation_warrant"].get(on[t]["leader"]) == "observation"
        rx = [t for t in clears if not xok(t)]
        ry = [t for t in clears if not yok(t)]
        rxy = [t for t in clears if not (xok(t) and yok(t))]
        decs = "; ".join(f"{t}: {'clears' if t in clears else on[t]['gate']}, X {'refuses' if t in rx else 'lets'}, "
                         f"Y {'refuses' if t in ry else 'lets'}" for t in dec)
        print(f"| {step} | {sid} | {p} | {runs(clears)} ({', '.join(G.short(h) for h in sorted(lead))}) | {runs(rx)} | "
              f"{runs(ry)} | {runs(rxy)} | {decs} |")
        h = sorted(lead)[0] if lead else None
        if h:
            b0 = off[0]["belief_h"]
            print(f"|  |  |  | off evidence at 0: " + ", ".join(f"{G.short(k)} {v:.4f}" for k, v in sorted(b0.items(), key=lambda kv: -kv[1]))
                  + f"; at {p - 1}: " + ", ".join(f"{G.short(k)} {v:.4f}" for k, v in sorted(off[p - 1]["belief_h"].items(), key=lambda kv: -kv[1]))
                  + " |  |  |  |  |")


def flicker(P):
    """Per true stretch, the number of changes of the answer from tick to tick inside the stretch, the answer being the
    hypothesis the gate admits on the tick (recorded, or filtered) or none; a stretch with 3 or more changes admits,
    drops and admits again (or changes its admitted hypothesis twice)."""
    out = {None: [], **{fl: [] for fl in FILTERS}}
    for step, d, o, on, off in P:
        _, _, st = A.stretches(d, C.NAME, C.THETA)
        for r in st:
            for fl in out:
                vals = []
                for t in range(r["a"], r["b"] + 1):
                    h = on.tick.get(t, {}).get("leader")
                    vals.append(h if h and admits(fl, on, off, t, h) else None)
                out[fl].append(sum(1 for a, b in zip(vals, vals[1:]) if a != b))
    print("| answer | true stretches | changes in total | stretches with 3 or more changes | most changes in one stretch |")
    print("|---|---|---|---|---|")
    for fl, xs in out.items():
        print(f"| {'recorded (on)' if fl is None else fl} | {len(xs)} | {sum(xs)} | {sum(x >= 3 for x in xs)} | {max(xs)} |")


def main():
    C.S.SCHEMAS.update({s.name: s for s in C.importlib.import_module("domains.kitting.registry").domain_config["task_model"]})
    P = pairs()
    print("## The ratios behind docs/assumptions.md 6.4\n")
    ratios(P)
    print("\n## What the lone assigned task admitted before the human starts it carries\n")
    concentration(P)
    print("\n## X and Y: the true task's earlier admissions\n")
    earlier(P)
    print("\n## X and Y: the admissions of a hypothesis that is not the true task\n")
    wrong(P)
    print("\n## X and Y: the two planning cases caused by a wrong admission\n")
    planning()
    print("\n## X and Y: flicker\n")
    flicker(P)


if __name__ == "__main__":
    main()
