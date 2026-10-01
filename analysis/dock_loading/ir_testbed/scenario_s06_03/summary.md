### scenario_s06_03

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 26 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 45 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 47 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 83; idle from 84 to 113. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 113 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 42 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 43 to 44 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 23 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 24 to 25 |
| office_break(office_chair) | move_to(office_door) | -1 to 113 |

Events (actual):

| tick | event |
|---|---|
| 26 | boundary |
| 26 | pin confirm_delivered_pallet(pallet_2) |
| 45 | boundary |
| 45 | pin confirm_delivered_pallet(pallet_0) |
| 63 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 47 to 83): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_2) | 0 to 27 | 21 | 0.7526 | yes | adequate |
| confirm_delivered_pallet(pallet_0) | 28 to 46 | not reached | - | - | - |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 11 | office_break(office_chair) | move_to(office_door) | 0.0294 | 0.0489 | 336.7 | 336.7 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 19 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.0405 | 0.0437 | 348.2 | 348.2 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 38 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0265 | 0.0397 | 357.9 | 357.9 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 63 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.5363 | 0.0457 | 343.6 | 343.6 | 0.0 | - |
| 63 | office_break(office_chair) | move_to(office_door) | 0.4487 | 0.0382 | 361.9 | 361.9 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_2) |
| 26 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 27 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 45 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 46 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 63 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 25, 47 to 62 |
| confirm_delivered_pallet(pallet_0) | 0 to 22, 28 to 44 |
| confirm_delivered_pallet(pallet_2) | 0 to 25 |
| office_break(office_chair) | 28 to 44, 47 to 61 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 20 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 21 to 25 | confirm_delivered_pallet(pallet_2) | clears |
| 26 to 27 | coffee_break(coffee_machine_0) | none(below_theta) |
| 28 to 44 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 45 to 46 | coffee_break(coffee_machine_0) | none(below_theta) |
| 47 to 58 | office_break(office_chair) | none(below_theta) |
| 59 to 113 | coffee_break(coffee_machine_0) | none(below_theta) |

The last entry (go_to(desk)): first step 47, last step 82, acknowledgement 83; the idle human from 84. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4891 at 47; S < α from 63 (belief 0.5363; v·D 343.6 cm); the finding unexplained from 63.

- office_break(office_chair): belief 0.4959 at 47; S < α from 63 (belief 0.4487; v·D 361.9 cm); the finding unexplained from 63.

