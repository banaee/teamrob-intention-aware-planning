### scenario_s13_14

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
| 124 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 169 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 171 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 215 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 217 | deliver_item(item_4,kitting_table_0) | covered | move_to | 0 | 1 |
| 261 | deliver_item(item_4,kitting_table_0) | covered | pick_up | 0 | 1 |
| 263 | deliver_item(item_4,kitting_table_0) | covered | move_to | 1 | 1 |
| 307 | deliver_item(item_4,kitting_table_0) | covered | place | 0 | 1 |
| 309 | go_to(corner_NE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 330; idle from 331 to 360. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2), deliver_item(item_3), deliver_item(item_4).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 360 |
| deliver_item(item_1) | move_to(item_1) | -1 to 31 |
| deliver_item(item_1) | place(item_3,shelf_3) | 32 to 33 |
| deliver_item(item_1) | move_to(shelf_3) | 34 to 64 |
| deliver_item(item_1) | move_to(item_1) | 65 to 93 |
| deliver_item(item_1) | place(item_2,shelf_2) | 94 to 95 |
| deliver_item(item_1) | move_to(shelf_2) | 96 to 121 |
| deliver_item(item_1) | move_to(item_1) | 122 to 166 |
| deliver_item(item_1) | pick_up(item_1) | 167 to 168 |
| deliver_item(item_1) | move_to(kitting_table_0) | 169 to 212 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 213 to 214 |
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
| deliver_item(item_4) | move_to(item_4) | 122 to 168 |
| deliver_item(item_4) | place(item_1,shelf_1) | 169 to 170 |
| deliver_item(item_4) | move_to(shelf_1) | 171 to 214 |
| deliver_item(item_4) | move_to(item_4) | 215 to 258 |
| deliver_item(item_4) | pick_up(item_4) | 259 to 260 |
| deliver_item(item_4) | move_to(kitting_table_0) | 261 to 304 |
| deliver_item(item_4) | place(item_4,kitting_table_0) | 305 to 306 |

Events (actual):

| tick | event |
|---|---|
| 65 | boundary |
| 65 | pin deliver_item(item_3) |
| 122 | boundary |
| 122 | pin deliver_item(item_2) |
| 215 | boundary |
| 215 | pin deliver_item(item_1) |
| 307 | boundary |
| 307 | pin deliver_item(item_4) |
| 331 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_NE), ticks 309 to 330): lifecycle and finding adequate; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_3) | 0 to 66 | 27 | 0.7656 | yes | adequate |
| deliver_item(item_2) | 67 to 123 | 102 | 0.8089 | yes | adequate |
| deliver_item(item_1) | 124 to 216 | 162 | 0.7658 | yes | adequate |
| deliver_item(item_4) | 217 to 308 | 253 | 0.7578 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 12 | deliver_item(item_2) | move_to(item_2) | 0.0152 | 0.0383 | 361.6 | 361.6 | 0.0 | deliver_item(item_3) |
| 16 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.2262 | 0.0495 | 335.5 | 335.5 | 0.0 | deliver_item(item_3) |
| 25 | deliver_item(item_4) | move_to(item_4) | 0.0428 | 0.0441 | 347.2 | 347.2 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_1) | move_to(shelf_3) | 0.0058 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_2) | move_to(shelf_3) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 43 | deliver_item(item_4) | move_to(shelf_3) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_3) |
| 87 | deliver_item(item_1) | move_to(item_1) | 0.0105 | 0.0418 | 352.6 | 352.6 | 0.0 | deliver_item(item_2) |
| 101 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.2356 | 0.0383 | 361.4 | 301.4 | 60.0 | deliver_item(item_2) |
| 105 | deliver_item(item_1) | move_to(shelf_2) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 105 | deliver_item(item_4) | move_to(shelf_2) | 0.0035 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_2) |
| 153 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1462 | 0.0498 | 334.8 | 334.8 | 0.0 | deliver_item(item_1) |
| 180 | deliver_item(item_4) | move_to(shelf_1) | 0.0041 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 258 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1051 | 0.0431 | 349.5 | 349.5 | 0.0 | deliver_item(item_4) |
| 331 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9960 | 0.0467 | 341.4 | 301.4 | 40.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_3) |
| 65 | adequate | unresolved | deliver_item(item_3) |
| 66 | unresolved | adequate | deliver_item(item_3) |
| 122 | adequate | unresolved | deliver_item(item_2) |
| 123 | unresolved | adequate | deliver_item(item_2) |
| 215 | adequate | unresolved | deliver_item(item_1) |
| 216 | unresolved | adequate | deliver_item(item_1) |
| 307 | adequate | unresolved | deliver_item(item_4) |
| 308 | unresolved | adequate | deliver_item(item_4) |
| 331 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 17, 46 to 64, 67 to 121, 124 to 214, 217 to 306, 309 to 360 |
| deliver_item(item_1) | 0 to 31, 67 to 93, 124 to 214 |
| deliver_item(item_2) | 67 to 121 |
| deliver_item(item_3) | 0 to 64 |
| deliver_item(item_4) | 0 to 31, 67 to 93, 124 to 168, 217 to 306 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 13 | coffee_break(coffee_machine_0) | none(below_theta) |
| 14 to 26 | deliver_item(item_3) | none(below_theta) |
| 27 to 64 | deliver_item(item_3) | clears |
| 65 to 80 | coffee_break(coffee_machine_0) | none(below_theta) |
| 81 to 91 | coffee_break(coffee_machine_0) | clears |
| 92 to 97 | coffee_break(coffee_machine_0) | none(below_theta) |
| 98 to 101 | deliver_item(item_2) | none(below_theta) |
| 102 to 121 | deliver_item(item_2) | clears |
| 122 to 144 | coffee_break(coffee_machine_0) | none(below_theta) |
| 145 to 161 | deliver_item(item_1) | none(below_theta) |
| 162 to 214 | deliver_item(item_1) | clears |
| 215 to 242 | coffee_break(coffee_machine_0) | none(below_theta) |
| 243 to 252 | deliver_item(item_4) | none(below_theta) |
| 253 to 306 | deliver_item(item_4) | clears |
| 307 to 307 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 308 to 308 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 309 to 330 | coffee_break(coffee_machine_0) | clears |
| 331 to 360 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of coffee_break | 0 to 360 raised |
| recency facts | 0 to 360 none |

The last entry (go_to(corner_NE)): first step 309, last step 329, acknowledgement 330; the idle human from 331. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9960 at 309; S < α from 331 (belief 0.9960; v·D 341.4 cm); the finding unexplained from 331.

