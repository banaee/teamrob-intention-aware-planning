#!/usr/bin/env python3
"""
H. The five named cases of the T-D R and E entry, walked through with ticks under current scenario ids.
  H1 a walk to a target no hypothesis expects; H2 the longest stand in the fixtures (modelled: a wait_at; and the
  idle human with no task on the stack); H3 the wrong table (scenario_s06_06, scenario_s07_03: supplementary runs);
  H4 the finished work order (scenario_s01_01 prior on, exhausted at 141); H5 the first ticks after a boundary.
Per tick: the human's action/micro, the record's top task (raw), leader(confidence), lifecycle, the finding at
α = .01/.05/.10 and the members' S; the meta-planner's decisions on those ticks (post-build, and pre-build where the
case exists before the build).
"""
from tdlib import runs, parse, parse_rec, truth, finding_at, label, ALPHAS, LAG
import d_decisions

L = {"adequate": "A", "unresolved": "U", "unexplained": "X", "exhausted": "E"}


def sk(k):
    if k in (None, "none"):
        return "none"
    if k.startswith("deliver_item"):
        return k.split("=")[1].split(",")[0].rstrip(")")
    if k.startswith("coffee_break"):
        return "coffee"
    return k.split("=")[1].rstrip(")")


def tick(log, rec, t):
    ir = log["ir"].get(t)
    if ir is None:
        return f"  {t:3} (no [IR] line)"
    h = log["human"].get(t, ("-", "-"))
    tr = truth(log, rec, t, 0)
    return (f"  {t:3} {h[0]:8}/{h[1]:7} rec={sk(tr['key']) if tr['key'] else tr['cov'][:14]:14} "
            f"{sk(ir['ml'])}({ir['conf']:.3f}) {ir['lifecycle']:9} "
            f"{''.join(L[finding_at(ir, a)] for a in ALPHAS)} "
            + " ".join(f"{sk(k)}={v:.4f}" for k, v in sorted(ir["tails"].items())))


def decisions(log, lo, hi, tag):
    for d in log["decisions"]:
        if lo <= d["step"] <= hi:
            print(f"      {tag} [meta] step={d['step']} {d['trigger']} proj={d['proj']} (conf {d['conf_proj']}) "
                  f"winner={d['winner']} sel={d['selection']} hold={d['hold']}")
    for s, k, f in log["holds"]:
        if lo <= s <= hi:
            print(f"      {tag} [hold] step={s} {k} {f}")


def show(r, ticks, lo=None, hi=None, pre=True):
    log, rec = parse(r["post"]), parse_rec(r["rec"])
    for t in ticks:
        print(tick(log, rec, t))
    lo = min(ticks) if lo is None else lo
    hi = max(ticks) if hi is None else hi
    decisions(log, lo, hi, "POST")
    if pre and r["pre"].exists():
        decisions(parse(r["pre"]), lo, hi, "PRE ")


def get(name, supp=False, set_="tb1a_destination"):
    return next(x for x in runs(supp) if x["name"] == name and (supp or x["set"] == set_))


def main():
    print(__doc__)
    print("columns: t  human action/micro  rec=top task (raw)  leader(confidence) lifecycle  finding@.01/.05/.10  members(S)")

    print("\n## H1 a walk to a target no hypothesis expects")
    n = 0
    for r in runs():
        log = parse(r["post"])
        n += sum(1 for v in log["coverage"].values() if v != "covered")
    print(f"  none of the 48 runs has one: every script entry is COVERED ({n} entries are not), and no script has a "
          f"go_to / an exit walk. The nearest measured case is the wrong-table carry walk (H3): a walk to a table no live "
          f"hypothesis expects the item at.")

    print("\n## H2 the longest stand")
    print("  modelled: the coffee_break wait_at, PT60S -> 30 ticks (s_exp = 30) plus the acknowledgement tick; "
          "scenario_s05_01 prior on, arrival 23, stand 25-54:")
    show(get("env_layout_07_scenario_s05_01_on"), [22, 23, 24, 25, 26, 39, 40, 41, 53, 54, 55, 56])
    print("  no task on the stack (the idle human after the script): the longest is scenario_s03_01 prior off, the record's")
    print("  stack empty from 123 to the run's end (300): 178 ticks; leader the robot's own remaining items:")
    show(get("env_layout_03_scenario_s03_01_off"), [119, 120, 121, 122, 123, 124, 137, 138, 139, 145, 146, 200, 233, 234, 299], 119, 299)
    print("  prior on, the same idle stand with a foreseeable task left live: scenario_s04_01, ac_switch_0 alone from 327:")
    show(get("env_layout_05_scenario_s04_01_on"), [326, 327, 328, 329, 330, 343, 344, 345, 381], 326, 381)

    print("\n## H3 the wrong table (supplementary runs; BINDING_ABSENT, the item's hypothesis carries its designated table)")
    for name, ts in [("env_layout_08_scenario_s06_06_on", [0, 16, 17, 18, 19, 20, 36, 37, 39, 40, 46, 47, 100, 101, 102, 103, 104, 105]),
                     ("env_layout_09_scenario_s07_03_on", [0, 8, 9, 10, 11, 12, 30, 31, 32, 33, 38, 39, 92, 93, 94, 95, 96])]:
        r = get(name, supp=True)
        print(f"\n  {label(r)}:")
        show(r, ts, 0, max(ts))
        post, pre = parse(r["post"]), parse(r["pre"])
        from tdlib import robot_completion
        print(f"      completion world tick pre {robot_completion(pre)} post {robot_completion(post)}; "
              f"declared pre {pre['done']} post {post['done']}")
    for name in ("env_layout_08_scenario_s06_06_off", "env_layout_09_scenario_s07_03_off"):
        r = get(name, supp=True)
        post, pre = parse(r["post"]), parse(r["pre"])
        from tdlib import robot_completion
        print(f"  {label(r)}: completion world tick pre {robot_completion(pre)} post {robot_completion(post)}; "
              f"declared pre {pre['done']} post {post['done']} (ticks in B4 and C)")
    print("\n  decision differences against the pre-build logs (d_decisions.diff):")
    for r in runs(True):
        out, comp, ap, aq = d_decisions.diff(r)
        print(f"  {label(r)}: {len(out)} differing entries; admitted/decisions pre {ap[0]}/{ap[1]} post {aq[0]}/{aq[1]}")
        for x in out:
            print("  " + x.replace("\n", "\n  "))

    print("\n## H4 the finished work order: scenario_s01_01 prior on")
    show(get("env_layout_01_scenario_s01_01_on"), [138, 139, 140, 141, 142, 143, 144, 170, 171], 138, 171)

    print("\n## H5 the first ticks after a boundary (every boundary of the 48 reads U on its tick, A from the next: B6)")
    print("  scenario_s01_01 prior on, boundary 78 (one live hypothesis left):")
    show(get("env_layout_01_scenario_s01_01_on"), [76, 77, 78, 79, 80, 81], 76, 81)
    print("  scenario_s01_01 prior off, boundary 78 (three live):")
    show(get("env_layout_01_scenario_s01_01_off"), [76, 77, 78, 79, 80, 81], 76, 81)
    print("  scenario_s02_01 prior on, boundary 75 (item_2 placed; coffee, item_5, ac_switch_0 live):")
    show(get("env_layout_02_scenario_s02_01_on"), [74, 75, 76, 77, 78], 74, 78)


if __name__ == "__main__":
    main()
