### scenario_s14_10

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_0,kitting_table_0) | covered | move_to | 0 | 1 |
| 43 | deliver_item(item_0,kitting_table_0) | covered | pick_up | 0 | 1 |
| 45 | deliver_item(item_0,kitting_table_0) | covered | move_to | 1 | 1 |
| 87 | deliver_item(item_0,kitting_table_0) | covered | place | 0 | 1 |
| 89 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 133 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 135 | ac_activation(ac_switch_0) | covered | move_to | 0 | 2 |
| 141 | ac_activation(ac_switch_0) | covered | switch_on | 0 | 2 |
| 143 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 190 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 192 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 241 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 243 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 292 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 294 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 316; idle from 317 to 346. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 138 |
| ac_activation(ac_switch_0) | switch_on(PT2S,ac_switch_0) | 139 to 140 |
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | 143 to 346 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 346 |
| deliver_item(item_0) | move_to(item_0) | -1 to 40 |
| deliver_item(item_0) | pick_up(item_0) | 41 to 42 |
| deliver_item(item_0) | move_to(kitting_table_0) | 43 to 84 |
| deliver_item(item_0) | place(item_0,kitting_table_0) | 85 to 86 |
| deliver_item(item_1) | move_to(item_1) | -1 to 42 |
| deliver_item(item_1) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_1) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_1) | move_to(item_1) | 87 to 132 |
| deliver_item(item_1) | place(item_2,shelf_2) | 133 to 135 |
| deliver_item(item_1) | move_to(shelf_2) | 136 to 189 |
| deliver_item(item_1) | move_to(item_1) | 190 to 238 |
| deliver_item(item_1) | pick_up(item_1) | 239 to 240 |
| deliver_item(item_1) | move_to(kitting_table_0) | 241 to 289 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 290 to 291 |
| deliver_item(item_2) | move_to(item_2) | -1 to 42 |
| deliver_item(item_2) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_2) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_2) | move_to(item_2) | 87 to 130 |
| deliver_item(item_2) | pick_up(item_2) | 131 to 132 |
| deliver_item(item_2) | move_to(kitting_table_0) | 133 to 187 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 188 to 189 |

Events (actual):

| tick | event |
|---|---|
| 87 | boundary |
| 87 | pin deliver_item(item_0) |
| 141 | boundary |
| 141 | pin ac_activation(ac_switch_0) |
| 143 | re-entry ac_activation(ac_switch_0) |
| 190 | boundary |
| 190 | pin deliver_item(item_2) |
| 292 | boundary |
| 292 | pin deliver_item(item_1) |
| 306 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_NE), ticks 294 to 316): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_0) | 0 to 88 | 48 | 0.7504 | yes | adequate |
| deliver_item(item_2) | 89 to 134 | 129 | 0.7534 | yes | adequate |
| ac_activation(ac_switch_0) | 135 to 142 | not reached | - | - | - |
| deliver_item(item_2) | 143 to 191 | 149 | 0.7744 | yes | adequate |
| deliver_item(item_1) | 192 to 293 | 192 | 0.9756 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 42 | deliver_item(item_2) | move_to(item_2) | 0.0328 | 0.0441 | 347.1 | 327.1 | 20.0 | deliver_item(item_0) |
| 47 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0025 | 0.0445 | 346.3 | 286.3 | 60.0 | deliver_item(item_0) |
| 49 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0033 | 0.0495 | 335.5 | 275.5 | 60.0 | deliver_item(item_0) |
| 54 | deliver_item(item_1) | move_to(shelf_0) | 0.0333 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 54 | deliver_item(item_2) | move_to(shelf_0) | 0.0025 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 152 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0403 | 356.4 | 356.4 | 0.0 | deliver_item(item_2) |
| 153 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0018 | 0.0362 | 367.2 | 367.2 | 0.0 | deliver_item(item_2) |
| 154 | deliver_item(item_1) | move_to(shelf_2) | 0.0464 | 0.0356 | 368.9 | 368.9 | 0.0 | deliver_item(item_2) |
| 244 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0482 | 338.3 | 278.3 | 60.0 | deliver_item(item_1) |
| 248 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0012 | 0.0442 | 347.0 | 287.0 | 60.0 | deliver_item(item_1) |
| 305 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.7617 | 0.0442 | 347.0 | 347.0 | 0.0 | - |
| 306 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.2385 | 0.0411 | 354.3 | 354.3 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_0) |
| 87 | adequate | unresolved | deliver_item(item_0) |
| 88 | unresolved | adequate | deliver_item(item_0) |
| 141 | adequate | unresolved | ac_activation(ac_switch_0) |
| 142 | unresolved | adequate | ac_activation(ac_switch_0) |
| 190 | adequate | unresolved | deliver_item(item_2) |
| 191 | unresolved | adequate | deliver_item(item_2) |
| 292 | adequate | unresolved | deliver_item(item_1) |
| 293 | unresolved | adequate | deliver_item(item_1) |
| 306 | adequate | unexplained | - |

