# Plan: T-viz stage 1a, the first sim-run in the browser

Written by ccode, 6 October 2026, for Hadi's review before any code of stage 1a is written; amended the same day by
Hadi's answers on it (P7 to P16 below). An item marked "preferred" is Hadi's; every other item is proposed by ccode and
open until Hadi says "I prefer" (the status words of `docs/handoffs/handoff_T-viz.md`, 1.1). Hadi reviews each
proposal at the pause after its increment. Hadi's preferences are recorded in `docs/design_records.md`, "T-viz, the
web-ui", 1a, HADI'S PREFERENCES and 1a, HADI'S ANSWERS ON THE PLAN. What 1a starts from: the handoff's section "State
after stage 0".

Every build session of 1a reads this file first, then the handoff's "State after stage 0". One increment per session;
ccode pauses after each increment for Hadi's review in the browser. AMENDED (Hadi, 6 October 2026, preferred, P24):
increments (ii) and (iii) are built in one session with no pause between them; then one pause; (iv) and (v) each in a
session of its own.

Progress: increment (iv) BUILT without the close (ccode, 6 October 2026; design_records.md, 1a, INCREMENT (iv), BUILT);
Hadi's review open; then (v), then the close of 1a. Increments (ii) and (iii) BUILT (ccode, 6 October 2026; design_records.md, 1a, INCREMENTS (ii) AND (iii),
BUILT); Hadi's review of them open. Increment (i) BUILT (ccode, 6 October 2026; design_records.md, "T-viz, the web-ui", 1a, INCREMENT (i),
BUILT, with its checks and its deviations from this plan); Hadi's review of it done (6 October 2026; design_records.md,
"T-viz, the web-ui", 1a, HADI'S REVIEW OF INCREMENT (i); P17 to P24 below). Increments (ii) to (v) not started.

---

## 0. Hadi's preferences this plan follows (6 October 2026)

Given with the task of the plan:

- P1. One plan for the whole of 1a, built in increments, a pause after each for Hadi's review.
- P2. The order of the selection: domain, layout, setup, scenario. The setups offered for a layout X are those with at
  least one scenario that has X among its reference layouts; the scenarios offered are the chosen setup's scenarios
  with that layout among their reference layouts. Proposed by cchat, not marked by Hadi: the page offers only these
  combinations; a sim-run on a layout outside a scenario's reference layouts stays possible headless.
- P3. With a layout chosen and the triple not complete, the env-pane shows the layout without a model (P7 adds the
  setup). Every change that completes a triple builds the model. The picture is read through the same loader as the
  model's.
- P4. The scenario list shows each scenario's description beside its id, with a plain text filter over both. The
  structured filter by composition (TODO-110) is stage 2, [FW].
- P5. Panel 4a: the action in hand with its progress and its task; the human executor's stack; the last few switches
  and resumptions with their ticks. Hadi adjusts it after he sees it.
- P6. One command per start. The web-ui's start command is a file in `mesa_sim/` that accepts the same run file and
  flags as the headless start. `webui/` stays at the root and imports no simulator. TODO-196 is answered for now.

Given as answers on the plan:

- P7 (Q1 (b)). With a layout and a setup chosen and no scenario, the env-pane shows the layout with the setup's movable
  objects in their home containers and the setup's object states, no agents (section 6).
- P8 (Q2 (a)). The key `space.note` of dock_loading's four layout files is renamed `notes`, in increment (ii).
- P9 (Q3 (a)). Started without a run file, the page opens on the default run file's sim-run at its start.
- P10. The page's choice is mirrored in the address, with one rule: the server's state wins (section 5, "The address").
  Reasons: a bookmark per scenario for a demonstration; a link that can be embedded in web-based slides, a later task
  Hadi will open. Limits: the link is not a run file (TODO-189); it reopens a choice at its start, not at a tick; one
  server holds one current sim-run (TODO-187).
- P11. The web-ui has no step limit by default; this changes 0.4's "a sim-run in the web-ui ends at the configured
  steps". Reason: a stopping point is needed for headless, not for a screen-user who can stop. Proposed by cchat and
  worked out here (section 4, item 11): the web-ui does not use the run file's `steps`; a limit applies only with
  `--steps` at the start or a number entered in the page; without one a sim-run ends by reset, by a change of choice
  or at the server's stop.
