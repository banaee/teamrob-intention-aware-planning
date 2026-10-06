#!/usr/bin/env python3
"""
tag.py — the tag per task (Hadi, 5 October 2026; design_records.md, "T-F part 1", THE TAG PER TASK; glossary §7), read
from the runs of run_set.sh, in any domain (T-K part 1, step 6; design_records.md, "T-K", STEP 6).

THE ONE DEFINITION (T-viz 1a (iv), 6 October 2026): the rule below lives in world/tag.py (the tag, the recency facts,
the stretches), which the web-ui's piece reads too; this reader parses a run's log and record and hands them to it.

Each task the human performs gets one tag by the facts in force when it starts:
- in accord: a fact holds and the human performs the task the fact makes more likely;
- not in accord: a fact holds and the human performs another task;
- no fact: no fact holds.
A label of the analysis, a term of the world: the robot never has it. It is read from the world, never from the robot's
mind, so a run in any condition gets the same tags for the same human trajectory.

What the reader takes as "the task a fact makes more likely": the foreseeable tasks at the raised level of the domain's
declared context knowledge (`ContextKnowledge.level`, AM36: the suppressing condition first, then the raising, else
ordinary), evaluated on the world's facts at the task's first tick: the timeline facts of the run's windows (its log's
`[run_mesa] timeline` line) and the recency facts of the foreseeable tasks the human completed in the run (its record,
`.rec`: a completion's tick and the task's recency duration, half-open, the completion tick included, AM46, AM47).
No name of a task or a fact is written here. Object states are not read (no raising condition of kitting or
dock_loading names one; a suppressing condition that names one, kitting's ac_on, is not seen in the `lowered` column).

PROVISIONAL (ccode, 6 October 2026; TODO-185, for Hadi's confirmation): a fact that lowers a task gives no tag. The tag
reads the raised level only; a task that starts while only a lowering fact holds (a recency fact; a raising fact
whose task is suppressed) is tagged "no fact". The tasks at the suppressed level at the task's start are listed beside
the tag (`lowered`), so the case "the human performs a task that a fact lowers" stays visible.

A task the human performs: one stretch of one task on top of the human's stack in the run's record (a task resumed after
a cut is a new stretch, tagged at its resumption). Every top-of-stack task is tagged, those with no hypothesis too (a
walk to the standby place or the desk, a stand); their admission measures are empty.

Measures per stretch, "admitted" in both readings (Hadi, 6 October 2026); the gate's reading over the whole stretch (the
recognizer and the gate run on every tick, the empty pool stops planning only), the decision record's over the
stretch's ticks before the robot's terminal decision (the whole run when it has none; as in T-F part 1's step 3b):
- adm_gate: ticks from the stretch's first tick to the first tick the gate's answer clears for the task's hypothesis
  (actual_ticks.json: `gate` clears and `leader` the hypothesis); adm_record: to the first tick the meta-planner's
  decision record holds it (`record`); "never": not within the stretch; empty: no hypothesis;
- wrong_gate: ticks the gate clears for another hypothesis; wrong_record: ticks the record holds another hypothesis;
- viol: the violation ticks (F1's class viol, a moving robot below min_separation) inside the stretch; near: every tick
  below min_separation inside it (any class); counted: the stretch's ticks before the terminal decision (the record's
  reading).

    tag.py <out_root> [domain]    writes <out_root>/tags.csv, one row per stretch per run (the run's settings beside it)
"""
import csv
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / "analysis" / "instruments" / "common")]

import separation
from shared.types import Predicate
from world.tag import Stretches, recent_tasks, tag_at

COLUMNS = ["run", "scenario", "layout", "condition", "context_knowledge", "task", "start", "end", "tag", "raised",
           "lowered", "hypothesis", "adm_gate", "adm_record", "wrong_gate", "wrong_record", "viol", "near", "counted"]


def _bind(key):
    name, args = key.split("(", 1)
    return name, dict(a.split("=", 1) for a in args.rstrip(")").split(",") if "=" in a)


def hypothesis_of(task, keys):
    """The hypothesis key of a task the human performs (its name, and its bindings a superset of the key's), or None."""
    name, b = _bind(task)
    for k in keys:
        kn, kb = _bind(k)
        if kn == name and all(b.get(x) == v for x, v in kb.items()):
            return k
    return None


