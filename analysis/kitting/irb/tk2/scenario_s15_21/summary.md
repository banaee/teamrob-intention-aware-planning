### scenario_s15_21

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
| 217 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 261 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 263 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 307 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 309 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 351 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 382 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 416; idle from 417 to 446. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 446 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 348 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 349 to 379 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 382 to 446 |
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
| deliver_item(item_4) | move_to(item_4) | 215 to 258 |
| deliver_item(item_4) | pick_up(item_4) | 259 to 260 |
| deliver_item(item_4) | move_to(kitting_table_0) | 261 to 304 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 305 to 306 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 122 | boundary |
| 122 | pin deliver_item(item_2) |
| 215 | boundary |
| 215 | pin deliver_item(item_1) |
| 307 | boundary |
| 307 | pin deliver_item(item_4) |
| 380 | boundary |
| 380 | pin coffee_break(coffee_machine_0) |
| 382 | re-entry coffee_break(coffee_machine_0) |
| 392 | finding turns unexplained |

Never pinned: ac_activation(ac_switch_0). At the last entry (go_to(corner_NE), ticks 382 to 416): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 26 | 0.7569 | yes | adequate |
| deliver_item(item_2) | 67 to 123 | 87 | 0.7557 | yes | adequate |
| deliver_item(item_1) | 124 to 216 | 162 | 0.7710 | yes | adequate |
| deliver_item(item_4) | 217 to 308 | 217 | 0.9617 | yes | adequate |
| coffee_break(coffee_machine_0) | 309 to 381 | 309 | 0.9903 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 12 | deliver_item(item_2) | move_to(item_2) | 0.0237 | 0.0383 | 361.6 | 361.6 | 0.0 | deliver_item(item_3) |
| 16 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0029 | 0.0495 | 335.5 | 335.5 | 0.0 | deliver_item(item_3) |
| 25 | deliver_item(item_4) | move_to(item_4) | 0.0441 | 0.0441 | 347.2 | 347.2 | 0.0 | deliver_item(item_3) |
| 30 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0041 | 0.0450 | 345.3 | 345.3 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_1) | move_to(shelf_3) | 0.0058 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_2) | move_to(shelf_3) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_4) | move_to(shelf_3) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 87 | deliver_item(item_1) | move_to(item_1) | 0.0431 | 0.0418 | 352.6 | 352.6 | 0.0 | deliver_item(item_2) |
| 91 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0029 | 0.0412 | 354.1 | 354.1 | 0.0 | deliver_item(item_2) |
| 101 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0031 | 0.0383 | 361.4 | 301.4 | 60.0 | deliver_item(item_2) |
| 105 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 105 | deliver_item(item_4) | move_to(shelf_2) | 0.0038 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 153 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0017 | 0.0498 | 334.8 | 334.8 | 0.0 | deliver_item(item_1) |
| 176 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0022 | 0.0403 | 356.4 | 296.4 | 60.0 | deliver_item(item_1) |
| 180 | deliver_item(item_4) | move_to(shelf_1) | 0.0041 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 258 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0012 | 0.0431 | 349.5 | 349.5 | 0.0 | deliver_item(item_4) |
| 268 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0011 | 0.0422 | 351.8 | 291.8 | 60.0 | deliver_item(item_4) |
| 345 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0459 | 343.2 | 343.2 | 0.0 | coffee_break(coffee_machine_0) |
| 391 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1195 | 0.0395 | 358.3 | 358.3 | 0.0 | - |
| 392 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.8835 | 0.0451 | 345.0 | 345.0 | 0.0 | - |

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
| 307 | adequate | unresolved | deliver_item(item_4) |
| 308 | unresolved | adequate | deliver_item(item_4) |
| 380 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 381 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 392 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 64, 67 to 119, 124 to 214, 217 to 304, 309 to 379 |
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 121, 124 to 214, 217 to 306, 309 to 379 |
| deliver_item(item_1) | 0 to 31, 67 to 93, 124 to 214 |
| deliver_item(item_2) | 67 to 121 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 93, 124 to 168, 217 to 306 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 25 | deliver_item(item_3) | none(below_theta) |
| 26 to 64 | deliver_item(item_3) | clears |
| 65 to 66 | deliver_item(item_1) | none(below_theta) |
| 67 to 86 | deliver_item(item_2) | none(below_theta) |
| 87 to 121 | deliver_item(item_2) | clears |
| 122 to 161 | deliver_item(item_1) | none(below_theta) |
| 162 to 214 | deliver_item(item_1) | clears |
| 215 to 215 | deliver_item(item_4) | none(leader_no_observation) |
| 216 to 306 | deliver_item(item_4) | clears |
| 307 to 307 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 308 to 308 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 309 to 379 | coffee_break(coffee_machine_0) | clears |
| 380 to 380 | ac_activation(ac_switch_0) | none(leader_no_observation) |
| 381 to 391 | ac_activation(ac_switch_0) | none(leader_unwarranted) |
| 392 to 446 | ac_activation(ac_switch_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of ac_activation | 0 to 446 ordinary |
| level of coffee_break | 0 to 306 ordinary, 307 to 379 raised, 380 to 381 retired, 382 to 446 suppressed |
| recency facts | 0 to 379 none, 380 to 446 coffee_break |

The last entry (go_to(corner_NE)): first step 382, last step 415, acknowledgement 416; the idle human from 417. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.7968 at 382; S < α from 392 (belief 0.8835; v·D 345.0 cm); the finding unexplained from 392.

- coffee_break(coffee_machine_0): belief 0.1992 at 382; S < α from 391 (belief 0.1195; v·D 358.3 cm); the finding unexplained from 392.

