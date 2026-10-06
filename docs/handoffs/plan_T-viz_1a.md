# Plan: T-viz stage 1a, the first sim-run in the browser

Written by ccode, 6 October 2026, for Hadi's review before any code of stage 1a is written. Every item is proposed by
ccode and open until Hadi says "I prefer" (the status words of `docs/handoffs/handoff_T-viz.md`, 1.1). Hadi's
preferences for 1a of 6 October 2026 (P1 to P6 below) are recorded in `docs/design_records.md`, "T-viz, the web-ui",
1a, HADI'S PREFERENCES. What 1a starts from: the handoff's section "State after stage 0".

Every build session of 1a reads this file first, then the handoff's "State after stage 0". One increment per session;
ccode pauses after each increment for Hadi's review in the browser.

---

## 0. Hadi's preferences this plan follows (6 October 2026)

- P1. One plan for the whole of 1a, built in increments, a pause after each for Hadi's review.
- P2. The order of the selection: domain, layout, setup, scenario. The setups offered for a layout X are those with at
  least one scenario that has X among its reference layouts; the scenarios offered are the chosen setup's scenarios
  with that layout among their reference layouts. Proposed by cchat, not marked by Hadi: the page offers only these
  combinations; a sim-run on a layout outside a scenario's reference layouts stays possible headless.
- P3. With a layout chosen and the triple not complete, the env-pane shows the layout alone (space, areas, fixed
  objects, no model). Every change that completes a triple builds the model. The layout's picture is read through
  the same loader as the model's.
- P4. The scenario list shows each scenario's description beside its id, with a plain text filter over both. The
  structured filter by composition (TODO-110) is stage 2, [FW].
- P5. Panel 4a: the action in hand with its progress and its task; the human executor's stack; the last few switches
  and resumptions with their ticks. Hadi adjusts it after he sees it.
- P6. One command per start. The web-ui's start command is a file in `mesa_sim/` that accepts the same run file and
  flags as the headless start. `webui/` stays at the root and imports no simulator. TODO-196 is answered for now.

---

## 1. Facts verified for this plan (ccode, 6 October 2026, at e5de942)

F1. Every one of the 1019 scenarios names exactly one reference layout (721 of 721 in kitting, 298 of 298 in
dock_loading). Under P2 the page offers exactly 1019 triples, one per scenario. The order domain, layout, setup,
scenario is a way through the catalogue, not a product of choices.

F2. Scenarios per pair of layout and setup (the length of the scenario list; layout and setup by their serials):

| domain | pairs | scenarios per pair | setups per layout |
|---|---|---|---|
| kitting | 33 | 1 to 52, median 21 | 1 to 3 |
| dock_loading | 10 | 7 to 58, median 19 | 1 to 3 |

kitting: 01: 01:5. 02: 02:3, 17:40, 18:30. 03: 03:5. 04: 01:3. 05: 04:3, 19:34, 20:30. 06: 03:4, 21:31, 22:26.
07: 05:4, 23:36, 24:30. 08: 06:6. 09: 07:5. 10: 08:4. 11: 09:13. 12: 10:24, 11:6. 13: 10:1. 14: 12:5. 15: 13:15.
16: 14:21. 17: 15:21. 18: 16:11. 19: 25:52, 26:52, 27:49. 20: 28:50, 29:51, 30:51.
dock_loading: 02: 02:19, 03:7, 10:58. 03: 04:19, 05:16, 08:58. 04: 06:19, 07:16, 09:58. 05: 11:28.

Three setups are offered under two layouts each (kitting env_setup_01 under 01 and 04, env_setup_03 under 03 and 06,
env_setup_10 under 12 and 13). No layout is without a scenario. The lists are short: 20 layouts at most, 3 setups, 58
scenarios. A plain filter suffices; no paging.

F3. Descriptions. Every scenario has one (107 to 2273 characters, median 588 in kitting; 186 to 984, median 202 in
dock_loading). Layouts and setups have no description field. They carry free-text notes that nothing reads:
- layouts: `space.notes` in 19 of kitting's 20 (env_layout_02 has none); dock_loading's four write `space.note`
  (singular), the same kind of text under another key;
- setups: a top-level `notes` in kitting's env_setup_17 to _30 (14 of 30) and in all 10 of dock_loading's.
The notes say what a room or a shift is for (for example "The IRB's enlarged room ..."), 81 to 1749 characters. The
layout's `space.name` (the catalogue's title) is stale in older layouts (open item 12).

