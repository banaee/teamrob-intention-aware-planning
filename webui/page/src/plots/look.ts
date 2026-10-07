/**
 * Panel 4c's look, shared by its two versions (T-viz 1c; Hadi, 7 October 2026, preferred: version A the page's own
 * drawing, version B drawn with a chart library; Hadi chooses between them). Both draw the same lanes (src/plots/lanes.ts)
 * on the same geometry, so that they differ in drawing only, and a click maps to a tick by one function.
 *
 * The geometry: each lane is a soft tinted box, as the right panel's blocks are: the human's task warm (the human's
 * light tone), the robot's belief in the recognition tint (the robot's light tone, as panel 4b's "Intention
 * recognition"), the robot's task in the planning tone (the robot's colour, as "Planning"), context and distance
 * neutral. A short title in small capitals sits at the box's left; the plot area starts after it, at one x for every
 * box, so that one tick is one x through all lanes; a column at the box's right holds a large number where it helps
 * (the leading belief, the present distance). The axis' few numbers under the last box. Much empty space, few labels,
 * as a product dashboard's cards (Hadi, 7 October 2026).
 *
 * Few colours: a task's colour (theme.taskSoft) shows as a light tint in a band, and as a line only for a hypothesis
 * that has led; the other hypotheses are thin grey lines.
 */

import type { TaskColours } from "../frame/colours";
import { keyText } from "../frame/robot";
import { taskText } from "../frame/activity";
import { CAUSE_SHORT, TRIGGER_SHORT } from "../frame/robot";
import { theme } from "../theme";
import type { FactLane, HumanLane, Lanes, PairLane, RobotLane } from "./lanes";

export const PAD = 2;          // px: the boxes' outer margin in the canvas
export const LABEL = 84;       // px: the title column inside a box
export const BIG = 156;        // px: the box's right column, for a large number, to the right of the plot area
export const GAP = 10;         // px: between boxes
export const AXIS = 22;        // px: the axis' numbers under the last box
export const ACCENT = 3;       // px: a box's left edge, as the right panel's blocks have
export const RADIUS = 10;

export const BAND = 20;
export const BELIEF = 96;
export const BELIEF_TOP = 11;  // px: the belief's 1 below the row's top, the held admission's strip above it
export const FACT = 16;
export const ROBOT = 24;
export const DISTANCE = 60;
export const ROW_GAP = 4;
export const BOX_PAD = 9;      // px: above and below the rows inside a box
export const SCALE = 4;        // the distance lane reaches SCALE × min_separation; a larger distance at its top

/** A version's proportions: the title column, the right column, the space between and inside boxes, the rows' heights. */
export interface Spec {
  label: number;
  big: number;
  right: number;
  gap: number;
  boxPad: number;
  band: number;
  belief: number;
  fact: number;
  robot: number;
  distance: number;
}

export const SPEC_A: Spec = { label: LABEL, big: BIG, right: 0, gap: GAP, boxPad: BOX_PAD, band: BAND, belief: BELIEF,
                              fact: FACT, robot: ROBOT, distance: DISTANCE };
/** Version B: a card's header column at the left (its title, a large number, a muted line), the plot to its right. */
export const SPEC_B: Spec = { label: 196, big: 0, right: 18, gap: 8, boxPad: 10, band: 28, belief: 92, fact: 18, robot: 32,
                              distance: 62 };

export type Tone = "human" | "recognition" | "planning" | "neutral";

/** A box's fill and its left edge, from the theme, as the right panel's blocks. */
export function toneOf(tone: Tone): { fill: string; edge: string; title: string } {
  const c = theme.color;
  switch (tone) {
    case "human": return { fill: mix(c.humanLight, "#FFFFFF", 0.82), edge: c.humanLight, title: c.humanDark };
    case "recognition": return { fill: mix(c.robotLight, "#FFFFFF", 0.86), edge: c.robotLight, title: c.robotDark };
    case "planning": return { fill: c.page, edge: c.robot, title: c.robotDark };
    case "neutral": return { fill: c.page, edge: c.lineFaint, title: c.inkSoft };
  }
}

export type Row =
  | { kind: "human"; lane: HumanLane; y: number; h: number }
  | { kind: "belief"; lane: RobotLane; y: number; h: number; off: boolean }
  | { kind: "fact"; lane: FactLane; y: number; h: number }
  | { kind: "robot"; lane: RobotLane; y: number; h: number }
  | { kind: "distance"; lane: PairLane; y: number; h: number; minSep: number };

export interface Box {
  title: string;
  tone: Tone;
  y: number;
  h: number;
  rows: Row[];
  /** A row's own name beside it, only where the box holds more than one row (two humans, two robots, two facts). */
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

export function geometry(lanes: Lanes, width: number, spec: Spec = SPEC_A): Geometry {
  const boxes: Box[] = [];
  let y = PAD;
  const box = <T,>(title: string, tone: Tone, elements: readonly T[], height: (e: T) => number,
                   row: (e: T, y: number, h: number) => Row) => {
    if (elements.length === 0) return;
    const rows: Row[] = [];
    let at = y + spec.boxPad;
    for (const e of elements) { const h = height(e); rows.push(row(e, at, h)); at += h + ROW_GAP; }
    const h = at - ROW_GAP + spec.boxPad - y;
    boxes.push({ title, tone, y, h, rows, named: elements.length > 1 });
    y += h + spec.gap;
  };
  box("human", "human", lanes.humans, () => spec.band, (lane, y, h) => ({ kind: "human", lane, y, h }));
  box("belief", "recognition", lanes.robots, (l) => (aware(l) ? spec.belief : spec.band),
      (lane, y, h) => ({ kind: "belief", lane, y, h, off: !aware(lane) }));
  box("context", "neutral", lanes.facts, () => spec.fact, (lane, y, h) => ({ kind: "fact", lane, y, h }));
  box("robot", "planning", lanes.robots, () => spec.robot, (lane, y, h) => ({ kind: "robot", lane, y, h }));
  box("distance", "neutral", lanes.pairs, () => spec.distance, (lane, y, h) => ({
    kind: "distance", lane, y, h, minSep: lanes.robots.find((r) => r.robot.robot === lane.robot)!.robot.min_separation,
  }));
  const axisY = y - spec.gap + 6;
  const x0 = PAD + spec.label;
  return { width, height: axisY + AXIS - 6, boxes, x0, x1: Math.max(x0 + 1, width - PAD - spec.big - spec.right), axisY };
}

function aware(lane: RobotLane): boolean {
  return lane.robot.condition === "intention-aware";
}

/** The x of a tick's left edge, and of its middle, on the axis from 0 to `end`. */
export function xOf(g: Geometry, end: number, t: number): number {
  return g.x0 + (t / end) * (g.x1 - g.x0);
}

/** The tick under an x of the plot area, among the ticks held; null outside it. Both versions' clicks read it. */
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
// The tooltip's rows: the tick's values, short (both versions)
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
