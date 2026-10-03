### scenario_s02_03

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 30 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 81 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 83 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 129; idle from 130 to 159. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 159 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 78 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 79 to 80 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 25 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 26 to 27 |
| office_break(office_chair) | move_to(office_door) | -1 to 159 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary |
| 28 | pin confirm_delivered_pallet(pallet_2) |
| 81 | boundary |
| 81 | pin confirm_delivered_pallet(pallet_0) |
| 133 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 83 to 129): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_2) | 0 to 29 | 25 | 0.7762 | yes | adequate |
| confirm_delivered_pallet(pallet_0) | 30 to 82 | 58 | 0.7862 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 9 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.0248 | 0.0409 | 355.0 | 355.0 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0274 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 41 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0243 | 0.0363 | 367.0 | 367.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 62 | office_break(office_chair) | move_to(office_door) | 0.0614 | 0.0488 | 337.1 | 337.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 107 | office_break(office_chair) | move_to(office_door) | 0.0820 | 0.0480 | 338.5 | 338.5 | 0.0 | - |
| 133 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9840 | 0.0418 | 352.8 | 252.8 | 100.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_2) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 81 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 82 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 133 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 27, 83 to 159 |
| confirm_delivered_pallet(pallet_0) | 30 to 80 |
| confirm_delivered_pallet(pallet_2) | 0 to 27 |
| office_break(office_chair) | 0 to 10, 30 to 78, 83 to 120 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 24 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 25 to 27 | confirm_delivered_pallet(pallet_2) | clears |
| 28 to 29 | coffee_break(coffee_machine_0) | none(below_theta) |
| 30 to 57 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 58 to 80 | confirm_delivered_pallet(pallet_0) | clears |
| 81 to 100 | coffee_break(coffee_machine_0) | none(below_theta) |
| 101 to 132 | coffee_break(coffee_machine_0) | clears |
| 133 to 159 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 83, last step 128, acknowledgement 129; the idle human from 130. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4971 at 83; S < α from 133 (belief 0.9840; v·D 352.8 cm); the finding unexplained from 133.

- office_break(office_chair): belief 0.4879 at 83; S < α from 107 (belief 0.0820; v·D 338.5 cm); the finding unexplained from 133.

