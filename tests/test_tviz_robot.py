"""
tests/test_tviz_robot.py

T-viz 1b, panel 4b: the values the page receives of the robot (the tick update's `robots`, the run description's
`robots`) equal the sim-run's own run log at every tick, on reference sim-runs of both domains: an admission, a refusal,
a fallback projection, a hold, a retraction (kitting scenario_s05_02, dock_loading scenario_s07_07, with the default
run file's options); a timeline fact in force (kitting scenario_s10_14); the robot intention-unaware and human-unaware.

The log is read independently of the piece: the recognizer's lines ([IR], [IR-rank], [IR-context]), the gate derived
from the logged values in the gate's order (MetaPlanner._clears_gate's: θ, the leader's adequacy, its warrant, its
rank), the decisions ([meta-trig], [meta-proj], [meta], [meta-b3], [hold]) and the body's step line.
"""

import ast
import math
import os
import re
from pathlib import Path

import pytest

from mesa_sim.sim_run import LOG_DIR
from mesa_sim.webui_adapter import MesaSimulator
from webui import messages as m

ROOT = Path(__file__).parent.parent
MARGIN = 5          # ticks run past the point where every agent has finished
MAX_STEPS = 1000

# (domain, scenario, run options changed from the default run file's)
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


def _sim_run(domain, scenario, changed):
    """The sim-run through the piece to MARGIN ticks past the point where every agent has finished: its description,
    its tick updates (the start's first) and its log's lines."""
    simulator = MesaSimulator()
    catalogue = simulator.catalogue()
    entry = next(s for d in catalogue.domains if d.name == domain for s in d.scenarios if s.id == scenario)
    options = tuple(o.model_copy(update={"value": changed[o.name]}) if o.name in changed else o
                    for o in catalogue.default_choice.options)
    side = simulator.build(m.SimRunChoice(domain=domain, layout=entry.reference_layouts[0], scenario=scenario,
                                          options=options), "robot")
    updates = [side.state()]
    for _ in range(MAX_STEPS):
        updates.append(side.step())
        finished = updates[-1].run.finished_at
        if finished is not None and updates[-1].tick >= finished + MARGIN:
            break
    path = side._run.log.log_path
    side.end(m.EndReason.RESET)
    with open(path) as f:
        return side.description, updates, f.read().splitlines()


# =============================================================================
# The log, read on its own
# =============================================================================

def _pairs(text, sep="  "):
    """`k=v  k=v` (keys may hold '='; the value is after the last one)."""
    return dict(item.rsplit("=", 1) for item in text.split(sep) if item)


IR = re.compile(r"^\[IR\] step=(\d+) most_likely=(\S+) confidence=([\d.]+) lifecycle=(\w+)( finding=(\w+))?"
                r"( leader_adequacy=(\w+))? tails=\[(.*?)\] warrant=\[(.*)\]$")
TRIG = re.compile(r"^\[meta-trig\] step=(\d+) trigger=(\w+)( cause=(\w+))?$")
META = re.compile(r"^\[meta\] step=(\d+) trigger=\w+ winner=(\w+)(\{.*?\}) queue=(\[.*\])$")
BODY = re.compile(r"^  step: (\d+): \[(\w+)\] task=(\S+) action=(\S+) micro=(\S+) ")


def _task(text):
    """A task as [meta] writes it, `name{'?p': 'v', ...}`: its name and bindings."""
    name, bindings = re.match(r"^(\w+)(\{.*\})$", text).groups()
    return name, ast.literal_eval(bindings)


