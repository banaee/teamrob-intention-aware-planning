### scenario_s06_04

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 17 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 19 | confirm_delivered_pallet(pallet_1) | covered | move_to | 0 | 1 |
| 20 | confirm_delivered_pallet(pallet_1) | covered | scan_it | 0 | 1 |
| 22 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 57; idle from 58 to 87. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_1), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 87 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 14 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 15 to 16 |
| confirm_delivered_pallet(pallet_1) | move_to(pallet_1) | -1 to 14 |
| confirm_delivered_pallet(pallet_1) | scan_it(pallet_1) | 15 to 19 |
| office_break(office_chair) | move_to(office_door) | -1 to 87 |

Events (actual):

| tick | event |
|---|---|
| 17 | boundary |
| 17 | pin confirm_delivered_pallet(pallet_0) |
| 20 | boundary |
| 20 | pin confirm_delivered_pallet(pallet_1) |
| 38 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 22 to 57): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 18 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_1) | 19 to 21 | not reached | - | - | - |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 16 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0291 | 0.0466 | 341.7 | 321.7 | 20.0 | confirm_delivered_pallet(pallet_0) |
| 37 | office_break(office_chair) | move_to(office_door) | 0.3897 | 0.0389 | 359.9 | 359.9 | 0.0 | - |
| 38 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.6103 | 0.0459 | 343.1 | 343.1 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 17 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 18 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 20 | adequate | unresolved | confirm_delivered_pallet(pallet_1) |
| 21 | unresolved | adequate | confirm_delivered_pallet(pallet_1) |
| 38 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 14, 22 to 37 |
| confirm_delivered_pallet(pallet_0) | 0 to 16 |
| confirm_delivered_pallet(pallet_1) | 0 to 16 |
| office_break(office_chair) | 0 to 16, 22 to 33 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 16 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 17 to 18 | coffee_break(coffee_machine_0) | none(below_theta) |
| 19 to 19 | confirm_delivered_pallet(pallet_1) | none(below_theta) |
| 20 to 21 | coffee_break(coffee_machine_0) | none(below_theta) |
| 22 to 28 | office_break(office_chair) | none(below_theta) |
| 29 to 50 | coffee_break(coffee_machine_0) | none(below_theta) |
| 51 to 87 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 22, last step 56, acknowledgement 57; the idle human from 58. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4897 at 22; S < α from 38 (belief 0.6103; v·D 343.1 cm); the finding unexplained from 38.

- office_break(office_chair): belief 0.4953 at 22; S < α from 37 (belief 0.3897; v·D 359.9 cm); the finding unexplained from 38.

