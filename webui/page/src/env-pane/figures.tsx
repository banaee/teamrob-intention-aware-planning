/**
 * The agents' figures (webui/appearance.py, Figure): a bit illustrative, neither realistic nor a plain shape, each in
 * its agent's semantic colour, standing on a faint ring of that colour so that it is found at once from above. The
 * figure's height is the appearance's; its proportions are the figure's.
 *
 * Facing: a figure with a front (the lift vehicle) faces the agent's `last_motion`; before the agent has moved, north.
 * A display convention: the model holds no heading (handoff, correction note on 8.4).
 */

import { useMemo } from "react";

import type { Direction, Figure } from "../gen/messages";
import { theme } from "../theme";
import { at, Ball, Block, Cylinder, disc, FloorPatch, type Paint, paints } from "./solids";

export interface Stance {
  x: number;
  y: number;
  facing: Direction | null;
}

/** The height at which a figure holds what it carries, as a share of its height. */
export function carryHeight(figure: Figure, h: number): number {
  switch (figure) {
    case "person": return 0.5 * h;
    case "cube_head_robot": return 0.5 * h;
    case "lift_vehicle": return 0.08 * h;
  }
}

/** Where a figure holds what it carries, relative to its standing point (the lift vehicle: on its forks). */
export function carryOffset(figure: Figure, h: number, facing: Direction | null): { x: number; y: number } {
  const f = facing ?? { x: 0, y: 1 };
  const reach = figure === "lift_vehicle" ? 0.62 * h : 0.22 * h;
  return { x: f.x * reach, y: f.y * reach };
}

export function FigureForm({ figure, h, stance, paint }: { figure: Figure; h: number; stance: Stance; paint: Paint }) {
  const ringR = figure === "lift_vehicle" ? 0.62 * h : 0.32 * h;
  const ring = useMemo(() => disc(ringR), [ringR]);
  return (
    <group>
      <FloorPatch x={stance.x} y={stance.y} shape={ring} colour={paint.tone.light} opacity={theme.opacity.agentRing} />
      {figure === "person" && <Person h={h} s={stance} paint={paint} />}
      {figure === "cube_head_robot" && <CubeHeadRobot h={h} s={stance} paint={paint} />}
      {figure === "lift_vehicle" && <LiftVehicle h={h} s={stance} paint={paint} />}
    </group>
  );
}

/** Two legs, a tapered body in a work safety vest, two arms and a round head. */
function Person({ h, s, paint }: { h: number; s: Stance; paint: Paint }) {
  const leg = 0.045 * h;
  return (
    <group>
      {[-1, 1].map((side) => (
        <Cylinder key={`leg${side}`} x={s.x + side * 0.055 * h} y={s.y} r={leg} rTop={leg * 1.25} h={0.42 * h}
                  paint={paint} segments={16} />
      ))}
      <Cylinder x={s.x} y={s.y} r={0.11 * h} rTop={0.14 * h} h={0.3 * h} base={0.4 * h} paint={paint} />
      <Cylinder x={s.x} y={s.y} r={0.122 * h} rTop={0.146 * h} h={0.22 * h} base={0.47 * h} paint={paints.vest} />
      {[-1, 1].map((side) => (
        <Cylinder key={`arm${side}`} x={s.x + side * 0.175 * h} y={s.y} r={0.032 * h} rTop={0.038 * h} h={0.27 * h}
                  base={0.42 * h} paint={paint} segments={14} />
      ))}
      <Ball x={s.x} y={s.y} r={0.12 * h} centre={0.85 * h} paint={paint} />
    </group>
  );
}

/** A round base on wheels, a box torso, a neck and a cube head with a small lamp. */
function CubeHeadRobot({ h, s, paint }: { h: number; s: Stance; paint: Paint }) {
  const head = 0.28 * h;
  const torso = 0.3 * h;
  return (
    <group>
      <Cylinder x={s.x} y={s.y} r={0.24 * h} rTop={0.22 * h} h={0.12 * h} paint={paint} />
      <Block x={s.x} y={s.y} sx={torso} sy={torso} h={0.34 * h} base={0.14 * h} paint={paint} />
      <Cylinder x={s.x} y={s.y} r={0.045 * h} h={0.1 * h} base={0.48 * h} paint={paint} segments={14} />
      <Block x={s.x} y={s.y} sx={head} sy={head} h={head} base={0.58 * h} paint={paint} />
      <Cylinder x={s.x} y={s.y} r={0.006 * h + 1} h={0.08 * h} base={0.86 * h} paint={paint} segments={8} />
      <Ball x={s.x} y={s.y} r={0.03 * h} centre={0.96 * h} paint={paint} />
    </group>
  );
}

/** A low body with a cab, a mast and two forks, facing its direction of motion. */
function LiftVehicle({ h, s, paint }: { h: number; s: Stance; paint: Paint }) {
  const f = s.facing ?? { x: 0, y: 1 };
  const angle = Math.atan2(-f.x, f.y);    // turns the forms below, which face the layout's +y, toward f
  const [px, py, pz] = at(s.x, s.y);
  return (
    <group position={[px, py, pz]} rotation={[0, angle, 0]}>
      <Block x={0} y={-0.12 * h} sx={0.5 * h} sy={0.62 * h} h={0.28 * h} base={0.06 * h} paint={paint} />
      <Block x={0} y={-0.24 * h} sx={0.42 * h} sy={0.3 * h} h={0.26 * h} base={0.34 * h} paint={paint} />
      {[-1, 1].map((side) => (
        <Block key={side} x={side * 0.17 * h} y={0.22 * h} sx={0.05 * h} sy={0.05 * h} h={h} paint={paint} />
      ))}
      <Block x={0} y={0.22 * h} sx={0.4 * h} sy={0.04 * h} h={0.05 * h} base={0.9 * h} paint={paint} />
      {[-1, 1].map((side) => (
        <Block key={side} x={side * 0.12 * h} y={0.52 * h} sx={0.06 * h} sy={0.56 * h} h={0.03 * h} base={0.04 * h}
               paint={paint} />
      ))}
      {[-1, 1].flatMap((side) => [-1, 1].map((end) => (
        <Cylinder key={`${side}${end}`} x={side * 0.26 * h} y={-0.12 * h + end * 0.2 * h} r={0.07 * h} h={0.06 * h}
                  paint={paint} segments={16} />
      )))}
    </group>
  );
}
