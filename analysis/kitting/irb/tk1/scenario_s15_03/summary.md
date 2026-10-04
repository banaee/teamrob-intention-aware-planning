### scenario_s15_03

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
| 124 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 167 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 198 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 231 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 233 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 278 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 280 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 324 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 326 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 370 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 372 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 393; idle from 394 to 423. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 423 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 164 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 165 to 198 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 199 to 423 |
| deliver_item(item_1) | move_to(item_1) | -1 to 31 |
| deliver_item(item_1) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_1) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_1) | move_to(item_1) | 65 to 93 |
| deliver_item(item_1) | place(item_2,shelf_2) | 94 to 95 |
| deliver_item(item_1) | move_to(shelf_2) | 96 to 121 |
| deliver_item(item_1) | move_to(item_1) | 122 to 228 |
| deliver_item(item_1) | pick_up(item_1) | 229 to 230 |
| deliver_item(item_1) | move_to(kitting_table_0) | 231 to 275 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 276 to 277 |
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
| deliver_item(item_4) | move_to(item_4) | 122 to 230 |
| deliver_item(item_4) | place(item_1,shelf_1) | 231 to 233 |
| deliver_item(item_4) | move_to(shelf_1) | 234 to 277 |
| deliver_item(item_4) | move_to(item_4) | 278 to 321 |
| deliver_item(item_4) | pick_up(item_4) | 322 to 323 |
| deliver_item(item_4) | move_to(kitting_table_0) | 324 to 367 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 368 to 369 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 122 | boundary |
| 122 | pin deliver_item(item_2) |
| 196 | boundary |
| 196 | pin coffee_break(coffee_machine_0) |
| 198 | re-entry coffee_break(coffee_machine_0) |
| 278 | boundary |
| 278 | pin deliver_item(item_1) |
| 370 | boundary |
| 370 | pin deliver_item(item_4) |
| 394 | finding turns unexplained |

Never pinned: ac_activation(ac_switch_0). At the last entry (go_to(corner_NE), ticks 372 to 393): lifecycle and finding adequate; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 28 | 0.7518 | yes | adequate |
| deliver_item(item_2) | 67 to 123 | 97 | 0.7820 | yes | adequate |
| coffee_break(coffee_machine_0) | 124 to 197 | 160 | 0.7705 | yes | adequate |
| deliver_item(item_1) | 198 to 279 | 227 | 0.7979 | yes | adequate |
| deliver_item(item_4) | 280 to 371 | 325 | 0.7553 | yes | adequate |

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
| 154 | deliver_item(item_1) | move_to(item_1) | 0.0396 | 0.0480 | 338.6 | 338.6 | 0.0 | coffee_break(coffee_machine_0) |
| 161 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0470 | 0.0433 | 349.2 | 349.2 | 0.0 | coffee_break(coffee_machine_0) |
| 167 | deliver_item(item_4) | move_to(item_4) | 0.0558 | 0.0443 | 346.9 | 306.9 | 40.0 | coffee_break(coffee_machine_0) |
| 208 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0181 | 0.0394 | 358.8 | 358.8 | 0.0 | deliver_item(item_1) |
| 223 | deliver_item(item_4) | move_to(item_4) | 0.0397 | 0.0495 | 335.4 | 335.4 | 0.0 | deliver_item(item_1) |
| 233 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0521 | 0.0405 | 355.8 | 295.8 | 60.0 | deliver_item(item_1) |
| 243 | deliver_item(item_4) | move_to(shelf_1) | 0.0010 | 0.0392 | 359.2 | 359.2 | 0.0 | deliver_item(item_1) |
| 321 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0359 | 0.0422 | 351.8 | 351.8 | 0.0 | deliver_item(item_4) |
| 331 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0535 | 0.0419 | 352.5 | 292.5 | 60.0 | deliver_item(item_4) |
| 385 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.1829 | 0.0475 | 339.6 | 339.6 | 0.0 | - |
| 394 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9062 | 0.0459 | 343.3 | 303.3 | 40.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_3) |
| 65 | adequate | unresolved | deliver_item(item_3) |
| 66 | unresolved | adequate | deliver_item(item_3) |
| 122 | adequate | unresolved | deliver_item(item_2) |
| 123 | unresolved | adequate | deliver_item(item_2) |
| 196 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 197 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 278 | adequate | unresolved | deliver_item(item_1) |
| 279 | unresolved | adequate | deliver_item(item_1) |
| 370 | adequate | unresolved | deliver_item(item_4) |
| 371 | unresolved | adequate | deliver_item(item_4) |
| 394 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 64, 67 to 119, 124 to 195, 198 to 256, 280 to 367 |
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 121, 124 to 195, 280 to 369, 372 to 423 |
| deliver_item(item_1) | 0 to 31, 67 to 93, 124 to 195, 198 to 277 |
| deliver_item(item_2) | 67 to 121 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 93, 124 to 195, 198 to 230, 280 to 369 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 27 | deliver_item(item_3) | none(below_theta) |
| 28 to 64 | deliver_item(item_3) | clears |
| 65 to 66 | ac_activation(ac_switch_0) | none(below_theta) |
| 67 to 96 | deliver_item(item_2) | none(below_theta) |
| 97 to 121 | deliver_item(item_2) | clears |
| 122 to 123 | ac_activation(ac_switch_0) | none(below_theta) |
| 124 to 159 | coffee_break(coffee_machine_0) | none(below_theta) |
| 160 to 195 | coffee_break(coffee_machine_0) | clears |
| 196 to 197 | ac_activation(ac_switch_0) | none(below_theta) |
| 198 to 226 | deliver_item(item_1) | none(below_theta) |
| 227 to 277 | deliver_item(item_1) | clears |
| 278 to 279 | ac_activation(ac_switch_0) | none(below_theta) |
| 280 to 324 | deliver_item(item_4) | none(below_theta) |
| 325 to 369 | deliver_item(item_4) | clears |
| 370 to 371 | ac_activation(ac_switch_0) | none(below_theta) |
| 372 to 381 | coffee_break(coffee_machine_0) | none(below_theta) |
| 382 to 393 | coffee_break(coffee_machine_0) | clears |
| 394 to 423 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_NE)): first step 372, last step 392, acknowledgement 393; the idle human from 394. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.4826 at 372; S < α from 385 (belief 0.1829; v·D 339.6 cm); the finding unexplained from 394.

- coffee_break(coffee_machine_0): belief 0.5134 at 372; S < α from 394 (belief 0.9062; v·D 343.3 cm); the finding unexplained from 394.

