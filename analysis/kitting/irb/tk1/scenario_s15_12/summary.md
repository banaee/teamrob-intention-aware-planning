### scenario_s15_12

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_3,kitting_table_0) | covered | move_to | 0 | 1 |
| 32 | deliver_item(item_3,kitting_table_0) | covered | pick_up | 0 | 1 |
| 34 | deliver_item(item_3,kitting_table_0) | covered | move_to | 1 | 1 |
| 65 | deliver_item(item_3,kitting_table_0) | covered | place | 0 | 1 |
| 67 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 94 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 96 | ac_activation(ac_switch_0) | covered | move_to | 0 | 2 |
| 135 | ac_activation(ac_switch_0) | covered | switch_on | 0 | 2 |
| 137 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 183 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 185 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 230 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 232 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 277 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 279 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 324 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 326 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 371 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 373 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 394; idle from 395 to 424. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 132 |
| ac_activation(ac_switch_0) | switch_on(PT2S,ac_switch_0) | 133 to 137 |
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | 138 to 424 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 424 |
| deliver_item(item_1) | move_to(item_1) | -1 to 31 |
| deliver_item(item_1) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_1) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_1) | move_to(item_1) | 65 to 93 |
| deliver_item(item_1) | place(item_2,shelf_2) | 94 to 96 |
| deliver_item(item_1) | move_to(shelf_2) | 97 to 182 |
| deliver_item(item_1) | move_to(item_1) | 183 to 227 |
| deliver_item(item_1) | pick_up(item_1) | 228 to 229 |
| deliver_item(item_1) | move_to(kitting_table_0) | 230 to 274 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 275 to 276 |
| deliver_item(item_2) | move_to(item_2) | -1 to 31 |
| deliver_item(item_2) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_2) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_2) | move_to(item_2) | 65 to 91 |
| deliver_item(item_2) | pick_up(item_2) | 92 to 93 |
| deliver_item(item_2) | move_to(kitting_table_0) | 94 to 180 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 181 to 182 |
| deliver_item(item_3) | move_to(item_3) | -1 to 29 |
| deliver_item(item_3) | pick_up(item_3) | 30 to 31 |
| deliver_item(item_3) | move_to(kitting_table_0) | 32 to 62 |
| deliver_item(item_3) | place(item_3,kitting_table_0) | 63 to 64 |
| deliver_item(item_4) | move_to(item_4) | -1 to 31 |
| deliver_item(item_4) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_4) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_4) | move_to(item_4) | 65 to 93 |
| deliver_item(item_4) | place(item_2,shelf_2) | 94 to 96 |
| deliver_item(item_4) | move_to(shelf_2) | 97 to 182 |
| deliver_item(item_4) | move_to(item_4) | 183 to 229 |
| deliver_item(item_4) | place(item_1,shelf_1) | 230 to 231 |
| deliver_item(item_4) | move_to(shelf_1) | 232 to 276 |
| deliver_item(item_4) | move_to(item_4) | 277 to 321 |
| deliver_item(item_4) | pick_up(item_4) | 322 to 323 |
| deliver_item(item_4) | move_to(kitting_table_0) | 324 to 368 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 369 to 370 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 112 | finding turns unexplained |
| 133 | finding turns adequate (from unexplained) |
| 135 | boundary |
| 135 | pin ac_activation(ac_switch_0) |
| 137 | re-entry ac_activation(ac_switch_0) |
| 183 | boundary |
| 183 | pin deliver_item(item_2) |
| 277 | boundary |
| 277 | pin deliver_item(item_1) |
| 371 | boundary |
| 371 | pin deliver_item(item_4) |
| 395 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_NE), ticks 373 to 394): lifecycle and finding adequate; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 28 | 0.7518 | yes | adequate |
| deliver_item(item_2) | 67 to 95 | not reached | - | - | - |
| ac_activation(ac_switch_0) | 96 to 136 | 121 | 0.7689 | yes | inadequate |
| deliver_item(item_2) | 137 to 184 | 164 | 0.7588 | yes | adequate |
| deliver_item(item_1) | 185 to 278 | 231 | 0.7510 | yes | adequate |
| deliver_item(item_4) | 279 to 372 | 325 | 0.7728 | yes | adequate |

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
| 106 | deliver_item(item_1) | move_to(shelf_2) | 0.0021 | 0.0405 | 356.0 | 356.0 | 0.0 | ac_activation(ac_switch_0) |
| 106 | deliver_item(item_4) | move_to(shelf_2) | 0.0121 | 0.0405 | 356.0 | 356.0 | 0.0 | ac_activation(ac_switch_0) |
| 109 | deliver_item(item_2) | move_to(kitting_table_0) | 0.2937 | 0.0418 | 352.7 | 352.7 | 0.0 | ac_activation(ac_switch_0) |
| 112 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.5688 | 0.0480 | 338.7 | 278.7 | 60.0 | ac_activation(ac_switch_0) |
| 147 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0186 | 0.0390 | 359.7 | 359.7 | 0.0 | deliver_item(item_2) |
| 154 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0285 | 0.0427 | 350.4 | 350.4 | 0.0 | deliver_item(item_2) |
| 169 | deliver_item(item_1) | move_to(shelf_2) | 0.0550 | 0.0455 | 344.1 | 344.1 | 0.0 | deliver_item(item_2) |
| 169 | deliver_item(item_4) | move_to(shelf_2) | 0.0550 | 0.0455 | 344.1 | 344.1 | 0.0 | deliver_item(item_2) |
| 214 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0255 | 0.0468 | 341.2 | 341.2 | 0.0 | deliver_item(item_1) |
| 237 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0499 | 0.0391 | 359.3 | 299.3 | 60.0 | deliver_item(item_1) |
| 241 | deliver_item(item_4) | move_to(shelf_1) | 0.0036 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 320 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0379 | 0.0453 | 344.6 | 344.6 | 0.0 | deliver_item(item_4) |
| 331 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0517 | 0.0403 | 356.3 | 296.3 | 60.0 | deliver_item(item_4) |
| 386 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.1851 | 0.0499 | 334.7 | 334.7 | 0.0 | - |
| 395 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9052 | 0.0488 | 337.1 | 297.1 | 40.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_3) |
| 65 | adequate | unresolved | deliver_item(item_3) |
| 66 | unresolved | adequate | deliver_item(item_3) |
| 112 | adequate | unexplained | ac_activation(ac_switch_0) |
| 133 | unexplained | adequate | ac_activation(ac_switch_0) |
| 135 | adequate | unresolved | ac_activation(ac_switch_0) |
| 136 | unresolved | adequate | ac_activation(ac_switch_0) |
| 183 | adequate | unresolved | deliver_item(item_2) |
| 184 | unresolved | adequate | deliver_item(item_2) |
| 277 | adequate | unresolved | deliver_item(item_1) |
| 278 | unresolved | adequate | deliver_item(item_1) |
| 371 | adequate | unresolved | deliver_item(item_4) |
| 372 | unresolved | adequate | deliver_item(item_4) |
| 395 | adequate | unexplained | - |

