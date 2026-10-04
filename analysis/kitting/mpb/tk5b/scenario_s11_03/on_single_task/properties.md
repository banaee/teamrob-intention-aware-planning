# scenario_s11_03: part 4 and the measures (single_task, prior on)

Completion (world tick) 35; terminal decision 37. [sep] minimum 11.33 (12), continuous 11.33 (12); near-encounters 9 ticks; F1 classes {'viol': 2, 'stand': 4, 'recede': 3, '?': 0}; holds [] (0 ticks).

## Declared properties

- **P11.3a**: DOES NOT HOLD. switch at 16 (recognition_changed); first grasp of item_8 4; carrying item_8 on the tick before: False
- **P11.3b**: DOES NOT HOLD. no release of item_8 after the switch
- **P11.3c**: DOES NOT HOLD. (tick, the return difference, item_8's hold), decisions while carrying: []

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | clears | deliver_item(?item=item_12) | admitted deliver_item(?item=item_12) | deliver_item(?item=item_8,?kitting_table=kitting_table_2) | 0 |
| 16 | recognition_changed | retraction | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=17 end=34.00 | deliver_item(?item=item_9,?kitting_table=kitting_table_4) | 0 |
| 34 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=35 end=70.00 | deliver_item(?item=item_9,?kitting_table=kitting_table_4) | 0 |
| 37 | no_current_task |  | none(leader_inadequate) | deliver_item(?item=item_12) | fallback standing k=38 end=76.00 | None | 0 |
