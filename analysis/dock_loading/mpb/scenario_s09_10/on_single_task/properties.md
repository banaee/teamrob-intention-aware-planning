# scenario_s09_10: part 4 and the measures (single_task, prior on)

Completion (world tick) 327; terminal decision 329. [sep] minimum 79.01 (264), continuous 78.96 (265); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

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
| 18 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=2 end=21.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 21 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=5 end=27.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 27 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=11 end=38.66 | deliver_pallet(?pallet=pallet_5) | 0 |
| 38 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_pallet(?pallet=pallet_5) | 0 |
| 59 | no_current_task |  | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_pallet(?pallet=pallet_4) | 0 |
| 69 | recognition_changed | replaced | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback standing k=31 end=101.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 101 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=4 end=106.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 106 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=9 end=113.45 | deliver_pallet(?pallet=pallet_4) | 0 |
| 114 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback standing k=1 end=116.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 116 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=120.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 120 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=128.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 128 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=144.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 144 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=31 end=176.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 150 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=37 end=188.00 | load_return(?pallet=pallet_6) | 0 |
| 188 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=75 end=264.00 | load_return(?pallet=pallet_6) | 0 |
| 238 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback moving k=25 end=254.27 | load_return(?pallet=pallet_7) | 0 |
| 255 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=1 end=257.00 | load_return(?pallet=pallet_7) | 0 |
| 257 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=3 end=261.00 | load_return(?pallet=pallet_7) | 0 |
| 261 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=7 end=269.00 | load_return(?pallet=pallet_7) | 0 |
| 269 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=15 end=285.00 | load_return(?pallet=pallet_7) | 0 |
| 285 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=31 end=317.00 | load_return(?pallet=pallet_7) | 0 |
| 317 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=63 end=381.00 | load_return(?pallet=pallet_7) | 0 |
| 329 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=75 end=405.00 | None | 0 |
