# domains/kitting/registry.py
"""
Assembles the kitting tree of task schemas (T-H) from tasks and actions, and
declares the task model a robot is given.
Entry point: register_kitting_domain()
Called once at startup by sim_model.py.
"""

from shared.knowledge import Tree
from domains.kitting.actions import move_to, pick_up, place, wait_at, stand
from domains.kitting.tasks import deliver_item, coffee_break, ac_activation, go_to, stand_task
from domains.kitting.scenarios import scenario_00, scenario_01, scenario_02, scenario_03, scenario_04, scenario_10, scenario_11, scenario_12, scenario_20, scenario_22, scenario_23, scenario_24, scenario_21, scenario_30, scenario_31, scenario_32, scenario_40, scenario_41, scenario_42, scenario_50, scenario_51, scenario_52, scenario_53, scenario_70, scenario_71, scenario_72, scenario_73, scenario_80, scenario_81, scenario_82, scenario_83, scenario_84, scenario_85, scenario_90, scenario_91, scenario_92, scenario_93, scenario_94

def register_kitting_domain() -> Tree:
    return Tree(
        tasks=[deliver_item, coffee_break, ac_activation, go_to, stand_task],
        actions=[move_to, pick_up, place, wait_at, stand],
        microactions=["STEP", "GRASP", "RELEASE", "STAND"],
    )


domain_config = {
    "register_fn": register_kitting_domain,
    # The task model every robot is given (T-H): every WorkTask and the
    # PersonalTasks it foresees; no HumanOnlyTask.
    "task_model":  [deliver_item, coffee_break, ac_activation],
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