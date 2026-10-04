# T-K part 1, step 5: the planning cases with context knowledge (kitting, env_layout_18): the report

Stage 3 (4 October 2026). The set, its expectations and their md5s: `README.md`. Nine runs, single_task, assignment
knowledge on; the sides: off (context knowledge off), on with no fact, on with the raising fact (break_time or
room_warm from tick 0).

## 1. The chain works

All nine runs agree with the oracle: 0 disagreements per tick, per decision and per log line (the gate, the leader,
the warrant, the identity of the admitted plan, the fallback, and the chain of triggers and causes). The runs left the
expectations' md5s unchanged. In every run the completion equals the robot-alone reference plus the hold ticks the
robot executed (63 + 6, + 5, + 4; 57 + 56, + 32, + 33; 101 + 5, + 0, + 5). With context knowledge on, the
admission the meta-planner holds, the projection it builds and the robot's decision follow as the oracle and the
reference state.

## 2. A gain where the human acts in accord with the context

The raised state (case 1, the coffee break inside break_time): the coffee break is admitted at 22 instead of 36, and
the robot's long hold for the stand at the machine is decided 14 ticks earlier, 80 cm from the machine instead of 95.
The outcome is the same: the robot waits for the human's stand either way. No fact (case 3, the last delivery at the
turn at shelf_4): the delivery is admitted on the human's first step, and the robot decides its hold at 0 instead of at
45 and 47, at its start instead of beside the turn. It completes one tick earlier (68 against 69) and its minimum
separation is 41.7 cm against 37.0. But it does not keep min_separation: the admitted plan runs about one tick ahead of
the executed human at the turn (TODO-146), and the planned clearance shrinks to 42 cm with the robot moving. The
clearest gain in the set comes from the no-fact early admission after an observed coffee break (E2's form, inside
cases 1 and 4's script): both on sides admit the delivery at 73. Off rests on the observed 31-tick stand from 72 and
holds until 97 while the human left at 74, so it completes at 113 against 89 and 90.

## 3. A cost where the human acts against the context

Case 5 (the A/C, no fact): the delivery is admitted from 0 to 45 while the human walks to the switch. The robot rests on
that plan, makes no hold and crosses the human at 28.3 cm while moving (F1 violations at 22 to 25). Off and the side
with room_warm hold 5 at 14 on the fallback and keep 60.4 cm; the robot pays 5 ticks for it (106 against 101). Case 4
(the coffee break, no fact): the delivery is admitted from 0 to 42 while the human walks to the machine, and the robot
plans no hold. Unheld, its route would pass the standing human at 12 cm. The retraction at 43 puts the decision on the
stand fallback and holds the robot 55.5 cm from the human (holds 3, 6, 12, then 33 once the coffee break is admitted at
55). Off decided its hold at 36 and waited 95 cm away. The cost is closeness: 39.5 cm nearer than off, still above
min_separation. The retraction and the decisions after it are what bounded it.

## Per case and side

`tk5.py report`. Decisions: tick, trigger (nct no_current_task, rc recognition_changed, pe projection_expired) and
cause, the projection, the hold. Held admissions: from a decision that admits to the next decision, up to the
terminal decision. Completion: the world tick. Window: the case's (turn 40 to 60, stand 38 to 75, walk 15 to 35),
the continuous [sep] minimum and F1's robot violations.

| scenario | side | case | decisions (tick trigger/cause: projection, hold) | held admissions | completion | window: min separation (tick), F1 violations | run: min separation (tick) |
|---|---|---|---|---|---|---|---|
| scenario_s16_01 | off | 3, 2 (reference) | 0 nct: fallback moving k=1 end=2, 0; 2 pe: fallback moving k=3 end=6, 0; 6 pe: fallback moving k=7 end=14, 0; 14 pe: fallback moving k=15 end=30, 0; 30 pe: fallback moving k=31 end=44, 0; 45 pe: fallback standing k=1 end=47, 2; 47 rc/entered: admitted deliver_item(item_4), 4; 71 nct: admitted deliver_item(item_4), 0 | deliver_item(item_4) 47-70 | 69 | 37.0 (48), [44] | 37.0 (48) |
| scenario_s16_01 | on, no fact | 3 | 0 nct: admitted deliver_item(item_4), 5; 70 nct: admitted deliver_item(item_4), 0 | deliver_item(item_4) 0-69 | 68 | 41.7 (50), [49, 50] | 41.7 (50) |
| scenario_s16_02 | on, break_time | 2 | 0 nct: fallback moving k=1 end=2, 0; 2 pe: fallback moving k=3 end=6, 0; 6 pe: fallback moving k=7 end=14, 0; 14 pe: fallback moving k=15 end=30, 0; 30 pe: fallback moving k=31 end=44, 0; 38 rc/entered: admitted deliver_item(item_4), 4; 69 nct: admitted deliver_item(item_4), 0 | deliver_item(item_4) 38-68 | 67 | 29.3 (49), [48, 49] | 29.3 (49) |
| scenario_s16_03 | off | 1, 4 (reference) | 0 nct: fallback moving k=1 end=2, 0; 2 pe: fallback moving k=3 end=6, 0; 6 pe: fallback moving k=7 end=14, 0; 14 pe: fallback moving k=15 end=30, 0; 30 pe: fallback moving k=31 end=42, 0; 36 rc/entered: admitted coffee_break, 31; 72 rc/replaced: fallback standing k=31 end=104, 30; 97 rc/entered: admitted deliver_item(item_4), 0; 115 nct: admitted deliver_item(item_4), 0 | coffee_break 36-71, deliver_item(item_4) 97-114 | 113 | 95.0 (71), none | 59.5 (27) |
| scenario_s16_03 | on, no fact | 4 | 0 nct: admitted deliver_item(item_4), 0; 43 rc/retraction: fallback standing k=2 end=46, 3; 46 pe: fallback standing k=5 end=52, 6; 52 pe: fallback standing k=11 end=64, 12; 55 rc/entered: admitted coffee_break, 33; 72 rc/replaced: fallback standing k=31 end=104, 32; 73 rc/entered: admitted deliver_item(item_4), 2; 91 nct: admitted deliver_item(item_4), 0 | deliver_item(item_4) 0-42, coffee_break 55-71, deliver_item(item_4) 73-90 | 89 | 55.5 (42), none | 55.5 (42) |
| scenario_s16_04 | on, break_time | 1 | 0 nct: fallback moving k=1 end=2, 0; 2 pe: fallback moving k=3 end=6, 0; 6 pe: fallback moving k=7 end=14, 0; 14 pe: fallback moving k=15 end=30, 0; 22 rc/entered: admitted coffee_break, 32; 72 rc/replaced: fallback standing k=31 end=104, 29; 73 rc/entered: admitted deliver_item(item_4), 0; 92 nct: admitted deliver_item(item_4), 0 | coffee_break 22-71, deliver_item(item_4) 73-91 | 90 | 80.1 (75), none | 68.5 (26) |
| scenario_s16_05 | off | 5 (reference) | 0 nct: fallback moving k=1 end=2, 0; 2 pe: fallback moving k=3 end=6, 0; 6 pe: fallback moving k=7 end=14, 0; 14 pe: fallback moving k=15 end=30, 5; 30 pe: fallback moving k=31 end=45, 0; 45 pe: fallback standing k=1 end=47, 0; 47 pe: fallback standing k=3 end=51, 0; 51 pe: fallback moving k=4 end=54, 0; 54 pe: fallback standing k=1 end=56, 0; 56 pe: fallback standing k=3 end=60, 0; 60 pe: fallback moving k=4 end=65, 0; 63 rc/entered: admitted deliver_item(item_4), 0; 102 rc/replaced: fallback standing k=2 end=105, 0; 105 pe: fallback moving k=2 end=108, 0; 108 nct: fallback moving k=5 end=114, 0 | deliver_item(item_4) 63-101 | 106 | 60.4 (27), none | 60.4 (27) |
| scenario_s16_05 | on, no fact | 5 | 0 nct: admitted deliver_item(item_4), 0; 46 rc/boundary: fallback standing k=2 end=49, 0; 47 rc/entered: admitted deliver_item(item_4), 0; 102 rc/replaced: fallback standing k=2 end=105, 0 | deliver_item(item_4) 0-45, deliver_item(item_4) 47-101 | 101 | 28.3 (25), [22, 23, 24, 25] | 28.3 (25) |
| scenario_s16_06 | on, room_warm | 5, the A/C raised | 0 nct: fallback moving k=1 end=2, 0; 2 pe: fallback moving k=3 end=6, 0; 6 pe: fallback moving k=7 end=14, 0; 14 pe: fallback moving k=15 end=30, 5; 30 pe: fallback moving k=31 end=45, 0; 45 pe: fallback standing k=1 end=47, 0; 47 rc/entered: admitted deliver_item(item_4), 0; 102 rc/replaced: fallback standing k=2 end=105, 0; 104 rc/entered: admitted coffee_break, 0; 108 nct: admitted coffee_break, 0 | deliver_item(item_4) 47-101, coffee_break 104-107 | 106 | 60.4 (27), none | 60.4 (27) |

The declared properties: all hold except PK3c (scenario_s16_01, on: violations at 49 and 50, 41.7 cm) and PK2b
(scenario_s16_02: violations at 48 and 49, 29.3 cm); per run in `<scenario>/on_single_task/properties.md`.

## Per case, what context knowledge changed for the robot

- Case 1 (raised, in accord; scenario_s16_04 against scenario_s16_03 off): the decision on the stand 14 ticks earlier
  (22 against 36). Nothing in ticks from break_time itself: 90 against 89 with no fact; the 23 ticks against off come
  from the admission after the break.
- Case 2 (raised, against; scenario_s16_02): break_time delays the correct admission to 38 and the hold is decided 7
  ticks before the turn. A cost in separation (29.3 cm against 41.7 with no fact and 37.0 off, 2 violation ticks). A
  gain of 1 to 2 ticks (67 against 68 and 69).
- Case 3 (no fact, in accord; scenario_s16_01): the decision at 0 instead of 45 and 47. A gain of 1 tick and 4.7 cm in
  the minimum, but 2 violation ticks against off's 1; min_separation is not kept (TODO-146).
- Case 4 (no fact, against; scenario_s16_03 on): no decision between 0 and the retraction at 43; the retraction's
  decision holds the robot at 55.5 cm. A cost in separation against off (95.0 cm). Nothing lost in ticks (89 against
  113, the post-break gain).
- Case 5 (no fact, against; scenario_s16_05 on): no hold, a pass at 28.3 cm while moving. A cost of 32.1 cm and 4
  violation ticks; a gain of 5 ticks. With room_warm (scenario_s16_06) the robot decides exactly as off.

## What surprised

- The early correct admission did not keep min_separation at the turn, and the later one (case 2) came closer than
  off. Realization clears the robot against the admitted plan, and that plan has the human stop at the arrival radius
  (145, -420) and leave at 47.1. The executed human walks on to (148, -438) and leaves at 48. About one tick and 18 cm on the
  human's side (TODO-146's rounding, measured here at a turn), and about 11 cm on the robot's (its executed position at 49
  ahead of its plan, step quantisation) turn a planned minimum of 54.8 cm (at 49.2) into an executed 41.7; in case 2,
  51.0 into 29.3.
