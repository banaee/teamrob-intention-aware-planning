# scripts/layout_tool.py
"""
Draw layout files, and derive a new layout from one by moving, adding and deleting its fixed objects.

    python scripts/layout_tool.py render <path> [<path> ...]
    python scripts/layout_tool.py edit <layout file>

A layout is one JSON file with the top-level keys "space", "areas", "env_objects"
(domains/README.md, section 2). The tool reads only that JSON: it imports nothing of
the repository and works on a layout file anywhere.

Geometry, read the way the loader reads it (mesa_sim/sim_model.py):
- the space is centred on the origin: x in [-width/2, width/2], y in [-height/2, height/2],
  y up (the ContinuousSpace's bounds);
- an object's "position" is its centre; "size" is [extent along x, extent along y];
- "orientation_deg" is not read by the loader, so it is not drawn: every rectangle is
  axis-aligned;
- an area is its "bounds" rectangle.

layout_svg() is the only drawing code. "render" rasterises its SVG to <stem>.png beside
the layout file (cairosvg); "edit" serves the same SVG, with a grid, in a page whose
JavaScript moves objects and asks the server for the drawing after an add or a delete.
"""

import argparse
import copy
import json
import math
import sys
import webbrowser
import zlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, List, Tuple
from xml.sax.saxutils import escape, quoteattr

LAYOUT_KEYS = ("space", "areas", "env_objects")
PNG_WIDTH_PX = 1600   # the larger side of the drawing in the PNG and on the page
GRID_CM = 5           # the edit page's snap step, in the layout's units
GRID_LINE_CM = 50     # the edit page's grid lines: every 50 cm, the multiples of 100 darker

# One colour per type. A type's colour is chosen by a stable hash of its name, so a type
# keeps its colour from one layout to the next; two types of one layout that hash to the
# same colour are separated by taking the next free colour, in sorted type order.
TYPE_COLOURS = (
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b",
    "#e377c2", "#7f7f7f", "#bcbd22", "#17becf", "#393b79", "#e7ba52",
)


# =============================================================================
# Reading
# =============================================================================

def load_layout(path: Path) -> dict:
    """The parsed layout; an error naming the file when a top-level key is missing."""
    with open(path, encoding="utf-8") as f:
        layout = json.load(f)
    missing = [k for k in LAYOUT_KEYS if not isinstance(layout, dict) or k not in layout]
    if missing:
        raise ValueError(f"{path}: not a layout (missing top-level key(s) {', '.join(missing)})")
    return layout


def type_colours(types: List[str]) -> Dict[str, str]:
    colours: Dict[str, str] = {}
    taken = set()
    for t in sorted(set(types)):
        i = zlib.crc32(t.encode("utf-8")) % len(TYPE_COLOURS)
        for k in range(len(TYPE_COLOURS)):
            c = TYPE_COLOURS[(i + k) % len(TYPE_COLOURS)]
            if c not in taken or len(taken) >= len(TYPE_COLOURS):
                break
        colours[t] = c
        taken.add(c)
    return colours


def _num(v: float) -> str:
    return f"{v:g}"


# =============================================================================
# Drawing
# =============================================================================

