### scenario_s13_05

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_3,kitting_table_0) | covered | move_to | 0 | 1 |
| 32 | deliver_item(item_3,kitting_table_0) | covered | pick_up | 0 | 1 |
| 34 | deliver_item(item_3,kitting_table_0) | covered | move_to | 1 | 1 |
| 65 | deliver_item(item_3,kitting_table_0) | covered | place | 0 | 1 |
| 67 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 94 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 116 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 147 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 167 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 169 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 197 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 199 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 244 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 246 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 290 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 292 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 336 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 338 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 382 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 384 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 405; idle from 406 to 435. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 113 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 114 to 144 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 147 to 435 |
| deliver_item(item_1) | move_to(item_1) | -1 to 31 |
| deliver_item(item_1) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_1) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_1) | move_to(item_1) | 65 to 166 |
| deliver_item(item_1) | place(item_2,shelf_2) | 167 to 169 |
| deliver_item(item_1) | move_to(shelf_2) | 170 to 196 |
| deliver_item(item_1) | move_to(item_1) | 197 to 241 |
| deliver_item(item_1) | pick_up(item_1) | 242 to 243 |
| deliver_item(item_1) | move_to(kitting_table_0) | 244 to 287 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 288 to 289 |
| deliver_item(item_2) | move_to(item_2) | -1 to 31 |
| deliver_item(item_2) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_2) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_2) | move_to(item_2) | 65 to 91 |
| deliver_item(item_2) | pick_up(item_2) | 92 to 94 |
| deliver_item(item_2) | move_to(item_2) | 95 to 164 |
| deliver_item(item_2) | pick_up(item_2) | 165 to 166 |
| deliver_item(item_2) | move_to(kitting_table_0) | 167 to 194 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 195 to 196 |
| deliver_item(item_3) | move_to(item_3) | -1 to 29 |
| deliver_item(item_3) | pick_up(item_3) | 30 to 31 |
| deliver_item(item_3) | move_to(kitting_table_0) | 32 to 62 |
| deliver_item(item_3) | place(item_3,kitting_table_0) | 63 to 64 |
| deliver_item(item_4) | move_to(item_4) | -1 to 31 |
| deliver_item(item_4) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_4) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_4) | move_to(item_4) | 65 to 166 |
| deliver_item(item_4) | place(item_2,shelf_2) | 167 to 169 |
| deliver_item(item_4) | move_to(shelf_2) | 170 to 196 |
| deliver_item(item_4) | move_to(item_4) | 197 to 243 |
| deliver_item(item_4) | place(item_1,shelf_1) | 244 to 245 |
| deliver_item(item_4) | move_to(shelf_1) | 246 to 289 |
| deliver_item(item_4) | move_to(item_4) | 290 to 333 |
| deliver_item(item_4) | pick_up(item_4) | 334 to 335 |
| deliver_item(item_4) | move_to(kitting_table_0) | 336 to 379 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 380 to 381 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 145 | boundary |
| 145 | pin coffee_break(coffee_machine_0) |
| 147 | re-entry coffee_break(coffee_machine_0) |
| 197 | boundary |
| 197 | pin deliver_item(item_2) |
| 290 | boundary |
| 290 | pin deliver_item(item_1) |
| 382 | boundary |
| 382 | pin deliver_item(item_4) |
| 406 | finding turns unexplained |

