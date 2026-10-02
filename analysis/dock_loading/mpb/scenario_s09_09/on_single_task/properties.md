# scenario_s09_09: part 4 and the measures (single_task, prior on)

Completion (world tick) 145; terminal decision 147. [sep] minimum 25.08 (44), continuous 20.85 (44); near-encounters 3 ticks; F1 classes {'viol': 2, 'stand': 0, 'recede': 1, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## k9

{'admission': {'tick': 37, 'key': 'office_break(?office_chair=office_chair)', 'winner': 'deliver_pallet(?pallet=pallet_4)', 'hold': 0}, 'recorded_hypothesis_inadequate_from': 59, 'retraction': None, 'masked_by_no_current_task': True}

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=1 end=2.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 2 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=3 end=6.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 6 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=7 end=14.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 14 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=15 end=24.31 | deliver_pallet(?pallet=pallet_4) | 0 |
| 21 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | deliver_pallet(?pallet=pallet_4) | 0 |
| 26 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=29.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 29 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=32.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 32 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=38.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 37 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | deliver_pallet(?pallet=pallet_4) | 0 |
| 59 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=8 end=68.00 | load_return(?pallet=pallet_6) | 0 |
| 68 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=17 end=86.00 | load_return(?pallet=pallet_6) | 0 |
| 86 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback moving k=3 end=90.00 | load_return(?pallet=pallet_6) | 0 |
| 90 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback moving k=7 end=98.00 | load_return(?pallet=pallet_6) | 0 |
| 98 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback moving k=15 end=103.07 | load_return(?pallet=pallet_6) | 0 |
| 104 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=1 end=106.00 | load_return(?pallet=pallet_6) | 0 |
| 106 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=3 end=110.00 | load_return(?pallet=pallet_6) | 0 |
| 110 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=7 end=118.00 | load_return(?pallet=pallet_6) | 0 |
| 118 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=15 end=134.00 | load_return(?pallet=pallet_6) | 0 |
| 134 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=31 end=166.00 | load_return(?pallet=pallet_6) | 0 |
| 147 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=44 end=192.00 | None | 0 |
