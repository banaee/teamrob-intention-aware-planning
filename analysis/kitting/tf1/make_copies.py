#!/usr/bin/env python3
"""
make_copies.py — part 1 of the last step of T-F part 1 (Hadi, 5 October 2026): context knowledge with a fact in force.
The copies of the measurement's scenarios with a timeline of their own, their class, and the copies still missing.

    make_copies.py            prints the plan: per base scenario its copies by class and the copies to author
    make_copies.py --write    authors the missing copies (new scenario literals appended to their setup's module,
                              each a copy of its base's literal text with its own id, description and timeline) and
                              their run files (configs/kitting/tf1/measurement/<scenario>/run_NNN.yaml, from run_689,
                              intention-aware with context knowledge on)

`classes()` is read by comparison.py: every copy of a measurement scenario with its base, class, fact and window.

The classes (the rule, written down before the runs; REPORT.md, "Part 1: context knowledge with a fact in force"):
- in accord: the fact holds over the ticks in which the human performs the foreseeable task the fact raises
  (coffee_break: break_time; ac_activation: room_warm);
- not in accord: the fact holds while the human performs another task, or the human never performs the foreseeable
  task;
- whole run: step 5's three copies (scenario_s16_02, _04, _06), whose fact holds from tick 0 to the run's end, over
  the foreseeable task and other tasks alike; reported apart, in neither class.
The existing copies are step 5e's (analysis/kitting/tk5e/README.md, "The scripts": accord is in accord; through and
through_rw are not in accord). A base gets a new copy in a class when its room has a foreseeable task (a coffee
machine or an A/C switch) and it has no copy in that class, in accord only when its human performs a foreseeable task.
The windows of a new copy, from the base's replay (its run's trajectory.json; half-open, in ticks):
- in accord: one window per stretch in which a foreseeable task is the top of the human's stack, [its first tick, the
  tick after its last), with that task's fact;
- not in accord: the fact of the first foreseeable task the human performs (break_time when it performs none and the
  room has a coffee machine, else room_warm), over the first stretch in which a task that is not foreseeable is the top
  of the human's stack.
"""
import csv
import glob
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
M = ROOT / "analysis" / "kitting" / "tf1" / "measurement"
CFG = ROOT / "configs" / "kitting" / "tf1" / "measurement"
SCEN = ROOT / "domains" / "kitting" / "scenarios"
FACT = {"coffee_break": "break_time", "ac_activation": "room_warm"}
CONST = {"break_time": "BREAK_TIME", "room_warm": "ROOM_WARM"}
WHOLE = {"scenario_s16_02": "scenario_s16_01", "scenario_s16_04": "scenario_s16_03", "scenario_s16_06": "scenario_s16_05"}
MARK = "T-F part 1, part 1b: "
FIRST = 689                                             # the measurement's run files end at run_688


def bases():
    rows = list(csv.DictReader(open(M / "results.csv")))
    return sorted({r["scenario"] for r in rows if int(r["run"][4:]) <= 512} - set(WHOLE))


def trajectory(scenario):
    return json.load(open(sorted(glob.glob(str(M / scenario / "run_*" / "trajectory.json")))[0]))


def stretches(t):
    """(task, first tick, tick after the last) per stretch of one top-of-stack task in the replay."""
    out = []
    for a in t["actions"]:
        if out and out[-1][0] == a["task"]:
            continue
        if out:
            out[-1][2] = a["tick"]
        out.append([a["task"], a["tick"], None])
    if out:
        out[-1][2] = t["last_ack"] + 1
    return [tuple(s) for s in out]


def kind(task):
    return task.split("(")[0]


def room_kinds(layout):
    objs = json.load(open(ROOT / "domains" / "kitting" / "layouts" / f"{layout}.json"))["env_objects"]
    return {o["type"] for o in objs}


def tk5e():
    """Step 5e's copies: working form -> [(class, copy, setting)] from its README's table of scripts."""
    out = {}
    for l in open(ROOT / "analysis" / "kitting" / "tk5e" / "README.md"):
        m = re.match(r"\| (\d{3}) \| [^|]+\| (s\d+_\d+) \| (s\d+_\d+(?:, s\d+_\d+)*) \| ([^|]*)\|", l)
        if not m:
            continue
        works = ["scenario_" + w for w in m[3].split(", ")]
        for setting, ws in re.findall(r"(accord|through_rw|through) s\d+_\d+ / (s\d+_\d+(?:, s\d+_\d+)*)", m[4]):
            for work, w in zip(works, ws.split(", ")):
                out.setdefault(work, []).append(("in accord" if setting == "accord" else "not in accord",
                                                 "scenario_" + w, setting))
    return out


def classes():
    """Every copy of a measurement scenario: {copy: dict(base, cls, source)}; from step 5e's table, step 5's three
    whole-run copies and the copies this script authored (their description names base and class)."""
    out = {}
    for base, cs in tk5e().items():
        for cls, copy, setting in cs:
            out[copy] = dict(base=base, cls=cls, source=f"step 5e ({setting})")
    for copy, base in WHOLE.items():
        out[copy] = dict(base=base, cls="whole run", source="step 5")
    for f in sorted(SCEN.glob("scenarios_s*.py")):
        for m in re.finditer(r'id="(scenario_s\d+_\d+)",.*?description=\(\s*"' + re.escape(MARK)
                             + r'(scenario_s\d+_\d+)\'s copy with a fact in force, (in accord|not in accord)', f.read_text(),
                             re.S):
            out[m[1]] = dict(base=m[2], cls=m[3], source="part 1b")
    return out


