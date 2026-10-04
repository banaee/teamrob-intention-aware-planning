### scenario_s14_05

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_0,kitting_table_0) | covered | move_to | 0 | 1 |
| 43 | deliver_item(item_0,kitting_table_0) | covered | pick_up | 0 | 1 |
| 45 | deliver_item(item_0,kitting_table_0) | covered | move_to | 1 | 1 |
| 87 | deliver_item(item_0,kitting_table_0) | covered | place | 0 | 1 |
| 89 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 133 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 135 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 146 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 177 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 225 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 227 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 276 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 278 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 327 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 329 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 351; idle from 352 to 381. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 381 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 143 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 144 to 177 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 178 to 381 |
| deliver_item(item_0) | move_to(item_0) | -1 to 40 |
| deliver_item(item_0) | pick_up(item_0) | 41 to 42 |
| deliver_item(item_0) | move_to(kitting_table_0) | 43 to 84 |
| deliver_item(item_0) | place(item_0,kitting_table_0) | 85 to 86 |
| deliver_item(item_1) | move_to(item_1) | -1 to 42 |
| deliver_item(item_1) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_1) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_1) | move_to(item_1) | 87 to 132 |
| deliver_item(item_1) | place(item_2,shelf_2) | 133 to 135 |
| deliver_item(item_1) | move_to(shelf_2) | 136 to 224 |
| deliver_item(item_1) | move_to(item_1) | 225 to 273 |
| deliver_item(item_1) | pick_up(item_1) | 274 to 275 |
| deliver_item(item_1) | move_to(kitting_table_0) | 276 to 324 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 325 to 326 |
| deliver_item(item_2) | move_to(item_2) | -1 to 42 |
| deliver_item(item_2) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_2) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_2) | move_to(item_2) | 87 to 130 |
| deliver_item(item_2) | pick_up(item_2) | 131 to 132 |
| deliver_item(item_2) | move_to(kitting_table_0) | 133 to 222 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 223 to 224 |

Events (actual):

| tick | event |
|---|---|
| 87 | boundary |
| 87 | pin deliver_item(item_0) |
| 175 | boundary |
| 175 | pin coffee_break(coffee_machine_0) |
| 177 | re-entry coffee_break(coffee_machine_0) |
| 225 | boundary |
| 225 | pin deliver_item(item_2) |
| 327 | boundary |
| 327 | pin deliver_item(item_1) |
| 341 | finding turns unexplained |

Never pinned: ac_activation(ac_switch_0). At the last entry (go_to(corner_NE), ticks 329 to 351): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_0) | 0 to 88 | 50 | 0.8052 | yes | adequate |
| deliver_item(item_2) | 89 to 134 | not reached | - | - | - |
| coffee_break(coffee_machine_0) | 135 to 176 | 150 | 0.7787 | yes | adequate |
| deliver_item(item_2) | 177 to 226 | 187 | 0.8026 | yes | adequate |
| deliver_item(item_1) | 227 to 328 | 278 | 0.7725 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 42 | deliver_item(item_2) | move_to(item_2) | 0.0254 | 0.0441 | 347.1 | 327.1 | 20.0 | deliver_item(item_0) |
| 47 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0375 | 0.0445 | 346.3 | 286.3 | 60.0 | deliver_item(item_0) |
| 49 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0504 | 0.0495 | 335.5 | 275.5 | 60.0 | deliver_item(item_0) |
| 54 | deliver_item(item_1) | move_to(shelf_0) | 0.0327 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 54 | deliver_item(item_2) | move_to(shelf_0) | 0.0025 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 146 | deliver_item(item_1) | move_to(shelf_2) | 0.0187 | 0.0418 | 352.6 | 312.6 | 40.0 | coffee_break(coffee_machine_0) |
| 147 | deliver_item(item_2) | move_to(kitting_table_0) | 0.1518 | 0.0459 | 343.2 | 283.2 | 60.0 | coffee_break(coffee_machine_0) |
| 148 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.1483 | 0.0421 | 352.0 | 212.0 | 140.0 | coffee_break(coffee_machine_0) |
| 187 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0429 | 0.0391 | 359.5 | 359.5 | 0.0 | deliver_item(item_2) |
| 187 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0407 | 0.0393 | 359.0 | 359.0 | 0.0 | deliver_item(item_2) |
| 190 | deliver_item(item_1) | move_to(shelf_2) | 0.0492 | 0.0391 | 359.4 | 359.4 | 0.0 | deliver_item(item_2) |
| 279 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0522 | 0.0477 | 339.3 | 279.3 | 60.0 | deliver_item(item_1) |
| 283 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0553 | 0.0441 | 347.3 | 287.3 | 60.0 | deliver_item(item_1) |
| 340 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.4459 | 0.0440 | 347.5 | 347.5 | 0.0 | - |
| 341 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.5554 | 0.0409 | 354.9 | 354.9 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_0) |
| 87 | adequate | unresolved | deliver_item(item_0) |
| 88 | unresolved | adequate | deliver_item(item_0) |
| 175 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 176 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 225 | adequate | unresolved | deliver_item(item_2) |
| 226 | unresolved | adequate | deliver_item(item_2) |
| 327 | adequate | unresolved | deliver_item(item_1) |
| 328 | unresolved | adequate | deliver_item(item_1) |
| 341 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 135 to 176, its hypothesis pinned at 175; the suspended task resumes at 177.

