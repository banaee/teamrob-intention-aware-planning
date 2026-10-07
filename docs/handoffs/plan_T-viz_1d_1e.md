# Plan: T-viz 1d and 1e, the paths on the floor

ccode, 7 October 2026. Planned and built in one session without a pause (the task of 7 October 2026). Hadi's
preferences: design_records.md, "T-viz, the web-ui", 1d AND 1e, THE PATHS ON THE FLOOR, items 1 to 5. Everything below
is decided by ccode unless it says otherwise.

## 1. What is drawn, and its source in the model

| drawing | form | source (Mesa's piece reads, after each step) | message |
|---|---|---|---|
| the robot's own plan | thin dashed line, robot blue; a small mark at each walk's end | the robot's executor: `current_plan.actions` from `action_index` on, the walk actions among them (`schema.movement_target_key` set) | `RobotTick.walks_ahead` |
| the human's real path | thin dashed line, human orange; a small mark at each walk's end | the human's stack machine: the top frame's action in hand and, unless it is a cut action being finished, the frame's later actions (`Frame.actions` from `index` on), the walk actions among them | `WorldTick.walks_ahead` |
| the robot's expectation of the human | wide light orange stripe below the lines: filled for an admitted projection, hatched for the fallback; a stand a disc at its place | `RobotAgent.last_decision.projection`, the projection panel 4b's projection block shows: its segments still ahead on the decision's projection clock (step s ends world tick decision − 1 + s) | `RobotTick.projection_ahead`; its kind is `RobotTick.decision.projection.kind` |

- A walk ahead: from the agent's position (the walk in hand) or from where the walk before it stops, in a straight line
  to where the body's walk stops: the body's own `walk_positions` (its first step within the `at` radius of the target)
  toward the target's present position (the body's own `_resolve_movement_target`). So a later walk starts where the
  body will stand, not at the target's centre. A walk the body has already completed (it is within the radius) has no
  segment.
- Verified before the build: the human's later walk actions are available before the human reaches them; the frame
  holds its whole expansion from the moment it is (re-)expanded. One exception: a cut action being finished on a
  resumption (`Frame.finishing`); the task is re-expanded only after it, so only that action is known then, and only it
  is drawn (raised in the report).
- The expectation ahead at tick t: the projection's segments with an end after τ = t − decision + 1; a moving segment
  under way is cut at its position at τ (linear in step-time, the Segment's own assumption); a stationary segment with
  an end after τ is a stand; consecutive stands at one place are one. Each part carries its end on the world's clock
  (decision − 1 + end_step). Past T_h nothing lies ahead and nothing is drawn (panel 4b still says "ran out").
- Run conditions follow from the source: human-unaware, the decision rests on no projection, so no stripe;
  intention-unaware, only fallback projections occur, so only hatched stripes. The human's real path is the world's and
  is drawn in every condition.
- The view of an earlier tick: the drawings are in the tick updates, so the past view shows that tick's.

## 2. The addition to the messages (`webui/messages.py`)

- `Walk` (start, end, target: the id of the object the walk action heads for).
- `HumanWalks` (human, walks); `WorldTick.walks_ahead: tuple[HumanWalks, ...] = ()`.
- `MovingSegment` (start, end, until) and `StationarySegment` (position, until), a union `ProjectedPart` by `kind`.
- `RobotTick.walks_ahead: tuple[Walk, ...] = ()`; `RobotTick.projection_ahead: tuple[ProjectedPart, ...] = ()`.
- Every field with an empty default; the page's types regenerated (`npm run gen:types`).

## 3. The page

- `src/env-pane/paths.tsx`: one layer on the floor, under the objects and the agents (depth-tested, drawn after the
  floor's marks): the stripe (one merged mesh per robot, width the human's floor ring's diameter, drawn once per pixel
  through the stencil so its overlaps do not darken; hatched in screen space for the fallback, as the scene's shaded
  faces are), then the dashed lines and their end marks. The page builds geometry from the segments it receives and
  computes no path.
- Three switches in the env-pane's header ("robot plan", "human path", "expectation"), each a small pill with a swatch
  of its drawing; on by default; remembered in the browser.
- The canvas asks for a stencil buffer (no change of look).

## 4. Checks

- Headless byte-identical (`mesa_sim/` changes only in the piece, which only reads): the four maintained sets and
  dock_loading's scenario_s03_02, s05_02, s07_02, B0 at the records commit, B1 on the change.
- `tests/test_tviz_paths.py`, on reference sim-runs of both domains (kitting scenario_s05_02, dock_loading
  scenario_s07_07, kitting scenario_s05_02 intention-unaware, dock_loading scenario_s07_07 human-unaware, kitting
  scenario_s09_13, a cut into a walk): every walk ends where the body's walk toward its target stops (within the `at`
  radius of the target's position) and the next starts there, the first at the agent; the human's real path at a tick
  agrees with the human's positions in the run log in the following ticks while the task on top runs on (each position
  on the path, in order, the path's end reached when the task completes); the robot's likewise while its plan runs on;
  the expectation's kind and end equal the run log's for the decision it belongs to (`[meta-proj]`, `[meta-b3]`'s
  T_h), human-unaware no expectation, intention-unaware only fallbacks.
- The suite; vitest (the stripe's geometry, the switches' memory); the page's build and type check; the solara-ui's
  light check is not needed if only the piece and the page change (it does not use them).
- Play at 5 ticks per second over 2000 ticks with all three drawings on, in Chrome at 2560 x 1440; screenshots checked
  and the look refined at 2560 x 1440.
