### scenario_s15_04

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_3,kitting_table_0) | covered | move_to | 0 | 1 |
| 32 | deliver_item(item_3,kitting_table_0) | covered | pick_up | 0 | 1 |
| 34 | deliver_item(item_3,kitting_table_0) | covered | move_to | 1 | 1 |
| 65 | deliver_item(item_3,kitting_table_0) | covered | place | 0 | 1 |
| 67 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 94 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 96 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 122 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 124 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 169 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 171 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 215 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 217 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 259 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 290 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 308 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 310 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 355 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 357 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 378; idle from 379 to 408. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 408 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 256 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 257 to 287 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 290 to 408 |
| deliver_item(item_1) | move_to(item_1) | -1 to 31 |
| deliver_item(item_1) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_1) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_1) | move_to(item_1) | 65 to 93 |
| deliver_item(item_1) | place(item_2,shelf_2) | 94 to 95 |
| deliver_item(item_1) | move_to(shelf_2) | 96 to 121 |
| deliver_item(item_1) | move_to(item_1) | 122 to 166 |
| deliver_item(item_1) | pick_up(item_1) | 167 to 168 |
| deliver_item(item_1) | move_to(kitting_table_0) | 169 to 212 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 213 to 214 |
| deliver_item(item_2) | move_to(item_2) | -1 to 31 |
| deliver_item(item_2) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_2) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_2) | move_to(item_2) | 65 to 91 |
| deliver_item(item_2) | pick_up(item_2) | 92 to 93 |
| deliver_item(item_2) | move_to(kitting_table_0) | 94 to 119 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 120 to 121 |
| deliver_item(item_3) | move_to(item_3) | -1 to 29 |
| deliver_item(item_3) | pick_up(item_3) | 30 to 31 |
| deliver_item(item_3) | move_to(kitting_table_0) | 32 to 62 |
| deliver_item(item_3) | place(item_3,kitting_table_0) | 63 to 64 |
| deliver_item(item_4) | move_to(item_4) | -1 to 31 |
| deliver_item(item_4) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_4) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_4) | move_to(item_4) | 65 to 93 |
| deliver_item(item_4) | place(item_2,shelf_2) | 94 to 95 |
| deliver_item(item_4) | move_to(shelf_2) | 96 to 121 |
| deliver_item(item_4) | move_to(item_4) | 122 to 168 |
| deliver_item(item_4) | place(item_1,shelf_1) | 169 to 170 |
| deliver_item(item_4) | move_to(shelf_1) | 171 to 214 |
| deliver_item(item_4) | move_to(item_4) | 215 to 305 |
| deliver_item(item_4) | pick_up(item_4) | 306 to 307 |
| deliver_item(item_4) | move_to(kitting_table_0) | 308 to 352 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 353 to 354 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 122 | boundary |
| 122 | pin deliver_item(item_2) |
| 215 | boundary |
| 215 | pin deliver_item(item_1) |
| 288 | boundary |
| 288 | pin coffee_break(coffee_machine_0) |
| 290 | re-entry coffee_break(coffee_machine_0) |
| 355 | boundary |
| 355 | pin deliver_item(item_4) |
| 379 | finding turns unexplained |