Across the started task ac_activation(ac_switch_0) (covered; actual): on top of the stack from 96 to 136, its hypothesis pinned at 135; the suspended task resumes at 137.

| tick | human action | truth | ac_activation(ac_switch_0) belief / S | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | deliver_item(item_3) belief / S | deliver_item(item_4) belief / S | finding |
|---|---|---|---|---|---|---|---|---|---|
| 94 | pick_up grasp | deliver_item(item_2) | 0.0204 / 0.0227 | 0.2683 / 0.3303 | 0.0082 / 1.0000 | 0.6555 / 1.0000 | retired | 0.0466 / 1.0000 | adequate |
| 95 | pick_up  | deliver_item(item_2) | 0.0176 / 0.0186 | 0.2386 / 0.2757 | 0.0085 / 1.0000 | 0.6856 / 1.0000 | retired | 0.0487 / 1.0000 | adequate |
| 96 | move_to step | ac_activation(ac_switch_0) | 0.0191 / 0.0186 | 0.2489 / 0.2638 | 0.0093 / 1.0000 | 0.6688 / 0.8596 | retired | 0.0529 / 1.0000 | adequate |
| 97 | move_to step | ac_activation(ac_switch_0) | 0.0209 / 0.0186 | 0.2612 / 0.2513 | 0.0102 / - | 0.6486 / 0.7297 | retired | 0.0580 / - | adequate |
| 98 | move_to step | ac_activation(ac_switch_0) | 0.0235 / 0.0186 | 0.2795 / 0.2384 | 0.0093 / 0.7491 | 0.6340 / 0.6116 | retired | 0.0528 / 0.7491 | adequate |
| 134 | move_to  | ac_activation(ac_switch_0) | 0.9927 / 1.0000 | 0.0033 / 0.0001 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | adequate |
| 135 | switch_on stand | ac_activation(ac_switch_0) | retired | 0.2495 / - | 0.2495 / - | 0.2495 / - | retired | 0.2495 / - | unresolved |
| 136 | switch_on  | ac_activation(ac_switch_0) | retired | 0.2495 / 1.0000 | 0.2495 / 1.0000 | 0.2495 / 1.0000 | retired | 0.2495 / 1.0000 | adequate |
| 137 | move_to step | deliver_item(item_2) | 0.1998 / 1.0000 | 0.1920 / 0.9111 | 0.2011 / 0.9726 | 0.2050 / 1.0000 | retired | 0.2011 / 0.9726 | adequate |
| 138 | move_to step | deliver_item(item_2) | 0.2043 / - | 0.1823 / 0.8235 | 0.2014 / 0.9445 | 0.2096 / 1.0000 | retired | 0.2014 / 0.9445 | adequate |
| 139 | move_to step | deliver_item(item_2) | 0.1752 / 0.7407 | 0.1793 / 0.7381 | 0.2103 / 0.9155 | 0.2238 / 1.0000 | retired | 0.2103 / 0.9155 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 64, 67 to 134, 185 to 274, 279 to 368 |
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 134, 137 to 155, 185 to 274, 279 to 370, 373 to 424 |
| deliver_item(item_1) | 0 to 31, 67 to 93, 137 to 182, 185 to 276 |
| deliver_item(item_2) | 67 to 134, 137 to 182 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 93, 137 to 182, 185 to 229, 279 to 370 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 27 | deliver_item(item_3) | none(below_theta) |
| 28 to 64 | deliver_item(item_3) | clears |
| 65 to 66 | ac_activation(ac_switch_0) | none(below_theta) |
| 67 to 104 | deliver_item(item_2) | none(below_theta) |
| 105 to 116 | coffee_break(coffee_machine_0) | none(below_theta) |
| 117 to 120 | ac_activation(ac_switch_0) | none(below_theta) |
| 121 to 132 | ac_activation(ac_switch_0) | none(leader_inadequate) |
| 133 to 134 | ac_activation(ac_switch_0) | clears |
| 135 to 136 | coffee_break(coffee_machine_0) | none(below_theta) |
| 137 to 163 | deliver_item(item_2) | none(below_theta) |
| 164 to 182 | deliver_item(item_2) | clears |
| 183 to 184 | ac_activation(ac_switch_0) | none(below_theta) |
| 185 to 230 | deliver_item(item_1) | none(below_theta) |
| 231 to 276 | deliver_item(item_1) | clears |
| 277 to 278 | ac_activation(ac_switch_0) | none(below_theta) |
| 279 to 324 | deliver_item(item_4) | none(below_theta) |
| 325 to 370 | deliver_item(item_4) | clears |
| 371 to 372 | ac_activation(ac_switch_0) | none(below_theta) |
| 373 to 382 | coffee_break(coffee_machine_0) | none(below_theta) |
| 383 to 394 | coffee_break(coffee_machine_0) | clears |
| 395 to 424 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_NE)): first step 373, last step 393, acknowledgement 394; the idle human from 395. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.4828 at 373; S < α from 386 (belief 0.1851; v·D 334.7 cm); the finding unexplained from 395.

- coffee_break(coffee_machine_0): belief 0.5132 at 373; S < α from 395 (belief 0.9052; v·D 337.1 cm); the finding unexplained from 395.

