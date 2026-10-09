/**
 * The forms of the shape vocabulary (webui/appearance.py): one drawing per form, over a fixed object's footprint and
 * height; the movable objects' forms; and the height at which a form holds its contents. The vocabulary names forms,
 * never a domain's object types. No form has a front: the messages carry no orientation (TODO-192).
 */

import { Line } from "@react-three/drei";
import { useMemo } from "react";

import type { MovableShape, ShapeKind } from "../gen/messages";
import { theme } from "../theme";
import { at, Block, Cylinder, FloorPatch, type Paint, rectangle, stroke } from "./solids";

export interface Footing {
  x: number;
  y: number;
  sx: number;
  sy: number;
  h: number;
}

const BOARD = 3;          // a board's thickness, in the layout's unit
const POST = 4;           // a post's side
const WALL = 5;           // an enclosure's wall
const BOARD_LEVELS = [0.12, 0.55];   // a rack's boards, as shares of its height; contents on the upper one

/** The height at which a form holds the movable objects in it (the display places' level). */
export function restHeight(shape: ShapeKind, h: number): number {
  switch (shape) {
    case "rack": return BOARD_LEVELS[BOARD_LEVELS.length - 1] * h + BOARD;
    case "pad": return 0.6;
    case "enclosure": return BOARD;
    case "seat": return 0.55 * h + 6;
    default: return h;
  }
}

export function FixedForm({ shape, f, paint }: { shape: ShapeKind; f: Footing; paint: Paint }) {
  switch (shape) {
    case "block": return <Block x={f.x} y={f.y} sx={f.sx} sy={f.sy} h={f.h} paint={paint} />;
    case "rack": return <Rack f={f} paint={paint} />;
    case "counter": return <Counter f={f} paint={paint} />;
    case "pad": return <Pad f={f} paint={paint} />;
    case "enclosure": return <Enclosure f={f} paint={paint} />;
    case "appliance": return <Appliance f={f} paint={paint} />;
    case "panel": return <Panel f={f} paint={paint} />;
    case "seat": return <Seat f={f} paint={paint} />;
    case "marker": return <Marker f={f} paint={paint} />;
    case "barrier": return <Barrier f={f} paint={paint} />;
  }
}

function corners(f: Footing, inset: number): [number, number][] {
  const dx = f.sx / 2 - inset;
  const dy = f.sy / 2 - inset;
  return [[f.x - dx, f.y - dy], [f.x + dx, f.y - dy], [f.x + dx, f.y + dy], [f.x - dx, f.y + dy]];
}

/** Four posts and two boards, open above: what it holds stays visible from above. */
function Rack({ f, paint }: { f: Footing; paint: Paint }) {
  return (
    <group>
      {corners(f, POST / 2).map(([x, y], i) => (
        <Block key={i} x={x} y={y} sx={POST} sy={POST} h={f.h} paint={stroke(paint)} />
      ))}
      {BOARD_LEVELS.map((level) => (
        <Block key={level} x={f.x} y={f.y} sx={f.sx} sy={f.sy} h={BOARD} base={level * f.h} paint={paint} />
      ))}
    </group>
  );
}

/** A top on four legs. The top is see-through, its outline kept, so that an agent at it is not hidden (Hadi, 6
 * October 2026, P21). */
function Counter({ f, paint }: { f: Footing; paint: Paint }) {
  const top = 5;
  return (
    <group>
      {corners(f, 6).map(([x, y], i) => (
        <Block key={i} x={x} y={y} sx={POST} sy={POST} h={f.h - top} paint={stroke(paint)} />
      ))}
      <Block x={f.x} y={f.y} sx={f.sx} sy={f.sy} h={top} base={f.h - top}
             paint={{ ...paint, opacity: theme.opacity.counterTop }} />
    </group>
  );
}

