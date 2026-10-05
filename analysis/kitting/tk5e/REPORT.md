# T-K part 1, step 5e: context knowledge on kitting's rooms 02, 05, 06, 07 and on two new rooms

Written by ccode, 5 October 2026. Step 5e of T-K part 1 (named by Hadi after step 5d). The set, its rules, the windows
and the expectations: `README.md` beside this file. The tables: appendix, written by `comp5e.py`. No framework code,
strength or ruled value was changed.

**The scenarios are authored.** Each was written to place a case. Every count below compares settings on the same
scripts; none is a rate of occurrence.

## What was run

- **Rooms.** The four rooms of layouts 1 to 9 that hold a coffee machine or an A/C switch: env_layout_02, _05, _06, _07.
  Two new rooms: env_layout_19 (env_layout_08 with a coffee machine at the north wall's free middle) and env_layout_20
  (env_layout_09 with one on the free stretch of the north wall between kitting_table_0 and shelf_3). Both new rooms
  have two kitting tables and no A/C switch.
- **Scripts.** 105: 10 new per room on the four rooms, 30 per new room, plus the 5 existing measured scripts
  (scenario_s02_01, s02_02, s04_01, s03_06, and the one script of s05_01 and s05_02).
- **Settings.**
  - **off**: context knowledge off.
  - **none**: context knowledge on, no timeline fact.
  - **accord**: on, with the foreseeable task's raising fact over the ticks the human does it (break_time for the
    coffee break, room_warm for the A/C).
  - **through**: on, with break_time over a delivery the human works through.
  - **through_rw**: on, with room_warm over a delivery (deliveries-only scripts in the rooms with an A/C switch).
- **Test-beds.** Each script ran with the idle robot through the recognition test-bed, then with a working robot
  through the planning test-bed: 384 recognition runs and 388 planning runs.
- **Checks.**
  - 0 disagreements with the oracles in all 772 runs.
  - Every planning expectation matches the md5 committed before the runs.
  - Recognition: 351 expectations match. 33 changed after an instrument fix, listed next.
  - Undetermined cells (D3, close values that are not equal, skipped): rank cells in 6 runs (s27_35, s27_37, s27_39,
    s30_15, s30_17, s30_19); one gate tick each in s30_15, s30_17 and s30_19.
- **An instrument defect, fixed during the runs** (`analysis/instruments/irb/oracle.py`).
  - The oracle's `recent` column was empty on ticks with no live hypothesis, although its own memory held the
    completion. The recognizer reports the memory's state there.
  - It showed in 9 runs: scripts ending with the coffee break and no exit walk (s03_06's copies), and the last ticks of
    s22's copies.
  - Fix: the column now reads the memory on those ticks too. The 9 runs' oracle and comparison were rerun from their
    logs, no new simulation.
  - Effect: 33 expectation tables changed (the 9, and 24 runs made after the fix). The committed oracle reproduces all
    33 committed tables. The fixed one changes only `recent` on ticks with no live hypothesis.
  - No other kitting set changes: none of them has a disagreement in that column.
- **The bulk data.** The per-run outputs stay untracked on Hadi's disk, under `analysis/kitting/tk5e/{irb,mpb}/{on,off}/`:
  the logs and `.rec` files in each `runs/`, and per scenario the trajectories, the oracle and actual tables, the
  figures, diff.md, separation.md, properties.md and summary.md. They are regenerated with the commands in README.md.

## 1. Do step 5d's results hold on these rooms?

Mostly yes in recognition. In planning, context knowledge more often makes completion later in the four rooms.

**Recognition, on (no fact) against off** (step 5d's values in brackets):
- Deliveries are admitted earlier.
  - Four rooms: 81 earlier, 11 equal, 0 later (median −6 ticks).
  - New rooms: 102 / 24 / 0 (median −3).
  - Step 5d: 182 / 43 / 2 (median −8).
  - Smaller in the new rooms because off already admits sooner there: median 9 ticks after the start against 14 in
    the four rooms. The walks separate their targets quickly.
- The coffee break outside break_time is admitted later.
  - Four rooms: 15 of 25 stretches (median +10). New rooms: 29 of 40 (median +13).
  - Step 5d: 24 of 28 (median +13.5). Holds.
- The coffee break inside break_time (accord) is admitted earlier, but by less than in step 5d.
  - Four rooms: 21 earlier, 4 equal, 0 later (median −7).
  - New rooms: 24 / 15 / 0 (median −3).
  - Step 5d: 11 of 11 earlier (median −14).
  - Two causes. Off admits the coffee break early in these rooms too (median 22 to 26 ticks), leaving less to gain.
    And AM68 now delays 11 of these first admissions by 1 to 6 ticks (question 5).
- Admissions of a hypothesis that is not the true task, during modelled tasks: barely more with it on.
  - Four rooms: 7 on (156 gate ticks) against 5 off (121).
  - New rooms: 9 (163) against 8 (157).
  - Step 5d: 19 against 9.
  - By the evidence alone, every one is kind (iii) (the evidence ranks the admitted task first) or kind (i)
    (a near-tie). None is kind (ii): the prior no longer overrules the evidence. This holds as in step 5d.

**Planning, on (no fact) against off:**
- Completion.
  - Four rooms: better in 1 run, equal in 39, worse in 6 (16 ticks gained, 32 lost).
  - New rooms: better in 2, equal in 58, worse in 0 (2 ticks gained).
  - Step 5d: better in 5, equal in 16, worse in 1. **This differs.**
- Why the four rooms lose time: the earlier admission makes the robot plan against the human's projected task and
  hold for it.
  - Script 041: a 67-tick hold at the shared shelf_3, against 55 off; +12 ticks.
  - Script 038: a hold against a delivery that the human then cuts for a coffee break; +7 ticks.
  - Script 043: +7 ticks.
  - Scripts 024 and 025: +1 and +2 ticks.
  - The one gain, scenario_s05_02 (−16), comes from the wrong admission described next.
  - Class: as expected by ruling. The hold is the decided response to an admitted projection; the cost is time.
- The response decision (the first hold or switch) is earlier in 11 of 17 responding runs in the four rooms and in 4
  of 7 in the new rooms. Never later.
- In the new rooms the robot responds to the human in only 7 of 60 runs: these scripts hold few conflicts, so context
  knowledge has little to act on in planning.
- Decision records holding a hypothesis that is not the true task, before the robot's completion:
  - Four rooms: 24 records (440 ticks) on, against 20 (347) off.
  - New rooms: 29 (524) against 28 (520).

**Cases below min_separation (planning; setting none).**
- 58 cases on and 58 off; the robot is moving in 17 of each. The rest have the robot standing.
- Most are identical on both sides, or shifted by a tick. Those are not a context effect.
- The cases that change with context knowledge, each with its cause:

| script (room) | off | on | cause | class |
|---|---|---|---|---|
| 035 (07; s05_01, s05_02) | none | 30.0 cm at 27 to 31, robot moving | deliver_item(item_5) admitted at 0 while the human walks to the coffee machine, which stands 100 cm short of shelf_5 on the same bearing. The evidence is a near-tie for 24 ticks and the prior picks the assigned delivery. The robot walks down x = 0 and passes the human standing at the machine | limitation (docs/assumptions.md 6.4, its first part), with a planning consequence |
| 038 (07) | none | 19.3 cm at 52 to 56, robot moving | the delivery is admitted rightly at 36 (off: still below θ). At shelf_5 the human steps to the coffee machine on the robot's route; the record holds until the trigger rule fires | limitation (an admitted task cut by a foreseeable task inside it; question G's reading) |
| 065 (19) | 32.0 cm | 23.1 cm, the same ticks | the human arrives at kitting_table_1 beside the robot holding there. On, a recognition_changed ends the hold a tick early and the robot moves off past the human | other: the same case, deeper on |
| 024, 025 (06; s03_06) | 48.2 cm at 57 to 58 | none | the robot meets the departing human on a moving fallback; on, the earlier admissions shift the robot's timeline | a gain on |
| 043 (07) | 28.4 cm at 268 to 273, robot moving | none | the robot's earlier decisions differ on; the case does not form | a gain on |

- In step 5d the two extra cases with context knowledge on came from the turn gap (TODO-146).
- Here the extra cases come from rooms where a foreseeable task's target and an assigned task's target lie on one line
  (07: the coffee machine beside shelf_5, on the robot's route).

**By room** (recognition, setting none, all stretches): earlier / equal / later against off.

| room | earlier / equal / later | median (ticks) |
|---|---|---|
| env_layout_02 | 26 / 4 / 4 | −6 |
| env_layout_05 | 19 / 6 / 3 | −7 |
| env_layout_06 | 18 / 9 / 4 | −1 |
| env_layout_07 | 19 / 2 / 7 | −4 |
| env_layout_19 | 55 / 15 / 15 | −2 |
| env_layout_20 | 47 / 19 / 14 | −2 |

In the new rooms the larger "later" share is the coffee break outside break_time: those scripts hold more coffee
breaks.

## 2. What the timeline facts add in accord, and what they cost when the human works through them

**In accord.**
- The coffee break is admitted earlier than with no fact.
  - Four rooms: 19 of 25 stretches earlier, by a median 25 ticks (564 in all); 2 admitted only with the window.
  - New rooms: 29 of 40 earlier, median 15 ticks (639 in all).
  - Against off, see question 1.
- The A/C: with room_warm it is admitted in 8 of 10 stretches, against 3 of 10 with no fact and 6 of 10 off (question
  4). Its belief at arrival rises: in env_layout_05, 0.02 to 0.36 with room_warm, against 0.53 off.
- The deliveries outside the windows are unchanged (136 stretches equal, 1 admitted with neither).
- Planning.
  - Four rooms: completion better in 2 runs, worse in 4 (13 ticks gained, 62 lost).
  - The 62 are mostly script 038, +52 ticks: the robot recognises the human's coffee break on its route and holds 33
    and then 32 ticks instead of passing. Its minimum separation is 52.1 cm, against 45.7 cm off.
  - Class: as expected by ruling: slower, and here above min_separation where off was below.
  - New rooms: better in 2, equal in 33 (7 ticks gained).
- A second coffee break soon after the first starts suppressed by its recency fact (3 stretches in the four rooms).
  The window gives it nothing while the fact holds. In 1 of 3 (script 010) the fact ends during the walk; from then
  the window raises it, and it is admitted 34 ticks earlier than with no fact. As ruled.

**When the human works through a window** (break_time over a delivery).
- That delivery is admitted later than with no fact.
  - Four rooms: 29 of 33 stretches, median +12 ticks, at most 61.
  - New rooms: 33 of 40, median +6, at most 44.
- Against off: later by a median of 4 ticks (four rooms; 2 earlier, 5 equal, 26 later) and 3 ticks (new rooms;
  0 / 8 / 30).
  - Step 5d: median +1, at most +5.
  - In 2 stretches of env_layout_20 (scripts 076, 084) the delivery is never admitted under the window, though off
    admits it.
- The cost grows where the delivery's walk heads at the coffee machine.
  - env_layout_20: the carry from shelf_2 to kitting_table_0 runs along the north wall straight at the machine.
  - env_layout_07: shelf_5 and shelf_1 lie beside and behind the machine.
  - There the raised coffee break takes the evidence's near-tie.
  - In 07 it is also admitted wrongly during the delivery: script 036 for 17 ticks, script 041 for 40. Step 5d
    measured no wrong admission under a raising fact.
- Class: as expected by ruling (the raised strength 2 against the assigned tasks), sharpened by the limitation of
  docs/assumptions.md 6.4 where targets share a bearing.
- room_warm over a delivery costs less: against off, 9 earlier, 1 equal, 1 later (median −4); against no fact, 9 later
  (median +3, at most 31). The raised A/C strength is 0.5.
- Planning under break_time.
  - Four rooms: completion better in 1 run, worse in 7 (16 ticks gained, 36 lost); response earlier in 9, later in 2.
  - One new case below min_separation: script 015, 33.1 cm, robot moving. The window delays the delivery's admission
    (59, against 37 with no fact and 55 off), and the robot rests on a moving fallback.
  - New rooms: better in 2, equal in 53, worse in 0.

## 3. Context knowledge under unmodelled behaviour

- **A stand at a table** (20 to 60 ticks): no admission of a hypothesis that is not the true task, on or off.
- **A walk elsewhere.**
  - Near the coffee machine, context knowledge on shortens the wrong admission of the coffee break: the ordinary
    strength lowers it.
    - Script 029 (06), a walk to corner_NE 50 cm from the machine: 32 ticks on against 45 off.
    - Script 023 (05): 15 ticks off, none on.
  - Near the next delivery's shelf, it lengthens the wrong admission of that delivery: the prior lifts the fewer
    deliveries left.
    - Script 061 (19): 76 ticks on against 60 off.
    - Script 103 (20): 45 against 40.
  - Script 072 (19), a walk to the corner and then a coffee break: the coffee break is admitted on the walk, 27 ticks
    on both sides.
- **An abandoned delivery** (before or after the grasp): the abandoned delivery is not admitted after the drop, on or
  off. The exception is one tick in script 063, on both sides, where the next delivery first returns the part.
- **A never-started delivery**: never admitted while the human works (AM67: no observation warrant). It is admitted
  only on the exit walk when that walk heads toward its shelf: 4 scripts, the same on and off.
  - Class: limitation (the movement warrant's half-plane test; TODO-140's note).
- **A delivery to the other table.**
  - The carry's hypothesis key carries no table, so it counts as the true delivery.
  - In script 105 (20) the carry to the wrong table heads at the coffee machine. AM68 refuses the delivery for 9 ticks
    on, and the coffee break is admitted wrongly for 20 ticks (off: 31).
- **Planning:** no case below min_separation that context knowledge adds comes from unmodelled behaviour.

## 4. Is the A/C activation admitted more often here than in step 5d?

Yes. With no fact: 3 of 10 stretches on, 6 of 10 off. With room_warm: 8 of 10. Step 5d: 2 of 20 on (equal to off), 0
of 8 raised.

Why, room by room:
- **env_layout_07.** The switch stands by the east wall, apart from every other target, so the movement evidence alone
  separates it: off admits it in all 4 scripts. On with no fact, the ordinary strength delays it but admits it in 3 of
  4. In script 035 it comes after the last delivery: with no assigned task live, the foreseeable tasks share the whole
  prior, and it is admitted at its first tick. With room_warm it is admitted in all 4.
- **env_layout_02.** The switch stands beside the coffee machine. With room_warm it is admitted in both scripts (at its
  first tick in s02_01, where no delivery is live); with no fact in neither.
- **env_layout_05.** The A/C is done while deliveries are live and the switch lies on the line to the next shelf. With
  no fact it is never admitted on; its belief at arrival is 0.02 to 0.40, against 0.53 to 0.88 off. With room_warm it
  is admitted in 2 of 4.
- In step 5d's rooms the switch stood near other targets (env_layout_16: in a dense cluster with the coffee machine;
  _17: between two deliveries) and every A/C walk had deliveries live.
- The difference therefore lies in where the rooms place the switch and where the scripts place the A/C, not in a
  change of the A/C's own case.

## 5. What the gate rulings refuse here that they did not meet before

- **AM68 refuses the true task.** In step 5d no admission of the true task moved: every tick the rulings removed lay
  outside the true task. Here:
  - The raised coffee break (accord) is refused `none(leader_outranked)` on 1 to 6 ticks just before its first
    admission, in 11 stretches over the six rooms. The prior lifts it above θ while the evidence still ranks a
    delivery first. Its admission comes 1 to 6 ticks later.
  - Two admitted deliveries are interrupted: script 099, 1 tick; script 105, 9 ticks (the carry to the other table
    heading at the machine). Both happen in every on setting.
  - Class: as expected by ruling. AM68 asks rank only.
- **AM68 also refuses on ticks with no true hypothesis:** 8 ticks in the four rooms and 35 in the new rooms (setting
  none). Off has none, since AM68 refuses nothing when the belief is the evidence.
- **AM67 never refused the true task.** It refused the never-started deliveries throughout the scripts.
- As in step 5d, the bulk of the refusals fall on wrong leaders: 310 ticks (four rooms) and 332 (new rooms) refused
  outranked, with context knowledge on and no fact.

## The two room groups side by side (setting none, on against off)

| measure | four rooms (02, 05, 06, 07) | two new rooms (19, 20) |
|---|---|---|
| deliveries earlier / equal / later (median) | 81 / 11 / 0 (−6) | 102 / 24 / 0 (−3) |
| coffee break, ordinary, later (median) | 15 of 25 (+10) | 29 of 40 (+13) |
| coffee break, accord, earlier than off (median) | 21 of 25 (−7) | 24 of 40 (−3) |
| delivery under break_time, against off (median) | 26 of 33 later (+4) | 30 of 40 later (+3) |
| wrong admissions, modelled tasks, on / off | 7 / 5 | 9 / 8 |
| planning completion better / equal / worse | 1 / 39 / 6 | 2 / 58 / 0 |
| cases below min_separation added on, robot moving | 2 scripts (035, 038) | 1 deeper (065) |

## Findings, classified

- As expected by ruling:
  - the deliveries earlier;
  - the coffee break earlier inside break_time and later outside it;
  - the work-through cost;
  - the holds that lengthen completion in the four rooms (041, 038 accord);
  - AM68's refusals of the true task;
  - the second coffee break suppressed.
- Limitations:
  - collinear targets (035: a wrong admission at a near-tie, a pass at 30 cm);
  - an admitted task cut by a foreseeable task inside it (038, 19.3 cm);
  - the never-started delivery admitted on an exit walk toward its shelf (both sides);
  - the coffee break as the only live hypothesis on env_layout_19's exit walks (both sides; step 5b's exit-walk case);
  - the A/C's ordinary strength against live deliveries (05).
