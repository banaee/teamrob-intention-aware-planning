### scenario_s04_02

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 30 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 82 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 84 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 100; idle from 101 to 130. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 130 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 27 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 79 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 80 to 81 |
| office_break(office_chair) | move_to(office_door) | -1 to 130 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary |
| 28 | pin confirm_delivered_pallet(pallet_0) |
| 82 | boundary |
| 82 | pin confirm_delivered_pallet(pallet_2) |
| 111 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 84 to 100): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 29 | 14 | 0.7579 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 30 to 83 | 54 | 0.7726 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0301 | 0.0431 | 349.6 | 349.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0406 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 20 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0538 | 0.0427 | 350.6 | 350.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 47 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0318 | 0.0403 | 356.5 | 356.5 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 60 | office_break(office_chair) | move_to(office_door) | 0.0517 | 0.0405 | 355.8 | 355.8 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 98 | office_break(office_chair) | move_to(office_door) | 0.0972 | 0.0470 | 340.8 | 340.8 | 0.0 | - |
| 111 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9224 | 0.0490 | 336.4 | 96.4 | 240.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 82 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 83 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 111 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 27, 30 to 47, 84 to 130 |
| confirm_delivered_pallet(pallet_0) | 0 to 27 |
| confirm_delivered_pallet(pallet_2) | 30 to 81 |
| office_break(office_chair) | 0 to 10, 30 to 75, 84 to 89 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 13 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 14 to 27 | confirm_delivered_pallet(pallet_0) | clears |
| 28 to 29 | coffee_break(coffee_machine_0) | none(below_theta) |
| 30 to 53 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 54 to 81 | confirm_delivered_pallet(pallet_2) | clears |
| 82 to 92 | coffee_break(coffee_machine_0) | none(below_theta) |
| 93 to 110 | coffee_break(coffee_machine_0) | clears |
| 111 to 130 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 84, last step 99, acknowledgement 100; the idle human from 101. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.5102 at 84; S < α from 111 (belief 0.9224; v·D 336.4 cm); the finding unexplained from 111.

- office_break(office_chair): belief 0.4748 at 84; S < α from 98 (belief 0.0972; v·D 340.8 cm); the finding unexplained from 111.

