"""
tests/test_tviz_paths.py

T-viz 1d and 1e, the paths on the floor: what the page receives of what lies ahead agrees with the sim-run, on reference
sim-runs of both domains (kitting scenario_s05_02 and dock_loading scenario_s07_07 with the default run file's options;
kitting scenario_s05_02 intention-unaware; dock_loading scenario_s07_07 human-unaware; kitting scenario_s09_13, a cut
into a carry and its resumption, the robot idle).

1. Each walk ahead starts at the agent (the first) or where the walk before it stops, and ends at the target of its walk
   action: within the `at` radius of the target's position at the tick, on the straight line from its start toward it.
2. The human's walks ahead at a tick agree with where the human walks in the following ticks (the run log's positions):
   while the task on top runs on (no transition in the record stream), every position lies on the walks, in order; when
   the task on top then completes, the human has reached the last walk's end. The robot's likewise, while its plan runs
   on (until its next decision), the end reached when its task completes.
3. The robot's projection ahead belongs to the decision the run log states last: its kind is the log's ([meta-proj]:
   built is admitted, fallback, none), its last part ends at decision - 1 + T_h ([meta-b3]), and something lies ahead
   exactly while that end is after the tick. Human-unaware: nothing ahead; intention-unaware: no admitted projection.

The log and the record stream are read independently of the piece.
"""

import math
import os
import re
from pathlib import Path

import pytest

from mesa_sim.sim_run import LOG_DIR
from mesa_sim.webui_adapter import MesaSimulator
from mesa_sim.world_state_builder import PROXIMITY_THRESHOLD
from webui import messages as m

ROOT = Path(__file__).parent.parent
MARGIN = 5          # ticks run past the point where every agent has finished
MAX_STEPS = 1000
ON_PATH = 0.02      # the log prints positions to 2 decimals
AT_END = 0.02

# (domain, scenario, run options changed from the default run file's)
# (domain, scenario, run options changed from the default run file's, the kinds of projection the run log states)
CASES = [
    ("kitting", "scenario_s05_02", {}, {"admitted", "fallback"}),
    ("dock_loading", "scenario_s07_07", {}, {"admitted", "fallback"}),
    ("kitting", "scenario_s05_02", {"intention_aware": False}, {"fallback"}),
    ("dock_loading", "scenario_s07_07", {"human_aware": False}, {"none"}),
    ("kitting", "scenario_s09_13", {}, {"fallback"}),
]


def _files():
    return set(os.listdir(LOG_DIR)) if os.path.isdir(LOG_DIR) else set()


@pytest.fixture
def new_files():
    before = _files()
    yield
    for name in sorted(_files() - before):
        os.remove(os.path.join(LOG_DIR, name))


def _sim_run(domain, scenario, changed):
    """The sim-run through the piece to MARGIN ticks past the point where every agent has finished: its description,
    its tick updates (the start's first), its log's lines and its record stream's lines."""
    simulator = MesaSimulator()
    catalogue = simulator.catalogue()
    entry = next(s for d in catalogue.domains if d.name == domain for s in d.scenarios if s.id == scenario)
    options = tuple(o.model_copy(update={"value": changed[o.name]}) if o.name in changed else o
                    for o in catalogue.default_choice.options)
    side = simulator.build(m.SimRunChoice(domain=domain, layout=entry.reference_layouts[0], scenario=scenario,
                                          options=options), "paths")
    updates = [side.state()]
    for _ in range(MAX_STEPS):
        updates.append(side.step())
        finished = updates[-1].run.finished_at
        if finished is not None and updates[-1].tick >= finished + MARGIN:
            break
    path = side._run.log.log_path
    side.end(m.EndReason.RESET)
    with open(path) as f, open(path[:-len(".log")] + ".rec") as r:
        return side.description, updates, f.read().splitlines(), r.read().splitlines()


# =============================================================================
# The log and the record stream, read on their own
# =============================================================================

