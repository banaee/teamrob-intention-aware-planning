### scenario_s09_03

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 55 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 86 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 127 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 129 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 159 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 161 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 191 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 193 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 240; idle from 241 to 270. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 52 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 53 to 83 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 86 to 270 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 124 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 125 to 126 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1,shelf_1) | 30 to 32 |
| deliver_item(item_2) | move_to(shelf_1) | 33 to 126 |
| deliver_item(item_2) | move_to(item_2) | 127 to 156 |
| deliver_item(item_2) | pick_up(item_2) | 157 to 158 |
| deliver_item(item_2) | move_to(kitting_table_0) | 159 to 188 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 189 to 190 |

Events (actual):

| tick | event |
|---|---|
| 84 | boundary |
| 84 | pin coffee_break(coffee_machine_0) |
| 86 | re-entry coffee_break(coffee_machine_0) |
| 127 | boundary |
| 127 | pin deliver_item(item_1) |
| 191 | boundary |
| 191 | pin deliver_item(item_2) |
| 224 | finding turns unexplained |

Never pinned: none. At the last entry (go_to(corner_SE), ticks 193 to 240): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 31 | 25 | 0.7544 | yes | adequate |
| coffee_break(coffee_machine_0) | 32 to 85 | 45 | 0.8036 | yes | adequate |
| deliver_item(item_1) | 86 to 128 | 100 | 0.7735 | yes | adequate |
| deliver_item(item_2) | 129 to 192 | 142 | 0.7594 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 42 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0422 | 351.8 | 351.8 | 0.0 | coffee_break(coffee_machine_0) |
| 43 | deliver_item(item_1) | move_to(kitting_table_0) | 0.3114 | 0.0440 | 347.5 | 347.5 | 0.0 | coffee_break(coffee_machine_0) |
| 95 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0332 | 0.0398 | 357.6 | 357.6 | 0.0 | deliver_item(item_1) |
| 107 | deliver_item(item_2) | move_to(shelf_1) | 0.0553 | 0.0429 | 350.0 | 350.0 | 0.0 | deliver_item(item_1) |
| 152 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0555 | 0.0431 | 349.6 | 349.6 | 0.0 | deliver_item(item_2) |
| 224 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0484 | 337.8 | 337.8 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 84 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 85 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 127 | adequate | unresolved | deliver_item(item_1) |
| 128 | unresolved | adequate | deliver_item(item_1) |
| 191 | adequate | unresolved | deliver_item(item_2) |
| 192 | unresolved | adequate | deliver_item(item_2) |
| 224 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 32 to 85, its hypothesis pinned at 84; the suspended task resumes at 86.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|
| 30 | pick_up grasp | deliver_item(item_1) | 0.1373 / 0.1199 | 0.8608 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 31 | pick_up  | deliver_item(item_1) | 0.1167 / 0.0989 | 0.8813 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 32 | move_to step | coffee_break(coffee_machine_0) | 0.1318 / 0.0989 | 0.8662 / 0.8248 | 0.0010 / 1.0000 | adequate |
| 33 | move_to step | coffee_break(coffee_machine_0) | 0.1510 / 0.0989 | 0.8470 / 0.6702 | 0.0010 / - | adequate |
| 34 | move_to step | coffee_break(coffee_machine_0) | 0.1754 / 0.0989 | 0.8226 / 0.5366 | 0.0010 / 0.7594 | adequate |
| 83 | wait_at stand | coffee_break(coffee_machine_0) | 0.9970 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 84 | wait_at stand | coffee_break(coffee_machine_0) | retired | 0.4990 / - | 0.4990 / - | unresolved |
| 85 | wait_at  | coffee_break(coffee_machine_0) | retired | 0.4990 / 1.0000 | 0.4990 / 1.0000 | adequate |
| 86 | move_to step | deliver_item(item_1) | 0.3330 / - | 0.3384 / 1.0000 | 0.3276 / 0.9544 | adequate |
| 87 | move_to step | deliver_item(item_1) | 0.2910 / 0.7460 | 0.3662 / 1.0000 | 0.3418 / 0.9068 | adequate |
| 88 | move_to step | deliver_item(item_1) | 0.2451 / 0.5422 | 0.3976 / 1.0000 | 0.3562 / 0.8571 | adequate |

The last entry (go_to(corner_SE)): first step 193, last step 239, acknowledgement 240; the idle human from 241. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 193; S < α from 224 (belief 0.9970; v·D 337.8 cm); the finding unexplained from 224.

