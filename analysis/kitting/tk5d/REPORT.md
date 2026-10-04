# T-K part 1, step 5d: the measurements after the gate change (kitting)

Written by ccode, 5 October 2026. Step 5d of T-K part 1 (docs/handoffs/T-G_forward_inputs.md, 5.7): the runs of steps
4, 5 and 5b again, with context knowledge on, after step 5c (the gate after step 5b: AM67, observation warrant required
at admission for every hypothesis; AM68, the gate refuses a leader the evidence alone ranks below another live
hypothesis; built 2c939a5 to b18a208, plan docs/handoffs/plan_T-K_gate.md). No scenario, value or framework code was
changed for this step.

**The scenarios are authored.** Each was written to place a case. Every count below compares settings on the same
scripts; none is a rate of occurrence.

The three settings:
- **off**: context knowledge off (the equal prior), after the gate change. With context knowledge off the gate change
  acts through AM67 only (AM68 refuses nothing when the belief is the evidence).
- **on, before**: context knowledge on, steps 4, 5 and 5b as measured (4 October 2026; analysis/kitting/mpb/tk5b/
  COMPARISON.md, frozen; outputs in /home/hadi/teamrob_analysis_2026-10-04_gate/).
- **on, after**: context knowledge on, step 5d.

The pairs: recognition, 74 (57 of step 4, 17 of step 5b), the robot idle; planning, 22 on runs (6 of step 5, 16 of step
5b) against their off runs, single_task. Each comparison is within one script.

## 0. What was run and checked

- Expectations from the updated oracles, committed before the runs (f02b04c), and step 5's properties moved by the
  rulings re-declared before them (D5): PK4a.r, PK4b.r, PK4e.r, PK1b.r, PK5a.r; PK4c and PK5b leave, the separation in
  their windows a measure (analysis/kitting/mpb/properties.py).
- The runs: step 4's 57 and its two off runs, step 5b's 17 recognition runs, step 5's 6 and its 3 off runs, step 5b's
  16 planning runs. Every run's own oracle call reproduced the committed expectations. The recognizer's outputs in the
  74 recognition runs are identical to before the gate change (belief, prior, adequacy, warrant): the gate does not act
  on recognition, and the human is open-loop.
- A stop, then a ruling. Two planning runs of step 5b (scenario_s10_04, s12_02) stopped the instrument's chain at their
  decision of tick 135: coffee_break re-enters after its completion with one delivery live, the re-entry rule gives it
  1/|H| = 1/2 of the evidence, so the two evidences are exactly equal; the recognizer passes the tie (AM75), the oracle
  marked it undetermined (D3). Hadi ruled D3 amended (5 October 2026): an exact equality of the oracle's own evidence is
  a tie, not outranked; undetermined stays for close values that are not equal. The oracle and the comparison were
  rerun on all of kitting's test-bed outputs (no simulation). Every change of the tables was a cell marked undetermined
  before: 3241 rank cells became not_outranked, 6 gate ticks clears (the same re-entry tie, in 6 recognition runs), and
  the two chains' gate at 135 clears.
- Result: 0 disagreements with the oracles in every run of the step (recognition 76, planning 25) and in every
  context-off test-bed set rerun under the amendment (the IRB's s08 and s09, round 1, the planning set under both
  strategies). Undetermined left: 2 rank cells in scenario_s09_07 at 35 (a tie decided by rounding, D7), no gate.
  Known and unchanged: the print-precision flag of the s14_02 script (its four runs).
- Step 5's properties: every re-declared one holds; PK3c and PK2b fail as before the gate change (the turn, TODO-146).
  Step 5b's: P10.10 fails as before (s10_10 does not reach E6); every other declared property holds.
- Coverage row B12 (the outranked refusal, D4): verified, scenario_s16_03 and s16_05 refuse their tick-0
  `no_current_task` decision `none(leader_outranked)`.
- The alteration test on step 5's six (D6): C4 (the outranked condition not asked) and C6 (the rank read from the
  belief) detected in s16_03 and s16_05 (56 disagreements each); C5 (an exact tie counted outranked, as amended)
  undetected in all six: on no tick of the six does a leader pass θ, adequacy and warrant tied with another hypothesis.
  A property of the set. As a diagnostic outside D6's scope, C5 is detected on s10_04 and s12_02 (99 each), where the
  tie falls on a decision.

## 1. The comparison: off, on before the gate change, on after it

