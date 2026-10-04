# scenario_s16_03: part 4 and the measures (single_task, prior on)

Completion (world tick) 89; terminal decision 91. [sep] minimum 55.51 (42), continuous 55.51 (42); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [(43, 3), (46, 6), (52, 12), (55, 33), (72, 32), (73, 2)] (88 ticks).

## Declared properties

- **PK4a**: holds. tick 0 no_current_task/None admitted deliver_item(item_4) hold 0
- **PK4b**: holds. tick 43 recognition_changed/retraction fallback hold 3
- **PK4d**: holds. next admission: tick 55 recognition_changed/entered admitted coffee_break hold 33
- **PK4e**: holds. item_4 after the break: tick 73 recognition_changed/entered admitted deliver_item(item_4) hold 2; decisions on a fallback stand after 72: []
- **PK4c**: holds. violations in 38 to 75: []

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 43 | recognition_changed | retraction | none(leader_inadequate) | deliver_item(?item=item_4) | fallback standing k=2 end=46.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 3 |
| 46 | projection_expired |  | none(below_theta) | deliver_item(?item=item_4) | fallback standing k=5 end=52.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 6 |
| 52 | projection_expired |  | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=11 end=64.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 12 |
| 55 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 33 |
| 72 | recognition_changed | replaced | none(leader_no_observation) | deliver_item(?item=item_4) | fallback standing k=31 end=104.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 32 |
| 73 | recognition_changed | entered | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 2 |
| 91 | no_current_task |  | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | None | 0 |
