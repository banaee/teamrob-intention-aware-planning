### scenario_s08_03

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

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 31 | 8 | 0.7837 | yes | adequate |
| coffee_break(coffee_machine_0) | 32 to 85 | 55 | 0.7821 | yes | adequate |
| deliver_item(item_1) | 86 to 128 | 100 | 0.7787 | yes | adequate |
| deliver_item(item_2) | 129 to 192 | 129 | 0.9953 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0505 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 42 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0422 | 351.8 | 351.8 | 0.0 | coffee_break(coffee_machine_0) |
| 43 | deliver_item(item_1) | move_to(kitting_table_0) | 0.9180 | 0.0440 | 347.5 | 347.5 | 0.0 | coffee_break(coffee_machine_0) |
| 95 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0398 | 357.6 | 357.6 | 0.0 | deliver_item(item_1) |
| 107 | deliver_item(item_2) | move_to(shelf_1) | 0.0553 | 0.0429 | 350.0 | 350.0 | 0.0 | deliver_item(item_1) |
| 152 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0010 | 0.0431 | 349.6 | 349.6 | 0.0 | deliver_item(item_2) |
| 224 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9980 | 0.0484 | 337.8 | 337.8 | 0.0 | - |

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
| 30 | pick_up grasp | deliver_item(item_1) | 0.0063 / 0.1199 | 0.9927 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 31 | pick_up  | deliver_item(item_1) | 0.0053 / 0.0989 | 0.9937 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 32 | move_to step | coffee_break(coffee_machine_0) | 0.0060 / 0.0989 | 0.9930 / 0.8248 | 0.0010 / 1.0000 | adequate |
| 33 | move_to step | coffee_break(coffee_machine_0) | 0.0071 / 0.0989 | 0.9919 / 0.6702 | 0.0010 / - | adequate |
| 34 | move_to step | coffee_break(coffee_machine_0) | 0.0084 / 0.0989 | 0.9906 / 0.5366 | 0.0010 / 0.7594 | adequate |
| 83 | wait_at stand | coffee_break(coffee_machine_0) | 0.9980 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 84 | wait_at stand | coffee_break(coffee_machine_0) | retired | 0.4995 / - | 0.4995 / - | unresolved |
| 85 | wait_at  | coffee_break(coffee_machine_0) | retired | 0.4995 / 1.0000 | 0.4995 / 1.0000 | adequate |
| 86 | move_to step | deliver_item(item_1) | 0.0050 / - | 0.5056 / 1.0000 | 0.4894 / 0.9544 | adequate |
| 87 | move_to step | deliver_item(item_1) | 0.0041 / 0.7460 | 0.5151 / 1.0000 | 0.4808 / 0.9068 | adequate |
| 88 | move_to step | deliver_item(item_1) | 0.0032 / 0.5422 | 0.5258 / 1.0000 | 0.4710 / 0.8571 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 83, 129 to 187, 193 to 270 |
| deliver_item(item_1) | 0 to 83, 86 to 126 |
| deliver_item(item_2) | 0 to 1, 86 to 114, 129 to 190 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 7 | deliver_item(item_1) | none(below_theta) |
| 8 to 40 | deliver_item(item_1) | clears |
| 41 to 42 | deliver_item(item_1) | none(leader_outranked) |
| 43 to 47 | deliver_item(item_1) | none(leader_inadequate) |
| 48 to 50 | deliver_item(item_1) | none(below_theta) |
| 51 to 54 | coffee_break(coffee_machine_0) | none(below_theta) |
| 55 to 83 | coffee_break(coffee_machine_0) | clears |
| 84 to 99 | deliver_item(item_1) | none(below_theta) |
| 100 to 126 | deliver_item(item_1) | clears |
| 127 to 127 | deliver_item(item_2) | none(leader_no_observation) |
| 128 to 128 | deliver_item(item_2) | none(leader_unwarranted) |
| 129 to 190 | deliver_item(item_2) | clears |
| 191 to 191 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 192 to 192 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 193 to 223 | coffee_break(coffee_machine_0) | clears |
| 224 to 270 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of coffee_break | 0 to 83 ordinary, 84 to 85 retired, 86 to 173 suppressed, 174 to 270 ordinary |
| recency facts | 0 to 83 none, 84 to 173 coffee_break, 174 to 270 none |

The last entry (go_to(corner_SE)): first step 193, last step 239, acknowledgement 240; the idle human from 241. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9980 at 193; S < α from 224 (belief 0.9980; v·D 337.8 cm); the finding unexplained from 224.

