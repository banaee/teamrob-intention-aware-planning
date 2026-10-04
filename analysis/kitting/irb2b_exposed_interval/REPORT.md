# IRB.2b: the 1.4 and 1.5b measurements over the exposed interval (closes TODO-121)

> Superseding note (4 October 2026, T-K part 1, step 1; design_records.md, "T-K", STEP 1): the case on scenario_s04_01 (scenario_40) is no longer reproducible. env_layout_05 now holds one A/C switch, ac_switch_1 (ac_switch_0 and ac_switch_2 removed), and scenario_s04_01's script one ac_activation (the walk to ac_switch_2 removed); this record describes three switches and two activations. The scenario's logs under `pre/tb1a_destination/` were deleted; they were local and git-ignored, in no commit (a copy as of 2 October 2026 at /home/hadi/teamrob_analysis_2026-10-02/kitting/tb2b_exposed_interval/); the layout and script they ran on are last held by 4345ef9.

27 September 2026, at the IRB.2b build: 4de9cce (records), d03e31e (`RobotAgent.step`), 50a2aab (tests), f3d64d6
(baselines). The cognitive-loop correction (design_decisions.md, "The cognitive loop does not end with the task pool"):
observation, recognition and their `[IR]` / `[IR-dist]` logging run on every tick; the `finished` guard sits after
them, so after the terminal return no trigger is evaluated, nothing is decided and the executor is not stepped.
Before it, every run's `[IR*]` lines ended at the robot's declared completion tick N (checked on the 16 tb1a logs
before the build: the last `[IR]` step equals N in each). This report reruns 1.4's and 1.5b's scripts over the
regenerated baselines, which now reach the run's last tick, and reports every number that moved against 1.5c, with
its ticks and whether it lies in the newly exposed interval N+1..last. No previous statistic is preserved for
comparability.

## Material and conventions

- PRE: the 1.5c baselines, md5-checked against the READMEs' "T-D cycle 1.5c" sections (48 of 48) and copied to
  `pre/<set>/` before any code changed; `pre/supp/`: the four supplementary wrong-table runs
  (`analysis/td_stage1b/supp_sweep.sh`) at cecf5ec, before the build, byte-identical to `td_stage1b/post/supp/`.
