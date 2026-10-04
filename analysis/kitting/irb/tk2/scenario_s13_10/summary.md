### scenario_s13_10

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_3,kitting_table_0) | covered | move_to | 0 | 1 |
| 32 | deliver_item(item_3,kitting_table_0) | covered | pick_up | 0 | 1 |
| 34 | deliver_item(item_3,kitting_table_0) | covered | move_to | 1 | 1 |
| 65 | deliver_item(item_3,kitting_table_0) | covered | place | 0 | 1 |
| 67 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 110 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 141 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 161 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 163 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 191 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 193 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 238 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 240 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 284 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 286 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 330 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 332 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 376 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 378 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 399; idle from 400 to 429. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 107 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 108 to 138 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 141 to 429 |
| deliver_item(item_1) | move_to(item_1) | -1 to 31 |
| deliver_item(item_1) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_1) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_1) | move_to(item_1) | 65 to 160 |
| deliver_item(item_1) | place(item_2,shelf_2) | 161 to 163 |
| deliver_item(item_1) | move_to(shelf_2) | 164 to 190 |
| deliver_item(item_1) | move_to(item_1) | 191 to 235 |
| deliver_item(item_1) | pick_up(item_1) | 236 to 237 |
| deliver_item(item_1) | move_to(kitting_table_0) | 238 to 281 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 282 to 283 |
| deliver_item(item_2) | move_to(item_2) | -1 to 31 |
| deliver_item(item_2) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_2) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_2) | move_to(item_2) | 65 to 158 |
| deliver_item(item_2) | pick_up(item_2) | 159 to 160 |
| deliver_item(item_2) | move_to(kitting_table_0) | 161 to 188 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 189 to 190 |
| deliver_item(item_3) | move_to(item_3) | -1 to 29 |
| deliver_item(item_3) | pick_up(item_3) | 30 to 31 |
| deliver_item(item_3) | move_to(kitting_table_0) | 32 to 62 |
| deliver_item(item_3) | place(item_3,kitting_table_0) | 63 to 64 |
| deliver_item(item_4) | move_to(item_4) | -1 to 31 |
| deliver_item(item_4) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_4) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_4) | move_to(item_4) | 65 to 160 |
| deliver_item(item_4) | place(item_2,shelf_2) | 161 to 163 |
| deliver_item(item_4) | move_to(shelf_2) | 164 to 190 |
| deliver_item(item_4) | move_to(item_4) | 191 to 237 |
| deliver_item(item_4) | place(item_1,shelf_1) | 238 to 239 |
| deliver_item(item_4) | move_to(shelf_1) | 240 to 283 |
| deliver_item(item_4) | move_to(item_4) | 284 to 327 |
| deliver_item(item_4) | pick_up(item_4) | 328 to 329 |
| deliver_item(item_4) | move_to(kitting_table_0) | 330 to 373 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 374 to 375 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 139 | boundary |
| 139 | pin coffee_break(coffee_machine_0) |
| 141 | re-entry coffee_break(coffee_machine_0) |
| 191 | boundary |
| 191 | pin deliver_item(item_2) |
| 284 | boundary |
| 284 | pin deliver_item(item_1) |
| 376 | boundary |
| 376 | pin deliver_item(item_4) |
| 400 | finding turns unexplained |

