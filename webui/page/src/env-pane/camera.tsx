/**
 * The env-pane's camera: orthographic (parallel lines stay parallel, a thing keeps its size wherever it stands), in one
 * of two preset poses over the same scene, or moved freely by the screen-user (T-viz 1a (iii); TODO-195;
 * docs/handoffs/plan_T-viz_1a.md, section 4, "The free camera"). Tilted: from the south-east at the isometric elevation. From
 * above: straight down, north up. A preset frames the space's bounds and the tallest form.
 *
 * The free camera (drei's orbit controls): drag turns around the room, and up and down tilts it, from straight down to
 * 10° above the floor; right drag, or shift and drag, moves it; the wheel zooms, between the whole room and about one
 * object. Moving it leaves the preset (`onFree`); a preset puts the camera back in its pose. The camera is the
 * screen-user's own: it changes nothing in the sim-run and is written nowhere.
 */

import { OrbitControls } from "@react-three/drei";
import { useThree } from "@react-three/fiber";
import { type ComponentRef, useLayoutEffect, useRef } from "react";
import * as THREE from "three";

import type { Bounds } from "../gen/messages";

export type View = "tilted" | "top";

const ISOMETRIC = Math.atan(1 / Math.SQRT2);   // 35.26°, the isometric elevation
const DISTANCE = 20000;
const MARGIN = 0.06;                            // of the pane, on each side
const LOWEST = (10 * Math.PI) / 180;            // the free camera's lowest elevation above the floor
const ONE_OBJECT = 120;                         // the free camera's closest zoom shows about this much of the room
const WIDEST = 0.6;                             // and its widest this share of the preset's zoom

/** A preset's pose: the elevation above the floor and the azimuth, from the south (0) toward the east. */
function pose(view: View): { elevation: number; azimuth: number } {
  if (view === "top") return { elevation: Math.PI / 2 - 1e-4, azimuth: 0 };
  return { elevation: ISOMETRIC, azimuth: Math.PI / 4 };
}

export function FramingCamera({ view, free, onFree, bounds, height }: {
  view: View; free: boolean; onFree: () => void; bounds: Bounds; height: number;
}) {
  const camera = useThree((state) => state.camera) as THREE.OrthographicCamera;
  const size = useThree((state) => state.size);
  const controls = useRef<ComponentRef<typeof OrbitControls>>(null);
  const moving = useRef(false);

  useLayoutEffect(() => {
    const orbit = controls.current;
    if (free || orbit === null) return;
    const { elevation, azimuth } = pose(view);
    const direction = new THREE.Vector3(
      Math.sin(azimuth) * Math.cos(elevation), Math.sin(elevation), Math.cos(azimuth) * Math.cos(elevation));
    const target = new THREE.Vector3((bounds.x_min + bounds.x_max) / 2, 0, -(bounds.y_min + bounds.y_max) / 2);
    camera.up.set(0, 1, 0);
    camera.position.copy(target).addScaledVector(direction, DISTANCE);
    camera.lookAt(target);
    camera.near = 1;
    camera.far = DISTANCE * 2;
    camera.updateMatrixWorld();

    // The space's box in the camera's frame; the view is centred on it and fitted to the pane.
    const box = new THREE.Box3();
    for (const x of [bounds.x_min, bounds.x_max])
      for (const y of [bounds.y_min, bounds.y_max])
        for (const h of [0, height]) box.expandByPoint(new THREE.Vector3(x, h, -y).applyMatrix4(camera.matrixWorldInverse));
    const centre = box.getCenter(new THREE.Vector3());
    const shift = new THREE.Vector3()
      .addScaledVector(new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 0), centre.x)
      .addScaledVector(new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 1), centre.y);
    camera.position.add(shift);
    target.add(shift);

    const span = box.getSize(new THREE.Vector3());
    const zoom = Math.min(size.width / (span.x * (1 + 2 * MARGIN)), size.height / (span.y * (1 + 2 * MARGIN)));
    camera.zoom = zoom;
    camera.updateProjectionMatrix();
    orbit.target.copy(target);
    orbit.minZoom = zoom * WIDEST;
    orbit.maxZoom = zoom * Math.max(span.x, span.y) / ONE_OBJECT;
    orbit.update();
  }, [camera, size.width, size.height, view, free, bounds, height]);

  return (
    <OrbitControls ref={controls} makeDefault enableDamping={false} screenSpacePanning
                   minPolarAngle={0} maxPolarAngle={Math.PI / 2 - LOWEST}
                   onStart={() => { moving.current = true; }} onEnd={() => { moving.current = false; }}
                   onChange={() => { if (moving.current && !free) onFree(); }} />
  );
}
