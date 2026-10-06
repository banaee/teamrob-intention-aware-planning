/**
 * The env-pane's camera: orthographic (parallel lines stay parallel, a thing keeps its size wherever it stands), in one
 * of two poses over the same scene. Tilted: from the south-east at the isometric elevation. From above: straight down,
 * north up. Switching moves the camera only. The camera frames the space's bounds and the tallest form.
 */

import { useThree } from "@react-three/fiber";
import { useLayoutEffect } from "react";
import * as THREE from "three";

import type { Bounds } from "../gen/messages";

export type View = "tilted" | "top";

const ELEVATION = Math.atan(1 / Math.SQRT2);   // 35.26°, the isometric elevation
const AZIMUTH = Math.PI / 4;                    // from the south-east
const DISTANCE = 20000;
const MARGIN = 0.06;                            // of the pane, on each side

function pose(view: View): { direction: THREE.Vector3; up: THREE.Vector3 } {
  if (view === "top") return { direction: new THREE.Vector3(0, 1, 0), up: new THREE.Vector3(0, 0, -1) };
  return {
    direction: new THREE.Vector3(
      Math.sin(AZIMUTH) * Math.cos(ELEVATION), Math.sin(ELEVATION), Math.cos(AZIMUTH) * Math.cos(ELEVATION)),
    up: new THREE.Vector3(0, 1, 0),
  };
}

export function FramingCamera({ view, bounds, height }: { view: View; bounds: Bounds; height: number }) {
  const camera = useThree((state) => state.camera) as THREE.OrthographicCamera;
  const size = useThree((state) => state.size);

  useLayoutEffect(() => {
    const { direction, up } = pose(view);
    const target = new THREE.Vector3((bounds.x_min + bounds.x_max) / 2, 0, -(bounds.y_min + bounds.y_max) / 2);
    camera.up.copy(up);
    camera.position.copy(target).addScaledVector(direction, DISTANCE);
    camera.lookAt(target);
    camera.near = 1;
    camera.far = DISTANCE * 2;
    camera.updateMatrixWorld();

    // The space's box in the camera's frame; the view is centred on it and fitted to the pane.
    const view_ = camera.matrixWorldInverse;
    const box = new THREE.Box3();
    for (const x of [bounds.x_min, bounds.x_max])
      for (const y of [bounds.y_min, bounds.y_max])
        for (const h of [0, height]) box.expandByPoint(new THREE.Vector3(x, h, -y).applyMatrix4(view_));
    const centre = box.getCenter(new THREE.Vector3());
    const right = new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 0);
    const upward = new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 1);
    camera.position.addScaledVector(right, centre.x).addScaledVector(upward, centre.y);

    camera.left = -size.width / 2;
    camera.right = size.width / 2;
    camera.top = size.height / 2;
    camera.bottom = -size.height / 2;
    const span = box.getSize(new THREE.Vector3());
    camera.zoom = Math.min(size.width / (span.x * (1 + 2 * MARGIN)), size.height / (span.y * (1 + 2 * MARGIN)));
    camera.updateProjectionMatrix();
    camera.updateMatrixWorld();
  }, [camera, size.width, size.height, view, bounds, height]);

  return null;
}
