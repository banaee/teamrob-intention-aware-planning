# domains/kitting/registry.py
"""
Assembles the kitting DomainModel from tasks and actions.
Entry point: build_kitting_domain()
Called once at startup by KnowledgeBase via sim_model.py.
"""

from shared.types import DomainModel
from domains.kitting.actions import move_to, pick_up, place, wait_at
from domains.kitting.tasks import deliver_item, coffee_break, ac_activation
from domains.kitting.scenarios import scenario_00, scenario_01, scenario_02, scenario_03, scenario_04, scenario_10, scenario_11, scenario_12, scenario_20, scenario_22, scenario_23, scenario_24, scenario_21, scenario_30, scenario_31, scenario_32, scenario_40, scenario_41, scenario_42, scenario_50, scenario_51, scenario_52, scenario_53, scenario_70, scenario_71, scenario_72, scenario_73, scenario_80, scenario_81, scenario_82, scenario_83, scenario_84, scenario_85, scenario_90, scenario_91, scenario_92, scenario_93, scenario_94

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
                "scenario_01": scenario_01,
                "scenario_02": scenario_02,   # script example (T-C2c play), not a measured fixture
                "scenario_03": scenario_03,   # script example
                "scenario_04": scenario_04,   # script example
            },
        },
        
        "env_layout1": {
            "path":      "domains/kitting/env_layout1.json",
            "scenarios": {
                "scenario_10": scenario_10,
                "scenario_11": scenario_11,
                "scenario_12": scenario_12,   # script example (T-C2c play), not a measured fixture
            },
        },
        "env_layout2": {
            "path":      "domains/kitting/env_layout2.json",
            "scenarios": {
                "scenario_20": scenario_20,
                "scenario_22": scenario_22,   # script example (T-C2c play), not a measured fixture
                "scenario_23": scenario_23,   # script example (T-C2c play), not a measured fixture
                "scenario_24": scenario_24,   # script example (T-C2c play), not a measured fixture
                "scenario_21": scenario_21,
            },
        },
        "env_layout3": {
            "path":      "domains/kitting/env_layout3.json",
            "scenarios": {
                "scenario_30": scenario_30,
                "scenario_31": scenario_31,   # script example (T-C2c play), not a measured fixture
                "scenario_32": scenario_32,   # script example (T-C2c play), not a measured fixture
            },
        },
        "env_layout4": {
            "path":      "domains/kitting/env_layout4.json",
            "scenarios": {
                "scenario_40": scenario_40,
                "scenario_41": scenario_41,   # script example (T-C2c play), not a measured fixture
                "scenario_42": scenario_42,   # script example (T-C2c play), not a measured fixture
            },
        },
        "env_layout5": {
            "path":      "domains/kitting/env_layout5.json",
            "scenarios": {
                "scenario_50": scenario_50,
                "scenario_51": scenario_51,   # script example (T-C2c play), not a measured fixture
                "scenario_52": scenario_52,   # script example (T-C2c play), not a measured fixture
                "scenario_53": scenario_53,   # script example (T-C2c play), not a measured fixture
            },
        },
        "env_layout7": {
            "path":      "domains/kitting/env_layout7.json",
            "scenarios": {
                "scenario_70": scenario_70,
                "scenario_71": scenario_71,
                "scenario_72": scenario_72,   # script example (T-C2c play), not a measured fixture
                "scenario_73": scenario_73,   # script example (T-C2c play), not a measured fixture
            },
        },
        "env_layout8": {
            "path":      "domains/kitting/env_layout8.json",
            "scenarios": {
                "scenario_80": scenario_80,
                "scenario_81": scenario_81,
                "scenario_82": scenario_82,   # for viewing the layout; not a fixture
                "scenario_83": scenario_83,
                "scenario_84": scenario_84,   # script example (T-C2c play), not a measured fixture
                "scenario_85": scenario_85,   # script example
            },
        },
        "env_layout9": {
            "path":      "domains/kitting/env_layout9.json",
            "scenarios": {
                "scenario_90": scenario_90,   # for viewing the layout; not a fixture
                "scenario_91": scenario_91,   # script example (T-C2c play), not a measured fixture
                "scenario_92": scenario_92,   # script example
                "scenario_93": scenario_93,   # script example
                "scenario_94": scenario_94,   # script example (T-C2c play), not a measured fixture
            },
        },
    },
}