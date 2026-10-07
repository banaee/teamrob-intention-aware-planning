# Plan: T-viz 1c, the bottom panel (panel 4c)

ccode, 7 October 2026. Hadi's preferences: design_records.md, "T-viz, the web-ui", 1c, THE BOTTOM PANEL (items 1 to 7).
Planned briefly and built without a pause, as the task asks. Status words of the T-viz records: everything here is
"decided by ccode" unless marked otherwise.

## 1. The lanes, their content and their source

One canvas, one tick axis, the lanes in Hadi's order, a lane title in a left gutter. Every value is read from the tick
updates the page holds (`ticks`, the start's first); the page derives bands from consecutive equal values and compares
nothing with a threshold of the robot's.

| lane | content | source in the messages |
|---|---|---|
| 1 the human's task | per human a band per stretch of the task on top of the stack, in the task's colour, its text inside where it fits; the tag per task as a thin strip under the band in the tag's colour, its word in the tooltip | `world.activity[h].stack[0]`, `.tag` (a new stretch where the top's label or the tag's `since` changes) |
| 2 the robot's belief | per robot one line per hypothesis over the ticks it is live, in the task's colour; a hypothesis that has led at some tick drawn full, the others thin and light; θ dashed; the held admission as a strip at the lane's top in the held hypothesis's colour | `robots[r].belief.live`, `.leader`; `description.robots[r].theta`; held = `robots[r].decision.projection` when `admitted` (1b's "held") |
| 3 context | one row per timeline fact, a band while it holds; the lane is absent when the sim-run's timeline has no window | `world.timeline_facts`; the rows from `description.world.timeline.windows` |
| 4 the robot's task | per robot a band per stretch of its task, in the task's colour; a hold as a dark hatched strip under the band; a mark above the band at each decision | `robots[r].body.task`, `.body.hold`; a decision where `robots[r].decision.tick` equals the update's tick |
| 5 distance | per robot–human pair the continuous minimum of the tick (the analyses' figure line), min_separation dashed, the ticks below it shaded; values above 4 × min_separation drawn at the top edge | NEW: `world.separations` (below) |

Conditions: intention-unaware or human-unaware, lane 2 reads "off · <condition>" in a short row; human-unaware, the
min_separation line is labelled "not kept". A robot with no task shows an empty lane 4. No robot: lanes 2, 4, 5 absent.

Axis: from tick 0 to the next multiple of 100 ticks past the latest (fixed portions, cchat's proposal taken). The
latest tick is a vertical line through all lanes; a viewed earlier tick a second line in the "past" colour. Hover: a
crosshair and a tooltip with the tick's values, short labels.

## 2. Additions to the messages

- `TaskRef.identity`: the task's identity in the framework's sense (task equality, `same_task`: the schema and its goal
  bindings), written as a hypothesis key is written, so that it equals `Hypothesis.key` for the task a hypothesis names.
  Made on the simulator's side from `goal_bindings` and `task_instance_key`; the page keys its colours by it. Reason:
  a human's task carries a determined binding (`deliver_item(?item=item_3,?kitting_table=kitting_table_0)`) that its
  hypothesis does not (`deliver_item(?item=item_3)`); only the simulator's side knows task equality.
- `WorldTick.separations`: per robot–human pair, after a step, `distance` (sampled at the end of the tick) and
  `minimum` (the continuous minimum over the tick), the two values the `[sep]` line prints, and `below` (the minimum
  under the robot's min_separation, the analyses' count). `mesa_sim/sim_run.py` keeps the values it prints
  (`SimRun.separation`), the piece reads them; nothing is computed twice. Empty at the start.

## 3. One colour per task

The colours are fixed once per sim-run from its run description, in this order: each human's script (entries in
written order with the tasks their events start, the repeatable entries, the closing part), then each robot's own
assigned tasks, then the hypotheses in the recognizer's order. The first ten identities get the ten hues of a
categorical palette (validated with the dataviz validator, light surface, adjacent pairs: worst CVD ΔE 6.4, legal with
the secondary encoding the page has: labels in bands, the tooltip, the right panel's labels); every further identity
gets one neutral "other" grey. The script's and the robot's tasks thus always have their own hue. Used in lanes 1, 2,
4, the right panel's belief chart and the left panel's script, stack and action in hand.

## 4. The view of an earlier tick

A click on the plot pauses play and sets the page's viewed tick k. The scene, both side panels and the control bar's
note read the prefix of the tick updates up to k (the panels already read a sequence; the place book is folded over
the prefix). The control bar says "viewing tick k · sim-run at tick n" with a button back to the latest. Play or step
first returns to the latest tick, then goes on. No request goes to the server; reset or a new choice clears the view.

## 5. Tests

- Python, `tests/test_tviz_plots.py`: on kitting scenario_s05_02 and scenario_s10_14, dock_loading scenario_s07_07,
  kitting scenario_s05_02 intention-unaware, dock_loading scenario_s07_07 human-unaware: `separations` equal the
  `[sep]` lines at every tick and `below` equals the analyses' count; `identity` equals the key of the hypothesis that
  names the human's task (task equality) wherever one does. Then each sim-run's tick updates and the values its log
  states (the `[rec]` stack top, the tag reader, `[IR]` and `[IR-rank]`, `[meta-trig]`, `[meta-proj]`, `[meta]`,
  `[hold]`, the step lines, the timeline line, `[sep]`) are written to a temporary folder, and the page's own lane
  reading runs on them under vitest (`test/lanes.log.test.ts`): every lane's value at every tick equals the log's.
- vitest: the lanes folded one tick at a time equal the lanes folded at once; the bands; the colours; the view of tick
  k (the prefix and the place book) equals what the page held when the sim-run was at tick k.
- Headless byte-identical (`mesa_sim/sim_run.py` and the piece change): the four maintained sets and dock_loading's
  three milestone runs against the baselines on disk.
- The suite; the page's build and type check; one look in Chrome at 1440 px (a timeline fact, a hold, ticks below
  min_separation, human-unaware), with a click in the past and the log pair's checksums before and after; play of a
  2000-tick sim-run at the default speed; the solara-ui's light check (sim_run.py is used by it).
