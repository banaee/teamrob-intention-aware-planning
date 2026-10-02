### scenario_s04_16

Script actions (replay expanded per tick; the first tick of each action; the task's coverage from the loader's [coverage] line):

| tick | task | coverage | action | occurrence | stack depth |
|---|---|---|---|---|---|
| 0 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 28 | coffee_break(coffee_machine_0) | covered | move_to | 0 | 2 |
| 50 | coffee_break(coffee_machine_0) | covered | wait_at | 0 | 2 |
| 81 | confirm_delivered_pallet(pallet_0) | covered | move_to | 0 | 1 |
| 103 | confirm_delivered_pallet(pallet_0) | covered | scan_it | 0 | 1 |
| 105 | office_break(office_chair) | covered | move_to | 0 | 1 |
| 131 | office_break(office_chair) | covered | move_to | 1 | 1 |
| 139 | office_break(office_chair) | covered | wait_at | 0 | 1 |
| 185 | confirm_delivered_pallet(pallet_2) | covered | move_to | 0 | 1 |
| 191 | confirm_delivered_pallet(pallet_2) | covered | move_to | 1 | 1 |
| 220 | confirm_delivered_pallet(pallet_2) | covered | scan_it | 0 | 1 |
| 222 | go_to(desk) | task_absent | move_to | 0 | 1 |

Last acknowledgement tick 238; idle from 239 to 268. The support (prior on): coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), confirm_delivered_pallet(pallet_2), office_break(office_chair).

