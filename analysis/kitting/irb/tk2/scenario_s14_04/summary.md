### scenario_s14_04

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_0,kitting_table_0) | covered | move_to | 0 | 1 |
| 43 | deliver_item(item_0,kitting_table_0) | covered | pick_up | 0 | 1 |
| 45 | deliver_item(item_0,kitting_table_0) | covered | move_to | 1 | 1 |
| 87 | deliver_item(item_0,kitting_table_0) | covered | place | 0 | 1 |
| 89 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 133 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 144 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 175 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 185 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 187 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 232 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 234 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 282 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 284 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 332 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 334 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 356; idle from 357 to 386. The support (prior on): ac_activation(ac_switch_0), coffee_break(coffee_machine_0), deliver_item(item_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | -1 to 177 |
| ac_activation(ac_switch_0) | switch_on(PT2S,ac_switch_0) | 178 to 179 |
| ac_activation(ac_switch_0) | move_to(ac_switch_0) | 180 to 386 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 141 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 142 to 172 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 175 to 386 |
| deliver_item(item_0) | move_to(item_0) | -1 to 40 |
| deliver_item(item_0) | pick_up(item_0) | 41 to 42 |
| deliver_item(item_0) | move_to(kitting_table_0) | 43 to 84 |
| deliver_item(item_0) | place(item_0,kitting_table_0) | 85 to 86 |
| deliver_item(item_1) | move_to(item_1) | -1 to 42 |
| deliver_item(item_1) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_1) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_1) | move_to(item_1) | 87 to 184 |
| deliver_item(item_1) | place(item_2,shelf_2) | 185 to 187 |
| deliver_item(item_1) | move_to(shelf_2) | 188 to 231 |
| deliver_item(item_1) | move_to(item_1) | 232 to 279 |
| deliver_item(item_1) | pick_up(item_1) | 280 to 281 |
| deliver_item(item_1) | move_to(kitting_table_0) | 282 to 329 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 330 to 331 |
| deliver_item(item_2) | move_to(item_2) | -1 to 42 |
| deliver_item(item_2) | place(item_0,shelf_0) | 43 to 44 |
| deliver_item(item_2) | move_to(shelf_0) | 45 to 86 |
| deliver_item(item_2) | move_to(item_2) | 87 to 130 |
| deliver_item(item_2) | pick_up(item_2) | 131 to 133 |
| deliver_item(item_2) | move_to(item_2) | 134 to 182 |
| deliver_item(item_2) | pick_up(item_2) | 183 to 184 |
| deliver_item(item_2) | move_to(kitting_table_0) | 185 to 229 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 230 to 231 |

Events (actual):

| tick | event |
|---|---|
| 87 | boundary |
| 87 | pin deliver_item(item_0) |
| 173 | boundary |
| 173 | pin coffee_break(coffee_machine_0) |
| 175 | re-entry coffee_break(coffee_machine_0) |
| 232 | boundary |
| 232 | pin deliver_item(item_2) |
| 332 | boundary |
| 332 | pin deliver_item(item_1) |
| 346 | finding turns unexplained |

Never pinned: ac_activation(ac_switch_0). At the last entry (go_to(corner_NE), ticks 334 to 356): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_0) | 0 to 88 | 48 | 0.7504 | yes | adequate |
| deliver_item(item_2) | 89 to 132 | 129 | 0.7534 | yes | adequate |
| coffee_break(coffee_machine_0) | 133 to 174 | 162 | 0.7510 | yes | adequate |
| deliver_item(item_2) | 175 to 233 | 179 | 0.7806 | yes | adequate |
| deliver_item(item_1) | 234 to 333 | 234 | 0.9757 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 42 | deliver_item(item_2) | move_to(item_2) | 0.0328 | 0.0441 | 347.1 | 327.1 | 20.0 | deliver_item(item_0) |
| 47 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0025 | 0.0445 | 346.3 | 286.3 | 60.0 | deliver_item(item_0) |
| 49 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0033 | 0.0495 | 335.5 | 275.5 | 60.0 | deliver_item(item_0) |
| 54 | deliver_item(item_1) | move_to(shelf_0) | 0.0333 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 54 | deliver_item(item_2) | move_to(shelf_0) | 0.0025 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_0) |
| 144 | deliver_item(item_2) | move_to(item_2) | 0.2979 | 0.0418 | 352.6 | 312.6 | 40.0 | coffee_break(coffee_machine_0) |
| 147 | deliver_item(item_1) | move_to(item_1) | 0.5633 | 0.0472 | 340.3 | 220.3 | 120.0 | coffee_break(coffee_machine_0) |
| 148 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0238 | 0.0421 | 352.0 | 212.0 | 140.0 | coffee_break(coffee_machine_0) |
| 183 | deliver_item(item_1) | move_to(item_1) | 0.0504 | 0.0396 | 358.2 | 358.2 | 0.0 | deliver_item(item_2) |
| 184 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0474 | 340.0 | 320.0 | 20.0 | deliver_item(item_2) |
| 191 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0022 | 0.0447 | 345.9 | 285.9 | 60.0 | deliver_item(item_2) |
| 197 | deliver_item(item_1) | move_to(shelf_2) | 0.0020 | 0.0396 | 358.2 | 358.2 | 0.0 | deliver_item(item_2) |
| 286 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.0010 | 0.0443 | 346.9 | 286.9 | 60.0 | deliver_item(item_1) |
| 289 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1112 | 0.0460 | 343.0 | 283.0 | 60.0 | deliver_item(item_1) |
| 345 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.4458 | 0.0431 | 349.5 | 349.5 | 0.0 | - |
| 346 | ac_activation(ac_switch_0) | move_to(ac_switch_0) | 0.5554 | 0.0400 | 357.1 | 357.1 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_0) |
| 87 | adequate | unresolved | deliver_item(item_0) |
| 88 | unresolved | adequate | deliver_item(item_0) |
| 173 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 174 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 232 | adequate | unresolved | deliver_item(item_2) |
| 233 | unresolved | adequate | deliver_item(item_2) |
| 332 | adequate | unresolved | deliver_item(item_1) |
| 333 | unresolved | adequate | deliver_item(item_1) |
| 346 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 133 to 174, its hypothesis pinned at 173; the suspended task resumes at 175.

