# scenario_s10_07: part 4 and the measures (full_reorder, prior on)

Completion (world tick) 137; terminal decision 138. [sep] minimum 441.32 (184), continuous 441.32 (184); near-encounters 0 ticks; F1 classes {'viol': 0, 'stand': 0, 'recede': 0, '?': 0}; holds [] (0 ticks).

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
| 14 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=15 end=28.91 | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 25 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_4,?kitting_table=kitting_table_1) | 0 |
| 35 | no_current_task |  | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 62 | recognition_changed | retraction | none(leader_inadequate) | deliver_item(?item=item_1) | fallback standing k=17 end=80.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 72 | no_current_task |  | none(leader_inadequate) | deliver_item(?item=item_1) | fallback standing k=27 end=100.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 100 | projection_expired |  | none(leader_inadequate) | deliver_item(?item=item_1) | fallback standing k=55 end=156.00 | deliver_item(?item=item_3,?kitting_table=kitting_table_1) | 0 |
| 116 | no_current_task |  | none(leader_inadequate) | deliver_item(?item=item_1) | fallback moving k=10 end=120.50 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 120 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 123 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=3 end=127.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 127 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=3 end=131.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 131 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=7 end=139.00 | deliver_item(?item=item_6,?kitting_table=kitting_table_1) | 0 |
| 138 | recognition_changed | entered | clears | deliver_item(?item=item_2) | admitted deliver_item(?item=item_2) | None | 0 |
