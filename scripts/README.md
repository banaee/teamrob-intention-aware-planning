# Scripts

Utility scripts. They are not on the run path.

---

## The layout tool (`layout_tool.py`)

The tool draws a layout as a PNG, without a simulator. It also derives a new layout from an existing one: you move,
add and delete fixed objects in a browser and save the result under a new id. One function draws the layout as SVG;
both commands use it.

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

- The program starts a local server on 127.0.0.1 and opens the browser on a page with the same drawing, with grid
  lines over the space: very light gray every 50 cm, slightly darker every 100 cm. The grid is in "edit" only; the PNG
  from "render" has none.
- **Move.** Dragging a fixed object moves its centre. The centre snaps to a 5 cm grid. While you drag, the page shows
  the object's id and position as numbers. Objects you do not drag keep their exact positions.
- **Refusal.** A drag that puts the centre outside the space is refused. The object stays at its last position inside,
  and the page says why.
- **Add.** The page has a list in a side panel, the object library, with each type's colour from the legend. The tool builds it from every layout file in the folder of the
  source layout: one entry per distinct (type, size, subtype). An object without a `subtype` field forms an entry
  without a subtype (dock_loading: a `delivery_bay` with `dry` and one with `frozen` are two entries). A click on an
  entry adds one object of that type, size and subtype. Then you drag it.
  - The new object has the fields `id`, `type`, `position`, `size`, and `subtype` if its entry has one. It has no
    other field.
  - Its id is the first of `<type>_0`, `<type>_1`, `<type>_2`, ... that equals no id of the source layout and no id
    used on the page, an id deleted during this edit included. The tool compares whole ids for equality only. It
    reads no meaning and no number from the text of an id. A deleted id is not used again, so a setup that names it
    does not attach to a new object.
  - It first appears at the origin (0, 0): inside every space, on the grid. If another object's centre is there, it
    appears 50 cm further along x, then along y.
- **Delete.** Click an object to select it, then "Delete selected" (or the Delete key). The page warns first. The
  loader refuses a setup that names a fixed object the layout lacks as a home container or as a destination, and
  refuses a scenario whose task names it. A setup that does not name the object still loads.
- **Save as** takes the new layout's id: the file stem, without `.json`. The page refuses the name, before saving,
  when:
  - it is empty;
  - it holds `/` or `\`;
  - it ends in `.json` (the id would then end in `.json`);
  - it starts with `.`;
  - `<id>.json` or `<id>.png` exists already in the source layout's folder.
- "Save as" writes `<id>.json` and `<id>.png` into the source layout's folder. The PNG is the one "render" writes.
  `space.name` of the new layout is its id. The server checks: ids are unique; every added object is an entry of the
  object library, subtype included; every centre is inside the space; a deleted object is absent.
- The program never overwrites a file and never modifies the source layout.
- Ctrl+C in the terminal stops the program.

### How the tool reads a layout

It reads the geometry as the loader does (`mesa_sim/sim_model.py`):
- The space is centred on the origin: x from −width/2 to width/2, y from −height/2 to height/2.
- The y axis points up.
- `position` is the object's centre.
- `size` is the object's extent along x, then along y.
- `subtype`, where an object has it, is shown after the id in the drawing, in "render" and in "edit".
- `orientation_deg` is read by no code. The tool does not draw it: every rectangle is axis-aligned (TODO-166).

### Limits

- "edit" moves, adds and deletes the entries of `"env_objects"`. It does not rotate or resize an object, it has no
  field for a size, it adds no new type (only types and sizes the folder already has), and it does not change the
  areas.
- It does not draw `slots` and gives no way to edit it. An existing object keeps its `slots` field, and every other
  field, unchanged in the saved layout. The same holds for `subtype`: the page gives no way to edit it.
- A saved layout copies the `notes` of the objects from its source, and the other fields of `space`. Edit them by
  hand if they describe the old layout.
- A moved or kept object keeps its id, type and size, so the setups of the source layout stay usable with the new
  layout unless an object they name was deleted.

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
