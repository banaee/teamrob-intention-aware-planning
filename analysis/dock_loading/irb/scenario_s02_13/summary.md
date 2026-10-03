### scenario_s02_13

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_1) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_1) | covered | scan_it | 0 | 1 |
| 30 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 81 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 83 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 108; idle from 109 to 138. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 138 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 29 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 30 to 138 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 78 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 79 to 80 |
| office_break(office_chair) | move_to(office_door) | -1 to 138 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary (no pin) |
| 81 | boundary |
| 81 | pin confirm_delivered_pallet(pallet_2) |
| 103 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair). At the last entry (go_to(desk), ticks 83 to 108): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_1) | 0 to 29 | outside the support (at the floor) | - | - | - |
| confirm_delivered_pallet(pallet_2) | 30 to 82 | 80 | 0.7759 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0409 | 0.0445 | 346.4 | 346.4 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 9 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0406 | 0.0409 | 355.0 | 355.0 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0475 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_1) |
| 39 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.0176 | 0.0391 | 359.4 | 359.4 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 62 | office_break(office_chair) | move_to(office_door) | 0.0342 | 0.0488 | 337.1 | 337.1 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 98 | office_break(office_chair) | move_to(office_door) | 0.1908 | 0.0447 | 345.9 | 345.9 | 0.0 | - |
| 99 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.2529 | 0.0464 | 342.0 | 342.0 | 0.0 | - |
| 103 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.6862 | 0.0476 | 339.4 | 339.4 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_1) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_1) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_1) |
| 81 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 82 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 103 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 30 to 80, 83 to 98 |
| confirm_delivered_pallet(pallet_0) | 0 to 27, 83 to 138 |
| confirm_delivered_pallet(pallet_2) | 30 to 80 |
| office_break(office_chair) | 0 to 10, 30 to 78, 83 to 93 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 9 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 10 to 27 | confirm_delivered_pallet(pallet_0) | clears |
| 28 to 29 | coffee_break(coffee_machine_0) | none(below_theta) |
| 30 to 30 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 31 to 79 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 80 to 80 | confirm_delivered_pallet(pallet_2) | clears |
| 81 to 94 | coffee_break(coffee_machine_0) | none(below_theta) |
| 95 to 105 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 106 to 138 | confirm_delivered_pallet(pallet_0) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 83, last step 107, acknowledgement 108; the idle human from 109. Live at its first tick: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.3426 at 83; S < α from 99 (belief 0.2529; v·D 342.0 cm); the finding unexplained from 103.

- confirm_delivered_pallet(pallet_0): belief 0.3246 at 83; S < α from 103 (belief 0.6862; v·D 339.4 cm); the finding unexplained from 103.

- office_break(office_chair): belief 0.3188 at 83; S < α from 98 (belief 0.1908; v·D 345.9 cm); the finding unexplained from 103.

