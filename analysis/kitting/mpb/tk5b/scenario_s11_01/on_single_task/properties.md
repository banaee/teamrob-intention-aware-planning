# scenario_s11_01: part 4 and the measures (single_task, prior on)

Completion (world tick) 74; terminal decision 76. [sep] minimum 66.17 (56), continuous 66.15 (56); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [(33, 23)] (23 ticks).

## Declared properties

- **P6.1**: holds. switch at 14 (projection_expired); first grasp of item_8: 64; the human standing: True
- **P6.2**: holds. (tick, the layout's cost difference, item_8's hold): [(0, 3.5, 0), (2, 3.5, 0), (6, 3.5, 0), (14, 3.5, 7)]

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(leader_unwarranted) | deliver_item(?item=item_12) | fallback standing k=1 end=2.00 | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 0 |
| 2 | projection_expired |  | none(leader_unwarranted) | deliver_item(?item=item_12) | fallback standing k=3 end=6.00 | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 0 |
| 6 | projection_expired |  | none(leader_unwarranted) | deliver_item(?item=item_12) | fallback standing k=7 end=14.00 | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 0 |
| 14 | projection_expired |  | none(leader_unwarranted) | deliver_item(?item=item_12) | fallback standing k=15 end=30.00 | deliver_item(?item=item_9,?kitting_table=kitting_table_4) | 0 |
| 30 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=31 end=62.00 | deliver_item(?item=item_9,?kitting_table=kitting_table_4) | 0 |
| 33 | no_current_task |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=34 end=68.00 | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 23 |
| 68 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback moving k=8 end=77.00 | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 0 |
| 76 | no_current_task |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback moving k=16 end=93.00 | None | 0 |
