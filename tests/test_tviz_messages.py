# tests/test_tviz_messages.py
"""
T-viz 0.4 (the messages between the web-ui and a simulator): the catalogue, the run description and the tick updates
Mesa's piece (mesa_sim/webui_adapter.py) produces validate against their definitions (webui/messages.py), in both
domains; producing them changes no sim-run (the log pair byte-identical to the same sim-run without); a choice that
cannot be built writes no log pair; webui/ imports no simulator, no domain and nothing of the framework's mind or
world, and names no domain, object type or area id. Each test removes the log files it made, and only those.
"""

import ast
import io
import json
import os
import re
import subprocess
import sys
import tokenize
from pathlib import Path

import pytest

from mesa_sim import webui_adapter
from mesa_sim.run_config import DOMAIN_REGISTRY, RUN_OPTIONS, load_experiment, run_configuration
from mesa_sim.sim_run import LOG_DIR, start_sim_run
from mesa_sim.webui_adapter import MesaSimulator
from shared.types import ScriptDependence, TimelineSource
from webui import messages as m
from webui.simulator import BuildFailed
from world import record as rec

ROOT = Path(__file__).parent.parent
WEBUI = ROOT / "webui"
# One sim-run per domain, with the step count its sweep uses (scenario_s01_01: tb1a's 300; scenario_s03_02: the
# milestone's 800).
RUNS = [("kitting", "scenario_s01_01", 300), ("dock_loading", "scenario_s03_02", 800)]
FIRST_STEPS = 20


def _files():
    return set(os.listdir(LOG_DIR)) if os.path.isdir(LOG_DIR) else set()


@pytest.fixture
def new_files():
    """The log files a test makes: listed after it, then removed."""
    before = _files()
    yield lambda: sorted(_files() - before)
    for name in sorted(_files() - before):
        os.remove(os.path.join(LOG_DIR, name))


@pytest.fixture(scope="module")
def simulator():
    return MesaSimulator()


def _choice(simulator, domain, scenario, steps):
    catalogue = simulator.catalogue()
    entry = next(s for d in catalogue.domains if d.name == domain for s in d.scenarios if s.id == scenario)
    options = tuple(m.CountValue(name=o.name, value=steps) if isinstance(o, m.CountValue) else o
                    for o in catalogue.default_choice.options)
    return m.SimRunChoice(domain=domain, layout=entry.reference_layouts[0], scenario=scenario, options=options)


def _round_trip(message):
    """The message written as JSON and read back against its definition: equal."""
    again = type(message).model_validate_json(message.model_dump_json())
    assert again == message
    return again


# =============================================================================
# The catalogue
# =============================================================================

def test_the_catalogue_validates_and_holds_the_registry_and_the_run_file(simulator):
    catalogue = _round_trip(simulator.catalogue())
    assert [d.name for d in catalogue.domains] == list(DOMAIN_REGISTRY)
    for d in catalogue.domains:
        registry = DOMAIN_REGISTRY[d.name]
        assert [l.id for l in d.layouts] == list(registry["layouts"])
        assert [s.id for s in d.setups] == list(registry["setups"])
        assert [s.id for s in d.scenarios] == list(registry["scenarios"])
        for s in d.scenarios:
            scenario = registry["scenarios"][s.id]
            assert (s.setup, s.reference_layouts) == (scenario.setup, tuple(scenario.reference_layouts))
    assert [o.name for o in catalogue.run_options] == [n for n in RUN_OPTIONS if n not in webui_adapter.TRIPLE]
    run_file = load_experiment(simulator.run_path, {})
    assert (catalogue.default_choice.domain, catalogue.default_choice.scenario) == (run_file["domain"],
                                                                                    run_file["scenario"])
    for declared, value in zip(catalogue.run_options, catalogue.default_choice.options):
        assert value.name == declared.name and value.value == declared.default
        if declared.name in run_file:
            assert declared.default == run_file[declared.name]


def test_every_run_option_has_its_value_in_effect():
    assert set(webui_adapter._EFFECTIVE) == {n for n in RUN_OPTIONS if n not in webui_adapter.TRIPLE}


def test_the_translations_cover_every_member():
    assert set(webui_adapter._OUTCOME) == set(rec.Outcome)
    assert set(webui_adapter._DECISION_REFUSAL) == set(rec.RefusalReason)
    assert set(webui_adapter._UNFIRED) == set(rec.UnfiredReason)
    assert set(webui_adapter._DEPENDENCE) == set(ScriptDependence)
    assert set(webui_adapter._TIMELINE_SOURCE) == set(TimelineSource)


