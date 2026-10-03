### scenario_s06_15

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 26 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 28 | go_to(standby_place) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 52; idle from 53 to 82. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_2), confirm_delivered_pallet(pallet_4), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 82 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 23 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 24 to 25 |
| office_break(office_chair) | move_to(office_door) | -1 to 82 |

Events (actual):

| tick | event |
|---|---|
| 26 | boundary |
| 26 | pin confirm_delivered_pallet(pallet_2) |
| 59 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_4), office_break(office_chair). At the last entry (go_to(standby_place), ticks 28 to 52): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_2) | 0 to 27 | 21 | 0.7705 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 11 | office_break(office_chair) | move_to(office_door) | 0.0357 | 0.0489 | 336.7 | 336.7 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 41 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0832 | 0.0468 | 341.2 | 341.2 | 0.0 | - |
| 59 | office_break(office_chair) | move_to(office_door) | 0.9795 | 0.0466 | 341.7 | 181.7 | 160.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_2) |
| 26 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 27 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 59 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 25, 28 to 35 |
| confirm_delivered_pallet(pallet_2) | 0 to 25 |
| confirm_delivered_pallet(pallet_4) | none |
| office_break(office_chair) | 28 to 82 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 20 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 21 to 25 | confirm_delivered_pallet(pallet_2) | clears |
| 26 to 27 | coffee_break(coffee_machine_0) | none(below_theta) |
| 28 to 36 | office_break(office_chair) | none(below_theta) |
| 37 to 58 | office_break(office_chair) | clears |
| 59 to 82 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(standby_place)): first step 28, last step 51, acknowledgement 52; the idle human from 53. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4793 at 28; S < α from 41 (belief 0.0832; v·D 341.2 cm); the finding unexplained from 59.

- office_break(office_chair): belief 0.5057 at 28; S < α from 59 (belief 0.9795; v·D 341.7 cm); the finding unexplained from 59.

Entries still open at the run's end (the record; a script that depends on the robot):

- confirm_delivered_pallet(?pallet=pallet_4)
- go_to(?landmark=desk)

