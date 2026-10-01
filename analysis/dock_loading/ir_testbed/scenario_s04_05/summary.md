### scenario_s04_05

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 30 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 82 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 84 | confirm_delivered_pallet(pallet_1) | covered | move_to | 0 | 1 |
| 136 | confirm_delivered_pallet(pallet_1) | covered | scan_it | 0 | 1 |
| 138 | confirm_delivered_pallet(pallet_3) | covered | move_to | 0 | 1 |
| 190 | confirm_delivered_pallet(pallet_3) | covered | scan_it | 0 | 1 |
| 192 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 208; idle from 209 to 238. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_1), confirm_delivered_pallet(pallet_2), confirm_delivered_pallet(pallet_3), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 238 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 27 |
| confirm_delivered_pallet(pallet_1) | move_to(pallet_1) | -1 to 25 |
| confirm_delivered_pallet(pallet_1) | scan_it(pallet_1) | 26 to 29 |
| confirm_delivered_pallet(pallet_1) | move_to(pallet_1) | 30 to 133 |
| confirm_delivered_pallet(pallet_1) | scan_it(pallet_1) | 134 to 135 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 79 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 80 to 81 |
| confirm_delivered_pallet(pallet_3) | move_to(pallet_3) | -1 to 79 |
| confirm_delivered_pallet(pallet_3) | scan_it(pallet_3) | 80 to 83 |
| confirm_delivered_pallet(pallet_3) | move_to(pallet_3) | 84 to 187 |
| confirm_delivered_pallet(pallet_3) | scan_it(pallet_3) | 188 to 189 |
| office_break(office_chair) | move_to(office_door) | -1 to 238 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary |
| 28 | pin confirm_delivered_pallet(pallet_0) |
| 82 | boundary |
| 82 | pin confirm_delivered_pallet(pallet_2) |
| 136 | boundary |
| 136 | pin confirm_delivered_pallet(pallet_1) |
| 190 | boundary |
| 190 | pin confirm_delivered_pallet(pallet_3) |
| 219 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 192 to 208): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 29 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_2) | 30 to 83 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_1) | 84 to 137 | 118 | 0.7664 | yes | adequate |
| confirm_delivered_pallet(pallet_3) | 138 to 191 | 162 | 0.7718 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0195 | 0.0431 | 349.6 | 349.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 8 | confirm_delivered_pallet(pallet_3) | move_to(pallet_3) | 0.0195 | 0.0431 | 349.6 | 349.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0225 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 20 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0278 | 0.0427 | 350.6 | 350.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 39 | confirm_delivered_pallet(pallet_1) | move_to(pallet_1) | 0.0161 | 0.0389 | 359.9 | 359.9 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 47 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0201 | 0.0403 | 356.5 | 356.5 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 60 | office_break(office_chair) | move_to(office_door) | 0.0266 | 0.0405 | 355.8 | 355.8 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 93 | confirm_delivered_pallet(pallet_3) | move_to(pallet_3) | 0.0185 | 0.0389 | 360.0 | 360.0 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 118 | office_break(office_chair) | move_to(office_door) | 0.0416 | 0.0397 | 357.9 | 357.9 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 126 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0583 | 0.0462 | 342.4 | 342.4 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 155 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0321 | 0.0407 | 355.4 | 355.4 | 0.0 | confirm_delivered_pallet(pallet_3) |
| 168 | office_break(office_chair) | move_to(office_door) | 0.0516 | 0.0405 | 356.0 | 356.0 | 0.0 | confirm_delivered_pallet(pallet_3) |
| 206 | office_break(office_chair) | move_to(office_door) | 0.0972 | 0.0470 | 340.8 | 340.8 | 0.0 | - |
| 219 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9223 | 0.0490 | 336.4 | 96.4 | 240.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 82 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 83 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 136 | adequate | unresolved | confirm_delivered_pallet(pallet_1) |
| 137 | unresolved | adequate | confirm_delivered_pallet(pallet_1) |
| 190 | adequate | unresolved | confirm_delivered_pallet(pallet_3) |
| 191 | unresolved | adequate | confirm_delivered_pallet(pallet_3) |
| 219 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 27, 30 to 47, 84 to 135, 138 to 155, 192 to 238 |
| confirm_delivered_pallet(pallet_0) | 0 to 27 |
| confirm_delivered_pallet(pallet_1) | 0 to 27, 84 to 135 |
| confirm_delivered_pallet(pallet_2) | 30 to 81 |
| confirm_delivered_pallet(pallet_3) | 30 to 81, 138 to 189 |
| office_break(office_chair) | 0 to 10, 30 to 75, 84 to 135, 138 to 183, 192 to 197 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 27 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 28 to 29 | coffee_break(coffee_machine_0) | none(below_theta) |
| 30 to 30 | confirm_delivered_pallet(pallet_1) | none(below_theta) |
| 31 to 81 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 82 to 83 | coffee_break(coffee_machine_0) | none(below_theta) |
| 84 to 84 | confirm_delivered_pallet(pallet_3) | none(below_theta) |
| 85 to 117 | confirm_delivered_pallet(pallet_1) | none(below_theta) |
| 118 to 135 | confirm_delivered_pallet(pallet_1) | clears |
| 136 to 137 | coffee_break(coffee_machine_0) | none(below_theta) |
| 138 to 161 | confirm_delivered_pallet(pallet_3) | none(below_theta) |
| 162 to 189 | confirm_delivered_pallet(pallet_3) | clears |
| 190 to 200 | coffee_break(coffee_machine_0) | none(below_theta) |
| 201 to 218 | coffee_break(coffee_machine_0) | clears |
| 219 to 238 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 192, last step 207, acknowledgement 208; the idle human from 209. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.5102 at 192; S < α from 219 (belief 0.9223; v·D 336.4 cm); the finding unexplained from 219.

- office_break(office_chair): belief 0.4748 at 192; S < α from 206 (belief 0.0972; v·D 340.8 cm); the finding unexplained from 219.