- P12. Play pauses by itself at the tick where the human's script has ended and the robot's pool is empty (the point
  MPB-5 names), and the page states that all agents have finished. The sim-run is not ended; step and play go on. A
  sim-run that never reaches the point is not paused (section 4, item 12).
- P13. The run options stay as set when the layout, the setup or the scenario changes.
- P14. Panel 4a's words "action in hand", "progress", "switch" and "resumption" have glossary entries (§6) describing
  the existing use; "suspended" stays the word for the task below the top of the stack.
- P15. Test 2's limit is stated (section 7).
- P16. Recorded in TODO-33, not decided: Hadi's idea that every start stops when no agent has anything left scheduled
  or scripted.

Given at the review of increment (i) (Hadi, 6 October 2026; design_records.md, "T-viz, the web-ui", 1a, HADI'S REVIEW
OF INCREMENT (i)). Increment (i) works for Hadi as a first stage; he will ask for tuning later.

- P17. The selection panel folds at the first step and reopens from the header's button: kept.
- P18. Panel 4a is 300 px wide for now and may grow to 400 px; its width is adjusted in increment (iv). Panel 4b stays
  a thin rail until stage 1b.
- P19. The control bar stays under the env-pane, for now.
- P20. The env-pane's header shows the layout's id only, not its title, for now, until the stale titles are corrected
  (open item 12 stays open).
- P21. Table tops are drawn see-through in increment (iii), so that an agent at a table is not hidden. Hadi judges it
  when he sees it.
- P22. The default play speed stays 5 ticks per second.
- P23. `mesa_sim/webui_export.py` and the saved sample messages of the 0.3 trial are removed in increment (ii), after
  verifying that nothing else reads them; the README is updated where it names them.
- P24. The order of the rest of 1a: (ii) and (iii) built together, no pause between them; one pause for Hadi's review;
  (iv) in a new session; then (v), polishing, from a written list Hadi gives, ccode working that list and nothing else.
  Whether a second polishing round follows after stage 1c is open.

Given during the build of (ii) and (iii) (Hadi, 6 October 2026; design_records.md, "T-viz, the web-ui", 1a, THE MODE
OF CHECKS FOR THE REST OF STAGE 1):

