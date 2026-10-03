### scenario_s15_05

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

Last acknowledgement tick 405; idle from 406 to 435. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 435 |
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

Never pinned: ac_activation(ac_switch_0). At the last entry (go_to(corner_NE), ticks 384 to 405): lifecycle and finding adequate; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 28 | 0.7512 | yes | adequate |
| deliver_item(item_2) | 67 to 93 | not reached | - | - | - |
| coffee_break(coffee_machine_0) | 94 to 146 | 104 | 0.7765 | yes | adequate |
| deliver_item(item_2) | 147 to 198 | 157 | 0.8006 | yes | adequate |
| deliver_item(item_1) | 199 to 291 | 246 | 0.7609 | yes | adequate |
| deliver_item(item_4) | 292 to 383 | 338 | 0.7872 | yes | adequate |

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
| 101 | deliver_item(item_4) | move_to(item_4) | 0.0874 | 0.0480 | 338.7 | 318.7 | 20.0 | coffee_break(coffee_machine_0) |
| 104 | deliver_item(item_2) | move_to(item_2) | 0.0897 | 0.0404 | 356.1 | 356.1 | 0.0 | coffee_break(coffee_machine_0) |
| 156 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0356 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 157 | deliver_item(item_4) | move_to(item_4) | 0.0432 | 0.0394 | 358.6 | 358.6 | 0.0 | deliver_item(item_2) |
| 158 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0421 | 0.0363 | 367.0 | 367.0 | 0.0 | deliver_item(item_2) |
| 159 | deliver_item(item_1) | move_to(item_1) | 0.0458 | 0.0379 | 362.7 | 362.7 | 0.0 | deliver_item(item_2) |
| 179 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0418 | 352.7 | 352.7 | 0.0 | deliver_item(item_2) |
| 179 | deliver_item(item_4) | move_to(shelf_2) | 0.0010 | 0.0418 | 352.7 | 352.7 | 0.0 | deliver_item(item_2) |
| 229 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0228 | 0.0414 | 353.6 | 353.6 | 0.0 | deliver_item(item_1) |
| 251 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0513 | 0.0405 | 356.0 | 296.0 | 60.0 | deliver_item(item_1) |
| 255 | deliver_item(item_4) | move_to(shelf_1) | 0.0041 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 333 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0366 | 0.0432 | 349.2 | 349.2 | 0.0 | deliver_item(item_4) |
| 343 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0539 | 0.0422 | 351.7 | 291.7 | 60.0 | deliver_item(item_4) |
| 397 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.1836 | 0.0483 | 337.9 | 337.9 | 0.0 | - |
| 406 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9059 | 0.0468 | 341.1 | 301.1 | 40.0 | - |

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

| tick | human action | truth | ac_activation(ac_switch_0) belief / S | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | deliver_item(item_3) belief / S | deliver_item(item_4) belief / S | finding |
|---|---|---|---|---|---|---|---|---|---|
| 92 | move_to step | deliver_item(item_2) | 0.0268 / 0.0337 | 0.3215 / 0.4686 | 0.0107 / 0.0134 | 0.5796 / 1.0000 | retired | 0.0604 / 0.0772 | adequate |
| 93 | move_to  | deliver_item(item_2) | 0.0235 / 0.0277 | 0.2953 / 0.3942 | 0.0094 / 0.0110 | 0.6176 / 1.0000 | retired | 0.0532 / 0.0635 | adequate |
| 94 | move_to step | coffee_break(coffee_machine_0) | 0.0224 / 0.0264 | 0.2963 / 0.3942 | 0.0088 / 0.0102 | 0.6196 / 1.0000 | retired | 0.0519 / 0.0617 | adequate |
| 95 | move_to step | coffee_break(coffee_machine_0) | 0.0214 / 0.0251 | 0.2972 / 0.3942 | 0.0082 / 0.0095 | 0.6216 / - | retired | 0.0506 / 0.0599 | adequate |
| 96 | move_to step | coffee_break(coffee_machine_0) | 0.0232 / 0.0238 | 0.3380 / 0.3942 | 0.0086 / 0.0088 | 0.5735 / 0.7505 | retired | 0.0558 / 0.0581 | adequate |
| 144 | wait_at stand | coffee_break(coffee_machine_0) | 0.0010 / 0.0000 | 0.9950 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | adequate |
| 145 | wait_at stand | coffee_break(coffee_machine_0) | 0.2495 / - | retired | 0.2495 / - | 0.2495 / - | retired | 0.2495 / - | unresolved |
| 146 | wait_at  | coffee_break(coffee_machine_0) | 0.2495 / 1.0000 | retired | 0.2495 / 1.0000 | 0.2495 / 1.0000 | retired | 0.2495 / 1.0000 | adequate |
| 147 | move_to step | deliver_item(item_2) | 0.1919 / 0.8146 | 0.1998 / - | 0.1949 / 0.8319 | 0.2224 / 1.0000 | retired | 0.1899 / 0.8029 | adequate |
| 148 | move_to step | deliver_item(item_2) | 0.1858 / 0.6527 | 0.1841 / 0.7401 | 0.1925 / 0.6825 | 0.2553 / 1.0000 | retired | 0.1812 / 0.6324 | adequate |
| 149 | move_to step | deliver_item(item_2) | 0.1780 / 0.5147 | 0.1652 / 0.5354 | 0.1887 / 0.5525 | 0.2966 / 1.0000 | retired | 0.1705 / 0.4891 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 64, 67 to 144, 199 to 289, 292 to 379 |
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 144, 199 to 289, 292 to 381, 384 to 435 |
| deliver_item(item_1) | 0 to 31, 67 to 144, 199 to 289 |
| deliver_item(item_2) | 67 to 94, 147 to 196 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 144, 199 to 243, 292 to 381 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 27 | deliver_item(item_3) | none(below_theta) |
| 28 to 64 | deliver_item(item_3) | clears |
| 65 to 66 | ac_activation(ac_switch_0) | none(below_theta) |
| 67 to 97 | deliver_item(item_2) | none(below_theta) |
| 98 to 103 | coffee_break(coffee_machine_0) | none(below_theta) |
| 104 to 144 | coffee_break(coffee_machine_0) | clears |
| 145 to 146 | ac_activation(ac_switch_0) | none(below_theta) |
| 147 to 156 | deliver_item(item_2) | none(below_theta) |
| 157 to 196 | deliver_item(item_2) | clears |
| 197 to 198 | ac_activation(ac_switch_0) | none(below_theta) |
| 199 to 245 | deliver_item(item_1) | none(below_theta) |
| 246 to 289 | deliver_item(item_1) | clears |
| 290 to 291 | ac_activation(ac_switch_0) | none(below_theta) |
| 292 to 337 | deliver_item(item_4) | none(below_theta) |
| 338 to 381 | deliver_item(item_4) | clears |
| 382 to 383 | ac_activation(ac_switch_0) | none(below_theta) |
| 384 to 394 | coffee_break(coffee_machine_0) | none(below_theta) |
| 395 to 405 | coffee_break(coffee_machine_0) | clears |
| 406 to 435 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_NE)): first step 384, last step 404, acknowledgement 405; the idle human from 406. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.4826 at 384; S < α from 397 (belief 0.1836; v·D 337.9 cm); the finding unexplained from 406.

- coffee_break(coffee_machine_0): belief 0.5134 at 384; S < α from 406 (belief 0.9059; v·D 341.1 cm); the finding unexplained from 406.

