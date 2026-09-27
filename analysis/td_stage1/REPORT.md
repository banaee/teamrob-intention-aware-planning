# T-D R and E, Stage 1: the verification analysis (cycle 1, session 1.4)

27 September 2026, at 7f4559a. A measurement: no code, baseline, record or doc changed. Findings for cycle 1.5 are
stated as findings, with ticks; no parameter value is proposed.

## Material and conventions

- POST: the four maintained sets at 7f4559a (`analysis/{tb1a_destination,tb1b_two_tables,tb1c_realized_flip,tb3_full_reorder}/sweep/`,
  48 logs; md5s checked against their READMEs, all match).
- PRE: the logs are git-ignored, so "the commit before 367a3a7" was re-run: a detached worktree at 84309e9, the four
  `sweep.sh` unchanged, into `pre/<set>/` (git-ignored). All 96 files (48 `.log`, 48 `.rec`) match the md5s of the
  T-L stage 3 sections of the READMEs at 84309e9. The 48 `.rec` streams are byte-identical pre and post: the
  ground truth is the same on both sides.
- SUPPLEMENTARY (section H names them; not among the 48): scenario_s06_06 on env_layout_08 and scenario_s07_03 on
  env_layout_09, prior off and on, the tb1a sweep's options, at HEAD (`supp/head/`) and at 84309e9 (`pre/supp/`);
  `supp_sweep.sh`. md5 (.log) HEAD: s06_06 off 06504fdc…, on e680b94b…; s07_03 off 4ecc3614…, on f39e633e…; PRE:
  3a56c579…, 40434e1a…, 91a3385d…, 188b5912…; `.rec` identical pre/post (bf173f1b…, e10041d7…).
- GROUND TRUTH: the record (`[rec]`: the stack's top task, the action) and the loader's `[coverage]` value per
  script entry. Oracle IR (TODO-101) is not built; every comparison is against these labels directly.
- ALIGNMENT: the record's ACTION is aligned with the body (lag 0: `place#0` on the tick of `micro=release`); its TASK
  transitions land 2 ticks after the world fact the recognizer reads (48 of 48 non-initial switches, `[IR-boundary]`
  at w, `entered:` at w + 2). "Raw" truth = the record at t, "lag-corrected" = the record at t + 2. Where a number
  depends on it, both are given (C); elsewhere lag-corrected, as in handback §3.
- α: every finding is recomputed from the logged 4-decimal tails at α ∈ {0.01, 0.05, 0.1}; at 0.05 the recomputed
  finding equals the logged one on every tick (A7). No level is selected.
- 36 of the 48 logs are distinct by md5; by recognizer output and record, 32 groups (16 per prior). Tables list one
  run per group, `[xN]` for its size; aggregates count every run.
- Prior ON is the primary set; prior OFF is an appendix to each section.

Scripts (run from this directory with `~/python-envs/ir-nomesa-env/bin/python`; G from the repo root with
`PYTHONHASHSEED=0`): `tdlib.py` (parser, truth, the finding at α), and one script per section, each writing the
`.txt` beside it.

---

## A. The R6 invariant — no violation (`a_invariant.py` → `a_invariant.txt`)

12,843 ticks (the 48 runs plus the four supplementary): 0 violations. Checked per tick: the `[IR-dist]` key set is
the space and never holds `unknown`; every pinned key (inadmissible under the prior, or `[IR-complete]` by t) reads
exactly 0.001; the live keys sum to 1 − |pinned|·0.001 within the 3-decimal rounding (max |residual| 0.003 over ten
keys); no retired key is ever most_likely, a member, or off the floor again, and none completes twice; lifecycle is
exhausted iff the live set is empty (then most_likely none, confidence 0, no finding); most_likely is a live argmax
with confidence equal to its P; every member is live with S ∈ [0, 1]. Limit: the dist lines carry 3 decimals, so
the sum is verified to rounding, not to machine precision (the unit tests check it exactly).

## B. Per ground-truth case (`b_cases.py` → `b_cases.txt`)

| case | in the 48? | where |
|---|---|---|
| B1 switch to a modelled task | yes: every script entry (80 switches; 48 after a boundary) | all |
| B2 switch outside the support | no (0 entries) | — |
| B3 TASK_ABSENT | no (0 entries; also none in the supplementary) | — |
| B4 BINDING_ABSENT | no | supplementary: s06_06, s07_03 (wrong table) |
| B5 no task on the stack | yes: every run after the script ends | all |
| B6 an episode's first ticks | yes: step 0 (32 groups) and 80 boundaries | all |

- B1: at every non-initial switch, the world tick w = record tick − 2 is an `[IR-boundary]`; the finding at w is U,
  from w + 1 A. The leader at w is the uniform prior's first sorted key, which need not be the new task (s02_01 on
  75: `ac_switch_0` 0.331 while the truth is coffee_break). Prior on, with one live task left, the new task leads on w at 1 − |pinned|·0.001 (0.991 to 0.996: s01_01 78,
  s03_01 54, s01_06 74, s02_01 309, s05 94).
