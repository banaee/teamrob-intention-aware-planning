# scenario_s16_05: part 4 and the measures (single_task, prior on)

Completion (world tick) 106; terminal decision 108. [sep] minimum 60.60 (27), continuous 60.39 (27); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [(14, 5)] (5 ticks).

## Declared properties

- **PK5a.r**: holds. tick 0 no_current_task/None fallback hold 0 gate none(leader_outranked); first admission: tick 48 recognition_changed/entered admitted deliver_item(item_4) hold 0

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(leader_outranked) | deliver_item(?item=item_4) | fallback moving k=1 end=2.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 2 | projection_expired |  | none(leader_outranked) | deliver_item(?item=item_4) | fallback moving k=3 end=6.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 6 | projection_expired |  | none(leader_outranked) | deliver_item(?item=item_4) | fallback moving k=7 end=14.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 14 | projection_expired |  | none(leader_outranked) | deliver_item(?item=item_4) | fallback moving k=15 end=30.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 5 |
| 30 | projection_expired |  | none(leader_outranked) | deliver_item(?item=item_4) | fallback moving k=31 end=45.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 45 | projection_expired |  | none(leader_outranked) | deliver_item(?item=item_4) | fallback standing k=1 end=47.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 47 | projection_expired |  | none(leader_unwarranted) | deliver_item(?item=item_4) | fallback standing k=3 end=51.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 48 | recognition_changed | entered | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 102 | recognition_changed | replaced | none(leader_no_observation) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=105.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 104 | recognition_changed | entered | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 108 | no_current_task |  | clears | coffee_break(?coffee_machine=coffee_machine_0) | admitted coffee_break(?coffee_machine=coffee_machine_0) | None | 0 |
