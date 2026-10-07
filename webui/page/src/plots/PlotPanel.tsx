/**
 * Panel 4c, the plots over the ticks (T-viz 1c; Hadi, 7 October 2026, preferred: version A, the page's own drawing, with
 * his changes): seven lanes on one tick axis, in Hadi's order: the human's task with its tag per task; the recognizer's
 * outputs together, the belief (θ, what the robot holds since its last decision, a legend), the tail probability S (α)
 * and the finding; context (absent when the sim-run's timeline has no window); the robot's task with its holds and
 * decisions; the robot-human distance with min_separation, the ticks below it shaded. Drawn on one canvas
 * (src/plots/draw.ts) over the geometry of src/plots/look.ts.
 *
 * A vertical line marks the latest tick; hovering shows the tick's values; a click shows that tick in the whole page (the
 * past view, App.tsx), a click on the latest tick returns to it. The panel fits its lanes (up to FIT of the window) until
 * the screen-user drags the border above it (App.tsx); then it keeps that height, and lanes taller than it scroll inside
 * it. The page computes nothing: every value is the
 * tick updates'.
 */

import { useEffect, useMemo, useRef, useState } from "react";

import type { TaskColours } from "../frame/colours";
import { draw } from "./draw";
import { axisEnd, type Lanes } from "./lanes";
import { FIT } from "../frame/layout";
import { geometry, tickOf, tipRows, xOf } from "./look";

export function PlotPanel({ lanes, colours, viewed, onView, height }: {
  lanes: Lanes | null; colours: TaskColours; viewed: number | null; onView: (tick: number | null) => void;
  height: number | null;
}) {
  const box = useRef<HTMLDivElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const [width, setWidth] = useState(0);
  const [hover, setHover] = useState<{ t: number; x: number; y: number } | null>(null);
  const length = lanes?.length ?? 0;
  const end = axisEnd(length);
  const sized = height === null ? { maxHeight: `${FIT * 100}vh` } : { height };
  const g = useMemo(() => (lanes === null || width === 0 ? null : geometry(lanes, width)), [lanes, width]);

  useEffect(() => {
    const el = box.current;
    if (el === null) return;
    const observer = new ResizeObserver(() => setWidth(el.clientWidth));
    observer.observe(el);
    setWidth(el.clientWidth);
    return () => observer.disconnect();
  }, [lanes === null]);   // the box exists once there are lanes

  useEffect(() => {
    const el = canvas.current;
    if (el === null || lanes === null || g === null) return;
    const dpr = window.devicePixelRatio || 1;
    // the canvas is re-allocated only when its size changes: a re-allocation each tick stalls the browser's renderer
    const w = Math.round(g.width * dpr), h = Math.round(g.height * dpr);
    if (el.width !== w) el.width = w;
    if (el.height !== h) el.height = h;
    // drawn by the CPU rasteriser: many-segment lines, redrawn each tick, stall a GPU-rasterised canvas
    const ctx = el.getContext("2d", { willReadFrequently: true })!;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    draw(ctx, g, lanes, colours, end, viewed);
  }, [lanes, g, colours, end, viewed]);

  if (lanes === null) {
    return (
      <aside className="plots plots-empty" aria-label="Plots over ticks" style={height === null ? { height: 32 } : { height }}>
        <span>plots over ticks</span>
      </aside>
    );
  }
  const at = (clientX: number) => {
    if (g === null) return null;
    const rect = box.current!.getBoundingClientRect();
    return tickOf(g, end, length, clientX - rect.left);
  };
  return (
    <aside className="plots" aria-label="Plots over ticks" style={sized}>
      <div ref={box} className="plots-box" style={{ height: g?.height ?? 120 }}
           onMouseMove={(e) => {
             const t = at(e.clientX);
             const rect = box.current!.getBoundingClientRect();
             setHover(t === null ? null : { t, x: e.clientX - rect.left, y: e.clientY - rect.top });
           }}
           onMouseLeave={() => setHover(null)}
           onClick={(e) => {
             const t = at(e.clientX);
             if (t !== null) onView(t === length - 1 ? null : t);
           }}>
        {g !== null && <canvas ref={canvas} className="plots-canvas" style={{ width: g.width, height: g.height }}
                               role="img" aria-label={`Plots over ticks 0 to ${length - 1}`} />}
        {length === 0 && <span className="plots-wait">no tick yet</span>}
        {hover !== null && g !== null && (
          <>
            <span className="plots-hair" style={{ left: xOf(g, end, hover.t + 0.5), top: g.boxes[0]?.y ?? 0,
                                                   height: g.axisY - (g.boxes[0]?.y ?? 0) - 6 }} />
            <Tip lanes={lanes} colours={colours} t={hover.t} left={hover.x} top={hover.y} wide={g.width} />
          </>
        )}
      </div>
    </aside>
  );
}

function Tip({ lanes, colours, t, left, top, wide }: {
  lanes: Lanes; colours: TaskColours; t: number; left: number; top: number; wide: number;
}) {
  const right = left > wide / 2;
  return (
    <div className="plots-tip" style={right ? { right: wide - left + 14, top: Math.max(0, top - 24) }
                                            : { left: left + 14, top: Math.max(0, top - 24) }}>
      <div className="plots-tip-head">tick {t}</div>
      {tipRows(lanes, t, colours).map((r, i) => (
        <div key={i} className="plots-tip-row">
          <i style={{ background: r.colour ?? "transparent" }} />
          <span>{r.label}</span>
          <b>{r.value}</b>
        </div>
      ))}
    </div>
  );
}
