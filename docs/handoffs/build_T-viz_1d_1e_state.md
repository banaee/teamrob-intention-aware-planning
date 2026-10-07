# Build state: T-viz 1d and 1e, the paths on the floor

The session's state file (the task of 7 October 2026: record Hadi's preferences for the paths on the floor; then a short
plan and the build without a pause). The plan: `docs/handoffs/plan_T-viz_1d_1e.md`; the records: design_records.md,
"T-viz, the web-ui", 1d AND 1e blocks.

## Done

- Part 1, the records (27792da): Hadi's items 1 to 5; the roadmap; TODO-197's form.
- Verified: the human's later walks are available ahead (the frame's whole expansion), except while a cut action is
  finished on a resumption.
- B0: the four maintained sets and dock_loading's scenario_s03_02, s05_02, s07_02 (800 steps), run at 27792da from a
  separate worktree.
- The messages and Mesa's piece, with tests/test_tviz_paths.py (90a6a12). B1 equals B0 on 150 files; the 96 logs and
  record streams of the maintained sets equal the baselines on disk.
- The page (3189877): the drawing layer, the switches, vitest test/paths.test.ts.
- Checks: the suite 455 passed; vitest 56; build and type check; Chrome at 2560 x 1440: 5.08 ticks per second, no long
  task, while walking and with 2000 ticks held; the past view; screenshots in docs/handoffs/tviz_1d/ (untracked).

## In progress

- None. Hadi's review of the build.

## Next

- Hadi's review; the polishing round (open).

## Decisions taken on the way

- ccode's design decisions and the two provisional readings: design_records.md, 1d AND 1e, THE PATHS ON THE FLOOR, BUILT.
- Recomputing the walk in hand from the agent's present position can put a step at 30.00000000000006 from the target
  instead of 30 (kitting scenario_s05_02 intention-unaware, tick 213), one step past where the body stops: the walk in
  hand is read from the body's queue. The queue runs on to the target's centre; the body stops at the `at` radius, so
  an agent within it has no walk left, whatever the queue holds.
- `pkill -f mesa_sim/run_webui.py` inside a compound command matches its own shell and ends it: stop the server alone.
- A browser look that runs a web-ui sim-run writes into logs/: never at the same time as a sweep that picks "the new
  log pair" (as in 1c).
- An untracked domains/kitting/layouts/env_layout_100.json (env_layout_00.json before) is not ccode's; left untouched.
