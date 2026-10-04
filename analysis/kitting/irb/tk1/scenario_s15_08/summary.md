### scenario_s15_08

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_3,kitting_table_0) | covered | move_to | 0 | 1 |
| 32 | deliver_item(item_3,kitting_table_0) | covered | pick_up | 0 | 1 |
| 34 | deliver_item(item_3,kitting_table_0) | covered | move_to | 1 | 1 |
| 65 | deliver_item(item_3,kitting_table_0) | covered | place | 0 | 1 |
| 67 | ac_activation(ac_switch_0) | covered | move_to | 0 | 1 |
| 113 | ac_activation(ac_switch_0) | covered | wait_at | 0 | 1 |
| 115 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 153 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 155 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 182 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 184 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 229 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 231 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 275 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 277 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 321 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 323 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 367 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 369 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 390; idle from 391 to 420. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 110 |
| ac_activation(ac_switch_0) | wait_at(PT2S,ac_switch_0) | 111 to 112 |
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | 115 to 420 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 420 |
| deliver_item(item_1) | move_to(item_1) | -1 to 31 |
| deliver_item(item_1) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_1) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_1) | move_to(item_1) | 65 to 152 |
| deliver_item(item_1) | place(item_2,shelf_2) | 153 to 155 |
| deliver_item(item_1) | move_to(shelf_2) | 156 to 181 |
| deliver_item(item_1) | move_to(item_1) | 182 to 226 |
| deliver_item(item_1) | pick_up(item_1) | 227 to 228 |
| deliver_item(item_1) | move_to(kitting_table_0) | 229 to 272 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 273 to 274 |
| deliver_item(item_2) | move_to(item_2) | -1 to 31 |
| deliver_item(item_2) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_2) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_2) | move_to(item_2) | 65 to 150 |
| deliver_item(item_2) | pick_up(item_2) | 151 to 152 |
| deliver_item(item_2) | move_to(kitting_table_0) | 153 to 179 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 180 to 181 |
| deliver_item(item_3) | move_to(item_3) | -1 to 29 |
| deliver_item(item_3) | pick_up(item_3) | 30 to 31 |
| deliver_item(item_3) | move_to(kitting_table_0) | 32 to 62 |
| deliver_item(item_3) | place(item_3,kitting_table_0) | 63 to 64 |
| deliver_item(item_4) | move_to(item_4) | -1 to 31 |
| deliver_item(item_4) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_4) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_4) | move_to(item_4) | 65 to 152 |
| deliver_item(item_4) | place(item_2,shelf_2) | 153 to 155 |
| deliver_item(item_4) | move_to(shelf_2) | 156 to 181 |
| deliver_item(item_4) | move_to(item_4) | 182 to 228 |
| deliver_item(item_4) | place(item_1,shelf_1) | 229 to 230 |
| deliver_item(item_4) | move_to(shelf_1) | 231 to 274 |
| deliver_item(item_4) | move_to(item_4) | 275 to 318 |
| deliver_item(item_4) | pick_up(item_4) | 319 to 320 |
| deliver_item(item_4) | move_to(kitting_table_0) | 321 to 364 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 365 to 366 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 113 | boundary |
| 113 | pin ac_activation(ac_switch_0) |
| 115 | re-entry ac_activation(ac_switch_0) |
| 182 | boundary |
| 182 | pin deliver_item(item_2) |
| 275 | boundary |
| 275 | pin deliver_item(item_1) |
| 367 | boundary |
| 367 | pin deliver_item(item_4) |
| 391 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_NE), ticks 369 to 390): lifecycle and finding adequate; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 28 | 0.7518 | yes | adequate |
| ac_activation(ac_switch_0) | 67 to 114 | not reached | - | - | - |
| deliver_item(item_2) | 115 to 183 | 135 | 0.7791 | yes | adequate |
| deliver_item(item_1) | 184 to 276 | 231 | 0.7644 | yes | adequate |
| deliver_item(item_4) | 277 to 368 | 322 | 0.7531 | yes | adequate |

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
| 87 | deliver_item(item_2) | move_to(item_2) | 0.0170 | 0.0424 | 351.3 | 351.3 | 0.0 | ac_activation(ac_switch_0) |
| 102 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0258 | 0.0496 | 335.3 | 335.3 | 0.0 | ac_activation(ac_switch_0) |
| 124 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0241 | 0.0393 | 358.9 | 358.9 | 0.0 | deliver_item(item_2) |
| 124 | deliver_item(item_1) | move_to(item_1) | 0.0266 | 0.0411 | 354.3 | 354.3 | 0.0 | deliver_item(item_2) |
| 128 | deliver_item(item_4) | move_to(item_4) | 0.0372 | 0.0464 | 342.1 | 342.1 | 0.0 | deliver_item(item_2) |
| 142 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0548 | 0.0426 | 350.7 | 350.7 | 0.0 | deliver_item(item_2) |
| 165 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0402 | 356.7 | 356.7 | 0.0 | deliver_item(item_2) |
| 165 | deliver_item(item_4) | move_to(shelf_2) | 0.0010 | 0.0402 | 356.7 | 356.7 | 0.0 | deliver_item(item_2) |
| 213 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0267 | 0.0496 | 335.3 | 335.3 | 0.0 | deliver_item(item_1) |
| 236 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0511 | 0.0402 | 356.6 | 296.6 | 60.0 | deliver_item(item_1) |
| 240 | deliver_item(item_4) | move_to(shelf_1) | 0.0041 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 318 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0364 | 0.0429 | 350.1 | 350.1 | 0.0 | deliver_item(item_4) |
| 328 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0538 | 0.0421 | 352.0 | 292.0 | 60.0 | deliver_item(item_4) |
| 382 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.1834 | 0.0480 | 338.5 | 338.5 | 0.0 | - |
| 391 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9060 | 0.0465 | 341.9 | 301.9 | 40.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_3) |
| 65 | adequate | unresolved | deliver_item(item_3) |
| 66 | unresolved | adequate | deliver_item(item_3) |
| 113 | adequate | unresolved | ac_activation(ac_switch_0) |
| 114 | unresolved | adequate | ac_activation(ac_switch_0) |
| 182 | adequate | unresolved | deliver_item(item_2) |
| 183 | unresolved | adequate | deliver_item(item_2) |
| 275 | adequate | unresolved | deliver_item(item_1) |
| 276 | unresolved | adequate | deliver_item(item_1) |
| 367 | adequate | unresolved | deliver_item(item_4) |
| 368 | unresolved | adequate | deliver_item(item_4) |
| 391 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 64, 67 to 112, 184 to 274, 277 to 364 |
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 112, 115 to 160, 184 to 274, 277 to 366, 369 to 420 |
| deliver_item(item_1) | 0 to 31, 67 to 112, 184 to 274 |
| deliver_item(item_2) | 67 to 95, 115 to 181 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 112, 115 to 123, 184 to 228, 277 to 366 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 27 | deliver_item(item_3) | none(below_theta) |
| 28 to 64 | deliver_item(item_3) | clears |
| 65 to 112 | ac_activation(ac_switch_0) | none(below_theta) |
| 113 to 114 | coffee_break(coffee_machine_0) | none(below_theta) |
| 115 to 134 | deliver_item(item_2) | none(below_theta) |
| 135 to 181 | deliver_item(item_2) | clears |
| 182 to 183 | ac_activation(ac_switch_0) | none(below_theta) |
| 184 to 230 | deliver_item(item_1) | none(below_theta) |
| 231 to 274 | deliver_item(item_1) | clears |
| 275 to 276 | ac_activation(ac_switch_0) | none(below_theta) |
| 277 to 321 | deliver_item(item_4) | none(below_theta) |
| 322 to 366 | deliver_item(item_4) | clears |
| 367 to 368 | ac_activation(ac_switch_0) | none(below_theta) |
| 369 to 378 | coffee_break(coffee_machine_0) | none(below_theta) |
| 379 to 390 | coffee_break(coffee_machine_0) | clears |
| 391 to 420 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_NE)): first step 369, last step 389, acknowledgement 390; the idle human from 391. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.4826 at 369; S < α from 382 (belief 0.1834; v·D 338.5 cm); the finding unexplained from 391.

- coffee_break(coffee_machine_0): belief 0.5134 at 369; S < α from 391 (belief 0.9060; v·D 341.9 cm); the finding unexplained from 391.

