/**
 * Panel 4c's look (T-viz 1c; Hadi, 7 October 2026, preferred: version A, the page's own drawing, with his changes): the
 * geometry the canvas draws on (src/plots/draw.ts), the colours, and the tooltip's rows.
 *
 * Each lane is a soft box in one tint for all, the very light blue of the robot's light tone (as panel 4b's "Intention
 * recognition"), with that tone as its left edge. A box's header column at its left holds the lane's title, a small number
 * where it helps (the leading belief, its S, the present distance) and a muted line; the plot area starts after it, at
 * one x for every box, so that one tick is one x through all lanes. The lanes, in Hadi's order: the human's task; the
 * recognizer's outputs together (belief, S, finding); context; the robot's task; distance. The axis' few numbers under
 * the last box. No grid lines; few colours: a task's colour (theme.taskSoft) shows as a light tint in a band, and as a
 * line only for a hypothesis that has led; the other hypotheses are thin grey lines.
 */

import type { TaskColours } from "../frame/colours";
import { keyText } from "../frame/robot";
import { taskText } from "../frame/activity";
import { CAUSE_SHORT, TRIGGER_SHORT } from "../frame/robot";
import { theme } from "../theme";
import { type FactLane, findingAt, type FindingState, type HumanLane, type Lanes, type PairLane, type RobotLane } from "./lanes";

export const PAD = 2;          // px: the boxes' outer margin in the canvas
export const LABEL = 172;      // px: a box's header column, to the left of the plot area
export const RIGHT = 16;       // px: the box's padding to the right of the plot area
export const GAP = 8;          // px: between boxes
export const AXIS = 22;        // px: the axis' numbers under the last box
export const ACCENT = 3;       // px: a box's left edge, as the right panel's blocks have
export const RADIUS = 10;
export const HEADER = 0.30;    // the header column's tint: a little deeper than the box

export const BAND = 20;
export const BELIEF = 92;
export const BELIEF_TOP = 9;   // px: the belief's 1 below the row's top, the held admission's strip above it
export const TAIL = 64;
export const FINDING = 12;
export const FACT = 16;
export const ROBOT = 24;
export const DISTANCE = 56;
export const ROW_GAP = 4;
export const BOX_PAD = 9;      // px: above and below the rows inside a box
export const SCALE = 4;        // the distance lane reaches SCALE × min_separation; a larger distance at its top

/** The finding's colours, as the analyses' figures show the states (analysis/instruments/irb/plot.py, BAND): adequate
 * nearly white, unresolved a light grey, unexplained red, exhausted a dark grey; softened to the page's tones. */
export const FINDING_COLOUR: Record<FindingState, string> = {
  adequate: "#FFFFFF",
  unresolved: "#D5D8E2",
  unexplained: "#E9A19D",
  exhausted: "#8C92A6",
};

/** The one box: its fill, its left edge, its header column's tint, its title's colour. */
export function box(): { fill: string; edge: string; header: string; title: string } {
  const c = theme.color;
  const fill = mix(c.robotLight, "#FFFFFF", 0.86);
  return { fill, edge: c.robotLight, header: mix(c.robotLight, "#FFFFFF", 0.86 - HEADER * 0.86 * 0.25), title: c.robotDark };
}

export type Row =
  | { kind: "human"; lane: HumanLane; y: number; h: number }
  | { kind: "belief"; lane: RobotLane; y: number; h: number; off: boolean }
  | { kind: "tail"; lane: RobotLane; y: number; h: number; off: boolean }
  | { kind: "finding"; lane: RobotLane; y: number; h: number; off: boolean }
  | { kind: "fact"; lane: FactLane; y: number; h: number }
  | { kind: "robot"; lane: RobotLane; y: number; h: number }
  | { kind: "distance"; lane: PairLane; y: number; h: number; minSep: number };

export interface Box {
  title: string;
  y: number;
  h: number;
  rows: Row[];
  /** A row's own name in the header, only where the box holds more than one row (two humans, two robots, two facts). */
  named: boolean;
}

export interface Geometry {
  width: number;
  height: number;
  boxes: Box[];
  /** The plot area's left and right x, the same for every box. */
  x0: number;
  x1: number;
  /** The axis' baseline. */
  axisY: number;
}

export function geometry(lanes: Lanes, width: number): Geometry {
  const boxes: Box[] = [];
  let y = PAD;
  const add = <T,>(title: string, elements: readonly T[], height: (e: T) => number, row: (e: T, y: number, h: number) => Row) => {
    if (elements.length === 0) return;
    const rows: Row[] = [];
    let at = y + BOX_PAD;
    for (const e of elements) { const h = height(e); rows.push(row(e, at, h)); at += h + ROW_GAP; }
    const h = at - ROW_GAP + BOX_PAD - y;
    boxes.push({ title, y, h, rows, named: elements.length > 1 });
    y += h + GAP;
  };
  const on = (l: RobotLane) => l.robot.condition === "intention-aware";
  add("human", lanes.humans, () => BAND, (lane, y, h) => ({ kind: "human", lane, y, h }));
  add("belief", lanes.robots, (l) => (on(l) ? BELIEF : BAND), (lane, y, h) => ({ kind: "belief", lane, y, h, off: !on(lane) }));
  add("S", lanes.robots, (l) => (on(l) ? TAIL : BAND), (lane, y, h) => ({ kind: "tail", lane, y, h, off: !on(lane) }));
  add("finding", lanes.robots, (l) => (on(l) ? FINDING : BAND), (lane, y, h) => ({ kind: "finding", lane, y, h, off: !on(lane) }));
  add("context", lanes.facts, () => FACT, (lane, y, h) => ({ kind: "fact", lane, y, h }));
  add("robot", lanes.robots, () => ROBOT, (lane, y, h) => ({ kind: "robot", lane, y, h }));
  add("distance", lanes.pairs, () => DISTANCE, (lane, y, h) => ({
    kind: "distance", lane, y, h, minSep: lanes.robots.find((r) => r.robot.robot === lane.robot)!.robot.min_separation,
  }));
  const axisY = y - GAP + 6;
  const x0 = PAD + LABEL;
  return { width, height: axisY + AXIS - 6, boxes, x0, x1: Math.max(x0 + 1, width - PAD - RIGHT), axisY };
}

