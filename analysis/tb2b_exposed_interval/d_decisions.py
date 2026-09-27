#!/usr/bin/env python3
"""
D. Decisions against the pre-build baseline (cycle 1.5b: the 1.3b logs, 7f4559a), prior on primary, prior off after.

Per run, one line per tick on which the decision differs: a [meta] decision present on one side only, or present on
both with a different trigger, admission ([meta-proj] projection=, the meta-planner's reason string), winner,
B3 selection, hold or ordering; and every [hold] start that differs. Each line carries, at that tick, the post-build
recognizer state (leader, confidence, finding at α = 0.05, the leader's hypothesis adequacy, lifecycle) and the
pre-build one (leader, confidence, finding; 1.5b adapts the two state strings to the logs' fields, the logic is 1.4's). Runs with identical decision streams on both sides are printed once. Then the completion ticks:
the world tick (T6: the tick after the robot's last release) and the declared empty-pool tick, before and after.
"""
from tdlib import runs, parse, robot_completion, label

L = {"adequate": "A", "unresolved": "U", "unexplained": "X", None: "-"}


def dsig(d):
    return (d["trigger"], d["proj"], d["winner"], d["selection"], d["hold"], d["ordering"])


def dstr(d):
    if d is None:
        return "-"
    s = f"{d['trigger']} proj={d['proj']} win={d['winner']}"
    if d["selection"]:
        s += f" sel={d['selection']} hold={d['hold']}"
    if d["ordering"]:
        s += f" ord={d['ordering']}"
    return s


def irpost(log, t):
    ir = log["ir"].get(t)
    if ir is None:
        return "IR -"
    return f"post {ir['ml']}({ir['conf']:.3f}) {L.get(ir['finding'], ir['finding'])} lead={ir['lead']} {ir['lifecycle']}"


def irpre(log, t):
    ir = log["ir"].get(t)
    if ir is None:
        return "pre -"
    return f"pre {ir['ml']}({ir['conf']:.3f}) {L.get(ir['finding'], ir['finding'])}"


def diff(r):
    post, pre = parse(r["post"]), parse(r["pre"])
    out = []
    dp = {}
    for d in post["decisions"]:
        dp.setdefault(d["step"], []).append(d)
    dq = {}
    for d in pre["decisions"]:
        dq.setdefault(d["step"], []).append(d)
    for t in sorted(set(dp) | set(dq)):
        a, b = dq.get(t, []), dp.get(t, [])
        for i in range(max(len(a), len(b))):
            x = a[i] if i < len(a) else None
            y = b[i] if i < len(b) else None
            if x is None or y is None or dsig(x) != dsig(y):
                out.append(f"  t={t:3} PRE {dstr(x)}\n        POST {dstr(y)}\n        {irpost(post, t)} | {irpre(pre, t)}")
    hp = {(s, f.get("planned")) for s, k, f in post["holds"] if k == "start"}
    hq = {(s, f.get("planned")) for s, k, f in pre["holds"] if k == "start"}
    for s, p in sorted(hp - hq):
        out.append(f"  t={s:3} hold start planned={p} POST only | {irpost(post, s)}")
    for s, p in sorted(hq - hp):
        out.append(f"  t={s:3} hold start planned={p} PRE only | {irpre(pre, s)}")
    comp = (robot_completion(pre), robot_completion(post), pre["done"], post["done"])
    admits = lambda lg: (sum(d["proj"] == "built" for d in lg["decisions"]), len(lg["decisions"]))
    return out, comp, admits(pre), admits(post)


def main():
    print(__doc__)
    table = []
    for prior in ("on", "off"):
        print(f"\n# prior {prior}" + (" (primary)" if prior == "on" else " (appendix)"))
        seen = {}
        for r in runs():
            if r["prior"] != prior:
                continue
            out, comp, ap, aq = diff(r)
            sig = ("\n".join(out), comp)
            table.append((r, comp, ap, aq, len(out)))
            if sig in seen:
                print(f"\n## {r['set']}/{r['name']}: identical to {seen[sig]}")
                continue
            seen[sig] = f"{r['set']}/{r['name']}"
            print(f"\n## {r['set']}/{r['name']}: {len(out)} differing entries; admissions built/decisions pre {ap[0]}/{ap[1]} "
                  f"post {aq[0]}/{aq[1]}; completion world pre {comp[0]} post {comp[1]}, declared pre {comp[2]} post {comp[3]}")
            for x in out:
                print(x)
    print("\n# completion ticks (world tick T6 / declared), before -> after")
    print(f"{'run':62} {'world':>13} {'declared':>13} {'admitted pre':>12} {'post':>6} {'diffs':>5}")
    for r, c, ap, aq, n in table:
        w = f"{c[0]}->{c[1]}"
        dcl = f"{c[2]}->{c[3]}"
        print(f"{r['set'] + '/' + r['name']:62} {w:>13} {dcl:>13} {ap[0]:>7}/{ap[1]:<4} {aq[0]:>3}/{aq[1]:<3} {n:5}")


def extras():
    """The minimum robot-human separation over the run ([sep] min), before and after; the post-only holds with the
    lone-hypothesis state at their tick (a live set of one, prior off: the robot's own remaining item)."""
    import re
    print("\n# minimum separation ([sep] min over the run, cm), before -> after; post-only holds with the admitted belief")
    for r in runs():
        seps = []
        for p in (r["pre"], r["post"]):
            m = [float(x) for x in re.findall(r"^\[sep\] step=\d+ \S+ dist=\S+ min=(\S+)", open(p).read(), re.M)]
            seps.append(min(m) if m else None)
        post = parse(r["post"])
        pre = parse(r["pre"])
        hq = {(s, f.get("planned")) for s, k, f in pre["holds"] if k == "start"}
        new = [(s, f.get("planned")) for s, k, f in post["holds"] if k == "start" and (s, f.get("planned")) not in hq]
        hs = "; ".join(f"hold {pl} at {s}: {post['ir'][s]['ml']}({post['ir'][s]['conf']:.3f}) "
                       f"{post['ir'][s]['finding']}, keys above the floor {sum(1 for v in post['dist'][s].values() if v > 0.001)}"
                       for s, pl in new)
        print(f"{r['set'] + '/' + r['name']:62} {seps[0]:7.2f} -> {seps[1]:7.2f}  {hs}")


if __name__ == "__main__":
    import sys
    extras() if sys.argv[1:] == ["extras"] else main()
