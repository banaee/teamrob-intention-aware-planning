# tests/dock_loading/test_subtype_rule.py
"""
The loader's subtype rule (design_decisions.md, "subtype is a stated fact of an
object", 3 October 2026): a movable object's subtype must equal the subtype of
its destination and of its home container, where that fixed object carries
one; otherwise loading the setup fails, naming the object, the container and
the two subtypes. An object without a subtype, or a container without one, is
not checked. A fixed object reads its subtype from the layout, a movable object
from the setup.
Run from the repo root:  PYTHONHASHSEED=0 python -m pytest tests/dock_loading/test_subtype_rule.py
"""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "mesa_sim"))

from shared.types import AgentConfig, ScenarioConfig, Script
from domains.dock_loading.registry import domain_config as dock, register_dock_loading_domain
from mesa_sim.sim_model import SimModel

H = "human_0"
LAYOUT = "env_layout_02"


def edited(tmp_path, kind, base, changes):
    """A copy of the registered layout or setup `base`, with `changes`
    ({object id: {field: value, or None to remove it}}) applied."""
    with open(dock[kind][base]) as f:
        data = json.load(f)
    for obj in data["env_objects"]:
        for field, value in changes.get(obj["id"], {}).items():
            if value is None:
                obj.pop(field, None)
            else:
                obj[field] = value
    path = tmp_path / f"{base}_test.json"
    path.write_text(json.dumps(data))
    return str(path)


def load(setup="env_setup_02", setup_path=None, layout_path=None):
    agents = [AgentConfig(agent_id=H, agent_type="human", start_position=(0, 0), scheduled_tasks=Script([]))]
    scenario = ScenarioConfig(id="scenario_test", description="t", agents=agents, setup=setup,
                              reference_layouts=[LAYOUT])
    return SimModel(scenario=scenario, register_fn=register_dock_loading_domain,
                    task_model_schemas=dock["task_model"],
                    layout_path=layout_path or dock["layouts"][LAYOUT],
                    setup_path=setup_path or dock["setups"][setup],
                    state_declarations=dock["states"])


def test_matching_subtypes_load():
    model = load()                                    # env_setup_02: pallets in their bays, one in the truck
    assert model.objects["dry_delivery_bay_0"].subtype == "dry"            # read from the layout
    assert model.objects["frozen_delivery_bay_0"].subtype == "frozen"
    assert model.objects["pallet_2"].subtype == "frozen"                   # read from the setup
    assert model.objects["pallet_4"].subtype == "dry"                      # in the truck, designated to the dry bay
    assert model.objects["truck_interior"].subtype is None


def test_every_registered_dock_loading_setup_loads():
    for setup in dock["setups"]:
        load(setup=setup)


def test_a_mismatch_with_the_destination_fails(tmp_path):
    # pallet_4 stands in the truck (no subtype) and is designated to the dry bay.
    path = edited(tmp_path, "setups", "env_setup_02", {"pallet_4": {"subtype": "frozen"}})
    with pytest.raises(ValueError, match=r"pallet 'pallet_4' of subtype 'frozen' has destination "
                                         r"'dry_delivery_bay_0' of subtype 'dry'"):
        load(setup_path=path)


def test_a_mismatch_with_the_home_container_fails(tmp_path):
    # pallet_2 stands in the frozen bay; designated to the truck, only its home container is checked.
    path = edited(tmp_path, "setups", "env_setup_02",
                  {"pallet_2": {"subtype": "dry", "destination": "truck_interior"}})
    with pytest.raises(ValueError, match=r"pallet 'pallet_2' of subtype 'dry' has home container "
                                         r"'frozen_delivery_bay_0' of subtype 'frozen'"):
        load(setup_path=path)


def test_a_movable_object_without_subtype_is_not_checked(tmp_path):
    # pallet_0 stands in the dry bay; without a subtype, a frozen destination loads.
    path = edited(tmp_path, "setups", "env_setup_02",
                  {"pallet_0": {"subtype": None, "destination": "frozen_delivery_bay_0"}})
    assert load(setup_path=path).objects["pallet_0"].subtype is None


def test_a_container_without_subtype_is_not_checked(tmp_path):
    # The dry bay without a subtype: a frozen pallet in it, designated to it, loads.
    layout = edited(tmp_path, "layouts", LAYOUT, {"dry_delivery_bay_0": {"subtype": None}})
    setup = edited(tmp_path, "setups", "env_setup_02", {"pallet_0": {"subtype": "frozen"}})
    assert load(setup_path=setup, layout_path=layout).objects["pallet_0"].subtype == "frozen"
