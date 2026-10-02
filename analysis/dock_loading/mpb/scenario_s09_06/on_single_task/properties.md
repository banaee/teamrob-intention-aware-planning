# scenario_s09_06: part 4 and the measures (single_task, prior on)

Completion (world tick) 327; terminal decision 329. [sep] minimum 78.90 (264), continuous 78.87 (265); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=1 end=2.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 2 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=3 end=6.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 6 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=7 end=14.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 14 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=15 end=15.18 | deliver_pallet(?pallet=pallet_5) | 0 |
| 16 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback standing k=1 end=18.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 18 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=22.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 22 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=4 end=27.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 27 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=9 end=37.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 36 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_pallet(?pallet=pallet_5) | 0 |
| 59 | no_current_task |  | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_pallet(?pallet=pallet_4) | 0 |
| 71 | recognition_changed | replaced | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback standing k=31 end=103.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 83 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | deliver_pallet(?pallet=pallet_4) | 0 |
| 84 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=87.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 87 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=2 end=90.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 90 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=96.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 96 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=11 end=108.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 100 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | deliver_pallet(?pallet=pallet_4) | 0 |
| 109 | recognition_changed | retraction | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback moving k=24 end=126.30 | deliver_pallet(?pallet=pallet_4) | 0 |
| 127 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=1 end=129.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 129 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=3 end=133.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 133 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=7 end=141.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 141 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=15 end=157.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 150 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=24 end=175.00 | load_return(?pallet=pallet_6) | 0 |
| 175 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=49 end=225.00 | load_return(?pallet=pallet_6) | 0 |
| 225 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=99 end=325.00 | load_return(?pallet=pallet_6) | 0 |
| 238 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=112 end=351.00 | load_return(?pallet=pallet_7) | 0 |
| 329 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=203 end=533.00 | None | 0 |
