### scenario_s15_10

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
| 217 | ac_activation(ac_switch_0) | covered | move_to | 0 | 1 |
| 262 | ac_activation(ac_switch_0) | covered | switch_on | 0 | 1 |
| 264 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 272 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 274 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 320 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 322 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 343; idle from 344 to 373. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 259 |
| ac_activation(ac_switch_0) | switch_on(PT2S,ac_switch_0) | 260 to 261 |
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | 264 to 373 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 373 |
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
| deliver_item(item_4) | move_to(item_4) | 215 to 269 |
| deliver_item(item_4) | pick_up(item_4) | 270 to 271 |
| deliver_item(item_4) | move_to(kitting_table_0) | 272 to 317 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 318 to 319 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 122 | boundary |
| 122 | pin deliver_item(item_2) |
| 215 | boundary |
| 215 | pin deliver_item(item_1) |
| 262 | boundary |
| 262 | pin ac_activation(ac_switch_0) |
| 264 | re-entry ac_activation(ac_switch_0) |
| 320 | boundary |
| 320 | pin deliver_item(item_4) |
| 345 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_NE), ticks 322 to 343): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 28 | 0.7518 | yes | adequate |
| deliver_item(item_2) | 67 to 123 | 97 | 0.7820 | yes | adequate |
| deliver_item(item_1) | 124 to 216 | 171 | 0.7635 | yes | adequate |
| ac_activation(ac_switch_0) | 217 to 263 | not reached | - | - | - |
| deliver_item(item_4) | 264 to 321 | 279 | 0.7521 | yes | adequate |

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
| 252 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0324 | 0.0434 | 348.8 | 348.8 | 0.0 | ac_activation(ac_switch_0) |
| 275 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0405 | 0.0480 | 338.7 | 278.7 | 60.0 | deliver_item(item_4) |
| 286 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0630 | 0.0495 | 335.4 | 275.4 | 60.0 | deliver_item(item_4) |
| 336 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.1698 | 0.0407 | 355.3 | 355.3 | 0.0 | - |
| 345 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9045 | 0.0430 | 349.7 | 289.7 | 60.0 | - |

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
| 262 | adequate | unresolved | ac_activation(ac_switch_0) |
| 263 | unresolved | adequate | ac_activation(ac_switch_0) |
| 320 | adequate | unresolved | deliver_item(item_4) |
| 321 | unresolved | adequate | deliver_item(item_4) |
| 345 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 64, 67 to 119, 124 to 214, 217 to 261 |
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 121, 124 to 214, 217 to 261, 264 to 297, 322 to 373 |
| deliver_item(item_1) | 0 to 31, 67 to 93, 124 to 214 |
| deliver_item(item_2) | 67 to 121 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 93, 124 to 168, 217 to 261, 264 to 319 |

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
| 215 to 261 | ac_activation(ac_switch_0) | none(below_theta) |
| 262 to 263 | coffee_break(coffee_machine_0) | none(below_theta) |
| 264 to 278 | deliver_item(item_4) | none(below_theta) |
| 279 to 319 | deliver_item(item_4) | clears |
| 320 to 321 | ac_activation(ac_switch_0) | none(below_theta) |
| 322 to 332 | coffee_break(coffee_machine_0) | none(below_theta) |
| 333 to 344 | coffee_break(coffee_machine_0) | clears |
| 345 to 373 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_NE)): first step 322, last step 342, acknowledgement 343; the idle human from 344. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.4830 at 322; S < α from 336 (belief 0.1698; v·D 355.3 cm); the finding unexplained from 345.

- coffee_break(coffee_machine_0): belief 0.5130 at 322; S < α from 345 (belief 0.9045; v·D 349.7 cm); the finding unexplained from 345.

