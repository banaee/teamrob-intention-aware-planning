### scenario_s13_06

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_3,kitting_table_0) | covered | move_to | 0 | 1 |
| 32 | deliver_item(item_3,kitting_table_0) | covered | pick_up | 0 | 1 |
| 34 | deliver_item(item_3,kitting_table_0) | covered | move_to | 1 | 1 |
| 65 | deliver_item(item_3,kitting_table_0) | covered | place | 0 | 1 |
| 67 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 94 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 96 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 118 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 149 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 192 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 194 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 239 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 241 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 285 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 287 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 331 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 333 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 377 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 379 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 400; idle from 401 to 430. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 115 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 116 to 146 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 149 to 430 |
| deliver_item(item_1) | move_to(item_1) | -1 to 31 |
| deliver_item(item_1) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_1) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_1) | move_to(item_1) | 65 to 93 |
| deliver_item(item_1) | place(item_2,shelf_2) | 94 to 96 |
| deliver_item(item_1) | move_to(shelf_2) | 97 to 191 |
| deliver_item(item_1) | move_to(item_1) | 192 to 236 |
| deliver_item(item_1) | pick_up(item_1) | 237 to 238 |
| deliver_item(item_1) | move_to(kitting_table_0) | 239 to 282 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 283 to 284 |
| deliver_item(item_2) | move_to(item_2) | -1 to 31 |
| deliver_item(item_2) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_2) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_2) | move_to(item_2) | 65 to 91 |
| deliver_item(item_2) | pick_up(item_2) | 92 to 93 |
| deliver_item(item_2) | move_to(kitting_table_0) | 94 to 189 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 190 to 191 |
| deliver_item(item_3) | move_to(item_3) | -1 to 29 |
| deliver_item(item_3) | pick_up(item_3) | 30 to 31 |
| deliver_item(item_3) | move_to(kitting_table_0) | 32 to 62 |
| deliver_item(item_3) | place(item_3,kitting_table_0) | 63 to 64 |
| deliver_item(item_4) | move_to(item_4) | -1 to 31 |
| deliver_item(item_4) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_4) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_4) | move_to(item_4) | 65 to 93 |
| deliver_item(item_4) | place(item_2,shelf_2) | 94 to 96 |
| deliver_item(item_4) | move_to(shelf_2) | 97 to 191 |
| deliver_item(item_4) | move_to(item_4) | 192 to 238 |
| deliver_item(item_4) | place(item_1,shelf_1) | 239 to 240 |
| deliver_item(item_4) | move_to(shelf_1) | 241 to 284 |
| deliver_item(item_4) | move_to(item_4) | 285 to 328 |
| deliver_item(item_4) | pick_up(item_4) | 329 to 330 |
| deliver_item(item_4) | move_to(kitting_table_0) | 331 to 374 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 375 to 376 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 147 | boundary |
| 147 | pin coffee_break(coffee_machine_0) |
| 149 | re-entry coffee_break(coffee_machine_0) |
| 192 | boundary |
| 192 | pin deliver_item(item_2) |
| 285 | boundary |
| 285 | pin deliver_item(item_1) |
| 377 | boundary |
| 377 | pin deliver_item(item_4) |
| 401 | finding turns unexplained |

