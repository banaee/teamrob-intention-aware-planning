### scenario_s02_15

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 28 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 30 | go_to(standby_place) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 56; idle from 57 to 86. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_2), confirm_delivered_pallet(pallet_4), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 86 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 25 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 26 to 27 |
| office_break(office_chair) | move_to(office_door) | -1 to 86 |

Events (actual):

| tick | event |
|---|---|
| 28 | boundary |
| 28 | pin confirm_delivered_pallet(pallet_2) |
| 57 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_4), office_break(office_chair). At the last entry (go_to(standby_place), ticks 30 to 56): lifecycle and finding adequate; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_2) | 0 to 29 | 25 | 0.7761 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 15 | office_break(office_chair) | move_to(office_door) | 0.0274 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 42 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0899 | 0.0472 | 340.5 | 340.5 | 0.0 | - |
| 57 | office_break(office_chair) | move_to(office_door) | 0.9796 | 0.0446 | 346.1 | 306.1 | 40.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_2) |
| 28 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 29 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 57 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 27, 30 to 35 |
| confirm_delivered_pallet(pallet_2) | 0 to 27 |
| confirm_delivered_pallet(pallet_4) | none |
| office_break(office_chair) | 0 to 10, 30 to 86 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 24 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 25 to 27 | confirm_delivered_pallet(pallet_2) | clears |
| 28 to 29 | coffee_break(coffee_machine_0) | none(below_theta) |
| 30 to 37 | office_break(office_chair) | none(below_theta) |
| 38 to 56 | office_break(office_chair) | clears |
| 57 to 86 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(standby_place)): first step 30, last step 55, acknowledgement 56; the idle human from 57. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4788 at 30; S < α from 42 (belief 0.0899; v·D 340.5 cm); the finding unexplained from 57.

- office_break(office_chair): belief 0.5062 at 30; S < α from 57 (belief 0.9796; v·D 346.1 cm); the finding unexplained from 57.

Entries still open at the run's end (the record; a script that depends on the robot):

- confirm_delivered_pallet(?pallet=pallet_4)
- go_to(?landmark=desk)

