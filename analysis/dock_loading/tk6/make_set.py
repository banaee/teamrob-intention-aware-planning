#!/usr/bin/env python3
"""
make_set.py — the authoring of T-K part 1's step 6 on dock_loading (Hadi, 6 October 2026; design_records.md, "T-K",
STEP 6; the rules: analysis/dock_loading/tk6/README.md). Writes scenario literals into domains/dock_loading/scenarios/
and the run files into configs/dock_loading/tk6/. The literals are the source; this file records how they were made.

    make_set.py bases       the new scripts and the copies of the planning scripts on env_layout_02 (new literals)
    make_set.py variants    per planning script, two or three scenarios that differ only in where break_time lies
    make_set.py runs        the run files, by serial (no setting in a name)
    make_set.py runs_full_reorder   the planning scripts' run files under full_reorder, serials after the first 568

The scripts (kind 3, "pallets in the bays", independent of the robot; the robot's pool deliver pallet_4 and pallet_5,
return pallet_6 and pallet_7; the human starts at the standby place and closes at the desk; sN the scan of pallet_N):
  a  a coffee break first, before any scan             CB, s0, s2
  b  scans only, across both bays                      s0, s2, s1, s3
  c  an office break inside a scan (on arrival)        s0[on arrival: OB], s2
  d  a second coffee break inside the first's recency  CB, s0, CB, s2
  e  a coffee break then an office break               s0, CB, OB, s2
  e' an office break then a coffee break               s0, OB, CB, s2
  f  one coffee break, for KT4's three window edges     s2, CB, s0
  g  a coffee break once every scan is done            s0, s2, CB

The windows (from the human's replay of the base, its top-of-stack stretches; for a script that depends on the robot,
from the robot's plain chain, horizon.py): see `windows()`.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / "mesa_sim"), str(ROOT / "analysis" / "instruments" / "irb"),
                str(ROOT / "analysis" / "dock_loading" / "mpb")]

import yaml

SCEN = ROOT / "domains" / "dock_loading" / "scenarios"
CFG = ROOT / "configs" / "dock_loading" / "tk6"
TMP = ROOT / "analysis" / "dock_loading" / "tk6" / "replay"          # the replays' run files and outputs (untracked)
MARK = "T-K part 1, step 6"

ROOMS = [("env_setup_10", "env_layout_02", "s10"), ("env_setup_08", "env_layout_03", "s08"),
         ("env_setup_09", "env_layout_04", "s09"), ("env_setup_11", "env_layout_05", "s11")]
S = lambda n: f'confirm_delivered_pallet("pallet_{n}")'
CB, OB = 'coffee_break("coffee_machine_0")', 'office_break("office_chair")'
SCRIPTS = [
    ("a", "a coffee break first, before any scan", [CB, S(0), S(2)]),
    ("b", "scans only, across both bays", [S(0), S(2), S(1), S(3)]),
    ("c", "an office break inside a scan, on arrival at the bay before the scan", [f"{S(0)}.at(move_to, {OB}, occurrence=0)", S(2)]),
    ("d", "a second coffee break inside the first's recency", [CB, S(0), CB, S(2)]),
    ("e", "a coffee break, then an office break", [S(0), CB, OB, S(2)]),
    ("e'", "an office break, then a coffee break", [S(0), OB, CB, S(2)]),
    ("f", "one coffee break between two scans, for the three window edges", [S(2), CB, S(0)]),
    ("g", "a coffee break once every scan is done (no assigned task live)", [S(0), S(2), CB]),
]
POOL = ['deliver_pallet("pallet_4")', 'deliver_pallet("pallet_5")', 'load_return("pallet_6")', 'load_return("pallet_7")']
DEPENDENT = ["scenario_s03_02", "scenario_s03_03", "scenario_s05_02", "scenario_s05_03", "scenario_s05_04",
             "scenario_s05_05", "scenario_s05_06", "scenario_s07_02", "scenario_s07_03", "scenario_s07_04",
             "scenario_s07_05", "scenario_s07_06"]
RECOGNITION = [f"scenario_s{m}_{n:02d}" for m in ("02", "04", "06") for n in range(2, 20)]
IMPORTS = {"Timeline": "from shared.types import Timeline", "window": "from domains.dock_loading.script import window",
           "BREAK_TIME": "from domains.dock_loading.facts import BREAK_TIME"}


def module(tag):
    return SCEN / f"scenarios_{tag}.py"


def literals(src):
    """{id: literal text} of a module's scenario literals."""
    out = {}
    for m in re.finditer(r"^(scenario_s\d+_\d+) = ScenarioConfig\(\n.*?^\)\n", src, re.M | re.S):
        out[m[1]] = m[0]
    return out


