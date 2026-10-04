# T-K part 1, step 4: context knowledge off against on (the IRB on env_layout_15, _16, _17, robot idle)

Stage 3 (4 October 2026). The set, its states and its expectations: `README.md` (stages 1 and 2). The tables here are
read from `actual.csv` by `offon.py` and `directions.py`; they equal the same tables read from `expected.csv`.

## The runs

- 57 runs with context knowledge on (the 31 scripts of round 1 under the default timeline or 3A, and the 26 new
  scenarios), and the 2 new scripts (P7 s13_15, P9 s15_21) with it off. Every run agrees with the oracle: 0
  disagreements at 1e-9 against `actual.csv`; the trajectory equals the run's human lines on every tick; the in-process
  lines equal the log's. Against the log's print precision, one disagreement in s14_02, s14_12, s14_13, s14_14 (one
  script): tick 181, the A/C's adequacy, round 1's known flag. The expectations' md5s are unchanged by the runs.
- The off side of every case is round 1's run of the same script (rerun at stage 2), or `off/` for P7 and P9.
- Kinds of comparison (Hadi, stage 3): "within" = one script (off against on, or the same script under different
  timelines); "across" = different scripts. Every verdict below is drawn from within-script comparisons. The sides:
  off; on without the raising fact for the case's foreseeable task; on with it.

## The measure per case (the foreseeable task; the deliveries are in the appendices)

θ / admitted: the first tick at θ and the first tick the gate clears for the true task, off → on. "Live": deliveries
live at the stretch's start. The state is the true task's level on its ticks (on).

| case | scenario | state (on) | live | θ off → on | admitted off → on | after admission (on) |
|---|---|---|---|---|---|---|
| default, break before the window | s13_02, s15_02 | ordinary | 3 | 101 → 117; 103 → 117 | same | - |
| 〃 inside the 2nd delivery | s13_05, s15_05 | ordinary | 3 | 103 → 120; 104 → 120 | same | - |
| 〃 | s13_06, s15_06 | ordinary | 3 | 104 → 112 | same | - |
| 〃 | s14_02, s14_04, s14_05 | ordinary | 2 | 143 → 157; 149 → 162; 150 → 163 | same | - |
| default, window opens in the wait | s13_03, s15_03 | ordinary to θ, raised from 178 | 2 | 158 → 175; 160 → 176 | same | - |
| 〃 (inside the 2nd delivery) | s13_07, s15_07 | 〃 | 3 | 153 → 160 | 163 → 163 | - |
| default, break inside the window | s13_04, s15_04 | raised | 1 | 249 → 238; 252 → 238 | same | - |
| 〃 | s14_03 | raised | 1 | 235 → 226 | same | - |
| 〃 (inside the 2nd delivery) | s14_06 | raised | 2 | 231 → 224 | 231 → 225 | - |
| 3B, edge before leaving | s13_08; s14_12 | raised | 3; 2 | 101 → 82; 143 → 129 | same | - |
| 3B, edge in the walk | s13_09 (90); s14_13 (110) | ordinary → raised | 3; 2 | 101 → 90; 143 → 129 | same | - |
| 3B, edge in the wait | s13_10 (120); s14_14 (150) | ordinary → raised | 3; 2 | 101 → 117; 143 → 150 | same | - |
| 3D, window closes in the wait | s13_11 (190) | raised → ordinary | 2 | 158 → 138 | same | - |
| 3D, window closes in the walk | s13_12 (150) | raised → ordinary | 2 | 158 → 138 | same | 150 to 174 not clearing (item_4 admitted 150 to 161) |
| 3D, window closes in the wait | s14_18 (250) | raised → ordinary | 1 | 235 → 226 | same | 250 to 251 below θ |
| 3E, no fact | s13_13; s14_19 | ordinary | 1 | 249 → 271; 235 → 252 | same | - |
| 3F, both facts | s15_17 | raised (A/C raised) | 1 | 252 → 243 | same | - |
| P7, break inside the lone delivery | s13_15 | ordinary | 1 | 274 → 291 | 277 → 291 | - |
| P9, no delivery live | s15_21 | raised | 0 | 334 → 309 | 334 → 309 | - |

The A/C activation is never admitted (its wait is one tick) except in s15_12 and s15_13 (133 and 166, off and on);
its belief at arrival:

| script (live at arrival) | off | on, A/C ordinary at arrival | on, A/C raised at arrival |
|---|---|---|---|
| s15_08 (3) | 0.6238 | 0.0914 (s15_08 3A, s15_16 "0 to 90") | 0.7154 (s15_14 "from 50", s15_15 "from 90") |
| s14_07 (2) | 0.4626 | 0.0599 (s14_07 3A, s14_17 "0 to 110") | 0.6144 (s14_15, s14_16) |
| s15_10 (1) | 0.7487 | 0.0574 (s15_19 P4, empty) | 0.6035 (s15_10 3A); 0.5932 (s15_20 P6, coffee raised too) |
| s14_08 (1) | 0.5475 | 0.0142 (s14_21 P5: coffee raised) | 0.6449 (s14_08 3A) |
| s14_09, s14_10 (2) | 0.4456, 0.4814 | 0.0467, 0.0558 | not in the set |
| s15_11, s15_12 (3) | 0.7468, 0.9961 | 0.1516, 0.9875 | not in the set |
| s14_11 (2), s15_09 (2), s15_13 (3) | 0.4351, 0.6130, 0.9952 | not in the set | 0.5192, 0.6152, 0.9990 |

## The directions of point 5

1. **No raising fact.**
   - A lone delivery is admitted at its first observation: CONFIRMED, within one script against off, 38 of 38
     stretches (1 live), each admitted on its stretch's first tick (the gate refuses only on the previous task's pin
     tick); off 5 to 51 ticks later. Against on with a raising fact (within): s14_08 / s14_21, s15_04 / s15_17,
     s15_10 / s15_20: 0 against 15, 20, 19 (direction 2's pairs).
   - A retraction follows if the human then takes the break: CONFIRMED within, all three sides: s13_04's script
     (s13_13 on, empty: item_4 admitted 216 to 258, retraction at 259, inadequate at the machine; s13_04 on with
     break_time and off: no early admission); s14_03's (s14_19: 180 to 239, retraction at 240, below θ; s14_03, s14_18
     and off: none). With the A/C (P4, s15_19): item_4 stays admitted through the whole walk to the switch, 216 to 261,
     and the gate stops only on the A/C's completion (262, no observation): no retraction by the movement, since the
     switch stands beside shelf_4. With a correct early admission cut by the break (P7, s13_15): item_4 admitted at
     217, retracted at 270 (inadequate, the break begun at 261); off it is admitted at 248 and lost at 269.
   - Several live, the deliveries come no later: CONFIRMED within against off, 143 stretches, none later: 2 live 38
     earlier and 12 equal, 3 live 50 and 10, 4 live 19 and 14.
   - The break later: CONFIRMED within against off, 15 of 17 later (1 live 3, 2 live 5, 3 live 7); 2 equal (s13_07,
     s15_07, 3 live: the break begun after the carry, admitted on adequacy at 163 in both).
   - The A/C's belief at its arrival lower: CONFIRMED within against off, 10 of 10 (table above; 1 to 3 live; 0.46 →
     0.06 at 2 live, 0.62 → 0.09 at 3 live, 0.75 → 0.06 at 1 live). s15_12: 0.9961 → 0.9875, the movement already
     decisive.
