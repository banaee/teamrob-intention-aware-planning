#!/usr/bin/env python3
"""
baseline_diff.py — what the L-build regeneration changed, per log (the 48 maintained runs and the 4 supplementary):
the .rec stream PRE against POST, and per grep family the first differing line's step and the count of differing
lines (a line-wise comparison of the family's lines in order). No criterion of identity: L changes behaviour; this is
the drift listing CLAUDE.md asks for (condition, first differing step, grep), and the families outside the recognizer
and the trigger say whether the robot's behaviour moved.

Both sides are compared after `normalise` (the two format changes undone); the `[meta-trig]` causes are counted
separately.
Families: [IR] [IR-dist] [IR-complete] [IR-boundary] [IR-reentry] (new) [meta-trig] [meta-proj] [meta] [meta-b3]
[hold] [sep], the robot's and the human's per-tick lines, and every other line.
Run from this directory: ~/python-envs/ir-nomesa-env/bin/python baseline_diff.py > baseline_diff.txt
"""
import re
import tdlib

FAMILIES = ["[IR] ", "[IR-dist]", "[IR-complete]", "[IR-boundary]", "[IR-reentry]", "[meta-trig]", "[meta-proj]",
            "[meta] ", "[meta-b3]", "[hold]", "[sep]"]
STEP = re.compile(r"step[=:] ?(\d+)")


def family(l):
    for f in FAMILIES:
        if l.startswith(f):
            return f.strip()
    if re.match(r"\s*step: \d+: \[robot_", l):
        return "robot"
    if re.match(r"\s*step: \d+: \[human_", l):
        return "human"
    return "other"


def normalise(l):
    """The two format changes of L-build, undone so that a remaining difference is behaviour: the [meta-trig] line's
    ` cause=` suffix, and the [IR-boundary] line's named action (`completed <action>:` for `completed a task:`)."""
    l = re.sub(r" cause=\S+$", "", l) if l.startswith("[meta-trig]") else l
    return re.sub(r" completed \S+?: belief", " completed a task: belief", l) if l.startswith("[IR-boundary]") else l


def lines(path):
    out = {}
    for l in open(path, errors="replace"):
        l = normalise(l.rstrip("\n"))
        if l.startswith("[run_mesa]") or l.startswith("[run]") and "log=" in l:
            continue
        out.setdefault(family(l), []).append(l)
    return out


def first_diff(a, b):
    n = sum(x != y for x, y in zip(a, b)) + abs(len(a) - len(b))
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            m = STEP.search(x) or STEP.search(y)
            return n, (m[1] if m else f"line {i}")
    if len(a) != len(b):
        extra = (a if len(a) > len(b) else b)[min(len(a), len(b))]
        m = STEP.search(extra)
        return n, (m[1] if m else "end")
    return 0, None


def main():
    rs = tdlib.runs() + tdlib.runs(supp=True)
    keys = [f.strip() for f in FAMILIES] + ["robot", "human", "other"]
    print("Per log: rec = the .rec stream PRE vs POST; then per family with a difference: family first-step (lines)."
          "\n")
    moved_robot = []
    for r in rs:
        rec = open(r["rec"], "rb").read() == open(r["prerec"], "rb").read()
        a, b = lines(r["pre"]), lines(r["post"])
        cells = []
        for k in keys:
            n, s = first_diff(a.get(k, []), b.get(k, []))
            if n:
                cells.append(f"{k} {s} ({n})")
        if any(c.split()[0] in ("robot", "[meta]", "[hold]", "[sep]") for c in cells):
            moved_robot.append(r)
        print(f"{r['set']:20} {r['name']:52} rec {'=' if rec else 'DIFF'}  " + ("; ".join(cells) or "identical"))
    print(f"\nRuns whose robot lines, [meta], [hold] or [sep] moved: {len(moved_robot)} of {len(rs)}")
    for r in moved_robot:
        print(f"  {r['set']} {r['name']}")


if __name__ == "__main__":
    main()
