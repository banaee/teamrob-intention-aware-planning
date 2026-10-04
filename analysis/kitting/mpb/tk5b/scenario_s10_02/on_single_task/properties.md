# scenario_s10_02: part 4 and the measures (single_task, prior on)

Completion (world tick) 66; terminal decision 68. [sep] minimum 53.19 (47), continuous 52.20 (47); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [(8, 5)] (5 ticks).

## Declared properties

- **P2a**: holds. tick 8: winner deliver_item(?item=item_7,?kitting_table=kitting_table_3), hold 5
- **P2b**: holds. assessed window ticks 9 to 63 (T_h 54.3276253029822); F1 violations []

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=1 end=2.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=3 end=6.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=7 end=14.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 8 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 5 |
| 61 | recognition_changed | replaced | none(leader_no_observation) | deliver_item(?item=item_2) | fallback standing k=2 end=64.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 62 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 68 | no_current_task |  | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | None | 0 |
