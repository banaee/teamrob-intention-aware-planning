### scenario_s14_03

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
| 179 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 181 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 229 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 260 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 266 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 268 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 317 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 319 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 341; idle from 342 to 371. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 371 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 226 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 227 to 260 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 261 to 371 |
| deliver_item(item_0) | move_to(item_0) | -1 to 40 |
| deliver_item(item_0) | pick_up(item_0) | 41 to 42 |
| deliver_item(item_0) | move_to(kitting_table_0) | 43 to 84 |
| deliver_item(item_0) | place(item_0,kitting_table_0) | 85 to 86 |
| deliver_item(item_1) | move_to(item_1) | -1 to 42 |
| deliver_item(item_1) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_1) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_1) | move_to(item_1) | 87 to 132 |
| deliver_item(item_1) | place(item_2,shelf_2) | 133 to 134 |
| deliver_item(item_1) | move_to(shelf_2) | 135 to 178 |
| deliver_item(item_1) | move_to(item_1) | 179 to 263 |
| deliver_item(item_1) | pick_up(item_1) | 264 to 265 |
| deliver_item(item_1) | move_to(kitting_table_0) | 266 to 314 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 315 to 316 |
| deliver_item(item_2) | move_to(item_2) | -1 to 42 |
| deliver_item(item_2) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_2) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_2) | move_to(item_2) | 87 to 130 |
| deliver_item(item_2) | pick_up(item_2) | 131 to 132 |
| deliver_item(item_2) | move_to(kitting_table_0) | 133 to 176 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 177 to 178 |

Events (actual):

| tick | event |
|---|---|
| 87 | boundary |
| 87 | pin deliver_item(item_0) |
| 179 | boundary |
| 179 | pin deliver_item(item_2) |
| 258 | boundary |
| 258 | pin coffee_break(coffee_machine_0) |
| 260 | re-entry coffee_break(coffee_machine_0) |
| 317 | boundary |
| 317 | pin deliver_item(item_1) |
| 331 | finding turns unexplained |

Never pinned: ac_activation(ac_switch_0). At the last entry (go_to(corner_NE), ticks 319 to 341): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_0) | 0 to 88 | 50 | 0.8052 | yes | adequate |
| deliver_item(item_2) | 89 to 180 | 138 | 0.7580 | yes | adequate |
| coffee_break(coffee_machine_0) | 181 to 259 | 235 | 0.7727 | yes | adequate |
| deliver_item(item_1) | 260 to 318 | 269 | 0.7775 | yes | adequate |

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
| 239 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0558 | 0.0466 | 341.6 | 101.6 | 240.0 | coffee_break(coffee_machine_0) |
| 240 | deliver_item(item_1) | move_to(item_1) | 0.0539 | 0.0440 | 347.4 | 87.4 | 260.0 | coffee_break(coffee_machine_0) |
| 271 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0570 | 0.0494 | 335.7 | 275.7 | 60.0 | deliver_item(item_1) |
| 273 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0540 | 0.0484 | 337.7 | 277.7 | 60.0 | deliver_item(item_1) |
| 330 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.4459 | 0.0432 | 349.4 | 349.4 | 0.0 | - |
| 331 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.5554 | 0.0401 | 357.0 | 357.0 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_0) |
| 87 | adequate | unresolved | deliver_item(item_0) |
| 88 | unresolved | adequate | deliver_item(item_0) |
| 179 | adequate | unresolved | deliver_item(item_2) |
| 180 | unresolved | adequate | deliver_item(item_2) |
| 258 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 259 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 317 | adequate | unresolved | deliver_item(item_1) |
| 318 | unresolved | adequate | deliver_item(item_1) |
| 331 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 86, 89 to 176, 181 to 257 |
| coffee_break(coffee_machine_0) | 0 to 86, 89 to 176, 181 to 257 |
| deliver_item(item_0) | 0 to 86 |
| deliver_item(item_1) | 0 to 42, 89 to 132, 181 to 257, 260 to 316 |
| deliver_item(item_2) | 0 to 42, 89 to 178 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 49 | deliver_item(item_0) | none(below_theta) |
| 50 to 86 | deliver_item(item_0) | clears |
| 87 to 88 | ac_activation(ac_switch_0) | none(below_theta) |
| 89 to 137 | deliver_item(item_2) | none(below_theta) |
| 138 to 178 | deliver_item(item_2) | clears |
| 179 to 180 | ac_activation(ac_switch_0) | none(below_theta) |
| 181 to 234 | coffee_break(coffee_machine_0) | none(below_theta) |
| 235 to 257 | coffee_break(coffee_machine_0) | clears |
| 258 to 259 | ac_activation(ac_switch_0) | none(below_theta) |
| 260 to 268 | deliver_item(item_1) | none(below_theta) |
| 269 to 316 | deliver_item(item_1) | clears |
| 317 to 371 | ac_activation(ac_switch_0) | none(below_theta) |

The last entry (go_to(corner_NE)): first step 319, last step 340, acknowledgement 341; the idle human from 342. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.5014 at 319; S < α from 331 (belief 0.5554; v·D 357.0 cm); the finding unexplained from 331.

- coffee_break(coffee_machine_0): belief 0.4956 at 319; S < α from 330 (belief 0.4459; v·D 349.4 cm); the finding unexplained from 331.