| measure | off | on, before | on, after |
|---|---|---|---|
| admissions of the true task (325 true stretches): earlier / equal / later than off | - | 206 / 48 / 42; on only 10, neither 19 | 206 / 48 / 42; on only 10, neither 19 |
| ticks earlier / later than off, in those admissions | - | 3005 / 365 | 3005 / 365 |
| of which assigned deliveries (266) | - | 193 / 44 / 18 (2824 / 47 ticks) | 193 / 44 / 18 (2824 / 47 ticks) |
| of which coffee_break (39) | - | raised: 11 of 11 earlier (median −14); ordinary: 24 of 28 later (median +13.5) | the same |
| admissions of a hypothesis that is not the true task, during modelled tasks: count; gate ticks; trigger-rule ticks | 9; 63; 88 (before: 17; 114; 146) | 47; 504; 613 | 19; 99; 184 |
| their kinds, by the evidence alone (off run): (i) near-tie / (ii) the true task first, the prior overruling / (iii) the evidence ranking the admitted one first / no true hypothesis: rows; gate ticks | - | 0 / 17 / 26 / 4; 0 / 310 / 149 / 45 | 0 / 0 / 17 / 2; 0 / 0 / 66 / 33 |
| the same on the exit walk: count; gate ticks | 52; 1089 (per pair; unchanged) | 51; 1166 | 50; 1149 |
| one-tick admissions of the next delivery on the previous task's pin tick | 0 (before: 6) | 58 | 0 |
| a lone assigned task admitted before the human starts it: started on the next tick; retracted (ticks) | 0; 0 (before: 5; 1, 7 ticks) | 59; 9 (247 ticks) | 0; 0 |
| planning, completion against off (22 runs): better / equal / worse | - | 7 / 13 / 2 | 5 / 16 / 1 |
| planning, completion ticks gained / lost | - | 134 (78 of them s11_03) / 3 | 50 / 1 |
| planning, decision records holding a hypothesis that is not the true task, before the robot's completion: count; ticks | 8; 100 (before: 11; 113) | 33; 305 | 10; 106 |
| planning, cases below min_separation | 2 (s16_01, s12_02) | 5 (s16_01, s16_02, s16_05, s11_03, s12_02) | 3 (s16_01, s16_02, s12_02) |
| their ticks: standing robot / moving robot (F1 viol / recede) | 8 / 3 (2 / 1) | 7 / 18 (10 / 8) | 3 / 7 (4 / 3) |
| by cause: a wrong admission | 0 | 2 (s16_05 28.3 cm; s11_03 11.3 cm) | 0 |
| by cause: the gap between plan and execution at a turn (TODO-146) | 0 | 2 (s16_01 41.7 cm; s16_02 29.3 cm) | 2 (the same) |
| by cause: other | 2 (s16_01 37.0 cm; s12_02 32.3 cm) | 1 (s12_02 33.6 cm) | 1 (s12_02 33.6 cm) |

The off column is the off setting after the gate change; where it differs from the off of COMPARISON.md, the earlier
value is in brackets. Notes on the measures as COMPARISON.md states them (kinds read per wrong tick from the off run's
belief, the ratio threshold 1.01 a reporting threshold; "per pair" in step 4, where one off run is the off side of
several timelines). The full tables after the gate change: appendix A.

### 1.1 Every case that moved

Classes: as expected by ruling (the case moves exactly as AM67 or AM68 states); a limitation; a defect. **Every case
that moved is as expected by ruling.** No case moved for any other reason, no new case formed, and no defect was found
in the framework. The instrument stop of section 0 is recorded there.

**Planning: the decisions that moved (on runs; the off runs of steps 5 and 5b are unchanged except where noted).**

