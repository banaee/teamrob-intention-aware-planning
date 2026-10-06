# domains/dock_loading/scenarios/scenarios_s10.py
"""
Dock_loading scenarios on env_setup_10 (T-K part 1, step 6, kind 3 "pallets in the bays", written for
env_layout_02; design_records.md, "T-K", STEP 6; analysis/dock_loading/tk6/README.md). One module per setup.
Written by analysis/dock_loading/tk6/make_set.py; the literals are the source.
"""

from shared.types import AgentConfig, ScenarioConfig, Script
from domains.dock_loading.actions import move_to
from domains.dock_loading.script import (coffee_break, confirm_delivered_pallet, deliver_pallet, go_to, load_return,
                                         office_break, stand)
from shared.types import Timeline
from domains.dock_loading.script import window
from domains.dock_loading.facts import BREAK_TIME


# T-K part 1, step 6 (6 October 2026): the planning scripts on env_layout_02 and the new scripts (analysis/dock_loading/tk6/make_set.py bases).
scenario_s10_01 = ScenarioConfig(
    id="scenario_s10_01",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6: scenario_s08_01's script and pools, unchanged, on env_layout_02 (env_setup_10, kind "
        "3), so that the planning runs cover three rooms (Hadi, 6 October 2026). The distances and derived "
        "durations its description states are env_layout_03's; they do not hold here. scenario_s08_01's "
        "description begins: MPB on dock_loading, K1, the control"
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
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
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s10_02 = ScenarioConfig(
    id="scenario_s10_02",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6: scenario_s08_02's script and pools, unchanged, on env_layout_02 (env_setup_10, kind "
        "3), so that the planning runs cover three rooms (Hadi, 6 October 2026). The distances and derived "
        "durations its description states are env_layout_03's; they do not hold here. scenario_s08_02's "
        "description begins: MPB on dock_loading, K2, admission and the admitted projection (meeting form 1)"
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
            ],
        ),
    ],
)


scenario_s10_03 = ScenarioConfig(
    id="scenario_s10_03",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6: scenario_s08_03's script and pools, unchanged, on env_layout_02 (env_setup_10, kind "
        "3), so that the planning runs cover three rooms (Hadi, 6 October 2026). The distances and derived "
        "durations its description states are env_layout_03's; they do not hold here. scenario_s08_03's "
        "description begins: MPB on dock_loading, K3, the stand at a bay with an alternative task (meeting form 2)"
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
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
            ],
        ),
    ],
)


scenario_s10_04 = ScenarioConfig(
    id="scenario_s10_04",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6: scenario_s08_04's script and pools, unchanged, on env_layout_02 (env_setup_10, kind "
        "3), so that the planning runs cover three rooms (Hadi, 6 October 2026). The distances and derived "
        "durations its description states are env_layout_03's; they do not hold here. scenario_s08_04's "
        "description begins: MPB on dock_loading, K4, the stand at a bay with no alternative"
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
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
            ],
        ),
    ],
)


scenario_s10_05 = ScenarioConfig(
    id="scenario_s10_05",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6: scenario_s08_05's script and pools, unchanged, on env_layout_02 (env_setup_10, kind "
        "3), so that the planning runs cover three rooms (Hadi, 6 October 2026). The distances and derived "
        "durations its description states are env_layout_03's; they do not hold here. scenario_s08_05's "
        "description begins: MPB on dock_loading, K5, the same motion"
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_1"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_1"),
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
            ],
        ),
    ],
)


scenario_s10_06 = ScenarioConfig(
    id="scenario_s10_06",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6: scenario_s08_06's script and pools, unchanged, on env_layout_02 (env_setup_10, kind "
        "3), so that the planning runs cover three rooms (Hadi, 6 October 2026). The distances and derived "
        "durations its description states are env_layout_03's; they do not hold here. scenario_s08_06's "
        "description begins: MPB on dock_loading, K6, a foreseeable task between scans"
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


scenario_s10_07 = ScenarioConfig(
    id="scenario_s10_07",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6: scenario_s08_07's script and pools, unchanged, on env_layout_02 (env_setup_10, kind "
        "3), so that the planning runs cover three rooms (Hadi, 6 October 2026). The distances and derived "
        "durations its description states are env_layout_03's; they do not hold here. scenario_s08_07's "
        "description begins: MPB on dock_loading, K7, the office"
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


scenario_s10_08 = ScenarioConfig(
    id="scenario_s10_08",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6: scenario_s08_08's script and pools, unchanged, on env_layout_02 (env_setup_10, kind "
        "3), so that the planning runs cover three rooms (Hadi, 6 October 2026). The distances and derived "
        "durations its description states are env_layout_03's; they do not hold here. scenario_s08_08's "
        "description begins: MPB on dock_loading, K8, the change during an action"
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").during(move_to, "PT52S", coffee_break("coffee_machine_0"), occurrence=0),
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
            ],
        ),
    ],
)