def layout_svg(layout: dict, grid: bool = False) -> str:
    """
    The drawing of a parsed layout as SVG text. SVG user units are the layout's units;
    the layout point (x, y) is drawn at SVG (x, -y), so y points up.

    Each entry of env_objects is one <g class="obj"> element carrying the object's id
    (data-id), its type (data-type) and its position (data-x, data-y), translated to its
    centre; its rectangle and label are drawn about (0, 0) inside it. With `grid`, grid lines
    are drawn over the areas and under the objects (the edit page's; "render" draws none).
    """
    space = layout["space"]
    W, H = float(space["width"]), float(space["height"])
    units = space.get("units", "")
    name = space.get("name", "")
    objects = layout["env_objects"]
    colours = type_colours([o["type"] for o in objects])

    font = max(W, H) / 75.0
    margin = font * 4
    legend_rows = math.ceil(len(colours) / 4) if colours else 0
    legend_h = legend_rows * font * 1.8 + font
    x0, y0 = -W / 2 - margin, -H / 2 - margin - font * 1.5
    vw, vh = W + 2 * margin, H + 2 * margin + font * 1.5 + legend_h
    px_w = PNG_WIDTH_PX if vw >= vh else PNG_WIDTH_PX * vw / vh
    px_h = px_w * vh / vw

    out: List[str] = []
    a = out.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" id="layout" '
      f'width="{px_w:.0f}" height="{px_h:.0f}" '
      f'viewBox="{_num(x0)} {_num(y0)} {_num(vw)} {_num(vh)}" '
      f'data-width="{_num(W)}" data-height="{_num(H)}" '
      f'font-family="DejaVu Sans, Arial, sans-serif">')
    a(f'<rect x="{_num(x0)}" y="{_num(y0)}" width="{_num(vw)}" height="{_num(vh)}" fill="#ffffff"/>')

    # Title: the space's name and its units.
    title = f"{name} ({units})" if units else name
    a(f'<text x="{_num(-W / 2)}" y="{_num(-H / 2 - font * 1.2)}" font-size="{_num(font * 1.4)}" '
      f'font-weight="bold">{escape(title)}</text>')

    # Areas: dashed rectangles with their ids.
    for area in layout["areas"]:
        b = area["bounds"]
        ax0, ax1 = float(b["x_min"]), float(b["x_max"])
        ay0, ay1 = float(b["y_min"]), float(b["y_max"])
        a(f'<g class="area" data-id={quoteattr(str(area["id"]))}>'
          f'<rect x="{_num(ax0)}" y="{_num(-ay1)}" width="{_num(ax1 - ax0)}" height="{_num(ay1 - ay0)}" '
          f'fill="#f4f4f8" stroke="#8888aa" stroke-width="{_num(font / 8)}" '
          f'stroke-dasharray="{_num(font / 2)} {_num(font / 3)}"/>'
          f'<text x="{_num(ax0 + font / 2)}" y="{_num(-ay1 + font * 1.3)}" font-size="{_num(font)}" '
          f'font-style="italic" fill="#666688">{escape(str(area["id"]))}</text></g>')

    # The edit page's grid: lines at the multiples of 50 from the origin, the multiples of 100 darker.
    if grid:
        step = GRID_LINE_CM
        lines: List[Tuple[int, str, float]] = []
        for k in range(math.ceil(-W / 2 / step), math.floor(W / 2 / step) + 1):
            lines.append((k * step, "v", W))
        for k in range(math.ceil(-H / 2 / step), math.floor(H / 2 / step) + 1):
            lines.append((k * step, "h", H))
        for dark in (False, True):
            for v, kind, _ in lines:
                if (v % (2 * step) == 0) != dark:
                    continue
                colour = "#c4c4c4" if dark else "#e6e6e6"
                if kind == "v":
                    a(f'<line class="grid" x1="{v}" y1="{_num(-H / 2)}" x2="{v}" y2="{_num(H / 2)}" '
                      f'stroke="{colour}" stroke-width="{_num(font / 25)}"/>')
                else:
                    a(f'<line class="grid" x1="{_num(-W / 2)}" y1="{-v}" x2="{_num(W / 2)}" y2="{-v}" '
                      f'stroke="{colour}" stroke-width="{_num(font / 25)}"/>')

    # The outline of the space, with the coordinates of two corners.
    a(f'<rect x="{_num(-W / 2)}" y="{_num(-H / 2)}" width="{_num(W)}" height="{_num(H)}" '
      f'fill="none" stroke="#000000" stroke-width="{_num(font / 4)}"/>')
    a(f'<text x="{_num(-W / 2)}" y="{_num(H / 2 + font * 1.3)}" font-size="{_num(font * 0.8)}" '
      f'fill="#555555">({_num(-W / 2)}, {_num(-H / 2)})</text>')
    a(f'<text x="{_num(W / 2)}" y="{_num(-H / 2 - font * 0.3)}" font-size="{_num(font * 0.8)}" '
      f'fill="#555555" text-anchor="end">({_num(W / 2)}, {_num(H / 2)})</text>')

    # Fixed objects: one element each.
    for o in objects:
        x, y = float(o["position"][0]), float(o["position"][1])
        w, h = float(o["size"][0]), float(o["size"][1])
        oid = str(o["id"])
        a(f'<g class="obj" data-id={quoteattr(oid)} data-type={quoteattr(str(o["type"]))} '
          f'data-w="{_num(w)}" data-h="{_num(h)}" '
          f'data-x="{_num(x)}" data-y="{_num(y)}" transform="translate({_num(x)} {_num(-y)})">'
          f'<rect x="{_num(-w / 2)}" y="{_num(-h / 2)}" width="{_num(w)}" height="{_num(h)}" '
          f'fill="{colours[o["type"]]}" fill-opacity="0.55" stroke="#222222" '
          f'stroke-width="{_num(font / 10)}"/>'
          f'<text x="0" y="{_num(font * 0.35)}" font-size="{_num(font * 0.9)}" text-anchor="middle" '
          f'fill="#000000">{escape(oid)}</text></g>')

    # Legend of the types.
    ly = H / 2 + font * 3.2
    col_w = W / 4
    for i, (t, c) in enumerate(colours.items()):
        lx = -W / 2 + (i % 4) * col_w
        ry = ly + (i // 4) * font * 1.8
        a(f'<rect x="{_num(lx)}" y="{_num(ry - font)}" width="{_num(font * 1.2)}" height="{_num(font * 1.2)}" '
          f'fill="{c}" fill-opacity="0.55" stroke="#222222" stroke-width="{_num(font / 10)}"/>'
          f'<text x="{_num(lx + font * 1.7)}" y="{_num(ry)}" font-size="{_num(font)}">{escape(t)}</text>')

    a("</svg>")
    return "\n".join(out)


# =============================================================================
# render
# =============================================================================

def png_path(layout_path: Path) -> Path:
    return layout_path.with_suffix(".png")


def write_png(layout: dict, out: Path) -> None:
    import cairosvg   # the one rendering dependency, needed by "render" alone
    cairosvg.svg2png(bytestring=layout_svg(layout).encode("utf-8"), write_to=str(out))


def layout_files(paths: List[str]) -> List[Path]:
    """Each path is a layout file or a folder of layout files (its *.json, sorted)."""
    files: List[Path] = []
    for p in map(Path, paths):
        if p.is_dir():
            found = sorted(p.glob("*.json"))
            if not found:
                raise ValueError(f"{p}: no *.json in this folder")
            files.extend(found)
        elif p.is_file():
            files.append(p)
        else:
            raise ValueError(f"{p}: no such file or folder")
    return files


def cmd_render(paths: List[str]) -> None:
    files = layout_files(paths)
    layouts = [(f, load_layout(f)) for f in files]   # every file read before any PNG is written
    for f, layout in layouts:
        out = png_path(f)
        write_png(layout, out)
        print(out)


# =============================================================================
# edit
# =============================================================================

# Object library entries: one per distinct (type, size) of the layout files in the source's folder.
LibraryEntry = Tuple[str, Tuple[float, float]]

PAGE = r"""<!doctype html>
<html><head><meta charset="utf-8"><title>Layout editor: __SOURCE__</title>
<style>
  body { font-family: sans-serif; margin: 12px; background: #fafafa; }
  #bar { margin-bottom: 8px; }
  #bar input { width: 18em; }
  #check, #status { margin-left: 1em; }
  .bad { color: #b00020; }
  .ok { color: #1b6e20; }
  #main { display: flex; gap: 12px; align-items: flex-start; }
  #stage { flex: 1 1 auto; min-width: 0; }
  #side { flex: 0 0 15em; background: #fff; border: 1px solid #ccc; padding: 8px; }
  #side h3 { margin: 8px 0 4px; font-size: 1em; }
  #side .type { margin-top: 6px; font-size: 0.85em; color: #555; }
  #side button.entry { display: block; width: 100%; text-align: left; margin: 2px 0; }
  #warn { display: none; margin: 6px 0; padding: 6px; background: #fff3cd; border: 1px solid #e0b000; }
  html { overflow-y: scroll; }
  svg { display: block; width: auto; height: 80vh; max-width: 100%; background: #fff; border: 1px solid #ccc; }
  g.obj { cursor: move; }
  g.obj.refused rect { stroke: #b00020; stroke-width: 6; }
  g.obj.selected rect { stroke: #0050ff; stroke-width: 5; }
  #tip { position: fixed; display: none; pointer-events: none; background: #222; color: #fff;
         padding: 2px 6px; font-size: 13px; border-radius: 3px; white-space: nowrap; }
  #tip.bad { background: #b00020; color: #fff; }
</style></head>
<body>
<div id="bar">
  <b>__SOURCE__</b> &nbsp; Save as
  <input id="name" placeholder="new layout id (file stem)">.json
  <button id="save" disabled>Save as</button>
  <span id="check"></span>
</div>
<div id="status">Drag an object to move it; centres snap to __GRID__ __UNITS__. Click an object to select it. The source is never modified.</div>
<div id="warn">
  <span id="warntext"></span>
  <button id="warnyes">Delete</button> <button id="warnno">Cancel</button>
</div>
<div id="main">
  <div id="stage">__SVG__</div>
  <div id="side">
    <h3>Object library</h3>
    <div id="library"></div>
    <h3>Selected</h3>
    <div id="selname">none</div>
    <button id="delete" disabled>Delete selected</button>
    <div id="moved" style="margin-top:10px; font-size:0.85em"></div>
  </div>
</div>
<div id="tip"></div>
<script>
"use strict";
const GRID = __GRID__;
const EXISTING = new Set(__EXISTING__);
const LIBRARY = __LIBRARY__;       // [{type, size: [w, h]}], one per distinct (type, size) in the folder
const SOURCE_IDS = __SOURCE_IDS__; // every id of the source layout, deleted ones included
const stage = document.getElementById("stage");
const status = document.getElementById("status");
const tip = document.getElementById("tip");
const getSvg = () => stage.querySelector("svg");
const W = parseFloat(getSvg().dataset.width), H = parseFloat(getSvg().dataset.height);

// The page's state: every object now in the layout. The server draws; this script moves.
const objs = [];
for (const g of stage.querySelectorAll("g.obj")) {
  const x = parseFloat(g.dataset.x), y = parseFloat(g.dataset.y);
  objs.push({ id: g.dataset.id, type: g.dataset.type, size: [parseFloat(g.dataset.w), parseFloat(g.dataset.h)],
              x: x, y: y, x0: x, y0: y, added: false });
}
const deleted = new Set();
let selected = null;

function inside(x, y) { return x >= -W / 2 && x <= W / 2 && y >= -H / 2 && y <= H / 2; }
function objGroup(id) {
  for (const g of getSvg().querySelectorAll("g.obj")) if (g.dataset.id === id) return g;
  return null;
}
function place(g, x, y) {
  g.dataset.x = x; g.dataset.y = y;
  g.setAttribute("transform", "translate(" + x + " " + (-y) + ")");
}
function svgPoint(evt) {
  const svg = getSvg();
  const p = svg.createSVGPoint(); p.x = evt.clientX; p.y = evt.clientY;
  const q = p.matrixTransform(svg.getScreenCTM().inverse());
  return [q.x, -q.y];   // layout coordinates, y up
}
function showTip(evt, text, bad) {
  tip.textContent = text; tip.className = bad ? "bad" : "";
  tip.style.display = "block";
  tip.style.left = (evt.clientX + 14) + "px"; tip.style.top = (evt.clientY + 14) + "px";
}
function summary() {
  const moved = objs.filter(o => !o.added && (o.x !== o.x0 || o.y !== o.y0));
  const added = objs.filter(o => o.added);
  const parts = [];
  if (moved.length) parts.push("Moved: " + moved.map(o => o.id + " (" + o.x + ", " + o.y + ")").join(", "));
  if (added.length) parts.push("Added: " + added.map(o => o.id + " (" + o.x + ", " + o.y + ")").join(", "));
  if (deleted.size) parts.push("Deleted: " + Array.from(deleted).sort().join(", "));
  document.getElementById("moved").textContent = parts.join(" | ");
}
function highlight() {
  for (const g of getSvg().querySelectorAll("g.obj")) g.classList.toggle("selected", g.dataset.id === selected);
  document.getElementById("selname").textContent = selected === null ? "none" : selected;
  document.getElementById("delete").disabled = selected === null;
}
function select(id) { selected = id; highlight(); hideWarn(); }

// The drawing comes from the server: after an add or a delete the page asks for the drawing of its state.
async function refresh() {
  const body = { objects: objs.map(o => ({ id: o.id, type: o.type, size: o.size, position: [o.x, o.y] })) };
  const resp = await fetch("/svg", { method: "POST", headers: { "Content-Type": "application/json" },
                                      body: JSON.stringify(body) });
  if (!resp.ok) { status.innerHTML = '<span class="bad">drawing failed: ' + (await resp.text()) + "</span>"; return; }
  stage.innerHTML = await resp.text();
  highlight();
  summary();
}

// Dragging (event delegation: the svg is replaced by refresh()).
let drag = null;
stage.addEventListener("pointerdown", evt => {
  const g = evt.target.closest("g.obj");
  if (!g) { select(null); return; }
  const o = objs.find(o => o.id === g.dataset.id);
  select(o.id);
  const [px, py] = svgPoint(evt);
  drag = { o: o, g: g, dx: o.x - px, dy: o.y - py };
  stage.setPointerCapture(evt.pointerId);
  evt.preventDefault();
  showTip(evt, o.id + " (" + o.x + ", " + o.y + ")", false);
});
stage.addEventListener("pointermove", evt => {
  if (!drag) return;
  const [px, py] = svgPoint(evt);
  const x = Math.round((px + drag.dx) / GRID) * GRID;
  const y = Math.round((py + drag.dy) / GRID) * GRID;
  if (!inside(x, y)) {
    drag.g.classList.add("refused");
    showTip(evt, drag.o.id + " (" + x + ", " + y + ") outside the space; stays (" + drag.o.x + ", " + drag.o.y + ")", true);
    status.innerHTML = '<span class="bad">' + drag.o.id + ": (" + x + ", " + y + ") is outside the space; kept at (" +
      drag.o.x + ", " + drag.o.y + ")</span>";
    return;
  }
  drag.g.classList.remove("refused");
  drag.o.x = x; drag.o.y = y;
  place(drag.g, x, y);
  showTip(evt, drag.o.id + " (" + x + ", " + y + ")", false);
  status.textContent = drag.o.id + ": (" + x + ", " + y + ")";
});
function endDrag() {
  if (!drag) return;
  drag.g.classList.remove("refused");
  drag = null;
  tip.style.display = "none";
  summary();
}
stage.addEventListener("pointerup", endDrag);
stage.addEventListener("pointercancel", endDrag);

// Object library: a click adds one object of the entry's type and size.
// Id: <type>_<N>, N one more than the highest N of that form among the source's ids and the page's objects.
function nextId(type) {
  const prefix = type + "_";
  let n = -1;
  for (const id of SOURCE_IDS.concat(objs.map(o => o.id))) {
    if (!id.startsWith(prefix)) continue;
    const rest = id.slice(prefix.length);
    if (/^[0-9]+$/.test(rest)) n = Math.max(n, parseInt(rest, 10));
  }
  return prefix + (n + 1);
}
// Position: the origin (inside every space, on the grid); if an object's centre is there, 50 cm further along x, then y.
function freeSpot() {
  let x = 0, y = 0;
  while (objs.some(o => o.x === x && o.y === y)) {
    x += 50;
    if (x > W / 2) { x = 0; y += 50; }
    if (y > H / 2) return [0, 0];
  }
  return [x, y];
}
async function addObject(entry) {
  const [x, y] = freeSpot();
  const o = { id: nextId(entry.type), type: entry.type, size: entry.size.slice(), x: x, y: y, x0: x, y0: y, added: true };
  objs.push(o);
  await refresh();
  select(o.id);
  status.textContent = "added " + o.id + " at (" + x + ", " + y + "); drag it";
}
const library = document.getElementById("library");
let lastType = null;
for (const entry of LIBRARY) {
  if (entry.type !== lastType) {
    const h = document.createElement("div"); h.className = "type"; h.textContent = entry.type; library.appendChild(h);
    lastType = entry.type;
  }
  const b = document.createElement("button");
  b.className = "entry"; b.textContent = entry.size[0] + " × " + entry.size[1];
  b.addEventListener("click", () => addObject(entry));
  library.appendChild(b);
}

// Delete: warn first. A layout without the object is refused at load by a setup (or scenario) that names it.
const warn = document.getElementById("warn");
function hideWarn() { warn.style.display = "none"; }
function askDelete() {
  if (selected === null) return;
  document.getElementById("warntext").textContent =
    "Delete " + selected + "? A setup or scenario that names this id (a home container, a destination, a task " +
    "parameter) is refused at load with the new layout. A setup that does not name it still loads.";
  warn.style.display = "block";
}
document.getElementById("delete").addEventListener("click", askDelete);
document.getElementById("warnno").addEventListener("click", hideWarn);
document.getElementById("warnyes").addEventListener("click", async () => {
  const i = objs.findIndex(o => o.id === selected);
  if (i < 0) return;
  const o = objs[i];
  objs.splice(i, 1);
  if (!o.added) deleted.add(o.id);
  selected = null;
  hideWarn();
  await refresh();
  status.textContent = "deleted " + o.id;
});
document.addEventListener("keydown", evt => {
  if (evt.key === "Delete" && document.activeElement.tagName !== "INPUT") askDelete();
});

// Save as.
const nameBox = document.getElementById("name");
const saveBtn = document.getElementById("save");
const check = document.getElementById("check");
// The name is the new layout's id, its file stem: the file is <name>.json in the source's folder.
// domains/discovery.py registers every *.json directly in a layouts folder, keyed by its stem.
function nameProblem(n) {
  if (n === "") return "type a name";
  if (/[\/\\]/.test(n)) return "no folder separators: the file goes into the source layout's folder";
  if (/\.json$/i.test(n)) return "type the id without .json (the file would be " + n + ".json, its id " + n + ")";
  if (n.startsWith(".")) return "a name may not start with '.'";
  if (EXISTING.has(n + ".json") || EXISTING.has(n + ".png")) return n + ".json or " + n + ".png exists already";
  return null;
}
function recheck() {
  const p = nameProblem(nameBox.value.trim());
  check.className = p ? "bad" : "ok";
  check.textContent = p ? p : "writes " + nameBox.value.trim() + ".json and " + nameBox.value.trim() + ".png";
  saveBtn.disabled = !!p;
}
nameBox.addEventListener("input", recheck);
recheck();
saveBtn.addEventListener("click", async () => {
  const name = nameBox.value.trim();
  const positions = {};
  for (const o of objs) if (!o.added && (o.x !== o.x0 || o.y !== o.y0)) positions[o.id] = [o.x, o.y];
  const added = objs.filter(o => o.added).map(o => ({ id: o.id, type: o.type, size: o.size, position: [o.x, o.y] }));
  const resp = await fetch("/save", { method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name: name, positions: positions, added: added, deleted: Array.from(deleted) }) });
  const res = await resp.json();
  if (resp.ok) {
    EXISTING.add(name + ".json"); EXISTING.add(name + ".png");
    status.innerHTML = '<span class="ok">Saved ' + res.json + " and " + res.png + "</span>";
  } else {
    status.innerHTML = '<span class="bad">Not saved: ' + res.error + "</span>";
  }
  recheck();
});
summary();
</script>
</body></html>
"""


def _clean(v: float):
    """A number as the layout files write it: an integer when it is one."""
    return int(v) if float(v).is_integer() else v


def name_problem(name: str, folder: Path) -> str:
    """Why `name` cannot be the new layout's id in `folder`, or "" when it can."""
    if not name:
        return "empty name"
    if "/" in name or "\\" in name:
        return "no folder separators: the file goes into the source layout's folder"
    if name.lower().endswith(".json"):
        return "type the id without .json"
    if name.startswith("."):
        return "a name may not start with '.'"
    for p in (folder / f"{name}.json", folder / f"{name}.png"):
        if p.exists():
            return f"{p} exists already"
    return ""


def object_library(folder: Path) -> List[LibraryEntry]:
    """
    One entry per distinct (type, size) among the env_objects of every layout file in
    `folder` (its *.json that are layouts, sorted); a file that is not a layout is
    skipped with a note.
    """
    entries = set()
    for path in sorted(folder.glob("*.json")):
        try:
            layout = load_layout(path)
            for o in layout["env_objects"]:
                entries.add((str(o["type"]), (float(o["size"][0]), float(o["size"][1]))))
        except (ValueError, OSError, KeyError, IndexError, TypeError, json.JSONDecodeError) as e:
            print(f"layout_tool: object library skips {path.name}: {e}", file=sys.stderr)
    return sorted(entries)


def _point(oid: str, pos, W: float, H: float) -> list:
    """A position as two finite numbers with the centre inside the space; else an error."""
    if (not isinstance(pos, list) or len(pos) != 2
            or not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in pos)):
        raise ValueError(f"'{oid}': a position is two numbers")
    x, y = pos
    if not (-W / 2 <= x <= W / 2 and -H / 2 <= y <= H / 2):
        raise ValueError(f"'{oid}': ({x:g}, {y:g}) is outside the space")
    return [_clean(x), _clean(y)]


