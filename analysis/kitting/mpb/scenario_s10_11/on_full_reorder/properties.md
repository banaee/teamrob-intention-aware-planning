# scenario_s10_11: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 137; terminal decision 138. [sep] minimum 437.79 (134), continuous 437.79 (134); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

## Declared properties

None declared.

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=1 end=2.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=3 end=6.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=7 end=14.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 7 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 35 | no_current_task |  | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 53 | recognition_changed | boundary | none(below_theta) | deliver_item(?item=item_1) | fallback standing k=2 end=56.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 56 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=2 end=59.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 59 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=5 end=65.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 60 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 72 | no_current_task |  | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 116 | no_current_task |  | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 135 | recognition_changed | replaced | none(leader_no_observation) | deliver_item(?item=item_1) | fallback standing k=2 end=138.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 138 | projection_expired |  | none(leader_unwarranted) | deliver_item(?item=item_1) | fallback moving k=2 end=141.00 | None | 0 |