/** A marked rectangle on the floor: its outline, a faint fill and short ticks at its corners. */
function Pad({ f, paint }: { f: Footing; paint: Paint }) {
  const shape = useMemo(() => rectangle(f.sx, f.sy), [f.sx, f.sy]);
  const tick = Math.min(f.sx, f.sy) * 0.14;
  const lift = 0.6;
  const outline = corners(f, 0).map(([x, y]) => at(x, y, lift));
  const inner = corners(f, tick * 0.5);
  return (
    <group>
      <FloorPatch x={f.x} y={f.y} shape={shape} colour={paint.tone.light} opacity={1} lift={0.3} />
      <Line points={[...outline, outline[0]]} color={paint.line} lineWidth={paint.lineWidth} />
      {inner.map(([x, y], i) => {
        const sx = Math.sign(x - f.x);
        const sy = Math.sign(y - f.y);
        return (
          <Line key={i} color={paint.line} lineWidth={paint.lineWidth}
                points={[at(x - sx * tick, y, lift), at(x, y, lift), at(x, y - sy * tick, lift)]} />
        );
      })}
    </group>
  );
}

/** A floor and low walls on every side, no roof. */
function Enclosure({ f, paint }: { f: Footing; paint: Paint }) {
  const walled = { ...paint, opacity: theme.opacity.barrierFace };
  return (
    <group>
      <Block x={f.x} y={f.y} sx={f.sx} sy={f.sy} h={BOARD} paint={paint} />
      <Block x={f.x} y={f.y + f.sy / 2 - WALL / 2} sx={f.sx} sy={WALL} h={f.h} paint={walled} />
      <Block x={f.x} y={f.y - f.sy / 2 + WALL / 2} sx={f.sx} sy={WALL} h={f.h} paint={walled} />
      <Block x={f.x - f.sx / 2 + WALL / 2} y={f.y} sx={WALL} sy={f.sy - 2 * WALL} h={f.h} paint={walled} />
      <Block x={f.x + f.sx / 2 - WALL / 2} y={f.y} sx={WALL} sy={f.sy - 2 * WALL} h={f.h} paint={walled} />
    </group>
  );
}

/** A box with a cup on its top: an object that serves something. */
function Appliance({ f, paint }: { f: Footing; paint: Paint }) {
  const r = 0.2 * Math.min(f.sx, f.sy);
  const body = 0.82 * f.h;
  return (
    <group>
      <Block x={f.x} y={f.y} sx={f.sx} sy={f.sy} h={body} paint={paint} />
      <Block x={f.x} y={f.y} sx={f.sx * 0.86} sy={f.sy * 0.86} h={0.06 * f.h} base={body} paint={paint} />
      <Cylinder x={f.x} y={f.y} r={r * 0.8} rTop={r} h={0.12 * f.h} base={0.88 * f.h} paint={paint} />
    </group>
  );
}

/** A plate on a slim post, with a round dial on its top. */
function Panel({ f, paint }: { f: Footing; paint: Paint }) {
  const plate = Math.max(0.22 * f.h, 18);
  const post = f.h - plate;
  return (
    <group>
      <Block x={f.x} y={f.y} sx={POST} sy={POST} h={post} paint={stroke(paint)} />
      <Block x={f.x} y={f.y} sx={f.sx} sy={f.sy} h={plate} base={post} paint={paint} />
      <Cylinder x={f.x} y={f.y} r={0.3 * Math.min(f.sx, f.sy)} h={2.5} base={f.h} paint={paint} />
    </group>
  );
}

/** A round seat on a stem and a base. */
function Seat({ f, paint }: { f: Footing; paint: Paint }) {
  const r = 0.48 * Math.min(f.sx, f.sy);
  return (
    <group>
      <Cylinder x={f.x} y={f.y} r={r * 0.75} h={3} paint={paint} />
      <Cylinder x={f.x} y={f.y} r={3} h={0.55 * f.h} paint={stroke(paint)} segments={12} />
      <Cylinder x={f.x} y={f.y} r={r} h={6} base={0.55 * f.h} paint={paint} />
    </group>
  );
}

/** A slim post with a small diamond on its top. */
function Marker({ f, paint }: { f: Footing; paint: Paint }) {
  const r = 0.4 * Math.min(f.sx, f.sy);
  return (
    <group>
      <Cylinder x={f.x} y={f.y} r={1.6} h={f.h - r} paint={stroke(paint)} segments={10} />
      <Diamond x={f.x} y={f.y} r={r} centre={f.h - r / 2} paint={paint} />
    </group>
  );
}