def edited_layout(source: dict, name: str, library: List[LibraryEntry],
                  positions: Dict[str, list], added: List[dict], deleted: List[str]) -> dict:
    """
    The source layout with: the positions of the named objects replaced, the objects
    `added` appended (fields id, type, position, size, in that order), the objects
    `deleted` removed, and space.name set to `name`. Everything else is unchanged: every
    other field of every kept object (slots included), the areas, the rest of the space.
    Refuses: an unknown id; a moved object that is deleted; an added id that is the id of
    a source object (a deleted id is never reused) or repeated; an added (type, size)
    that is not an entry of the object library; a centre outside the space.
    """
    space = source["space"]
    W, H = float(space["width"]), float(space["height"])
    source_ids = [str(o["id"]) for o in source["env_objects"]]
    deleted_set = set(deleted)
    for oid in deleted_set:
        if oid not in source_ids:
            raise ValueError(f"cannot delete '{oid}': no such object in the source layout")
    moves = {}
    for oid, pos in positions.items():
        if oid not in source_ids:
            raise ValueError(f"no object '{oid}' in the source layout")
        if oid in deleted_set:
            raise ValueError(f"'{oid}' is moved and deleted")
        moves[oid] = _point(oid, pos, W, H)
    allowed = set(library)
    new_objects = []
    seen = set()
    for a in added:
        if not isinstance(a, dict) or not {"id", "type", "size", "position"} <= set(a):
            raise ValueError("an added object has the fields id, type, size, position")
        oid = str(a["id"])
        if not oid:
            raise ValueError("an added object has an empty id")
        if oid in source_ids or oid in seen:
            raise ValueError(f"added id '{oid}' is not unique")
        seen.add(oid)
        try:
            size = (float(a["size"][0]), float(a["size"][1]))
        except (TypeError, ValueError, IndexError):
            raise ValueError(f"'{oid}': a size is two numbers")
        if (str(a["type"]), size) not in allowed:
            raise ValueError(f"'{oid}': type {a['type']} with size {list(size)} is not in the object library")
        new_objects.append({"id": oid, "type": str(a["type"]), "position": _point(oid, a["position"], W, H),
                            "size": [_clean(size[0]), _clean(size[1])]})
    new = copy.deepcopy(source)
    new["space"]["name"] = name
    kept = []
    for o in new["env_objects"]:
        oid = str(o["id"])
        if oid in deleted_set:
            continue
        if oid in moves:
            o["position"] = moves[oid]
        kept.append(o)
    new["env_objects"] = kept + new_objects
    return new


