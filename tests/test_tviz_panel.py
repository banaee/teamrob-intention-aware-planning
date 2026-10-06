"""
tests/test_tviz_panel.py

T-viz 1a (iv), panel 4a's second part: the human's script and the tag per task.

- The fixtures of the page's script test (tests/tviz_panel_cases.py, tests/fixtures/tviz_panel/) are what the piece
  gives now: the human activity of panel 4a's four reference cases and the executor's state of every script line.
- The tag the page receives (the tick update's `tag`, world/tag.py through the piece) equals the analysis reader's
  (analysis/instruments/mpb/tag.py, from the sim-run's own log pair) on every stretch of four scenarios with a timeline
  fact, one per domain for each of "in accord" and "not in accord"; "no fact" among them.
"""

import importlib.util
import json
import os
from pathlib import Path

import pytest

from mesa_sim.action_decomposer import _parse_duration_to_steps
from mesa_sim.sim_run import LOG_DIR
from mesa_sim.webui_adapter import MesaSimulator
from tests import tviz_panel_cases as cases
from webui import messages as m

ROOT = Path(__file__).parent.parent


def _files():
    return set(os.listdir(LOG_DIR)) if os.path.isdir(LOG_DIR) else set()


@pytest.fixture
def new_files():
    before = _files()
    yield lambda: sorted(_files() - before)
    for name in sorted(_files() - before):
        os.remove(os.path.join(LOG_DIR, name))


@pytest.mark.parametrize("name,domain,scenario", cases.CASES)
def test_the_script_fixtures_are_what_the_piece_gives(name, domain, scenario):
    made = json.loads(json.dumps(cases.run_case(domain, scenario)))
    assert made == json.loads((cases.FIXTURES / f"{name}.json").read_text())


def _reader():
    spec = importlib.util.spec_from_file_location("tag_reader", ROOT / "analysis" / "instruments" / "mpb" / "tag.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Scenarios with a timeline fact (their own window of break_time): one stretch "in accord" and one "not in accord"
# per domain (found with the reader on T-F part 1's and T-K step 6's runs).
TAGGED = [("kitting", "scenario_s10_14"), ("kitting", "scenario_s10_12"),
          ("dock_loading", "scenario_s05_16"), ("dock_loading", "scenario_s03_04")]


def test_the_tag_the_page_receives_is_the_analysis_readers(new_files):
    reader = _reader()
    simulator = MesaSimulator()
    catalogue = simulator.catalogue()
    values = set()
    for domain, scenario in TAGGED:
        entry = next(s for d in catalogue.domains if d.name == domain for s in d.scenarios if s.id == scenario)
        side = simulator.build(m.SimRunChoice(domain=domain, layout=entry.reference_layouts[0], scenario=scenario,
                                              options=catalogue.default_choice.options), "tagged")
        model = side._model
        human = side.description.world.humans[0].id
        assert model.timeline.windows, f"{scenario} has no timeline fact"
        tags = {}
        for _ in range(cases.MAX_STEPS):
            update = side.step()
            activity = next(a for a in update.world.activity if a.human == human)
            tags[update.tick] = activity.tag
            if update.run.finished_at is not None:
                break
        known = set(new_files())
        side.end(m.EndReason.RESET)
        log = next(n for n in new_files() if n.endswith(".log"))
        stem = Path(LOG_DIR) / log[:-4]
        recency = {e.task.name: _parse_duration_to_steps(e.recency.duration, model)
                   for e in model.declared_context.entries() if e.recency is not None}
        stretches, done = reader.record(f"{stem}.rec")
        world = reader.World(domain, f"{stem}.log", done, recency)
        assert stretches
        for task, a, b in stretches:
            tag, raised, lowered = world.tag(task, a)
            for t in range(a, b):
                if t not in tags:
                    continue                      # after the last tick stepped
                got = tags[t]
                assert got is not None and (got.tag.value, got.since) == (tag, a), (scenario, task, t, got, tag)
                assert (list(got.raised), list(got.lowered)) == (raised, lowered), (scenario, task, t)
            values.add(tag)
        for n in sorted(set(new_files()) - known) + [log, log[:-4] + ".rec"]:
            if os.path.exists(os.path.join(LOG_DIR, n)):
                os.remove(os.path.join(LOG_DIR, n))
    assert values == {"in accord", "not in accord", "no fact"}