F4. The loader. `SimModel.__init__` reads the layout inline: the space and its title, the areas, and the fixed
objects in the first pass of `_init_objects` with its checks (`mesa_sim/sim_model.py`, 175 to 212 and 316 to 353).
No function reads a layout alone today. P3's condition therefore needs that part moved into one function that
`SimModel` calls and the web-ui's piece calls. This is the one addition to cchat's estimate of P3's cost; it is a
change of `mesa_sim/` with no change of behaviour, checked by byte-identity (section 8).

F5. Agents have no size in the model: they are points (`agent.pos`); `min_separation` (50) is a distance between
positions, read by the mind and the separation stop. An area's `label` is in 22 of the 24 registered layouts (not in
kitting's env_layout_08 and _19); the model does not read it; only the paused `ros_sim/` does.

F6. The server's libraries are installed already: Starlette 0.48.0 (pinned in `requirements.txt` for Solara) and
uvicorn 0.30.5 (installed with Solara, not pinned). FastAPI and httpx are not installed. Node.js 22.13.1; Chrome for
the screenshots through playwright-core, as in 0.3.

F7. Sizes. A tick update is 1.0 to 1.8 KB as JSON (mean 1.3 KB over scenario_s02_01's 450 ticks, 1.0 KB over
scenario_s08_01's 400); a run description 4 to 5 KB. A sim-run of 2000 ticks holds about 2.6 MB of tick updates.

F8. The glossary terms of panel 4a. With an entry: **stack** (top first), **record**, **outcome** (completed,
suspended, abandoned, infeasible), **event trigger**, **decision**, **open entry**. Without an entry of their own:
"action in hand" (the record's `Snapshot` and the message `ActionInHand` use it; the entry **record** says "the action
and its progress"), "switch" and "resumption" (named in the entry **record** as its queries `switches`, every applied
`Start`, and `resumptions`, every `Resumed`), "progress". The panel uses them in those meanings. Whether they get
entries is Hadi's.

---

## 2. The increments

Four increments, each ending with a pause for Hadi's review. They follow cchat's proposal with two changes, each with
its reason:
- The page layout moves from (iv) to (i): the whole frame of the page (header, selection panel, env-pane with its
  control bar, the places of 4a, 4b and 4c) is built first, empty where later increments fill it. Reason: Hadi
  reviews the page layout while it is cheap to change, and the later increments fill places instead of moving them.
- Test 1 (a sim-run through the server writes the same log pair as headless) moves to (i). Reason: the server writes
  log pairs from (i) on; a fault there must be found before anything is built on it.

### (i) The server, the start, the page's frame, a minimal choice, the moving env-pane

Scope:
- `webui/server.py` (new): the web-ui's server: the rules (which sim-run is current, the end at the configured steps,
  the lock after the first step, the refusals) and the requests of 0.4 over HTTP (section 4, item 5). It imports no
  simulator: it takes a `Simulator` (webui/simulator.py).
- `mesa_sim/run_webui.py` (new): the web-ui's start (P6, section 4 item 6): the run file and the flags read by
  `run_config` as the headless start reads them, Mesa's piece built on them, the server started.
- `mesa_sim/sim_run.py`: the log pair of a web-ui sim-run takes only its own thread's lines and does not echo to the
  terminal (section 4, item 9). Headless and the solara-ui unchanged.
- `mesa_sim/webui_adapter.py`: the catalogue carries each domain's scene appearance (section 4, item 1); the default
  choice comes from the start's run file and flags.
- The page: the frame of section 5; a minimal choice (domain, and the scenario from one list, on its reference
  layout; the run options at the start's values, shown, not yet changeable); the control bar (play, pause, step,
  reset, the speed, the tick); the env-pane reading the server's messages, the agents moving, turning to their last
  motion, movable objects carried and placed by 0.3's rule.
- `README.md`: the web-ui's start, beside the other starts.

What Hadi sees: one command; the browser opens the page on the run file's sim-run at its start; play, and the human
and the robot walk, pick up and place; pause, step, reset; another scenario chosen, and its start shown at once.

Checks: test 1 in both domains, and the thread filter's test (section 7); headless byte-identical (section 8); the
solara-ui still serves and steps; the screenshots (section 8).