/** The x of a tick's left edge, and of its middle, on the axis from 0 to `end`. */
export function xOf(g: Geometry, end: number, t: number): number {
  return g.x0 + (t / end) * (g.x1 - g.x0);
}

/** The tick under an x of the plot area, among the ticks held; null outside it: what a click shows. */
export function tickOf(g: Geometry, end: number, length: number, x: number): number | null {
  if (x < g.x0 || x > g.x1 || length === 0) return null;
  return Math.min(length - 1, Math.max(0, Math.floor(((x - g.x0) / (g.x1 - g.x0)) * end)));
}

/** The axis' step: few numbers, at least 160 px apart. */
export function axisStep(g: Geometry, end: number): number {
  return [25, 50, 100, 200, 500, 1000].find((s) => (s / end) * (g.x1 - g.x0) >= 160) ?? 2000;
}

/** The tick the large numbers and the dots show: the viewed earlier tick, or the latest; null before the first. */
export function shownTick(lanes: Lanes, viewed: number | null): number | null {
  if (lanes.length === 0) return null;
  return viewed !== null && viewed < lanes.length ? viewed : lanes.length - 1;
}

/** The leading belief at a tick: the leader, its value, its colour; null where the recognizer gave none. */
export function leading(lane: RobotLane, t: number): { key: string; value: number } | null {
  const b = lane.belief[t];
  if (!b || b.leader === null) return null;
  const h = b.live.find((x) => x.key === b.leader);
  return h === undefined ? null : { key: h.key, value: h.belief };
}

// =============================================================================
// Colour
// =============================================================================

/** A task's colour in panel 4c (theme.taskSoft), by its identity. */
export function softOf(colours: TaskColours, identity: string): string {
  return colours.get(identity) ?? theme.taskSoftOther;
}

/** `a` mixed toward `b`: f = 0 gives a, f = 1 gives b. Hex colours only. */
export function mix(a: string, b: string, f: number): string {
  const p = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const [x, y] = [p(a), p(b)];
  return "#" + x.map((v, i) => Math.round(v + (y[i] - v) * f).toString(16).padStart(2, "0")).join("");
}

/** A band's fill (a light tint of the task's colour) and its text (the colour, deepened toward the ink). */
export function bandFill(colour: string): string { return mix(colour, "#FFFFFF", 0.72); }
export function bandText(colour: string): string { return mix(colour, theme.color.ink, 0.45); }

// =============================================================================
// The tooltip's rows: the tick's values, short
// =============================================================================

/** A row of the tooltip: a short label, its value, and the colour square of the task it names (null: none). */
export interface TipRow {
  label: string;
  value: string;
  colour: string | null;
}

export function tipRows(lanes: Lanes, t: number, colours: TaskColours): TipRow[] {
  const rows: TipRow[] = [];
  for (const h of lanes.humans) {
    const task = h.task[t], tag = h.tag[t];
    rows.push({ label: "human", value: task === null ? "–" : `${taskText(task)}${tag !== null && tag.tag !== "no fact" ? ` · ${tag.tag}` : ""}`,
                colour: task === null ? null : softOf(colours, task.identity) });
  }
  for (const r of lanes.robots) {
    const b = r.belief[t];
    if (b !== null && b.leader !== null) {
      for (const x of [...b.live].sort((a, z) => z.belief - a.belief).slice(0, 2)) {
        rows.push({ label: keyText(r.robot, x.key), value: x.belief.toFixed(2), colour: softOf(colours, x.key) });
      }
    } else if (r.robot.condition !== "intention-aware") rows.push({ label: "belief", value: "off", colour: null });
    const lead = b === null || b.leader === null ? undefined : b.live.find((x) => x.key === b.leader);
    if (lead !== undefined && lead.tail !== null) rows.push({ label: "S", value: lead.tail.toFixed(2), colour: null });
    const finding = findingAt(r, t);
    if (finding !== null) rows.push({ label: "finding", value: finding, colour: null });
    const held = r.held[t];
    if (held !== null) rows.push({ label: "held", value: keyText(r.robot, held), colour: softOf(colours, held) });
  }
  const on = lanes.facts.filter((f) => f.holds[t]).map((f) => f.fact);
  if (on.length > 0) rows.push({ label: "context", value: on.join(", "), colour: null });
  for (const r of lanes.robots) {
    const task = r.task[t];
    rows.push({ label: "robot", value: `${task === null ? "–" : taskText(task)}${r.hold[t] ? " · hold" : ""}`,
                colour: task === null ? null : softOf(colours, task.identity) });
    const d = r.decision[t];
    if (d !== null) {
      rows.push({ label: "decision", value: `${TRIGGER_SHORT[d.trigger]}${d.cause !== null ? ` · ${CAUSE_SHORT[d.cause]}` : ""}`,
                  colour: null });
    }
  }
  for (const p of lanes.pairs) {
    const s = p.separation[t];
    if (s !== null) {
      rows.push({ label: "distance", value: `${s.minimum.toFixed(0)}${s.below ? " · below min" : ""}`,
                  colour: s.below ? theme.color.separation : null });
    }
  }
  return rows;
}
