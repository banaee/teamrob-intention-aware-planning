"""
tests/test_tviz_server.py

T-viz 1a, increment (i): the web-ui's server and its start (webui/server.py, mesa_sim/run_webui.py), the log pair of a
web-ui sim-run (mesa_sim/sim_run.py) and the point where all agents have finished (mesa_sim/webui_adapter.py).
docs/handoffs/plan_T-viz_1a.md, sections 2 (i) and 7.

- Test 1: a sim-run through the server, started as its own process and driven over HTTP, writes the same log pair as
  the headless start of the same run file and flags; one sim-run per domain.
- A sim-run without a step limit, reset at tick k, equals the headless start of k steps but for the start line's
  `steps=` field.
- The thread filter: a web-ui log pair takes the lines of its own thread only.
- The point where all agents have finished is the tick of the robot's empty-pool line or of the human's last tick
  with a task, whichever is later, read from the sim-run's own log pair.
- The start refuses what the page cannot show.
- The view (T-viz 1a (ii)): refused while a stepped sim-run is current.
- Test 2 (T-viz 1a (iv); plan section 7): a domain the web-ui has never seen, under a new name, with dock_loading's
  content and no scene appearance of its own, is listed by the catalogue with the default appearance and builds and
  steps through the server. Its limit (P15): the new domain's object types and area ids are dock_loading's; that the
  web-ui's code names none is the domain-word scan's (tests/test_tviz_messages.py).
"""

import json
import logging
import os
import re
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from mesa_sim.run_webui import read_start
from mesa_sim.sim_run import LOG_DIR, RunLog
from webui import messages as m

ROOT = Path(__file__).parent.parent
PYTHON = sys.executable
# One sim-run per domain, with the steps 0.4's check 3 used (scenario_s01_01: tb1a's 300; scenario_s03_02: the
# milestone's 800).
RUNS = [("kitting", "scenario_s01_01", 300), ("dock_loading", "scenario_s03_02", 800)]


def _files():
    return set(os.listdir(LOG_DIR)) if os.path.isdir(LOG_DIR) else set()


@pytest.fixture
def new_files():
    """The log files a test makes: listed after it, then removed."""
    before = _files()
    yield lambda: sorted(_files() - before)
    for name in sorted(_files() - before):
        os.remove(os.path.join(LOG_DIR, name))


def _pair(names):
    """The one log pair among `names`, read: (.log text, .rec text)."""
    logs = [n for n in names if n.endswith(".log")]
    assert len(logs) == 1, names
    stem = os.path.join(LOG_DIR, logs[0][:-4])
    return Path(stem + ".log").read_text(), Path(stem + ".rec").read_text()


def _env():
    return dict(os.environ, PYTHONHASHSEED="0", PYTHONPATH=str(ROOT))


def _headless(args):
    done = subprocess.run([PYTHON, "mesa_sim/run_mesa.py", *args], cwd=ROOT, env=_env(), capture_output=True)
    assert done.returncode == 0, done.stderr.decode()[-2000:]


