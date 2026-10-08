# The deck (T-pres)

The slides of Hadi's talk at the TeamRob final demo day, as an HTML deck: reveal.js over slides written in React. The
records: `docs/design_records.md`, "T-pres, the talk"; the content's starting point: `docs/handoffs/handoff_T-pres.md`,
read in full in every T-pres session. A "talk stage" is a row of the talk (the handoff's section 5, 0 to 12); a "part"
is a unit of work on the deck.

The scenes draw with the web-ui page's own code (`webui/page/src`), imported directly, so that a change of the web-ui's
look reaches the slides after one build; `webui/` is never changed for the deck. The type's family, weights and colours
are the web-ui's theme (`webui/page/src/theme.ts`); the three questions' colours (`src/look.ts`) and all sizes are the
deck's own. "Anton" and "Donny" are display text only.

## Start the deck

Needs Node.js 22.12 or later. Install once, with network; then nothing is loaded from outside.

```bash
cd presentation
npm ci            # once, with network
npm run build     # after a change of the slides, the web-ui page's sources, a layout or a look
npm run preview   # the deck at http://127.0.0.1:4173/ (offline)
```

In the browser: F fullscreen; a click, the right arrow, Space or the clicker's key advances one step; the left arrow or
PageUp goes back; Esc the overview; S the speaker view (the notes, the next slide, a clock) in its own window, which
goes on the laptop's screen while the deck is fullscreen on the projector. The notes never show on the projected deck.
The built deck (`dist/`) needs a local server: Chrome runs no module script from a file opened by double-click. While
working on the slides: `npm run dev` (http://127.0.0.1:5174/).

## The recorded rooms

The deck needs no server of the framework: what the web-ui's server would send for the view of a layout (the domain's
scene appearance from the catalogue, and the view of the layout without a setup) is recorded by the same piece of code
that feeds the web-ui (`mesa_sim/webui_adapter.py`; `scripts/record_view.py`) into `data/<domain>_<layout>.json`
(untracked): kitting's env_layout_01 and dock_loading's env_layout_03. `npm run build` and `npm run dev` record them again
every time, from the original files (`scripts/record.mjs`). The old recording is deleted first; if the recording cannot
run, the build stops with a message and nothing is built.

The Python environment: `TEAMROB_PYTHON` if set, else `~/python-envs/ir-nomesa-env/bin/python` (the repository's
working environment). On another machine: `TEAMROB_PYTHON=/path/to/python npm run build`.

## Checks

- `npm run pins` (run by `build` and `dev`): every package the deck shares with `webui/page` is pinned to the same
  version in both; a difference stops the build.
- `npm run shots` (with `npm run preview` running): clicks through the whole deck at 2560 x 1440 and 1920 x 1080 in the
  installed Google Chrome, one click per step, a screenshot after each into `shots/<size>/` (untracked); it fails on a
  page error, on any request that leaves the local server, or on a speaker note visible on the screen. `--only 1920`
  runs one size.
- `npm run pdf` (with `npm run preview` running): the deck as a PDF, one page per slide in its final step, at 2560 x
  1440, into `pdf/deck.pdf` (untracked); no speaker notes. A fallback copy and a handout for review.

## How it is put together

- `src/talk.ts`: the talk's skeleton (talk stages, levels, the three questions and the keywords of each talk stage's
  columns), the one place of their wording.
- `src/architecture/`: the architecture diagram (the handoff's section 6). `model.ts` holds the elements with their kinds,
  the talk stage at which each appears, the arrows with their keywords and the talk stages at which they appear or give
  way, and the positions; `Architecture.tsx` draws it with React Flow (`@xyflow/react`, pinned, bundled into the build).
  One diagram whose state is a talk stage: a slide opens on the state before its talk stage and a click adds what the
  talk stage adds (it fades in, an arrow is drawn along its length; the rest recedes). `colouring="questions"` colours it
  by know, believe, decide (the recap).
- `src/slides/`: `kit.tsx` (the slide frame with its footer and notes, steps, TODO boxes, a talk stage's card, a level's
  title, the architecture slide), one file per stretch of the talk, and `index.ts`, the order.
- `src/scene/AgentsInRoom.tsx`: one canvas; the env-pane's `FramingCamera` framing a box that moves from a figure's ring
  to the room; the env-pane's `Scene` with a moment without agents (as the web-ui draws a layout's view); the figures
  (the domain's robot and human) drawn beside it; a veil in the slide's ground over the room and under the figures,
  fading out as the view moves back. It mounts only while its slide is current or next to it.
- `src/Deck.tsx`: reveal.js with its own layout off (`disableLayout`); `src/deck.css` sizes a 16:9 stage in the unit
  `--u` (1/1920 of the stage), so a canvas is never scaled by CSS and renders sharp at both screen sizes. A slide's step
  is a reveal fragment (`useShown`); `useNear` mounts heavy content near the current slide only.
- `vite.config.ts`: `dedupe` makes the web-ui's modules use the deck's own React, three and R3F (one copy of each).

A TODO box on a slide says what is to be shown there and why, and which part (or Hadi) fills it.