- The largest difference in ticks is not from break_time or the A/C. After the observed coffee break, off holds for 25
  ticks on a stand fallback that projects the observed 31-tick stand forward. The on sides end it at 73 by admitting
  the lone delivery (the recency fact suppresses the coffee break; without it the delivery's prior is 0.96 anyway).
- In the raised state the gain is only an earlier decision. Off's admission at 36 still comes before the stand
  begins at 42.

## Flags

- The room env_layout_18: the three robot objects and their positions are ccode's (stage 1, revised).
- The human's reduced assignment (item_4 alone) instead of step 4's scripts: no prefix with a working robot; the lone
  delivery is admitted on the first step, not on a previous task's pin tick.
- One robot task per case and single_task only (with one task, full_reorder has one ordering).
- The raising facts hold from tick 0 to the run's end (no edge inside an episode).
- Not taken: case 4's needless hold for a walk that never comes (the first proposal's form); case 5 at the human's turn
  east at the switch; E2 as a case of its own (its form is observed in cases 1 and 4's script); E1 is case 3's form.
- One expectation corrected before any run: PK4e and PK1b read "after 72", because the boundary's decision at 72 rests
  on the stand fallback on every side.
- PK3c and PK2b do not hold, from TODO-146 at a turn. Suggest: TODO-146 gets this measurement (scenario_s16_01 and
  _02: about one tick and 18 cm at the turn at shelf_4; the planned minimum 54.8 and 51.0 cm, executed 41.7 and 29.3).
- The stand fallback after a stand ends (off, 72 to 97: 25 ticks held while the human walks away). Suggest: add this
  measurement to TODO-132 (a).
- The instrument: reference.py carries a scenario's own timeline (step 4's flag); properties.CONTROLS includes the six
  scenarios; tk5.py, the set's reader; the registry's counts in tests/test_tl2_discovery.py.