class _Server:
    """The web-ui's server as its own process, from the start's own reading of the command line (read_start), the page
    not served (an API-only server: the test reads no page)."""

    def __init__(self, args, prelude=""):
        with socket.socket() as s:
            s.bind(("127.0.0.1", 0))
            self.port = s.getsockname()[1]
        code = (prelude + "from mesa_sim.run_webui import read_start; from webui.server import serve; "
                "simulator, port = read_start(%r); serve(simulator, port, None)" % ([*args, "--port", str(self.port)],))
        self.process = subprocess.Popen([PYTHON, "-c", code], cwd=ROOT, env=_env(), stderr=subprocess.PIPE)
        for _ in range(200):
            try:
                self.get("current")
                return
            except (urllib.error.URLError, ConnectionError):
                time.sleep(0.05)
        raise RuntimeError("the server did not start: " + self.process.stderr.read().decode())

    def _ask(self, path, body=None):
        request = urllib.request.Request("http://127.0.0.1:%d/api/%s" % (self.port, path),
                                         data=None if body is None else body.encode(),
                                         headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(request) as answer:
                return answer.status, answer.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()

    def get(self, path):
        return self._ask(path)

    def post(self, path, message):
        return self._ask(path, message.model_dump_json())

    def stop(self):
        self.process.terminate()
        self.process.wait(timeout=30)


@pytest.fixture
def server():
    started = []

    def start(*args, prelude=""):
        started.append(_Server(args, prelude))
        return started[-1]
    yield start
    for s in started:
        s.stop()


def _choose(server, choice):
    status, body = server.post("choose", choice)
    assert status == 200, body
    return m.SimRunState.model_validate_json(body)


def _with_limit(choice, limit):
    return choice.model_copy(update={"options": tuple(
        m.LimitValue(name=o.name, value=limit) if isinstance(o, m.LimitValue) else o for o in choice.options)})


# =============================================================================
# Test 1
# =============================================================================

@pytest.mark.parametrize("domain,scenario,steps", RUNS)
def test_a_sim_run_through_the_server_writes_the_headless_log_pair(server, new_files, domain, scenario, steps):
    args = ["--domain", domain, "--scenario", scenario, "--steps", str(steps)]
    _headless(args)
    headless = _pair(new_files())
    known = set(new_files())

    web = server(*args)
    status, body = web.get("catalogue")
    catalogue = m.Catalogue.model_validate_json(body)
    state = _choose(web, catalogue.default_choice)
    assert (state.description.run.domain, state.description.run.scenario) == (domain, scenario)
    ref = m.SimRunRef(sim_run=state.description.sim_run)
    updates = [state.tick]
    for k in range(steps):
        status, body = web.post("step", ref)
        assert status == 200, body
        update = m.TickUpdate.model_validate_json(body)
        assert update.tick == k
        assert (update.end is None) == (k < steps - 1)
        updates.append(update)
    assert update.end.reason == m.EndReason.STEPS_REACHED
    status, body = web.post("step", ref)
    assert status == 409 and m.StepRefusal.model_validate_json(body).reason == m.StepRefusalReason.ENDED
    # current answers with every tick update the sim-run gave, the start's first (T-viz 1a (iii), M3)
    history = m.Current.model_validate_json(web.get("current")[1]).state
    assert history.description == state.description and list(history.ticks) == updates
    web.stop()
    assert _pair(sorted(set(new_files()) - known)) == headless


def test_a_sim_run_reset_at_tick_k_is_the_headless_run_of_k_steps(server, new_files):
    domain, scenario, k = "kitting", "scenario_s01_01", 37
    _headless(["--domain", domain, "--scenario", scenario, "--steps", str(k)])
    headless = _pair(new_files())
    known = set(new_files())

    web = server("--domain", domain, "--scenario", scenario)
    catalogue = m.Catalogue.model_validate_json(web.get("catalogue")[1])
    state = _choose(web, catalogue.default_choice)
    ref = m.SimRunRef(sim_run=state.description.sim_run)
    for _ in range(k):
        assert web.post("step", ref)[0] == 200
    status, body = web.post("reset", ref)
    again = m.SimRunState.model_validate_json(body)
    assert status == 200 and again.tick.tick is None and again.description.sim_run != ref.sim_run
    assert web.post("step", ref)[0] == 409       # the reset sim-run is no longer current
    web.stop()
    log, rec = _pair(sorted(set(new_files()) - known))
    first, rest = log.split("\n", 1)
    h_first, h_rest = headless[0].split("\n", 1)
    assert first == h_first.replace("steps=%d" % k, "steps=none")
    assert (rest, rec) == (h_rest, headless[1])


def test_the_server_answers_current_and_refuses_what_it_cannot_do(server, new_files):
    web = server("--domain", "kitting", "--scenario", "scenario_s01_01", "--steps", "3")
    assert m.Current.model_validate_json(web.get("current")[1]).state is None
    catalogue = m.Catalogue.model_validate_json(web.get("catalogue")[1])
    limits = [o for o in catalogue.run_options if isinstance(o, m.LimitOption)]
    assert [o.default for o in limits] == [3]
    bad = catalogue.default_choice.model_copy(update={"scenario": "scenario_s99_99"})
    status, body = web.post("choose", bad)
    assert status == 422 and m.BuildFailure.model_validate_json(body).message
    state = _choose(web, catalogue.default_choice)
    current = m.Current.model_validate_json(web.get("current")[1]).state
    assert current.description == state.description and current.ticks == (state.tick,)
    assert web.post("step", m.SimRunRef(sim_run="sim-run-0"))[0] == 409
    web.stop()
    assert new_files() == []      # a sim-run never stepped writes no file, at a choice or at the server's stop


def test_a_view_is_refused_while_a_stepped_sim_run_is_current(server, new_files):
    """The view (T-viz 1a (ii)): it discards an unstepped sim-run and is the current view until a choice replaces it;
    refused while a stepped sim-run is current; one that cannot be produced changes nothing."""
    web = server("--domain", "kitting", "--scenario", "scenario_s01_01")
    catalogue = m.Catalogue.model_validate_json(web.get("catalogue")[1])
    state = _choose(web, catalogue.default_choice)
    run = state.description.run
    view_choice = m.ViewChoice(domain=run.domain, layout=run.layout, setup=run.setup)
    status, body = web.post("view", view_choice)
    assert status == 200
    view = m.LayoutView.model_validate_json(body)
    assert view.setup.movable_objects == state.description.world.movable_objects
    current = m.Current.model_validate_json(web.get("current")[1])
    assert current.state is None and current.view == view          # the unstepped sim-run discarded
    status, body = web.post("view", m.ViewChoice(domain=run.domain, layout="no_layout", setup=None))
    assert status == 422 and m.BuildFailure.model_validate_json(body).message
    assert m.Current.model_validate_json(web.get("current")[1]).view == view      # nothing changed

    state = _choose(web, catalogue.default_choice)
    assert m.Current.model_validate_json(web.get("current")[1]).view is None
    assert web.post("step", m.SimRunRef(sim_run=state.description.sim_run))[0] == 200
    status, body = web.post("view", view_choice)
    assert status == 409 and m.ViewRefusal.model_validate_json(body).sim_run == state.description.sim_run
    assert m.Current.model_validate_json(web.get("current")[1]).state.description == state.description
    web.stop()
    assert len(new_files()) == 2      # the stepped sim-run's pair, ended at the server's stop


# =============================================================================
# Test 2: a domain the web-ui has never seen
# =============================================================================

UNSEEN = "unseen_domain"
# The registry of the server's process gains the new domain before its start reads it: dock_loading's content under a
# name no file of the web-ui, and no domains/<name>/appearance.json, knows.
UNSEEN_PRELUDE = ("from mesa_sim import run_config; "
                  "run_config.DOMAIN_REGISTRY[%r] = dict(run_config.DOMAIN_REGISTRY['dock_loading']); " % UNSEEN)


def test_a_domain_the_web_ui_has_never_seen_is_listed_built_and_stepped(server, new_files):
    from webui.appearance import Appearance
    assert not (ROOT / "domains" / UNSEEN).exists()
    web = server("--domain", UNSEEN, "--scenario", "scenario_s03_02", prelude=UNSEEN_PRELUDE)
    catalogue = m.Catalogue.model_validate_json(web.get("catalogue")[1])
    entry = next(d for d in catalogue.domains if d.name == UNSEEN)
    assert entry.appearance == Appearance()                 # drawn from the defaults
    assert catalogue.default_choice.domain == UNSEEN
    state = _choose(web, catalogue.default_choice)
    assert state.description.run.domain == UNSEEN
    ref = m.SimRunRef(sim_run=state.description.sim_run)
    for k in range(20):
        status, body = web.post("step", ref)
        assert status == 200 and m.TickUpdate.model_validate_json(body).tick == k
    view = web.post("view", m.ViewChoice(domain=UNSEEN, layout=state.description.run.layout, setup=None))
    assert view[0] == 409                                   # the choices are locked after the first step
    web.stop()
    assert len(new_files()) == 2                            # its log pair, ended at the server's stop


# =============================================================================
# The thread filter
# =============================================================================

def test_a_web_ui_log_pair_takes_only_its_own_threads_lines(new_files):
    log = RunLog(echo=False, own_thread_only=True)
    try:
        logging.info("on the sim-run's thread")
        other = threading.Thread(target=lambda: logging.info("on another thread"))
        other.start()
        other.join()
        log.open()
        logging.info("again on the sim-run's thread")
    finally:
        log.close()
    assert Path(log.log_path).read_text() == "on the sim-run's thread\nagain on the sim-run's thread\n"


# =============================================================================
# The point where all agents have finished
# =============================================================================

# tb1a's eight sim-runs with their sweep's steps (analysis/kitting/tb1a_destination/sweep.sh), assignment knowledge
# on, context knowledge off.
TB1A = [("env_layout_01", "scenario_s01_01", 300), ("env_layout_02", "scenario_s02_01", 450),
        ("env_layout_03", "scenario_s03_01", 300), ("env_layout_04", "scenario_s01_06", 200),
        ("env_layout_05", "scenario_s04_01", 400), ("env_layout_06", "scenario_s03_06", 300),
        ("env_layout_07", "scenario_s05_01", 300), ("env_layout_07", "scenario_s05_02", 300)]


def finished_point(log: str, rec: str):
    """The point MPB-5 names, read from a sim-run's log pair: the tick of the robot's `[meta] step=N all tasks
    complete` line or the first tick from which the human's stack stays empty, whichever is later; None when either is
    not reached."""
    meta = [int(x) for x in re.findall(r"^\[meta\] step=(\d+) all tasks complete$", log, re.M)]
    ticks = [(int(t), stack) for t, stack in re.findall(r"^\[rec\] step=(\d+) stack=(\S+)", rec, re.M)]
    busy = [t for t, stack in ticks if stack != "-"]
    human_end = (max(busy) + 1) if busy else 0
    if not meta or human_end > ticks[-1][0]:
        return None
    return max(meta[0], human_end)


@pytest.mark.parametrize("layout,scenario,steps", TB1A)
def test_finished_at_is_the_point_the_log_pair_shows(new_files, layout, scenario, steps):
    from mesa_sim.webui_adapter import MesaSimulator
    simulator = MesaSimulator()
    catalogue = simulator.catalogue()
    options = tuple(m.LimitValue(name=o.name, value=steps) if isinstance(o, m.LimitValue)
                    else m.SwitchValue(name=o.name, value=False) if o.name == "context_knowledge" else o
                    for o in catalogue.default_choice.options)
    side = simulator.build(m.SimRunChoice(domain="kitting", layout=layout, scenario=scenario, options=options), "t")
    seen = []
    for _ in range(steps):
        seen.append(side.step().run.finished_at)
    side.end(m.EndReason.STEPS_REACHED)
    log, rec = _pair(new_files())
    point = finished_point(log, rec)
    assert seen[-1] == point
    if point is not None:       # None before the point, the point from it on
        assert seen[:point] == [None] * point and set(seen[point:]) == {point}


# =============================================================================
# The start
# =============================================================================

def test_the_start_refuses_what_the_page_cannot_show():
    with pytest.raises(SystemExit, match="overrides"):
        read_start(["--override", "layout.shelf_2.position=-300,-300"])
    with pytest.raises(SystemExit, match="reference layouts"):
        read_start(["--domain", "kitting", "--scenario", "scenario_s01_01", "--layout", "env_layout_02"])
    simulator, port = read_start(["--domain", "dock_loading", "--scenario", "scenario_s03_02", "--port", "8123"])
    choice = simulator.catalogue().default_choice
    assert (port, choice.domain, choice.scenario) == (8123, "dock_loading", "scenario_s03_02")
    assert [o.value for o in choice.options if isinstance(o, m.LimitValue)] == [None]
