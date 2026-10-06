# Handoff: T-viz, the web-ui

Written in cchat (the design chat with Hadi), 4 to 6 October 2026. Written for ccode.
Intended place in the repo: `docs/handoffs/handoff_T-viz.md`, with the reference images in `docs/handoffs/tviz_refs/`.

This file is the first record of T-viz in the repo. Nothing of this discussion was recorded before it.
It is written in full on purpose. It holds what Hadi prefers, what is still open, what cchat proposed, what cchat
doubted or corrected, and the facts that ccode must verify. It is not a specification and it is not a set of rulings.

---

## 1. How to read this file

### 1.1 Status words

Hadi asked that the web-ui work does not use the words "ruling" and "ruled". He finds them too strong for this work,
as if a choice could not change in a later design stage. The rest of the project (the core design, the conceptual
records) keeps "ruling" and "ruled". This file and every T-viz record use the following words.

| Word | Meaning |
|---|---|
| **open** | Not chosen. Alternatives exist. This is the state of every item until Hadi says otherwise. |
| **preferred** | Hadi said he prefers it. It is the default for now. It can change. |
| **preferred, replaceable** | A default that is defined from the start as exchangeable for a named later alternative. Hadi's example: an agent's path is a straight line now, and another path method can replace it later. |
| **proposed by cchat** | A recommendation or observation of cchat. Hadi has not marked it. Treat it as open. |
| **verified** | cchat read it in the repo's files during this chat. The file is named. |
| **not verified** | cchat states it from memory, from an earlier chat, or by inference. ccode checks it before relying on it. |

Hadi's rule for the whole discussion: nothing is decided and nothing is to be assumed. Everything is open, with
alternatives, until he says "I prefer this".

### 1.2 Who decides what

- Hadi's taste and stated preferences come first.
- The visual design is left to ccode. Hadi said that he does not dictate the web design to ccode. He offers his
  ideas and reference images as inspiration. ccode may propose its own design. Hadi's described taste is more
  important than any single reference image.
- Where ccode's judgement and a "proposed by cchat" item differ, ccode states the difference and Hadi decides.
- Where this file and the repo disagree on a fact, the repo wins. ccode reports the disagreement.

### 1.3 Scope of the first ccode task (0.1)

The first task is recording only. It changes no code. Section 16 states it.

---

## 2. Terms

### 2.1 Terms Hadi chose in this chat (preferred)

