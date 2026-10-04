### scenario_s13_15

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
| 261 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 279 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 310 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 327 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 329 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 374 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 376 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 397; idle from 398 to 427. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 276 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 277 to 307 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 310 to 427 |
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
| deliver_item(item_4) | move_to(item_4) | 261 to 324 |
| deliver_item(item_4) | pick_up(item_4) | 325 to 326 |
| deliver_item(item_4) | move_to(kitting_table_0) | 327 to 371 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 372 to 373 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 122 | boundary |
| 122 | pin deliver_item(item_2) |
| 215 | boundary |
| 215 | pin deliver_item(item_1) |
| 261 | finding turns unexplained |
| 262 | finding turns adequate (from unexplained) |
| 270 | finding turns unexplained |
| 277 | finding turns adequate (from unexplained) |
| 308 | boundary |
| 308 | pin coffee_break(coffee_machine_0) |
| 310 | re-entry coffee_break(coffee_machine_0) |
| 374 | boundary |
| 374 | pin deliver_item(item_4) |
| 398 | finding turns unexplained |

Never pinned: none. At the last entry (go_to(corner_NE), ticks 376 to 397): lifecycle and finding adequate; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 26 | 0.7624 | yes | adequate |
| deliver_item(item_2) | 67 to 123 | 87 | 0.7597 | yes | adequate |
| deliver_item(item_1) | 124 to 216 | 161 | 0.7660 | yes | adequate |
| deliver_item(item_4) | 217 to 260 | 217 | 0.9806 | yes | adequate |
| coffee_break(coffee_machine_0) | 261 to 309 | 291 | 0.7739 | yes | adequate |
| deliver_item(item_4) | 310 to 375 | 310 | 0.9950 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 12 | deliver_item(item_2) | move_to(item_2) | 0.0241 | 0.0383 | 361.6 | 361.6 | 0.0 | deliver_item(item_3) |
| 16 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0029 | 0.0495 | 335.5 | 335.5 | 0.0 | deliver_item(item_3) |
| 25 | deliver_item(item_4) | move_to(item_4) | 0.0445 | 0.0441 | 347.2 | 347.2 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_1) | move_to(shelf_3) | 0.0058 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_2) | move_to(shelf_3) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_4) | move_to(shelf_3) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 87 | deliver_item(item_1) | move_to(item_1) | 0.0434 | 0.0418 | 352.6 | 352.6 | 0.0 | deliver_item(item_2) |
| 101 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0031 | 0.0383 | 361.4 | 301.4 | 60.0 | deliver_item(item_2) |
| 105 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 105 | deliver_item(item_4) | move_to(shelf_2) | 0.0038 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 153 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0017 | 0.0498 | 334.8 | 334.8 | 0.0 | deliver_item(item_1) |
| 180 | deliver_item(item_4) | move_to(shelf_1) | 0.0041 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 258 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0012 | 0.0431 | 349.5 | 349.5 | 0.0 | deliver_item(item_4) |
| 270 | deliver_item(item_4) | move_to(item_4) | 0.9841 | 0.0426 | 350.7 | 350.7 | 0.0 | coffee_break(coffee_machine_0) |
| 319 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_4) |
| 398 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9960 | 0.0471 | 340.6 | 300.6 | 40.0 | - |

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
| 261 | adequate | unexplained | coffee_break(coffee_machine_0) |
| 262 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 270 | adequate | unexplained | coffee_break(coffee_machine_0) |
| 277 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 308 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 309 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 374 | adequate | unresolved | deliver_item(item_4) |
| 375 | unresolved | adequate | deliver_item(item_4) |
| 398 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 261 to 309, its hypothesis pinned at 308; the suspended task resumes at 310.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | deliver_item(item_3) belief / S | deliver_item(item_4) belief / S | finding |
|---|---|---|---|---|---|---|---|---|
| 259 | move_to step | deliver_item(item_4) | 0.0010 / 0.0339 | retired | retired | retired | 0.9960 / 1.0000 | adequate |
| 260 | move_to  | deliver_item(item_4) | 0.0010 / 0.0278 | retired | retired | retired | 0.9960 / 1.0000 | adequate |
| 261 | move_to step | coffee_break(coffee_machine_0) | 0.0010 / 0.0278 | retired | retired | retired | 0.9960 / - | unexplained |
| 262 | move_to step | coffee_break(coffee_machine_0) | 0.0010 / 0.0278 | retired | retired | retired | 0.9960 / 0.7633 | adequate |
| 263 | move_to step | coffee_break(coffee_machine_0) | 0.0012 / 0.0278 | retired | retired | retired | 0.9958 / 0.5623 | adequate |
| 307 | wait_at stand | coffee_break(coffee_machine_0) | 0.9853 / 1.0000 | retired | retired | retired | 0.0117 / 0.0000 | adequate |
| 308 | wait_at stand | coffee_break(coffee_machine_0) | retired | retired | retired | retired | 0.9960 / - | unresolved |
| 309 | wait_at  | coffee_break(coffee_machine_0) | retired | retired | retired | retired | 0.9960 / 1.0000 | adequate |
| 310 | move_to step | deliver_item(item_4) | 0.0050 / - | retired | retired | retired | 0.9920 / 1.0000 | adequate |
| 311 | move_to step | deliver_item(item_4) | 0.0040 / 0.7402 | retired | retired | retired | 0.9930 / 1.0000 | adequate |
| 312 | move_to step | deliver_item(item_4) | 0.0031 / 0.5355 | retired | retired | retired | 0.9939 / 1.0000 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 121, 124 to 214, 217 to 307, 376 to 427 |
| deliver_item(item_1) | 0 to 31, 67 to 93, 124 to 214 |
| deliver_item(item_2) | 67 to 121 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 93, 124 to 168, 217 to 260, 310 to 373 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 25 | deliver_item(item_3) | none(below_theta) |
| 26 to 64 | deliver_item(item_3) | clears |
| 65 to 66 | deliver_item(item_1) | none(below_theta) |
| 67 to 86 | deliver_item(item_2) | none(below_theta) |
| 87 to 121 | deliver_item(item_2) | clears |
| 122 to 160 | deliver_item(item_1) | none(below_theta) |
| 161 to 214 | deliver_item(item_1) | clears |
| 215 to 215 | deliver_item(item_4) | none(leader_no_observation) |
| 216 to 216 | deliver_item(item_4) | none(leader_unwarranted) |
| 217 to 260 | deliver_item(item_4) | clears |
| 261 to 261 | deliver_item(item_4) | none(leader_no_observation) |
| 262 to 269 | deliver_item(item_4) | none(leader_unwarranted) |
| 270 to 279 | deliver_item(item_4) | none(leader_inadequate) |
| 280 to 284 | deliver_item(item_4) | none(below_theta) |
| 285 to 290 | coffee_break(coffee_machine_0) | none(below_theta) |
| 291 to 307 | coffee_break(coffee_machine_0) | clears |
| 308 to 308 | deliver_item(item_4) | none(leader_no_observation) |
| 309 to 309 | deliver_item(item_4) | none(leader_unwarranted) |
| 310 to 373 | deliver_item(item_4) | clears |
| 374 to 374 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 375 to 375 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 376 to 397 | coffee_break(coffee_machine_0) | clears |
| 398 to 427 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of coffee_break | 0 to 307 ordinary, 308 to 309 retired, 310 to 397 suppressed, 398 to 427 ordinary |
| recency facts | 0 to 307 none, 308 to 397 coffee_break, 398 to 427 none |

The last entry (go_to(corner_NE)): first step 376, last step 396, acknowledgement 397; the idle human from 398. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9960 at 376; S < α from 398 (belief 0.9960; v·D 340.6 cm); the finding unexplained from 398.