scenario_s10_09 = ScenarioConfig(
    id="scenario_s10_09",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6: scenario_s08_09's script and pools, unchanged, on env_layout_02 (env_setup_10, kind "
        "3), so that the planning runs cover three rooms (Hadi, 6 October 2026). The distances and derived "
        "durations its description states are env_layout_03's; they do not hold here. scenario_s08_09's "
        "description begins: MPB on dock_loading, K9, the admission that is wrong about the human"
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    go_to("standby_place"),
                    stand("PT60S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
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
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s10_10 = ScenarioConfig(
    id="scenario_s10_10",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6: scenario_s08_10's script and pools, unchanged, on env_layout_02 (env_setup_10, kind "
        "3), so that the planning runs cover three rooms (Hadi, 6 October 2026). The distances and derived "
        "durations its description states are env_layout_03's; they do not hold here. scenario_s08_10's "
        "description begins: MPB on dock_loading, M3, combined deviations (mixed; independent of the robot, kind "
        "3, full"
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                    confirm_delivered_pallet("pallet_1"),
                    confirm_delivered_pallet("pallet_2"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_1"),
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


scenario_s10_11 = ScenarioConfig(
    id="scenario_s10_11",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6, script a (a coffee break first, before any scan), on env_layout_02: the human takes a "
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


scenario_s10_12 = ScenarioConfig(
    id="scenario_s10_12",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6, script b (scans only, across both bays), on env_layout_02: the human scans pallet_0, "
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


scenario_s10_13 = ScenarioConfig(
    id="scenario_s10_13",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6, script c (an office break inside a scan, on arrival at the bay before the scan), on "
        "env_layout_02: the human scans pallet_0 with an office break on arrival at the bay, scans pallet_2, then "
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


scenario_s10_14 = ScenarioConfig(
    id="scenario_s10_14",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6, script d (a second coffee break inside the first's recency), on env_layout_02: the "
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


scenario_s10_15 = ScenarioConfig(
    id="scenario_s10_15",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6, script e (a coffee break, then an office break), on env_layout_02: the human scans "
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


scenario_s10_16 = ScenarioConfig(
    id="scenario_s10_16",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6, script e' (an office break, then a coffee break), on env_layout_02: the human scans "
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


scenario_s10_17 = ScenarioConfig(
    id="scenario_s10_17",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6, script f (one coffee break between two scans, for the three window edges), on "
        "env_layout_02: the human scans pallet_2, takes a coffee break, scans pallet_0, then the walk to the desk; "
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


scenario_s10_18 = ScenarioConfig(
    id="scenario_s10_18",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    description=(
        "T-K part 1, step 6, script g (a coffee break once every scan is done (no assigned task live)), on "
        "env_layout_02: the human scans pallet_0, scans pallet_2, takes a coffee break, then the walk to the desk; "
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
scenario_s10_19 = ScenarioConfig(
    id="scenario_s10_19",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s10_01's copy with break_time from 0 to 30 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_01's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
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
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s10_20 = ScenarioConfig(
    id="scenario_s10_20",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 30, 55),)),
    description=(
        "T-K part 1, step 6: scenario_s10_01's copy with break_time from 30 to 55 (V2, over another task; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_01's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
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
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s10_21 = ScenarioConfig(
    id="scenario_s10_21",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s10_02's copy with break_time from 0 to 30 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_02's."
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
            ],
        ),
    ],
)


scenario_s10_22 = ScenarioConfig(
    id="scenario_s10_22",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 30, 83),)),
    description=(
        "T-K part 1, step 6: scenario_s10_02's copy with break_time from 30 to 83 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_02's."
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
            ],
        ),
    ],
)


scenario_s10_23 = ScenarioConfig(
    id="scenario_s10_23",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s10_03's copy with break_time from 0 to 30 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_03's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
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
            ],
        ),
    ],
)


scenario_s10_24 = ScenarioConfig(
    id="scenario_s10_24",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 30, 127),)),
    description=(
        "T-K part 1, step 6: scenario_s10_03's copy with break_time from 30 to 127 (V2, over another task; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_03's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
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
            ],
        ),
    ],
)


