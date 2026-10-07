# The deck (a trial)

The slides of the TeamRob demo day's talk, as an HTML deck: reveal.js over slides written in React. The slides draw with
the web-ui page's own code (`webui/page/src`), imported directly, so that a change of the web-ui's look reaches the
slides without a second edit. A trial: one slide, its structure replaceable.

Slide 1, two steps (a click or the clicker's key advances, PageUp or the left arrow goes back): the robot's figure as
the env-pane draws it in the tilted view (`env-pane/figures.tsx`, its paint and material, the env-pane's camera); then
the same figure in kitting's env_layout_01, drawn by the env-pane's own `Scene` (fixed objects only), the view moving
back in about one second until the whole room shows as the env-pane frames it. The type's family, weights and colours
are the web-ui's theme (`webui/page/src/theme.ts`); its sizes are the deck's own. "Anton" is the robot's name in the
talk only.

## The recorded room

The deck needs no server: what the web-ui's server would send for the view of a layout (the domain's scene appearance
from the catalogue, and the view of the layout without a setup) is recorded by the same piece of code that feeds the
web-ui (`mesa_sim/webui_adapter.py`; `scripts/record_view.py`) into `data/<domain>_<layout>.json` (untracked).
`npm run build` and `npm run dev` record it again every time, from the original files (`scripts/record.mjs`), so a
changed layout or look reaches the slide with one build. The old recording is deleted first; if the recording cannot
run, the build stops with a message and nothing is built.

The Python environment: `TEAMROB_PYTHON` if set, else `~/python-envs/ir-nomesa-env/bin/python` (the repository's
working environment). On another machine: `TEAMROB_PYTHON=/path/to/python npm run build`.

## Build and start

Needs Node.js 22.12 or later. Install once, with network; then nothing is loaded from outside.

```bash
cd presentation
npm ci            # once, with network
npm run build     # after a change of the slides, the web-ui page's sources, a layout or a look
npm run preview   # the deck at http://127.0.0.1:4173/ (offline); F for fullscreen, Esc for the overview
```

The built deck (`dist/`) needs a local server: Chrome runs no module script from a file opened by double-click.
While working on the slides: `npm run dev` (http://127.0.0.1:5174/).

## Checks

- `npm run pins` (run by `build` and `dev`): every package the deck shares with `webui/page` is pinned to the same
  version in both; a difference stops the build.
- `npm run shots` (with `npm run preview` running): each slide at 2560 x 1440 and 1920 x 1080 in the installed Google
  Chrome, each step (a click; one shot halfway through the view's movement) and back to the first, written to `shots/`
  (untracked); it fails on a page error or on any request that leaves the local server.

## How it is put together

- `vite.config.ts`: `dedupe` makes the web-ui's modules use the deck's own React, three and R3F (one copy of each).
- `src/Deck.tsx`: reveal.js with its own layout off (`disableLayout`); `src/deck.css` sizes a 16:9 stage in the unit
  `--u` (1/1920 of the stage), so a canvas is never scaled by CSS and renders sharp at both screen sizes.
- `src/Deck.tsx`: a slide's step is a reveal fragment; `useShown` tells a slide whether its fragment is shown.
- `src/scene/RobotInRoom.tsx`: one canvas; the env-pane's `FramingCamera` framing a box that moves from the robot's ring
  to the room; the env-pane's `Scene` with a moment without agents (as the web-ui draws a layout's view); the figure
  drawn beside it; a veil in the slide's ground over the room and under the robot, fading out as the view moves back.
- `src/slides/`: one file per slide.