def next_serial(src):
    return max([int(x) for x in re.findall(r"^scenario_s\d+_(\d+) = ", src, re.M)] or [0]) + 1


def ensure_imports(src, names):
    imported = " ".join(l for l in src.split("\n") if l.startswith(("from ", "import ")))
    need = [IMPORTS[n] for n in names if not re.search(rf"\b{n}\b", imported)]
    if need:
        lines = src.split("\n")
        i = max(k for k, l in enumerate(lines) if l.startswith(("from ", "import ")))
        if "(" in lines[i] and ")" not in lines[i]:          # a parenthesised import over several lines
            while ")" not in lines[i]:
                i += 1
        src = "\n".join(lines[:i + 1] + need + lines[i + 1:])
    return src


def new_literal(sid, setup, layout, description, entries, assigned):
    ind = " " * 20
    desc = "\n".join(f'        "{line}"' for line in wrap(description))
    return (f"{sid} = ScenarioConfig(\n    id=\"{sid}\",\n    setup=\"{setup}\",\n    reference_layouts=[\"{layout}\"],\n"
            f"    description=(\n{desc}\n    ),\n    agents=[\n        AgentConfig(\n            agent_id=\"human_0\",\n"
            f"            agent_type=\"human\",\n            start_position=(0, 0),\n            scheduled_tasks=Script(\n"
            f"                [\n" + "".join(f"{ind}{e},\n" for e in entries) +
            f"                ],\n                closing=[go_to(\"desk\")],\n            ),\n            observes=[],\n"
            f"            assigned_tasks=[\n" + "".join(f"                {a},\n" for a in assigned) +
            f"            ],\n        ),\n        AgentConfig(\n            agent_id=\"robot_0\",\n"
            f"            agent_type=\"robot\",\n            start_position=(0, -370),\n            observes=[\"human_0\"],\n"
            f"            assigned_tasks=[\n" + "".join(f"                {p},\n" for p in POOL) +
            f"            ],\n        ),\n    ],\n)\n")


def wrap(text, width=105):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur + " ")
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    lines.append(cur)
    return [l.replace('"', '\\"') for l in lines]


def replace_description(text, description):
    out, skip = [], False
    for l in text.split("\n"):
        if l.startswith("    description="):
            skip = True
            out.append("    description=(")
            out += [f'        "{line}"' for line in wrap(description)]
            out.append("    ),")
            continue
        if skip:
            if re.match(r"^    \w+=", l):
                skip = False
            else:
                continue
        out.append(l)
    return "\n".join(out)


