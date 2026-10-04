### scenario_s14_09

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_0,kitting_table_0) | covered | move_to | 0 | 1 |
| 43 | deliver_item(item_0,kitting_table_0) | covered | pick_up | 0 | 1 |
| 45 | deliver_item(item_0,kitting_table_0) | covered | move_to | 1 | 1 |
| 87 | deliver_item(item_0,kitting_table_0) | covered | place | 0 | 1 |
| 89 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 133 | ac_activation(ac_switch_0) | covered | move_to | 0 | 2 |
| 139 | ac_activation(ac_switch_0) | covered | switch_on | 0 | 2 |
| 141 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 145 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 147 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 193 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 195 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 244 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 246 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 295 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 297 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 319; idle from 320 to 349. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 136 |
| ac_activation(ac_switch_0) | switch_on(PT2S,ac_switch_0) | 137 to 138 |
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | 141 to 349 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 349 |
| deliver_item(item_0) | move_to(item_0) | -1 to 40 |
| deliver_item(item_0) | pick_up(item_0) | 41 to 42 |
| deliver_item(item_0) | move_to(kitting_table_0) | 43 to 84 |
| deliver_item(item_0) | place(item_0,kitting_table_0) | 85 to 86 |
| deliver_item(item_1) | move_to(item_1) | -1 to 42 |
| deliver_item(item_1) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_1) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_1) | move_to(item_1) | 87 to 144 |
| deliver_item(item_1) | place(item_2,shelf_2) | 145 to 147 |
| deliver_item(item_1) | move_to(shelf_2) | 148 to 192 |
| deliver_item(item_1) | move_to(item_1) | 193 to 241 |
| deliver_item(item_1) | pick_up(item_1) | 242 to 243 |
| deliver_item(item_1) | move_to(kitting_table_0) | 244 to 292 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 293 to 294 |
| deliver_item(item_2) | move_to(item_2) | -1 to 42 |
| deliver_item(item_2) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_2) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_2) | move_to(item_2) | 87 to 130 |
| deliver_item(item_2) | pick_up(item_2) | 131 to 133 |
| deliver_item(item_2) | move_to(item_2) | 134 to 142 |
| deliver_item(item_2) | pick_up(item_2) | 143 to 144 |
| deliver_item(item_2) | move_to(kitting_table_0) | 145 to 190 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 191 to 192 |

Events (actual):

| tick | event |
|---|---|
| 87 | boundary |
| 87 | pin deliver_item(item_0) |
| 139 | boundary |
| 139 | pin ac_activation(ac_switch_0) |
| 141 | re-entry ac_activation(ac_switch_0) |
| 193 | boundary |
| 193 | pin deliver_item(item_2) |
| 295 | boundary |
| 295 | pin deliver_item(item_1) |
| 309 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_NE), ticks 297 to 319): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_0) | 0 to 88 | 48 | 0.7504 | yes | adequate |
| deliver_item(item_2) | 89 to 132 | 129 | 0.7534 | yes | adequate |
| ac_activation(ac_switch_0) | 133 to 140 | not reached | - | - | - |
| deliver_item(item_2) | 141 to 194 | 149 | 0.7757 | yes | adequate |
| deliver_item(item_1) | 195 to 296 | 195 | 0.9756 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 42 | deliver_item(item_2) | move_to(item_2) | 0.0328 | 0.0441 | 347.1 | 327.1 | 20.0 | deliver_item(item_0) |
| 47 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0025 | 0.0445 | 346.3 | 286.3 | 60.0 | deliver_item(item_0) |
| 49 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0033 | 0.0495 | 335.5 | 275.5 | 60.0 | deliver_item(item_0) |
| 54 | deliver_item(item_1) | move_to(shelf_0) | 0.0333 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 54 | deliver_item(item_2) | move_to(shelf_0) | 0.0025 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 152 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0425 | 350.9 | 290.9 | 60.0 | deliver_item(item_2) |
| 152 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0020 | 0.0412 | 354.1 | 294.1 | 60.0 | deliver_item(item_2) |
| 157 | deliver_item(item_1) | move_to(shelf_2) | 0.0193 | 0.0420 | 352.3 | 352.3 | 0.0 | deliver_item(item_2) |
| 248 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0413 | 353.8 | 293.8 | 60.0 | deliver_item(item_1) |
| 251 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0012 | 0.0450 | 345.3 | 285.3 | 60.0 | deliver_item(item_1) |
| 308 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.7617 | 0.0451 | 345.0 | 345.0 | 0.0 | - |
| 309 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.2384 | 0.0420 | 352.2 | 352.2 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_0) |
| 87 | adequate | unresolved | deliver_item(item_0) |
| 88 | unresolved | adequate | deliver_item(item_0) |
| 139 | adequate | unresolved | ac_activation(ac_switch_0) |
| 140 | unresolved | adequate | ac_activation(ac_switch_0) |
| 193 | adequate | unresolved | deliver_item(item_2) |
| 194 | unresolved | adequate | deliver_item(item_2) |
| 295 | adequate | unresolved | deliver_item(item_1) |
| 296 | unresolved | adequate | deliver_item(item_1) |
| 309 | adequate | unexplained | - |