2. **break_time.**
   - The coffee break reaches the threshold earlier: CONFIRMED within against both sides. Against off: 10 of 10
     raised throughout (0 live 1, 1 live 5, 2 live 3, 3 live 1). Against on without the fact: 7 of 7 pairs (s13_08 /
     s13_02 and s13_10: 15 against 50; s13_11 / s13_03: 14 against 51; s13_04 / s13_13: 21 against 54; s14_12 /
     s14_02: 40 against 68; s14_03 and s14_18 / s14_19: 45 against 71). No on side without the fact in the set for
     s14_06, s15_04, s15_17 (one script each), s15_21. An edge after the threshold changes nothing (s13_10: 117 as
     without the fact); an edge late in the wait helps less than off (s14_14: 150 against off 143).
   - Not on the prior alone while a delivery is live: CONFIRMED. On the stretch's first tick the raised coffee break's
     belief (its prior) is 0.66 to 0.67 at 1 to 3 live, 0.57 with the A/C raised too (s15_17), below θ in all 11.
   - With none live it is, and only the observation rule delays it: CONFIRMED in its one case (P9, s15_21): 0.9903 on
     its first tick, admitted on that tick (the walk's first step gives the warrant at once), so the delay is 0; off
     334, 25 ticks later.
   - A delivery inside the window is admitted later: CONFIRMED within against on without the fact, 22 of 22 pairs
     (1 live 4, 2 live 5, 3 live 8, 4 live 5; the rival raised is the coffee break or the A/C). Against off, MIXED: 16
     later, 1 equal, 5 earlier. The 5 are in env_layout_16 and _17 with the A/C live: off gives the A/C the share of a
     delivery, 1/(n+2), and its switch stands beside shelf_1 and shelf_4; on gives it 0.02 (s15_01 and s15_18 item_4,
     1 live: off 45, on 37 and 39; s15_17 item_4: 23 → 20; s14_17 item_0 and s15_18 item_2, 3 live). Off is not a
     neutral side here (Hadi's addition). No on side without the fact for the last delivery of s13_01, s13_14, s14_01,
     s14_20, s15_01, s15_18 (1 live; the default window covers it).
3. **room_warm, the A/C off: its belief at its arrival higher.** CONFIRMED within against on without the fact: 4 of 4
   scripts (3 live 0.72 against 0.09; 2 live 0.61 against 0.06; 1 live 0.60 against 0.06; s14_08 0.64 against 0.014,
   where the side without also has break_time). Against off, CONTRADICTED in one script at 1 live: s15_10 0.60 and
   s15_20 0.59 against off 0.75 (off gives the lone delivery beside the switch and the A/C a third each; on, room_warm
   gives the A/C 0.5 against the delivery's 1, so the delivery takes two thirds of the prior). Confirmed against off in
   the other 6 cases (0.44 → 0.52 at 2 live, 0.46 → 0.61 at 2, 0.55 → 0.64 at 1, 0.62 → 0.72 at 3, 0.613 → 0.615 at 2,
   0.995 → 0.999 at 3). No on side without the fact for s14_11, s15_09, s15_13.
4. **After an observed break: suppressed for 90 ticks, inside break_time too.** CONFIRMED in all 31 observed
   completions: suppressed on every tick it is live within the 90 (88; it is retired on the completion tick and the
   next), inside break_time on 0 to 88 of them; on the 91st tick raised where break_time holds, ordinary otherwise. Its
   effect within one script: the lone delivery after the break is admitted on its first tick (s13_04 290 against off
   295; s14_03 260 against 269).
5. **At a window's edge inside an episode: the belief changes at that tick, and an admitted delivery can lose the
   threshold.** CONFIRMED, within one script (the edge table, appendix B). The belief of the true task changes on
   every edge tick. An admitted delivery loses θ on the tick the coffee break goes from suppressed to raised, the end
   of its recency fact inside break_time, in 5 cases, all with 1 live (s13_03 and s15_03 at 286, to 299; s14_02 at
   255, s14_04 at 263, s14_05 at 265; for 14 to 23 ticks). The opening of a window never made an admitted delivery
   lose θ (19 cases: break_time at 178 in ten, at 40 to 70 in five; room_warm at 50 to 70 in two, at 150 in two). The window's closing edge made an admitted coffee break
   lose θ twice (s13_12 at 150 in the walk: 0.85 → 0.06, item_4 admitted in its place 150 to 161; s14_18 at 250 in the
   wait: 0.99 → 0.70, 2 ticks). Edges also gave admissions on their tick (s13_09 at 90, s14_14 at 150, the last
   deliveries at 300).

## Admissions of a hypothesis that is not the true task (P8)

Appendix B, last table; per run off against on.
- The exit walk (unmodelled, no delivery live). env_layout_15: the same in all 15 (the coffee break is the only live
  hypothesis, so the prior cannot act; 309 to 330 and the like, retracted as inadequate). env_layout_16: none, off and
  on (the walk leads away from the cluster). env_layout_17: longer on where the A/C is on (coffee break 0.8: s15_08 to
  s15_16, s15_19, s15_20, from 10 to 11 ticks earlier: 369 against 379); shorter where the break is recent (s15_04: 378
  against 367 to 378); none on where room_warm raises the A/C that is still off (s15_17, s15_18; off 367 to 378 and 319
  to 330); none in P9, off and on. Every one is retracted as inadequate.
- During modelled tasks, on only (beyond the early lone admissions in 1):
  - a delivery admitted before a break begun inside it stays admitted a few ticks into the break, then is retracted
    (s13_05, s13_06, s15_05, s15_06, s14_04, s14_05 and with the A/C s14_09, s14_10, s15_11, s15_12; 1 to 13 ticks):
    off the same delivery had not reached θ before the break;
  - with break_time raised from the start (s13_11, s13_12, s13_14), the coffee break is admitted 81 to 91 while the
    human walks to shelf_2, its neighbour, retracted at 92 (below θ);
  - s13_03, s15_03: item_4 admitted 150 to 161 while the human walks to the machine (no fact holds), retracted at 162;
  - s14_21 (P5): the coffee break, raised, admitted 221 to 227 while the human walks to its neighbour, the A/C switch.
- Unchanged off and on: s13_07, s15_07, s13_15, s14_06, s14_11, s15_13 (a delivery admitted while a break inside it
  begins).
- One-tick admissions of the next lone delivery on the tick the true task is already complete and pinned (the human
  still on the place's last tick): 0 to 2 per run, on only. Not a retraction case.

## What surprised

- The window's position before the arrival does not change the belief at the arrival: s15_14 (from 50) and s15_15
  (from 90) give 0.7154, s14_15 and s14_16 give 0.6144, and the window closing before the arrival gives the ordinary
  value (s15_16 = s15_08). The prior is not folded into the evidence (R2), so the belief at a tick depends only on the
  facts at that tick. The same holds for the coffee break's admission once the edge is passed (s14_13's edge in the
  walk gives 129, as s14_12's raised from the start).
- With the A/C as the foreseeable task in a lone-delivery state (P4), the early admission of the delivery is never
  retracted by the movement: the switch stands beside shelf_4, and the gate stops only at the A/C's completion.
- The end of the recency fact, not the window's opening, is where admitted deliveries lose the threshold in this set.
- The early admission reaches several live deliveries too: a delivery reaches θ before the break begun inside it (3
  live), so the break now begins with a wrong admission that off did not have.
- Under break_time the coffee break is admitted wrongly while the human walks to the shelf beside the machine (s13_11,
  s13_12, s13_14), though its prior stays below θ.

## Flags

- The A/C's belief at arrival against off is lower with room_warm at 1 live (s15_10, s15_20): a finding against
  direction 3 read against off; within the script direction 3 holds. Suggest: read direction 3 against on without the
  fact, and state that off is no reference when a delivery's shelf stands beside the switch.
- P4: a delivery admitted early stays admitted through a whole foreseeable task whose target lies beside its own.
  Suggest: a case for the planning cases (step 5), since an admitted delivery is what the robot plans around.
- Missing sides, not added (Hadi): no on side without the fact for the coffee break of s14_06, s15_04, s15_17, s15_21,
  the last delivery of the three controls and their whole-run variants, and the A/C of s14_11, s15_09, s15_13; no
  raised side for the A/C of s14_09, s14_10, s15_11, s15_12.
- The MPB instrument's `reference.py` drops a scenario's own timeline as `trajectory.py` did (stage 2's flag; no MPB
  scenario states one).
- `directions.py` reads this set only (its folder); `offon.py` is general.

## Appendix A: off against on, every true stretch (`offon.py analysis/kitting/irb/tk2 actual.csv 0.75 analysis/kitting/irb/tk2/off analysis/kitting/irb/tk1`)

From `actual.csv`, θ = 0.75; off: the same script's run in the off folder named. Ticks inclusive; delay from the stretch's first tick in brackets. "after admission": ticks from the admission to the pin on which the gate no longer clears for the true hypothesis (the retraction reading).

| scenario | timeline in force (on) | off from | true hypothesis | ticks | state at start (on) | first ≥ θ off | on | admitted off | on | after admission off | on | A/C belief at arrival off | on |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s13_01 | break_time 178 to 300 | tk1/s13_01 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_01 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s13_01 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | coffee_break ordinary | 161 (37) | 161 (37) | 161 (37) | 161 (37) | - | - | - | - |
| s13_01 | 〃 | 〃 | deliver_item(item_4) | 217 to 308 | coffee_break raised | 248 (31) | 253 (36) | 248 (31) | 253 (36) | - | - | - | - |
| s13_02 | break_time 178 to 300 | tk1/s13_02 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_02 | 〃 | 〃 | coffee_break(coffee_machine_0) | 67 to 140 | ordinary | 101 (34) | 117 (50) | 101 (34) | 117 (50) | - | - | - | - |
| s13_02 | 〃 | 〃 | deliver_item(item_2) | 141 to 192 | coffee_break suppressed | 149 (8) | 149 (8) | 149 (8) | 149 (8) | - | - | - | - |
| s13_02 | 〃 | 〃 | deliver_item(item_1) | 193 to 285 | coffee_break suppressed | 230 (37) | 231 (38) | 230 (37) | 231 (38) | - | - | - | - |
| s13_02 | 〃 | 〃 | deliver_item(item_4) | 286 to 377 | coffee_break raised | 317 (31) | 300 (14) | 317 (31) | 300 (14) | - | - | - | - |
| s13_03 | break_time 178 to 300 | tk1/s13_03 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_03 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s13_03 | 〃 | 〃 | coffee_break(coffee_machine_0) | 124 to 197 | ordinary | 158 (34) | 175 (51) | 158 (34) | 175 (51) | - | - | - | - |
| s13_03 | 〃 | 〃 | deliver_item(item_1) | 198 to 279 | coffee_break suppressed | 219 (21) | 219 (21) | 219 (21) | 219 (21) | - | - | - | - |
| s13_03 | 〃 | 〃 | deliver_item(item_4) | 280 to 371 | coffee_break suppressed | 311 (31) | 280 (0) | 311 (31) | 280 (0) | - | 286 to 299 none(below_theta) (coffee_break(coffee_machine_0)) | - | - |
| s13_04 | break_time 178 to 300 | tk1/s13_04 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_04 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s13_04 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | coffee_break ordinary | 161 (37) | 161 (37) | 161 (37) | 161 (37) | - | - | - | - |
| s13_04 | 〃 | 〃 | coffee_break(coffee_machine_0) | 217 to 289 | raised | 249 (32) | 238 (21) | 249 (32) | 238 (21) | - | - | - | - |
| s13_04 | 〃 | 〃 | deliver_item(item_4) | 290 to 356 | coffee_break suppressed | 295 (5) | 290 (0) | 295 (5) | 290 (0) | - | - | - | - |
| s13_05 | break_time 178 to 300 | tk1/s13_05 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_05 | 〃 | 〃 | deliver_item(item_2) | 67 to 93 | coffee_break ordinary | never | 87 (20) | never | 87 (20) | - | - | - | - |
| s13_05 | 〃 | 〃 | coffee_break(coffee_machine_0) | 94 to 146 | ordinary | 103 (9) | 120 (26) | 103 (9) | 120 (26) | - | - | - | - |
| s13_05 | 〃 | 〃 | deliver_item(item_2) | 147 to 198 | coffee_break suppressed | 156 (9) | 155 (8) | 156 (9) | 155 (8) | - | - | - | - |
| s13_05 | 〃 | 〃 | deliver_item(item_1) | 199 to 291 | coffee_break suppressed | 236 (37) | 237 (38) | 236 (37) | 237 (38) | - | - | - | - |
| s13_05 | 〃 | 〃 | deliver_item(item_4) | 292 to 383 | coffee_break raised | 323 (31) | 300 (8) | 323 (31) | 300 (8) | - | - | - | - |
| s13_06 | break_time 178 to 300 | tk1/s13_06 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_06 | 〃 | 〃 | deliver_item(item_2) | 67 to 95 | coffee_break ordinary | never | 87 (20) | never | 87 (20) | - | - | - | - |
| s13_06 | 〃 | 〃 | coffee_break(coffee_machine_0) | 96 to 148 | ordinary | 104 (8) | 112 (16) | 104 (8) | 112 (16) | - | - | - | - |
| s13_06 | 〃 | 〃 | deliver_item(item_2) | 149 to 193 | coffee_break suppressed | 170 (21) | 170 (21) | 170 (21) | 170 (21) | - | - | - | - |
| s13_06 | 〃 | 〃 | deliver_item(item_1) | 194 to 286 | coffee_break suppressed | 231 (37) | 231 (37) | 231 (37) | 231 (37) | - | - | - | - |
| s13_06 | 〃 | 〃 | deliver_item(item_4) | 287 to 378 | coffee_break raised | 318 (31) | 300 (13) | 318 (31) | 300 (13) | - | - | - | - |
| s13_07 | break_time 178 to 300 | tk1/s13_07 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_07 | 〃 | 〃 | deliver_item(item_2) | 67 to 121 | coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s13_07 | 〃 | 〃 | coffee_break(coffee_machine_0) | 122 to 195 | ordinary | 153 (31) | 160 (38) | 163 (41) | 163 (41) | - | - | - | - |
| s13_07 | 〃 | 〃 | deliver_item(item_2) | 196 to 240 | coffee_break suppressed | 217 (21) | 217 (21) | 217 (21) | 217 (21) | - | - | - | - |
| s13_07 | 〃 | 〃 | deliver_item(item_1) | 241 to 334 | coffee_break suppressed | 278 (37) | 278 (37) | 278 (37) | 278 (37) | - | - | - | - |
| s13_07 | 〃 | 〃 | deliver_item(item_4) | 335 to 428 | coffee_break ordinary | 367 (32) | 335 (0) | 367 (32) | 335 (0) | - | - | - | - |
| s13_08 | break_time 50 to 200 | tk1/s13_02 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_08 | 〃 | 〃 | coffee_break(coffee_machine_0) | 67 to 140 | raised | 101 (34) | 82 (15) | 101 (34) | 82 (15) | - | - | - | - |
| s13_08 | 〃 | 〃 | deliver_item(item_2) | 141 to 192 | coffee_break suppressed | 149 (8) | 149 (8) | 149 (8) | 149 (8) | - | - | - | - |
| s13_08 | 〃 | 〃 | deliver_item(item_1) | 193 to 285 | coffee_break suppressed | 230 (37) | 230 (37) | 230 (37) | 230 (37) | - | - | - | - |
| s13_08 | 〃 | 〃 | deliver_item(item_4) | 286 to 377 | coffee_break ordinary | 317 (31) | 286 (0) | 317 (31) | 286 (0) | - | - | - | - |
| s13_09 | break_time 90 to 200 | tk1/s13_02 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_09 | 〃 | 〃 | coffee_break(coffee_machine_0) | 67 to 140 | ordinary | 101 (34) | 90 (23) | 101 (34) | 90 (23) | - | - | - | - |
| s13_09 | 〃 | 〃 | deliver_item(item_2) | 141 to 192 | coffee_break suppressed | 149 (8) | 149 (8) | 149 (8) | 149 (8) | - | - | - | - |
| s13_09 | 〃 | 〃 | deliver_item(item_1) | 193 to 285 | coffee_break suppressed | 230 (37) | 230 (37) | 230 (37) | 230 (37) | - | - | - | - |
| s13_09 | 〃 | 〃 | deliver_item(item_4) | 286 to 377 | coffee_break ordinary | 317 (31) | 286 (0) | 317 (31) | 286 (0) | - | - | - | - |
| s13_10 | break_time 120 to 200 | tk1/s13_02 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_10 | 〃 | 〃 | coffee_break(coffee_machine_0) | 67 to 140 | ordinary | 101 (34) | 117 (50) | 101 (34) | 117 (50) | - | - | - | - |
| s13_10 | 〃 | 〃 | deliver_item(item_2) | 141 to 192 | coffee_break suppressed | 149 (8) | 149 (8) | 149 (8) | 149 (8) | - | - | - | - |
| s13_10 | 〃 | 〃 | deliver_item(item_1) | 193 to 285 | coffee_break suppressed | 230 (37) | 230 (37) | 230 (37) | 230 (37) | - | - | - | - |
| s13_10 | 〃 | 〃 | deliver_item(item_4) | 286 to 377 | coffee_break ordinary | 317 (31) | 286 (0) | 317 (31) | 286 (0) | - | - | - | - |
| s13_11 | break_time 40 to 190 | tk1/s13_03 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_11 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break raised | 97 (30) | 102 (35) | 97 (30) | 102 (35) | - | - | - | - |
| s13_11 | 〃 | 〃 | coffee_break(coffee_machine_0) | 124 to 197 | raised | 158 (34) | 138 (14) | 158 (34) | 138 (14) | - | - | - | - |
| s13_11 | 〃 | 〃 | deliver_item(item_1) | 198 to 279 | coffee_break suppressed | 219 (21) | 219 (21) | 219 (21) | 219 (21) | - | - | - | - |
| s13_11 | 〃 | 〃 | deliver_item(item_4) | 280 to 371 | coffee_break suppressed | 311 (31) | 280 (0) | 311 (31) | 280 (0) | - | - | - | - |
| s13_12 | break_time 40 to 150 | tk1/s13_03 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_12 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break raised | 97 (30) | 102 (35) | 97 (30) | 102 (35) | - | - | - | - |
| s13_12 | 〃 | 〃 | coffee_break(coffee_machine_0) | 124 to 197 | raised | 158 (34) | 138 (14) | 158 (34) | 138 (14) | - | 150 to 161 clears (deliver_item(item_4)); 162 to 169 none(below_theta) (deliver_item(item_4)); 170 to 174 none(below_theta) (coffee_break(coffee_machine_0)) | - | - |
| s13_12 | 〃 | 〃 | deliver_item(item_1) | 198 to 279 | coffee_break suppressed | 219 (21) | 219 (21) | 219 (21) | 219 (21) | - | - | - | - |
| s13_12 | 〃 | 〃 | deliver_item(item_4) | 280 to 371 | coffee_break suppressed | 311 (31) | 280 (0) | 311 (31) | 280 (0) | - | - | - | - |
| s13_13 | none | tk1/s13_04 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_13 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s13_13 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | coffee_break ordinary | 161 (37) | 161 (37) | 161 (37) | 161 (37) | - | - | - | - |
| s13_13 | 〃 | 〃 | coffee_break(coffee_machine_0) | 217 to 289 | ordinary | 249 (32) | 271 (54) | 249 (32) | 271 (54) | - | - | - | - |
| s13_13 | 〃 | 〃 | deliver_item(item_4) | 290 to 356 | coffee_break suppressed | 295 (5) | 290 (0) | 295 (5) | 290 (0) | - | - | - | - |
| s13_14 | break_time 0 to end | tk1/s13_01 | deliver_item(item_3) | 0 to 66 | coffee_break raised | 26 (26) | 27 (27) | 26 (26) | 27 (27) | - | - | - | - |
| s13_14 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break raised | 97 (30) | 102 (35) | 97 (30) | 102 (35) | - | - | - | - |
| s13_14 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | coffee_break raised | 161 (37) | 162 (38) | 161 (37) | 162 (38) | - | - | - | - |
| s13_14 | 〃 | 〃 | deliver_item(item_4) | 217 to 308 | coffee_break raised | 248 (31) | 253 (36) | 248 (31) | 253 (36) | - | - | - | - |
| s13_15 | none | off/s13_15 | deliver_item(item_3) | 0 to 66 | coffee_break ordinary | 26 (26) | 26 (26) | 26 (26) | 26 (26) | - | - | - | - |
| s13_15 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s13_15 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | coffee_break ordinary | 161 (37) | 161 (37) | 161 (37) | 161 (37) | - | - | - | - |
| s13_15 | 〃 | 〃 | deliver_item(item_4) | 217 to 260 | coffee_break ordinary | 248 (31) | 217 (0) | 248 (31) | 217 (0) | - | - | - | - |
| s13_15 | 〃 | 〃 | coffee_break(coffee_machine_0) | 261 to 309 | ordinary | 274 (13) | 291 (30) | 277 (16) | 291 (30) | - | - | - | - |
| s13_15 | 〃 | 〃 | deliver_item(item_4) | 310 to 375 | coffee_break suppressed | 315 (5) | 310 (0) | 315 (5) | 310 (0) | - | - | - | - |
| s14_01 | break_time 178 to 300 | tk1/s14_01 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_01 | 〃 | 〃 | deliver_item(item_2) | 89 to 180 | ac_activation ordinary coffee_break ordinary | 138 (49) | 129 (40) | 138 (49) | 129 (40) | - | - | - | - |
| s14_01 | 〃 | 〃 | deliver_item(item_1) | 181 to 282 | ac_activation ordinary coffee_break raised | 232 (51) | 234 (53) | 232 (51) | 234 (53) | - | - | - | - |
| s14_02 | break_time 178 to 300 | tk1/s14_02 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_02 | 〃 | 〃 | coffee_break(coffee_machine_0) | 89 to 166 | ordinary | 143 (54) | 157 (68) | 143 (54) | 157 (68) | - | - | - | - |
| s14_02 | 〃 | 〃 | deliver_item(item_2) | 167 to 225 | ac_activation ordinary coffee_break suppressed | 177 (10) | 171 (4) | 177 (10) | 171 (4) | - | - | - | - |
| s14_02 | 〃 | 〃 | deliver_item(item_1) | 226 to 325 | ac_activation ordinary coffee_break suppressed | 277 (51) | 226 (0) | 277 (51) | 226 (0) | - | 255 to 271 none(below_theta) (coffee_break(coffee_machine_0)); 272 to 277 none(below_theta) (deliver_item(item_1)) | - | - |
| s14_03 | break_time 178 to 300 | tk1/s14_03 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_03 | 〃 | 〃 | deliver_item(item_2) | 89 to 180 | ac_activation ordinary coffee_break ordinary | 138 (49) | 129 (40) | 138 (49) | 129 (40) | - | - | - | - |
| s14_03 | 〃 | 〃 | coffee_break(coffee_machine_0) | 181 to 259 | raised | 235 (54) | 226 (45) | 235 (54) | 226 (45) | - | - | - | - |
| s14_03 | 〃 | 〃 | deliver_item(item_1) | 260 to 318 | ac_activation ordinary coffee_break suppressed | 269 (9) | 260 (0) | 269 (9) | 260 (0) | - | - | - | - |
| s14_04 | break_time 178 to 300 | tk1/s14_04 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_04 | 〃 | 〃 | deliver_item(item_2) | 89 to 132 | ac_activation ordinary coffee_break ordinary | never | 129 (40) | never | 129 (40) | - | - | - | - |
| s14_04 | 〃 | 〃 | coffee_break(coffee_machine_0) | 133 to 174 | ordinary | 149 (16) | 162 (29) | 149 (16) | 162 (29) | - | - | - | - |
| s14_04 | 〃 | 〃 | deliver_item(item_2) | 175 to 233 | ac_activation ordinary coffee_break suppressed | 187 (12) | 179 (4) | 187 (12) | 179 (4) | - | - | - | - |
| s14_04 | 〃 | 〃 | deliver_item(item_1) | 234 to 333 | ac_activation ordinary coffee_break suppressed | 285 (51) | 234 (0) | 285 (51) | 234 (0) | - | 263 to 279 none(below_theta) (coffee_break(coffee_machine_0)); 280 to 285 none(below_theta) (deliver_item(item_1)) | - | - |
| s14_05 | break_time 178 to 300 | tk1/s14_05 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_05 | 〃 | 〃 | deliver_item(item_2) | 89 to 134 | ac_activation ordinary coffee_break ordinary | never | 129 (40) | never | 129 (40) | - | - | - | - |
| s14_05 | 〃 | 〃 | coffee_break(coffee_machine_0) | 135 to 176 | ordinary | 150 (15) | 163 (28) | 150 (15) | 163 (28) | - | - | - | - |
| s14_05 | 〃 | 〃 | deliver_item(item_2) | 177 to 226 | ac_activation ordinary coffee_break suppressed | 187 (10) | 184 (7) | 187 (10) | 184 (7) | - | - | - | - |
| s14_05 | 〃 | 〃 | deliver_item(item_1) | 227 to 328 | ac_activation ordinary coffee_break suppressed | 278 (51) | 227 (0) | 278 (51) | 227 (0) | - | 265 to 272 none(below_theta) (coffee_break(coffee_machine_0)); 273 to 279 none(below_theta) (deliver_item(item_1)) | - | - |
| s14_06 | break_time 178 to 300 | tk1/s14_06 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_06 | 〃 | 〃 | deliver_item(item_2) | 89 to 178 | ac_activation ordinary coffee_break ordinary | 138 (49) | 129 (40) | 138 (49) | 129 (40) | - | - | - | - |
| s14_06 | 〃 | 〃 | coffee_break(coffee_machine_0) | 179 to 257 | raised | 231 (52) | 224 (45) | 231 (52) | 225 (46) | - | - | - | - |
| s14_06 | 〃 | 〃 | deliver_item(item_2) | 258 to 307 | ac_activation ordinary coffee_break suppressed | 267 (9) | 265 (7) | 267 (9) | 265 (7) | - | - | - | - |
| s14_06 | 〃 | 〃 | deliver_item(item_1) | 308 to 409 | ac_activation ordinary coffee_break suppressed | 359 (51) | 308 (0) | 359 (51) | 308 (0) | - | - | - | - |
| s14_07 | room_warm 150 to end | tk1/s14_07 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_07 | 〃 | 〃 | ac_activation(ac_switch_0) | 89 to 137 | ordinary | never | never | never | never | - | - | 0.4626 at 135 | 0.0599 at 135 |
| s14_07 | 〃 | 〃 | deliver_item(item_2) | 138 to 192 | ac_activation suppressed coffee_break ordinary | 148 (10) | 142 (4) | 148 (10) | 142 (4) | - | - | - | - |
| s14_07 | 〃 | 〃 | deliver_item(item_1) | 193 to 294 | ac_activation suppressed coffee_break ordinary | 244 (51) | 193 (0) | 244 (51) | 193 (0) | - | - | - | - |
| s14_08 | room_warm 150 to end | tk1/s14_08 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_08 | 〃 | 〃 | deliver_item(item_2) | 89 to 180 | ac_activation ordinary coffee_break ordinary | 138 (49) | 129 (40) | 138 (49) | 129 (40) | - | - | - | - |
| s14_08 | 〃 | 〃 | ac_activation(ac_switch_0) | 181 to 229 | raised | never | never | never | never | - | - | 0.5475 at 227 | 0.6449 at 227 |
| s14_08 | 〃 | 〃 | deliver_item(item_1) | 230 to 293 | ac_activation suppressed coffee_break ordinary | 242 (12) | 230 (0) | 242 (12) | 230 (0) | - | - | - | - |
| s14_09 | room_warm 150 to end | tk1/s14_09 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_09 | 〃 | 〃 | deliver_item(item_2) | 89 to 132 | ac_activation ordinary coffee_break ordinary | never | 129 (40) | never | 129 (40) | - | - | - | - |
| s14_09 | 〃 | 〃 | ac_activation(ac_switch_0) | 133 to 140 | ordinary | never | never | never | never | - | - | 0.4456 at 138 | 0.0467 at 138 |
| s14_09 | 〃 | 〃 | deliver_item(item_2) | 141 to 194 | ac_activation suppressed coffee_break ordinary | 151 (10) | 149 (8) | 151 (10) | 149 (8) | - | - | - | - |
| s14_09 | 〃 | 〃 | deliver_item(item_1) | 195 to 296 | ac_activation suppressed coffee_break ordinary | 246 (51) | 195 (0) | 246 (51) | 195 (0) | - | - | - | - |
| s14_10 | room_warm 150 to end | tk1/s14_10 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_10 | 〃 | 〃 | deliver_item(item_2) | 89 to 134 | ac_activation ordinary coffee_break ordinary | never | 129 (40) | never | 129 (40) | - | - | - | - |
| s14_10 | 〃 | 〃 | ac_activation(ac_switch_0) | 135 to 142 | ordinary | never | never | never | never | - | - | 0.4814 at 140 | 0.0558 at 140 |
| s14_10 | 〃 | 〃 | deliver_item(item_2) | 143 to 191 | ac_activation suppressed coffee_break ordinary | 151 (8) | 149 (6) | 151 (8) | 149 (6) | - | - | - | - |
| s14_10 | 〃 | 〃 | deliver_item(item_1) | 192 to 293 | ac_activation suppressed coffee_break ordinary | 243 (51) | 192 (0) | 243 (51) | 192 (0) | - | - | - | - |
| s14_11 | room_warm 150 to end | tk1/s14_11 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_11 | 〃 | 〃 | deliver_item(item_2) | 89 to 178 | ac_activation ordinary coffee_break ordinary | 138 (49) | 129 (40) | 138 (49) | 129 (40) | - | - | - | - |
| s14_11 | 〃 | 〃 | ac_activation(ac_switch_0) | 179 to 227 | raised | never | never | never | never | - | - | 0.4351 at 225 | 0.5192 at 225 |
| s14_11 | 〃 | 〃 | deliver_item(item_2) | 228 to 276 | ac_activation suppressed coffee_break ordinary | 236 (8) | 234 (6) | 236 (8) | 234 (6) | - | - | - | - |
| s14_11 | 〃 | 〃 | deliver_item(item_1) | 277 to 378 | ac_activation suppressed coffee_break ordinary | 328 (51) | 277 (0) | 328 (51) | 277 (0) | - | - | - | - |
| s14_12 | break_time 70 to 250 | tk1/s14_02 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_12 | 〃 | 〃 | coffee_break(coffee_machine_0) | 89 to 166 | raised | 143 (54) | 129 (40) | 143 (54) | 129 (40) | - | - | - | - |
| s14_12 | 〃 | 〃 | deliver_item(item_2) | 167 to 225 | ac_activation ordinary coffee_break suppressed | 177 (10) | 171 (4) | 177 (10) | 171 (4) | - | - | - | - |
| s14_12 | 〃 | 〃 | deliver_item(item_1) | 226 to 325 | ac_activation ordinary coffee_break suppressed | 277 (51) | 226 (0) | 277 (51) | 226 (0) | - | - | - | - |
| s14_13 | break_time 110 to 250 | tk1/s14_02 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_13 | 〃 | 〃 | coffee_break(coffee_machine_0) | 89 to 166 | ordinary | 143 (54) | 129 (40) | 143 (54) | 129 (40) | - | - | - | - |
| s14_13 | 〃 | 〃 | deliver_item(item_2) | 167 to 225 | ac_activation ordinary coffee_break suppressed | 177 (10) | 171 (4) | 177 (10) | 171 (4) | - | - | - | - |
| s14_13 | 〃 | 〃 | deliver_item(item_1) | 226 to 325 | ac_activation ordinary coffee_break suppressed | 277 (51) | 226 (0) | 277 (51) | 226 (0) | - | - | - | - |
| s14_14 | break_time 150 to 250 | tk1/s14_02 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_14 | 〃 | 〃 | coffee_break(coffee_machine_0) | 89 to 166 | ordinary | 143 (54) | 150 (61) | 143 (54) | 150 (61) | - | - | - | - |
| s14_14 | 〃 | 〃 | deliver_item(item_2) | 167 to 225 | ac_activation ordinary coffee_break suppressed | 177 (10) | 171 (4) | 177 (10) | 171 (4) | - | - | - | - |
| s14_14 | 〃 | 〃 | deliver_item(item_1) | 226 to 325 | ac_activation ordinary coffee_break suppressed | 277 (51) | 226 (0) | 277 (51) | 226 (0) | - | - | - | - |
| s14_15 | room_warm 70 to end | tk1/s14_07 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_15 | 〃 | 〃 | ac_activation(ac_switch_0) | 89 to 137 | raised | never | never | never | never | - | - | 0.4626 at 135 | 0.6144 at 135 |
| s14_15 | 〃 | 〃 | deliver_item(item_2) | 138 to 192 | ac_activation suppressed coffee_break ordinary | 148 (10) | 142 (4) | 148 (10) | 142 (4) | - | - | - | - |
| s14_15 | 〃 | 〃 | deliver_item(item_1) | 193 to 294 | ac_activation suppressed coffee_break ordinary | 244 (51) | 193 (0) | 244 (51) | 193 (0) | - | - | - | - |
| s14_16 | room_warm 110 to end | tk1/s14_07 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_16 | 〃 | 〃 | ac_activation(ac_switch_0) | 89 to 137 | ordinary | never | never | never | never | - | - | 0.4626 at 135 | 0.6144 at 135 |
| s14_16 | 〃 | 〃 | deliver_item(item_2) | 138 to 192 | ac_activation suppressed coffee_break ordinary | 148 (10) | 142 (4) | 148 (10) | 142 (4) | - | - | - | - |
| s14_16 | 〃 | 〃 | deliver_item(item_1) | 193 to 294 | ac_activation suppressed coffee_break ordinary | 244 (51) | 193 (0) | 244 (51) | 193 (0) | - | - | - | - |
| s14_17 | room_warm 0 to 110 | tk1/s14_07 | deliver_item(item_0) | 0 to 88 | ac_activation raised coffee_break ordinary | 50 (50) | 49 (49) | 50 (50) | 49 (49) | - | - | - | - |
| s14_17 | 〃 | 〃 | ac_activation(ac_switch_0) | 89 to 137 | raised | never | never | never | never | - | - | 0.4626 at 135 | 0.0599 at 135 |
| s14_17 | 〃 | 〃 | deliver_item(item_2) | 138 to 192 | ac_activation suppressed coffee_break ordinary | 148 (10) | 142 (4) | 148 (10) | 142 (4) | - | - | - | - |
| s14_17 | 〃 | 〃 | deliver_item(item_1) | 193 to 294 | ac_activation suppressed coffee_break ordinary | 244 (51) | 193 (0) | 244 (51) | 193 (0) | - | - | - | - |
| s14_18 | break_time 60 to 250 | tk1/s14_03 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_18 | 〃 | 〃 | deliver_item(item_2) | 89 to 180 | ac_activation ordinary coffee_break raised | 138 (49) | 139 (50) | 138 (49) | 139 (50) | - | - | - | - |
| s14_18 | 〃 | 〃 | coffee_break(coffee_machine_0) | 181 to 259 | raised | 235 (54) | 226 (45) | 235 (54) | 226 (45) | - | 250 to 251 none(below_theta) (coffee_break(coffee_machine_0)) | - | - |
| s14_18 | 〃 | 〃 | deliver_item(item_1) | 260 to 318 | ac_activation ordinary coffee_break suppressed | 269 (9) | 260 (0) | 269 (9) | 260 (0) | - | - | - | - |
| s14_19 | none | tk1/s14_03 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_19 | 〃 | 〃 | deliver_item(item_2) | 89 to 180 | ac_activation ordinary coffee_break ordinary | 138 (49) | 129 (40) | 138 (49) | 129 (40) | - | - | - | - |
| s14_19 | 〃 | 〃 | coffee_break(coffee_machine_0) | 181 to 259 | ordinary | 235 (54) | 252 (71) | 235 (54) | 252 (71) | - | - | - | - |
| s14_19 | 〃 | 〃 | deliver_item(item_1) | 260 to 318 | ac_activation ordinary coffee_break suppressed | 269 (9) | 260 (0) | 269 (9) | 260 (0) | - | - | - | - |
| s14_20 | break_time 0 to end | tk1/s14_01 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break raised | 50 (50) | 51 (51) | 50 (50) | 51 (51) | - | - | - | - |
| s14_20 | 〃 | 〃 | deliver_item(item_2) | 89 to 180 | ac_activation ordinary coffee_break raised | 138 (49) | 139 (50) | 138 (49) | 139 (50) | - | - | - | - |
| s14_20 | 〃 | 〃 | deliver_item(item_1) | 181 to 282 | ac_activation ordinary coffee_break raised | 232 (51) | 234 (53) | 232 (51) | 234 (53) | - | - | - | - |
| s14_21 | break_time 178 to 300 | tk1/s14_08 | deliver_item(item_0) | 0 to 88 | ac_activation ordinary coffee_break ordinary | 50 (50) | 48 (48) | 50 (50) | 48 (48) | - | - | - | - |
| s14_21 | 〃 | 〃 | deliver_item(item_2) | 89 to 180 | ac_activation ordinary coffee_break ordinary | 138 (49) | 129 (40) | 138 (49) | 129 (40) | - | - | - | - |
| s14_21 | 〃 | 〃 | ac_activation(ac_switch_0) | 181 to 229 | ordinary | never | never | never | never | - | - | 0.5475 at 227 | 0.0142 at 227 |
| s14_21 | 〃 | 〃 | deliver_item(item_1) | 230 to 293 | ac_activation suppressed coffee_break raised | 242 (12) | 245 (15) | 242 (12) | 245 (15) | - | - | - | - |
| s15_01 | break_time 178 to 300 | tk1/s15_01 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_01 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_01 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation ordinary coffee_break ordinary | 171 (47) | 162 (38) | 171 (47) | 162 (38) | - | - | - | - |
| s15_01 | 〃 | 〃 | deliver_item(item_4) | 217 to 308 | ac_activation ordinary coffee_break raised | 262 (45) | 254 (37) | 262 (45) | 254 (37) | - | - | - | - |
| s15_02 | break_time 178 to 300 | tk1/s15_02 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_02 | 〃 | 〃 | coffee_break(coffee_machine_0) | 67 to 140 | ordinary | 103 (36) | 117 (50) | 103 (36) | 117 (50) | - | - | - | - |
| s15_02 | 〃 | 〃 | deliver_item(item_2) | 141 to 192 | ac_activation ordinary coffee_break suppressed | 150 (9) | 149 (8) | 150 (9) | 149 (8) | - | - | - | - |
| s15_02 | 〃 | 〃 | deliver_item(item_1) | 193 to 285 | ac_activation ordinary coffee_break suppressed | 240 (47) | 232 (39) | 240 (47) | 232 (39) | - | - | - | - |
| s15_02 | 〃 | 〃 | deliver_item(item_4) | 286 to 377 | ac_activation ordinary coffee_break raised | 331 (45) | 300 (14) | 331 (45) | 300 (14) | - | - | - | - |
| s15_03 | break_time 178 to 300 | tk1/s15_03 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_03 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_03 | 〃 | 〃 | coffee_break(coffee_machine_0) | 124 to 197 | ordinary | 160 (36) | 176 (52) | 160 (36) | 176 (52) | - | - | - | - |
| s15_03 | 〃 | 〃 | deliver_item(item_1) | 198 to 279 | ac_activation ordinary coffee_break suppressed | 227 (29) | 219 (21) | 227 (29) | 219 (21) | - | - | - | - |
| s15_03 | 〃 | 〃 | deliver_item(item_4) | 280 to 371 | ac_activation ordinary coffee_break suppressed | 325 (45) | 280 (0) | 325 (45) | 280 (0) | - | 286 to 299 none(below_theta) (coffee_break(coffee_machine_0)) | - | - |
| s15_04 | break_time 178 to 300 | tk1/s15_04 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_04 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_04 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation ordinary coffee_break ordinary | 171 (47) | 162 (38) | 171 (47) | 162 (38) | - | - | - | - |
| s15_04 | 〃 | 〃 | coffee_break(coffee_machine_0) | 217 to 289 | raised | 252 (35) | 238 (21) | 252 (35) | 238 (21) | - | - | - | - |
| s15_04 | 〃 | 〃 | deliver_item(item_4) | 290 to 356 | ac_activation ordinary coffee_break suppressed | 313 (23) | 290 (0) | 313 (23) | 290 (0) | - | - | - | - |
| s15_05 | break_time 178 to 300 | tk1/s15_05 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_05 | 〃 | 〃 | deliver_item(item_2) | 67 to 93 | ac_activation ordinary coffee_break ordinary | never | 87 (20) | never | 87 (20) | - | - | - | - |
| s15_05 | 〃 | 〃 | coffee_break(coffee_machine_0) | 94 to 146 | ordinary | 104 (10) | 120 (26) | 104 (10) | 120 (26) | - | - | - | - |
| s15_05 | 〃 | 〃 | deliver_item(item_2) | 147 to 198 | ac_activation ordinary coffee_break suppressed | 157 (10) | 155 (8) | 157 (10) | 155 (8) | - | - | - | - |
| s15_05 | 〃 | 〃 | deliver_item(item_1) | 199 to 291 | ac_activation ordinary coffee_break suppressed | 246 (47) | 238 (39) | 246 (47) | 238 (39) | - | - | - | - |
| s15_05 | 〃 | 〃 | deliver_item(item_4) | 292 to 383 | ac_activation ordinary coffee_break raised | 337 (45) | 300 (8) | 337 (45) | 300 (8) | - | - | - | - |
| s15_06 | break_time 178 to 300 | tk1/s15_06 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_06 | 〃 | 〃 | deliver_item(item_2) | 67 to 95 | ac_activation ordinary coffee_break ordinary | never | 87 (20) | never | 87 (20) | - | - | - | - |
| s15_06 | 〃 | 〃 | coffee_break(coffee_machine_0) | 96 to 148 | ordinary | 104 (8) | 112 (16) | 104 (8) | 112 (16) | - | - | - | - |
| s15_06 | 〃 | 〃 | deliver_item(item_2) | 149 to 193 | ac_activation ordinary coffee_break suppressed | 170 (21) | 170 (21) | 170 (21) | 170 (21) | - | - | - | - |
| s15_06 | 〃 | 〃 | deliver_item(item_1) | 194 to 286 | ac_activation ordinary coffee_break suppressed | 241 (47) | 232 (38) | 241 (47) | 232 (38) | - | - | - | - |
| s15_06 | 〃 | 〃 | deliver_item(item_4) | 287 to 378 | ac_activation ordinary coffee_break raised | 332 (45) | 300 (13) | 332 (45) | 300 (13) | - | - | - | - |
| s15_07 | break_time 178 to 300 | tk1/s15_07 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_07 | 〃 | 〃 | deliver_item(item_2) | 67 to 121 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_07 | 〃 | 〃 | coffee_break(coffee_machine_0) | 122 to 195 | ordinary | 153 (31) | 160 (38) | 163 (41) | 163 (41) | - | - | - | - |
| s15_07 | 〃 | 〃 | deliver_item(item_2) | 196 to 240 | ac_activation ordinary coffee_break suppressed | 217 (21) | 217 (21) | 217 (21) | 217 (21) | - | - | - | - |
| s15_07 | 〃 | 〃 | deliver_item(item_1) | 241 to 334 | ac_activation ordinary coffee_break suppressed | 288 (47) | 278 (37) | 288 (47) | 278 (37) | - | - | - | - |
| s15_07 | 〃 | 〃 | deliver_item(item_4) | 335 to 428 | ac_activation ordinary coffee_break ordinary | 381 (46) | 335 (0) | 381 (46) | 335 (0) | - | - | - | - |
| s15_08 | room_warm 150 to end | tk1/s15_08 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_08 | 〃 | 〃 | ac_activation(ac_switch_0) | 67 to 114 | ordinary | never | never | never | never | - | - | 0.6238 at 112 | 0.0914 at 112 |
| s15_08 | 〃 | 〃 | deliver_item(item_2) | 115 to 183 | ac_activation suppressed coffee_break ordinary | 135 (20) | 125 (10) | 135 (20) | 125 (10) | - | - | - | - |
| s15_08 | 〃 | 〃 | deliver_item(item_1) | 184 to 276 | ac_activation suppressed coffee_break ordinary | 231 (47) | 221 (37) | 231 (47) | 221 (37) | - | - | - | - |
| s15_08 | 〃 | 〃 | deliver_item(item_4) | 277 to 368 | ac_activation suppressed coffee_break ordinary | 322 (45) | 277 (0) | 322 (45) | 277 (0) | - | - | - | - |
| s15_09 | room_warm 150 to end | tk1/s15_09 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_09 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_09 | 〃 | 〃 | ac_activation(ac_switch_0) | 124 to 171 | ordinary | never | never | never | never | - | - | 0.6130 at 169 | 0.6152 at 169 |
| s15_09 | 〃 | 〃 | deliver_item(item_1) | 172 to 229 | ac_activation suppressed coffee_break ordinary | 180 (8) | 176 (4) | 180 (8) | 176 (4) | - | - | - | - |
| s15_09 | 〃 | 〃 | deliver_item(item_4) | 230 to 323 | ac_activation suppressed coffee_break ordinary | 276 (46) | 230 (0) | 276 (46) | 230 (0) | - | - | - | - |
| s15_10 | room_warm 150 to end | tk1/s15_10 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_10 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_10 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation ordinary coffee_break ordinary | 171 (47) | 171 (47) | 171 (47) | 171 (47) | - | - | - | - |
| s15_10 | 〃 | 〃 | ac_activation(ac_switch_0) | 217 to 263 | raised | never | never | never | never | - | - | 0.7487 at 261 | 0.6035 at 261 |
| s15_10 | 〃 | 〃 | deliver_item(item_4) | 264 to 321 | ac_activation suppressed coffee_break ordinary | 279 (15) | 264 (0) | 279 (15) | 264 (0) | - | - | - | - |
| s15_11 | room_warm 150 to end | tk1/s15_11 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_11 | 〃 | 〃 | deliver_item(item_2) | 67 to 93 | ac_activation ordinary coffee_break ordinary | never | 87 (20) | never | 87 (20) | - | - | - | - |
| s15_11 | 〃 | 〃 | ac_activation(ac_switch_0) | 94 to 134 | ordinary | never | never | never | never | - | - | 0.7468 at 132 | 0.1516 at 132 |
| s15_11 | 〃 | 〃 | deliver_item(item_2) | 135 to 203 | ac_activation suppressed coffee_break ordinary | 155 (20) | 145 (10) | 155 (20) | 145 (10) | - | - | - | - |
| s15_11 | 〃 | 〃 | deliver_item(item_1) | 204 to 296 | ac_activation suppressed coffee_break ordinary | 251 (47) | 241 (37) | 251 (47) | 241 (37) | - | - | - | - |
| s15_11 | 〃 | 〃 | deliver_item(item_4) | 297 to 388 | ac_activation suppressed coffee_break ordinary | 342 (45) | 297 (0) | 342 (45) | 297 (0) | - | - | - | - |
| s15_12 | room_warm 150 to end | tk1/s15_12 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_12 | 〃 | 〃 | deliver_item(item_2) | 67 to 95 | ac_activation ordinary coffee_break ordinary | never | 87 (20) | never | 87 (20) | - | - | - | - |
| s15_12 | 〃 | 〃 | ac_activation(ac_switch_0) | 96 to 136 | ordinary | 121 (25) | 125 (29) | 133 (37) | 133 (37) | - | - | 0.9961 at 134 | 0.9875 at 134 |
| s15_12 | 〃 | 〃 | deliver_item(item_2) | 137 to 184 | ac_activation suppressed coffee_break ordinary | 164 (27) | 164 (27) | 164 (27) | 164 (27) | - | - | - | - |
| s15_12 | 〃 | 〃 | deliver_item(item_1) | 185 to 278 | ac_activation suppressed coffee_break ordinary | 231 (46) | 221 (36) | 231 (46) | 221 (36) | - | - | - | - |
| s15_12 | 〃 | 〃 | deliver_item(item_4) | 279 to 372 | ac_activation suppressed coffee_break ordinary | 325 (46) | 279 (0) | 325 (46) | 279 (0) | - | - | - | - |
| s15_13 | room_warm 150 to end | tk1/s15_13 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_13 | 〃 | 〃 | deliver_item(item_2) | 67 to 121 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_13 | 〃 | 〃 | ac_activation(ac_switch_0) | 122 to 169 | ordinary | 154 (32) | 152 (30) | 166 (44) | 166 (44) | - | - | 0.9952 at 167 | 0.9990 at 167 |
| s15_13 | 〃 | 〃 | deliver_item(item_2) | 170 to 216 | ac_activation suppressed coffee_break ordinary | 197 (27) | 197 (27) | 197 (27) | 197 (27) | - | - | - | - |
| s15_13 | 〃 | 〃 | deliver_item(item_1) | 217 to 308 | ac_activation suppressed coffee_break ordinary | 263 (46) | 253 (36) | 263 (46) | 253 (36) | - | - | - | - |
| s15_13 | 〃 | 〃 | deliver_item(item_4) | 309 to 400 | ac_activation suppressed coffee_break ordinary | 354 (45) | 309 (0) | 354 (45) | 309 (0) | - | - | - | - |
| s15_14 | room_warm 50 to end | tk1/s15_08 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_14 | 〃 | 〃 | ac_activation(ac_switch_0) | 67 to 114 | raised | never | never | never | never | - | - | 0.6238 at 112 | 0.7154 at 112 |
| s15_14 | 〃 | 〃 | deliver_item(item_2) | 115 to 183 | ac_activation suppressed coffee_break ordinary | 135 (20) | 125 (10) | 135 (20) | 125 (10) | - | - | - | - |
| s15_14 | 〃 | 〃 | deliver_item(item_1) | 184 to 276 | ac_activation suppressed coffee_break ordinary | 231 (47) | 221 (37) | 231 (47) | 221 (37) | - | - | - | - |
| s15_14 | 〃 | 〃 | deliver_item(item_4) | 277 to 368 | ac_activation suppressed coffee_break ordinary | 322 (45) | 277 (0) | 322 (45) | 277 (0) | - | - | - | - |
| s15_15 | room_warm 90 to end | tk1/s15_08 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_15 | 〃 | 〃 | ac_activation(ac_switch_0) | 67 to 114 | ordinary | never | never | never | never | - | - | 0.6238 at 112 | 0.7154 at 112 |
| s15_15 | 〃 | 〃 | deliver_item(item_2) | 115 to 183 | ac_activation suppressed coffee_break ordinary | 135 (20) | 125 (10) | 135 (20) | 125 (10) | - | - | - | - |
| s15_15 | 〃 | 〃 | deliver_item(item_1) | 184 to 276 | ac_activation suppressed coffee_break ordinary | 231 (47) | 221 (37) | 231 (47) | 221 (37) | - | - | - | - |
| s15_15 | 〃 | 〃 | deliver_item(item_4) | 277 to 368 | ac_activation suppressed coffee_break ordinary | 322 (45) | 277 (0) | 322 (45) | 277 (0) | - | - | - | - |
| s15_16 | room_warm 0 to 90 | tk1/s15_08 | deliver_item(item_3) | 0 to 66 | ac_activation raised coffee_break ordinary | 28 (28) | 30 (30) | 28 (28) | 30 (30) | - | - | - | - |
| s15_16 | 〃 | 〃 | ac_activation(ac_switch_0) | 67 to 114 | raised | never | never | never | never | - | - | 0.6238 at 112 | 0.0914 at 112 |
| s15_16 | 〃 | 〃 | deliver_item(item_2) | 115 to 183 | ac_activation suppressed coffee_break ordinary | 135 (20) | 125 (10) | 135 (20) | 125 (10) | - | - | - | - |
| s15_16 | 〃 | 〃 | deliver_item(item_1) | 184 to 276 | ac_activation suppressed coffee_break ordinary | 231 (47) | 221 (37) | 231 (47) | 221 (37) | - | - | - | - |
| s15_16 | 〃 | 〃 | deliver_item(item_4) | 277 to 368 | ac_activation suppressed coffee_break ordinary | 322 (45) | 277 (0) | 322 (45) | 277 (0) | - | - | - | - |
| s15_17 | break_time 178 to 300; room_warm 150 to end | tk1/s15_04 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_17 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_17 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation ordinary coffee_break ordinary | 171 (47) | 171 (47) | 171 (47) | 171 (47) | - | - | - | - |
| s15_17 | 〃 | 〃 | coffee_break(coffee_machine_0) | 217 to 289 | raised | 252 (35) | 243 (26) | 252 (35) | 243 (26) | - | - | - | - |
| s15_17 | 〃 | 〃 | deliver_item(item_4) | 290 to 356 | ac_activation raised coffee_break suppressed | 313 (23) | 310 (20) | 313 (23) | 310 (20) | - | - | - | - |
| s15_18 | room_warm 0 to end | tk1/s15_01 | deliver_item(item_3) | 0 to 66 | ac_activation raised coffee_break ordinary | 28 (28) | 30 (30) | 28 (28) | 30 (30) | - | - | - | - |
| s15_18 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation raised coffee_break ordinary | 97 (30) | 90 (23) | 97 (30) | 90 (23) | - | - | - | - |
| s15_18 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation raised coffee_break ordinary | 171 (47) | 171 (47) | 171 (47) | 171 (47) | - | - | - | - |
| s15_18 | 〃 | 〃 | deliver_item(item_4) | 217 to 308 | ac_activation raised coffee_break ordinary | 262 (45) | 256 (39) | 262 (45) | 256 (39) | - | - | - | - |
| s15_19 | none | tk1/s15_10 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_19 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_19 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation ordinary coffee_break ordinary | 171 (47) | 162 (38) | 171 (47) | 162 (38) | - | - | - | - |
| s15_19 | 〃 | 〃 | ac_activation(ac_switch_0) | 217 to 263 | ordinary | never | never | never | never | - | - | 0.7487 at 261 | 0.0574 at 261 |
| s15_19 | 〃 | 〃 | deliver_item(item_4) | 264 to 321 | ac_activation suppressed coffee_break ordinary | 279 (15) | 264 (0) | 279 (15) | 264 (0) | - | - | - | - |
| s15_20 | break_time 178 to 300; room_warm 150 to end | tk1/s15_10 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_20 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_20 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation ordinary coffee_break ordinary | 171 (47) | 171 (47) | 171 (47) | 171 (47) | - | - | - | - |
| s15_20 | 〃 | 〃 | ac_activation(ac_switch_0) | 217 to 263 | raised | never | never | never | never | - | - | 0.7487 at 261 | 0.5932 at 261 |
| s15_20 | 〃 | 〃 | deliver_item(item_4) | 264 to 321 | ac_activation suppressed coffee_break raised | 279 (15) | 283 (19) | 279 (15) | 283 (19) | - | - | - | - |
| s15_21 | break_time 307 to end | off/s15_21 | deliver_item(item_3) | 0 to 66 | ac_activation ordinary coffee_break ordinary | 28 (28) | 26 (26) | 28 (28) | 26 (26) | - | - | - | - |
| s15_21 | 〃 | 〃 | deliver_item(item_2) | 67 to 123 | ac_activation ordinary coffee_break ordinary | 97 (30) | 87 (20) | 97 (30) | 87 (20) | - | - | - | - |
| s15_21 | 〃 | 〃 | deliver_item(item_1) | 124 to 216 | ac_activation ordinary coffee_break ordinary | 171 (47) | 162 (38) | 171 (47) | 162 (38) | - | - | - | - |
| s15_21 | 〃 | 〃 | deliver_item(item_4) | 217 to 308 | ac_activation ordinary coffee_break ordinary | 262 (45) | 217 (0) | 262 (45) | 217 (0) | - | - | - | - |
| s15_21 | 〃 | 〃 | coffee_break(coffee_machine_0) | 309 to 381 | raised | 334 (25) | 309 (0) | 334 (25) | 309 (0) | - | - | - | - |

Admissions of a hypothesis that is not the true task (every tick, the unmodelled ones included), off and on.

| scenario | side | hypothesis admitted | ticks | true task on those ticks | how it ends |
|---|---|---|---|---|---|
| s13_01 | off | coffee_break(coffee_machine_0) | 309 to 330 | unmodelled | retraction at 331 (none(leader_inadequate)) |
| s13_01 | on | coffee_break(coffee_machine_0) | 309 to 330 | unmodelled | retraction at 331 (none(leader_inadequate)) |
| s13_02 | off | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_02 | on | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_03 | off | coffee_break(coffee_machine_0) | 372 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s13_03 | on | deliver_item(item_4) | 150 to 161 | coffee_break(coffee_machine_0) | retraction at 162 (none(below_theta)) |
| s13_03 | on | deliver_item(item_4) | 279 | deliver_item(item_1) (complete: pinned) | the human starts it at 280 |
| s13_03 | on | coffee_break(coffee_machine_0) | 372 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s13_04 | off | deliver_item(item_4) | 289 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 290 |
| s13_04 | off | coffee_break(coffee_machine_0) | 357 to 378 | unmodelled | retraction at 379 (none(leader_inadequate)) |
| s13_04 | on | deliver_item(item_4) | 289 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 290 |
| s13_04 | on | coffee_break(coffee_machine_0) | 357 to 378 | unmodelled | retraction at 379 (none(leader_inadequate)) |
| s13_05 | off | coffee_break(coffee_machine_0) | 384 to 405 | unmodelled | retraction at 406 (none(leader_inadequate)) |
| s13_05 | on | deliver_item(item_2) | 94 | coffee_break(coffee_machine_0) | retraction at 95 (none(leader_no_observation)) |
| s13_05 | on | deliver_item(item_2) | 96 to 99 | coffee_break(coffee_machine_0) | retraction at 100 (none(below_theta)) |
| s13_05 | on | coffee_break(coffee_machine_0) | 384 to 405 | unmodelled | retraction at 406 (none(leader_inadequate)) |
| s13_06 | off | coffee_break(coffee_machine_0) | 379 to 400 | unmodelled | retraction at 401 (none(leader_inadequate)) |
| s13_06 | on | deliver_item(item_2) | 96 to 103 | coffee_break(coffee_machine_0) | retraction at 104 (none(below_theta)) |
| s13_06 | on | coffee_break(coffee_machine_0) | 379 to 400 | unmodelled | retraction at 401 (none(leader_inadequate)) |
| s13_07 | off | deliver_item(item_2) | 123 to 130 | coffee_break(coffee_machine_0) | retraction at 131 (none(leader_inadequate)) |
| s13_07 | off | coffee_break(coffee_machine_0) | 429 to 451 | unmodelled | retraction at 452 (none(leader_inadequate)) |
| s13_07 | on | deliver_item(item_2) | 123 to 130 | coffee_break(coffee_machine_0) | retraction at 131 (none(leader_inadequate)) |
| s13_07 | on | deliver_item(item_4) | 334 | deliver_item(item_1) (complete: pinned) | the human starts it at 335 |
| s13_07 | on | coffee_break(coffee_machine_0) | 429 to 451 | unmodelled | retraction at 452 (none(leader_inadequate)) |
| s13_08 | off | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_08 | on | deliver_item(item_4) | 285 | deliver_item(item_1) (complete: pinned) | the human starts it at 286 |
| s13_08 | on | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_09 | off | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_09 | on | deliver_item(item_4) | 285 | deliver_item(item_1) (complete: pinned) | the human starts it at 286 |
| s13_09 | on | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_10 | off | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_10 | on | deliver_item(item_4) | 285 | deliver_item(item_1) (complete: pinned) | the human starts it at 286 |
| s13_10 | on | coffee_break(coffee_machine_0) | 378 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s13_11 | off | coffee_break(coffee_machine_0) | 372 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s13_11 | on | coffee_break(coffee_machine_0) | 81 to 91 | deliver_item(item_2) | retraction at 92 (none(below_theta)) |
| s13_11 | on | deliver_item(item_4) | 279 | deliver_item(item_1) (complete: pinned) | the human starts it at 280 |
| s13_11 | on | coffee_break(coffee_machine_0) | 372 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s13_12 | off | coffee_break(coffee_machine_0) | 372 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s13_12 | on | coffee_break(coffee_machine_0) | 81 to 91 | deliver_item(item_2) | retraction at 92 (none(below_theta)) |
| s13_12 | on | deliver_item(item_4) | 150 to 161 | coffee_break(coffee_machine_0) | retraction at 162 (none(below_theta)) |
| s13_12 | on | deliver_item(item_4) | 279 | deliver_item(item_1) (complete: pinned) | the human starts it at 280 |
| s13_12 | on | coffee_break(coffee_machine_0) | 372 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s13_13 | off | deliver_item(item_4) | 289 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 290 |
| s13_13 | off | coffee_break(coffee_machine_0) | 357 to 378 | unmodelled | retraction at 379 (none(leader_inadequate)) |
| s13_13 | on | deliver_item(item_4) | 216 to 258 | deliver_item(item_1) (complete: pinned), coffee_break(coffee_machine_0) | retraction at 259 (none(leader_inadequate)) |
| s13_13 | on | deliver_item(item_4) | 289 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 290 |
| s13_13 | on | coffee_break(coffee_machine_0) | 357 to 378 | unmodelled | retraction at 379 (none(leader_inadequate)) |
| s13_14 | off | coffee_break(coffee_machine_0) | 309 to 330 | unmodelled | retraction at 331 (none(leader_inadequate)) |
| s13_14 | on | coffee_break(coffee_machine_0) | 81 to 91 | deliver_item(item_2) | retraction at 92 (none(below_theta)) |
| s13_14 | on | coffee_break(coffee_machine_0) | 309 to 330 | unmodelled | retraction at 331 (none(leader_inadequate)) |
| s13_15 | off | deliver_item(item_4) | 262 to 268 | coffee_break(coffee_machine_0) | retraction at 269 (none(below_theta)) |
| s13_15 | off | deliver_item(item_4) | 309 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 310 |
| s13_15 | off | coffee_break(coffee_machine_0) | 376 to 397 | unmodelled | retraction at 398 (none(leader_inadequate)) |
| s13_15 | on | deliver_item(item_4) | 216 | deliver_item(item_1) (complete: pinned) | the human starts it at 217 |
| s13_15 | on | deliver_item(item_4) | 262 to 269 | coffee_break(coffee_machine_0) | retraction at 270 (none(leader_inadequate)) |
| s13_15 | on | deliver_item(item_4) | 309 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 310 |
| s13_15 | on | coffee_break(coffee_machine_0) | 376 to 397 | unmodelled | retraction at 398 (none(leader_inadequate)) |
| s14_01 | off | none | - | - | - |
| s14_01 | on | none | - | - | - |
| s14_02 | off | none | - | - | - |
| s14_02 | on | deliver_item(item_1) | 225 | deliver_item(item_2) (complete: pinned) | the human starts it at 226 |
| s14_03 | off | none | - | - | - |
| s14_03 | on | deliver_item(item_1) | 259 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 260 |
| s14_04 | off | none | - | - | - |
| s14_04 | on | deliver_item(item_2) | 133 | coffee_break(coffee_machine_0) | retraction at 134 (none(leader_no_observation)) |
| s14_04 | on | deliver_item(item_2) | 135 to 136 | coffee_break(coffee_machine_0) | retraction at 137 (none(below_theta)) |
| s14_04 | on | deliver_item(item_1) | 233 | deliver_item(item_2) (complete: pinned) | the human starts it at 234 |
| s14_05 | off | none | - | - | - |
| s14_05 | on | deliver_item(item_2) | 135 to 146 | coffee_break(coffee_machine_0) | retraction at 147 (none(leader_inadequate)) |
| s14_05 | on | deliver_item(item_1) | 226 | deliver_item(item_2) (complete: pinned) | the human starts it at 227 |
| s14_06 | off | deliver_item(item_2) | 180 to 187 | coffee_break(coffee_machine_0) | retraction at 188 (none(leader_inadequate)) |
| s14_06 | on | deliver_item(item_2) | 180 to 187 | coffee_break(coffee_machine_0) | retraction at 188 (none(leader_inadequate)) |
| s14_06 | on | deliver_item(item_1) | 307 | deliver_item(item_2) (complete: pinned) | the human starts it at 308 |
| s14_07 | off | none | - | - | - |
| s14_07 | on | deliver_item(item_1) | 192 | deliver_item(item_2) (complete: pinned) | the human starts it at 193 |
| s14_08 | off | none | - | - | - |
| s14_08 | on | deliver_item(item_1) | 229 | ac_activation(ac_switch_0) (complete: pinned) | the human starts it at 230 |
| s14_09 | off | none | - | - | - |
| s14_09 | on | deliver_item(item_2) | 133 | ac_activation(ac_switch_0) | retraction at 134 (none(leader_no_observation)) |
| s14_09 | on | deliver_item(item_2) | 135 to 136 | ac_activation(ac_switch_0) | retraction at 137 (none(below_theta)) |
| s14_09 | on | deliver_item(item_1) | 194 | deliver_item(item_2) (complete: pinned) | the human starts it at 195 |
| s14_10 | off | none | - | - | - |
| s14_10 | on | deliver_item(item_2) | 135 to 140 | ac_activation(ac_switch_0) | retraction at 141 (none(below_theta)) |
| s14_10 | on | deliver_item(item_1) | 191 | deliver_item(item_2) (complete: pinned) | the human starts it at 192 |
| s14_11 | off | deliver_item(item_2) | 180 to 187 | ac_activation(ac_switch_0) | retraction at 188 (none(leader_inadequate)) |
| s14_11 | on | deliver_item(item_2) | 180 to 187 | ac_activation(ac_switch_0) | retraction at 188 (none(leader_inadequate)) |
| s14_11 | on | deliver_item(item_1) | 276 | deliver_item(item_2) (complete: pinned) | the human starts it at 277 |
| s14_12 | off | none | - | - | - |
| s14_12 | on | deliver_item(item_1) | 225 | deliver_item(item_2) (complete: pinned) | the human starts it at 226 |
| s14_13 | off | none | - | - | - |
| s14_13 | on | deliver_item(item_1) | 225 | deliver_item(item_2) (complete: pinned) | the human starts it at 226 |
| s14_14 | off | none | - | - | - |
| s14_14 | on | deliver_item(item_1) | 225 | deliver_item(item_2) (complete: pinned) | the human starts it at 226 |
| s14_15 | off | none | - | - | - |
| s14_15 | on | deliver_item(item_1) | 192 | deliver_item(item_2) (complete: pinned) | the human starts it at 193 |
| s14_16 | off | none | - | - | - |
| s14_16 | on | deliver_item(item_1) | 192 | deliver_item(item_2) (complete: pinned) | the human starts it at 193 |
| s14_17 | off | none | - | - | - |
| s14_17 | on | deliver_item(item_1) | 192 | deliver_item(item_2) (complete: pinned) | the human starts it at 193 |
| s14_18 | off | none | - | - | - |
| s14_18 | on | deliver_item(item_1) | 259 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 260 |
| s14_19 | off | none | - | - | - |
| s14_19 | on | deliver_item(item_1) | 180 to 239 | deliver_item(item_2) (complete: pinned), coffee_break(coffee_machine_0) | retraction at 240 (none(below_theta)) |
| s14_19 | on | deliver_item(item_1) | 259 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 260 |
| s14_20 | off | none | - | - | - |
| s14_20 | on | none | - | - | - |
| s14_21 | off | none | - | - | - |
| s14_21 | on | coffee_break(coffee_machine_0) | 221 to 227 | ac_activation(ac_switch_0) | retraction at 228 (none(below_theta)) |
| s15_01 | off | coffee_break(coffee_machine_0) | 319 to 330 | unmodelled | retraction at 331 (none(leader_inadequate)) |
| s15_01 | on | coffee_break(coffee_machine_0) | 319 to 330 | unmodelled | retraction at 331 (none(leader_inadequate)) |
| s15_02 | off | coffee_break(coffee_machine_0) | 388 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s15_02 | on | coffee_break(coffee_machine_0) | 388 to 399 | unmodelled | retraction at 400 (none(leader_inadequate)) |
| s15_03 | off | coffee_break(coffee_machine_0) | 382 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s15_03 | on | deliver_item(item_4) | 151 to 161 | coffee_break(coffee_machine_0) | retraction at 162 (none(below_theta)) |
| s15_03 | on | deliver_item(item_4) | 279 | deliver_item(item_1) (complete: pinned) | the human starts it at 280 |
| s15_03 | on | coffee_break(coffee_machine_0) | 382 to 393 | unmodelled | retraction at 394 (none(leader_inadequate)) |
| s15_04 | off | coffee_break(coffee_machine_0) | 367 to 378 | unmodelled | retraction at 379 (none(leader_inadequate)) |
| s15_04 | on | deliver_item(item_4) | 289 | coffee_break(coffee_machine_0) (complete: pinned) | the human starts it at 290 |
| s15_04 | on | coffee_break(coffee_machine_0) | 378 | unmodelled | retraction at 379 (none(leader_inadequate)) |
| s15_05 | off | coffee_break(coffee_machine_0) | 394 to 405 | unmodelled | retraction at 406 (none(leader_inadequate)) |
| s15_05 | on | deliver_item(item_2) | 94 | coffee_break(coffee_machine_0) | retraction at 95 (none(leader_no_observation)) |
| s15_05 | on | deliver_item(item_2) | 96 to 99 | coffee_break(coffee_machine_0) | retraction at 100 (none(below_theta)) |
| s15_05 | on | coffee_break(coffee_machine_0) | 394 to 405 | unmodelled | retraction at 406 (none(leader_inadequate)) |
| s15_06 | off | coffee_break(coffee_machine_0) | 389 to 400 | unmodelled | retraction at 401 (none(leader_inadequate)) |
| s15_06 | on | deliver_item(item_2) | 96 to 103 | coffee_break(coffee_machine_0) | retraction at 104 (none(below_theta)) |
| s15_06 | on | coffee_break(coffee_machine_0) | 389 to 400 | unmodelled | retraction at 401 (none(leader_inadequate)) |
| s15_07 | off | deliver_item(item_2) | 123 to 130 | coffee_break(coffee_machine_0) | retraction at 131 (none(leader_inadequate)) |
| s15_07 | off | coffee_break(coffee_machine_0) | 440 to 451 | unmodelled | retraction at 452 (none(leader_inadequate)) |
| s15_07 | on | deliver_item(item_2) | 123 to 130 | coffee_break(coffee_machine_0) | retraction at 131 (none(leader_inadequate)) |
| s15_07 | on | deliver_item(item_4) | 334 | deliver_item(item_1) (complete: pinned) | the human starts it at 335 |
| s15_07 | on | coffee_break(coffee_machine_0) | 440 to 451 | unmodelled | retraction at 452 (none(leader_inadequate)) |
| s15_08 | off | coffee_break(coffee_machine_0) | 379 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_08 | on | deliver_item(item_4) | 276 | deliver_item(item_1) (complete: pinned) | the human starts it at 277 |
| s15_08 | on | coffee_break(coffee_machine_0) | 369 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_09 | off | coffee_break(coffee_machine_0) | 335 to 346 | unmodelled | retraction at 347 (none(leader_inadequate)) |
| s15_09 | on | deliver_item(item_4) | 229 | deliver_item(item_1) (complete: pinned) | the human starts it at 230 |
| s15_09 | on | coffee_break(coffee_machine_0) | 324 to 346 | unmodelled | retraction at 347 (none(leader_inadequate)) |
| s15_10 | off | coffee_break(coffee_machine_0) | 333 to 344 | unmodelled | retraction at 345 (none(leader_inadequate)) |
| s15_10 | on | deliver_item(item_4) | 263 | ac_activation(ac_switch_0) (complete: pinned) | the human starts it at 264 |
| s15_10 | on | coffee_break(coffee_machine_0) | 322 to 344 | unmodelled | retraction at 345 (none(leader_inadequate)) |
| s15_11 | off | coffee_break(coffee_machine_0) | 399 to 410 | unmodelled | retraction at 411 (none(leader_inadequate)) |
| s15_11 | on | deliver_item(item_2) | 94 | ac_activation(ac_switch_0) | retraction at 95 (none(leader_no_observation)) |
| s15_11 | on | deliver_item(item_2) | 96 to 98 | ac_activation(ac_switch_0) | retraction at 99 (none(below_theta)) |
| s15_11 | on | deliver_item(item_4) | 111 to 118 | ac_activation(ac_switch_0) | retraction at 119 (none(leader_inadequate)) |
| s15_11 | on | deliver_item(item_4) | 296 | deliver_item(item_1) (complete: pinned) | the human starts it at 297 |
| s15_11 | on | coffee_break(coffee_machine_0) | 389 to 410 | unmodelled | retraction at 411 (none(leader_inadequate)) |
| s15_12 | off | coffee_break(coffee_machine_0) | 383 to 394 | unmodelled | retraction at 395 (none(leader_inadequate)) |
| s15_12 | on | deliver_item(item_2) | 96 to 108 | ac_activation(ac_switch_0) | retraction at 109 (none(leader_inadequate)) |
| s15_12 | on | deliver_item(item_4) | 278 | deliver_item(item_1) (complete: pinned) | the human starts it at 279 |
| s15_12 | on | coffee_break(coffee_machine_0) | 373 to 394 | unmodelled | retraction at 395 (none(leader_inadequate)) |
| s15_13 | off | deliver_item(item_2) | 123 to 130 | ac_activation(ac_switch_0) | retraction at 131 (none(leader_inadequate)) |
| s15_13 | off | coffee_break(coffee_machine_0) | 411 to 422 | unmodelled | retraction at 423 (none(leader_inadequate)) |
| s15_13 | on | deliver_item(item_2) | 123 to 130 | ac_activation(ac_switch_0) | retraction at 131 (none(leader_inadequate)) |
| s15_13 | on | deliver_item(item_4) | 308 | deliver_item(item_1) (complete: pinned) | the human starts it at 309 |
| s15_13 | on | coffee_break(coffee_machine_0) | 401 to 422 | unmodelled | retraction at 423 (none(leader_inadequate)) |
| s15_14 | off | coffee_break(coffee_machine_0) | 379 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_14 | on | deliver_item(item_4) | 276 | deliver_item(item_1) (complete: pinned) | the human starts it at 277 |
| s15_14 | on | coffee_break(coffee_machine_0) | 369 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_15 | off | coffee_break(coffee_machine_0) | 379 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_15 | on | deliver_item(item_4) | 276 | deliver_item(item_1) (complete: pinned) | the human starts it at 277 |
| s15_15 | on | coffee_break(coffee_machine_0) | 369 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_16 | off | coffee_break(coffee_machine_0) | 379 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_16 | on | deliver_item(item_4) | 276 | deliver_item(item_1) (complete: pinned) | the human starts it at 277 |
| s15_16 | on | coffee_break(coffee_machine_0) | 369 to 390 | unmodelled | retraction at 391 (none(leader_inadequate)) |
| s15_17 | off | coffee_break(coffee_machine_0) | 367 to 378 | unmodelled | retraction at 379 (none(leader_inadequate)) |
| s15_17 | on | none | - | - | - |
| s15_18 | off | coffee_break(coffee_machine_0) | 319 to 330 | unmodelled | retraction at 331 (none(leader_inadequate)) |
| s15_18 | on | none | - | - | - |
| s15_19 | off | coffee_break(coffee_machine_0) | 333 to 344 | unmodelled | retraction at 345 (none(leader_inadequate)) |
| s15_19 | on | deliver_item(item_4) | 216 to 261 | deliver_item(item_1) (complete: pinned), ac_activation(ac_switch_0) | retraction at 262 (none(leader_no_observation)) |
| s15_19 | on | deliver_item(item_4) | 263 | ac_activation(ac_switch_0) (complete: pinned) | the human starts it at 264 |
| s15_19 | on | coffee_break(coffee_machine_0) | 322 to 344 | unmodelled | retraction at 345 (none(leader_inadequate)) |
| s15_20 | off | coffee_break(coffee_machine_0) | 333 to 344 | unmodelled | retraction at 345 (none(leader_inadequate)) |
| s15_20 | on | coffee_break(coffee_machine_0) | 322 to 344 | unmodelled | retraction at 345 (none(leader_inadequate)) |
| s15_21 | off | none | - | - | - |
| s15_21 | on | deliver_item(item_4) | 216 | deliver_item(item_1) (complete: pinned) | the human starts it at 217 |

## Appendix B: the directions' readings (`analysis/kitting/irb/tk2/directions.py actual.csv`)

### Per true stretch, off and every on side of the same script (within one script)

Side: the level of the case's foreseeable task (a foreseeable stretch: its own; a delivery: its rivals') on the ticks from the stretch's start to the later of the two admissions. `live`: deliveries live at the start.

| script (off from) | true hypothesis | ticks | live | off: θ / admitted | on, per scenario: side → θ / admitted |
|---|---|---|---|---|---|
| s13_01 | deliver_item(item_3) | 0 to 66 | 4 | 26 (26) / 26 (26) | s13_01 [coffee_break ordinary] → 26 (26) / 26 (26); s13_14 [coffee_break raised] → 27 (27) / 27 (27) |
| s13_01 | deliver_item(item_2) | 67 to 123 | 3 | 97 (30) / 97 (30) | s13_01 [coffee_break ordinary] → 87 (20) / 87 (20); s13_14 [coffee_break raised] → 102 (35) / 102 (35) |
| s13_01 | deliver_item(item_1) | 124 to 216 | 2 | 161 (37) / 161 (37) | s13_01 [coffee_break ordinary] → 161 (37) / 161 (37); s13_14 [coffee_break raised] → 162 (38) / 162 (38) |
| s13_01 | deliver_item(item_4) | 217 to 308 | 1 | 248 (31) / 248 (31) | s13_01 [coffee_break raised] → 253 (36) / 253 (36); s13_14 [coffee_break raised] → 253 (36) / 253 (36) |
| s13_02 | deliver_item(item_3) | 0 to 66 | 4 | 26 (26) / 26 (26) | s13_02 [coffee_break ordinary] → 26 (26) / 26 (26); s13_08 [coffee_break ordinary] → 26 (26) / 26 (26); s13_09 [coffee_break ordinary] → 26 (26) / 26 (26); s13_10 [coffee_break ordinary] → 26 (26) / 26 (26) |
| s13_02 | coffee_break(coffee_machine_0) | 67 to 140 | 3 | 101 (34) / 101 (34) | s13_02 [ordinary] → 117 (50) / 117 (50); s13_08 [raised] → 82 (15) / 82 (15); s13_09 [ordinary, raised] → 90 (23) / 90 (23); s13_10 [ordinary] → 117 (50) / 117 (50) |
| s13_02 | deliver_item(item_2) | 141 to 192 | 3 | 149 (8) / 149 (8) | s13_02 [coffee_break suppressed] → 149 (8) / 149 (8); s13_08 [coffee_break suppressed] → 149 (8) / 149 (8); s13_09 [coffee_break suppressed] → 149 (8) / 149 (8); s13_10 [coffee_break suppressed] → 149 (8) / 149 (8) |
| s13_02 | deliver_item(item_1) | 193 to 285 | 2 | 230 (37) / 230 (37) | s13_02 [coffee_break raised/suppressed] → 231 (38) / 231 (38); s13_08 [coffee_break ordinary/suppressed] → 230 (37) / 230 (37); s13_09 [coffee_break ordinary/suppressed] → 230 (37) / 230 (37); s13_10 [coffee_break ordinary/suppressed] → 230 (37) / 230 (37) |
| s13_02 | deliver_item(item_4) | 286 to 377 | 1 | 317 (31) / 317 (31) | s13_02 [coffee_break ordinary/raised] → 300 (14) / 300 (14); s13_08 [coffee_break ordinary] → 286 (0) / 286 (0); s13_09 [coffee_break ordinary] → 286 (0) / 286 (0); s13_10 [coffee_break ordinary] → 286 (0) / 286 (0) |
| s13_03 | deliver_item(item_3) | 0 to 66 | 4 | 26 (26) / 26 (26) | s13_03 [coffee_break ordinary] → 26 (26) / 26 (26); s13_11 [coffee_break ordinary] → 26 (26) / 26 (26); s13_12 [coffee_break ordinary] → 26 (26) / 26 (26) |
| s13_03 | deliver_item(item_2) | 67 to 123 | 3 | 97 (30) / 97 (30) | s13_03 [coffee_break ordinary] → 87 (20) / 87 (20); s13_11 [coffee_break raised] → 102 (35) / 102 (35); s13_12 [coffee_break raised] → 102 (35) / 102 (35) |
| s13_03 | coffee_break(coffee_machine_0) | 124 to 197 | 2 | 158 (34) / 158 (34) | s13_03 [ordinary] → 175 (51) / 175 (51); s13_11 [raised] → 138 (14) / 138 (14); s13_12 [ordinary, raised] → 138 (14) / 138 (14) |
| s13_03 | deliver_item(item_1) | 198 to 279 | 2 | 219 (21) / 219 (21) | s13_03 [coffee_break suppressed] → 219 (21) / 219 (21); s13_11 [coffee_break suppressed] → 219 (21) / 219 (21); s13_12 [coffee_break suppressed] → 219 (21) / 219 (21) |
| s13_03 | deliver_item(item_4) | 280 to 371 | 1 | 311 (31) / 311 (31) | s13_03 [coffee_break ordinary/raised/suppressed] → 280 (0) / 280 (0); s13_11 [coffee_break ordinary/suppressed] → 280 (0) / 280 (0); s13_12 [coffee_break ordinary/suppressed] → 280 (0) / 280 (0) |
| s13_04 | deliver_item(item_3) | 0 to 66 | 4 | 26 (26) / 26 (26) | s13_04 [coffee_break ordinary] → 26 (26) / 26 (26); s13_13 [coffee_break ordinary] → 26 (26) / 26 (26) |
| s13_04 | deliver_item(item_2) | 67 to 123 | 3 | 97 (30) / 97 (30) | s13_04 [coffee_break ordinary] → 87 (20) / 87 (20); s13_13 [coffee_break ordinary] → 87 (20) / 87 (20) |
| s13_04 | deliver_item(item_1) | 124 to 216 | 2 | 161 (37) / 161 (37) | s13_04 [coffee_break ordinary] → 161 (37) / 161 (37); s13_13 [coffee_break ordinary] → 161 (37) / 161 (37) |
| s13_04 | coffee_break(coffee_machine_0) | 217 to 289 | 1 | 249 (32) / 249 (32) | s13_04 [raised] → 238 (21) / 238 (21); s13_13 [ordinary] → 271 (54) / 271 (54) |
| s13_04 | deliver_item(item_4) | 290 to 356 | 1 | 295 (5) / 295 (5) | s13_04 [coffee_break suppressed] → 290 (0) / 290 (0); s13_13 [coffee_break suppressed] → 290 (0) / 290 (0) |
| s13_05 | deliver_item(item_3) | 0 to 66 | 4 | 26 (26) / 26 (26) | s13_05 [coffee_break ordinary] → 26 (26) / 26 (26) |
| s13_05 | deliver_item(item_2) | 67 to 93 | 3 | never / never | s13_05 [coffee_break ordinary] → 87 (20) / 87 (20) |
| s13_05 | coffee_break(coffee_machine_0) | 94 to 146 | 3 | 103 (9) / 103 (9) | s13_05 [ordinary] → 120 (26) / 120 (26) |
| s13_05 | deliver_item(item_2) | 147 to 198 | 3 | 156 (9) / 156 (9) | s13_05 [coffee_break suppressed] → 155 (8) / 155 (8) |
| s13_05 | deliver_item(item_1) | 199 to 291 | 2 | 236 (37) / 236 (37) | s13_05 [coffee_break raised/suppressed] → 237 (38) / 237 (38) |
| s13_05 | deliver_item(item_4) | 292 to 383 | 1 | 323 (31) / 323 (31) | s13_05 [coffee_break ordinary/raised] → 300 (8) / 300 (8) |
| s13_06 | deliver_item(item_3) | 0 to 66 | 4 | 26 (26) / 26 (26) | s13_06 [coffee_break ordinary] → 26 (26) / 26 (26) |
| s13_06 | deliver_item(item_2) | 67 to 95 | 3 | never / never | s13_06 [coffee_break ordinary] → 87 (20) / 87 (20) |
| s13_06 | coffee_break(coffee_machine_0) | 96 to 148 | 3 | 104 (8) / 104 (8) | s13_06 [ordinary] → 112 (16) / 112 (16) |
| s13_06 | deliver_item(item_2) | 149 to 193 | 3 | 170 (21) / 170 (21) | s13_06 [coffee_break suppressed] → 170 (21) / 170 (21) |
| s13_06 | deliver_item(item_1) | 194 to 286 | 2 | 231 (37) / 231 (37) | s13_06 [coffee_break suppressed] → 231 (37) / 231 (37) |
| s13_06 | deliver_item(item_4) | 287 to 378 | 1 | 318 (31) / 318 (31) | s13_06 [coffee_break ordinary/raised] → 300 (13) / 300 (13) |
| s13_07 | deliver_item(item_3) | 0 to 66 | 4 | 26 (26) / 26 (26) | s13_07 [coffee_break ordinary] → 26 (26) / 26 (26) |
| s13_07 | deliver_item(item_2) | 67 to 121 | 3 | 97 (30) / 97 (30) | s13_07 [coffee_break ordinary] → 87 (20) / 87 (20) |
| s13_07 | coffee_break(coffee_machine_0) | 122 to 195 | 3 | 153 (31) / 163 (41) | s13_07 [ordinary] → 160 (38) / 163 (41) |
| s13_07 | deliver_item(item_2) | 196 to 240 | 3 | 217 (21) / 217 (21) | s13_07 [coffee_break suppressed] → 217 (21) / 217 (21) |
| s13_07 | deliver_item(item_1) | 241 to 334 | 2 | 278 (37) / 278 (37) | s13_07 [coffee_break suppressed] → 278 (37) / 278 (37) |
| s13_07 | deliver_item(item_4) | 335 to 428 | 1 | 367 (32) / 367 (32) | s13_07 [coffee_break ordinary] → 335 (0) / 335 (0) |
| s13_15 | deliver_item(item_3) | 0 to 66 | 4 | 26 (26) / 26 (26) | s13_15 [coffee_break ordinary] → 26 (26) / 26 (26) |
| s13_15 | deliver_item(item_2) | 67 to 123 | 3 | 97 (30) / 97 (30) | s13_15 [coffee_break ordinary] → 87 (20) / 87 (20) |
| s13_15 | deliver_item(item_1) | 124 to 216 | 2 | 161 (37) / 161 (37) | s13_15 [coffee_break ordinary] → 161 (37) / 161 (37) |
| s13_15 | deliver_item(item_4) | 217 to 260 | 1 | 248 (31) / 248 (31) | s13_15 [coffee_break ordinary] → 217 (0) / 217 (0) |
| s13_15 | coffee_break(coffee_machine_0) | 261 to 309 | 1 | 274 (13) / 277 (16) | s13_15 [ordinary] → 291 (30) / 291 (30) |
| s13_15 | deliver_item(item_4) | 310 to 375 | 1 | 315 (5) / 315 (5) | s13_15 [coffee_break suppressed] → 310 (0) / 310 (0) |
| s14_01 | deliver_item(item_0) | 0 to 88 | 3 | 50 (50) / 50 (50) | s14_01 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48); s14_20 [coffee_break raised, ac_activation ordinary] → 51 (51) / 51 (51) |
| s14_01 | deliver_item(item_2) | 89 to 180 | 2 | 138 (49) / 138 (49) | s14_01 [coffee_break ordinary, ac_activation ordinary] → 129 (40) / 129 (40); s14_20 [coffee_break raised, ac_activation ordinary] → 139 (50) / 139 (50) |
| s14_01 | deliver_item(item_1) | 181 to 282 | 1 | 232 (51) / 232 (51) | s14_01 [coffee_break raised, ac_activation ordinary] → 234 (53) / 234 (53); s14_20 [coffee_break raised, ac_activation ordinary] → 234 (53) / 234 (53) |
| s14_02 | deliver_item(item_0) | 0 to 88 | 3 | 50 (50) / 50 (50) | s14_02 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48); s14_12 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48); s14_13 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48); s14_14 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48) |
| s14_02 | coffee_break(coffee_machine_0) | 89 to 166 | 2 | 143 (54) / 143 (54) | s14_02 [ordinary] → 157 (68) / 157 (68); s14_12 [raised] → 129 (40) / 129 (40); s14_13 [ordinary, raised] → 129 (40) / 129 (40); s14_14 [ordinary, raised] → 150 (61) / 150 (61) |
| s14_02 | deliver_item(item_2) | 167 to 225 | 2 | 177 (10) / 177 (10) | s14_02 [coffee_break suppressed, ac_activation ordinary] → 171 (4) / 171 (4); s14_12 [coffee_break suppressed, ac_activation ordinary] → 171 (4) / 171 (4); s14_13 [coffee_break suppressed, ac_activation ordinary] → 171 (4) / 171 (4); s14_14 [coffee_break suppressed, ac_activation ordinary] → 171 (4) / 171 (4) |
| s14_02 | deliver_item(item_1) | 226 to 325 | 1 | 277 (51) / 277 (51) | s14_02 [coffee_break raised/suppressed, ac_activation ordinary] → 226 (0) / 226 (0); s14_12 [coffee_break ordinary/suppressed, ac_activation ordinary] → 226 (0) / 226 (0); s14_13 [coffee_break ordinary/suppressed, ac_activation ordinary] → 226 (0) / 226 (0); s14_14 [coffee_break ordinary/suppressed, ac_activation ordinary] → 226 (0) / 226 (0) |
| s14_03 | deliver_item(item_0) | 0 to 88 | 3 | 50 (50) / 50 (50) | s14_03 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48); s14_18 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48); s14_19 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48) |
| s14_03 | deliver_item(item_2) | 89 to 180 | 2 | 138 (49) / 138 (49) | s14_03 [coffee_break ordinary, ac_activation ordinary] → 129 (40) / 129 (40); s14_18 [coffee_break raised, ac_activation ordinary] → 139 (50) / 139 (50); s14_19 [coffee_break ordinary, ac_activation ordinary] → 129 (40) / 129 (40) |
| s14_03 | coffee_break(coffee_machine_0) | 181 to 259 | 1 | 235 (54) / 235 (54) | s14_03 [raised] → 226 (45) / 226 (45); s14_18 [raised] → 226 (45) / 226 (45); s14_19 [ordinary] → 252 (71) / 252 (71) |
| s14_03 | deliver_item(item_1) | 260 to 318 | 1 | 269 (9) / 269 (9) | s14_03 [coffee_break suppressed, ac_activation ordinary] → 260 (0) / 260 (0); s14_18 [coffee_break suppressed, ac_activation ordinary] → 260 (0) / 260 (0); s14_19 [coffee_break suppressed, ac_activation ordinary] → 260 (0) / 260 (0) |
| s14_04 | deliver_item(item_0) | 0 to 88 | 3 | 50 (50) / 50 (50) | s14_04 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48) |
| s14_04 | deliver_item(item_2) | 89 to 132 | 2 | never / never | s14_04 [coffee_break ordinary, ac_activation ordinary] → 129 (40) / 129 (40) |
| s14_04 | coffee_break(coffee_machine_0) | 133 to 174 | 2 | 149 (16) / 149 (16) | s14_04 [ordinary] → 162 (29) / 162 (29) |
| s14_04 | deliver_item(item_2) | 175 to 233 | 2 | 187 (12) / 187 (12) | s14_04 [coffee_break suppressed, ac_activation ordinary] → 179 (4) / 179 (4) |
| s14_04 | deliver_item(item_1) | 234 to 333 | 1 | 285 (51) / 285 (51) | s14_04 [coffee_break raised/suppressed, ac_activation ordinary] → 234 (0) / 234 (0) |
| s14_05 | deliver_item(item_0) | 0 to 88 | 3 | 50 (50) / 50 (50) | s14_05 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48) |
| s14_05 | deliver_item(item_2) | 89 to 134 | 2 | never / never | s14_05 [coffee_break ordinary, ac_activation ordinary] → 129 (40) / 129 (40) |
| s14_05 | coffee_break(coffee_machine_0) | 135 to 176 | 2 | 150 (15) / 150 (15) | s14_05 [ordinary] → 163 (28) / 163 (28) |
| s14_05 | deliver_item(item_2) | 177 to 226 | 2 | 187 (10) / 187 (10) | s14_05 [coffee_break suppressed, ac_activation ordinary] → 184 (7) / 184 (7) |
| s14_05 | deliver_item(item_1) | 227 to 328 | 1 | 278 (51) / 278 (51) | s14_05 [coffee_break raised/suppressed, ac_activation ordinary] → 227 (0) / 227 (0) |
| s14_06 | deliver_item(item_0) | 0 to 88 | 3 | 50 (50) / 50 (50) | s14_06 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48) |
| s14_06 | deliver_item(item_2) | 89 to 178 | 2 | 138 (49) / 138 (49) | s14_06 [coffee_break ordinary, ac_activation ordinary] → 129 (40) / 129 (40) |
| s14_06 | coffee_break(coffee_machine_0) | 179 to 257 | 2 | 231 (52) / 231 (52) | s14_06 [raised] → 224 (45) / 225 (46) |
| s14_06 | deliver_item(item_2) | 258 to 307 | 2 | 267 (9) / 267 (9) | s14_06 [coffee_break suppressed, ac_activation ordinary] → 265 (7) / 265 (7) |
| s14_06 | deliver_item(item_1) | 308 to 409 | 1 | 359 (51) / 359 (51) | s14_06 [coffee_break ordinary/suppressed, ac_activation ordinary] → 308 (0) / 308 (0) |
| s14_07 | deliver_item(item_0) | 0 to 88 | 3 | 50 (50) / 50 (50) | s14_07 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48); s14_15 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48); s14_16 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48); s14_17 [coffee_break ordinary, ac_activation raised] → 49 (49) / 49 (49) |
| s14_07 | ac_activation(ac_switch_0) | 89 to 137 | 2 | never / never | s14_07 [ordinary] → never / never; s14_15 [raised] → never / never; s14_16 [ordinary] → never / never; s14_17 [raised] → never / never |
| s14_07 | deliver_item(item_2) | 138 to 192 | 2 | 148 (10) / 148 (10) | s14_07 [coffee_break ordinary, ac_activation suppressed] → 142 (4) / 142 (4); s14_15 [coffee_break ordinary, ac_activation suppressed] → 142 (4) / 142 (4); s14_16 [coffee_break ordinary, ac_activation suppressed] → 142 (4) / 142 (4); s14_17 [coffee_break ordinary, ac_activation suppressed] → 142 (4) / 142 (4) |
| s14_07 | deliver_item(item_1) | 193 to 294 | 1 | 244 (51) / 244 (51) | s14_07 [coffee_break ordinary, ac_activation suppressed] → 193 (0) / 193 (0); s14_15 [coffee_break ordinary, ac_activation suppressed] → 193 (0) / 193 (0); s14_16 [coffee_break ordinary, ac_activation suppressed] → 193 (0) / 193 (0); s14_17 [coffee_break ordinary, ac_activation suppressed] → 193 (0) / 193 (0) |
| s14_08 | deliver_item(item_0) | 0 to 88 | 3 | 50 (50) / 50 (50) | s14_08 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48); s14_21 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48) |
| s14_08 | deliver_item(item_2) | 89 to 180 | 2 | 138 (49) / 138 (49) | s14_08 [coffee_break ordinary, ac_activation ordinary] → 129 (40) / 129 (40); s14_21 [coffee_break ordinary, ac_activation ordinary] → 129 (40) / 129 (40) |
| s14_08 | ac_activation(ac_switch_0) | 181 to 229 | 1 | never / never | s14_08 [raised] → never / never; s14_21 [ordinary] → never / never |
| s14_08 | deliver_item(item_1) | 230 to 293 | 1 | 242 (12) / 242 (12) | s14_08 [coffee_break ordinary, ac_activation suppressed] → 230 (0) / 230 (0); s14_21 [coffee_break raised, ac_activation suppressed] → 245 (15) / 245 (15) |
| s14_09 | deliver_item(item_0) | 0 to 88 | 3 | 50 (50) / 50 (50) | s14_09 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48) |
| s14_09 | deliver_item(item_2) | 89 to 132 | 2 | never / never | s14_09 [coffee_break ordinary, ac_activation ordinary] → 129 (40) / 129 (40) |
| s14_09 | ac_activation(ac_switch_0) | 133 to 140 | 2 | never / never | s14_09 [ordinary] → never / never |
| s14_09 | deliver_item(item_2) | 141 to 194 | 2 | 151 (10) / 151 (10) | s14_09 [coffee_break ordinary, ac_activation suppressed] → 149 (8) / 149 (8) |
| s14_09 | deliver_item(item_1) | 195 to 296 | 1 | 246 (51) / 246 (51) | s14_09 [coffee_break ordinary, ac_activation suppressed] → 195 (0) / 195 (0) |
| s14_10 | deliver_item(item_0) | 0 to 88 | 3 | 50 (50) / 50 (50) | s14_10 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48) |
| s14_10 | deliver_item(item_2) | 89 to 134 | 2 | never / never | s14_10 [coffee_break ordinary, ac_activation ordinary] → 129 (40) / 129 (40) |
| s14_10 | ac_activation(ac_switch_0) | 135 to 142 | 2 | never / never | s14_10 [ordinary] → never / never |
| s14_10 | deliver_item(item_2) | 143 to 191 | 2 | 151 (8) / 151 (8) | s14_10 [coffee_break ordinary, ac_activation suppressed] → 149 (6) / 149 (6) |
| s14_10 | deliver_item(item_1) | 192 to 293 | 1 | 243 (51) / 243 (51) | s14_10 [coffee_break ordinary, ac_activation suppressed] → 192 (0) / 192 (0) |
| s14_11 | deliver_item(item_0) | 0 to 88 | 3 | 50 (50) / 50 (50) | s14_11 [coffee_break ordinary, ac_activation ordinary] → 48 (48) / 48 (48) |
| s14_11 | deliver_item(item_2) | 89 to 178 | 2 | 138 (49) / 138 (49) | s14_11 [coffee_break ordinary, ac_activation ordinary] → 129 (40) / 129 (40) |
| s14_11 | ac_activation(ac_switch_0) | 179 to 227 | 2 | never / never | s14_11 [raised] → never / never |
| s14_11 | deliver_item(item_2) | 228 to 276 | 2 | 236 (8) / 236 (8) | s14_11 [coffee_break ordinary, ac_activation suppressed] → 234 (6) / 234 (6) |
| s14_11 | deliver_item(item_1) | 277 to 378 | 1 | 328 (51) / 328 (51) | s14_11 [coffee_break ordinary, ac_activation suppressed] → 277 (0) / 277 (0) |
| s15_01 | deliver_item(item_3) | 0 to 66 | 4 | 28 (28) / 28 (28) | s15_01 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26); s15_18 [coffee_break ordinary, ac_activation raised] → 30 (30) / 30 (30) |
| s15_01 | deliver_item(item_2) | 67 to 123 | 3 | 97 (30) / 97 (30) | s15_01 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20); s15_18 [coffee_break ordinary, ac_activation raised] → 90 (23) / 90 (23) |
| s15_01 | deliver_item(item_1) | 124 to 216 | 2 | 171 (47) / 171 (47) | s15_01 [coffee_break ordinary, ac_activation ordinary] → 162 (38) / 162 (38); s15_18 [coffee_break ordinary, ac_activation raised] → 171 (47) / 171 (47) |
| s15_01 | deliver_item(item_4) | 217 to 308 | 1 | 262 (45) / 262 (45) | s15_01 [coffee_break raised, ac_activation ordinary] → 254 (37) / 254 (37); s15_18 [coffee_break ordinary, ac_activation raised] → 256 (39) / 256 (39) |
| s15_02 | deliver_item(item_3) | 0 to 66 | 4 | 28 (28) / 28 (28) | s15_02 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26) |
| s15_02 | coffee_break(coffee_machine_0) | 67 to 140 | 3 | 103 (36) / 103 (36) | s15_02 [ordinary] → 117 (50) / 117 (50) |
| s15_02 | deliver_item(item_2) | 141 to 192 | 3 | 150 (9) / 150 (9) | s15_02 [coffee_break suppressed, ac_activation ordinary] → 149 (8) / 149 (8) |
| s15_02 | deliver_item(item_1) | 193 to 285 | 2 | 240 (47) / 240 (47) | s15_02 [coffee_break raised/suppressed, ac_activation ordinary] → 232 (39) / 232 (39) |
| s15_02 | deliver_item(item_4) | 286 to 377 | 1 | 331 (45) / 331 (45) | s15_02 [coffee_break ordinary/raised, ac_activation ordinary] → 300 (14) / 300 (14) |
| s15_03 | deliver_item(item_3) | 0 to 66 | 4 | 28 (28) / 28 (28) | s15_03 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26) |
| s15_03 | deliver_item(item_2) | 67 to 123 | 3 | 97 (30) / 97 (30) | s15_03 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20) |
| s15_03 | coffee_break(coffee_machine_0) | 124 to 197 | 2 | 160 (36) / 160 (36) | s15_03 [ordinary] → 176 (52) / 176 (52) |
| s15_03 | deliver_item(item_1) | 198 to 279 | 2 | 227 (29) / 227 (29) | s15_03 [coffee_break suppressed, ac_activation ordinary] → 219 (21) / 219 (21) |
| s15_03 | deliver_item(item_4) | 280 to 371 | 1 | 325 (45) / 325 (45) | s15_03 [coffee_break ordinary/raised/suppressed, ac_activation ordinary] → 280 (0) / 280 (0) |
| s15_04 | deliver_item(item_3) | 0 to 66 | 4 | 28 (28) / 28 (28) | s15_04 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26); s15_17 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26) |
| s15_04 | deliver_item(item_2) | 67 to 123 | 3 | 97 (30) / 97 (30) | s15_04 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20); s15_17 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20) |
| s15_04 | deliver_item(item_1) | 124 to 216 | 2 | 171 (47) / 171 (47) | s15_04 [coffee_break ordinary, ac_activation ordinary] → 162 (38) / 162 (38); s15_17 [coffee_break ordinary, ac_activation ordinary/raised] → 171 (47) / 171 (47) |
| s15_04 | coffee_break(coffee_machine_0) | 217 to 289 | 1 | 252 (35) / 252 (35) | s15_04 [raised] → 238 (21) / 238 (21); s15_17 [raised] → 243 (26) / 243 (26) |
| s15_04 | deliver_item(item_4) | 290 to 356 | 1 | 313 (23) / 313 (23) | s15_04 [coffee_break suppressed, ac_activation ordinary] → 290 (0) / 290 (0); s15_17 [coffee_break suppressed, ac_activation raised] → 310 (20) / 310 (20) |
| s15_05 | deliver_item(item_3) | 0 to 66 | 4 | 28 (28) / 28 (28) | s15_05 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26) |
| s15_05 | deliver_item(item_2) | 67 to 93 | 3 | never / never | s15_05 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20) |
| s15_05 | coffee_break(coffee_machine_0) | 94 to 146 | 3 | 104 (10) / 104 (10) | s15_05 [ordinary] → 120 (26) / 120 (26) |
| s15_05 | deliver_item(item_2) | 147 to 198 | 3 | 157 (10) / 157 (10) | s15_05 [coffee_break suppressed, ac_activation ordinary] → 155 (8) / 155 (8) |
| s15_05 | deliver_item(item_1) | 199 to 291 | 2 | 246 (47) / 246 (47) | s15_05 [coffee_break raised/suppressed, ac_activation ordinary] → 238 (39) / 238 (39) |
| s15_05 | deliver_item(item_4) | 292 to 383 | 1 | 337 (45) / 337 (45) | s15_05 [coffee_break ordinary/raised, ac_activation ordinary] → 300 (8) / 300 (8) |
| s15_06 | deliver_item(item_3) | 0 to 66 | 4 | 28 (28) / 28 (28) | s15_06 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26) |
| s15_06 | deliver_item(item_2) | 67 to 95 | 3 | never / never | s15_06 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20) |
| s15_06 | coffee_break(coffee_machine_0) | 96 to 148 | 3 | 104 (8) / 104 (8) | s15_06 [ordinary] → 112 (16) / 112 (16) |
| s15_06 | deliver_item(item_2) | 149 to 193 | 3 | 170 (21) / 170 (21) | s15_06 [coffee_break suppressed, ac_activation ordinary] → 170 (21) / 170 (21) |
| s15_06 | deliver_item(item_1) | 194 to 286 | 2 | 241 (47) / 241 (47) | s15_06 [coffee_break raised/suppressed, ac_activation ordinary] → 232 (38) / 232 (38) |
| s15_06 | deliver_item(item_4) | 287 to 378 | 1 | 332 (45) / 332 (45) | s15_06 [coffee_break ordinary/raised, ac_activation ordinary] → 300 (13) / 300 (13) |
| s15_07 | deliver_item(item_3) | 0 to 66 | 4 | 28 (28) / 28 (28) | s15_07 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26) |
| s15_07 | deliver_item(item_2) | 67 to 121 | 3 | 97 (30) / 97 (30) | s15_07 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20) |
| s15_07 | coffee_break(coffee_machine_0) | 122 to 195 | 3 | 153 (31) / 163 (41) | s15_07 [ordinary] → 160 (38) / 163 (41) |
| s15_07 | deliver_item(item_2) | 196 to 240 | 3 | 217 (21) / 217 (21) | s15_07 [coffee_break suppressed, ac_activation ordinary] → 217 (21) / 217 (21) |
| s15_07 | deliver_item(item_1) | 241 to 334 | 2 | 288 (47) / 288 (47) | s15_07 [coffee_break raised/suppressed, ac_activation ordinary] → 278 (37) / 278 (37) |
| s15_07 | deliver_item(item_4) | 335 to 428 | 1 | 381 (46) / 381 (46) | s15_07 [coffee_break ordinary, ac_activation ordinary] → 335 (0) / 335 (0) |
| s15_08 | deliver_item(item_3) | 0 to 66 | 4 | 28 (28) / 28 (28) | s15_08 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26); s15_14 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26); s15_15 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26); s15_16 [coffee_break ordinary, ac_activation raised] → 30 (30) / 30 (30) |
| s15_08 | ac_activation(ac_switch_0) | 67 to 114 | 3 | never / never | s15_08 [ordinary] → never / never; s15_14 [raised] → never / never; s15_15 [ordinary] → never / never; s15_16 [raised] → never / never |
| s15_08 | deliver_item(item_2) | 115 to 183 | 3 | 135 (20) / 135 (20) | s15_08 [coffee_break ordinary, ac_activation suppressed] → 125 (10) / 125 (10); s15_14 [coffee_break ordinary, ac_activation suppressed] → 125 (10) / 125 (10); s15_15 [coffee_break ordinary, ac_activation suppressed] → 125 (10) / 125 (10); s15_16 [coffee_break ordinary, ac_activation suppressed] → 125 (10) / 125 (10) |
| s15_08 | deliver_item(item_1) | 184 to 276 | 2 | 231 (47) / 231 (47) | s15_08 [coffee_break ordinary, ac_activation suppressed] → 221 (37) / 221 (37); s15_14 [coffee_break ordinary, ac_activation suppressed] → 221 (37) / 221 (37); s15_15 [coffee_break ordinary, ac_activation suppressed] → 221 (37) / 221 (37); s15_16 [coffee_break ordinary, ac_activation suppressed] → 221 (37) / 221 (37) |
| s15_08 | deliver_item(item_4) | 277 to 368 | 1 | 322 (45) / 322 (45) | s15_08 [coffee_break ordinary, ac_activation suppressed] → 277 (0) / 277 (0); s15_14 [coffee_break ordinary, ac_activation suppressed] → 277 (0) / 277 (0); s15_15 [coffee_break ordinary, ac_activation suppressed] → 277 (0) / 277 (0); s15_16 [coffee_break ordinary, ac_activation suppressed] → 277 (0) / 277 (0) |
| s15_09 | deliver_item(item_3) | 0 to 66 | 4 | 28 (28) / 28 (28) | s15_09 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26) |
| s15_09 | deliver_item(item_2) | 67 to 123 | 3 | 97 (30) / 97 (30) | s15_09 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20) |
| s15_09 | ac_activation(ac_switch_0) | 124 to 171 | 2 | never / never | s15_09 [ordinary] → never / never |
| s15_09 | deliver_item(item_1) | 172 to 229 | 2 | 180 (8) / 180 (8) | s15_09 [coffee_break ordinary, ac_activation suppressed] → 176 (4) / 176 (4) |
| s15_09 | deliver_item(item_4) | 230 to 323 | 1 | 276 (46) / 276 (46) | s15_09 [coffee_break ordinary, ac_activation suppressed] → 230 (0) / 230 (0) |
| s15_10 | deliver_item(item_3) | 0 to 66 | 4 | 28 (28) / 28 (28) | s15_10 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26); s15_19 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26); s15_20 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26) |
| s15_10 | deliver_item(item_2) | 67 to 123 | 3 | 97 (30) / 97 (30) | s15_10 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20); s15_19 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20); s15_20 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20) |
| s15_10 | deliver_item(item_1) | 124 to 216 | 2 | 171 (47) / 171 (47) | s15_10 [coffee_break ordinary, ac_activation ordinary/raised] → 171 (47) / 171 (47); s15_19 [coffee_break ordinary, ac_activation ordinary] → 162 (38) / 162 (38); s15_20 [coffee_break ordinary, ac_activation ordinary/raised] → 171 (47) / 171 (47) |
| s15_10 | ac_activation(ac_switch_0) | 217 to 263 | 1 | never / never | s15_10 [raised] → never / never; s15_19 [ordinary] → never / never; s15_20 [raised] → never / never |
| s15_10 | deliver_item(item_4) | 264 to 321 | 1 | 279 (15) / 279 (15) | s15_10 [coffee_break ordinary, ac_activation suppressed] → 264 (0) / 264 (0); s15_19 [coffee_break ordinary, ac_activation suppressed] → 264 (0) / 264 (0); s15_20 [coffee_break raised, ac_activation suppressed] → 283 (19) / 283 (19) |
| s15_11 | deliver_item(item_3) | 0 to 66 | 4 | 28 (28) / 28 (28) | s15_11 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26) |
| s15_11 | deliver_item(item_2) | 67 to 93 | 3 | never / never | s15_11 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20) |
| s15_11 | ac_activation(ac_switch_0) | 94 to 134 | 3 | never / never | s15_11 [ordinary] → never / never |
| s15_11 | deliver_item(item_2) | 135 to 203 | 3 | 155 (20) / 155 (20) | s15_11 [coffee_break ordinary, ac_activation suppressed] → 145 (10) / 145 (10) |
| s15_11 | deliver_item(item_1) | 204 to 296 | 2 | 251 (47) / 251 (47) | s15_11 [coffee_break ordinary, ac_activation suppressed] → 241 (37) / 241 (37) |
| s15_11 | deliver_item(item_4) | 297 to 388 | 1 | 342 (45) / 342 (45) | s15_11 [coffee_break ordinary, ac_activation suppressed] → 297 (0) / 297 (0) |
| s15_12 | deliver_item(item_3) | 0 to 66 | 4 | 28 (28) / 28 (28) | s15_12 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26) |
| s15_12 | deliver_item(item_2) | 67 to 95 | 3 | never / never | s15_12 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20) |
| s15_12 | ac_activation(ac_switch_0) | 96 to 136 | 3 | 121 (25) / 133 (37) | s15_12 [ordinary] → 125 (29) / 133 (37) |
| s15_12 | deliver_item(item_2) | 137 to 184 | 3 | 164 (27) / 164 (27) | s15_12 [coffee_break ordinary, ac_activation suppressed] → 164 (27) / 164 (27) |
| s15_12 | deliver_item(item_1) | 185 to 278 | 2 | 231 (46) / 231 (46) | s15_12 [coffee_break ordinary, ac_activation suppressed] → 221 (36) / 221 (36) |
| s15_12 | deliver_item(item_4) | 279 to 372 | 1 | 325 (46) / 325 (46) | s15_12 [coffee_break ordinary, ac_activation suppressed] → 279 (0) / 279 (0) |
| s15_13 | deliver_item(item_3) | 0 to 66 | 4 | 28 (28) / 28 (28) | s15_13 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26) |
| s15_13 | deliver_item(item_2) | 67 to 121 | 3 | 97 (30) / 97 (30) | s15_13 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20) |
| s15_13 | ac_activation(ac_switch_0) | 122 to 169 | 3 | 154 (32) / 166 (44) | s15_13 [ordinary, raised] → 152 (30) / 166 (44) |
| s15_13 | deliver_item(item_2) | 170 to 216 | 3 | 197 (27) / 197 (27) | s15_13 [coffee_break ordinary, ac_activation suppressed] → 197 (27) / 197 (27) |
| s15_13 | deliver_item(item_1) | 217 to 308 | 2 | 263 (46) / 263 (46) | s15_13 [coffee_break ordinary, ac_activation suppressed] → 253 (36) / 253 (36) |
| s15_13 | deliver_item(item_4) | 309 to 400 | 1 | 354 (45) / 354 (45) | s15_13 [coffee_break ordinary, ac_activation suppressed] → 309 (0) / 309 (0) |
| s15_21 | deliver_item(item_3) | 0 to 66 | 4 | 28 (28) / 28 (28) | s15_21 [coffee_break ordinary, ac_activation ordinary] → 26 (26) / 26 (26) |
| s15_21 | deliver_item(item_2) | 67 to 123 | 3 | 97 (30) / 97 (30) | s15_21 [coffee_break ordinary, ac_activation ordinary] → 87 (20) / 87 (20) |
| s15_21 | deliver_item(item_1) | 124 to 216 | 2 | 171 (47) / 171 (47) | s15_21 [coffee_break ordinary, ac_activation ordinary] → 162 (38) / 162 (38) |
| s15_21 | deliver_item(item_4) | 217 to 308 | 1 | 262 (45) / 262 (45) | s15_21 [coffee_break ordinary, ac_activation ordinary] → 217 (0) / 217 (0) |
| s15_21 | coffee_break(coffee_machine_0) | 309 to 381 | 0 | 334 (25) / 334 (25) | s15_21 [raised] → 309 (0) / 309 (0) |

