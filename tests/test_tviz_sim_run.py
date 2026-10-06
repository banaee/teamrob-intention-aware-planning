# tests/test_tviz_sim_run.py
"""
T-viz 0.2 (the code structure): the run configuration from a mapping is checked as a run
file's is; the flags are the run options; two sim-runs in one process get their own log
pairs; a sim-run built and never stepped leaves no file; a failed start writes its pair;
the headless start imports neither Solara nor the solara-ui's modules. Each test removes
the log files it made, and only those.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from mesa_sim.run_config import (RUN_OPTIONS, build_model, load_experiment, parse_user_args,
                                 run_configuration)
from mesa_sim.sim_model import SimModel
from mesa_sim.sim_run import LOG_DIR, RunLog, start_sim_run

ROOT = Path(__file__).parent.parent
RUN = {"domain": "kitting", "scenario": "scenario_s01_01", "steps": 2, "assignment_knowledge": True,
       "context_knowledge": False}


def _files():
    return set(os.listdir(LOG_DIR)) if os.path.isdir(LOG_DIR) else set()


@pytest.fixture
def new_files():
    """The log files a test makes: listed after it, then removed."""
    before = _files()
    yield lambda: sorted(_files() - before)
    for name in sorted(_files() - before):
        os.remove(os.path.join(LOG_DIR, name))


def test_the_flags_are_the_run_options():
    dests = list(vars(parse_user_args([])))
    assert tuple(d for d in dests if d not in ("run", "override")) == RUN_OPTIONS


@pytest.mark.parametrize("stated", [
    {"bogus_key": 1},
    {"strategy": "greedy"},
    {"context_knowledge": "false"},
    {"test_level": 1.0},
    {"overrides": {"layout.nowhere.position": [1, 2]}},
])
def test_a_stated_configuration_is_refused_as_the_run_file_is(tmp_path, stated):
    path = tmp_path / "run.yaml"
    path.write_text(yaml.safe_dump({**RUN, **stated}))
    with pytest.raises(Exception) as from_file:
        build_model(load_experiment(str(path), {}))
    with pytest.raises(Exception) as from_mapping:
        build_model(run_configuration({**RUN, **stated}, str(path)))
    assert type(from_file.value) is type(from_mapping.value)
    assert str(from_file.value) == str(from_mapping.value)


def test_a_stated_configuration_builds_the_run_files_model(tmp_path):
    path = tmp_path / "run.yaml"
    path.write_text(yaml.safe_dump(RUN))
    stated = run_configuration(RUN, "a mapping")
    assert stated == load_experiment(str(path), {})
    assert isinstance(build_model(stated), SimModel)


def _start(scenario):
    return start_sim_run(lambda: run_configuration({**RUN, "scenario": scenario}, "a mapping"))


def _starts(path):
    return [l for l in open(path) if l.startswith("[run_mesa] Starting")]


def test_two_sim_runs_one_after_the_other_get_their_own_log_pairs(new_files):
    first = _start("scenario_s01_01")
    for _ in range(2):
        first.step()
    first.end()
    second = _start("scenario_s01_06")
    for _ in range(2):
        second.step()
    second.end()
    assert first.log.log_path != second.log.log_path and first.log.rec_path != second.log.rec_path
    assert len(new_files()) == 4
    assert [l.split("scenario=")[1].split()[0] for l in _starts(first.log.log_path)] == ["scenario_s01_01"]
    assert [l.split("scenario=")[1].split()[0] for l in _starts(second.log.log_path)] == ["scenario_s01_06"]
    assert open(first.log.log_path).read().rstrip("\n").endswith("[run_mesa] Headless run complete.")
    assert all(open(p).read() for p in (first.log.rec_path, second.log.rec_path))


def test_a_sim_run_left_unended_keeps_its_own_pair(new_files):
    first = _start("scenario_s01_01")
    first.step()
    first_lines = open(first.log.log_path).read()
    second = _start("scenario_s01_06")   # closes the first's pair where it stands
    second.step()
    second.end()
    assert open(first.log.log_path).read() == first_lines
    assert "scenario_s01_06" not in first_lines
    assert len(new_files()) == 4


def test_a_sim_run_never_stepped_leaves_no_file(new_files):
    _start("scenario_s01_01")
    _start("scenario_s01_06")           # the first, never stepped, is closed unopened
    _start("scenario_s01_01").close()
    assert new_files() == []


def test_a_failed_start_writes_its_pair(new_files):
    with pytest.raises(ValueError, match="Unknown scenario"):
        _start("scenario_nope")
    made = new_files()
    assert len(made) == 2 and all(os.path.getsize(os.path.join(LOG_DIR, f)) == 0 for f in made)


def test_a_log_pair_takes_a_suffix_when_its_name_is_taken(new_files):
    first = RunLog()
    first.open()
    second = RunLog()                    # closes the first
    second.open()
    assert first.log_path != second.log_path
    assert len(new_files()) == 4


BLOCKED = """
import runpy, sys
class Block:
    def find_spec(self, name, path=None, target=None):
        if name.split('.')[0] in ('solara', 'reacton') or name.startswith(
                ('mesa_sim.viz', 'mesa_fork.visualization', 'mesa_sim.mesa_fork.visualization')):
            raise ImportError('a headless start imported ' + name)
sys.meta_path.insert(0, Block())
sys.argv = ['mesa_sim/run_mesa.py', '--steps', '1']
runpy.run_path('mesa_sim/run_mesa.py', run_name='__main__')
"""


def test_the_headless_start_imports_no_solara(new_files):
    done = subprocess.run([sys.executable, "-c", BLOCKED], cwd=ROOT, capture_output=True, text=True,
                          env={**os.environ, "PYTHONHASHSEED": "0"})
    assert done.returncode == 0, done.stderr[-2000:]
    assert len(new_files()) == 2