- Defects in the framework: none found.
- Defects in an instrument: one, the oracle's `recent` column on ticks with no live hypothesis (fixed, above).

## Conclusion

- On these six rooms context knowledge keeps step 5d's recognition results:
  - deliveries are admitted earlier;
  - the coffee break earlier inside break_time and later outside it;
  - wrong admissions are no more frequent than off, and none of them overrules the evidence.
- The gains are smaller where off already recognises quickly (the two new rooms).
- The costs are larger where an assigned task's target and a foreseeable task's target share a line (env_layout_07,
  env_layout_20). There:
  - a delivery worked through under break_time is admitted up to 61 ticks later than with no fact, or not at all;
  - a near-tie is resolved for the assigned delivery and the robot passes the human at 30 cm.
- In planning the earlier recognition mostly turns into earlier and longer holds. In the four rooms completion is
  later in 6 runs and earlier in 1; in the new rooms it hardly changes.
- The gate's AM68 now refuses the true task on a few ticks, delaying the raised coffee break's admission by 1 to 6
  ticks.

## Decided by ccode (confirmed by Hadi, 5 October 2026)

- The window rules: accord per instance, over the task's ticks. through with break_time over the first delivery
  performed with no event inside it, in every room. through_rw with room_warm for the deliveries-only scripts of the
  rooms with an A/C switch.
- The idle robot's place per room.
- The coffee machines' places in env_layout_19 and _20 (reasons in their notes).
- The literals written by ccode's generator, which stays outside the repository (the literals are the source).
- The classes of a wrong admission (main, unmodelled, exit, pin) and the rule "the same case on both sides" for a case
  below min_separation with the same ticks and minimum on both sides.
- The oracle's `recent` fix.

## Appendix: the tables

Written by `comp5e.py` from the step's outputs.

### 0. The runs' checks

- irb off: 0 disagreements: 105
- irb off: undetermined rank 2, gate 0: 1 (s30_15)
- irb off: undetermined rank 4, gate 0: 1 (s27_35)
- irb on: 0 disagreements: 279
- irb on: undetermined rank 2, gate 1: 3 (s30_15, s30_17, s30_19)
- irb on: undetermined rank 4, gate 0: 3 (s27_35, s27_37, s27_39)
- mpb off: 0 disagreements: 106
- mpb on: 0 disagreements: 282

### A. Recognition (279 on runs against their off run)

### A1. Admissions of the true task

**four rooms: on against off, by setting and by the state on the stretch's first tick**

| category | stretches | earlier / equal / later | admitted on only / off only / neither | difference (ticks, both admitted) | ticks earlier / later |
|---|---|---|---|---|---|
| none: delivery, no raising fact | 93 | 81 / 11 / 0 | 1 / 0 / 0 | median -6, range -45 to 0 | 967 / 0 |
| none: coffee_break, ordinary | 25 | 0 / 8 / 15 | 0 / 2 / 0 | median 10, range 0 to 21 | 0 / 195 |
| none: coffee_break, suppressed | 3 | 0 / 2 / 1 | 0 / 0 / 0 | median 0, range 0 to 10 | 0 / 10 |
| none: ac_activation, ordinary | 10 | 1 / 0 / 2 | 0 / 3 / 4 | median 12, range -14 to 15 | 14 / 27 |
| accord: delivery, no raising fact | 60 | 54 / 5 / 0 | 1 / 0 / 0 | median -7, range -44 to 0 | 606 / 0 |
| accord: coffee_break, raised | 25 | 21 / 4 / 0 | 0 / 0 / 0 | median -7, range -53 to 0 | 381 / 0 |
| accord: coffee_break, suppressed | 3 | 1 / 1 / 1 | 0 / 0 / 0 | median 0, range -34 to 10 | 34 / 10 |
| accord: ac_activation, raised | 10 | 3 / 2 / 1 | 2 / 0 / 2 | median -3, range -14 to 1 | 27 / 1 |
| through: delivery, no raising fact | 58 | 51 / 6 / 0 | 1 / 0 / 0 | median -6, range -44 to 0 | 585 / 0 |
| through: delivery, a raising fact holding | 33 | 2 / 5 / 26 | 0 / 0 / 0 | median 4, range -14 to 16 | 15 / 121 |
| through: coffee_break, ordinary | 24 | 0 / 8 / 15 | 0 / 1 / 0 | median 10, range 0 to 21 | 0 / 195 |
| through: coffee_break, suppressed | 3 | 0 / 2 / 1 | 0 / 0 / 0 | median 0, range 0 to 10 | 0 / 10 |
| through: ac_activation, ordinary | 9 | 1 / 0 / 2 | 0 / 2 / 4 | median 12, range -14 to 15 | 14 / 27 |
| through_rw: delivery, no raising fact | 13 | 10 / 3 / 0 | 0 / 0 / 0 | median -6, range -40 to 0 | 159 / 0 |
| through_rw: delivery, a raising fact holding | 11 | 9 / 1 / 1 | 0 / 0 / 0 | median -4, range -25 to 8 | 71 / 8 |
| none: all | 131 | 82 / 21 / 18 | 1 / 5 / 4 | median -4, range -45 to 21 | 981 / 232 |

**two new rooms: on against off, by setting and by the state on the stretch's first tick**

| category | stretches | earlier / equal / later | admitted on only / off only / neither | difference (ticks, both admitted) | ticks earlier / later |
|---|---|---|---|---|---|
| none: delivery, no raising fact | 131 | 102 / 24 / 0 | 3 / 0 / 2 | median -3, range -38 to 0 | 752 / 0 |
| none: coffee_break, ordinary | 40 | 0 / 10 / 29 | 0 / 0 / 1 | median 13, range 0 to 30 | 0 / 448 |
| accord: delivery, no raising fact | 77 | 64 / 9 / 0 | 3 / 0 / 1 | median -3, range -35 to 0 | 432 / 0 |
| accord: coffee_break, raised | 40 | 24 / 15 / 0 | 0 / 0 / 1 | median -3, range -21 to 0 | 191 / 0 |
| through: delivery, no raising fact | 83 | 66 / 14 / 0 | 1 / 0 / 2 | median -4, range -38 to 0 | 543 / 0 |
| through: delivery, a raising fact holding | 40 | 0 / 8 / 30 | 0 / 2 / 0 | median 3, range 0 to 30 | 0 / 197 |
| through: coffee_break, ordinary | 37 | 0 / 10 / 27 | 0 / 0 / 0 | median 13, range 0 to 30 | 0 / 419 |
| none: all | 171 | 102 / 34 / 29 | 3 / 0 / 3 | median -2, range -38 to 30 | 752 / 448 |

**The window against no fact (on with the window against on with no timeline, the same stretch)**

| category | stretches | earlier / equal / later | admitted with the window only / with no fact only / neither | difference (ticks, both admitted) | ticks earlier / later |
|---|---|---|---|---|---|
| four rooms, accord: delivery, no raising fact | 60 | 0 / 60 / 0 | 0 / 0 / 0 | median 0, range 0 to 0 | 0 / 0 |
| four rooms, accord: coffee_break, raised | 25 | 19 / 4 / 0 | 2 / 0 / 0 | median -25, range -55 to 0 | 564 / 0 |
| four rooms, accord: coffee_break, suppressed | 3 | 1 / 2 / 0 | 0 / 0 / 0 | median 0, range -34 to 0 | 34 / 0 |
| four rooms, accord: ac_activation, raised | 10 | 2 / 1 / 0 | 5 / 0 / 2 | median -14, range -19 to 0 | 33 / 0 |
| four rooms, through: delivery, no raising fact | 58 | 0 / 58 / 0 | 0 / 0 / 0 | median 0, range 0 to 0 | 0 / 0 |
| four rooms, through: delivery, a raising fact holding | 33 | 0 / 4 / 29 | 0 / 0 / 0 | median 12, range 0 to 61 | 0 / 479 |
| four rooms, through: coffee_break, ordinary | 24 | 0 / 23 / 0 | 0 / 0 / 1 | median 0, range 0 to 0 | 0 / 0 |
| four rooms, through: coffee_break, suppressed | 3 | 0 / 3 / 0 | 0 / 0 / 0 | median 0, range 0 to 0 | 0 / 0 |
| four rooms, through: ac_activation, ordinary | 9 | 0 / 3 / 0 | 0 / 0 / 6 | median 0, range 0 to 0 | 0 / 0 |
| four rooms, through_rw: delivery, no raising fact | 13 | 0 / 13 / 0 | 0 / 0 / 0 | median 0, range 0 to 0 | 0 / 0 |
| four rooms, through_rw: delivery, a raising fact holding | 11 | 0 / 2 / 9 | 0 / 0 / 0 | median 3, range 0 to 31 | 0 / 90 |
| two new rooms, accord: delivery, no raising fact | 77 | 0 / 76 / 0 | 0 / 0 / 1 | median 0, range 0 to 0 | 0 / 0 |
| two new rooms, accord: coffee_break, raised | 40 | 29 / 10 / 0 | 0 / 0 / 1 | median -15, range -43 to 0 | 639 / 0 |
| two new rooms, through: delivery, no raising fact | 83 | 0 / 81 / 0 | 0 / 0 / 2 | median 0, range 0 to 0 | 0 / 0 |
| two new rooms, through: delivery, a raising fact holding | 40 | 0 / 5 / 33 | 0 / 2 / 0 | median 6, range 0 to 44 | 0 / 349 |
| two new rooms, through: coffee_break, ordinary | 37 | 0 / 37 / 0 | 0 / 0 / 0 | median 0, range 0 to 0 | 0 / 0 |

**Per room, setting none, all stretches (on against off)**

| category | stretches | earlier / equal / later | admitted on only / off only / neither | difference (ticks, both admitted) | ticks earlier / later |
|---|---|---|---|---|---|
| env_layout_02 | 37 | 26 / 4 / 4 | 0 / 1 / 2 | median -6, range -44 to 16 | 352 / 38 |
| env_layout_05 | 33 | 19 / 6 / 3 | 0 / 3 / 2 | median -7, range -31 to 11 | 281 / 31 |
| env_layout_06 | 31 | 18 / 9 / 4 | 0 / 0 / 0 | median -1, range -19 to 21 | 104 / 71 |
| env_layout_07 | 30 | 19 / 2 / 7 | 1 / 1 / 0 | median -4, range -45 to 20 | 244 / 92 |
| env_layout_19 | 87 | 55 / 15 / 15 | 0 / 0 / 2 | median -2, range -35 to 24 | 397 / 202 |
| env_layout_20 | 84 | 47 / 19 / 14 | 3 / 0 / 1 | median -2, range -38 to 30 | 355 / 246 |

### A2. The A/C activation, every stretch

| room | script | setting | stretch | admitted on / off | belief at arrival on / off |
|---|---|---|---|---|---|
| 02 | 001 | none | 311 to 363 | never / never | 0.6744 at 361 / 0.6744 at 361 |
| 02 | 001 | accord | 311 to 363 | 311 (0) / never | 0.9811 at 361 / 0.6744 at 361 |
| 02 | 001 | through | 311 to 363 | never / never | 0.6744 at 361 / 0.6744 at 361 |
| 02 | 005 | none | 74 to 125 | never / never | 0.6758 at 123 / 0.6758 at 123 |
| 02 | 005 | accord | 74 to 125 | 82 (8) / never | 0.9812 at 123 / 0.6758 at 123 |
| 02 | 005 | through | 74 to 125 | never / never | 0.6758 at 123 / 0.6758 at 123 |
| 05 | 013 | none | 185 to 206 | never / never | 0.0218 at 204 / 0.5259 at 204 |
| 05 | 013 | accord | 185 to 206 | never / never | 0.3573 at 204 / 0.5259 at 204 |
| 05 | 013 | through | 185 to 206 | never / never | 0.0218 at 204 / 0.5259 at 204 |
| 05 | 015 | none | 0 to 32 | never / 26 (26) | 0.4020 at 30 / 0.8586 at 30 |
| 05 | 015 | accord | 0 to 32 | 20 (20) / 26 (26) | 0.9439 at 30 / 0.8586 at 30 |
| 05 | 015 | through | 0 to 32 | never / 26 (26) | 0.4020 at 30 / 0.8586 at 30 |
| 05 | 017 | none | 55 to 85 | never / 82 (27) | 0.2573 at 83 / 0.8836 at 83 |
| 05 | 017 | accord | 55 to 85 | 82 (27) / 82 (27) | 0.8965 at 83 / 0.8836 at 83 |
| 05 | 017 | through | 55 to 85 | never / 82 (27) | 0.2573 at 83 / 0.8836 at 83 |
| 05 | 021 | none | 198 to 219 | never / never | 0.0217 at 217 / 0.5259 at 217 |
| 05 | 021 | accord | 198 to 219 | never / never | 0.3572 at 217 / 0.5259 at 217 |
| 05 | 021 | through | 198 to 219 | never / never | 0.0217 at 217 / 0.5259 at 217 |
| 07 | 035 | none | 96 to 142 | 96 (0) / 110 (14) | 1.0000 at 140 / 0.9999 at 140 |
| 07 | 035 | accord | 96 to 142 | 96 (0) / 110 (14) | 1.0000 at 140 / 0.9999 at 140 |
| 07 | 035 | through | 96 to 142 | 96 (0) / 110 (14) | 1.0000 at 140 / 0.9999 at 140 |
| 07 | 037 | none | 0 to 48 | 35 (35) / 23 (23) | 0.9810 at 46 / 0.9979 at 46 |
| 07 | 037 | accord | 0 to 48 | 16 (16) / 23 (23) | 0.9992 at 46 / 0.9979 at 46 |
| 07 | 037 | through | 0 to 48 | 35 (35) / 23 (23) | 0.9810 at 46 / 0.9979 at 46 |
| 07 | 039 | none | 54 to 137 | never / 134 (80) | 0.1495 at 135 / 0.8147 at 135 |
| 07 | 039 | accord | 54 to 137 | 134 (80) / 134 (80) | 0.8147 at 135 / 0.8147 at 135 |
| 07 | 045 | none | 125 to 161 | 149 (24) / 134 (9) | 0.9829 at 159 / 0.9996 at 159 |
| 07 | 045 | accord | 125 to 161 | 135 (10) / 134 (9) | 0.9993 at 159 / 0.9996 at 159 |
| 07 | 045 | through | 125 to 161 | 149 (24) / 134 (9) | 0.9829 at 159 / 0.9996 at 159 |

### A3. Admissions of a hypothesis that is not the true task

| group | side | kind | count | gate ticks | trigger-rule ticks | of them a never-started delivery (count) |
|---|---|---|---|---|---|---|
| four rooms | off | main | 5 | 121 | 131 | 0 |
| four rooms | off | unmodelled | 2 | 60 | 69 | 0 |
| four rooms | off | exit | 17 | 311 | 332 | 2 |
| four rooms | none | main | 7 | 156 | 188 | 0 |
| four rooms | none | unmodelled | 1 | 32 | 41 | 0 |
| four rooms | none | exit | 19 | 319 | 378 | 2 |
| four rooms | accord | main | 4 | 95 | 105 | 0 |
| four rooms | accord | exit | 13 | 193 | 246 | 2 |
| four rooms | through | main | 7 | 138 | 183 | 0 |
| four rooms | through | unmodelled | 1 | 32 | 41 | 0 |
| four rooms | through | exit | 18 | 315 | 374 | 2 |
| four rooms | through_rw | exit | 6 | 126 | 132 | 0 |
| two new rooms | off | main | 8 | 157 | 170 | 0 |
| two new rooms | off | unmodelled | 3 | 127 | 127 | 0 |
| two new rooms | off | exit | 25 | 617 | 644 | 2 |
| two new rooms | none | main | 9 | 163 | 176 | 0 |
| two new rooms | none | unmodelled | 3 | 148 | 148 | 0 |
| two new rooms | none | exit | 24 | 593 | 620 | 2 |
| two new rooms | accord | main | 6 | 133 | 142 | 0 |
| two new rooms | accord | unmodelled | 1 | 27 | 27 | 0 |
| two new rooms | accord | exit | 12 | 328 | 346 | 2 |
| two new rooms | through | main | 6 | 106 | 107 | 0 |
| two new rooms | through | unmodelled | 3 | 148 | 148 | 0 |
| two new rooms | through | exit | 21 | 546 | 564 | 1 |

