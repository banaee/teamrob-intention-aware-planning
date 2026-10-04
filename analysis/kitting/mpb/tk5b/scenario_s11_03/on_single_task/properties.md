# scenario_s11_03: part 4 and the measures (single_task, prior on)

Completion (world tick) 113; terminal decision 115. [sep] minimum 51.33 (13), continuous 51.33 (13); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [(6, 3), (14, 16), (53, 43)] (62 ticks).

## Declared properties

- **P11.3a**: holds. switch at 30 (projection_expired); first grasp of item_8 4; carrying item_8 on the tick before: True
- **P11.3b**: holds. item_8 released at 35, 19.4 cm from shelf_3; first grasp of item_9 41
- **P11.3c**: holds. (tick, the return difference, item_8's hold), decisions while carrying: [(6, 9.082, 3), (14, 16.364, 16), (30, 16.364, 32)]

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(leader_unwarranted) | deliver_item(?item=item_12) | fallback standing k=1 end=2.00 | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 0 |
| 2 | projection_expired |  | none(leader_unwarranted) | deliver_item(?item=item_12) | fallback standing k=3 end=6.00 | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 0 |
| 6 | projection_expired |  | none(leader_unwarranted) | deliver_item(?item=item_12) | fallback standing k=7 end=14.00 | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 3 |
| 14 | projection_expired |  | none(leader_unwarranted) | deliver_item(?item=item_12) | fallback standing k=15 end=30.00 | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 16 |
| 30 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=31 end=62.00 | deliver_item(?item=item_9,?kitting_table=kitting_table_4) | 0 |
| 53 | no_current_task |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=54 end=108.00 | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 43 |
| 108 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=48 end=132.49 | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 0 |
| 115 | no_current_task |  | none(leader_inadequate) | coffee_break(?coffee_machine=coffee_machine_0) | fallback moving k=55 end=132.49 | None | 0 |
