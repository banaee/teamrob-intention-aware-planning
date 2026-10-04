### scenario_s14_02

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_0,kitting_table_0) | covered | move_to | 0 | 1 |
| 43 | deliver_item(item_0,kitting_table_0) | covered | pick_up | 0 | 1 |
| 45 | deliver_item(item_0,kitting_table_0) | covered | move_to | 1 | 1 |
| 87 | deliver_item(item_0,kitting_table_0) | covered | place | 0 | 1 |
| 89 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 136 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 167 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 177 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 179 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 224 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 226 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 274 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 276 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 324 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 326 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 348; idle from 349 to 378. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 378 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 133 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 134 to 164 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 167 to 378 |
| deliver_item(item_0) | move_to(item_0) | -1 to 40 |
| deliver_item(item_0) | pick_up(item_0) | 41 to 42 |
| deliver_item(item_0) | move_to(kitting_table_0) | 43 to 84 |
| deliver_item(item_0) | place(item_0,kitting_table_0) | 85 to 86 |
| deliver_item(item_1) | move_to(item_1) | -1 to 42 |
| deliver_item(item_1) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_1) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_1) | move_to(item_1) | 87 to 176 |
| deliver_item(item_1) | place(item_2,shelf_2) | 177 to 179 |
| deliver_item(item_1) | move_to(shelf_2) | 180 to 223 |
| deliver_item(item_1) | move_to(item_1) | 224 to 271 |
| deliver_item(item_1) | pick_up(item_1) | 272 to 273 |
| deliver_item(item_1) | move_to(kitting_table_0) | 274 to 321 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 322 to 323 |
| deliver_item(item_2) | move_to(item_2) | -1 to 42 |
| deliver_item(item_2) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_2) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_2) | move_to(item_2) | 87 to 174 |
| deliver_item(item_2) | pick_up(item_2) | 175 to 176 |
| deliver_item(item_2) | move_to(kitting_table_0) | 177 to 221 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 222 to 223 |

Events (actual):

| tick | event |
|---|---|
| 87 | boundary |
| 87 | pin deliver_item(item_0) |
| 165 | boundary |
| 165 | pin coffee_break(coffee_machine_0) |
| 167 | re-entry coffee_break(coffee_machine_0) |
| 224 | boundary |
| 224 | pin deliver_item(item_2) |
| 324 | boundary |
| 324 | pin deliver_item(item_1) |
| 338 | finding turns unexplained |

Never pinned: ac_activation(ac_switch_0). At the last entry (go_to(corner_NE), ticks 326 to 348): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_0) | 0 to 88 | 48 | 0.7504 | yes | adequate |
| coffee_break(coffee_machine_0) | 89 to 166 | 157 | 0.7725 | yes | adequate |
| deliver_item(item_2) | 167 to 225 | 171 | 0.7846 | yes | adequate |
| deliver_item(item_1) | 226 to 325 | 226 | 0.9757 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 42 | deliver_item(item_2) | move_to(item_2) | 0.0328 | 0.0441 | 347.1 | 327.1 | 20.0 | deliver_item(item_0) |
| 47 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0025 | 0.0445 | 346.3 | 286.3 | 60.0 | deliver_item(item_0) |
| 49 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0033 | 0.0495 | 335.5 | 275.5 | 60.0 | deliver_item(item_0) |
| 54 | deliver_item(item_1) | move_to(shelf_0) | 0.0333 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 54 | deliver_item(item_2) | move_to(shelf_0) | 0.0025 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 140 | deliver_item(item_2) | move_to(item_2) | 0.1652 | 0.0431 | 349.5 | 229.5 | 120.0 | coffee_break(coffee_machine_0) |
| 147 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0200 | 0.0459 | 343.2 | 83.2 | 260.0 | coffee_break(coffee_machine_0) |
| 147 | deliver_item(item_1) | move_to(item_1) | 0.5399 | 0.0495 | 335.5 | 75.5 | 260.0 | coffee_break(coffee_machine_0) |
| 175 | deliver_item(item_1) | move_to(item_1) | 0.0500 | 0.0390 | 359.7 | 359.7 | 0.0 | deliver_item(item_2) |
| 177 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0426 | 350.8 | 310.8 | 40.0 | deliver_item(item_2) |
| 181 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0026 | 0.0500 | 334.5 | 274.5 | 60.0 | deliver_item(item_2) |
| 189 | deliver_item(item_1) | move_to(shelf_2) | 0.0020 | 0.0400 | 357.3 | 357.3 | 0.0 | deliver_item(item_2) |
| 278 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0448 | 345.7 | 285.7 | 60.0 | deliver_item(item_1) |
| 281 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1116 | 0.0462 | 342.6 | 282.6 | 60.0 | deliver_item(item_1) |
| 337 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.4458 | 0.0433 | 349.0 | 349.0 | 0.0 | - |
| 338 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.5554 | 0.0402 | 356.6 | 356.6 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_0) |
| 87 | adequate | unresolved | deliver_item(item_0) |
| 88 | unresolved | adequate | deliver_item(item_0) |
| 165 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 166 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 224 | adequate | unresolved | deliver_item(item_2) |
| 225 | unresolved | adequate | deliver_item(item_2) |
| 324 | adequate | unresolved | deliver_item(item_1) |
| 325 | unresolved | adequate | deliver_item(item_1) |
| 338 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 86, 89 to 164, 167 to 178, 226 to 321 |
| coffee_break(coffee_machine_0) | 0 to 86, 89 to 164, 226 to 321 |
| deliver_item(item_0) | 0 to 86 |
| deliver_item(item_1) | 0 to 42, 89 to 164, 226 to 323 |
| deliver_item(item_2) | 0 to 42, 89 to 164, 167 to 223 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 47 | deliver_item(item_0) | none(below_theta) |
| 48 to 86 | deliver_item(item_0) | clears |
| 87 to 149 | deliver_item(item_1) | none(below_theta) |
| 150 to 156 | coffee_break(coffee_machine_0) | none(below_theta) |
| 157 to 164 | coffee_break(coffee_machine_0) | clears |
| 165 to 166 | deliver_item(item_1) | none(below_theta) |
| 167 to 170 | deliver_item(item_2) | none(below_theta) |
| 171 to 223 | deliver_item(item_2) | clears |
| 224 to 224 | deliver_item(item_1) | none(leader_no_observation) |
| 225 to 225 | deliver_item(item_1) | none(leader_unwarranted) |
| 226 to 254 | deliver_item(item_1) | clears |
| 255 to 271 | coffee_break(coffee_machine_0) | none(below_theta) |
| 272 to 277 | deliver_item(item_1) | none(below_theta) |
| 278 to 323 | deliver_item(item_1) | clears |
| 324 to 378 | ac_activation(ac_switch_0) | none(below_theta) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of ac_activation | 0 to 378 ordinary |
| level of coffee_break | 0 to 164 ordinary, 165 to 166 retired, 167 to 254 suppressed, 255 to 299 raised, 300 to 378 ordinary |
| recency facts | 0 to 164 none, 165 to 254 coffee_break, 255 to 378 none |

The last entry (go_to(corner_NE)): first step 326, last step 347, acknowledgement 348; the idle human from 349. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.5014 at 326; S < α from 338 (belief 0.5554; v·D 356.6 cm); the finding unexplained from 338.

- coffee_break(coffee_machine_0): belief 0.4956 at 326; S < α from 337 (belief 0.4458; v·D 349.0 cm); the finding unexplained from 338.

