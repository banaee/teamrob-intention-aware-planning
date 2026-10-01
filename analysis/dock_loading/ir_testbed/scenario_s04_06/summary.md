### scenario_s04_06

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 30 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 52 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 83 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 130 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 132 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 147; idle from 148 to 177. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 49 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 50 to 80 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 83 to 177 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 27 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 127 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 128 to 129 |
| office_break(office_chair) | move_to(office_door) | -1 to 177 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary |
| 28 | pin confirm_delivered_pallet(pallet_0) |
| 81 | boundary |
| 81 | pin coffee_break(coffee_machine_0) |
| 83 | re-entry coffee_break(coffee_machine_0) |
| 130 | boundary |
| 130 | pin confirm_delivered_pallet(pallet_2) |
| 159 | finding turns unexplained |

Never pinned: office_break(office_chair). At the last entry (go_to(desk), ticks 132 to 147): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 29 | 14 | 0.7579 | yes | adequate |
| coffee_break(coffee_machine_0) | 30 to 82 | 43 | 0.7574 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 83 to 131 | 102 | 0.7538 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0301 | 0.0431 | 349.6 | 349.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0406 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 20 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0538 | 0.0427 | 350.6 | 350.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 43 | office_break(office_chair) | move_to(office_door) | 0.0476 | 0.0461 | 342.8 | 342.8 | 0.0 | coffee_break(coffee_machine_0) |
| 51 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0549 | 0.0435 | 348.7 | 328.7 | 20.0 | coffee_break(coffee_machine_0) |
| 92 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0333 | 0.0443 | 346.8 | 346.8 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 111 | office_break(office_chair) | move_to(office_door) | 0.0573 | 0.0453 | 344.6 | 344.6 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 146 | office_break(office_chair) | move_to(office_door) | 0.0930 | 0.0437 | 348.2 | 348.2 | 0.0 | - |
| 159 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9130 | 0.0423 | 351.6 | 91.6 | 260.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 81 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 82 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 130 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 131 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 159 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 27, 30 to 80, 132 to 177 |
| confirm_delivered_pallet(pallet_0) | 0 to 27 |
| confirm_delivered_pallet(pallet_2) | 30 to 80, 83 to 129 |
| office_break(office_chair) | 0 to 10, 30 to 30, 83 to 129, 132 to 136 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 13 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 14 to 27 | confirm_delivered_pallet(pallet_0) | clears |
| 28 to 42 | coffee_break(coffee_machine_0) | none(below_theta) |
| 43 to 80 | coffee_break(coffee_machine_0) | clears |
| 81 to 101 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 102 to 129 | confirm_delivered_pallet(pallet_2) | clears |
| 130 to 140 | coffee_break(coffee_machine_0) | none(below_theta) |
| 141 to 158 | coffee_break(coffee_machine_0) | clears |
| 159 to 177 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 132, last step 146, acknowledgement 147; the idle human from 148. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.5107 at 132; S < α from 159 (belief 0.9130; v·D 351.6 cm); the finding unexplained from 159.

- office_break(office_chair): belief 0.4743 at 132; S < α from 146 (belief 0.0930; v·D 348.2 cm); the finding unexplained from 159.

