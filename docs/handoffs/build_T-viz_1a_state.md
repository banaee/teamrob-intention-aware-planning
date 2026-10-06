# Build state: T-viz 1a, increments (ii) and (iii)

The session's state file (the task of 6 October 2026: record Hadi's review of increment (i), then build (ii) and (iii)
with no pause between them). Kept so that the work continues after a context compaction or in a new session. The plan:
`docs/handoffs/plan_T-viz_1a.md` (P17 to P24 from the review); the records: `docs/design_records.md`, "T-viz, the
web-ui", 1a blocks.

## Done

- Part 1, the records: Hadi's review of increment (i) recorded (design_records.md, 1a, HADI'S REVIEW OF INCREMENT (i));
  the plan amended (P17 to P24, increment (v)); the roadmap's T-viz bullet; the handoff's state section. Commit
  be3c200.
- B0: the 48 runs of the four maintained sets and dock_loading's scenario_s03_02, s05_02, s07_02 (800 steps), taken at
  be3c200 into the session's scratch folder; the 32 files of tb1a equal the baselines on disk.

- Increment (ii) BUILT, its checks passed (commits 5f578dc, db28f6f, 0038743, e55c066 and the readers' commit after
  it; webui_export.py's deletion landed in 0038743). Checks: B1 and B2 (after the loader's move and after the notes
  rename) equal B0, 102 files; every offered triple (1020: the 1019 and Hadi's scenario_s31_01) builds and its view
  equals its start (tests/test_tviz_view.py, 5 s); the page's offer equals P2's rule on 25 layouts, 44 pairs, 1020
  scenarios (a one-off vitest over the real catalogue against Python's offer from the registry); the view's server
  rules (test); the suite 435 passed, 1 failed (tests/test_tl2_discovery.py counts 721 kitting scenarios, the
  registry holds 722 since Hadi's 0536293: not mine, flagged); vitest 8 passed; npm build passes; the solara-ui
  serves per domain and steps; the screenshots in Chrome (docs/handoffs/tviz_1a/), the address's three cases passed.

- Increment (iii) BUILT (9e1bef1, e42bd2b): B3 equals B0; the suite 436 passed, 1 failed (the same count); vitest 15
  passed; the build; in Chrome: the reload gives the same picture as the steps before it, a free angle, the looks by
  state, the see-through table top.
- Hadi's change of mode recorded (design_records.md, 1a, THE MODE OF CHECKS; the plan's P25 and section 8), and the
  records of (ii) and (iii).

- Session of (iv), part 1 (6 October 2026): Hadi's review of (ii) and (iii) recorded (ddde9cc; P25 corrected, P26);
  the discovery test for scenario_s31_01 (0edd3dc); dock_loading's four layout notes (1fef671, B4 equals B0); the page
  logic of (ii) and (iii) tested (7e9716e: opening.ts, withOption, foldBook; vitest 23).

- Increment (iv) BUILT (8f05287 panel 4a, 795fc34 test 2): the suite 438 passed; vitest 27; the build; one look in
  Chrome (kitting scenario_s02_02, dock_loading scenario_s06_09, the unseen domain). Records: design_records.md, 1a,
  INCREMENT (iv), BUILT.

- Increment (iv), second part, COMPLETE (512a167, 33c9394, a48b1b3, e50cb81, fddcf7b, 705653e, 3cb88e5, ca6a037;
  records: design_records.md, 1a, INCREMENT (iv), SECOND PART, BUILT, with ccode's decisions): the suite 444 passed;
  vitest 32; headless byte-identical; the analyses' tags unchanged on samples of both domains.

## In progress

- None. Increment (iv) is complete.

## Next

- (v), polishing from Hadi's written list, in a new session; then the close of 1a (the solara-ui check once, the
  README's archive line, the roadmap's line).

## Decisions taken on the way

- vitest brought into (ii) (planned for (iii)): the selection rule and the address needed unit tests. Tests live in
  webui/page/test/ (outside tsconfig's include; vitest transpiles them).
- The filter: every word of the filter appears in the id or the description, in any case.
- The selection shows a layout's id and notes, not its title (the titles are stale, P20's reason).
- The page offers every layout of the domain; a layout without a scenario would offer no setup.
- A view request is refused (409 ViewRefusal) while a stepped sim-run is current; a failed view changes nothing on
  the server. A failed choice leaves no sim-run on the server (as in (i)); the page keeps its picture with the controls
  disabled ("Not built").
- The address: `?domain&layout&setup&scenario&<option>=<value>`; an undeclared option, a value not of the option's
  kind, an unknown domain, or a scenario not offered on the address's layout, is a problem the page states before
  opening the default choice; an unknown layout, setup or scenario is the server's BuildFailure.
- A refusal's message is capped at three lines (the unknown-scenario message lists every scenario of the domain).
