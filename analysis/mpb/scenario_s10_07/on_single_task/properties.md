# scenario_s10_07: part 4 and the measures (single_task, prior on)

Completion (world tick) 161; terminal decision 163. [sep] minimum 405.43 (120), continuous 405.43 (120); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

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
| 29 | no_current_task |  | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 62 | recognition_changed | retraction | none(leader_inadequate) | deliver_item(?item=item_1) | fallback standing k=17 end=80.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 67 | no_current_task |  | none(leader_inadequate) | deliver_item(?item=item_1) | fallback standing k=22 end=90.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 90 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_1) | fallback standing k=45 end=136.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 110 | no_current_task |  | none(leader_inadequate) | deliver_item(?item=item_1) | fallback moving k=4 end=115.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 115 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_1) | fallback moving k=9 end=120.50 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 120 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 123 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=127.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 127 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=3 end=131.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 131 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=7 end=139.00 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 138 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 163 | no_current_task |  | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | None | 0 |
