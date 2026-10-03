# domains/kitting/scenarios/scenarios_s09.py
"""
Kitting scenarios on env_setup_09 — the IRB on its enlarged room (IRB.4b; design_records.md, "The intention-recognition test-bed (IRB)"; TODO-122). One module per setup. Every task instance is written in the kitting call form
(domains/kitting/script.py), a human's script as a Script of task instances with events (T-H): an event's anchor is
an action schema of the task's decomposition.
The room is env_layout_11 (env_layout_10 plus kitting_table_1 and shelf_3), the shift env_setup_09 (item_1, item_2,
item_3, all designated to kitting_table_0). The recognizer is tested in isolation: the robot has an empty task pool
and only observes; the human starts at the kitting table, is assigned two deliveries (never in an order; item_1 and
item_2, or item_1 and item_3 in _10 and _11) and ends every script with the exit walk to corner_SE. Prior ON in every
run (configs/irb/). The coffee break's duration is the schema's.
_01 to _04: the four IRB.3b scripts (scenarios_s08.py) re-authored on this room; _05 to _09: the deviations; _10 to _12:
the alternates, both deliveries on the same side and the reverse order; _13 (Track 2.5): the mid-action change, a
coffee_break cut into item_1's carry.
"""

from shared.types import AgentConfig, ScenarioConfig, Script
from domains.kitting.actions import move_to, pick_up
from domains.kitting.script import deliver_item, coffee_break, go_to, stand


# ===============================================================
# the IRB, on "env_layout_11" (analysis/irb/)
# ===============================================================
_IRB = (
    "IRB, enlarged room: the recognizer in isolation, against expectations derived from the records "
    "before the run (analysis/irb/). The robot at (0.10 W, 0.10 H) with an empty task pool, observing only; the "
    "human starts at the kitting table, assigned deliver_item(item_1) and deliver_item(item_2), and ends with the exit "
    "walk to corner_SE. Prior on: deliver_item(item_3) is outside the support. "
)
_IRB_WEST = (
    "IRB, enlarged room: the recognizer in isolation, against expectations derived from the records "
    "before the run (analysis/irb/). The robot at (0.10 W, 0.10 H) with an empty task pool, observing only; the "
    "human starts at the kitting table, assigned deliver_item(item_1) and deliver_item(item_3), both on the west side, "
    "and ends with the exit walk to corner_SE. Prior on: deliver_item(item_2) is outside the support. "
)