| tick | human action | truth | ac_activation(ac_switch_0) belief / S | coffee_break(coffee_machine_0) belief / S | deliver_item(item_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|---|---|
| 131 | move_to step | deliver_item(item_2) | 0.0245 / 0.7017 | 0.0142 / 0.3649 | retired | 0.1653 / 0.1584 | 0.7950 / 1.0000 | adequate |
| 132 | move_to  | deliver_item(item_2) | 0.0223 / 0.5973 | 0.0125 / 0.3052 | retired | 0.1426 / 0.1310 | 0.8216 / 1.0000 | adequate |
| 133 | move_to step | coffee_break(coffee_machine_0) | 0.0221 / 0.5921 | 0.0125 / 0.3052 | retired | 0.1424 / 0.1307 | 0.8219 / 1.0000 | adequate |
| 134 | move_to step | coffee_break(coffee_machine_0) | 0.0219 / 0.5847 | 0.0125 / 0.3052 | retired | 0.1421 / 0.1304 | 0.8224 / - | adequate |
| 135 | move_to step | coffee_break(coffee_machine_0) | 0.0254 / 0.5733 | 0.0148 / 0.3052 | retired | 0.1670 / 0.1301 | 0.7918 / 0.7581 | adequate |
| 172 | wait_at stand | coffee_break(coffee_machine_0) | 0.0012 / 0.0004 | 0.9560 / 1.0000 | retired | 0.0281 / 0.0003 | 0.0136 / 0.0002 | adequate |
| 173 | wait_at stand | coffee_break(coffee_machine_0) | 0.0196 / - | retired | retired | 0.4892 / - | 0.4892 / - | unresolved |
| 174 | wait_at  | coffee_break(coffee_machine_0) | 0.0196 / 1.0000 | retired | retired | 0.4892 / 1.0000 | 0.4892 / 1.0000 | adequate |
| 175 | move_to step | deliver_item(item_2) | 0.0214 / 0.9923 | 0.0050 / - | retired | 0.4336 / 0.7425 | 0.5389 / 1.0000 | adequate |
| 176 | move_to step | deliver_item(item_2) | 0.0236 / 0.9790 | 0.0045 / 0.7402 | retired | 0.3728 / 0.5387 | 0.5982 / 1.0000 | adequate |
| 177 | move_to step | deliver_item(item_2) | 0.0255 / 0.9516 | 0.0038 / 0.5355 | retired | 0.3084 / 0.3831 | 0.6612 / 1.0000 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| ac_activation(ac_switch_0) | 0 to 86, 89 to 172, 175 to 179, 234 to 329 |
| coffee_break(coffee_machine_0) | 0 to 86, 89 to 172, 234 to 329 |
| deliver_item(item_0) | 0 to 86 |
| deliver_item(item_1) | 0 to 42, 89 to 172, 234 to 331 |
| deliver_item(item_2) | 0 to 42, 89 to 133, 175 to 231 |

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
| 137 to 140 | deliver_item(item_2) | none(below_theta) |
| 141 to 154 | deliver_item(item_1) | none(below_theta) |
| 155 to 161 | coffee_break(coffee_machine_0) | none(below_theta) |
| 162 to 172 | coffee_break(coffee_machine_0) | clears |
| 173 to 174 | deliver_item(item_1) | none(below_theta) |
| 175 to 178 | deliver_item(item_2) | none(below_theta) |
| 179 to 231 | deliver_item(item_2) | clears |
| 232 to 232 | deliver_item(item_1) | none(leader_no_observation) |
| 233 to 262 | deliver_item(item_1) | clears |
| 263 to 279 | coffee_break(coffee_machine_0) | none(below_theta) |
| 280 to 285 | deliver_item(item_1) | none(below_theta) |
| 286 to 331 | deliver_item(item_1) | clears |
| 332 to 386 | ac_activation(ac_switch_0) | none(below_theta) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of ac_activation | 0 to 386 ordinary |
| level of coffee_break | 0 to 172 ordinary, 173 to 174 retired, 175 to 262 suppressed, 263 to 299 raised, 300 to 386 ordinary |
| recency facts | 0 to 172 none, 173 to 262 coffee_break, 263 to 386 none |

The last entry (go_to(corner_NE)): first step 334, last step 355, acknowledgement 356; the idle human from 357. Live at its first tick: ac_activation(ac_switch_0), coffee_break(coffee_machine_0).

- ac_activation(ac_switch_0): belief 0.5014 at 334; S < α from 346 (belief 0.5554; v·D 357.1 cm); the finding unexplained from 346.

- coffee_break(coffee_machine_0): belief 0.4956 at 334; S < α from 345 (belief 0.4458; v·D 349.5 cm); the finding unexplained from 346.

