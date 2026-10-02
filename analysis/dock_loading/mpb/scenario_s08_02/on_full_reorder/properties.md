# scenario_s08_02: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 175; terminal decision 177. [sep] minimum 106.07 (158), continuous 105.93 (158); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=1 end=2.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 2 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=3 end=6.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 6 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=7 end=14.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 14 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_0) | admitted confirm_delivered_pallet(?pallet=pallet_0) | deliver_pallet(?pallet=pallet_4) | 0 |
| 28 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=31.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 31 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=2 end=34.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 34 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=5 end=40.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 40 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=11 end=52.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 52 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=23 end=76.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 54 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | deliver_pallet(?pallet=pallet_4) | 0 |
| 66 | no_current_task |  | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | load_return(?pallet=pallet_6) | 0 |
| 82 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=85.00 | load_return(?pallet=pallet_6) | 0 |
| 85 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=2 end=88.00 | load_return(?pallet=pallet_6) | 0 |
| 88 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=5 end=94.00 | load_return(?pallet=pallet_6) | 0 |
| 93 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | load_return(?pallet=pallet_6) | 0 |
| 111 | recognition_changed | retraction | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=12 end=124.00 | load_return(?pallet=pallet_6) | 0 |
| 124 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=25 end=150.00 | load_return(?pallet=pallet_6) | 0 |
| 127 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=28 end=156.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 156 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=57 end=214.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 177 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=78 end=256.00 | None | 0 |
