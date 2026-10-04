### scenario_s14_08

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
| 181 | ac_activation(ac_switch_0) | covered | move_to | 0 | 1 |
| 228 | ac_activation(ac_switch_0) | covered | switch_on | 0 | 1 |
| 230 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 241 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 243 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 292 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 294 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 316; idle from 317 to 346. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 225 |
| ac_activation(ac_switch_0) | switch_on(PT2S,ac_switch_0) | 226 to 230 |
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | 231 to 346 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 232 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 233 to 235 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 236 to 346 |
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
| deliver_item(item_1) | move_to(item_1) | 179 to 238 |
| deliver_item(item_1) | pick_up(item_1) | 239 to 240 |
| deliver_item(item_1) | move_to(kitting_table_0) | 241 to 289 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 290 to 291 |
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
| 228 | boundary |
| 228 | pin ac_activation(ac_switch_0) |
| 230 | re-entry ac_activation(ac_switch_0) |
| 292 | boundary |
| 292 | pin deliver_item(item_1) |
| 306 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_NE), ticks 294 to 316): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_0) | 0 to 88 | 48 | 0.7504 | yes | adequate |
| deliver_item(item_2) | 89 to 180 | 129 | 0.7534 | yes | adequate |
| ac_activation(ac_switch_0) | 181 to 229 | not reached | - | - | - |
| deliver_item(item_1) | 230 to 293 | 230 | 0.9756 | yes | adequate |

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
| 240 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0489 | 336.7 | 316.7 | 20.0 | deliver_item(item_1) |
| 248 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0013 | 0.0482 | 338.3 | 278.3 | 60.0 | deliver_item(item_1) |
| 305 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.7616 | 0.0433 | 349.2 | 349.2 | 0.0 | - |
| 306 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.2385 | 0.0402 | 356.8 | 356.8 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_0) |
| 87 | adequate | unresolved | deliver_item(item_0) |
| 88 | unresolved | adequate | deliver_item(item_0) |
| 179 | adequate | unresolved | deliver_item(item_2) |
| 180 | unresolved | adequate | deliver_item(item_2) |
| 228 | adequate | unresolved | ac_activation(ac_switch_0) |
| 229 | unresolved | adequate | ac_activation(ac_switch_0) |
| 292 | adequate | unresolved | deliver_item(item_1) |
| 293 | unresolved | adequate | deliver_item(item_1) |
| 306 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 86, 89 to 176, 181 to 227 |
| coffee_break(coffee_machine_0) | 0 to 86, 89 to 176, 181 to 227, 230 to 235 |
| deliver_item(item_0) | 0 to 86 |
| deliver_item(item_1) | 0 to 42, 89 to 132, 181 to 227, 230 to 291 |
| deliver_item(item_2) | 0 to 42, 89 to 178 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 47 | deliver_item(item_0) | none(below_theta) |
| 48 to 86 | deliver_item(item_0) | clears |
| 87 to 88 | deliver_item(item_1) | none(below_theta) |
| 89 to 128 | deliver_item(item_2) | none(below_theta) |
| 129 to 178 | deliver_item(item_2) | clears |
| 179 to 221 | deliver_item(item_1) | none(below_theta) |
| 222 to 227 | ac_activation(ac_switch_0) | none(below_theta) |
| 228 to 228 | deliver_item(item_1) | none(leader_no_observation) |
| 229 to 229 | deliver_item(item_1) | none(leader_unwarranted) |
| 230 to 291 | deliver_item(item_1) | clears |
| 292 to 292 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 293 to 304 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 305 to 309 | coffee_break(coffee_machine_0) | none(leader_inadequate) |
| 310 to 346 | coffee_break(coffee_machine_0) | none(below_theta) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of ac_activation | 0 to 149 ordinary, 150 to 227 raised, 228 to 229 retired, 230 to 346 suppressed |
| level of coffee_break | 0 to 346 ordinary |
| recency facts | 0 to 346 none |

The last entry (go_to(corner_NE)): first step 294, last step 315, acknowledgement 316; the idle human from 317. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.2012 at 294; S < α from 306 (belief 0.2385; v·D 356.8 cm); the finding unexplained from 306.

- coffee_break(coffee_machine_0): belief 0.7958 at 294; S < α from 305 (belief 0.7616; v·D 349.2 cm); the finding unexplained from 306.

