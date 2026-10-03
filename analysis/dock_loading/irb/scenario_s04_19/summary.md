### scenario_s04_19

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_1) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_1) | covered | scan_it | 0 | 1 |
| 30 | office_break(office_chair) | covered | move_to | 0 | 1 |
| 55 | office_break(office_chair) | covered | move_to | 1 | 1 |
| 64 | office_break(office_chair) | covered | wait_at | 0 | 1 |
| 110 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 117 | confirm_delivered_pallet(pallet_2) | covered | move_to | 1 | 1 |
| 146 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 148 | go_to(standby_place) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 172; idle from 173 to 202. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), confirm_delivered_pallet(pallet_4), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 56 |
| coffee_break(coffee_machine_0) | move_to(office_door) | 57 to 114 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 115 to 202 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 29 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 30 to 56 |
| confirm_delivered_pallet(pallet_0) | move_to(office_door) | 57 to 114 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 115 to 202 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 56 |
| confirm_delivered_pallet(pallet_2) | move_to(office_door) | 57 to 114 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 115 to 143 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 144 to 145 |
| office_break(office_chair) | move_to(office_door) | -1 to 52 |
| office_break(office_chair) | move_to(office_chair) | 53 to 61 |
| office_break(office_chair) | wait_at(PT90S,office_chair) | 62 to 107 |
| office_break(office_chair) | move_to(office_chair) | 110 to 117 |
| office_break(office_chair) | move_to(office_door) | 118 to 202 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary (no pin) |
| 108 | boundary |
| 108 | pin office_break(office_chair) |
| 110 | re-entry office_break(office_chair) |
| 146 | boundary |
| 146 | pin confirm_delivered_pallet(pallet_2) |
| 187 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_4). At the last entry (go_to(standby_place), ticks 148 to 172): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_1) | 0 to 29 | outside the support (at the floor) | - | - | - |
| office_break(office_chair) | 30 to 109 | 60 | 0.7970 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 110 to 147 | 125 | 0.7660 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0301 | 0.0431 | 349.6 | 349.6 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0406 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 20 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0538 | 0.0427 | 350.6 | 350.6 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 39 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.0248 | 0.0393 | 358.9 | 358.9 | 0.0 | office_break(office_chair) |
| 43 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0297 | 0.0425 | 351.0 | 351.0 | 0.0 | office_break(office_chair) |
| 69 | coffee_break(coffee_machine_0) | move_to(office_door) | 0.0010 | 0.0476 | 339.6 | 199.6 | 140.0 | office_break(office_chair) |
| 69 | confirm_delivered_pallet(pallet_0) | move_to(office_door) | 0.0010 | 0.0476 | 339.6 | 199.6 | 140.0 | office_break(office_chair) |
| 69 | confirm_delivered_pallet(pallet_2) | move_to(office_door) | 0.0314 | 0.0476 | 339.6 | 199.6 | 140.0 | office_break(office_chair) |
| 126 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.0419 | 0.0378 | 363.0 | 363.0 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 127 | office_break(office_chair) | move_to(office_door) | 0.0073 | 0.0393 | 358.8 | 358.8 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 130 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0478 | 0.0377 | 363.0 | 363.0 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 178 | office_break(office_chair) | move_to(office_door) | 0.0805 | 0.0420 | 352.3 | 212.3 | 140.0 | - |
| 187 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.4465 | 0.0441 | 347.3 | 27.3 | 320.0 | - |
| 187 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.4674 | 0.0462 | 342.6 | 22.6 | 320.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_1) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_1) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_1) |
| 108 | adequate | unresolved | office_break(office_chair) |
| 109 | unresolved | adequate | office_break(office_chair) |
| 146 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 147 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 187 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 27, 30 to 30, 110 to 145, 148 to 202 |
| confirm_delivered_pallet(pallet_0) | 0 to 27, 110 to 145, 148 to 202 |
| confirm_delivered_pallet(pallet_2) | 30 to 56, 110 to 145 |
| confirm_delivered_pallet(pallet_4) | none |
| office_break(office_chair) | 0 to 10, 30 to 107, 148 to 202 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 13 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 14 to 27 | confirm_delivered_pallet(pallet_0) | clears |
| 28 to 29 | coffee_break(coffee_machine_0) | none(below_theta) |
| 30 to 30 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 31 to 59 | office_break(office_chair) | none(below_theta) |
| 60 to 107 | office_break(office_chair) | clears |
| 108 to 116 | coffee_break(coffee_machine_0) | none(below_theta) |
| 117 to 124 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 125 to 145 | confirm_delivered_pallet(pallet_2) | clears |
| 146 to 147 | coffee_break(coffee_machine_0) | none(below_theta) |
| 148 to 202 | confirm_delivered_pallet(pallet_0) | none(below_theta) |

The last entry (go_to(standby_place)): first step 148, last step 171, acknowledgement 172; the idle human from 173. Live at its first tick: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.3300 at 148; S < α from 187 (belief 0.4465; v·D 347.3 cm); the finding unexplained from 187.

- confirm_delivered_pallet(pallet_0): belief 0.3301 at 148; S < α from 187 (belief 0.4674; v·D 342.6 cm); the finding unexplained from 187.

- office_break(office_chair): belief 0.3258 at 148; S < α from 178 (belief 0.0805; v·D 352.3 cm); the finding unexplained from 187.

Entries still open at the run's end (the record; a script that depends on the robot):

- confirm_delivered_pallet(?pallet=pallet_4)
- go_to(?landmark=desk)