| run | before | after | cause | class |
|---|---|---|---|---|
| s16_03 (case 4) | item_4 admitted at 0 (no hold), held 43 ticks against the coffee break; retraction at 43 | tick 0 refused `none(leader_outranked)`, fallbacks until coffee_break entered at 55; item_4 at 74; completion 89 (unchanged) | AM68 | as expected by ruling |
| s16_04 (case 1) | item_4 at 73 (one tick before the human starts it) | item_4 at 74; completion 90 → 91 | AM67 | as expected by ruling |
| s16_05 (case 5) | item_4 admitted at 0, no hold; the pass 22 to 27 at 28.3 cm (4 F1 violations); completion 101 | tick 0 refused `none(leader_outranked)`; the decisions of off (hold 5 at 14 on a fallback); item_4 at 48 (off 63); min 60.4 cm; completion 106 (= off) | AM68 | as expected by ruling |
| s16_06 (the A/C raised) | item_4 at 47 | `none(leader_unwarranted)` at 47, item_4 at 48; measures unchanged | AM67 | as expected by ruling |
| s10_01, s10_02, s10_05, s12_01 | item_2 at 62, one tick before the human starts it | item_2 at 63; s12_01's later decisions shift (one fewer), completion unchanged | AM67 | as expected by ruling |
| s10_03, s10_07, s10_08, s10_10 | a delivery at 150 / 124 / 109 / 140, one tick before its start | one tick later, on its start | AM67 | as expected by ruling |
| s10_04 | item_2 at 62 and 67 (22 ticks held while the human takes a coffee break), retraction at 84; item_2 at 134 | from 64 refused `none(leader_outranked)`; item_2 at 135 (the re-entry tie, passed); measures unchanged | AM68, AM67 | as expected by ruling |
| s10_09 | item_1, never placed, admitted at 160 near the robot's last decision | refused `none(leader_unwarranted)` | AM67 | as expected by ruling |
| s10_11 | item_1 at 136 on commitment alone, retraction at 147 | refused `none(leader_unwarranted)` (the same in its off run, the build) | AM67 | as expected by ruling |
| s11_01, s11_02 | the standing human's never-performed item_12 admitted at 0, retraction at 16 / 10 | refused `none(leader_unwarranted)` throughout; the decisions of off; s11_01 completion 76 → 74 | AM67 | as expected by ruling |
| s11_03 | item_12 admitted at 0; no hold; item_8 released 11.3 cm from the standing human (4 standing, 5 moving ticks below 50 cm); completion 35 | refused `none(leader_unwarranted)` throughout; the decisions of off (hold 3 at 6); min 51.3 cm; completion 113 (= off) | AM67 | as expected by ruling |
| s12_02 | item_2 at 62 held 22 ticks while the human takes a coffee break, retraction at 84; item_2 at 134 | from 64 refused `none(leader_outranked)`; item_2 at 135 (the tie, passed); its case below min_separation unchanged (33.6 cm, the human walking past the robot standing in its hold) | AM68, AM67 | as expected by ruling |
| off: s10_04, s10_11, s12_02 (the planning set's reference) | commitment-only admissions at 134 / 136 / 134 | 140 / none / 140 (moved in the build, stage 3; completion unchanged) | AM67 | as expected by ruling |

**Recognition: the admissions of a hypothesis that is not the true task that moved** (108 rows; `kind`: main, during
modelled tasks; pin, on the previous task's pin tick; exit, on the exit walk. "The gate after the change on the lost
ticks" names the refusal on every tick the row lost: none(leader_outranked) is AM68, none(leader_unwarranted) AM67;
written by `moved5d.py`):

| side | scenario | kind | admitted | before: ticks (gate) | after | the gate after the change on the lost ticks | class |
|---|---|---|---|---|---|---|---|
| step 4, on | s13_03 | main | item_4 | 150-161 (12) | absent | none(leader_outranked) 12 | as expected by ruling (AM68) |
| step 4, on | s13_03 | pin | item_4 | 279-279 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s13_04 | pin | item_4 | 289-289 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s13_05 | main | item_2 | 96-99 (4) | absent | none(leader_unwarranted) 4 | as expected by ruling (AM67) |
| step 4, on | s13_06 | main | item_2 | 96-103 (8) | 96-99 (4) | none(leader_outranked) 4 | as expected by ruling (AM68) |
| step 4, on | s13_07 | main | item_2 | 123-130 (8) | absent | none(leader_unwarranted) 8 | as expected by ruling (AM67) |
| step 4, on | s13_07 | pin | item_4 | 334-334 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s13_08 | pin | item_4 | 285-285 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s13_09 | pin | item_4 | 285-285 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s13_10 | pin | item_4 | 285-285 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s13_11 | main | coffee_break | 81-91 (11) | absent | none(leader_outranked) 11 | as expected by ruling (AM68) |
| step 4, on | s13_11 | pin | item_4 | 279-279 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s13_12 | main | coffee_break | 81-91 (11) | absent | none(leader_outranked) 11 | as expected by ruling (AM68) |
| step 4, on | s13_12 | main | item_4 | 150-161 (12) | absent | none(leader_outranked) 12 | as expected by ruling (AM68) |
| step 4, on | s13_12 | pin | item_4 | 279-279 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s13_13 | main | item_4 | 216-258 (43) | absent | none(leader_outranked) 42, none(leader_unwarranted) 1 | as expected by ruling (AM68, AM67) |
| step 4, on | s13_13 | pin | item_4 | 289-289 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s13_14 | main | coffee_break | 81-91 (11) | absent | none(leader_outranked) 11 | as expected by ruling (AM68) |
| step 4, on | s13_15 | pin | item_4 | 216-216 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s13_15 | main | item_4 | 262-269 (8) | absent | none(leader_unwarranted) 8 | as expected by ruling (AM67) |
| step 4, on | s13_15 | pin | item_4 | 309-309 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_02 | pin | item_1 | 225-225 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_03 | pin | item_1 | 259-259 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_04 | main | item_2 | 135-136 (2) | absent | none(leader_unwarranted) 2 | as expected by ruling (AM67) |
| step 4, on | s14_04 | pin | item_1 | 233-233 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_05 | main | item_2 | 135-146 (12) | 135-138 (4) | none(leader_outranked) 8 | as expected by ruling (AM68) |
| step 4, on | s14_05 | pin | item_1 | 226-226 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_06 | main | item_2 | 180-187 (8) | absent | none(leader_unwarranted) 8 | as expected by ruling (AM67) |
| step 4, on | s14_06 | pin | item_1 | 307-307 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_07 | pin | item_1 | 192-192 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_08 | pin | item_1 | 229-229 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_09 | main | item_2 | 135-136 (2) | absent | none(leader_unwarranted) 2 | as expected by ruling (AM67) |
| step 4, on | s14_09 | pin | item_1 | 194-194 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_10 | main | item_2 | 135-140 (6) | 135-137 (3) | none(leader_outranked) 3 | as expected by ruling (AM68) |
| step 4, on | s14_10 | pin | item_1 | 191-191 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_11 | main | item_2 | 180-187 (8) | absent | none(leader_unwarranted) 8 | as expected by ruling (AM67) |
| step 4, on | s14_11 | pin | item_1 | 276-276 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_12 | pin | item_1 | 225-225 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_13 | pin | item_1 | 225-225 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_14 | pin | item_1 | 225-225 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_15 | pin | item_1 | 192-192 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_16 | pin | item_1 | 192-192 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_17 | pin | item_1 | 192-192 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_18 | pin | item_1 | 259-259 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_19 | main | item_1 | 180-239 (60) | absent | none(leader_outranked) 59, none(leader_unwarranted) 1 | as expected by ruling (AM68, AM67) |
| step 4, on | s14_19 | pin | item_1 | 259-259 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s14_21 | main | coffee_break | 221-227 (7) | absent | none(leader_outranked) 7 | as expected by ruling (AM68) |
| step 4, on | s15_03 | main | item_4 | 151-161 (11) | absent | none(leader_outranked) 11 | as expected by ruling (AM68) |
| step 4, on | s15_03 | pin | item_4 | 279-279 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s15_04 | pin | item_4 | 289-289 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s15_05 | main | item_2 | 96-99 (4) | absent | none(leader_unwarranted) 4 | as expected by ruling (AM67) |
| step 4, on | s15_06 | main | item_2 | 96-103 (8) | 96-99 (4) | none(leader_outranked) 4 | as expected by ruling (AM68) |
| step 4, on | s15_07 | main | item_2 | 123-130 (8) | absent | none(leader_unwarranted) 8 | as expected by ruling (AM67) |
| step 4, on | s15_07 | pin | item_4 | 334-334 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s15_08 | pin | item_4 | 276-276 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s15_09 | pin | item_4 | 229-229 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s15_10 | pin | item_4 | 263-263 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s15_11 | main | item_2 | 96-98 (3) | absent | none(leader_unwarranted) 3 | as expected by ruling (AM67) |
| step 4, on | s15_11 | main | item_4 | 111-118 (8) | 112-118 (7) | none(leader_outranked) 1 | as expected by ruling (AM68) |
| step 4, on | s15_11 | pin | item_4 | 296-296 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s15_12 | main | item_2 | 96-108 (13) | 96-104 (9) | none(leader_outranked) 4 | as expected by ruling (AM68) |
| step 4, on | s15_12 | pin | item_4 | 278-278 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s15_13 | main | item_2 | 123-130 (8) | absent | none(leader_unwarranted) 8 | as expected by ruling (AM67) |
| step 4, on | s15_13 | pin | item_4 | 308-308 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s15_14 | pin | item_4 | 276-276 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s15_15 | pin | item_4 | 276-276 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s15_16 | pin | item_4 | 276-276 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s15_19 | main | item_4 | 216-261 (46) | absent | none(leader_outranked) 45, none(leader_unwarranted) 1 | as expected by ruling (AM68, AM67) |
| step 4, on | s15_19 | pin | item_4 | 263-263 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 4, on | s15_21 | pin | item_4 | 216-216 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s08_01 | pin | item_2 | 62-62 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s08_02 | main | item_2 | 62-83 (22) | absent | none(leader_outranked) 21, none(leader_unwarranted) 1 | as expected by ruling (AM68, AM67) |
| step 5b, on | s08_02 | pin | item_2 | 134-134 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s08_03 | main | item_1 | 32-42 (11) | 32-40 (9) | none(leader_outranked) 2 | as expected by ruling (AM68) |
| step 5b, on | s08_03 | pin | item_2 | 128-128 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s08_04 | main | item_1 | 32-39 (8) | absent | none(leader_unwarranted) 8 | as expected by ruling (AM67) |
| step 5b, on | s08_04 | pin | item_2 | 140-140 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s09_01 | pin | item_2 | 62-62 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s09_02 | main | item_2 | 62-83 (22) | absent | none(leader_outranked) 21, none(leader_unwarranted) 1 | as expected by ruling (AM68, AM67) |
| step 5b, on | s09_02 | pin | item_2 | 134-134 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s09_03 | main | item_1 | 32-42 (11) | 32-40 (9) | none(leader_outranked) 2 | as expected by ruling (AM68) |
| step 5b, on | s09_03 | pin | item_2 | 128-128 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s09_04 | main | item_1 | 32-39 (8) | absent | none(leader_unwarranted) 8 | as expected by ruling (AM67) |
| step 5b, on | s09_04 | pin | item_2 | 140-140 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s09_05 | pin | item_2 | 129-129 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s09_06 | pin | item_2 | 104-104 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s09_07 | pin | item_1 | 109-109 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s09_08 | exit | item_1 | 132-148 (17) | absent | none(leader_outranked) 14, none(leader_unwarranted) 3 | as expected by ruling (AM68, AM67) |
| step 5b, on | s09_09 | main | item_2 | 62-72 (11) | absent | none(leader_unwarranted) 11 | as expected by ruling (AM67) |
| step 5b, on | s09_09 | main | item_2 | 108-108 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s09_10 | pin | item_3 | 62-62 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s09_11 | main | item_3 | 62-79 (18) | absent | none(leader_outranked) 17, none(leader_unwarranted) 1 | as expected by ruling (AM68, AM67) |
| step 5b, on | s09_11 | pin | item_3 | 134-134 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s09_12 | pin | item_1 | 62-62 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| step 5b, on | s09_13 | pin | item_2 | 150-150 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| off (step 4's) | s13_15 | main | item_4 | 262-268 (7) | absent | none(leader_unwarranted) 7 | as expected by ruling (AM67) |
| off (step 4's) | s13_15 | pin | item_4 | 309-309 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| off (round 1) | s13_04 | pin | item_4 | 289-289 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| off (round 1) | s13_07 | main | item_2 | 123-130 (8) | absent | none(leader_unwarranted) 8 | as expected by ruling (AM67) |
| off (round 1) | s14_06 | main | item_2 | 180-187 (8) | absent | none(leader_unwarranted) 8 | as expected by ruling (AM67) |
| off (round 1) | s14_11 | main | item_2 | 180-187 (8) | absent | none(leader_unwarranted) 8 | as expected by ruling (AM67) |
| off (round 1) | s15_07 | main | item_2 | 123-130 (8) | absent | none(leader_unwarranted) 8 | as expected by ruling (AM67) |
| off (round 1) | s15_13 | main | item_2 | 123-130 (8) | absent | none(leader_unwarranted) 8 | as expected by ruling (AM67) |
| off (s08, s09) | s08_02 | pin | item_2 | 134-134 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| off (s08, s09) | s08_04 | main | item_1 | 32-33 (2) | absent | none(leader_unwarranted) 2 | as expected by ruling (AM67) |
| off (s08, s09) | s09_02 | pin | item_2 | 134-134 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |
| off (s08, s09) | s09_04 | main | item_1 | 32-33 (2) | absent | none(leader_unwarranted) 2 | as expected by ruling (AM67) |
| off (s08, s09) | s09_11 | pin | item_3 | 134-134 (1) | absent | none(leader_unwarranted) 1 | as expected by ruling (AM67) |

No admission of the true task moved in any of the 543 true stretches of these runs (on and off, the reference sets
included): the ticks the gate change removed all lie outside the true task.

## 2. The effect of step 5c alone (on, before against on, after)

**What the two rulings removed.**
- Recognition, during modelled tasks: 28 of 47 wrong admissions removed and 8 shortened; 405 of 504 gate ticks
  (trigger rule: 429 of 613). By kind: all 17 rows of kind (ii), where the evidence alone ranked the true task first and
  the prior overruled it (310 gate ticks; the admitted leader is outranked by construction, so AM68 refuses it, or AM67
  where the leader also lacks observation warrant, since outranked is asked last); 9 of 26 rows of kind (iii) removed
  and 8 shortened; 2 of 4 rows with no true hypothesis (s09_09). The ruling per row: 1.1.
- The one-tick admissions of the next delivery on the previous task's pin tick (58) and the lone assigned task admitted
  before the human starts it (59 started on the next tick, 9 retracted after 8 to 60 ticks, 247 ticks): all removed
  (AM67). With context knowledge off the same holds for its 6 and 1.
- Planning: decision records holding a wrong hypothesis before the robot's completion 33 → 10 (305 → 106 ticks).
- **The two cases below min_separation that came from a wrong admission are gone, and no violation recurs in another
  form.** scenario_s16_05 (case 5): the admission of item_4 at 0 while the human walks to the A/C switch is refused
  outranked; the robot decides as off does (a hold of 5 at 14 on the moving fallback), the minimum separation is 60.4 cm
  at 27 (before: 28.3 cm at 25, 4 F1 violations). scenario_s11_03: the never-performed delivery of the standing human
  is never admitted (no observation warrant); the robot decides as off does (a hold of 3 at 6), 51.3 cm at 13 (before:
  11.3 cm at 12, item_8 released beside the human). No new case below min_separation appears in any run.

**What they cost.**
- Completion: s11_03 35 → 113 (+78: the gain of step 5b came from admitting a delivery the human never performed;
  after, it equals off); s16_05 101 → 106 (+5, equal to off); s16_04 90 → 91 (+1). s11_01 gains 2 (76 → 74). The planning
  gain of context knowledge against off falls from 134 to 50 ticks.
- No admission of the true task is later than its first tick: every admission that moved one tick (13 decision records
  in planning; the pin-tick rows in recognition) was one tick before the human started the task, and now falls on its
  start.
- Case 5 loses its premise (D5): with the human walking to the A/C switch against the context, the robot no longer acts
  on the context at all; it behaves as with context knowledge off.

**What they left unchanged.** The recognizer's outputs (belief, adequacy, warrant: identical in all 74 recognition
runs); every admission of the true task in recognition (206 / 48 / 42 against off, 3005 ticks earlier, 365 later);
the coffee break's later admission outside break_time (the prior, not the gate); the A/C never admitted in 18 of its 20
stretches; the turn cases (TODO-146) and s12_02's standing-robot case; the 17 wrong admissions of kind (iii) that
remain (the evidence itself ranks the admitted delivery first) and the 2 with no true hypothesis.

## 3. What context knowledge adds, as it stands after step 5c (on, after against off)

**Earlier recognition of the true task** (the gate's answer on the true stretch; recognition runs, robot idle):

| task, state on the stretch's first tick | stretches | earlier / equal / later | difference on − off (both admitted) | ticks earlier / later |
|---|---|---|---|---|
| assigned delivery, no raising fact | 238 | 182 / 43 / 2; on only 10, neither 1 | median −8, range −51 to +1 | 2641 / 2 |
| assigned delivery, a raising fact holding (break_time or room_warm) | 28 | 11 / 1 / 16 | median +1, range −37 to +5 | 183 / 45 |
| coffee_break, break_time holding (raised) | 11 | 11 / 0 / 0 | median −14, range −25 to −6 | 156 / 0 |
| coffee_break, ordinary | 28 | 2 / 2 / 24 | median +13.5, range −14 to +22 | 25 / 318 |
| ac_activation, room_warm holding (raised) | 8 | neither admitted in 8 | - | - |
| ac_activation, ordinary | 12 | 0 / 2 / 0; neither 10 | 0 | 0 / 0 |
| all | 325 | 206 / 48 / 42; on only 10, neither 19 | - | 3005 / 365 |

**Where it makes recognition later or wrong.**
- Later: the coffee break outside break_time (24 of 28 stretches, 318 ticks, median +13.5); a delivery while a raising
  fact favours a foreseeable task (16 of 28, 45 ticks, at most +5).
- Wrong, during modelled tasks: 19 admissions (99 gate ticks; 184 ticks held by the trigger rule) against off's 9 (63;
  88). 11 occur with context knowledge on only (36 gate ticks), all in step 4: a delivery admitted while the human walks
  to the coffee machine or the A/C switch, 1 to 9 ticks, in each the evidence alone ranking the delivery first (kind
  (iii)). 8 occur on both sides, longer on (s08_03 and s09_03: 9 against 5 ticks; s09_05: 16 against 11). 1 occurs with
  context knowledge off only (s09_09: coffee_break 70 to 82, avoided on). On the exit walk 50 against 52 (1149 against
  1089 gate ticks).
- Planning: decision records holding a wrong hypothesis before the robot's completion 10 (106 ticks) against off's 8
  (100).

**The robot's decisions and completion (planning, 22 on runs).**
- Completion: better in 5 runs (s16_03 −24, s16_04 −22, s16_02 −2, s16_01 −1, s12_01 −1; 50 ticks), equal in 16, worse
  in 1 (s12_02 +1).
- The response decision (the first decision with a positive hold or a switch): earlier in 5 runs (s16_01 −45, s16_02 −7,
  s16_04 −14, s10_02 −17, s12_01 −17), later in 2 (s16_03 +6, s12_02 +18), as off in the rest.
- Separation: 3 cases below min_separation against off's 2. The two that occur on only (s16_01 41.7 cm, s16_02 29.3 cm,
  moving robot) are the gap between the admitted plan and the executed human at a turn (TODO-146): the earlier
  admission lets the robot plan against the human's projected turn, which runs about one tick ahead. The third (s12_02,
  33.6 cm; off 32.3 cm) is the human walking past the robot standing in its hold, on both sides.

