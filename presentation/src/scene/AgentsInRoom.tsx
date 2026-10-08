/**
 * The robot alone, then the robot in a room: one canvas, one figure that is never replaced. The room is the env-pane's
 * own Scene, given a recorded view of a layout (data/, scripts/record_view.py) and a moment without agents, as the
 * web-ui draws a layout's view; the robot is the env-pane's figure, drawn beside the Scene at a free place on the floor.
 *
 * The view: the env-pane's own camera (FramingCamera) at its tilted preset, framing a box that moves over about one
 * second from the robot's ring to the room, as the env-pane frames it. The box's centre moves linearly, its extents
 * geometrically, so the zoom changes at an even pace. The room appears during the movement: a veil in the slide's
 * ground lies over the room and under the robot, and fades out.
 */

import { Canvas, createPortal, useFrame, useThree } from "@react-three/fiber";
import { useLayoutEffect, useMemo, useRef, useState } from "react";
import * as THREE from "three";

import { FramingCamera } from "../../../webui/page/src/env-pane/camera";
import { FigureForm, ringRadius } from "../../../webui/page/src/env-pane/figures";
import { NO_AHEAD, ALL_SHOWN } from "../../../webui/page/src/env-pane/paths";
import { EMPTY_BOOK } from "../../../webui/page/src/env-pane/places";
import { type Moment, type Room, Scene } from "../../../webui/page/src/env-pane/Scene";
import { setPixelRatio } from "../../../webui/page/src/env-pane/material";
import { paints } from "../../../webui/page/src/env-pane/solids";
import type { Appearance, Bounds, LayoutView } from "../../../webui/page/src/gen/messages";
import { theme } from "../../../webui/page/src/theme";

export interface Recorded {
  appearance: Appearance;
  view: LayoutView;
}

const MOVE_MS = 1000;
const NO_AGENTS: Moment = { humans: [], robots: [], fixed_object_contents: [], carried: [], object_states: [] };

/** `inRoom`: false the robot alone, true the robot in the room; a change moves the view. The canvas takes no
 * pointer, so the camera's orbit controls never move it. */
export function RobotInRoom(props: { recorded: Recorded; place: { x: number; y: number }; inRoom: boolean }) {
  return (
    <div className="scene-canvas">
      <Canvas orthographic flat dpr={[1, 2]} gl={{ antialias: true, stencil: true }}>
        <PixelRatio />
        <RobotInRoomScene {...props} />
      </Canvas>
    </div>
  );
}

function RobotInRoomScene({ recorded, place, inRoom }: {
  recorded: Recorded; place: { x: number; y: number }; inRoom: boolean;
}) {
  const { appearance, view } = recorded;
  const robot = appearance.robot;
  const room = useMemo<Room>(() => ({
    key: `view ${view.domain} ${view.layout}`, space: view.space, areas: view.areas, fixed_objects: view.fixed_objects,
    movable_objects: [],
  }), [view]);
  // The room's framing, as the env-pane's: the space's bounds and the tallest form of the domain's appearance.
  const tallest = Math.max(appearance.human.height, robot.height, appearance.default_fixed.height,
    ...Object.values(appearance.fixed).map((l) => l.height));
  const r = ringRadius(robot.figure, robot.height);
  const alone = { centre: place, half: { x: r, y: r }, height: robot.height };
  const b = view.space.bounds;
  const whole = {
    centre: { x: (b.x_min + b.x_max) / 2, y: (b.y_min + b.y_max) / 2 },
    half: { x: (b.x_max - b.x_min) / 2, y: (b.y_max - b.y_min) / 2 },
    height: tallest,
  };

  const [k, setK] = useState(inRoom ? 1 : 0);
  const moving = useRef({ from: k, start: performance.now(), to: inRoom ? 1 : 0 });
  const target = inRoom ? 1 : 0;
  if (moving.current.to !== target) moving.current = { from: k, start: performance.now(), to: target };
  useFrame(() => {
    const { from, start, to } = moving.current;
    const s = Math.min(1, (performance.now() - start) / MOVE_MS);
    const next = from + (to - from) * s;
    if (next !== k) setK(next);
  });
  const e = k * k * (3 - 2 * k);      // eased

  const geo = (a: number, c: number) => a * Math.pow(c / a, e);
  const cx = alone.centre.x + e * (whole.centre.x - alone.centre.x);
  const cy = alone.centre.y + e * (whole.centre.y - alone.centre.y);
  const hx = geo(alone.half.x, whole.half.x);
  const hy = geo(alone.half.y, whole.half.y);
  const bounds: Bounds = { x_min: cx - hx, x_max: cx + hx, y_min: cy - hy, y_max: cy + hy };

  const robotScene = useMemo(() => new THREE.Scene(), []);
  return (
    <>
      <FramingCamera view="tilted" free={false} onFree={() => {}} bounds={bounds} height={geo(alone.height, whole.height)} />
      <Scene room={room} moment={NO_AGENTS} book={EMPTY_BOOK} appearance={appearance} glideMs={0} ahead={NO_AHEAD}
             shown={ALL_SHOWN} />
      {createPortal(
        <FigureForm figure={robot.figure} h={robot.height} stance={{ x: place.x, y: place.y, facing: null }}
                    paint={paints.robot} />,
        robotScene)}
      <Passes robotScene={robotScene} veil={1 - e} />
    </>
  );
}

/** Takes over the canvas's rendering: the room, the veil over it, then the robot (against the room's depth). */
function Passes({ robotScene, veil }: { robotScene: THREE.Scene; veil: number }) {
  const { gl, scene, camera } = useThree();
  const quad = useMemo(() => {
    const s = new THREE.Scene();
    const material = new THREE.MeshBasicMaterial({ color: theme.color.floor, transparent: true, depthTest: false,
                                                   depthWrite: false });
    s.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), material));
    return { scene: s, material, camera: new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1) };
  }, []);
  useFrame(() => {
    gl.autoClear = false;
    gl.clear();
    gl.render(scene, camera);
    quad.material.opacity = veil;
    if (veil > 0) gl.render(quad.scene, quad.camera);
    gl.render(robotScene, camera);
  }, 1);
  return null;
}

/** The hatching's spacing in device pixels, as the env-pane sets it. */
function PixelRatio() {
  const dpr = useThree((state) => state.viewport.dpr);
  useLayoutEffect(() => setPixelRatio(dpr), [dpr]);
  return null;
}
