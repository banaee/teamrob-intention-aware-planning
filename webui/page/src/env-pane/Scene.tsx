/**
 * The scene at one moment, drawn from the room (what is constant: a sim-run's run description, or a view of a layout
 * and a setup) and the moment (what changes: a tick update's world, or a view's start without agents), and the
 * domain's scene appearance (how things look). Three levels of presence: the space, the areas and the
 * background objects as lines and pale faces; the active objects with a representative form and a warm tone; the
 * agents as figures in their semantic colours. The movable objects are solid ink: what can change stands out.
 *
 * A movable object in a fixed object is drawn at its display place (src/env-pane/places.ts), from the place book the
 * page keeps over the sequence of tick updates (`book`). An object's look follows the states that hold for it (its
 * look by state, src/env-pane/look.ts).
 *
 * What is constant is drawn once per sim-run (the fixed objects again when an object state changes); a tick moves the
 * existing shapes. An agent moves smoothly from its last
 * position to the tick's over `glideMs` (during play), or is put there at once (`glideMs` 0: paused, or a step), so
 * that a paused scene shows exactly the tick's positions. It turns at once to its last motion.
 *
 * What lies ahead of the agents (T-viz 1d and 1e) is drawn on the floor by src/env-pane/Paths.tsx, from the tick
 * update's walks ahead and projection ahead (`ahead`), each drawing shown by its switch (`shown`).
 *
 * Nothing here names a domain, an object type or an area id: they arrive as data.
 */

import { Html, Line, Text } from "@react-three/drei";
import { useFrame } from "@react-three/fiber";
import { type ReactNode, useLayoutEffect, useMemo, useRef } from "react";
import * as THREE from "three";

import plexMono from "@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff?url";

import type {
  AgentTick, Appearance, Area, Bounds, Carried, FixedObject, FixedObjectContents, MovableObject, ObjectState, Space,
} from "../gen/messages";
import { theme } from "../theme";
import { heldBy, statesHeld } from "./look";
import { type Place, type PlaceBook, placeGrid, slotOf } from "./places";
import { carryHeight, carryOffset, FigureForm, ringRadius } from "./figures";
import type { Ahead, PathsShown } from "./paths";
import { Paths } from "./Paths";
import { FixedForm, MovableForm, restHeight } from "./forms";
import { fixedLook, movableLook } from "./look";
import { at, Block, type Paint, paints, SoftShadow } from "./solids";

const FLOOR_DEPTH = 12;
const AREA_INSET = 10;
const SHADOW_SHARE = 0.12;        // a shadow's offset to the south-east, as a share of the form's height
const SHADOW_MAX = 18;
const LABEL_GAP = 10;

const floorPaint: Paint = {
  tone: { top: theme.color.floor, light: theme.color.floorEdge, shade: theme.color.floorEdge, hatch: theme.color.hatch },
  line: theme.color.line,
  lineWidth: theme.line.floor,
};

/** What is constant in the scene: a sim-run's world, or a view's layout with the setup's movable objects. `key` names
 * it (a sim-run, or a view), so that a new one is drawn anew. */
export interface Room {
  key: string;
  space: Space;
  areas: readonly Area[];
  fixed_objects: readonly FixedObject[];
  movable_objects: readonly MovableObject[];
}

/** What changes: the agents, where the movable objects are, the object states. A view's moment has no agent. */
export interface Moment {
  humans: readonly AgentTick[];
  robots: readonly AgentTick[];
  fixed_object_contents: readonly FixedObjectContents[];
  carried: readonly Carried[];
  object_states: readonly ObjectState[];
}

