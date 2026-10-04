### scenario_s15_09

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_3,kitting_table_0) | covered | move_to | 0 | 1 |
| 32 | deliver_item(item_3,kitting_table_0) | covered | pick_up | 0 | 1 |
| 34 | deliver_item(item_3,kitting_table_0) | covered | move_to | 1 | 1 |
| 65 | deliver_item(item_3,kitting_table_0) | covered | place | 0 | 1 |
| 67 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 94 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 96 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 122 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 124 | ac_activation(ac_switch_0) | covered | move_to | 0 | 1 |
| 170 | ac_activation(ac_switch_0) | covered | switch_on | 0 | 1 |
| 172 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 180 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 182 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 228 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 230 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 275 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 277 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 322 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 324 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 345; idle from 346 to 375. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 167 |
| ac_activation(ac_switch_0) | switch_on(PT2S,ac_switch_0) | 168 to 172 |
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | 173 to 375 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 375 |
| deliver_item(item_1) | move_to(item_1) | -1 to 31 |
| deliver_item(item_1) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_1) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_1) | move_to(item_1) | 65 to 93 |
| deliver_item(item_1) | place(item_2,shelf_2) | 94 to 95 |
| deliver_item(item_1) | move_to(shelf_2) | 96 to 121 |
| deliver_item(item_1) | move_to(item_1) | 122 to 177 |
| deliver_item(item_1) | pick_up(item_1) | 178 to 179 |
| deliver_item(item_1) | move_to(kitting_table_0) | 180 to 225 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 226 to 227 |
| deliver_item(item_2) | move_to(item_2) | -1 to 31 |
| deliver_item(item_2) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_2) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_2) | move_to(item_2) | 65 to 91 |
| deliver_item(item_2) | pick_up(item_2) | 92 to 93 |
| deliver_item(item_2) | move_to(kitting_table_0) | 94 to 119 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 120 to 121 |
| deliver_item(item_3) | move_to(item_3) | -1 to 29 |
| deliver_item(item_3) | pick_up(item_3) | 30 to 31 |
| deliver_item(item_3) | move_to(kitting_table_0) | 32 to 62 |
| deliver_item(item_3) | place(item_3,kitting_table_0) | 63 to 64 |
| deliver_item(item_4) | move_to(item_4) | -1 to 31 |
| deliver_item(item_4) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_4) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_4) | move_to(item_4) | 65 to 93 |
| deliver_item(item_4) | place(item_2,shelf_2) | 94 to 95 |
| deliver_item(item_4) | move_to(shelf_2) | 96 to 121 |
| deliver_item(item_4) | move_to(item_4) | 122 to 179 |
| deliver_item(item_4) | place(item_1,shelf_1) | 180 to 182 |
| deliver_item(item_4) | move_to(shelf_1) | 183 to 227 |
| deliver_item(item_4) | move_to(item_4) | 228 to 272 |
| deliver_item(item_4) | pick_up(item_4) | 273 to 274 |
| deliver_item(item_4) | move_to(kitting_table_0) | 275 to 319 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 320 to 321 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 122 | boundary |
| 122 | pin deliver_item(item_2) |
| 170 | boundary |
| 170 | pin ac_activation(ac_switch_0) |
| 172 | re-entry ac_activation(ac_switch_0) |
| 228 | boundary |
| 228 | pin deliver_item(item_1) |
| 322 | boundary |
| 322 | pin deliver_item(item_4) |
| 347 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_NE), ticks 324 to 345): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 26 | 0.7569 | yes | adequate |
| deliver_item(item_2) | 67 to 123 | 87 | 0.7557 | yes | adequate |
| ac_activation(ac_switch_0) | 124 to 171 | not reached | - | - | - |
| deliver_item(item_1) | 172 to 229 | 176 | 0.7977 | yes | adequate |
| deliver_item(item_4) | 230 to 323 | 230 | 0.9758 | yes | adequate |

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
| 101 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0031 | 0.0383 | 361.4 | 301.4 | 60.0 | deliver_item(item_2) |
| 105 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 105 | deliver_item(item_4) | move_to(shelf_2) | 0.0038 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 159 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0473 | 340.1 | 340.1 | 0.0 | ac_activation(ac_switch_0) |
| 182 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0023 | 0.0464 | 342.0 | 282.0 | 60.0 | deliver_item(item_1) |
| 185 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0385 | 361.0 | 301.0 | 60.0 | deliver_item(item_1) |
| 192 | deliver_item(item_4) | move_to(shelf_1) | 0.0042 | 0.0398 | 357.7 | 357.7 | 0.0 | deliver_item(item_1) |
| 271 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0013 | 0.0492 | 336.2 | 336.2 | 0.0 | deliver_item(item_4) |
| 282 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0416 | 353.1 | 293.1 | 60.0 | deliver_item(item_4) |
| 338 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0487 | 0.0408 | 355.2 | 355.2 | 0.0 | - |
| 347 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9714 | 0.0431 | 349.6 | 289.6 | 60.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_3) |
| 65 | adequate | unresolved | deliver_item(item_3) |
| 66 | unresolved | adequate | deliver_item(item_3) |
| 122 | adequate | unresolved | deliver_item(item_2) |
| 123 | unresolved | adequate | deliver_item(item_2) |
| 170 | adequate | unresolved | ac_activation(ac_switch_0) |
| 171 | unresolved | adequate | ac_activation(ac_switch_0) |
| 228 | adequate | unresolved | deliver_item(item_1) |
| 229 | unresolved | adequate | deliver_item(item_1) |
| 322 | adequate | unresolved | deliver_item(item_4) |
| 323 | unresolved | adequate | deliver_item(item_4) |
| 347 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 64, 67 to 119, 124 to 169, 230 to 319 |
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 121, 124 to 169, 230 to 321, 324 to 375 |
| deliver_item(item_1) | 0 to 31, 67 to 93, 124 to 169, 172 to 227 |
| deliver_item(item_2) | 67 to 121 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 93, 124 to 169, 230 to 321 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 25 | deliver_item(item_3) | none(below_theta) |
| 26 to 64 | deliver_item(item_3) | clears |
| 65 to 66 | deliver_item(item_1) | none(below_theta) |
| 67 to 86 | deliver_item(item_2) | none(below_theta) |
| 87 to 121 | deliver_item(item_2) | clears |
| 122 to 123 | deliver_item(item_1) | none(below_theta) |
| 124 to 149 | deliver_item(item_4) | none(below_theta) |
| 150 to 169 | ac_activation(ac_switch_0) | none(below_theta) |
| 170 to 175 | deliver_item(item_1) | none(below_theta) |
| 176 to 227 | deliver_item(item_1) | clears |
| 228 to 228 | deliver_item(item_4) | none(leader_no_observation) |
| 229 to 321 | deliver_item(item_4) | clears |
| 322 to 322 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 323 to 323 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 324 to 346 | coffee_break(coffee_machine_0) | clears |
| 347 to 375 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of ac_activation | 0 to 149 ordinary, 150 to 169 raised, 170 to 171 retired, 172 to 375 suppressed |
| level of coffee_break | 0 to 375 ordinary |
| recency facts | 0 to 375 none |

The last entry (go_to(corner_NE)): first step 324, last step 344, acknowledgement 345; the idle human from 346. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.1898 at 324; S < α from 338 (belief 0.0487; v·D 355.2 cm); the finding unexplained from 347.

- coffee_break(coffee_machine_0): belief 0.8062 at 324; S < α from 347 (belief 0.9714; v·D 349.6 cm); the finding unexplained from 347.

