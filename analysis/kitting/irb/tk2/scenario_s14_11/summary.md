### scenario_s14_11

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
| 179 | ac_activation(ac_switch_0) | covered | move_to | 0 | 2 |
| 226 | ac_activation(ac_switch_0) | covered | switch_on | 0 | 2 |
| 228 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 275 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 277 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 326 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 328 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 377 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 379 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 401; idle from 402 to 431. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 223 |
| ac_activation(ac_switch_0) | switch_on(PT2S,ac_switch_0) | 224 to 225 |
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | 228 to 431 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 431 |
| deliver_item(item_0) | move_to(item_0) | -1 to 40 |
| deliver_item(item_0) | pick_up(item_0) | 41 to 42 |
| deliver_item(item_0) | move_to(kitting_table_0) | 43 to 84 |
| deliver_item(item_0) | place(item_0,kitting_table_0) | 85 to 86 |
| deliver_item(item_1) | move_to(item_1) | -1 to 42 |
| deliver_item(item_1) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_1) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_1) | move_to(item_1) | 87 to 132 |
| deliver_item(item_1) | place(item_2,shelf_2) | 133 to 134 |
| deliver_item(item_1) | move_to(shelf_2) | 135 to 274 |
| deliver_item(item_1) | move_to(item_1) | 275 to 323 |
| deliver_item(item_1) | pick_up(item_1) | 324 to 325 |
| deliver_item(item_1) | move_to(kitting_table_0) | 326 to 374 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 375 to 376 |
| deliver_item(item_2) | move_to(item_2) | -1 to 42 |
| deliver_item(item_2) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_2) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_2) | move_to(item_2) | 87 to 130 |
| deliver_item(item_2) | pick_up(item_2) | 131 to 132 |
| deliver_item(item_2) | move_to(kitting_table_0) | 133 to 176 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 177 to 178 |
| deliver_item(item_2) | move_to(kitting_table_0) | 179 to 272 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 273 to 274 |

Events (actual):

| tick | event |
|---|---|
| 87 | boundary |
| 87 | pin deliver_item(item_0) |
| 179 | finding turns unexplained |
| 180 | finding turns adequate (from unexplained) |
| 188 | finding turns unexplained |
| 224 | finding turns adequate (from unexplained) |
| 226 | boundary |
| 226 | pin ac_activation(ac_switch_0) |
| 228 | re-entry ac_activation(ac_switch_0) |
| 275 | boundary |
| 275 | pin deliver_item(item_2) |
| 377 | boundary |
| 377 | pin deliver_item(item_1) |
| 391 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_NE), ticks 379 to 401): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_0) | 0 to 88 | 48 | 0.7504 | yes | adequate |
| deliver_item(item_2) | 89 to 178 | 129 | 0.7534 | yes | adequate |
| ac_activation(ac_switch_0) | 179 to 227 | not reached | - | - | - |
| deliver_item(item_2) | 228 to 276 | 234 | 0.7693 | yes | adequate |
| deliver_item(item_1) | 277 to 378 | 277 | 0.9756 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 42 | deliver_item(item_2) | move_to(item_2) | 0.0328 | 0.0441 | 347.1 | 327.1 | 20.0 | deliver_item(item_0) |
| 47 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0025 | 0.0445 | 346.3 | 286.3 | 60.0 | deliver_item(item_0) |
| 49 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0033 | 0.0495 | 335.5 | 275.5 | 60.0 | deliver_item(item_0) |
| 54 | deliver_item(item_1) | move_to(shelf_0) | 0.0333 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 54 | deliver_item(item_2) | move_to(shelf_0) | 0.0025 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 140 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0019 | 0.0361 | 367.6 | 307.6 | 60.0 | deliver_item(item_2) |
| 141 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0021 | 0.0396 | 358.1 | 298.1 | 60.0 | deliver_item(item_2) |
| 144 | deliver_item(item_1) | move_to(shelf_2) | 0.0076 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 188 | deliver_item(item_2) | move_to(kitting_table_0) | 0.9960 | 0.0389 | 360.0 | 360.0 | 0.0 | ac_activation(ac_switch_0) |
| 237 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 237 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0023 | 0.0463 | 342.3 | 342.3 | 0.0 | deliver_item(item_2) |
| 239 | deliver_item(item_1) | move_to(shelf_2) | 0.0500 | 0.0386 | 360.8 | 360.8 | 0.0 | deliver_item(item_2) |
| 329 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0493 | 335.9 | 275.9 | 60.0 | deliver_item(item_1) |
| 333 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0012 | 0.0446 | 346.2 | 286.2 | 60.0 | deliver_item(item_1) |
| 390 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.7617 | 0.0446 | 346.1 | 346.1 | 0.0 | - |
| 391 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.2384 | 0.0415 | 353.4 | 353.4 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_0) |
| 87 | adequate | unresolved | deliver_item(item_0) |
| 88 | unresolved | adequate | deliver_item(item_0) |
| 179 | adequate | unexplained | ac_activation(ac_switch_0) |
| 180 | unexplained | adequate | ac_activation(ac_switch_0) |
| 188 | adequate | unexplained | ac_activation(ac_switch_0) |
| 224 | unexplained | adequate | ac_activation(ac_switch_0) |
| 226 | adequate | unresolved | ac_activation(ac_switch_0) |
| 227 | unresolved | adequate | ac_activation(ac_switch_0) |
| 275 | adequate | unresolved | deliver_item(item_2) |
| 276 | unresolved | adequate | deliver_item(item_2) |
| 377 | adequate | unresolved | deliver_item(item_1) |
| 378 | unresolved | adequate | deliver_item(item_1) |
| 391 | adequate | unexplained | - |

