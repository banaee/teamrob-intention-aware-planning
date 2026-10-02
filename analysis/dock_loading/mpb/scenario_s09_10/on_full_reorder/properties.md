# scenario_s09_10: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 265; terminal decision 267. [sep] minimum 129.86 (238), continuous 128.83 (238); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

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
| 14 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=15 end=15.18 | load_return(?pallet=pallet_6) | 0 |
| 16 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback standing k=1 end=18.00 | load_return(?pallet=pallet_6) | 0 |
| 18 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=2 end=21.00 | load_return(?pallet=pallet_6) | 0 |
| 21 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=5 end=27.00 | load_return(?pallet=pallet_6) | 0 |
| 27 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=11 end=38.66 | load_return(?pallet=pallet_6) | 0 |
| 38 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | load_return(?pallet=pallet_6) | 0 |
| 69 | recognition_changed | replaced | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback standing k=31 end=101.00 | load_return(?pallet=pallet_6) | 0 |
| 81 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=11 end=91.75 | deliver_pallet(?pallet=pallet_4) | 0 |
| 92 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback standing k=1 end=94.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 94 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=98.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 98 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=1 end=100.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 100 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=3 end=104.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 104 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=7 end=112.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 112 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=15 end=113.45 | deliver_pallet(?pallet=pallet_4) | 0 |
| 114 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback standing k=1 end=116.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 116 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=120.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 120 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=128.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 128 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=144.00 | load_return(?pallet=pallet_7) | 0 |
| 144 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=31 end=176.00 | load_return(?pallet=pallet_7) | 0 |
| 176 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=63 end=240.00 | load_return(?pallet=pallet_7) | 0 |
| 218 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=224.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 224 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=11 end=236.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 236 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback moving k=23 end=254.27 | deliver_pallet(?pallet=pallet_5) | 0 |
| 255 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=1 end=257.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 257 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=3 end=261.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 261 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=7 end=269.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 267 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=13 end=281.00 | None | 0 |
