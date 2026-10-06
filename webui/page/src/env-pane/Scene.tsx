/**
 * The scene of one sim-run at one tick, drawn from the run description (what is constant), the tick update (what
 * changes) and the domain's scene appearance (how things look). Three levels of presence: the space, the areas and the
 * background objects as lines and pale faces; the active objects with a representative form and a warm tone; the
 * agents as figures in their semantic colours. The movable objects are solid ink: what can change stands out.
 *
 * Nothing here names a domain, an object type or an area id: they arrive as data.
 */

import { Html, Line, Text } from "@react-three/drei";
import { useMemo } from "react";
import * as THREE from "three";

import plexMono from "@fontsource/ibm-plex-mono/files/ibm-plex-mono-latin-500-normal.woff?url";

import type { Appearance, Bounds, FixedObject, RunDescription, TickUpdate } from "../gen/messages";
import { theme } from "../theme";
import { displayPlaces } from "./displayPlaces";
import { carryHeight, carryOffset, FigureForm } from "./figures";
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

export function Scene({ description, tick, appearance }: {
  description: RunDescription; tick: TickUpdate; appearance: Appearance;
}) {
  const world = description.world;
  const fixedById = useMemo(() => new Map(world.fixed_objects.map((f) => [f.id, f])), [world]);
  const movableById = useMemo(() => new Map(world.movable_objects.map((o) => [o.id, o])), [world]);

  return (
    <group>
      <Floor bounds={world.space.bounds} />
      {world.areas.map((area) => (
        <AreaMark key={area.id} id={area.id} bounds={area.bounds} space={world.space.bounds}
                  occupied={world.fixed_objects} />
      ))}

      {world.fixed_objects.map((f) => <Fixed key={f.id} f={f} appearance={appearance} bounds={world.space.bounds} />)}

      {tick.world.fixed_object_contents.flatMap((contents) => {
        const holder = fixedById.get(contents.fixed_object);
        if (!holder) return [];
        const holderLook = fixedLook(appearance, holder.type);
        const objects = contents.movable_objects.map((id) => movableById.get(id)!);
        const places = displayPlaces(
          { x: holder.position.x, y: holder.position.y, sx: holder.size.x, sy: holder.size.y },
          objects.map((o) => o.size));
        const base = restHeight(holderLook.shape, holderLook.height);
        return objects.map((o, i) => {
          const look = movableLook(appearance, o.type);
          return <MovableForm key={o.id} shape={look.shape} x={places[i].x} y={places[i].y} sx={o.size.x}
                              sy={o.size.y} h={look.height} base={base} paint={paints.movable} />;
        });
      })}

      {[...tick.world.humans.map((a) => ({ a, figure: appearance.human, paint: paints.human, colour: theme.color.human })),
        ...tick.world.robots.map((a) => ({ a, figure: appearance.robot, paint: paints.robot, colour: theme.color.robot }))]
        .map(({ a, figure, paint, colour }) => {
          const stance = { x: a.position.x, y: a.position.y, facing: a.last_motion };
          const carried = tick.world.carried.filter((c) => c.agent === a.id).map((c) => movableById.get(c.movable_object)!);
          const hold = carryOffset(figure.figure, figure.height, a.last_motion);
          return (
            <group key={a.id}>
              <FigureForm figure={figure.figure} h={figure.height} stance={stance} paint={paint} />
              {carried.map((o) => {
                const look = movableLook(appearance, o.type);
                return <MovableForm key={o.id} shape={look.shape} x={a.position.x + hold.x} y={a.position.y + hold.y}
                                    sx={o.size.x} sy={o.size.y} h={look.height}
                                    base={carryHeight(figure.figure, figure.height)} paint={paints.movable} />;
              })}
              <Pill position={at(a.position.x, a.position.y, figure.height)} text={a.id} dot={colour} />
            </group>
          );
        })}
    </group>
  );
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

/** An area: a dashed outline just inside its bounds, and its id written small and light on the floor in one of its
 * corners, the farthest from the space's centre first, where the text covers no fixed object; else at its centre. */
function AreaMark({ id, bounds, space, occupied }: {
  id: string; bounds: Bounds; space: Bounds; occupied: readonly FixedObject[];
}) {
  const x0 = bounds.x_min + AREA_INSET;
  const x1 = bounds.x_max - AREA_INSET;
  const y0 = bounds.y_min + AREA_INSET;
  const y1 = bounds.y_max - AREA_INSET;
  const lift = 0.3;
  const size = Math.min(theme.scene.areaLabel, (0.5 * (x1 - x0)) / (TEXT_WIDTH * id.length));
  const place = areaLabelPlace(id, size, { x_min: x0, x_max: x1, y_min: y0, y_max: y1 }, space, occupied);
  return (
    <group>
      <Line points={[at(x0, y0, lift), at(x1, y0, lift), at(x1, y1, lift), at(x0, y1, lift), at(x0, y0, lift)]}
            color={theme.color.lineFaint} lineWidth={theme.line.area} dashed dashSize={14} gapSize={10} />
      <FloorText text={id} x={place.x} y={place.y} size={size} colour={theme.color.labelFaint}
                 anchorX="center" anchorY="middle" />
    </group>
  );
}

const TEXT_WIDTH = 0.62;   // a mono character's width, as a share of the font size

function areaLabelPlace(id: string, size: number, inner: Bounds, space: Bounds, occupied: readonly FixedObject[]) {
  const w = TEXT_WIDTH * size * id.length;
  const h = size;
  const pad = 16;
  const cx = (inner.x_min + inner.x_max) / 2;
  const cy = (inner.y_min + inner.y_max) / 2;
  const left = inner.x_min + pad + w / 2;
  const right = inner.x_max - pad - w / 2;
  const low = inner.y_min + pad + h / 2;
  const high = inner.y_max - pad - h / 2;
  const sx = (space.x_min + space.x_max) / 2;
  const sy = (space.y_min + space.y_max) / 2;
  const candidates = [{ x: left, y: low }, { x: left, y: high }, { x: right, y: low }, { x: right, y: high }]
    .sort((a, b) => Math.hypot(b.x - sx, b.y - sy) - Math.hypot(a.x - sx, a.y - sy));
  const free = (c: { x: number; y: number }) => occupied.every((f) =>
    Math.abs(c.x - f.position.x) > (w + f.size.x) / 2 + pad || Math.abs(c.y - f.position.y) > (h + f.size.y) / 2 + pad);
  return candidates.find(free) ?? { x: cx, y: cy };
}

function Fixed({ f, appearance, bounds }: { f: FixedObject; appearance: Appearance; bounds: Bounds }) {
  const look = fixedLook(appearance, f.type);
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
