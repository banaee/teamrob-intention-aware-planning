# scenario_s10_08: part 4 and the measures (single_task, prior on)

Completion (world tick) 167; terminal decision 169. [sep] minimum 319.79 (0), continuous 316.43 (0); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=1 end=2.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=3 end=6.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=7 end=14.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 14 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=15 end=28.91 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 25 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 33 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=5 end=39.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 37 | no_current_task |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=3 end=41.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 41 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=7 end=49.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 46 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 74 | no_current_task |  | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 108 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=111.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 111 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=2 end=114.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 114 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=5 end=120.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 118 | no_current_task |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=9 end=128.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 128 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=19 end=138.87 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 135 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 169 | no_current_task |  | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | None | 0 |
