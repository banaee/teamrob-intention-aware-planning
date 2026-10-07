// T-viz 1c: panel 4c's bands, its tick axis in fixed portions, and one colour per task fixed from the run description.

import { describe, expect, it } from "vitest";

import { colourOf, taskColours } from "../src/frame/colours";
import type { RunDescription } from "../src/gen/messages";
import { axisEnd, bands } from "../src/plots/lanes";
import { theme } from "../src/theme";

describe("bands", () => {
  it("are runs of one value, null values forming none", () => {
    const v = ["a", "a", null, "a", "b", "b", null];
    expect(bands(v, v.length, (x, y) => x === y)).toEqual([
      { start: 0, end: 1, value: "a" }, { start: 3, end: 3, value: "a" }, { start: 4, end: 5, value: "b" },
    ]);
  });
  it("read only up to the length given", () => {
    expect(bands(["a", "a", "a"], 2, (x, y) => x === y)).toEqual([{ start: 0, end: 1, value: "a" }]);
  });
});

describe("the tick axis", () => {
  it("extends in fixed portions of 100 ticks", () => {
    expect([0, 1, 100, 101, 250, 2000].map(axisEnd)).toEqual([100, 100, 100, 200, 300, 2000]);
  });
});

const task = (identity: string) => ({ task: "t", bindings: [], label: identity, identity });

describe("one colour per task", () => {
  const description = {
    world: {
      scripts: [{
        human: "h", dependence: "independent",
        entries: [{ task: task("x(1)"), events: [{ trigger: { kind: "now" }, decision: { kind: "start", task: task("y()") } }] },
                  { task: task("x(2)"), events: [] }],
        repeatable: [{ task: task("y()") }],
        closing: [{ task: task("z()"), events: [] }],
      }],
    },
    robots: [{ assigned: [task("x(3)")], hypotheses: Array.from({ length: 12 }, (_, i) => ({ key: `x(${i})`, task: "x", bindings: [] })) }],
  } as unknown as RunDescription;
  const colours = taskColours(description);

  it("in the script's order, then the robot's tasks, then the hypotheses", () => {
    expect([...colours.keys()].slice(0, 6)).toEqual(["x(1)", "y()", "x(2)", "z()", "x(3)", "x(0)"]);
    expect(colours.get("x(1)")).toBe(theme.task[0]);
    expect(colours.get("x(3)")).toBe(theme.task[4]);
  });
  it("one hue per task for the first ten, the neutral grey after them and for a task not named", () => {
    const hues = [...colours.values()];
    expect(new Set(hues.slice(0, 10)).size).toBe(10);
    expect(hues.slice(10).every((h) => h === theme.taskOther)).toBe(true);
    expect(colourOf(colours, "unknown()")).toBe(theme.taskOther);
  });
});

// Both versions' clicks map a pointer's x to a tick by one function over the version's geometry (src/plots/look.ts).
import { geometry, SPEC_A, SPEC_B, tickOf, xOf } from "../src/plots/look";
import type { Lanes } from "../src/plots/lanes";

describe("a click maps to its tick in both versions", () => {
  const lanes = { key: "k", length: 137, humans: [], robots: [], facts: [], pairs: [] } as unknown as Lanes;
  for (const [name, spec] of [["A", SPEC_A], ["B", SPEC_B]] as const) {
    it(`version ${name}`, () => {
      const g = geometry(lanes, 1888, spec);
      const end = axisEnd(lanes.length);
      for (let t = 0; t < lanes.length; t++) expect(tickOf(g, end, lanes.length, xOf(g, end, t + 0.5))).toBe(t);
      expect(tickOf(g, end, lanes.length, g.x0 - 1)).toBeNull();
      expect(tickOf(g, end, lanes.length, g.x1 - 1)).toBe(lanes.length - 1);   // past the latest tick: the latest
    });
  }
});
