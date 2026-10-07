/**
 * The paths on the floor (src/env-pane/paths.ts, T-viz 1d and 1e): what the scene reads of a tick update, the points of
 * a dashed line, the stripe's triangles, and the switches' memory. The segments themselves are the simulator's side's
 * (tests/test_tviz_paths.py checks them against the run).
 */

import { describe, expect, it } from "vitest";

import type { MovingSegment, StationarySegment, TickUpdate, Walk } from "../src/gen/messages";
import { ALL_SHOWN, aheadOf, linePoints, readShown, saveShown, stripeTriangles } from "../src/env-pane/paths";

const p = (x: number, y: number) => ({ x, y });
const walk = (sx: number, sy: number, ex: number, ey: number, target = "t"): Walk =>
  ({ start: p(sx, sy), end: p(ex, ey), target });
const moving = (sx: number, sy: number, ex: number, ey: number, until: number): MovingSegment =>
  ({ kind: "moving", start: p(sx, sy), end: p(ex, ey), until });
const stand = (x: number, y: number, until: number): StationarySegment => ({ kind: "stationary", position: p(x, y), until });

function update(robot: Partial<TickUpdate["robots"][number]>, kind: "admitted" | "fallback" | "none" | null): TickUpdate {
  const projection = kind === "admitted" ? { kind, hypothesis: "h", plan: [], until: 40 }
    : kind === "fallback" ? { kind, mode: "moving" as const, span: 4, until: 40 }
    : { kind: "none" as const, reason: "no_human" as const };
  return {
    sim_run: "s", tick: 12, run: { finished_at: null }, end: null,
    world: { humans: [], robots: [], fixed_object_contents: [], carried: [], object_states: [], timeline_facts: [],
             activity: [], separations: [], walks_ahead: [{ human: "h0", walks: [walk(0, 0, 100, 0)] }] },
    robots: [{
      robot: "r0", body: { task: null, action: null, microaction: null, hold: null, finished: false },
      belief: null, gate_answer: "clears",
      decision: kind === null ? null : { tick: 10, trigger: "no_current_task", cause: null, gate_answer: "clears",
                                         projection, change: "starts", chosen: null, hold: 0, queue: [] },
      walks_ahead: [], projection_ahead: [], ...robot,
    }],
  } as TickUpdate;
}

describe("what the scene reads of a tick update", () => {
  it("takes the human's walks from the world and the robot's from its section", () => {
    const ahead = aheadOf(update({ walks_ahead: [walk(5, 5, 50, 5)] }, null));
    expect(ahead.humans).toEqual([{ human: "h0", walks: [walk(0, 0, 100, 0)] }]);
    expect(ahead.robots[0].walks).toEqual([walk(5, 5, 50, 5)]);
    expect(ahead.robots[0].expectation).toBeNull();
  });

  it("gives the expectation the kind of the projection the last decision rests on", () => {
    const parts = [moving(0, 0, 10, 0, 20), stand(10, 0, 23)];
    expect(aheadOf(update({ projection_ahead: parts }, "admitted")).robots[0].expectation).toEqual({ kind: "admitted", parts });
    expect(aheadOf(update({ projection_ahead: parts }, "fallback")).robots[0].expectation).toEqual({ kind: "fallback", parts });
  });

  it("has no expectation with no projection, or past its end", () => {
    expect(aheadOf(update({}, "none")).robots[0].expectation).toBeNull();
    expect(aheadOf(update({ projection_ahead: [] }, "admitted")).robots[0].expectation).toBeNull();
  });
});

describe("the dashed line", () => {
  it("runs from the far end back to the agent, through every walk's end", () => {
    expect(linePoints([walk(0, 0, 10, 0), walk(10, 0, 10, 20)])).toEqual([[10, 20], [10, 0], [0, 0]]);
    expect(linePoints([])).toEqual([]);
  });
});

describe("the stripe", () => {
  const inside = (tris: Float32Array, x: number, y: number) => {
    for (let i = 0; i < tris.length; i += 6) {
      const [ax, ay, bx, by, cx, cy] = Array.from(tris.slice(i, i + 6));
      const d1 = (x - bx) * (ay - by) - (ax - bx) * (y - by);
      const d2 = (x - cx) * (by - cy) - (bx - cx) * (y - cy);
      const d3 = (x - ax) * (cy - ay) - (cx - ax) * (y - ay);
      if (!((d1 < 0 || d2 < 0 || d3 < 0) && (d1 > 0 || d2 > 0 || d3 > 0))) return true;
    }
    return false;
  };

  it("covers a band of its width along a moving segment, with round ends", () => {
    const tris = stripeTriangles([moving(0, 0, 100, 0, 10)], 40, 30);
    expect(tris.length % 6).toBe(0);
    expect(inside(tris, 50, 19)).toBe(true);
    expect(inside(tris, 50, 21)).toBe(false);
    expect(inside(tris, -19, 0)).toBe(true);     // the round end at the start
    expect(inside(tris, 119, 0)).toBe(true);     // and at the end
    expect(inside(tris, 119, 15)).toBe(false);
  });

  it("draws a stand as a disc of its radius at its place", () => {
    const tris = stripeTriangles([stand(200, 50, 10)], 40, 30);
    expect(inside(tris, 200, 79)).toBe(true);
    expect(inside(tris, 200, 81)).toBe(false);
    expect(inside(tris, 0, 0)).toBe(false);
  });
});

describe("the switches' memory", () => {
  const store = () => {
    const held = new Map<string, string>();
    return { getItem: (k: string) => held.get(k) ?? null, setItem: (k: string, v: string) => void held.set(k, v) };
  };

  it("shows every drawing where nothing is remembered, and what was left otherwise", () => {
    const s = store();
    expect(readShown(s)).toEqual(ALL_SHOWN);
    saveShown({ plan: true, path: false, expectation: true }, s);
    expect(readShown(s)).toEqual({ plan: true, path: false, expectation: true });
  });

  it("reads a damaged memory as every drawing shown", () => {
    const s = store();
    s.setItem("tviz.pathsShown", "{not json");
    expect(readShown(s)).toEqual(ALL_SHOWN);
    s.setItem("tviz.pathsShown", JSON.stringify({ plan: "no" }));
    expect(readShown(s)).toEqual(ALL_SHOWN);
    expect(readShown(null)).toEqual(ALL_SHOWN);
  });
});