POS = re.compile(r"^  step: (\d+): \[(\w+)\] .* pos=\[\s*(\S+)\s+(\S+?)\s*\]")
REC = re.compile(r"^\[rec\] step=(\d+) stack=(\S+) .* events=(\S+)$")
TRIG = re.compile(r"^\[meta-trig\] step=(\d+) trigger=(\w+)")


def _read(lines, rec_lines, robot):
    log = dict(pos={}, decisions={}, proj={}, t_h={}, complete=set())
    step = None
    for line in lines:
        if (g := POS.match(line)):
            log["pos"][(int(g[1]), g[2])] = (float(g[3]), float(g[4]))
        elif (g := TRIG.match(line)):
            step = int(g[1])
            if g[2] != "none":
                log["decisions"][step] = g[2]
        elif line.startswith("[meta-proj] "):
            log["proj"][step] = re.search(r" projection=(\w+)", line)[1]
        elif line.startswith("[meta-b3] "):
            t_h = re.search(r" T_h=(\S+)", line)[1]
            if t_h != "None":
                log["t_h"][step] = float(t_h)
    rec = {}
    for line in rec_lines:
        if (g := REC.match(line)):
            rec[int(g[1])] = (g[2], g[3])
    return log, rec


# =============================================================================
# Geometry
# =============================================================================

def _xy(p):
    return p.x, p.y


def _along(point, walks, since):
    """The first arc position on the walks' polyline, not before `since`, at which `point` lies (within ON_PATH), or
    None; and the polyline's length. A walk may go back along the one before it, so the polyline is followed forward."""
    found, done = None, 0.0
    for w in walks:
        (ax, ay), (bx, by) = _xy(w.start), _xy(w.end)
        length = math.hypot(bx - ax, by - ay)
        k = 0.0 if length == 0 else max(0.0, min(1.0, ((point[0] - ax) * (bx - ax) + (point[1] - ay) * (by - ay))
                                                 / length ** 2))
        arc = done + k * length
        if found is None and arc >= since - ON_PATH and math.hypot(ax + k * (bx - ax) - point[0],
                                                                   ay + k * (by - ay) - point[1]) <= ON_PATH:
            found = arc
        done += length
    return found, done


def _target_position(target, update, description):
    """Where `target` is at the tick: a fixed object's position; a movable object's container's, or its holder's."""
    world = description.world
    fixed = {f.id: _xy(f.position) for f in world.fixed_objects}
    if target in fixed:
        return fixed[target]
    agents = {a.id: _xy(a.position) for a in update.world.humans + update.world.robots}
    for c in update.world.carried:
        if c.movable_object == target:
            return agents[c.agent]
    for c in update.world.fixed_object_contents:
        if target in c.movable_objects:
            return fixed[c.fixed_object]
    raise AssertionError(f"{target} is nowhere at tick {update.tick}")


def _check_chain(walks, start, update, description, who):
    """Point 1: the first walk starts at the agent, each next one where the one before stops; each ends at its target."""
    expected = start
    for w in walks:
        assert math.dist(_xy(w.start), expected) < 1e-6, (who, update.tick, w)
        target = _target_position(w.target, update, description)
        end, begin = _xy(w.end), _xy(w.start)
        assert math.dist(end, target) <= PROXIMITY_THRESHOLD + 1e-6, (who, update.tick, w, target)
        assert math.dist(begin, target) > PROXIMITY_THRESHOLD, (who, update.tick, w, "a walk with no step")
        # on the straight line from the start toward the target
        (sx, sy), (ex, ey), (tx, ty) = begin, end, target
        cross = (ex - sx) * (ty - sy) - (ey - sy) * (tx - sx)
        assert abs(cross) / math.dist(begin, target) < 1e-6, (who, update.tick, w, target)
        expected = end


def _check_followed(walks, tick, positions, until, completes, who):
    """Point 2: from `tick` + 1 to `until` - 1 every position lies on the walks, in order; if `completes`, the last of them
    is the walks' end."""
    if not walks:
        return 0
    last_arc, total, checked = 0.0, 0.0, 0
    for t in range(tick + 1, until):
        if t not in positions:
            break
        arc, total = _along(positions[t], walks, last_arc)
        assert arc is not None, (who, tick, t, positions[t], "off the walks ahead, or back along them")
        last_arc, checked = arc, checked + 1
    if completes and checked:
        assert abs(total - last_arc) <= AT_END, (who, tick, until, "the walks' end not reached")
    return checked


