# Build state: T-viz 1b, the right panel

The session's state file (the task of 6 October 2026: record Hadi's preferences for panel 4b and stages 1d, 1e; then a
short plan and the build without a pause). The plan: `docs/handoffs/plan_T-viz_1b.md`; the records: design_records.md,
"T-viz, the web-ui", 1b blocks.

## Done

- Part 1, the records (d0db39e): the five blocks of panel 4b; stages 1d and 1e after 1c; TODO-197 answered; the
  roadmap's T-viz bullet; the handoff's state section.
- B0: the four maintained sets and dock_loading's scenario_s03_02, s05_02, s07_02 (800 steps) at d0db39e equal the
  baselines on disk (102 files). The scratch script picks the log pair its own run created: a web-ui sim-run of another
  process writing into logs/ at the same time made "the newest log" wrong once.
- The model (b69d9b6): `RobotAgent.last_decision`; B1 equals B0, 102 files.
- The messages, the piece, the page, the tests: see design_records.md, 1b, THE RIGHT PANEL, BUILT. Checks: the suite,
  vitest 38, the build and type check, one look in Chrome at 1440 wide, the solara-ui's light check.

- Hadi's review (7 October 2026) recorded and built: design_records.md, 1b, HADI'S REVIEW (the exception "gate" named
  alone; the admission's two parts "held" and "gate now", "held" tested against the decision record at every tick;
  the panel in three parts with short labels; the belief chart with fixed rows). No simulator code changed.

## In progress

- None.

## Next

- Stage 1c (plots over ticks), then 1d and 1e; the polishing round after 1c or after 1e (open).

## Decisions taken on the way

- The design decisions and the five provisional readings: design_records.md, 1b, THE RIGHT PANEL, BUILT.
- The test's gate derivation allows both answers where the logged confidence (3 decimals) lies within its rounding of
  θ: the log cannot decide such a tick (kitting scenario_s05_02 had one, tick 7).
