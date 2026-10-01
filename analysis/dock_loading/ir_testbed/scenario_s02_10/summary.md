### scenario_s02_10

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 14 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 53 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 55 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 80; idle from 81 to 110. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 110 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 110 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 50 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 51 to 52 |
| office_break(office_chair) | move_to(office_door) | -1 to 110 |

Events (actual):

| tick | event |
|---|---|
| 22 | finding turns unexplained |
| 51 | finding turns adequate (from unexplained) |
| 53 | boundary |
| 53 | pin confirm_delivered_pallet(pallet_2) |
| 75 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair). At the last entry (go_to(desk), ticks 55 to 80): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 13 | 10 | 0.7745 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 14 to 54 | 45 | 0.7562 | yes | inadequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0409 | 0.0445 | 346.4 | 346.4 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 9 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0406 | 0.0409 | 355.0 | 355.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 21 | office_break(office_chair) | move_to(office_door) | 0.3685 | 0.0486 | 337.3 | 337.3 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 22 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.4227 | 0.0453 | 344.6 | 344.6 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 70 | office_break(office_chair) | move_to(office_door) | 0.1893 | 0.0418 | 352.7 | 352.7 | 0.0 | - |
| 71 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.2481 | 0.0429 | 350.1 | 350.1 | 0.0 | - |
| 75 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.6904 | 0.0447 | 345.8 | 345.8 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 22 | adequate | unexplained | confirm_delivered_pallet(pallet_2) |
| 51 | unexplained | adequate | confirm_delivered_pallet(pallet_2) |
| 53 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 54 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 75 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 27 to 52, 55 to 70 |
| confirm_delivered_pallet(pallet_0) | 0 to 28, 55 to 110 |
| confirm_delivered_pallet(pallet_2) | 25 to 52 |
| office_break(office_chair) | 0 to 10, 15 to 39, 55 to 64 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 9 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 10 to 17 | confirm_delivered_pallet(pallet_0) | clears |
| 18 to 22 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 23 to 30 | office_break(office_chair) | none(below_theta) |
| 31 to 44 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 45 to 50 | confirm_delivered_pallet(pallet_2) | none(leader_inadequate) |
| 51 to 52 | confirm_delivered_pallet(pallet_2) | clears |
| 53 to 66 | coffee_break(coffee_machine_0) | none(below_theta) |
| 67 to 77 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 78 to 110 | confirm_delivered_pallet(pallet_0) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 55, last step 79, acknowledgement 80; the idle human from 81. Live at its first tick: coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.3427 at 55; S < α from 71 (belief 0.2481; v·D 350.1 cm); the finding unexplained from 75.

- confirm_delivered_pallet(pallet_0): belief 0.3247 at 55; S < α from 75 (belief 0.6904; v·D 345.8 cm); the finding unexplained from 75.

- office_break(office_chair): belief 0.3186 at 55; S < α from 70 (belief 0.1893; v·D 352.7 cm); the finding unexplained from 75.

