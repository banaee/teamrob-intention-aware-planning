### scenario_s04_10

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 14 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 53 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 55 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 70; idle from 71 to 100. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 100 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 100 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 50 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 51 to 52 |
| office_break(office_chair) | move_to(office_door) | -1 to 100 |

Events (actual):

| tick | event |
|---|---|
| 22 | finding turns unexplained |
| 51 | finding turns adequate (from unexplained) |
| 53 | boundary |
| 53 | pin confirm_delivered_pallet(pallet_2) |
| 82 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair). At the last entry (go_to(desk), ticks 55 to 70): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 13 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_2) | 14 to 54 | 35 | 0.8038 | yes | inadequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0301 | 0.0431 | 349.6 | 349.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 18 | office_break(office_chair) | move_to(office_door) | 0.1616 | 0.0472 | 340.4 | 340.4 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 19 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1923 | 0.0420 | 352.2 | 352.2 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 22 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.4330 | 0.0403 | 356.4 | 356.4 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 69 | office_break(office_chair) | move_to(office_door) | 0.0706 | 0.0440 | 347.5 | 347.5 | 0.0 | - |
| 75 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.2218 | 0.0496 | 335.2 | 215.2 | 120.0 | - |
| 82 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.7160 | 0.0421 | 351.9 | 91.9 | 260.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 22 | adequate | unexplained | confirm_delivered_pallet(pallet_2) |
| 51 | unexplained | adequate | confirm_delivered_pallet(pallet_2) |
| 53 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 54 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 82 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 23, 55 to 100 |
| confirm_delivered_pallet(pallet_0) | 0 to 27, 55 to 100 |
| confirm_delivered_pallet(pallet_2) | 27 to 52 |
| office_break(office_chair) | 0 to 10, 15 to 34, 55 to 59 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 23 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 24 to 29 | office_break(office_chair) | none(below_theta) |
| 30 to 34 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 35 to 50 | confirm_delivered_pallet(pallet_2) | none(leader_inadequate) |
| 51 to 52 | confirm_delivered_pallet(pallet_2) | clears |
| 53 to 100 | coffee_break(coffee_machine_0) | none(below_theta) |

The last entry (go_to(desk)): first step 55, last step 69, acknowledgement 70; the idle human from 71. Live at its first tick: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.3410 at 55; S < α from 82 (belief 0.7160; v·D 351.9 cm); the finding unexplained from 82.

- confirm_delivered_pallet(pallet_0): belief 0.3282 at 55; S < α from 75 (belief 0.2218; v·D 335.2 cm); the finding unexplained from 82.

- office_break(office_chair): belief 0.3168 at 55; S < α from 69 (belief 0.0706; v·D 347.5 cm); the finding unexplained from 82.

