# scenario_s05_05: part 4 and the measures (single_task, prior on)

Completion (world tick) 422; terminal decision 424. [sep] minimum 10.84 (447), continuous 10.81 (451); near-encounters 9 ticks; F1 classes {'viol': 0, 'stand': 9, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

- **M(i)**: holds. the terminal decision 424
- **M(ii)**: holds. entries still open at the run's end: []
- **M(iii)**: holds. F1 classes {'viol': 0, 'stand': 9, 'recede': 0, '?': 0}
- **M(iv)**: holds. (pallet, the tick its delivery is first observable, the scan's first live tick): [('pallet_2', 58, 58), ('pallet_3', 150, 150), ('pallet_0', 305, 305), ('pallet_1', 422, 422)]

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## m2

{'two_scans_live_in_one_bay': [], 'decisions_at_an_occupied_bay': [84]}

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=2.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 2 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=6.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 6 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=14.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 14 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=30.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 30 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=31 end=62.00 | deliver_pallet(?pallet=pallet_2) | 0 |
| 60 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=3 end=64.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 64 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_2) | fallback moving k=7 end=72.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 65 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_2) | admitted confirm_delivered_pallet(?pallet=pallet_2) | deliver_pallet(?pallet=pallet_3) | 0 |
| 84 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=87.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 87 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=90.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 90 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=96.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 96 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=11 end=108.00 | deliver_pallet(?pallet=pallet_3) | 0 |
| 105 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | deliver_pallet(?pallet=pallet_3) | 0 |
| 152 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback standing k=32 end=185.00 | load_return(?pallet=pallet_4) | 0 |
| 155 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | load_return(?pallet=pallet_4) | 0 |
| 166 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=46 end=213.00 | load_return(?pallet=pallet_4) | 0 |
| 182 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_3) | admitted confirm_delivered_pallet(?pallet=pallet_3) | load_return(?pallet=pallet_4) | 0 |
| 204 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=207.00 | load_return(?pallet=pallet_4) | 0 |
| 207 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=2 end=210.00 | load_return(?pallet=pallet_4) | 0 |
| 210 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=5 end=216.00 | load_return(?pallet=pallet_4) | 0 |
| 216 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=11 end=228.00 | load_return(?pallet=pallet_4) | 0 |
| 228 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | load_return(?pallet=pallet_4) | 0 |
| 244 | recognition_changed | retraction | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=16 end=261.00 | load_return(?pallet=pallet_4) | 0 |
| 250 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=22 end=273.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 273 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=45 end=319.00 | deliver_pallet(?pallet=pallet_0) | 0 |
| 307 | no_current_task |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=3 end=311.00 | load_return(?pallet=pallet_5) | 0 |
| 311 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=7 end=319.00 | load_return(?pallet=pallet_5) | 0 |
| 319 | recognition_changed | entered | clears | confirm_delivered_pallet(?pallet=pallet_0) | admitted confirm_delivered_pallet(?pallet=pallet_0) | load_return(?pallet=pallet_5) | 0 |
| 334 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=337.00 | load_return(?pallet=pallet_5) | 0 |
| 337 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=2 end=340.00 | load_return(?pallet=pallet_5) | 0 |
| 340 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=5 end=346.00 | load_return(?pallet=pallet_5) | 0 |
| 346 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=11 end=358.00 | load_return(?pallet=pallet_5) | 0 |
| 352 | recognition_changed | entered | clears | office_break(?office_chair=office_chair) | admitted office_break(?office_chair=office_chair) | load_return(?pallet=pallet_5) | 0 |
| 362 | recognition_changed | retraction | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=1 end=364.00 | load_return(?pallet=pallet_5) | 0 |
| 364 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=3 end=368.00 | load_return(?pallet=pallet_5) | 0 |
| 368 | no_current_task |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=7 end=376.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 376 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=15 end=392.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 392 | projection_expired |  | none(leader_inadequate) | office_break(?office_chair=office_chair) | fallback standing k=31 end=424.00 | deliver_pallet(?pallet=pallet_1) | 0 |
| 424 | no_current_task |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=3 end=428.00 | None | 0 |
