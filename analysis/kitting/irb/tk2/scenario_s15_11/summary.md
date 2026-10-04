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
| 133 | ac_activation(ac_switch_0) | covered | switch_on | 0 | 2 |
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
| ac_activation(ac_switch_0) | switch_on(PT2S,ac_switch_0) | 131 to 132 |
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
| deliver_item(item_3) | 0 to 66 | 26 | 0.7569 | yes | adequate |
| deliver_item(item_2) | 67 to 93 | 87 | 0.7557 | yes | adequate |
| ac_activation(ac_switch_0) | 94 to 134 | not reached | - | - | - |
| deliver_item(item_2) | 135 to 203 | 145 | 0.7921 | yes | adequate |
| deliver_item(item_1) | 204 to 296 | 241 | 0.7626 | yes | adequate |
| deliver_item(item_4) | 297 to 388 | 297 | 0.9758 | yes | adequate |

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
| 104 | deliver_item(item_2) | move_to(item_2) | 0.3272 | 0.0405 | 356.0 | 356.0 | 0.0 | ac_activation(ac_switch_0) |
| 112 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0382 | 0.0464 | 342.1 | 322.1 | 20.0 | ac_activation(ac_switch_0) |
| 119 | deliver_item(item_4) | move_to(item_4) | 0.8089 | 0.0484 | 337.8 | 317.8 | 20.0 | ac_activation(ac_switch_0) |
| 144 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 144 | deliver_item(item_1) | move_to(item_1) | 0.0441 | 0.0436 | 348.4 | 348.4 | 0.0 | deliver_item(item_2) |
| 148 | deliver_item(item_4) | move_to(item_4) | 0.0567 | 0.0463 | 342.2 | 342.2 | 0.0 | deliver_item(item_2) |
| 162 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0035 | 0.0428 | 350.3 | 350.3 | 0.0 | deliver_item(item_2) |
| 185 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0405 | 355.8 | 355.8 | 0.0 | deliver_item(item_2) |
| 185 | deliver_item(item_4) | move_to(shelf_2) | 0.0010 | 0.0405 | 355.8 | 355.8 | 0.0 | deliver_item(item_2) |
| 233 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0017 | 0.0495 | 335.5 | 335.5 | 0.0 | deliver_item(item_1) |
| 256 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0402 | 356.7 | 296.7 | 60.0 | deliver_item(item_1) |
| 260 | deliver_item(item_4) | move_to(shelf_1) | 0.0041 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 338 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0012 | 0.0428 | 350.3 | 350.3 | 0.0 | deliver_item(item_4) |
| 348 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0421 | 352.0 | 292.0 | 60.0 | deliver_item(item_4) |
| 402 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0532 | 0.0480 | 338.6 | 338.6 | 0.0 | - |
| 411 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9719 | 0.0464 | 342.0 | 302.0 | 40.0 | - |

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
| 92 | move_to step | deliver_item(item_2) | 0.0024 / 0.0337 | 0.0287 / 0.4686 | 0.0160 / 0.0134 | 0.8621 / 1.0000 | retired | 0.0898 / 0.0772 | adequate |
| 93 | move_to  | deliver_item(item_2) | 0.0020 / 0.0277 | 0.0253 / 0.3942 | 0.0134 / 0.0110 | 0.8823 / 1.0000 | retired | 0.0760 / 0.0635 | adequate |
| 94 | move_to step | ac_activation(ac_switch_0) | 0.0020 / 0.0277 | 0.0244 / 0.3777 | 0.0134 / 0.0110 | 0.8833 / 1.0000 | retired | 0.0759 / 0.0633 | adequate |
| 95 | move_to step | ac_activation(ac_switch_0) | 0.0020 / 0.0277 | 0.0235 / 0.3605 | 0.0134 / 0.0109 | 0.8844 / - | retired | 0.0757 / 0.0631 | adequate |
| 96 | move_to step | ac_activation(ac_switch_0) | 0.0024 / 0.0277 | 0.0270 / 0.3426 | 0.0160 / 0.0109 | 0.8626 / 0.7491 | retired | 0.0909 / 0.0630 | adequate |
| 132 | move_to  | ac_activation(ac_switch_0) | 0.1512 / 1.0000 | 0.0010 / 0.0001 | 0.3803 / 0.0041 | 0.0010 / 0.0000 | retired | 0.4655 / 0.0051 | adequate |
| 133 | switch_on stand | ac_activation(ac_switch_0) | retired | 0.0196 / - | 0.3261 / - | 0.3261 / - | retired | 0.3261 / - | unresolved |
| 134 | switch_on  | ac_activation(ac_switch_0) | retired | 0.0196 / 1.0000 | 0.3261 / 1.0000 | 0.3261 / 1.0000 | retired | 0.3261 / 1.0000 | adequate |
| 135 | move_to step | deliver_item(item_2) | 0.0049 / - | 0.0204 / 0.9774 | 0.2940 / 0.7985 | 0.3458 / 1.0000 | retired | 0.3338 / 0.9505 | adequate |
| 136 | move_to step | deliver_item(item_2) | 0.0042 / 0.7401 | 0.0216 / 0.9534 | 0.2598 / 0.6209 | 0.3714 / 1.0000 | retired | 0.3420 / 0.8901 | adequate |
| 137 | move_to step | deliver_item(item_2) | 0.0035 / 0.5354 | 0.0229 / 0.9280 | 0.2237 / 0.4710 | 0.4016 / 1.0000 | retired | 0.3473 / 0.8169 | adequate |

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
| 0 to 25 | deliver_item(item_3) | none(below_theta) |
| 26 to 64 | deliver_item(item_3) | clears |
| 65 to 66 | deliver_item(item_1) | none(below_theta) |
| 67 to 86 | deliver_item(item_2) | none(below_theta) |
| 87 to 94 | deliver_item(item_2) | clears |
| 95 to 95 | deliver_item(item_2) | none(leader_no_observation) |
| 96 to 98 | deliver_item(item_2) | clears |
| 99 to 102 | deliver_item(item_2) | none(below_theta) |
| 103 to 110 | deliver_item(item_4) | none(below_theta) |
| 111 to 118 | deliver_item(item_4) | clears |
| 119 to 125 | deliver_item(item_4) | none(leader_inadequate) |
| 126 to 132 | deliver_item(item_4) | none(below_theta) |
| 133 to 134 | deliver_item(item_1) | none(below_theta) |
| 135 to 144 | deliver_item(item_2) | none(below_theta) |
| 145 to 201 | deliver_item(item_2) | clears |
| 202 to 240 | deliver_item(item_1) | none(below_theta) |
| 241 to 294 | deliver_item(item_1) | clears |
| 295 to 295 | deliver_item(item_4) | none(leader_no_observation) |
| 296 to 386 | deliver_item(item_4) | clears |
| 387 to 387 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 388 to 388 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 389 to 410 | coffee_break(coffee_machine_0) | clears |
| 411 to 440 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of ac_activation | 0 to 132 ordinary, 133 to 134 retired, 135 to 440 suppressed |
| level of coffee_break | 0 to 440 ordinary |
| recency facts | 0 to 440 none |

The last entry (go_to(corner_NE)): first step 389, last step 409, acknowledgement 410; the idle human from 411. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.1895 at 389; S < α from 402 (belief 0.0532; v·D 338.6 cm); the finding unexplained from 411.

- coffee_break(coffee_machine_0): belief 0.8065 at 389; S < α from 411 (belief 0.9719; v·D 342.0 cm); the finding unexplained from 411.