scenario_s10_25 = ScenarioConfig(
    id="scenario_s10_25",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s10_04's copy with break_time from 0 to 30 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_04's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
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
            ],
        ),
    ],
)


scenario_s10_26 = ScenarioConfig(
    id="scenario_s10_26",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 30, 127),)),
    description=(
        "T-K part 1, step 6: scenario_s10_04's copy with break_time from 30 to 127 (V2, over another task; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_04's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
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
            ],
        ),
    ],
)


scenario_s10_27 = ScenarioConfig(
    id="scenario_s10_27",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s10_05's copy with break_time from 0 to 30 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_05's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_1"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_1"),
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
            ],
        ),
    ],
)


scenario_s10_28 = ScenarioConfig(
    id="scenario_s10_28",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 30, 33),)),
    description=(
        "T-K part 1, step 6: scenario_s10_05's copy with break_time from 30 to 33 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_05's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0"),
                    confirm_delivered_pallet("pallet_1"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_1"),
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
            ],
        ),
    ],
)


scenario_s10_29 = ScenarioConfig(
    id="scenario_s10_29",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 30, 112),)),
    description=(
        "T-K part 1, step 6: scenario_s10_06's copy with break_time from 30 to 112 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_06's."
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


scenario_s10_30 = ScenarioConfig(
    id="scenario_s10_30",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s10_06's copy with break_time from 0 to 30 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_06's."
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


scenario_s10_31 = ScenarioConfig(
    id="scenario_s10_31",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 30, 110),)),
    description=(
        "T-K part 1, step 6: scenario_s10_07's copy with break_time from 30 to 110 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_07's."
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


scenario_s10_32 = ScenarioConfig(
    id="scenario_s10_32",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s10_07's copy with break_time from 0 to 30 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_07's."
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


scenario_s10_33 = ScenarioConfig(
    id="scenario_s10_33",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 26, 107),)),
    description=(
        "T-K part 1, step 6: scenario_s10_08's copy with break_time from 26 to 107 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_08's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").during(move_to, "PT52S", coffee_break("coffee_machine_0"), occurrence=0),
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
            ],
        ),
    ],
)


scenario_s10_34 = ScenarioConfig(
    id="scenario_s10_34",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 26),)),
    description=(
        "T-K part 1, step 6: scenario_s10_08's copy with break_time from 0 to 26 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_08's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").during(move_to, "PT52S", coffee_break("coffee_machine_0"), occurrence=0),
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
            ],
        ),
    ],
)


scenario_s10_35 = ScenarioConfig(
    id="scenario_s10_35",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s10_09's copy with break_time from 0 to 30 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_09's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    go_to("standby_place"),
                    stand("PT60S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
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
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s10_36 = ScenarioConfig(
    id="scenario_s10_36",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 30, 57),)),
    description=(
        "T-K part 1, step 6: scenario_s10_09's copy with break_time from 30 to 57 (V2, over another task; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_09's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_2"),
                    go_to("standby_place"),
                    stand("PT60S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
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
                load_return("pallet_6"),
            ],
        ),
    ],
)