export function Scene({ room, moment, book, appearance, glideMs, ahead, shown }: {
  room: Room; moment: Moment; book: PlaceBook; appearance: Appearance; glideMs: number; ahead: Ahead;
  shown: PathsShown;
}) {
  const world = room;
  const fixedById = useMemo(() => new Map(world.fixed_objects.map((f) => [f.id, f])), [world]);
  const movableById = useMemo(() => new Map(world.movable_objects.map((o) => [o.id, o])), [world]);
  // The object states as a key, so that the fixed objects are drawn again only when one changes.
  const statesKey = JSON.stringify(moment.object_states);
  const held = useMemo(() => statesHeld(moment.object_states), [statesKey]);
  const constant = useMemo(() => (
    <group>
      <Floor bounds={world.space.bounds} />
      {world.areas.map((area) => (
        <AreaMark key={area.id} bounds={area.bounds} />
      ))}
      {world.fixed_objects.map((f) => (
        <Fixed key={f.id} f={f} appearance={appearance} held={heldBy(held, f.id)} bounds={world.space.bounds} />
      ))}
    </group>
  ), [world, appearance, held]);

  // The run's largest movable extents, the grid of each fixed object (fixed for the sim-run), and the height of one
  // layer of objects: the tallest look a movable object of the run may take.
  const largest = useMemo(() => ({
    x: Math.max(1, ...world.movable_objects.map((o) => o.size.x)),
    y: Math.max(1, ...world.movable_objects.map((o) => o.size.y)),
  }), [world]);
  const grids = useMemo(() => new Map<string, Place[]>(), [world, largest]);
  const gridOf = (f: FixedObject) => {
    if (!grids.has(f.id)) {
      grids.set(f.id, placeGrid({ x: f.position.x, y: f.position.y, sx: f.size.x, sy: f.size.y }, largest));
    }
    return grids.get(f.id)!;
  };
  const layerHeight = useMemo(() => Math.max(0, ...world.movable_objects.flatMap((o) => {
    const entry = appearance.movable[o.type];
    return entry === undefined ? [appearance.default_movable.height]
      : [entry.height, ...entry.states.map((s) => s.look.height)];
  })), [world, appearance]);

  // The robot's expectation of the human as wide as the human's ring: where the human is where expected, its ring lies
  // in the stripe.
  const stripeWidth = 2 * ringRadius(appearance.human.figure, appearance.human.height);

  return (
    <group>
      {constant}

      <Paths ahead={ahead} shown={shown} stripeWidth={stripeWidth} />

      {moment.fixed_object_contents.flatMap((contents) => {
        const holder = fixedById.get(contents.fixed_object);
        if (!holder) return [];
        const holderLook = fixedLook(appearance, holder.type, heldBy(held, holder.id));
        const grid = gridOf(holder);
        const numbers = book.get(holder.id);
        const base = restHeight(holderLook.shape, holderLook.height);
        return contents.movable_objects.map((id, i) => {
          const o = movableById.get(id)!;
          const look = movableLook(appearance, o.type, heldBy(held, o.id));
          const slot = slotOf(grid, numbers?.get(id) ?? i);
          return <MovableForm key={o.id} shape={look.shape} x={slot.x} y={slot.y} sx={o.size.x} sy={o.size.y}
                              h={look.height} base={base + slot.layer * layerHeight} paint={paints.movable} />;
        });
      })}

      {[...moment.humans.map((a) => ({ a, figure: appearance.human, paint: paints.human, colour: theme.color.human })),
        ...moment.robots.map((a) => ({ a, figure: appearance.robot, paint: paints.robot, colour: theme.color.robot }))]
        .map(({ a, figure, paint, colour }) => {
          // Drawn at the group's origin; the group carries the agent to its position.
          const stance = { x: 0, y: 0, facing: a.last_motion };
          const carried = moment.carried.filter((c) => c.agent === a.id).map((c) => movableById.get(c.movable_object)!);
          const hold = carryOffset(figure.figure, figure.height, a.last_motion);
          return (
            <Gliding key={`${room.key} ${a.id}`} x={a.position.x} y={a.position.y} glideMs={glideMs}>
              <FigureForm figure={figure.figure} h={figure.height} stance={stance} paint={paint} />
              {carried.map((o) => {
                const look = movableLook(appearance, o.type, heldBy(held, o.id));
                return <MovableForm key={o.id} shape={look.shape} x={hold.x} y={hold.y}
                                    sx={o.size.x} sy={o.size.y} h={look.height}
                                    base={carryHeight(figure.figure, figure.height)} paint={paints.movable} />;
              })}
              <Pill position={at(0, 0, figure.height)} text={a.id} dot={colour} />
            </Gliding>
          );
        })}
    </group>
  );
}

/** A group at a point of the floor that moves to a new point over `glideMs`, from where it is drawn now; at once when
 * `glideMs` is 0. A display convention between two ticks: the world knows only the ticks' positions. */
function Gliding({ x, y, glideMs, children }: { x: number; y: number; glideMs: number; children: ReactNode }) {
  const group = useRef<THREE.Group>(null);
  const glide = useRef({ fromX: x, fromY: y, toX: x, toY: y, start: 0, ms: 0 });

  useLayoutEffect(() => {
    const g = group.current!;
    const placed = glide.current.start === 0;
    glide.current = {
      fromX: placed ? x : g.position.x, fromY: placed ? y : -g.position.z, toX: x, toY: y,
      start: performance.now(), ms: glideMs,
    };
    if (placed || glideMs <= 0) g.position.set(...at(x, y));
  }, [x, y, glideMs]);

  useFrame(() => {
    const { fromX, fromY, toX, toY, start, ms } = glide.current;
    if (ms <= 0) return;
    const k = Math.min(1, (performance.now() - start) / ms);
    group.current!.position.set(...at(fromX + k * (toX - fromX), fromY + k * (toY - fromY)));
  });

  return <group ref={group}>{children}</group>;
}

