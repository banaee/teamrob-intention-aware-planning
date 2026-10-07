"""
tests/test_tviz_plots.py

T-viz 1c, panel 4c: the lanes the page draws equal the sim-run's own run log at every tick, on reference sim-runs of
both domains (docs/handoffs/plan_T-viz_1c.md, section 5): kitting scenario_s05_02 and dock_loading scenario_s07_07 (an
admission, holds, a retraction, ticks below min_separation), kitting scenario_s10_14 (a timeline fact), kitting
scenario_s05_02 intention-unaware and dock_loading scenario_s07_07 human-unaware.

- The two additions to the messages, here: `world.separations` equal the [sep] lines at every tick (the distance and the
  continuous minimum to the log's two decimals; below as the analyses count it, the minimum under the [run] header's
  min_separation); a task's `identity` is the key of the hypothesis that names it (task equality, shared.types.same_task)
  wherever one does, and no hypothesis's key otherwise.
- The lanes: each sim-run's run description and tick updates, and the values its log states per tick, read here
  independently of the piece, are written to a temporary folder; the page's own reading (webui/page/src/plots/lanes.ts)
  then runs on them under vitest (webui/page/test/lanes.log.test.ts) and compares at every tick: the human's task (the
  [rec] stack's top) and its tag (the analyses' tag reader), the belief (the live hypotheses, the leader and its
  confidence of [IR]), what the robot holds (the decision record of the last [meta-proj]), the decisions ([meta-trig]),
  the robot's task (the step line), the holds ([hold]), the timeline facts (the timeline line's windows) and the
  distance ([sep]).
"""

import importlib.util
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from mesa_sim.sim_run import LOG_DIR
from mesa_sim.webui_adapter import MesaSimulator
from shared.types import same_task
from webui import messages as m
from world.queries import truth_at

ROOT = Path(__file__).parent.parent
PAGE = ROOT / "webui" / "page"
MARGIN = 5
MAX_STEPS = 1000

CASES = [
    ("kitting", "scenario_s05_02", {}),
    ("dock_loading", "scenario_s07_07", {}),
    ("kitting", "scenario_s10_14", {}),
    ("kitting", "scenario_s05_02", {"intention_aware": False}),
    ("dock_loading", "scenario_s07_07", {"human_aware": False}),
]


def _files():
    return set(os.listdir(LOG_DIR)) if os.path.isdir(LOG_DIR) else set()


@pytest.fixture
def new_files():
    before = _files()
    yield lambda: sorted(_files() - before)
    for name in sorted(_files() - before):
        os.remove(os.path.join(LOG_DIR, name))