- POST: the four maintained sets regenerated at IRB.2b (`analysis/<set>/sweep/`, md5s in the READMEs' "IRB.2b" sections)
  and `post/supp/`. All logs git-ignored. The 52 `.rec` streams are byte-identical PRE and POST.
- SCRIPTS: `analysis/td_stage1b/`'s copies of 1.4's scripts (1.4's logic, adapted there to the `leader_adequacy=`
  field), copied here with the paths only changed, plus one switch in `tdlib.py`: `TD_SIDE=pre` makes a script read
  the PRE logs as its primary side, so each statistic is computed by the same code on both sides and the outputs are
  diffed (`<script>_pre.txt` against `<script>.txt`). `analysis/td_stage1/`'s own copies were not run: their `[IR]`
  regex has no `leader_adequacy=` group and would drop the tails silently (confirmed with Hadi at the plan step).
  D and E compare PRE with POST themselves (one output each). G and the clip drive the simulator: G's simulator part was run at
  cecf5ec (a scratch worktree, before the build) and at HEAD, identical; `g_priced_standing_pre.txt` is HEAD's
  simulator part with the log tally on the PRE logs (`TD_SIDE=pre`). The clip (`clip_sweep.sh`, the 17 prior-off
  conditions of `td_stage1b/clip_ticks.txt`, each at its sweep's step count) was run at cecf5ec and at HEAD, identical
  to each other and to 1.5b's file (the PRE output not kept).
- NEW: `baseline_diff.py` (the regeneration criterion), `x_moved.py` (every statistic's tick set per run, ungrouped, on
  both sides, and the moved ticks, each marked EXPOSED (> N) or TRUNCATED (≤ N)), `x_summary.py` → `x_summary.txt` (per run: N, the
  exposed span, the added ticks per moved statistic), `clip_sweep.sh`.
- Truth lag-corrected (the record at t + 2), α ∈ {0.01, 0.05, 0.1}, prior ON primary, prior OFF an appendix, as in
  1.4 and 1.5b. Run from this directory with `~/python-envs/ir-nomesa-env/bin/python <script>.py > <script>.txt`
  (`TD_SIDE=pre` for `_pre.txt`); G and `clip_sweep.sh` from the repo root with `PYTHONHASHSEED=0`.

## The regeneration criterion (`baseline_diff.py` → `baseline_diff.txt`) — MET in every log

Per log: (i) the log with every `[IR*]` line removed is byte-identical; (ii) the `[IR*]` lines up to and including the
declared tick N are byte-identical (`[IR-prior]` included); (iii) the `.rec` is byte-identical; and every new `[IR*]`
line carries a step > N.

| set | logs | met |
|---|---|---|
| tb1a_destination | 16 | 16 |
| tb1b_two_tables | 4 | 4 |
| tb1c_realized_flip | 8 | 8 |
| tb3_full_reorder | 20 | 20 |
| supplementary | 4 | 4 |

No failing log, so no first differing line to report. Every md5 changed: within every tick the robot's `[IR]` and
`[IR-dist]` lines now precede its `[meta-trig]` line (recorded in the entry's consequences), and the runs whose robot
completes gain lines. Two runs have no exposed interval, their robot never completing: scenario_s03_01 full_reorder
prior off (TODO-118) and scenario_s07_03 (supplementary, both priors); their `[IR*]` lines are unchanged apart from
their position within the tick.

The new lines are `[IR]` and `[IR-dist]` only: no `[IR-complete]` and no `[IR-boundary]` falls in any exposed
interval. In all 52 runs the human's stack is empty before N (every exposed tick's truth, raw and lag-corrected, is
"no task": 2,033 ticks prior on, 1,898 prior off), so the exposed interval is the idle human after its script, never a
modelled tick, a boundary or a pin.

## What moved, prior ON (`x_moved.txt`, `x_summary.txt`)

Every added tick lies in the exposed interval; no tick was added at or before N and none was removed. Unmoved, at every
α where α applies: false unexplained on modelled ticks (0 / 4,352 modelled ticks and 0 / 204 phase instances in C's
aggregate, raw and lag-corrected, every phase 0: the denominators do not move, no modelled tick being exposed);
non-member ticks (the true hypothesis live and not a member: 0 added); unresolved ticks (0 added); adequate-below-θ
(F: 0 added); boundaries (0 added; B6's 64 `UAAAAA` and the step-0 `A` rows unchanged); pins (0 added);
admissions (D: 0 differing decisions in 48 runs, admissions built/decisions and the world and declared completion ticks
identical in every run). Reveals (E): none lost or later. G (the priced standing) identical at cecf5ec and at HEAD;
its walking-D tally reads 3,891 member ticks at D = 0 on both sides.

| statistic | added ticks | runs, ticks |
|---|---|---|
| exhausted | +1,983 | every prior-on run with an exposed interval except s04_01 and s06_06: from N+1 to the run's end (s01_01 172–299, s02_01 429–449, s03_01 241–299 / full_reorder 224–299, s01_06 163–199, s03_06 239–299, s05_01 200–299, s05_02 201–299, s06_01 227–339 or 268–339, s06_02 227–339 or 270–339, s06_03 227–339, 229–339 or 268–339) |
| unexplained (any truth), at α = .01 / .05 / .1 alike | +50 | s04_01 on 382–399 (18), s06_06 on (supp.) 268–299 (32) |
| lone live hypothesis | +50 | the same ticks: `ac_activation(ac_switch_0)` in s04_01, `deliver_item(item_0)` in s06_06 |

- s04_01 on is TODO-117's case: `ac_switch_0` the lone live foreseeable hypothesis after the work order, unexplained
  from 344 (1.4, §H case 2) and now through 399; B5 (no task on the stack) 55 → 73 ticks, X 29 → 47 / 37 → 55 /
  40 → 58 (α .01 / .05 / .1).
- s06_06 on is the wrong table (BINDING_ABSENT, TODO-87): `item_0` was delivered to the other table, so its hypothesis is
  never pinned and stays live; the idle human reads unexplained against it through the run's end (B5 110 → 142 ticks,
  X 83 → 115 / 91 → 123 / 94 → 126). The BINDING_ABSENT detection itself (C: first unexplained s06_06 48 / 41 / 38,
  s07_03 39 / 34 / 31) is unchanged.
- 1.4's exhausted episode rows (B5) grow accordingly: s01_01 on 31 → 159 exhausted ticks, s02_01 67 → 88, s03_01
  120 → 179, s01_06 43 → 80, s03_06 63 → 124, s05_01 59 → 159, s06_01 97 → 169, s06_02 82 → 152, s06_03 7 / 9 / 48 → 120 (its runs now one group).
- A (the R6 invariant, A1–A8): 12,929 → 16,860 ticks checked, 0 violations on both sides.
- The clip (E10, decision 3): identical to 1.5b's `clip_ticks.txt`; no clip tick in any exposed interval.

A reading that changes, not a number of a statistic:
- GROUPING. `tdlib.ir_groups` merges runs with identical `[IR*]` lines and `.rec`. Before, prior-on runs of one scenario
  differed only in where the robot's completion cut the `[IR*]` stream; now every stream reaches the run's last tick,
  and with the prior on the recognizer's output does not depend on the robot's options: s06_01 on is one group of 5
  (tb1b, tb1c plain / realized, tb3 full_reorder / single_task), s06_03 on one of 4, s06_02 on and s03_01 on one of 3
  each, s05_01 on and s05_02 on one group (their `.rec` streams are identical, 1.5c's table). The per-group lines of
  B, C and F change with it; their per-run tick sets do not (`x_moved.txt`).

## Appendix: prior OFF

Every added tick lies in the exposed interval; none added at or before N, none removed. Unmoved: false unexplained
(0 / 4,352, 0 / 204), non-member, unresolved, adequate-below-θ, boundaries, pins, admissions, reveals, the clip.

| statistic | added ticks | runs, ticks |
|---|---|---|
| exhausted | +1,375 | s01_01 202–299, s03_01 239–299 (×2), s03_06 237–299, s06_01 / s06_02 / s06_03 in every set from N+1 to 339 |
| unexplained (any truth), every α | +523 | s02_01 425–449 (25), s01_06 163–199 (37), s04_01 382–399 (18), s05_01 197–299 (103; ×3: tb1a, tb3 full_reorder, tb3 single_task), s05_02 198–299 (102), s06_06 (supp.) 268–299 (32) |
| lone live hypothesis | +498 | the same runs except s02_01 (more than one hypothesis live there): item_6 (s01_06), ac_switch_0 (s04_01), item_3 (s05_01), item_2 (s05_02), item_0 (s06_06) |

With the prior off the hypothesis space holds every item of the setup; an item hypothesis no agent completes is never
pinned and stays live after both agents finish, and the idle human reads unexplained against it (s05_01: `item_3` is in
the room and assigned to neither agent; `[IR] step=250 … deliver_item(?item=item_3) confidence=0.995 … finding=
unexplained leader_adequacy=inadequate tails=[…=0.0000]`). This is TODO-119's and TODO-117's ground (P, G, L), not a
new mechanism question.

B6, the one boundary row that moved: s06_03 plain prior off (tb1c), boundary b = 220, `UAAAE` in 1.5c, `UAAAEE` now.
B6 reads the window b..b+5 (220–225). The run's N is 224, the tick on which the robot's last delivery pins the last live
item, so the recognizer is exhausted from 224; the PRE `[IR]` lines ended there, and the sixth tick, 225 (E), was
missing. It lies in the exposed interval. 1.5c's description "one `UAAAE` cut by exhaustion" was a cut by the
truncation, which fell on the exhaustion tick.

## Runs and tests that disagree with the mechanism

None. The regeneration criterion holds in all 52 logs. The two new tests (`tests/test_irb2b_cognitive_loop.py`) pass at
HEAD and fail on the previous `RobotAgent.step` (checked by swapping the file back); the full suite passes (135).
Every added unexplained tick is on an unmodelled tick (the idle human, no task on the stack) with every member's
S below α, which is the finding the mechanism defines (E4, E6); every added exhausted tick has no live hypothesis
(R4). Whether an idle human after the work order should read unexplained against a lone foreseeable hypothesis
(s04_01) or an undelivered item (prior off) is TODO-117's and TODO-119's question, not a disagreement.

## TODO-121, closed

The 1.4 and 1.5b measurements are rerun over the exposed interval. In these baselines the interval is the idle human
after its script in every run: no modelled tick, no boundary, no pin, no decision lies in it, so every statistic 1.5c
reported over modelled ticks or decisions is unchanged (false unexplained 0 at every α; non-member, adequate-below-θ,
boundaries, admissions unchanged), and what moved is the recognizer's output over the idle human: exhausted ticks
(+1,983 prior on), and unexplained ticks against a lone live hypothesis that nothing will complete (+50 prior on:
s04_01's `ac_switch_0`, s06_06's wrong-table `item_0`). The truncation had hidden no false unexplained tick.

## Flags (not fixed)

- TODO-34 is not reachable before or after the build: `build_observation` returns an `Observation` on every path and no
  human leaves `model.humans`, so whenever `human is not None`, `obs` is bound and belongs to this tick.
- `d_decisions.txt` prints, for the prior-off runs, a world completion tick (`tdlib.robot_completion`, T6) equal to the
  declared one (e.g. s06_02 off: world 267, declared 267), where the prior-on runs read world = declared − 2 (s01_01 on
  169 / 171). Identical PRE and POST, so not IRB.2b's; not examined.