def _read_log(lines, robot):
    log = dict(theta=None, known=None, flags={}, ir={}, rank={}, context={}, trig={}, proj={}, meta={}, b3={},
               finished=None, hold_start={}, holds=[], body={})
    step = None
    for line in lines:
        if line.startswith(f"[run] {robot} "):
            log["theta"] = float(re.search(r" theta=([\d.]+)", line)[1])
            log["flags"] = dict(re.findall(r" (human_aware|intention_aware)=(on|off)", line))
        elif line.startswith("[IR-assignment] "):
            log["known"] = (ast.literal_eval(re.search(r"known=(\[.*\])$", line)[1])
                            if " knowledge=on " in line else None)
        elif (g := IR.match(line)):
            log["ir"][int(g[1])] = dict(leader=g[2], confidence=g[3], lifecycle=g[4], finding=g[6], adequacy=g[8],
                                        tails=_pairs(g[9]), warrant=_pairs(g[10]))
        elif line.startswith("[IR-rank] "):
            g = re.match(r"^\[IR-rank\] step=(\d+) rank=\[(.*)\]$", line)
            log["rank"][int(g[1])] = _pairs(g[2])
        elif line.startswith("[IR-context] "):
            g = re.match(r"^\[IR-context\] step=(\d+) facts=\[.*?\] recent=\[(.*?)\] levels=\[(.*?)\] prior=\[(.*)\]$",
                         line)
            log["context"][int(g[1])] = dict(recent=set(g[2].split()), levels=_pairs(g[3], " "), prior=_pairs(g[4]))
        elif (g := TRIG.match(line)):
            step = int(g[1])
            if g[2] != "none":
                log["trig"][step] = (g[2], g[4])
        elif line.startswith("[meta-proj] "):
            log["proj"][step] = re.search(r" projection=(.*)$", line)[1]
        elif line.startswith("[meta-b3] "):
            log["b3"][step] = (int(re.search(r" hold=(\d+)", line)[1]), re.search(r" T_h=(\S+)", line)[1])
        elif (g := META.match(line)):
            log["meta"][int(g[1])] = (_task(g[2] + g[3]), [_task(t) for t in ast.literal_eval(g[4])])
        elif (g := re.match(r"^\[meta\] step=(\d+) all tasks complete$", line)):
            log["meta"][int(g[1])] = None
            log["finished"] = int(g[1])
        elif line.startswith("[hold] ") and f" {robot} start " in line:
            tick, planned = int(re.search(r"step=(\d+)", line)[1]), int(re.search(r" planned=(\d+)", line)[1])
            log["hold_start"][tick] = planned
            log["holds"].append([tick, planned, None])
        elif line.startswith("[hold] ") and f" {robot} end " in line:
            # a hold's end: the line after its start (an interruption is logged before the next hold's start)
            log["holds"][-1][2] = (int(re.search(r"step=(\d+)", line)[1]), int(re.search(r" executed=(\d+)", line)[1]),
                                   " interrupted=True" in line)
        elif (g := BODY.match(line)) and g[2] == robot:
            log["body"][int(g[1])] = dict(task=g[3], action=g[4], micro=g[5])
    return log


def _gate(log, tick):
    """The gates' answers at `tick` the logged values allow, in _clears_gate's order (none(no_human) asked first): one,
    or two where the confidence, logged to 3 decimals, lies within its rounding of θ (below θ, or the answer after)."""
    if log["flags"]["human_aware"] == "off":
        return {"none(no_human)"}
    if log["flags"]["intention_aware"] == "off":
        return {"none(intention_off)"}
    ir = log["ir"][tick]
    confidence = float(ir["confidence"])
    if confidence < log["theta"] - 5e-4:
        return {"none(below_theta)"}
    rest = _gate_at_theta(log, tick)
    return rest | {"none(below_theta)"} if confidence < log["theta"] + 5e-4 else rest


def _gate_at_theta(log, tick):
    ir = log["ir"][tick]
    if ir["adequacy"] == "inadequate":
        return {"none(leader_inadequate)"}
    if ir["adequacy"] != "adequate":
        return {"none(leader_no_observation)"}
    if ir["warrant"].get(ir["leader"]) != "observation":
        return {"none(leader_unwarranted)"}
    if log["rank"][tick].get(ir["leader"]) == "outranked":
        return {"none(leader_outranked)"}
    return {"clears"}


def _holds(log, last):
    """Per tick, the hold the [hold] lines state in progress: (decision tick, planned), and the ticks stood where a
    line states them (the end of a hold run out, the tick before an interruption)."""
    shown, stood = {}, {}
    for start, planned, ended in log["holds"]:
        if ended is None:
            ticks = range(start, last + 1)
        else:
            end, executed, interrupted = ended
            ticks = range(start, end if interrupted else end + 1)
            if ticks:
                stood[ticks[-1]] = executed
        for t in ticks:
            shown[t] = (start, planned)
    return shown, stood


def _ref(task):
    return task.task, {b.parameter: b.value for b in task.bindings}


# =============================================================================
# The test
# =============================================================================

