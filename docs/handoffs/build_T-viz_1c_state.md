# Build state: T-viz 1c, the bottom panel

The session's state file (the task of 7 October 2026: record Hadi's preferences for panel 4c; then a short plan and the
build without a pause). The plan: `docs/handoffs/plan_T-viz_1c.md`; the records: design_records.md, "T-viz, the
web-ui", 1c blocks.

## Done

- Part 1, the records (2c06aba): Hadi's items 1 to 7; TODO-189's "moving back along the ticks" taken out; the roadmap.
- B0: the four maintained sets (equal to the baselines on disk, 96 files) and dock_loading's scenario_s03_02, s05_02,
  s07_02 (800 steps), run at 2c06aba from a separate worktree, each run's log pair picked as its own new files.
- The messages (a859c55): `WorldTick.separations`, `TaskRef.identity`; the panel fixtures regenerated (only the new
  field differs). B1 equals B0, 102 files.
- The page (07bf71f): panel 4c, the past view, one colour per task.
- The tests and the plan (56c7e2c): `tests/test_tviz_plots.py` with `webui/page/test/lanes.log.test.ts`;
  `webui/page/test/lanes.test.ts`. The suite 450 passed; vitest 44; the build and type check; Chrome at 1440 wide;
  2000 ticks at the default speed; the solara-ui's light check.

## In progress

- None.

## Next

- Hadi's review of 1c; then 1d and 1e; the polishing round after 1c or after 1e (open).

## Decisions taken on the way

- The design decisions and the two provisional readings: design_records.md, 1c, THE BOTTOM PANEL, BUILT.
- `pytest -p no:logging` removes `caplog` and makes tests/kitting/test_g_build.py error: run the suite without it.
- A browser look that runs a web-ui sim-run writes into logs/: never at the same time as a sweep that picks "the new
  log pair".