Never pinned: ac_activation(ac_switch_0). At the last entry (go_to(corner_NE), ticks 357 to 378): lifecycle and finding adequate; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 28 | 0.7518 | yes | adequate |
| deliver_item(item_2) | 67 to 123 | 97 | 0.7820 | yes | adequate |
| deliver_item(item_1) | 124 to 216 | 171 | 0.7635 | yes | adequate |
| coffee_break(coffee_machine_0) | 217 to 289 | 252 | 0.7732 | yes | adequate |
| deliver_item(item_4) | 290 to 356 | 313 | 0.7592 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 12 | deliver_item(item_2) | move_to(item_2) | 0.0183 | 0.0383 | 361.6 | 361.6 | 0.0 | deliver_item(item_3) |
| 16 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0292 | 0.0495 | 335.5 | 335.5 | 0.0 | deliver_item(item_3) |
| 25 | deliver_item(item_4) | move_to(item_4) | 0.0402 | 0.0441 | 347.2 | 347.2 | 0.0 | deliver_item(item_3) |
| 30 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0493 | 0.0450 | 345.3 | 345.3 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_1) | move_to(shelf_3) | 0.0057 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_2) | move_to(shelf_3) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_4) | move_to(shelf_3) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 87 | deliver_item(item_1) | move_to(item_1) | 0.0274 | 0.0418 | 352.6 | 352.6 | 0.0 | deliver_item(item_2) |
| 91 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0315 | 0.0412 | 354.1 | 354.1 | 0.0 | deliver_item(item_2) |
| 101 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0485 | 0.0383 | 361.4 | 301.4 | 60.0 | deliver_item(item_2) |
| 105 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 105 | deliver_item(item_4) | move_to(shelf_2) | 0.0037 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 153 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0268 | 0.0498 | 334.8 | 334.8 | 0.0 | deliver_item(item_1) |
| 176 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0512 | 0.0403 | 356.4 | 296.4 | 60.0 | deliver_item(item_1) |
| 180 | deliver_item(item_4) | move_to(shelf_1) | 0.0041 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 253 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0496 | 0.0456 | 343.8 | 343.8 | 0.0 | coffee_break(coffee_machine_0) |
| 259 | deliver_item(item_4) | move_to(item_4) | 0.0596 | 0.0475 | 339.7 | 299.7 | 40.0 | coffee_break(coffee_machine_0) |
| 299 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0290 | 0.0437 | 348.2 | 348.2 | 0.0 | deliver_item(item_4) |
| 319 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0488 | 0.0377 | 363.2 | 303.2 | 60.0 | deliver_item(item_4) |
| 370 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.1844 | 0.0491 | 336.3 | 336.3 | 0.0 | - |
| 379 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9055 | 0.0477 | 339.2 | 299.2 | 40.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_3) |
| 65 | adequate | unresolved | deliver_item(item_3) |
| 66 | unresolved | adequate | deliver_item(item_3) |
| 122 | adequate | unresolved | deliver_item(item_2) |
| 123 | unresolved | adequate | deliver_item(item_2) |
| 215 | adequate | unresolved | deliver_item(item_1) |
| 216 | unresolved | adequate | deliver_item(item_1) |
| 288 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 289 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 355 | adequate | unresolved | deliver_item(item_4) |
| 356 | unresolved | adequate | deliver_item(item_4) |
| 379 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 64, 67 to 119, 124 to 214, 217 to 287, 290 to 332 |
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 121, 124 to 214, 217 to 287, 357 to 408 |
| deliver_item(item_1) | 0 to 31, 67 to 93, 124 to 214 |
| deliver_item(item_2) | 67 to 121 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 93, 124 to 168, 217 to 287, 290 to 354 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 27 | deliver_item(item_3) | none(below_theta) |
| 28 to 64 | deliver_item(item_3) | clears |
| 65 to 66 | ac_activation(ac_switch_0) | none(below_theta) |
| 67 to 96 | deliver_item(item_2) | none(below_theta) |
| 97 to 121 | deliver_item(item_2) | clears |
| 122 to 123 | ac_activation(ac_switch_0) | none(below_theta) |
| 124 to 170 | deliver_item(item_1) | none(below_theta) |
| 171 to 214 | deliver_item(item_1) | clears |
| 215 to 216 | ac_activation(ac_switch_0) | none(below_theta) |
| 217 to 251 | coffee_break(coffee_machine_0) | none(below_theta) |
| 252 to 287 | coffee_break(coffee_machine_0) | clears |
| 288 to 289 | ac_activation(ac_switch_0) | none(below_theta) |
| 290 to 312 | deliver_item(item_4) | none(below_theta) |
| 313 to 354 | deliver_item(item_4) | clears |
| 355 to 356 | ac_activation(ac_switch_0) | none(below_theta) |
| 357 to 366 | coffee_break(coffee_machine_0) | none(below_theta) |
| 367 to 378 | coffee_break(coffee_machine_0) | clears |
| 379 to 408 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_NE)): first step 357, last step 377, acknowledgement 378; the idle human from 379. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.4827 at 357; S < α from 370 (belief 0.1844; v·D 336.3 cm); the finding unexplained from 379.

- coffee_break(coffee_machine_0): belief 0.5133 at 357; S < α from 379 (belief 0.9055; v·D 339.2 cm); the finding unexplained from 379.