### The A/C activation's belief at its arrival (within one script)

| script (off) | arrival | live | off | on, per scenario: level at arrival → belief |
|---|---|---|---|---|
| s14_07 | 135 | 2 | 0.4626 | s14_07 [ordinary; coffee ordinary] → 0.0599; s14_15 [raised; coffee ordinary] → 0.6144; s14_16 [raised; coffee ordinary] → 0.6144; s14_17 [ordinary; coffee ordinary] → 0.0599 |
| s14_08 | 227 | 1 | 0.5475 | s14_08 [raised; coffee ordinary] → 0.6449; s14_21 [ordinary; coffee raised] → 0.0142 |
| s14_09 | 138 | 2 | 0.4456 | s14_09 [ordinary; coffee ordinary] → 0.0467 |
| s14_10 | 140 | 2 | 0.4814 | s14_10 [ordinary; coffee ordinary] → 0.0558 |
| s14_11 | 225 | 2 | 0.4351 | s14_11 [raised; coffee ordinary] → 0.5192 |
| s15_08 | 112 | 3 | 0.6238 | s15_08 [ordinary; coffee ordinary] → 0.0914; s15_14 [raised; coffee ordinary] → 0.7154; s15_15 [raised; coffee ordinary] → 0.7154; s15_16 [ordinary; coffee ordinary] → 0.0914 |
| s15_09 | 169 | 2 | 0.6130 | s15_09 [raised; coffee ordinary] → 0.6152 |
| s15_10 | 261 | 1 | 0.7487 | s15_10 [raised; coffee ordinary] → 0.6035; s15_19 [ordinary; coffee ordinary] → 0.0574; s15_20 [raised; coffee raised] → 0.5932 |
| s15_11 | 132 | 3 | 0.7468 | s15_11 [ordinary; coffee ordinary] → 0.1516 |
| s15_12 | 134 | 3 | 0.9961 | s15_12 [ordinary; coffee ordinary] → 0.9875 |
| s15_13 | 167 | 3 | 0.9952 | s15_13 [raised; coffee ordinary] → 0.9990 |

