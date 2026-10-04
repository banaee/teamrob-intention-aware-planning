# L-build: T-D L, the belief lifecycle — the 1.5c and IRB.2b measures rerun

> Superseding note (4 October 2026, T-K part 1, step 1; design_records.md, "T-K", STEP 1): the case on scenario_s04_01 (scenario_40) is no longer reproducible. env_layout_05 now holds one A/C switch, ac_switch_1 (ac_switch_0 and ac_switch_2 removed), and scenario_s04_01's script one ac_activation (the walk to ac_switch_2 removed); this record describes three switches and two activations. The scenario's logs under `pre/tb1a_destination/` were deleted; they were local and git-ignored, in no commit (a copy as of 2 October 2026 at /home/hadi/teamrob_analysis_2026-10-02/kitting/l_build/); the layout and script they ran on are last held by 4345ef9.

28 September 2026, at the L-build commits: c4beb1d (records), 2c54c4a (recognizer: L1, L4, the flag), 493c095
(meta-planner: L2 (ii), L5 B), 013cd35 (tests), 5129d90 and 3d65ca6 (two tie-break defects in the re-entry, found by the
IRB and fixed, each with a test), 2a4ab60 (the four maintained baseline sets), 695f5a8 (the IRB). The
mechanism is design_decisions.md, "T-D L: the belief lifecycle", as amended on the L-records report (confirmed at the
L-build plan step: L1 read through the terminal action's preconditions on the previous tick; L2 (ii) as the state "the
recorded hypothesis is inadequate"; the boundary governs a re-entry on its tick; the `[IR-boundary]` line names the
action; `[meta-trig]` names the cause of every `recognition_changed`; re-entry arithmetic C). Every number that moved is
reported with its ticks and its cause (L1, L2, L4, L5 B). No previous statistic is preserved for comparability.

## Material and conventions

- PRE: the IRB.2b baselines, md5-checked against the READMEs' "IRB.2b" sections (48 logs and 48 `.rec` of 48) and
  copied to `pre/<set>/` before any code changed; `pre/supp/`: the four supplementary wrong-table runs
  (`analysis/td_stage1b/supp_sweep.sh`) at ec155f3, before the build, byte-identical to IRB.2b's `post/supp/`.
- POST: the four maintained sets regenerated at L-build (`analysis/<set>/sweep/`, md5s in the READMEs' "L-build"
  sections) and `post/supp/`. All logs git-ignored. The 52 `.rec` streams are byte-identical PRE and POST: the human's
  script, and with the separation stop off nothing the robot does reaches it.
