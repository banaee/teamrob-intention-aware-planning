### scenario_s09_06

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 30 | stand(PT80S) | task_absent | stand | 0 | 2 |
| 71 | deliver_item(item_1,kitting_table_0) | covered | move_to | 0 | 1 |
| 72 | deliver_item(item_1,kitting_table_0) | covered | pick_up | 0 | 1 |
| 74 | deliver_item(item_1,kitting_table_0) | covered | move_to | 1 | 1 |
| 103 | deliver_item(item_1,kitting_table_0) | covered | place | 0 | 1 |
| 105 | deliver_item(item_2,kitting_table_0) | covered | move_to | 0 | 1 |
| 135 | deliver_item(item_2,kitting_table_0) | covered | pick_up | 0 | 1 |
| 137 | deliver_item(item_2,kitting_table_0) | covered | move_to | 1 | 1 |
| 166 | deliver_item(item_2,kitting_table_0) | covered | place | 0 | 1 |
| 168 | go_to(corner_SE) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 215; idle from 216 to 245. The support (prior on): coffee_break(coffee_machine_0), deliver_item(item_1), deliver_item(item_2).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 245 |
| deliver_item(item_1) | move_to(item_1) | -1 to 27 |
| deliver_item(item_1) | pick_up(item_1) | 28 to 71 |
| deliver_item(item_1) | move_to(kitting_table_0) | 72 to 100 |
| deliver_item(item_1) | place(item_1,kitting_table_0) | 101 to 102 |
| deliver_item(item_2) | move_to(item_2) | -1 to 71 |
| deliver_item(item_2) | place(item_1,shelf_1) | 72 to 73 |
| deliver_item(item_2) | move_to(shelf_1) | 74 to 102 |
| deliver_item(item_2) | move_to(item_2) | 103 to 132 |
| deliver_item(item_2) | pick_up(item_2) | 133 to 134 |
| deliver_item(item_2) | move_to(kitting_table_0) | 135 to 163 |
| deliver_item(item_2) | place(item_2,kitting_table_0) | 164 to 165 |

Events (actual):

| tick | event |
|---|---|
| 47 | finding turns unexplained |
| 72 | finding turns adequate (from unexplained) |
| 103 | boundary |
| 103 | pin deliver_item(item_1) |
| 166 | boundary |
| 166 | pin deliver_item(item_2) |
| 199 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(corner_SE), ticks 168 to 215): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ (the belief over H, the value the gate reads; AM42), its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver_item(item_1) | 0 to 29 | 8 | 0.7837 | yes | adequate |
| deliver_item(item_1) | 71 to 104 | 71 | 0.9963 | yes | inadequate |
| deliver_item(item_2) | 105 to 167 | 105 | 0.9813 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver_item(item_2) | move_to(item_2) | 0.0504 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver_item(item_1) |
| 35 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0046 | 0.0453 | 344.6 | 204.6 | 140.0 | - |
| 47 | deliver_item(item_1) | pick_up(item_1) | 0.9945 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 83 | deliver_item(item_2) | move_to(shelf_1) | 0.0010 | 0.0389 | 360.0 | 360.0 | 0.0 | deliver_item(item_1) |
| 128 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0012 | 0.0453 | 344.4 | 344.4 | 0.0 | deliver_item(item_2) |
| 199 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9970 | 0.0456 | 343.9 | 343.9 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver_item(item_1) |
| 47 | adequate | unexplained | - |
| 72 | unexplained | adequate | deliver_item(item_1) |
| 103 | adequate | unresolved | deliver_item(item_1) |
| 104 | unresolved | adequate | deliver_item(item_1) |
| 166 | adequate | unresolved | deliver_item(item_2) |
| 167 | unresolved | adequate | deliver_item(item_2) |
| 199 | adequate | unexplained | - |

Across the started task stand(PT80S) (task_absent; actual): on top of the stack from 30 to 70, no pin; the suspended task resumes at 71.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | deliver_item(item_1) belief / S | deliver_item(item_2) belief / S | finding |
|---|---|---|---|---|---|---|
| 28 | move_to step | deliver_item(item_1) | 0.0091 / 0.1754 | 0.9889 / 1.0000 | 0.0010 / 0.0005 | adequate |
| 29 | move_to  | deliver_item(item_1) | 0.0076 / 0.1451 | 0.9904 / 1.0000 | 0.0010 / 0.0004 | adequate |
| 30 | stand stand | - | 0.0063 / 0.1199 | 0.9917 / 1.0000 | 0.0010 / 0.0003 | adequate |
| 31 | stand stand | - | 0.0058 / 0.0989 | 0.9922 / 0.8629 | 0.0010 / 0.0003 | adequate |
| 32 | stand stand | - | 0.0054 / 0.0814 | 0.9926 / 0.7401 | 0.0010 / 0.0002 | adequate |
| 69 | stand stand | - | 0.0034 / 0.0001 | 0.9946 / 0.0006 | 0.0010 / 0.0000 | unexplained |
| 70 | stand  | - | 0.0034 / 0.0000 | 0.9946 / 0.0005 | 0.0010 / 0.0000 | unexplained |
| 71 | move_to  | deliver_item(item_1) | 0.0034 / 0.0000 | 0.9946 / 0.0004 | 0.0010 / 0.0000 | unexplained |
| 72 | pick_up grasp | deliver_item(item_1) | 0.0034 / 0.0000 | 0.9946 / 1.0000 | 0.0010 / 1.0000 | adequate |
| 73 | pick_up  | deliver_item(item_1) | 0.0028 / 0.0000 | 0.9952 / 1.0000 | 0.0010 / 1.0000 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 102, 105 to 163, 168 to 245 |
| deliver_item(item_1) | 0 to 102 |
| deliver_item(item_2) | 0 to 1, 105 to 165 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 7 | deliver_item(item_1) | none(below_theta) |
| 8 to 46 | deliver_item(item_1) | clears |
| 47 to 71 | deliver_item(item_1) | none(leader_inadequate) |
| 72 to 102 | deliver_item(item_1) | clears |
| 103 to 103 | deliver_item(item_2) | none(leader_no_observation) |
| 104 to 104 | deliver_item(item_2) | none(leader_unwarranted) |
| 105 to 165 | deliver_item(item_2) | clears |
| 166 to 166 | coffee_break(coffee_machine_0) | none(leader_no_observation) |
| 167 to 167 | coffee_break(coffee_machine_0) | none(leader_unwarranted) |
| 168 to 198 | coffee_break(coffee_machine_0) | clears |
| 199 to 245 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

Context knowledge (actual): per foreseeable task its level, and the recency facts, as stretches of ticks (the prior's inputs; `[IR-context]`).

| what | stretches |
|---|---|
| level of coffee_break | 0 to 245 ordinary |
| recency facts | 0 to 245 none |

The last entry (go_to(corner_SE)): first step 168, last step 214, acknowledgement 215; the idle human from 216. Live at its first tick: coffee_break(coffee_machine_0).

- coffee_break(coffee_machine_0): belief 0.9970 at 168; S < α from 199 (belief 0.9970; v·D 343.9 cm); the finding unexplained from 199.