Across the started task ac_activation(ac_switch_0) (covered; actual): on top of the stack from 135 to 142, its hypothesis pinned at 141; the suspended task resumes at 143.

| tick | human action | truth | ac_activation(ac_switch_0) belief / S | coffee_break(coffee_machine_0) belief / S | deliver_item(item_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|---|---|
| 133 | pick_up grasp | deliver_item(item_2) | 0.0200 / 0.5058 | 0.0109 / 0.2545 | retired | 0.1221 / 1.0000 | 0.8459 / 1.0000 | adequate |
| 134 | pick_up  | deliver_item(item_2) | 0.0174 / 0.4263 | 0.0093 / 0.2116 | retired | 0.1227 / 1.0000 | 0.8497 / 1.0000 | adequate |
| 135 | move_to step | ac_activation(ac_switch_0) | 0.0201 / 0.4263 | 0.0106 / 0.2096 | retired | 0.1417 / 1.0000 | 0.8265 / 0.7882 | adequate |
| 136 | move_to step | ac_activation(ac_switch_0) | 0.0236 / 0.4263 | 0.0124 / 0.2073 | retired | 0.1666 / - | 0.7964 / 0.6106 | adequate |
| 137 | move_to step | ac_activation(ac_switch_0) | 0.0292 / 0.4263 | 0.0151 / 0.2044 | retired | 0.1684 / 0.7595 | 0.7863 / 0.4656 | adequate |
| 140 | move_to  | ac_activation(ac_switch_0) | 0.0557 / 1.0000 | 0.0232 / 0.1625 | retired | 0.1626 / 0.3345 | 0.7575 / 0.2162 | adequate |
| 141 | switch_on stand | ac_activation(ac_switch_0) | retired | 0.0196 / - | retired | 0.4892 / - | 0.4892 / - | unresolved |
| 142 | switch_on  | ac_activation(ac_switch_0) | retired | 0.0196 / 1.0000 | retired | 0.4892 / 1.0000 | 0.4892 / 1.0000 | adequate |
| 143 | move_to step | deliver_item(item_2) | 0.0047 / - | 0.0177 / 0.8317 | retired | 0.4717 / 0.9081 | 0.5049 / 1.0000 | adequate |
| 144 | move_to step | deliver_item(item_2) | 0.0040 / 0.7487 | 0.0158 / 0.6699 | retired | 0.4488 / 0.7936 | 0.5304 / 1.0000 | adequate |
| 145 | move_to step | deliver_item(item_2) | 0.0033 / 0.5454 | 0.0138 / 0.5233 | retired | 0.4166 / 0.6631 | 0.5653 / 1.0000 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 86, 89 to 140, 192 to 289 |
| coffee_break(coffee_machine_0) | 0 to 86, 89 to 140, 192 to 289 |
| deliver_item(item_0) | 0 to 86 |
| deliver_item(item_1) | 0 to 42, 89 to 132, 143 to 145, 192 to 291 |
| deliver_item(item_2) | 0 to 42, 89 to 140, 143 to 189 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 47 | deliver_item(item_0) | none(below_theta) |
| 48 to 86 | deliver_item(item_0) | clears |
| 87 to 88 | deliver_item(item_1) | none(below_theta) |
| 89 to 128 | deliver_item(item_2) | none(below_theta) |
| 129 to 137 | deliver_item(item_2) | clears |
| 138 to 140 | deliver_item(item_2) | none(leader_outranked) |
| 141 to 142 | deliver_item(item_1) | none(below_theta) |
| 143 to 148 | deliver_item(item_2) | none(below_theta) |
| 149 to 189 | deliver_item(item_2) | clears |
| 190 to 190 | deliver_item(item_1) | none(leader_no_observation) |
| 191 to 191 | deliver_item(item_1) | none(leader_unwarranted) |
| 192 to 291 | deliver_item(item_1) | clears |
| 292 to 292 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 293 to 304 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 305 to 309 | coffee_break(coffee_machine_0) | none(leader_inadequate) |
| 310 to 346 | coffee_break(coffee_machine_0) | none(below_theta) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of ac_activation | 0 to 140 ordinary, 141 to 142 retired, 143 to 346 suppressed |
| level of coffee_break | 0 to 346 ordinary |
| recency facts | 0 to 346 none |

The last entry (go_to(corner_NE)): first step 294, last step 315, acknowledgement 316; the idle human from 317. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.2012 at 294; S < α from 306 (belief 0.2385; v·D 354.3 cm); the finding unexplained from 306.

- coffee_break(coffee_machine_0): belief 0.7958 at 294; S < α from 305 (belief 0.7617; v·D 347.0 cm); the finding unexplained from 306.

