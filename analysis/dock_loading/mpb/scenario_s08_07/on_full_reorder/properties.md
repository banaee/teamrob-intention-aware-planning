# scenario_s08_07: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 246; terminal decision 248. [sep] minimum 98.14 (228), continuous 98.09 (229); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=1 end=2.00 | load_return(?pallet=pallet_6) | 0 |
| 2 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=3 end=6.00 | load_return(?pallet=pallet_6) | 0 |
| 6 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=7 end=14.00 | load_return(?pallet=pallet_6) | 0 |
| 14 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_0) | admitted confirm_delivered_pallet(?pallet=pallet_0) | load_return(?pallet=pallet_6) | 0 |
| 28 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=31.00 | load_return(?pallet=pallet_6) | 0 |
| 31 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=34.00 | load_return(?pallet=pallet_6) | 0 |
| 34 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=40.00 | load_return(?pallet=pallet_6) | 0 |
| 40 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=11 end=52.00 | load_return(?pallet=pallet_6) | 0 |
| 52 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=23 end=53.84 | load_return(?pallet=pallet_6) | 0 |
| 54 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback standing k=1 end=56.00 | load_return(?pallet=pallet_6) | 0 |
| 56 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=59.00 | load_return(?pallet=pallet_6) | 0 |
| 59 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=62.06 | load_return(?pallet=pallet_6) | 0 |
| 60 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | load_return(?pallet=pallet_6) | 0 |
| 81 | no_current_task |  | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | deliver_pallet(?pallet=pallet_4) | 0 |
| 108 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=46 end=155.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 124 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | deliver_pallet(?pallet=pallet_4) | 0 |
| 137 | no_current_task |  | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | load_return(?pallet=pallet_7) | 0 |
| 146 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=149.00 | load_return(?pallet=pallet_7) | 0 |
| 149 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=2 end=152.00 | load_return(?pallet=pallet_7) | 0 |
| 152 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=5 end=158.00 | load_return(?pallet=pallet_7) | 0 |
| 157 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | load_return(?pallet=pallet_7) | 0 |
| 175 | recognition_changed | retraction | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=12 end=188.00 | load_return(?pallet=pallet_7) | 0 |
| 188 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=25 end=214.00 | load_return(?pallet=pallet_7) | 0 |
| 198 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=35 end=234.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 234 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=71 end=306.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 248 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=85 end=334.00 | None | 0 |
