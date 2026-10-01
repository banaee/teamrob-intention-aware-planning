### scenario_s06_07

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 17 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 19 | office_break(office_chair) | covered | move_to | 0 | 1 |
| 32 | office_break(office_chair) | covered | move_to | 1 | 1 |
| 40 | office_break(office_chair) | covered | wait_at | 0 | 1 |
| 86 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 92 | confirm_delivered_pallet(pallet_2) | covered | move_to | 1 | 1 |
| 124 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 126 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 167; idle from 168 to 197. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 33 |
| coffee_break(coffee_machine_0) | move_to(office_door) | 34 to 89 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 90 to 197 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 14 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 15 to 16 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 33 |
| confirm_delivered_pallet(pallet_2) | move_to(office_door) | 34 to 89 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 90 to 121 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 122 to 123 |
| office_break(office_chair) | move_to(office_door) | -1 to 29 |
| office_break(office_chair) | move_to(office_chair) | 30 to 37 |
| office_break(office_chair) | wait_at(PT90S,office_chair) | 38 to 83 |
| office_break(office_chair) | move_to(office_chair) | 86 to 93 |
| office_break(office_chair) | move_to(office_door) | 94 to 197 |

Events (actual):

| tick | event |
|---|---|
| 17 | boundary |
| 17 | pin confirm_delivered_pallet(pallet_0) |
| 84 | boundary |
| 84 | pin office_break(office_chair) |
| 86 | re-entry office_break(office_chair) |
| 124 | boundary |
| 124 | pin confirm_delivered_pallet(pallet_2) |
| 149 | finding turns unexplained |

Never pinned: coffee_break(coffee_machine_0). At the last entry (go_to(desk), ticks 126 to 167): lifecycle and finding adequate, unexplained; on the idle ticks after it: unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 18 | not reached | - | - | - |
| office_break(office_chair) | 19 to 85 | 25 | 0.7664 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 86 to 125 | 123 | 0.7773 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 16 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0440 | 0.0466 | 341.7 | 321.7 | 20.0 | confirm_delivered_pallet(pallet_0) |
| 27 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0496 | 0.0420 | 352.1 | 352.1 | 0.0 | office_break(office_chair) |
| 28 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0530 | 0.0433 | 349.2 | 349.2 | 0.0 | office_break(office_chair) |
| 47 | coffee_break(coffee_machine_0) | move_to(office_door) | 0.0010 | 0.0474 | 340.0 | 160.0 | 180.0 | office_break(office_chair) |
| 47 | confirm_delivered_pallet(pallet_2) | move_to(office_door) | 0.0010 | 0.0474 | 340.0 | 160.0 | 180.0 | office_break(office_chair) |
| 103 | office_break(office_chair) | move_to(office_door) | 0.0026 | 0.0389 | 360.0 | 360.0 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 142 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.1755 | 0.0390 | 359.6 | 359.6 | 0.0 | - |
| 149 | office_break(office_chair) | move_to(office_door) | 0.9240 | 0.0468 | 341.2 | 341.2 | 0.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 17 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 18 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 84 | adequate | unresolved | office_break(office_chair) |
| 85 | unresolved | adequate | office_break(office_chair) |
| 124 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 125 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 149 | adequate | unexplained | - |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 14, 86 to 123, 126 to 140 |
| confirm_delivered_pallet(pallet_0) | 0 to 16 |
| confirm_delivered_pallet(pallet_2) | 0 to 16, 86 to 123 |
| office_break(office_chair) | 0 to 16, 19 to 83, 126 to 164 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 16 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 17 to 18 | coffee_break(coffee_machine_0) | none(below_theta) |
| 19 to 24 | office_break(office_chair) | none(below_theta) |
| 25 to 83 | office_break(office_chair) | clears |
| 84 to 91 | coffee_break(coffee_machine_0) | none(below_theta) |
| 92 to 122 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 123 to 123 | confirm_delivered_pallet(pallet_2) | clears |
| 124 to 127 | coffee_break(coffee_machine_0) | none(below_theta) |
| 128 to 139 | office_break(office_chair) | none(below_theta) |
| 140 to 148 | office_break(office_chair) | clears |
| 149 to 197 | office_break(office_chair) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 126, last step 166, acknowledgement 167; the idle human from 168. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.4930 at 126; S < α from 142 (belief 0.1755; v·D 359.6 cm); the finding unexplained from 149.

- office_break(office_chair): belief 0.4920 at 126; S < α from 149 (belief 0.9240; v·D 341.2 cm); the finding unexplained from 149.