/** The space: a floor plate with its outline, and a faint dot grid at the floor's step. */
function Floor({ bounds }: { bounds: Bounds }) {
  const sx = bounds.x_max - bounds.x_min;
  const sy = bounds.y_max - bounds.y_min;
  const cx = (bounds.x_min + bounds.x_max) / 2;
  const cy = (bounds.y_min + bounds.y_max) / 2;
  const grid = useMemo(() => {
    const step = theme.scene.gridStep;
    const points: number[] = [];
    for (let x = Math.ceil(bounds.x_min / step) * step + step; x < bounds.x_max; x += step)
      for (let y = Math.ceil(bounds.y_min / step) * step + step; y < bounds.y_max; y += step)
        points.push(...at(x, y, 0.2));
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute("position", new THREE.Float32BufferAttribute(points, 3));
    return geometry;
  }, [bounds]);
  return (
    <group>
      <Block x={cx} y={cy} sx={sx} sy={sy} h={FLOOR_DEPTH} base={-FLOOR_DEPTH} paint={floorPaint} />
      <points geometry={grid}>
        <pointsMaterial color={theme.color.lineFaint} size={2} sizeAttenuation={false} />
      </points>
    </group>
  );
}

/** An area: a dashed outline just inside its bounds. Its id is not written on the floor (Hadi, 8 October 2026,
 * preferred: no area names in the scene). */
function AreaMark({ bounds }: { bounds: Bounds }) {
  const x0 = bounds.x_min + AREA_INSET;
  const x1 = bounds.x_max - AREA_INSET;
  const y0 = bounds.y_min + AREA_INSET;
  const y1 = bounds.y_max - AREA_INSET;
  const lift = 0.3;
  return (
    <Line points={[at(x0, y0, lift), at(x1, y0, lift), at(x1, y1, lift), at(x0, y1, lift), at(x0, y0, lift)]}
          color={theme.color.lineFaint} lineWidth={theme.line.area} dashed dashSize={14} gapSize={10} />
  );
}

function Fixed({ f, appearance, held, bounds }: {
  f: FixedObject; appearance: Appearance; held: ReadonlySet<string>; bounds: Bounds;
}) {
  const look = fixedLook(appearance, f.type, held);
  const paint = look.presence === "active" ? paints.active : paints.background;
  const offset = Math.min(SHADOW_SHARE * look.height, SHADOW_MAX);
  const footing = { x: f.position.x, y: f.position.y, sx: f.size.x, sy: f.size.y, h: look.height };
  // The id on the floor south of the footprint, or north of it where the floor ends.
  const south = f.position.y - f.size.y / 2 - LABEL_GAP;
  const active = look.presence === "active";
  const labelSize = active ? theme.scene.activeLabel : theme.scene.passiveLabel;
  const below = south - labelSize > bounds.y_min;
  return (
    <group>
      {look.height > 0 && (
        <SoftShadow x={f.position.x + offset} y={f.position.y - offset} sx={f.size.x} sy={f.size.y}
                    colour={theme.color.shadow} opacity={theme.opacity.shadow} />
      )}
      <FixedForm shape={look.shape} f={footing} paint={paint} />
      <FloorText text={f.id} x={f.position.x - f.size.x / 2}
                 y={below ? south : f.position.y + f.size.y / 2 + LABEL_GAP} size={labelSize}
                 colour={active ? theme.color.activeLine : theme.color.labelFaint}
                 anchorY={below ? "top" : "bottom"} />
    </group>
  );
}

/** Text lying on the floor, read with north up. */
function FloorText({ text, x, y, size, colour, anchorX = "left", anchorY }: {
  text: string; x: number; y: number; size: number; colour: string; anchorX?: "left" | "center";
  anchorY: "top" | "bottom" | "middle";
}) {
  return (
    <Text font={plexMono} position={at(x, y, 0.5)} rotation={[-Math.PI / 2, 0, 0]} fontSize={size} color={colour}
          anchorX={anchorX} anchorY={anchorY} letterSpacing={0.04}>
      {text}
    </Text>
  );
}

/** A label above an agent: a white pill with a dot of the agent's colour (sketch J, image 13). */
function Pill({ position, text, dot }: { position: [number, number, number]; text: string; dot: string }) {
  return (
    <Html position={position} center zIndexRange={[10, 0]} className="scene-pill-anchor">
      <div className="scene-pill">
        <span className="scene-pill-dot" style={{ background: dot }} />
        {text}
      </div>
    </Html>
  );
}