**The limitations that remain.**
- In the first ticks of a walk the evidence for two targets is nearly equal; no setting of the prior helps there
  (docs/assumptions.md 6.4, its first part).
- A delivery the evidence itself ranks first while the human walks elsewhere (kind (iii)): the context knowledge
  lifts it over θ where the equal prior did not (11 rows, 36 gate ticks).
- A coffee break outside break_time is recognised later (median +13.5 ticks): the ordinary strength against the
  assigned tasks as a whole.
- The A/C activation is not admitted in 18 of 20 stretches, on or off; its measure is its belief at arrival (step 4's
  REPORT.md, KT10; the belief is unchanged by step 5c).
- The human acting against the context (cases 4 and 5): context knowledge now gives the robot nothing there; it acts
  as with context knowledge off once the evidence ranks the context's task first.
- What these sets do not exercise: in step 5b only the state with no raising fact; dock_loading (step 6).

## 4. Conclusion

With context knowledge on, the robot recognises the human's task earlier when the human does what the context makes
likely: the assigned deliveries by a median of 8 ticks, the coffee break inside break_time by 14. The robot then acts
earlier and finishes sooner in 5 of 22 planning runs, by 1 to 24 ticks.

Before step 5c it also admitted tasks against the evidence: a delivery the human had not started, or never did. That
produced the two passes below min_separation. The two gate rulings remove those admissions without delaying the true
task anywhere. The cost is a gain that rested on a wrong admission (78 ticks in s11_03) and one tick in s16_04.

