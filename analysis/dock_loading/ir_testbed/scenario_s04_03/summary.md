### scenario_s04_03

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 26 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 80 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 82 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 127; idle from 128 to 157. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 157 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 77 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 78 to 79 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 23 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 24 to 25 |
| office_break(office_chair) | move_to(office_door) | -1 to 157 |

Events (actual):

| tick | event |
|---|---|
| 26 | boundary |
| 26 | pin confirm_delivered_pallet(pallet_2) |
| 80 | boundary |
| 80 | pin confirm_delivered_pallet(pallet_0) |
| 106 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 82 to 127): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_2) | 0 to 27 | 8 | 0.7566 | yes | adequate |
| confirm_delivered_pallet(pallet_0) | 28 to 81 | 62 | 0.7671 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0477 | 0.0462 | 342.5 | 342.5 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 8 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.0446 | 0.0432 | 349.4 | 349.4 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 12 | office_break(office_chair) | move_to(office_door) | 0.0500 | 0.0401 | 357.0 | 357.0 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 62 | office_break(office_chair) | move_to(office_door) | 0.0416 | 0.0396 | 358.1 | 358.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 70 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0578 | 0.0458 | 343.5 | 343.5 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 103 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.3242 | 0.0459 | 343.3 | 343.3 | 0.0 | - |
| 106 | office_break(office_chair) | move_to(office_door) | 0.6878 | 0.0456 | 343.8 | 343.8 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_2) |
| 26 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 27 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 80 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 81 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 106 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 28 to 79, 82 to 111 |
| confirm_delivered_pallet(pallet_0) | 28 to 79 |
| confirm_delivered_pallet(pallet_2) | 0 to 25 |
| office_break(office_chair) | 28 to 79, 82 to 119 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 7 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 8 to 25 | confirm_delivered_pallet(pallet_2) | clears |
| 26 to 27 | coffee_break(coffee_machine_0) | none(below_theta) |
| 28 to 61 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 62 to 79 | confirm_delivered_pallet(pallet_0) | clears |
| 80 to 81 | coffee_break(coffee_machine_0) | none(below_theta) |
| 82 to 122 | office_break(office_chair) | none(below_theta) |
| 123 to 157 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 82, last step 126, acknowledgement 127; the idle human from 128. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4905 at 82; S < α from 103 (belief 0.3242; v·D 343.3 cm); the finding unexplained from 106.

- office_break(office_chair): belief 0.4945 at 82; S < α from 106 (belief 0.6878; v·D 343.8 cm); the finding unexplained from 106.

