/**
 * Panel 4c, the plots over the ticks (T-viz 1c; docs/handoffs/plan_T-viz_1c.md; Hadi, 7 October 2026, preferred): five
 * lanes on one tick axis, in Hadi's order, drawn on one canvas from the lanes the page folds over its tick updates
 * (src/plots/lanes.ts):
 *   (1) the human's task, a band per stretch in the task's colour, its tag per task as a thin strip under it;
 *   (2) the robot's belief, one line per hypothesis in the task's colour (a hypothesis that has led drawn full, the
 *       others thin and light), θ dashed, what the robot holds since its last decision as a strip along the top;
 *   (3) context, a band per timeline fact while it holds (absent when the sim-run's timeline has no window);
 *   (4) the robot's task, a band per task, a hold as a dark strip under it, a mark above it at each decision;
 *   (5) distance, the continuous minimum over the tick, min_separation dashed, the ticks below it shaded.
 * A vertical line marks the latest tick through all lanes, a second one the viewed earlier tick. Hovering shows the
 * tick's values; a click shows that tick in the whole page (the page's past view, App.tsx), a click on the latest tick
 * returns to it. Short labels, no sentences. The page computes nothing: every value is the tick updates'.
 * Drawn by the page itself on a canvas (no plotting library): the lanes are mostly bands and marks on one shared tick
 * axis, with one hairline, one click and the past view across all five; the colours, line weights, opacities and type
 * are the theme's (src/theme.ts), as the panels' and the scene's are.
 */

import { useEffect, useMemo, useRef, useState } from "react";

import { colourOf, taskColour, type TaskColours } from "../frame/colours";
import { taskText } from "../frame/activity";
import { CAUSE_SHORT, keyText, TRIGGER_SHORT } from "../frame/robot";
import type { TagValue } from "../gen/messages";
import { theme } from "../theme";
import {
  axisEnd, beliefLines, type FactLane, heldBands, humanBands, type HumanLane, type Lanes, type PairLane, robotBands,
  type RobotLane, trueBands,
} from "./lanes";

const GUTTER = 156;   // px: the lane titles and the row labels
const RIGHT = 16;
const TOP = 6;
const AXIS = 20;
const GAP = 10;
const BAND = 16;
const TAG = 3;
const BELIEF = 84;
const OFF = 16;
const FACT = 13;
const MARK = 7;
const HOLD = 4;
const DISTANCE = 48;
const SCALE = 4;      // the distance lane reaches SCALE × min_separation; a larger distance is drawn at its top edge

const TAG_COLOUR: Record<TagValue, string> = {
  "in accord": theme.color.tagAccord,
  "not in accord": theme.color.tagNotAccord,
  "no fact": theme.color.tagNoFact,
};

type Row =
  | { kind: "human"; lane: HumanLane; y: number; h: number }
  | { kind: "belief"; lane: RobotLane; y: number; h: number; off: string | null }
  | { kind: "fact"; lane: FactLane; y: number; h: number }
  | { kind: "robot"; lane: RobotLane; y: number; h: number }
  | { kind: "distance"; lane: PairLane; y: number; h: number; minSep: number; kept: boolean };

interface Section {
  title: string;
  y: number;
  rows: Row[];
}

function layout(lanes: Lanes): { sections: Section[]; height: number } {
  const sections: Section[] = [];
  let y = TOP;
  const section = (title: string, make: (y: number) => Row[]) => {
    const rows = make(y);
    if (rows.length === 0) return;
    sections.push({ title, y, rows });
    const last = rows[rows.length - 1];
    y = last.y + last.h + GAP;
  };
  const stack = <T,>(elements: readonly T[], height: (element: T) => number, row: (element: T, y: number, h: number) => Row) =>
    (y0: number) => {
      let at = y0;
      return elements.map((element) => { const h = height(element); const r = row(element, at, h); at += h + 4; return r; });
    };
  section("human's task", stack(lanes.humans, () => BAND + TAG + 1, (lane, y, h) => ({ kind: "human", lane, y, h })));
  section("robot's belief", stack(lanes.robots, (l) => (offText(l) === null ? BELIEF : OFF),
                                  (lane, y, h) => ({ kind: "belief", lane, y, h, off: offText(lane) })));
  section("context", stack(lanes.facts, () => FACT, (lane, y, h) => ({ kind: "fact", lane, y, h })));
  section("robot's task", stack(lanes.robots, () => MARK + BAND + HOLD + 1, (lane, y, h) => ({ kind: "robot", lane, y, h })));
  section("distance", stack(lanes.pairs, () => DISTANCE, (lane, y, h) => {
    const robot = lanes.robots.find((r) => r.robot.robot === lane.robot)!.robot;
    return { kind: "distance", lane, y, h, minSep: robot.min_separation, kept: robot.condition !== "human-unaware" };
  }));
  return { sections, height: y - GAP + AXIS };
}