def plan():
    have = {}
    for copy, c in classes().items():
        have.setdefault(c["base"], set()).add(c["cls"])
    todo = []
    for b in bases():
        t = trajectory(b)
        room = room_kinds(t["layout"])
        if not room & {"coffee_machine", "ac_switch"}:
            continue
        st = stretches(t)
        fore = [s for s in st if kind(s[0]) in FACT]
        if fore and "in accord" not in have.get(b, set()):
            todo.append((b, "in accord", [(FACT[kind(s[0])], s[1], s[2], s[0]) for s in fore]))
        if "not in accord" not in have.get(b, set()):
            fact = FACT[kind(fore[0][0])] if fore else ("break_time" if "coffee_machine" in room else "room_warm")
            other = next(s for s in st if kind(s[0]) not in FACT)
            todo.append((b, "not in accord", [(fact, other[1], other[2], other[0])]))
    return todo


def literal(src, base, new, cls, windows):
    """The base's literal text with the new id, description and timeline."""
    m = re.search(rf"^{base} = ScenarioConfig\(\n.*?^\)\n", src, re.M | re.S)
    lines = m[0].split("\n")
    out, skip = [], False
    short = lambda task: re.sub(r"\?\w+=", "", task)
    what = "; ".join(f"{f} over ticks {a} to {b} ({short(task)})" for f, a, b, task in windows)
    for l in lines:
        if l.startswith(f"{base} = "):
            out.append(f"{new} = ScenarioConfig(")
            continue
        if l.startswith('    id="'):
            out.append(f'    id="{new}",')
            continue
        if l.startswith("    timeline="):
            continue
        if l.startswith("    description="):
            skip = True
            win = ", ".join(f"window({CONST[f]}, {a}, {b})" for f, a, b, _ in windows)
            out.append(f"    timeline=Timeline(({win},)),")
            out.append("    description=(")
            out.append(f'        "{MARK}{base}\'s copy with a fact in force, {cls}: {what}. "')
            out.append(f'        "Everything else is {base}\'s (analysis/kitting/tf1/make_copies.py)."')
            out.append("    ),")
            continue
        if skip:
            if re.match(r"^    \w+=", l):
                skip = False
            else:
                continue
        out.append(l)
    return "\n".join(out)


IMPORTS = ["from shared.types import Timeline", "from domains.kitting.script import window",
           "from domains.kitting.facts import BREAK_TIME, ROOM_WARM"]


def write(todo):
    n = FIRST
    by_module = {}
    for b, cls, windows in todo:
        by_module.setdefault(SCEN / f"scenarios_{b.split('_')[1]}.py", []).append((b, cls, windows))
    runs = []
    for f, items in by_module.items():
        src = f.read_text()
        serial = max(int(x) for x in re.findall(r"^scenario_s\d+_(\d+) = ", src, re.M))
        imported = " ".join(l for l in src.split("\n") if l.startswith(("from ", "import ")))
        need = [i for i, name in zip(IMPORTS, ("Timeline", "window", "BREAK_TIME"))
                if not re.search(rf"\b{name}\b", imported)]
        if need:
            head = list(re.finditer(r"^(from|import) .*$", src, re.M))[-1]
            src = src[:head.end()] + "\n" + "\n".join(need) + src[head.end():]
        add = []
        for b, cls, windows in items:
            serial += 1
            new = f"scenario_{b.split('_')[1]}_{serial:02d}"
            add.append(literal(src, b, new, cls, windows))
            runs.append((b, new, cls))
        src = src.rstrip("\n") + "\n\n\n# T-F part 1, part 1b (5 October 2026): copies with a fact in force " \
            "(analysis/kitting/tf1/make_copies.py; REPORT.md, \"Part 1\").\n" + "\n\n".join(add) + "\n"
        f.write_text(src)
    for b, new, cls in sorted(runs, key=lambda x: x[0]):
        src = yaml.safe_load(open(sorted(glob.glob(str(CFG / b / "run_*.yaml")))[-1]))   # the base's IA-on run file
        run = dict(src, scenario=new)
        d = CFG / new
        d.mkdir(parents=True, exist_ok=True)
        (d / f"run_{n:03d}.yaml").write_text(
            f"# The measurement of T-F part 1, part 1b (not a baseline): {new}, {b}'s copy {cls}, intention-aware, "
            f"context knowledge on.\n# Run: analysis/instruments/mpb/run_set.sh kitting -o analysis/kitting/tf1/measurement "
            f"<this file>\n\n" + yaml.safe_dump(run, sort_keys=False))
        n += 1
    print(f"{len(runs)} copies authored; run files run_{FIRST:03d} to run_{n - 1:03d}")


if __name__ == "__main__":
    todo = plan()
    for b, cls, windows in todo:
        print(b, cls, windows)
    print(f"{len(todo)} copies to author")
    if "--write" in sys.argv:
        write(todo)