### A3, the kinds from the evidence alone (main, on)

| group | setting | (i) near-tie | (ii) the prior overruling | (iii) the evidence ranking it first | no true hypothesis |
|---|---|---|---|---|---|
| four rooms | none | 1 (24 ticks) | 0 (0 ticks) | 6 (132 ticks) | 0 (0 ticks) |
| four rooms | accord | 0 (0 ticks) | 0 (0 ticks) | 4 (95 ticks) | 0 (0 ticks) |
| four rooms | through | 3 (81 ticks) | 0 (0 ticks) | 4 (57 ticks) | 0 (0 ticks) |
| two new rooms | none | 0 (0 ticks) | 0 (0 ticks) | 9 (163 ticks) | 0 (0 ticks) |
| two new rooms | accord | 0 (0 ticks) | 0 (0 ticks) | 6 (133 ticks) | 0 (0 ticks) |
| two new rooms | through | 0 (0 ticks) | 0 (0 ticks) | 6 (106 ticks) | 0 (0 ticks) |

### A3, every main and unmodelled row

| group | side | room | script | setting | admitted | ticks (gate) | trigger rule | true task / human's top task | never-started |
|---|---|---|---|---|---|---|---|---|---|
| four rooms | accord | 02 | 002 | main | item_2 | 33-38 (6) | 10 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | accord | 02 | 006 | main | item_1 | 38-51 (14) | 20 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | accord | 05 | 018 | main | item_3 | 34-66 (33) | 33 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | accord | 07 | 039 | main | item_3 | 54-95 (42) | 42 | ac_activation(ac_switch_0) / ac_activation |  |
| four rooms | none | 02 | 002 | main | item_2 | 33-43 (11) | 11 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | none | 02 | 006 | main | item_1 | 38-61 (24) | 24 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | none | 05 | 018 | main | item_3 | 34-66 (33) | 33 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | none | 06 | 027 | main | item_2 | 14-34 (21) | 22 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | none | 07 | 035 | main | item_5 | 0-23 (24) | 40 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | none | 07 | 038 | main | item_5 | 48-48 (1) | 16 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | none | 07 | 039 | main | item_3 | 54-95 (42) | 42 | ac_activation(ac_switch_0) / ac_activation |  |
| four rooms | none | 06 | 029 | unmodelled | coffee_break | 65-96 (32) | 41 | unmodelled, deliver_item(item_3) / go_to_and_stand |  |
| four rooms | off | 02 | 002 | main | item_2 | 33-42 (10) | 11 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | off | 02 | 006 | main | item_1 | 38-57 (20) | 24 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | off | 05 | 018 | main | item_3 | 34-66 (33) | 33 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | off | 06 | 027 | main | item_2 | 14-29 (16) | 21 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | off | 07 | 039 | main | item_3 | 54-95 (42) | 42 | ac_activation(ac_switch_0) / ac_activation |  |
| four rooms | off | 05 | 023 | unmodelled | coffee_break | 113-127 (15) | 15 | unmodelled / go_to_and_stand |  |
| four rooms | off | 06 | 029 | unmodelled | coffee_break | 52-96 (45) | 54 | unmodelled, deliver_item(item_3) / go_to_and_stand |  |
| four rooms | through | 02 | 002 | main | item_2 | 33-43 (11) | 11 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | through | 02 | 006 | main | item_1 | 38-61 (24) | 24 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | through | 06 | 027 | main | item_2 | 14-34 (21) | 22 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | through | 07 | 035 | main | item_5 | 0-23 (24) | 40 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | through | 07 | 036 | main | coffee_break | 10-26 (17) | 25 | deliver_item(item_5) / deliver_item |  |
| four rooms | through | 07 | 038 | main | item_5 | 48-48 (1) | 16 | coffee_break(coffee_machine_0) / coffee_break |  |
| four rooms | through | 07 | 041 | main | coffee_break | 4-43 (40) | 45 | deliver_item(item_51) / deliver_item |  |
| four rooms | through | 06 | 029 | unmodelled | coffee_break | 65-96 (32) | 41 | unmodelled, deliver_item(item_3) / go_to_and_stand |  |
| two new rooms | accord | 19 | 050 | main | item_3 | 32-48 (17) | 17 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | accord | 20 | 080 | main | item_3 | 25-40 (16) | 16 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | accord | 20 | 081 | main | item_1 | 93-93 (1) | 10 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | accord | 20 | 095 | main | item_63 | 97-139 (43) | 43 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | accord | 20 | 100 | main | item_76 | 25-60 (36) | 36 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | accord | 20 | 105 | main | coffee_break | 40-59 (20) | 20 | deliver_item(item_75) / deliver_item |  |
| two new rooms | accord | 19 | 072 | unmodelled | coffee_break | 45-71 (27) | 27 | unmodelled / go_to |  |
| two new rooms | none | 19 | 050 | main | item_3 | 32-48 (17) | 17 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | none | 19 | 063 | main | item_23 | 30-30 (1) | 1 | deliver_item(item_26) / deliver_item |  |
| two new rooms | none | 19 | 075 | main | item_35 | 10-25 (16) | 17 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | none | 20 | 080 | main | item_3 | 25-40 (16) | 16 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | none | 20 | 081 | main | item_1 | 93-93 (1) | 10 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | none | 20 | 095 | main | item_63 | 97-139 (43) | 43 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | none | 20 | 100 | main | item_76 | 25-60 (36) | 36 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | none | 20 | 104 | main | item_78 | 9-21 (13) | 16 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | none | 20 | 105 | main | coffee_break | 40-59 (20) | 20 | deliver_item(item_75) / deliver_item |  |
| two new rooms | none | 19 | 061 | unmodelled | item_25 | 71-146 (76) | 76 | unmodelled / go_to_and_stand |  |
| two new rooms | none | 19 | 072 | unmodelled | coffee_break | 45-71 (27) | 27 | unmodelled / go_to |  |
| two new rooms | none | 20 | 103 | unmodelled | item_76 | 66-110 (45) | 45 | unmodelled / go_to_and_stand |  |
| two new rooms | off | 19 | 050 | main | item_3 | 32-48 (17) | 17 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | off | 19 | 063 | main | item_23 | 30-30 (1) | 1 | deliver_item(item_26) / deliver_item |  |
| two new rooms | off | 19 | 075 | main | item_35 | 10-21 (12) | 16 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | off | 20 | 080 | main | item_3 | 25-40 (16) | 16 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | off | 20 | 081 | main | item_1 | 93-93 (1) | 10 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | off | 20 | 095 | main | item_63 | 97-139 (43) | 43 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | off | 20 | 100 | main | item_76 | 25-60 (36) | 36 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | off | 20 | 105 | main | coffee_break | 29-59 (31) | 31 | deliver_item(item_75) / deliver_item |  |
| two new rooms | off | 19 | 061 | unmodelled | item_25 | 87-146 (60) | 60 | unmodelled / go_to_and_stand |  |
| two new rooms | off | 19 | 072 | unmodelled | coffee_break | 45-71 (27) | 27 | unmodelled / go_to |  |
| two new rooms | off | 20 | 103 | unmodelled | item_76 | 71-110 (40) | 40 | unmodelled / go_to_and_stand |  |
| two new rooms | through | 19 | 050 | main | item_3 | 32-48 (17) | 17 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | through | 19 | 063 | main | item_23 | 30-30 (1) | 1 | deliver_item(item_26) / deliver_item |  |
| two new rooms | through | 19 | 075 | main | item_35 | 10-25 (16) | 17 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | through | 20 | 080 | main | item_3 | 25-40 (16) | 16 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | through | 20 | 100 | main | item_76 | 25-60 (36) | 36 | coffee_break(coffee_machine_0) / coffee_break |  |
| two new rooms | through | 20 | 105 | main | coffee_break | 40-59 (20) | 20 | deliver_item(item_75) / deliver_item |  |
| two new rooms | through | 19 | 061 | unmodelled | item_25 | 71-146 (76) | 76 | unmodelled / go_to_and_stand |  |
| two new rooms | through | 19 | 072 | unmodelled | coffee_break | 45-71 (27) | 27 | unmodelled / go_to |  |
| two new rooms | through | 20 | 103 | unmodelled | item_76 | 66-110 (45) | 45 | unmodelled / go_to_and_stand |  |

### A4. The gate's outcome with a leader at or above θ (ticks)

| group | side | leader (≥ θ) | none(leader_inadequate) | none(leader_no_observation) | none(leader_outranked) | none(leader_unwarranted) |
|---|---|---|---|---|---|---|
| four rooms | off | true task | 133 | 0 | 0 | 0 |
| four rooms | off | another task | 87 | 21 | 0 | 41 |
| four rooms | off | unmodelled tick | 1909 | 3 | 0 | 125 |
| four rooms | none | true task | 302 | 0 | 0 | 0 |
| four rooms | none | another task | 191 | 85 | 310 | 174 |
| four rooms | none | unmodelled tick | 2388 | 3 | 8 | 322 |
| four rooms | accord | true task | 94 | 0 | 14 | 0 |
| four rooms | accord | another task | 56 | 64 | 19 | 86 |
| four rooms | accord | unmodelled tick | 1514 | 3 | 8 | 202 |
| four rooms | through | true task | 302 | 0 | 0 | 0 |
| four rooms | through | another task | 117 | 63 | 414 | 152 |
| four rooms | through | unmodelled tick | 2373 | 3 | 8 | 322 |
| four rooms | through_rw | true task | 213 | 0 | 0 | 0 |
| four rooms | through_rw | another task | 0 | 3 | 0 | 3 |
| four rooms | through_rw | unmodelled tick | 638 | 0 | 0 | 75 |
| two new rooms | off | true task | 305 | 0 | 0 | 0 |
| two new rooms | off | another task | 263 | 69 | 0 | 118 |
| two new rooms | off | unmodelled tick | 3689 | 11 | 0 | 297 |
| two new rooms | none | true task | 264 | 0 | 10 | 0 |
| two new rooms | none | another task | 442 | 122 | 332 | 216 |
| two new rooms | none | unmodelled tick | 3841 | 12 | 35 | 425 |
| two new rooms | accord | true task | 267 | 0 | 15 | 0 |
| two new rooms | accord | another task | 164 | 80 | 0 | 127 |
| two new rooms | accord | unmodelled tick | 2243 | 11 | 35 | 246 |
| two new rooms | through | true task | 217 | 0 | 10 | 0 |
| two new rooms | through | another task | 377 | 89 | 370 | 176 |
| two new rooms | through | unmodelled tick | 3666 | 10 | 35 | 398 |

### A4, the true task refused by AM67 or AM68 (on)

| group | room | script | setting | true task | ticks | refusal | off: the gate on those ticks |
|---|---|---|---|---|---|---|---|
| four rooms | 02 | 002 | accord | coffee_break | 48-49 | none(leader_outranked) | none(below_theta) |
| four rooms | 02 | 006 | accord | coffee_break | 64-64 | none(leader_outranked) | none(below_theta) |
| four rooms | 02 | 011 | accord | coffee_break | 53-58 | none(leader_outranked) | none(below_theta) |
| four rooms | 05 | 018 | accord | coffee_break | 89-90 | none(leader_outranked) | none(below_theta) |
| four rooms | 06 | 027 | accord | coffee_break | 34-34 | none(leader_outranked) | none(below_theta) |
| four rooms | 07 | 038 | accord | coffee_break | 51-52 | none(leader_outranked) | none(below_theta) |
| two new rooms | 19 | 059 | accord | coffee_break | 134-134 | none(leader_outranked) | none(below_theta) |
| two new rooms | 19 | 075 | accord | coffee_break | 25-25 | none(leader_outranked) | none(below_theta) |
| two new rooms | 20 | 080 | accord | coffee_break | 51-51 | none(leader_outranked) | none(below_theta) |
| two new rooms | 20 | 099 | none | item_75 | 120-120 | none(leader_outranked) | none(below_theta) |
| two new rooms | 20 | 099 | accord | item_75 | 120-120 | none(leader_outranked) | none(below_theta) |
| two new rooms | 20 | 099 | through | item_75 | 120-120 | none(leader_outranked) | none(below_theta) |
| two new rooms | 20 | 100 | accord | coffee_break | 84-84 | none(leader_outranked) | none(below_theta) |
| two new rooms | 20 | 104 | accord | coffee_break | 21-21 | none(leader_outranked) | none(below_theta) |
| two new rooms | 20 | 105 | none | item_75 | 22-30 | none(leader_outranked) | clears, none(below_theta) |
| two new rooms | 20 | 105 | accord | item_75 | 22-30 | none(leader_outranked) | clears, none(below_theta) |
| two new rooms | 20 | 105 | through | item_75 | 22-30 | none(leader_outranked) | clears, none(below_theta) |

### B. Planning (282 on runs against their off run)

