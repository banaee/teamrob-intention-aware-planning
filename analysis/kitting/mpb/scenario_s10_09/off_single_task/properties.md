# scenario_s10_09: part 4 and the measures (single_task, prior off)

Completion (world tick) 161; terminal decision 162. [sep] minimum 387.55 (66), continuous 387.55 (66); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## x5_ground1

[{'first': 60, 'last': 72, 'refused_decisions': [60, 67, 72], 'ground1_from': 61}]

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=1 end=2.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=3 end=6.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=7 end=14.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 14 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=15 end=28.91 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 26 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 29 | no_current_task |  | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 60 | recognition_changed | retraction | none(leader_inadequate) | deliver_item(?item=item_1) | fallback moving k=29 end=71.99 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 67 | no_current_task |  | none(leader_inadequate) | deliver_item(?item=item_1) | fallback moving k=36 end=71.99 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 72 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_1) | fallback standing k=1 end=74.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 74 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=78.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 78 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=4 end=83.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 83 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=9 end=93.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 93 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=19 end=113.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 110 | no_current_task |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=36 end=126.87 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 113 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 159 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=162.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 162 | projection_expired |  | none(below_theta) | deliver_item(?item=item_7) | fallback moving k=2 end=165.00 | None | 0 |