### The coffee break on its stretch's first observed ticks (the prior alone, direction 2)

The evidence restarts equal at the episode's boundary, so the belief on the stretch's first tick is the prior over the live hypotheses. `first clears`: the first tick on which the gate clears for it.

| scenario | stretch | live | level | belief at start | gate at start | first ≥ θ | first clears |
|---|---|---|---|---|---|---|---|
| s13_02 | 67 to 140 | 3 | ordinary | 0.0199 | none(below_theta) | 117 (50) | 117 (50) |
| s13_03 | 124 to 197 | 2 | ordinary | 0.0200 | none(below_theta) | 175 (51) | 175 (51) |
| s13_04 | 217 to 289 | 1 | raised | 0.6687 | none(below_theta) | 238 (21) | 238 (21) |
| s13_05 | 94 to 146 | 3 | ordinary | 0.0255 | clears | 120 (26) | 120 (26) |
| s13_06 | 96 to 148 | 3 | ordinary | 0.0222 | clears | 112 (16) | 112 (16) |
| s13_07 | 122 to 195 | 3 | ordinary | 0.0000 | none(leader_no_observation) | 160 (38) | 163 (41) |
| s13_08 | 67 to 140 | 3 | raised | 0.6701 | none(below_theta) | 82 (15) | 82 (15) |
| s13_09 | 67 to 140 | 3 | ordinary | 0.0199 | none(below_theta) | 90 (23) | 90 (23) |
| s13_10 | 67 to 140 | 3 | ordinary | 0.0199 | none(below_theta) | 117 (50) | 117 (50) |
| s13_11 | 124 to 197 | 2 | raised | 0.6708 | none(below_theta) | 138 (14) | 138 (14) |
| s13_12 | 124 to 197 | 2 | raised | 0.6708 | none(below_theta) | 138 (14) | 138 (14) |
| s13_13 | 217 to 289 | 1 | ordinary | 0.0198 | clears | 271 (54) | 271 (54) |
| s13_15 | 261 to 309 | 1 | ordinary | 0.0008 | none(leader_no_observation) | 291 (30) | 291 (30) |
| s14_02 | 89 to 166 | 2 | ordinary | 0.0193 | none(below_theta) | 157 (68) | 157 (68) |
| s14_03 | 181 to 259 | 1 | raised | 0.6624 | none(below_theta) | 226 (45) | 226 (45) |
| s14_04 | 133 to 174 | 2 | ordinary | 0.0126 | clears | 162 (29) | 162 (29) |
| s14_05 | 135 to 176 | 2 | ordinary | 0.0105 | clears | 163 (28) | 163 (28) |
| s14_06 | 179 to 257 | 2 | raised | 0.0000 | none(leader_no_observation) | 224 (45) | 225 (46) |
| s14_12 | 89 to 166 | 2 | raised | 0.6626 | none(below_theta) | 129 (40) | 129 (40) |
| s14_13 | 89 to 166 | 2 | ordinary | 0.0193 | none(below_theta) | 129 (40) | 129 (40) |
| s14_14 | 89 to 166 | 2 | ordinary | 0.0193 | none(below_theta) | 150 (61) | 150 (61) |
| s14_18 | 181 to 259 | 1 | raised | 0.6624 | none(below_theta) | 226 (45) | 226 (45) |
| s14_19 | 181 to 259 | 1 | ordinary | 0.0192 | clears | 252 (71) | 252 (71) |
| s15_02 | 67 to 140 | 3 | ordinary | 0.0195 | none(below_theta) | 117 (50) | 117 (50) |
| s15_03 | 124 to 197 | 2 | ordinary | 0.0196 | none(below_theta) | 176 (52) | 176 (52) |
| s15_04 | 217 to 289 | 1 | raised | 0.6643 | none(below_theta) | 238 (21) | 238 (21) |
| s15_05 | 94 to 146 | 3 | ordinary | 0.0254 | clears | 120 (26) | 120 (26) |
| s15_06 | 96 to 148 | 3 | ordinary | 0.0222 | clears | 112 (16) | 112 (16) |
| s15_07 | 122 to 195 | 3 | ordinary | 0.0000 | none(leader_no_observation) | 160 (38) | 163 (41) |
| s15_17 | 217 to 289 | 1 | raised | 0.5744 | none(below_theta) | 243 (26) | 243 (26) |
| s15_21 | 309 to 381 | 0 | raised | 0.9903 | clears | 309 (0) | 309 (0) |

