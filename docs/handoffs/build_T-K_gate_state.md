# The build of the two gate rulings (AM67, AM68): the session's state

Written by ccode on 4 October 2026 during the build (the plan: `docs/handoffs/plan_T-K_gate.md`, approved with D1 to
D7), kept current stage by stage, so that a compaction or a new session loses nothing. Each stage is its own commit
after its check; a pause after each stage's commit until Hadi's "continue". Every report opens with "BUILD STAGE <n>
<committed | in progress>. <waiting for Hadi | stopped: blocking condition>." The measurements with context
knowledge on (the plan's section 8) are not in this session.

## Status

| stage | commits | check |
|---|---|---|
| (rulings) | 3a4f00b | D1 to D7 recorded, the plan approved |
| 0 | none (B0 at 3a4f00b, local) | all jobs exit 0; 0 oracle disagreements (s14_02's known print-precision flag apart); every MPB property holds; 352 tests; B0 byte-identical to the repository's outputs |
| 1 | 2c939a5 | passed: 1298 output files identical to B0 after dropping `[IR-rank]` lines (logs, .rec, every instrument output); 54,816 `[IR-rank]` lines; the leader never outranked on 50,734 ticks (context off, F7); 359 tests |
| 2 | 02956ba | passed: 1298 output files byte-identical to stage 1 (context knowledge off: AM68 refuses nothing, F7); 365 tests |
| 3 | 725d673 | passed: 153 logs as predicted (17 maintained and 6 MPB logs first differ on their commitment-only admission's tick; the rest identical with `warrant=commitment,observation` read as `warrant=observation`); every .rec identical; IRB gate column 7 ticks in 5 runs, round 1 41 in 6 (clears to unwarranted, nothing else); every MPB property holds; the old oracles' disagreements are those ticks and the warrant text (stage 4); 363 tests |
| 4 | (this commit) | passed: every log identical to stage 3; IRB (17) and round 1 (31): 0 disagreements with the oracle (s14_02's known print-precision flag apart), 972 rank cells undetermined and skipped (exact ties), no gate undetermined; MPB (16 x 2 strategies): 0 disagreements on parts 1 to 3, no chain stop, every declared property holds; the prior-off appendix runs; 365 tests |

## Where the outputs lie

- B0 and each stage's scope: the session's scratchpad (`b0/`, `s1/`, ...; lost with the session; regenerated from the
  commits by `run_scope.sh`): the four sets' sweeps, `irb/` (s08, s09), `tk1/` (round 1), `mpb/` (single_task),
  `mpb_f/` (full_reorder), `mpb_off/` (the prior-off appendix), `dl/` (dock_loading's six milestones, context
  knowledge off), `pytest.txt`.
- The scripts (scratchpad): `snapshot.sh <dir>` (the working tree's tracked and untracked files), `run_scope.sh <tree>
  <out>` (eight parallel jobs, each in its own copy of the tree with its own `logs/`), `compare_scope.py <base> <new>
  [--drop PREFIX]` (logs line by line after dropping lines with the prefix, every other file by bytes).
- The external copy of the untracked data before the build: `/home/hadi/teamrob_analysis_2026-10-04_gate/` (3a4f00b).

## Decided by ccode in the build (listed in the stage reports)

- Stage 1: the rank is logged on its own line `[IR-rank]`, not as a field of `[IR]` (the plan's alternative; amended in
  the plan, section 2.1).
- Stage 3: the MPB instrument's in-process hook (`mpb/actual.py`) reads the leader's observation warrant in place of the
  removed `_warrant`, so stage 3's scope runs; the rest of the instruments is stage 4's. Unused imports (`FrozenSet`,
  `Set` in the meta-planner; `domain_config` in test_g_build) removed.
- Stage 4 (instruments): the IRB oracle's `rank` column and `undetermined` (D3) within compare.py's agreement level
  (relative 1e-9, absolute 1e-12), so an exact tie (a boundary tick, a symmetric stand) is undetermined there; the gate
  `undetermined` when it turns on an undetermined rank; compare.py skips and counts both. The MPB: `Gate.LEADER_OUTRANKED`
  and `Gate.UNDETERMINED` in mpblib; chain.py stops (SystemExit, nothing guessed) when it asks an undetermined gate, and
  run.sh then reports "no chain" and continues (cannot occur with context knowledge off). The alteration engine: C1
  retired, C3's anchor follows the new gate text, RANK = C4 to C6 run only by `analysis/kitting/mpb/alteration.py
  --rank` on step 5's six; the run file found below `configs/<domain>/mpb/` (step 5's are in `tk/`). C4 to C6 are built
  but NOT RUN in this session: they compare against step 5's actual files, which are the pre-build runs until the
  measurement step reruns them; they run there (D6). Step 5's re-declared properties (D5) are written in the
  measurement step, before its runs.
