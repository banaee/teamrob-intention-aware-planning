### scenario_s02_06

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 30 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 81 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 112 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 121 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 123 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 147; idle from 148 to 177. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 78 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 79 to 112 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 113 to 177 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 27 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 118 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 119 to 120 |
| office_break(office_chair) | move_to(office_door) | -1 to 177 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary |
| 28 | pin confirm_delivered_pallet(pallet_0) |
| 110 | boundary |
| 110 | pin coffee_break(coffee_machine_0) |
| 112 | re-entry coffee_break(coffee_machine_0) |
| 121 | boundary |
| 121 | pin confirm_delivered_pallet(pallet_2) |
| 138 | finding turns unexplained |

Never pinned: office_break(office_chair). At the last entry (go_to(desk), ticks 123 to 147): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 29 | 10 | 0.7745 | yes | adequate |
| coffee_break(coffee_machine_0) | 30 to 111 | 79 | 0.7534 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 112 to 122 | not reached | - | - | - |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0409 | 0.0445 | 346.4 | 346.4 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 9 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0406 | 0.0409 | 355.0 | 355.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0475 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 60 | office_break(office_chair) | move_to(office_door) | 0.0320 | 0.0461 | 342.8 | 342.8 | 0.0 | coffee_break(coffee_machine_0) |
| 88 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0543 | 0.0427 | 350.6 | 170.6 | 180.0 | coffee_break(coffee_machine_0) |
| 138 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.5022 | 0.0470 | 340.9 | 340.9 | 0.0 | - |
| 138 | office_break(office_chair) | move_to(office_door) | 0.4828 | 0.0451 | 344.9 | 344.9 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 110 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 111 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 121 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 122 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 138 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 30 to 109, 123 to 136 |
| confirm_delivered_pallet(pallet_0) | 0 to 27 |
| confirm_delivered_pallet(pallet_2) | 30 to 109, 112 to 120 |
| office_break(office_chair) | 0 to 10, 30 to 76, 112 to 120, 123 to 133 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 9 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 10 to 27 | confirm_delivered_pallet(pallet_0) | clears |
| 28 to 78 | coffee_break(coffee_machine_0) | none(below_theta) |
| 79 to 109 | coffee_break(coffee_machine_0) | clears |
| 110 to 120 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 121 to 138 | coffee_break(coffee_machine_0) | none(below_theta) |
| 139 to 177 | office_break(office_chair) | none(below_theta) |

The last entry (go_to(desk)): first step 123, last step 146, acknowledgement 147; the idle human from 148. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.5106 at 123; S < α from 138 (belief 0.5022; v·D 340.9 cm); the finding unexplained from 138.

- office_break(office_chair): belief 0.4744 at 123; S < α from 138 (belief 0.4828; v·D 344.9 cm); the finding unexplained from 138.

