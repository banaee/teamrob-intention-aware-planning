# domains/kitting/registry.py
"""
Assembles the kitting DomainModel from tasks and actions.
Entry point: build_kitting_domain()
Called once at startup by KnowledgeBase via sim_model.py.
"""

from shared.types import DomainModel
from domains.kitting.actions import move_to, pick_up, place, wait_at
from domains.kitting.tasks import deliver_item, coffee_break, ac_activation
from domains.kitting.scenarios import scenario_00, scenario_10, scenario_20, scenario_21, scenario_30, scenario_40, scenario_50, scenario_70, scenario_71, scenario_08

def register_kitting_domain() -> DomainModel:
    return DomainModel(
        tasks={
            "deliver_item":  deliver_item,
            "coffee_break":  coffee_break,
            "ac_activation": ac_activation,
        },
        actions={
            "move_to":   move_to,
            "pick_up":   pick_up,
            "place":     place,
            "wait_at":   wait_at,
        },
        microactions=["STEP", "GRASP", "RELEASE", "STAND"],
        intentions={"deliver_item", 
                    "coffee_break", 
                    "ac_activation", 
                    },
    )
    

domain_config = {
    "register_fn": register_kitting_domain,
    "layouts": {
        "env_layout0": {
            "path":      "domains/kitting/env_layout0.json",
            "scenarios": {
                "scenario_00": scenario_00,
            },
        },
        
        "env_layout1": {
            "path":      "domains/kitting/env_layout1.json",
            "scenarios": {
                "scenario_10": scenario_10,
            },
        },
        "env_layout2": {
            "path":      "domains/kitting/env_layout2.json",
            "scenarios": {
                "scenario_20": scenario_20,
                "scenario_21": scenario_21,
            },
        },
        "env_layout3": {
            "path":      "domains/kitting/env_layout3.json",
            "scenarios": {
                "scenario_30": scenario_30,
            },
        },
        "env_layout4": {
            "path":      "domains/kitting/env_layout4.json",
            "scenarios": {
                "scenario_40": scenario_40,
            },
        },
        "env_layout5": {
            "path":      "domains/kitting/env_layout5.json",
            "scenarios": {
                "scenario_50": scenario_50,
            },
        },
        "env_layout7": {
            "path":      "domains/kitting/env_layout7.json",
            "scenarios": {
                "scenario_70": scenario_70,
                "scenario_71": scenario_71,
            },
        },
        "env_layout8": {
            "path":      "domains/kitting/env_layout8.json",
            "scenarios": {
                "scenario_08": scenario_08,   # for viewing the layout; the fixtures are generated (below)
            },
        },
    },
}

# Generated fixtures register themselves (fixture_generation.py, TODO-47 (a)).
from domains.kitting.fixture_two_tables import register as _register_two_tables
_register_two_tables(domain_config)
