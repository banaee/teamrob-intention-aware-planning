### scenario_s08_04

Script actions (replay expanded per tick; the first tick of each action):

| tick | task | action | occurrence |
|---|---|---|---|
| 0 | deliver item_1 | move_to | 0 |
| 30 | coffee_break | move_to | 0 |
| 53 | coffee_break | wait_at | 0 |
| 84 | deliver item_1 | move_to | 0 |
| 106 | deliver item_1 | pick_up | 0 |
| 108 | deliver item_1 | move_to | 1 |
| 139 | deliver item_1 | place | 0 |
| 141 | deliver item_2 | move_to | 0 |
| 171 | deliver item_2 | pick_up | 0 |
| 173 | deliver item_2 | move_to | 1 |
| 202 | deliver item_2 | place | 0 |
| 204 | go_to(?landmark=corner_SE) | move_to | 0 |

Last acknowledgement tick 251; idle from 252 to 281.

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break | move_to(?target=coffee_machine_0) | -1 to 50 |
| coffee_break | wait_at(?duration=PT60S,?entity=coffee_machine_0) | 51 to 81 |
| deliver item_1 | move_to(?target=item_1) | -1 to 27 |
| deliver item_1 | pick_up(?item=item_1) | 28 to 30 |
| deliver item_1 | move_to(?target=item_1) | 31 to 103 |
| deliver item_1 | pick_up(?item=item_1) | 104 to 105 |
| deliver item_1 | move_to(?target=kitting_table_0) | 106 to 136 |
| deliver item_1 | place(?item=item_1,?target=kitting_table_0) | 137 to 138 |
| deliver item_2 | move_to(?target=item_2) | -1 to 105 |
| deliver item_2 | place(?item=item_1,?target=shelf_1) | 106 to 108 |
| deliver item_2 | move_to(?target=shelf_1) | 109 to 138 |
| deliver item_2 | move_to(?target=item_2) | 139 to 168 |
| deliver item_2 | pick_up(?item=item_2) | 169 to 170 |
| deliver item_2 | move_to(?target=kitting_table_0) | 171 to 199 |
| deliver item_2 | place(?item=item_2,?target=kitting_table_0) | 200 to 201 |

Events (actual):

| tick | event |
|---|---|
| 82 | boundary |
| 82 | pin coffee_break |
| 139 | boundary |
| 139 | pin deliver item_1 |
| 202 | boundary |
| 202 | exhausted (no live hypothesis) from here |
| 202 | pin deliver item_2 |

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| deliver item_1 | 0 to 29 | 25 | 0.7552 | yes | adequate |
| coffee_break | 30 to 83 | 40 | 0.7678 | yes | adequate |
| deliver item_1 | 84 to 140 | 91 | 0.7854 | yes | adequate |
| deliver item_2 | 141 to 203 | 141 | 0.9980 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 14 | deliver item_2 | move_to(?target=item_2) | 0.0315 | 0.0399 | 357.3 | 357.3 | 0.0 | deliver item_1 |
| 40 | deliver item_1 | move_to(?target=item_1) | 0.2312 | 0.0422 | 351.8 | 351.8 | 0.0 | coffee_break |
| 97 | deliver item_2 | move_to(?target=item_2) | 0.0578 | 0.0450 | 345.2 | 345.2 | 0.0 | deliver item_1 |
| 118 | deliver item_2 | move_to(?target=shelf_1) | 0.0010 | 0.0395 | 358.3 | 358.3 | 0.0 | deliver item_1 |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | deliver item_1 |
| 82 | adequate | unresolved | coffee_break |
| 83 | unresolved | adequate | coffee_break |
| 139 | adequate | unresolved | deliver item_1 |
| 140 | unresolved | adequate | deliver item_1 |
| 202 | adequate | exhausted | deliver item_2 |

Across the coffee boundary (actual): the coffee_break starts at 30 (its walk), is pinned at 82 (the boundary), and the suspended delivery resumes at 84.

| tick | human action | truth | coffee_break belief / S | deliver item_1 belief / S | deliver item_2 belief / S | finding |
|---|---|---|---|---|---|---|
| 28 | move_to step | deliver item_1 | 0.1861 / 0.1754 | 0.8129 / 1.0000 | 0.0010 / 0.0005 | adequate |
| 29 | move_to  | deliver item_1 | 0.1605 / 0.1451 | 0.8385 / 1.0000 | 0.0010 / 0.0004 | adequate |
| 30 | move_to step | coffee_break | 0.1605 / 0.1451 | 0.8385 / 1.0000 | 0.0010 / 0.0004 | adequate |
| 31 | move_to step | coffee_break | 0.1605 / 0.1451 | 0.8385 / - | 0.0010 / 0.0004 | adequate |
| 32 | move_to step | coffee_break | 0.1893 / 0.1451 | 0.8097 / 0.7594 | 0.0010 / 0.0003 | adequate |
| 81 | wait_at stand | coffee_break | 0.9980 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 82 | wait_at stand | coffee_break | retired | 0.4995 / - | 0.4995 / - | unresolved |
| 83 | wait_at  | coffee_break | retired | 0.4995 / 1.0000 | 0.4995 / 1.0000 | adequate |
| 84 | move_to step | deliver item_1 | retired | 0.5273 / 1.0000 | 0.4717 / 0.8554 | adequate |
| 85 | move_to step | deliver item_1 | retired | 0.5585 / 1.0000 | 0.4405 / 0.7235 | adequate |
| 86 | move_to step | deliver item_1 | retired | 0.5928 / 1.0000 | 0.4062 / 0.6050 | adequate |

Exit walk (go_to corner_SE): first step 204, last step 250, acknowledgement 251; the idle human from 252. Live at its first tick: none (exhausted).