# =============================================================================
# The run description and the tick updates, one sim-run per domain
# =============================================================================

def _check_world(description, update):
    """Every movable object is in exactly one fixed object or carried by one agent."""
    movable = [o.id for o in description.world.movable_objects]
    placed = [oid for c in update.world.fixed_object_contents for oid in c.movable_objects]
    placed += [c.movable_object for c in update.world.carried]
    assert sorted(placed) == sorted(movable)
    fixed = {o.id for o in description.world.fixed_objects}
    assert all(c.fixed_object in fixed for c in update.world.fixed_object_contents)


def _kept_order(before, after):
    """An object that stays in a fixed object keeps its place in the order of arrival."""
    after_of = {c.fixed_object: c.movable_objects for c in after.world.fixed_object_contents}
    for c in before.world.fixed_object_contents:
        now = after_of.get(c.fixed_object, ())
        staying = [oid for oid in c.movable_objects if oid in now]
        assert list(now[:len(staying)]) == staying


@pytest.mark.parametrize("domain, scenario, steps", RUNS)
def test_the_messages_validate_at_build_and_after_each_first_step(simulator, new_files, domain, scenario, steps):
    choice = _choice(simulator, domain, scenario, steps)
    run = simulator.build(choice, "sim-run-1")
    description = _round_trip(run.description)
    assert description.sim_run == "sim-run-1" and description.stated == choice
    start = _round_trip(run.state())
    assert start.tick is None and start.end is None
    # at the start, each fixed object holds its movable objects in the setup's order
    order = [o.id for o in description.world.movable_objects]
    for c in start.world.fixed_object_contents:
        assert list(c.movable_objects) == sorted(c.movable_objects, key=order.index)
    _check_world(description, start)
    before = start
    positions = {a.id: a.position for a in start.world.humans + start.world.robots}
    for k in range(FIRST_STEPS):
        update = _round_trip(run.step())
        assert update.tick == k and update.sim_run == "sim-run-1"
        _check_world(description, update)
        _kept_order(before, update)
        for agent in update.world.humans + update.world.robots:
            p, q = positions[agent.id], agent.position
            if (p.x, p.y) != (q.x, q.y):   # it moved: its last motion is its own step's direction
                n = ((q.x - p.x) ** 2 + (q.y - p.y) ** 2) ** 0.5
                assert (agent.last_motion.x, agent.last_motion.y) == pytest.approx(((q.x - p.x) / n, (q.y - p.y) / n))
            positions[agent.id] = q
        before = update
    ended = _round_trip(run.end(m.EndReason.STEPS_REACHED))
    assert ended.tick == FIRST_STEPS - 1 and ended.end.reason is m.EndReason.STEPS_REACHED
    assert ended.world == before.world
    with pytest.raises(RuntimeError):
        run.step()


@pytest.mark.parametrize("domain, scenario, steps", RUNS)
def test_producing_messages_changes_no_sim_run(simulator, new_files, domain, scenario, steps):
    """The log pair of a headless sim-run and of the same sim-run with messages produced at every step: byte-identical."""
    choice = _choice(simulator, domain, scenario, steps)
    mapping = simulator._configuration(choice)

    headless = start_sim_run(lambda: run_configuration(mapping, "a mapping"))
    for _ in range(steps):
        headless.step()
    headless.end()

    run = simulator.build(choice, "sim-run-1")
    for _ in range(steps):
        run.step()
    run.end(m.EndReason.STEPS_REACHED)

    for suffix in ("log", "rec"):
        a = Path(headless.log.log_path if suffix == "log" else headless.log.rec_path).read_bytes()
        b = Path(run._run.log.log_path if suffix == "log" else run._run.log.rec_path).read_bytes()
        assert a == b and len(a) > 0


def test_a_sim_run_discarded_unstepped_writes_no_file(simulator, new_files):
    run = simulator.build(_choice(simulator, *RUNS[0]), "sim-run-1")
    run.discard()
    assert new_files() == []


# =============================================================================
# A choice that cannot be built
# =============================================================================

def _with(choice, options):
    return choice.model_copy(update={"options": options})


@pytest.mark.parametrize("change", ["undeclared", "wrong_kind", "missing", "twice", "count_below", "bad_one_of",
                                    "unknown_scenario"])
