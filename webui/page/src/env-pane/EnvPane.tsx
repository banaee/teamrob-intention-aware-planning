/**
 * The env-pane (glossary §11): the region of the page that shows the simulated environment. In stage 0.3 it holds the
 * scene of one sim-run at its start, seen tilted or from above (the same scene, the camera moved), and a header that
 * names the sim-run.
 */

import { Canvas, useThree } from "@react-three/fiber";
import { useLayoutEffect, useMemo } from "react";

import type { Appearance, RunDescription, TickUpdate } from "../gen/messages";
import { FramingCamera, type View } from "./camera";
import { setPixelRatio } from "./material";
import { Scene } from "./Scene";

export function EnvPane({ description, tick, appearance, view, onView }: {
  description: RunDescription;
  tick: TickUpdate;
  appearance: Appearance;
  view: View;
  onView: (view: View) => void;
}) {
  const run = description.run;
  const tallest = useMemo(() => Math.max(
    appearance.human.height, appearance.robot.height, appearance.default_fixed.height,
    ...Object.values(appearance.fixed).map((l) => l.height)), [appearance]);
  return (
    <section className="env-pane">
      <header className="env-pane-header">
        <div className="env-pane-title">
          <span className="env-pane-name">{description.world.space.title}</span>
          <span className="env-pane-run">
            {run.domain} · {run.layout} · {run.setup} · {run.scenario} · {tick.tick === null ? "start" : `tick ${tick.tick}`}
          </span>
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
          <Scene description={description} tick={tick} appearance={appearance} />
        </Canvas>
      </div>
    </section>
  );
}

/** The hatching's spacing in device pixels. */
function PixelRatio() {
  const dpr = useThree((state) => state.viewport.dpr);
  useLayoutEffect(() => setPixelRatio(dpr), [dpr]);
  return null;
}
