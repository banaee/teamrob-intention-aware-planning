### scenario_s15_07

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
| 122 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 165 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 196 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 239 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 241 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 286 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 288 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 333 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 335 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 380 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 382 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 427 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 429 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 450; idle from 451 to 480. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 480 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 162 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 163 to 193 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 196 to 480 |
| deliver_item(item_1) | move_to(item_1) | -1 to 31 |
| deliver_item(item_1) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_1) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_1) | move_to(item_1) | 65 to 93 |
| deliver_item(item_1) | place(item_2,shelf_2) | 94 to 95 |
| deliver_item(item_1) | move_to(shelf_2) | 96 to 238 |
| deliver_item(item_1) | move_to(item_1) | 239 to 283 |
| deliver_item(item_1) | pick_up(item_1) | 284 to 285 |
| deliver_item(item_1) | move_to(kitting_table_0) | 286 to 330 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 331 to 332 |
| deliver_item(item_2) | move_to(item_2) | -1 to 31 |
| deliver_item(item_2) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_2) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_2) | move_to(item_2) | 65 to 91 |
| deliver_item(item_2) | pick_up(item_2) | 92 to 93 |
| deliver_item(item_2) | move_to(kitting_table_0) | 94 to 119 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 120 to 121 |
| deliver_item(item_2) | move_to(kitting_table_0) | 122 to 236 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 237 to 238 |
| deliver_item(item_3) | move_to(item_3) | -1 to 29 |
| deliver_item(item_3) | pick_up(item_3) | 30 to 31 |
| deliver_item(item_3) | move_to(kitting_table_0) | 32 to 62 |
| deliver_item(item_3) | place(item_3,kitting_table_0) | 63 to 64 |
| deliver_item(item_4) | move_to(item_4) | -1 to 31 |
| deliver_item(item_4) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_4) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_4) | move_to(item_4) | 65 to 93 |
| deliver_item(item_4) | place(item_2,shelf_2) | 94 to 95 |
| deliver_item(item_4) | move_to(shelf_2) | 96 to 238 |
| deliver_item(item_4) | move_to(item_4) | 239 to 285 |
| deliver_item(item_4) | place(item_1,shelf_1) | 286 to 287 |
| deliver_item(item_4) | move_to(shelf_1) | 288 to 332 |
| deliver_item(item_4) | move_to(item_4) | 333 to 377 |
| deliver_item(item_4) | pick_up(item_4) | 378 to 379 |
| deliver_item(item_4) | move_to(kitting_table_0) | 380 to 424 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 425 to 426 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 122 | finding turns unexplained |
| 123 | finding turns adequate (from unexplained) |
| 131 | finding turns unexplained |
| 163 | finding turns adequate (from unexplained) |
| 194 | boundary |
| 194 | pin coffee_break(coffee_machine_0) |
| 196 | re-entry coffee_break(coffee_machine_0) |
| 239 | boundary |
| 239 | pin deliver_item(item_2) |
| 333 | boundary |
| 333 | pin deliver_item(item_1) |
| 427 | boundary |
| 427 | pin deliver_item(item_4) |
| 452 | finding turns unexplained |

Never pinned: ac_activation(ac_switch_0). At the last entry (go_to(corner_NE), ticks 429 to 450): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 26 | 0.7569 | yes | adequate |
| deliver_item(item_2) | 67 to 121 | 87 | 0.7557 | yes | adequate |
| coffee_break(coffee_machine_0) | 122 to 195 | 160 | 0.7968 | yes | inadequate |
| deliver_item(item_2) | 196 to 240 | 217 | 0.7622 | yes | adequate |
| deliver_item(item_1) | 241 to 334 | 278 | 0.7524 | yes | adequate |
| deliver_item(item_4) | 335 to 428 | 335 | 0.9617 | yes | adequate |

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
| 131 | deliver_item(item_2) | move_to(kitting_table_0) | 0.9950 | 0.0391 | 359.5 | 359.5 | 0.0 | coffee_break(coffee_machine_0) |
| 205 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 210 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0018 | 0.0469 | 341.0 | 341.0 | 0.0 | deliver_item(item_2) |
| 220 | deliver_item(item_1) | move_to(shelf_2) | 0.0595 | 0.0497 | 335.1 | 335.1 | 0.0 | deliver_item(item_2) |
| 220 | deliver_item(item_4) | move_to(shelf_2) | 0.0595 | 0.0497 | 335.1 | 335.1 | 0.0 | deliver_item(item_2) |
| 270 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0492 | 336.2 | 336.2 | 0.0 | deliver_item(item_1) |
| 293 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0021 | 0.0401 | 357.0 | 297.0 | 60.0 | deliver_item(item_1) |
| 297 | deliver_item(item_4) | move_to(shelf_1) | 0.0040 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 376 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0013 | 0.0496 | 335.2 | 335.2 | 0.0 | deliver_item(item_4) |
| 387 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0011 | 0.0418 | 352.8 | 292.8 | 60.0 | deliver_item(item_4) |
| 443 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.1701 | 0.0411 | 354.5 | 354.5 | 0.0 | - |
| 452 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9044 | 0.0434 | 348.8 | 288.8 | 60.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_3) |
| 65 | adequate | unresolved | deliver_item(item_3) |
| 66 | unresolved | adequate | deliver_item(item_3) |
| 122 | adequate | unexplained | coffee_break(coffee_machine_0) |
| 123 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 131 | adequate | unexplained | coffee_break(coffee_machine_0) |
| 163 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 194 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 195 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 239 | adequate | unresolved | deliver_item(item_2) |
| 240 | unresolved | adequate | deliver_item(item_2) |
| 333 | adequate | unresolved | deliver_item(item_1) |
| 334 | unresolved | adequate | deliver_item(item_1) |
| 427 | adequate | unresolved | deliver_item(item_4) |
| 428 | unresolved | adequate | deliver_item(item_4) |
| 452 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 122 to 195, its hypothesis pinned at 194; the suspended task resumes at 196.