def _reader():
    spec = importlib.util.spec_from_file_location("tag_reader", ROOT / "analysis" / "instruments" / "mpb" / "tag.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sim_run(domain, scenario, changed):
    """The sim-run through the piece to MARGIN ticks past the point where every agent has finished: the piece's side,
    its tick updates (the start's first), the identities checked on the way, and its log pair's paths."""
    simulator = MesaSimulator()
    catalogue = simulator.catalogue()
    entry = next(s for d in catalogue.domains if d.name == domain for s in d.scenarios if s.id == scenario)
    options = tuple(o.model_copy(update={"value": changed[o.name]}) if o.name in changed else o
                    for o in catalogue.default_choice.options)
    side = simulator.build(m.SimRunChoice(domain=domain, layout=entry.reference_layouts[0], scenario=scenario,
                                          options=options), "plots")
    model = side._model
    updates = [side.state()]
    matched = 0
    for _ in range(MAX_STEPS):
        update = side.step()
        updates.append(update)
        # the identity of the human's task: the key of the hypothesis that names it, by task equality
        for hid, human in model.humans.items():
            stack = truth_at(human.record, update.tick).stack
            sent = next(a for a in update.world.activity if a.human == hid).stack
            for task, ref in zip(stack, sent):
                for rid in model.robots:
                    keys = {repr(h) for h in model.observing[rid].hypotheses if same_task(h.task_instance(), task)}
                    if keys:
                        assert keys == {ref.identity}, (update.tick, ref.label, keys)
                        matched += 1
                    else:
                        assert ref.identity not in {repr(h) for h in model.observing[rid].hypotheses}
        if update.run.finished_at is not None and update.tick >= update.run.finished_at + MARGIN:
            break
    path = side._run.log.log_path
    side.end(m.EndReason.RESET)
    assert matched > 0
    return side, updates, path


# =============================================================================
# The log, read on its own
# =============================================================================

def _pairs(text, sep="  "):
    return dict(item.rsplit("=", 1) for item in text.split(sep) if item)


IR = re.compile(r"^\[IR\] step=(\d+) most_likely=(\S+) confidence=([\d.]+) .* warrant=\[(.*)\]$")
TRIG = re.compile(r"^\[meta-trig\] step=(\d+) trigger=(\w+)( cause=(\w+))?$")
BODY = re.compile(r"^  step: (\d+): \[(\w+)\] task=(\S+) ")
SEP = re.compile(r"^\[sep\] step=(\d+) (\w+)-(\w+) dist=(\S+) min=(\S+)$")
WINDOW = re.compile(r"(\w+) (\d+)\.\.(\d+|end)")


def _expected(log_path, rec_path, domain, model, robot, human, last):
    """Per tick 0 to `last`, the values the log states for each lane."""
    lines = open(log_path).read().splitlines()
    ticks = range(last + 1)
    exp = dict(human={}, belief={}, held={}, decision={}, task={}, hold={}, facts={}, separation={})
    min_sep, windows, step, record = None, [], None, None
    holds = []
    for line in lines:
        if line.startswith(f"[run] {robot} "):
            min_sep = float(re.search(r" min_separation=([\d.]+)", line)[1])
        elif line.startswith("[run_mesa] timeline "):
            windows = [(f, int(a), None if b == "end" else int(b)) for f, a, b in WINDOW.findall(line)]
        elif (g := IR.match(line)):
            exp["belief"][int(g[1])] = dict(leader=g[2], confidence=g[3], live=sorted(_pairs(g[4])))
        elif (g := TRIG.match(line)):
            step = int(g[1])
            if g[2] != "none":
                exp["decision"][step] = dict(trigger=g[2], cause=g[4])
        elif line.startswith("[meta-proj] "):
            ir = exp["belief"].get(step)
            record = ir["leader"] if " projection=built " in line + " " and ir is not None else None
            exp["held"][step] = record
        elif line.startswith("[hold] ") and f" {robot} start " in line:
            holds.append([int(re.search(r"step=(\d+)", line)[1]), None])
        elif line.startswith("[hold] ") and f" {robot} end " in line:
            end = int(re.search(r"step=(\d+)", line)[1])
            holds[-1][1] = end if " interrupted=True" in line else end + 1
        elif (g := BODY.match(line)) and g[2] == robot:
            exp["task"][int(g[1])] = None if g[3] == "None" else g[3]
        elif (g := SEP.match(line)) and g[2] == robot and g[3] == human:
            minimum = float(g[5])
            # below as the analyses count it, on the logged minimum; at the rounding edge either answer
            below = None if abs(minimum - min_sep) <= 0.005 else minimum < min_sep
            exp["separation"][int(g[1])] = dict(distance=g[4], minimum=g[5], below=below)
    # what the robot holds is the last decision record, kept between decisions
    held, kept = {}, None
    for t in ticks:
        kept = exp["held"].get(t, kept)
        held[t] = kept
    exp["held"] = held
    exp["hold"] = {t: any(a <= t < (last + 1 if b is None else b) for a, b in holds) for t in ticks}
    exp["facts"] = {t: sorted({f for f, a, b in windows if a <= t and (b is None or t < b)}) for t in ticks}
    exp["fact_rows"] = sorted({f for f, _, _ in windows})
    # the human's task: the top of the [rec] stack; its tag: the analyses' reader
    top = {}
    for line in open(rec_path):
        g = re.match(r"\[rec\] step=(\d+) stack=(\S+) ", line)
        if g:
            top[int(g[1])] = None if g[2] == "-" else g[2].split(";")[0]
    exp["human"] = {t: dict(task=top.get(t), tag=None) for t in ticks}
    if model.declared_context is not None:
        from mesa_sim.action_decomposer import _parse_duration_to_steps
        reader = _reader()
        recency = {e.task.name: _parse_duration_to_steps(e.recency.duration, model)
                   for e in model.declared_context.entries() if e.recency is not None}
        stretches, done = reader.record(rec_path)
        world = reader.World(domain, log_path, done, recency)
        for task, a, b in stretches:
            tag = world.tag(task, a)[0]
            for t in range(a, b):
                if t in exp["human"]:
                    exp["human"][t]["tag"] = tag
    for key in ("belief", "decision", "task", "separation"):
        exp[key] = {t: exp[key].get(t) for t in ticks}
    return {k: ({str(t): v for t, v in val.items()} if isinstance(val, dict) else val) for k, val in exp.items()}


# =============================================================================
# The test
# =============================================================================

def test_the_lanes_are_the_logs(new_files, tmp_path):
    if shutil.which("npx") is None or not (PAGE / "node_modules").is_dir():
        pytest.skip("the page's node_modules are not installed (cd webui/page && npm ci)")
    for i, (domain, scenario, changed) in enumerate(CASES):
        side, updates, log_path = _sim_run(domain, scenario, changed)
        description = side.description
        (robot,) = description.robots
        (human,) = description.world.humans
        last = updates[-1].tick

        # the distance the page receives is the [sep] line's
        exp = _expected(log_path, log_path[:-4] + ".rec", domain, side._model, robot.robot, human.id, last)
        for update in updates[1:]:
            (s,) = update.world.separations
            e = exp["separation"][str(update.tick)]
            assert (f"{s.distance:.2f}", f"{s.minimum:.2f}") == (e["distance"], e["minimum"]), update.tick
            assert e["below"] is None or s.below == e["below"], update.tick
        assert updates[0].world.separations == ()

        # what the reference runs are chosen for
        if not changed and scenario != "scenario_s10_14":
            assert any(e and e["below"] for e in exp["separation"].values())
            assert any(exp["hold"].values()) and any(exp["held"].values())
        if scenario == "scenario_s10_14":
            assert exp["fact_rows"] and any(exp["facts"].values())

        case = dict(name=f"{domain} {scenario} {changed or 'default'}",
                    description=description.model_dump(mode="json"),
                    ticks=[u.model_dump(mode="json") for u in updates], expected=exp)
        (tmp_path / f"case_{i}.json").write_text(json.dumps(case))

    run = subprocess.run(["npx", "vitest", "run", "test/lanes.log.test.ts"], cwd=PAGE, capture_output=True, text=True,
                         env=dict(os.environ, TVIZ_LANES_CASES=str(tmp_path)), timeout=300)
    assert run.returncode == 0, run.stdout[-4000:] + run.stderr[-2000:]
    assert f"{len(CASES)} passed" in run.stdout, run.stdout[-2000:]
