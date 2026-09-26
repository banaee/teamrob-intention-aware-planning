# tests/test_tl4_overrides.py
"""
T-L stage 4 (the run file and overrides): each of the three overrides applied
and printed; the refused kinds refused with the path named; an out-of-bounds
start and a container not in the layout refused by the loader's existing
checks; an --override and the same override in the run file give the same log
line; an unknown path, agent or object refused; the viewer's write keeps the
run file's comments.
"""

import logging
import shutil
import sys

import pytest

from domains.kitting.registry import domain_config, register_kitting_domain
from mesa_sim.overrides import (FixedPositionOverride, HomeContainerOverride, StartPositionOverride,
                                file_overrides, read_cli_override, read_override, write_overrides)
from mesa_sim.sim_model import SimModel

SCENARIO = domain_config["scenarios"]["scenario_s01_01"]   # env_layout_01, env_setup_01


def model(overrides):
    return SimModel(scenario=SCENARIO, register_fn=register_kitting_domain,
                    task_model_schemas=domain_config["task_model"],
                    layout_path=domain_config["layouts"]["env_layout_01"],
                    setup_path=domain_config["setups"][SCENARIO.setup],
                    overrides=overrides)


def start_lines(monkeypatch, caplog, argv):
    """The [run_mesa] lines of a headless run of 0 steps under these arguments."""
    monkeypatch.setattr(sys, "argv", ["run_mesa.py", "--steps", "0"] + argv)
    import mesa_sim.run_mesa as run_mesa
    caplog.clear()
    with caplog.at_level(logging.INFO):
        run_mesa.run_headless()
    return [r.getMessage() for r in caplog.records if r.getMessage().startswith("[run_mesa] ")]


# ---------------------------------------------------------------- applied and printed

def test_a_start_position_override_is_applied():
    m = model((StartPositionOverride("human_0", (40.0, 50.0)),))
    assert tuple(m.humans["human_0"].pos) == (40.0, 50.0)
    assert tuple(SCENARIO.agents[0].start_position) == (350, 200)   # the registered literal is unchanged


def test_a_fixed_position_override_moves_the_object_and_what_it_holds():
    m = model((FixedPositionOverride("shelf_2", (380.0, -120.0)),))
    assert m.objects["shelf_2"].position == (380.0, -120.0)
    held = [o for o in m.objects.values() if o.home_container == "shelf_2"]
    assert held and all(o.position == (380.0, -120.0) for o in held)


def test_a_home_container_override_is_applied():
    m = model((HomeContainerOverride("item_4", "shelf_2"),))
    assert m.objects["item_4"].home_container == "shelf_2"
    assert m.objects["item_4"].at_location == "shelf_2"
    assert m.objects["item_4"].position == m.objects["shelf_2"].position


def test_each_override_is_printed_after_the_triple(monkeypatch, caplog):
    lines = start_lines(monkeypatch, caplog, [
        "--override", "setup.item_4.initial_container=shelf_2",
        "--override", "scenario.human_0.start_position=40,50",
        "--override", "layout.shelf_2.position=380,-120"])
    assert lines[0].startswith("[run_mesa] Starting headless run — ")
    assert lines[1:4] == ["[run_mesa] override layout.shelf_2.position=380.0,-120.0",
                          "[run_mesa] override scenario.human_0.start_position=40.0,50.0",
                          "[run_mesa] override setup.item_4.initial_container=shelf_2"]


def test_the_cli_and_the_run_file_give_the_same_line(monkeypatch, caplog, tmp_path):
    run_file = tmp_path / "run.yaml"
    shutil.copy("configs/experiment.yaml", run_file)
    with open(run_file, "a") as f:
        f.write("\noverrides:\n  layout.shelf_2.position: [380, -120]\n")
    from_file = start_lines(monkeypatch, caplog, ["--run", str(run_file)])
    from_cli = start_lines(monkeypatch, caplog, ["--override", "layout.shelf_2.position=380,-120"])
    # between the start line and the completion line
    assert from_file[1:-1] == from_cli[1:-1] == ["[run_mesa] override layout.shelf_2.position=380.0,-120.0"]


