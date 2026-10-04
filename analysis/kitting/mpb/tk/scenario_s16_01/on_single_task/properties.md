# scenario_s16_01: part 4 and the measures (single_task, prior on)

Completion (world tick) 68; terminal decision 70. [sep] minimum 42.20 (49), continuous 41.66 (50); near-encounters 3 ticks; F1 classes {'viol': 2, 'stand': 0, 'recede': 1, '?': 0}; holds [(0, 5)] (5 ticks).

## Declared properties

- **PK3a**: holds. tick 0 no_current_task/None admitted deliver_item(item_4) hold 5
- **PK3b**: holds. projection_expired decisions before 47: []
- **PK3c**: DOES NOT HOLD. violations [49, 50]; below [49, 50, 51] (40 to 60)

## Detectors

- TODO-134 (a decision on a fallback stand whose first robot tick violates): none
- The arrival-tick ray: none

## Decisions

| tick | trigger | cause | gate | leader | projection | winner | hold |
|---|---|---|---|---|---|---|---|
| 0 | no_current_task |  | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | deliver_item(?item=item_5,?kitting_table=kitting_table_1) | 5 |
| 70 | no_current_task |  | clears | deliver_item(?item=item_4) | admitted deliver_item(?item=item_4) | None | 0 |
