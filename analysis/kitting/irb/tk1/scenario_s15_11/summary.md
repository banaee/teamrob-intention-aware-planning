### scenario_s15_11

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_3,kitting_table_0) | covered | move_to | 0 | 1 |
| 32 | deliver_item(item_3,kitting_table_0) | covered | pick_up | 0 | 1 |
| 34 | deliver_item(item_3,kitting_table_0) | covered | move_to | 1 | 1 |
| 65 | deliver_item(item_3,kitting_table_0) | covered | place | 0 | 1 |
| 67 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 94 | ac_activation(ac_switch_0) | covered | move_to | 0 | 2 |
| 133 | ac_activation(ac_switch_0) | covered | wait_at | 0 | 2 |
| 135 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 173 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 175 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 202 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 204 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 249 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 251 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 295 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 297 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 341 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 343 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 387 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 389 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 410; idle from 411 to 440. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 130 |
| ac_activation(ac_switch_0) | wait_at(PT2S,ac_switch_0) | 131 to 132 |
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | 135 to 440 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 440 |
| deliver_item(item_1) | move_to(item_1) | -1 to 31 |
| deliver_item(item_1) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_1) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_1) | move_to(item_1) | 65 to 172 |
| deliver_item(item_1) | place(item_2,shelf_2) | 173 to 175 |
| deliver_item(item_1) | move_to(shelf_2) | 176 to 201 |
| deliver_item(item_1) | move_to(item_1) | 202 to 246 |
| deliver_item(item_1) | pick_up(item_1) | 247 to 248 |
| deliver_item(item_1) | move_to(kitting_table_0) | 249 to 292 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 293 to 294 |
| deliver_item(item_2) | move_to(item_2) | -1 to 31 |
| deliver_item(item_2) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_2) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_2) | move_to(item_2) | 65 to 91 |
| deliver_item(item_2) | pick_up(item_2) | 92 to 94 |
| deliver_item(item_2) | move_to(item_2) | 95 to 170 |
| deliver_item(item_2) | pick_up(item_2) | 171 to 172 |
| deliver_item(item_2) | move_to(kitting_table_0) | 173 to 199 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 200 to 201 |
| deliver_item(item_3) | move_to(item_3) | -1 to 29 |
| deliver_item(item_3) | pick_up(item_3) | 30 to 31 |
| deliver_item(item_3) | move_to(kitting_table_0) | 32 to 62 |
| deliver_item(item_3) | place(item_3,kitting_table_0) | 63 to 64 |
| deliver_item(item_4) | move_to(item_4) | -1 to 31 |
| deliver_item(item_4) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_4) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_4) | move_to(item_4) | 65 to 172 |
| deliver_item(item_4) | place(item_2,shelf_2) | 173 to 175 |
| deliver_item(item_4) | move_to(shelf_2) | 176 to 201 |
| deliver_item(item_4) | move_to(item_4) | 202 to 248 |
| deliver_item(item_4) | place(item_1,shelf_1) | 249 to 250 |
| deliver_item(item_4) | move_to(shelf_1) | 251 to 294 |
| deliver_item(item_4) | move_to(item_4) | 295 to 338 |
| deliver_item(item_4) | pick_up(item_4) | 339 to 340 |
| deliver_item(item_4) | move_to(kitting_table_0) | 341 to 384 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 385 to 386 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 119 | finding turns unexplained |
| 131 | finding turns adequate (from unexplained) |
| 133 | boundary |
| 133 | pin ac_activation(ac_switch_0) |
| 135 | re-entry ac_activation(ac_switch_0) |
| 202 | boundary |
| 202 | pin deliver_item(item_2) |
| 295 | boundary |
| 295 | pin deliver_item(item_1) |
| 387 | boundary |
| 387 | pin deliver_item(item_4) |
| 411 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_NE), ticks 389 to 410): lifecycle and finding adequate; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 28 | 0.7518 | yes | adequate |
| deliver_item(item_2) | 67 to 93 | not reached | - | - | - |
| ac_activation(ac_switch_0) | 94 to 134 | not reached | - | - | - |
| deliver_item(item_2) | 135 to 203 | 155 | 0.7774 | yes | adequate |
| deliver_item(item_1) | 204 to 296 | 251 | 0.7646 | yes | adequate |
| deliver_item(item_4) | 297 to 388 | 342 | 0.7534 | yes | adequate |

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
| 104 | deliver_item(item_2) | move_to(item_2) | 0.1300 | 0.0405 | 356.0 | 356.0 | 0.0 | ac_activation(ac_switch_0) |
| 112 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.3250 | 0.0464 | 342.1 | 322.1 | 20.0 | ac_activation(ac_switch_0) |
| 119 | deliver_item(item_4) | move_to(item_4) | 0.5222 | 0.0484 | 337.8 | 317.8 | 20.0 | ac_activation(ac_switch_0) |
| 144 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0238 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 144 | deliver_item(item_1) | move_to(item_1) | 0.0280 | 0.0436 | 348.4 | 348.4 | 0.0 | deliver_item(item_2) |
| 148 | deliver_item(item_4) | move_to(item_4) | 0.0371 | 0.0463 | 342.2 | 342.2 | 0.0 | deliver_item(item_2) |
| 162 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0550 | 0.0428 | 350.3 | 350.3 | 0.0 | deliver_item(item_2) |
| 185 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0405 | 355.8 | 355.8 | 0.0 | deliver_item(item_2) |
| 185 | deliver_item(item_4) | move_to(shelf_2) | 0.0010 | 0.0405 | 355.8 | 355.8 | 0.0 | deliver_item(item_2) |
| 233 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0266 | 0.0495 | 335.5 | 335.5 | 0.0 | deliver_item(item_1) |
| 256 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0510 | 0.0402 | 356.7 | 296.7 | 60.0 | deliver_item(item_1) |
| 260 | deliver_item(item_4) | move_to(shelf_1) | 0.0041 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 338 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0363 | 0.0428 | 350.3 | 350.3 | 0.0 | deliver_item(item_4) |
| 348 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0537 | 0.0421 | 352.0 | 292.0 | 60.0 | deliver_item(item_4) |
| 402 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.1833 | 0.0480 | 338.6 | 338.6 | 0.0 | - |
| 411 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9060 | 0.0464 | 342.0 | 302.0 | 40.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_3) |
| 65 | adequate | unresolved | deliver_item(item_3) |
| 66 | unresolved | adequate | deliver_item(item_3) |
| 119 | adequate | unexplained | ac_activation(ac_switch_0) |
| 131 | unexplained | adequate | ac_activation(ac_switch_0) |
| 133 | adequate | unresolved | ac_activation(ac_switch_0) |
| 134 | unresolved | adequate | ac_activation(ac_switch_0) |
| 202 | adequate | unresolved | deliver_item(item_2) |
| 203 | unresolved | adequate | deliver_item(item_2) |
| 295 | adequate | unresolved | deliver_item(item_1) |
| 296 | unresolved | adequate | deliver_item(item_1) |
| 387 | adequate | unresolved | deliver_item(item_4) |
| 388 | unresolved | adequate | deliver_item(item_4) |
| 411 | adequate | unexplained | - |

