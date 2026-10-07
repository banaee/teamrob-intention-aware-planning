/**
 * What lies ahead of the agents (T-viz 1d and 1e; Hadi, 7 October 2026, preferred), read from a tick update for the
 * scene: the human's walks ahead (a world fact the robot does not know), each robot's own walks ahead and the part of its
 * last decision's projection of the human still ahead, with that projection's kind. The simulator's side derives every
 * segment; this module only turns them into what the scene draws: the points of a dashed line and the triangles of a
 * stripe on the floor. It computes no path.
 */

import type { HumanWalks, MovingSegment, StationarySegment, TickUpdate, Walk } from "../gen/messages";

export type ProjectedPart = MovingSegment | StationarySegment;

/** The robot's expectation of the human: the projection its last decision rests on, by kind, its parts still ahead. */
export interface Expectation {
  kind: "admitted" | "fallback";
  parts: readonly ProjectedPart[];
}

export interface RobotAhead {
  robot: string;
  walks: readonly Walk[];
  expectation: Expectation | null;
}

export interface Ahead {
  humans: readonly HumanWalks[];
  robots: readonly RobotAhead[];
}

export const NO_AHEAD: Ahead = { humans: [], robots: [] };

/** What lies ahead at the tick of `update`. No expectation where the decision rests on no projection, or nothing of it
 * lies ahead (past its end); before the first decision, none. */
export function aheadOf(update: TickUpdate): Ahead {
  return {
    humans: update.world.walks_ahead,
    robots: update.robots.map((r) => {
      const kind = r.decision?.projection.kind;
      const expectation = (kind === "admitted" || kind === "fallback") && r.projection_ahead.length > 0
        ? { kind, parts: r.projection_ahead } : null;
      return { robot: r.robot, walks: r.walks_ahead, expectation };
    }),
  };
}

/** Which of the three drawings are shown: the robot's plan, the human's real path, the robot's expectation. */
export interface PathsShown {
  plan: boolean;
  path: boolean;
  expectation: boolean;
}

const SHOWN_KEY = "tviz.pathsShown";
export const ALL_SHOWN: PathsShown = { plan: true, path: true, expectation: true };

type Store = Pick<Storage, "getItem" | "setItem">;

/** The switches as the screen-user left them in this browser; every one on where nothing is remembered. */
export function readShown(store: Store | null = globalStore()): PathsShown {
  try {
    const saved = JSON.parse(store?.getItem(SHOWN_KEY) ?? "null") as Partial<PathsShown> | null;
    const read = (key: keyof PathsShown) => (typeof saved?.[key] === "boolean" ? saved[key] : ALL_SHOWN[key]);
    return { plan: read("plan"), path: read("path"), expectation: read("expectation") };
  } catch {
    return ALL_SHOWN;
  }
}

export function saveShown(shown: PathsShown, store: Store | null = globalStore()): void {
  try { store?.setItem(SHOWN_KEY, JSON.stringify(shown)); } catch { /* kept for the page's life only */ }
}

function globalStore(): Store | null {
  try { return typeof window === "undefined" ? null : window.localStorage; } catch { return null; }
}

export type XY = [number, number];

/** The points of the line through `walks`, from the far end back to the agent: a dashed line's dashes are counted from
 * its first point, so they stay where they are on the floor while the agent walks and the line shortens. */
export function linePoints(walks: readonly Walk[]): XY[] {
  if (walks.length === 0) return [];
  return [...walks.map((w): XY => [w.end.x, w.end.y]).reverse(), [walks[0].start.x, walks[0].start.y]];
}

/** The triangles of a stripe on the floor, as x, y pairs per corner: per moving segment a band of `width` along it with
 * a round end at each side; per stationary segment a disc of `standRadius` at its place. The pieces overlap; the scene
 * draws each pixel of them once. */
export function stripeTriangles(parts: readonly ProjectedPart[], width: number, standRadius: number,
                                arc = 28): Float32Array {
  const out: number[] = [];
  const disc = (x: number, y: number, r: number) => {
    for (let i = 0; i < arc; i++) {
      const a0 = (2 * Math.PI * i) / arc;
      const a1 = (2 * Math.PI * (i + 1)) / arc;
      out.push(x, y, x + r * Math.cos(a0), y + r * Math.sin(a0), x + r * Math.cos(a1), y + r * Math.sin(a1));
    }
  };
  const half = width / 2;
  for (const p of parts) {
    if (p.kind === "stationary") {
      disc(p.position.x, p.position.y, standRadius);
      continue;
    }
    const { x: x0, y: y0 } = p.start;
    const { x: x1, y: y1 } = p.end;
    const length = Math.hypot(x1 - x0, y1 - y0);
    if (length > 0) {
      const nx = (-(y1 - y0) / length) * half;
      const ny = ((x1 - x0) / length) * half;
      out.push(x0 + nx, y0 + ny, x0 - nx, y0 - ny, x1 - nx, y1 - ny);
      out.push(x0 + nx, y0 + ny, x1 - nx, y1 - ny, x1 + nx, y1 + ny);
    }
    disc(x0, y0, half);
    disc(x1, y1, half);
  }
  return new Float32Array(out);
}
