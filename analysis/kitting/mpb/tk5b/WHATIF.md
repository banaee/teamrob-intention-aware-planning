# Two what-if readings on the recorded gate answers with context knowledge on (X and Y)

Hadi, 4 October 2026. A reading of existing outputs only: the runs with context knowledge on of step 4 (57) and of
step 5b's recognition set (17), each against the off run of the same script, and the two planning cases caused by a
wrong admission (step 5's scenario_s16_05, step 5b's scenario_s11_03). `whatif.py` writes every table below "The
tables".

**These are filters on recorded answers, not runs.** On each tick the recorded answer (the gate clears, leader h) is
kept or refused by the filter; nothing after it is recomputed. In a run a changed admission would change the later
ticks: the decision record, the trigger rule, the projection and, with a working robot, its path. The scenarios are
authored; the counts compare settings and are no rate of occurrence. Numbers only, no design conclusion.

The filters:
- **X**: h is admissible on a tick only if the evidence alone (the run with context knowledge off, the equal prior)
  ranks no other live hypothesis strictly above it (by more than 1e-9).
- **Y**: commitment warrant alone does not admit; h needs observation warrant on the tick.
- **X and Y** together.

## Summary

| measure | recorded (on) | X | Y | X and Y |
|---|---|---|---|---|
| the true task's admissions earlier than off (216): keep their tick | 216 | 216 | 157 | 157 |
| of them delayed (all are the 59 lone assigned tasks admitted on the previous task's completion tick; still earlier than off) | - | 0 | 59, by 1 tick | 59, by 1 tick |
| wrong admissions during modelled tasks, kind (ii), the true task first in the evidence (17 rows, 310 gate ticks): rows that disappear; ticks that remain | - | 7; 18 | 1; 302 | 14; 11 |
| kind (iii), the admitted one first in the evidence (26 rows, 149 ticks) | - | 0; 122 | 12; 72 | 12; 55 |
| no true hypothesis (4 rows, 45 ticks) | - | 0; 35 | 2; 33 | 2; 33 |
| the one-tick admissions on a completion tick (58) | 58 | 58 | 0 | 0 |
| the exit walk (51 rows, 1166 ticks): ticks that remain | 1166 | 1150 | 1163 | 1149 |
| scenario_s16_05 (pass at 22; item_4 admitted 0 to 21, decision at 0) | admitted | refused 0 to 21 (the A/C ×1.0015 above item_4 at 0) | admitted (observation warrant held) | refused 0 to 21 |
| scenario_s11_03 (pass at 11; item_12 admitted 0 to 10, decision at 0) | admitted | admitted (a tie, 0.5 / 0.5) | refused 0 to 10 (commitment alone) | refused 0 to 10 |
| changes of the answer within a true stretch: total; stretches with 3 or more | 673; 92 | 653; 87 | 579; 31 | 560; 21 |

Notes:
- The kinds are COMPARISON.md's rows (a row takes the kind of most of its wrong ticks; (i), a ratio within 1 percent,
  has no row). Of the 10 kind (ii) rows that remain under X, 6 remain on their first wrong tick only, the completion
  tick of the previous task, where the evidence restarts equal (scenario_s13_13 216, s14_19 180, s15_19 216, s08_02 62,
  s09_02 62, s09_11 62); s14_09 keeps its first tick 135; s13_06 and s15_06 keep 96 to 99, s14_10 135 to 137.
- Under Y the lone assigned task admitted on the previous task's completion tick has no observation warrant there; it is
  admitted on the next tick, when the human starts it. The early wrong admissions of a lone delivery keep their later
  ticks under Y, because the walk to the coffee machine or the A/C switch gains path toward the delivery's shelf
  (observation warrant).
- The planning rows read the recorded per-tick tables of the MPB (belief over the live hypotheses, observation
  warrant). They say what the filter would answer on the recorded ticks before the pass; with the admission refused the
  robot would have rested on the fallback projection, whose consequence a filter cannot show.
- The flicker measure counts the changes of the admitted hypothesis (or none) from tick to tick inside a true
  stretch, including the changes at its start and at its end.

## The tables

### The ratios behind docs/assumptions.md 6.4

Wrong ticks with a true hypothesis: 453 (in 43 admissions).

| the evidence alone on the tick (the off run) | ticks | the ratio true / admitted |
|---|---|---|
| a tie (equal within 1e-9) | 0 | ×1 |
| the true task first | 311 | min ×1.0008, quartiles ×1.1039 / ×1.4452 / ×2.5074, max ×14.2002 |
| the true task above the admitted one, a third hypothesis first | 1 | - |
| the admitted one above the true task | 141 | min ×0.0000, quartiles ×0.0003 / ×0.1521 / ×0.4946, max ×0.9275 |

