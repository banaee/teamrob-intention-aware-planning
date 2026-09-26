# Layouts, setups, scenarios and overrides: a user's guide

Written after T-L stages 1 to 3 (September 2026); sections 3 and 4 aligned with stage 4 as built.
Where this guide and the T-L entry in `docs/design_decisions.md` or `docs/glossary.md` §9 differ, they win.

## 1. The three layers

A run is one layout, one setup and one scenario, plus the run options.

| layer | what it holds | file |
|---|---|---|
| layout (the room) | space, zones, the fixed objects with positions: tables, shelves, machines, switches, landmarks | `domains/<domain>/layouts/env_layout_KK.json` |
| setup (the shift) | the movable objects that exist, each with its home container and its designated destination | `domains/<domain>/setups/env_setup_NN.json` |
| scenario (the episode) | per agent: start position, assigned tasks, `observes`, the human's script; the purpose; `setup`; `reference_layouts` | `domains/<domain>/scenarios/scenarios_sNN.py` |
| run options | gate, cost strategy, strategy, prior, separation stop, steps | `configs/experiment.yaml` or the command line |

Rules that follow:

- A scenario declares the setup it is written on (`setup=`) and the rooms it was written for
  (`reference_layouts=`). Both are validated at load.
- The ids encode nothing about a binding except one convention: `scenario_s03_04` lives in
  `scenarios_s03.py` and has `setup="env_setup_03"`. A layout's serial is never in a scenario id.
- A layout and a setup are shared. Editing `env_layout_07.json` changes every scenario that
  references it. That is intended for fixtures, and it is why the override exists for a tweak.
- A change worth keeping is a new artefact: a new layout file, a new setup file, or a new scenario
  literal. Discovery registers it at import; nothing else is edited.

## 2. Where a change goes

| you want to change | layer | do this |
|---|---|---|
| move a shelf, table or machine; add a landmark or zone | layout | edit the layout file, or copy it to a new `env_layout_KK.json` |
| which items exist; the shelf an item starts on; the table an item goes to | setup | edit the setup file, or copy it to a new `env_setup_NN.json` |
| an agent's start position | scenario | edit the literal, or add a new one |
| the robot's or the human's assigned tasks | scenario | a new literal (the old one may be a fixture) |
| the human's script | scenario | a new literal |
| which room a scenario may run on | scenario | add the layout id to `reference_layouts` |
| prior, strategy, gate, steps | run options | the run file or the command line |

A new scenario: copy a literal in the module of its setup, give it the next counter
(`scenario_s03_10`), set the Python variable equal to the id, and write the purpose in
`description`. Stated tables in its tasks must agree with the setup's designations.

## 3. Running

```
python mesa_sim/run_mesa.py --scenario scenario_s05_01
python mesa_sim/run_mesa.py --scenario scenario_s05_01 --layout env_layout_09
python mesa_sim/run_mesa.py --run my_run.yaml
solara run mesa_sim/run_mesa.py
solara run mesa_sim/run_mesa.py -- --run my_run.yaml
```

- With no `--layout`, the scenario's first reference layout is run.
- `--layout` may name any registered layout. The run is validated (every bound object exists with
  the right type, every stated table agrees with the setup, every start position lies inside the
  space). A run on a layout outside the scenario's reference list is valid but is not a baseline;
  to make it one, add the layout's id to `reference_layouts`.
- The log's first line names the triple: `layout=... setup=... scenario=...`. Any log says what it ran.
- `PYTHONHASHSEED=0` on every run.

## 4. Overriding one fact for a debugging run (stage 4)

You ran `scenario_s05_01` and want the human a bit to the right, `shelf_2` moved, and `item_1`
starting on `shelf_5`, without touching any artefact.

Write a run file:

```yaml
domain: kitting
scenario: scenario_s05_01
steps: 300
overrides:
  scenario.human_0.start_position: [560, -550]
  layout.shelf_2.position: [-300, -300]
  setup.item_1.initial_container: shelf_5
```

and run `python mesa_sim/run_mesa.py --run my_run.yaml`. For one tweak, the command line does
the same: `--override scenario.human_0.start_position=560,-550`.

The path is `<layer>.<id>.<key>`: the layer tells you which file the permanent edit would go to,
the key is that file's own key. A position is two numbers (`[x, y]` in the file, `x,y` on the
command line), a container an id. The three lines above are the whole list of what can be
overridden; any other path is refused with the path named:

| overridable | not overridable, and why |
|---|---|
| an agent's `start_position` | assigned tasks: a variant is a new scenario |
| a fixed object's `position` | the script: a new scenario |
| a movable object's `initial_container` | an item's destination: a different designation set is a different setup |
| | a movable object's position: it is its container's |
| | any id: an object's identity |

What happens:

- The loader reads the three artefacts, applies the overrides, then validates and runs exactly as
  any run. A start outside the space or a container not in the layout is refused as usual.
- The log prints each override on its own line under the triple, sorted by path, in the
  command-line form (an `--override` for the same path replaces the file's):

  ```
  [run_mesa] override layout.shelf_2.position=-300.0,-300.0
  [run_mesa] override scenario.human_0.start_position=560.0,-550.0
  [run_mesa] override setup.item_1.initial_container=shelf_5
  ```

  so a colleague can paste them back and reproduce the run.
- A run with overrides is for looking. It never becomes a fixture or a baseline.

In the viewer: the sidebar shows the run file's path, the triple and the overrides (those given by
`--override` marked "command line", not editable there). A form lets you add one of the three kinds
and press "Write and reload", or press "remove" on one; the run is tried first, and only a run that
loads is written into the run file the viewer was started from (its comments kept) and reloaded. If you started it from
`configs/experiment.yaml`, remove the overrides afterwards: the sweeps read that file.

## 5. Keeping a tweak

Move it from the overrides block into the owning file, then delete the block:

- a start position: into the scenario literal, or a new literal if the original is a fixture;
- a shelf position: a new layout file, added to the scenario's `reference_layouts`;
- an item's shelf: a new setup file and a new scenario on it.

## 6. Old ids

The frozen analyses keep the old ids (`scenario_70`, `env_layout7`, `s70_off.log`). The map to
the new ids is `docs/rename_table.md`. The maintained baseline sets were regenerated under the
new names with byte-identical `.rec` streams, so a finding on `s70` is a finding on
`env_layout_07 / scenario_s05_01`.
