### scenario_s09_04

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 53 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 84 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 106 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 108 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 139 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 141 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 171 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 173 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 202 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 204 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 251; idle from 252 to 281. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 50 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 51 to 81 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 84 to 281 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 30 |
| deliver_item(item_1) | move_to(item_1) | 31 to 103 |
| deliver_item(item_1) | pick_up(item_1) | 104 to 105 |
| deliver_item(item_1) | move_to(kitting_table_0) | 106 to 136 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 137 to 138 |
| deliver_item(item_2) | move_to(item_2) | -1 to 105 |
| deliver_item(item_2) | place(item_1,shelf_1) | 106 to 108 |
| deliver_item(item_2) | move_to(shelf_1) | 109 to 138 |
| deliver_item(item_2) | move_to(item_2) | 139 to 168 |
| deliver_item(item_2) | pick_up(item_2) | 169 to 170 |
| deliver_item(item_2) | move_to(kitting_table_0) | 171 to 199 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 200 to 201 |

Events (actual):

| tick | event |
|---|---|
| 82 | boundary |
| 82 | pin coffee_break(coffee_machine_0) |
| 84 | re-entry coffee_break(coffee_machine_0) |
| 139 | boundary |
| 139 | pin deliver_item(item_1) |
| 202 | boundary |
| 202 | pin deliver_item(item_2) |
| 235 | finding turns unexplained |

Never pinned: none. At the last entry (go_to(corner_SE), ticks 204 to 251): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 29 | 25 | 0.7552 | yes | adequate |
| coffee_break(coffee_machine_0) | 30 to 83 | 40 | 0.7681 | yes | adequate |
| deliver_item(item_1) | 84 to 140 | 92 | 0.7742 | yes | adequate |
| deliver_item(item_2) | 141 to 203 | 154 | 0.7526 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 40 | deliver_item(item_1) | move_to(item_1) | 0.2309 | 0.0422 | 351.8 | 351.8 | 0.0 | coffee_break(coffee_machine_0) |
| 93 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0412 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 97 | deliver_item(item_2) | move_to(item_2) | 0.0572 | 0.0450 | 345.2 | 345.2 | 0.0 | deliver_item(item_1) |
| 118 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0395 | 358.3 | 358.3 | 0.0 | deliver_item(item_1) |
| 164 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0611 | 0.0478 | 339.0 | 339.0 | 0.0 | deliver_item(item_2) |
| 235 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0456 | 343.9 | 343.9 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 82 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 83 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 139 | adequate | unresolved | deliver_item(item_1) |
| 140 | unresolved | adequate | deliver_item(item_1) |
| 202 | adequate | unresolved | deliver_item(item_2) |
| 203 | unresolved | adequate | deliver_item(item_2) |
| 235 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 30 to 83, its hypothesis pinned at 82; the suspended task resumes at 84.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|
| 28 | move_to step | deliver_item(item_1) | 0.1859 / 0.1754 | 0.8121 / 1.0000 | 0.0010 / 0.0005 | adequate |
| 29 | move_to  | deliver_item(item_1) | 0.1603 / 0.1451 | 0.8377 / 1.0000 | 0.0010 / 0.0004 | adequate |
| 30 | move_to step | coffee_break(coffee_machine_0) | 0.1603 / 0.1451 | 0.8377 / 1.0000 | 0.0010 / 0.0004 | adequate |
| 31 | move_to step | coffee_break(coffee_machine_0) | 0.1603 / 0.1451 | 0.8377 / - | 0.0010 / 0.0004 | adequate |
| 32 | move_to step | coffee_break(coffee_machine_0) | 0.1891 / 0.1451 | 0.8089 / 0.7594 | 0.0010 / 0.0003 | adequate |
| 81 | wait_at stand | coffee_break(coffee_machine_0) | 0.9970 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 82 | wait_at stand | coffee_break(coffee_machine_0) | retired | 0.4990 / - | 0.4990 / - | unresolved |
| 83 | wait_at  | coffee_break(coffee_machine_0) | retired | 0.4990 / 1.0000 | 0.4990 / 1.0000 | adequate |
| 84 | move_to step | deliver_item(item_1) | 0.3330 / - | 0.3515 / 1.0000 | 0.3145 / 0.8554 | adequate |
| 85 | move_to step | deliver_item(item_1) | 0.2980 / 0.7402 | 0.3919 / 1.0000 | 0.3091 / 0.7235 | adequate |
| 86 | move_to step | deliver_item(item_1) | 0.2582 / 0.5354 | 0.4396 / 1.0000 | 0.3012 / 0.6050 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 81, 141 to 201, 204 to 281 |
| deliver_item(item_1) | 0 to 30, 84 to 138 |
| deliver_item(item_2) | 0 to 1, 141 to 201 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 24 | deliver_item(item_1) | none(below_theta) |
| 25 to 30 | deliver_item(item_1) | clears |
| 31 to 31 | deliver_item(item_1) | none(leader_no_observation) |
| 32 to 33 | deliver_item(item_1) | clears |
| 34 to 36 | deliver_item(item_1) | none(below_theta) |
| 37 to 39 | coffee_break(coffee_machine_0) | none(below_theta) |
| 40 to 81 | coffee_break(coffee_machine_0) | clears |
| 82 to 91 | deliver_item(item_1) | none(below_theta) |
| 92 to 138 | deliver_item(item_1) | clears |
| 139 to 140 | coffee_break(coffee_machine_0) | none(below_theta) |
| 141 to 153 | deliver_item(item_2) | none(below_theta) |
| 154 to 201 | deliver_item(item_2) | clears |
| 202 to 202 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 203 to 203 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 204 to 234 | coffee_break(coffee_machine_0) | clears |
| 235 to 281 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_SE)): first step 204, last step 250, acknowledgement 251; the idle human from 252. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 204; S < α from 235 (belief 0.9970; v·D 343.9 cm); the finding unexplained from 235.