def test_no_override_prints_no_line(monkeypatch, caplog):
    assert len(start_lines(monkeypatch, caplog, [])) == 2   # the start line and the completion line


# ---------------------------------------------------------------- refused

@pytest.mark.parametrize("path, value", [
    ("scenario.human_0.assigned_tasks", "x"),          # a variant is a new scenario
    ("scenario.human_0.scheduled_tasks", "x"),         # the script
    ("setup.item_4.destination", "kitting_table_0"),   # a different designation set is a different setup
    ("setup.item_4.position", [0, 0]),                 # a movable object's position is its container's
    ("layout.shelf_2.id", "shelf_9"),                  # an object's own id
    ("setup.item_4.id", "item_9"),
    ("scenario.human_0.agent_id", "human_9"),
])
def test_a_refused_kind_is_refused_with_its_path(path, value):
    with pytest.raises(ValueError, match=rf"override '{path}': not overridable"):
        read_override(path, value)


@pytest.mark.parametrize("text", ["shelf_2.position=1,2", "layout.position=1,2", "layout.shelf_2.position.x=1",
                                  "room.shelf_2.position=1,2", "layout.shelf_2.position"])
def test_an_unknown_path_is_refused(text):
    with pytest.raises(ValueError, match=r"override '"):
        read_cli_override(text)


@pytest.mark.parametrize("path, value", [("layout.shelf_2.position", [1]),
                                         ("layout.shelf_2.position", "1,a"),
                                         ("scenario.human_0.start_position", [True, 1]),
                                         ("setup.item_4.initial_container", [1, 2])])
def test_a_value_of_the_wrong_type_is_refused(path, value):
    with pytest.raises(ValueError, match=rf"override '{path}'"):
        read_override(path, value)


@pytest.mark.parametrize("override, message", [
    (StartPositionOverride("human_9", (0.0, 0.0)), r"no agent 'human_9' in scenario 'scenario_s01_01'"),
    (FixedPositionOverride("shelf_99", (0.0, 0.0)), r"no object 'shelf_99' in layout"),
    (FixedPositionOverride("item_4", (0.0, 0.0)), r"'item_4' is a movable object of setup"),
    (HomeContainerOverride("item_99", "shelf_2"), r"no object 'item_99' in setup"),
])
def test_an_unknown_agent_or_object_is_refused_with_its_path(override, message):
    with pytest.raises(ValueError, match=rf"override '{override.path()}': {message}"):
        model((override,))


def test_an_out_of_bounds_start_is_refused_by_the_existing_check():
    with pytest.raises(ValueError, match=r"scenario 'scenario_s01_01', agent 'human_0': "
                                         r"start_position .* outside the space's bounds"):
        model((StartPositionOverride("human_0", (10000.0, 0.0)),))


def test_a_container_not_in_the_layout_is_refused_by_the_existing_check():
    with pytest.raises(ValueError, match=r"setup .*'item_4' has home container 'shelf_99', "
                                         r"which is not an object of layout"):
        model((HomeContainerOverride("item_4", "shelf_99"),))


def test_the_same_path_twice_on_the_command_line_is_refused(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["run_mesa.py", "--override", "layout.shelf_2.position=1,2",
                                      "--override", "layout.shelf_2.position=3,4"])
    import mesa_sim.run_mesa as run_mesa
    with pytest.raises(ValueError, match=r"override 'layout.shelf_2.position': given twice"):
        run_mesa.load_user_config()


# ---------------------------------------------------------------- the viewer's write

def test_the_viewers_write_keeps_the_run_files_comments(tmp_path):
    run_file = tmp_path / "run.yaml"
    shutil.copy("configs/experiment.yaml", run_file)
    original = run_file.read_text()
    overrides = (FixedPositionOverride("shelf_2", (380.0, -120.0)), HomeContainerOverride("item_4", "shelf_2"))
    write_overrides(str(run_file), overrides)
    written = run_file.read_text()
    assert written.startswith(original.rstrip("\n"))   # every key and comment kept, the block appended
    assert file_overrides(str(run_file)) == overrides
    write_overrides(str(run_file), ())
    assert run_file.read_text() == original
