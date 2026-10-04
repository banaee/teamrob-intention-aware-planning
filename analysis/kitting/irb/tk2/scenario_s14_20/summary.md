### scenario_s14_20

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
| 181 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 230 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 232 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 281 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 283 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 305; idle from 306 to 335. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 335 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 335 |
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
| deliver_item(item_1) | move_to(item_1) | 179 to 227 |
| deliver_item(item_1) | pick_up(item_1) | 228 to 229 |
| deliver_item(item_1) | move_to(kitting_table_0) | 230 to 278 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 279 to 280 |
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
| 281 | boundary |
| 281 | pin deliver_item(item_1) |
| 295 | finding turns unexplained |

Never pinned: ac_activation(ac_switch_0), coffee_break(coffee_machine_0). At the last entry (go_to(corner_NE), ticks 283 to 305): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_0) | 0 to 88 | 51 | 0.7539 | yes | adequate |
| deliver_item(item_2) | 89 to 180 | 139 | 0.7543 | yes | adequate |
| deliver_item(item_1) | 181 to 282 | 234 | 0.7745 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 42 | deliver_item(item_2) | move_to(item_2) | 0.0145 | 0.0441 | 347.1 | 327.1 | 20.0 | deliver_item(item_0) |
| 47 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0017 | 0.0445 | 346.3 | 286.3 | 60.0 | deliver_item(item_0) |
| 49 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.2464 | 0.0495 | 335.5 | 275.5 | 60.0 | deliver_item(item_0) |
| 54 | deliver_item(item_1) | move_to(shelf_0) | 0.0311 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 54 | deliver_item(item_2) | move_to(shelf_0) | 0.0024 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 140 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1597 | 0.0361 | 367.6 | 307.6 | 60.0 | deliver_item(item_2) |
| 141 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0019 | 0.0396 | 358.1 | 298.1 | 60.0 | deliver_item(item_2) |
| 144 | deliver_item(item_1) | move_to(shelf_2) | 0.0072 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 233 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0493 | 335.9 | 275.9 | 60.0 | deliver_item(item_1) |
| 237 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1081 | 0.0445 | 346.2 | 286.2 | 60.0 | deliver_item(item_1) |
| 294 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9848 | 0.0447 | 345.9 | 345.9 | 0.0 | - |
| 295 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0124 | 0.0416 | 353.2 | 353.2 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_0) |
| 87 | adequate | unresolved | deliver_item(item_0) |
| 88 | unresolved | adequate | deliver_item(item_0) |
| 179 | adequate | unresolved | deliver_item(item_2) |
| 180 | unresolved | adequate | deliver_item(item_2) |
| 281 | adequate | unresolved | deliver_item(item_1) |
| 282 | unresolved | adequate | deliver_item(item_1) |
| 295 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 86, 89 to 176, 181 to 278 |
| coffee_break(coffee_machine_0) | 0 to 86, 89 to 176, 181 to 278 |
| deliver_item(item_0) | 0 to 86 |
| deliver_item(item_1) | 0 to 42, 89 to 132, 181 to 280 |
| deliver_item(item_2) | 0 to 42, 89 to 178 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 46 | coffee_break(coffee_machine_0) | none(below_theta) |
| 47 to 50 | deliver_item(item_0) | none(below_theta) |
| 51 to 86 | deliver_item(item_0) | clears |
| 87 to 134 | coffee_break(coffee_machine_0) | none(below_theta) |
| 135 to 138 | deliver_item(item_2) | none(below_theta) |
| 139 to 178 | deliver_item(item_2) | clears |
| 179 to 227 | coffee_break(coffee_machine_0) | none(below_theta) |
| 228 to 233 | deliver_item(item_1) | none(below_theta) |
| 234 to 280 | deliver_item(item_1) | clears |
| 281 to 281 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 282 to 293 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 294 to 335 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of ac_activation | 0 to 335 ordinary |
| level of coffee_break | 0 to 335 raised |
| recency facts | 0 to 335 none |

The last entry (go_to(corner_NE)): first step 283, last step 304, acknowledgement 305; the idle human from 306. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.0100 at 283; S < α from 295 (belief 0.0124; v·D 353.2 cm); the finding unexplained from 295.

- coffee_break(coffee_machine_0): belief 0.9870 at 283; S < α from 294 (belief 0.9848; v·D 345.9 cm); the finding unexplained from 295.