Per admission whose ticks end with the true task first: the ratio on its first and its last wrong tick.

| step | scenario | admitted | wrong ticks | true task | ratio, first wrong tick | ratio, last wrong tick | ties |
|---|---|---|---|---|---|---|---|
| step 4 | s13_03 | item_4 | 150-161 (12) | coffee_break | ×1.8963 | ×5.5787 | 0 |
| step 4 | s13_05 | item_2 | 96-99 (4) | coffee_break | ×0.5894 | ×1.3849 | 0 |
| step 4 | s13_06 | item_2 | 96-103 (8) | coffee_break | ×0.4163 | ×2.9061 | 0 |
| step 4 | s13_11 | coffee_break | 81-91 (11) | item_2 | ×1.2248 | ×1.7103 | 0 |
| step 4 | s13_12 | coffee_break | 81-91 (11) | item_2 | ×1.2248 | ×1.7103 | 0 |
| step 4 | s13_12 | item_4 | 150-161 (12) | coffee_break | ×1.8963 | ×5.5787 | 0 |
| step 4 | s13_13 | item_4 | 216-258 (43) | coffee_break | ×1.0092 | ×12.7307 | 0 |
| step 4 | s13_14 | coffee_break | 81-91 (11) | item_2 | ×1.2248 | ×1.7103 | 0 |
| step 4 | s14_05 | item_2 | 135-146 (12) | coffee_break | ×0.3144 | ×3.5912 | 0 |
| step 4 | s14_09 | item_2 | 135-136 (2) | ac_activation | ×0.8283 | ×1.0580 | 0 |
| step 4 | s14_10 | item_2 | 135-140 (6) | ac_activation | ×0.6078 | ×1.8381 | 0 |
| step 4 | s14_19 | item_1 | 180-239 (60) | coffee_break | ×1.0008 | ×13.7117 | 0 |
| step 4 | s14_21 | coffee_break | 221-227 (7) | ac_activation | ×1.1772 | ×1.7775 | 0 |
| step 4 | s15_03 | item_4 | 151-161 (11) | coffee_break | ×2.0139 | ×5.5787 | 0 |
| step 4 | s15_05 | item_2 | 96-99 (4) | coffee_break | ×0.5894 | ×1.3849 | 0 |
| step 4 | s15_06 | item_2 | 96-103 (8) | coffee_break | ×0.4163 | ×2.9061 | 0 |
| step 4 | s15_19 | item_4 | 216-261 (46) | ac_activation | ×1.0015 | ×3.0458 | 0 |
| step 5b | s08_02 | item_2 | 62-83 (22) | coffee_break | ×1.0482 | ×13.5576 | 0 |
| step 5b | s08_03 | item_1 | 32-42 (11) | coffee_break | ×0.1521 | ×1.6265 | 0 |
| step 5b | s08_04 | item_1 | 32-39 (8) | coffee_break | ×0.2338 | ×2.2619 | 0 |
| step 5b | s09_02 | item_2 | 62-83 (22) | coffee_break | ×1.0482 | ×13.5576 | 0 |
| step 5b | s09_03 | item_1 | 32-42 (11) | coffee_break | ×0.1521 | ×1.6265 | 0 |
| step 5b | s09_04 | item_1 | 32-39 (8) | coffee_break | ×0.2338 | ×2.2619 | 0 |
| step 5b | s09_11 | item_3 | 62-79 (18) | coffee_break | ×1.0625 | ×14.2002 | 0 |

### What the lone assigned task admitted before the human starts it carries

- the true task's admission earlier than off, ticks gained in total: 3005; of them by a lone assigned task admitted on the previous task's completion tick: 1773
- wrong gate ticks during modelled tasks: 504; of them a lone assigned task admitted before the human starts it and retracted: 230

### X and Y: the true task's earlier admissions