| Term | Meaning |
|---|---|
| **web-ui** | The new program: its page in the browser and its small Python server. |
| **solara-ui** | The existing Solara program (`solara run mesa_sim/run_mesa.py`). Hadi said this name with "maybe". It is tentative. |
| **screen-user** | The person who sits at the screen during a sim-run, watches, and presses controls. |
| **author** | Unchanged. The repo's existing word for the person who writes a scenario and the other artefacts before a run. The glossary uses the word, but cchat found no glossary entry that defines "author" by itself (not verified as absent). |
| **sim-run** | One simulation, from a built model at step 0 to its end. Hadi uses this word only where "run" could be confused with starting a program. The glossary's "run", "run file" and "run options" stay unchanged. Hadi stated explicitly that the glossary is not to be changed for this. |
| **start** | Starting a program (the web-ui's server, the headless command). cchat's working word, used with "sim-run". |
| **env-pane** | The region of the page that shows the simulated environment, with agents and objects that move. It may hold 2D or 3D graphics. |
| **scene** | The picture inside the env-pane: the room, the objects and the agents at one tick. Used only where the region and its content must be distinguished. |

For every other part of the page Hadi uses the standard terms of web design: page, page layout, panel, widget or
control, header, sidebar, card, tab, dialog, theme or design system, design tokens, wireframe, mockup.

### 2.2 The word "viewer"

- The repo's records and code use "viewer" for the program. Verified in three places: the glossary's entry "run
  file" ("The viewer reads and edits the same file"), `mesa_sim/run_mesa.py` (the `Page` docstring, "The viewer (T-L
  stage 4, ruling 7)"), and `mesa_sim/viz/run_file_panel.py` ("The viewer's run-file panel").
- For Hadi, a viewer is a person, not a program. He asked for another name for the program. The result is "web-ui"
  for the new program and "solara-ui" for the existing one.
- Open: whether the existing records and code comments are renamed. Nothing is to be renamed without Hadi's word.
- In text that Hadi wrote before these names existed (for example the slots input in section 9), "the viewer" means
  the web-ui.

### 2.3 Words to keep apart

The glossary uses these words for the simulated world. Web designers use some of them for the page. In T-viz text,
do not use them for the page without a qualifier.

- "layout": the room (the layout artefact). For the page, say "page layout", always in two words.
- "area": a declared region of the room.
- "space": the bounds of the room.
- "environment": the holder of the world's true states.
- "setup": the shift (the setup artefact). Hadi once wrote "stages" where he meant setups. He confirmed that he
  meant setups.

### 2.4 Working terms without a glossary entry

These are used in this file. None is a glossary term. ccode proposes entries where one is needed. Hadi decides.

- "display place" (from the slots discussion, section 9).
- "run description" and "tick update" (cchat's names for the two messages, section 8).
- "preview" (the scene shown before a sim-run is stepped, section 7.5).
- "draft" (the chosen artefacts plus edits, held in the server's memory before a model is built, section 7.6).
- "active object" and "passive object" (Hadi's distinction for the look of objects, section 10.5).
- "scene appearance" (cchat's phrase for the look of things inside the scene, as distinct from the page's theme).
- "shape kind" (cchat's phrase for a generic geometric form that the scene drawer knows, section 10.6).

---

## 3. Why this task exists

Hadi's reasons, in his words where possible.

- The solara-ui is "kind of rigid and hard to add elements".
- It redraws the entire Plotly figure on every tick. Hadi called this "kind of dummy" and said it is slow.
- Plotly is a charting library. Hadi's view: "plotly is not for this", meaning the drawing of a room with moving
  agents.
- With Solara, "we have to stick to its way of architecture".
- He wants to design his own page layout and panels for the framework ("IR+AP framework"), in his own way.
- He considers an own server plus an own front end a manageable job for ccode with Opus 5.5.
- He wants full freedom of web technology.

Hadi's stated minimum, early in the chat: the same as the solara-ui's content. That is an environment visualisation
that changes per tick, play and pause, and a few values per tick. More (for example a panel for the robot's mind)
was to come as a second task. The stages in section 12 later widened stage 1. See 12.3.

---

## 4. The present state of the repo, as far as it concerns T-viz

### 4.1 How the solara-ui works (verified)

Sources: `mesa_sim/mesa_fork/visualization/solara_viz.py` (uploaded by Hadi and read in full), `mesa_sim/run_mesa.py`,
`mesa_sim/viz/space_drawer.py`, `mesa_sim/viz/portrayal.py`, `mesa_sim/viz/run_file_panel.py`, `requirements.txt`.

**Start.** `solara run mesa_sim/run_mesa.py`, with this script's own arguments after `--`.

**Page.** `run_mesa.py` defines `Page()`. It places `RunFilePanel` in `solara.Sidebar()` and calls the fork's
`SolaraViz(model_class=SimModel, model_params=..., space_drawer=space_drawer, agent_portrayal=agent_portrayal,
name="TeamRob Simulation", play_interval=5).key(f"run-{reload_count.value}")`.

**Clock.** The browser owns it.
- `ModelController` creates `widgets.Play(interval=play_interval, on_value=on_value_play)` (an `ipywidgets.Play`).
- The widget's timer runs in the browser. At each interval it increments a counter.
- Solara syncs the counter to Python. `on_value_play` calls `do_step`, which calls `model.step()` once.
- `play_interval=5` means 5 milliseconds. The round trip cannot meet it, so the round trip sets the real rate.
- Play stops when `model.running` is false.
- A threaded alternative (`threaded_do_play`, a Python loop that owns the clock) is in the file and is not used.

**Controls.** Three: Step (`do_step` once), the Play widget (play and pause), Reset (increments `reset_counter`,
and `solara.use_memo` then constructs a new model).

**Redraw.** The whole figure, on every step.
- `do_step` sets `current_step.value = model._steps`.
- That change makes Solara render `SolaraViz` again.
- `Card` calls `space_drawer(model, agent_portrayal)`, which builds a new Plotly `go.Figure` from the model objects
  and hands it to `solara.FigurePlotly`.
- The areas and the fixed objects are rebuilt and sent again on every tick, although they are constant in a run.

**No description of the state exists.** `space_drawer` receives the Python model object. It reads `model.areas`,
`model.env_objects`, `model.robots`, `model.humans`, `agent.pos`, `agent.planned_path`, `model.space.x_min` and the
other bounds directly. The browser receives a finished drawing, not a description of the state. The drawing code
and the model are in one Python process with no boundary between them. This is why a message design is needed for
the web-ui: nothing in the repo lists what a drawer in another process needs to know.

**Per-tick information.** Three values, in the "Information" card: the step number, the position of
`model.robots['robot_0']`, the position of `model.humans['human_0']`, both rounded to one decimal.

**Page layout.** A top bar with the name. A sidebar with a "Controls" card and an "Information" card, plus
`RunFilePanel`. A main area with one card: the scene, titled `model.env_display_name`. `run_mesa.py` passes no
`measures`, so no other card exists.

**The run-file panel** (`mesa_sim/viz/run_file_panel.py`, T-L stage 4). It shows the run file's path, the domain,
the triple and every override. It adds, replaces or removes one override of the three kinds. It first builds the
run with the new overrides (`SimModel(**{**model_params, "overrides": trial})`). Only a run that loads is written
(`write_overrides`). Then the page reloads: `reload_count` increases and `SolaraViz` remounts under a new key, which
gives a fresh model.

**Versions.** Python 3.10. `solara==1.57.3`, `starlette==0.48.0`, `reacton==1.9.1`, `plotly==5.23.0`. Mesa is not
installed by pip. The fork is vendored at `mesa_sim/mesa_fork/` (Mesa 3.0.0a1, from an earlier chat, not verified
in this one).

### 4.2 How a run is read and built (verified, `mesa_sim/run_mesa.py`)

`run_mesa.py` holds three things in one file.

- **A. Reading.** `parse_user_args()` (strict argparse), `load_user_config()`, `load_experiment(run_path, flags,
  cli_overrides)`. The run file (`configs/experiment.yaml` by default, `--run <path>` for another) and the flags are
  merged into one run configuration. A flag given on the command line replaces the file's value. Unknown keys,
  values outside their choices and non-boolean switches stop the run.
- **B. Building.** `resolve_triple(config)` looks up the domain in `DOMAIN_REGISTRY`, the scenario, the scenario's
  setup, and the layout (the one named, or the scenario's first reference layout). `resolve_model_params(config)`
  returns the keyword arguments of `SimModel`. `SimModel(**params)` builds the model. The docstring says that
  both the headless factory and the Solara page use it, "so a name the registry does not have fails the same way on
  both".
- **C. Two uses of the model.** The headless loop (`run_headless()`), and the Solara page.

The flags: `--run`, `--override`, `--domain`, `--layout`, `--scenario`, `--steps`, `--human_aware`,
`--intention_aware`, `--assignment_knowledge`, `--context_knowledge`, `--strategy`, `--gate_strategy`,
`--cost_strategy`, `--separation_stop`, `--test_level`.

Dependencies between run options, from the help texts (verified as text; the behaviour in `SimModel` is for ccode to
confirm):
- `--human_aware` off: "the human-unaware robot, no observed human; sets intention_aware, both knowledge options and
  separation_stop off; T-F part 1".
- `--intention_aware` off: "the intention-unaware robot, the recognizer computes nothing and the gate admits
  nothing; sets both knowledge options off; T-F part 1".
- A comment in `resolve_model_params`: "both on by default (T-F part 1, R3); SimModel applies the override (R5)".

Hadi described this mechanism the same way ("if human_aware is OFF, automatically intention_aware becomes off").
**Correction of a cchat statement:** in the chat cchat told Hadi that the help text said "not valid with human_aware
off" and that this suggested a refusal. That quotation was wrong. The help text says "sets ... off", which is an
automatic switch, as Hadi said.

**Solara is imported by the headless run.** `run_mesa.py` imports `solara`, `space_drawer`, `agent_portrayal`,
`RunFilePanel` and `SolaraViz` at module level, without a guard. A comment says that Solara needs the page at the
top level at module load time. A flag `_UNDER_SOLARA` only decides whether `run_headless()` is called. Consequence:
a headless run imports Solara and the viz modules. A fault in those modules at import would stop a headless run.

### 4.3 Faults and inconsistencies noticed on the way (outside T-viz's scope, flagged)

- `solara_viz.py` hardcodes the ids `robot_0` and `human_0` in the Information card. A scenario with other agent
  ids would fail there.
- `space_drawer.py` holds two tables in code: `OBJ_COLORS` (object type to colour, with a kitting block and a
  dock_loading block) and `AREA_COLORS` (area id to colour, again per domain). Adding dock_loading needed an edit
  of the drawer. The module's own header says that it does not hardcode colours per object id. That is accurate
  for ids of objects and not for types and area ids.
- `docs/roadmap.md`, Phase 2.2, says "Live agent positions, task progress, belief state display". In the files
  cchat read (`solara_viz.py`, `space_drawer.py`, `run_mesa.py`), neither task progress nor a belief state is
  displayed. Either another file displays them or the roadmap line is not accurate. This belongs to the records
  cleaning.
- The README lists "Mesa visualization (Solara)" as "Running". That line needs a change when the solara-ui becomes
  archived (section 6.3).

### 4.4 Existing records that already speak of a viewer (partly verified)

cchat first told Hadi that it found no roadmap entry for viewer work. That was incomplete. Later searches returned
these. ccode verifies their current state.

- **T-E, "the viewer"**: `docs/handoffs/handoff_T-D_onward.md` lists it as a task: "shows belief, admitted
  projection, decision, hold, refusal, and now the script's events; check `mesa_sim/viz/` first".
- **Phase 7, T-V (track 2)**: `docs/design_decisions.md` records (recorded, not decided, 23 September 2026; scheduled
  30 September 2026) that a deviation of the human can arrive "as an event during the run (from a viewer)", applied
  at the next action boundary. The first decision of that phase is the replay rule: the viewer offers a fixed set of
  events, every event is logged with its tick, and a finished live run exports its event log as a pre-loaded script.
  "Live runs demonstrate; every evaluation number comes from pre-loaded scripts."
- **T-L stage 4, ruling 7**: "The viewer reads and edits the same file" (the run file). The run-file panel is the
  built form of this.
- **TODO-110** (not built): selection by composition and coverage. The glossary says that scenario composition is
  "what a selector for batch runs or the viewer reads".
- **CLAUDE.md** lists "the viewer and the demonstration" among the things not to be started unasked. T-viz is now
  asked for by Hadi. The 0.1 task updates that line as far as the records require.

Hadi named the present work "T-viz" and confirmed the name. Its relation to T-E is to be stated in the records.
cchat's reading (proposed): T-viz's stage 1b and 1c cover what T-E lists, and T-viz's stage 3 is the page's side of
T-V. ccode checks whether T-E still exists as an open task and proposes how the records join the two.

---

## 5. The course of the discussion

This section keeps the path, including the positions that were given up, so that a later reader does not repeat
them.

### 5.1 Keep Solara, or leave it

An earlier chat (deleted by Hadi since) had set out two options.

- **Option A:** keep Solara as the host. Replace `SolaraViz` with a custom page. Embed a custom JavaScript scene
  component through anywidget or ipyreact. Solara passes the state to it as widget properties.
- **Option B:** replace Solara with a small server of our own and a front end that is entirely our own code.

Points established about option A.
- The fixed page layout that Hadi disliked comes from the fork's `SolaraViz` and from `Page` in `run_mesa.py`, not
  from Solara itself. Solara allows free layouts (`solara.Row`, `solara.Column`, `solara.GridFixed`, tabs, pages).
- Solara still generates the page. Every component runs inside ipyvue and Vue. The update channel is Solara's own
  widget-sync protocol. A change in Solara's dependencies can break the page. The earlier chat's example: the release of
  ipyvue and ipyvuetify 3.0 (Vue 2 to Vue 3, August 2026) was the likely cause of an empty map that Franziska
  reported with Mesa's example models. The cause was not confirmed (from the earlier chat, not verified here).
- cchat first presented the description of the state as a cost of option B only. cchat corrected this: option A
  needs the same description, passed as widget properties. The real differences are smaller: the run-file panel
  stays in Python under A, the controls are in-process calls under A, the front-end stack is fixed to Vue under A.

Where it landed: Hadi wants an own page with an own server, without Solara. His reason: with Solara one must keep
to its architecture. He asked whether a fully custom front end can replace Solara's page. cchat's answer: if Solara
stays as the server, it always generates the page and constrains the tools, so it would contribute only the
transport. If the front end is fully our own, Solara has no remaining purpose.

### 5.2 What others build (searched 4 October 2026)

- **WareTrack** by Dilum Sanjaya (X post of 3 October 2026, "Built with Opus 5.5"). A warehouse dashboard that looks
  like a strategy game. The author stated: React, and React Three Fiber for the 3D parts (a React renderer for
  three.js). He recommended React, preferably Next.js, over plain JavaScript for similar work. According to Grok's
  reading of the thread, all 3D objects are generated by code, not loaded from model files, and the author called it
  "just a simulation". No backend is stated. No code is published. Hadi's comment: he does not want something that
  advanced, but it shows a dynamic scene with panels.
- **A pull request co-authored by Opus 5.5** (`soham10i/stf-hw`, PR 4, from the search excerpt only). A FastAPI app
  runs a simulation kernel and streams world frames over a WebSocket. A separate `GET /layout` gives the browser a
  scene descriptor. The front end is Vite, React, TypeScript and react-three-fiber. This is the same split as
  cchat's proposal in section 8: constant content once, changing content per tick.
- **Rerun**, an existing viewer tool with a Python SDK, a timeline panel and a blueprint API for 2D and 3D views.
  cchat's judgement: it gives replay with little front-end code, but its view types are fixed, it hosts no panels of
  our own design, and it displays data without commanding the simulation. It does not meet Hadi's wish.

Hadi also ran a search prompt (written by cchat) in ChatGPT and Gemini. cchat's reading of the four reports:
- Gemini's first report: its project table had no links and generic names. cchat treated it as invented.
- Gemini's second report: weak, with one link reused for three projects.
- ChatGPT's two reports: usable. They said "not found" where nothing existed. cchat did not open their links.
- Agreement of all four with cchat's recommendations at that time: React with TypeScript, HTTP for the step request,
  message types defined once in Python, a custom page over Rerun or Foxglove.
- The important finding: neither model found a published Opus 5.5 project that combines a Python simulation server,
  step control from the page and a custom scene. The published examples are standalone demos and games in which the
  browser owns everything. No template exists to copy. The server side and the messages are our own design.
- Among ChatGPT's 18 examples: SVG with plain JavaScript in 4, three.js in 3, no framework in 4 or more, no named
  theme or component library in any.
- Three working practices from the reports are in section 14.

### 5.3 The page draws, the model owns the state

A point that came out of the WareTrack comparison. In that demo the page most likely owns the simulation. In this
framework the direction is the reverse: Mesa and the cognitive layer own all state. The page receives a description
and draws it. cchat proposed as a rule that the page contains no simulation logic. This follows from the
framework's goal of independence from the simulator. Hadi did not mark the rule. He agreed with its consequences in
several places (section 15, item 1).

### 5.4 The messages, and where cchat went too fast

cchat proposed the content of two messages (section 8) and listed, as if settled, a separation of world content and
mind content into two named sections. Hadi stopped this: he had not yet said how he wants the visualisation to
separate the actual world from the state that the robot keeps in mind, and he was still at the level of
architecture ideas. cchat withdrew the separation as a settled item. The message contents are parked. Later, in the
stage list, Hadi described three information parts (4a the human and the actual world, 4b the robot's mind, 4c
plots). That is his description of the separation on the page. It does not yet settle the messages.

On planned paths: cchat proposed to leave them out of the first stage, reasoning that the robot's planned path is
content of the robot's mind. Hadi asked "why not?" and proposed a default assumption of a straight Euclidean line,
replaceable later. cchat withdrew the omission and added one correction: the page should not compute a straight
line itself. The model already holds a path per agent (`agent.planned_path`, read by the current drawer). The
server copies it. Today that path is a straight line. When the model's path method changes, the page shows the new
path without a change to the page. This meets Hadi's intent ("straight line now, replaced later") without planning
logic in the page.

### 5.5 Three ways to run, and the archived solara-ui

Hadi's position moved in three steps.
1. He questioned why the solara-ui should stay beside the new program at all.
2. He then preferred to keep it: "we keep current solara as well, in case new one did not finish as I want". The
   repo then has three ways to run: headless, solara-ui, web-ui.
3. He then defined its state: kept in the repo as archived. Not updated with core and model changes. Not deleted.

cchat raised when the archived status begins. Hadi prefers: it begins when he accepts stage 1a of the web-ui. Until
then the solara-ui is kept working. See 6.3.

### 5.6 Time

cchat had remarked that the share of drawing in the solara-ui's slowness was not measured. Hadi's answer: for this
framework as a proof of concept, the time of a run is the number of ticks, not wall-clock time. The CPU time of the
reasoner and the planner is not counted. cchat dropped the remark. Hadi added an idea: a global freeze button in the
web-ui, to stop the world and show the information of one moment to an audience.

### 5.7 The web-ui as the place where a sim-run starts

Hadi's architecture idea (he said "now I am thinking"): the web-ui is overarching. One starts it and the page comes
up first. In the page the screen-user chooses the arguments and the configuration (domain, layout, scenario). The
Mesa model is then initialised with its objects and agents. The visualisation of the environment appears. Then
come widgets such as toggles (his examples: prior on or off, context on or off). Then play steps the model.

He asked how `run_mesa.py` reads its configuration, and whether a starting point is needed before the web-ui or the
headless run. Section 4.2 and section 7 hold the answer. He agreed ("I agree") to move the reading and the building
out of `run_mesa.py` into a module of their own.

He confirmed: run options are fixed for a sim-run. The toggles are set before the model is built. They are not
switched during a sim-run.

### 5.8 Editing, and changes during a sim-run

Hadi raised an interactive web-ui: the screen-user edits the layout and the setup and arranges her own scripted
human (for example his window of rest or break), acting as an author for a sim-run started in the web-ui. He also
raised injecting an interruption or deviation into the human's script in real time. He asked whether such a sim-run
is conceptually temporary, whether it is saved at the end, how the code is structured, and whether it needs session
state. He said that he is not knowledgeable in web programming.

cchat's answer is in section 7.6. Hadi then drew the boundary himself: changing the human's behaviour during a
sim-run is a separate task among the Ts, already discussed (Phase 7, T-V). T-viz is the UI. It allows editing
before the model is built, and no edit once the Mesa model is initiated. Editing became stage 2. The page's side of
changes during a sim-run became stage 3.

### 5.9 The visual direction

Section 10 holds the result. The path: Hadi shared twelve reference images, then a thirteenth. cchat drew twelve
small sketches of one room in different treatments (A to L). Hadi picked H among D to I, asked for something between
H, G and the thirteenth image, and kept J from the resulting three.

Two cchat positions changed on the way.
- cchat first recommended 2D drawing with SVG and advised against 3D, because the simulation space is 2D and 3D adds
  no information. That recommendation assumed a top-down view. After Hadi's taste turned to a tilted (isometric)
  view with height, cchat revised it: for a tilted view with agents that move between objects, the drawer must work
  out at every tick which shape is in front. Real 3D does this by itself. cchat then favoured three.js with a
  camera without perspective (an orthographic camera). The same scene gives a top-down view by pointing the camera
  straight down.
- cchat first said that 3D would need a 3D model per object. The WareTrack case showed that Opus generates objects
  from code. The cost is lower than cchat had said.

### 5.10 Sim-runs side by side

Hadi's idea for demonstrations: after the layout, setup and scenario are loaded, two copies of the env-pane on the
same triple, for example one with `intention_aware` on and one with it off, so that the screen-user sees both at the
same time. Section 13.2 holds the considerations. Hadi first named it "viz-stage2". After the stage list existed he
assigned it to stage 2, to be resolved there. The label "viz-stage2" is dropped.

---

## 6. Where it landed: the general preferences

### 6.1 Preferred by Hadi

1. The framework gets a web-ui: an own page with a small Python server, without Solara.
2. The web-ui is domain-independent. It does the same for kitting and for dock_loading.
3. The scene is drawn by a JavaScript drawer, not by Plotly. A tick moves existing shapes. The scene is not rebuilt.
4. Run options are fixed for a sim-run. Editing happens before the model is built. Nothing is edited while a
   sim-run is in progress (within T-viz stages 0 to 2).
5. The time of a sim-run is the number of ticks.
6. The technologies are chosen for the full target, not for the first increment. Hadi's words: he does not want
   ccode to build stages 0 and 1 "with some shortcut, easy, simple technologies or web framework and libraries
   solution to just deliver", and to find later that it must be changed. "If threeJS and react is needed later, it
   consider it from beginning." Only the visual design of stage 1 may be a simple first round. The backend is not
   provisional.
7. The work is incremental: the most basic version first, then gradual changes.
8. The reading of the run configuration and the building of the `SimModel` move into a module of their own (7.2).
9. The visual design is left to ccode, within Hadi's described taste (section 10).
10. The records carry this work as T-viz. They say "preferred", not "ruled".

### 6.2 Preferred, replaceable

- An agent's path is a straight line now. Another path method can replace it later. (The page shows whatever path
  the model holds, see 5.4.)

### 6.3 The solara-ui

- Preferred: it stays in the repo as archived. Archived means: nobody updates it with core and model changes,
  nobody guarantees that it runs, nobody deletes it. Hadi's reason: a fallback "in case new one did not finish as I
  want".
- Preferred: the archived status begins when Hadi accepts stage 1a. Until then it is the working visual run and is
  kept working.
- Proposed by cchat, two conditions that "archived" needs:
  1. Archived code must not be able to break the working parts. This is met by 7.2, after which the headless start
     no longer imports Solara.
  2. The records state the status. The README and the roadmap say "archived, not maintained, since <date>" from that
     point, so that a reader does not expect it to work.

### 6.4 The test of domain independence (proposed by cchat, consistent with 6.1 item 2)

Adding a third domain requires no change to the web-ui's code. The web-ui's code (server module and page) contains
no domain name, no object type name and no area id. Everything that the page draws comes from data. Kitting and
dock_loading differ only in the data that the page receives. The page is also independent of Mesa, because it reads
only messages. The server module is the one Mesa-specific part.

Two terms of the framework itself are not domain words: "human" and "robot". The scene drawer may know these two
kinds.

---

## 7. Architecture

### 7.1 The parts

- **The page**: runs in the browser. It draws the scene, shows the panels, and sends requests.
- **The server module**: a small Python program (for example with FastAPI, open). It holds the model object. It
  builds a model from a run configuration. It calls `model.step()`. It reads the model's attributes and writes them
  as messages. It writes files where the page asks for it (later stages).
- **The model**: `SimModel`, unchanged. It stays the only source of the state. A message is a copy of a selection
  of the model's content, written as text (JSON), because JavaScript in the browser cannot read Python objects in
  another process. Nobody writes a message by hand. If the page and the model ever disagree, the model is right.

Hadi asked about this directly: he had thought the information is already inside the Mesa model and the
visualisation takes it from there. That is correct. The messages do not add information. They carry it across the
process boundary.

### 7.2 The shared module (preferred, "I agree")

Parts A and B of section 4.2 (reading the run configuration, building the `SimModel`) move out of `run_mesa.py`
into a module of their own. The three starts each import it.

```
headless:   run file + flags   ->  run configuration  ->  SimModel  ->  loop of N steps
solara-ui:  run file + flags   ->  run configuration  ->  SimModel  ->  Solara page
web-ui:     choice in the page ->  run configuration  ->  SimModel  ->  step on request
```

- Behaviour does not change. The same run file and flags give the same run.
- The headless start no longer imports Solara.
- Open: the module's name and location, and where the headless loop itself lives afterwards.
- This is the first change to existing files. It does not depend on any design choice of the web-ui.

### 7.3 The web-ui as the starting place (Hadi's idea, 5.7)

Phases on the page:
1. Start: one command starts the web-ui. No model exists yet.
2. Choose: the screen-user picks the domain, the layout, the scenario, and the run options.
3. Build: the server builds the model from that choice.
4. Show: the scene appears.
5. Run: play, pause and step advance the model.

What this adds to the server: a **catalogue** request before any model exists. The server lists what the registry
holds: the domains, their layouts, setups and scenarios, and the run options with their choices and defaults. The
page fills its selection widgets from that list. This keeps the page domain-independent, because the list comes
from the registry's discovery (`domains/discovery.py`) and not from the page's code.

A fact, not a choice: the selection is not three free choices. In the repo a scenario declares one setup (`setup`,
required) and its reference layouts (`reference_layouts`). A run on a layout outside the reference layouts is valid
and is never a baseline. The selection panel follows these bindings.

Proposed by cchat, open:
- The screen-user's choice is the same information as a run file: the triple plus the run options. If the web-ui can
  write that choice as a run file, every sim-run configured in the page can be repeated headless, and the framework
  keeps one description of a run. (Listed under "unassigned", section 13.4.)
- Both entries can exist together. Started without arguments, the web-ui opens on the choice. Started with a run
  file, it opens with that run already chosen.
- The rules between run options (4.2) live in the code. The page must not hold its own copy. It takes them from the
  server, for example by sending the choice and receiving the resolved options back.

### 7.4 The clock and the controls

Proposed by cchat, open: the page requests each step. The server never advances by itself.
- Play means that the page sends step requests in sequence, each after the answer to the one before. Pause means
  that it stops sending. This is also how the solara-ui works today (4.1).
- Pause is then a complete freeze of the world: nothing changes until the next request. Hadi's freeze button needs
  no further mechanism.
- The server refuses a step request while another step is in progress.
- With this arrangement plain HTTP requests suffice: one for the catalogue, one to build, one per step, one for
  reset. cchat had first assumed a WebSocket and withdrew that as unjustified. A WebSocket is needed only if the
  server sends without being asked. The choice of transport is open.
- A sim-run with the web-ui produces the same tick sequence as the headless run with the same run configuration.
  The web-ui does not influence the sim-run.

Controls of stage 1a: play, pause, step, reset.

### 7.5 What the env-pane shows before the first step (preferred: alternative B)

The question was what the env-pane shows between the screen-user's choice and the first step. cchat first called
this a "still picture" and then used the standard word "preview".

- Alternative A: no preview. The env-pane is empty until a "build" action.
- **Alternative B (preferred by Hadi):** every change of a choice or a toggle builds the model at once, and the
  env-pane shows its step 0. A separate "build" button is not needed. After the first step the choices lock. Reset
  unlocks them.
- Alternative C: a preview from the files. The server reads the layout, setup and scenario and describes them
  without building a model.

Condition on B, to be measured by ccode: building a model takes about a second or less. The load includes
validation and the load-time replay (`check_script`), which may take noticeable time. If the build time is too long,
the question returns to Hadi. Alternative C becomes relevant in stage 2, where editing needs a picture while no
valid model exists.

### 7.6 Where state lives (cchat's answer to Hadi's question on session state)

"Session state" in plain words is the question of where the edited content lives while the page is open. Three
places exist.

| Place | Lifetime | Use |
|---|---|---|
| The page in the browser | Until the tab closes or reloads | Display only |
| The server's memory (Python objects) | Until the server process stops | The draft and the model |
| Files on disk | Permanent | Saved artefacts, run files, logs |

Session state becomes a real problem only when many people use one server over the internet. This case is one
screen-user and one Python process on the same machine. The server's memory is the session. No login and no
database are needed.

For editing (stage 2), cchat's reading, open: the server holds one **draft** (the chosen layout, setup and scenario
plus the screen-user's edits) in memory. A model is built from the draft. Saving is an explicit act that turns the
draft into artefacts. The repo already has the principle: a small change for one run is an override, and "a change
worth keeping is a new artefact" with its own id. A sim-run from an unsaved draft is a demonstration, because
nobody can repeat it.

---

## 8. The messages (open, parked)

Hadi asked that the backend and the messages be settled before the page design, and trusted cchat to architect the
connection. cchat then proposed contents too early (5.4). The contents below are **proposed by cchat and parked**.
Stage 0.4 settles them.

### 8.1 Two kinds of message (proposed)

The two faults of the solara-ui (4.1) give two requirements.
1. Constant content travels once. The room's areas and fixed objects go to the page when a sim-run is built. They do
   not travel per tick.
2. Per-tick content contains only what can change.

This gives two messages. It matches the repo's own separation: the layout holds the fixed objects, and a run changes
only agents and movable objects.

Clarification: "only what can change" means the complete changing state at each tick (all agent positions, all
movable objects' places). It does not mean differences from the previous tick. With tens of objects, differences add
bookkeeping and no benefit.

### 8.2 Run description (proposed content), sent when a model is built and after reset

| Item | Content | What the page does with it |
|---|---|---|
| The run | Domain and the triple (layout id, setup id, scenario id), and the resolved run options | Shows which sim-run is loaded |
| The space | Its bounds | Sets the size and proportions of the scene |
| The areas | Id and bounds of each | Draws the areas |
| The fixed objects | Id, type, position and size of each | Draws each once. They do not move in a sim-run |
| The movable objects | Id and type of each | Creates one shape per object. Its place comes per tick |
| The agents | Id of each, and human or robot | Creates one figure per agent. Its position comes per tick |

### 8.3 Tick update (proposed content), sent after each step

| Item | Content |
|---|---|
| Step number | The current step |
| Each agent | Its position, the movable object it holds if any, and its planned path as the model holds it (a list of points, empty when the agent is not moving) |
| Each movable object | Where it is now: its container, or the agent holding it |
| Run ended | Yes or no |

Stage 1a adds what panel 4a needs. Stages 1b and 1c add what panels 4b and 4c need. Those additions are not listed
here, because Hadi decides the contents of 4b later.

### 8.4 Points that the message design must cover

- **The sim-run's identity.** Proposed by cchat, following Hadi's principle 6.1 item 6: each message names the
  sim-run it belongs to, so that one sim-run is the special case of several stepped together. Stage 2's
  side-by-side sim-runs then need no redesign.
- **The order of arrival in a container** (section 9, requirement 3). The scene drawer needs it to assign display
  places. Proposed by cchat: the server supplies it. If the page derived it from the tick updates it has seen, a
  page reload in the middle of a sim-run would lose it and the picture would change, which would contradict
  requirement 3. Supplying it does not contradict requirement 6, because the server sends it to the page only and
  writes it nowhere.
- **One definition.** Proposed by cchat: Python defines the messages once, as typed classes, in line with the
  repo's practice of typed dataclasses. The page's types are generated from that definition. A test catches a
  mismatch.
- **Whether a path is world content or mind content.** Not verified: which module writes `planned_path` for each
  kind of agent. If the Mesa body writes it for a movement in execution, it is the route of a movement that is
  happening. If the robot's cognitive layer writes it, the robot's path is what the robot intends. The current
  drawer does not distinguish the two. The human's planned path is in any case something the robot does not know.
- **How the model represents a carried object.** Verified in the slots discussion: a carried object has its
  holder's position (section 9).
- **Facing.** If the agents are drawn as figures with a front (10.5), the drawer needs a direction per agent. Not
  verified: whether the model holds a heading. The usual substitute is the direction of the last movement.
- **"Tick" and "step".** cchat used both as the code does. ccode checks whether the glossary distinguishes them.

### 8.5 A capability that follows at low cost (unassigned, 13.4)

The page can keep every tick update it receives. That gives a timeline that moves back to an earlier tick for
display, without running the model again. Writing the same updates to a file gives replay without Mesa.

---

## 9. Input from the slots discussion (6 October 2026)

Hadi brought the following text from another chat and asked that it be kept with T-viz. It is reproduced verbatim.
"The viewer" in it means the web-ui, and within it the scene drawer of the env-pane.

> INPUT FROM THE SLOTS DISCUSSION (6 October 2026), for the viewer's requirements
>
> Ruling by Hadi, 6 October 2026:
> - Slots in containers (TODO-173) are deferred to the framework's next version.
> - In the current version, the viewer alone spreads the movable objects of one container across that container's
>   footprint. The world does not change.
>
> Facts of the world that the viewer must not contradict (verified in the repo, 6 October 2026):
> - A movable object in a container has exactly the container's position (mesa_sim/sim_model.py at load,
>   executor._execute_release at a release).
> - Several movable objects can be in one container. They then share one position (examples: env_setup_27,
>   env_setup_30).
> - A carried object has its holder's position.
> - An agent's walk to a container ends the body's arrival_radius short of the container's position, the same point
>   for every object of that container.
>
> Requirements for the viewer:
> 1. The viewer draws each movable object of a container at its own display place inside the container's footprint.
> 2. An object's display place is fixed while the object stays in that container. The viewer does not recompute the
>    places of the remaining objects when one object leaves.
> 3. The rule that assigns display places is deterministic: order of arrival in the container, with the setup's
>    order at load. The same run always gives the same picture.
> 4. The rule applies to every container, origins and destinations alike (kitting: shelves and kitting tables;
>    dock_loading: bays and the truck).
> 5. The viewer draws a carried object at its holder.
> 6. The viewer never writes a display place to the world, to a log, or to a layout or setup file.
> 7. The viewer's documentation states that a position inside a container is a display convention and not a world
>    fact.
>
> Known limit, accepted:
> - The agent stops at the same point for every object of a container. In a 3D view the body does not face or reach
>   the drawn object.
>
> Open for the viewer chat:
> - The geometry of the spread (a grid, a row, the spacing, the handling of more objects than the footprint can show
>   without overlap).
> - Whether "display place" needs a glossary entry. It is a working term here, not a glossary term.

cchat's additions, open:
- The text does not say whether the solara-ui also gets this behaviour. cchat assumes that it does not, since the
  solara-ui is to be archived. Hadi did not object. Not confirmed.
- Freed places: requirement 2 keeps the remaining objects where they are when one leaves. The text does not say
  whether a later arrival takes the freed place or the next place after the last one. This belongs to the open
  geometry of the spread.
- The accepted limit is more visible in a tilted view with figure-like agents than in a flat top-down view.
- Where the order of arrival is kept: see 8.4.

---

## 10. The visual direction

### 10.1 Hadi's instruction on design

Hadi does not dictate the web design to ccode. In his words, he is "just offering", and ccode and Opus decide "based
on its fantastic abilities in web designing". ccode should take inspiration from the references and may suggest its
own. Hadi's described taste weighs more than any single image. ccode also decides where configuration lives.

The check on this freedom is the trial in stage 0.3: ccode shows a picture of one real layout before stage 1 builds
on it, and Hadi reviews it.

### 10.2 Hadi's taste, in his words

- "Something minimal yet elegant."
- For the kitting and dock_loading environments: something similar to images 4 and 12, also to 3, 10 and 9 "with
  less coloring. And less realistic... Still modern and not flat as 2D".
- "I like 4, and like the basic plan-drawing style but a bit of illustrations with few colors helps, maybe isometric
  as it apparently called. 3D is fine with height... At the end, it is abstract and conceptual illustration."
- "I want something between 4 and others."
- On sketch J: "J looks more academic minimal classy. We keep it, and maybe still a bit more to lines drawing A of
  BG or static objects." ("BG" is the background.) Sketch K he also finds nice.
- On the page as a whole: in the WareTrack example he noticed that the widgets and components are harmonised with
  the illustrations of the simulation. His reading: all page elements and the scene of the env-pane can be under one
  uniform theme or palette.

### 10.3 The reference images

The files are in `docs/handoffs/tviz_refs/`. The numbers are the ones used in the chat. They are third-party images
(screenshots of posts and stock illustrations). They serve as inspiration only. If the repository is public, the
folder should stay out of version control.

| No. | File | What it is | Hadi's relation to it |
|---|---|---|---|
| 1 | `ref01_robot_simulator_page_layout.jpg` | A robot-arm simulator page by Dilum Sanjaya (built with Gemini 3, look generated with Nano Banana). A central "3D simulator area", panels on both sides (gauges, charts, sliders), a time-control panel with play, pause, stop. Grey with one orange accent in both panels and scene. | Not picked for style. cchat noted that its page layout is the closest of the set to Hadi's stated minimum. |
| 2 | `ref02_orange_white_isometric_closeup.jpg` | An isometric logistics scene, white and light grey with orange buildings (Ian, @ianneo_ai), close view. | Shown, not picked. |
| 3 | `ref03_isometric_warehouse_room.jpg` | A stock isometric illustration of a warehouse room with racks, pallets, pallet jacks, barrels. | Named with 10 and 9 as "similar, with less colouring and less realistic". |
| 4 | `ref04_line_drawing_plant_opus55_threejs.jpg` | A monochrome isometric line drawing of a plant with trucks and bays, labels written on the ground ("BAY 1", "IN", "OUT"). Caption: built with Opus 5.5, Three.js and WebGL (Khalid). | **Liked. The main reference for the line style.** |
| 5 | `ref05_detailed_logistics_isometric.jpg` | A detailed, many-coloured isometric logistics illustration. | Shown, not picked. |
| 6 | `ref06_colourful_isometric_shops.jpg` | A colourful outlined isometric illustration of shop containers. | Shown, not picked. |
| 7 | `ref07_orange_white_isometric_city.jpg` | The scene of image 2 from further away. | Shown, not picked. |
| 8 | `ref08_teal_isometric_city.jpg` | A flat isometric city in teal, white and grey (Beth Goody). | Shown, not picked. |
| 9 | `ref09_waretrack_dashboard.jpg` | WareTrack (Dilum Sanjaya, Opus 5.5, React and React Three Fiber). Soft 3D warehouse with panels over it. | The first example of the chat. "Not as advanced as this." Named again for the harmony of widgets and scene. |
| 10 | `ref10_isometric_shelf_rack.jpg` | A stock isometric illustration of a shelf rack with boxes. | Named with 3 and 9. |
| 11 | `ref11_minimal_hatched_line_drawing.jpg` | A minimal isometric line drawing of a car on a road, with dotted hatching on the side faces and one coloured object. | Not picked directly. It is the source of sketch H, which Hadi picked. |
| 12 | `ref12_l_shaped_warehouse_flat_isometric.png` | "L-shaped Warehouse Layout" (The Retail Exec). Flat filled faces in one blue, black and white on a pink ground, labels in black rounded boxes joined to their place by a thin line with a dot. | **Liked**, with image 4. |
| 13 | `ref13_mining_software_soft_3d.jpg` | A mining-software scene (Rish Dodhia, @tradphi). Near-white ground, pale shaded faces without hard outlines, one soft blue on the tops, soft ground shadows, small white labels with a status dot next to the objects. | Hadi asked for "something between H and attached and G". |

What cchat observed in the set:
- Eleven of the first twelve show an isometric view: three-dimensional, seen from above at an angle, without
  perspective. Parallel lines stay parallel and an object keeps its size wherever it stands. The architects' name
  for the family is axonometric drawing. Isometric is one member.
- Images 4 and 12 share: almost only boxes and flat planes, no gradients or textures, a very small palette, emphasis
  by contrast (in 4 the solid black cargo, in 12 the blue), much empty space, consistent line weights.
- "Elegant" in both comes from discipline, not from added detail: one line weight, few colours, aligned labels, one
  typeface. These are rules of the theme, so they apply to the panels as much as to the scene.
- The two label styles map onto two things of the glossary: labels on the ground suit areas, and joined label boxes
  suit objects and agents.
- The small labels of image 13 (a short id plus a coloured dot for a state) suit an object's id and one of its
  states.

### 10.4 The sketches A to L

cchat drew the same small room (a shelf, a table with one item, a marked area on the floor, two agents) in twelve
treatments. They were hand-made 2D drawings with invented positions and plain boxes. They compared treatments. They
are not output of any library and not a target quality. `tviz_refs/sketch_A_and_J.svg` holds A and J.

| Sketch | Treatment | Outcome |
|---|---|---|
| A | Lines only, no colour (image 4) | The direction for the background and static objects |
| B | Lines plus pale face shades, colour on a few things only | cchat's first "between" |
| C | Filled faces, no outlines, strong colour (image 12) | |
| D | Blueprint: light lines on a dark ground | Not picked |
| E | Objects as open frames, agents solid | Not picked. It addresses hiding: nothing conceals an agent |
| F | No outlines, soft colours, flat floor shadows | Not picked |
| G | Greys only, one accent colour for the things that matter | Named by Hadi as one end of the blend |
| H | Hatched side faces, outlines, one coloured thing (image 11) | **Picked among D to I** |
| I | Objects almost flat, agents stand up, labels joined by lines | Not picked |
| J | Soft lines, light hatching on the shaded side, near-white ground, floor shadows, one accent colour for the robot and its item, labels with a status dot | **Kept as the reference style** |
| K | No lines, pale shaded faces, a soft blue top, shadows, several soft colours, labels | Also liked. An alternative, not the reference |
| L | Greys, hatching on the shaded side, one accent, no outlines | Not picked |

The properties that the sketches vary are separate: line or fill, light or dark ground, how depth is shown (line
geometry, face shades, hatching, shadows), how much colour, how tall the objects are. A final style is one choice
per property.

### 10.5 The reference style as it stands (preferred, with Hadi's adjustments)

- Base: sketch J.
- Adjustment: the background and the static objects move further toward the pure line drawing of A.
- A tilted view with height. 3D is acceptable. Hadi's word in the stage list: "minimal 3d".
- The purpose is an abstract, conceptual illustration, not a realistic picture.
- **Agents** (human, robot, worker, autonomous lift truck) can be a bit illustrative: "not realistic, but also not a
  plain shape". Hadi's later examples: a human with a circle head, a robot with a cube head. He may attach further
  images to borrow elements from.
- **Active and passive objects** (Hadi's idea, 6 October). Environment objects are passive or active. Active does
  not mean movable. It means that the object plays a role in the behaviours and activities of the agents. His
  example: the coffee machine is an active object. The visualisation gives active objects more presence, for example
  3D with a specific shape, "a bit of abstract and conceptual but still representative of their meanings". Hadi
  added that this need not be dictated to ccode, which may use its own abilities and imagination.

cchat's reading of these together, three levels of presence (proposed):

| Level | What | Treatment |
|---|---|---|
| Background | The space, the areas, the passive objects | Line drawing |
| Active objects | Objects that take part in activities | 3D, a representative abstract shape |
| Agents | The human, the robot | Illustrative figures |

An observation of cchat that Hadi has not marked: with static things drawn as lines and changing things drawn with
fill and colour, the drawing states by itself what can change during a sim-run.

### 10.6 Points that the style raises (proposed by cchat, open)

1. **Recognisable shapes against domain independence.** A rack is readable because it looks like a rack. A drawer
   that may not name object types cannot draw "a rack". A middle way: the drawer knows a small set of generic shape
   kinds (for example a solid block, an open frame, a flat marked zone, a low platform), and data states which kind
   each object type uses. The drawer's code then knows geometry and no domain word. A lift truck is one possible
   body of the robot in one domain, so the robot's figure would also be chosen by data.
2. **Where the look comes from.** Hadi's preference (question 1.4): a visualisation configuration per domain,
   "domain-customised visualization config file", read only by the web-ui. It maps an object type to its look (a
   shape kind, a height, a palette entry) and names the robot's figure. A type without an entry falls back to a
   default, so a new domain works without a file. ccode decides its location and form. cchat advised against
   appearance fields in the layout files: the simulation reads those files, and the look is not a fact of the world.
3. **Height is missing.** The layout gives each fixed object a position and a size on the floor. It gives no height.
   A tilted view needs one per object, from a default or from the configuration of item 2.
4. **Where "active" comes from.** If a person marks objects by hand for the look, the marking can disagree with the
   world. The data already contains the answer: an object is active when a task of the domain or a script of the
   scenario refers to it. ccode can derive it by such a rule. Hadi did not mark this.
5. **Hiding.** In a tilted view a tall object can hide an agent behind it. A top-down view hides nothing. For a
   research tool this matters more than for a showcase. Outlined and see-through objects, and low heights, reduce
   it. With real 3D a top-down view is the same scene with the camera pointing straight down, so the two views need
   not exclude each other.
6. **The size of agents.** At room scale an agent is small on the screen. A figure of five to ten simple shapes is
   about the most that stays readable. A figure can show what it carries (a worker with an item, a lift truck with a
   pallet), which is more readable than a label.
7. **Facing.** See 8.4.

### 10.7 Theme and colour

- A theme (or design system) is page-wide by definition: colours, spacing, type sizes, borders and corner shapes of
  all panels and widgets, light or dark mode. Its values are called design tokens.
- The env-pane's frame follows the theme like any panel. The scene additionally needs rules that no other panel
  needs: how the things of the simulated world look. cchat called this the scene appearance.
- Hadi's reading: one uniform theme or palette can cover every page element and the scene. cchat agreed. In the
  WareTrack images the harmony comes from identifiable choices: one accent colour in both places, few hues in total,
  one background family, one shape language (rounded corners and soft shadows on panels and on objects).
- Proposed by cchat: one shared file for the theme's values, existing from the first version, so that gradual
  redesign stays consistent. Its values can change at any time. The scene takes its colours only from the theme's
  palette.
- Proposed by cchat, **semantic colours**: a colour is reserved for one meaning and used for that meaning everywhere
  on the page. For example the robot's colour marks the robot in the scene and also the panel and the values that
  concern the robot. In WareTrack the colours are mostly decoration and brand. Here colour also carries meaning:
  which agent is the human and which the robot, later what belongs to the robot's mind. A nearly monochrome scene
  leaves colour free for this. The colours must be clearly distinguishable from each other, not only pleasant
  together.

### 10.8 Technology for the scene (open, to be chosen in stage 0.3)

Background that cchat gave Hadi:
- WebGL is a programming interface built into browsers that lets JavaScript draw with the graphics processor inside
  one canvas element. It is low-level. three.js is a JavaScript library on top of it (scenes, cameras, lights,
  shapes, materials). React Three Fiber lets a React page describe a three.js scene as components. WebGPU is the
  newer successor of WebGL, and three.js can use either.
- 2D counterparts: SVG (each shape is an element of the page, simple, clickable, suited to tens or hundreds of
  shapes), Canvas 2D (shapes drawn by commands), PixiJS (a 2D library on WebGL for thousands of shapes).
- The theme and palette do not depend on the drawing technique. Every technique takes its colours as values.

cchat's position at the end of the chat: for the tilted view with moving agents, three.js with an orthographic
camera, on a React and TypeScript page. Outlines, flat pale faces and hatching are standard capabilities of 3D
libraries (object edges drawn as lines, a hatch as a surface pattern), so style J is not tied to one technique.
Hadi's answer on the library: "later let's see what actual web library can give us something similar". The trial of
stage 0.3 answers it.

The page reads only messages. The scene component is therefore replaceable later without touching the server.

---

## 11. The page layout

### 11.1 Hadi's suggestion for stage 1 (offered to ccode, not dictated)

Hadi's words: "for web design, i will not rule anything to ccode, just offering, let ccode and opus decides".

| Part of stage 1 | Hadi's suggested place |
|---|---|
| 1. Selection of layout, setup and scenario | A panel on top, page-wide |
| 2. Toggles of the run options | A page-wide panel below the selection panel |
| 3. The env-pane | Below those panels, 3/5 of the page width |
| 4a. The human and the actual world | A panel (not a sidebar) on the left, 1/5 of the page |
| 4b. The robot's mind | A panel (not a sidebar) on the right, 1/5 of the page |
| 4c. Plots | A page-wide panel under 3, 4a and 4b |

### 11.2 cchat's observations on it (for ccode)

- The world on the left, the robot's mind on the right and the env-pane between them is a clear arrangement.
- The controls (play, pause, step, reset) and the step number have no place in the suggestion yet.
- Height: two page-wide panels above and one below leave little height for the env-pane on a laptop screen. The
  selection and toggle panels are needed mainly before the first step. They could shrink to one summary line once
  the choices are locked.

### 11.3 An earlier question that Hadi's suggestion mostly answers

cchat had asked where the two phases (choosing a sim-run, watching it) live: on two screens, on one screen with a
setup panel, or on one screen with a dialog. cchat recommended one screen. Hadi's suggestion is one screen with the
selection on top. With alternative B of 7.5, choosing and watching are states of the same screen.

### 11.4 How to specify behaviour, not only the static layout

Hadi asked how web designers sketch what happens ("first this, then if click this appears, this changes to this").
The standard tools:

| Tool | What it shows |
|---|---|
| Wireframe | The static layout of one screen or state, as boxes and labels without styling |
| User flow | A person's path through the application, as a flowchart |
| Wireflow | Wireframes joined by arrows. Each arrow starts at the widget that is clicked and names the action |
| Storyboard | One typical use from start to end, as wireframes in a row |
| State diagram | Every state the page can be in and every event that changes the state |
| Annotations | Numbered marks on a wireframe with a note each, for the behaviour of single widgets |
| Clickable prototype | A mock page in which the clicks work |

What Hadi described is a wireflow, supported by a state diagram. The state diagram matters here because it maps
directly to code and tests, and because it matches the server's own states. An illustration of the method (not a
design): states "nothing chosen", "chosen, at step 0", "playing", "paused", "ended". "Choose a scenario" leads from
the first to the second. "Play" and "pause" alternate. "Reset" leads from any later state back to step 0 and unlocks
the choices.

Hadi said that he will share his own page-layout ideas to explore. Apart from 11.1 he has not yet done so.

---

## 12. The stages

Hadi defined the pipeline on 6 October 2026. cchat added what was missing. Hadi answered a numbered list of
questions. cchat then showed a consolidated list and a tree. Hadi raised no objection to either and moved on to ask
what comes next. He did not explicitly confirm the consolidated list.

### 12.1 The tree

```
T-viz: the web-ui
│
├── Stage 0: foundation
│   ├── 0.1 Recording
│   │   ├── this handoff, placed in the repo by Hadi
│   │   ├── entries in the other records, written by ccode
│   │   ├── terms: web-ui, solara-ui, screen-user, env-pane, scene
│   │   ├── relation to T-E, Phase 7 (T-V), T-L's run-file panel, TODO-110
│   │   ├── input from the slots discussion
│   │   └── open questions of stages 2 and 3
│   ├── 0.2 Code structure
│   │   ├── own module: read the run configuration, build the SimModel
│   │   ├── three starts: headless, solara-ui, web-ui
│   │   └── headless no longer imports Solara
│   ├── 0.3 Trial of the style
│   │   ├── one real layout, drawn without motion
│   │   ├── choice of page framework and drawing library, for the needs of all stages
│   │   └── review by Hadi
│   └── 0.4 Messages between server and page
│
├── Stage 1: the first web-ui
│   ├── 1a Sim-run in the browser
│   │   ├── selection: layout, setup, scenario (predefined only)
│   │   ├── toggles and selectors: all run options
│   │   ├── every change builds the model, env-pane shows step 0
│   │   ├── controls: play, pause, step, reset
│   │   ├── env-pane, first version
│   │   │   ├── minimal 3D in the style direction
│   │   │   ├── movable objects spread inside a container (section 9)
│   │   │   ├── planned paths
│   │   │   └── visualisation configuration per domain
│   │   ├── panel 4a: the human and the actual world
│   │   ├── shared theme file
│   │   ├── tests: same result as headless, a third domain without code change
│   │   └── on Hadi's acceptance: the solara-ui becomes archived
│   ├── 1b Robot's mind
│   │   └── panel 4b: belief, decision, current task, last plan change (contents decided later)
│   └── 1c Plots
│       ├── panel 4c: plots over ticks, growing during the sim-run
│       └── the timeline of context facts, where one exists
│
├── Stage 2: editing and comparison (questions recorded, decided when reached)
│   ├── 2.1 Editing layouts, saved as new ones
│   ├── 2.2 Editing setups, saved as new ones
│   ├── 2.3 Editing scenarios: the human's script, the timeline of context facts
│   └── 2.4 Sim-runs side by side
│
├── Stage 3: changes during a sim-run (questions recorded, decided when reached)
│   └── 3.1 Events, interruptions and deviations of the human's script
│
└── Unassigned
    ├── inspect an object during a pause
    ├── automatic pause at an event of the robot's cognition
    ├── move back along the ticks
    ├── replay without Mesa
    └── save the page's choice as a run file
```

The numbers inside stage 0 and stage 2 are cchat's, for reference. Inside stage 2 cchat split Hadi's one editing
item into three, one per artefact, because they differ in difficulty.

### 12.2 Stage 0 in Hadi's words, and the order of work

Hadi's stage 0:
1. "recording everything we discussed into repo as a doc and in decision docs".
2. "fix skeleton and architecture of code to start runs of headless, solara (direct sim-run) or web-run start that
   have choosing and loading model etc".

Added by cchat and accepted in the answers: the trial (Hadi's answer 0.2: "yes, i think so", with the principle of
6.1 item 6) and the message design (accepted without comment as part of the list).

How 0.1 changed: cchat first planned a prompt that has ccode write the whole record. Hadi then proposed that cchat
write this handoff with everything that helps ccode, including the discussions, doubts and progress, that he place
it in the repo's docs, and that the 0.1 prompt ask ccode to carry the decisions into the other files.

Order proposed by cchat:
1. 0.1 Recording.
2. 0.2 Code structure. Independent of every design choice.
3. 0.4 Messages. Needs a short design round with Hadi first.
4. 0.3 Trial. Last in stage 0, because it can use the start from 0.2 and real data in the form that 0.4 defines.

The trial judges each candidate technology against the needs of all stages: the style of section 10 in 3D, panels,
plots that grow during a sim-run, later editing inside the scene, later two env-panes.

What Hadi sees first: the trial shows one real layout in the style, without motion. After stage 1a he starts the
web-ui, the browser shows the page, he chooses a sim-run, and the agents move in the env-pane under play, pause and
step. He asked exactly this ("after stage1a there will be a very first web-run to see something on web browser?")
and cchat confirmed it.

### 12.3 Stage 1 in Hadi's words

1. "stage 1 only accept loading predefined layouts and [setups] and scenarios (edit is stage2)".
2. "stage1 allows toggling arguments of x_aware".
3. "stage1 makes first version of env-pane visualization, simple yet in the preferences I asked (minimal 3d)".
4. "stage1 will have three parts of information to show:
   a. human and actual world info, what human is doing (from script), but I guess info comes from some objects of
      core or simulation
   b. robot mind (what robot now believes, what its current decision, what is current task, what it changed last as
      adaptive plan, etc, we decide later what to list)
   c. still from robot mind and maybe from world, but something we do not list descriptive in (b) instead show as
      graph of timeline/ plots. ticks of simulation on x-axis in subplots, then something similar to what analysis
      and test was saving as figures... Also plot of given timeline facts as context knowledge if any is
      available... these plots will incrementally update as simulation runs".

Changes from the answers:
- The toggles cover **all** run options, not only the two "aware" options (Hadi: "all, why not, we do not need to
  postpone this").
- Stage 1 is split into 1a, 1b and 1c (Hadi: "your stage1a, stage1b, stage1c is fine"). cchat's reason: earlier
  Hadi wanted a skeleton first and the robot's mind as a second task. The stage list put both, plus live plots, into
  one stage. The split restores the increments.

Pointers for the three information parts. These are cchat's guesses at sources, not verified, to help ccode start.
- 4a: the human executor's stack and record (`world/human_executor.py`, `world/queries.py`: `truth_at`, `switches`,
  `resumptions`, `assigned`, `unperformed`, `coverage`; the `[rec]` stream in `logs/run_<timestamp>.rec`).
- 4b: the recognizer's belief over the live task hypotheses, the adequacy finding (unresolved, adequate,
  unexplained), the lifecycle state, the gate's admission, `UpdateResult` (with `hold` and `queue`), the robot's
  current task. Hadi decides the list later.
- 4c: the figures that the analyses save. T-F part 1 produced "one figure per run on one tick axis" (ruling N,
  `analysis/kitting/tf1/REPORT.md`). The timeline of context facts is the setup's optional `"timeline"` or the
  scenario's own (`ScenarioConfig.timeline`, T-K part 1).

The world's vocabulary and the robot's mind's vocabulary stay separate on the page, as the glossary defines them.
Panel 4a shows what the human does. Panel 4b shows what the robot believes.

Items of stage 1a that cchat added and that follow from earlier statements: the controls, the spreading of movable
objects (section 9), planned paths (5.4), the shared theme file (10.7), the two tests, and that a sim-run from the
web-ui writes the same logs as a headless one.

### 12.4 Hadi's answers to the numbered questions

| No. | Question | Hadi's answer |
|---|---|---|
| 0.1 | When does the solara-ui's archived status begin? | B: when he accepts stage 1a. |
| 0.2 | Does a trial of the style on one real layout belong in stage 0? | Yes. With the principle of 6.1 item 6. |
| 0.3 | Under which name do the records carry the work? | T-viz. |
| 1.1 | The split into 1a, 1b, 1c? | Accepted. |
| 1.2 | Which run options do the toggles cover? | All. |
| 1.3 | What does the env-pane show before the first step? | B: every change builds the model, step 0 is shown. |
| 1.4 | Where do an object type's look and height come from? | A per-domain visualisation configuration is fine. The active and passive idea (10.5). The design and the place of the configuration are left to ccode. |
| 2.x, 3.x | The questions of stages 2 and 3 | Record them as open. "We decide later when we reach the stages." |
| 4.1 | Where do the side-by-side sim-runs belong? | Stage 2, resolved then. |
| 4.2 | Did "stages" mean setups? | Yes. |

---

## 13. Later stages and unassigned items

### 13.1 Stage 2, editing: open questions

Hadi's words: "stage2 will allow editing of layouts (scene arrangement, add/remove objects etc), [setups]
(placements etc) and scenarios (scripted human behaviour, editing context timeline facts, etc), save them as new
ones".

- **The three existing override kinds** (an agent's start position, a fixed object's position, a movable object's
  home container; `mesa_sim/overrides.py`). The solara-ui's run-file panel offers them today. Open: whether the
  web-ui offers them in stage 1 or in stage 2. The Python logic is reusable.
- **Scripts have no typed textual form.** Layouts and setups are JSON files, so saving an edited one is simple.
  Scenarios are Python literals (`ScenarioConfig`), and the records state that a task instance has no typed textual
  form. Editing a human's script in a page needs a structured form of scripts that the page can show, change and
  write back. That is a core design matter, not a web matter. cchat proposed that stage 2 begins with layouts and
  setups, and that scripts follow after that core step. Not answered.
- **The draft and its saving** (7.6). An edited artefact is saved as a new artefact with its own serial id, by the
  repo's rule that a change worth keeping is a new artefact.
- **A preview without a model** (alternative C of 7.5). While the screen-user edits, the draft may not load.
- **Validation.** The loader validates a triple at load. The page shows the loader's error when a draft fails.
- **The existing layout tool.** `scripts/layout_tool.py` draws a layout as a PNG and derives a new layout by
  dragging its fixed objects (`scripts/README.md`). Its relation to stage 2.1 is open.
- **TODO-110**, selection by composition and coverage, for the selection panel.

### 13.2 Stage 2, sim-runs side by side: considerations

Hadi's idea (5.10). His expectation: the two sim-runs are fully isolated, each with its own cognitive instances.

Three ways to have them:

| | 1. A mode inside the web-ui | 2. Two tabs, one server | 3. Two starts, two windows |
|---|---|---|---|
| Models | Two `SimModel` instances in one server | One per tab | One per server |
| Controls | One set. One step request advances both | One set per tab | One set per window |
| Same tick in both | Guaranteed | Not guaranteed | Not guaranteed |
| Work | An addition to the server and the page layout | The server keeps one model per tab | None |

cchat's view: the mode is the better form for a demonstration. The comparison is meaningful only at equal ticks. A
pause freezes both, so one can point at the moment where the two robots start to differ. Way 3 works from the first
day for a first demonstration.

Isolation. Each `SimModel` creates its own agents, and each robot its own recognizer and planner. Two objects in one
Python process are still isolated only if the code keeps nothing shared. Four kinds of thing can be shared inside
one process and are not visible from the instances:
- a random number source used through Python's global `random` or NumPy's global generator,
- a variable at module or class level that the code changes during a sim-run (a cache, a counter),
- a registry that the load modifies,
- one fixed file name for a log.

None of these is verified. Two processes are isolated in any case, at the cost of passing requests and tick updates
between them.

A decisive check, proposed by cchat: ccode steps two models alternately in one process and compares each one's log
with the log of the same sim-run executed alone and headless. Identical logs show isolation. A difference shows
where the shared state is. The check has value beyond this mode: a shared random source or cache would also be a
reproducibility fault of the framework.

To define when the stage is reached: what may differ between the two sides (Hadi's example differs in one run
option, with the same triple), what happens when one sim-run ends earlier (the usual answer: it stays at its last
tick while the other continues), and the page layout with two env-panes and panels that belong to one side.

A limit to state plainly: the side-by-side view demonstrates. Evaluation numbers come from headless sim-runs.

### 13.3 Stage 3, changes during a sim-run: open questions

Hadi's words: "stage3 will allow interactive changes while sim-run, like adding events and interruptions and
deviations to human scripted behaviours".

- Hadi said earlier that changing the human's behaviour during a sim-run is a separate task, already in the records
  (Phase 7, T-V). cchat's reading, not answered: stage 3 is the page's side of that task, and the mechanism (the
  human executor's injection path, the replay rule, the event log) stays in that task.
- The web-ui's architecture leaves room for it: the server already holds the model, so a later "inject" request is
  an addition.

### 13.4 Unassigned

Raised in the chat, with no stage.
- Clicking an object or an agent during a pause to inspect it.
- An automatic pause at an event of the robot's cognition (a cognitive-clock event), to show the robot's decision
  at that tick. An earlier chat designed this for the solara-ui (pause on `theta_crossed` and `task_committed`). Not
  verified whether it was built.
- Moving back along the ticks for display (8.5).
- Replay of a finished sim-run without Mesa (8.5).
- Saving the page's choice as a run file (7.3).
- Hadi's global freeze button. With 7.4 it is the pause.

---

## 14. Working practices for the build (from the search reports, proposed by cchat)

1. Build the page against mock data first. The look and the page layout are judged before a connection to Mesa
   exists. Visual acceptance and functional acceptance become two separate checks.
2. Give a visual reference instead of adjectives. The reference images and sketch J serve this. Anthropic's guide
   for Opus 5.5, as ChatGPT reported it, says that "avoid a generic look" is too weak and that a prompt should name
   the patterns to avoid (not verified by cchat).
3. ccode checks screenshots of the page in a real browser. Passing tests do not show that the page looks correct.
4. The spacing scale, the type sizes, the colours and component examples are written into one project file, so that
   the look stays consistent over many sessions.

Two tests that cchat proposed for stage 1a:
- A sim-run through the web-ui's server gives the same result and the same logs as the headless run with the same
  run configuration.
- A domain that the web-ui's code has never seen (a small test domain) is drawn without a change to the web-ui's
  code.

Risks that cchat named to Hadi:
1. The look of the page can consume unbounded time. Each increment needs a written scope.
2. Two languages in one repository, with a Node.js toolchain and a build step that Hadi must be able to run.
3. Appearance against domain independence (10.6).
4. The work competes with T-K and T-G for Hadi's attention.

---

## 15. cchat's proposals that Hadi has not marked

They appear in the sections above. They are collected here so that nobody takes them as preferred.

1. The page contains no simulation logic. The page requests each step, and the server never advances by itself.
   (Hadi agreed with consequences of this: pause as a freeze, 5.6, and no straight-line computation in the page was
   not contested, 5.4.)
2. Constant content travels once, and each tick sends the complete changing state (8.1).
3. The server supplies the order of arrival in a container (8.4).
4. A colour is reserved for one meaning across the whole page (10.7).
5. "Active" is derived from the data: an object that a task or a script refers to (10.6).
6. Plain HTTP requests for the transport (7.4).
7. React with TypeScript for the page, three.js with an orthographic camera for the scene (10.8). The trial decides.
8. The messages are defined once in Python, and the page's types are generated (8.4).
9. Each message names its sim-run (8.4).
10. The rules between run options stay in the server (7.3).
11. Stage 2 begins with layouts and setups, and scripts follow after a core design step (13.1).
12. Stage 3 is the page's side of Phase 7 (13.3).

---

## 16. What ccode does first (0.1), and what it verifies

### 16.1 The task

Recording only. No code changes.

- Read this handoff in full.
- Verify the facts listed in 16.2 by reading the repo. Report every difference between this handoff and the repo.
- Carry what belongs in the repo's records into them: the roadmap, the record of planning and building, the
  glossary where a term needs an entry, the list of TODOs and deferred items, CLAUDE.md's pointers. Follow
  CLAUDE.md's rule on where a record goes. Use the status words of section 1.1. Do not turn a "preferred" or a
  "proposed by cchat" item into a ruling.
- State the relation of T-viz to T-E, to Phase 7 (T-V), to T-L's run-file panel and to TODO-110.
- Record the open questions of stages 2 and 3 as open.
- List every place where the records or the code use "viewer" for the program. Do not rename anything.
- Propose glossary entries for the terms of 2.1 and 2.4 that need one. Hadi decides which are added.

### 16.2 Facts to verify

1. The current state of T-E in the roadmap and the handoffs. Whether it is still an open task.
2. The behaviour, in `SimModel`, of the dependencies between run options (4.2), and whether the model exposes the
   resolved options.
3. Which module writes an agent's `planned_path`, for the human and for the robot (8.4).
4. Whether the model holds a heading or facing for an agent (8.4).
5. The time to build a `SimModel`, for a small and a large scenario of each domain (7.5).
6. Whether the roadmap's Phase 2.2 line on "task progress, belief state display" matches the code (4.3).
7. Whether a headless run is affected by an import fault in the Solara modules today (4.2).
8. Whether the glossary distinguishes "tick" and "step", and whether it has an entry for "author" and for "viewer".
9. Whether the pause on cognitive events from the earlier chat exists in the code (13.4).
10. Whether the model or the cognitive layer keeps shared changing state outside the model object (13.2). A reading
    check is enough for 0.1. The decisive check with two models belongs to stage 2.
11. The vendored Mesa fork's version (4.1).
12. Which run files, logs and record streams a sim-run writes, and from where, so that 7.2 can keep them identical.

---

## 17. Reference material

- `docs/handoffs/tviz_refs/ref01_...` to `ref13_...`: the reference images of section 10.3.
- `docs/handoffs/tviz_refs/sketch_A_and_J.svg`: cchat's sketches A and J (10.4).
- The earlier chat "Mesa fork and Solara compatibility" (29 September 2026) held the first comparison of options A
  and B. Hadi deleted it. Its content is in 5.1.
- The slots discussion: TODO-173. Section 9 holds its input.

---

## Correction note (ccode, 6 October 2026, T-viz 0.1)

The body above is left as written. Where it and the repo differ, the repo wins. Read at commit 069282b; the detail,
with files and lines, is in `docs/design_records.md`, "T-viz, the web-ui", 0.1.

- Sections 4, 10.3, 17: the reference images and `sketch_A_and_J.svg` are in `docs/handoffs/tviz_refs/` since 4e71335,
  as stated here. The repository is public and the images are committed and pushed (069282b, 4e71335), so the
  third-party images are in version control, against 10.3's condition.
- 4.4: T-E is not an open task. It was superseded by T-V track 1 on 30 September 2026. T-V track 1 ("the viewer for
  pre-loaded scripts") is the existing record of the viewer as a task; the handoff names T-V for track 2 only.
- 5.4, 8.4, 12.1 ("planned paths"): no module writes `agent.planned_path`. The drawer reads it behind a `hasattr` guard
  and draws nothing; the model holds no path per agent under that name. "Today that path is a straight line" does not
  hold. Where a path can be copied from is a question for 0.4.
- 8.4 (facing): no agent holds a heading. The robot's mind keeps the observed human's last step direction (a
  perception fact), not a facing.
- 4.1: no framework code sets `model.running`, which the fork initialises to True, so the solara-ui's play does not
  stop at a run's end.
- 4.4: Phase 7's deviation "applied at the next action boundary" is superseded in part by T-H. Events may cut
  mid-action (`DuringAction`).
- 4.2 and 7.2: besides A, B and C, `mesa_sim/run_mesa.py` opens the run log and the `.rec` stream at import, once per
  process. The start line, the override lines, the per-step agent lines, `[sep]` and the run's end (`end_run`) are
  written by `run_headless()`, not by the model, so the solara-ui writes none of them.
- 2.2: "viewer" for the program occurs about 110 times in the records and code, not in three places only.
- 13.4: the earlier chat's pause events `theta_crossed` and `task_committed` no longer exist (D2, D3). No pause on a
  cognitive event was built.
- 7.5's condition is measured: a `SimModel` builds in 1 to 6 ms (one outlier of 68 ms) over all 1019 registered
  scenarios, after a one-time import of about 1.7 s.
