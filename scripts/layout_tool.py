# scripts/layout_tool.py
"""
Draw layout files, and derive a new layout from one by dragging its fixed objects.

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
the layout file (cairosvg); "edit" serves the same SVG in a page whose JavaScript only
moves the existing object elements.
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
from typing import Dict, List
from xml.sax.saxutils import escape, quoteattr

LAYOUT_KEYS = ("space", "areas", "env_objects")
PNG_WIDTH_PX = 1600   # the larger side of the drawing in the PNG and on the page
GRID_CM = 10          # the edit page's snap step, in the layout's units

# One colour per type. A type's colour is chosen by a stable hash of its name, so a type
# keeps its colour from one layout to the next; two types of one layout that hash to the
# same colour are separated by taking the next free colour, in sorted type order.
PALETTE = (
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
        i = zlib.crc32(t.encode("utf-8")) % len(PALETTE)
        for k in range(len(PALETTE)):
            c = PALETTE[(i + k) % len(PALETTE)]
            if c not in taken or len(taken) >= len(PALETTE):
                break
        colours[t] = c
        taken.add(c)
    return colours


def _num(v: float) -> str:
    return f"{v:g}"


# =============================================================================
# Drawing
# =============================================================================

def layout_svg(layout: dict) -> str:
    """
    The drawing of a parsed layout as SVG text. SVG user units are the layout's units;
    the layout point (x, y) is drawn at SVG (x, -y), so y points up.

    Each entry of env_objects is one <g class="obj"> element carrying the object's id
    (data-id), its type (data-type) and its position (data-x, data-y), translated to its
    centre; its rectangle and label are drawn about (0, 0) inside it.
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

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>Layout editor: __SOURCE__</title>
<style>
  body { font-family: sans-serif; margin: 12px; background: #fafafa; }
  #bar { margin-bottom: 8px; }
  #bar input { width: 18em; }
  #check, #status { margin-left: 1em; }
  .bad { color: #b00020; }
  .ok { color: #1b6e20; }
  svg { max-width: 100%; height: auto; max-height: 82vh; background: #fff; border: 1px solid #ccc; }
  g.obj { cursor: move; }
  g.obj.refused rect { stroke: #b00020; stroke-width: 6; }
</style></head>
<body>
<div id="bar">
  <b>__SOURCE__</b> &nbsp; Save as
  <input id="name" placeholder="new layout id (file stem)">.json
  <button id="save" disabled>Save as</button>
  <span id="check"></span>
</div>
<div id="status">Drag an object to move it; positions snap to __GRID__ __UNITS__. The source is never modified.</div>
__SVG__
<div id="moved"></div>
<script>
"use strict";
const GRID = __GRID__;
const EXISTING = new Set(__EXISTING__);
const svg = document.getElementById("layout");
const W = parseFloat(svg.dataset.width), H = parseFloat(svg.dataset.height);
const status = document.getElementById("status");
const movedBox = document.getElementById("moved");
const moved = {};   // id -> [x, y], layout coordinates, objects whose position changed

function inside(x, y) { return x >= -W / 2 && x <= W / 2 && y >= -H / 2 && y <= H / 2; }
function place(g, x, y) {
  g.dataset.x = x; g.dataset.y = y;
  g.setAttribute("transform", "translate(" + x + " " + (-y) + ")");
}
function svgPoint(evt) {
  const p = svg.createSVGPoint(); p.x = evt.clientX; p.y = evt.clientY;
  const q = p.matrixTransform(svg.getScreenCTM().inverse());
  return [q.x, -q.y];   // layout coordinates, y up
}
function showMoved() {
  const ids = Object.keys(moved).sort();
  movedBox.textContent = ids.length ? "Moved: " + ids.map(i => i + " (" + moved[i] + ")").join(", ") : "";
}

for (const g of svg.querySelectorAll("g.obj")) {
  const x0 = parseFloat(g.dataset.x), y0 = parseFloat(g.dataset.y);
  let drag = null;
  g.addEventListener("pointerdown", evt => {
    const [px, py] = svgPoint(evt);
    drag = { dx: parseFloat(g.dataset.x) - px, dy: parseFloat(g.dataset.y) - py };
    g.setPointerCapture(evt.pointerId);
    evt.preventDefault();
  });
  g.addEventListener("pointermove", evt => {
    if (!drag) return;
    const [px, py] = svgPoint(evt);
    const x = Math.round((px + drag.dx) / GRID) * GRID;
    const y = Math.round((py + drag.dy) / GRID) * GRID;
    if (!inside(x, y)) {
      g.classList.add("refused");
      status.innerHTML = '<span class="bad">' + g.dataset.id + ": (" + x + ", " + y +
        ") is outside the space; kept at (" + g.dataset.x + ", " + g.dataset.y + ")</span>";
      return;
    }
    g.classList.remove("refused");
    place(g, x, y);
    status.textContent = g.dataset.id + ": (" + x + ", " + y + ")";
  });
  const end = () => {
    if (!drag) return;
    drag = null;
    g.classList.remove("refused");
    const x = parseFloat(g.dataset.x), y = parseFloat(g.dataset.y);
    if (x === x0 && y === y0) delete moved[g.dataset.id]; else moved[g.dataset.id] = [x, y];
    showMoved();
  };
  g.addEventListener("pointerup", end);
  g.addEventListener("pointercancel", end);
}

const nameBox = document.getElementById("name");
const saveBtn = document.getElementById("save");
const check = document.getElementById("check");
// The name is the new layout's id, its file stem: the file is <name>.json in the source's
// folder. domains/discovery.py registers every *.json directly in a layouts folder, keyed by
// its stem.
function nameProblem(n) {
  if (n === "") return "type a name";
  if (/[\\/\\\\]/.test(n)) return "no folder separators: the file goes into the source layout's folder";
  if (/\\.json$/i.test(n)) return "type the id without .json (the file would be " + n + ".json, its id " + n + ")";
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
  const resp = await fetch("/save", { method: "POST", headers: { "Content-Type": "application/json" },
                                      body: JSON.stringify({ name: name, positions: moved }) });
  const res = await resp.json();
  if (resp.ok) {
    EXISTING.add(name + ".json"); EXISTING.add(name + ".png");
    status.innerHTML = '<span class="ok">Saved ' + res.json + " and " + res.png + "</span>";
  } else {
    status.innerHTML = '<span class="bad">Not saved: ' + res.error + "</span>";
  }
  recheck();
});
</script>
</body></html>
"""


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


def moved_layout(source: dict, positions: Dict[str, list]) -> dict:
    """
    The source layout with the positions of the named env_objects replaced; everything
    else (ids, types, sizes, areas, the space) unchanged. Refuses an unknown id or a centre
    outside the space.
    """
    space = source["space"]
    W, H = float(space["width"]), float(space["height"])
    new = copy.deepcopy(source)
    by_id = {str(o["id"]): o for o in new["env_objects"]}
    for oid, pos in positions.items():
        if oid not in by_id:
            raise ValueError(f"no object '{oid}' in the source layout")
        if (not isinstance(pos, list) or len(pos) != 2
                or not all(isinstance(v, (int, float)) and math.isfinite(v) for v in pos)):
            raise ValueError(f"'{oid}': a position is two numbers")
        x, y = pos
        if not (-W / 2 <= x <= W / 2 and -H / 2 <= y <= H / 2):
            raise ValueError(f"'{oid}': ({x:g}, {y:g}) is outside the space")
        by_id[oid]["position"] = [int(v) if float(v).is_integer() else v for v in pos]
    return new


def cmd_edit(source_path: Path) -> None:
    source = load_layout(source_path)
    folder = source_path.resolve().parent
    units = str(source["space"].get("units", ""))

    def page() -> bytes:
        existing = sorted(p.name for p in folder.iterdir())
        html = (PAGE.replace("__SVG__", layout_svg(source))
                    .replace("__SOURCE__", escape(source_path.name))
                    .replace("__GRID__", str(GRID_CM))
                    .replace("__UNITS__", escape(units))
                    .replace("__EXISTING__", json.dumps(existing)))
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

        def do_GET(self) -> None:
            if self.path == "/":
                self._send(200, page(), "text/html; charset=utf-8")
            else:
                self._send(404, b"not found", "text/plain")

        def do_POST(self) -> None:
            if self.path != "/save":
                self._send(404, b"not found", "text/plain")
                return
            try:
                req = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
                name = str(req.get("name", "")).strip()
                problem = name_problem(name, folder)
                if problem:
                    raise ValueError(problem)
                new = moved_layout(source, req.get("positions", {}))
                json_out, png_out = folder / f"{name}.json", folder / f"{name}.png"
                with open(json_out, "x", encoding="utf-8") as f:   # "x": never overwrite
                    f.write(json.dumps(new, indent=2, ensure_ascii=False) + "\n")
                write_png(new, png_out)
            except ValueError as e:
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
