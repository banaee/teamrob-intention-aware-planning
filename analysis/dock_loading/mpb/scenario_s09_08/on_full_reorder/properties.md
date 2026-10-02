# scenario_s09_08: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 194; terminal decision 196. [sep] minimum 289.42 (161), continuous 289.42 (161); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

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
| 14 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=15 end=15.18 | deliver_pallet(?pallet=pallet_4) | 0 |
| 16 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=2 end=19.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 19 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=5 end=25.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 25 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=11 end=36.32 | deliver_pallet(?pallet=pallet_4) | 0 |
| 36 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_pallet(?pallet=pallet_4) | 0 |
| 59 | no_current_task |  | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | load_return(?pallet=pallet_6) | 0 |
| 67 | recognition_changed | replaced | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback standing k=31 end=99.00 | load_return(?pallet=pallet_6) | 0 |
| 99 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=5 end=105.00 | load_return(?pallet=pallet_6) | 0 |
| 105 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=11 end=111.03 | load_return(?pallet=pallet_6) | 0 |
| 112 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback standing k=1 end=114.00 | load_return(?pallet=pallet_6) | 0 |
| 114 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=118.00 | load_return(?pallet=pallet_6) | 0 |
| 118 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=4 end=123.00 | load_return(?pallet=pallet_6) | 0 |
| 123 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=9 end=133.00 | load_return(?pallet=pallet_6) | 0 |
| 130 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | load_return(?pallet=pallet_6) | 0 |
| 138 | recognition_changed | retraction | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback moving k=24 end=155.50 | load_return(?pallet=pallet_6) | 0 |
| 147 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback moving k=33 end=155.50 | deliver_pallet(?pallet=pallet_5) | 0 |
| 156 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=1 end=158.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 158 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=3 end=162.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 162 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=7 end=170.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 170 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=15 end=186.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 186 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=31 end=218.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 196 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=41 end=238.00 | None | 0 |