def bases():
    """The copies of env_setup_08's ten planning scripts on env_layout_02 (env_setup_10), then the eight new scripts in
    each of the four rooms."""
    s08 = literals(module("s08").read_text())
    texts = {}
    for n in range(1, 11):
        b = f"scenario_s08_{n:02d}"
        new = f"scenario_s10_{n:02d}"
        t = s08[b].replace(b, new).replace('"env_setup_08"', '"env_setup_10"').replace('"env_layout_03"', '"env_layout_02"')
        t = replace_description(t, f"{MARK}: {b}'s script and pools, unchanged, on env_layout_02 (env_setup_10, kind 3), "
                                   f"so that the planning runs cover three rooms (Hadi, 6 October 2026). The distances "
                                   f"and derived durations its description states are env_layout_03's; they do not "
                                   f"hold here. {b}'s description begins: " + first_sentence(s08[b]))
        texts.setdefault("s10", []).append(t)
    for setup, layout, tag in ROOMS:
        src = module(tag).read_text() if module(tag).exists() else ""
        n = next_serial(src) + (10 if tag == "s10" else 0)
        for key, what, entries in SCRIPTS:
            sid = f"scenario_{tag}_{n:02d}"
            scans = [e.split(".at(")[0] for e in entries if e.startswith("confirm")]
            texts.setdefault(tag, []).append(new_literal(
                sid, setup, layout, f"{MARK}, script {key} ({what}), on {layout}: the human "
                + ", ".join(human_word(e) for e in entries) + ", then the walk to the desk; the robot delivers pallet_4 "
                "and pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script independent of the robot, the "
                "disjointness rule (MPB-DL7). No timeline (no fact); its copies with break_time follow. No expectation "
                "derived by hand (Hadi, 6 October 2026); the oracle's tables are committed before the runs.",
                entries, scans))
            n += 1
    for tag, items in texts.items():
        f = module(tag)
        if f.exists():
            src = f.read_text().rstrip("\n") + "\n\n\n"
        else:
            setup = next(s for s, _, t in ROOMS if t == tag)
            layout = next(l for _, l, t in ROOMS if t == tag)
            src = (f'# domains/dock_loading/scenarios/scenarios_{tag}.py\n"""\nDock_loading scenarios on {setup} '
                   f'({MARK}, kind 3 "pallets in the bays", written for\n{layout}; design_records.md, "T-K", STEP 6; '
                   f'analysis/dock_loading/tk6/README.md). One module per setup.\nWritten by '
                   f'analysis/dock_loading/tk6/make_set.py; the literals are the source.\n"""\n\n'
                   "from shared.types import AgentConfig, ScenarioConfig, Script\n"
                   "from domains.dock_loading.actions import move_to\n"
                   "from domains.dock_loading.script import (coffee_break, confirm_delivered_pallet, deliver_pallet, "
                   "go_to, load_return,\n                                         office_break, stand)\n\n\n")
        src += f"# {MARK} (6 October 2026): " + ("the planning scripts on env_layout_02 and " if tag == "s10" else "") \
            + "the new scripts (analysis/dock_loading/tk6/make_set.py bases).\n" + "\n\n".join(items)
        f.write_text(src)
        print(f"{f.name}: {len(items)} literals")


def first_sentence(text):
    m = re.search(r'description=\(\n\s+"([^"]*)', text)
    return (m[1].split(": ")[0] if m else "").strip()


def human_word(e):
    if e.startswith("coffee_break"):
        return "takes a coffee break"
    if e.startswith("office_break"):
        return "takes an office break"
    n = re.search(r"pallet_(\d)", e)[1]
    return f"scans pallet_{n}" + (" with an office break on arrival at the bay" if ".at(" in e else "")


def planning_bases():
    """The planning scripts: (scenario, independent) in run order."""
    out = [(f"scenario_s{m}_{n:02d}", True) for m in ("08", "09") for n in range(1, 11)]
    for _, _, tag in ROOMS:
        src = module(tag).read_text()
        ids = [i for i in literals(src) if MARK in literals(src)[i].split("agents=")[0] and "copy with break_time" not in literals(src)[i]]
        out += [(i, True) for i in sorted(ids)]
    out += [(i, False) for i in DEPENDENT]
    return out


def run_file(sid, path, **change):
    from domains.dock_loading.registry import domain_config
    sc = domain_config["scenarios"][sid]
    run = dict(domain="dock_loading", layout=sc.reference_layouts[0], setup=sc.setup, scenario=sid, steps=900,
               human_aware=True, intention_aware=True, assignment_knowledge=True, context_knowledge=True,
               strategy="single_task", gate_strategy="none", cost_strategy="realized", separation_stop=False,
               test_level=0.05)
    run.update(change)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(run, sort_keys=False))
    return path