Expected action per hypothesis (the oracle's derived phases; ticks inclusive, -1 the observation before the clock starts; after the pin the hypothesis is retired):

| hypothesis | expected action | ticks |
|---|---|---|
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | -1 to 47 |
| coffee_break(coffee_machine_0) | wait_at(PT60S,coffee_machine_0) | 48 to 78 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 81 to 132 |
| coffee_break(coffee_machine_0) | move_to(office_door) | 133 to 188 |
| coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 189 to 268 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | -1 to 25 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 26 to 27 |
| confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 28 to 100 |
| confirm_delivered_pallet(pallet_0) | scan_it(pallet_0) | 101 to 102 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | -1 to 132 |
| confirm_delivered_pallet(pallet_2) | move_to(office_door) | 133 to 188 |
| confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 189 to 217 |
| confirm_delivered_pallet(pallet_2) | scan_it(pallet_2) | 218 to 219 |
| office_break(office_chair) | move_to(office_door) | -1 to 128 |
| office_break(office_chair) | move_to(office_chair) | 129 to 136 |
| office_break(office_chair) | wait_at(PT90S,office_chair) | 137 to 182 |
| office_break(office_chair) | move_to(office_chair) | 185 to 190 |
| office_break(office_chair) | move_to(office_door) | 191 to 268 |

Events (actual):

| tick | event |
|---|---|
| 28 | finding turns unexplained |
| 29 | finding turns adequate (from unexplained) |
| 37 | finding turns unexplained |
| 48 | finding turns adequate (from unexplained) |
| 79 | boundary |
| 79 | pin coffee_break(coffee_machine_0) |
| 81 | re-entry coffee_break(coffee_machine_0) |
| 103 | boundary |
| 103 | pin confirm_delivered_pallet(pallet_0) |
| 183 | boundary |
| 183 | pin office_break(office_chair) |
| 185 | re-entry office_break(office_chair) |
| 220 | boundary |
| 220 | pin confirm_delivered_pallet(pallet_2) |
| 249 | finding turns unexplained |

Never pinned: none. At the last entry (go_to(desk), ticks 222 to 238): lifecycle and finding adequate; on the idle ticks after it: adequate, unexplained.

True hypothesis and θ (actual): per contiguous stretch of ticks on which the hypothesis is the truth, its first tick with belief ≥ θ, its belief and hypothesis adequacy there, and whether it leads.

| true hypothesis | ticks | first tick ≥ θ | belief | leads | hypothesis adequacy |
|---|---|---|---|---|---|
| confirm_delivered_pallet(pallet_0) | 0 to 27 | 14 | 0.7579 | yes | adequate |
| coffee_break(coffee_machine_0) | 28 to 80 | 45 | 0.7725 | yes | inadequate |
| confirm_delivered_pallet(pallet_0) | 81 to 104 | 96 | 0.7655 | yes | adequate |
| office_break(office_chair) | 105 to 184 | 135 | 0.7532 | yes | adequate |
| confirm_delivered_pallet(pallet_2) | 185 to 221 | 198 | 0.7697 | yes | adequate |

Refutations (actual): each tick on which a hypothesis's S falls below α = 0.05 (from ≥ α or from no observation), its belief there and the v·D that took it there (from S); e and v·(s − s_exp) from expected.csv; the truth on that tick.

| tick | hypothesis | expected action | belief | S | v·D (cm) | e (cm) | v·(s − s_exp) (cm) | truth |
|---|---|---|---|---|---|---|---|---|
| 8 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0301 | 0.0431 | 349.6 | 349.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 15 | office_break(office_chair) | move_to(office_door) | 0.0406 | 0.0373 | 364.1 | 364.1 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 20 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0538 | 0.0427 | 350.6 | 350.6 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 37 | confirm_delivered_pallet(pallet_0) | move_to(pallet_0) | 0.8543 | 0.0400 | 357.1 | 357.1 | 0.0 | coffee_break(coffee_machine_0) |
| 90 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0285 | 0.0389 | 360.0 | 360.0 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 95 | confirm_delivered_pallet(pallet_2) | move_to(pallet_2) | 0.0399 | 0.0398 | 357.8 | 357.8 | 0.0 | confirm_delivered_pallet(pallet_0) |
| 118 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0319 | 0.0457 | 343.6 | 343.6 | 0.0 | office_break(office_chair) |
| 146 | coffee_break(coffee_machine_0) | move_to(office_door) | 0.0010 | 0.0475 | 339.8 | 159.8 | 180.0 | office_break(office_chair) |
| 146 | confirm_delivered_pallet(pallet_2) | move_to(office_door) | 0.0306 | 0.0475 | 339.8 | 159.8 | 180.0 | office_break(office_chair) |
| 200 | office_break(office_chair) | move_to(office_door) | 0.0120 | 0.0403 | 356.3 | 356.3 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 204 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.0490 | 0.0383 | 361.5 | 361.5 | 0.0 | confirm_delivered_pallet(pallet_2) |
| 236 | office_break(office_chair) | move_to(office_door) | 0.0932 | 0.0429 | 350.1 | 350.1 | 0.0 | - |
| 249 | coffee_break(coffee_machine_0) | move_to(coffee_machine_0) | 0.9244 | 0.0460 | 343.0 | 103.0 | 240.0 | - |

Finding transitions (actual; `exhausted` is the lifecycle state, no finding):

| tick | from | to | truth |
|---|---|---|---|
| 0 | - | adequate | confirm_delivered_pallet(pallet_0) |
| 28 | adequate | unexplained | coffee_break(coffee_machine_0) |
| 29 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 37 | adequate | unexplained | coffee_break(coffee_machine_0) |
| 48 | unexplained | adequate | coffee_break(coffee_machine_0) |
| 79 | adequate | unresolved | coffee_break(coffee_machine_0) |
| 80 | unresolved | adequate | coffee_break(coffee_machine_0) |
| 103 | adequate | unresolved | confirm_delivered_pallet(pallet_0) |
| 104 | unresolved | adequate | confirm_delivered_pallet(pallet_0) |
| 183 | adequate | unresolved | office_break(office_chair) |
| 184 | unresolved | adequate | office_break(office_chair) |
| 220 | adequate | unresolved | confirm_delivered_pallet(pallet_2) |
| 221 | unresolved | adequate | confirm_delivered_pallet(pallet_2) |
| 249 | adequate | unexplained | - |

Across the started task coffee_break(coffee_machine_0) (covered; actual): on top of the stack from 28 to 80, its hypothesis pinned at 79; the suspended task resumes at 81.

| tick | human action | truth | coffee_break(coffee_machine_0) belief / S | confirm_delivered_pallet(pallet_0) belief / S | confirm_delivered_pallet(pallet_2) belief / S | office_break(office_chair) belief / S | finding |
|---|---|---|---|---|---|---|---|
| 26 | move_to step | confirm_delivered_pallet(pallet_0) | 0.0099 / 0.0074 | 0.9750 / 1.0000 | 0.0010 / 0.0000 | 0.0011 / 0.0008 | adequate |
| 27 | move_to  | confirm_delivered_pallet(pallet_0) | 0.0082 / 0.0060 | 0.9769 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0007 | adequate |
| 28 | move_to step | coffee_break(coffee_machine_0) | 0.0082 / 0.0060 | 0.9769 / - | 0.0010 / 0.0000 | 0.0010 / 0.0006 | unexplained |
| 29 | move_to step | coffee_break(coffee_machine_0) | 0.0101 / 0.0060 | 0.9750 / 0.7475 | 0.0010 / 0.0000 | 0.0010 / 0.0005 | adequate |
| 30 | move_to step | coffee_break(coffee_machine_0) | 0.0129 / 0.0060 | 0.9721 / 0.5437 | 0.0010 / 0.0000 | 0.0010 / 0.0004 | adequate |
| 78 | wait_at stand | coffee_break(coffee_machine_0) | 0.9840 / 1.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | 0.0010 / 0.0000 | adequate |
| 79 | wait_at stand | coffee_break(coffee_machine_0) | retired | 0.3287 / - | 0.3287 / - | 0.3287 / - | unresolved |
| 80 | wait_at  | coffee_break(coffee_machine_0) | retired | 0.3287 / 1.0000 | 0.3287 / 1.0000 | 0.3287 / 1.0000 | adequate |
| 81 | move_to step | confirm_delivered_pallet(pallet_0) | 0.2467 / - | 0.2594 / 1.0000 | 0.2323 / 0.8565 | 0.2486 / 0.9411 | adequate |
| 82 | move_to step | confirm_delivered_pallet(pallet_0) | 0.2172 / 0.7401 | 0.2845 / 1.0000 | 0.2250 / 0.7262 | 0.2602 / 0.8819 | adequate |
| 83 | move_to step | confirm_delivered_pallet(pallet_0) | 0.1849 / 0.5354 | 0.3135 / 1.0000 | 0.2161 / 0.6097 | 0.2725 / 0.8226 | adequate |

Observation warrant (actual): the stretches of ticks on which each hypothesis holds it.

| hypothesis | warranted ticks |
|---|---|
| coffee_break(coffee_machine_0) | 0 to 78, 105 to 107, 185 to 219, 222 to 268 |
| confirm_delivered_pallet(pallet_0) | 0 to 27, 81 to 102 |
| confirm_delivered_pallet(pallet_2) | 105 to 132, 185 to 219 |
| office_break(office_chair) | 0 to 10, 81 to 102, 105 to 182, 222 to 226 |

The gate's answer per tick (actual; the leader and the outcome, stretches):

| ticks | leader | gate |
|---|---|---|
| 0 to 13 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 14 to 27 | confirm_delivered_pallet(pallet_0) | clears |
| 28 to 28 | confirm_delivered_pallet(pallet_0) | none(leader_no_observation) |
| 29 to 36 | confirm_delivered_pallet(pallet_0) | clears |
| 37 to 38 | confirm_delivered_pallet(pallet_0) | none(leader_inadequate) |
| 39 to 41 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 42 to 44 | coffee_break(coffee_machine_0) | none(below_theta) |
| 45 to 47 | coffee_break(coffee_machine_0) | none(leader_inadequate) |
| 48 to 78 | coffee_break(coffee_machine_0) | clears |
| 79 to 95 | confirm_delivered_pallet(pallet_0) | none(below_theta) |
| 96 to 102 | confirm_delivered_pallet(pallet_0) | clears |
| 103 to 104 | coffee_break(coffee_machine_0) | none(below_theta) |
| 105 to 134 | office_break(office_chair) | none(below_theta) |
| 135 to 182 | office_break(office_chair) | clears |
| 183 to 190 | coffee_break(coffee_machine_0) | none(below_theta) |
| 191 to 197 | confirm_delivered_pallet(pallet_2) | none(below_theta) |
| 198 to 219 | confirm_delivered_pallet(pallet_2) | clears |
| 220 to 230 | coffee_break(coffee_machine_0) | none(below_theta) |
| 231 to 248 | coffee_break(coffee_machine_0) | clears |
| 249 to 268 | coffee_break(coffee_machine_0) | none(leader_inadequate) |

The last entry (go_to(desk)): first step 222, last step 237, acknowledgement 238; the idle human from 239. Live at its first tick: coffee_break(coffee_machine_0), office_break(office_chair).

- coffee_break(coffee_machine_0): belief 0.5106 at 222; S < α from 249 (belief 0.9244; v·D 343.0 cm); the finding unexplained from 249.

- office_break(office_chair): belief 0.4744 at 222; S < α from 236 (belief 0.0932; v·D 350.1 cm); the finding unexplained from 249.