### The recency fact after an observed coffee break (direction 4)

Per completion: the ticks on which the coffee break is live and suppressed, those of them inside break_time, and its level on the first tick after the 90.

| scenario | completion | suppressed on (live ticks) | of them inside break_time | level after |
|---|---|---|---|---|
| s13_02 | 139 | 88 of 88 | 51 | raised |
| s13_03 | 196 | 88 of 88 | 88 | raised |
| s13_04 | 288 | 88 of 88 | 10 | ordinary |
| s13_05 | 145 | 88 of 88 | 57 | raised |
| s13_06 | 147 | 88 of 88 | 59 | raised |
| s13_07 | 194 | 88 of 88 | 88 | raised |
| s13_08 | 139 | 88 of 88 | 59 | ordinary |
| s13_09 | 139 | 88 of 88 | 59 | ordinary |
| s13_10 | 139 | 88 of 88 | 59 | ordinary |
| s13_11 | 196 | 88 of 88 | 0 | ordinary |
| s13_12 | 196 | 88 of 88 | 0 | ordinary |
| s13_13 | 288 | 88 of 88 | 0 | ordinary |
| s13_15 | 308 | 88 of 88 | 0 | ordinary |
| s14_02 | 165 | 88 of 88 | 77 | raised |
| s14_03 | 258 | 88 of 88 | 40 | ordinary |
| s14_04 | 173 | 88 of 88 | 85 | raised |
| s14_05 | 175 | 88 of 88 | 87 | raised |
| s14_06 | 256 | 88 of 88 | 42 | ordinary |
| s14_12 | 165 | 88 of 88 | 83 | ordinary |
| s14_13 | 165 | 88 of 88 | 83 | ordinary |
| s14_14 | 165 | 88 of 88 | 83 | ordinary |
| s14_18 | 258 | 88 of 88 | 0 | ordinary |
| s14_19 | 258 | 88 of 88 | 0 | ordinary |
| s15_02 | 139 | 88 of 88 | 51 | raised |
| s15_03 | 196 | 88 of 88 | 88 | raised |
| s15_04 | 288 | 88 of 88 | 10 | ordinary |
| s15_05 | 145 | 88 of 88 | 57 | raised |
| s15_06 | 147 | 88 of 88 | 59 | raised |
| s15_07 | 194 | 88 of 88 | 88 | raised |
| s15_17 | 288 | 88 of 88 | 10 | ordinary |
| s15_21 | 380 | 65 of 65 | 65 | run ended |