@pytest.mark.parametrize("domain,scenario,changed", CASES)
def test_the_robot_the_page_receives_is_the_logs(domain, scenario, changed, new_files):
    description, updates, lines = _sim_run(domain, scenario, changed)
    (robot,) = description.robots
    log = _read_log(lines, robot.robot)
    last = updates[-1].tick

    # the run description
    assert robot.theta == pytest.approx(log["theta"], abs=5e-4)
    expected_condition = ("human-unaware" if log["flags"]["human_aware"] == "off" else
                          "intention-unaware" if log["flags"]["intention_aware"] == "off" else "intention-aware")
    assert robot.condition.value == expected_condition
    assert (None if robot.known_assigned is None else [t.label for t in robot.known_assigned]) == log["known"]

    start = updates[0].robots[0]
    assert start.belief is None and start.decision is None
    shown, stood = _holds(log, last)
    previous = None
    for update in updates[1:]:
        t, r = update.tick, update.robots[0]

        # the belief
        if t in log["ir"]:
            ir, b = log["ir"][t], r.belief
            live = {h.key: h for h in b.live}
            assert (b.leader or "none") == ir["leader"]
            assert f"{b.confidence:.3f}" == ir["confidence"]
            assert b.lifecycle.value == ir["lifecycle"]
            assert (None if b.finding is None else b.finding.value) == ir["finding"]
            assert (None if b.leader is None else live[b.leader].adequacy.value) == ir["adequacy"]
            assert {k: f"{h.tail:.4f}" for k, h in live.items() if h.tail is not None} == ir["tails"]
            assert {k: h.warrant.value for k, h in live.items()} == ir["warrant"]
            assert {k: h.rank.value for k, h in live.items()} == log["rank"][t]
            context = log["context"].get(t)
            if context is None:
                assert all(h.prior is None for h in b.live) and b.levels == () and b.recent == ()
            else:
                assert {k: f"{h.prior:.4f}" for k, h in live.items()} == context["prior"]
                assert {lv.task: lv.level.value for lv in b.levels} == context["levels"]
                assert set(b.recent) == context["recent"]
        else:
            assert r.belief is None, t

        # the gate at the tick
        if t in log["ir"] or log["flags"]["intention_aware"] == "off":
            assert r.gate_answer.value in _gate(log, t), t

        # the decision
        d = r.decision
        if t in log["trig"]:
            assert d is not None and d.tick == t
            trigger, cause = log["trig"][t]
            assert d.trigger.value == trigger and (None if d.cause is None else d.cause.value) == cause
            reason = log["proj"][t]
            if reason.startswith("built "):
                assert d.gate_answer.value == "clears" and d.projection.kind == "admitted"
                assert d.projection.hypothesis == log["ir"][t]["leader"]
            elif reason.startswith("fallback refused="):
                refused = reason[len("fallback refused="):]
                assert d.projection.kind == "fallback"
                assert d.gate_answer.value == ("clears" if refused == "none(unprojectable)" else refused)
            else:
                assert d.projection.kind == "none" and d.gate_answer.value == reason
            meta = log["meta"][t]
            if meta is None:
                assert d.change.value == "finishes" and d.chosen is None
            else:
                winner, queue = meta
                assert _ref(d.chosen) == winner and [_ref(q) for q in d.queue] == queue
            assert d.hold == log["hold_start"].get(t, 0)
            if t in log["b3"]:
                hold, t_h = log["b3"][t]
                assert d.hold == hold
                if d.projection.kind != "none":
                    assert f"{d.projection.until - t + 1:.2f}" == t_h
            # a projection_expired fires on the first tick the last fallback has run out
            if trigger == "projection_expired":
                assert previous.projection.kind == "fallback"
                assert t == math.ceil(previous.projection.until + 1 - 1e-9)
            previous = d
        else:
            assert d is previous, t

        # the body
        body, line = r.body, log["body"][t]
        assert str(body.microaction) == line["micro"]
        if line["micro"] != "None":
            assert body.action is not None and body.action.action.action == line["action"]
        if line["task"] != "None":
            assert body.task is not None and body.task.task == line["task"]
        assert body.finished == (log["finished"] is not None and t >= log["finished"])
        if t in shown:
            assert body.hold is not None and (body.hold.decided_at, body.hold.planned) == shown[t], t
            if t in stood:
                assert body.hold.stood == stood[t]
        else:
            assert body.hold is None, t

    # the reference runs hold what they are chosen for
    if not changed:
        kinds = {u.robots[0].decision.projection.kind for u in updates[1:] if u.robots[0].decision is not None}
        causes = {u.robots[0].decision.cause for u in updates[1:] if u.robots[0].decision is not None}
        if scenario != "scenario_s10_14":
            assert {"admitted", "fallback"} <= kinds and m.Cause.RETRACTION in causes and log["hold_start"]
        else:
            assert any(r.belief is not None and any(lv.level.value == "raised" for lv in r.belief.levels)
                       for u in updates[1:] for r in u.robots)