/** Why a robot's belief lane is empty: its recognizer does not run in its condition. */
function offText(lane: RobotLane): string | null {
  return lane.robot.condition === "intention-aware" ? null : `off · ${lane.robot.condition}`;
}

export function PlotPanel({ lanes, colours, viewed, onView }: {
  lanes: Lanes | null; colours: TaskColours; viewed: number | null; onView: (tick: number | null) => void;
}) {
  const box = useRef<HTMLDivElement>(null);
  const base = useRef<HTMLCanvasElement>(null);
  const [width, setWidth] = useState(0);
  const [hover, setHover] = useState<{ t: number; x: number; y: number } | null>(null);
  const shape = useMemo(() => (lanes === null ? null : layout(lanes)), [lanes]);
  const length = lanes?.length ?? 0;
  const end = axisEnd(length);

  useEffect(() => {
    const el = box.current;
    if (el === null) return;
    const observer = new ResizeObserver(() => setWidth(el.clientWidth));
    observer.observe(el);
    setWidth(el.clientWidth);
    return () => observer.disconnect();
  }, [lanes === null]);   // the box exists once there are lanes

  useEffect(() => {
    const canvas = base.current;
    if (canvas === null || lanes === null || shape === null || width === 0) return;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(shape.height * dpr);
    const ctx = canvas.getContext("2d")!;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    draw(ctx, width, shape, lanes, colours, end, viewed);
  }, [lanes, shape, colours, width, end, viewed]);

  const plotW = Math.max(1, width - GUTTER - RIGHT);
  const tickAt = (clientX: number): number | null => {
    const rect = box.current!.getBoundingClientRect();
    const x = clientX - rect.left - GUTTER;
    if (x < 0 || x > plotW || length === 0) return null;
    return Math.min(length - 1, Math.max(0, Math.floor((x / plotW) * end)));
  };

  if (lanes === null || shape === null) {
    return (
      <aside className="plots plots-empty" aria-label="Plots over ticks">
        <span className="strip-title">Plots over ticks · no sim-run</span>
      </aside>
    );
  }
  const x = (t: number) => GUTTER + ((t + 0.5) / end) * plotW;
  return (
    <aside className="plots" aria-label="Plots over ticks">
      <div ref={box} className="plots-box" style={{ height: shape.height }}
           onMouseMove={(e) => {
             const t = tickAt(e.clientX);
             const rect = box.current!.getBoundingClientRect();
             setHover(t === null ? null : { t, x: e.clientX - rect.left, y: e.clientY - rect.top });
           }}
           onMouseLeave={() => setHover(null)}
           onClick={(e) => {
             const t = tickAt(e.clientX);
             if (t !== null) onView(t === length - 1 ? null : t);
           }}>
        <canvas ref={base} className="plots-canvas" style={{ width, height: shape.height }}
                role="img" aria-label={`Plots over ticks 0 to ${length - 1}`} />
        {length === 0 && <span className="plots-wait">no tick yet</span>}
        {hover !== null && (
          <>
            <span className="plots-hair" style={{ left: x(hover.t), height: shape.height - AXIS }} />
            <Tip lanes={lanes} t={hover.t} left={hover.x} top={hover.y} wide={width} />
          </>
        )}
      </div>
    </aside>
  );
}

// =============================================================================
// Drawing
// =============================================================================

