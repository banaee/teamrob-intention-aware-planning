/**
 * Panel 4c, the plots over the ticks (T-viz 1c; docs/handoffs/plan_T-viz_1c.md; Hadi, 7 October 2026, preferred): five
 * lanes on one tick axis, in Hadi's order: the human's task with its tag per task; the robot's belief with θ and what it
 * holds since its last decision; context (absent when the sim-run's timeline has no window); the robot's task with its
 * holds and decisions; the robot-human distance with min_separation, the ticks below it shaded.
 *
 * Two versions, for Hadi to choose between (T-viz 1c, HADI'S REVIEW AND TWO VERSIONS): A, the page's own drawing on a
 * canvas (src/plots/drawA.ts); B, a product dashboard's cards with Recharts (src/plots/PlotsB.tsx). Both draw the same lanes on the same
 * geometry (src/plots/look.ts); a small switch at the panel's foot chooses one, remembered in this browser. A vertical
 * line marks the latest tick; hovering shows the tick's values; a click shows that tick in the whole page (the past view,
 * App.tsx), a click on the latest tick returns to it. The page computes nothing: every value is the tick updates'.
 */

import { useEffect, useMemo, useRef, useState } from "react";

import type { TaskColours } from "../frame/colours";
import { drawA } from "./drawA";
import { axisEnd, type Lanes } from "./lanes";
import { geometry, SPEC_A, SPEC_B, tickOf, tipRows, xOf } from "./look";
import { PlotsB } from "./PlotsB";

export type Version = "A" | "B";

const KEY = "tviz.plots.version";

function remembered(): Version {
  try { return window.localStorage.getItem(KEY) === "B" ? "B" : "A"; } catch { return "A"; }
}

export function PlotPanel({ lanes, colours, viewed, onView }: {
  lanes: Lanes | null; colours: TaskColours; viewed: number | null; onView: (tick: number | null) => void;
}) {
  const box = useRef<HTMLDivElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const [width, setWidth] = useState(0);
  const [version, setVersion] = useState<Version>(remembered);
  const [hover, setHover] = useState<{ t: number; x: number; y: number } | null>(null);
  const length = lanes?.length ?? 0;
  const end = axisEnd(length);
  const g = useMemo(() => (lanes === null || width === 0 ? null
    : geometry(lanes, width, version === "A" ? SPEC_A : SPEC_B)), [lanes, width, version]);

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
    if (version !== "A" || el === null || lanes === null || g === null) return;
    const dpr = window.devicePixelRatio || 1;
    el.width = Math.round(g.width * dpr);
    el.height = Math.round(g.height * dpr);
    const ctx = el.getContext("2d")!;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    drawA(ctx, g, lanes, colours, end, viewed);
  }, [version, lanes, g, colours, end, viewed]);

  const choose = (v: Version) => {
    setVersion(v);
    try { window.localStorage.setItem(KEY, v); } catch { /* a private window keeps it for the page's life */ }
  };

  if (lanes === null) {
    return (
      <aside className="plots plots-empty" aria-label="Plots over ticks">
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
    <aside className="plots" aria-label="Plots over ticks">
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
        {g !== null && (version === "A"
          ? <canvas ref={canvas} className="plots-canvas" style={{ width: g.width, height: g.height }}
                    role="img" aria-label={`Plots over ticks 0 to ${length - 1}`} />
          : <PlotsB g={g} lanes={lanes} length={length} colours={colours} end={end} viewed={viewed} />)}
        {length === 0 && <span className="plots-wait">no tick yet</span>}
        {hover !== null && g !== null && (
          <>
            <span className="plots-hair" style={{ left: xOf(g, end, hover.t + 0.5), top: g.boxes[0]?.y ?? 0,
                                                   height: g.axisY - (g.boxes[0]?.y ?? 0) - 6 }} />
            <Tip lanes={lanes} colours={colours} t={hover.t} left={hover.x} top={hover.y} wide={g.width} />
          </>
        )}
        <div className="plots-switch" role="group" aria-label="Plots version" onClick={(e) => e.stopPropagation()}>
          {(["A", "B"] as const).map((v) => (
            <button key={v} type="button" className={v === version ? "is-on" : undefined} onClick={() => choose(v)}
                    title={v === "A" ? "Version A: the page's own drawing" : "Version B: drawn with Recharts"}>{v}</button>
          ))}
        </div>
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