Never pinned: none. At the last entry (go_to(corner_NE), ticks 384 to 405): lifecycle and finding adequate; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 26 | 0.7624 | yes | adequate |
| deliver_item(item_2) | 67 to 93 | 87 | 0.7597 | yes | adequate |
| coffee_break(coffee_machine_0) | 94 to 146 | 120 | 0.7723 | yes | adequate |
| deliver_item(item_2) | 147 to 198 | 155 | 0.7882 | yes | adequate |
| deliver_item(item_1) | 199 to 291 | 237 | 0.7646 | yes | adequate |
| deliver_item(item_4) | 292 to 383 | 300 | 0.9823 | yes | adequate |

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
| 101 | deliver_item(item_4) | move_to(item_4) | 0.2386 | 0.0480 | 338.7 | 318.7 | 20.0 | coffee_break(coffee_machine_0) |
| 104 | deliver_item(item_2) | move_to(item_2) | 0.3775 | 0.0404 | 356.1 | 356.1 | 0.0 | coffee_break(coffee_machine_0) |
| 156 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 157 | deliver_item(item_4) | move_to(item_4) | 0.0469 | 0.0394 | 358.6 | 358.6 | 0.0 | deliver_item(item_2) |
| 159 | deliver_item(item_1) | move_to(item_1) | 0.0479 | 0.0379 | 362.7 | 362.7 | 0.0 | deliver_item(item_2) |
| 179 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0418 | 352.7 | 352.7 | 0.0 | deliver_item(item_2) |
| 179 | deliver_item(item_4) | move_to(shelf_2) | 0.0010 | 0.0418 | 352.7 | 352.7 | 0.0 | deliver_item(item_2) |
| 229 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0414 | 353.6 | 353.6 | 0.0 | deliver_item(item_1) |
| 255 | deliver_item(item_4) | move_to(shelf_1) | 0.0042 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 333 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0012 | 0.0432 | 349.2 | 349.2 | 0.0 | deliver_item(item_4) |
| 406 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9960 | 0.0468 | 341.1 | 301.1 | 40.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_3) |
| 65 | adequate | unresolved | deliver_item(item_3) |
| 66 | unresolved | adequate | deliver_item(item_3) |
| 145 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 146 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 197 | adequate | unresolved | deliver_item(item_2) |
| 198 | unresolved | adequate | deliver_item(item_2) |
| 290 | adequate | unresolved | deliver_item(item_1) |
| 291 | unresolved | adequate | deliver_item(item_1) |
| 382 | adequate | unresolved | deliver_item(item_4) |
| 383 | unresolved | adequate | deliver_item(item_4) |
| 406 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 94 to 146, its hypothesis pinned at 145; the suspended task resumes at 147.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | deliver_item(item_3) belief / S | deliver_item(item_4) belief / S | finding |
|---|---|---|---|---|---|---|---|---|
| 92 | move_to step | deliver_item(item_2) | 0.0288 / 0.4686 | 0.0160 / 0.0134 | 0.8642 / 1.0000 | retired | 0.0900 / 0.0772 | adequate |
| 93 | move_to  | deliver_item(item_2) | 0.0254 / 0.3942 | 0.0134 / 0.0110 | 0.8841 / 1.0000 | retired | 0.0761 / 0.0635 | adequate |
| 94 | move_to step | coffee_break(coffee_machine_0) | 0.0254 / 0.3942 | 0.0125 / 0.0102 | 0.8867 / 1.0000 | retired | 0.0743 / 0.0617 | adequate |
| 95 | move_to step | coffee_break(coffee_machine_0) | 0.0255 / 0.3942 | 0.0117 / 0.0095 | 0.8894 / - | retired | 0.0724 / 0.0599 | adequate |
| 96 | move_to step | coffee_break(coffee_machine_0) | 0.0308 / 0.3942 | 0.0130 / 0.0088 | 0.8705 / 0.7505 | retired | 0.0846 / 0.0581 | adequate |
| 144 | wait_at stand | coffee_break(coffee_machine_0) | 0.9948 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0022 / 0.0000 | adequate |
| 145 | wait_at stand | coffee_break(coffee_machine_0) | retired | 0.3327 / - | 0.3327 / - | retired | 0.3327 / - | unresolved |
| 146 | wait_at  | coffee_break(coffee_machine_0) | retired | 0.3327 / 1.0000 | 0.3327 / 1.0000 | retired | 0.3327 / 1.0000 | adequate |
| 147 | move_to step | deliver_item(item_2) | 0.0050 / - | 0.3191 / 0.8319 | 0.3641 / 1.0000 | retired | 0.3108 / 0.8029 | adequate |
| 148 | move_to step | deliver_item(item_2) | 0.0044 / 0.7401 | 0.3043 / 0.6825 | 0.4037 / 1.0000 | retired | 0.2865 / 0.6324 | adequate |
| 149 | move_to step | deliver_item(item_2) | 0.0038 / 0.5354 | 0.2864 / 0.5525 | 0.4500 / 1.0000 | retired | 0.2588 / 0.4891 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 144, 199 to 289, 292 to 381, 384 to 435 |
| deliver_item(item_1) | 0 to 31, 67 to 144, 199 to 289 |
| deliver_item(item_2) | 67 to 94, 147 to 196 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 144, 199 to 243, 292 to 381 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 25 | deliver_item(item_3) | none(below_theta) |
| 26 to 64 | deliver_item(item_3) | clears |
| 65 to 66 | deliver_item(item_1) | none(below_theta) |
| 67 to 86 | deliver_item(item_2) | none(below_theta) |
| 87 to 94 | deliver_item(item_2) | clears |
| 95 to 95 | deliver_item(item_2) | none(leader_no_observation) |
| 96 to 99 | deliver_item(item_2) | clears |
| 100 to 103 | deliver_item(item_2) | none(below_theta) |
| 104 to 112 | deliver_item(item_4) | none(below_theta) |
| 113 to 119 | coffee_break(coffee_machine_0) | none(below_theta) |
| 120 to 144 | coffee_break(coffee_machine_0) | clears |
| 145 to 146 | deliver_item(item_1) | none(below_theta) |
| 147 to 154 | deliver_item(item_2) | none(below_theta) |
| 155 to 196 | deliver_item(item_2) | clears |
| 197 to 236 | deliver_item(item_1) | none(below_theta) |
| 237 to 289 | deliver_item(item_1) | clears |
| 290 to 299 | coffee_break(coffee_machine_0) | none(below_theta) |
| 300 to 381 | deliver_item(item_4) | clears |
| 382 to 382 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 383 to 383 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 384 to 405 | coffee_break(coffee_machine_0) | clears |
| 406 to 435 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of coffee_break | 0 to 144 ordinary, 145 to 146 retired, 147 to 234 suppressed, 235 to 299 raised, 300 to 435 ordinary |
| recency facts | 0 to 144 none, 145 to 234 coffee_break, 235 to 435 none |

The last entry (go_to(corner_NE)): first step 384, last step 404, acknowledgement 405; the idle human from 406. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9960 at 384; S < α from 406 (belief 0.9960; v·D 341.1 cm); the finding unexplained from 406.

