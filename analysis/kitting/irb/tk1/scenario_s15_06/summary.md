### scenario_s15_06

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

Last acknowledgement tick 400; idle from 401 to 430. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 430 |
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

Never pinned: ac_activation(ac_switch_0). At the last entry (go_to(corner_NE), ticks 379 to 400): lifecycle and finding adequate; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 28 | 0.7512 | yes | adequate |
| deliver_item(item_2) | 67 to 95 | not reached | - | - | - |
| coffee_break(coffee_machine_0) | 96 to 148 | 104 | 0.7583 | yes | adequate |
| deliver_item(item_2) | 149 to 193 | 170 | 0.7659 | yes | adequate |
| deliver_item(item_1) | 194 to 286 | 241 | 0.7608 | yes | adequate |
| deliver_item(item_4) | 287 to 378 | 332 | 0.7512 | yes | adequate |

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
| 105 | deliver_item(item_2) | move_to(kitting_table_0) | 0.1403 | 0.0441 | 347.1 | 347.1 | 0.0 | coffee_break(coffee_machine_0) |
| 106 | deliver_item(item_1) | move_to(shelf_2) | 0.0017 | 0.0404 | 356.1 | 356.1 | 0.0 | coffee_break(coffee_machine_0) |
| 106 | deliver_item(item_4) | move_to(shelf_2) | 0.0096 | 0.0404 | 356.1 | 356.1 | 0.0 | coffee_break(coffee_machine_0) |
| 158 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0185 | 0.0392 | 359.2 | 359.2 | 0.0 | deliver_item(item_2) |
| 163 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0303 | 0.0473 | 340.1 | 340.1 | 0.0 | deliver_item(item_2) |
| 173 | deliver_item(item_1) | move_to(shelf_2) | 0.0556 | 0.0461 | 342.8 | 342.8 | 0.0 | deliver_item(item_2) |
| 173 | deliver_item(item_4) | move_to(shelf_2) | 0.0556 | 0.0461 | 342.8 | 342.8 | 0.0 | deliver_item(item_2) |
| 224 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0231 | 0.0419 | 352.5 | 352.5 | 0.0 | deliver_item(item_1) |
| 246 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0516 | 0.0407 | 355.5 | 295.5 | 60.0 | deliver_item(item_1) |
| 250 | deliver_item(item_4) | move_to(shelf_1) | 0.0041 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 328 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0363 | 0.0428 | 350.4 | 350.4 | 0.0 | deliver_item(item_4) |
| 338 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0537 | 0.0421 | 352.1 | 292.1 | 60.0 | deliver_item(item_4) |
| 392 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.1833 | 0.0480 | 338.7 | 338.7 | 0.0 | - |
| 401 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9060 | 0.0464 | 342.1 | 302.1 | 40.0 | - |

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

| tick | human action | truth | ac_activation(ac_switch_0) belief / S | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | deliver_item(item_3) belief / S | deliver_item(item_4) belief / S | finding |
|---|---|---|---|---|---|---|---|---|---|
| 94 | pick_up grasp | deliver_item(item_2) | 0.0204 / 0.0227 | 0.2683 / 0.3303 | 0.0082 / 1.0000 | 0.6555 / 1.0000 | retired | 0.0466 / 1.0000 | adequate |
| 95 | pick_up  | deliver_item(item_2) | 0.0176 / 0.0186 | 0.2386 / 0.2757 | 0.0085 / 1.0000 | 0.6856 / 1.0000 | retired | 0.0487 / 1.0000 | adequate |
| 96 | move_to step | coffee_break(coffee_machine_0) | 0.0189 / 0.0177 | 0.2691 / 0.2757 | 0.0096 / 1.0000 | 0.6464 / 0.7806 | retired | 0.0550 / 1.0000 | adequate |
| 97 | move_to step | coffee_break(coffee_machine_0) | 0.0205 / 0.0169 | 0.3068 / 0.2757 | 0.0110 / - | 0.5980 / 0.5975 | retired | 0.0626 / - | adequate |
| 98 | move_to step | coffee_break(coffee_machine_0) | 0.0227 / 0.0160 | 0.3573 / 0.2757 | 0.0104 / 0.7505 | 0.5495 / 0.4493 | retired | 0.0592 / 0.7505 | adequate |
| 146 | wait_at stand | coffee_break(coffee_machine_0) | 0.0010 / 0.0000 | 0.9950 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | adequate |
| 147 | wait_at stand | coffee_break(coffee_machine_0) | 0.2495 / - | retired | 0.2495 / - | 0.2495 / - | retired | 0.2495 / - | unresolved |
| 148 | wait_at  | coffee_break(coffee_machine_0) | 0.2495 / 1.0000 | retired | 0.2495 / 1.0000 | 0.2495 / 1.0000 | retired | 0.2495 / 1.0000 | adequate |
| 149 | move_to step | deliver_item(item_2) | 0.1878 / 0.8798 | 0.1998 / - | 0.2028 / 0.9801 | 0.2057 / 1.0000 | retired | 0.2028 / 0.9801 | adequate |
| 150 | move_to step | deliver_item(item_2) | 0.1810 / 0.7660 | 0.1717 / 0.7421 | 0.2133 / 0.9585 | 0.2197 / 1.0000 | retired | 0.2133 / 0.9585 | adequate |
| 151 | move_to step | deliver_item(item_2) | 0.1727 / 0.6596 | 0.1422 / 0.5377 | 0.2244 / 0.9350 | 0.2353 / 1.0000 | retired | 0.2244 / 0.9350 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 64, 67 to 146, 149 to 155, 194 to 284, 287 to 374 |
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 146, 194 to 284, 287 to 376, 379 to 430 |
| deliver_item(item_1) | 0 to 31, 67 to 93, 149 to 183, 194 to 284 |
| deliver_item(item_2) | 67 to 146, 149 to 191 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 93, 149 to 183, 194 to 238, 287 to 376 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 27 | deliver_item(item_3) | none(below_theta) |
| 28 to 64 | deliver_item(item_3) | clears |
| 65 to 66 | ac_activation(ac_switch_0) | none(below_theta) |
| 67 to 99 | deliver_item(item_2) | none(below_theta) |
| 100 to 103 | coffee_break(coffee_machine_0) | none(below_theta) |
| 104 to 146 | coffee_break(coffee_machine_0) | clears |
| 147 to 148 | ac_activation(ac_switch_0) | none(below_theta) |
| 149 to 169 | deliver_item(item_2) | none(below_theta) |
| 170 to 191 | deliver_item(item_2) | clears |
| 192 to 193 | ac_activation(ac_switch_0) | none(below_theta) |
| 194 to 240 | deliver_item(item_1) | none(below_theta) |
| 241 to 284 | deliver_item(item_1) | clears |
| 285 to 286 | ac_activation(ac_switch_0) | none(below_theta) |
| 287 to 331 | deliver_item(item_4) | none(below_theta) |
| 332 to 376 | deliver_item(item_4) | clears |
| 377 to 378 | ac_activation(ac_switch_0) | none(below_theta) |
| 379 to 389 | coffee_break(coffee_machine_0) | none(below_theta) |
| 390 to 400 | coffee_break(coffee_machine_0) | clears |
| 401 to 430 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_NE)): first step 379, last step 399, acknowledgement 400; the idle human from 401. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.4826 at 379; S < α from 392 (belief 0.1833; v·D 338.7 cm); the finding unexplained from 401.

- coffee_break(coffee_machine_0): belief 0.5134 at 379; S < α from 401 (belief 0.9060; v·D 342.1 cm); the finding unexplained from 401.