| tick | human action | truth | ac_activation(ac_switch_0) belief / S | coffee_break(coffee_machine_0) belief / S | deliver_item(item_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|---|---|
| 133 | pick_up grasp | deliver_item(item_2) | 0.2869 / 0.5058 | 0.1569 / 0.2545 | retired | 0.0700 / 1.0000 | 0.4851 / 1.0000 | adequate |
| 134 | pick_up  | deliver_item(item_2) | 0.2650 / 0.4263 | 0.1413 / 0.2116 | retired | 0.0748 / 1.0000 | 0.5179 / 1.0000 | adequate |
| 135 | move_to step | coffee_break(coffee_machine_0) | 0.2829 / 0.4224 | 0.1520 / 0.2116 | retired | 0.0805 / 1.0000 | 0.4836 / 0.8206 | adequate |
| 136 | move_to step | coffee_break(coffee_machine_0) | 0.3026 / 0.4168 | 0.1645 / 0.2116 | retired | 0.0870 / - | 0.4449 / 0.6642 | adequate |
| 137 | move_to step | coffee_break(coffee_machine_0) | 0.3285 / 0.4082 | 0.1818 / 0.2116 | retired | 0.0786 / 0.7581 | 0.4101 / 0.5305 | adequate |
| 174 | wait_at stand | coffee_break(coffee_machine_0) | 0.0012 / 0.0002 | 0.9957 / 1.0000 | retired | 0.0010 / 0.0002 | 0.0011 / 0.0002 | adequate |
| 175 | wait_at stand | coffee_break(coffee_machine_0) | 0.3327 / - | retired | retired | 0.3327 / - | 0.3327 / - | unresolved |
| 176 | wait_at  | coffee_break(coffee_machine_0) | 0.3327 / 1.0000 | retired | retired | 0.3327 / 1.0000 | 0.3327 / 1.0000 | adequate |
| 177 | move_to step | deliver_item(item_2) | 0.2379 / 0.8617 | 0.2498 / 1.0000 | retired | 0.2469 / 0.9075 | 0.2645 / 1.0000 | adequate |
| 178 | move_to step | deliver_item(item_2) | 0.2175 / 0.7132 | 0.2633 / - | retired | 0.2394 / 0.8091 | 0.2788 / 1.0000 | adequate |
| 179 | move_to step | deliver_item(item_2) | 0.2040 / 0.5673 | 0.2383 / 0.7424 | retired | 0.2430 / 0.7070 | 0.3137 / 1.0000 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 86, 89 to 174, 227 to 324 |
| coffee_break(coffee_machine_0) | 0 to 86, 89 to 174, 227 to 324 |
| deliver_item(item_0) | 0 to 86 |
| deliver_item(item_1) | 0 to 42, 89 to 132, 177 to 183, 227 to 326 |
| deliver_item(item_2) | 0 to 42, 89 to 174, 177 to 224 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 49 | deliver_item(item_0) | none(below_theta) |
| 50 to 86 | deliver_item(item_0) | clears |
| 87 to 88 | ac_activation(ac_switch_0) | none(below_theta) |
| 89 to 138 | deliver_item(item_2) | none(below_theta) |
| 139 to 141 | ac_activation(ac_switch_0) | none(below_theta) |
| 142 to 149 | coffee_break(coffee_machine_0) | none(below_theta) |
| 150 to 174 | coffee_break(coffee_machine_0) | clears |
| 175 to 176 | ac_activation(ac_switch_0) | none(below_theta) |
| 177 to 186 | deliver_item(item_2) | none(below_theta) |
| 187 to 224 | deliver_item(item_2) | clears |
| 225 to 226 | ac_activation(ac_switch_0) | none(below_theta) |
| 227 to 277 | deliver_item(item_1) | none(below_theta) |
| 278 to 326 | deliver_item(item_1) | clears |
| 327 to 381 | ac_activation(ac_switch_0) | none(below_theta) |

The last entry (go_to(corner_NE)): first step 329, last step 350, acknowledgement 351; the idle human from 352. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.5014 at 329; S < α from 341 (belief 0.5554; v·D 354.9 cm); the finding unexplained from 341.

- coffee_break(coffee_machine_0): belief 0.4956 at 329; S < α from 340 (belief 0.4459; v·D 347.5 cm); the finding unexplained from 341.

