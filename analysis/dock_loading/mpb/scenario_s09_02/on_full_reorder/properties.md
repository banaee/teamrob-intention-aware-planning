# scenario_s09_02: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 194; terminal decision 196. [sep] minimum 97.40 (115), continuous 97.27 (115); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

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
| 16 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback standing k=1 end=18.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 18 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=22.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 22 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=4 end=27.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 27 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=9 end=35.62 | deliver_pallet(?pallet=pallet_4) | 0 |
| 36 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback standing k=1 end=38.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 38 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=42.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 42 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=4 end=47.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 47 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=9 end=57.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 54 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | deliver_pallet(?pallet=pallet_4) | 0 |
| 59 | no_current_task |  | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | load_return(?pallet=pallet_6) | 0 |
| 62 | recognition_changed | retraction | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback moving k=24 end=79.18 | load_return(?pallet=pallet_6) | 0 |
| 80 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=1 end=82.00 | load_return(?pallet=pallet_6) | 0 |
| 82 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=3 end=86.00 | load_return(?pallet=pallet_6) | 0 |
| 86 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=7 end=94.00 | load_return(?pallet=pallet_6) | 0 |
| 94 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=15 end=110.00 | load_return(?pallet=pallet_6) | 0 |
| 110 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=31 end=142.00 | load_return(?pallet=pallet_6) | 0 |
| 142 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=63 end=206.00 | load_return(?pallet=pallet_6) | 0 |
| 147 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=68 end=216.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 196 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=117 end=314.00 | None | 0 |
