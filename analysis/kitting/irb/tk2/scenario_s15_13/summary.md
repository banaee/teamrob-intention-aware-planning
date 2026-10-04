### scenario_s15_13

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
| 122 | ac_activation(ac_switch_0) | covered | move_to | 0 | 2 |
| 168 | ac_activation(ac_switch_0) | covered | switch_on | 0 | 2 |
| 170 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 215 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 217 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 261 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 263 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 307 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 309 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 353 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 355 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 399 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 401 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 422; idle from 423 to 452. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 165 |
| ac_activation(ac_switch_0) | switch_on(PT2S,ac_switch_0) | 166 to 167 |
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | 170 to 452 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 452 |
| deliver_item(item_1) | move_to(item_1) | -1 to 31 |
| deliver_item(item_1) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_1) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_1) | move_to(item_1) | 65 to 93 |
| deliver_item(item_1) | place(item_2,shelf_2) | 94 to 95 |
| deliver_item(item_1) | move_to(shelf_2) | 96 to 214 |
| deliver_item(item_1) | move_to(item_1) | 215 to 258 |
| deliver_item(item_1) | pick_up(item_1) | 259 to 260 |
| deliver_item(item_1) | move_to(kitting_table_0) | 261 to 304 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 305 to 306 |
| deliver_item(item_2) | move_to(item_2) | -1 to 31 |
| deliver_item(item_2) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_2) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_2) | move_to(item_2) | 65 to 91 |
| deliver_item(item_2) | pick_up(item_2) | 92 to 93 |
| deliver_item(item_2) | move_to(kitting_table_0) | 94 to 119 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 120 to 121 |
| deliver_item(item_2) | move_to(kitting_table_0) | 122 to 212 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 213 to 214 |
| deliver_item(item_3) | move_to(item_3) | -1 to 29 |
| deliver_item(item_3) | pick_up(item_3) | 30 to 31 |
| deliver_item(item_3) | move_to(kitting_table_0) | 32 to 62 |
| deliver_item(item_3) | place(item_3,kitting_table_0) | 63 to 64 |
| deliver_item(item_4) | move_to(item_4) | -1 to 31 |
| deliver_item(item_4) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_4) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_4) | move_to(item_4) | 65 to 93 |
| deliver_item(item_4) | place(item_2,shelf_2) | 94 to 95 |
| deliver_item(item_4) | move_to(shelf_2) | 96 to 214 |
| deliver_item(item_4) | move_to(item_4) | 215 to 260 |
| deliver_item(item_4) | place(item_1,shelf_1) | 261 to 262 |
| deliver_item(item_4) | move_to(shelf_1) | 263 to 306 |
| deliver_item(item_4) | move_to(item_4) | 307 to 350 |
| deliver_item(item_4) | pick_up(item_4) | 351 to 352 |
| deliver_item(item_4) | move_to(kitting_table_0) | 353 to 396 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 397 to 398 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 122 | finding turns unexplained |
| 123 | finding turns adequate (from unexplained) |
| 131 | finding turns unexplained |
| 166 | finding turns adequate (from unexplained) |
| 168 | boundary |
| 168 | pin ac_activation(ac_switch_0) |
| 170 | re-entry ac_activation(ac_switch_0) |
| 215 | boundary |
| 215 | pin deliver_item(item_2) |
| 307 | boundary |
| 307 | pin deliver_item(item_1) |
| 399 | boundary |
| 399 | pin deliver_item(item_4) |
| 423 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_NE), ticks 401 to 422): lifecycle and finding adequate; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 26 | 0.7569 | yes | adequate |
| deliver_item(item_2) | 67 to 121 | 87 | 0.7557 | yes | adequate |
| ac_activation(ac_switch_0) | 122 to 169 | 152 | 0.7873 | yes | inadequate |
| deliver_item(item_2) | 170 to 216 | 197 | 0.7730 | yes | adequate |
| deliver_item(item_1) | 217 to 308 | 253 | 0.7593 | yes | adequate |
| deliver_item(item_4) | 309 to 400 | 309 | 0.9758 | yes | adequate |

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
| 131 | deliver_item(item_2) | move_to(kitting_table_0) | 0.9950 | 0.0399 | 357.5 | 357.5 | 0.0 | ac_activation(ac_switch_0) |
| 179 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 187 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0017 | 0.0399 | 357.4 | 357.4 | 0.0 | deliver_item(item_2) |
| 202 | deliver_item(item_1) | move_to(shelf_2) | 0.0506 | 0.0413 | 353.9 | 353.9 | 0.0 | deliver_item(item_2) |
| 202 | deliver_item(item_4) | move_to(shelf_2) | 0.0506 | 0.0413 | 353.9 | 353.9 | 0.0 | deliver_item(item_2) |
| 246 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0015 | 0.0443 | 346.8 | 346.8 | 0.0 | deliver_item(item_1) |
| 268 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0408 | 355.2 | 295.2 | 60.0 | deliver_item(item_1) |
| 272 | deliver_item(item_4) | move_to(shelf_1) | 0.0042 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 350 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0012 | 0.0424 | 351.3 | 351.3 | 0.0 | deliver_item(item_4) |
| 360 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0419 | 352.4 | 292.4 | 60.0 | deliver_item(item_4) |
| 414 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0531 | 0.0477 | 339.4 | 339.4 | 0.0 | - |
| 423 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9719 | 0.0460 | 342.9 | 302.9 | 40.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_3) |
| 65 | adequate | unresolved | deliver_item(item_3) |
| 66 | unresolved | adequate | deliver_item(item_3) |
| 122 | adequate | unexplained | ac_activation(ac_switch_0) |
| 123 | unexplained | adequate | ac_activation(ac_switch_0) |
| 131 | adequate | unexplained | ac_activation(ac_switch_0) |
| 166 | unexplained | adequate | ac_activation(ac_switch_0) |
| 168 | adequate | unresolved | ac_activation(ac_switch_0) |
| 169 | unresolved | adequate | ac_activation(ac_switch_0) |
| 215 | adequate | unresolved | deliver_item(item_2) |
| 216 | unresolved | adequate | deliver_item(item_2) |
| 307 | adequate | unresolved | deliver_item(item_1) |
| 308 | unresolved | adequate | deliver_item(item_1) |
| 399 | adequate | unresolved | deliver_item(item_4) |
| 400 | unresolved | adequate | deliver_item(item_4) |
| 423 | adequate | unexplained | - |

