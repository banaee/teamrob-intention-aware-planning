# scenario_s10_03: part 4 and the measures (single_task, prior on)

Completion (world tick) 172; terminal decision 174. [sep] minimum 409.02 (154), continuous 408.88 (155); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

- **P3a**: holds. interval 46 to 54: decisions []
- **P3b**: holds. record on the interval: ['deliver_item(?item=item_1)']
- **P3c**: holds. leaders on the interval: ['deliver_item(?item=item_1)']; item_1 assigned

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## retention_observation_warrant

[(46, 'observation'), (47, 'observation'), (48, 'observation'), (49, 'observation'), (50, 'observation'), (51, 'observation'), (52, 'observation'), (53, 'observation'), (54, 'observation')]

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=1 end=2.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=3 end=6.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=7 end=14.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 8 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 40 | no_current_task |  | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 55 | recognition_changed | retraction | none(leader_inadequate) | deliver_item(?item=item_1) | fallback moving k=10 end=66.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 66 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_1) | fallback moving k=21 end=74.71 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 75 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=1 end=77.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 76 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 79 | no_current_task |  | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 105 | recognition_changed | replaced | none(below_theta) | deliver_item(?item=item_1) | fallback standing k=31 end=137.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 120 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 123 | no_current_task |  | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 149 | recognition_changed | replaced | none(leader_no_observation) | deliver_item(?item=item_2) | fallback standing k=3 end=153.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 151 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 174 | no_current_task |  | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | None | 0 |
