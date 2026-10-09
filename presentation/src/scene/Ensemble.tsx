/**
 * The last slide's four figures standing together (Hadi, tpres-v5): the kitting worker, the kitting robot, the lift
 * truck and the dock worker, drawn by the env-pane's own figures (FigureForm) in their domains' appearances (the recorded
 * views of kitting and dock_loading, data/), on no floor.
 *
 * Facing the viewers: the deck's own camera, not the env-pane's (whose two presets, tilted and top, frame the floor's
 * axis-aligned box and would leave the four small): orthographic, from the south at a low elevation, fitted to the
 * figures. The four stand on a line along the layout's x, which the screen shows from left to right. The person and the
 * cube-head robot are round, with no front; the lift truck has one, and it faces the camera. Nothing in webui/
 * changes.
 */

import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { useEffect, useLayoutEffect, useRef } from "react";
import * as THREE from "three";

import { FigureForm, ringRadius } from "../../../webui/page/src/env-pane/figures";
import { setPixelRatio } from "../../../webui/page/src/env-pane/material";
import { at, paints } from "../../../webui/page/src/env-pane/solids";
import type { Appearance } from "../../../webui/page/src/gen/messages";
import dock from "../../data/dock_loading_env_layout_03.json";
import kitting from "../../data/kitting_env_layout_01.json";
import { useSlideCurrent, useSlideNear } from "../slides/kit";

const KITTING = (kitting as unknown as { appearance: Appearance }).appearance;
const DOCK = (dock as unknown as { appearance: Appearance }).appearance;

/** Toward the camera (the south), in the layout's frame; the camera's elevation above the floor. */
const TOWARD_VIEWER = { x: 0, y: -1 };
const ELEVATION = (16 * Math.PI) / 180;
const MARGIN = 0.04;   // of the canvas, on each side

/** The four, left to right, with the gap (cm, along the line) before each. */
const LINE: { look: Appearance; who: "robot" | "human"; gap: number }[] = [
  { look: KITTING, who: "human", gap: 0 },
  { look: KITTING, who: "robot", gap: 120 },
  { look: DOCK, who: "robot", gap: 190 },
  { look: DOCK, who: "human", gap: 190 },
];

const PLACED = (() => {
  let s = 0;
  const along = LINE.map((f) => (s += f.gap));
  const mid = (along[0] + along[along.length - 1]) / 2;
  return LINE.map((f, i) => ({ ...f, x: along[i] - mid, y: 0 }));
})();

export function Ensemble() {
  const near = useSlideNear();
  const current = useSlideCurrent();
  return (
    <div className="ensemble">
      {near && (
        <Canvas orthographic flat dpr={[1, 2]} gl={{ antialias: true }} frameloop={current ? "always" : "never"}>
          <PixelRatio />
          <FitCamera />
          <Turning current={current} />
        </Canvas>
      )}
    </div>
  );
}

/** One turn in this many seconds, all four alike (Hadi, tpres-v7). */
const TURN_S = 9;

/** The four, each turning slowly around its own vertical axis on its spot, from facing the viewers; the turn starts
 * again from there each time the slide opens, and runs only while it is shown (the canvas renders only then). */
function Turning({ current }: { current: boolean }) {
  const groups = useRef<(THREE.Group | null)[]>([]);
  const start = useRef<number | null>(null);
  useEffect(() => { if (current) start.current = null; }, [current]);
  useFrame((state) => {
    if (start.current === null) start.current = state.clock.elapsedTime;
    const angle = ((state.clock.elapsedTime - start.current) / TURN_S) * 2 * Math.PI;
    for (const g of groups.current) if (g !== null) g.rotation.y = angle;
  });
  return (
    <>
      {PLACED.map((f, i) => {
        const [px, py, pz] = at(f.x, f.y);
        return (
          <group key={i} position={[px, py, pz]} ref={(g) => { groups.current[i] = g; }}>
            <FigureForm figure={f.look[f.who].figure} h={f.look[f.who].height} paint={paints[f.who]}
                        stance={{ x: 0, y: 0, facing: TOWARD_VIEWER }} />
          </group>
        );
      })}
    </>
  );
}

/** The camera from the south at ELEVATION, centred on the four and zoomed to fit them: each figure's ring on the floor
 * and its height, seen in the camera's frame. */
function FitCamera() {
  const camera = useThree((state) => state.camera) as THREE.OrthographicCamera;
  const size = useThree((state) => state.size);
  useLayoutEffect(() => {
    const direction = new THREE.Vector3(0, Math.sin(ELEVATION), Math.cos(ELEVATION));   // the layout's -y is three's +z
    camera.up.set(0, 1, 0);
    camera.position.copy(direction).multiplyScalar(20000);
    camera.lookAt(0, 0, 0);
    camera.near = 1;
    camera.far = 40000;
    camera.updateMatrixWorld();
    const box = new THREE.Box3();
    for (const f of PLACED) {
      const r = ringRadius(f.look[f.who].figure, f.look[f.who].height);
      for (const [dx, dy] of [[-r, 0], [r, 0], [0, -r], [0, r]])
        for (const h of [0, f.look[f.who].height]) {
          const [x, y, z] = at(f.x + dx, f.y + dy, h);
          box.expandByPoint(new THREE.Vector3(x, y, z).applyMatrix4(camera.matrixWorldInverse));
        }
    }
    const centre = box.getCenter(new THREE.Vector3());
    const shift = new THREE.Vector3()
      .addScaledVector(new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 0), centre.x)
      .addScaledVector(new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 1), centre.y);
    camera.position.add(shift);
    const span = box.getSize(new THREE.Vector3());
    camera.zoom = Math.min(size.width / (span.x * (1 + 2 * MARGIN)), size.height / (span.y * (1 + 2 * MARGIN)));
    camera.updateProjectionMatrix();
  }, [camera, size.width, size.height]);
  return null;
}

/** The hatching's spacing in device pixels, as the env-pane sets it. */
function PixelRatio() {
  const dpr = useThree((state) => state.viewport.dpr);
  useLayoutEffect(() => setPixelRatio(dpr), [dpr]);
  return null;
}