def stretches(sid):
    """The human's top-of-stack stretches in the replay of the base, the robot idle: [(task, first, tick after last)];
    for a coffee break or an office break also the first tick of its wait."""
    import trajectory
    t = trajectory.expand(run_file(sid, TMP / f"{sid}.yaml"), 1500)
    out = []
    for a in t["actions"]:
        if out and out[-1][0] == a["task"]:
            if a.get("action", "").startswith("wait_at") and out[-1][3] is None:
                out[-1][3] = a["tick"]
            continue
        if out:
            out[-1][2] = a["tick"]
        out.append([a["task"], a["tick"], None, None])
    if out:
        out[-1][2] = t["last_ack"] + 1
    return [tuple(s) for s in out]


def foreseeable(task):
    return task.startswith(("coffee_break", "office_break"))


def windows(sid, independent):
    """The variants of a script, each a list of break_time windows [(first tick, end)] with its rule's name.
    Independent scripts, from the base's replay (the top-of-stack stretches):
      V1 over the first break's stretch (a coffee break: the fact in accord; an office break: not), else over the
         first scan's;
      V2 over the first stretch not overlapping V1's window, scans first, then any other (a stand, the walk to the desk);
      V3, a script with two breaks: over both breaks (two windows);
      script f: in place of V1 to V3, KT4's three edges, each ending with the coffee break's stretch: the window opens
         10 ticks before the human leaves for it, at the middle of its walk, at its arrival (the wait's first tick).
    Scripts that depend on the robot (no replay before the run): from the robot's plain chain (horizon.py), the first
    delivery's completion tick c1 and the second's c2: V1 [c1, c1 + 60), V2 [c2, c2 + 60) (one delivery: [0, 60)).
    Placed roughly; written before the runs and never moved."""
    if not independent:
        import horizon
        _, per, _ = horizon.plain_chain(run_file(sid, TMP / f"{sid}.yaml"))
        from domains.dock_loading.registry import domain_config
        robot = next(a for a in domain_config["scenarios"][sid].agents if a.agent_type == "robot")
        ends, t = [], 0
        for task, ticks in zip(robot.assigned_tasks, per):
            t += ticks
            if task.schema.name == "deliver_pallet":
                ends.append(t)
        v2 = (ends[1], ends[1] + 60) if len(ends) > 1 else (0, 60)
        return [("V1, from the first delivery", [(ends[0], ends[0] + 60)]),
                ("V2, from the second delivery" if len(ends) > 1 else "V2, the first 60 ticks", [v2])]
    st = stretches(sid)
    breaks = [s for s in st if foreseeable(s[0])]
    if "script f" in description_of(sid):
        task, a, b, wait = breaks[0]
        return [("edge before the human leaves", [(a - 10, b)]), ("edge in the walk", [((a + wait) // 2, b)]),
                ("edge at the arrival", [(wait, b)])]
    first = breaks[0] if breaks else next(s for s in st if s[0].startswith("confirm"))
    v1 = [(first[1], first[2])]
    rest = [s for s in st if s[0].startswith("confirm")] + [s for s in st if not s[0].startswith("confirm")]
    second = next((s for s in rest if not foreseeable(s[0]) and (s[2] <= v1[0][0] or s[1] >= v1[0][1])), None)
    out = [("V1, over the first " + ("break" if breaks else "scan"), v1)]
    if second is not None:
        out.append(("V2, over " + ("a scan" if second[0].startswith("confirm") else "another task"),
                    [(second[1], second[2])]))
    if len(breaks) > 1:
        out.append(("V3, over both breaks", [(s[1], s[2]) for s in breaks[:2]]))
    return out


def description_of(sid):
    from domains.dock_loading.registry import domain_config
    return domain_config["scenarios"][sid].description


def variants():
    by_module = {}
    for sid, independent in planning_bases():
        for rule, ws in windows(sid, independent):
            by_module.setdefault(sid.split("_")[1], []).append((sid, rule, ws))
    for tag, items in by_module.items():
        f = module(tag)
        src = ensure_imports(f.read_text(), ["Timeline", "window", "BREAK_TIME"])
        lits, n, add = literals(src), next_serial(src), []
        for sid, rule, ws in items:
            new = f"scenario_{tag}_{n:02d}"
            n += 1
            t = lits[sid].replace(f"{sid} = ", f"{new} = ").replace(f'id="{sid}"', f'id="{new}"')
            t = re.sub(r"^    timeline=.*\n", "", t, flags=re.M)
            win = ", ".join(f"window(BREAK_TIME, {a}, {b})" for a, b in ws)
            t = t.replace("    description=(", f"    timeline=Timeline(({win},)),\n    description=(", 1)
            span = " and ".join(f"from {a} to {b}" for a, b in ws)
            add.append(replace_description(t, f"{MARK}: {sid}'s copy with break_time {span} ({rule}; the rule: "
                                              f"analysis/dock_loading/tk6/make_set.py, windows). Everything else is "
                                              f"{sid}'s."))
        f.write_text(src.rstrip("\n") + f"\n\n\n# {MARK} (6 October 2026): the copies with break_time "
                     "(analysis/dock_loading/tk6/make_set.py variants).\n" + "\n\n".join(add))
        print(f"{f.name}: {len(add)} copies")


CONDITIONS = [("human-unaware", dict(human_aware=False)), ("intention-unaware", dict(intention_aware=False)),
              ("intention-aware, context knowledge off", dict(context_knowledge=False)),
              ("intention-aware, context knowledge on", {})]


def runs():
    from domains.dock_loading.registry import domain_config
    n = 0

    def write(sid, label, change):
        nonlocal n
        n += 1
        p = run_file(sid, CFG / sid / f"run_{n:03d}.yaml", **change)
        p.write_text(f"# {MARK} (not a baseline): {sid}, {label}.\n# Run: analysis/instruments/mpb/run_set.sh "
                     f"dock_loading -o analysis/dock_loading/tk6/measurement <this file>\n\n" + p.read_text())
    bases_ = [s for s, _ in planning_bases()]
    for sid in bases_:
        for label, change in CONDITIONS:
            write(sid, label, change)
    copies = sorted((s for s, sc in domain_config["scenarios"].items() if sc.description.startswith(f"{MARK}: ")
                     and "copy with break_time" in sc.description), key=lambda s: (s.split("_")[1], s))
    for sid in copies:
        write(sid, CONDITIONS[3][0], CONDITIONS[3][1])
    for sid in RECOGNITION:
        for label, change in CONDITIONS[2:]:
            write(sid, label, change)
    print(f"{n} run files: {len(bases_)} planning scripts in four conditions, {len(copies)} copies with break_time "
          f"(context knowledge on), {len(RECOGNITION)} recognition scenarios in the two intention-aware conditions")


def runs_full_reorder():
    """The 74 planning scripts under full_reorder in the four conditions (Hadi, 6 October 2026; design_records.md,
    "T-K", STEP 6, FULL_REORDER), serials after the existing 568, in the order of `runs`."""
    n = max(int(p.stem[4:]) for p in CFG.glob("*/run_*.yaml"))
    first = n + 1
    for sid in [s for s, _ in planning_bases()]:
        for label, change in CONDITIONS:
            n += 1
            p = run_file(sid, CFG / sid / f"run_{n:03d}.yaml", strategy="full_reorder", **change)
            p.write_text(f"# {MARK} (not a baseline): {sid}, {label}, full_reorder.\n# Run: analysis/instruments/mpb/"
                         f"run_set.sh dock_loading -o analysis/dock_loading/tk6/measurement <this file>\n\n" + p.read_text())
    print(f"run_{first:03d} to run_{n:03d}: {n - first + 1} run files under full_reorder")


if __name__ == "__main__":
    {"bases": bases, "variants": variants, "runs": runs, "runs_full_reorder": runs_full_reorder}[sys.argv[1]]()
