### scenario_s06_06

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 17 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 19 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 1 |
| 42 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 1 |
| 73 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 84 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 86 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 127; idle from 128 to 157. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 39 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 40 to 70 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 73 to 157 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 14 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 15 to 16 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 81 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 82 to 83 |
| office_break(office_chair) | move_to(office_door) | -1 to 157 |

Events (actual):

| tick | event |
|---|---|
| 17 | boundary |
| 17 | pin confirm_delivered_pallet(pallet_0) |
| 71 | boundary |
| 71 | pin coffee_break(coffee_machine_0) |
| 73 | re-entry coffee_break(coffee_machine_0) |
| 84 | boundary |
| 84 | pin confirm_delivered_pallet(pallet_2) |
| 109 | finding turns unexplained |

Never pinned: office_break(office_chair). At the last entry (go_to(desk), ticks 86 to 127): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 18 | not reached | - | - | - |
| coffee_break(coffee_machine_0) | 19 to 72 | 36 | 0.7613 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 73 to 85 | 83 | 0.7587 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 16 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0440 | 0.0466 | 341.7 | 321.7 | 20.0 | confirm_delivered_pallet(pallet_0) |
| 28 | office_break(office_chair) | move_to(office_door) | 0.0292 | 0.0395 | 358.5 | 358.5 | 0.0 | coffee_break(coffee_machine_0) |
| 43 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0546 | 0.0429 | 350.0 | 290.0 | 60.0 | coffee_break(coffee_machine_0) |
| 82 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0388 | 0.0405 | 355.8 | 355.8 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 102 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1626 | 0.0362 | 367.2 | 367.2 | 0.0 | - |
| 109 | office_break(office_chair) | move_to(office_door) | 0.9324 | 0.0490 | 336.5 | 336.5 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 17 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 18 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 71 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 72 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 84 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 85 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 109 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 14, 19 to 70, 86 to 100 |
| confirm_delivered_pallet(pallet_0) | 0 to 16 |
| confirm_delivered_pallet(pallet_2) | 0 to 16, 19 to 70, 73 to 83 |
| office_break(office_chair) | 0 to 16, 73 to 83, 86 to 125 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 16 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 17 to 35 | coffee_break(coffee_machine_0) | none(below_theta) |
| 36 to 70 | coffee_break(coffee_machine_0) | clears |
| 71 to 82 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 83 to 83 | confirm_delivered_pallet(pallet_2) | clears |
| 84 to 87 | coffee_break(coffee_machine_0) | none(below_theta) |
| 88 to 99 | office_break(office_chair) | none(below_theta) |
| 100 to 108 | office_break(office_chair) | clears |
| 109 to 157 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 86, last step 126, acknowledgement 127; the idle human from 128. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4935 at 86; S < α from 102 (belief 0.1626; v·D 367.2 cm); the finding unexplained from 109.

- office_break(office_chair): belief 0.4915 at 86; S < α from 109 (belief 0.9324; v·D 336.5 cm); the finding unexplained from 109.

