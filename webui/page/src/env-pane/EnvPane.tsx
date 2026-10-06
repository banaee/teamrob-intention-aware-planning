/**
 * The env-pane (glossary §11): the region of the page that shows the simulated environment. A header with the layout's
 * id (not its title, which is stale in older layouts: Hadi, 6 October 2026, P20) and the two views (tilted, from above:
 * the same scene, the camera moved); the scene of the current sim-run at its latest tick, or of a view of a layout and
 * a setup; and, at its foot, the control bar the page passes in (it acts on what the env-pane shows).
 */

import { Canvas, useThree } from "@react-three/fiber";
import { type ReactNode, useLayoutEffect, useMemo } from "react";

import type { Appearance } from "../gen/messages";
import { FramingCamera, type View } from "./camera";
import { setPixelRatio } from "./material";
import { type Moment, type Room, Scene } from "./Scene";

export function EnvPane({ layout, room, moment, appearance, view, onView, glideMs, controls }: {
  layout: string;
  room: Room;
  moment: Moment;
  appearance: Appearance;
  view: View;
  onView: (view: View) => void;
  glideMs: number;
  controls: ReactNode;
}) {
  const tallest = useMemo(() => Math.max(
    appearance.human.height, appearance.robot.height, appearance.default_fixed.height,
    ...Object.values(appearance.fixed).map((l) => l.height)), [appearance]);
  return (
    <section className="env-pane">
      <header className="env-pane-header">
        <div className="env-pane-title">
          <span className="env-pane-name">{layout}</span>
        </div>
        <div className="segmented" role="group" aria-label="View">
          {(["tilted", "top"] as const).map((v) => (
            <button key={v} type="button" aria-pressed={view === v} onClick={() => onView(v)}>
              {v === "tilted" ? "Tilted" : "From above"}
            </button>
          ))}
        </div>
      </header>
      <div className="env-pane-scene">
        <Canvas orthographic flat dpr={[1, 2]} gl={{ antialias: true, preserveDrawingBuffer: true }}>
          <PixelRatio />
          <FramingCamera view={view} bounds={room.space.bounds} height={tallest} />
          <Scene room={room} moment={moment} appearance={appearance} glideMs={glideMs} />
        </Canvas>
      </div>
      {controls}
    </section>
  );
}

/** The hatching's spacing in device pixels. */
function PixelRatio() {
  const dpr = useThree((state) => state.viewport.dpr);
  useLayoutEffect(() => setPixelRatio(dpr), [dpr]);
  return null;
}