Across the started task ac_activation(ac_switch_0) (covered; actual): on top of the stack from 133 to 140, its hypothesis pinned at 139; the suspended task resumes at 141.

| tick | human action | truth | ac_activation(ac_switch_0) belief / S | coffee_break(coffee_machine_0) belief / S | deliver_item(item_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|---|---|
| 131 | move_to step | deliver_item(item_2) | 0.0245 / 0.7017 | 0.0142 / 0.3649 | retired | 0.1653 / 0.1584 | 0.7950 / 1.0000 | adequate |
| 132 | move_to  | deliver_item(item_2) | 0.0223 / 0.5973 | 0.0125 / 0.3052 | retired | 0.1426 / 0.1310 | 0.8216 / 1.0000 | adequate |
| 133 | move_to step | ac_activation(ac_switch_0) | 0.0223 / 0.5973 | 0.0125 / 0.3025 | retired | 0.1404 / 0.1285 | 0.8238 / 1.0000 | adequate |
| 134 | move_to step | ac_activation(ac_switch_0) | 0.0224 / 0.5973 | 0.0124 / 0.2993 | retired | 0.1379 / 0.1257 | 0.8263 / - | adequate |
| 135 | move_to step | ac_activation(ac_switch_0) | 0.0265 / 0.5973 | 0.0145 / 0.2952 | retired | 0.1590 / 0.1226 | 0.7990 / 0.7595 | adequate |
| 138 | move_to  | ac_activation(ac_switch_0) | 0.0467 / 1.0000 | 0.0208 / 0.2362 | retired | 0.2194 / 0.0951 | 0.7121 / 0.3345 | adequate |
| 139 | switch_on stand | ac_activation(ac_switch_0) | retired | 0.0196 / - | retired | 0.4892 / - | 0.4892 / - | unresolved |
| 140 | switch_on  | ac_activation(ac_switch_0) | retired | 0.0196 / 1.0000 | retired | 0.4892 / 1.0000 | 0.4892 / 1.0000 | adequate |
| 141 | move_to step | deliver_item(item_2) | 0.0047 / - | 0.0174 / 0.7443 | retired | 0.4367 / 0.7471 | 0.5402 / 1.0000 | adequate |
| 142 | move_to step | deliver_item(item_2) | 0.0042 / 0.7409 | 0.0150 / 0.5411 | retired | 0.3785 / 0.5454 | 0.6012 / 1.0000 | adequate |
| 143 | move_to step | deliver_item(item_2) | 0.0036 / 0.5363 | 0.0125 / 0.3855 | retired | 0.3161 / 0.3904 | 0.6667 / 1.0000 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 86, 89 to 138, 195 to 292 |
| coffee_break(coffee_machine_0) | 0 to 86, 89 to 138, 195 to 292 |
| deliver_item(item_0) | 0 to 86 |
| deliver_item(item_1) | 0 to 42, 89 to 138, 195 to 294 |
| deliver_item(item_2) | 0 to 42, 89 to 133, 141 to 192 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 47 | deliver_item(item_0) | none(below_theta) |
| 48 to 86 | deliver_item(item_0) | clears |
| 87 to 88 | deliver_item(item_1) | none(below_theta) |
| 89 to 128 | deliver_item(item_2) | none(below_theta) |
| 129 to 133 | deliver_item(item_2) | clears |
| 134 to 134 | deliver_item(item_2) | none(leader_no_observation) |
| 135 to 136 | deliver_item(item_2) | clears |
| 137 to 138 | deliver_item(item_2) | none(below_theta) |
| 139 to 140 | deliver_item(item_1) | none(below_theta) |
| 141 to 148 | deliver_item(item_2) | none(below_theta) |
| 149 to 192 | deliver_item(item_2) | clears |
| 193 to 193 | deliver_item(item_1) | none(leader_no_observation) |
| 194 to 294 | deliver_item(item_1) | clears |
| 295 to 295 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 296 to 307 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 308 to 312 | coffee_break(coffee_machine_0) | none(leader_inadequate) |
| 313 to 349 | coffee_break(coffee_machine_0) | none(below_theta) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of ac_activation | 0 to 138 ordinary, 139 to 140 retired, 141 to 349 suppressed |
| level of coffee_break | 0 to 349 ordinary |
| recency facts | 0 to 349 none |

The last entry (go_to(corner_NE)): first step 297, last step 318, acknowledgement 319; the idle human from 320. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.2012 at 297; S < α from 309 (belief 0.2384; v·D 352.2 cm); the finding unexplained from 309.

- coffee_break(coffee_machine_0): belief 0.7958 at 297; S < α from 308 (belief 0.7617; v·D 345.0 cm); the finding unexplained from 309.

