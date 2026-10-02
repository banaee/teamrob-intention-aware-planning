### scenario_s06_17

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 14 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 37 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 68 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 79 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 81 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 99 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 101 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 137; idle from 138 to 167. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 34 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 35 to 68 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 69 to 167 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 96 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 97 to 98 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 76 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 77 to 78 |
| office_break(office_chair) | move_to(office_door) | -1 to 167 |

Events (actual):

| tick | event |
|---|---|
| 66 | boundary |
| 66 | pin coffee_break(coffee_machine_0) |
| 68 | re-entry coffee_break(coffee_machine_0) |
| 79 | boundary |
| 79 | pin confirm_delivered_pallet(pallet_2) |
| 99 | boundary |
| 99 | pin confirm_delivered_pallet(pallet_0) |
| 117 | finding turns unexplained |

Never pinned: office_break(office_chair). At the last entry (go_to(desk), ticks 101 to 137): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 13 | not reached | - | - | - |
| coffee_break(coffee_machine_0) | 14 to 67 | 34 | 0.7552 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 68 to 80 | not reached | - | - | - |
| confirm_delivered_pallet(pallet_0) | 81 to 100 | not reached | - | - | - |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 16 | office_break(office_chair) | move_to(office_door) | 0.0589 | 0.0495 | 335.6 | 335.6 | 0.0 | coffee_break(coffee_machine_0) |
| 23 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.1080 | 0.0363 | 367.1 | 367.1 | 0.0 | coffee_break(coffee_machine_0) |
| 32 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.3337 | 0.0481 | 338.4 | 338.4 | 0.0 | coffee_break(coffee_machine_0) |
| 78 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0348 | 0.0477 | 339.3 | 319.3 | 20.0 | confirm_delivered_pallet(pallet_2) |
| 91 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0270 | 0.0405 | 355.9 | 355.9 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 117 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.5437 | 0.0460 | 342.9 | 342.9 | 0.0 | - |
| 117 | office_break(office_chair) | move_to(office_door) | 0.4413 | 0.0372 | 364.4 | 364.4 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 66 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 67 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 79 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 80 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 99 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 100 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 117 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 65, 101 to 116 |
| confirm_delivered_pallet(pallet_0) | 0 to 28, 68 to 78, 81 to 98 |
| confirm_delivered_pallet(pallet_2) | 0 to 65, 68 to 78 |
| office_break(office_chair) | 0 to 16, 68 to 78, 81 to 98, 101 to 114 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 17 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 18 to 29 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 30 to 33 | coffee_break(coffee_machine_0) | none(below_theta) |
| 34 to 65 | coffee_break(coffee_machine_0) | clears |
| 66 to 67 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 68 to 78 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 79 to 80 | coffee_break(coffee_machine_0) | none(below_theta) |
| 81 to 98 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 99 to 100 | coffee_break(coffee_machine_0) | none(below_theta) |
| 101 to 111 | office_break(office_chair) | none(below_theta) |
| 112 to 167 | coffee_break(coffee_machine_0) | none(below_theta) |

The last entry (go_to(desk)): first step 101, last step 136, acknowledgement 137; the idle human from 138. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4891 at 101; S < α from 117 (belief 0.5437; v·D 342.9 cm); the finding unexplained from 117.

- office_break(office_chair): belief 0.4959 at 101; S < α from 117 (belief 0.4413; v·D 364.4 cm); the finding unexplained from 117.

