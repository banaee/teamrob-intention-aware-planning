# The web-ui's page (T-viz)

Stage 1a, increments (i) to (iv): the page served by the web-ui's server (`webui/server.py`, started by
`mesa_sim/run_webui.py`). The frame of the page for the whole of stage 1 (the selection on top; the human and the world,
the env-pane with its control bar, the robot's mind; the plots below); the choice by domain, layout, setup and scenario,
a layout or a layout and setup drawn before a scenario is chosen, every run option, the choice mirrored in the address;
the env-pane drawing the current sim-run tick by tick under play, pause, step and reset, its camera at two presets or
moved freely; panel 4a, what each human does (the action in hand, the stack, the last switches and resumptions).
The plan: `docs/handoffs/plan_T-viz_1a.md`; the records: `docs/design_records.md`, "T-viz, the web-ui".

## Run it

Needs Node.js 22.12 or later (`node --version`); every dependency is pinned in `package.json` and `package-lock.json`.
From the repository's root:

```bash
# build the page: once, and after a change of the page's sources (the start stops when the build is older)
cd webui/page && npm ci && npm run build && cd ../..

# the web-ui, at http://127.0.0.1:8000/ (the headless start's run file and flags, and --port)
PYTHONHASHSEED=0 ~/python-envs/ir-nomesa-env/bin/python mesa_sim/run_webui.py
```

While working on the page: the server as above, and Vite's dev server (`npm run dev`, http://localhost:5173), which
passes `/api/` to the server on port 8000.

Screenshots in the installed Google Chrome, driving a running web-ui: `npm run shots -- --runs '[["<domain>",
"<scenario>"], ...]'` writes them to `docs/handoffs/tviz_1a/` (untracked): per sim-run its start chosen in the page, a
moment after 60 steps (tilted, from above, and at 1920 wide), play until all agents have finished, and an end at a step
limit.

The page's unit tests: `npm test` (vitest).

After a change of `webui/messages.py` or `webui/appearance.py`, regenerate the page's types:
`~/python-envs/ir-nomesa-env/bin/python -m webui.schema`, then `npm run gen:types` here.

## What is where

- `src/App.tsx`: the page's state and its frame; the play loop (one step requested after another, pausing by itself
  on the tick at which all agents have finished).
- `src/api.ts`: the requests to the server. The server holds every rule; the page asks and draws the answers.
- `src/frame/`: the selection panel (`selection.ts` the offer), the control bar, panel 4a (`activity.ts` its reading
  of the human's activity).
- `src/opening.ts`: what the page opens on; `src/address.ts`: the address.
- `src/theme.ts`: the theme, the one file of colours, line weights, spacing and type sizes; the page's CSS and the
  scene read it.
- `src/env-pane/`: the env-pane. `Scene.tsx` draws one tick from the run description, the tick update and the scene
  appearance (what is constant once per sim-run; the agents glide between two ticks during play); `forms.tsx` the shape
  vocabulary; `figures.tsx` the agents; `material.ts` the flat faces and the hatching; `camera.tsx` the two presets and the free camera;
  `places.ts` where movable objects are drawn inside a fixed object; `look.ts` an object's look, by its type and
  the states that hold for it.
- `src/gen/`: the types, generated from the Python definitions (never edited by hand).
- The scene appearance of a domain is the domain's `domains/<domain>/appearance.json` (`webui/appearance.py`), carried
  by the catalogue; a domain without one is drawn from the defaults.

A display place (where a movable object is drawn inside the fixed object that holds it) is a display convention, not a
world fact: in the world the object has the container's position. It is derived on the page and written nowhere. The
same holds for an agent's glide between two ticks: the world knows only the ticks' positions.

The page's code names no domain, object type or area id (`tests/test_tviz_messages.py`).