def test_a_choice_that_cannot_be_built_fails_and_writes_no_file(simulator, new_files, change):
    choice = _choice(simulator, *RUNS[0])
    options = choice.options
    if change == "undeclared":
        choice = _with(choice, options + (m.SwitchValue(name="bogus", value=True),))
    elif change == "wrong_kind":
        choice = _with(choice, tuple(m.OneOfValue(name=o.name, value="x") if o.name == "human_aware" else o
                                     for o in options))
    elif change == "missing":
        choice = _with(choice, options[1:])
    elif change == "twice":
        choice = _with(choice, options + options[:1])
    elif change == "count_below":
        choice = _with(choice, tuple(m.CountValue(name=o.name, value=0) if isinstance(o, m.CountValue) else o
                                     for o in options))
    elif change == "bad_one_of":
        choice = _with(choice, tuple(m.OneOfValue(name=o.name, value="greedy") if o.name == "strategy" else o
                                     for o in options))
    else:
        choice = choice.model_copy(update={"scenario": "scenario_s99_99"})
    with pytest.raises(BuildFailed):
        simulator.build(choice, "sim-run-1")
    assert new_files() == []


# =============================================================================
# webui/ is independent of every simulator and every domain
# =============================================================================

FORBIDDEN = ("mesa", "mesa_sim", "mesa_fork", "domains", "shared", "world", "ros_sim", "solara")


def _webui_sources():
    return sorted(WEBUI.rglob("*.py"))


# The page's own files (T-viz 0.3): its code, styles and configuration; not its dependencies, its build output or the
# exported samples (data, git-ignored), nor the lock file (the dependencies' names).
PAGE = WEBUI / "page"
PAGE_SUFFIXES = {".ts", ".tsx", ".mjs", ".js", ".css", ".html", ".json"}
PAGE_SKIPPED = {"node_modules", "dist", "samples"}


def _page_sources():
    return sorted(p for p in PAGE.rglob("*") if p.is_file() and p.suffix in PAGE_SUFFIXES
                  and not PAGE_SKIPPED & set(p.relative_to(PAGE).parts) and p.name != "package-lock.json")


def test_webui_imports_no_simulator_domain_or_framework_module():
    for path in _webui_sources():
        for node in ast.walk(ast.parse(path.read_text())):
            names = ([a.name for a in node.names] if isinstance(node, ast.Import)
                     else [node.module or ""] if isinstance(node, ast.ImportFrom) and node.level == 0 else [])
            for name in names:
                assert name.split(".")[0] not in FORBIDDEN, f"{path.relative_to(ROOT)} imports {name}"


BLOCKED = f"""
import importlib, pkgutil, sys
class Refuse:
    def find_spec(self, name, path=None, target=None):
        if name.split(".")[0] in {FORBIDDEN!r}:
            raise ImportError("refused: " + name)
sys.meta_path.insert(0, Refuse())
import webui
for info in pkgutil.walk_packages(webui.__path__, "webui."):
    importlib.import_module(info.name)
"""


def test_webui_imports_with_every_simulator_domain_and_framework_module_refused():
    done = subprocess.run([sys.executable, "-c", BLOCKED], cwd=ROOT, capture_output=True, text=True)
    assert done.returncode == 0, done.stderr


def _domain_words():
    """Every domain name, object type and area id of the registered layouts and setups."""
    words = set(DOMAIN_REGISTRY)
    for domain in DOMAIN_REGISTRY.values():
        for path in list(domain["layouts"].values()) + list(domain["setups"].values()):
            artefact = json.loads((ROOT / path).read_text())
            words |= {o["type"] for o in artefact.get("env_objects", [])}
            words |= {a["id"] for a in artefact.get("areas", [])}
    return words


def test_webui_names_no_domain_object_type_or_area_id():
    words = _domain_words()
    for path in _webui_sources():
        for token in tokenize.generate_tokens(io.StringIO(path.read_text()).readline):
            if token.type == tokenize.NAME:
                found = {token.string} & words
            elif token.type == tokenize.STRING:
                found = set(ast.literal_eval(token.string).replace(".", " ").replace(",", " ").split()) & words
            else:
                continue
            assert not found, f"{path.relative_to(ROOT)}:{token.start[0]} names {sorted(found)}"


def test_the_page_names_no_domain_object_type_or_area_id():
    words = _domain_words()
    sources = _page_sources()
    assert any(p.suffix == ".tsx" for p in sources)
    for path in sources:
        for number, line in enumerate(path.read_text().splitlines(), 1):
            found = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", line)) & words
            assert not found, f"{path.relative_to(ROOT)}:{number} names {sorted(found)}"
