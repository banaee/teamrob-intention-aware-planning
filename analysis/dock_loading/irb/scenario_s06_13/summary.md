### scenario_s06_13

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_1) | covered | move_to | 0 | 1 |
| 17 | confirm_delivered_pallet(pallet_1) | covered | scan_it | 0 | 1 |
| 19 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 37 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 39 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 80; idle from 81 to 110. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 110 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 14 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 15 to 19 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 20 to 110 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 34 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 35 to 36 |
| office_break(office_chair) | move_to(office_door) | -1 to 110 |

Events (actual):

| tick | event |
|---|---|
| 17 | boundary (no pin) |
| 37 | boundary |
| 37 | pin confirm_delivered_pallet(pallet_2) |
| 62 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair). At the last entry (go_to(desk), ticks 39 to 80): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_1) | 0 to 18 | outside the support (at the floor) | - | - | - |
| confirm_delivered_pallet(pallet_2) | 19 to 38 | not reached | - | - | - |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 16 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0440 | 0.0466 | 341.7 | 321.7 | 20.0 | confirm_delivered_pallet(pallet_1) |
| 27 | office_break(office_chair) | move_to(office_door) | 0.0280 | 0.0417 | 353.0 | 353.0 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 29 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.0289 | 0.0396 | 358.1 | 358.1 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 55 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1464 | 0.0383 | 361.6 | 361.6 | 0.0 | - |
| 55 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.1727 | 0.0453 | 344.6 | 344.6 | 0.0 | - |
| 62 | office_break(office_chair) | move_to(office_door) | 0.8373 | 0.0440 | 347.6 | 347.6 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_1) |
| 17 | adequate | unresolved | confirm_delivered_pallet(pallet_1) |
| 18 | unresolved | adequate | confirm_delivered_pallet(pallet_1) |
| 37 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 38 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 62 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 14, 19 to 36, 39 to 53 |
| confirm_delivered_pallet(pallet_0) | 0 to 16, 39 to 54 |
| confirm_delivered_pallet(pallet_2) | 0 to 16, 19 to 36 |
| office_break(office_chair) | 0 to 16, 39 to 76 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 16 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 17 to 18 | coffee_break(coffee_machine_0) | none(below_theta) |
| 19 to 20 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 21 to 36 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 37 to 39 | coffee_break(coffee_machine_0) | none(below_theta) |
| 40 to 57 | office_break(office_chair) | none(below_theta) |
| 58 to 61 | office_break(office_chair) | clears |
| 62 to 110 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 39, last step 79, acknowledgement 80; the idle human from 81. Live at its first tick: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.3307 at 39; S < α from 55 (belief 0.1464; v·D 361.6 cm); the finding unexplained from 62.

- confirm_delivered_pallet(pallet_0): belief 0.3247 at 39; S < α from 55 (belief 0.1727; v·D 344.6 cm); the finding unexplained from 62.

- office_break(office_chair): belief 0.3306 at 39; S < α from 62 (belief 0.8373; v·D 347.6 cm); the finding unexplained from 62.

