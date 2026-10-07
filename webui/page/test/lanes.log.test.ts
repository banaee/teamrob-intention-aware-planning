// T-viz 1c: the lanes the page reads (src/plots/lanes.ts) equal the run log's values at every tick. The sim-runs and
// their logs' values are written by tests/test_tviz_plots.py into the folder TVIZ_LANES_CASES names; run alone, without
// it, this file has nothing to compare and is skipped.

import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

import { describe, expect, it } from "vitest";

import type { RunDescription, TickUpdate } from "../src/gen/messages";
import { foldBook } from "../src/env-pane/places";
import { foldLanes, humanBands, robotBands, trueBands, type Lanes } from "../src/plots/lanes";
import { viewedTicks } from "../src/plots/past";

interface Expected {
  human: Record<string, { task: string | null; tag: string | null }>;
  belief: Record<string, { leader: string; confidence: string; live: string[] } | null>;
  held: Record<string, string | null>;
  decision: Record<string, { trigger: string; cause: string | null } | null>;
  task: Record<string, string | null>;
  hold: Record<string, boolean>;
  facts: Record<string, string[]>;
  fact_rows: string[];
  separation: Record<string, { distance: string; minimum: string; below: boolean | null } | null>;
}

interface Case {
  name: string;
  description: RunDescription;
  ticks: TickUpdate[];
  expected: Expected;
}

const dir = process.env.TVIZ_LANES_CASES;
const cases: Case[] = dir === undefined ? [] : readdirSync(dir).filter((f) => f.endsWith(".json")).sort()
  .map((f) => JSON.parse(readFileSync(join(dir, f), "utf8")) as Case);

/** Every band's ticks hold its one value, and the bands cover exactly the ticks with a value. */
function covered(bandsOf: { start: number; end: number }[], has: (t: number) => boolean, length: number): void {
  const inBand = new Set<number>();
  for (const b of bandsOf) for (let t = b.start; t <= b.end; t++) inBand.add(t);
  for (let t = 0; t < length; t++) expect(inBand.has(t), `tick ${t}`).toBe(has(t));
}

describe.skipIf(cases.length === 0)("the lanes are the run log's", () => {
  for (const c of cases) {
    it(c.name, () => {
      // folded one tick update at a time, as during play
      let lanes: Lanes | null = null;
      for (let i = 1; i <= c.ticks.length; i++) lanes = foldLanes(lanes, c.description, c.ticks.slice(0, i));
      const all = lanes!;
      expect(all.length).toBe(c.ticks.length - 1);
      const e = c.expected;
      const [human] = all.humans;
      const [robot] = all.robots;
      const [pair] = all.pairs;
      expect(all.facts.map((f) => f.fact).sort()).toEqual(e.fact_rows);
      for (let t = 0; t < all.length; t++) {
        const k = String(t);
        const at = `${c.name}, tick ${t}`;
        // (1) the human's task and its tag
        expect(human.task[t]?.label ?? null, at).toBe(e.human[k].task);
        expect(human.tag[t]?.tag ?? null, at).toBe(e.human[k].tag);
        // (2) the belief: the live hypotheses, the leader and its confidence; what the robot holds
        const b = robot.belief[t];
        const ir = e.belief[k];
        if (ir === null) expect(b, at).toBeNull();
        else {
          expect(b, at).not.toBeNull();
          expect(b!.live.map((h) => h.key).sort(), at).toEqual(ir.live);
          expect(b!.leader, at).toBe(ir.leader);
          expect(b!.live.find((h) => h.key === b!.leader)!.belief.toFixed(3), at).toBe(ir.confidence);
          expect(b!.live.reduce((s, h) => s + h.belief, 0), at).toBeCloseTo(1, 9);
        }
        expect(robot.held[t], at).toBe(e.held[k]);
        // (3) context
        expect(all.facts.filter((f) => f.holds[t]).map((f) => f.fact).sort(), at).toEqual(e.facts[k]);
        // (4) the robot's task, its holds, its decisions
        expect(robot.task[t]?.task ?? null, at).toBe(e.task[k]);
        expect(robot.hold[t], at).toBe(e.hold[k]);
        const d = robot.decision[t];
        const trig = e.decision[k];
        if (trig === null) expect(d, at).toBeNull();
        else expect(d === null ? null : { trigger: d.trigger, cause: d.cause }, at).toEqual(trig);
        // (5) the distance
        const s = pair.separation[t];
        const sep = e.separation[k];
        expect(s === null ? null : [s.distance.toFixed(2), s.minimum.toFixed(2)], at)
          .toEqual(sep === null ? null : [sep.distance, sep.minimum]);
        if (sep !== null && sep.below !== null) expect(s!.below, at).toBe(sep.below);
      }
      // folded at once, the same lanes
      const once = foldLanes(null, c.description, c.ticks);
      expect(JSON.stringify({ ...once, robots: once.robots.map((r) => ({ ...r, leaders: [...r.leaders] })) }))
        .toBe(JSON.stringify({ ...all, robots: all.robots.map((r) => ({ ...r, leaders: [...r.leaders] })) }));
      // the view of tick k is what the page held when the sim-run was at tick k: the same tick updates, and the place
      // book folded over them equals the one the page had folded one update at a time
      for (const k of [0, Math.floor(all.length / 3), Math.floor((2 * all.length) / 3), all.length - 1]) {
        const heldAtK = c.ticks.slice(0, k + 2);
        const shown = viewedTicks(c.ticks, k);
        expect(shown).toEqual(heldAtK);
        expect(shown[shown.length - 1].tick).toBe(k);
        let book = null;
        for (let i = 1; i <= heldAtK.length; i++) {
          book = foldBook(book, "run", heldAtK.slice(0, i).map((u) => u.world.fixed_object_contents));
        }
        const past = foldBook(null, "run", shown.map((u) => u.world.fixed_object_contents));
        expect([...past.book].map(([f, m]) => [f, [...m]])).toEqual([...book!.book].map(([f, m]) => [f, [...m]]));
      }
      expect(viewedTicks(c.ticks, null)).toBe(c.ticks);
      // the bands drawn cover the ticks with a value
      covered(humanBands(human, all.length), (t) => human.task[t] !== null, all.length);
      covered(robotBands(robot, all.length), (t) => robot.task[t] !== null, all.length);
      covered(trueBands(robot.hold, all.length), (t) => robot.hold[t], all.length);
      for (const f of all.facts) covered(trueBands(f.holds, all.length), (t) => f.holds[t], all.length);
    });
  }
});
