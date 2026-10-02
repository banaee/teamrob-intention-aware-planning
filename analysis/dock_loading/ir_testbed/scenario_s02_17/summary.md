### scenario_s02_17

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 14 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 52 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 83 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 92 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 94 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 145 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 147 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 192; idle from 193 to 222. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 49 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 50 to 80 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 83 to 222 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 142 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 143 to 144 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 89 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 90 to 91 |
| office_break(office_chair) | move_to(office_door) | -1 to 222 |

Events (actual):

| tick | event |
|---|---|
| 22 | finding turns unexplained |
| 50 | finding turns adequate (from unexplained) |
| 81 | boundary |
| 81 | pin coffee_break(coffee_machine_0) |
| 83 | re-entry coffee_break(coffee_machine_0) |
| 92 | boundary |
| 92 | pin confirm_delivered_pallet(pallet_2) |
| 145 | boundary |
| 145 | pin confirm_delivered_pallet(pallet_0) |
| 196 | finding turns unexplained |

Never pinned: office_break(office_chair). At the last entry (go_to(desk), ticks 147 to 192): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 13 | 10 | 0.7745 | yes | adequate |
| coffee_break(coffee_machine_0) | 14 to 82 | 51 | 0.7676 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 83 to 93 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_0) | 94 to 146 | 122 | 0.7633 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0409 | 0.0445 | 346.4 | 346.4 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 9 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0406 | 0.0409 | 355.0 | 355.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 18 | office_break(office_chair) | move_to(office_door) | 0.1967 | 0.0487 | 337.2 | 337.2 | 0.0 | coffee_break(coffee_machine_0) |
| 22 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.4639 | 0.0407 | 355.3 | 355.3 | 0.0 | coffee_break(coffee_machine_0) |
| 105 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0242 | 0.0360 | 367.9 | 367.9 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 127 | office_break(office_chair) | move_to(office_door) | 0.0534 | 0.0419 | 352.4 | 352.4 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 171 | office_break(office_chair) | move_to(office_door) | 0.0741 | 0.0424 | 351.2 | 351.2 | 0.0 | - |
| 196 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9840 | 0.0448 | 345.5 | 245.5 | 100.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 22 | adequate | unexplained | coffee_break(coffee_machine_0) |
| 50 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 81 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 82 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 92 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 93 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 145 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 146 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 196 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 27 to 80, 147 to 222 |
| confirm_delivered_pallet(pallet_0) | 0 to 27, 94 to 144 |
| confirm_delivered_pallet(pallet_2) | 25 to 80, 83 to 91 |
| office_break(office_chair) | 0 to 10, 15 to 35, 83 to 91, 94 to 144, 147 to 183 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 9 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 10 to 17 | confirm_delivered_pallet(pallet_0) | clears |
| 18 to 23 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 24 to 28 | office_break(office_chair) | none(below_theta) |
| 29 to 38 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 39 to 50 | coffee_break(coffee_machine_0) | none(below_theta) |
| 51 to 80 | coffee_break(coffee_machine_0) | clears |
| 81 to 82 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 83 to 91 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 92 to 93 | coffee_break(coffee_machine_0) | none(below_theta) |
| 94 to 121 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 122 to 144 | confirm_delivered_pallet(pallet_0) | clears |
| 145 to 164 | coffee_break(coffee_machine_0) | none(below_theta) |
| 165 to 195 | coffee_break(coffee_machine_0) | clears |
| 196 to 222 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 147, last step 191, acknowledgement 192; the idle human from 193. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4972 at 147; S < α from 196 (belief 0.9840; v·D 345.5 cm); the finding unexplained from 196.

- office_break(office_chair): belief 0.4878 at 147; S < α from 171 (belief 0.0741; v·D 351.2 cm); the finding unexplained from 196.