scenario_s10_37 = ScenarioConfig(
    id="scenario_s10_37",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 28, 110),)),
    description=(
        "T-K part 1, step 6: scenario_s10_10's copy with break_time from 28 to 110 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_10's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                    confirm_delivered_pallet("pallet_1"),
                    confirm_delivered_pallet("pallet_2"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_1"),
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


scenario_s10_38 = ScenarioConfig(
    id="scenario_s10_38",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 28),)),
    description=(
        "T-K part 1, step 6: scenario_s10_10's copy with break_time from 0 to 28 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_10's."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 0),
            scheduled_tasks=Script(
                [
                    confirm_delivered_pallet("pallet_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                    confirm_delivered_pallet("pallet_1"),
                    confirm_delivered_pallet("pallet_2"),
                    stand("PT192S"),
                ],
                closing=[go_to("desk")],
            ),
            observes=[],
            assigned_tasks=[
                confirm_delivered_pallet("pallet_0"),
                confirm_delivered_pallet("pallet_1"),
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


scenario_s10_39 = ScenarioConfig(
    id="scenario_s10_39",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 56),)),
    description=(
        "T-K part 1, step 6: scenario_s10_11's copy with break_time from 0 to 56 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_11's."
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


scenario_s10_40 = ScenarioConfig(
    id="scenario_s10_40",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 56, 109),)),
    description=(
        "T-K part 1, step 6: scenario_s10_11's copy with break_time from 56 to 109 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_11's."
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


scenario_s10_41 = ScenarioConfig(
    id="scenario_s10_41",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s10_12's copy with break_time from 0 to 30 (V1, over the first scan; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_12's."
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


scenario_s10_42 = ScenarioConfig(
    id="scenario_s10_42",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 30, 83),)),
    description=(
        "T-K part 1, step 6: scenario_s10_12's copy with break_time from 30 to 83 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_12's."
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


scenario_s10_43 = ScenarioConfig(
    id="scenario_s10_43",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 28, 108),)),
    description=(
        "T-K part 1, step 6: scenario_s10_13's copy with break_time from 28 to 108 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_13's."
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


scenario_s10_44 = ScenarioConfig(
    id="scenario_s10_44",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 28),)),
    description=(
        "T-K part 1, step 6: scenario_s10_13's copy with break_time from 0 to 28 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_13's."
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


scenario_s10_45 = ScenarioConfig(
    id="scenario_s10_45",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 56),)),
    description=(
        "T-K part 1, step 6: scenario_s10_14's copy with break_time from 0 to 56 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_14's."
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


scenario_s10_46 = ScenarioConfig(
    id="scenario_s10_46",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 56, 109),)),
    description=(
        "T-K part 1, step 6: scenario_s10_14's copy with break_time from 56 to 109 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_14's."
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


scenario_s10_47 = ScenarioConfig(
    id="scenario_s10_47",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 56), window(BREAK_TIME, 109, 191),)),
    description=(
        "T-K part 1, step 6: scenario_s10_14's copy with break_time from 0 to 56 and from 109 to 191 (V3, over "
        "both breaks; the rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is "
        "scenario_s10_14's."
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


scenario_s10_48 = ScenarioConfig(
    id="scenario_s10_48",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 30, 112),)),
    description=(
        "T-K part 1, step 6: scenario_s10_15's copy with break_time from 30 to 112 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_15's."
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


scenario_s10_49 = ScenarioConfig(
    id="scenario_s10_49",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s10_15's copy with break_time from 0 to 30 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_15's."
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


scenario_s10_50 = ScenarioConfig(
    id="scenario_s10_50",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 30, 112), window(BREAK_TIME, 112, 193),)),
    description=(
        "T-K part 1, step 6: scenario_s10_15's copy with break_time from 30 to 112 and from 112 to 193 (V3, over "
        "both breaks; the rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is "
        "scenario_s10_15's."
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


scenario_s10_51 = ScenarioConfig(
    id="scenario_s10_51",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 30, 110),)),
    description=(
        "T-K part 1, step 6: scenario_s10_16's copy with break_time from 30 to 110 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_16's."
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


scenario_s10_52 = ScenarioConfig(
    id="scenario_s10_52",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s10_16's copy with break_time from 0 to 30 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_16's."
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


scenario_s10_53 = ScenarioConfig(
    id="scenario_s10_53",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 30, 110), window(BREAK_TIME, 110, 176),)),
    description=(
        "T-K part 1, step 6: scenario_s10_16's copy with break_time from 30 to 110 and from 110 to 176 (V3, over "
        "both breaks; the rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is "
        "scenario_s10_16's."
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


scenario_s10_54 = ScenarioConfig(
    id="scenario_s10_54",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 20, 70),)),
    description=(
        "T-K part 1, step 6: scenario_s10_17's copy with break_time from 20 to 70 (edge before the human leaves; "
        "the rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_17's."
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


scenario_s10_55 = ScenarioConfig(
    id="scenario_s10_55",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 34, 70),)),
    description=(
        "T-K part 1, step 6: scenario_s10_17's copy with break_time from 34 to 70 (edge in the walk; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_17's."
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


scenario_s10_56 = ScenarioConfig(
    id="scenario_s10_56",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 39, 70),)),
    description=(
        "T-K part 1, step 6: scenario_s10_17's copy with break_time from 39 to 70 (edge at the arrival; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_17's."
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


scenario_s10_57 = ScenarioConfig(
    id="scenario_s10_57",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 83, 123),)),
    description=(
        "T-K part 1, step 6: scenario_s10_18's copy with break_time from 83 to 123 (V1, over the first break; the "
        "rule: analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_18's."
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


scenario_s10_58 = ScenarioConfig(
    id="scenario_s10_58",
    setup="env_setup_10",
    reference_layouts=["env_layout_02"],
    timeline=Timeline((window(BREAK_TIME, 0, 30),)),
    description=(
        "T-K part 1, step 6: scenario_s10_18's copy with break_time from 0 to 30 (V2, over a scan; the rule: "
        "analysis/dock_loading/tk6/make_set.py, windows). Everything else is scenario_s10_18's."
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
