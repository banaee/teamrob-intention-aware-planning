# T-K part 1, step 3 (the build): the session's state

Written by ccode on 4 October 2026 during the build (the plan: `docs/handoffs/plan_T-K_part1.md`), kept current
stage by stage, so that a compaction or a new session loses nothing. The records of what was built are in
`docs/design_records.md`, "T-K", THE BUILD (stages 1 and 2 recorded at the gate's stage; the rest in stage 7).

## Status

BUILD STAGE 7 committed: the build of T-K part 1 (step 3) is complete. Stage 6 (766f7d3) and stage 7 (the records
commit that carries this file) were built in the second session (4 October 2026, one model, no pause before stage 7,
as Hadi ruled). Nothing of the build is left to do; the next step is step 4 of `docs/handoffs/T-G_forward_inputs.md`,
section 5.7 (the timelines and the runs with context knowledge on), in the design chat.

| stage | commits | check |
|---|---|---|
| 0 | none (baselines B0 at 93f9083, local) | one pass of the scope: about 8 minutes |
| 1 | b85494d (the rename) | passed: 85 logs identical except the `[run]` field and `[IR-assignment]`; .rec byte-identical |
| 2 | 91774ce (2a, the gate), 3b05a8a (2b, the instruments), 733e593 (2c, B2 and the records) | passed: 0 disagreements (round 1, IRB, MPB); every declared property as before; every coverage cell reached |
| 3 | bbb7227 (the option, ω removed), 67b899e (the sweeps' mode) | passed: identical to B2 except the `[run]` field; milestones from step 500 the recognizer's lines only |
| 4 | f70f72f (4a, the timeline), 2393935 (4b, the facts, switch_on, dock_loading's ac_activation) | passed: the timeline line and switch_on's name only; every scenario loads; 329 tests |
| 5 | e589731 (the mind) | passed: off identical to stage 4 (85 logs, .rec, round 1's 248 instrument files, the `[run]` header); on: all 85 runs complete; 352 tests |
| 6 | 766f7d3 (the instruments) | passed: round 1, the IRB and the MPB (both strategies, prior-off diagnostic) with context off, every instrument output identical to B2 after the named additions; round 1 on, 0 disagreements in all 31 (results not read); 352 tests |
| 7 | the records commit (HEAD) | the final regeneration at 766f7d3: the four sets, kitting's IRB, round 1 and the MPB in the repository, md5s in the READMEs |

## The rules Hadi added in this session (beside the build prompt)

- Small and obvious: a defect in code, a test, an instrument or a run file, a stale reference, a name or wording, the
  order of work inside a stage, a check that failed for a reason ccode can state and repair without changing what is
  built: ccode decides it, fixes it, continues, and notes it in one line in the final report's flag list. The test:
  does it change what is built or why, a ruled value, a ruling, or a core algorithm beyond the plan? If no, decide.
- Parallel work, three conditions: a check never reads a tree being edited (it runs on a snapshot of the stage it
  checks); each stage is committed from its own files, alone, after its check passed, and the next stage's check runs
  after that commit against that stage's outputs; a failed check that is not a plain defect stops the later stage's
  work too. Noted in the final report's flag list.
- Every message that reports, pauses or stops opens with: "BUILD STAGE <n> <committed | in progress>. <continuing |
  waiting for Hadi: model switch | stopped: blocking condition>."
- Two planned pauses for a model switch: after stage 4's commit, before stage 5's first edit ("stage 5 next", with the
  gate's stage report printed again); after stage 6's commit, before stage 7. Hadi answers "continue".
- This file: the session's state, kept current; the session ends after stage 5's commit (Hadi, 4 October 2026).
- The second session (Hadi, the build prompt of stages 6 and 7): one model, so no pause before stage 7; the oracle's
  independence stated in the report; a disagreement in round 1 with context knowledge on that is not a plain defect
  stops the session (none occurred).

## Where the outputs lie on disk

- The repository's analysis folders hold B2 (stage 2's regenerated outputs): `analysis/kitting/<set>/sweep/` for
  the four maintained sets (md5s in each README's last section), `analysis/kitting/irb/` (s08, s09), `irb/tk1/`
  (round 1) and `analysis/kitting/mpb/`. Stages 3 to 5 regenerate nothing there: their checks compare against B2
  with the named lines set aside (the `[run]` field, the timeline line, switch_on's name).
- The old data (before the gate's stage): `/home/hadi/teamrob_analysis_2026-10-04/` (AM59; its README.txt).
- After stage 7 the repository's analysis folders hold the final regeneration at 766f7d3 (the four sets' `sweep/`,
  `irb/`, `irb/tk1/`, `mpb/`); B2's md5s stay in the READMEs' stage 2 sections, the final ones in their stage 7 sections.
- The second session's scratch (lost with it): `.../a763ea38-811e-46c5-b748-82fb87a4397a/scratchpad/`: `s6_tree/`,
  `s6/` (stage 6's first pass: irb, tk1, tk1_on, pytest), `s6b_tree/`, `s6b/` (the MPB passes after the repair),
  `final/` (stage 7's regeneration outputs: the sweeps' and instruments' console output, sep_classes tables),
  `compare_outputs.py` (extended for the stage 6 additions), `run_stage6.sh`, `run_mpb6.sh`, `run_final.sh`, `fticks.py`.
- The first session's scratch outputs (session-specific; lost with it): `/tmp/claude-1000/-home-hadi-Nextcloud---Research---TeamRob-Framework-teamrob-intention-aware-planning/a9b7dcc0-3fd2-4649-a7e9-11f4fdf149f0/scratchpad/`: `b0/` (B0), `s1/`, `s3/`, `s4/`, `s5/`
  (each stage's scope: the four sets, `tk1/`, `dl_milestone/`), `s2_tree/analysis/kitting/` (B2 as produced),
  `s5/on_*` (the on runs). The scripts: `run_scope.sh <tree> <out>` (the scope), `run_on.sh`, `run_stage6.sh`,
  `compare_scope.sh`, `compare_gate.sh`, `compare_s4.sh`, `compare_outputs.py`, `gate_moves.py`,
  `mpb_moves.py`, `snapshot_tree.sh`. A new session regenerates any of them from the commits.

## What the next session reads first

THE BUILD IS COMPLETE (stage 7 committed). The two sections below describe the state between stages 5 and 6 and are
kept as the record of how the build was carried over; nothing in them is left to do.

`docs/handoffs/plan_T-K_part1.md` (stages 6 and 7, sections 8 and 9), this file, CLAUDE.md, `docs/glossary.md`, the
T-K entries of the records; then `git status` (stage 6's 14 modified files below, plus nothing untracked). The build
prompt and Hadi's rules of this session (above) hold. Stage 6's check needs no scratch file from this session: its
baseline is the repository's analysis folders (B2) and the named differences; `run_stage6.sh` and
`compare_outputs.py` are reproduced from their description here if the scratchpad is gone.

## Stage 6, as it stands in the working tree (uncommitted)

Files: `analysis/instruments/irb/{trajectory,oracle,compare,actual,admission,summary,run.sh}`,
`analysis/instruments/common/tdlib.py`, `analysis/instruments/mpb/{actual,reference,mpb_oracle}.py`,
`mesa_sim/list_scenarios.py` (the declaration at every instrument SimModel call), `analysis/kitting/irb/README.md`
(rules 29 to 33), `analysis/instruments/irb/README.md`. Smoke test on scenario_s15_02: 0 disagreements with
context knowledge off and on. Its check (`run_stage6.sh`): round 1, the IRB and the MPB sets with context off, every
instrument output byte-identical to B2 after the named differences (the new columns prior/levels/recent, switch_on's
name, the timeline line); round 1 with it on: 0 disagreements (AM49), results not read; pytest.

## Stage 7 (not started)

The BUILT block under "T-K" (stages 3 to 7, commits, acceptance); docs: `docs/assumptions.md` 1.4 (both options on
by default), `shared/io_contracts.md` (BeliefState: belief, prior, levels; update()'s recent), `docs/recognizer_handback.md`
§1.7 and §2 (ω gone, the prior), the glossary's BUILT lines (§5's T-K terms, `[IR-prior]` renamed), CLAUDE.md (the
commands' flag, the state, the greps: `[IR-assignment]`, `[IR-context]`, `[run_mesa] timeline`), the roadmap,
TODO-66 closed, TODO-139; the maintained sets' and round 1's README sections (the final md5s and every named line
since B2); `docs/handoffs/T-G_forward_inputs.md` section 5 (5.5, 5.6, 5.7 step 3 done).

## The flag list so far, by stage (each with what ccode suggests)

- Stage 1: the tb1c set's `check.py` renamed too (a maintained set's script, not frozen); the frozen folders' scripts
  keep the old flag. Suggest: nothing.
- Stage 2: `tests/kitting/test_td1_adequacy.py` and `test_tg_liveness.py` asserted the old gate's reading of a lone
  live hypothesis's confidence (1 − floor·pins); updated to AM42 (small, obvious). The MPB's `plot_ir.py` needed the
  new column (a plain defect, found by the first MPB pass). Round 1's rerun confirmed all 31 rows of its
  foreseeable-task ticks. Finding: scenario_s07_02 (dock_loading milestone) gains one moving-robot F1 violation from the
  admission one tick earlier (recorded; dock_loading's step). Suggest: read it at dock_loading's step.
- Stage 3: the sweep scripts lost their executable bit in bbb7227 (restored, 67b899e). The run without context
  knowledge in the milestone runs differs from step 500 only in the recognizer's lines (as the plan expects).
- Stage 4: the 4a load check also covers the completion condition (AM54) and the `"states"` block (AM50). The named
  lines also reach the human's per-tick step lines and the executor's `_load_plan` line (switch_on's name), beside
  `[rec]` and `[human]`. The override tests count `[run_mesa]` lines; updated for the timeline line. My test helper
  built kitting's tree from a hand list (a defect of the test; now from the registry).
- Stage 5: a task schema is unhashable (a dataclass with eq), so the recency facts are a tuple compared by identity,
  not the plan's frozenset. The declared knowledge's source strings are in the registries (one per value). The
  recognizer's constructor requires `context` (every caller states it; three tests updated). Observed in the smoke
  run with context on, not read (AM49): a lone live delivery is admitted at its stretch's first tick (KT11's ruled
  expectation); the coffee break at the ordinary strength reaches θ later than under the equal prior.
- Stage 6: `run.sh --context on|off` (how); the oracle's prior is in a class of its own, ContextPrior, with rules 29
  to 33, and its lookup of a task's entry is its own (`entries()` read once); the A/C's belief at arrival is read at
  the first tick of its switch_on in the trajectory. Found by the check and repaired (small, obvious): the MPB's
  `actual.py` compared the in-process lines unfiltered against the filtered log, so the model's own `[run_mesa]
  timeline` line (stage 4a) failed its identity assertion in every MPB run; a stray indentation in
  `mesa_sim/list_scenarios.py`. The comparer's named additions grew by two the plan did not list: the A/C's effect
  `ac_on(switch)` among the trajectory's facts from the completion on (stage 4b's ruling, AM43) and
  `params.recency_ticks`. Suggest: nothing; both are consequences of ruled items.
- Stage 7: the final regeneration ran in the repository's working tree at 766f7d3 while this session edited documents
  only (no code, no config, no artefact); the runs read none of them. Suggest: nothing.
- Parallel work used as Hadi allowed: each stage's check ran on a snapshot while the next stage was edited; each
  commit was staged from the snapshot's files.