What it pays now: the coffee break outside break_time is recognised later (median +13.5 ticks); a delivery the
evidence already ranks first is admitted while the human walks elsewhere (11 short episodes, 36 ticks); and the turn
cases (TODO-146) show up because the robot plans earlier.

What stays open: the A/C activation (rarely admitted, on or off), the first ticks of a walk, the turn gap (TODO-146),
and dock_loading's part (step 6).

## Appendix A. The full tables after the gate change

Written by `analysis/kitting/mpb/tk5b/comparison.py` from the step's outputs (the off sides after the gate change).

### A. Recognition (57 pairs of step 4, 17 of step 5b)

### A1. Admissions of the true task, on against off

| category (the state on the stretch's first tick, on) | stretches | earlier | equal | later | difference on − off (ticks, both admitted) | ticks earlier, total | ticks later, total | admitted on only | off only | neither |
|---|---|---|---|---|---|---|---|---|---|---|
| assigned delivery, no raising fact | 238 | 182 | 43 | 2 | median -8, range -51 to 1 | 2641 | 2 | 10 | 0 | 1 |
| assigned delivery, a raising fact holding | 28 | 11 | 1 | 16 | median 1, range -37 to 5 | 183 | 45 | 0 | 0 | 0 |
| coffee_break, its raising fact holding | 11 | 11 | 0 | 0 | median -14, range -25 to -6 | 156 | 0 | 0 | 0 | 0 |
| coffee_break, no raising fact (ordinary) | 28 | 2 | 2 | 24 | median 13.5, range -14 to 22 | 25 | 318 | 0 | 0 | 0 |
| ac_activation, its raising fact holding | 8 | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 8 |
| ac_activation, no raising fact (ordinary) | 12 | 0 | 2 | 0 | median 0, range 0 to 0 | 0 | 0 | 0 | 0 | 10 |

### A2. Admissions of a hypothesis that is not the true task

During modelled tasks (the exit walk and the one-tick rows on a completion left out):

| side | count | gate: median | max | total ticks | trigger rule: median | max | total ticks |
|---|---|---|---|---|---|---|---|
| off (per pair) | 9 | 5 | 17 | 63 | 9 | 17 | 88 |
| off (each script once) | 9 | 5 | 17 | 63 | 9 | 17 | 88 |
| on | 19 | 4 | 17 | 99 | 10 | 17 | 184 |
| on, no raising fact | 19 | 4 | 17 | 99 | 10 | 17 | 184 |
| on, a raising fact holding | 0 | - | - | - | - | - | - |

The exit walk:

| side | count | gate: median | max | total ticks | trigger rule: median | max | total ticks |
|---|---|---|---|---|---|---|---|
| off (per pair) | 52 | 22 | 32 | 1089 | 22 | 32 | 1089 |
| off (each script once) | 38 | 22 | 32 | 851 | 22 | 32 | 851 |
| on | 50 | 22 | 32 | 1149 | 22 | 32 | 1149 |

The one-tick rows on a completion (the next delivery admitted on the previous task's pin tick; not wrong from the next tick):

| side | count | gate: median | max | total ticks | trigger rule: median | max | total ticks |
|---|---|---|---|---|---|---|---|
| off (per pair) | 0 | - | - | - | - | - | - |
| off (each script once) | 0 | - | - | - | - | - | - |
| on | 0 | - | - | - | - | - | - |

### A2, the kinds: what the evidence alone said (the off run)

| step | scenario | admitted (on) | wrong ticks (gate) | true task | off ratio true / admitted: first wrong tick, last | ticks (i) / (ii) / (iii) | kind |
|---|---|---|---|---|---|---|---|
| step 4 | s13_05 | item_2 | 94-94 (1) | coffee_break | ×0.4781, ×0.4781 | 0 / 0 / 1 | (iii) |
| step 4 | s13_06 | item_2 | 96-99 (4) | coffee_break | ×0.4163, ×0.8451 | 0 / 0 / 4 | (iii) |
| step 4 | s14_04 | item_2 | 133-133 (1) | coffee_break | ×0.3814, ×0.3814 | 0 / 0 / 1 | (iii) |
| step 4 | s14_05 | item_2 | 135-138 (4) | coffee_break | ×0.3144, ×0.5417 | 0 / 0 / 4 | (iii) |
| step 4 | s14_09 | item_2 | 133-133 (1) | ac_activation | ×0.6780, ×0.6780 | 0 / 0 / 1 | (iii) |
| step 4 | s14_10 | item_2 | 135-137 (3) | ac_activation | ×0.6078, ×0.9275 | 0 / 0 / 3 | (iii) |
| step 4 | s15_05 | item_2 | 94-94 (1) | coffee_break | ×0.4781, ×0.4781 | 0 / 0 / 1 | (iii) |
| step 4 | s15_06 | item_2 | 96-99 (4) | coffee_break | ×0.4163, ×0.8451 | 0 / 0 / 4 | (iii) |
| step 4 | s15_11 | item_2 | 94-94 (1) | ac_activation | ×0.0380, ×0.0380 | 0 / 0 / 1 | (iii) |
| step 4 | s15_11 | item_4 | 112-118 (7) | ac_activation | ×0.4912, ×0.5553 | 0 / 0 / 7 | (iii) |
| step 4 | s15_12 | item_2 | 96-104 (9) | ac_activation | ×0.0285, ×0.1191 | 0 / 0 / 9 | (iii) |
| step 5b | s08_03 | item_1 | 32-40 (9) | coffee_break | ×0.1521, ×0.9065 | 0 / 0 / 9 | (iii) |
| step 5b | s08_04 | item_1 | 30-30 (1) | coffee_break | ×0.1914, ×0.1914 | 0 / 0 / 1 | (iii) |
| step 5b | s09_03 | item_1 | 32-40 (9) | coffee_break | ×0.1521, ×0.9065 | 0 / 0 / 9 | (iii) |
| step 5b | s09_04 | item_1 | 30-30 (1) | coffee_break | ×0.1914, ×0.1914 | 0 / 0 / 1 | (iii) |
| step 5b | s09_05 | item_1 | 32-47 (16) | unmodelled | - | - | none (the true task is no hypothesis) |
| step 5b | s09_06 | item_1 | 30-46 (17) | unmodelled | - | - | none (the true task is no hypothesis) |
| step 5b | s09_07 | item_1 | 32-32 (1) | item_2 | ×0.0005, ×0.0005 | 0 / 0 / 1 | (iii) |
| step 5b | s09_13 | item_1 | 46-54 (9) | coffee_break | ×0.0025, ×0.0272 | 0 / 0 / 9 | (iii) |

Rows: (i) 0, (ii) 0, (iii) 17, no kind 2. Ticks: (i) 0, (ii) 0, (iii) 66, (iv) 0. Gate ticks per kind of row: (i) 0, (ii) 0, (iii) 66, none 33.

### A3. A lone assigned task admitted before the human starts it

| side | ends | count | ticks until it ends: median | range | total | where (scenario: first tick, ticks) |
|---|---|---|---|---|---|---|

### B. Planning (6 on runs of step 5, 16 of step 5b)

### B1 and B2. Completion, the response decision, the separation

| step | scenario | side | completion | Δ to off | response decision (tick: what) | Δ to off | min separation (tick) | ticks below: standing robot | moving robot (F1 viol / recede) | cases below (first-last: min) |
|---|---|---|---|---|---|---|---|---|---|---|
| step 5 | scenario_s16_01 | off | 69 | - | 45: hold 2 | - | 37.0 (48) | 6 | 1 (1 / 0) | 44-50: 37.0 |
| step 5 | scenario_s16_01 | on | 68 | -1 | 0: hold 5 | -45 | 41.7 (50) | 0 | 3 (2 / 1) | 49-51: 41.7 |
| step 5 | scenario_s16_02 | on | 67 | -2 | 38: hold 4 | -7 | 29.3 (49) | 0 | 3 (2 / 1) | 48-50: 29.3 |
| step 5 | scenario_s16_03 | off | 113 | - | 36: hold 31 | - | 59.5 (27) | 0 | 0 (0 / 0) | none |
| step 5 | scenario_s16_03 | on | 89 | -24 | 42: hold 1 | +6 | 55.5 (43) | 0 | 0 (0 / 0) | none |
| step 5 | scenario_s16_04 | on | 91 | -22 | 22: hold 32 | -14 | 68.5 (26) | 0 | 0 (0 / 0) | none |
| step 5 | scenario_s16_05 | off | 106 | - | 14: hold 5 | - | 60.4 (27) | 0 | 0 (0 / 0) | none |
| step 5 | scenario_s16_05 | on | 106 | +0 | 14: hold 5 | +0 | 60.4 (27) | 0 | 0 (0 / 0) | none |
| step 5 | scenario_s16_06 | on | 106 | +0 | 14: hold 5 | +0 | 60.4 (27) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_01 | off | 161 | - | -: none | - | 384.0 (59) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_01 | on | 161 | +0 | -: none | - | 384.0 (59) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_02 | off | 66 | - | 25: hold 5 | - | 52.2 (47) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_02 | on | 66 | +0 | 8: hold 5 | -17 | 52.2 (47) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_03 | off | 172 | - | -: none | - | 408.9 (155) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_03 | on | 172 | +0 | -: none | - | 408.9 (155) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_04 | off | 161 | - | -: none | - | 384.0 (59) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_04 | on | 161 | +0 | -: none | - | 384.0 (59) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_05 | off | 161 | - | -: none | - | 384.0 (59) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_05 | on | 161 | +0 | -: none | - | 384.0 (59) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_06 | off | 161 | - | -: none | - | 349.0 (47) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_06 | on | 161 | +0 | -: none | - | 349.0 (47) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_07 | off | 161 | - | -: none | - | 405.4 (120) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_07 | on | 161 | +0 | -: none | - | 405.4 (120) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_08 | off | 167 | - | -: none | - | 316.4 (0) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_08 | on | 167 | +0 | -: none | - | 316.4 (0) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_09 | off | 161 | - | -: none | - | 387.6 (66) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_09 | on | 161 | +0 | -: none | - | 387.6 (66) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_10 | off | 171 | - | -: none | - | 352.8 (1) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_10 | on | 171 | +0 | -: none | - | 352.8 (1) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_11 | off | 161 | - | -: none | - | 411.2 (127) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_11 | on | 161 | +0 | -: none | - | 411.2 (127) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s11_01 | off | 74 | - | 14: switch | - | 66.2 (56) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s11_01 | on | 74 | +0 | 14: switch | +0 | 66.2 (56) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s11_02 | off | 169 | - | 14: hold 2 | - | 50.4 (24) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s11_02 | on | 169 | +0 | 14: hold 2 | +0 | 50.4 (24) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s11_03 | off | 113 | - | 6: hold 3 | - | 51.3 (13) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s11_03 | on | 113 | +0 | 6: hold 3 | +0 | 51.3 (13) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s12_01 | off | 131 | - | 25: switch | - | 87.6 (79) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s12_01 | on | 130 | -1 | 8: switch | -17 | 72.1 (78) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s12_02 | off | 161 | - | 75: hold 18 | - | 32.3 (140) | 2 | 2 (1 / 1) | 138-141: 32.3 |
| step 5b | scenario_s12_02 | on | 162 | +1 | 93: hold 18 | +18 | 33.6 (139) | 3 | 1 (0 / 1) | 138-141: 33.6 |

### B3. Every case below min_separation, with its cause

| step | scenario | side | ticks | min | standing / viol / recede | decision in force: projection | human's true task | cause | the same span below min_separation on the other side (±5 ticks) |
|---|---|---|---|---|---|---|---|---|---|
| step 5 | scenario_s16_01 | off | 44-50 | 37.0 | 6 / 1 / 0 | 30: fallback moving k=31 | item_4 | other: no projection past the human's arrival at shelf_4 (the moving fallback runs to 44); the robot arrives beside the turn and holds there, standing | 49-51 |
| step 5 | scenario_s16_01 | on | 49-51 | 41.7 | 0 / 2 / 1 | 0: admitted item_4 | item_4 | turn (TODO-146): the admitted plan about one tick and 18 cm ahead of the executed human at the turn | 44-50 |
| step 5 | scenario_s16_02 | on | 48-50 | 29.3 | 0 / 2 / 1 | 38: admitted item_4 | item_4 | turn (TODO-146): the admitted plan about one tick and 18 cm ahead of the executed human at the turn | 44-50 |
| step 5b | scenario_s12_02 | off | 138-141 | 32.3 | 2 / 1 / 1 | 133: fallback standing k=31 | item_2 | other: the human, leaving the coffee machine, walks past the robot standing in its hold (decided at 137 on a moving fallback); the robot moves off at 140 | 138-141 |
| step 5b | scenario_s12_02 | on | 138-141 | 33.6 | 3 / 0 / 1 | 135: admitted item_2 | item_2 | other: the human, leaving the coffee machine, walks past the robot standing in its hold (decided at 135 on the admitted deliver_item(item_2), the true task; 134 before the gate change); the robot moves off at 141 | 138-141 |

### Planning tallies

- completion, on against off: better 5, equal 16, worse 1; ticks gained 50 over 5 runs ([-24, -22, -2, -1, -1]), ticks lost 1 over 1 runs ([1])
- cases below min_separation, off, other: 2 (s16_01 44, s12_02 138)
- cases below min_separation, on, other: 1 (s12_02 138)
- cases below min_separation, on, turn (TODO-146): 2 (s16_01 49, s16_02 48)
