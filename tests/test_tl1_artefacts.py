# tests/test_tl1_artefacts.py
"""
T-L stage 1 (the split): the loader's two added checks and the resolver's
triple. A missing home container and an out-of-bounds start are refused; a run
file's setup must equal the scenario's; a run that names no layout takes the
scenario's first reference layout; a registered layout outside the reference
layouts is a valid selection.
"""

import json
import sys

import pytest

from shared.types import AgentConfig, ScenarioConfig
from domains.kitting.registry import domain_config, register_kitting_domain
from mesa_sim.sim_model import SimModel


@pytest.fixture
def run_mesa(monkeypatch):
    """mesa_sim.run_mesa parses sys.argv and resolves the default run at
    import (the Solara page), so it is imported under a bare argv."""
    monkeypatch.setattr(sys, "argv", ["run_mesa.py"])
    import mesa_sim.run_mesa as run_mesa
    return run_mesa


def model(scenario, layout_path, setup_path):
    return SimModel(scenario=scenario, register_fn=register_kitting_domain,
                    task_model_schemas=domain_config["task_model"],
                    layout_path=layout_path, setup_path=setup_path)


def test_a_missing_home_container_is_refused(tmp_path):
    with open(domain_config["setups"]["env_setup0"]) as f:
        setup = json.load(f)
    broken = next(o for o in setup["env_objects"] if o["id"] == "item_3")
    broken["initial_container"] = "shelf_99"
    path = tmp_path / "env_setup_broken.json"
    path.write_text(json.dumps(setup))
    with pytest.raises(ValueError, match=r"setup .*'item_3' has home container 'shelf_99', "
                                         r"which is not an object of layout"):
        model(domain_config["scenarios"]["scenario_00"],
              domain_config["layouts"]["env_layout0"], str(path))


def test_an_out_of_bounds_start_is_refused():
    base = domain_config["scenarios"]["scenario_00"]
    agents = [a if a.agent_type == "human" else
              AgentConfig(agent_id=a.agent_id, agent_type="robot", start_position=(10000.0, 0.0),
                          assigned_tasks=a.assigned_tasks, observes=a.observes)
              for a in base.agents]
    scenario = ScenarioConfig(id="scenario_test", description="t", agents=agents,
                              setup=base.setup, reference_layouts=base.reference_layouts)
    with pytest.raises(ValueError, match=r"scenario 'scenario_test', agent 'robot_0': "
                                         r"start_position .* outside the space's bounds"):
        model(scenario, domain_config["layouts"]["env_layout0"],
              domain_config["setups"][base.setup])


def test_a_mismatched_setup_in_the_run_file_is_refused(run_mesa):
    with pytest.raises(ValueError, match=r"setup 'env_setup1': scenario 'scenario_00' "
                                         r"declares setup 'env_setup0'"):
        run_mesa.resolve_triple({"domain": "kitting", "scenario": "scenario_00",
                                 "setup": "env_setup1"})


def test_no_layout_takes_the_first_reference_layout(run_mesa):
    _, layout_id, setup_id, scenario = run_mesa.resolve_triple(
        {"domain": "kitting", "scenario": "scenario_30"})
    assert layout_id == "env_layout3"
    assert setup_id == "env_setup3"
    assert scenario.id == "scenario_30"


def test_a_non_reference_registered_layout_resolves(run_mesa):
    _, layout_id, _, _ = run_mesa.resolve_triple(
        {"domain": "kitting", "scenario": "scenario_30", "layout": "env_layout0"})
    assert layout_id == "env_layout0"
