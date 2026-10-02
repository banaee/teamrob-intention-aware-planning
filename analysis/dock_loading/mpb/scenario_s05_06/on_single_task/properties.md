# scenario_s05_06: part 4 and the measures (single_task, prior on)

Completion (world tick) 428; terminal decision 430. [sep] minimum 57.59 (359), continuous 54.34 (359); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

- **M(i)**: holds. the terminal decision 430
- **M(ii)**: holds. entries still open at the run's end: []
- **M(iii)**: holds. F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}
- **M(iv)**: holds. (pallet, the tick its delivery is first observable, the scan's first live tick): [('pallet_2', 58, 58), ('pallet_3', 150, 150), ('pallet_0', 249, 249), ('pallet_1', 367, 367)]

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=2.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 2 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=6.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 6 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=14.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 14 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=30.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 30 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=31 end=62.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 60 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=3 end=64.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 64 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=7 end=72.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 65 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | deliver_pallet(?pallet=pallet_3) | 0 |
| 84 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=87.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 87 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=2 end=90.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 90 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=5 end=96.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 96 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=11 end=108.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 108 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=23 end=109.50 | deliver_pallet(?pallet=pallet_3) | 0 |
| 109 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_pallet(?pallet=pallet_3) | 0 |
| 125 | recognition_changed | retraction | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=16 end=142.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 142 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=33 end=176.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 152 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_3) | fallback moving k=3 end=156.00 | load_return(?pallet=pallet_4) | 0 |
| 156 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_3) | admitted confirm_delivered_pallet(?pallet=pallet_3) | deliver_pallet(?pallet=pallet_0) | 0 |
| 184 | recognition_changed | retraction | none(leader_inadequate) | confirm_delivered_pallet(?pallet=pallet_3) | fallback moving k=10 end=195.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 195 | projection_expired |  | none(leader_inadequate) | confirm_delivered_pallet(?pallet=pallet_3) | fallback moving k=21 end=217.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 217 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=43 end=219.95 | deliver_pallet(?pallet=pallet_0) | 0 |
| 219 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_pallet(?pallet=pallet_0) | 0 |
| 250 | recognition_changed | replaced | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback standing k=31 end=282.00 | load_return(?pallet=pallet_4) | 0 |
| 271 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_3) | admitted confirm_delivered_pallet(?pallet=pallet_3) | load_return(?pallet=pallet_4) | 0 |
| 298 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=301.00 | load_return(?pallet=pallet_4) | 0 |
| 301 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=2 end=304.00 | load_return(?pallet=pallet_4) | 0 |
| 304 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=5 end=310.00 | load_return(?pallet=pallet_4) | 0 |
| 310 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=11 end=322.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 322 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=23 end=346.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 334 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_0) | admitted confirm_delivered_pallet(?pallet=pallet_0) | deliver_pallet(?pallet=pallet_1) | 0 |
| 352 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=355.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 355 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=358.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 358 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=364.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 364 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=11 end=376.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 369 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=16 end=379.46 | load_return(?pallet=pallet_5) | 0 |
| 376 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | load_return(?pallet=pallet_5) | 0 |
| 381 | recognition_changed | retraction | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback moving k=1 end=383.00 | load_return(?pallet=pallet_5) | 0 |
| 383 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback moving k=3 end=387.00 | load_return(?pallet=pallet_5) | 0 |
| 387 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=7 end=395.00 | load_return(?pallet=pallet_5) | 0 |
| 395 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_1) | fallback moving k=15 end=406.44 | load_return(?pallet=pallet_5) | 0 |
| 406 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_1) | admitted confirm_delivered_pallet(?pallet=pallet_1) | load_return(?pallet=pallet_5) | 0 |
| 408 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=411.00 | load_return(?pallet=pallet_5) | 0 |
| 411 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=414.00 | load_return(?pallet=pallet_5) | 0 |
| 414 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=420.00 | load_return(?pallet=pallet_5) | 0 |
| 420 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=11 end=432.00 | load_return(?pallet=pallet_5) | 0 |
| 430 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=21 end=452.00 | None | 0 |
