# scenario_s08_10: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 326; terminal decision 328. [sep] minimum 18.78 (263), continuous 16.74 (263); near-encounters 5 ticks; F1 classes {'viol': 0, 'stand': 5, 'recede': 0, '?': 0}; holds [(239, 80)] (80 ticks).

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
| 14 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=15 end=26.40 | load_return(?pallet=pallet_6) | 0 |
| 27 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback standing k=1 end=29.00 | load_return(?pallet=pallet_6) | 0 |
| 29 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=2 end=32.00 | load_return(?pallet=pallet_6) | 0 |
| 32 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=5 end=38.00 | load_return(?pallet=pallet_6) | 0 |
| 38 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=11 end=48.95 | load_return(?pallet=pallet_6) | 0 |
| 48 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | load_return(?pallet=pallet_6) | 0 |
| 79 | recognition_changed | replaced | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback standing k=31 end=111.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 111 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=4 end=116.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 116 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=9 end=126.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 126 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=19 end=146.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 133 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | deliver_pallet(?pallet=pallet_4) | 0 |
| 137 | no_current_task |  | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | load_return(?pallet=pallet_7) | 0 |
| 160 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=163.00 | load_return(?pallet=pallet_7) | 0 |
| 163 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=5 end=169.00 | load_return(?pallet=pallet_7) | 0 |
| 169 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=11 end=181.00 | load_return(?pallet=pallet_7) | 0 |
| 181 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=23 end=205.00 | load_return(?pallet=pallet_7) | 0 |
| 198 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=40 end=239.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 239 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=81 end=321.00 | deliver_pallet(?pallet=pallet_5) | 80 |
| 321 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=48 end=370.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 328 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=55 end=384.00 | None | 0 |
