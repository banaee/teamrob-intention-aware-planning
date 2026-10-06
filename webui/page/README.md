# The web-ui's page (T-viz)

Stage 0.3, the style trial: the env-pane alone, drawing the start of one sim-run per domain from saved messages, tilted
or from above (the same scene, the camera moved). Stage 1a continues from here and adds the server. Records:
`docs/design_records.md`, "T-viz, the web-ui", 0.3.

## Run it

Needs Node.js 22.12 or later (`node --version`); every dependency is pinned in `package.json` and `package-lock.json`.

```bash
# once, and after a change of package.json
cd webui/page && npm ci

# the samples: the run description, the start tick update and the domain's scene appearance of the trial's two
# sim-runs, written to webui/page/public/samples/ (git-ignored); from the repository's root
PYTHONHASHSEED=0 ~/python-envs/ir-nomesa-env/bin/python -m mesa_sim.webui_export
# another sim-run:  ... -m mesa_sim.webui_export --domain kitting --scenario scenario_s01_01 [--layout env_layout_01]

# the page, at http://localhost:5173 (opens the browser)
cd webui/page && npm run dev
```

The address names the sample and the view: `?sample=kitting_scenario_s02_01&view=top`.

Screenshots of every sample in both views, in the installed Google Chrome (the page served by `npm run dev`):
`npm run shots` writes them to `docs/handoffs/tviz_trial/` (untracked).

After a change of `webui/messages.py` or `webui/appearance.py`, regenerate the page's types:
`~/python-envs/ir-nomesa-env/bin/python -m webui.schema`, then `npm run gen:types` here.

## What is where

- `src/theme.ts`: the theme, the one file of colours, line weights, spacing and type sizes; the page's CSS and the
  scene read it.
- `src/env-pane/`: the env-pane. `Scene.tsx` draws one tick from the run description, the tick update and the scene
  appearance; `forms.tsx` the shape vocabulary; `figures.tsx` the agents; `material.ts` the flat faces and the hatching;
  `camera.tsx` the two views; `displayPlaces.ts` where movable objects are drawn inside a fixed object.
- `src/gen/`: the types, generated from the Python definitions (never edited by hand).
- The scene appearance of a domain is the domain's `domains/<domain>/appearance.json` (`webui/appearance.py`); a domain
  without one is drawn from the defaults.

A display place (where a movable object is drawn inside the fixed object that holds it) is a display convention, not a
world fact: in the world the object has the container's position. It is derived on the page and written nowhere.

The page's code names no domain, object type or area id (`tests/test_tviz_messages.py`).