Across the started task ac_activation(ac_switch_0) (covered; actual): on top of the stack from 122 to 169, its hypothesis pinned at 168; the suspended task resumes at 170.

| tick | human action | truth | ac_activation(ac_switch_0) belief / S | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | deliver_item(item_3) belief / S | deliver_item(item_4) belief / S | finding |
|---|---|---|---|---|---|---|---|---|---|
| 120 | move_to step | deliver_item(item_2) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0001 | 0.9950 / 1.0000 | retired | 0.0010 / 0.0001 | adequate |
| 121 | move_to  | deliver_item(item_2) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0001 | 0.9950 / 1.0000 | retired | 0.0010 / 0.0001 | adequate |
| 122 | move_to step | ac_activation(ac_switch_0) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0001 | 0.9950 / - | retired | 0.0010 / 0.0001 | unexplained |
| 123 | move_to step | ac_activation(ac_switch_0) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0001 | 0.9950 / 0.7468 | retired | 0.0010 / 0.0001 | adequate |
| 124 | move_to step | ac_activation(ac_switch_0) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0001 | 0.9950 / 0.5429 | retired | 0.0010 / 0.0001 | adequate |
| 167 | move_to  | ac_activation(ac_switch_0) | 0.9950 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | adequate |
| 168 | switch_on stand | ac_activation(ac_switch_0) | retired | 0.0196 / - | 0.3261 / - | 0.3261 / - | retired | 0.3261 / - | unresolved |
| 169 | switch_on  | ac_activation(ac_switch_0) | retired | 0.0196 / 1.0000 | 0.3261 / 1.0000 | 0.3261 / 1.0000 | retired | 0.3261 / 1.0000 | adequate |
| 170 | move_to step | deliver_item(item_2) | 0.0048 / - | 0.0185 / 0.9084 | 0.3231 / 0.9718 | 0.3296 / 1.0000 | retired | 0.3231 / 0.9718 | adequate |
| 171 | move_to step | deliver_item(item_2) | 0.0039 / 0.7401 | 0.0174 / 0.8185 | 0.3214 / 0.9428 | 0.3349 / 1.0000 | retired | 0.3214 / 0.9428 | adequate |
| 172 | move_to step | deliver_item(item_2) | 0.0031 / 0.5354 | 0.0163 / 0.7312 | 0.3195 / 0.9130 | 0.3407 / 1.0000 | retired | 0.3195 / 0.9130 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 64, 67 to 119, 122 to 167, 217 to 304, 309 to 396 |
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 167, 170 to 187, 217 to 304, 309 to 398, 401 to 452 |
| deliver_item(item_1) | 0 to 31, 67 to 93, 170 to 214, 217 to 306 |
| deliver_item(item_2) | 67 to 121, 170 to 214 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 93, 170 to 214, 217 to 260, 309 to 398 |

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
| 131 to 149 | deliver_item(item_2) | none(leader_inadequate) |
| 150 to 151 | ac_activation(ac_switch_0) | none(below_theta) |
| 152 to 165 | ac_activation(ac_switch_0) | none(leader_inadequate) |
| 166 to 167 | ac_activation(ac_switch_0) | clears |
| 168 to 169 | deliver_item(item_1) | none(below_theta) |
| 170 to 196 | deliver_item(item_2) | none(below_theta) |
| 197 to 214 | deliver_item(item_2) | clears |
| 215 to 252 | deliver_item(item_1) | none(below_theta) |
| 253 to 306 | deliver_item(item_1) | clears |
| 307 to 307 | deliver_item(item_4) | none(leader_no_observation) |
| 308 to 308 | deliver_item(item_4) | none(leader_unwarranted) |
| 309 to 398 | deliver_item(item_4) | clears |
| 399 to 399 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 400 to 400 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 401 to 422 | coffee_break(coffee_machine_0) | clears |
| 423 to 452 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of ac_activation | 0 to 149 ordinary, 150 to 167 raised, 168 to 169 retired, 170 to 452 suppressed |
| level of coffee_break | 0 to 452 ordinary |
| recency facts | 0 to 452 none |

The last entry (go_to(corner_NE)): first step 401, last step 421, acknowledgement 422; the idle human from 423. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.1895 at 401; S < α from 414 (belief 0.0531; v·D 339.4 cm); the finding unexplained from 423.

- coffee_break(coffee_machine_0): belief 0.8065 at 401; S < α from 423 (belief 0.9719; v·D 342.9 cm); the finding unexplained from 423.

