"""
tests/test_tviz_view.py

T-viz 1a, increment (ii): the view of a layout, or of a layout and a setup (mesa_sim/webui_adapter.py, `view`), and
the catalogue's offer. docs/handoffs/plan_T-viz_1a.md, section 2 (ii) and M2.

- Every triple the page offers builds: every scenario on each of its reference layouts (P2).
- The view of a layout with a setup equals the matching part of the run description and of the start tick update of
  every scenario on it (P3, P7): the space, the areas, the fixed objects, the movable objects, the fixed objects'
  contents and the object states. The view of the layout alone equals its layout part.
- A view writes no file; a layout or a setup that is not registered is refused with BuildFailed.
- The catalogue carries the notes of the layout and setup files.
- Increment (iii): every state a domain's appearance names is a state the domain declares for the entry's type; a look
  that names another stops the start.
"""

import json
import os
from pathlib import Path

import pytest

from mesa_sim.run_config import DOMAIN_REGISTRY
from mesa_sim.sim_run import LOG_DIR
from mesa_sim.webui_adapter import MesaSimulator, appearance, check_looks_by_state
from webui import messages as m
from webui.appearance import Appearance
from webui.simulator import BuildFailed

ROOT = Path(__file__).parent.parent


def _files():
    return set(os.listdir(LOG_DIR)) if os.path.isdir(LOG_DIR) else set()


@pytest.fixture(scope="module")
def simulator():
    return MesaSimulator()


def _offered():
    """Every (domain, layout, scenario) the page offers: each scenario on each of its reference layouts."""
    return [(d, layout, s.id) for d, domain in DOMAIN_REGISTRY.items() for s in domain["scenarios"].values()
            for layout in s.reference_layouts]


def test_every_offered_triple_builds_and_its_view_equals_its_start(simulator):
    before = _files()
    options = simulator.catalogue().default_choice.options
    offered = _offered()
    assert len(offered) >= 1019
    for domain, layout, scenario in offered:
        choice = m.SimRunChoice(domain=domain, layout=layout, scenario=scenario, options=options)
        side = simulator.build(choice, "sim-run-1")
        try:
            world, start = side.description.world, side.state().world
            setup = side.description.run.setup
            view = simulator.view(m.ViewChoice(domain=domain, layout=layout, setup=setup))
            alone = simulator.view(m.ViewChoice(domain=domain, layout=layout, setup=None))
        finally:
            side.discard()
        where = f"{domain} {layout} {setup} {scenario}"
        for v in (view, alone):
            assert (v.space, v.areas, v.fixed_objects) == (world.space, world.areas, world.fixed_objects), where
        assert alone.setup is None
        assert view.setup.id == setup
        assert view.setup.movable_objects == world.movable_objects, where
        assert view.setup.fixed_object_contents == start.fixed_object_contents, where
        assert view.setup.object_states == start.object_states, where
    assert _files() == before


def test_a_view_of_what_is_not_registered_is_refused(simulator):
    for choice in (m.ViewChoice(domain="no_domain", layout="env_layout_02", setup=None),
                   m.ViewChoice(domain="kitting", layout="no_layout", setup=None),
                   m.ViewChoice(domain="kitting", layout="env_layout_02", setup="no_setup")):
        with pytest.raises(BuildFailed):
            simulator.view(choice)


def test_the_catalogue_carries_the_notes_of_layouts_and_setups(simulator):
    catalogue = simulator.catalogue()
    for entry in catalogue.domains:
        domain = DOMAIN_REGISTRY[entry.name]
        for layout in entry.layouts:
            space = json.loads((ROOT / domain["layouts"][layout.id]).read_text())["space"]
            assert "note" not in space, layout.id
            assert layout.notes == space.get("notes")
        for setup in entry.setups:
            assert setup.notes == json.loads((ROOT / domain["setups"][setup.id]).read_text()).get("notes")


def test_a_look_by_state_names_a_state_its_domain_declares_for_the_type():
    for domain in DOMAIN_REGISTRY:
        appearance(domain)      # the domains' own files pass
    states = DOMAIN_REGISTRY["dock_loading"]["states"]
    named = next(d for d in states if d.object_type is not None)
    good = {"movable": {named.object_type: {"shape": "skid", "height": 14,
                                            "states": [{"state": named.name, "look": {"shape": "crate", "height": 9}}]}}}
    check_looks_by_state(Appearance.model_validate_json(json.dumps(good)), states, "made up")
    for kind, entry in (("movable", {named.object_type: {"shape": "skid", "height": 14, "states": [
                            {"state": named.name + "_misspelt", "look": {"shape": "crate", "height": 9}}]}}),
                        ("movable", {"other_type": {"shape": "skid", "height": 14, "states": [
                            {"state": named.name, "look": {"shape": "crate", "height": 9}}]}})):
        with pytest.raises(ValueError):
            check_looks_by_state(Appearance.model_validate_json(json.dumps({kind: entry})), states, "made up")
