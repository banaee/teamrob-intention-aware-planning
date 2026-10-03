#!/usr/bin/env python3
"""
E. Completion and reveal evidence, PRE (L-build: the IRB.2b logs) against POST (L-build). The "unknown" column of the
tick tables is 1.4's; the PRE logs have no `unknown` key and it reads 0.000.

REVEAL: the first tick of a human task's span at which its hypothesis is most_likely with confidence >= θ (0.75), the
span read from the record lag-corrected (the ticks t whose record at t + 2 has the task on top): the handback §3
definition. Per run, every reveal that is lost or later than before, with the human's completion ticks on the body
inside the span before the post-build reveal (an arrival: the last walking tick of a move_to; a grasp; a release;
the end of a wait), and whether one precedes it.

Then tick by tick: the coffee walk, the arrival at the machine and the stand in scenario_s05_01, scenario_s05_02 and
scenario_s02_01 (prior on), and scenario_s01_01's item_2 (prior off, reveal 114 against the grasp at 110; and prior
on for comparison): per tick the human's action/micro, P(true) and each live rival's P before and after (before: and
`unknown`), the post-build finding at α = 0.05 and the members' S.
"""
from tdlib import runs, parse, parse_rec, truth, human_events, finding_at, ir_groups, label, THETA, LAG

L = {"adequate": "A", "unresolved": "U", "unexplained": "X", "exhausted": "E"}


def spans(log, rec):
    """task key -> (first, last) tick of its lag-corrected span, for COVERED tasks, in order."""
    out = {}
    for t in sorted(log["ir"]):
        k = truth(log, rec, t, LAG)["key"]
        if k is None:
            continue
        a, b = out.get(k, (t, t))
        out[k] = (min(a, t), max(b, t))
    return out


def reveal(log, key, span):
    for t in range(span[0], span[1] + 1):
        ir = log["ir"].get(t)
        if ir and ir["ml"] == key and ir["conf"] >= THETA:
            return t
    return None


def sk(k):
    if k.startswith("deliver_item"):
        return k.split("=")[1].rstrip(")")
    if k.startswith("coffee_break"):
        return "coffee"
    if k.startswith("ac_activation"):
        return k.split("=")[1].rstrip(")")
    return k


def main():
    print(__doc__)
    print("## reveals lost or later than before (all 48 runs; runs with identical IR streams on both sides printed once)")
    seen = set()
    for prior in ("on", "off"):
        print(f"\n# prior {prior}")
        for r in runs():
            if r["prior"] != prior:
                continue
            post, pre = parse(r["post"]), parse(r["pre"])
            rec, prerec = parse_rec(r["rec"]), parse_rec(r["prerec"])
            sp, spp = spans(post, rec), spans(pre, prerec)
            ev = human_events(post)
            rows = []
            for k, s in sp.items():
                a = reveal(pre, k, spp.get(k, s))
                b = reveal(post, k, s)
                if a is not None and (b is None or b > a):
                    # the task's own body events (the raw record has it on top), up to the post-build reveal
                    own = [(t, e) for t, e in ev if truth(post, rec, t, 0)["key"] == k
                           and s[0] <= t <= (b if b is not None else s[1])]
                    kinds = {e for t, e in own if b is None or t < b}
                    rows.append(f"  {sk(k):12} span {s[0]}-{s[1]}: reveal {a} -> {b if b is not None else 'none'}; "
                                f"the task's body events before it: {' '.join(f'{e}@{t}' for t, e in own) or '-'}; "
                                f"a completion tick precedes: {'yes: ' + ','.join(sorted(kinds)) if kinds else 'no'}")
                elif a is None and b is not None:
                    rows.append(f"  {sk(k):12} span {s[0]}-{s[1]}: reveal none -> {b} (gained)")
                elif a is not None and b is not None and b < a:
                    rows.append(f"  {sk(k):12} span {s[0]}-{s[1]}: reveal {a} -> {b} (earlier)")
            sig = (r["scenario"], r["prior"], "\n".join(rows))
            if sig in seen:
                continue
            seen.add(sig)
            print(f"\n{label(r)} ({r['set']})")
            for x in rows:
                print(x)

    for name, key in [("env_layout_07_scenario_s05_01_on", "coffee_break(?coffee_machine=coffee_machine_0)"),
                      ("env_layout_07_scenario_s05_02_on", "coffee_break(?coffee_machine=coffee_machine_0)"),
                      ("env_layout_02_scenario_s02_01_on", "coffee_break(?coffee_machine=coffee_machine_0)"),
                      ("env_layout_01_scenario_s01_01_off", "deliver_item(?item=item_2)"),
                      ("env_layout_01_scenario_s01_01_on", "deliver_item(?item=item_2)")]:
        r = next(x for x in runs() if x["name"] == name and x["set"] == "tb1a_destination")
        post, pre = parse(r["post"]), parse(r["pre"])
        rec = parse_rec(r["rec"])
        s = spans(post, rec)[key]
        print(f"\n## {label(r)}: {sk(key)}, lag-corrected span {s[0]}-{s[1]}; reveal pre "
              f"{reveal(pre, key, s)} post {reveal(post, key, s)}")
        print("   t  human           | PRE  P(true) unknown  rivals                         | POST P(true) rivals"
              "                          finding members(S)")
        for t in range(s[0], s[1] + 1):
            h = post["human"].get(t, ("-", "-"))
            dq, dp = pre["dist"][t], post["dist"][t]
            live_pre = {k: v for k, v in dq.items() if v > 0.001 and k not in (key, "unknown")}
            live_post = {k: v for k, v in dp.items() if v > 0.001 and k != key}
            ir = post["ir"][t]
            f = L[finding_at(ir, 0.05)]
            print(f"  {t:3} {h[0]:8}/{h[1]:7}| {dq.get(key, 0):.3f} {dq.get('unknown', 0):.3f}  "
                  f"{' '.join(f'{sk(k)}={v:.3f}' for k, v in sorted(live_pre.items())):30} | {dp.get(key, 0):.3f} "
                  f"{' '.join(f'{sk(k)}={v:.3f}' for k, v in sorted(live_post.items())):30} {f} "
                  f"{' '.join(f'{sk(k)}={v:.4f}' for k, v in sorted(ir['tails'].items()))}")


if __name__ == "__main__":
    main()