function Diamond({ x, y, r, centre, paint }: { x: number; y: number; r: number; centre: number; paint: Paint }) {
  return (
    <group>
      <Cylinder x={x} y={y} r={r} rTop={0.01} h={r} base={centre} paint={paint} segments={4} />
      <Cylinder x={x} y={y} r={0.01} rTop={r} h={r} base={centre - r} paint={paint} segments={4} />
    </group>
  );
}

/** A frame over the footprint: two posts, a beam and a pane one sees through, so it hides little. */
function Barrier({ f, paint }: { f: Footing; paint: Paint }) {
  const along = f.sx >= f.sy;
  const length = along ? f.sx : f.sy;
  const depth = along ? f.sy : f.sx;
  const beam = 6;
  const pane = { ...paint, opacity: theme.opacity.barrierFace };
  const end = (s: number) => (along ? { x: f.x + s * (length / 2 - POST / 2), y: f.y }
                                    : { x: f.x, y: f.y + s * (length / 2 - POST / 2) });
  const post = { sx: along ? POST : depth, sy: along ? depth : POST };
  const inner = { sx: along ? length - 2 * POST : depth * 0.4, sy: along ? depth * 0.4 : length - 2 * POST };
  return (
    <group>
      {[-1, 1].map((s) => <Block key={s} {...end(s)} {...post} h={f.h} paint={paint} />)}
      <Block x={f.x} y={f.y} sx={along ? length : depth} sy={along ? depth : length} h={beam} base={f.h - beam}
             paint={paint} />
      <Block x={f.x} y={f.y} {...inner} h={f.h - beam} paint={pane} />
    </group>
  );
}

/** A movable object's form, its base at `base`. */
export function MovableForm({ shape, x, y, sx, sy, h, base, paint }: {
  shape: MovableShape; x: number; y: number; sx: number; sy: number; h: number; base: number; paint: Paint;
}) {
  switch (shape) {
    case "crate":
      return (
        <group>
          <Block x={x} y={y} sx={sx} sy={sy} h={h * 0.82} base={base} paint={paint} />
          <Block x={x} y={y} sx={sx * 1.04} sy={sy * 1.04} h={h * 0.18} base={base + h * 0.82} paint={paint} />
        </group>
      );
    case "skid":
      return <Skid x={x} y={y} sx={sx} sy={sy} h={h} base={base} paint={paint} />;
    case "loaded_skid": {
      // A skid of the low skid's height, and a closed load on it with a lid line, a little inside the skid's edges.
      const skid = Math.min(LOW_SKID, h * 0.5);
      const load = h - skid;
      return (
        <group>
          <Skid x={x} y={y} sx={sx} sy={sy} h={skid} base={base} paint={paint} />
          <Block x={x} y={y} sx={sx * 0.9} sy={sy * 0.9} h={load * 0.88} base={base + skid} paint={paint} />
          <Block x={x} y={y} sx={sx * 0.92} sy={sy * 0.92} h={load * 0.12} base={base + skid + load * 0.88}
                 paint={paint} />
        </group>
      );
    }
  }
}

const LOW_SKID = 7;       // the height of a loaded skid's skid, in the layout's unit: as high as a bare skid in the
                          // domains' data (the scene's cleaning of 9 October 2026)

/** A low slatted platform: three runners and a deck. */
function Skid({ x, y, sx, sy, h, base, paint }: {
  x: number; y: number; sx: number; sy: number; h: number; base: number; paint: Paint;
}) {
  const deck = Math.max(h * 0.3, 2.5);
  const runner = Math.min(sx, sy) * 0.14;
  const across = sx <= sy;   // runners along the longer side
  return (
    <group>
      {[-1, 0, 1].map((s) => (
        <Block key={s} x={across ? x + s * (sx / 2 - runner / 2) : x} y={across ? y : y + s * (sy / 2 - runner / 2)}
               sx={across ? runner : sx} sy={across ? sy : runner} h={h - deck} base={base} paint={paint} />
      ))}
      <Block x={x} y={y} sx={sx} sy={sy} h={deck} base={base + h - deck} paint={paint} />
    </group>
  );
}