| room | script | setting | scenario | completion off → on (Δ) | response decision off → on | wrong records off → on (count; ticks) | min separation off → on | cases below on (first-last: min) |
|---|---|---|---|---|---|---|---|---|
| 02 | 001 | accord | s17_03 | 422 → 422 (+0) | None: none → None: none | 0; 0 → 0; 0 | 30.9 → 30.9 | 72-78: 30.9 |
| 02 | 001 | through | s17_05 | 422 → 422 (+0) | None: none → None: none | 0; 0 → 0; 0 | 30.9 → 30.9 | 72-78: 30.9 |
| 02 | 001 | none | s02_01 | 422 → 422 (+0) | None: none → None: none | 0; 0 → 0; 0 | 30.9 → 30.9 | 72-78: 30.9 |
| 02 | 002 | accord | s17_08 | 167 → 167 (+0) | 270: hold 14 → 270: hold 14 | 1; 11 → 1; 10 | 60.3 → 60.3 | none |
| 02 | 002 | through | s17_10 | 167 → 167 (+0) | 270: hold 14 → 270: hold 14 | 1; 11 → 1; 11 | 60.3 → 60.3 | none |
| 02 | 002 | none | s02_02 | 167 → 167 (+0) | 270: hold 14 → 270: hold 14 | 1; 11 → 1; 11 | 60.3 → 60.3 | none |
| 02 | 003 | none | s17_12 | 279 → 279 (+0) | None: none → None: none | 0; 0 → 0; 0 | 40.6 → 40.6 | 291-295: 40.6 |
| 02 | 003 | through | s17_14 | 279 → 279 (+0) | None: none → None: none | 0; 0 → 0; 0 | 40.6 → 40.6 | 291-295: 40.6 |
| 02 | 003 | through_rw | s17_16 | 279 → 279 (+0) | None: none → None: none | 0; 0 → 0; 0 | 40.6 → 40.6 | 291-295: 40.6 |
| 02 | 004 | none | s17_18 | 305 → 305 (+0) | None: none → None: none | 0; 0 → 0; 0 | 86.7 → 86.7 | none |
| 02 | 004 | accord | s17_20 | 305 → 305 (+0) | None: none → None: none | 0; 0 → 0; 0 | 86.7 → 86.7 | none |
| 02 | 004 | through | s17_22 | 305 → 305 (+0) | None: none → None: none | 0; 0 → 0; 0 | 86.7 → 86.7 | none |
| 02 | 005 | none | s17_24 | 299 → 299 (+0) | 153: hold 4 → 153: hold 4 | 0; 0 → 0; 0 | 9.7 → 9.7 | 286-290: 9.7 |
| 02 | 005 | accord | s17_26 | 299 → 299 (+0) | 153: hold 4 → 153: hold 4 | 0; 0 → 0; 0 | 9.7 → 9.7 | 286-290: 9.7 |
| 02 | 005 | through | s17_28 | 299 → 299 (+0) | 153: hold 4 → 153: hold 4 | 0; 0 → 0; 0 | 9.7 → 9.7 | 286-290: 9.7 |
| 02 | 006 | none | s17_30 | 326 → 326 (+0) | None: none → None: none | 1; 24 → 1; 24 | 66.5 → 66.5 | none |
| 02 | 006 | accord | s17_32 | 326 → 326 (+0) | None: none → None: none | 1; 24 → 1; 20 | 66.5 → 66.5 | none |
| 02 | 006 | through | s17_34 | 326 → 326 (+0) | None: none → None: none | 1; 24 → 1; 24 | 66.5 → 66.5 | none |
| 02 | 007 | none | s17_36 | 332 → 332 (+0) | None: none → None: none | 0; 0 → 0; 0 | 124.6 → 124.6 | none |
| 02 | 007 | through | s17_38 | 332 → 332 (+0) | None: none → None: none | 0; 0 → 0; 0 | 124.6 → 124.6 | none |
| 02 | 007 | through_rw | s17_40 | 332 → 332 (+0) | None: none → None: none | 0; 0 → 0; 0 | 124.6 → 124.6 | none |
| 02 | 008 | none | s18_02 | 340 → 340 (+0) | None: none → None: none | 0; 0 → 0; 0 | 23.6 → 23.6 | 197-202: 23.6 |
| 02 | 008 | through | s18_04 | 340 → 340 (+0) | None: none → None: none | 0; 0 → 0; 0 | 23.6 → 23.6 | 197-202: 23.6 |
| 02 | 008 | through_rw | s18_06 | 340 → 340 (+0) | None: none → None: none | 0; 0 → 0; 0 | 23.6 → 23.6 | 197-202: 23.6 |
| 02 | 009 | none | s18_08 | 331 → 331 (+0) | None: none → None: none | 0; 0 → 0; 0 | 234.6 → 234.6 | none |
| 02 | 009 | accord | s18_10 | 331 → 331 (+0) | None: none → None: none | 0; 0 → 0; 0 | 234.6 → 234.6 | none |
| 02 | 009 | through | s18_12 | 331 → 331 (+0) | None: none → None: none | 0; 0 → 0; 0 | 234.6 → 234.6 | none |
| 02 | 010 | none | s18_14 | 310 → 310 (+0) | None: none → None: none | 0; 0 → 0; 0 | 317.4 → 317.4 | none |
| 02 | 010 | accord | s18_16 | 310 → 310 (+0) | None: none → None: none | 0; 0 → 0; 0 | 317.4 → 317.4 | none |
| 02 | 010 | through | s18_18 | 310 → 310 (+0) | None: none → None: none | 0; 0 → 0; 0 | 317.4 → 317.4 | none |
| 02 | 011 | none | s18_20 | 337 → 337 (+0) | None: none → None: none | 1; 6 → 1; 10 | 144.2 → 144.2 | none |
| 02 | 011 | accord | s18_22 | 337 → 337 (+0) | None: none → None: none | 1; 6 → 1; 6 | 144.2 → 144.2 | none |
| 02 | 011 | through | s18_24 | 337 → 337 (+0) | None: none → None: none | 1; 6 → 1; 10 | 144.2 → 144.2 | none |
| 02 | 012 | none | s18_26 | 369 → 369 (+0) | 335: hold 7 → 335: hold 7 | 0; 0 → 0; 0 | 50.6 → 50.6 | none |
| 02 | 012 | through | s18_28 | 369 → 369 (+0) | 335: hold 7 → 335: hold 7 | 0; 0 → 0; 0 | 50.6 → 50.6 | none |
| 02 | 012 | through_rw | s18_30 | 369 → 369 (+0) | 335: hold 7 → 335: hold 7 | 0; 0 → 0; 0 | 50.6 → 50.6 | none |
| 05 | 013 | accord | s19_03 | 379 → 379 (+0) | None: none → None: none | 1; 25 → 1; 16 | 59.9 → 59.9 | none |
| 05 | 013 | through | s19_05 | 379 → 379 (+0) | None: none → None: none | 1; 25 → 1; 16 | 59.9 → 59.9 | none |
| 05 | 013 | none | s04_01 | 379 → 379 (+0) | None: none → None: none | 1; 25 → 1; 16 | 59.9 → 59.9 | none |
| 05 | 014 | none | s19_07 | 379 → 379 (+0) | None: none → None: none | 0; 0 → 0; 0 | 73.3 → 73.3 | none |
| 05 | 014 | through | s19_09 | 379 → 379 (+0) | None: none → None: none | 0; 0 → 0; 0 | 73.3 → 73.3 | none |
| 05 | 014 | through_rw | s19_11 | 379 → 379 (+0) | None: none → None: none | 0; 0 → 0; 0 | 73.3 → 73.3 | none |
| 05 | 015 | none | s19_13 | 405 → 405 (+0) | 43: hold 6 → 37: hold 6 | 0; 0 → 1; 14 | 2.2 → 2.2 | 153-154: 34.9; 270-275: 2.2 |
| 05 | 015 | accord | s19_15 | 405 → 405 (+0) | 43: hold 6 → 37: hold 6 | 0; 0 → 1; 14 | 2.2 → 2.2 | 153-154: 34.9; 270-275: 2.2 |
| 05 | 015 | through | s19_17 | 405 → 405 (+0) | 43: hold 6 → 41: hold 2 | 0; 0 → 1; 14 | 2.2 → 2.2 | 51-52: 33.1; 270-275: 2.2 |
| 05 | 016 | none | s19_19 | 282 → 282 (+0) | None: none → None: none | 0; 0 → 0; 0 | 28.8 → 28.8 | 291-298: 28.8 |
| 05 | 016 | accord | s19_21 | 282 → 282 (+0) | None: none → None: none | 0; 0 → 0; 0 | 28.8 → 28.8 | 291-298: 28.8 |
| 05 | 016 | through | s19_23 | 282 → 282 (+0) | None: none → None: none | 0; 0 → 0; 0 | 28.8 → 28.8 | 291-298: 28.8 |
| 05 | 017 | none | s19_25 | 379 → 379 (+0) | None: none → None: none | 1; 9 → 1; 9 | 142.8 → 142.8 | none |
| 05 | 017 | accord | s19_27 | 379 → 379 (+0) | None: none → None: none | 1; 9 → 1; 9 | 142.8 → 142.8 | none |
| 05 | 017 | through | s19_29 | 379 → 379 (+0) | None: none → None: none | 1; 9 → 1; 9 | 142.8 → 142.8 | none |
| 05 | 018 | none | s19_31 | 282 → 282 (+0) | None: none → None: none | 3; 50 → 3; 37 | 164.5 → 164.5 | none |
| 05 | 018 | accord | s19_33 | 282 → 282 (+0) | None: none → None: none | 3; 50 → 3; 37 | 164.5 → 164.5 | none |
| 05 | 019 | none | s20_02 | 254 → 254 (+0) | 245: hold 1 → 244: hold 1 | 0; 0 → 0; 0 | 12.4 → 12.4 | 356-364: 12.4 |
| 05 | 019 | through | s20_04 | 254 → 254 (+0) | 245: hold 1 → 244: hold 1 | 0; 0 → 0; 0 | 12.4 → 12.4 | 356-364: 12.4 |
| 05 | 019 | through_rw | s20_06 | 254 → 254 (+0) | 245: hold 1 → 244: hold 1 | 0; 0 → 0; 0 | 12.4 → 12.4 | 356-364: 12.4 |
| 05 | 020 | none | s20_08 | 275 → 275 (+0) | 96: switch → 96: switch | 0; 0 → 0; 0 | 62.0 → 62.0 | none |
| 05 | 020 | accord | s20_10 | 275 → 275 (+0) | 96: switch → 96: switch | 0; 0 → 0; 0 | 62.0 → 62.0 | none |
| 05 | 020 | through | s20_12 | 275 → 275 (+0) | 96: switch → 96: switch | 0; 0 → 0; 0 | 62.0 → 62.0 | none |
| 05 | 021 | none | s20_14 | 276 → 276 (+0) | None: none → None: none | 0; 0 → 0; 0 | 12.4 → 12.4 | 307-314: 12.4 |
| 05 | 021 | accord | s20_16 | 276 → 276 (+0) | None: none → None: none | 0; 0 → 0; 0 | 12.4 → 12.4 | 307-314: 12.4 |
| 05 | 021 | through | s20_18 | 276 → 276 (+0) | None: none → None: none | 0; 0 → 0; 0 | 12.4 → 12.4 | 307-314: 12.4 |
| 05 | 022 | none | s20_20 | 271 → 271 (+0) | None: none → None: none | 0; 0 → 0; 0 | 122.1 → 122.1 | none |
| 05 | 022 | through | s20_22 | 271 → 271 (+0) | None: none → None: none | 0; 0 → 0; 0 | 122.1 → 122.1 | none |
| 05 | 022 | through_rw | s20_24 | 271 → 271 (+0) | None: none → None: none | 0; 0 → 0; 0 | 122.1 → 122.1 | none |
| 05 | 023 | none | s20_26 | 292 → 292 (+0) | 88: hold 10 → 88: hold 10 | 1; 15 → 0; 0 | 9.0 → 9.0 | 94-100: 29.7; 374-382: 9.0 |
| 05 | 023 | accord | s20_28 | 292 → 292 (+0) | 88: hold 10 → 88: hold 10 | 1; 15 → 0; 0 | 9.0 → 9.0 | 94-100: 29.7; 374-382: 9.0 |
| 05 | 023 | through | s20_30 | 292 → 292 (+0) | 88: hold 10 → 88: hold 10 | 1; 15 → 0; 0 | 9.0 → 9.0 | 94-100: 29.7; 374-382: 9.0 |
| 06 | 024 | accord | s21_03 | 237 → 238 (+1) | 6: hold 7 → 5: hold 7 | 0; 0 → 0; 0 | 48.2 → 60.1 | none |
| 06 | 024 | through | s21_05 | 237 → 238 (+1) | 6: hold 7 → 8: hold 7 | 0; 0 → 0; 0 | 48.2 → 60.1 | none |
| 06 | 024 | none | s03_06 | 237 → 238 (+1) | 6: hold 7 → 5: hold 7 | 0; 0 → 0; 0 | 48.2 → 60.1 | none |
| 06 | 025 | none | s21_07 | 240 → 242 (+2) | 6: hold 7 → 5: hold 7 | 0; 0 → 0; 0 | 33.9 → 34.4 | 134-137: 34.4 |
| 06 | 025 | through | s21_09 | 240 → 242 (+2) | 6: hold 7 → 8: hold 7 | 0; 0 → 0; 0 | 33.9 → 34.4 | 134-137: 34.4 |
| 06 | 026 | none | s21_11 | 229 → 229 (+0) | None: none → None: none | 0; 0 → 0; 0 | 73.2 → 73.2 | none |
| 06 | 026 | accord | s21_13 | 229 → 229 (+0) | None: none → None: none | 0; 0 → 0; 0 | 73.2 → 73.2 | none |
| 06 | 026 | through | s21_15 | 229 → 229 (+0) | None: none → None: none | 0; 0 → 0; 0 | 73.2 → 73.2 | none |
| 06 | 027 | none | s21_17 | 229 → 229 (+0) | None: none → None: none | 1; 21 → 1; 22 | 145.6 → 145.6 | none |
| 06 | 027 | accord | s21_19 | 229 → 229 (+0) | None: none → None: none | 1; 21 → 1; 14 | 145.6 → 145.6 | none |
| 06 | 027 | through | s21_21 | 229 → 229 (+0) | None: none → None: none | 1; 21 → 1; 22 | 145.6 → 145.6 | none |
| 06 | 028 | none | s21_23 | 201 → 201 (+0) | None: none → None: none | 1; 18 → 2; 23 | 11.4 → 11.4 | 54-59: 11.4 |
| 06 | 028 | accord | s21_25 | 201 → 201 (+0) | None: none → None: none | 1; 18 → 2; 23 | 11.4 → 11.4 | 54-59: 11.4 |
| 06 | 028 | through | s21_27 | 201 → 201 (+0) | None: none → None: none | 1; 18 → 2; 23 | 11.4 → 11.4 | 54-59: 11.4 |
| 06 | 029 | none | s21_29 | 229 → 229 (+0) | None: none → None: none | 2; 54 → 1; 41 | 98.1 → 98.1 | none |
| 06 | 029 | through | s21_31 | 229 → 229 (+0) | None: none → None: none | 2; 54 → 1; 41 | 98.1 → 98.1 | none |
| 06 | 030 | none | s22_02 | 118 → 118 (+0) | None: none → None: none | 0; 0 → 0; 0 | 12.1 → 12.1 | 150-157: 12.1; 235-241: 14.9 |
| 06 | 030 | through | s22_04 | 118 → 118 (+0) | None: none → None: none | 0; 0 → 0; 0 | 12.1 → 12.1 | 150-157: 12.1; 235-241: 14.9 |
| 06 | 031 | none | s22_06 | 118 → 118 (+0) | None: none → None: none | 0; 0 → 0; 0 | 12.0 → 12.0 | 207-213: 20.3; 288-293: 12.0 |
| 06 | 031 | accord | s22_08 | 118 → 118 (+0) | None: none → None: none | 0; 0 → 0; 0 | 12.0 → 12.0 | 207-213: 20.3; 288-293: 12.0 |
| 06 | 031 | through | s22_10 | 118 → 118 (+0) | None: none → None: none | 0; 0 → 0; 0 | 12.0 → 12.0 | 207-213: 20.3; 288-293: 12.0 |
| 06 | 032 | none | s22_12 | 134 → 134 (+0) | 10: hold 3 → 8: hold 3 | 1; 9 → 1; 9 | 9.8 → 9.8 | 168-176: 9.8 |
| 06 | 032 | accord | s22_14 | 134 → 134 (+0) | 10: hold 3 → 8: hold 3 | 1; 9 → 1; 9 | 9.8 → 9.8 | 168-176: 9.8 |
| 06 | 032 | through | s22_16 | 134 → 134 (+0) | 10: hold 3 → 8: hold 3 | 1; 9 → 1; 9 | 9.8 → 9.8 | 168-176: 9.8 |
| 06 | 033 | none | s22_18 | 118 → 118 (+0) | None: none → None: none | 0; 0 → 0; 0 | 6.3 → 6.3 | 145-174: 6.3; 250-254: 12.2 |
| 06 | 033 | accord | s22_20 | 118 → 118 (+0) | None: none → None: none | 0; 0 → 0; 0 | 6.3 → 6.3 | 145-174: 6.3; 250-254: 12.2 |
| 06 | 033 | through | s22_22 | 118 → 118 (+0) | None: none → None: none | 0; 0 → 0; 0 | 6.3 → 6.3 | 145-174: 6.3; 250-254: 12.2 |
| 06 | 034 | none | s22_24 | 141 → 141 (+0) | 51: hold 3 → 50: hold 9 | 0; 0 → 0; 0 | 1.4 → 3.5 | 55-59: 3.5; 136-136: 49.4 |
| 06 | 034 | through | s22_26 | 141 → 141 (+0) | 51: hold 3 → 50: hold 9 | 0; 0 → 0; 0 | 1.4 → 3.5 | 55-59: 3.5; 136-136: 49.4 |
| 07 | 035 | accord | s23_03 | 194 → 189 (-5) | 24: hold 1 → 24: hold 1 | 0; 0 → 0; 0 | 58.3 → 58.3 | none |
| 07 | 035 | accord | s23_04 | 214 → 206 (-8) | 24: hold 1 → 24: hold 1 | 0; 0 → 0; 0 | 50.0 → 50.0 | none |
| 07 | 035 | through | s23_06 | 194 → 197 (+3) | 24: hold 1 → 0: hold 2 | 0; 0 → 1; 40 | 58.3 → 30.0 | 27-31: 30.0 |
| 07 | 035 | through | s23_07 | 214 → 198 (-16) | 24: hold 1 → 0: hold 2 | 0; 0 → 1; 40 | 50.0 → 30.0 | 27-31: 30.0 |
| 07 | 035 | none | s05_01 | 194 → 197 (+3) | 24: hold 1 → 0: hold 2 | 0; 0 → 1; 40 | 58.3 → 30.0 | 27-31: 30.0 |
| 07 | 035 | none | s05_02 | 214 → 198 (-16) | 24: hold 1 → 0: hold 2 | 0; 0 → 1; 40 | 50.0 → 30.0 | 27-31: 30.0 |
| 07 | 036 | none | s23_09 | 173 → 173 (+0) | 24: hold 2 → 11: hold 2 | 1; 7 → 1; 7 | 56.6 → 56.6 | none |
| 07 | 036 | through | s23_11 | 173 → 177 (+4) | 24: hold 2 → 10: switch | 1; 7 → 2; 32 | 56.6 → 297.2 | none |
| 07 | 036 | through_rw | s23_13 | 173 → 173 (+0) | 24: hold 2 → 12: hold 2 | 1; 7 → 1; 7 | 56.6 → 56.6 | none |
| 07 | 037 | none | s23_15 | 171 → 171 (+0) | None: none → None: none | 0; 0 → 0; 0 | 14.8 → 14.8 | 213-220: 14.8 |
| 07 | 037 | accord | s23_17 | 171 → 171 (+0) | None: none → None: none | 0; 0 → 0; 0 | 14.8 → 14.8 | 213-220: 14.8 |
| 07 | 037 | through | s23_19 | 171 → 171 (+0) | None: none → None: none | 0; 0 → 0; 0 | 14.8 → 14.8 | 213-220: 14.8 |
| 07 | 038 | none | s23_21 | 172 → 179 (+7) | None: none → 36: hold 7 | 0; 0 → 1; 16 | 45.7 → 19.3 | 52-56: 19.3; 210-214: 45.7 |
| 07 | 038 | accord | s23_23 | 172 → 224 (+52) | None: none → 36: hold 7 | 0; 0 → 1; 2 | 45.7 → 52.1 | none |
| 07 | 038 | through | s23_25 | 172 → 179 (+7) | None: none → 36: hold 7 | 0; 0 → 1; 16 | 45.7 → 19.3 | 52-56: 19.3; 210-214: 45.7 |
| 07 | 039 | none | s23_27 | 171 → 171 (+0) | None: none → None: none | 2; 42 → 2; 42 | 392.1 → 392.1 | none |
| 07 | 039 | accord | s23_29 | 171 → 171 (+0) | None: none → None: none | 2; 42 → 2; 42 | 392.1 → 392.1 | none |
| 07 | 040 | none | s23_31 | 172 → 172 (+0) | None: none → None: none | 0; 0 → 0; 0 | 41.4 → 41.4 | 186-190: 41.4 |
| 07 | 040 | through | s23_33 | 172 → 172 (+0) | None: none → None: none | 0; 0 → 0; 0 | 41.4 → 41.4 | 186-190: 41.4 |
| 07 | 040 | through_rw | s23_35 | 172 → 172 (+0) | None: none → None: none | 0; 0 → 0; 0 | 41.4 → 41.4 | 186-190: 41.4 |
| 07 | 041 | none | s24_02 | 301 → 313 (+12) | 100: hold 55 → 94: hold 67 | 1; 17 → 1; 17 | 4.0 → 5.7 | 118-123: 5.7; 157-161: 5.7 |
| 07 | 041 | through | s24_04 | 301 → 313 (+12) | 100: hold 55 → 94: hold 67 | 1; 17 → 2; 62 | 4.0 → 5.7 | 118-123: 5.7; 157-161: 5.7 |
| 07 | 041 | through_rw | s24_06 | 301 → 313 (+12) | 100: hold 55 → 94: hold 67 | 1; 17 → 1; 17 | 4.0 → 5.7 | 118-123: 5.7; 157-161: 5.7 |
| 07 | 042 | none | s24_08 | 252 → 252 (+0) | 116: hold 4 → 83: hold 3 | 0; 0 → 1; 14 | 4.1 → 4.1 | 147-151: 4.1 |
| 07 | 042 | accord | s24_10 | 252 → 254 (+2) | 116: hold 4 → 83: hold 3 | 0; 0 → 1; 14 | 4.1 → 3.9 | 148-152: 3.9 |
| 07 | 042 | through | s24_12 | 252 → 252 (+0) | 116: hold 4 → 83: hold 3 | 0; 0 → 1; 14 | 4.1 → 4.1 | 147-151: 4.1 |
| 07 | 043 | none | s24_14 | 272 → 279 (+7) | 85: hold 5 → 85: hold 5 | 0; 0 → 0; 0 | 28.4 → 35.2 | 86-90: 35.2 |
| 07 | 043 | accord | s24_16 | 272 → 279 (+7) | 85: hold 5 → 85: hold 5 | 0; 0 → 0; 0 | 28.4 → 35.2 | 86-90: 35.2 |
| 07 | 043 | through | s24_18 | 272 → 279 (+7) | 85: hold 5 → 85: hold 5 | 0; 0 → 0; 0 | 28.4 → 35.2 | 86-90: 35.2 |
| 07 | 044 | none | s24_20 | 261 → 261 (+0) | None: none → None: none | 0; 0 → 0; 0 | 26.6 → 26.6 | 308-314: 26.6 |
| 07 | 044 | through | s24_22 | 261 → 261 (+0) | None: none → None: none | 0; 0 → 0; 0 | 26.6 → 26.6 | 308-314: 26.6 |
| 07 | 044 | through_rw | s24_24 | 261 → 261 (+0) | None: none → None: none | 0; 0 → 0; 0 | 26.6 → 26.6 | 308-314: 26.6 |
| 07 | 045 | none | s24_26 | 261 → 261 (+0) | None: none → None: none | 2; 39 → 2; 48 | 353.5 → 353.5 | none |
| 07 | 045 | accord | s24_28 | 261 → 261 (+0) | None: none → None: none | 2; 39 → 2; 48 | 353.5 → 353.5 | none |
| 07 | 045 | through | s24_30 | 261 → 261 (+0) | None: none → None: none | 2; 39 → 2; 48 | 353.5 → 353.5 | none |
| 19 | 046 | none | s25_02 | 122 → 122 (+0) | None: none → None: none | 0; 0 → 0; 0 | 40.3 → 40.3 | 175-181: 40.3 |
| 19 | 046 | through | s25_04 | 122 → 122 (+0) | None: none → None: none | 0; 0 → 0; 0 | 40.3 → 40.3 | 175-181: 40.3 |
| 19 | 047 | none | s25_06 | 58 → 58 (+0) | None: none → None: none | 0; 0 → 0; 0 | 13.2 → 13.2 | 180-188: 13.2 |
| 19 | 047 | through | s25_08 | 58 → 58 (+0) | None: none → None: none | 0; 0 → 0; 0 | 13.2 → 13.2 | 180-188: 13.2 |
| 19 | 048 | none | s25_10 | 152 → 152 (+0) | 146: hold 2 → 145: hold 2 | 0; 0 → 0; 0 | 51.9 → 51.9 | none |
| 19 | 048 | accord | s25_12 | 152 → 152 (+0) | 146: hold 2 → 145: hold 2 | 0; 0 → 0; 0 | 51.9 → 51.9 | none |
| 19 | 048 | through | s25_14 | 152 → 152 (+0) | 146: hold 2 → 145: hold 2 | 0; 0 → 0; 0 | 51.9 → 51.9 | none |
| 19 | 049 | none | s25_16 | 100 → 100 (+0) | 93: hold 3 → 93: hold 3 | 0; 0 → 0; 0 | 61.6 → 61.6 | none |
| 19 | 049 | accord | s25_18 | 100 → 100 (+0) | 93: hold 3 → 93: hold 3 | 0; 0 → 0; 0 | 61.6 → 61.6 | none |
| 19 | 049 | through | s25_20 | 100 → 100 (+0) | 93: hold 3 → 93: hold 3 | 0; 0 → 0; 0 | 61.6 → 61.6 | none |
| 19 | 050 | none | s25_22 | 74 → 74 (+0) | None: none → None: none | 2; 17 → 2; 17 | 31.6 → 31.6 | 271-277: 31.6 |
| 19 | 050 | accord | s25_24 | 74 → 74 (+0) | None: none → None: none | 2; 17 → 2; 17 | 31.6 → 31.6 | 271-277: 31.6 |
| 19 | 050 | through | s25_26 | 74 → 74 (+0) | None: none → None: none | 2; 17 → 2; 17 | 31.6 → 31.6 | 271-277: 31.6 |
| 19 | 051 | none | s25_28 | 145 → 145 (+0) | None: none → None: none | 0; 0 → 0; 0 | 246.6 → 246.6 | none |
| 19 | 051 | accord | s25_30 | 145 → 145 (+0) | None: none → None: none | 0; 0 → 0; 0 | 246.6 → 246.6 | none |
| 19 | 051 | through | s25_32 | 145 → 145 (+0) | None: none → None: none | 0; 0 → 0; 0 | 246.6 → 246.6 | none |
| 19 | 052 | none | s25_34 | 150 → 150 (+0) | None: none → None: none | 0; 0 → 0; 0 | 8.0 → 8.0 | 163-168: 8.0; 190-197: 29.5 |
| 19 | 052 | accord | s25_36 | 150 → 150 (+0) | None: none → None: none | 0; 0 → 0; 0 | 8.0 → 8.0 | 163-168: 8.0; 190-197: 29.5 |
| 19 | 052 | through | s25_38 | 150 → 150 (+0) | None: none → None: none | 0; 0 → 0; 0 | 8.0 → 8.0 | 163-168: 8.0; 190-197: 29.5 |
| 19 | 053 | none | s25_40 | 122 → 122 (+0) | None: none → None: none | 0; 0 → 0; 0 | 215.7 → 215.7 | none |
| 19 | 053 | through | s25_42 | 122 → 122 (+0) | None: none → None: none | 0; 0 → 0; 0 | 215.7 → 215.7 | none |
| 19 | 054 | none | s25_44 | 111 → 111 (+0) | None: none → None: none | 1; 9 → 1; 9 | 41.0 → 41.0 | 193-198: 41.0 |
| 19 | 054 | accord | s25_46 | 111 → 111 (+0) | None: none → None: none | 1; 9 → 1; 9 | 41.0 → 41.0 | 193-198: 41.0 |
| 19 | 054 | through | s25_48 | 111 → 111 (+0) | None: none → None: none | 1; 9 → 1; 9 | 41.0 → 41.0 | 193-198: 41.0 |
| 19 | 055 | none | s25_50 | 87 → 87 (+0) | None: none → None: none | 0; 0 → 0; 0 | 37.5 → 37.5 | 242-247: 37.5 |
| 19 | 055 | through | s25_52 | 87 → 87 (+0) | None: none → None: none | 0; 0 → 0; 0 | 37.5 → 37.5 | 242-247: 37.5 |
| 19 | 056 | none | s26_02 | 232 → 232 (+0) | None: none → None: none | 0; 0 → 0; 0 | 308.7 → 308.7 | none |
| 19 | 056 | through | s26_04 | 232 → 232 (+0) | None: none → None: none | 0; 0 → 0; 0 | 308.7 → 308.7 | none |
| 19 | 057 | none | s26_06 | 162 → 162 (+0) | None: none → None: none | 0; 0 → 0; 0 | 2.7 → 2.7 | 236-243: 11.3; 443-451: 2.7 |
| 19 | 057 | through | s26_08 | 162 → 162 (+0) | None: none → None: none | 0; 0 → 0; 0 | 2.7 → 2.7 | 236-243: 11.3; 443-451: 2.7 |
| 19 | 058 | none | s26_10 | 271 → 271 (+0) | None: none → None: none | 0; 0 → 0; 0 | 52.8 → 52.8 | none |
| 19 | 058 | accord | s26_12 | 271 → 271 (+0) | None: none → None: none | 0; 0 → 0; 0 | 52.8 → 52.8 | none |
| 19 | 058 | through | s26_14 | 271 → 271 (+0) | None: none → None: none | 0; 0 → 0; 0 | 52.8 → 52.8 | none |
| 19 | 059 | none | s26_16 | 286 → 286 (+0) | 174: hold 8 → 172: hold 8 | 1; 9 → 1; 9 | 8.4 → 8.4 | 288-298: 8.4 |
| 19 | 059 | accord | s26_18 | 286 → 286 (+0) | 174: hold 8 → 172: hold 8 | 1; 9 → 1; 9 | 8.4 → 8.4 | 288-298: 8.4 |
| 19 | 059 | through | s26_20 | 286 → 286 (+0) | 174: hold 8 → 172: hold 8 | 1; 9 → 1; 9 | 8.4 → 8.4 | 288-298: 8.4 |
| 19 | 060 | none | s26_22 | 250 → 250 (+0) | None: none → None: none | 0; 0 → 0; 0 | 11.2 → 11.2 | 316-324: 11.2 |
| 19 | 060 | accord | s26_24 | 250 → 250 (+0) | None: none → None: none | 0; 0 → 0; 0 | 11.2 → 11.2 | 316-324: 11.2 |
| 19 | 060 | through | s26_26 | 250 → 250 (+0) | None: none → None: none | 0; 0 → 0; 0 | 11.2 → 11.2 | 316-324: 11.2 |
| 19 | 061 | none | s26_28 | 272 → 272 (+0) | None: none → None: none | 2; 60 → 2; 76 | 111.2 → 111.2 | none |
| 19 | 061 | through | s26_30 | 272 → 272 (+0) | None: none → None: none | 2; 60 → 2; 76 | 111.2 → 111.2 | none |
| 19 | 062 | none | s26_32 | 281 → 281 (+0) | 172: hold 9 → 167: hold 9 | 1; 64 → 1; 69 | 124.9 → 124.9 | none |
| 19 | 062 | accord | s26_34 | 281 → 281 (+0) | 172: hold 9 → 167: hold 9 | 1; 64 → 1; 69 | 124.9 → 124.9 | none |
| 19 | 062 | through | s26_36 | 281 → 281 (+0) | 172: hold 9 → 167: hold 9 | 1; 64 → 1; 69 | 124.9 → 124.9 | none |
| 19 | 063 | none | s26_38 | 214 → 214 (+0) | None: none → None: none | 1; 1 → 1; 1 | 471.8 → 471.8 | none |
| 19 | 063 | through | s26_40 | 214 → 214 (+0) | None: none → None: none | 1; 1 → 1; 1 | 471.8 → 471.8 | none |
| 19 | 064 | none | s26_42 | 267 → 267 (+0) | None: none → None: none | 1; 9 → 1; 9 | 0.2 → 0.2 | 356-364: 0.2 |
| 19 | 064 | accord | s26_44 | 267 → 267 (+0) | None: none → None: none | 1; 9 → 1; 9 | 0.2 → 0.2 | 356-364: 0.2 |
| 19 | 064 | through | s26_46 | 267 → 267 (+0) | None: none → None: none | 1; 9 → 1; 9 | 0.2 → 0.2 | 356-364: 0.2 |
| 19 | 065 | none | s26_48 | 257 → 256 (-1) | 72: hold 15 → 72: hold 15 | 0; 0 → 0; 0 | 3.6 → 3.6 | 180-185: 23.1; 281-289: 3.6 |
| 19 | 065 | accord | s26_50 | 257 → 256 (-1) | 72: hold 15 → 72: hold 15 | 0; 0 → 0; 0 | 3.6 → 3.6 | 180-185: 23.1; 281-289: 3.6 |
| 19 | 065 | through | s26_52 | 257 → 256 (-1) | 72: hold 15 → 72: hold 15 | 0; 0 → 0; 0 | 3.6 → 3.6 | 180-185: 23.1; 281-289: 3.6 |
| 19 | 066 | none | s27_02 | 86 → 86 (+0) | None: none → None: none | 0; 0 → 0; 0 | 379.0 → 379.0 | none |
| 19 | 066 | through | s27_04 | 86 → 86 (+0) | None: none → None: none | 0; 0 → 0; 0 | 379.0 → 379.0 | none |
| 19 | 067 | none | s27_06 | 74 → 74 (+0) | None: none → None: none | 0; 0 → 0; 0 | 1045.6 → 1045.6 | none |
| 19 | 067 | through | s27_08 | 74 → 74 (+0) | None: none → None: none | 0; 0 → 0; 0 | 1045.6 → 1045.6 | none |
| 19 | 068 | none | s27_10 | 151 → 151 (+0) | None: none → None: none | 0; 0 → 0; 0 | 25.6 → 25.6 | 246-252: 25.6 |
| 19 | 068 | through | s27_12 | 151 → 151 (+0) | None: none → None: none | 0; 0 → 0; 0 | 25.6 → 25.6 | 246-252: 25.6 |
| 19 | 069 | none | s27_14 | 97 → 97 (+0) | None: none → None: none | 0; 0 → 0; 0 | 40.0 → 40.0 | 197-203: 40.0 |
| 19 | 069 | accord | s27_16 | 97 → 97 (+0) | None: none → None: none | 0; 0 → 0; 0 | 40.0 → 40.0 | 197-203: 40.0 |
| 19 | 069 | through | s27_18 | 97 → 97 (+0) | None: none → None: none | 0; 0 → 0; 0 | 40.0 → 40.0 | 197-203: 40.0 |
| 19 | 070 | none | s27_20 | 65 → 65 (+0) | None: none → None: none | 1; 9 → 1; 9 | 20.9 → 20.9 | 292-299: 20.9 |
| 19 | 070 | accord | s27_22 | 65 → 65 (+0) | None: none → None: none | 1; 9 → 1; 9 | 20.9 → 20.9 | 292-299: 20.9 |
| 19 | 070 | through | s27_24 | 65 → 65 (+0) | None: none → None: none | 1; 9 → 1; 9 | 20.9 → 20.9 | 292-299: 20.9 |
| 19 | 071 | none | s27_26 | 118 → 118 (+0) | None: none → None: none | 0; 0 → 0; 0 | 948.7 → 948.7 | none |
| 19 | 071 | through | s27_28 | 118 → 118 (+0) | None: none → None: none | 0; 0 → 0; 0 | 948.7 → 948.7 | none |
| 19 | 072 | none | s27_30 | 116 → 116 (+0) | None: none → None: none | 2; 27 → 2; 27 | 141.9 → 141.9 | none |
| 19 | 072 | accord | s27_32 | 116 → 116 (+0) | None: none → None: none | 2; 27 → 2; 27 | 141.9 → 141.9 | none |
| 19 | 072 | through | s27_34 | 116 → 116 (+0) | None: none → None: none | 2; 27 → 2; 27 | 141.9 → 141.9 | none |
| 19 | 073 | none | s27_36 | 116 → 116 (+0) | None: none → None: none | 0; 0 → 0; 0 | 119.5 → 119.5 | none |
| 19 | 073 | accord | s27_38 | 116 → 116 (+0) | None: none → None: none | 0; 0 → 0; 0 | 119.5 → 119.5 | none |
| 19 | 073 | through | s27_40 | 116 → 116 (+0) | None: none → None: none | 0; 0 → 0; 0 | 119.5 → 119.5 | none |
| 19 | 074 | none | s27_42 | 100 → 100 (+0) | None: none → None: none | 1; 9 → 1; 9 | 88.0 → 88.0 | none |
| 19 | 075 | none | s27_44 | 59 → 59 (+0) | None: none → None: none | 1; 15 → 2; 17 | 1012.1 → 1012.1 | none |
| 19 | 075 | accord | s27_46 | 59 → 59 (+0) | None: none → None: none | 1; 15 → 1; 11 | 1012.1 → 1012.1 | none |
| 19 | 075 | through | s27_48 | 59 → 59 (+0) | None: none → None: none | 1; 15 → 2; 17 | 1012.1 → 1012.1 | none |
| 20 | 076 | none | s28_02 | 293 → 293 (+0) | 139: hold 7 → 139: hold 7 | 0; 0 → 0; 0 | 2.5 → 2.5 | 140-146: 2.5 |
| 20 | 076 | through | s28_04 | 293 → 293 (+0) | 139: hold 7 → 139: hold 7 | 0; 0 → 0; 0 | 2.5 → 2.5 | 140-146: 2.5 |
| 20 | 077 | none | s28_06 | 107 → 107 (+0) | None: none → None: none | 0; 0 → 0; 0 | 710.2 → 710.2 | none |
| 20 | 077 | through | s28_08 | 107 → 107 (+0) | None: none → None: none | 0; 0 → 0; 0 | 710.2 → 710.2 | none |
| 20 | 078 | none | s28_10 | 98 → 98 (+0) | None: none → None: none | 0; 0 → 0; 0 | 35.4 → 35.4 | 249-253: 35.4 |
| 20 | 078 | accord | s28_12 | 98 → 98 (+0) | None: none → None: none | 0; 0 → 0; 0 | 35.4 → 35.4 | 249-253: 35.4 |
| 20 | 078 | through | s28_14 | 98 → 98 (+0) | None: none → None: none | 0; 0 → 0; 0 | 35.4 → 35.4 | 249-253: 35.4 |
| 20 | 079 | none | s28_16 | 211 → 211 (+0) | None: none → None: none | 0; 0 → 0; 0 | 196.9 → 196.9 | none |
| 20 | 079 | accord | s28_18 | 211 → 211 (+0) | None: none → None: none | 0; 0 → 0; 0 | 196.9 → 196.9 | none |
| 20 | 079 | through | s28_20 | 211 → 211 (+0) | None: none → None: none | 0; 0 → 0; 0 | 196.9 → 196.9 | none |
| 20 | 080 | none | s28_22 | 171 → 171 (+0) | None: none → None: none | 1; 16 → 1; 16 | 200.0 → 200.0 | none |
| 20 | 080 | accord | s28_24 | 171 → 171 (+0) | None: none → None: none | 1; 16 → 1; 16 | 200.0 → 200.0 | none |
| 20 | 080 | through | s28_26 | 171 → 171 (+0) | None: none → None: none | 1; 16 → 1; 16 | 200.0 → 200.0 | none |
| 20 | 081 | none | s28_28 | 101 → 101 (+0) | None: none → None: none | 1; 8 → 1; 8 | 17.9 → 17.9 | 217-224: 17.9 |
| 20 | 081 | accord | s28_30 | 101 → 101 (+0) | None: none → None: none | 1; 8 → 1; 8 | 17.9 → 17.9 | 217-224: 17.9 |
| 20 | 082 | none | s28_32 | 143 → 143 (+0) | None: none → None: none | 0; 0 → 0; 0 | 30.1 → 30.1 | 201-207: 30.1 |
| 20 | 082 | accord | s28_34 | 143 → 143 (+0) | None: none → None: none | 0; 0 → 0; 0 | 30.1 → 30.1 | 201-207: 30.1 |
| 20 | 082 | through | s28_36 | 143 → 143 (+0) | None: none → None: none | 0; 0 → 0; 0 | 30.1 → 30.1 | 201-207: 30.1 |
| 20 | 083 | none | s28_38 | 178 → 178 (+0) | None: none → None: none | 0; 0 → 0; 0 | 890.7 → 890.7 | none |
| 20 | 083 | through | s28_40 | 178 → 178 (+0) | None: none → None: none | 0; 0 → 0; 0 | 890.7 → 890.7 | none |
| 20 | 084 | none | s28_42 | 250 → 250 (+0) | None: none → None: none | 0; 0 → 0; 0 | 55.0 → 55.0 | none |
| 20 | 084 | accord | s28_44 | 250 → 250 (+0) | None: none → None: none | 0; 0 → 0; 0 | 55.0 → 55.0 | none |
| 20 | 084 | through | s28_46 | 250 → 250 (+0) | None: none → None: none | 0; 0 → 0; 0 | 55.0 → 55.0 | none |
| 20 | 085 | none | s28_48 | 93 → 93 (+0) | None: none → None: none | 1; 2 → 0; 0 | 267.6 → 267.6 | none |
| 20 | 086 | none | s29_02 | 167 → 167 (+0) | None: none → None: none | 1; 41 → 1; 41 | 329.5 → 329.5 | none |
| 20 | 086 | through | s29_04 | 167 → 167 (+0) | None: none → None: none | 1; 41 → 1; 41 | 329.5 → 329.5 | none |
| 20 | 087 | none | s29_06 | 242 → 242 (+0) | None: none → None: none | 0; 0 → 0; 0 | 185.8 → 185.8 | none |
| 20 | 087 | through | s29_08 | 242 → 242 (+0) | None: none → None: none | 0; 0 → 0; 0 | 185.8 → 185.8 | none |
| 20 | 088 | none | s29_10 | 219 → 219 (+0) | None: none → None: none | 0; 0 → 0; 0 | 72.0 → 72.0 | none |
| 20 | 088 | accord | s29_12 | 219 → 219 (+0) | None: none → None: none | 0; 0 → 0; 0 | 72.0 → 72.0 | none |
| 20 | 088 | through | s29_14 | 219 → 219 (+0) | None: none → None: none | 0; 0 → 0; 0 | 72.0 → 72.0 | none |
| 20 | 089 | none | s29_16 | 217 → 216 (-1) | 166: hold 24 → 146: hold 5 | 0; 0 → 0; 0 | 207.5 → 213.3 | none |
| 20 | 089 | accord | s29_18 | 217 → 211 (-6) | 166: hold 24 → 166: hold 24 | 0; 0 → 0; 0 | 207.5 → 207.5 | none |
| 20 | 089 | through | s29_20 | 217 → 216 (-1) | 166: hold 24 → 146: hold 5 | 0; 0 → 0; 0 | 207.5 → 213.3 | none |
| 20 | 090 | none | s29_22 | 256 → 256 (+0) | None: none → None: none | 1; 9 → 1; 9 | 332.2 → 332.2 | none |
| 20 | 090 | accord | s29_24 | 256 → 256 (+0) | None: none → None: none | 1; 9 → 1; 9 | 332.2 → 332.2 | none |
| 20 | 090 | through | s29_26 | 256 → 256 (+0) | None: none → None: none | 1; 9 → 1; 9 | 332.2 → 332.2 | none |
| 20 | 091 | none | s29_28 | 160 → 160 (+0) | None: none → None: none | 0; 0 → 0; 0 | 646.7 → 646.7 | none |
| 20 | 091 | accord | s29_30 | 160 → 160 (+0) | None: none → None: none | 0; 0 → 0; 0 | 646.7 → 646.7 | none |
| 20 | 091 | through | s29_32 | 160 → 160 (+0) | None: none → None: none | 0; 0 → 0; 0 | 646.7 → 646.7 | none |
| 20 | 092 | none | s29_34 | 182 → 182 (+0) | None: none → None: none | 1; 9 → 1; 9 | 696.0 → 696.0 | none |
| 20 | 092 | accord | s29_36 | 182 → 182 (+0) | None: none → None: none | 1; 9 → 1; 9 | 696.0 → 696.0 | none |
| 20 | 092 | through | s29_38 | 182 → 182 (+0) | None: none → None: none | 1; 9 → 1; 9 | 696.0 → 696.0 | none |
| 20 | 093 | none | s29_40 | 184 → 184 (+0) | None: none → None: none | 0; 0 → 0; 0 | 24.3 → 24.3 | 238-244: 24.3 |
| 20 | 093 | through | s29_42 | 184 → 184 (+0) | None: none → None: none | 0; 0 → 0; 0 | 24.3 → 24.3 | 238-244: 24.3 |
| 20 | 094 | none | s29_44 | 214 → 214 (+0) | None: none → None: none | 1; 21 → 1; 7 | 91.0 → 91.0 | none |
| 20 | 094 | through | s29_46 | 214 → 214 (+0) | None: none → None: none | 1; 21 → 1; 7 | 91.0 → 91.0 | none |
| 20 | 095 | none | s29_48 | 267 → 267 (+0) | None: none → None: none | 3; 78 → 3; 65 | 226.9 → 226.9 | none |
| 20 | 095 | accord | s29_50 | 267 → 267 (+0) | None: none → None: none | 3; 78 → 3; 65 | 226.9 → 226.9 | none |
| 20 | 096 | none | s30_02 | 101 → 101 (+0) | None: none → None: none | 0; 0 → 0; 0 | 1367.6 → 1367.6 | none |
| 20 | 096 | through | s30_04 | 101 → 101 (+0) | None: none → None: none | 0; 0 → 0; 0 | 1367.6 → 1367.6 | none |
| 20 | 097 | none | s30_06 | 145 → 145 (+0) | None: none → None: none | 0; 0 → 0; 0 | 4.0 → 4.0 | 324-332: 4.0 |
| 20 | 097 | through | s30_08 | 145 → 145 (+0) | None: none → None: none | 0; 0 → 0; 0 | 4.0 → 4.0 | 324-332: 4.0 |
| 20 | 098 | none | s30_10 | 151 → 151 (+0) | None: none → None: none | 0; 0 → 0; 0 | 603.0 → 603.0 | none |
| 20 | 098 | accord | s30_12 | 151 → 151 (+0) | None: none → None: none | 0; 0 → 0; 0 | 603.0 → 603.0 | none |
| 20 | 098 | through | s30_14 | 151 → 151 (+0) | None: none → None: none | 0; 0 → 0; 0 | 603.0 → 603.0 | none |
| 20 | 099 | none | s30_16 | 162 → 162 (+0) | None: none → None: none | 0; 0 → 0; 0 | 26.6 → 26.6 | 198-204: 26.6 |
| 20 | 099 | accord | s30_18 | 162 → 162 (+0) | None: none → None: none | 0; 0 → 0; 0 | 26.6 → 26.6 | 198-204: 26.6 |
| 20 | 099 | through | s30_20 | 162 → 162 (+0) | None: none → None: none | 0; 0 → 0; 0 | 26.6 → 26.6 | 198-204: 26.6 |
| 20 | 100 | none | s30_22 | 92 → 92 (+0) | None: none → None: none | 2; 36 → 2; 36 | 926.7 → 926.7 | none |
| 20 | 100 | accord | s30_24 | 92 → 92 (+0) | None: none → None: none | 2; 36 → 2; 36 | 926.7 → 926.7 | none |
| 20 | 100 | through | s30_26 | 92 → 92 (+0) | None: none → None: none | 2; 36 → 2; 36 | 926.7 → 926.7 | none |
| 20 | 101 | none | s30_28 | 149 → 149 (+0) | None: none → None: none | 0; 0 → 0; 0 | 262.7 → 262.7 | none |
| 20 | 101 | accord | s30_30 | 149 → 149 (+0) | None: none → None: none | 0; 0 → 0; 0 | 262.7 → 262.7 | none |
| 20 | 101 | through | s30_32 | 149 → 149 (+0) | None: none → None: none | 0; 0 → 0; 0 | 262.7 → 262.7 | none |
| 20 | 102 | none | s30_34 | 154 → 154 (+0) | None: none → None: none | 0; 0 → 0; 0 | 1334.8 → 1334.8 | none |
| 20 | 102 | through | s30_36 | 154 → 154 (+0) | None: none → None: none | 0; 0 → 0; 0 | 1334.8 → 1334.8 | none |
| 20 | 103 | none | s30_38 | 151 → 151 (+0) | None: none → None: none | 1; 40 → 1; 45 | 514.5 → 514.5 | none |
| 20 | 103 | through | s30_40 | 151 → 151 (+0) | None: none → None: none | 1; 40 → 1; 45 | 514.5 → 514.5 | none |
| 20 | 104 | none | s30_42 | 92 → 92 (+0) | None: none → None: none | 0; 0 → 1; 16 | 697.4 → 697.4 | none |
| 20 | 104 | accord | s30_44 | 92 → 92 (+0) | None: none → None: none | 0; 0 → 1; 6 | 697.4 → 697.4 | none |
| 20 | 105 | none | s30_46 | 107 → 107 (+0) | None: none → None: none | 1; 31 → 1; 20 | 20.5 → 20.5 | 182-189: 20.5 |
| 20 | 105 | accord | s30_48 | 107 → 107 (+0) | None: none → None: none | 1; 31 → 1; 20 | 20.5 → 20.5 | 182-189: 20.5 |
| 20 | 105 | through | s30_50 | 107 → 107 (+0) | None: none → None: none | 1; 31 → 1; 20 | 20.5 → 20.5 | 182-189: 20.5 |