Across the started task ac_activation(ac_switch_0) (covered; actual): on top of the stack from 179 to 227, its hypothesis pinned at 226; the suspended task resumes at 228.

| tick | human action | truth | ac_activation(ac_switch_0) belief / S | coffee_break(coffee_machine_0) belief / S | deliver_item(item_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|---|---|
| 177 | move_to step | deliver_item(item_2) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | 0.9960 / 1.0000 | adequate |
| 178 | move_to  | deliver_item(item_2) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | 0.9960 / 1.0000 | adequate |
| 179 | move_to step | ac_activation(ac_switch_0) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | 0.9960 / - | unexplained |
| 180 | move_to step | ac_activation(ac_switch_0) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | 0.9960 / 0.7402 | adequate |
| 181 | move_to step | ac_activation(ac_switch_0) | 0.0010 / 0.0000 | 0.0010 / 0.0000 | retired | 0.0010 / 0.0000 | 0.9960 / 0.5355 | adequate |
| 225 | move_to  | ac_activation(ac_switch_0) | 0.5187 / 1.0000 | 0.0080 / 0.0000 | retired | 0.0434 / 0.0000 | 0.4289 / 0.0000 | adequate |
| 226 | switch_on stand | ac_activation(ac_switch_0) | retired | 0.0196 / - | retired | 0.4892 / - | 0.4892 / - | unresolved |
| 227 | switch_on  | ac_activation(ac_switch_0) | retired | 0.0196 / 1.0000 | retired | 0.4892 / 1.0000 | 0.4892 / 1.0000 | adequate |
| 228 | move_to step | deliver_item(item_2) | 0.0047 / - | 0.0176 / 0.8218 | retired | 0.4701 / 0.8998 | 0.5065 / 1.0000 | adequate |
| 229 | move_to step | deliver_item(item_2) | 0.0040 / 0.7401 | 0.0155 / 0.6523 | retired | 0.4465 / 0.7830 | 0.5330 / 1.0000 | adequate |
| 230 | move_to step | deliver_item(item_2) | 0.0033 / 0.5354 | 0.0133 / 0.5016 | retired | 0.4147 / 0.6558 | 0.5677 / 1.0000 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 86, 89 to 176, 179 to 225, 277 to 374 |
| coffee_break(coffee_machine_0) | 0 to 86, 89 to 176, 179 to 225, 277 to 374 |
| deliver_item(item_0) | 0 to 86 |
| deliver_item(item_1) | 0 to 42, 89 to 132, 228 to 230, 277 to 376 |
| deliver_item(item_2) | 0 to 42, 89 to 178, 228 to 274 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 47 | deliver_item(item_0) | none(below_theta) |
| 48 to 86 | deliver_item(item_0) | clears |
| 87 to 88 | deliver_item(item_1) | none(below_theta) |
| 89 to 128 | deliver_item(item_2) | none(below_theta) |
| 129 to 178 | deliver_item(item_2) | clears |
| 179 to 179 | deliver_item(item_2) | none(leader_no_observation) |
| 180 to 187 | deliver_item(item_2) | clears |
| 188 to 220 | deliver_item(item_2) | none(leader_inadequate) |
| 221 to 224 | deliver_item(item_2) | none(below_theta) |
| 225 to 225 | ac_activation(ac_switch_0) | none(below_theta) |
| 226 to 227 | deliver_item(item_1) | none(below_theta) |
| 228 to 233 | deliver_item(item_2) | none(below_theta) |
| 234 to 274 | deliver_item(item_2) | clears |
| 275 to 275 | deliver_item(item_1) | none(leader_no_observation) |
| 276 to 376 | deliver_item(item_1) | clears |
| 377 to 377 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 378 to 389 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 390 to 394 | coffee_break(coffee_machine_0) | none(leader_inadequate) |
| 395 to 431 | coffee_break(coffee_machine_0) | none(below_theta) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of ac_activation | 0 to 149 ordinary, 150 to 225 raised, 226 to 227 retired, 228 to 431 suppressed |
| level of coffee_break | 0 to 431 ordinary |
| recency facts | 0 to 431 none |

The last entry (go_to(corner_NE)): first step 379, last step 400, acknowledgement 401; the idle human from 402. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.2012 at 379; S < α from 391 (belief 0.2384; v·D 353.4 cm); the finding unexplained from 391.

- coffee_break(coffee_machine_0): belief 0.7958 at 379; S < α from 390 (belief 0.7617; v·D 346.1 cm); the finding unexplained from 391.