Across the started task ac_activation(ac_switch_0) (covered; actual): on top of the stack from 94 to 134, its hypothesis pinned at 133; the suspended task resumes at 135.

| tick | human action | truth | ac_activation(ac_switch_0) belief / S | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | deliver_item(item_3) belief / S | deliver_item(item_4) belief / S | finding |
|---|---|---|---|---|---|---|---|---|---|
| 92 | move_to step | deliver_item(item_2) | 0.0268 / 0.0337 | 0.3215 / 0.4686 | 0.0107 / 0.0134 | 0.5796 / 1.0000 | retired | 0.0604 / 0.0772 | adequate |
| 93 | move_to  | deliver_item(item_2) | 0.0235 / 0.0277 | 0.2953 / 0.3942 | 0.0094 / 0.0110 | 0.6176 / 1.0000 | retired | 0.0532 / 0.0635 | adequate |
| 94 | move_to step | ac_activation(ac_switch_0) | 0.0237 / 0.0277 | 0.2877 / 0.3777 | 0.0095 / 0.0110 | 0.6245 / 1.0000 | retired | 0.0536 / 0.0633 | adequate |
| 95 | move_to step | ac_activation(ac_switch_0) | 0.0240 / 0.0277 | 0.2795 / 0.3605 | 0.0095 / 0.0109 | 0.6319 / - | retired | 0.0541 / 0.0631 | adequate |
| 96 | move_to step | ac_activation(ac_switch_0) | 0.0277 / 0.0277 | 0.3080 / 0.3426 | 0.0110 / 0.0109 | 0.5901 / 0.7491 | retired | 0.0622 / 0.0630 | adequate |
| 132 | move_to  | ac_activation(ac_switch_0) | 0.7454 / 1.0000 | 0.0025 / 0.0001 | 0.1125 / 0.0041 | 0.0010 / 0.0000 | retired | 0.1377 / 0.0051 | adequate |
| 133 | wait_at stand | ac_activation(ac_switch_0) | retired | 0.2495 / - | 0.2495 / - | 0.2495 / - | retired | 0.2495 / - | unresolved |
| 134 | wait_at  | ac_activation(ac_switch_0) | retired | 0.2495 / 1.0000 | 0.2495 / 1.0000 | 0.2495 / 1.0000 | retired | 0.2495 / 1.0000 | adequate |
| 135 | move_to step | deliver_item(item_2) | 0.1998 / - | 0.2070 / 0.9774 | 0.1788 / 0.7985 | 0.2103 / 1.0000 | retired | 0.2030 / 0.9505 | adequate |
| 136 | move_to step | deliver_item(item_2) | 0.1751 / 0.7401 | 0.2221 / 0.9534 | 0.1606 / 0.6209 | 0.2297 / 1.0000 | retired | 0.2115 / 0.8901 | adequate |
| 137 | move_to step | deliver_item(item_2) | 0.1486 / 0.5354 | 0.2394 / 0.9280 | 0.1406 / 0.4710 | 0.2523 / 1.0000 | retired | 0.2182 / 0.8169 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 64, 67 to 132, 204 to 294, 297 to 384 |
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 132, 135 to 180, 204 to 294, 297 to 386, 389 to 440 |
| deliver_item(item_1) | 0 to 31, 67 to 132, 204 to 294 |
| deliver_item(item_2) | 67 to 94, 135 to 201 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 132, 135 to 144, 204 to 248, 297 to 386 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 27 | deliver_item(item_3) | none(below_theta) |
| 28 to 64 | deliver_item(item_3) | clears |
| 65 to 66 | ac_activation(ac_switch_0) | none(below_theta) |
| 67 to 98 | deliver_item(item_2) | none(below_theta) |
| 99 to 111 | coffee_break(coffee_machine_0) | none(below_theta) |
| 112 to 125 | deliver_item(item_4) | none(below_theta) |
| 126 to 132 | ac_activation(ac_switch_0) | none(below_theta) |
| 133 to 134 | coffee_break(coffee_machine_0) | none(below_theta) |
| 135 to 154 | deliver_item(item_2) | none(below_theta) |
| 155 to 201 | deliver_item(item_2) | clears |
| 202 to 203 | ac_activation(ac_switch_0) | none(below_theta) |
| 204 to 250 | deliver_item(item_1) | none(below_theta) |
| 251 to 294 | deliver_item(item_1) | clears |
| 295 to 296 | ac_activation(ac_switch_0) | none(below_theta) |
| 297 to 341 | deliver_item(item_4) | none(below_theta) |
| 342 to 386 | deliver_item(item_4) | clears |
| 387 to 388 | ac_activation(ac_switch_0) | none(below_theta) |
| 389 to 398 | coffee_break(coffee_machine_0) | none(below_theta) |
| 399 to 410 | coffee_break(coffee_machine_0) | clears |
| 411 to 440 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_NE)): first step 389, last step 409, acknowledgement 410; the idle human from 411. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.4826 at 389; S < α from 402 (belief 0.1833; v·D 338.6 cm); the finding unexplained from 411.

- coffee_break(coffee_machine_0): belief 0.5134 at 389; S < α from 411 (belief 0.9060; v·D 342.0 cm); the finding unexplained from 411.

