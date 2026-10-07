/**
 * The env-pane (glossary §11): the region of the page that shows the simulated environment. A header with the layout's
 * id (not its title, which is stale in older layouts: Hadi, 6 October 2026, P20) and the two views (tilted, from above:
 * the same scene, the camera moved); the scene of the current sim-run at its latest tick, or of a view of a layout and
 * a setup; and, at its foot, the control bar the page passes in (it acts on what the env-pane shows). While the camera
 * is moved freely (`free`) neither preset shows pressed; a preset puts it back.
 *
 * Three switches in the header (T-viz 1d and 1e; Hadi, 7 October 2026, preferred), one per drawing on the floor: the
 * robot's plan, the human's real path, the robot's expectation of the human; each a small pill with a swatch of its
 * drawing, on by default, remembered in the browser.
 */

import { Canvas, useThree } from "@react-three/fiber";
import { type ReactNode, useLayoutEffect, useMemo, useState } from "react";

import type { Appearance } from "../gen/messages";
import { FramingCamera, type View } from "./camera";
import { setPixelRatio } from "./material";
import { type Ahead, type PathsShown, readShown, saveShown } from "./paths";
import type { PlaceBook } from "./places";
import { theme } from "../theme";
import { type Moment, type Room, Scene } from "./Scene";

export function EnvPane({ layout, room, moment, book, appearance, view, free, onView, onFree, glideMs, ahead,
                          controls }: {
  layout: string;
  room: Room;
  moment: Moment;
  book: PlaceBook;
  appearance: Appearance;
  view: View;
  free: boolean;
  onView: (view: View) => void;
  onFree: () => void;
  glideMs: number;
  ahead: Ahead;
  controls: ReactNode;
}) {
  const [shown, setShown] = useState<PathsShown>(() => readShown());
  const toggle = (key: keyof PathsShown) => setShown((s) => {
    const next = { ...s, [key]: !s[key] };
    saveShown(next);
    return next;
  });
  const tallest = useMemo(() => Math.max(
    appearance.human.height, appearance.robot.height, appearance.default_fixed.height,
    ...Object.values(appearance.fixed).map((l) => l.height)), [appearance]);
  return (
    <section className="env-pane">
      <header className="env-pane-header">
        <div className="env-pane-title">
          <span className="env-pane-name">{layout}</span>
        </div>
        <div className="env-pane-tools">
        <div className="path-switches" role="group" aria-label="Drawn on the floor">
          {SWITCHES.map(({ key, label, title, swatch }) => (
            <button key={key} type="button" className="path-switch" aria-pressed={shown[key]} title={title}
                    onClick={() => toggle(key)}>
              {swatch}
              {label}
            </button>
          ))}
        </div>
        <div className="segmented" role="group" aria-label="View">
          {(["tilted", "top"] as const).map((v) => (
            <button key={v} type="button" aria-pressed={!free && view === v} onClick={() => onView(v)}>
              {v === "tilted" ? "Tilted" : "From above"}
            </button>
          ))}
        </div>
        </div>
      </header>
      <div className="env-pane-scene">
        <Canvas orthographic flat dpr={[1, 2]} gl={{ antialias: true, preserveDrawingBuffer: true, stencil: true }}>
          <PixelRatio />
          <FramingCamera view={view} free={free} onFree={onFree} bounds={room.space.bounds} height={tallest} />
          <Scene room={room} moment={moment} book={book} appearance={appearance} glideMs={glideMs} ahead={ahead}
                 shown={shown} />
        </Canvas>
      </div>
      {controls}
    </section>
  );
}

/** A swatch of a drawing: a short dashed line, or a short stripe, as the scene draws it. */
function LineSwatch({ colour }: { colour: string }) {
  return (
    <svg className="path-swatch" width="22" height="10" viewBox="0 0 22 10" aria-hidden="true">
      <line x1="1" y1="5" x2="17" y2="5" stroke={colour} strokeWidth="2" strokeDasharray="4 3" />
      <circle cx="18.5" cy="5" r="2.6" fill={colour} stroke={theme.color.surface} strokeWidth="1.2" />
    </svg>
  );
}

function StripeSwatch() {
  return (
    <svg className="path-swatch" width="22" height="10" viewBox="0 0 22 10" aria-hidden="true">
      <rect x="1" y="1" width="20" height="8" rx="4" fill={theme.color.human} fillOpacity={0.22} />
    </svg>
  );
}

const SWITCHES: { key: keyof PathsShown; label: string; title: string; swatch: ReactNode }[] = [
  { key: "plan", label: "Robot plan", title: "The robot's own walks ahead", swatch: <LineSwatch colour={theme.color.robot} /> },
  { key: "path", label: "Human path", title: "The human's real walks ahead, which the robot does not know",
    swatch: <LineSwatch colour={theme.color.human} /> },
  { key: "expectation", label: "Expectation", title: "The robot's expectation of the human: filled for an admitted task, hatched for the fallback projection",
    swatch: <StripeSwatch /> },
];

/** The hatching's spacing in device pixels. */
function PixelRatio() {
  const dpr = useThree((state) => state.viewport.dpr);
  useLayoutEffect(() => setPixelRatio(dpr), [dpr]);
  return null;
}
