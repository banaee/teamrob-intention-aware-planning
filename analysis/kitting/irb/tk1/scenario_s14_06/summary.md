### scenario_s14_06

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_0,kitting_table_0) | covered | move_to | 0 | 1 |
| 43 | deliver_item(item_0,kitting_table_0) | covered | pick_up | 0 | 1 |
| 45 | deliver_item(item_0,kitting_table_0) | covered | move_to | 1 | 1 |
| 87 | deliver_item(item_0,kitting_table_0) | covered | place | 0 | 1 |
| 89 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 133 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 135 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 179 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 227 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 258 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 306 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 308 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 357 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 359 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 408 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 410 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 432; idle from 433 to 462. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 462 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 224 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 225 to 255 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 258 to 462 |
| deliver_item(item_0) | move_to(item_0) | -1 to 40 |
| deliver_item(item_0) | pick_up(item_0) | 41 to 42 |
| deliver_item(item_0) | move_to(kitting_table_0) | 43 to 84 |
| deliver_item(item_0) | place(item_0,kitting_table_0) | 85 to 86 |
| deliver_item(item_1) | move_to(item_1) | -1 to 42 |
| deliver_item(item_1) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_1) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_1) | move_to(item_1) | 87 to 132 |
| deliver_item(item_1) | place(item_2,shelf_2) | 133 to 134 |
| deliver_item(item_1) | move_to(shelf_2) | 135 to 305 |
| deliver_item(item_1) | move_to(item_1) | 306 to 354 |
| deliver_item(item_1) | pick_up(item_1) | 355 to 356 |
| deliver_item(item_1) | move_to(kitting_table_0) | 357 to 405 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 406 to 407 |
| deliver_item(item_2) | move_to(item_2) | -1 to 42 |
| deliver_item(item_2) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_2) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_2) | move_to(item_2) | 87 to 130 |
| deliver_item(item_2) | pick_up(item_2) | 131 to 132 |
| deliver_item(item_2) | move_to(kitting_table_0) | 133 to 176 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 177 to 178 |
| deliver_item(item_2) | move_to(kitting_table_0) | 179 to 303 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 304 to 305 |

Events (actual):

| tick | event |
|---|---|
| 87 | boundary |
| 87 | pin deliver_item(item_0) |
| 179 | finding turns unexplained |
| 180 | finding turns adequate (from unexplained) |
| 188 | finding turns unexplained |
| 225 | finding turns adequate (from unexplained) |
| 256 | boundary |
| 256 | pin coffee_break(coffee_machine_0) |
| 258 | re-entry coffee_break(coffee_machine_0) |
| 306 | boundary |
| 306 | pin deliver_item(item_2) |
| 408 | boundary |
| 408 | pin deliver_item(item_1) |
| 422 | finding turns unexplained |

Never pinned: ac_activation(ac_switch_0). At the last entry (go_to(corner_NE), ticks 410 to 432): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_0) | 0 to 88 | 50 | 0.8052 | yes | adequate |
| deliver_item(item_2) | 89 to 178 | 138 | 0.7588 | yes | adequate |
| coffee_break(coffee_machine_0) | 179 to 257 | 231 | 0.7545 | yes | adequate |
| deliver_item(item_2) | 258 to 307 | 267 | 0.7576 | yes | adequate |
| deliver_item(item_1) | 308 to 409 | 359 | 0.7666 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 42 | deliver_item(item_2) | move_to(item_2) | 0.0254 | 0.0441 | 347.1 | 327.1 | 20.0 | deliver_item(item_0) |
| 47 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0375 | 0.0445 | 346.3 | 286.3 | 60.0 | deliver_item(item_0) |
| 49 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0504 | 0.0495 | 335.5 | 275.5 | 60.0 | deliver_item(item_0) |
| 54 | deliver_item(item_1) | move_to(shelf_0) | 0.0327 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 54 | deliver_item(item_2) | move_to(shelf_0) | 0.0025 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 140 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0424 | 0.0361 | 367.6 | 307.6 | 60.0 | deliver_item(item_2) |
| 141 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0486 | 0.0396 | 358.1 | 298.1 | 60.0 | deliver_item(item_2) |
| 144 | deliver_item(item_1) | move_to(shelf_2) | 0.0074 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 188 | deliver_item(item_2) | move_to(kitting_table_0) | 0.9960 | 0.0390 | 359.8 | 359.8 | 0.0 | coffee_break(coffee_machine_0) |
| 267 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0380 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 268 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0451 | 0.0406 | 355.6 | 355.6 | 0.0 | deliver_item(item_2) |
| 271 | deliver_item(item_1) | move_to(shelf_2) | 0.0499 | 0.0395 | 358.4 | 358.4 | 0.0 | deliver_item(item_2) |
| 360 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0538 | 0.0495 | 335.5 | 275.5 | 60.0 | deliver_item(item_1) |
| 364 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0559 | 0.0447 | 346.0 | 286.0 | 60.0 | deliver_item(item_1) |
| 421 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.4459 | 0.0446 | 346.1 | 346.1 | 0.0 | - |
| 422 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.5553 | 0.0415 | 353.4 | 353.4 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_0) |
| 87 | adequate | unresolved | deliver_item(item_0) |
| 88 | unresolved | adequate | deliver_item(item_0) |
| 179 | adequate | unexplained | coffee_break(coffee_machine_0) |
| 180 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 188 | adequate | unexplained | coffee_break(coffee_machine_0) |
| 225 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 256 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 257 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 306 | adequate | unresolved | deliver_item(item_2) |
| 307 | unresolved | adequate | deliver_item(item_2) |
| 408 | adequate | unresolved | deliver_item(item_1) |
| 409 | unresolved | adequate | deliver_item(item_1) |
| 422 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 179 to 257, its hypothesis pinned at 256; the suspended task resumes at 258.

