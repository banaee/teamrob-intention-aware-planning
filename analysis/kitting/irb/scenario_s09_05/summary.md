### scenario_s09_05

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 32 | go_to(corner_SE) | task_absent | move_to | 0 | 2 |
| 80 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 128 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 130 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 159 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 161 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 190 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 192 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 239; idle from 240 to 269. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 269 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 29 |
| deliver_item(item_1) | move_to(kitting_table_0) | 30 to 125 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 126 to 127 |
| deliver_item(item_2) | move_to(item_2) | -1 to 29 |
| deliver_item(item_2) | place(item_1,shelf_1) | 30 to 31 |
| deliver_item(item_2) | move_to(shelf_1) | 32 to 127 |
| deliver_item(item_2) | move_to(item_2) | 128 to 156 |
| deliver_item(item_2) | pick_up(item_2) | 157 to 158 |
| deliver_item(item_2) | move_to(kitting_table_0) | 159 to 187 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 188 to 189 |

Events (actual):

| tick | event |
|---|---|
| 48 | finding turns unexplained |
| 126 | finding turns adequate (from unexplained) |
| 128 | boundary |
| 128 | pin deliver_item(item_1) |
| 190 | boundary |
| 190 | pin deliver_item(item_2) |
| 223 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_SE), ticks 192 to 239): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 31 | 25 | 0.7544 | yes | adequate |
| deliver_item(item_1) | 80 to 129 | 87 | 0.7671 | yes | inadequate |
| deliver_item(item_2) | 130 to 191 | 143 | 0.7580 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 41 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0427 | 350.6 | 350.6 | 0.0 | - |
| 44 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.2906 | 0.0467 | 341.3 | 281.3 | 60.0 | - |
| 48 | deliver_item(item_1) | move_to(kitting_table_0) | 0.6104 | 0.0441 | 347.3 | 347.3 | 0.0 | - |
| 153 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0565 | 0.0440 | 347.5 | 347.5 | 0.0 | deliver_item(item_2) |
| 223 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0457 | 343.6 | 343.6 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 48 | adequate | unexplained | - |
| 126 | unexplained | adequate | deliver_item(item_1) |
| 128 | adequate | unresolved | deliver_item(item_1) |
| 129 | unresolved | adequate | deliver_item(item_1) |
| 190 | adequate | unresolved | deliver_item(item_2) |
| 191 | unresolved | adequate | deliver_item(item_2) |
| 223 | adequate | unexplained | - |

Across the started task go_to(corner_SE) (task_absent; actual): on top of the stack from 32 to 79, no pin; the suspended task resumes at 80.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|
| 30 | pick_up grasp | deliver_item(item_1) | 0.1373 / 0.1199 | 0.8608 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 31 | pick_up  | deliver_item(item_1) | 0.1167 / 0.0989 | 0.8813 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 32 | move_to step | - | 0.1217 / 0.0959 | 0.8763 / 0.8966 | 0.0010 / - | adequate |
| 33 | move_to step | - | 0.1276 / 0.0927 | 0.8704 / 0.7971 | 0.0010 / 0.7631 | adequate |
| 34 | move_to step | - | 0.1345 / 0.0894 | 0.8635 / 0.7024 | 0.0010 / 0.5622 | adequate |
| 78 | move_to step | - | 0.4421 / 0.0000 | 0.5559 / 0.0000 | 0.0010 / 0.0000 | unexplained |
| 79 | move_to  | - | 0.4421 / 0.0000 | 0.5559 / 0.0000 | 0.0010 / 0.0000 | unexplained |
| 80 | move_to step | deliver_item(item_1) | 0.4173 / 0.0000 | 0.5807 / 0.0000 | 0.0010 / 0.0000 | unexplained |
| 81 | move_to step | deliver_item(item_1) | 0.3917 / 0.0000 | 0.6064 / 0.0000 | 0.0010 / 0.0000 | unexplained |
| 82 | move_to step | deliver_item(item_1) | 0.3653 / 0.0000 | 0.6327 / 0.0000 | 0.0010 / 0.0000 | unexplained |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 127, 130 to 187, 192 to 269 |
| deliver_item(item_1) | 0 to 127 |
| deliver_item(item_2) | 0 to 1, 130 to 189 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 24 | deliver_item(item_1) | none(below_theta) |
| 25 to 42 | deliver_item(item_1) | clears |
| 43 to 54 | deliver_item(item_1) | none(below_theta) |
| 55 to 66 | coffee_break(coffee_machine_0) | none(below_theta) |
| 67 to 86 | deliver_item(item_1) | none(below_theta) |
| 87 to 125 | deliver_item(item_1) | none(leader_inadequate) |
| 126 to 127 | deliver_item(item_1) | clears |
| 128 to 129 | coffee_break(coffee_machine_0) | none(below_theta) |
| 130 to 142 | deliver_item(item_2) | none(below_theta) |
| 143 to 189 | deliver_item(item_2) | clears |
| 190 to 190 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 191 to 191 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 192 to 222 | coffee_break(coffee_machine_0) | clears |
| 223 to 269 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(corner_SE)): first step 192, last step 238, acknowledgement 239; the idle human from 240. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 192; S < α from 223 (belief 0.9970; v·D 343.6 cm); the finding unexplained from 223.