- SCRIPTS: `analysis/irb2b_exposed_interval/`'s scripts copied here. `tdlib.py` extended for the L lines (a key pinned
  more than once and re-entering, `retired(log, key, t)` the interval; `[IR-reentry]`; the action an `[IR-boundary]`
  names; `[meta-trig]`'s `cause=`); A reads retirement as an interval and A4 as L4 (a retired key is not most likely,
  not a member and at the floor WHILE retired; a key's pins and re-entries alternate); X drops IRB.2b's EXPOSED /
  TRUNCATED classes (L's changes are not confined to an interval) and adds `reent`; D shows the POST trigger's cause
  (not compared: PRE has none) and covers the supplementary runs; `x_summary.py` (IRB.2b's exposed-interval table) is
  not carried. NEW: `baseline_diff.py` (per log and grep family, the first differing step, with the two format changes
  undone), `l_events.py` (per run: boundaries with and without a pin, re-entries, pins, retractions, boundary fires,
  the causes), `irb_compare.py` (the IRB against IRB).
- A, B, C, F, H were run on both sides (`<script>.txt`, `TD_SIDE=pre` for `<script>_pre.txt`); D, E, X and
  `baseline_diff` compare PRE with POST themselves. G (the priced standing) and the clip (`clip_sweep.sh`, 17 prior-off
  conditions) drive the simulator: run at HEAD, both byte-identical to IRB.2b's outputs.
- Truth lag-corrected (the record at t + 2), α ∈ {0.01, 0.05, 0.1}, prior ON primary, prior OFF an appendix, the four
  supplementary runs (the wrong table: TODO-87's case, where L1 acts) beside them. Run from this directory with
  `~/python-envs/ir-nomesa-env/bin/python <script>.py > <script>.txt`; G and `clip_sweep.sh` from the repo root with
  `PYTHONHASHSEED=0`.

## The regeneration (`baseline_diff.txt`)

Two format changes reach every log: `[meta-trig] … trigger=recognition_changed cause=<entered | replaced | boundary |
retraction>` and `[IR-boundary] … completed <action>:` (for `completed a task:`). With both undone:

| set | logs | identical | recognizer and triggers moved, robot not | robot moved (`[meta]`, `[hold]`, `[sep]`, its lines) |
|---|---|---|---|---|
| tb1a_destination | 16 | 6 | 0 | 10 |
| tb1b_two_tables | 4 | 2 | 0 | 2 |
| tb1c_realized_flip | 8 | 6 | 0 | 2 |
| tb3_full_reorder | 20 | 10 | 0 | 10 |
| supplementary | 4 | 0 | 0 | 4 |

Identical (24 of 48): every prior-on run of scenario_s01_01, s03_01, s01_06, s03_06, s06_01, s06_02, s06_03, and the
prior-off runs of s03_01 single_task (tb1a, tb3), s01_06, s06_03 (tb1c plain and realized, tb3 full_reorder): no
foreseeable task is performed, no terminal action lacks its fact, and no recorded hypothesis turns inadequate. Moved:
every run with a coffee break or an AC walk (s02_01, s04_01, s05_01, s05_02: L4), the prior-off runs where an admitted
projection outlived its leader's adequacy (L2 (ii)), and the wrong-table runs (L1, L2 (ii)). The `[IR-boundary]` ticks
are unchanged in all 48 maintained runs (only the live count they print grew, by the re-entries).

## A: the R6 invariant — 0 violations on 16,860 ticks, both sides

`a_invariant.txt`, `a_invariant_pre.txt`: the 48 and the 4 supplementary runs, 0 violations PRE and POST, with A4 read
as L4 (pins and re-entries alternate in every run; no inadmissible key re-enters; a retired key is at the floor and
neither leader nor member while retired).

## C: false unexplained on modelled ticks — 0 at every α, both priors, unchanged

`c_findings.txt` is byte-identical to `c_findings_pre.txt`: 0 false unexplained on modelled ticks (the truth a COVERED
task) at α = 0.01, 0.05 and 0.1, prior on and off; X confirms it tick by tick (fx@α +0 / −0 in every run). Every added
unexplained tick is on the idle human after the work order (below, L4).

## Boundaries with and without a pin (`l_events.txt`)

- The 48 maintained runs: every boundary is at a pin, at the PRE ticks (0 boundaries without a pin, 0 added, 0 lost).
- The supplementary runs (both priors): a boundary WITHOUT a pin at the misdelivery, scenario_s06_06 at 103
  (`place(item_0,kitting_table_1)`) and scenario_s07_03 at 94 (`place(item_2,kitting_table_1)`); PRE had none. Their
  second boundaries (158 and 189, the pins) unchanged.
- The IRB (`analysis/irb/REPORT.md`, "L-build"): without a pin at scenario_s09_07 33 (the return of a
  change of mind), s09_08 75 (the misdelivery), s09_09 107 (item_3, outside the support).

## Re-entries (L4)

| scenario (runs) | re-entries (tick, hypothesis) |
|---|---|
| s02_01 on and off (tb1a) | 155 `coffee_break(coffee_machine_0)` (pinned 153) |
| s04_01 on and off (tb1a) | 185 `coffee_break` (pinned 183); 207 `ac_activation(ac_switch_1)` (205); 227 `ac_activation(ac_switch_2)` (225) |
| s05_01 on and off (tb1a; tb3 full_reorder and single_task), s05_02 on and off (tb1a) | 56 `coffee_break` (pinned 54) |
| the seven coffee scenarios of the test-bed | 135, 86, 84, 135, 86, 84, 135 (s08_02 to _04, s09_02 to _04, s09_11) |

Every re-entry falls on the tick `waited` clears, two ticks after its pin (the human's latency tick, then its first
step). `ac_activation(ac_switch_0)` in s02_01 and s05 is pinned at the work order's end (362, 141) and the runs end with
the human still there, so it never re-enters. In the test-bed `coffee_break` re-enters in its walk phase every time
(the case of re-entering in the `wait_at` phase, recorded for G at the plan step, did not occur).

## Retractions (L2 (ii)) and boundary fires (L5 B)

Every retraction is refused by admission as `none(leader_inadequate)` and clears the record.

| runs | retraction ticks | what the retracted decision rested on |
|---|---|---|
| s05_01 on, s05_02 on, s05_01 on (tb3 full_reorder, single_task) | 159 | `coffee_break` lone after the work order, admitted at 142 (b + 1 after the AC boundary at 141), inadequate on the idle stand |
| s02_01 on | 380 | `coffee_break` lone after the work order, admitted at 363 (b + 1 after 362) |
| s01_01 off | 159 | `deliver_item(item_4)`, admitted at 143 (TODO-118's measured case) |
| s03_01 full_reorder off (tb3) | 139 | `deliver_item(item_7)`, admitted at 131 (TODO-118's second case) |
| s03_06 off | 194 | `deliver_item(item_7)` |
| s06_01 off (tb1b; tb1c plain, realized; tb3 full_reorder, single_task) | 189 | `deliver_item(item_4)` / `item_1` (the robot's remaining item, lone) |
| s06_02 off (tb1b; tb3 full_reorder, single_task) | 206 | `deliver_item(item_4)` |
| s06_03 single_task off (tb3) | 238 | `deliver_item(item_4)` |
| s06_06 off / on (supp.) | 41 / 41, 177 | the wrong-table leader `deliver_item(item_0)` on its walk to kitting_table_1 (1.4's BINDING_ABSENT, first unexplained 41 at α .05); on, also 177 |
| s07_03 off / on (supp.) | 34 / 34, 208 | the wrong-table leader `deliver_item(item_2)`; on, also 208 |

Totals: prior on 5, prior off 12, supplementary 6. Boundary fires (`cause=boundary`, L5 B): **0 in all 52 runs.** At
every boundary that met a recorded decision, `most_likely` changed (D2's identity side, `cause=replaced`), so the new
condition never had to decide; it is exercised by `tests/test_l_build.py` only. The ten retractions of s06_01 (×5) / s06_02
(×3) / s06_03 / s03_06 prior off, like s01_01 off's, are TODO-119's case bounded as its L note predicted: the lone
hypothesis (the robot's own remaining item, 0.995) is admitted as before, and the decision on it ends when it turns
inadequate.

## Admissions and decisions that moved (`d_decisions.txt`, `x_moved.txt`), by cause

Prior on (primary):
- L4, a re-entered rival lowers the leader's share, so admissions come later and the lone-hypothesis admission at b + 1
  disappears:
  - s05_01 / s05_02 on (×4 runs): the admission of `deliver_item(item_5)` at 60 moves to 67 (0.788; PRE 0.804 at 60),
    its hold of 3 with it; at the AC boundary 94 `ac_activation(ac_switch_0)` is no longer lone at 0.995 but at 0.498
    beside the re-entered `coffee_break`, so PRE's admission at 95 (hold 3) is gone and the next is at 110
    (`recognition_changed(entered)`; PRE 106 by `no_current_task`); after the work order `coffee_break` is lone and
    admitted at 142, retracted at 159 (above). World completion 197 → 194, 198 → 195 (s05_02): the hold of 3 at 95 is
    gone.
  - s02_01 on: `deliver_item(item_5)` admitted at 162 (PRE 160); PRE's admission of the lone `ac_switch_0` at 310 is
    gone (0.496 beside coffee); `coffee_break` admitted at 363, retracted at 380. Completion unchanged (426).
  - s04_01 on: admissions 214 → 218 and 243 → 246 (PRE's `no_current_task` admission at 247 gone); after the work
    order four foreseeable hypotheses are live at 0.249 each (`ac_switch_0`, `_1`, `_2`, `coffee_break`), so PRE's
    admission of the lone `ac_switch_0` at 328 is gone. Completion unchanged (379).
  - reveals (E): later or lost only here: s02_01 item_5 160 → 162, `ac_switch_0` 309 → none (PRE's reveal was the lone
    hypothesis at 0.991 by normalisation on the boundary tick); s04_01 `ac_switch_2` 214 → 218, item_6 243 → 246;
    s05_01 / _02 item_5 60 → 67, `ac_switch_0` 94 → 110.
- The supplementary runs, prior on (L1 and L2 (ii)): the retraction at 41 (34) withdraws the wrong-table leader's
  projection; at the misdelivery boundary 103 (94) the belief is reset, so PRE's admission of the stale leader at 103
  (94) and at 154 (125) is gone, and the next delivery is admitted at 111 (101) on its own evidence
  (`deliver_item(item_3)` 0.799; 0.796). Completion unchanged.

| run | world completion (T6) | declared | admissions built / decisions |
|---|---|---|---|
| s02_01 on | 426 → 426 | 428 → 428 | 6/12 → 6/12 |
| s04_01 on | 379 → 379 | 381 → 381 | 6/12 → 4/10 |
| s05_01 on (tb1a; tb3 ×2) | 197 → 194 | 199 → 196 | 4/8 → 4/10 |
| s05_02 on | 198 → 195 | 200 → 197 | 4/8 → 4/10 |
| s06_06 on (supp.) | 265 → 265 | 267 → 267 | 6/10 → 5/10 |
| s07_03 on (supp.) | 243 → 243 | never | 5/10 → 4/10 |

Every other prior-on run: no decision moved, completion unchanged.

Other statistics that moved, prior on (`x_moved.txt`): unexplained (any truth) +634 at α = 0.05 (+594 / +649 at .01 /
.1), all on the idle human after the work order with `coffee_break` lone and re-entered: s02_01 380–449, s05_01 /
s05_02 (×4 runs) 159–299 (the entry's consequence: "the exit walk reads unexplained"); exhausted −724 (s02_01 362–449,
s05 ×4 141–299: the same ticks); lone live hypothesis +774 / −312; adequate below θ +162 / −25 (the lower shares beside
a re-entered rival: s02_01 160–161, 310–361; s04_01 214–217, 243–245; s05 60–66, 95–109; supp. s06_06 104–110 added,
129–153 removed, s07_03 95–100 added); unresolved +7 (boundary ticks that were exhausted in PRE, the last foreseeable
hypothesis now live again: s02_01 362, s05 ×4 141; and the new boundaries without a pin, supp. 103 / 94).

## Completion ticks

Prior on above. Prior off (appendix, below). TODO-127, checked before comparing: `tdlib.robot_completion` reads the
right line; the world tick is the tick after the robot's last release with a task (s06_02 off: release 266, world 267).
The declared tick equals it when the pool empties on a `recognition_changed` of that tick (the robot's item pinned
changes `most_likely`, and `update()` drops the completed task, T7), and is world + 2 when `no_current_task` ends the
pool. Under L the retraction clears the record earlier in these prior-off runs, so the pin no longer fires a trigger
and their declared tick moves by 2 with the world tick unchanged (s03_06, s06_01 ×5, s06_02 ×3 below). Not a reader
defect; the relation "declared = world + 2" in CLAUDE.md holds for `no_current_task` endings only.

## Appendix: prior OFF

| run | world | declared | admissions | cause |
|---|---|---|---|---|
| s01_01 off | 201 → 186 | 201 → 188 | 3/8 → 3/9 | L2 (ii): retraction at 159 ends the 31-tick hold (PRE 143–173) |
| s03_01 full_reorder off (tb3) | never (last release 130) → 227 | never → 229 | 3/7 → 3/8 | L2 (ii): retraction at 139 ends the 89-tick hold (PRE to 219, never completing; TODO-118) |
| s06_03 single_task off (tb3) | 316 → 282 | 316 → 284 | 5/8 → 5/9 | L2 (ii): retraction at 238; the robot's lines differ from 238 |
| s03_06 off | 236 → 236 | 236 → 238 | 5/10 → 5/11 | L2 (ii) at 194; see TODO-127 above |
| s06_01 off (tb1b; tb1c ×2; tb3 ×2) | unchanged (265 or 224) | +2 | +1 decision | L2 (ii) at 189 |
| s06_02 off (tb1b; tb3 ×2) | unchanged (267 or 224) | +2 | +1 decision | L2 (ii) at 206 |
| s02_01 off | 422 → 422 | 424 → 424 | 5/11 → 4/9 | L4: PRE's admission of `ac_switch_0` at 328 gone (0.431 beside coffee) |
| s04_01 off | 379 → 379 | 381 → 381 | 4/11 → 4/11 | L4: `ac_switch_2` admitted 217 → 219 |
| s05_01 / s05_02 off (×4) | unchanged (194, 195) | unchanged | 3/8 → 3/8 | L4: admissions 70 → 71 (hold 5), 104 → 111 |
| s06_06 / s07_03 off (supp.) | unchanged | unchanged | 4/9 → 3/8 | L1 and L2 (ii), as prior on |

Other statistics, prior off: unexplained −122 and exhausted +122, on the same ticks (s01_01 186–200, s03_01
full_reorder 227–299, s06_03 single_task 282–315): the robot completes earlier, its remaining item is pinned earlier and
nothing is live; lone live hypothesis +41 / −651; adequate below θ +95 / −25; pins +3 / −2 (the robot's last pins at
the earlier completion ticks); boundaries +2 (supp.); re-entries +8 (as prior on).

B (`b_cases.txt` against `_pre`): only B6's boundary rows moved, by the beliefs printed at b .. b + 5 where a re-entered
rival shares the mass (s02_01, s04_01, s05); the letter sequences (U on the boundary tick, A after) are unchanged.
H (`h_cases.txt`): H4 (the finished work order, s04_01 on) now reads four foreseeable hypotheses live at 0.249 each,
none admitted, the finding unexplained from 343 / 344 as before; the wrong-table case (s06_06) reads the boundary at
103 (unresolved, the stale leader at the prior 0.498) in place of PRE's leader at 0.995.

## Runs and tests that disagree with the mechanism

None at HEAD.
- The IRB found two build defects of L-build, both in the recognizer and both against the records (handback
  §1.7, the tie-break "the first live key in sorted order"): the re-entering key's evidence and base were set after the
  loop, so a 1/2 tie at the re-entry (135 in s08_02, s09_02, s09_11) and at the next boundary (127 in s08_03, s09_03;
  139 in s08_04, s09_04) went to the incumbent. Fixed in 5129d90 and 3d65ca6, each with a test that fails on the code
  before it; the sixteen then agree at 1e-9 and at print precision. The maintained baselines above are the regeneration
  after both fixes.
- Tests: the full suite passes (149). td1, td15 and irb2b needed no re-derivation: every hand-built release in them is a
  boundary under both criteria and every delivery by another agent a pin without one; td1's helper followed the rename
  `_completed` → `_retired` (mechanical). The 14 new tests (`tests/test_l_build.py`) pass; the tie-break test fails on
  the code before each fix. The other new tests were not run against the pre-L code: every one constructs a
  `BeliefState` with `episode_boundary` or reads `_retired`, which that code does not have.

## Flags (not fixed)

- Commit 2c54c4a alone does not run a simulation: the recognizer passes `episode_boundary` to `BeliefState` there, and
  the body's dummy belief gains the field only in 493c095 (the test suite at 2c54c4a passes; nothing in it builds the
  dummy belief). History not rewritten.
- A retired hypothesis the planner cannot decompose on a later tick stays retired (its terminal fact cannot be read, so
  nothing says it stopped holding); the entry does not state it; no scenario reaches it.
- L5 B never fired in the 52 baselines or the sixteen test-bed runs (the robot's pool is empty there): its only evidence
  is the unit test.
- CLAUDE.md's "declared = world + 2" holds for `no_current_task` endings only (TODO-127, above).
