/**
 * One agent's figure alone, as the env-pane draws it (webui/page/src/env-pane): the same figure, paint and material,
 * the env-pane's own camera at its tilted preset, framed on the figure's ring and height instead of a room. Nothing
 * else of the scene: no floor, no objects, no labels. The canvas takes no pointer, so the camera's orbit controls
 * never move it.
 */

import { Canvas, useThree } from "@react-three/fiber";
import { useLayoutEffect } from "react";

import { FramingCamera } from "../../../webui/page/src/env-pane/camera";
import { FigureForm, ringRadius } from "../../../webui/page/src/env-pane/figures";
import { setPixelRatio } from "../../../webui/page/src/env-pane/material";
import type { Paint } from "../../../webui/page/src/env-pane/solids";
import type { FigureLook } from "../../../webui/page/src/gen/messages";

export function FigureAlone({ look, paint }: { look: FigureLook; paint: Paint }) {
  const r = ringRadius(look.figure, look.height);
  const bounds = { x_min: -r, x_max: r, y_min: -r, y_max: r };
  return (
    <div className="figure-alone">
      <Canvas orthographic flat dpr={[1, 2]} gl={{ antialias: true, stencil: true }}>
        <PixelRatio />
        <FramingCamera view="tilted" free={false} onFree={() => {}} bounds={bounds} height={look.height} />
        <FigureForm figure={look.figure} h={look.height} stance={{ x: 0, y: 0, facing: null }} paint={paint} />
      </Canvas>
    </div>
  );
}

/** The hatching's spacing in device pixels, as the env-pane sets it. */
function PixelRatio() {
  const dpr = useThree((state) => state.viewport.dpr);
  useLayoutEffect(() => setPixelRatio(dpr), [dpr]);
  return null;
}