| tick | human action | truth | ac_activation(ac_switch_0) belief / S | coffee_break(coffee_machine_0) belief / S | deliver_item(item_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|---|---|
| 177 | move_to step | deliver_item(item_2) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | 0.9960 / 1.0000 | adequate |
| 178 | move_to  | deliver_item(item_2) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | 0.9960 / 1.0000 | adequate |
| 179 | move_to step | coffee_break(coffee_machine_0) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | 0.9960 / - | unexplained |
| 180 | move_to step | coffee_break(coffee_machine_0) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | 0.9960 / 0.7405 | adequate |
| 181 | move_to step | coffee_break(coffee_machine_0) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | 0.9960 / 0.5358 | adequate |
| 255 | wait_at stand | coffee_break(coffee_machine_0) | 0.0010 / 0.0000 | 0.9953 / 1.0000 | retired | 0.0010 / 0.0000 | 0.0017 / 0.0000 | adequate |
| 256 | wait_at stand | coffee_break(coffee_machine_0) | 0.3327 / - | retired | retired | 0.3327 / - | 0.3327 / - | unresolved |
| 257 | wait_at  | coffee_break(coffee_machine_0) | 0.3327 / 1.0000 | retired | retired | 0.3327 / 1.0000 | 0.3327 / 1.0000 | adequate |
| 258 | move_to step | deliver_item(item_2) | 0.2376 / 0.8586 | 0.2497 / - | retired | 0.2467 / 0.9044 | 0.2649 / 1.0000 | adequate |
| 259 | move_to step | deliver_item(item_2) | 0.2293 / 0.7104 | 0.2231 / 0.7401 | retired | 0.2519 / 0.8039 | 0.2948 / 1.0000 | adequate |
| 260 | move_to step | deliver_item(item_2) | 0.2161 / 0.5667 | 0.1944 / 0.5354 | retired | 0.2559 / 0.7006 | 0.3326 / 1.0000 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 86, 89 to 176, 179 to 255, 308 to 405 |
| coffee_break(coffee_machine_0) | 0 to 86, 89 to 176, 179 to 255, 308 to 405 |
| deliver_item(item_0) | 0 to 86 |
| deliver_item(item_1) | 0 to 42, 89 to 132, 258 to 264, 308 to 407 |
| deliver_item(item_2) | 0 to 42, 89 to 178, 258 to 305 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 49 | deliver_item(item_0) | none(below_theta) |
| 50 to 86 | deliver_item(item_0) | clears |
| 87 to 88 | ac_activation(ac_switch_0) | none(below_theta) |
| 89 to 137 | deliver_item(item_2) | none(below_theta) |
| 138 to 178 | deliver_item(item_2) | clears |
| 179 to 179 | deliver_item(item_2) | none(leader_no_observation) |
| 180 to 187 | deliver_item(item_2) | none(leader_unwarranted) |
| 188 to 219 | deliver_item(item_2) | none(leader_inadequate) |
| 220 to 224 | deliver_item(item_2) | none(below_theta) |
| 225 to 230 | coffee_break(coffee_machine_0) | none(below_theta) |
| 231 to 255 | coffee_break(coffee_machine_0) | clears |
| 256 to 257 | ac_activation(ac_switch_0) | none(below_theta) |
| 258 to 266 | deliver_item(item_2) | none(below_theta) |
| 267 to 305 | deliver_item(item_2) | clears |
| 306 to 307 | ac_activation(ac_switch_0) | none(below_theta) |
| 308 to 358 | deliver_item(item_1) | none(below_theta) |
| 359 to 407 | deliver_item(item_1) | clears |
| 408 to 462 | ac_activation(ac_switch_0) | none(below_theta) |

The last entry (go_to(corner_NE)): first step 410, last step 431, acknowledgement 432; the idle human from 433. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.5013 at 410; S < α from 422 (belief 0.5553; v·D 353.4 cm); the finding unexplained from 422.

- coffee_break(coffee_machine_0): belief 0.4957 at 410; S < α from 421 (belief 0.4459; v·D 346.1 cm); the finding unexplained from 422.