def record(rec):
    """(stretches, completions) from a run's record: [(task, first tick, tick after the last)] of the top of the stack,
    and [(tick, task)] of each completed task."""
    top, done = {}, []
    for l in open(rec):
        m = re.match(r"\[rec\] step=(\d+) stack=(\S+) .* events=(\S+)$", l.rstrip("\n"))
        if not m:
            continue
        t = int(m[1])
        top[t] = None if m[2] == "-" else m[2].split(";")[0]
        done += [(t, e[len("completed:"):]) for e in re.findall(r"completed:[^,]+\)", m[3])]
    out = []
    stretches = Stretches()
    for t in sorted(top):
        start = stretches.at(t, top[t])
        if start is None:
            if out and out[-1][2] is None:
                out[-1][2] = t
            continue
        if out and out[-1][1] == start and out[-1][2] is None:
            continue
        if out and out[-1][2] is None:
            out[-1][2] = t
        out.append([top[t], t, None])
    if out and out[-1][2] is None:
        out[-1][2] = max(top) + 1
    return [tuple(s) for s in out], done


def windows(log):
    line = next(l for l in open(log) if l.startswith("[run_mesa] timeline"))
    return [(f, int(a), 10 ** 9 if b == "end" else int(b))
            for f, a, b in re.findall(r"(\w+) (\d+)\.\.(\d+|end)", line.split("windows=")[1])]


class World:
    """The run's facts as world/tag.py reads them: the timeline's windows, the completed tasks, the recency durations
    in ticks; the record's task names resolved to the domain's task schemas (parsing the log, here only)."""

    def __init__(self, domain, log, done, recency_ticks):
        config = importlib.import_module(f"domains.{domain}.registry").domain_config
        self.ck = config["context_knowledge"]
        self.schemas = {s.name: s for s in config["register_fn"]().task_schemas()}
        self.windows = windows(log)
        self.recency = [(e.task, recency_ticks[e.task.name]) for e in self.ck.entries()
                        if e.recency is not None and e.task.name in recency_ticks]
        self.done = [(c, self.schemas[_bind(task)[0]]) for c, task in done]

    def tag(self, task, t):
        facts = {Predicate(f, ()) for f, a, e in self.windows if a <= t < e}
        found = tag_at(self.ck, self.schemas[_bind(task)[0]], facts, recent_tasks(self.ck, self.done, self.recency, t))
        return found.tag.value, sorted(s.name for s in found.raised), sorted(s.name for s in found.lowered)


def run_rows(d):
    s = json.load(open(d / "settings.json"))
    log, rec = d / f"{d.name}.log", d / f"{d.name}.rec"
    obs = json.load(open(d / "observed.json"))
    end = obs["terminal"] if obs["terminal"] is not None else obs["steps"]
    ticks = {t["tick"]: t for t in json.load(open(d / "actual_ticks.json"))}
    keys = sorted({k for t in ticks.values() for k in (t.get("belief_h") or t.get("belief") or {})})
    recency = json.load(open(d / "trajectory.json"))["params"].get("recency_ticks", {})
    stretches, done = record(rec)
    world = World(s["domain"], log, done, recency)
    _, by, passing, beside, unknown, _, _ = separation.counts(log)
    viol = set(by["viol"])
    near = set(by["viol"]) | set(by["recede"]) | set(by["stand"]) | set(by["?"])
    out = []
    for task, a, b in stretches:
        tag, raised, lowered = world.tag(task, a)
        h = hypothesis_of(task, keys)
        span, whole = range(a, min(b, end)), range(a, b)
        clears = lambda t: ticks.get(t, {}).get("gate") == "clears"
        first = lambda ok, ts: next((t - a for t in ts if ok(t)), None)
        out.append(dict(
            run=d.name, scenario=s["scenario"], layout=s["layout"], condition=s["condition"],
            context_knowledge=s["header"]["context_knowledge"], task=task, start=a, end=b, tag=tag,
            raised=";".join(raised), lowered=";".join(lowered), hypothesis=h or "",
            adm_gate="" if h is None else first(lambda t: clears(t) and ticks[t].get("leader") == h, whole),
            adm_record="" if h is None else first(lambda t: ticks.get(t, {}).get("record") == h, span),
            wrong_gate=sum(1 for t in whole if clears(t) and ticks[t].get("leader") not in (None, h)),
            wrong_record=sum(1 for t in span if ticks.get(t, {}).get("record") not in (None, h)),
            viol=sum(1 for t in range(a, b) if t in viol), near=sum(1 for t in range(a, b) if t in near),
            counted=len(span)))
    for r in out:
        for k in ("adm_gate", "adm_record"):
            r[k] = "never" if r[k] is None else r[k]      # never within the stretch; "" (no hypothesis) stays
    return out


if __name__ == "__main__":
    root = Path(sys.argv[1])
    rows = [r for d in sorted(root.glob("*/*"), key=lambda p: p.name) if (d / "settings.json").exists()
            for r in run_rows(d)]
    with open(root / "tags.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f"tags: {len(rows)} task stretches in {len({r['run'] for r in rows})} runs; "
          + ", ".join(f"{k} {sum(r['tag'] == k for r in rows)}" for k in ("in accord", "not in accord", "no fact")))