- P25. Stage 1 is a prototype; checks of the page are reduced for the rest of stage 1. Kept: headless byte-identical
  whenever `mesa_sim/`, `shared/`, `world/` or `domains/` changes (a difference stops the work); the test suite once at
  the end of each increment; the page's build and type check; one look in a real browser per new feature at one window
  size (fix what is broken, do not refine the look). Dropped or deferred: screenshot sets, the second window size,
  saved screenshot folders; visual comparison and refinement (to (v)); page-side unit tests (deferred); the solara-ui
  check per increment (once, before Hadi's acceptance of 1a); long record entries.
  CORRECTED (Hadi, 6 October 2026, preferred; design_records.md, 1a, HADI'S REVIEW OF INCREMENTS (ii) AND (iii)): the
  message went further than meant. Tested: the flow, the functions and the logic of the web-ui, page-side included
  (written, not deferred; logic of (ii) and (iii) without a test gets one). Not tested: details of appearance and how
  good the page looks (no screenshot sets, no second window size, no visual refinement rounds). The rest of P25 stands.
- P27 to P33 (Hadi, 6 October 2026, after trying (iv); design_records.md, 1a, THE PANELS' CONTENT): P27, the roles
  of the panels: 4a the human and the world's context at the tick, 4b (1b) the robot's body and mind, 4c (1c) both over
  time. P28, panel 4a holds (A) the human now, (B) the recent switches and resumptions, (C) the human's script, (D) the
  world's context now; C and D in (iv)'s second part. P29, the robot-human distance and a subplot of the timeline facts
  go to 4c, not 4a. P30, the tag per task is wanted in 4a, its definition open, nothing built. P31, task names show
  values only. P32, 4a's reference cases (the record lists them). P33, every layout's notes rewritten for a
  screen-user.
- P26. Kept at the review of (ii) and (iii): the page's behaviour on a choice that cannot be built; the address with
  every run option; the table top's opacity for now; the 15 page tests. dock_loading's four layout notes rewritten.

---

## 1. Facts verified for this plan (ccode, 6 October 2026, at e5de942 and d44fda3)

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
  (singular), the same kind of text under another key (renamed in (ii), P8);
- setups: a top-level `notes` in kitting's env_setup_17 to _30 (14 of 30) and in all 10 of dock_loading's.
The notes say what a room or a shift is for (for example "The IRB's enlarged room ..."), 81 to 1749 characters. The
layout's `space.name` (the catalogue's title) is stale in older layouts (open item 12).

F4. The loader. `SimModel.__init__` reads the layout inline: the space and its title, the areas, and the fixed
objects in the first pass of `_init_objects` with its checks (`mesa_sim/sim_model.py`, 175 to 212 and 316 to 353); the
setup in the second pass of `_init_objects` (the movable objects at their home containers) and `_init_states`. No
function reads a layout or a setup alone today. P3 and P7 therefore need those parts moved into functions that
`SimModel` calls and the web-ui's piece calls. A change of `mesa_sim/` with no change of behaviour, checked by
byte-identity (section 8).

F5. Agents have no size in the model: they are points (`agent.pos`); `min_separation` (50) is a distance between
positions, read by the mind and the separation stop. An area's `label` is in 22 of the 24 registered layouts (not in
kitting's env_layout_08 and _19); the model does not read it; only the paused `ros_sim/` does.

F6. The server's libraries are installed already: Starlette 0.48.0 (pinned in `requirements.txt` for Solara) and
uvicorn 0.30.5 (installed with Solara, not pinned). FastAPI and httpx are not installed. Node.js 22.13.1; Chrome for
the screenshots through playwright-core, as in 0.3.

F7. Sizes. A tick update is 1.0 to 1.8 KB as JSON (mean 1.3 KB over scenario_s02_01's 450 ticks, 1.0 KB over
scenario_s08_01's 400); a run description 4 to 5 KB. A sim-run of 2000 ticks holds about 2.6 MB of tick updates, one of
10 000 ticks (possible without a limit, P11) about 13 MB.

F8. The glossary terms of panel 4a. With an entry: **stack** (top first), **record**, **outcome** (completed,
suspended, abandoned, infeasible), **event trigger**, **decision**, **open entry**. "Action in hand", "progress",
"switch" and "resumption" had no entry of their own; they get one (P14).

F9. The steps in the code. `steps` has no default (`run_config.OPTION_DEFAULTS` names none); `SimRun` reads
`config["steps"]` for the start line's `steps=` field; the headless start steps that many times; the catalogue declares
`steps` as a `CountOption` (minimum 1) whose default is the run file's, and refuses a run file that states none
(`webui_adapter._declarations`); a `SimRunChoice` must give it a value; `EndReason.STEPS_REACHED` ends a sim-run there.

F10. The point of P12 in the code. The robot's pool is empty from the tick of its `[meta] step=N all tasks complete`
line, where `RobotAgent.finished` is set (the declared tick; the world tick of completion is N or N − 2, TODO-127). The
test-beds read MPB-5's "first observed completion point" from that line. The human's script has ended when every
ordinary and closing entry is closed and the stack is empty (`HumanStackMachine.all_closed()`, the executor then
selects nothing more). Measured on the 48 maintained baseline logs: 46 run past the point, by 5 to 116 ticks; the two
of scenario_s02_01 (450 steps) end at tick 449 with the human 86 of 91 ticks into the closing walk to corner_SE, five
ticks before the point.

---

## 2. The increments

Four increments, each ending with a pause for Hadi's review. AMENDED (P24): five increments; (ii) and (iii) share
one pause, and (v), polishing, follows (iv). They follow cchat's proposal with two changes, each with its reason:
- The page layout moves from (iv) to (i): the whole frame of the page (header, selection panel, env-pane with its
  control bar, the places of 4a, 4b and 4c) is built first, empty where later increments fill it. Reason: Hadi
  reviews the page layout while it is cheap to change, and the later increments fill places instead of moving them.
- Test 1 (a sim-run through the server writes the same log pair as headless) moves to (i). Reason: the server writes
  log pairs from (i) on; a fault there must be found before anything is built on it.

### (i) The server, the start, the page's frame, a minimal choice, the moving env-pane

Scope:
- `webui/server.py` (new): the web-ui's server: the rules (which sim-run is current, the end at a step limit when one
  is set, the lock after the first step, the refusals) and the requests of 0.4 over HTTP (section 4, item 5). It
  imports no simulator: it takes a `Simulator` (webui/simulator.py).
- `mesa_sim/run_webui.py` (new): the web-ui's start (P6, section 4 item 6): the run file and the flags read by
  `run_config` as the headless start reads them, Mesa's piece built on them, the server started.
- `mesa_sim/sim_run.py`: the log pair of a web-ui sim-run takes only its own thread's lines and does not echo to the
  terminal (section 4, item 9); a sim-run without a step limit (P11; section 4, item 11). Headless and the solara-ui
  unchanged.
- `mesa_sim/webui_adapter.py`: the catalogue carries each domain's scene appearance (section 4, item 1); the default
  choice comes from the start's run file and flags; the step limit optional (M8); the point where all agents have
  finished (M7).
- The page: the frame of section 5; a minimal choice (domain, and the scenario from one list, on its reference
  layout; the run options at the start's values, shown, not yet changeable); the control bar (play, pause, step,
  reset, the speed, the tick); the pause where all agents have finished (P12); the env-pane reading the server's
  messages, the agents moving, turning to their last motion, movable objects carried and placed by 0.3's rule.
- `README.md`: the web-ui's start, beside the other starts.

What Hadi sees: one command; the browser opens the page on the run file's sim-run at its start (P9); play, and the
human and the robot walk, pick up and place; play pauses by itself when all agents have finished, and the page says
so; step and play go on; pause, step, reset; another scenario chosen, and its start shown at once.

Checks: test 1 in both domains, and the thread filter's test (section 7); a test that the point of P12 is the tick of
the `[meta] ... all tasks complete` line and of the human's last record change, on the four maintained sets' sim-runs;
headless byte-identical (section 8); the solara-ui still serves and steps; the screenshots (section 8).

### (ii) The full selection, all run options, lock and unlock, the address

Scope:
- The loader's layout part and setup part moved into functions that `SimModel` and the piece both call (F4); the view
  of a layout and the view of a layout with a setup produced from them (section 3, M2; P3, P7).
- dock_loading's four layout files: the key `space.note` renamed `notes` (P8); nothing reads it, no sim-run changes.
- `mesa_sim/webui_export.py` and the 0.3 trial's sample messages (`webui/page/public/samples/`) removed, after
  verifying that nothing else reads them; the README and CLAUDE.md updated where they name them (P23).
- The env-pane's header shows the layout's id only (P20).
- The selection panel: domain, layouts, setups, scenarios as P2 states; the layout shown on choosing a layout, with
  the setup's objects on choosing a setup (P3, P7); the notes of layouts and setups, the scenarios' descriptions and
  the text filter (P4).
- All run options, each by its declared kind (switch, one of, level, the step limit), the value stated and the value
  in effect side by side: an option that another sets off shows "off in effect". The page holds no rule between them;
  the run description's `effective` tells it. The run options stay as set when the layout, the setup or the scenario
  changes (P13).
- Lock and unlock: every change that completes a triple, or changes an option, builds the model and shows its start;
  the first step locks the choices; reset unlocks them. A choice that cannot be built shows its `BuildFailure` and
  the page stays on the view it had.
- The page's choice mirrored in the address, by the rule of section 5 (P10).

What Hadi sees: kitting's twenty rooms, one after another, each drawn alone; a room's setups, each with its objects
where the shift starts them; a setup's scenarios with their descriptions, filtered by a word; a scenario's start; an
option switched, and the options it sets off marked; a bookmark that reopens a scenario at its start.

Checks: every offered triple builds (all 1019, about 3 ms each); the offered setups and scenarios equal P2's rule for
every layout; the view of a layout with a setup equals the matching part of the run description of every scenario on
it, at its start (P3's condition, all 1019); headless byte-identical after the loader's move; the solara-ui still
serves and steps; the address rule's cases (section 5) in the browser; screenshots.

### (iii) The env-pane additions

Scope:
- The free camera beside the two presets (section 4, item 3).
- An object's state changing its look (section 4, item 2): the appearance data's states, dock_loading's empty pallet
  and open gate as the first two.
- Display places kept while an object stays, freed places and too many objects (section 4, item 10).
- `current` returns every tick update of the sim-run (section 3, M3): a reload keeps the picture.
- Table tops see-through (P21): the `counter` form's top is drawn see-through, so that an agent at a table is not
  hidden; the page names the form, not the domain's type.
- Page-side unit tests (vitest, pinned) for the display places and the choice of a look by state.

What Hadi sees: the camera turned, tilted, zoomed and moved during play, and the presets bringing it back; pallets
emptied in dock_loading drawn as empty skids; a container whose objects leave one by one, the others staying in their
places; a reload in the middle of a sim-run showing the same picture.

Checks: the unit tests; a screenshot before and after a reload, equal; screenshots of both domains, both presets and
one free angle.

### (iv) Panel 4a, test 2, the close of 1a

Scope:
- Panel 4a (section 4, item 8; P5); its width adjusted between 300 and 400 pixels (P18). AMENDED (P28): also the
  human's script (C) and the world's context now (D), in a second part of (iv).
- Test 2 (section 7).
- The page's README, the README's starts, and the records of 1a's build.

What Hadi sees: the whole page of 1a; the human's activity changing as the human works, is interrupted (a coffee
break started by an event) and resumes.

Checks: test 2; the domain-word scan of `webui/` and the page; screenshots of both domains, every page state
(AMENDED, P25: one look in a browser per new feature, one window size; the solara-ui checked once here). Then
Hadi's acceptance of 1a, from which the solara-ui is archived (the README and the roadmap say so). AMENDED (P24):
Hadi's acceptance of 1a follows (v).

### (v) Polishing (added by Hadi, 6 October 2026, P24)

Scope: the written list Hadi gives after (iv), and nothing else; in a session of its own. Whether a second polishing
round follows after stage 1c is open.

Checks: those of section 8, as P25 reduces them, that the list's items touch.

---

## 3. The message round of 1a

What 1a adds to the messages of 0.4. Of 0.4's messages, M3 changes the request `current`, and M8 the declaration of
the steps.

M1. The catalogue.
- `DomainEntry.appearance`: the domain's scene appearance, read by the piece from `domains/<domain>/appearance.json`,
  the defaults when there is none (section 4, item 1).
- `LayoutEntry.notes` and `SetupEntry.notes`, optional text: the notes of the layout and the setup files (F3), shown
  in the selection. Reason: P4's reason (Hadi cannot choose from an id alone) holds for rooms and shifts too.

M2. The view (P3, P7), a new message: the domain, the layout's id, the space, the areas, the fixed objects; with a
setup chosen also the setup's id, its movable objects in their home containers in the setup's order, and the object
states that hold at its start. The field types are the run description's and the tick update's (`Space`, `Area`,
`FixedObject`, `MovableObject`, `FixedObjectContents`, `ObjectState`), produced from the same functions that the
model's loader calls (F4). A view has no sim-run, no agent and no tick.

M3. The requests. Two changes to 0.4's list:
- `view` (new): the view of a layout, or of a layout and a setup; an unstepped current sim-run is discarded (no file);
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

M7. The point where all agents have finished (P12). The tick update gets a third section beside `world` (and 1b's
`mind`): `run`, the facts of the sim-run that are neither the world's nor the robot's mind's. In 1a it holds one value,
`finished_at`: the first tick at which every human's script has ended and every robot's pool is empty (F10), None
before. Once set it is kept: the human's executor selects nothing more after its script has ended (stage 3's live
events may change this), and a robot's pool does not refill. Why not under `world`: the robot's pool is not a world
fact. Why not under `end`: the sim-run has not ended. Why not left to the page (the human's script from `world`, the
robot's pool from 1b's `mind`): the rule that defines the point would then live in the page, and 1a has no `mind`
section. The piece reads it from the model: `HumanStackMachine.all_closed()` with an empty stack, and
`RobotAgent.finished`.

M8. The step limit (P11). 0.4's `CountOption` and `CountValue`, used only for `steps`, become `LimitOption` and
`LimitValue`: a whole number at least its minimum, or no limit (`None`). The catalogue's default is no limit, or the
number given with `--steps` at the web-ui's start; the run file's `steps` is not used by the web-ui. The run
description's `effective` carries the limit as stated. `EndReason.STEPS_REACHED` stays, for a sim-run with a limit.

---

## 4. Proposals on the open items of "State after stage 0"

Items 4, 6 and 8 are answered by Hadi's preferences P6, P2 to P4 and P5; the plan states how they are built. Items 11
and 12 below are new with Hadi's answers.

### Item 1: how the scene appearance reaches the page

The catalogue's per-domain entry carries it (M1), read by Mesa's piece from `domains/<domain>/appearance.json`. The
page has it before any model exists, so a view (P3, P7) is drawn in its look. Every state a domain's appearance names
(item 2) is checked by the piece against the domain's declared states when the catalogue is built: a misspelt state
stops the start with a message, instead of being silently never drawn. A small change of form: `webui/appearance.py`
imports `webui/messages.py` for its base class, so for the catalogue to name `Appearance` the base class moves to a
module of its own; no message changes by it.

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
  give the catalogue's default choice; the page opens on it (P9), unless its address names a choice (section 5).
- `--steps` given at the start sets the default step limit; the run file's `steps` is not used (P11), and the start
  says so on the terminal when the run file states one.
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

Per human, under a header with the human's id and its colour, in the glossary's words (P14):
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
  run's largest movable object at its own size with 0.3's gap.
- The places are taken from the centre outward: numbered by their distance from the footprint's centre, nearest first,
  equal distances row by row from the north-west. Reason (ccode's choice of visual design, after cchat's note): a
  container with one object shows it in its middle, as in the trial Hadi accepted, while no place moves; numbered from
  the north-west corner, a lone object would sit in the corner. Where the grid has an even count along an axis, its
  middle is between two places, and a lone object sits half a place off the centre.
- An arriving object takes the lowest-numbered free place, and keeps it while it stays (section 9's requirement 2). A
  freed place is taken by the next arrival. At the start the setup's order fills the places from the first.
- More objects than places: the next ones are drawn on a second layer, on the places in the same order, then a third.
  Objects never overlap side by side, and no object moves when another arrives or leaves.
- Determined by the sequence of tick updates (the order of arrival per tick), so the same sim-run always gives the
  same picture, a reload included (M3).
- What changes from the trial: the trial's grid was shaped for the objects present, so a full container looked the
  same; a container with fewer objects than places now shows them gathered at its middle, with free places around.

### Item 11: the step limit (P11)

- A sim-run has a step limit only when the screen-user enters one in the page or the start was given `--steps` (M8).
  With a limit the sim-run ends at it (`steps_reached`), as 0.4 stated; without one it ends by reset, by a change of
  choice after the first step, or at the server's stop.
- The start line. `SimRun` writes `steps=<n>` on the start line, and a web-ui sim-run without a limit has no number.
  Proposed: it writes `steps=none`; a sim-run with a limit, and every headless start, write the number as now. The log
  pair of a web-ui sim-run without a limit therefore differs from every headless pair in that field only.
- Test 1 states its steps (section 7).
- Without a limit a sim-run's tick updates grow with it; the page and `current` hold them all (F7: about 13 MB at
  10 000 ticks). No limit is set for this; it is noted for Hadi.

### Item 12: the pause where all agents have finished (P12)

- The tick update's `run.finished_at` (M7) is set on the first tick at which it holds. On that tick update, play
  pauses; the env-pane's header and the control bar state "All agents have finished at tick N". Step and play continue
  the sim-run; the statement stays. A page reloaded after the point does not pause again.
- With a step limit that comes first, the sim-run ends without reaching the point; with a human whose script never
  ends, or a robot whose pool never empties, there is no pause.
- The point is the declared tick of the robot's empty pool (F10), the tick the test-beds read; the world tick of the
  robot's completion is up to two ticks earlier (TODO-127).

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
│            │ env_layout_03 …   │ env_setup_18    │   …                              │ limit [none ]   │ step
├──────────────┬───────────────────────────────────────────────────────────────┬───────────────┤
│ The human    │ env_layout_02                             [Tilted|From above]  │ The robot's   │
│ ● human_0    │                                                               │ mind          │
│ action in    │                                                               │ (stage 1b)    │
│ hand …       │                        the scene                              │               │ main row
│ ███████░ 12  │                                                               │ folded to a   │
│ stack …      │                                                               │ rail in 1a    │
│ switches …   ├───────────────────────────────────────────────────────────────┤               │
│              │ ⟲ Reset  ⏭ Step  ▶ Play   5 ticks/s ▾   tick 211 · 212 steps                    │ control bar
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
  while locked. About 240 pixels high when open. The run options keep their values when the layout, the setup or the
  scenario changes (P13); the step limit is a number field that reads "none" when empty.
- The main row: panel 4a 300 pixels wide, the env-pane the rest, panel 4b 300 pixels. In 1a, 4b is folded to a narrow
  rail with its title, so the env-pane gets its width; in 1b it unfolds. Below 1200 pixels of width, 4a also folds to
  a rail. PREFERRED (P18): 4a is 300 pixels for now and may grow to 400, adjusted in (iv); 4b a thin rail until 1b.
- The env-pane's header: the layout's id only, not its title, for now (P20), and the two presets.
- The control bar: at the foot of the env-pane (PREFERRED for now, P19), because it acts on what the env-pane shows;
  the plots of 1c, below it, share its tick axis. Reset, step, play and pause (one button), the speed in ticks per
  second (1, 2, 5, 10, 20, as fast as the server answers; 5 by default, P22), and the tick as the run log numbers it,
  beside the steps done. Without a step limit (P11): "tick 211 · 212 steps", no bar. With a limit: "tick 211 · 212 of 450 steps", with a bar over the limit.
  Before the first step the tick reads "start". The tick's number is the one a log line or a figure carries, so a
  moment seen in the page is found in the log. From the point where all agents have finished (P12), the bar also reads
  "All agents have finished at tick N".
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
     ended (locked) ◀──step limit, if one is set── playing / paused (locked) ───────────────────┘
          │                                          │  ▲
          └──reset──▶ start                          │  └─ step, play
                                                     └──all agents finished──▶ paused, "all agents have finished"
```

### The address (P10)

- The address holds the page's choice: the domain, the layout, the setup and the scenario as far as chosen, and every
  run option's value with the step limit if one is set. It is rewritten on every change of the choice, without a new
  entry in the browser's history.
- On loading the page, the server's state wins: the page asks `current` first. If a stepped sim-run is current, the
  page shows it and ignores the address. Otherwise the page requests the address's choice: `choose` for a complete
  triple, `view` for a layout or a layout with a setup; with no choice in the address, the catalogue's default choice
  (P9). An address whose choice cannot be built (a scenario renamed since the bookmark, an option no longer declared)
  shows its `BuildFailure` and opens the catalogue's default choice.
- The limits (P10): the address is not a run file (TODO-189); it reopens a choice at its start, not at a tick; one
  server holds one current sim-run (TODO-187), so two tabs on one server share it, and a second tab opened while a
  stepped sim-run is current shows that sim-run whatever its address says.
- Embedding the page in web-based slides is a later task Hadi will open; 1a builds nothing for it beyond the address.

---

## 6. What the env-pane shows with a layout and a setup and no scenario (preferred, P7)

The layout with the setup's movable objects in their home containers, at their display places, and the setup's object
states at its start (an empty pallet drawn empty); no agents, no tick, the control bar disabled. Reason: Hadi compares
rooms first, then a room's setups; what distinguishes two setups of one room is which objects lie where. Cost: the
setup's part of the loader (the second pass of `_init_objects` and `_init_states`) moves into a function, as the
layout's part does (F4), and the view message carries it (M2).

---

## 7. The two tests, and the same log pair

Test 1: a sim-run through the server gives the same result and the same logs as the headless start.
- For scenario_s01_01 (kitting) and scenario_s03_02 (dock_loading), the run options of the run file and an explicit
  step limit equal to the headless steps (300 and 800, as 0.4's check 3): the server started as its own process by
  `mesa_sim/run_webui.py --steps <n>`, driven over HTTP (choose, then step until the end, with the standard library's
  HTTP client), and its log pair compared byte for byte with the pair of the headless start with the same flags. Both
  write the start line, the override lines (none), the model's lines, the per-step lines, `[sep]`, the end
  (`end_run`) and the end line, through the same `SimRun`.
- A sim-run without a limit, reset at tick k, equals the headless start of k steps except the `steps=` field of the
  start line (`none` against k).
- The pause where all agents have finished changes nothing in the log pair: it is the page's, and the sim-run steps on.
- The thread filter: a line logged on another thread while a web-ui sim-run is attached stays out of its pair; the
  same line on the sim-run's thread goes in.
How the same log pair is reached: the server builds and steps through Mesa's piece, which builds and steps the same
`SimRun` as the headless start; the server only decides when to step and when to end; the thread filter takes nothing
the sim-run writes, since it writes everything on its own thread; the piece only reads the model (0.4's check 3).

Test 2: a domain the web-ui has never seen is drawn without a change to the web-ui's code.
- The server started with one more domain in the registry, under a new name, with dock_loading's content and no
  appearance file: the catalogue lists it, a sim-run of it builds and steps through the server, and in Chrome the page
  draws it from the default appearance with no error on the console (a screenshot).
- Its limit (P15): the copy shows that a domain without its own look is drawn, under a name the web-ui has not seen.
  Its object types and area ids are dock_loading's, so it does not show that new object types or new area ids are
  drawn; that the web-ui's code names none is shown by the code scan (no domain name, object type or area id of any
  registered layout or setup in `webui/` or in the page's files), which runs beside it.

---

## 8. Checks in every increment

AMENDED (Hadi, 6 October 2026, P25), from (iii) on: the list below is reduced to headless byte-identity where
`mesa_sim/`, `shared/`, `world/` or `domains/` changes; the test suite once per increment; the page's build and type
check; one look in a browser per new feature at one window size; the domain-word scan stays (it is in the suite). The
screenshot sets and the second size, the saved folder and the solara-ui per increment are dropped (the solara-ui once
before Hadi's acceptance of 1a). CORRECTED (P25): page-side tests of logic are written in every increment.

- Headless byte-identical where `mesa_sim/` changes ((i): `sim_run.py`; (ii): the loader's move): the four maintained
  sets (48 logs and their `.rec`) and dock_loading's scenario_s03_02, s05_02, s07_02, rerun into a scratch folder and
  compared with the baselines, as in 0.2 and 0.4.
- The test suite (418 passed at the close of stage 0).
- The solara-ui kept working until Hadi accepts 1a: `solara run` serves per domain and a sim-run steps, as 0.2's
  check 3.
- `npm run build` and the type check pass; the page's types regenerated from `webui/schema.py` when a message changes.
- Screenshots in Chrome (playwright-core, as 0.3's `npm run shots`, extended to drive the running server), both
  domains, at 1440 x 900 and 1920 x 1080: each increment's states (a layout view, a layout and setup view from (ii)
  on, a start, a moment of play, the pause where all agents have finished, an end at a limit; both presets, a free
  angle from (iii) on), saved to `docs/handoffs/tviz_1a/`, git-ignored as 0.3's `tviz_trial/` (one line added to
  `.gitignore` in (i)).
- `webui/` imports no simulator, and neither it nor the page names a domain, an object type or an area id (the tests
  of stage 0, extended to the new files).

---

## 9. Outside 1a: flagged, not done

- The stale layout titles (open item 12): the selection shows the id first and the title beside it. AMENDED (P20):
  the env-pane's header shows the layout's id only, until the titles are corrected; the item stays open.
- The run-level lines say "headless" for the web-ui too (TODO-191), unchanged until the next regeneration; the start
  line's `steps=none` (item 11) joins that question.
- `analysis/instruments/mpb/actual.py` keeps its own copy of reading and ending (flagged in 0.2), untouched.
- Saving the page's choice as a run file stays unassigned (TODO-189); the address (section 5) is not a run file.
- A stop of every start at the point where all agents have finished is Hadi's idea, recorded in TODO-33, not decided;
  1a only pauses play there (P12). Headless keeps its step limit.

---

## 10. Questions to Hadi

Answered on 6 October 2026: Q1 (b), Q2 (a), Q3 (a) (P7, P8, P9). No question is open. Every proposal above stays
proposed by ccode until Hadi says "I prefer"; he reviews each at the pause after its increment.
