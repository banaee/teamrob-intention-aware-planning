# scripts/layout_tool.py
"""
Draw layout files.

    python scripts/layout_tool.py render <path> [<path> ...]

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
the layout file (cairosvg).
"""

import argparse
import json
import math
import sys
import zlib
from pathlib import Path
from typing import Dict, List
from xml.sax.saxutils import escape, quoteattr

LAYOUT_KEYS = ("space", "areas", "env_objects")
PNG_WIDTH_PX = 1600   # the larger side of the drawing in the PNG

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
# main
# =============================================================================

def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    r = sub.add_parser("render", help="write <stem>.png beside each layout file")
    r.add_argument("paths", nargs="+", help="layout files or folders of layout files")
    args = parser.parse_args(argv)
    try:
        cmd_render(args.paths)
    except (ValueError, OSError, json.JSONDecodeError) as e:
        print(f"layout_tool: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
