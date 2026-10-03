### scenario_s09_09

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 61 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 63 | deliver_item(item_3,kitting_table_0) | covered | move_to | 0 | 1 |
| 84 | deliver_item(item_3,kitting_table_0) | covered | pick_up | 0 | 1 |
| 86 | deliver_item(item_3,kitting_table_0) | covered | move_to | 1 | 1 |
| 107 | deliver_item(item_3,kitting_table_0) | covered | place | 0 | 1 |
| 109 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 140 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 142 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 172 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 174 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 221; idle from 222 to 251. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 251 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 58 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 59 to 60 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1,shelf_1) | 30 to 31 |
| deliver_item(item_2) | move_to(shelf_1) | 32 to 60 |
| deliver_item(item_2) | move_to(item_2) | 61 to 83 |
| deliver_item(item_2) | place(item_3,shelf_3) | 84 to 85 |
| deliver_item(item_2) | move_to(shelf_3) | 86 to 106 |
| deliver_item(item_2) | move_to(item_2) | 107 to 137 |
| deliver_item(item_2) | pick_up(item_2) | 138 to 139 |
| deliver_item(item_2) | move_to(kitting_table_0) | 140 to 169 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 170 to 171 |

Events (actual):

| tick | event |
|---|---|
| 61 | boundary |
| 61 | pin deliver_item(item_1) |
| 83 | finding turns unexplained |
| 84 | finding turns adequate (from unexplained) |
| 86 | finding turns unexplained |
| 87 | finding turns adequate (from unexplained) |
| 95 | finding turns unexplained |
| 107 | boundary (no pin) |
| 107 | finding turns unresolved (from unexplained) |
| 172 | boundary |
| 172 | pin deliver_item(item_2) |
| 205 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_SE), ticks 174 to 221): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 62 | 25 | 0.7544 | yes | adequate |
| deliver_item(item_3) | 63 to 108 | outside the support (at the floor) | - | - | - |
| deliver_item(item_2) | 109 to 173 | 123 | 0.7717 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 34 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0579 | 0.0451 | 345.0 | 285.0 | 60.0 | deliver_item(item_1) |
| 41 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 73 | deliver_item(item_2) | move_to(item_2) | 0.1314 | 0.0399 | 357.5 | 357.5 | 0.0 | deliver_item(item_3) |
| 83 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9690 | 0.0468 | 341.3 | 321.3 | 20.0 | deliver_item(item_3) |
| 95 | deliver_item(item_2) | move_to(shelf_3) | 0.0166 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 132 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0627 | 0.0492 | 336.2 | 336.2 | 0.0 | deliver_item(item_2) |
| 205 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0483 | 338.1 | 338.1 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 61 | adequate | unresolved | deliver_item(item_1) |
| 62 | unresolved | adequate | deliver_item(item_1) |
| 83 | adequate | unexplained | deliver_item(item_3) |
| 84 | unexplained | adequate | deliver_item(item_3) |
| 86 | adequate | unexplained | deliver_item(item_3) |
| 87 | unexplained | adequate | deliver_item(item_3) |
| 95 | adequate | unexplained | deliver_item(item_3) |
| 107 | unexplained | unresolved | deliver_item(item_3) |
| 108 | unresolved | adequate | deliver_item(item_3) |
| 172 | adequate | unresolved | deliver_item(item_2) |
| 173 | unresolved | adequate | deliver_item(item_2) |
| 205 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 60, 63 to 103, 109 to 169, 174 to 251 |
| deliver_item(item_1) | 0 to 60 |
| deliver_item(item_2) | 0 to 1, 109 to 171 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 24 | deliver_item(item_1) | none(below_theta) |
| 25 to 60 | deliver_item(item_1) | clears |
| 61 to 69 | coffee_break(coffee_machine_0) | none(below_theta) |
| 70 to 82 | coffee_break(coffee_machine_0) | clears |
| 83 to 106 | coffee_break(coffee_machine_0) | none(leader_inadequate) |
| 107 to 108 | coffee_break(coffee_machine_0) | none(below_theta) |
| 109 to 122 | deliver_item(item_2) | none(below_theta) |
| 123 to 171 | deliver_item(item_2) | clears |
| 172 to 172 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 173 to 173 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 174 to 204 | coffee_break(coffee_machine_0) | clears |
| 205 to 251 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_SE)): first step 174, last step 220, acknowledgement 221; the idle human from 222. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 174; S < α from 205 (belief 0.9970; v·D 338.1 cm); the finding unexplained from 205.

