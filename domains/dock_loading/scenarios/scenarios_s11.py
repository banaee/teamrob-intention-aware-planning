# domains/dock_loading/scenarios/scenarios_s11.py
"""
Dock_loading scenarios on env_setup_11 (T-K part 1, step 6, kind 3 "pallets in the bays", written for
env_layout_05; design_records.md, "T-K", STEP 6; analysis/dock_loading/tk6/README.md). One module per setup.
Written by analysis/dock_loading/tk6/make_set.py; the literals are the source.
"""

from shared.types import AgentConfig, ScenarioConfig, Script
from domains.dock_loading.actions import move_to
from domains.dock_loading.script import (coffee_break, confirm_delivered_pallet, deliver_pallet, go_to, load_return,
                                         office_break, stand)
from shared.types import Timeline
from domains.dock_loading.script import window
from domains.dock_loading.facts import BREAK_TIME


# T-K part 1, step 6 (6 October 2026): the new scripts (analysis/dock_loading/tk6/make_set.py bases).
scenario_s11_01 = ScenarioConfig(
    id="scenario_s11_01",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    description=(
        "T-K part 1, step 6, script a (a coffee break first, before any scan), on env_layout_05: the human takes a "
        "coffee break, scans pallet_0, scans pallet_2, then the walk to the desk; the robot delivers pallet_4 and "
        "pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script independent of the robot, the disjointness "
        "rule (MPB-DL7). No timeline (no fact); its copies with break_time follow. No expectation derived by hand "
        "(Hadi, 6 October 2026); the oracle's tables are committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_02 = ScenarioConfig(
    id="scenario_s11_02",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    description=(
        "T-K part 1, step 6, script b (scans only, across both bays), on env_layout_05: the human scans pallet_0, "
        "scans pallet_2, scans pallet_1, scans pallet_3, then the walk to the desk; the robot delivers pallet_4 "
        "and pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script independent of the robot, the "
        "disjointness rule (MPB-DL7). No timeline (no fact); its copies with break_time follow. No expectation "
        "derived by hand (Hadi, 6 October 2026); the oracle's tables are committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                    confirm_delivered_pallet("pallet_1"),
                    confirm_delivered_pallet("pallet_3"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_1"),
                confirm_delivered_pallet("pallet_3"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_03 = ScenarioConfig(
    id="scenario_s11_03",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    description=(
        "T-K part 1, step 6, script c (an office break inside a scan, on arrival at the bay before the scan), on "
        "env_layout_05: the human scans pallet_0 with an office break on arrival at the bay, scans pallet_2, then "
        "the walk to the desk; the robot delivers pallet_4 and pallet_5 and returns pallet_6 and pallet_7. Kind 3, "
        "a script independent of the robot, the disjointness rule (MPB-DL7). No timeline (no fact); its copies "
        "with break_time follow. No expectation derived by hand (Hadi, 6 October 2026); the oracle's tables are "
        "committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").at(move_to, office_break("office_chair"), occurrence=0),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_04 = ScenarioConfig(
    id="scenario_s11_04",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    description=(
        "T-K part 1, step 6, script d (a second coffee break inside the first's recency), on env_layout_05: the "
        "human takes a coffee break, scans pallet_0, takes a coffee break, scans pallet_2, then the walk to the "
        "desk; the robot delivers pallet_4 and pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script "
        "independent of the robot, the disjointness rule (MPB-DL7). No timeline (no fact); its copies with "
        "break_time follow. No expectation derived by hand (Hadi, 6 October 2026); the oracle's tables are "
        "committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_05 = ScenarioConfig(
    id="scenario_s11_05",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    description=(
        "T-K part 1, step 6, script e (a coffee break, then an office break), on env_layout_05: the human scans "
        "pallet_0, takes a coffee break, takes an office break, scans pallet_2, then the walk to the desk; the "
        "robot delivers pallet_4 and pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script independent of "
        "the robot, the disjointness rule (MPB-DL7). No timeline (no fact); its copies with break_time follow. No "
        "expectation derived by hand (Hadi, 6 October 2026); the oracle's tables are committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    office_break("office_chair"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_06 = ScenarioConfig(
    id="scenario_s11_06",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    description=(
        "T-K part 1, step 6, script e' (an office break, then a coffee break), on env_layout_05: the human scans "
        "pallet_0, takes an office break, takes a coffee break, scans pallet_2, then the walk to the desk; the "
        "robot delivers pallet_4 and pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script independent of "
        "the robot, the disjointness rule (MPB-DL7). No timeline (no fact); its copies with break_time follow. No "
        "expectation derived by hand (Hadi, 6 October 2026); the oracle's tables are committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    office_break("office_chair"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_07 = ScenarioConfig(
    id="scenario_s11_07",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    description=(
        "T-K part 1, step 6, script f (one coffee break between two scans, for the three window edges), on "
        "env_layout_05: the human scans pallet_2, takes a coffee break, scans pallet_0, then the walk to the desk; "
        "the robot delivers pallet_4 and pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script independent "
        "of the robot, the disjointness rule (MPB-DL7). No timeline (no fact); its copies with break_time follow. "
        "No expectation derived by hand (Hadi, 6 October 2026); the oracle's tables are committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_08 = ScenarioConfig(
    id="scenario_s11_08",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    description=(
        "T-K part 1, step 6, script g (a coffee break once every scan is done (no assigned task live)), on "
        "env_layout_05: the human scans pallet_0, scans pallet_2, takes a coffee break, then the walk to the desk; "
        "the robot delivers pallet_4 and pallet_5 and returns pallet_6 and pallet_7. Kind 3, a script independent "
        "of the robot, the disjointness rule (MPB-DL7). No timeline (no fact); its copies with break_time follow. "
        "No expectation derived by hand (Hadi, 6 October 2026); the oracle's tables are committed before the runs."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                    coffee_break("coffee_machine_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


# T-K part 1, step 6 (6 October 2026): the copies with break_time (analysis/dock_loading/tk6/make_set.py variants).
scenario_s11_09 = ScenarioConfig(
    id="scenario_s11_09",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 44),)),
    description=(
        "T-K part 1, step 6: scenario_s11_01's copy with break_time from 0 to 44 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_01's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_10 = ScenarioConfig(
    id="scenario_s11_10",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 44, 68),)),
    description=(
        "T-K part 1, step 6: scenario_s11_01's copy with break_time from 44 to 68 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_01's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_11 = ScenarioConfig(
    id="scenario_s11_11",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s11_02's copy with break_time from 0 to 30 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_02's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                    confirm_delivered_pallet("pallet_1"),
                    confirm_delivered_pallet("pallet_3"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_1"),
                confirm_delivered_pallet("pallet_3"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_12 = ScenarioConfig(
    id="scenario_s11_12",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 30, 84),)),
    description=(
        "T-K part 1, step 6: scenario_s11_02's copy with break_time from 30 to 84 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_02's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                    confirm_delivered_pallet("pallet_1"),
                    confirm_delivered_pallet("pallet_3"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_1"),
                confirm_delivered_pallet("pallet_3"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_13 = ScenarioConfig(
    id="scenario_s11_13",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 28, 108),)),
    description=(
        "T-K part 1, step 6: scenario_s11_03's copy with break_time from 28 to 108 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_03's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").at(move_to, office_break("office_chair"), occurrence=0),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_14 = ScenarioConfig(
    id="scenario_s11_14",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 28),)),
    description=(
        "T-K part 1, step 6: scenario_s11_03's copy with break_time from 0 to 28 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_03's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").at(move_to, office_break("office_chair"), occurrence=0),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_15 = ScenarioConfig(
    id="scenario_s11_15",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 44),)),
    description=(
        "T-K part 1, step 6: scenario_s11_04's copy with break_time from 0 to 44 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_04's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_16 = ScenarioConfig(
    id="scenario_s11_16",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 44, 68),)),
    description=(
        "T-K part 1, step 6: scenario_s11_04's copy with break_time from 44 to 68 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_04's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_17 = ScenarioConfig(
    id="scenario_s11_17",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 44), window(BREAK_TIME, 68, 120),)),
    description=(
        "T-K part 1, step 6: scenario_s11_04's copy with break_time from 0 to 44 and from 68 to 120 (V3, over both "
        "breaks; the rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_04's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_18 = ScenarioConfig(
    id="scenario_s11_18",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 30, 82),)),
    description=(
        "T-K part 1, step 6: scenario_s11_05's copy with break_time from 30 to 82 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_05's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    office_break("office_chair"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_19 = ScenarioConfig(
    id="scenario_s11_19",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s11_05's copy with break_time from 0 to 30 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_05's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    office_break("office_chair"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_20 = ScenarioConfig(
    id="scenario_s11_20",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 30, 82), window(BREAK_TIME, 82, 142),)),
    description=(
        "T-K part 1, step 6: scenario_s11_05's copy with break_time from 30 to 82 and from 82 to 142 (V3, over "
        "both breaks; the rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is "
        "scenario_s11_05's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    coffee_break("coffee_machine_0"),
                    office_break("office_chair"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_21 = ScenarioConfig(
    id="scenario_s11_21",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 30, 110),)),
    description=(
        "T-K part 1, step 6: scenario_s11_06's copy with break_time from 30 to 110 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_06's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    office_break("office_chair"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_22 = ScenarioConfig(
    id="scenario_s11_22",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s11_06's copy with break_time from 0 to 30 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_06's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    office_break("office_chair"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_23 = ScenarioConfig(
    id="scenario_s11_23",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 30, 110), window(BREAK_TIME, 110, 154),)),
    description=(
        "T-K part 1, step 6: scenario_s11_06's copy with break_time from 30 to 110 and from 110 to 154 (V3, over "
        "both breaks; the rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is "
        "scenario_s11_06's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    office_break("office_chair"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_24 = ScenarioConfig(
    id="scenario_s11_24",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 18, 91),)),
    description=(
        "T-K part 1, step 6: scenario_s11_07's copy with break_time from 18 to 91 (edge before the human leaves; "
        "the rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_07's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_25 = ScenarioConfig(
    id="scenario_s11_25",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 44, 91),)),
    description=(
        "T-K part 1, step 6: scenario_s11_07's copy with break_time from 44 to 91 (edge in the walk; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_07's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_26 = ScenarioConfig(
    id="scenario_s11_26",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 60, 91),)),
    description=(
        "T-K part 1, step 6: scenario_s11_07's copy with break_time from 60 to 91 (edge at the arrival; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_07's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    coffee_break("coffee_machine_0"),
                    confirm_delivered_pallet("pallet_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_2"),
                confirm_delivered_pallet("pallet_0"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_27 = ScenarioConfig(
    id="scenario_s11_27",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 84, 147),)),
    description=(
        "T-K part 1, step 6: scenario_s11_08's copy with break_time from 84 to 147 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_08's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                    coffee_break("coffee_machine_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)


scenario_s11_28 = ScenarioConfig(
    id="scenario_s11_28",
    setup="env_setup_11",
    reference_layouts=["env_layout_05"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s11_08's copy with break_time from 0 to 30 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s11_08's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_2"),
                    coffee_break("coffee_machine_0"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_2"),
            ],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(0, -370),
            observes=["human_0"],
            assigned_tasks=[
                deliver_pallet("pallet_4"),
                deliver_pallet("pallet_5"),
                load_return("pallet_6"),
                load_return("pallet_7"),
            ],
        ),
    ],
)
