# scenario_s10_02: part 4 and the measures (single_task, prior off)

Completion (world tick) 65; terminal decision 67. [sep] minimum 38.25 (46), continuous 38.05 (47); near-encounters 4 ticks; F1 classes {'viol': 3, 'stand': 0, 'recede': 1, '?': 0}; holds [(26, 4)] (4 ticks).

## Declared properties

- **P2a**: holds. tick 26: winner deliver_item(?item=item_7,?kitting_table=kitting_table_3), hold 4
- **P2b**: DOES NOT HOLD. assessed window ticks 27 to 63 (T_h 36.3276253029822); F1 violations [45, 46, 47]

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=1 end=2.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 2 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=3 end=6.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 6 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=7 end=14.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 14 | projection_expired |  | none(below_theta) | deliver_item(?item=item_1) | fallback moving k=15 end=28.91 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 26 | recognition_changed | entered | clears | deliver_item(?item=item_1) | admitted deliver_item(?item=item_1) | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 4 |
| 61 | recognition_changed | replaced | none(below_theta) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=64.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 64 | projection_expired |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=2 end=67.00 | deliver_item(?item=item_7,?kitting_table=kitting_table_3) | 0 |
| 67 | no_current_task |  | none(below_theta) | deliver_item(?item=item_2) | fallback moving k=5 end=73.00 | None | 0 |
