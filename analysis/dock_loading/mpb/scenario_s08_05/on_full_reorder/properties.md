# scenario_s08_05: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 175; terminal decision 177. [sep] minimum 87.80 (157), continuous 87.47 (157); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

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
| 14 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=15 end=26.40 | deliver_pallet(?pallet=pallet_4) | 0 |
| 27 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback standing k=1 end=29.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 29 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=33.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 33 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=1 end=35.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 35 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=3 end=39.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 39 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=7 end=47.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 47 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=15 end=63.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 63 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=31 end=77.77 | deliver_pallet(?pallet=pallet_4) | 0 |
| 66 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=34 end=77.77 | load_return(?pallet=pallet_6) | 0 |
| 78 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=1 end=80.00 | load_return(?pallet=pallet_6) | 0 |
| 80 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=3 end=84.00 | load_return(?pallet=pallet_6) | 0 |
| 84 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=7 end=92.00 | load_return(?pallet=pallet_6) | 0 |
| 92 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=15 end=108.00 | load_return(?pallet=pallet_6) | 0 |
| 108 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=31 end=140.00 | load_return(?pallet=pallet_6) | 0 |
| 127 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=50 end=178.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 177 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=100 end=278.00 | None | 0 |