Never pinned: none. At the last entry (go_to(corner_NE), ticks 378 to 399): lifecycle and finding adequate; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 26 | 0.7624 | yes | adequate |
| coffee_break(coffee_machine_0) | 67 to 140 | 117 | 0.7844 | yes | adequate |
| deliver_item(item_2) | 141 to 192 | 149 | 0.7966 | yes | adequate |
| deliver_item(item_1) | 193 to 285 | 230 | 0.7644 | yes | adequate |
| deliver_item(item_4) | 286 to 377 | 286 | 0.9806 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 12 | deliver_item(item_2) | move_to(item_2) | 0.0241 | 0.0383 | 361.6 | 361.6 | 0.0 | deliver_item(item_3) |
| 16 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0029 | 0.0495 | 335.5 | 335.5 | 0.0 | deliver_item(item_3) |
| 25 | deliver_item(item_4) | move_to(item_4) | 0.0445 | 0.0441 | 347.2 | 347.2 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_1) | move_to(shelf_3) | 0.0058 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_2) | move_to(shelf_3) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_4) | move_to(shelf_3) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 97 | deliver_item(item_1) | move_to(item_1) | 0.1061 | 0.0464 | 342.0 | 342.0 | 0.0 | coffee_break(coffee_machine_0) |
| 98 | deliver_item(item_2) | move_to(item_2) | 0.1003 | 0.0392 | 359.2 | 359.2 | 0.0 | coffee_break(coffee_machine_0) |
| 110 | deliver_item(item_4) | move_to(item_4) | 0.4829 | 0.0444 | 346.5 | 306.5 | 40.0 | coffee_break(coffee_machine_0) |
| 150 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0395 | 358.5 | 358.5 | 0.0 | deliver_item(item_2) |
| 151 | deliver_item(item_4) | move_to(item_4) | 0.0443 | 0.0369 | 365.2 | 365.2 | 0.0 | deliver_item(item_2) |
| 152 | deliver_item(item_1) | move_to(item_1) | 0.0591 | 0.0478 | 339.1 | 339.1 | 0.0 | deliver_item(item_2) |
| 173 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0416 | 353.2 | 353.2 | 0.0 | deliver_item(item_2) |
| 173 | deliver_item(item_4) | move_to(shelf_2) | 0.0010 | 0.0416 | 353.2 | 353.2 | 0.0 | deliver_item(item_2) |
| 223 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0417 | 352.9 | 352.9 | 0.0 | deliver_item(item_1) |
| 249 | deliver_item(item_4) | move_to(shelf_1) | 0.0042 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 327 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0012 | 0.0434 | 348.8 | 348.8 | 0.0 | deliver_item(item_4) |
| 400 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9960 | 0.0470 | 340.7 | 300.7 | 40.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_3) |
| 65 | adequate | unresolved | deliver_item(item_3) |
| 66 | unresolved | adequate | deliver_item(item_3) |
| 139 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 140 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 191 | adequate | unresolved | deliver_item(item_2) |
| 192 | unresolved | adequate | deliver_item(item_2) |
| 284 | adequate | unresolved | deliver_item(item_1) |
| 285 | unresolved | adequate | deliver_item(item_1) |
| 376 | adequate | unresolved | deliver_item(item_4) |
| 377 | unresolved | adequate | deliver_item(item_4) |
| 400 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 138, 193 to 283, 286 to 375, 378 to 429 |
| deliver_item(item_1) | 0 to 31, 67 to 138, 193 to 283 |
| deliver_item(item_2) | 67 to 138, 141 to 190 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 138, 193 to 237, 286 to 375 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 25 | deliver_item(item_3) | none(below_theta) |
| 26 to 64 | deliver_item(item_3) | clears |
| 65 to 66 | deliver_item(item_1) | none(below_theta) |
| 67 to 68 | deliver_item(item_2) | none(below_theta) |
| 69 to 110 | deliver_item(item_4) | none(below_theta) |
| 111 to 116 | coffee_break(coffee_machine_0) | none(below_theta) |
| 117 to 138 | coffee_break(coffee_machine_0) | clears |
| 139 to 140 | deliver_item(item_1) | none(below_theta) |
| 141 to 148 | deliver_item(item_2) | none(below_theta) |
| 149 to 190 | deliver_item(item_2) | clears |
| 191 to 229 | deliver_item(item_1) | none(below_theta) |
| 230 to 283 | deliver_item(item_1) | clears |
| 284 to 284 | deliver_item(item_4) | none(leader_no_observation) |
| 285 to 375 | deliver_item(item_4) | clears |
| 376 to 376 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 377 to 377 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 378 to 399 | coffee_break(coffee_machine_0) | clears |
| 400 to 429 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of coffee_break | 0 to 119 ordinary, 120 to 138 raised, 139 to 140 retired, 141 to 228 suppressed, 229 to 429 ordinary |
| recency facts | 0 to 138 none, 139 to 228 coffee_break, 229 to 429 none |

The last entry (go_to(corner_NE)): first step 378, last step 398, acknowledgement 399; the idle human from 400. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9960 at 378; S < α from 400 (belief 0.9960; v·D 340.7 cm); the finding unexplained from 400.

