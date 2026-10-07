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

- Hadi's review of 1c recorded (0942d69); the two versions of panel 4c built (19d62e1): A the page's own canvas, B the
  ReUI look on Recharts; the A/B switch at the panel's foot; screenshots in docs/handoffs/tviz_1c/ (untracked).

- Hadi chose version A (b85616c, recorded; a choice of B given before it was withdrawn): built (a6f79c8): S and the
  finding under the belief, one tint, header columns, a legend, no grid, the soft colours across the page, panel 4a in
  cards, three dragged borders; screenshot docs/handoffs/tviz_1c/page_2560x1440_kitting_s05_02_tick120.png. The look is
  judged at 2560 x 1440 (Hadi), usable at 1920 x 1080.

## In progress

- None. Hadi's review of the build.

## Next

- Hadi's review; then 1d and 1e; the polishing round (open).

## Decisions taken on the way

- The design decisions and the two provisional readings: design_records.md, 1c, THE BOTTOM PANEL, BUILT.
- `pytest -p no:logging` removes `caplog` and makes tests/kitting/test_g_build.py error: run the suite without it.
- A browser look that runs a web-ui sim-run writes into logs/: never at the same time as a sweep that picks "the new
  log pair".
- ECharts and visx were started and removed on Hadi's word; Motion was tried and removed (slower steps at 2000 ticks).
- In Chrome, an SVG filter on a Recharts area, and Recharts' own animation across a gap, each leave a stale curve.
- A canvas redrawn each tick with many-segment lines stalls Chrome's GPU rasteriser (seen in headless Chrome with software
  GL): `getContext("2d", { willReadFrequently: true })` draws it on the CPU, without stalls.
- The scan for domain words reads comments too: "item" (a kitting object type) cannot be written in the page, not even
  "item 9" of a ruling; write "point 9".
- An untracked domains/kitting/layouts/env_layout_00.json appeared during the session (not ccode's); left untouched.
