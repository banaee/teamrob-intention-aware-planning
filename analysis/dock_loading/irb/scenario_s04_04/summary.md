### scenario_s04_04

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 30 | confirm_delivered_pallet(pallet_1) | covered | move_to | 0 | 1 |
| 31 | confirm_delivered_pallet(pallet_1) | covered | scan_it | 0 | 1 |
| 33 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 78; idle from 79 to 108. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_1), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 108 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 27 |
| confirm_delivered_pallet(pallet_1) | move_to(pallet_1) | -1 to 25 |
| confirm_delivered_pallet(pallet_1) | scan_it(pallet_1) | 26 to 30 |
| office_break(office_chair) | move_to(office_door) | -1 to 108 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary |
| 28 | pin confirm_delivered_pallet(pallet_0) |
| 31 | boundary |
| 31 | pin confirm_delivered_pallet(pallet_1) |
| 57 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), office_break(office_chair). At the last entry (go_to(desk), ticks 33 to 78): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 29 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_1) | 30 to 32 | not reached | - | - | - |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 15 | office_break(office_chair) | move_to(office_door) | 0.0225 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 20 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0278 | 0.0427 | 350.6 | 350.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 54 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.3213 | 0.0449 | 345.4 | 345.4 | 0.0 | - |
| 57 | office_break(office_chair) | move_to(office_door) | 0.6915 | 0.0453 | 344.6 | 344.6 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 31 | adequate | unresolved | confirm_delivered_pallet(pallet_1) |
| 32 | unresolved | adequate | confirm_delivered_pallet(pallet_1) |
| 57 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 27, 33 to 62 |
| confirm_delivered_pallet(pallet_0) | 0 to 27 |
| confirm_delivered_pallet(pallet_1) | 0 to 27 |
| office_break(office_chair) | 0 to 10, 33 to 70 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 27 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 28 to 29 | coffee_break(coffee_machine_0) | none(below_theta) |
| 30 to 30 | confirm_delivered_pallet(pallet_1) | none(below_theta) |
| 31 to 32 | coffee_break(coffee_machine_0) | none(below_theta) |
| 33 to 70 | office_break(office_chair) | none(below_theta) |
| 71 to 108 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 33, last step 77, acknowledgement 78; the idle human from 79. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4905 at 33; S < α from 54 (belief 0.3213; v·D 345.4 cm); the finding unexplained from 57.

- office_break(office_chair): belief 0.4945 at 33; S < α from 57 (belief 0.6915; v·D 344.6 cm); the finding unexplained from 57.

