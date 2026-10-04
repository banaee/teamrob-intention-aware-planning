# scenario_s16_05: part 4 and the measures (single_task, prior on)

Completion (world tick) 101; terminal decision 102. [sep] minimum 28.63 (24), continuous 28.33 (25); near-encounters 6 ticks; F1 classes {'viol': 4, 'stand': 0, 'recede': 2, '?': 0}; holds [] (0 ticks).

## Declared properties

- **PK5a**: holds. tick 0 no_current_task/None admitted deliver_item(item_4) hold 0
- **PK5b**: holds. violations in 15 to 35: [22, 23, 24, 25]; below [22, 23, 24, 25, 26, 27]

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 46 | recognition_changed | boundary | none(leader_no_observation) | deliver_item(?item=item_4) | fallback standing k=2 end=49.00 | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 47 | recognition_changed | entered | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 0 |
| 102 | recognition_changed | replaced | none(leader_no_observation) | coffee_break(?coffee_machine=coffee_machine_0) | fallback standing k=2 end=105.00 | None | 0 |
