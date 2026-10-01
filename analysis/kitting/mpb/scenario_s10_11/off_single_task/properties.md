# scenario_s10_11: part 4 and the measures (single_task, prior off)

Completion (world tick) 161; terminal decision 163. [sep] minimum 411.20 (127), continuous 411.19 (127); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

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
| 15 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 29 | no_current_task |  | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 53 | recognition_changed | boundary | none(below_theta) | deliver_item(?item=item_1) | fallback standing k=2 end=56.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 56 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=2 end=59.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 59 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=5 end=65.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 65 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=11 end=77.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 77 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=23 end=101.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 87 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 110 | no_current_task |  | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 135 | recognition_changed | replaced | none(below_theta) | deliver_item(?item=item_1) | fallback standing k=2 end=138.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 138 | projection_expired |  | none(below_theta) | deliver_item(?item=item_7) | fallback moving k=2 end=141.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 141 | projection_expired |  | none(below_theta) | deliver_item(?item=item_7) | fallback moving k=5 end=147.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 145 | recognition_changed | entered | clears | deliver_item(?item=item_7) | admitted deliver_item(?item=item_7) | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 163 | no_current_task |  | none(leader_inadequate) | deliver_item(?item=item_7) | fallback moving k=27 end=183.78 | None | 0 |
