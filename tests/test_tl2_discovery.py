# tests/test_tl2_discovery.py
"""
T-L stage 2 (the package and discovery): a duplicate scenario id is refused at
import; every module's scenarios carry that module's setup — one setup per
module and one module per setup, on the registry's content and the module
namespaces, never on strings inside ids (the module-name serial is an
authoring convention the code does not check, T-L ruling 4); the merged
setups (env_setup_01 from env_setup0/3, env_setup_03 from env_setup2/5) load
the scenarios that were on env_layout_04 and env_layout_06.

Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/test_tl2_discovery.py
"""

import importlib
import pkgutil

import pytest

import mesa_sim.run_config  # noqa: F401  (puts mesa_sim/ on the path, so that SimModel's mesa_fork imports alone)
from shared.types import ScenarioConfig
from domains.discovery import discover_scenarios
from domains.dock_loading.registry import domain_config as dock_config
from domains.kitting.registry import domain_config, register_kitting_domain
import domains.kitting.scenarios as kitting_scenarios
import domains.dock_loading.scenarios as dock_scenarios
import tests.tl2_fixture_dup as fixture_dup
from mesa_sim.sim_model import SimModel


def scenarios_by_module(package):
    """Each module of the package with its top-level ScenarioConfigs."""
    result = {}
    for module_info in sorted(pkgutil.iter_modules(package.__path__), key=lambda m: m.name):
        module = importlib.import_module(f"{package.__name__}.{module_info.name}")
        result[module.__name__] = [v for v in vars(module).values()
                                   if isinstance(v, ScenarioConfig)]
    return result


def test_a_duplicate_scenario_id_is_refused_at_import():
    with pytest.raises(ValueError, match=r"duplicate scenario id 'scenario_dup'.*"
                                         r"mod_a.*mod_b"):
        discover_scenarios(fixture_dup)


def test_every_module_carries_one_setup_and_no_two_modules_share_one():
    for package in (kitting_scenarios, dock_scenarios):
        by_module = scenarios_by_module(package)
        setups_seen = {}
        for module_name, configs in by_module.items():
            assert configs, f"{module_name} defines no scenario"
            module_setups = {cfg.setup for cfg in configs}
            assert len(module_setups) == 1, (
                f"{module_name} mixes setups {sorted(module_setups)}")
            setup = module_setups.pop()
            assert setup not in setups_seen, (
                f"setup '{setup}' is held by {setups_seen[setup]} and {module_name}")
            setups_seen[setup] = module_name


@pytest.mark.parametrize("package,config", [(kitting_scenarios, domain_config), (dock_scenarios, dock_config)])
def test_the_registry_is_the_union_of_the_modules(package, config):
    """Every scenario of every module is registered, and nothing else is; every module's setup is a registered setup.
    No count and no list of ids is pinned (TODO-126): a scenario or a setup added by hand needs no edit here."""
    by_module = scenarios_by_module(package)
    from_modules = [cfg.id for configs in by_module.values() for cfg in configs]
    assert len(from_modules) == len(set(from_modules))     # no id twice (discovery refuses it at import, above)
    assert set(from_modules) == set(config["scenarios"])
    for configs in by_module.values():
        assert configs[0].setup in config["setups"]


@pytest.mark.parametrize("scenario_id,layout_id", [
    ("scenario_s01_06", "env_layout_04"),   # was on env_setup3, merged into env_setup_01
    ("scenario_s03_06", "env_layout_06"),   # was on env_setup5, merged into env_setup_03
])
def test_the_merged_setups_load(scenario_id, layout_id):
    scenario = domain_config["scenarios"][scenario_id]
    SimModel(scenario=scenario, register_fn=register_kitting_domain,
             task_model_schemas=domain_config["task_model"],
             layout_path=domain_config["layouts"][layout_id],
             setup_path=domain_config["setups"][scenario.setup], human_aware=True, intention_aware=True, assignment_knowledge=False, context_knowledge=False)