### A level changing inside an episode (direction 5)

Every tick on which a foreseeable task's level changes while it stays live, inside a true stretch: the true hypothesis's belief before and on that tick, and the gate for it before and on that tick.

| scenario | tick | change | true task | belief before → on | gate before → on |
|---|---|---|---|---|---|
| s13_01 | 178 | coffee_break ordinary→raised | deliver_item(item_1) | 0.9871 → 0.9894 | clears → clears |
| s13_01 | 300 | coffee_break raised→ordinary | deliver_item(item_4) | 1.0000 → 1.0000 | clears → clears |
| s13_02 | 229 | coffee_break suppressed→raised | deliver_item(item_1) | 0.7236 → 0.7107 | none(below_theta) (deliver_item(item_1)) → none(below_theta) (deliver_item(item_1)) |
| s13_02 | 300 | coffee_break raised→ordinary | deliver_item(item_4) | 0.3785 → 0.9842 | none(below_theta) (coffee_break(coffee_machine_0)) → clears |
| s13_03 | 178 | coffee_break ordinary→raised | coffee_break(coffee_machine_0) | 0.8175 → 0.9982 | clears → clears |
| s13_03 | 286 | coffee_break suppressed→raised | deliver_item(item_4) | 0.9953 → 0.3508 | clears → none(below_theta) (coffee_break(coffee_machine_0)) |
| s13_03 | 300 | coffee_break raised→ordinary | deliver_item(item_4) | 0.4195 → 0.9868 | none(below_theta) (coffee_break(coffee_machine_0)) → clears |
| s13_04 | 178 | coffee_break ordinary→raised | deliver_item(item_1) | 0.9871 → 0.9894 | clears → clears |
| s13_05 | 235 | coffee_break suppressed→raised | deliver_item(item_1) | 0.7243 → 0.7117 | none(below_theta) (deliver_item(item_1)) → none(below_theta) (deliver_item(item_1)) |
| s13_05 | 300 | coffee_break raised→ordinary | deliver_item(item_4) | 0.3538 → 0.9823 | none(below_theta) (coffee_break(coffee_machine_0)) → clears |
| s13_06 | 237 | coffee_break suppressed→raised | deliver_item(item_1) | 0.8757 → 0.8877 | clears → clears |
| s13_06 | 300 | coffee_break raised→ordinary | deliver_item(item_4) | 0.3738 → 0.9839 | none(below_theta) (coffee_break(coffee_machine_0)) → clears |
| s13_07 | 178 | coffee_break ordinary→raised | coffee_break(coffee_machine_0) | 0.9957 → 1.0000 | clears → clears |
| s13_07 | 284 | coffee_break suppressed→raised | deliver_item(item_1) | 0.8797 → 0.8918 | clears → clears |
| s13_07 | 300 | coffee_break raised→ordinary | deliver_item(item_1) | 0.9973 → 0.9987 | clears → clears |
| s13_08 | 50 | coffee_break ordinary→raised | deliver_item(item_3) | 0.9994 → 0.9989 | clears → clears |
| s13_08 | 229 | coffee_break suppressed→ordinary | deliver_item(item_1) | 0.7236 → 0.7433 | none(below_theta) (deliver_item(item_1)) → none(below_theta) (deliver_item(item_1)) |
| s13_09 | 90 | coffee_break ordinary→raised | coffee_break(coffee_machine_0) | 0.0454 → 0.8387 | none(below_theta) (deliver_item(item_4)) → clears |
| s13_09 | 229 | coffee_break suppressed→ordinary | deliver_item(item_1) | 0.7236 → 0.7433 | none(below_theta) (deliver_item(item_1)) → none(below_theta) (deliver_item(item_1)) |
| s13_10 | 120 | coffee_break ordinary→raised | coffee_break(coffee_machine_0) | 0.8441 → 0.9985 | clears → clears |
| s13_10 | 229 | coffee_break suppressed→ordinary | deliver_item(item_1) | 0.7236 → 0.7433 | none(below_theta) (deliver_item(item_1)) → none(below_theta) (deliver_item(item_1)) |
| s13_11 | 40 | coffee_break ordinary→raised | deliver_item(item_3) | 0.9713 → 0.9768 | clears → clears |
| s13_11 | 190 | coffee_break raised→ordinary | coffee_break(coffee_machine_0) | 0.9998 → 0.9836 | clears → clears |
| s13_11 | 286 | coffee_break suppressed→ordinary | deliver_item(item_4) | 0.9953 → 0.9818 | clears → clears |
| s13_12 | 40 | coffee_break ordinary→raised | deliver_item(item_3) | 0.9713 → 0.9768 | clears → clears |
| s13_12 | 150 | coffee_break raised→ordinary | coffee_break(coffee_machine_0) | 0.8501 → 0.0575 | clears → clears (deliver_item(item_4)) |
| s13_12 | 286 | coffee_break suppressed→ordinary | deliver_item(item_4) | 0.9953 → 0.9818 | clears → clears |
| s14_01 | 178 | coffee_break ordinary→raised | deliver_item(item_2) | 1.0000 → 1.0000 | clears → clears |
| s14_02 | 255 | coffee_break suppressed→raised | deliver_item(item_1) | 0.9796 → 0.3460 | clears → none(below_theta) (coffee_break(coffee_machine_0)) |
| s14_02 | 300 | coffee_break raised→ordinary | deliver_item(item_1) | 0.9999 → 1.0000 | clears → clears |
| s14_03 | 178 | coffee_break ordinary→raised | deliver_item(item_2) | 1.0000 → 1.0000 | clears → clears |
| s14_04 | 263 | coffee_break suppressed→raised | deliver_item(item_1) | 0.9796 → 0.3460 | clears → none(below_theta) (coffee_break(coffee_machine_0)) |
| s14_04 | 300 | coffee_break raised→ordinary | deliver_item(item_1) | 0.9968 → 1.0000 | clears → clears |
| s14_05 | 265 | coffee_break suppressed→raised | deliver_item(item_1) | 0.9841 → 0.3701 | clears → none(below_theta) (coffee_break(coffee_machine_0)) |
| s14_05 | 300 | coffee_break raised→ordinary | deliver_item(item_1) | 0.9997 → 1.0000 | clears → clears |
| s14_06 | 178 | coffee_break ordinary→raised | deliver_item(item_2) | 1.0000 → 1.0000 | clears → clears |
| s14_06 | 346 | coffee_break suppressed→ordinary | deliver_item(item_1) | 0.9840 → 0.9726 | clears → clears |
| s14_08 | 150 | ac_activation ordinary→raised | deliver_item(item_2) | 0.9988 → 0.9976 | clears → clears |
| s14_11 | 150 | ac_activation ordinary→raised | deliver_item(item_2) | 0.9988 → 0.9976 | clears → clears |
| s14_12 | 70 | coffee_break ordinary→raised | deliver_item(item_0) | 0.9999 → 0.9998 | clears → clears |
| s14_12 | 255 | coffee_break suppressed→ordinary | deliver_item(item_1) | 0.9796 → 0.9666 | clears → clears |
| s14_13 | 110 | coffee_break ordinary→raised | coffee_break(coffee_machine_0) | 0.0204 → 0.6768 | none(below_theta) (deliver_item(item_1)) → none(below_theta) (coffee_break(coffee_machine_0)) |
| s14_13 | 255 | coffee_break suppressed→ordinary | deliver_item(item_1) | 0.9796 → 0.9666 | clears → clears |
| s14_14 | 150 | coffee_break ordinary→raised | coffee_break(coffee_machine_0) | 0.4106 → 0.9883 | none(below_theta) (deliver_item(item_1)) → clears |
| s14_14 | 255 | coffee_break suppressed→ordinary | deliver_item(item_1) | 0.9796 → 0.9666 | clears → clears |
| s14_15 | 70 | ac_activation ordinary→raised | deliver_item(item_0) | 0.9999 → 0.9999 | clears → clears |
| s14_16 | 110 | ac_activation ordinary→raised | ac_activation(ac_switch_0) | 0.0204 → 0.3437 | none(below_theta) (deliver_item(item_2)) → none(below_theta) (ac_activation(ac_switch_0)) |
| s14_17 | 110 | ac_activation raised→ordinary | ac_activation(ac_switch_0) | 0.3425 → 0.0205 | none(below_theta) (ac_activation(ac_switch_0)) → none(below_theta) (deliver_item(item_2)) |
| s14_18 | 60 | coffee_break ordinary→raised | deliver_item(item_0) | 0.9947 → 0.9885 | clears → clears |
| s14_18 | 250 | coffee_break raised→ordinary | coffee_break(coffee_machine_0) | 0.9948 → 0.7018 | clears → none(below_theta) (coffee_break(coffee_machine_0)) |
| s14_21 | 178 | coffee_break ordinary→raised | deliver_item(item_2) | 1.0000 → 1.0000 | clears → clears |
| s15_01 | 178 | coffee_break ordinary→raised | deliver_item(item_1) | 0.9855 → 0.9883 | clears → clears |
| s15_01 | 300 | coffee_break raised→ordinary | deliver_item(item_4) | 1.0000 → 1.0000 | clears → clears |
| s15_02 | 229 | coffee_break suppressed→raised | deliver_item(item_1) | 0.7075 → 0.6957 | none(below_theta) (deliver_item(item_1)) → none(below_theta) (deliver_item(item_1)) |
| s15_02 | 300 | coffee_break raised→ordinary | deliver_item(item_4) | 0.3758 → 0.9658 | none(below_theta) (coffee_break(coffee_machine_0)) → clears |
| s15_03 | 178 | coffee_break ordinary→raised | coffee_break(coffee_machine_0) | 0.8159 → 0.9982 | clears → clears |
| s15_03 | 286 | coffee_break suppressed→raised | deliver_item(item_4) | 0.9761 → 0.3483 | clears → none(below_theta) (coffee_break(coffee_machine_0)) |
| s15_03 | 300 | coffee_break raised→ordinary | deliver_item(item_4) | 0.4162 → 0.9688 | none(below_theta) (coffee_break(coffee_machine_0)) → clears |
| s15_04 | 178 | coffee_break ordinary→raised | deliver_item(item_1) | 0.9855 → 0.9883 | clears → clears |
| s15_05 | 235 | coffee_break suppressed→raised | deliver_item(item_1) | 0.7082 → 0.6966 | none(below_theta) (deliver_item(item_1)) → none(below_theta) (deliver_item(item_1)) |
| s15_05 | 300 | coffee_break raised→ordinary | deliver_item(item_4) | 0.3514 → 0.9637 | none(below_theta) (coffee_break(coffee_machine_0)) → clears |
| s15_06 | 237 | coffee_break suppressed→raised | deliver_item(item_1) | 0.8599 → 0.8732 | clears → clears |
| s15_06 | 300 | coffee_break raised→ordinary | deliver_item(item_4) | 0.3711 → 0.9654 | none(below_theta) (coffee_break(coffee_machine_0)) → clears |
| s15_07 | 178 | coffee_break ordinary→raised | coffee_break(coffee_machine_0) | 0.9951 → 1.0000 | clears → clears |
| s15_07 | 284 | coffee_break suppressed→raised | deliver_item(item_1) | 0.8641 → 0.8775 | clears → clears |
| s15_07 | 300 | coffee_break raised→ordinary | deliver_item(item_1) | 0.9971 → 0.9986 | clears → clears |
| s15_09 | 150 | ac_activation ordinary→raised | ac_activation(ac_switch_0) | 0.0213 → 0.3541 | none(below_theta) (deliver_item(item_4)) → none(below_theta) (ac_activation(ac_switch_0)) |
| s15_10 | 150 | ac_activation ordinary→raised | deliver_item(item_1) | 0.5779 → 0.3884 | none(below_theta) (deliver_item(item_1)) → none(below_theta) (deliver_item(item_1)) |
| s15_13 | 150 | ac_activation ordinary→raised | ac_activation(ac_switch_0) | 0.0430 → 0.6260 | none(leader_inadequate) (deliver_item(item_2)) → none(below_theta) (ac_activation(ac_switch_0)) |
| s15_14 | 50 | ac_activation ordinary→raised | deliver_item(item_3) | 0.9993 → 0.9987 | clears → clears |
| s15_15 | 90 | ac_activation ordinary→raised | ac_activation(ac_switch_0) | 0.0302 → 0.4410 | none(below_theta) (deliver_item(item_4)) → none(below_theta) (ac_activation(ac_switch_0)) |
| s15_16 | 90 | ac_activation raised→ordinary | ac_activation(ac_switch_0) | 0.4381 → 0.0306 | none(below_theta) (ac_activation(ac_switch_0)) → none(below_theta) (deliver_item(item_4)) |
| s15_17 | 150 | ac_activation ordinary→raised | deliver_item(item_1) | 0.5779 → 0.3884 | none(below_theta) (deliver_item(item_1)) → none(below_theta) (deliver_item(item_1)) |
| s15_17 | 178 | coffee_break ordinary→raised | deliver_item(item_1) | 0.9501 → 0.9628 | clears → clears |
| s15_20 | 150 | ac_activation ordinary→raised | deliver_item(item_1) | 0.5779 → 0.3884 | none(below_theta) (deliver_item(item_1)) → none(below_theta) (deliver_item(item_1)) |
| s15_20 | 178 | coffee_break ordinary→raised | deliver_item(item_1) | 0.9501 → 0.9628 | clears → clears |
| s15_20 | 300 | coffee_break raised→ordinary | deliver_item(item_4) | 0.9977 → 1.0000 | clears → clears |
| s15_21 | 307 | coffee_break ordinary→raised | deliver_item(item_4) | 1.0000 → - | clears → none(leader_no_observation) (coffee_break(coffee_machine_0)) |