| filter | category | earlier on than off | keep their tick | delayed: count | delay in ticks (median, range) | still earlier than off | never admitted in the stretch |
|---|---|---|---|---|---|---|---|
| X | assigned delivery | 144 | 144 | 0 | - | 144 | 0 |
| X | a lone assigned task admitted before the human starts it | 59 | 59 | 0 | - | 59 | 0 |
| X | foreseeable task, its raising fact holding | 11 | 11 | 0 | - | 11 | 0 |
| X | foreseeable task, no raising fact | 2 | 2 | 0 | - | 2 | 0 |
| Y | assigned delivery | 144 | 144 | 0 | - | 144 | 0 |
| Y | a lone assigned task admitted before the human starts it | 59 | 0 | 59 | median 1, range 1 to 1 | 59 | 0 |
| Y | foreseeable task, its raising fact holding | 11 | 11 | 0 | - | 11 | 0 |
| Y | foreseeable task, no raising fact | 2 | 2 | 0 | - | 2 | 0 |
| X and Y | assigned delivery | 144 | 144 | 0 | - | 144 | 0 |
| X and Y | a lone assigned task admitted before the human starts it | 59 | 0 | 59 | median 1, range 1 to 1 | 59 | 0 |
| X and Y | foreseeable task, its raising fact holding | 11 | 11 | 0 | - | 11 | 0 |
| X and Y | foreseeable task, no raising fact | 2 | 2 | 0 | - | 2 | 0 |

### X and Y: the admissions of a hypothesis that is not the true task

| filter | kind (COMPARISON.md) | admissions | gate ticks | disappear | remain | ticks remaining |
|---|---|---|---|---|---|---|
| X | (ii) | 17 | 310 | 7 | 10 | 18 |
| X | (iii) | 26 | 149 | 0 | 26 | 122 |
| X | no true hypothesis | 4 | 45 | 0 | 4 | 35 |
| X | the exit walk | 51 | 1166 | 0 | 51 | 1150 |
| X | pin tick | 58 | 58 | 0 | 58 | 58 |
| Y | (ii) | 17 | 310 | 1 | 16 | 302 |
| Y | (iii) | 26 | 149 | 12 | 14 | 72 |
| Y | no true hypothesis | 4 | 45 | 2 | 2 | 33 |
| Y | the exit walk | 51 | 1166 | 0 | 51 | 1163 |
| Y | pin tick | 58 | 58 | 58 | 0 | 0 |
| X and Y | (ii) | 17 | 310 | 14 | 3 | 11 |
| X and Y | (iii) | 26 | 149 | 12 | 14 | 55 |
| X and Y | no true hypothesis | 4 | 45 | 2 | 2 | 33 |
| X and Y | the exit walk | 51 | 1166 | 1 | 50 | 1149 |
| X and Y | pin tick | 58 | 58 | 58 | 0 | 0 |

Every admission of a hypothesis that is not the true task during modelled tasks, the ticks remaining under each filter:

| step | scenario | admitted | wrong ticks (gate) | kind | X | Y | X and Y |
|---|---|---|---|---|---|---|---|
| step 4 | s13_03 | item_4 | 150-161 (12) | (ii) | none | 150-161 | none |
| step 4 | s13_05 | item_2 | 94-94 (1) | (iii) | 94 | 94 | 94 |
| step 4 | s13_05 | item_2 | 96-99 (4) | (iii) | 96-97 | none | none |
| step 4 | s13_06 | item_2 | 96-103 (8) | (ii) | 96-99 | 96-103 | 96-99 |
| step 4 | s13_07 | item_2 | 123-130 (8) | (iii) | 123-130 | none | none |
| step 4 | s13_11 | coffee_break | 81-91 (11) | (ii) | none | 81-91 | none |
| step 4 | s13_12 | coffee_break | 81-91 (11) | (ii) | none | 81-91 | none |
| step 4 | s13_12 | item_4 | 150-161 (12) | (ii) | none | 150-161 | none |
| step 4 | s13_13 | item_4 | 216-258 (43) | (ii) | 216 | 217-258 | none |
| step 4 | s13_14 | coffee_break | 81-91 (11) | (ii) | none | 81-91 | none |
| step 4 | s13_15 | item_4 | 262-269 (8) | (iii) | 262-269 | none | none |
| step 4 | s14_04 | item_2 | 133-133 (1) | (iii) | 133 | 133 | 133 |
| step 4 | s14_04 | item_2 | 135-136 (2) | (iii) | 135-136 | none | none |
| step 4 | s14_05 | item_2 | 135-146 (12) | (iii) | 135-138 | 135-146 | 135-138 |
| step 4 | s14_06 | item_2 | 180-187 (8) | (iii) | 180-187 | none | none |
| step 4 | s14_09 | item_2 | 133-133 (1) | (iii) | 133 | 133 | 133 |
| step 4 | s14_09 | item_2 | 135-136 (2) | (ii) | 135 | none | none |
| step 4 | s14_10 | item_2 | 135-140 (6) | (ii) | 135-137 | 135-140 | 135-137 |
| step 4 | s14_11 | item_2 | 180-187 (8) | (iii) | 180-187 | none | none |
| step 4 | s14_19 | item_1 | 180-239 (60) | (ii) | 180 | 181-239 | none |
| step 4 | s14_21 | coffee_break | 221-227 (7) | (ii) | none | 221-227 | none |
| step 4 | s15_03 | item_4 | 151-161 (11) | (ii) | none | 151-161 | none |
| step 4 | s15_05 | item_2 | 94-94 (1) | (iii) | 94 | 94 | 94 |
| step 4 | s15_05 | item_2 | 96-99 (4) | (iii) | 96-97 | none | none |
| step 4 | s15_06 | item_2 | 96-103 (8) | (ii) | 96-99 | 96-103 | 96-99 |
| step 4 | s15_07 | item_2 | 123-130 (8) | (iii) | 123-130 | none | none |
| step 4 | s15_11 | item_2 | 94-94 (1) | (iii) | 94 | 94 | 94 |
| step 4 | s15_11 | item_2 | 96-98 (3) | (iii) | 96-98 | none | none |
| step 4 | s15_11 | item_4 | 111-118 (8) | (iii) | 112-118 | 111-118 | 112-118 |
| step 4 | s15_12 | item_2 | 96-108 (13) | (iii) | 96-104 | 96-108 | 96-104 |
| step 4 | s15_13 | item_2 | 123-130 (8) | (iii) | 123-130 | none | none |
| step 4 | s15_19 | item_4 | 216-261 (46) | (ii) | 216 | 217-261 | none |
| step 5b | s08_02 | item_2 | 62-83 (22) | (ii) | 62 | 63-83 | none |
| step 5b | s08_03 | item_1 | 32-42 (11) | (iii) | 32-40 | 32-42 | 32-40 |
| step 5b | s08_04 | item_1 | 30-30 (1) | (iii) | 30 | 30 | 30 |
| step 5b | s08_04 | item_1 | 32-39 (8) | (iii) | 32-36 | none | none |
| step 5b | s09_02 | item_2 | 62-83 (22) | (ii) | 62 | 63-83 | none |
| step 5b | s09_03 | item_1 | 32-42 (11) | (iii) | 32-40 | 32-42 | 32-40 |
| step 5b | s09_04 | item_1 | 30-30 (1) | (iii) | 30 | 30 | 30 |
| step 5b | s09_04 | item_1 | 32-39 (8) | (iii) | 32-36 | none | none |
| step 5b | s09_05 | item_1 | 32-47 (16) | no true hypothesis | 32-47 | 32-47 | 32-47 |
| step 5b | s09_06 | item_1 | 30-46 (17) | no true hypothesis | 30-46 | 30-46 | 30-46 |
| step 5b | s09_07 | item_1 | 32-32 (1) | (iii) | 32 | 32 | 32 |
| step 5b | s09_09 | item_2 | 62-72 (11) | no true hypothesis | 62 | none | none |
| step 5b | s09_09 | item_2 | 108-108 (1) | no true hypothesis | 108 | none | none |
| step 5b | s09_11 | item_3 | 62-79 (18) | (ii) | 62 | 63-79 | none |
| step 5b | s09_13 | item_1 | 46-54 (9) | (iii) | 46-54 | 46-54 | 46-54 |

### X and Y: the two planning cases caused by a wrong admission

| step | scenario | the pass from | ticks before it on which the recorded gate clears (leader) | X refuses | Y refuses | X and Y refuse | the decision ticks before the pass: recorded, X, Y |
|---|---|---|---|---|---|---|---|
| step 5 | scenario_s16_05 | 22 | 0-21 (item_4) | 0-21 | none | 0-21 | 0: clears, X refuses, Y lets |
|  |  |  | off evidence at 0: ac_activation 0.3354, item_4 0.3349, coffee_break 0.3298; at 21: ac_activation 0.4200, item_4 0.3961, coffee_break 0.1839 |  |  |  |  |
| step 5b | scenario_s11_03 | 11 | 0-10 (item_12) | none | 0-10 | 0-10 | 0: clears, X lets, Y refuses |
|  |  |  | off evidence at 0: coffee_break 0.5000, item_12 0.5000; at 10: coffee_break 0.5000, item_12 0.5000 |  |  |  |  |

### X and Y: flicker

| answer | true stretches | changes in total | stretches with 3 or more changes | most changes in one stretch |
|---|---|---|---|---|
| recorded (on) | 325 | 673 | 92 | 5 |
| X | 325 | 653 | 87 | 5 |
| Y | 325 | 579 | 31 | 5 |
| X and Y | 325 | 560 | 21 | 4 |