- B4 (wrong table, lag-corrected span): shared prefix 0–18 (s06_06) / 0–10 (s07_03), finding A at all α (true: the
  item hypothesis explains the walk and the pick-up). Carry walk to the wrong table 19–102 / 11–93: A, then X from
  37 / 40 / 47 (s06_06, α = .10 / .05 / .01) and 31 / 33 / 39 (s07_03), to the release; the leader is the item's
  hypothesis at 0.993–0.995 throughout (prior on and off alike: every rival is refuted by then).
- B5 (no task on the stack): prior ON, 14 of 16 groups EXHAUSTED on every idle tick (no finding). The exception is
  s04_01: a foreseeable task never performed (`ac_switch_0`) stays live, leads at 0.992, and the finding reads A
  for 16 ticks, then X from 344 / 341 / 352 (α .05 / .10 / .01). Prior OFF: the robot's remaining items stay live;
  the idle stand reads A on the first 16 ticks at α = .05 (13 at .10, 24 at .01) and X after (e.g. s03_01 off: X from
  138 at .05 to the run's end, 162 of 179 ticks).
- B6: step 0 reads A (32 of 32). Of the 80 boundaries, 15 end in EXHAUSTED; each of the other 65 reads U on its
  tick and A from the next (one of them cut short by the run's end). The A at b + 1 is carried by the place-acknowledgement tick: standing in
  the new `move_to` phase, D = 1, S = 0.8629 (see G), not by any walk.
- DISAGREEMENTS on modelled ticks (X while the truth is a COVERED task): 3 ticks, prior on, at every α. See C.

## C. Finding statistics (`c_findings.py` → `c_findings.txt`)

FALSE UNEXPLAINED (the truth a COVERED task; ticks / phase instances):

| | α = 0.01 | α = 0.05 | α = 0.1 |
|---|---|---|---|
| prior ON, lag-corrected (4352 ticks, 204 instances) | 3 / 3 | 3 / 3 | 3 / 3 |
| prior ON, raw (4400 ticks, 204 instances) | 3 / 3 | 3 / 3 | 3 / 3 |
| prior OFF, either | 0 / 0 | 0 / 0 | 0 / 0 |

The three: s02_01 on t = 247, s04_01 on t = 268, s03_06 on t = 88: each a grasp tick (phase `pick_up#0` raw,
`move_to#1` lag-corrected). The true hypothesis advances on that tick into its carry walk with nothing walked, so it
is not a member (E6 (2)); the only member is a refuted foreseeable rival (`ac_switch_0` S = 0.0000 / 0.0021,
`coffee_break` 0.0016). The next tick the true hypothesis is a member again (S = 0.8629) and the finding is A. By
phase, prior on, summed over its 24 runs: `move_to#0` 0/58 instances, `pick_up#0` 0/44, `move_to#1` 3/44, `place#0`
0/44, `wait_at#0` 0/14.

MISSED UNEXPLAINED: TASK_ABSENT and outside-support ticks: none exist in the test set, so neither missed findings nor
detection delay can be measured for them. BINDING_ABSENT (supplementary), in their place. SHARED PREFIX: the wrong-
table task's actions that the item's modelled hypothesis also expects with the same targets: its walk to the item
and the pick-up; it ends on the record's first `move_to#1` tick (s06_06 19, s07_03 11). Cross-check from the
evidence: the item hypothesis's S first falls below its one-tick value 0.8629 on the same ticks.

| | span after prefix | missed α=.01 / .05 / .10 | first X | delay from switch (0) | from prefix end |
|---|---|---|---|---|---|
| s06_06 (on = off) | 19–102 (84) | 28 / 21 / 18 | 47 / 40 / 37 | 47 / 40 / 37 | 28 / 21 / 18 |
| s07_03 (on = off) | 11–93 (83) | 28 / 22 / 20 | 39 / 33 / 31 | 39 / 33 / 31 | 28 / 22 / 20 |

## D. Decisions against the pre-build baseline (`d_decisions.py` → `d_decisions.txt`, `d_extras.txt`)

Every differing decision is listed in `d_decisions.txt` (tick, both sides' trigger / `[meta-proj]` reason / winner /
selection / hold, the post recognizer state and the pre one with `unknown`'s share). The pattern, prior ON:

- ADMISSIONS MOVE EARLIER where the leader's share over H crosses θ sooner (first reveal: s01_01 20 → 9, s03_01
  11 → 5, s01_06 23 → 18, s04_01 30 → 19); a `recognition_changed` at a boundary with one live task now admits
  (`none(below_theta)` at 0.498 → `built` at 0.996: s01_01 78, s03_01 54, s01_06 74, s02_01 309, s05 94). The
  `none(unknown)` reason is gone: exhausted reads `none(below_theta)` at confidence 0 (s01_01 141, s02_01 362, …).
- ADMISSIONS LOST: coffee_break (s02_01 122, s04_01 152, s05_01 / _02 23) and ac_switch_1 (s04_01 203): see E.
- HOLDS: new, s02_01 hold 4 at 23 (item_2 at 0.756), s03_01 hold 7 at 5 (was at 11) and hold 1 at 54 (lone task,
  finding U), s01_06 hold 6 at 18 (was at 23); lost, s05_02 hold 31 at 23 (coffee_break at 0.930 before the build).

Completion, world tick (T6), prior ON: 17 of 24 runs unchanged; later s02_01 422 → 426, s03_01 (single_task, x2)
236 → 237; earlier s05_01 (x3) 185 → 171, s05_02 203 → 172 (no coffee stay projected, no hold). Minimum separation
(`[sep] min`) moved in s05_01 66.40 → 30.00 cm, s05_02 14.14 → 30.00, s01_06 8.47 → 25.28; elsewhere unchanged.

APPENDIX, prior OFF. The lone-hypothesis admission of the robot's own remaining item after the human's last task,
with the human idle: s01_01 hold 33 at 141 (`item_4` 0.996, finding U), completion 169 → 202; s03_01 hold 89 at
145 (`item_7` 0.996, finding X since 138), the robot stands 145–233 and the 300-step run ends before it delivers
(pre 236); s03_01 full_reorder hold 89 at 131, not completed (pre 221); s06_03 realized / full_reorder hold 13 at
220 (`item_1`), 226 → 239; s06_03 single_task hold 52 at 220 (`item_4`), 265 → 317. Others: s05 as prior on, the rest
unchanged. Minimum separation s03_01 3.85 → 30.12 / 17.89 (full_reorder), s05 as prior on. NOTE: under prior off the
empty-pool line now comes on a `recognition_changed` fired by the robot's own pin, so the declared tick equals the
world tick (e.g. s01_06 162 → 160 with the world tick 160 on both sides): compare world ticks only.

## E. Completion and reveal evidence (`e_reveals.py` → `e_reveals.txt`)

Reveals lost or later (reveal = the task most_likely at ≥ θ inside its lag-corrected span); every other reveal is
equal or earlier:

| prior | task | reveal pre → post | the task's body events before the post reveal |
|---|---|---|---|
| on/off | coffee_break s02_01, s04_01, s05_01, s05_02 | 122, 152, 23, 23 → none | arrival 122, 152, 23, 23 (= the pre reveal tick) |
| on/off | ac_switch_1 s04_01 | 203 → none | arrival 203 |
| on | item_5 s05_01 / _02 | 59 → 60 | none before (60 is the arrival) |
| off | item_2 s01_01 | 108 → 114 | arrival 108, grasp 110 |
| off | item_2 s02_01 | 29 → 35 | arrival 29, grasp 31 |
| off | item_3 s03_01 / s03_06 | 20 → 30 | arrival 20, grasp 22 |
| off | item_2 s03_01 / s03_06 | 86 → 94 | arrival 86, grasp 88 |
| off | item_5 s05_01 / _02 | 60 → 71 | arrival 60, grasp 62 |
| off | item_0 s06_01 (x5 runs) | 11 → 13 | none (a walk reveal, 2 ticks later) |

Every lost or later reveal but the last was, before the build, the arrival tick: the arrival fold, worth 1/u against
`unknown`. Now the arrival folds L = 1 against rivals that are not refuted, and adds nothing.

THE COFFEE WALK, prior ON (tick by tick in `e_reveals.txt`):
- s05_01 / s05_02 (identical recognizer streams): walk 0–23, arrival 23, acknowledgement 24, stand 25–53. Before:
  the walk took coffee_break 0.274 → 0.542 (ac_switch_0 refuted, `unknown` 0.25 → 0.07; item_5, on the same bearing,
  tied at 0.39); the ARRIVAL carried it over θ (23: 0.542 → 0.930, item_5 0.386 → 0.057); the stand added nothing.
  Now: the walk ends in a tie, coffee_break = item_5 = 0.498 from 16 on; the arrival adds nothing; the stand adds
  nothing to the belief (0.498 to 53). The stand now works in the adequacy test only: item_5, a `move_to` member,
  is charged its standing (S 0.8629 at 24 → < 0.05 from 40, < 0.01 from 48), and coffee_break, a member in its
  `wait_at` within s_exp = 30 at S = 1, keeps the finding A. The robot receives neither.
- s02_01: walk 77–122 against ac_switch_0 (item_5 refuted). Before: 0.518 at 121, the arrival 0.914 at 122. Now:
  0.512 → 0.516 at the arrival, flat through the stand (ac_switch_0 0.476); ac_switch_0's S < 0.05 from 137, the
  finding A throughout (coffee_break a member at S = 1).
- s01_01 item_2, prior OFF: before, 0.707 → 0.964 at the arrival (108). Now 0.638 → 0.657 at 108, flat through the
  grasp (110) because item_4 (the robot's own item, same bearing) is not refuted; it crosses θ at 114 on the carry
  walk, when item_4's phase after the grasp (its method now returns item_2 first) is refuted (0.704 at 113, 0.755
  at 114). Prior ON, item_2 is the lone live
  task from the boundary: 0.996 from 78.

## F. The adequate-below-θ pattern (`f_adequate_below_theta.py` → `f_adequate_below_theta.txt`)

Ticks with the finding A, the true hypothesis a member at S = 1, and its belief < θ; the same at every α (the
member at S = 1 keeps A at any level). By phase, over the 48 runs:

| | wait_at | pick_up | place | move_to |
|---|---|---|---|---|
| prior ON | 174 (29 per coffee stand: s02_01 124–152, s04_01 154–182, s05_01 / _02 25–53) | 0 | 0 | 244 |
| prior OFF | 174 (the same stands) | 0 | 0 | 607 |

`pick_up` and `place` never show it: the true task is at θ before its location in every run. The `move_to` ticks
are the first walk from step 0 before the reveal (e.g. s01_01 on 0–8) and the arrival plus acknowledgement ticks
of an unrevealed task (s02_01 122–123, s01_01 off 108–109). A walk after a boundary is not in the pattern: there the
true hypothesis carries S = 0.8629, not 1 (G).

## G. The Projector's priced standing (`g_priced_standing.py` → `g_priced_standing.txt`)

Read from the Projector's own output: scenario_s01_01 prior on, the human projections admitted at 9 (item_3) and 78
(item_2). Each action is followed by a 1.00-tick latency segment:

| action | own segment | latency | projected standing at the location | recognizer s_exp |
|---|---|---|---|---|
| move_to | walk (29.50 / 32.97 ticks) | 1.00 | 1.00 (at the arrival point) | 0 |
| pick_up | 1.00 | 1.00 | 2.00 | 1 |
| place | 1.00 | 1.00 | 2.00 | 1 |

The Projector prices 3 stationary ticks at a shelf or table (the walk's latency, the action, its latency). The body
stands exactly 3 (s01_01: 40–42 `move_to/None, pick_up/grasp, pick_up/None`; 77–79 for the place; 109–111). The
entry's s_exp = 1 is the action's own segment only. How the recognizer splits the 3 ticks: the stationary phase
begins on the arrival tick (s = 0) and absorbs the walk's latency tick (s = 1 ≤ s_exp, S = 1). It advances on the
grasp or release (the world fact), and the action's latency tick is charged as standing in the NEXT phase, a
`move_to` with s_exp = 0: D = 1 tick, v·D = 20 cm, S = 0.8629, for the whole of that walk (D does not decrease within
a phase). Over the 48 runs, the true hypothesis's D on the human's walking ticks where it is a member: exactly 0 on
22.5%, exactly 1 on 77.5% (3015 of 3891 ticks, prior on and off alike), never anything else. After a boundary the
same tick is the place's acknowledgement, and it is what makes the new episode's hypotheses members at b + 1 (B6).

## H. The five named cases (`h_cases.py` → `h_cases.txt`, tick by tick)

1. A WALK TO A TARGET NO HYPOTHESIS EXPECTS: none of the 48 runs has one (every entry COVERED, no `go_to`, no exit
   walk). The nearest measured case is the wrong-table carry walk (3).
2. THE LONGEST STAND. Modelled: the coffee_break `wait_at`, 30 ticks + acknowledgement (s05_01 on 25–54): coffee_break
   at S = 1 throughout, A, belief 0.498; at 54 (waited holds) pin, boundary, U; 55 A. With no task on the stack:
   s03_01 prior off, the stack empty 123–299 (178 ticks). 121 U; 122–137 A as item_6 and item_7 (`move_to`) are
   charged the standing; X from 135 / 138 / 146 (α .10 / .05 / .01). At 145 item_6 is pinned by the robot's delivery,
   item_7 becomes the lone live task at 0.996, and the meta-planner admits it with a hold of 89 (145–233) while the
   finding is X. Prior on (s04_01), the idle human with `ac_switch_0` alone live at 0.992 from 327, admitted at 327:
   A to 343, X from 344 (α .05).
3. THE WRONG TABLE (supplementary). s06_06 on: prefix 0–18 A; the grasp at 17 (item_0 not a member, item_3 at
   S = 1 in its stationary phase: A); carry 19–102 X from 40 (α .05), leader item_0 at 0.995. At 76 the meta-planner
   ADMITS deliver_item(item_0) (to its designated table) at 0.995 while the finding is X; before the build the same
   tick read `unknown` 0.994 and was refused `none(unknown)`. At the release on the wrong table (103) no hypothesis
   completes, so no boundary. item_0's hypothesis is a member at S = 1 with the human standing at the item, i.e. in
   a stationary phase (the item is to be picked up where it now lies); finding A, still the leader at 0.995 while the human walks to item_3. s07_03 on: the same at
   79 (admitted at 0.995, X), release 94, A. Completion world ticks unchanged (265; 243).
4. THE FINISHED WORK ORDER, s01_01 prior on: 139–140 item_2 at 0.996, A; 141 the release: pin, boundary, EXHAUSTED,
   most_likely none, confidence 0; the meta-planner `none(below_theta)` at 0.000 (before: `none(unknown)` at 0.995);
   the record's stack empty from 143; exhausted to the robot's completion (169, unchanged).
5. THE FIRST TICKS AFTER A BOUNDARY: s01_01 on 78 (one live): U, item_2 0.996; 79 A (item_2 S = 0.8629, the place
   acknowledgement). s01_01 off 78 (three live): U at the uniform 0.333; 79 A with all three members at 0.8629. s02_01
   on 75: U, leader ac_switch_0 at 0.331 (the first sorted key; the truth is coffee_break); 76 A. The first tick
   stays unresolved, as E6 (2) states, for exactly one tick at each of the 65 boundaries that leave a live task.

---

## Findings for cycle 1.5 (numbers that look wrong, with the ticks that show them)

1. GRASP-TICK FALSE UNEXPLAINED: s02_01 on 247, s04_01 on 268, s03_06 on 88, at every α. On the tick a phase advance
   lands in a `move_to` with nothing walked, the true hypothesis leaves the test, and a refuted rival alone decides.
   It is the E6-amendment pattern (s01_01 76–77) at the other kind of advance.
2. THE LATENCY TICK: s_exp for `pick_up` / `place` (1) is the action's own segment; the Projector prices 2 plus the
   walk's 1, matching the body's 3. The action's latency tick is charged to the following walk, so the true
   hypothesis carries D = 1 on 77.5% of its walking ticks (S = 0.8629), and every boundary's b + 1 resolution rests on
   that tick.
3. THE ADMITTED LONE HYPOTHESIS AGAINST AN UNEXPLAINED FINDING: s03_01 off 145 (hold 89, the run does not complete),
   s06_06 on 76 and s07_03 on 79 (the wrong table, admitted at 0.995). The belief and the finding disagree, and the
   meta-planner reads the belief only (R5: G's question, measured here).
4. THE FORESEEN STAY IS NO LONGER FORESEEN: coffee_break is never at θ in s02_01, s04_01 or s05_01 / _02 (both
   priors), and s05_02's 31-tick hold at 23 is gone (completion 203 → 172, minimum separation 14.14 → 30.00 cm). The
   evidence that separates coffee_break from a rival on its bearing, the stand, reaches the adequacy test and not
   the belief.
5. A MISDELIVERY IS NOT A BOUNDARY: after the wrong-table release (s06_06 103, s07_03 94) the item's hypothesis
   stays live and leads at 0.995 into the human's next task (L's question).

Flags (outside the task): the robot's per-tick line keeps `action=place micro=release` with `task=None` after its
pool empties, so a "last release" metric must filter on the task (`tdlib.robot_completion` does). s07_03 prior on
declares no empty pool within 300 steps, before and after alike.