### Admissions of a hypothesis that is not the true task, off against on (P8)

Excluding the one-tick rows on a true task's completion tick ("complete: pinned"; the next task leads on its last action's ticks), counted separately. Exit walk: the unmodelled ticks.

| scenario | off: exit walk | off: other | on: exit walk | on: other | on: one-tick on a completion |
|---|---|---|---|---|---|
| s13_01 | coffee_break(coffee_machine_0) 309 to 330 (retraction at 331 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 309 to 330 (retraction at 331 (none(leader_inadequate))) | none | 0 |
| s13_02 | coffee_break(coffee_machine_0) 378 to 399 (retraction at 400 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 378 to 399 (retraction at 400 (none(leader_inadequate))) | none | 0 |
| s13_03 | coffee_break(coffee_machine_0) 372 to 393 (retraction at 394 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 372 to 393 (retraction at 394 (none(leader_inadequate))) | deliver_item(item_4) 150 to 161 (retraction at 162 (none(below_theta))) while coffee_break(coffee_machine_0) | 1 |
| s13_04 | coffee_break(coffee_machine_0) 357 to 378 (retraction at 379 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 357 to 378 (retraction at 379 (none(leader_inadequate))) | none | 1 |
| s13_05 | coffee_break(coffee_machine_0) 384 to 405 (retraction at 406 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 384 to 405 (retraction at 406 (none(leader_inadequate))) | deliver_item(item_2) 94 (retraction at 95 (none(leader_no_observation))) while coffee_break(coffee_machine_0); deliver_item(item_2) 96 to 99 (retraction at 100 (none(below_theta))) while coffee_break(coffee_machine_0) | 0 |
| s13_06 | coffee_break(coffee_machine_0) 379 to 400 (retraction at 401 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 379 to 400 (retraction at 401 (none(leader_inadequate))) | deliver_item(item_2) 96 to 103 (retraction at 104 (none(below_theta))) while coffee_break(coffee_machine_0) | 0 |
| s13_07 | coffee_break(coffee_machine_0) 429 to 451 (retraction at 452 (none(leader_inadequate))) | deliver_item(item_2) 123 to 130 (retraction at 131 (none(leader_inadequate))) while coffee_break(coffee_machine_0) | coffee_break(coffee_machine_0) 429 to 451 (retraction at 452 (none(leader_inadequate))) | deliver_item(item_2) 123 to 130 (retraction at 131 (none(leader_inadequate))) while coffee_break(coffee_machine_0) | 1 |
| s13_08 | coffee_break(coffee_machine_0) 378 to 399 (retraction at 400 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 378 to 399 (retraction at 400 (none(leader_inadequate))) | none | 1 |
| s13_09 | coffee_break(coffee_machine_0) 378 to 399 (retraction at 400 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 378 to 399 (retraction at 400 (none(leader_inadequate))) | none | 1 |
| s13_10 | coffee_break(coffee_machine_0) 378 to 399 (retraction at 400 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 378 to 399 (retraction at 400 (none(leader_inadequate))) | none | 1 |
| s13_11 | coffee_break(coffee_machine_0) 372 to 393 (retraction at 394 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 372 to 393 (retraction at 394 (none(leader_inadequate))) | coffee_break(coffee_machine_0) 81 to 91 (retraction at 92 (none(below_theta))) while deliver_item(item_2) | 1 |
| s13_12 | coffee_break(coffee_machine_0) 372 to 393 (retraction at 394 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 372 to 393 (retraction at 394 (none(leader_inadequate))) | coffee_break(coffee_machine_0) 81 to 91 (retraction at 92 (none(below_theta))) while deliver_item(item_2); deliver_item(item_4) 150 to 161 (retraction at 162 (none(below_theta))) while coffee_break(coffee_machine_0) | 1 |
| s13_13 | coffee_break(coffee_machine_0) 357 to 378 (retraction at 379 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 357 to 378 (retraction at 379 (none(leader_inadequate))) | deliver_item(item_4) 216 to 258 (retraction at 259 (none(leader_inadequate))) while deliver_item(item_1) (complete: pinned), coffee_break(coffee_machine_0) | 1 |
| s13_14 | coffee_break(coffee_machine_0) 309 to 330 (retraction at 331 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 309 to 330 (retraction at 331 (none(leader_inadequate))) | coffee_break(coffee_machine_0) 81 to 91 (retraction at 92 (none(below_theta))) while deliver_item(item_2) | 0 |
| s13_15 | coffee_break(coffee_machine_0) 376 to 397 (retraction at 398 (none(leader_inadequate))) | deliver_item(item_4) 262 to 268 (retraction at 269 (none(below_theta))) while coffee_break(coffee_machine_0) | coffee_break(coffee_machine_0) 376 to 397 (retraction at 398 (none(leader_inadequate))) | deliver_item(item_4) 262 to 269 (retraction at 270 (none(leader_inadequate))) while coffee_break(coffee_machine_0) | 2 |
| s14_01 | none | none | none | none | 0 |
| s14_02 | none | none | none | none | 1 |
| s14_03 | none | none | none | none | 1 |
| s14_04 | none | none | none | deliver_item(item_2) 133 (retraction at 134 (none(leader_no_observation))) while coffee_break(coffee_machine_0); deliver_item(item_2) 135 to 136 (retraction at 137 (none(below_theta))) while coffee_break(coffee_machine_0) | 1 |
| s14_05 | none | none | none | deliver_item(item_2) 135 to 146 (retraction at 147 (none(leader_inadequate))) while coffee_break(coffee_machine_0) | 1 |
| s14_06 | none | deliver_item(item_2) 180 to 187 (retraction at 188 (none(leader_inadequate))) while coffee_break(coffee_machine_0) | none | deliver_item(item_2) 180 to 187 (retraction at 188 (none(leader_inadequate))) while coffee_break(coffee_machine_0) | 1 |
| s14_07 | none | none | none | none | 1 |
| s14_08 | none | none | none | none | 1 |
| s14_09 | none | none | none | deliver_item(item_2) 133 (retraction at 134 (none(leader_no_observation))) while ac_activation(ac_switch_0); deliver_item(item_2) 135 to 136 (retraction at 137 (none(below_theta))) while ac_activation(ac_switch_0) | 1 |
| s14_10 | none | none | none | deliver_item(item_2) 135 to 140 (retraction at 141 (none(below_theta))) while ac_activation(ac_switch_0) | 1 |
| s14_11 | none | deliver_item(item_2) 180 to 187 (retraction at 188 (none(leader_inadequate))) while ac_activation(ac_switch_0) | none | deliver_item(item_2) 180 to 187 (retraction at 188 (none(leader_inadequate))) while ac_activation(ac_switch_0) | 1 |
| s14_12 | none | none | none | none | 1 |
| s14_13 | none | none | none | none | 1 |
| s14_14 | none | none | none | none | 1 |
| s14_15 | none | none | none | none | 1 |
| s14_16 | none | none | none | none | 1 |
| s14_17 | none | none | none | none | 1 |
| s14_18 | none | none | none | none | 1 |
| s14_19 | none | none | none | deliver_item(item_1) 180 to 239 (retraction at 240 (none(below_theta))) while deliver_item(item_2) (complete: pinned), coffee_break(coffee_machine_0) | 1 |
| s14_20 | none | none | none | none | 0 |
| s14_21 | none | none | none | coffee_break(coffee_machine_0) 221 to 227 (retraction at 228 (none(below_theta))) while ac_activation(ac_switch_0) | 0 |
| s15_01 | coffee_break(coffee_machine_0) 319 to 330 (retraction at 331 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 319 to 330 (retraction at 331 (none(leader_inadequate))) | none | 0 |
| s15_02 | coffee_break(coffee_machine_0) 388 to 399 (retraction at 400 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 388 to 399 (retraction at 400 (none(leader_inadequate))) | none | 0 |
| s15_03 | coffee_break(coffee_machine_0) 382 to 393 (retraction at 394 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 382 to 393 (retraction at 394 (none(leader_inadequate))) | deliver_item(item_4) 151 to 161 (retraction at 162 (none(below_theta))) while coffee_break(coffee_machine_0) | 1 |
| s15_04 | coffee_break(coffee_machine_0) 367 to 378 (retraction at 379 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 378 (retraction at 379 (none(leader_inadequate))) | none | 1 |
| s15_05 | coffee_break(coffee_machine_0) 394 to 405 (retraction at 406 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 394 to 405 (retraction at 406 (none(leader_inadequate))) | deliver_item(item_2) 94 (retraction at 95 (none(leader_no_observation))) while coffee_break(coffee_machine_0); deliver_item(item_2) 96 to 99 (retraction at 100 (none(below_theta))) while coffee_break(coffee_machine_0) | 0 |
| s15_06 | coffee_break(coffee_machine_0) 389 to 400 (retraction at 401 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 389 to 400 (retraction at 401 (none(leader_inadequate))) | deliver_item(item_2) 96 to 103 (retraction at 104 (none(below_theta))) while coffee_break(coffee_machine_0) | 0 |
| s15_07 | coffee_break(coffee_machine_0) 440 to 451 (retraction at 452 (none(leader_inadequate))) | deliver_item(item_2) 123 to 130 (retraction at 131 (none(leader_inadequate))) while coffee_break(coffee_machine_0) | coffee_break(coffee_machine_0) 440 to 451 (retraction at 452 (none(leader_inadequate))) | deliver_item(item_2) 123 to 130 (retraction at 131 (none(leader_inadequate))) while coffee_break(coffee_machine_0) | 1 |
| s15_08 | coffee_break(coffee_machine_0) 379 to 390 (retraction at 391 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 369 to 390 (retraction at 391 (none(leader_inadequate))) | none | 1 |
| s15_09 | coffee_break(coffee_machine_0) 335 to 346 (retraction at 347 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 324 to 346 (retraction at 347 (none(leader_inadequate))) | none | 1 |
| s15_10 | coffee_break(coffee_machine_0) 333 to 344 (retraction at 345 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 322 to 344 (retraction at 345 (none(leader_inadequate))) | none | 1 |
| s15_11 | coffee_break(coffee_machine_0) 399 to 410 (retraction at 411 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 389 to 410 (retraction at 411 (none(leader_inadequate))) | deliver_item(item_2) 94 (retraction at 95 (none(leader_no_observation))) while ac_activation(ac_switch_0); deliver_item(item_2) 96 to 98 (retraction at 99 (none(below_theta))) while ac_activation(ac_switch_0); deliver_item(item_4) 111 to 118 (retraction at 119 (none(leader_inadequate))) while ac_activation(ac_switch_0) | 1 |
| s15_12 | coffee_break(coffee_machine_0) 383 to 394 (retraction at 395 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 373 to 394 (retraction at 395 (none(leader_inadequate))) | deliver_item(item_2) 96 to 108 (retraction at 109 (none(leader_inadequate))) while ac_activation(ac_switch_0) | 1 |
| s15_13 | coffee_break(coffee_machine_0) 411 to 422 (retraction at 423 (none(leader_inadequate))) | deliver_item(item_2) 123 to 130 (retraction at 131 (none(leader_inadequate))) while ac_activation(ac_switch_0) | coffee_break(coffee_machine_0) 401 to 422 (retraction at 423 (none(leader_inadequate))) | deliver_item(item_2) 123 to 130 (retraction at 131 (none(leader_inadequate))) while ac_activation(ac_switch_0) | 1 |
| s15_14 | coffee_break(coffee_machine_0) 379 to 390 (retraction at 391 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 369 to 390 (retraction at 391 (none(leader_inadequate))) | none | 1 |
| s15_15 | coffee_break(coffee_machine_0) 379 to 390 (retraction at 391 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 369 to 390 (retraction at 391 (none(leader_inadequate))) | none | 1 |
| s15_16 | coffee_break(coffee_machine_0) 379 to 390 (retraction at 391 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 369 to 390 (retraction at 391 (none(leader_inadequate))) | none | 1 |
| s15_17 | coffee_break(coffee_machine_0) 367 to 378 (retraction at 379 (none(leader_inadequate))) | none | none | none | 0 |
| s15_18 | coffee_break(coffee_machine_0) 319 to 330 (retraction at 331 (none(leader_inadequate))) | none | none | none | 0 |
| s15_19 | coffee_break(coffee_machine_0) 333 to 344 (retraction at 345 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 322 to 344 (retraction at 345 (none(leader_inadequate))) | deliver_item(item_4) 216 to 261 (retraction at 262 (none(leader_no_observation))) while deliver_item(item_1) (complete: pinned), ac_activation(ac_switch_0) | 1 |
| s15_20 | coffee_break(coffee_machine_0) 333 to 344 (retraction at 345 (none(leader_inadequate))) | none | coffee_break(coffee_machine_0) 322 to 344 (retraction at 345 (none(leader_inadequate))) | none | 0 |
| s15_21 | none | none | none | none | 1 |

### The stretches sorted by direction and side (within one script: off against on, the same tick span)

Delay: admitted tick minus the stretch's first tick; `never` sorts last. A rival's side is the set of its levels from the stretch's start to the later admission.

- 1, a delivery, no rival raised (on: ordinary or suppressed), admitted earlier on than off, against off: 181 stretches; 1 live: as stated 38 (on's delays 0: 38); 2 live: as stated 38, equal 12 (on's delays 4: 10, 6: 2, 7: 2, 8: 1, 21: 4, 36: 2, 37: 14, 38: 4, 40: 11); 3 live: as stated 50, equal 10 (on's delays 8: 7, 10: 5, 20: 23, 21: 4, 27: 2, 48: 19); 4 live: as stated 19, equal 14 (on's delays 26: 33)
  - equal: s13_01 deliver_item(item_1) from 124 (2 live): off 37, on 37
  - equal: s13_08 deliver_item(item_1) from 193 (2 live): off 37, on 37
  - equal: s13_09 deliver_item(item_1) from 193 (2 live): off 37, on 37
  - equal: s13_10 deliver_item(item_1) from 193 (2 live): off 37, on 37
  - equal: s13_03 deliver_item(item_1) from 198 (2 live): off 21, on 21
  - equal: s13_11 deliver_item(item_1) from 198 (2 live): off 21, on 21
  - equal: s13_12 deliver_item(item_1) from 198 (2 live): off 21, on 21
  - equal: s13_04 deliver_item(item_1) from 124 (2 live): off 37, on 37
  - equal: s13_13 deliver_item(item_1) from 124 (2 live): off 37, on 37
  - equal: s13_06 deliver_item(item_1) from 194 (2 live): off 37, on 37
  - equal: s13_07 deliver_item(item_1) from 241 (2 live): off 37, on 37
  - equal: s13_15 deliver_item(item_1) from 124 (2 live): off 37, on 37
  - equal: s13_02 deliver_item(item_2) from 141 (3 live): off 8, on 8
  - equal: s13_08 deliver_item(item_2) from 141 (3 live): off 8, on 8
  - equal: s13_09 deliver_item(item_2) from 141 (3 live): off 8, on 8
  - equal: s13_10 deliver_item(item_2) from 141 (3 live): off 8, on 8
  - equal: s13_06 deliver_item(item_2) from 149 (3 live): off 21, on 21
  - equal: s13_07 deliver_item(item_2) from 196 (3 live): off 21, on 21
  - equal: s15_06 deliver_item(item_2) from 149 (3 live): off 21, on 21
  - equal: s15_07 deliver_item(item_2) from 196 (3 live): off 21, on 21
  - equal: s15_12 deliver_item(item_2) from 137 (3 live): off 27, on 27
  - equal: s15_13 deliver_item(item_2) from 170 (3 live): off 27, on 27
  - equal: s13_01 deliver_item(item_3) from 0 (4 live): off 26, on 26
  - equal: s13_02 deliver_item(item_3) from 0 (4 live): off 26, on 26
  - equal: s13_08 deliver_item(item_3) from 0 (4 live): off 26, on 26
  - equal: s13_09 deliver_item(item_3) from 0 (4 live): off 26, on 26
  - equal: s13_10 deliver_item(item_3) from 0 (4 live): off 26, on 26
  - equal: s13_03 deliver_item(item_3) from 0 (4 live): off 26, on 26
  - equal: s13_11 deliver_item(item_3) from 0 (4 live): off 26, on 26
  - equal: s13_12 deliver_item(item_3) from 0 (4 live): off 26, on 26
  - equal: s13_04 deliver_item(item_3) from 0 (4 live): off 26, on 26
  - equal: s13_13 deliver_item(item_3) from 0 (4 live): off 26, on 26
  - equal: s13_05 deliver_item(item_3) from 0 (4 live): off 26, on 26
  - equal: s13_06 deliver_item(item_3) from 0 (4 live): off 26, on 26
  - equal: s13_07 deliver_item(item_3) from 0 (4 live): off 26, on 26
  - equal: s13_15 deliver_item(item_3) from 0 (4 live): off 26, on 26
- 1, the coffee break never raised, admitted later on than off, against off: 17 stretches; 1 live: as stated 3 (on's delays 30: 1, 54: 1, 71: 1); 2 live: as stated 5 (on's delays 28: 1, 29: 1, 51: 1, 52: 1, 68: 1); 3 live: as stated 7, equal 2 (on's delays 16: 2, 26: 2, 41: 2, 50: 3)
  - equal: s13_07 coffee_break(coffee_machine_0) from 122 (3 live): off 41, on 41
  - equal: s15_07 coffee_break(coffee_machine_0) from 122 (3 live): off 41, on 41
- 2, the coffee break raised throughout, admitted earlier, against off: 10 stretches; 0 live: as stated 1 (on's delays 0: 1); 1 live: as stated 5 (on's delays 21: 2, 26: 1, 45: 2); 2 live: as stated 3 (on's delays 14: 1, 40: 1, 46: 1); 3 live: as stated 1 (on's delays 15: 1)
- 2, the coffee break raised throughout, admitted earlier, against on without the raising fact (the same script): 7 pairs
  - as stated: coffee_break(coffee_machine_0) from 67 (3 live): s13_08 with 15, s13_02 without 50, off 34
  - as stated: coffee_break(coffee_machine_0) from 67 (3 live): s13_08 with 15, s13_10 without 50, off 34
  - as stated: coffee_break(coffee_machine_0) from 124 (2 live): s13_11 with 14, s13_03 without 51, off 34
  - as stated: coffee_break(coffee_machine_0) from 217 (1 live): s13_04 with 21, s13_13 without 54, off 32
  - as stated: coffee_break(coffee_machine_0) from 89 (2 live): s14_12 with 40, s14_02 without 68, off 54
  - as stated: coffee_break(coffee_machine_0) from 181 (1 live): s14_03 with 45, s14_19 without 71, off 54
  - as stated: coffee_break(coffee_machine_0) from 181 (1 live): s14_18 with 45, s14_19 without 71, off 54
  - no on side without the raising fact in the set for: s14_06 coffee_break(coffee_machine_0) from 179 (2 live); s15_04 coffee_break(coffee_machine_0) from 217 (1 live); s15_17 coffee_break(coffee_machine_0) from 217 (1 live); s15_21 coffee_break(coffee_machine_0) from 309 (0 live)
- 2, a delivery with a rival raised throughout, admitted later, against off: 22 stretches; 1 live: against 3, as stated 6 (on's delays 15: 1, 19: 1, 20: 1, 36: 2, 37: 1, 39: 1, 53: 2); 2 live: as stated 3, equal 1 (on's delays 38: 1, 47: 1, 50: 2); 3 live: against 2, as stated 4 (on's delays 23: 1, 35: 3, 49: 1, 51: 1); 4 live: as stated 3 (on's delays 27: 1, 30: 2)
  - against: s15_01 deliver_item(item_4) from 217 (1 live): off 45, on 37
  - against: s15_18 deliver_item(item_4) from 217 (1 live): off 45, on 39
  - against: s15_17 deliver_item(item_4) from 290 (1 live): off 23, on 20
  - equal: s15_18 deliver_item(item_1) from 124 (2 live): off 47, on 47
  - against: s14_17 deliver_item(item_0) from 0 (3 live): off 50, on 49
  - against: s15_18 deliver_item(item_2) from 67 (3 live): off 30, on 23
- 2, a delivery with a rival raised throughout, admitted later, against on without the raising fact (the same script): 22 pairs
  - as stated: deliver_item(item_3) from 0 (4 live): s13_14 with 27, s13_01 without 26, off 26
  - as stated: deliver_item(item_2) from 67 (3 live): s13_14 with 35, s13_01 without 20, off 30
  - as stated: deliver_item(item_1) from 124 (2 live): s13_14 with 38, s13_01 without 37, off 37
  - as stated: deliver_item(item_2) from 67 (3 live): s13_11 with 35, s13_03 without 20, off 30
  - as stated: deliver_item(item_2) from 67 (3 live): s13_12 with 35, s13_03 without 20, off 30
  - as stated: deliver_item(item_0) from 0 (3 live): s14_20 with 51, s14_01 without 48, off 50
  - as stated: deliver_item(item_2) from 89 (2 live): s14_20 with 50, s14_01 without 40, off 49
  - as stated: deliver_item(item_2) from 89 (2 live): s14_18 with 50, s14_03 without 40, off 49
  - as stated: deliver_item(item_2) from 89 (2 live): s14_18 with 50, s14_19 without 40, off 49
  - as stated: deliver_item(item_0) from 0 (3 live): s14_17 with 49, s14_07 without 48, off 50
  - as stated: deliver_item(item_0) from 0 (3 live): s14_17 with 49, s14_15 without 48, off 50
  - as stated: deliver_item(item_0) from 0 (3 live): s14_17 with 49, s14_16 without 48, off 50
  - as stated: deliver_item(item_1) from 230 (1 live): s14_21 with 15, s14_08 without 0, off 12
  - as stated: deliver_item(item_3) from 0 (4 live): s15_18 with 30, s15_01 without 26, off 28
  - as stated: deliver_item(item_2) from 67 (3 live): s15_18 with 23, s15_01 without 20, off 30
  - as stated: deliver_item(item_1) from 124 (2 live): s15_18 with 47, s15_01 without 38, off 47
  - as stated: deliver_item(item_4) from 290 (1 live): s15_17 with 20, s15_04 without 0, off 23
  - as stated: deliver_item(item_3) from 0 (4 live): s15_16 with 30, s15_08 without 26, off 28
  - as stated: deliver_item(item_3) from 0 (4 live): s15_16 with 30, s15_14 without 26, off 28
  - as stated: deliver_item(item_3) from 0 (4 live): s15_16 with 30, s15_15 without 26, off 28
  - as stated: deliver_item(item_4) from 264 (1 live): s15_20 with 19, s15_10 without 0, off 15
  - as stated: deliver_item(item_4) from 264 (1 live): s15_20 with 19, s15_19 without 0, off 15
  - no on side without the raising fact in the set for: s13_01 deliver_item(item_4) from 217 (1 live); s13_14 deliver_item(item_4) from 217 (1 live); s14_01 deliver_item(item_1) from 181 (1 live); s14_20 deliver_item(item_1) from 181 (1 live); s15_01 deliver_item(item_4) from 217 (1 live); s15_18 deliver_item(item_4) from 217 (1 live)
- 5, stretches with a level changing to or from raised inside the span (read in the section on edges): 25: s13_09 coffee_break(coffee_machine_0), s13_02 deliver_item(item_1), s13_02 deliver_item(item_4), s13_12 coffee_break(coffee_machine_0), s13_03 deliver_item(item_4), s13_05 deliver_item(item_1), s13_05 deliver_item(item_4), s13_06 deliver_item(item_4), s14_13 coffee_break(coffee_machine_0), s14_14 coffee_break(coffee_machine_0), s14_02 deliver_item(item_1), s14_04 deliver_item(item_1), s14_05 deliver_item(item_1), s15_02 deliver_item(item_1), s15_02 deliver_item(item_4), s15_03 deliver_item(item_4), s15_17 deliver_item(item_1), s15_05 deliver_item(item_1), s15_05 deliver_item(item_4), s15_06 deliver_item(item_1), s15_06 deliver_item(item_4), s15_07 deliver_item(item_1), s15_10 deliver_item(item_1), s15_20 deliver_item(item_1), s15_13 ac_activation(ac_switch_0)