Never pinned: none. At the last entry (go_to(corner_NE), ticks 379 to 400): lifecycle and finding adequate; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 26 | 0.7624 | yes | adequate |
| deliver_item(item_2) | 67 to 95 | 87 | 0.7597 | yes | adequate |
| coffee_break(coffee_machine_0) | 96 to 148 | 112 | 0.8015 | yes | adequate |
| deliver_item(item_2) | 149 to 193 | 170 | 0.7723 | yes | adequate |
| deliver_item(item_1) | 194 to 286 | 231 | 0.7651 | yes | adequate |
| deliver_item(item_4) | 287 to 378 | 300 | 0.9839 | yes | adequate |

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
| 105 | deliver_item(item_2) | move_to(kitting_table_0) | 0.6847 | 0.0441 | 347.1 | 347.1 | 0.0 | coffee_break(coffee_machine_0) |
| 106 | deliver_item(item_1) | move_to(shelf_2) | 0.0101 | 0.0404 | 356.1 | 356.1 | 0.0 | coffee_break(coffee_machine_0) |
| 106 | deliver_item(item_4) | move_to(shelf_2) | 0.0578 | 0.0404 | 356.1 | 356.1 | 0.0 | coffee_break(coffee_machine_0) |
| 158 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0392 | 359.2 | 359.2 | 0.0 | deliver_item(item_2) |
| 173 | deliver_item(item_1) | move_to(shelf_2) | 0.0557 | 0.0461 | 342.8 | 342.8 | 0.0 | deliver_item(item_2) |
| 173 | deliver_item(item_4) | move_to(shelf_2) | 0.0557 | 0.0461 | 342.8 | 342.8 | 0.0 | deliver_item(item_2) |
| 224 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0419 | 352.5 | 352.5 | 0.0 | deliver_item(item_1) |
| 250 | deliver_item(item_4) | move_to(shelf_1) | 0.0042 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 328 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0012 | 0.0428 | 350.4 | 350.4 | 0.0 | deliver_item(item_4) |
| 401 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9960 | 0.0464 | 342.1 | 302.1 | 40.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_3) |
| 65 | adequate | unresolved | deliver_item(item_3) |
| 66 | unresolved | adequate | deliver_item(item_3) |
| 147 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 148 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 192 | adequate | unresolved | deliver_item(item_2) |
| 193 | unresolved | adequate | deliver_item(item_2) |
| 285 | adequate | unresolved | deliver_item(item_1) |
| 286 | unresolved | adequate | deliver_item(item_1) |
| 377 | adequate | unresolved | deliver_item(item_4) |
| 378 | unresolved | adequate | deliver_item(item_4) |
| 401 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 96 to 148, its hypothesis pinned at 147; the suspended task resumes at 149.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | deliver_item(item_3) belief / S | deliver_item(item_4) belief / S | finding |
|---|---|---|---|---|---|---|---|---|
| 94 | pick_up grasp | deliver_item(item_2) | 0.0221 / 0.3303 | 0.0112 / 1.0000 | 0.9016 / 1.0000 | retired | 0.0641 / 1.0000 | adequate |
| 95 | pick_up  | deliver_item(item_2) | 0.0189 / 0.2757 | 0.0113 / 1.0000 | 0.9046 / 1.0000 | retired | 0.0643 / 1.0000 | adequate |
| 96 | move_to step | coffee_break(coffee_machine_0) | 0.0222 / 0.2757 | 0.0132 / 1.0000 | 0.8881 / 0.7806 | retired | 0.0755 / 1.0000 | adequate |
| 97 | move_to step | coffee_break(coffee_machine_0) | 0.0266 / 0.2757 | 0.0159 / - | 0.8657 / 0.5975 | retired | 0.0907 / - | adequate |
| 98 | move_to step | coffee_break(coffee_machine_0) | 0.0334 / 0.2757 | 0.0162 / 0.7505 | 0.8571 / 0.4493 | retired | 0.0923 / 0.7505 | adequate |
| 146 | wait_at stand | coffee_break(coffee_machine_0) | 0.9960 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | adequate |
| 147 | wait_at stand | coffee_break(coffee_machine_0) | retired | 0.3327 / - | 0.3327 / - | retired | 0.3327 / - | unresolved |
| 148 | wait_at  | coffee_break(coffee_machine_0) | retired | 0.3327 / 1.0000 | 0.3327 / 1.0000 | retired | 0.3327 / 1.0000 | adequate |
| 149 | move_to step | deliver_item(item_2) | 0.0050 / - | 0.3298 / 0.9801 | 0.3344 / 1.0000 | retired | 0.3298 / 0.9801 | adequate |
| 150 | move_to step | deliver_item(item_2) | 0.0040 / 0.7421 | 0.3284 / 0.9585 | 0.3382 / 1.0000 | retired | 0.3284 / 0.9585 | adequate |
| 151 | move_to step | deliver_item(item_2) | 0.0032 / 0.5377 | 0.3267 / 0.9350 | 0.3425 / 1.0000 | retired | 0.3267 / 0.9350 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 146, 194 to 284, 287 to 376, 379 to 430 |
| deliver_item(item_1) | 0 to 31, 67 to 93, 149 to 183, 194 to 284 |
| deliver_item(item_2) | 67 to 146, 149 to 191 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 93, 149 to 183, 194 to 238, 287 to 376 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 25 | deliver_item(item_3) | none(below_theta) |
| 26 to 64 | deliver_item(item_3) | clears |
| 65 to 66 | deliver_item(item_1) | none(below_theta) |
| 67 to 86 | deliver_item(item_2) | none(below_theta) |
| 87 to 103 | deliver_item(item_2) | clears |
| 104 to 107 | deliver_item(item_2) | none(below_theta) |
| 108 to 111 | coffee_break(coffee_machine_0) | none(below_theta) |
| 112 to 146 | coffee_break(coffee_machine_0) | clears |
| 147 to 148 | deliver_item(item_1) | none(below_theta) |
| 149 to 169 | deliver_item(item_2) | none(below_theta) |
| 170 to 191 | deliver_item(item_2) | clears |
| 192 to 230 | deliver_item(item_1) | none(below_theta) |
| 231 to 284 | deliver_item(item_1) | clears |
| 285 to 299 | coffee_break(coffee_machine_0) | none(below_theta) |
| 300 to 376 | deliver_item(item_4) | clears |
| 377 to 377 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 378 to 378 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 379 to 400 | coffee_break(coffee_machine_0) | clears |
| 401 to 430 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of coffee_break | 0 to 146 ordinary, 147 to 148 retired, 149 to 236 suppressed, 237 to 299 raised, 300 to 430 ordinary |
| recency facts | 0 to 146 none, 147 to 236 coffee_break, 237 to 430 none |

The last entry (go_to(corner_NE)): first step 379, last step 399, acknowledgement 400; the idle human from 401. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9960 at 379; S < α from 401 (belief 0.9960; v·D 342.1 cm); the finding unexplained from 401.