| tick | human action | truth | ac_activation(ac_switch_0) belief / S | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | deliver_item(item_3) belief / S | deliver_item(item_4) belief / S | finding |
|---|---|---|---|---|---|---|---|---|---|
| 120 | move_to step | deliver_item(item_2) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0001 | 0.9950 / 1.0000 | retired | 0.0010 / 0.0001 | adequate |
| 121 | move_to  | deliver_item(item_2) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0001 | 0.9950 / 1.0000 | retired | 0.0010 / 0.0001 | adequate |
| 122 | move_to step | coffee_break(coffee_machine_0) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0001 | 0.9950 / - | retired | 0.0010 / 0.0001 | unexplained |
| 123 | move_to step | coffee_break(coffee_machine_0) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0001 | 0.9950 / 0.7413 | retired | 0.0010 / 0.0001 | adequate |
| 124 | move_to step | coffee_break(coffee_machine_0) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0001 | 0.9950 / 0.5367 | retired | 0.0010 / 0.0001 | adequate |
| 193 | wait_at stand | coffee_break(coffee_machine_0) | 0.0010 / 0.0000 | 0.9950 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | adequate |
| 194 | wait_at stand | coffee_break(coffee_machine_0) | 0.0196 / - | retired | 0.3261 / - | 0.3261 / - | retired | 0.3261 / - | unresolved |
| 195 | wait_at  | coffee_break(coffee_machine_0) | 0.0196 / 1.0000 | retired | 0.3261 / 1.0000 | 0.3261 / 1.0000 | retired | 0.3261 / 1.0000 | adequate |
| 196 | move_to step | deliver_item(item_2) | 0.0180 / 0.8799 | 0.0048 / - | 0.3239 / 0.9799 | 0.3285 / 1.0000 | retired | 0.3239 / 0.9799 | adequate |
| 197 | move_to step | deliver_item(item_2) | 0.0165 / 0.7661 | 0.0039 / 0.7401 | 0.3230 / 0.9582 | 0.3327 / 1.0000 | retired | 0.3230 / 0.9582 | adequate |
| 198 | move_to step | deliver_item(item_2) | 0.0149 / 0.6597 | 0.0030 / 0.5354 | 0.3218 / 0.9347 | 0.3375 / 1.0000 | retired | 0.3218 / 0.9347 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 64, 67 to 119, 122 to 193, 196 to 202, 241 to 330, 335 to 424 |
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 193, 241 to 330, 335 to 426, 429 to 480 |
| deliver_item(item_1) | 0 to 31, 67 to 93, 196 to 230, 241 to 332 |
| deliver_item(item_2) | 67 to 121, 196 to 238 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 93, 196 to 230, 241 to 285, 335 to 426 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 25 | deliver_item(item_3) | none(below_theta) |
| 26 to 64 | deliver_item(item_3) | clears |
| 65 to 66 | deliver_item(item_1) | none(below_theta) |
| 67 to 86 | deliver_item(item_2) | none(below_theta) |
| 87 to 121 | deliver_item(item_2) | clears |
| 122 to 122 | deliver_item(item_2) | none(leader_no_observation) |
| 123 to 130 | deliver_item(item_2) | none(leader_unwarranted) |
| 131 to 153 | deliver_item(item_2) | none(leader_inadequate) |
| 154 to 156 | deliver_item(item_2) | none(below_theta) |
| 157 to 159 | coffee_break(coffee_machine_0) | none(below_theta) |
| 160 to 162 | coffee_break(coffee_machine_0) | none(leader_inadequate) |
| 163 to 193 | coffee_break(coffee_machine_0) | clears |
| 194 to 195 | deliver_item(item_1) | none(below_theta) |
| 196 to 216 | deliver_item(item_2) | none(below_theta) |
| 217 to 238 | deliver_item(item_2) | clears |
| 239 to 277 | deliver_item(item_1) | none(below_theta) |
| 278 to 332 | deliver_item(item_1) | clears |
| 333 to 333 | deliver_item(item_4) | none(leader_no_observation) |
| 334 to 334 | deliver_item(item_4) | none(leader_unwarranted) |
| 335 to 426 | deliver_item(item_4) | clears |
| 427 to 428 | ac_activation(ac_switch_0) | none(below_theta) |
| 429 to 439 | coffee_break(coffee_machine_0) | none(below_theta) |
| 440 to 451 | coffee_break(coffee_machine_0) | clears |
| 452 to 480 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of ac_activation | 0 to 480 ordinary |
| level of coffee_break | 0 to 177 ordinary, 178 to 193 raised, 194 to 195 retired, 196 to 283 suppressed, 284 to 299 raised, 300 to 480 ordinary |
| recency facts | 0 to 193 none, 194 to 283 coffee_break, 284 to 480 none |

The last entry (go_to(corner_NE)): first step 429, last step 449, acknowledgement 450; the idle human from 451. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.4830 at 429; S < α from 443 (belief 0.1701; v·D 354.5 cm); the finding unexplained from 452.

- coffee_break(coffee_machine_0): belief 0.5130 at 429; S < α from 452 (belief 0.9044; v·D 348.8 cm); the finding unexplained from 452.

