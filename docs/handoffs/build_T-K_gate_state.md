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
| 3 | (this commit) | passed: 153 logs as predicted (17 maintained and 6 MPB logs first differ on their commitment-only admission's tick; the rest identical with `warrant=commitment,observation` read as `warrant=observation`); every .rec identical; IRB gate column 7 ticks in 5 runs, round 1 41 in 6 (clears to unwarranted, nothing else); every MPB property holds; the old oracles' disagreements are those ticks and the warrant text (stage 4); 363 tests |

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
