### scenario_s09_07

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 2 |
| 33 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 2 |
| 35 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 2 |
| 76 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 2 |
| 78 | deliver_item(item_2,kitting_table_0) | covered | move_to | 2 | 2 |
| 108 | deliver_item(item_2,kitting_table_0) | covered | place | 1 | 2 |
| 110 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 140 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 142 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 171 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 173 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 221; idle from 222 to 251. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 251 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 32 |
| deliver_item(item_1) | pick_up(item_1) | 33 to 34 |
| deliver_item(item_1) | move_to(item_1) | 35 to 75 |
| deliver_item(item_1) | place(item_2,shelf_2) | 76 to 77 |
| deliver_item(item_1) | move_to(shelf_2) | 78 to 107 |
| deliver_item(item_1) | move_to(item_1) | 108 to 137 |
| deliver_item(item_1) | pick_up(item_1) | 138 to 139 |
| deliver_item(item_1) | move_to(kitting_table_0) | 140 to 168 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 169 to 170 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1,shelf_1) | 30 to 32 |
| deliver_item(item_2) | move_to(item_2) | 33 to 73 |
| deliver_item(item_2) | pick_up(item_2) | 74 to 75 |
| deliver_item(item_2) | move_to(kitting_table_0) | 76 to 105 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 106 to 107 |

Events (actual):

| tick | event |
|---|---|
| 33 | boundary (no pin) |
| 108 | boundary |
| 108 | pin deliver_item(item_2) |
| 171 | boundary |
| 171 | pin deliver_item(item_1) |
| 204 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_SE), ticks 173 to 221): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 31 | 25 | 0.7544 | yes | adequate |
| deliver_item(item_2) | 32 to 109 | 46 | 0.7524 | yes | adequate |
| deliver_item(item_1) | 110 to 172 | 135 | 0.7638 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 44 | deliver_item(item_1) | move_to(item_1) | 0.0377 | 0.0406 | 355.7 | 355.7 | 0.0 | deliver_item(item_2) |
| 53 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0625 | 0.0490 | 336.5 | 336.5 | 0.0 | deliver_item(item_2) |
| 87 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0399 | 357.4 | 357.4 | 0.0 | deliver_item(item_2) |
| 144 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0542 | 0.0420 | 352.2 | 292.2 | 60.0 | deliver_item(item_1) |
| 204 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0468 | 341.2 | 341.2 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 33 | adequate | unresolved | deliver_item(item_2) |
| 34 | unresolved | adequate | deliver_item(item_2) |
| 108 | adequate | unresolved | deliver_item(item_2) |
| 109 | unresolved | adequate | deliver_item(item_2) |
| 171 | adequate | unresolved | deliver_item(item_1) |
| 172 | unresolved | adequate | deliver_item(item_1) |
| 204 | adequate | unexplained | - |

Across the started task deliver_item(item_2,kitting_table_0) (covered; actual): on top of the stack from 32 to 109, its hypothesis pinned at 108; the suspended task resumes at 110.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|
| 30 | pick_up grasp | deliver_item(item_1) | 0.1373 / 0.1199 | 0.8608 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 31 | pick_up  | deliver_item(item_1) | 0.1167 / 0.0989 | 0.8813 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 32 | move_to  | deliver_item(item_2) | 0.1085 / 0.0814 | 0.8895 / 0.8629 | 0.0010 / 0.8629 | adequate |
| 33 | place release | deliver_item(item_2) | 0.3330 / - | 0.3330 / - | 0.3330 / - | unresolved |
| 34 | place  | deliver_item(item_2) | 0.3330 / 1.0000 | 0.3330 / 1.0000 | 0.3330 / 1.0000 | adequate |
| 107 | move_to  | deliver_item(item_2) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.9970 / 1.0000 | adequate |
| 108 | place release | deliver_item(item_2) | 0.4990 / - | 0.4990 / - | retired | unresolved |
| 109 | place  | deliver_item(item_2) | 0.4990 / 1.0000 | 0.4990 / 1.0000 | retired | adequate |
| 110 | move_to step | deliver_item(item_1) | 0.4950 / 0.9771 | 0.5030 / 1.0000 | retired | adequate |
| 111 | move_to step | deliver_item(item_1) | 0.4907 / 0.9535 | 0.5073 / 1.0000 | retired | adequate |
| 112 | move_to step | deliver_item(item_1) | 0.4861 / 0.9293 | 0.5119 / 1.0000 | retired | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 32, 35 to 58, 110 to 170, 173 to 251 |
| deliver_item(item_1) | 0 to 32, 110 to 170 |
| deliver_item(item_2) | 0 to 1, 35 to 107 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 24 | deliver_item(item_1) | none(below_theta) |
| 25 to 32 | deliver_item(item_1) | clears |
| 33 to 34 | coffee_break(coffee_machine_0) | none(below_theta) |
| 35 to 35 | deliver_item(item_1) | none(below_theta) |
| 36 to 45 | deliver_item(item_2) | none(below_theta) |
| 46 to 107 | deliver_item(item_2) | clears |
| 108 to 109 | coffee_break(coffee_machine_0) | none(below_theta) |
| 110 to 134 | deliver_item(item_1) | none(below_theta) |
| 135 to 170 | deliver_item(item_1) | clears |
| 171 to 171 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 172 to 172 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 173 to 203 | coffee_break(coffee_machine_0) | clears |
| 204 to 251 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_SE)): first step 173, last step 220, acknowledgement 221; the idle human from 222. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 173; S < α from 204 (belief 0.9970; v·D 341.2 cm); the finding unexplained from 204.

