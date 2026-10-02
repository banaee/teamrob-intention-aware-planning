# scenario_s09_05: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 194; terminal decision 196. [sep] minimum 91.44 (115), continuous 91.05 (115); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: [{'tick': 36, 'objects': ['standby_place'], 'k': 15, 'duration': 15.0, 'end': 52.0}]

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=1 end=2.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 2 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=3 end=6.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 6 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=7 end=14.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 14 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback moving k=15 end=15.18 | deliver_pallet(?pallet=pallet_4) | 0 |
| 16 | projection_expired |  | none(below_theta) | confirm_delivered_pallet(?pallet=pallet_0) | fallback standing k=1 end=18.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 18 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=22.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 22 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=1 end=24.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 24 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=3 end=28.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 28 | projection_expired |  | none(below_theta) | office_break(?office_chair=office_chair) | fallback moving k=7 end=36.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 36 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=15 end=52.00 | deliver_pallet(?pallet=pallet_4) | 0 |
| 52 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=31 end=56.35 | deliver_pallet(?pallet=pallet_4) | 0 |
| 57 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=59.00 | load_return(?pallet=pallet_6) | 0 |
| 59 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=63.00 | load_return(?pallet=pallet_6) | 0 |
| 63 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=7 end=71.00 | load_return(?pallet=pallet_6) | 0 |
| 71 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=15 end=87.00 | load_return(?pallet=pallet_6) | 0 |
| 87 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=31 end=119.00 | load_return(?pallet=pallet_6) | 0 |
| 119 | projection_expired |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=63 end=183.00 | load_return(?pallet=pallet_6) | 0 |
| 147 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=91 end=239.00 | deliver_pallet(?pallet=pallet_5) | 0 |
| 196 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=140 end=337.00 | None | 0 |