function draw(ctx: CanvasRenderingContext2D, width: number, shape: { sections: Section[]; height: number },
              lanes: Lanes, colours: TaskColours, end: number, viewed: number | null): void {
  const c = theme.color;
  const W = Math.max(1, width - GUTTER - RIGHT);
  const px = (t: number) => GUTTER + (t / end) * W;          // the left edge of tick t
  const mid = (t: number) => px(t + 0.5);
  const n = lanes.length;
  ctx.clearRect(0, 0, width, shape.height);
  ctx.textBaseline = "middle";
  const font = (size: number, weight: number = theme.type.weight.regular) => `${weight} ${size}px ${theme.type.family}`;
  const text = (s: string, x: number, y: number, colour: string, size: number = theme.type.size.xs, align: CanvasTextAlign = "left",
                weight: number = theme.type.weight.regular) => {
    ctx.font = font(size, weight); ctx.fillStyle = colour; ctx.textAlign = align; ctx.fillText(s, x, y);
  };
  /** A band from tick a to tick b, its label inside where it fits. */
  const band = (a: number, b: number, y: number, h: number, colour: string, label: string | null, alpha = 1) => {
    const x0 = px(a), x1 = px(b + 1);
    ctx.globalAlpha = alpha; ctx.fillStyle = colour;
    ctx.fillRect(x0, y, Math.max(1, x1 - x0 - 0.5), h);
    ctx.globalAlpha = 1;
    if (label !== null) {
      ctx.font = font(theme.type.size.xs);
      const w = ctx.measureText(label).width;
      if (w + 8 < x1 - x0) {
        ctx.save(); ctx.beginPath(); ctx.rect(x0, y, x1 - x0, h); ctx.clip();
        text(label, x0 + 4, y + h / 2 + 0.5, "#FFFFFF");
        ctx.restore();
      }
    }
  };
  const dashed = (y: number, colour: string) => {
    ctx.save(); ctx.strokeStyle = colour; ctx.lineWidth = theme.line.guide; ctx.setLineDash([4, 3]);
    ctx.beginPath(); ctx.moveTo(GUTTER, y); ctx.lineTo(GUTTER + W, y); ctx.stroke(); ctx.restore();
  };
  const line = (ys: readonly (number | null)[], y: (v: number) => number, colour: string, weight: number, alpha: number) => {
    ctx.save(); ctx.strokeStyle = colour; ctx.lineWidth = weight; ctx.globalAlpha = alpha; ctx.lineJoin = "round";
    ctx.beginPath();
    let open = false;
    for (let t = 0; t < n; t++) {
      const v = ys[t];
      if (v === null) { open = false; continue; }
      if (open) ctx.lineTo(mid(t), y(v)); else { ctx.moveTo(mid(t), y(v)); open = true; }
      // a value standing alone is drawn as a short dash
      if (t + 1 >= n || ys[t + 1] === null) ctx.lineTo(mid(t) + 0.5, y(v));
    }
    ctx.stroke(); ctx.restore();
  };

  for (const section of shape.sections) {
    text(section.title, 0, section.y + 7, c.ink, theme.type.size.sm, "left", theme.type.weight.medium);
    for (const row of section.rows) {
      // the plot's ground, so that the lane's extent reads
      ctx.fillStyle = c.page;
      ctx.fillRect(GUTTER, row.y, W, row.h);
      switch (row.kind) {
        case "human": {
          text(row.lane.human, GUTTER - 6, row.y + BAND / 2, c.inkSoft, theme.type.size.xs, "right");
          for (const b of humanBands(row.lane, n)) {
            band(b.start, b.end, row.y, BAND, taskColour(colours, b.value.task), taskText(b.value.task));
            if (b.value.tag !== null) band(b.start, b.end, row.y + BAND + 1, TAG, TAG_COLOUR[b.value.tag.tag], null);
          }
          break;
        }
        case "belief": {
          const robot = row.lane.robot;
          if (row.off !== null) {
            text(robot.robot, GUTTER - 6, row.y + row.h / 2, c.inkSoft, theme.type.size.xs, "right");
            text(row.off, GUTTER + 6, row.y + row.h / 2, c.inkFaint);
            break;
          }
          text(robot.robot, 0, row.y + 22, c.inkSoft);
          const top = row.y + 5, h = row.h - 6;
          const y = (v: number) => top + (1 - v) * h;
          text("1", GUTTER - 6, top, c.inkFaint, theme.type.size.xs, "right");
          text("0", GUTTER - 6, top + h, c.inkFaint, theme.type.size.xs, "right");
          dashed(y(robot.theta), c.inkFaint);
          text(`θ ${robot.theta.toFixed(2)}`, GUTTER - 16, y(robot.theta), c.inkSoft, theme.type.size.xs, "right");
          for (const b of heldBands(row.lane, n)) band(b.start, b.end, row.y, 3, colourOf(colours, b.value), null);
          const lines = beliefLines(row.lane, n);
          const keys = [...lines.keys()];
          // the hypotheses that have led drawn last, full; the others thin and light
          for (const k of keys.filter((k) => !row.lane.leaders.has(k))) line(lines.get(k)!, y, colourOf(colours, k), theme.line.plotFaint, theme.opacity.plotFaint);
          for (const k of keys.filter((k) => row.lane.leaders.has(k))) line(lines.get(k)!, y, colourOf(colours, k), theme.line.plotLead, 1);
          // the leader at the latest tick named at its line's end
          const leader = n > 0 ? row.lane.belief[n - 1]?.leader ?? null : null;
          const value = leader === null ? null : lines.get(leader)?.[n - 1] ?? null;
          if (leader !== null && value !== null) {
            ctx.font = font(theme.type.size.xs);
            const label = keyText(robot, leader);
            const w = ctx.measureText(label).width;
            const lx = Math.min(mid(n - 1) + 6, GUTTER + W - w);
            text(label, lx, Math.max(top + 6, y(value) - 7), c.ink);
          }
          break;
        }
        case "fact": {
          text(row.lane.fact, GUTTER - 6, row.y + row.h / 2, c.inkSoft, theme.type.size.xs, "right");
          for (const b of trueBands(row.lane.holds, n)) band(b.start, b.end, row.y, row.h, c.inkSoft, row.lane.fact, theme.opacity.plotFact);
          break;
        }
        case "robot": {
          text(row.lane.robot.robot, GUTTER - 6, row.y + MARK + BAND / 2, c.inkSoft, theme.type.size.xs, "right");
          text("▾ decision  ▬ hold", 0, row.y + MARK + BAND + 2, c.inkFaint);
          const y = row.y + MARK;
          for (const b of robotBands(row.lane, n)) band(b.start, b.end, y, BAND, taskColour(colours, b.value), taskText(b.value));
          for (const b of trueBands(row.lane.hold, n)) band(b.start, b.end, y + BAND + 1, HOLD, c.ink, null, theme.opacity.plotHold);
          ctx.fillStyle = c.ink;
          for (let t = 0; t < n; t++) {
            if (row.lane.decision[t] === null) continue;
            const m = mid(t);
            ctx.beginPath(); ctx.moveTo(m - 3.5, row.y); ctx.lineTo(m + 3.5, row.y); ctx.lineTo(m, row.y + MARK - 1);
            ctx.closePath(); ctx.fill();
          }
          break;
        }
        case "distance": {
          text(`${row.lane.robot}–${row.lane.human}`, GUTTER - 6, row.y + 7, c.inkSoft, theme.type.size.xs, "right");
          const top = row.y + 2, h = row.h - 4, span = SCALE * row.minSep;
          const y = (v: number) => top + (1 - Math.min(v, span) / span) * h;
          for (let t = 0; t < n; t++) {
            if (row.lane.separation[t]?.below) { ctx.fillStyle = c.below; ctx.fillRect(px(t), row.y, Math.max(1, px(t + 1) - px(t)), row.h); }
          }
          dashed(y(row.minSep), c.separation);
          text(row.kept ? `min sep ${row.minSep}` : `min sep ${row.minSep} · not kept`, GUTTER - 6, y(row.minSep),
               c.separation, theme.type.size.xs, "right");
          line(row.lane.separation.slice(0, n).map((s) => (s === null ? null : s.minimum)), y, c.ink, theme.line.plot, 1);
          break;
        }
      }
    }
  }

  // the axis
  const axisY = shape.height - AXIS + 4;
  ctx.strokeStyle = c.lineFaint; ctx.lineWidth = theme.line.guide;
  ctx.beginPath(); ctx.moveTo(GUTTER, axisY); ctx.lineTo(GUTTER + W, axisY); ctx.stroke();
  const every = [10, 20, 50, 100, 200, 500, 1000].find((s) => (s / end) * W >= 48) ?? 2000;
  for (let t = 0; t <= end; t += every) {
    ctx.beginPath(); ctx.moveTo(px(t), axisY); ctx.lineTo(px(t), axisY + 3); ctx.stroke();
    text(`${t}`, px(t), axisY + 10, c.inkFaint, theme.type.size.xs, "center");
  }
  text("tick", 0, axisY + 10, c.inkFaint);

  // the latest tick through all lanes, and the viewed earlier tick
  const through = (t: number, colour: string, weight: number) => {
    ctx.strokeStyle = colour; ctx.lineWidth = weight;
    ctx.beginPath(); ctx.moveTo(mid(t), TOP); ctx.lineTo(mid(t), axisY); ctx.stroke();
  };
  if (n > 0) through(n - 1, c.ink, theme.line.guide);
  if (viewed !== null && viewed < n) {
    through(viewed, c.past, theme.line.viewed);
    ctx.font = font(theme.type.size.xs, theme.type.weight.medium);
    const label = `viewing ${viewed}`;
    const w = ctx.measureText(label).width;
    ctx.fillStyle = c.pastLight;
    ctx.fillRect(mid(viewed) - w / 2 - 4, axisY + 3, w + 8, 14);
    text(label, mid(viewed), axisY + 10, c.past, theme.type.size.xs, "center", theme.type.weight.medium);
  }
}

