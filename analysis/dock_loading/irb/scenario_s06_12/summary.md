### scenario_s06_12

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 17 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 19 | stand(PT80S) | task_absent | stand | 0 | 1 |
| 60 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 78 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 80 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 121; idle from 122 to 151. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 151 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 14 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 15 to 16 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 75 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 76 to 77 |
| office_break(office_chair) | move_to(office_door) | -1 to 151 |

Events (actual):

| tick | event |
|---|---|
| 17 | boundary |
| 17 | pin confirm_delivered_pallet(pallet_0) |
| 35 | finding turns unexplained |
| 76 | finding turns adequate (from unexplained) |
| 78 | boundary |
| 78 | pin confirm_delivered_pallet(pallet_2) |
| 103 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 80 to 121): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 18 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_2) | 60 to 79 | 77 | 0.7718 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 16 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0440 | 0.0466 | 341.7 | 321.7 | 20.0 | confirm_delivered_pallet(pallet_0) |
| 35 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 35 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 35 | office_break(office_chair) | move_to(office_door) | 0.3287 | 0.0474 | 340.0 | 0.0 | 340.0 | - |
| 96 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1773 | 0.0383 | 361.6 | 361.6 | 0.0 | - |
| 103 | office_break(office_chair) | move_to(office_door) | 0.9207 | 0.0440 | 347.6 | 347.6 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 17 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 18 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 35 | adequate | unexplained | - |
| 76 | unexplained | adequate | confirm_delivered_pallet(pallet_2) |
| 78 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 79 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 103 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 14, 60 to 77, 80 to 94 |
| confirm_delivered_pallet(pallet_0) | 0 to 16 |
| confirm_delivered_pallet(pallet_2) | 0 to 16, 60 to 77 |
| office_break(office_chair) | 0 to 16, 80 to 117 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 16 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 17 to 59 | coffee_break(coffee_machine_0) | none(below_theta) |
| 60 to 76 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 77 to 77 | confirm_delivered_pallet(pallet_2) | clears |
| 78 to 80 | coffee_break(coffee_machine_0) | none(below_theta) |
| 81 to 94 | office_break(office_chair) | none(below_theta) |
| 95 to 102 | office_break(office_chair) | clears |
| 103 to 151 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 80, last step 120, acknowledgement 121; the idle human from 122. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4925 at 80; S < α from 96 (belief 0.1773; v·D 361.6 cm); the finding unexplained from 103.

- office_break(office_chair): belief 0.4925 at 80; S < α from 103 (belief 0.9207; v·D 347.6 cm); the finding unexplained from 103.

