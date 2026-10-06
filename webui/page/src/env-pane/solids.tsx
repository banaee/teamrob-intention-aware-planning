/**
 * The scene's building blocks: a box or a cylinder with the illustration material and its outline. Every form of the
 * shape vocabulary is put together from them.
 *
 * Coordinates: a block is placed by its centre on the floor, in the layout's x and y, and its base height; the scene's
 * axes are x, up, and minus the layout's y (north is -z).
 */

import { Edges } from "@react-three/drei";
import { useMemo } from "react";
import * as THREE from "three";

import { theme } from "../theme";
import { illustration, type Tone } from "./material";

export interface Paint {
  tone: Tone;
  line: string;
  lineWidth: number;
  opacity?: number;
}

export const paints = {
  background: {
    tone: { top: theme.color.faceTop, light: theme.color.faceLight, shade: theme.color.faceShade,
            hatch: theme.color.hatch },
    line: theme.color.line,
    lineWidth: theme.line.object,
  },
  active: {
    tone: { top: theme.color.activeTop, light: theme.color.activeLight, shade: theme.color.activeShade,
            hatch: theme.color.activeLine },
    line: theme.color.activeLine,
    lineWidth: theme.line.object,
  },
  movable: {
    tone: { top: theme.color.movableTop, light: theme.color.movableLight, shade: theme.color.movableShade,
            hatch: null },
    line: theme.color.movableLine,
    lineWidth: theme.line.movable,
  },
  robot: {
    tone: { top: theme.color.robotLight, light: theme.color.robot, shade: theme.color.robotDark, hatch: null },
    line: theme.color.robotDark,
    lineWidth: theme.line.agent,
  },
  human: {
    tone: { top: theme.color.humanLight, light: theme.color.human, shade: theme.color.humanDark, hatch: null },
    line: theme.color.humanDark,
    lineWidth: theme.line.agent,
  },
} satisfies Record<string, Paint>;

/** A thin member (a post, a leg, a stem) drawn as one stroke: its faces in its outline's colour, no outline. */
export function stroke(paint: Paint): Paint {
  const c = paint.line;
  return { tone: { top: c, light: c, shade: c, hatch: null }, line: c, lineWidth: 0 };
}

/** The scene position of a point of the layout at a height. */
export function at(x: number, y: number, height = 0): [number, number, number] {
  return [x, height, -y];
}

function Solid({ geometry, position, paint }: {
  geometry: THREE.BufferGeometry;
  position: [number, number, number];
  paint: Paint;
}) {
  const material = useMemo(() => illustration(paint.tone, theme.hatch, paint.opacity ?? 1),
    [paint.tone, paint.opacity]);
  return (
    <mesh geometry={geometry} material={material} position={position}>
      {paint.lineWidth > 0 && <Edges threshold={20} color={paint.line} lineWidth={paint.lineWidth} />}
    </mesh>
  );
}

/** A box of extent sx (along x), sy (along the layout's y) and h, centred at (x, y), its base at `base`. */
export function Block({ x, y, sx, sy, h, base = 0, paint }: {
  x: number; y: number; sx: number; sy: number; h: number; base?: number; paint: Paint;
}) {
  const geometry = useMemo(() => new THREE.BoxGeometry(sx, h, sy), [sx, h, sy]);
  return <Solid geometry={geometry} position={at(x, y, base + h / 2)} paint={paint} />;
}

/** An upright cylinder of radius r (rTop at its top, if given) and height h, its base at `base`. */
export function Cylinder({ x, y, r, rTop, h, base = 0, paint, segments = 28 }: {
  x: number; y: number; r: number; rTop?: number; h: number; base?: number; paint: Paint; segments?: number;
}) {
  const geometry = useMemo(() => new THREE.CylinderGeometry(rTop ?? r, r, h, segments), [r, rTop, h, segments]);
  return <Solid geometry={geometry} position={at(x, y, base + h / 2)} paint={paint} />;
}

/** A sphere of radius r, centred at height `centre`. */
export function Ball({ x, y, r, centre, paint }: { x: number; y: number; r: number; centre: number; paint: Paint }) {
  const geometry = useMemo(() => new THREE.SphereGeometry(r, 28, 18), [r]);
  const material = useMemo(() => illustration(paint.tone, theme.hatch), [paint.tone]);
  // A sphere has no crease to outline; its silhouette is the ring the tones draw.
  return <mesh geometry={geometry} material={material} position={at(x, y, centre)} />;
}

/** A flat shape on the floor, just above it: a footprint's shadow, an agent's ring. */
export function FloorPatch({ x, y, shape, colour, opacity, lift = 0.4 }: {
  x: number; y: number; shape: THREE.Shape; colour: string; opacity: number; lift?: number;
}) {
  const geometry = useMemo(() => new THREE.ShapeGeometry(shape, 32), [shape]);
  return (
    <mesh geometry={geometry} position={at(x, y, lift)} rotation={[-Math.PI / 2, 0, 0]} renderOrder={1}>
      <meshBasicMaterial color={colour} transparent opacity={opacity} depthWrite={false} />
    </mesh>
  );
}

/** A soft shadow under a footprint: a blurred rectangle, its core the footprint. */
export function SoftShadow({ x, y, sx, sy, colour, opacity }: {
  x: number; y: number; sx: number; sy: number; colour: string; opacity: number;
}) {
  const scale = SHADOW_TEXTURE / SHADOW_CORE;
  return (
    <mesh position={at(x, y, 0.2)} rotation={[-Math.PI / 2, 0, 0]} renderOrder={1}>
      <planeGeometry args={[sx * scale, sy * scale]} />
      <meshBasicMaterial map={shadowTexture()} color={colour} transparent opacity={opacity} depthWrite={false} />
    </mesh>
  );
}

const SHADOW_TEXTURE = 128;   // px
const SHADOW_CORE = 72;       // px: the footprint's part of the texture
let shadowMap: THREE.CanvasTexture | null = null;

function shadowTexture(): THREE.CanvasTexture {
  if (shadowMap) return shadowMap;
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = SHADOW_TEXTURE;
  const g = canvas.getContext("2d")!;
  const edge = (SHADOW_TEXTURE - SHADOW_CORE) / 2;
  g.filter = "blur(9px)";
  g.fillStyle = "#ffffff";
  g.fillRect(edge, edge, SHADOW_CORE, SHADOW_CORE);
  shadowMap = new THREE.CanvasTexture(canvas);
  return shadowMap;
}

export function rectangle(sx: number, sy: number): THREE.Shape {
  const s = new THREE.Shape();
  s.moveTo(-sx / 2, -sy / 2);
  s.lineTo(sx / 2, -sy / 2);
  s.lineTo(sx / 2, sy / 2);
  s.lineTo(-sx / 2, sy / 2);
  s.closePath();
  return s;
}

export function disc(r: number): THREE.Shape {
  const s = new THREE.Shape();
  s.absarc(0, 0, r, 0, Math.PI * 2, false);
  return s;
}
