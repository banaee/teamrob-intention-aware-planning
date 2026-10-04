### scenario_s14_07

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_0,kitting_table_0) | covered | move_to | 0 | 1 |
| 43 | deliver_item(item_0,kitting_table_0) | covered | pick_up | 0 | 1 |
| 45 | deliver_item(item_0,kitting_table_0) | covered | move_to | 1 | 1 |
| 87 | deliver_item(item_0,kitting_table_0) | covered | place | 0 | 1 |
| 89 | ac_activation(ac_switch_0) | covered | move_to | 0 | 1 |
| 136 | ac_activation(ac_switch_0) | covered | switch_on | 0 | 1 |
| 138 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 143 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 145 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 191 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 193 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 242 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 244 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 293 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 295 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 317; idle from 318 to 347. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 133 |
| ac_activation(ac_switch_0) | switch_on(PT2S,ac_switch_0) | 134 to 135 |
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | 138 to 347 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 347 |
| deliver_item(item_0) | move_to(item_0) | -1 to 40 |
| deliver_item(item_0) | pick_up(item_0) | 41 to 42 |
| deliver_item(item_0) | move_to(kitting_table_0) | 43 to 84 |
| deliver_item(item_0) | place(item_0,kitting_table_0) | 85 to 86 |
| deliver_item(item_1) | move_to(item_1) | -1 to 42 |
| deliver_item(item_1) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_1) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_1) | move_to(item_1) | 87 to 142 |
| deliver_item(item_1) | place(item_2,shelf_2) | 143 to 145 |
| deliver_item(item_1) | move_to(shelf_2) | 146 to 190 |
| deliver_item(item_1) | move_to(item_1) | 191 to 239 |
| deliver_item(item_1) | pick_up(item_1) | 240 to 241 |
| deliver_item(item_1) | move_to(kitting_table_0) | 242 to 290 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 291 to 292 |
| deliver_item(item_2) | move_to(item_2) | -1 to 42 |
| deliver_item(item_2) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_2) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_2) | move_to(item_2) | 87 to 140 |
| deliver_item(item_2) | pick_up(item_2) | 141 to 142 |
| deliver_item(item_2) | move_to(kitting_table_0) | 143 to 188 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 189 to 190 |

Events (actual):

| tick | event |
|---|---|
| 87 | boundary |
| 87 | pin deliver_item(item_0) |
| 136 | boundary |
| 136 | pin ac_activation(ac_switch_0) |
| 138 | re-entry ac_activation(ac_switch_0) |
| 191 | boundary |
| 191 | pin deliver_item(item_2) |
| 293 | boundary |
| 293 | pin deliver_item(item_1) |
| 307 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_NE), ticks 295 to 317): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_0) | 0 to 88 | 48 | 0.7504 | yes | adequate |
| ac_activation(ac_switch_0) | 89 to 137 | not reached | - | - | - |
| deliver_item(item_2) | 138 to 192 | 142 | 0.7672 | yes | adequate |
| deliver_item(item_1) | 193 to 294 | 193 | 0.9756 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 42 | deliver_item(item_2) | move_to(item_2) | 0.0328 | 0.0441 | 347.1 | 327.1 | 20.0 | deliver_item(item_0) |
| 47 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0025 | 0.0445 | 346.3 | 286.3 | 60.0 | deliver_item(item_0) |
| 49 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0033 | 0.0495 | 335.5 | 275.5 | 60.0 | deliver_item(item_0) |
| 54 | deliver_item(item_1) | move_to(shelf_0) | 0.0333 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 54 | deliver_item(item_2) | move_to(shelf_0) | 0.0025 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 149 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0428 | 350.3 | 290.3 | 60.0 | deliver_item(item_2) |
| 149 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0018 | 0.0377 | 363.1 | 303.1 | 60.0 | deliver_item(item_2) |
| 155 | deliver_item(item_1) | move_to(shelf_2) | 0.0134 | 0.0411 | 354.5 | 354.5 | 0.0 | deliver_item(item_2) |
| 246 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0427 | 350.6 | 290.6 | 60.0 | deliver_item(item_1) |
| 249 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0012 | 0.0455 | 344.1 | 284.1 | 60.0 | deliver_item(item_1) |
| 306 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.7617 | 0.0457 | 343.6 | 343.6 | 0.0 | - |
| 307 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.2384 | 0.0426 | 350.7 | 350.7 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_0) |
| 87 | adequate | unresolved | deliver_item(item_0) |
| 88 | unresolved | adequate | deliver_item(item_0) |
| 136 | adequate | unresolved | ac_activation(ac_switch_0) |
| 137 | unresolved | adequate | ac_activation(ac_switch_0) |
| 191 | adequate | unresolved | deliver_item(item_2) |
| 192 | unresolved | adequate | deliver_item(item_2) |
| 293 | adequate | unresolved | deliver_item(item_1) |
| 294 | unresolved | adequate | deliver_item(item_1) |
| 307 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 86, 89 to 135, 193 to 290 |
| coffee_break(coffee_machine_0) | 0 to 86, 89 to 135, 193 to 290 |
| deliver_item(item_0) | 0 to 86 |
| deliver_item(item_1) | 0 to 42, 89 to 135, 193 to 292 |
| deliver_item(item_2) | 0 to 42, 89 to 135, 138 to 190 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 47 | deliver_item(item_0) | none(below_theta) |
| 48 to 86 | deliver_item(item_0) | clears |
| 87 to 88 | deliver_item(item_1) | none(below_theta) |
| 89 to 135 | deliver_item(item_2) | none(below_theta) |
| 136 to 137 | deliver_item(item_1) | none(below_theta) |
| 138 to 141 | deliver_item(item_2) | none(below_theta) |
| 142 to 190 | deliver_item(item_2) | clears |
| 191 to 191 | deliver_item(item_1) | none(leader_no_observation) |
| 192 to 192 | deliver_item(item_1) | none(leader_unwarranted) |
| 193 to 292 | deliver_item(item_1) | clears |
| 293 to 293 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 294 to 305 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 306 to 310 | coffee_break(coffee_machine_0) | none(leader_inadequate) |
| 311 to 347 | coffee_break(coffee_machine_0) | none(below_theta) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of ac_activation | 0 to 135 ordinary, 136 to 137 retired, 138 to 347 suppressed |
| level of coffee_break | 0 to 347 ordinary |
| recency facts | 0 to 347 none |

The last entry (go_to(corner_NE)): first step 295, last step 316, acknowledgement 317; the idle human from 318. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.2012 at 295; S < α from 307 (belief 0.2384; v·D 350.7 cm); the finding unexplained from 307.

- coffee_break(coffee_machine_0): belief 0.7958 at 295; S < α from 306 (belief 0.7617; v·D 343.6 cm); the finding unexplained from 307.