def drawing_layout(source: dict, objects: List[dict]) -> dict:
    """The layout to draw for the page's state: the source's space and areas, the page's objects."""
    return {"space": source["space"], "areas": source["areas"],
            "env_objects": [{"id": str(o["id"]), "type": str(o["type"]), "position": o["position"],
                             "size": o["size"]} for o in objects]}


def cmd_edit(source_path: Path) -> None:
    source = load_layout(source_path)
    folder = source_path.resolve().parent
    units = str(source["space"].get("units", ""))
    library = object_library(folder)

    def embed(value) -> str:
        return json.dumps(value).replace("</", "<\\/")

    def page() -> bytes:
        existing = sorted(p.name for p in folder.iterdir())
        html = (PAGE.replace("__SVG__", layout_svg(source, grid=True))
                    .replace("__SOURCE__", escape(source_path.name))
                    .replace("__GRID__", str(GRID_CM))
                    .replace("__UNITS__", escape(units))
                    .replace("__EXISTING__", embed(existing))
                    .replace("__LIBRARY__", embed([{"type": t, "size": [_clean(w), _clean(h)]}
                                                    for t, (w, h) in library]))
                    .replace("__SOURCE_IDS__", embed([str(o["id"]) for o in source["env_objects"]])))
        return html.encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        def _send(self, code: int, body: bytes, ctype: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _json(self, code: int, obj: dict) -> None:
            self._send(code, json.dumps(obj).encode("utf-8"), "application/json")

        def _body(self) -> dict:
            return json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))

        def do_GET(self) -> None:
            if self.path == "/":
                self._send(200, page(), "text/html; charset=utf-8")
            else:
                self._send(404, b"not found", "text/plain")

        def do_POST(self) -> None:
            if self.path == "/svg":
                try:
                    svg = layout_svg(drawing_layout(source, self._body()["objects"]), grid=True)
                except (KeyError, TypeError, ValueError, IndexError) as e:
                    self._send(400, f"bad state: {e}".encode("utf-8"), "text/plain")
                    return
                self._send(200, svg.encode("utf-8"), "image/svg+xml")
                return
            if self.path != "/save":
                self._send(404, b"not found", "text/plain")
                return
            try:
                req = self._body()
                name = str(req.get("name", "")).strip()
                problem = name_problem(name, folder)
                if problem:
                    raise ValueError(problem)
                new = edited_layout(source, name, library, req.get("positions", {}),
                                    req.get("added", []), req.get("deleted", []))
                json_out, png_out = folder / f"{name}.json", folder / f"{name}.png"
                with open(json_out, "x", encoding="utf-8") as f:   # "x": never overwrite
                    f.write(json.dumps(new, indent=2, ensure_ascii=False) + "\n")
                write_png(new, png_out)
            except (ValueError, AttributeError) as e:
                self._json(400, {"error": str(e)})
                return
            except FileExistsError as e:
                self._json(400, {"error": f"{e.filename} exists already"})
                return
            print(f"saved {json_out}\nsaved {png_out}")
            self._json(200, {"json": str(json_out), "png": str(png_out)})

        def log_message(self, fmt: str, *args) -> None:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    url = f"http://127.0.0.1:{server.server_address[1]}/"
    print(f"editing {source_path} at {url}  (Ctrl+C stops)")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        server.server_close()


# =============================================================================
# main
# =============================================================================

def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    r = sub.add_parser("render", help="write <stem>.png beside each layout file")
    r.add_argument("paths", nargs="+", help="layout files or folders of layout files")
    e = sub.add_parser("edit", help="drag the fixed objects of a layout and save it as a new layout")
    e.add_argument("layout", help="the source layout file (never modified)")
    args = parser.parse_args(argv)
    try:
        if args.command == "render":
            cmd_render(args.paths)
        else:
            cmd_edit(Path(args.layout))
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"layout_tool: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
