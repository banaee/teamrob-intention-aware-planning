/**
 * The env-pane (glossary §11): the region of the page that shows the simulated environment. A header with the room's
 * title and the two views (tilted, from above: the same scene, the camera moved); the scene of the current sim-run at
 * its latest tick; and, at its foot, the control bar the page passes in (it acts on what the env-pane shows).
 */

import { Canvas, useThree } from "@react-three/fiber";
import { type ReactNode, useLayoutEffect, useMemo } from "react";

import type { Appearance, RunDescription, TickUpdate } from "../gen/messages";
import { FramingCamera, type View } from "./camera";
import { setPixelRatio } from "./material";
import { Scene } from "./Scene";

export function EnvPane({ description, tick, appearance, view, onView, glideMs, controls }: {
  description: RunDescription;
  tick: TickUpdate;
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
          <span className="env-pane-name">{description.world.space.title}</span>
          <span className="env-pane-run">{description.run.layout}</span>
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
          <FramingCamera view={view} bounds={description.world.space.bounds} height={tallest} />
          <Scene description={description} tick={tick} appearance={appearance} glideMs={glideMs} />
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
