# Scripts

Utility scripts. They are not on the run path.

---

## The layout tool (`layout_tool.py`)

The tool draws a layout as a PNG, without a simulator. It also derives a new layout from an existing one: you drag the
fixed objects in a browser and save the result under a new id. One function draws the layout as SVG; both commands use
it.

A layout is one JSON file with the top-level keys `"space"`, `"areas"` and `"env_objects"` (`domains/README.md`,
section 2; `docs/glossary.md` §9). The file stem is the layout's id.

### render

```bash
# one layout file
python scripts/layout_tool.py render domains/kitting/layouts/env_layout_02.json
# one folder: every *.json in it
python scripts/layout_tool.py render domains/kitting/layouts
# both domains at once
python scripts/layout_tool.py render domains/kitting/layouts domains/dock_loading/layouts
```

- Each layout gets one PNG, `<id>.png`, beside its JSON file. An existing PNG of that name is replaced.
- No SVG file is kept.
- Every file is read before any PNG is written. A file that is not a layout stops the command and is named.
- The PNGs in `domains/*/layouts/` are ignored by git (`.gitignore`).

The drawing shows:
- the outline of the space, with its name, its units and the coordinates of two corners;
- each area as its rectangle, with its id;
- each fixed object as its rectangle, with its id, coloured by its type;
- a legend of the types.

A type keeps its colour from one layout to the next.

### edit

```bash
python scripts/layout_tool.py edit domains/kitting/layouts/env_layout_02.json
```

- The program starts a local server on 127.0.0.1 and opens the browser on a page with the same drawing.
- Dragging a fixed object moves its centre. The centre snaps to a 10 cm grid. Objects you do not drag keep their exact
  positions.
- A drag that puts the centre outside the space is refused. The object stays at its last position inside, and the page
  says why.
- "Save as" takes the new layout's id: the file stem, without `.json`. The page refuses the name, before saving, when:
  - it is empty;
  - it holds `/` or `\`;
  - it ends in `.json` (the id would then end in `.json`);
  - it starts with `.`;
  - `<id>.json` or `<id>.png` exists already in the source layout's folder.
- "Save as" writes `<id>.json` and `<id>.png` into the source layout's folder. The PNG is the one "render" writes.
- The program never overwrites a file and never modifies the source layout.
- Ctrl+C in the terminal stops the program.

### How the tool reads a layout

It reads the geometry as the loader does (`mesa_sim/sim_model.py`):
- The space is centred on the origin: x from −width/2 to width/2, y from −height/2 to height/2.
- The y axis points up.
- `position` is the object's centre.
- `size` is the object's extent along x, then along y.
- `orientation_deg` is read by no code. The tool does not draw it: every rectangle is axis-aligned (TODO-166).

### Limits

- "edit" changes only the positions of the entries of `"env_objects"`. It does not rotate, resize, add or delete an
  object, and it does not change the areas. Every id, type and size stays, so the setups of the source layout stay
  usable with the new layout.
- A saved layout copies `space.name` and every object's `notes` from its source. Edit them by hand if they describe
  the old positions.

### Dependency

- "render" and "edit" need `cairosvg` (`requirements.txt`), which uses the system library libcairo2. It turns the SVG
  into a PNG.
- The tool imports nothing from the repository. It reads only the layout JSON, so it also works on a layout file
  outside the repository.

### Registration

- `domains/discovery.py` registers every `*.json` directly in a domain's `layouts/` folder as a layout, keyed by its
  stem. The PNGs are not registered.
- A layout saved by "edit" into a `layouts/` folder is therefore registered at the next import of that domain's
  registry, and a run can name it with `--layout <id>`.
