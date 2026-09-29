### scenario_s09_13

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 46 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 76 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 107 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 148 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 149 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 151 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 181 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 183 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 212 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 214 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 261; idle from 262 to 291. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 73 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 74 to 104 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 107 to 291 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 145 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 146 to 148 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1,shelf_1) | 30 to 31 |
| deliver_item(item_2) | move_to(shelf_1) | 32 to 148 |
| deliver_item(item_2) | move_to(item_2) | 149 to 178 |
| deliver_item(item_2) | pick_up(item_2) | 179 to 180 |
| deliver_item(item_2) | move_to(kitting_table_0) | 181 to 209 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 210 to 211 |

Events (actual):

| tick | event |
|---|---|
| 55 | finding turns unexplained |
| 74 | finding turns adequate (from unexplained) |
| 105 | boundary |
| 105 | pin coffee_break(coffee_machine_0) |
| 107 | re-entry coffee_break(coffee_machine_0) |
| 149 | boundary |
| 149 | pin deliver_item(item_1) |
| 212 | boundary |
| 212 | pin deliver_item(item_2) |
| 245 | finding turns unexplained |

Never pinned: none. At the last entry (go_to(corner_SE), ticks 214 to 261): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 45 | 25 | 0.7544 | yes | adequate |
| coffee_break(coffee_machine_0) | 46 to 106 | 67 | 0.7904 | yes | inadequate |
| deliver_item(item_1) | 107 to 150 | 121 | 0.7794 | yes | adequate |
| deliver_item(item_2) | 151 to 213 | 164 | 0.7548 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 34 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0579 | 0.0451 | 345.0 | 285.0 | 60.0 | deliver_item(item_1) |
| 41 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 55 | deliver_item(item_1) | move_to(kitting_table_0) | 0.9604 | 0.0389 | 359.9 | 359.9 | 0.0 | coffee_break(coffee_machine_0) |
| 116 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0328 | 0.0390 | 359.6 | 359.6 | 0.0 | deliver_item(item_1) |
| 128 | deliver_item(item_2) | move_to(shelf_1) | 0.0527 | 0.0408 | 355.1 | 355.1 | 0.0 | deliver_item(item_1) |
| 174 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0586 | 0.0457 | 343.7 | 343.7 | 0.0 | deliver_item(item_2) |
| 245 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0435 | 348.6 | 348.6 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 55 | adequate | unexplained | coffee_break(coffee_machine_0) |
| 74 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 105 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 106 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 149 | adequate | unresolved | deliver_item(item_1) |
| 150 | unresolved | adequate | deliver_item(item_1) |
| 212 | adequate | unresolved | deliver_item(item_2) |
| 213 | unresolved | adequate | deliver_item(item_2) |
| 245 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 46 to 106, its hypothesis pinned at 105; the suspended task resumes at 107.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|
| 44 | move_to step | deliver_item(item_1) | 0.0029 / 0.0021 | 0.9951 / 1.0000 | 0.0010 / 0.0118 | adequate |
| 45 | move_to step | deliver_item(item_1) | 0.0021 / 0.0015 | 0.9959 / 1.0000 | 0.0010 / 0.0079 | adequate |
| 46 | move_to step | coffee_break(coffee_machine_0) | 0.0025 / 0.0015 | 0.9955 / 0.7759 | 0.0010 / 0.0074 | adequate |
| 47 | move_to step | coffee_break(coffee_machine_0) | 0.0031 / 0.0015 | 0.9949 / 0.5889 | 0.0010 / 0.0069 | adequate |
| 48 | move_to step | coffee_break(coffee_machine_0) | 0.0039 / 0.0015 | 0.9941 / 0.4381 | 0.0010 / 0.0063 | adequate |
| 104 | wait_at stand | coffee_break(coffee_machine_0) | 0.9970 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 105 | wait_at stand | coffee_break(coffee_machine_0) | retired | 0.4990 / - | 0.4990 / - | unresolved |
| 106 | wait_at  | coffee_break(coffee_machine_0) | retired | 0.4990 / 1.0000 | 0.4990 / 1.0000 | adequate |
| 107 | move_to step | deliver_item(item_1) | 0.3330 / - | 0.3386 / 1.0000 | 0.3274 / 0.9529 | adequate |
| 108 | move_to step | deliver_item(item_1) | 0.2901 / 0.7410 | 0.3671 / 1.0000 | 0.3418 / 0.9038 | adequate |
| 109 | move_to step | deliver_item(item_1) | 0.2437 / 0.5364 | 0.3991 / 1.0000 | 0.3562 / 0.8526 | adequate |

The last entry (go_to(corner_SE)): first step 214, last step 260, acknowledgement 261; the idle human from 262. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 214; S < α from 245 (belief 0.9970; v·D 348.6 cm); the finding unexplained from 245.