// =============================================================================
// The tooltip: the tick's values, short
// =============================================================================

function Tip({ lanes, t, left, top, wide }: { lanes: Lanes; t: number; left: number; top: number; wide: number }) {
  const rows: [string, string][] = [];
  for (const h of lanes.humans) {
    const task = h.task[t], tag = h.tag[t];
    rows.push([h.human, task === null ? "no task" : `${taskText(task)}${tag !== null ? ` · ${tag.tag}` : ""}`]);
  }
  for (const r of lanes.robots) {
    const b = r.belief[t];
    if (b !== null && b.leader !== null) {
      const top3 = [...b.live].sort((a, z) => z.belief - a.belief).slice(0, 3)
        .map((x) => `${keyText(r.robot, x.key)} ${x.belief.toFixed(2)}`).join(", ");
      rows.push(["belief", top3]);
    } else rows.push(["belief", r.robot.condition === "intention-aware" ? "none" : "off"]);
    const held = r.held[t];
    rows.push(["held", held === null ? "–" : keyText(r.robot, held)]);
  }
  if (lanes.facts.length > 0) {
    const on = lanes.facts.filter((f) => f.holds[t]).map((f) => f.fact);
    rows.push(["context", on.length === 0 ? "–" : on.join(", ")]);
  }
  for (const r of lanes.robots) {
    const task = r.task[t];
    rows.push([r.robot.robot, `${task === null ? "no task" : taskText(task)}${r.hold[t] ? " · hold" : ""}`]);
    const d = r.decision[t];
    if (d !== null) {
      rows.push(["decision", `${TRIGGER_SHORT[d.trigger]}${d.cause !== null ? ` (${CAUSE_SHORT[d.cause]})` : ""}`]);
    }
  }
  for (const p of lanes.pairs) {
    const s = p.separation[t];
    if (s !== null) rows.push(["distance", `${s.minimum.toFixed(1)} (end ${s.distance.toFixed(1)})${s.below ? " · below" : ""}`]);
  }
  const right = left > wide / 2;
  return (
    <div className="plots-tip" style={right ? { right: wide - left + 12, top: Math.max(0, top - 20) }
                                            : { left: left + 12, top: Math.max(0, top - 20) }}>
      <strong>tick {t}</strong>
      {rows.map(([k, v], i) => <div key={i}><span>{k}</span>{v}</div>)}
    </div>
  );
}