scenario_s09_01 = ScenarioConfig(
    id="scenario_s09_01",
    setup="env_setup_09",
    reference_layouts=["env_layout_11"],
    description=_IRB + (
        "scenario_s09_01, two deliveries (scenario_s08_01 on this room): deliver item_1, deliver item_2, exit. "
        "After both deliveries coffee_break is the lone live hypothesis and the exit walk is charged against its walk to the "
        "machine (TODO-117's case). Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s09_02 = ScenarioConfig(
    id="scenario_s09_02",
    setup="env_setup_09",
    reference_layouts=["env_layout_11"],
    description=_IRB + (
        "scenario_s09_02, coffee between (scenario_s08_02 on this room): deliver item_1, coffee_break, deliver "
        "item_2, exit. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s09_03 = ScenarioConfig(
    id="scenario_s09_03",
    setup="env_setup_09",
    reference_layouts=["env_layout_11"],
    description=_IRB + (
        "scenario_s09_03, coffee after the pick-up (scenario_s08_03 on this room): coffee_break started at the "
        "boundary after item_1's pick_up (the item in hand during the break), then deliver item_2, exit. L's subject: "
        "the expectations are mechanical. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(pick_up, coffee_break("coffee_machine_0")),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s09_04 = ScenarioConfig(
    id="scenario_s09_04",
    setup="env_setup_09",
    reference_layouts=["env_layout_11"],
    description=_IRB + (
        "scenario_s09_04, coffee before the pick-up (scenario_s08_04 on this room): coffee_break started at the "
        "boundary after item_1's first move_to (empty-handed at the shelf), then deliver item_2, exit. L's subject: the "
        "expectations are mechanical. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(move_to, coffee_break("coffee_machine_0"), occurrence=0),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s09_05 = ScenarioConfig(
    id="scenario_s09_05",
    setup="env_setup_09",
    reference_layouts=["env_layout_11"],
    description=_IRB + (
        "scenario_s09_05, the corner walk mid-delivery (TODO-94): go_to(corner_SE) started at the boundary after "
        "item_1's pick_up (the item in hand), the carry to the table resumed, then deliver item_2, exit. Its unmodelled "
        "behaviour: the walk to corner_SE mid-delivery (TASK_ABSENT), besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(pick_up, go_to("corner_SE")),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s09_06 = ScenarioConfig(
    id="scenario_s09_06",
    setup="env_setup_09",
    reference_layouts=["env_layout_11"],
    description=_IRB + (
        "scenario_s09_06, the long stand (TODO-95): stand(PT80S) (40 ticks; Stay(40) migrated) started at the "
        "boundary after item_1's first move_to, at the shelf before the pick-up (standing beyond s_exp), then the delivery "
        "resumes, deliver item_2, exit. Its unmodelled behaviour: the stand (TASK_ABSENT), besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(move_to, stand("PT80S"), occurrence=0),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s09_07 = ScenarioConfig(
    id="scenario_s09_07",
    setup="env_setup_09",
    reference_layouts=["env_layout_11"],
    description=_IRB + (
        "scenario_s09_07, the change of mind (TODO-94): after item_1's pick_up the human delivers item_2 first "
        "(started with item_1 in hand, so expanded by deliver_with_return: item_1 back to its shelf first), then item_1's "
        "delivery resumes, re-expanded, then exit. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").at(pick_up, deliver_item("item_2", table="kitting_table_0")),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s09_08 = ScenarioConfig(
    id="scenario_s09_08",
    setup="env_setup_09",
    reference_layouts=["env_layout_11"],
    description=_IRB + (
        "scenario_s09_08, the misdelivery (TODO-87): item_1 placed on kitting_table_1 instead of its designated "
        "kitting_table_0 (a binding-level deviation: no pin, no boundary), then deliver item_2, exit. Its unmodelled "
        "behaviour: the wrong-table delivery (BINDING_ABSENT), besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_1"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s09_09 = ScenarioConfig(
    id="scenario_s09_09",
    setup="env_setup_09",
    reference_layouts=["env_layout_11"],
    description=_IRB + (
        "scenario_s09_09, a delivery outside the support (TODO-101): deliver item_1, then item_3 to "
        "kitting_table_0, which nobody is assigned (its task is modelled, COVERED, and its hypothesis is outside the support "
        "with the prior on: no pin and no boundary at its completion), then deliver item_2, exit. Modelled behaviour only, "
        "besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s09_10 = ScenarioConfig(
    id="scenario_s09_10",
    setup="env_setup_09",
    reference_layouts=["env_layout_11"],
    description=_IRB_WEST + (
        "scenario_s09_10, both deliveries west: deliver item_1, deliver item_3, exit (the walks to the two "
        "shelves share most of their bearing from the table). Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s09_11 = ScenarioConfig(
    id="scenario_s09_11",
    setup="env_setup_09",
    reference_layouts=["env_layout_11"],
    description=_IRB_WEST + (
        "scenario_s09_11, both deliveries west with coffee between: deliver item_1, coffee_break, deliver "
        "item_3, exit. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0"),
                coffee_break("coffee_machine_0"),
                deliver_item("item_3", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_3", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s09_12 = ScenarioConfig(
    id="scenario_s09_12",
    setup="env_setup_09",
    reference_layouts=["env_layout_11"],
    description=_IRB + (
        "scenario_s09_12, the deliveries of scenario_s09_01 in the reverse order: deliver item_2, deliver "
        "item_1, exit. Modelled behaviour only, besides the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_2", table="kitting_table_0"),
                deliver_item("item_1", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)

scenario_s09_13 = ScenarioConfig(
    id="scenario_s09_13",
    setup="env_setup_09",
    reference_layouts=["env_layout_11"],
    description=_IRB + (
        "scenario_s09_13, the mid-action change (Track 2.5; docs/assumptions.md, 3.1 rejected): coffee_break cut into "
        "the carry of item_1 mid-walk (T-H's during: 14 of the carry's 28 steps, PT28S), the human stopping where it "
        "stands and walking to the machine with item_1 in hand; on resumption the cut walk is completed from the "
        "machine and the delivery re-expanded (place); then deliver item_2, exit. Intent: the recognition side of the "
        "general machinery (the delivery's derived phase turns inadequate, the break's phase fits, the boundary at the "
        "break's wait_at), not the recognition-to-planning chain (the robot is idle). Modelled behaviour only, besides "
        "the exit walk."
    ),
    agents=[
        AgentConfig(
            agent_id="human_0",
            agent_type="human",
            start_position=(0, 420),
            scheduled_tasks=Script([
                deliver_item("item_1", table="kitting_table_0").during(
                    move_to, "PT28S", coffee_break("coffee_machine_0"), occurrence=1),
                deliver_item("item_2", table="kitting_table_0"),
                go_to("corner_SE"),
            ]),
            assigned_tasks=[
                deliver_item("item_1", table="kitting_table_0"),
                deliver_item("item_2", table="kitting_table_0"),
            ],
            observes=[],
        ),
        AgentConfig(
            agent_id="robot_0",
            agent_type="robot",
            start_position=(-400, 400),
            assigned_tasks=[],
            observes=["human_0"],
        ),
    ],
)