# =============================================================================
# The test
# =============================================================================

@pytest.mark.parametrize("domain,scenario,changed,stated", CASES)
def test_the_paths_the_page_receives_agree_with_the_run(domain, scenario, changed, stated, new_files):
    description, updates, lines, rec_lines = _sim_run(domain, scenario, changed)
    (human,) = [h.id for h in description.world.humans]
    (robot,) = [r.id for r in description.world.robots]
    log, rec = _read(lines, rec_lines, robot)
    condition = description.robots[0].condition
    ticks = [u for u in updates if u.tick is not None]
    last = ticks[-1].tick
    human_pos = {t: p for (t, a), p in log["pos"].items() if a == human}
    robot_pos = {t: p for (t, a), p in log["pos"].items() if a == robot}
    decisions = sorted(log["decisions"])
    followed = {"human": 0, "robot": 0}
    kinds = set()

    for u in ticks:
        t = u.tick
        # --- the human's real path -------------------------------------------------------------------------------
        (hw,) = [w for w in u.world.walks_ahead if w.human == human]
        here = {a.id: _xy(a.position) for a in u.world.humans + u.world.robots}
        assert math.dist(here[human], human_pos[t]) <= ON_PATH and math.dist(here[robot], robot_pos[t]) <= ON_PATH, t
        _check_chain(hw.walks, here[human], u, description, "human")
        # the task on top runs on until the next tick with a transition in the record stream
        after = next((v for v in range(t + 1, last + 1) if rec.get(v, ("", "-"))[1] != "-"), last + 1)
        top = rec[t][0].split(";")[0]
        completes = after <= last and f"completed:{top}" in rec[after][1].split(",")
        followed["human"] += _check_followed(hw.walks, t, human_pos, after, completes, "human")

        # --- the robot's own plan --------------------------------------------------------------------------------
        r = next(r for r in u.robots if r.robot == robot)
        _check_chain(r.walks_ahead, here[robot], u, description, "robot")
        nxt = next((d for d in decisions if d > t), last + 1)
        completes = nxt <= last and log["decisions"][nxt] == "no_current_task"
        followed["robot"] += _check_followed(r.walks_ahead, t, robot_pos, nxt, completes, "robot")

        # --- the robot's expectation of the human ----------------------------------------------------------------
        made = [d for d in decisions if d <= t]
        if not made:
            assert r.decision is None and r.projection_ahead == (), t
            continue
        d = made[-1]
        assert r.decision is not None and r.decision.tick == d, (t, d)
        kind = {"built": "admitted", "fallback": "fallback"}.get(log["proj"].get(d), "none")
        assert r.decision.projection.kind == kind, (t, d, log["proj"].get(d))
        kinds.add(kind)
        if kind == "none" or d not in log["t_h"]:
            assert r.projection_ahead == () or kind != "none", (t, d)
            continue
        end = d - 1 + log["t_h"][d]
        assert bool(r.projection_ahead) == (end > t + 0.005) or abs(end - t) <= 0.005, (t, d, end)
        if r.projection_ahead:
            assert abs(r.projection_ahead[-1].until - end) <= 0.005, (t, d, end, r.projection_ahead[-1])
            assert all(p.until > t for p in r.projection_ahead), (t, d)

    assert kinds == stated, kinds
    if condition is m.RobotCondition.HUMAN_UNAWARE:
        assert all(r.projection_ahead == () for u in ticks for r in u.robots)
    if condition is m.RobotCondition.INTENTION_UNAWARE:
        assert "admitted" not in kinds
    # each reading was exercised on this sim-run (the robot's where it has tasks: the IRB's robot is idle)
    assert followed["human"] > 0 and (followed["robot"] > 0) == bool(description.robots[0].assigned), followed
