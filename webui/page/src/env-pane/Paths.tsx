/**
 * The paths on the floor (T-viz 1d and 1e; Hadi, 7 October 2026, preferred; design_records.md, "T-viz, the web-ui",
 * 1d AND 1e, THE PATHS ON THE FLOOR). Colour says whose movement it is; form says what kind of knowledge it is:
 *   - the robot's own plan: a thin dashed line in the robot's colour;
 *   - the human's real path, which the robot does not know: a thin dashed line in the human's colour;
 *   - the robot's expectation of the human: a wide, light stripe in the human's colour, below the lines; filled for the
 *     plan of an admitted task, hatched for the fallback projection; a stand in it a disc at its place.
 * Only what lies ahead is drawn: a line starts at the agent and ends with a small mark at each walk's end. Flat on the
 * floor, under the objects and the agents (depth-tested, just above the floor's own marks). Each drawing is shown by its
 * switch in the env-pane's header.
 *
 * The stripe's pieces (a band per moving segment, its round ends, the discs of stands) overlap; each pixel of one
 * robot's stripe is tinted once, through the stencil, so the stripe is one even tint.
 */

import { Line } from "@react-three/drei";
import { useEffect, useMemo } from "react";
import * as THREE from "three";

import { theme } from "../theme";
import { pixelRatioUniform } from "./material";
import { type Ahead, type Expectation, linePoints, type PathsShown, stripeTriangles } from "./paths";
import type { Walk } from "../gen/messages";
import { at } from "./solids";

// Heights above the floor, in the layout's unit: over the floor's dots and shadows (0.2), under the agents' rings (0.4)
// and the floor's text (0.5).
const STRIPE_LIFT = 0.25;
const LINE_LIFT = 0.32;
const MARK_LIFT = 0.34;

export function Paths({ ahead, shown, stripeWidth }: { ahead: Ahead; shown: PathsShown; stripeWidth: number }) {
  return (
    <group>
      {shown.expectation && ahead.robots.map((r, i) => r.expectation && (
        <Stripe key={r.robot} expectation={r.expectation} width={stripeWidth} stencil={i + 1} />
      ))}
      {shown.plan && ahead.robots.map((r) => (
        <WalkLine key={r.robot} walks={r.walks} colour={theme.color.robot} />
      ))}
      {shown.path && ahead.humans.map((h) => (
        <WalkLine key={h.human} walks={h.walks} colour={theme.color.human} />
      ))}
    </group>
  );
}

/** A dashed line through the walks ahead, from the agent, with a small mark at each walk's end. */
function WalkLine({ walks, colour }: { walks: readonly Walk[]; colour: string }) {
  const points = useMemo(() => linePoints(walks).map(([x, y]) => at(x, y, LINE_LIFT)), [walks]);
  if (points.length < 2) return null;
  return (
    <group>
      <Line points={points} color={colour} lineWidth={theme.line.path} dashed dashSize={theme.scene.pathDash}
            gapSize={theme.scene.pathGap} />
      {walks.map((w, i) => <Mark key={i} x={w.end.x} y={w.end.y} colour={colour} />)}
    </group>
  );
}

const RIM = new THREE.CircleGeometry(theme.scene.pathMark + theme.scene.pathMarkRim, 24).rotateX(-Math.PI / 2);
const DOT = new THREE.CircleGeometry(theme.scene.pathMark, 24).rotateX(-Math.PI / 2);
const flat = new Map<string, THREE.MeshBasicMaterial>();
function flatMaterial(colour: string): THREE.MeshBasicMaterial {
  if (!flat.has(colour)) flat.set(colour, new THREE.MeshBasicMaterial({ color: colour }));
  return flat.get(colour)!;
}

/** A walk's end: a dot of the agent's colour in a white rim, flat on the floor. */
function Mark({ x, y, colour }: { x: number; y: number; colour: string }) {
  return (
    <group>
      <mesh geometry={RIM} material={flatMaterial(theme.color.surface)} position={at(x, y, MARK_LIFT)} />
      <mesh geometry={DOT} material={flatMaterial(colour)} position={at(x, y, MARK_LIFT + 0.01)} />
    </group>
  );
}

const stripeVertex = /* glsl */ `
  void main() {
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
`;

const stripeFragment = /* glsl */ `
  uniform vec3 uColour;
  uniform float uFill;
  uniform float uHatch;
  uniform float uSpacing;
  uniform float uWidth;
  uniform float uPixelRatio;
  void main() {
    float a = uFill;
    if (uHatch > 0.0) {
      float period = uSpacing * uPixelRatio;
      float u = (gl_FragCoord.x + gl_FragCoord.y) * 0.70710678;
      float d = abs(mod(u, period) - 0.5 * period);
      float halfWidth = 0.5 * uWidth * uPixelRatio;
      a = max(a, uHatch * (1.0 - smoothstep(halfWidth - 0.5, halfWidth + 0.5, d)));
    }
    gl_FragColor = vec4(uColour, a);
    #include <colorspace_fragment>
  }
`;

const stripes = new Map<string, THREE.ShaderMaterial>();

/** The stripe's material: filled (admitted) or hatched (fallback); `stencil` one robot's mark in the stencil buffer. */
function stripeMaterial(kind: Expectation["kind"], stencil: number): THREE.ShaderMaterial {
  const key = `${kind} ${stencil}`;
  const found = stripes.get(key);
  if (found) return found;
  const hatched = kind === "fallback";
  const material = new THREE.ShaderMaterial({
    vertexShader: stripeVertex,
    fragmentShader: stripeFragment,
    uniforms: {
      uColour: { value: new THREE.Color(theme.color.human) },
      uFill: { value: hatched ? theme.opacity.expectationHatchFill : theme.opacity.expectationFill },
      uHatch: { value: hatched ? theme.opacity.expectationHatch : 0 },
      uSpacing: { value: theme.scene.expectationHatchSpacing },
      uWidth: { value: theme.scene.expectationHatchWidth },
      uPixelRatio: pixelRatioUniform,
    },
    transparent: true,
    depthWrite: false,
    side: THREE.DoubleSide,
    // each pixel once: drawn where this robot's stripe has not been drawn yet, which it then marks
    stencilWrite: true,
    stencilRef: stencil,
    stencilFunc: THREE.NotEqualStencilFunc,
    stencilZPass: THREE.ReplaceStencilOp,
  });
  stripes.set(key, material);
  return material;
}

function Stripe({ expectation, width, stencil }: { expectation: Expectation; width: number; stencil: number }) {
  const geometry = useMemo(() => {
    const flatXY = stripeTriangles(expectation.parts, width, theme.scene.expectationStand * width);
    const xyz = new Float32Array((flatXY.length / 2) * 3);
    for (let i = 0, j = 0; i < flatXY.length; i += 2, j += 3) {
      xyz[j] = flatXY[i];
      xyz[j + 1] = STRIPE_LIFT;
      xyz[j + 2] = -flatXY[i + 1];
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute("position", new THREE.BufferAttribute(xyz, 3));
    return g;
  }, [expectation, width]);
  useEffect(() => () => geometry.dispose(), [geometry]);
  return <mesh geometry={geometry} material={stripeMaterial(expectation.kind, stencil)} renderOrder={1} />;
}