### (ii) The full selection, all run options, lock and unlock

Scope:
- The loader's layout part moved into one function that `SimModel` and the piece both call (F4); the view of a layout
  (and of a layout with a setup, if Hadi prefers Q1 (b)) produced from it (section 3, M2).
- The selection panel: domain, layouts, setups, scenarios as P2 states; the layout alone shown on choosing a layout
  (P3); the notes of layouts and setups, the scenarios' descriptions and the text filter (P4).
- All run options, each by its declared kind (switch, one of, level, count), the value stated and the value in
  effect side by side: an option that another sets off shows "off in effect". The page holds no rule between them;
  the run description's `effective` tells it.
- Lock and unlock: every change that completes a triple, or changes an option, builds the model and shows its start;
  the first step locks the choices; reset unlocks them. A choice that cannot be built shows its `BuildFailure` and
  the page stays on the view it had.
- The page's choice mirrored in the address, so a reload or a copied link reopens it.

What Hadi sees: kitting's twenty rooms, one after another, each drawn alone; a room's setups; a setup's scenarios with
their descriptions, filtered by a word; a scenario's start; an option switched, and the options it sets off marked.

Checks: every offered triple builds (all 1019, about 3 ms each); the offered setups and scenarios equal P2's rule for
every layout; the view of a layout equals the layout part of the run description of every scenario on it (P3's
condition, all 1019); headless byte-identical after the loader's move; the solara-ui still serves and steps;
screenshots.

### (iii) The env-pane additions

Scope:
- The free camera beside the two presets (section 4, item 3).
- An object's state changing its look (section 4, item 2): the appearance data's states, dock_loading's empty pallet
  and open gate as the first two.
- Display places kept while an object stays, freed places and too many objects (section 4, item 10).
- `current` returns every tick update of the sim-run (section 3, M3): a reload keeps the picture.
- Page-side unit tests (vitest, pinned) for the display places and the choice of a look by state.

What Hadi sees: the camera turned, tilted, zoomed and moved during play, and the presets bringing it back; pallets
emptied in dock_loading drawn as empty skids; a container whose objects leave one by one, the others staying in their
places; a reload in the middle of a sim-run showing the same picture.

Checks: the unit tests; a screenshot before and after a reload, equal; screenshots of both domains, both presets and
one free angle.

### (iv) Panel 4a, test 2, the close of 1a

Scope:
- Panel 4a (section 4, item 8; P5).
- Test 2 (section 7).
- The page's README, the README's starts, and the records of 1a's build.

What Hadi sees: the whole page of 1a; the human's activity changing as the human works, is interrupted (a coffee
break started by an event) and resumes.

Checks: test 2; the domain-word scan of `webui/` and the page; screenshots of both domains, every page state. Then
Hadi's acceptance of 1a, from which the solara-ui is archived (the README and the roadmap say so).

---

## 3. The message round of 1a

What 1a adds to the messages of 0.4. Nothing of 0.4 changes except M3.

M1. The catalogue.
- `DomainEntry.appearance`: the domain's scene appearance, read by the piece from `domains/<domain>/appearance.json`,
  the defaults when there is none (section 4, item 1).
- `LayoutEntry.notes` and `SetupEntry.notes`, optional text: the notes of the layout and the setup files (F3), shown
  in the selection. Reason: P4's reason (Hadi cannot choose from an id alone) holds for rooms and shifts too.

M2. The view of a layout (P3), a new message: the domain, the layout's id, the space, the areas, the fixed objects,
with the field types of the run description (`Space`, `Area`, `FixedObject`), produced from the same function that
the model's loader calls (F4). If Hadi prefers Q1 (b): also the setup's id, its movable objects in their home
containers in the setup's order, and the object states that hold at the setup's start; produced from the setup's part
of the same loader, which then also moves into a function. A view has no sim-run and no tick.

M3. The requests. Two changes to 0.4's list:
- `view` (new): the view of a layout, or of a layout and setup; an unstepped current sim-run is discarded (no file);
  refused while a stepped sim-run is current (the choices are locked).