**Tallies (on against off)**

| group | setting | runs | completion better / equal / worse (ticks gained / lost) | response earlier / equal / later | wrong records off → on (count; ticks) |
|---|---|---|---|---|---|
| four rooms | none | 46 | 1 / 39 / 6 (16 / 32) | 11 / 6 / 0 | 20; 347 → 24; 440 |
| four rooms | accord | 31 | 2 / 25 / 4 (13 / 62) | 4 / 7 / 0 | 16; 269 → 19; 264 |
| four rooms | through | 44 | 1 / 36 / 7 (16 / 36) | 9 / 6 / 2 | 15; 255 → 21; 431 |
| four rooms | through_rw | 11 | 0 / 10 / 1 (0 / 12) | 3 / 1 / 0 | 2; 24 → 2; 24 |
| two new rooms | none | 60 | 2 / 58 / 0 (2 / 0) | 4 / 3 / 0 | 28; 520 → 29; 524 |
| two new rooms | accord | 35 | 2 / 33 / 0 (7 / 0) | 3 / 3 / 0 | 20; 346 → 21; 329 |
| two new rooms | through | 55 | 2 / 53 / 0 (2 / 0) | 4 / 3 / 0 | 22; 423 → 23; 426 |

**Every case below min_separation, with its cause**

| room | script | setting | side | scenario | ticks | min | standing / viol / recede | decision in force | human's true task | wrong admission in force | cause |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 02 | 001 | accord | on | s17_03 | 72-78 | 30.9 | 4 / 0 / 3 | 5: admitted item_2 | item_2 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 02 | 001 | accord | off | s02_01 | 72-78 | 30.9 | 4 / 0 / 3 | 23: admitted item_2 | item_2 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 02 | 001 | through | on | s17_05 | 72-78 | 30.9 | 4 / 0 / 3 | 27: admitted item_2 | item_2 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 02 | 001 | none | on | s02_01 | 72-78 | 30.9 | 4 / 0 / 3 | 5: admitted item_2 | item_2 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 02 | 003 | none | on | s17_12 | 291-295 | 40.6 | 5 / 0 / 0 | 281: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 02 | 003 | none | off | s17_12 | 291-295 | 40.6 | 5 / 0 / 0 | 281: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 02 | 003 | through | on | s17_14 | 291-295 | 40.6 | 5 / 0 / 0 | 281: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 02 | 003 | through_rw | on | s17_16 | 291-295 | 40.6 | 5 / 0 / 0 | 281: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 02 | 005 | none | on | s17_24 | 286-290 | 9.7 | 4 / 0 / 1 | 286: fallback moving k=5 | unmodelled |  | the same on both sides: not a context effect; decision in force: a fallback |
| 02 | 005 | none | off | s17_24 | 286-290 | 9.7 | 4 / 0 / 1 | 286: fallback moving k=5 | unmodelled |  | the same on both sides: not a context effect; decision in force: a fallback |
| 02 | 005 | accord | on | s17_26 | 286-290 | 9.7 | 4 / 0 / 1 | 286: fallback moving k=5 | unmodelled |  | the same on both sides: not a context effect; decision in force: a fallback |
| 02 | 005 | through | on | s17_28 | 286-290 | 9.7 | 4 / 0 / 1 | 286: fallback moving k=5 | unmodelled |  | the same on both sides: not a context effect; decision in force: a fallback |
| 02 | 008 | none | on | s18_02 | 197-202 | 23.6 | 4 / 2 / 0 | 134: admitted item_11 | item_11 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 02 | 008 | none | off | s18_02 | 197-202 | 23.6 | 4 / 2 / 0 | 157: admitted item_11 | item_11 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 02 | 008 | through | on | s18_04 | 197-202 | 23.6 | 4 / 2 / 0 | 134: admitted item_11 | item_11 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 02 | 008 | through_rw | on | s18_06 | 197-202 | 23.6 | 4 / 2 / 0 | 134: admitted item_11 | item_11 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 05 | 015 | none | on | s19_13 | 153-154 | 34.9 | 1 / 0 / 1 | 37: admitted item_3 | item_3 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 05 | 015 | none | on | s19_13 | 270-275 | 2.2 | 3 / 1 / 2 | 253: admitted item_6 | item_6 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 05 | 015 | none | off | s19_13 | 153-154 | 34.9 | 1 / 0 / 1 | 55: admitted item_3 | item_3 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 05 | 015 | none | off | s19_13 | 270-275 | 2.2 | 3 / 1 / 2 | 253: admitted item_6 | item_6 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 05 | 015 | accord | on | s19_15 | 153-154 | 34.9 | 1 / 0 / 1 | 37: admitted item_3 | item_3 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 05 | 015 | accord | on | s19_15 | 270-275 | 2.2 | 3 / 1 / 2 | 253: admitted item_6 | item_6 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 05 | 015 | through | on | s19_17 | 51-52 | 33.1 | 0 / 1 / 1 | 51: fallback moving k=19 | item_3 |  | fallback under the window: under break_time the delivery of item_3 is admitted at 59 (no fact: 37; off: 55); at 51 the robot rests on a moving fallback (k = 19) and passes the human |
| 05 | 015 | through | on | s19_17 | 270-275 | 2.2 | 3 / 1 / 2 | 249: admitted item_6 | item_6 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 05 | 016 | none | on | s19_19 | 291-298 | 28.8 | 8 / 0 / 0 | 284: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 016 | none | off | s19_19 | 291-298 | 28.8 | 8 / 0 / 0 | 284: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 016 | accord | on | s19_21 | 291-298 | 28.8 | 8 / 0 / 0 | 284: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 016 | through | on | s19_23 | 291-298 | 28.8 | 8 / 0 / 0 | 284: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 019 | none | on | s20_02 | 356-364 | 12.4 | 9 / 0 / 0 | 256: admitted item_33 | item_33 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 019 | none | off | s20_02 | 356-364 | 12.4 | 9 / 0 / 0 | 254: fallback moving k=11 | item_33 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 019 | through | on | s20_04 | 356-364 | 12.4 | 9 / 0 / 0 | 256: admitted item_33 | item_33 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 019 | through_rw | on | s20_06 | 356-364 | 12.4 | 9 / 0 / 0 | 256: admitted item_33 | item_33 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 021 | none | on | s20_14 | 307-314 | 12.4 | 8 / 0 / 0 | 278: admitted item_33 | item_33 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 021 | none | off | s20_14 | 307-314 | 12.4 | 8 / 0 / 0 | 278: admitted item_33 | item_33 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 021 | accord | on | s20_16 | 307-314 | 12.4 | 8 / 0 / 0 | 278: admitted item_33 | item_33 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 021 | through | on | s20_18 | 307-314 | 12.4 | 8 / 0 / 0 | 278: admitted item_33 | item_33 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 023 | none | on | s20_26 | 94-100 | 29.7 | 5 / 1 / 1 | 88: admitted item_32 | item_32 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 05 | 023 | none | on | s20_26 | 374-382 | 9.0 | 9 / 0 / 0 | 294: admitted item_33 | item_33 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 023 | none | off | s20_26 | 94-100 | 29.7 | 5 / 1 / 1 | 88: admitted item_32 | item_32 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 05 | 023 | none | off | s20_26 | 374-382 | 9.0 | 9 / 0 / 0 | 294: fallback moving k=27 | item_33 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 023 | accord | on | s20_28 | 94-100 | 29.7 | 5 / 1 / 1 | 88: admitted item_32 | item_32 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 05 | 023 | accord | on | s20_28 | 374-382 | 9.0 | 9 / 0 / 0 | 294: admitted item_33 | item_33 |  | standing: the robot standing (not robot-responsible under F1) |
| 05 | 023 | through | on | s20_30 | 94-100 | 29.7 | 5 / 1 / 1 | 88: admitted item_32 | item_32 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 05 | 023 | through | on | s20_30 | 374-382 | 9.0 | 9 / 0 / 0 | 294: admitted item_33 | item_33 |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 024 | accord | off | s03_06 | 57-58 | 48.2 | 0 / 1 / 1 | 57: fallback moving k=2 | item_2 |  | off only (a gain on): scenario_s03_06's recorded meeting with the departing human on a moving fallback; on, the earlier admission of the deliveries shifts the robot's timeline and the case does not form |
| 06 | 025 | none | on | s21_07 | 134-137 | 34.4 | 3 / 0 / 1 | 133: fallback moving k=11 | unmodelled |  | the same case on both sides, a tick apart: the exit walk passes the robot resting on a moving fallback |
| 06 | 025 | none | off | s21_07 | 57-58 | 48.2 | 0 / 1 / 1 | 57: fallback moving k=2 | item_2 |  | off only (a gain on): as script 024: the robot meets the departing human on a moving fallback; on, the case does not form |
| 06 | 025 | none | off | s21_07 | 133-136 | 33.9 | 3 / 0 / 1 | 133: fallback moving k=11 | unmodelled |  | the same case on both sides, a tick apart: the exit walk passes the robot resting on a moving fallback |
| 06 | 025 | through | on | s21_09 | 134-137 | 34.4 | 3 / 0 / 1 | 133: fallback moving k=11 | unmodelled |  | the same case on both sides, a tick apart: the exit walk passes the robot resting on a moving fallback |
| 06 | 028 | none | on | s21_23 | 54-59 | 11.4 | 2 / 1 / 3 | 14: admitted item_3 | item_3 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 06 | 028 | none | off | s21_23 | 54-59 | 11.4 | 2 / 1 / 3 | 15: admitted item_3 | item_3 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 06 | 028 | accord | on | s21_25 | 54-59 | 11.4 | 2 / 1 / 3 | 14: admitted item_3 | item_3 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 06 | 028 | through | on | s21_27 | 54-59 | 11.4 | 2 / 1 / 3 | 16: admitted item_3 | item_3 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 06 | 030 | none | on | s22_02 | 150-157 | 12.1 | 8 / 0 / 0 | 120: admitted item_42 | item_42 |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 030 | none | on | s22_02 | 235-241 | 14.9 | 7 / 0 / 0 | 120: admitted item_42 | item_43 | yes | standing: the robot standing (not robot-responsible under F1) |
| 06 | 030 | none | off | s22_02 | 150-157 | 12.1 | 8 / 0 / 0 | 120: admitted item_42 | item_42 |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 030 | none | off | s22_02 | 235-241 | 14.9 | 7 / 0 / 0 | 120: admitted item_42 | item_43 | yes | standing: the robot standing (not robot-responsible under F1) |
| 06 | 030 | through | on | s22_04 | 150-157 | 12.1 | 8 / 0 / 0 | 120: admitted item_42 | item_42 |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 030 | through | on | s22_04 | 235-241 | 14.9 | 7 / 0 / 0 | 120: admitted item_42 | item_43 | yes | standing: the robot standing (not robot-responsible under F1) |
| 06 | 031 | none | on | s22_06 | 207-213 | 20.3 | 7 / 0 / 0 | 119: fallback moving k=23 | item_41 |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 031 | none | on | s22_06 | 288-293 | 12.0 | 6 / 0 / 0 | 119: fallback moving k=23 | unmodelled |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 031 | none | off | s22_06 | 207-213 | 20.3 | 7 / 0 / 0 | 120: admitted coffee_break | item_41 | yes | standing: the robot standing (not robot-responsible under F1) |
| 06 | 031 | none | off | s22_06 | 288-293 | 12.0 | 6 / 0 / 0 | 120: admitted coffee_break | unmodelled | yes | standing: the robot standing (not robot-responsible under F1) |
| 06 | 031 | accord | on | s22_08 | 207-213 | 20.3 | 7 / 0 / 0 | 120: admitted coffee_break | item_41 | yes | standing: the robot standing (not robot-responsible under F1) |
| 06 | 031 | accord | on | s22_08 | 288-293 | 12.0 | 6 / 0 / 0 | 120: admitted coffee_break | unmodelled | yes | standing: the robot standing (not robot-responsible under F1) |
| 06 | 031 | through | on | s22_10 | 207-213 | 20.3 | 7 / 0 / 0 | 119: fallback moving k=23 | item_41 |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 031 | through | on | s22_10 | 288-293 | 12.0 | 6 / 0 / 0 | 119: fallback moving k=23 | unmodelled |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 032 | none | on | s22_12 | 168-176 | 9.8 | 9 / 0 / 0 | 136: admitted item_41 | item_41 |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 032 | none | off | s22_12 | 168-176 | 9.8 | 9 / 0 / 0 | 136: admitted item_41 | item_41 |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 032 | accord | on | s22_14 | 168-176 | 9.8 | 9 / 0 / 0 | 136: admitted item_41 | item_41 |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 032 | through | on | s22_16 | 168-176 | 9.8 | 9 / 0 / 0 | 136: admitted item_41 | item_41 |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 033 | none | on | s22_18 | 145-174 | 6.3 | 30 / 0 / 0 | 120: admitted item_43 | item_43 |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 033 | none | on | s22_18 | 250-254 | 12.2 | 5 / 0 / 0 | 120: admitted item_43 | unmodelled | yes | standing: the robot standing (not robot-responsible under F1) |
| 06 | 033 | none | off | s22_18 | 145-174 | 6.3 | 30 / 0 / 0 | 120: admitted item_43 | item_43 |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 033 | none | off | s22_18 | 250-254 | 12.2 | 5 / 0 / 0 | 120: admitted item_43 | unmodelled | yes | standing: the robot standing (not robot-responsible under F1) |
| 06 | 033 | accord | on | s22_20 | 145-174 | 6.3 | 30 / 0 / 0 | 120: admitted item_43 | item_43 |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 033 | accord | on | s22_20 | 250-254 | 12.2 | 5 / 0 / 0 | 120: admitted item_43 | unmodelled | yes | standing: the robot standing (not robot-responsible under F1) |
| 06 | 033 | through | on | s22_22 | 145-174 | 6.3 | 30 / 0 / 0 | 120: admitted item_43 | item_43 |  | standing: the robot standing (not robot-responsible under F1) |
| 06 | 033 | through | on | s22_22 | 250-254 | 12.2 | 5 / 0 / 0 | 120: admitted item_43 | unmodelled | yes | standing: the robot standing (not robot-responsible under F1) |
| 06 | 034 | none | on | s22_24 | 55-59 | 3.5 | 4 / 0 / 1 | 50: admitted item_43 | item_43 |  | the same case on both sides, a tick apart: the human passes the robot standing at kitting_table_0 (one receding tick) |
| 06 | 034 | none | on | s22_24 | 136-136 | 49.4 | 0 / 1 / 0 | 136: fallback moving k=2 | unmodelled |  | the same on both sides: not a context effect; decision in force: a fallback |
| 06 | 034 | none | off | s22_24 | 54-58 | 1.4 | 4 / 0 / 1 | 54: admitted item_43 | item_43 |  | the same case on both sides, a tick apart: the human passes the robot standing at kitting_table_0 (one receding tick) |
| 06 | 034 | none | off | s22_24 | 136-136 | 49.4 | 0 / 1 / 0 | 136: fallback moving k=2 | unmodelled |  | the same on both sides: not a context effect; decision in force: a fallback |
| 06 | 034 | through | on | s22_26 | 55-59 | 3.5 | 4 / 0 / 1 | 50: admitted item_43 | item_43 |  | the same case on both sides, a tick apart: the human passes the robot standing at kitting_table_0 (one receding tick) |
| 06 | 034 | through | on | s22_26 | 136-136 | 49.4 | 0 / 1 / 0 | 136: fallback moving k=2 | unmodelled |  | the same on both sides: not a context effect; decision in force: a fallback |
| 07 | 035 | through | on | s23_06 | 27-31 | 30.0 | 0 / 3 / 2 | 0: admitted item_5 | coffee_break | yes | wrong admission (limitation, docs/assumptions.md 6.4): deliver_item(item_5) admitted at 0 while the human walks to the coffee machine, which stands 100 cm short of shelf_5 on the same bearing (a near-tie for 24 ticks; the prior picks the assigned delivery); the robot, its plan resting on the delivery, walks down x = 0 and passes the human standing at the machine (off: fallbacks, a hold at 24, 58 cm) |
| 07 | 035 | through | on | s23_07 | 27-31 | 30.0 | 0 / 3 / 2 | 0: admitted item_5 | coffee_break | yes | wrong admission (limitation, docs/assumptions.md 6.4): deliver_item(item_5) admitted at 0 while the human walks to the coffee machine, which stands 100 cm short of shelf_5 on the same bearing (a near-tie for 24 ticks; the prior picks the assigned delivery); the robot, its plan resting on the delivery, walks down x = 0 and passes the human standing at the machine (off: fallbacks, a hold at 24, 58 cm) |
| 07 | 035 | none | on | s05_01 | 27-31 | 30.0 | 0 / 3 / 2 | 0: admitted item_5 | coffee_break | yes | wrong admission (limitation, docs/assumptions.md 6.4): deliver_item(item_5) admitted at 0 while the human walks to the coffee machine, which stands 100 cm short of shelf_5 on the same bearing (a near-tie for 24 ticks; the prior picks the assigned delivery); the robot, its plan resting on the delivery, walks down x = 0 and passes the human standing at the machine (off: fallbacks, a hold at 24, 58 cm) |
| 07 | 035 | none | on | s05_02 | 27-31 | 30.0 | 0 / 3 / 2 | 0: admitted item_5 | coffee_break | yes | wrong admission (limitation, docs/assumptions.md 6.4): deliver_item(item_5) admitted at 0 while the human walks to the coffee machine, which stands 100 cm short of shelf_5 on the same bearing (a near-tie for 24 ticks; the prior picks the assigned delivery); the robot, its plan resting on the delivery, walks down x = 0 and passes the human standing at the machine (off: fallbacks, a hold at 24, 58 cm) |
| 07 | 037 | none | on | s23_15 | 213-220 | 14.8 | 8 / 0 / 0 | 173: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 037 | none | off | s23_15 | 213-220 | 14.8 | 8 / 0 / 0 | 173: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 037 | accord | on | s23_17 | 213-220 | 14.8 | 8 / 0 / 0 | 173: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 037 | through | on | s23_19 | 213-220 | 14.8 | 8 / 0 / 0 | 173: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 038 | none | on | s23_21 | 52-56 | 19.3 | 0 / 3 / 2 | 36: admitted item_5 | coffee_break | yes | limitation (an admitted task cut by a foreseeable task inside it): deliver_item(item_5) admitted at 36, rightly (the human walks to shelf_5; off still below θ); at the shelf the human steps to the coffee machine beside it, onto the robot's route, and the robot's plan still rests on the delivery (the record kept until the trigger rule fires: question G's reading) |
| 07 | 038 | none | on | s23_21 | 210-214 | 45.7 | 5 / 0 / 0 | 181: admitted item_2 | item_2 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 038 | none | off | s23_21 | 210-214 | 45.7 | 5 / 0 / 0 | 174: admitted item_2 | item_2 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 038 | through | on | s23_25 | 52-56 | 19.3 | 0 / 3 / 2 | 36: admitted item_5 | coffee_break | yes | limitation (an admitted task cut by a foreseeable task inside it): deliver_item(item_5) admitted at 36, rightly (the human walks to shelf_5; off still below θ); at the shelf the human steps to the coffee machine beside it, onto the robot's route, and the robot's plan still rests on the delivery (the record kept until the trigger rule fires: question G's reading) |
| 07 | 038 | through | on | s23_25 | 210-214 | 45.7 | 5 / 0 / 0 | 181: admitted item_2 | item_2 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 040 | none | on | s23_31 | 186-190 | 41.4 | 5 / 0 / 0 | 174: admitted item_5 | item_5 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 040 | none | off | s23_31 | 186-190 | 41.4 | 5 / 0 / 0 | 174: admitted item_5 | item_5 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 040 | through | on | s23_33 | 186-190 | 41.4 | 5 / 0 / 0 | 174: admitted item_5 | item_5 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 040 | through_rw | on | s23_35 | 186-190 | 41.4 | 5 / 0 / 0 | 174: admitted item_5 | item_5 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 041 | none | on | s24_02 | 118-123 | 5.7 | 6 / 0 / 0 | 94: admitted item_53 | item_53 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 041 | none | on | s24_02 | 157-161 | 5.7 | 4 / 0 / 1 | 94: admitted item_53 | item_53 |  | the same case on both sides, six ticks apart: the human at shelf_3, the robot standing there for its item_55 (one receding tick) |
| 07 | 041 | none | off | s24_02 | 124-129 | 4.0 | 6 / 0 / 0 | 100: admitted item_53 | item_53 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 041 | none | off | s24_02 | 151-155 | 4.0 | 4 / 0 / 1 | 100: admitted item_53 | item_53 |  | the same case on both sides, six ticks apart: the human at shelf_3, the robot standing there for its item_55 (one receding tick) |
| 07 | 041 | through | on | s24_04 | 118-123 | 5.7 | 6 / 0 / 0 | 94: admitted item_53 | item_53 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 041 | through | on | s24_04 | 157-161 | 5.7 | 4 / 0 / 1 | 94: admitted item_53 | item_53 |  | the same case on both sides, six ticks apart: the human at shelf_3, the robot standing there for its item_55 (one receding tick) |
| 07 | 041 | through_rw | on | s24_06 | 118-123 | 5.7 | 6 / 0 / 0 | 94: admitted item_53 | item_53 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 041 | through_rw | on | s24_06 | 157-161 | 5.7 | 4 / 0 / 1 | 94: admitted item_53 | item_53 |  | the same case on both sides, six ticks apart: the human at shelf_3, the robot standing there for its item_55 (one receding tick) |
| 07 | 042 | none | on | s24_08 | 147-151 | 4.1 | 3 / 1 / 1 | 145: fallback standing k=2 | coffee_break |  | the same case on both sides, a tick apart: the human arrives at the coffee machine beside the robot standing on its route (one receding tick) |
| 07 | 042 | none | off | s24_08 | 147-151 | 4.1 | 3 / 1 / 1 | 145: fallback standing k=2 | coffee_break |  | the same case on both sides, a tick apart: the human arrives at the coffee machine beside the robot standing on its route (one receding tick) |
| 07 | 042 | accord | on | s24_10 | 148-152 | 3.9 | 4 / 0 / 1 | 147: admitted coffee_break | coffee_break |  | the same case on both sides, a tick apart: the human arrives at the coffee machine beside the robot standing on its route (one receding tick) |
| 07 | 042 | through | on | s24_12 | 147-151 | 4.1 | 3 / 1 / 1 | 145: fallback standing k=2 | coffee_break |  | the same case on both sides, a tick apart: the human arrives at the coffee machine beside the robot standing on its route (one receding tick) |
| 07 | 043 | none | on | s24_14 | 86-90 | 35.2 | 5 / 0 / 0 | 85: admitted item_52 | item_52 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 043 | none | off | s24_14 | 86-90 | 35.2 | 5 / 0 / 0 | 85: admitted item_52 | item_52 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 043 | none | off | s24_14 | 268-273 | 28.4 | 4 / 2 / 0 | 191: admitted item_53 | item_53 |  | off only (a gain on): the robot moving past the human at kitting_table_0 on the admitted item_53; on, the robot's earlier decisions differ and the case does not form |
| 07 | 043 | accord | on | s24_16 | 86-90 | 35.2 | 5 / 0 / 0 | 85: admitted item_52 | item_52 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 043 | through | on | s24_18 | 86-90 | 35.2 | 5 / 0 / 0 | 85: admitted item_52 | item_52 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 044 | none | on | s24_20 | 308-314 | 26.6 | 7 / 0 / 0 | 263: fallback moving k=90 | item_51 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 044 | none | off | s24_20 | 308-314 | 26.6 | 7 / 0 / 0 | 263: fallback moving k=90 | item_51 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 044 | through | on | s24_22 | 308-314 | 26.6 | 7 / 0 / 0 | 263: fallback moving k=90 | item_51 |  | standing: the robot standing (not robot-responsible under F1) |
| 07 | 044 | through_rw | on | s24_24 | 308-314 | 26.6 | 7 / 0 / 0 | 263: fallback moving k=90 | item_51 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 046 | none | on | s25_02 | 175-181 | 40.3 | 7 / 0 / 0 | 124: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 046 | none | off | s25_02 | 175-181 | 40.3 | 7 / 0 / 0 | 124: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 046 | through | on | s25_04 | 175-181 | 40.3 | 7 / 0 / 0 | 124: admitted item_3 | item_3 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 047 | none | on | s25_06 | 180-188 | 13.2 | 9 / 0 / 0 | 60: admitted item_3 | item_4 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 047 | none | off | s25_06 | 180-188 | 13.2 | 9 / 0 / 0 | 60: admitted item_3 | item_4 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 047 | through | on | s25_08 | 180-188 | 13.2 | 9 / 0 / 0 | 60: admitted item_3 | item_4 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 050 | none | on | s25_22 | 271-277 | 31.6 | 7 / 0 / 0 | 76: fallback moving k=45 | item_0 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 050 | none | off | s25_22 | 271-277 | 31.6 | 7 / 0 / 0 | 76: fallback moving k=45 | item_0 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 050 | accord | on | s25_24 | 271-277 | 31.6 | 7 / 0 / 0 | 76: fallback moving k=45 | item_0 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 050 | through | on | s25_26 | 271-277 | 31.6 | 7 / 0 / 0 | 76: fallback moving k=45 | item_0 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 052 | none | on | s25_34 | 163-168 | 8.0 | 6 / 0 / 0 | 152: admitted item_5 | item_5 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 052 | none | on | s25_34 | 190-197 | 29.5 | 8 / 0 / 0 | 152: admitted item_5 | item_5 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 052 | none | off | s25_34 | 163-168 | 8.0 | 6 / 0 / 0 | 152: admitted item_5 | item_5 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 052 | none | off | s25_34 | 190-197 | 29.5 | 8 / 0 / 0 | 152: admitted item_5 | item_5 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 052 | accord | on | s25_36 | 163-168 | 8.0 | 6 / 0 / 0 | 152: admitted item_5 | item_5 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 052 | accord | on | s25_36 | 190-197 | 29.5 | 8 / 0 / 0 | 152: admitted item_5 | item_5 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 052 | through | on | s25_38 | 163-168 | 8.0 | 6 / 0 / 0 | 152: admitted item_5 | item_5 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 052 | through | on | s25_38 | 190-197 | 29.5 | 8 / 0 / 0 | 152: admitted item_5 | item_5 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 054 | none | on | s25_44 | 193-198 | 41.0 | 6 / 0 / 0 | 113: admitted coffee_break | item_5 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 054 | none | off | s25_44 | 193-198 | 41.0 | 6 / 0 / 0 | 113: admitted coffee_break | item_5 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 054 | accord | on | s25_46 | 193-198 | 41.0 | 6 / 0 / 0 | 113: admitted coffee_break | item_5 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 054 | through | on | s25_48 | 193-198 | 41.0 | 6 / 0 / 0 | 113: admitted coffee_break | item_5 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 055 | none | on | s25_50 | 242-247 | 37.5 | 6 / 0 / 0 | 89: fallback moving k=12 | item_2 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 055 | none | off | s25_50 | 242-247 | 37.5 | 6 / 0 / 0 | 89: fallback moving k=12 | item_2 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 055 | through | on | s25_52 | 242-247 | 37.5 | 6 / 0 / 0 | 89: fallback moving k=12 | item_2 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 057 | none | on | s26_06 | 236-243 | 11.3 | 8 / 0 / 0 | 164: admitted item_21 | item_21 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 057 | none | on | s26_06 | 443-451 | 2.7 | 9 / 0 / 0 | 164: admitted item_21 | item_22 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 057 | none | off | s26_06 | 236-243 | 11.3 | 8 / 0 / 0 | 164: admitted item_21 | item_21 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 057 | none | off | s26_06 | 443-451 | 2.7 | 9 / 0 / 0 | 164: admitted item_21 | item_22 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 057 | through | on | s26_08 | 236-243 | 11.3 | 8 / 0 / 0 | 164: admitted item_21 | item_21 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 057 | through | on | s26_08 | 443-451 | 2.7 | 9 / 0 / 0 | 164: admitted item_21 | item_22 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 059 | none | on | s26_16 | 288-298 | 8.4 | 11 / 0 / 0 | 288: admitted item_27 | item_27 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 059 | none | off | s26_16 | 288-298 | 8.4 | 11 / 0 / 0 | 288: admitted item_27 | item_27 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 059 | accord | on | s26_18 | 288-298 | 8.4 | 11 / 0 / 0 | 288: admitted item_27 | item_27 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 059 | through | on | s26_20 | 288-298 | 8.4 | 11 / 0 / 0 | 288: admitted item_27 | item_27 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 060 | none | on | s26_22 | 316-324 | 11.2 | 9 / 0 / 0 | 252: admitted item_20 | item_20 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 060 | none | off | s26_22 | 316-324 | 11.2 | 9 / 0 / 0 | 252: admitted item_20 | item_20 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 060 | accord | on | s26_24 | 316-324 | 11.2 | 9 / 0 / 0 | 252: admitted item_20 | item_20 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 060 | through | on | s26_26 | 316-324 | 11.2 | 9 / 0 / 0 | 252: admitted item_20 | item_20 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 064 | none | on | s26_42 | 356-364 | 0.2 | 9 / 0 / 0 | 269: admitted item_22 | item_22 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 064 | none | off | s26_42 | 356-364 | 0.2 | 9 / 0 / 0 | 269: admitted item_22 | item_22 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 064 | accord | on | s26_44 | 356-364 | 0.2 | 9 / 0 / 0 | 269: admitted item_22 | item_22 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 064 | through | on | s26_46 | 356-364 | 0.2 | 9 / 0 / 0 | 268: admitted item_22 | item_22 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 065 | none | on | s26_48 | 180-185 | 23.1 | 2 / 2 / 2 | 72: admitted item_20 | item_20 |  | other, deeper on: the human arrives at kitting_table_1 beside the robot holding there (both sides); on, a recognition_changed at 183 ends the hold a tick early and the robot moves off past the human (23.1 cm; off 32.0 cm, the hold completed) |
| 19 | 065 | none | on | s26_48 | 281-289 | 3.6 | 9 / 0 / 0 | 258: admitted item_24 | item_24 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 065 | none | off | s26_48 | 180-185 | 32.0 | 3 / 2 / 1 | 72: admitted item_20 | item_20 |  | other, deeper on: the human arrives at kitting_table_1 beside the robot holding there (both sides); on, a recognition_changed at 183 ends the hold a tick early and the robot moves off past the human (23.1 cm; off 32.0 cm, the hold completed) |
| 19 | 065 | none | off | s26_48 | 281-289 | 3.6 | 9 / 0 / 0 | 259: admitted item_24 | item_24 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 065 | accord | on | s26_50 | 180-185 | 23.1 | 2 / 2 / 2 | 72: admitted item_20 | item_20 |  | other, deeper on: the human arrives at kitting_table_1 beside the robot holding there (both sides); on, a recognition_changed at 183 ends the hold a tick early and the robot moves off past the human (23.1 cm; off 32.0 cm, the hold completed) |
| 19 | 065 | accord | on | s26_50 | 281-289 | 3.6 | 9 / 0 / 0 | 258: admitted item_24 | item_24 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 065 | through | on | s26_52 | 180-185 | 23.1 | 2 / 2 / 2 | 72: admitted item_20 | item_20 |  | other, deeper on: the human arrives at kitting_table_1 beside the robot holding there (both sides); on, a recognition_changed at 183 ends the hold a tick early and the robot moves off past the human (23.1 cm; off 32.0 cm, the hold completed) |
| 19 | 065 | through | on | s26_52 | 281-289 | 3.6 | 9 / 0 / 0 | 258: admitted item_24 | item_24 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 068 | none | on | s27_10 | 246-252 | 25.6 | 7 / 0 / 0 | 153: admitted item_33 | item_36 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 068 | none | off | s27_10 | 246-252 | 25.6 | 7 / 0 / 0 | 153: admitted item_33 | item_36 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 068 | through | on | s27_12 | 246-252 | 25.6 | 7 / 0 / 0 | 153: admitted item_33 | item_36 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 069 | none | on | s27_14 | 197-203 | 40.0 | 7 / 0 / 0 | 98: fallback standing k=7 | item_39 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 069 | none | off | s27_14 | 197-203 | 40.0 | 7 / 0 / 0 | 99: admitted coffee_break | item_39 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 069 | accord | on | s27_16 | 197-203 | 40.0 | 7 / 0 / 0 | 99: admitted coffee_break | item_39 | yes | standing: the robot standing (not robot-responsible under F1) |
| 19 | 069 | through | on | s27_18 | 197-203 | 40.0 | 7 / 0 / 0 | 98: fallback standing k=7 | item_39 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 070 | none | on | s27_20 | 292-299 | 20.9 | 8 / 0 / 0 | 67: fallback moving k=30 | item_32 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 070 | none | off | s27_20 | 292-299 | 20.9 | 8 / 0 / 0 | 67: fallback moving k=30 | item_32 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 070 | accord | on | s27_22 | 292-299 | 20.9 | 8 / 0 / 0 | 67: fallback moving k=30 | item_32 |  | standing: the robot standing (not robot-responsible under F1) |
| 19 | 070 | through | on | s27_24 | 292-299 | 20.9 | 8 / 0 / 0 | 67: fallback moving k=30 | item_32 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 076 | none | on | s28_02 | 140-146 | 2.5 | 4 / 1 / 2 | 139: admitted item_3 | item_3 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 20 | 076 | none | off | s28_02 | 140-146 | 2.5 | 4 / 1 / 2 | 139: admitted item_3 | item_3 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 20 | 076 | through | on | s28_04 | 140-146 | 2.5 | 4 / 1 / 2 | 139: admitted item_3 | item_3 |  | the same on both sides: not a context effect; decision in force: the true task admitted |
| 20 | 078 | none | on | s28_10 | 249-253 | 35.4 | 5 / 0 / 0 | 100: admitted item_2 | item_1 | yes | standing: the robot standing (not robot-responsible under F1) |
| 20 | 078 | none | off | s28_10 | 249-253 | 35.4 | 5 / 0 / 0 | 100: admitted item_2 | item_1 | yes | standing: the robot standing (not robot-responsible under F1) |
| 20 | 078 | accord | on | s28_12 | 249-253 | 35.4 | 5 / 0 / 0 | 100: admitted item_2 | item_1 | yes | standing: the robot standing (not robot-responsible under F1) |
| 20 | 078 | through | on | s28_14 | 249-253 | 35.4 | 5 / 0 / 0 | 100: admitted item_2 | item_1 | yes | standing: the robot standing (not robot-responsible under F1) |
| 20 | 081 | none | on | s28_28 | 217-224 | 17.9 | 8 / 0 / 0 | 103: fallback moving k=11 | item_1 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 081 | none | off | s28_28 | 217-224 | 17.9 | 8 / 0 / 0 | 103: fallback moving k=11 | item_1 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 081 | accord | on | s28_30 | 217-224 | 17.9 | 8 / 0 / 0 | 103: fallback moving k=11 | item_1 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 082 | none | on | s28_32 | 201-207 | 30.1 | 7 / 0 / 0 | 145: admitted item_7 | item_7 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 082 | none | off | s28_32 | 201-207 | 30.1 | 7 / 0 / 0 | 145: admitted item_7 | item_7 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 082 | accord | on | s28_34 | 201-207 | 30.1 | 7 / 0 / 0 | 145: admitted item_7 | item_7 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 082 | through | on | s28_36 | 201-207 | 30.1 | 7 / 0 / 0 | 145: admitted item_7 | item_7 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 093 | none | on | s29_40 | 238-244 | 24.3 | 7 / 0 / 0 | 186: admitted item_65 | item_65 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 093 | none | off | s29_40 | 238-244 | 24.3 | 7 / 0 / 0 | 186: admitted item_65 | item_65 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 093 | through | on | s29_42 | 238-244 | 24.3 | 7 / 0 / 0 | 186: admitted item_65 | item_65 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 097 | none | on | s30_06 | 324-332 | 4.0 | 9 / 0 / 0 | 147: fallback moving k=51 | item_75 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 097 | none | off | s30_06 | 324-332 | 4.0 | 9 / 0 / 0 | 147: fallback moving k=51 | item_75 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 097 | through | on | s30_08 | 324-332 | 4.0 | 9 / 0 / 0 | 147: fallback moving k=51 | item_75 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 099 | none | on | s30_16 | 198-204 | 26.6 | 7 / 0 / 0 | 164: admitted item_75 | item_75 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 099 | none | off | s30_16 | 198-204 | 26.6 | 7 / 0 / 0 | 164: admitted item_75 | item_75 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 099 | accord | on | s30_18 | 198-204 | 26.6 | 7 / 0 / 0 | 164: admitted item_75 | item_75 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 099 | through | on | s30_20 | 198-204 | 26.6 | 7 / 0 / 0 | 164: admitted item_75 | item_75 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 105 | none | on | s30_46 | 182-189 | 20.5 | 8 / 0 / 0 | 109: admitted item_71 | item_71 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 105 | none | off | s30_46 | 182-189 | 20.5 | 8 / 0 / 0 | 109: admitted item_71 | item_71 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 105 | accord | on | s30_48 | 182-189 | 20.5 | 8 / 0 / 0 | 109: admitted item_71 | item_71 |  | standing: the robot standing (not robot-responsible under F1) |
| 20 | 105 | through | on | s30_50 | 182-189 | 20.5 | 8 / 0 / 0 | 109: admitted item_71 | item_71 |  | standing: the robot standing (not robot-responsible under F1) |