- `current` returns the run description and every tick update of the current sim-run, in order, instead of the latest
  only; or the current view; or nothing. Reason: the page derives the display places (section 4, item 10), panel 4a's
  last switches and resumptions, and in 1c the plots from the sequence of tick updates; with the whole sequence, a
  reload gives the same picture (section 9's requirement 3). Size: F7.

M4. The scene appearance: per object type, optional looks by state (section 4, item 2).

M5. Open item 11, proposed:
- Agents get no size in the messages. The model has none (F5); a figure's size is the appearance's. Whether the
  scene shows `min_separation` around the robot is a question of the robot's side, for 1b.
- Areas keep their id as their label, as Hadi prefers for labels; the layout's `label` is not carried in 1a. It
  returns with inspecting an object during a pause (TODO-189), where a detail of the room has its place.

M6. No change: the tick update carries the transitions of its own tick only; the history comes from M3.

---

## 4. Proposals on the open items of "State after stage 0"

Items 4, 6 and 8 are answered by Hadi's preferences P6, P2 to P4 and P5; the plan states how they are built.

### Item 1: how the scene appearance reaches the page

The catalogue's per-domain entry carries it (M1), read by Mesa's piece from `domains/<domain>/appearance.json`. The
page has it before any model exists, so a layout's view (P3) is drawn in its look. Every state a domain's appearance
names (item 2) is checked by the piece against the domain's declared states when the catalogue is built: a misspelt
state stops the start with a message, instead of being silently never drawn. A small change of form:
`webui/appearance.py` imports `webui/messages.py` for its base class, so for the catalogue to name `Appearance` the
base class moves to a module of its own; no message changes by it.

### Item 2: an object's state changes its shape (TODO-194)

The appearance data gives an object type, beside its look, an ordered list of looks by state:

```json
"pallet": {"shape": "loaded_skid", "height": 40,
           "states": [{"state": "is_empty", "look": {"shape": "skid", "height": 14}}]},
"gate":   {"shape": "barrier", "height": 130, "presence": "background",
           "states": [{"state": "is_open", "look": {"shape": "barrier", "height": 8, "presence": "background"}}]}
```

When a listed state holds for the object at the tick (the tick update's `object_states`), its look replaces the
type's; when several hold, the first in the list. A look by state is a look of the same vocabulary, so the page's code
gains no domain word: it compares the state names of two pieces of data, as it already compares object types. One new
form, `loaded_skid` (a skid with a closed load on it), so that a full pallet differs from an empty one; the open gate
needs no new form (a barrier drawn low). In all ten of dock_loading's setups the gate is open from the start
(`is_open`; opening it on request is T-G's stage 2), so in stage 1 it is always drawn open. kitting's A/C switch
(`ac_on`) and dock_loading's `is_scanned` get no look in 1a; their data entries can be added at any time without code.

### Item 3: the free camera (TODO-195)

drei's orbit controls on the orthographic camera, with the two presets kept as the segmented control in the
env-pane's header:
- drag: turn around the room's centre; drag up and down: tilt, from straight down to 10° above the floor; right drag
  or shift and drag: move; wheel: zoom, bounded between the whole room and about one object;
- a preset button puts the camera back in that pose, framed on the room; while the camera is moved neither preset
  shows pressed;
- the camera is the screen-user's own: it changes nothing in the sim-run, is written nowhere, stays through the ticks,
  a reset and a change of scenario on the same layout, and returns to the last preset when the layout changes.

### Item 5: the server's library and its transport

- Starlette with uvicorn, both installed (F6), pinned in `requirements.txt` under a block for the web-ui. Not
  FastAPI: it adds a dependency for automatic validation and documentation that six requests do not need; pydantic
  reads each body (`model_validate_json`) and writes each answer (`model_dump_json`). Starlette also serves the page.
- Plain request and response over HTTP, JSON, on 127.0.0.1 only (one screen-user on one machine, no login). Answers
  over 1 KB compressed (gzip; the catalogue's 645 KB becomes about 40 KB). The page from `webui/page/dist` at `/`, the
  requests under `/api/`: `GET catalogue`, `POST view`, `POST choose`, `POST step`, `POST reset`, `GET current`. A
  `BuildFailure` answers with status 422, a `StepRefusal` with 409, each with its message as the body.
- Every call into the simulator's side (build, step, end, discard) runs on one worker thread of the server; a second
  step while one runs is refused (`busy`). At the server's stop a stepped current sim-run is ended with
  `server_stopped`.
- No WebSocket in 1a: the server sends nothing unasked (the page requests each step).
- During the page's development, Vite's dev server passes `/api/` to a running server.

### Item 6: the start command (P6, TODO-196)

```bash
PYTHONHASHSEED=0 ~/python-envs/ir-nomesa-env/bin/python mesa_sim/run_webui.py [--run <file>] [flags] [--port 8000]
```

- The flags are the headless start's (`run_config`'s parser, as strict), plus `--port`. The run file and the flags
  give the catalogue's default choice; the page opens on it (Q3).
- A start whose run file or flags state an override, or a layout outside the scenario's reference layouts, stops with
  a message naming it: neither can be shown in the page's choice (0.4's Q8; P2), and a sim-run the page cannot show
  would not be repeatable from it. Both stay possible headless.
- The page is served built. The start stops, naming the command `cd webui/page && npm ci && npm run build`, when
  `webui/page/dist` is missing or older than the page's sources. Node.js is needed only to build the page.
- The README carries the `PYTHONHASHSEED=0` prefix as for headless: a sim-run in the web-ui equals the headless one
  only under the same hash seed (TODO-42).

### Item 7: the page layout

Section 5.

### Item 8: panel 4a (P5)

Per human, under a header with the human's id and its colour:
- The action in hand: the action and its bindings (for example `pick_up(item_3, shelf_2)`), its progress as a bar and
  "12 of 20 ticks", and the task it belongs to, the top of the stack, by its label.
- The stack, top first: the top as the task in progress; below it the suspended task, if any (the stack is one level
  deep in T-H), marked suspended. An empty stack reads "no task".
- The last switches and resumptions, newest first, five at most, each with its tick: a switch as the started task and
  where it cut the task below it (after an action, or inside one), a resumption as the resumed task. From the `Started`
  and `Resumed` transitions of the tick updates the page holds (M3).
- Not shown in 1a, available in the messages for Hadi's adjustment: the open entries of the script, the other
  transitions (entered, left with its outcome, refused, unfired), the script itself.

### Item 9: third-party log lines kept out of a sim-run's log

Two parts, both in `mesa_sim/sim_run.py`, both off for headless and the solara-ui:
- The thread. The server runs every call into the simulator's side on one worker thread (item 5); a web-ui sim-run's
  log pair takes only the lines logged on the thread that built it. A web server's lines are logged on its own threads
  and never reach a sim-run's log, whatever library writes them and at whatever level. This holds without naming any
  logger. Headless logs everything on one thread and is unchanged.
- The echo. A web-ui sim-run's lines are not echoed to the terminal (the per-step lines would flood it); the terminal
  shows the server's own lines: its address, each sim-run's start and end, the refusals.
`webui/simulator.py` gains the contract that the server makes every call into a simulator's side on one thread.

### Item 10: freed display places and too many objects

- Each fixed object has one grid of places over its footprint, fixed for the sim-run: the most places that hold the
  run's largest movable object at its own size with 0.3's gap, numbered row by row from the north-west.
- An arriving object takes the lowest-numbered free place, and keeps it while it stays (section 9's requirement 2). A
  freed place is taken by the next arrival. At the start the setup's order fills the places from the first.
- More objects than places: the next ones are drawn on a second layer, on the places from the first, then a third.
  Objects never overlap side by side, and no object moves when another arrives or leaves.
- Determined by the sequence of tick updates (the order of arrival per tick), so the same sim-run always gives the
  same picture, a reload included (M3).
- What changes from the trial: a fixed object that is not full shows its objects from its north-west corner, not
  centred.

---

## 5. The page layout of stage 1

Designed for the whole of stage 1; 1a fills the selection, the env-pane and panel 4a, and gives 4b and 4c their
places. Hadi's suggestion (handoff, 11.1) is kept in its arrangement: the selection on top, page-wide; the human and
the world on the left, the env-pane in the middle, the robot's mind on the right; the plots page-wide below. Laid out
for a laptop screen (1440 x 900) and up.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ TeamRob web-ui    kitting / env_layout_02 / env_setup_02 / scenario_s02_01   ⊘ locked   [▾ Selection] │ header
├──────────────────────────────────────────────────────────────────────────────────────────────┤
│ Domain     │ Layout            │ Setup           │ Scenario  [filter...]   12 of 40 │ Run options     │ selection
│ ◉ kitting  │ env_layout_01     │ env_setup_02    │ scenario_s02_01                  │ human_aware   ● │ panel,
│ ○ dock_lo… │ ▸env_layout_02    │   notes…        │   description, two lines…        │ intention_a.. ● │ open before
│            │   notes…          │ env_setup_17    │ scenario_s02_02                  │ strategy  [..]  │ the first
│            │ env_layout_03 …   │ env_setup_18    │   …                              │ steps    [450]  │ step
├──────────────┬───────────────────────────────────────────────────────────────┬───────────────┤
│ The human    │ Kitting Domain Layout 1                   [Tilted|From above]  │ The robot's   │
│ ● human_0    │                                                               │ mind          │
│ action in    │                                                               │ (stage 1b)    │
│ hand …       │                        the scene                              │               │ main row
│ ███████░ 12  │                                                               │ folded to a   │
│ stack …      │                                                               │ rail in 1a    │
│ switches …   ├───────────────────────────────────────────────────────────────┤               │
│              │ ⟲ Reset  ⏭ Step  ▶ Play   5 ticks/s ▾   tick 211 · 212 of 450 steps ▬▬▬▬░░░  │               │ control bar
├──────────────┴───────────────────────────────────────────────────────────────┴───────────────┤
│ Plots over ticks (stage 1c) · folded in 1a                                                   │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
```

- The header: one line, the choice as a path in the mono type, a lock mark when locked, and a button that opens and
  closes the selection panel.
- The selection panel: five columns, in P2's order and then the run options, each column a short list. A layout and a
  setup show their notes in two lines; a scenario its description in two lines, the whole of it when chosen; the
  filter field and the count over the scenario column. It is open before the first step, folds at the first step to
  give the env-pane the height (cchat's observation, handoff 11.2), and opens again by the header's button, read only
  while locked. About 240 pixels high when open.
- The main row: panel 4a 300 pixels wide, the env-pane the rest, panel 4b 300 pixels. In 1a, 4b is folded to a narrow
  rail with its title, so the env-pane gets its width; in 1b it unfolds. Below 1200 pixels of width, 4a also folds to
  a rail.
- The control bar: at the foot of the env-pane, because it acts on what the env-pane shows; the plots of 1c, below
  it, share its tick axis. Reset, step, play and pause (one button), the speed in ticks per second (1, 2, 5, 10, 20,
  as fast as the server answers), and the tick as the run log numbers it, beside the steps done of the configured
  steps, with a bar. Before the first step the tick reads "start". The tick's number is the one a log line or a
  figure carries, so a moment seen in the page is found in the log.
- During play the agents move smoothly between two ticks' positions over the tick's display time; paused, or after a
  step, the scene shows exactly the tick's positions.
- Panel 4c: page-wide under the main row, folded to a strip with its title in 1a.
- The look: the theme file of 0.3 (`webui/page/src/theme.ts`) for every panel and the scene: the near-white ground,
  thin lines, the robot's blue and the human's orange used for their agent everywhere on the page (panel 4a's header
  dot and bar in the human's colour), the mono type for ids and numbers, no UI kit.

The page's states, and what changes them:

```
nothing chosen ──layout──▶ layout view ──setup──▶ layout and setup view ──scenario──▶ start (unlocked)
      ▲                         ▲  (any change of layout, setup or scenario goes to its view;   │  ▲
      └──domain─────────────────┘   an option or a scenario change rebuilds the start)          │  │ reset
                                                                                    first step ▼  │
                                                     ended (locked) ◀──configured steps── playing / paused (locked)
                                                           └──────────────────reset──────────────────┘
```

---

## 6. What the env-pane shows with a layout and a setup and no scenario

Proposed (Q1 (b)): the layout with the setup's movable objects in their home containers, at their display places, and
the setup's object states at its start (an empty pallet drawn empty); no agents, no tick, the control bar disabled.
Reason: Hadi compares rooms first, then a room's setups; what distinguishes two setups of one room is exactly which
objects lie where, which the layout alone does not show. Cost: the setup's part of the loader (the second pass of
`_init_objects` and `_init_states`) moves into a function too, as the layout's part does (F4), and the view message
carries it (M2); about as much again as the layout's part. Q1 (a), the layout alone as P3 states, costs nothing more.

---

## 7. The two tests, and the same log pair

Test 1: a sim-run through the server gives the same result and the same logs as the headless start.
- For scenario_s01_01 (kitting) and scenario_s03_02 (dock_loading), the run options of the run file, each to its
  configured steps: the server started as its own process by `mesa_sim/run_webui.py`, driven over HTTP (choose, then
  step until the end, with the standard library's HTTP client), and its log pair compared byte for byte with the pair
  of the headless start of the same run file and flags. Both write the start line, the override lines (none), the
  model's lines, the per-step lines, `[sep]`, the end (`end_run`) and the end line, through the same `SimRun`.
- A sim-run reset at tick k equals the headless start of k steps except the `steps=` field of the start line (the
  configured steps against k).
- The thread filter: a line logged on another thread while a web-ui sim-run is attached stays out of its pair; the
  same line on the sim-run's thread goes in.
How the same log pair is reached: the server builds and steps through Mesa's piece, which builds and steps the same
`SimRun` as the headless start; the server only decides when to step and when to end; the thread filter takes nothing
the sim-run writes, since it writes everything on its own thread; the piece only reads the model (0.4's check 3).

Test 2: a domain the web-ui has never seen is drawn without a change to the web-ui's code.
- The server started with one more domain in the registry, under a new name, with dock_loading's content and no
  appearance file: the catalogue lists it, a sim-run of it builds and steps through the server, and in Chrome the page
  draws it from the default appearance with no error on the console (a screenshot).
- With the existing scan (no domain name, object type or area id of any registered layout or setup in `webui/` or in
  the page's files), this shows that the code names no domain and that a domain without its own look is drawn.

---

## 8. Checks in every increment

- Headless byte-identical where `mesa_sim/` changes ((i): `sim_run.py`; (ii): the loader's move): the four maintained
  sets (48 logs and their `.rec`) and dock_loading's scenario_s03_02, s05_02, s07_02, rerun into a scratch folder and
  compared with the baselines, as in 0.2 and 0.4.
- The test suite (418 passed at the close of stage 0).
- The solara-ui kept working until Hadi accepts 1a: `solara run` serves per domain and a sim-run steps, as 0.2's
  check 3.
- `npm run build` and the type check pass; the page's types regenerated from `webui/schema.py` when a message changes.
- Screenshots in Chrome (playwright-core, as 0.3's `npm run shots`, extended to drive the running server), both
  domains, at 1440 x 900 and 1920 x 1080: each increment's states (a layout view, a start, a moment of play, an end;
  both presets, a free angle from (iii) on), saved to `docs/handoffs/tviz_1a/`, git-ignored as 0.3's `tviz_trial/`
  (one line added to `.gitignore` in (i)).
- `webui/` imports no simulator, and neither it nor the page names a domain, an object type or an area id (the tests
  of stage 0, extended to the new files).

---

## 9. Outside 1a: flagged, not done

- dock_loading's layouts write `space.note`, kitting's `space.notes` (F3; Q2).
- The stale layout titles (open item 12): the selection shows the id first and the title beside it.
- The run file's default of 50 steps: most scenarios need more (scenario_s02_01 about 450); the page opens with the
  run file's steps, and the screen-user sets them. A run's step count derived per scenario (docs/assumptions.md 1.3,
  TODO-138) is not 1a's.
- The run-level lines say "headless" for the web-ui too (TODO-191), unchanged until the next regeneration.
- `analysis/instruments/mpb/actual.py` keeps its own copy of reading and ending (flagged in 0.2), untouched.
- Saving the page's choice as a run file stays unassigned (TODO-189); the address of the page (ii) is not a run file.

---

## 10. Questions to Hadi

Q1. With a layout and a setup chosen and no scenario yet, what does the env-pane show?
- (a) The layout alone, as P3 states.
- (b) The layout with the setup's movable objects in their places and its starting object states, no agents.
  Recommended: it shows what distinguishes two setups of one room, at about twice P3's cost (section 6).

Q2. dock_loading's four layouts write their notes under `space.note`, kitting's under `space.notes`. Which?
- (a) The key in dock_loading's four layout files renamed to `notes`, in increment (ii); nothing reads it, no run
  changes. Recommended.
- (b) The piece reads either key.
- (c) No notes shown for dock_loading's rooms.

Q3. Started without a run file, what does the page open on?
- (a) The default run file's sim-run (`configs/experiment.yaml`: kitting, scenario_s01_01) at its start, as the
  headless start runs it. Recommended: one rule for every start, and the page is never empty.
- (b) Nothing chosen: the domains only, until the screen-user chooses.
