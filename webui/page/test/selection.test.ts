/**
 * The way through the catalogue (src/frame/selection.ts; plan_T-viz_1a.md, P2 and P4), on a catalogue made up here:
 * the setups offered for a layout, the scenarios offered for a layout and a setup, the plain text filter.
 */

import { describe, expect, it } from "vitest";

import type { DomainEntry, ScenarioEntry } from "../src/gen/messages";
import { isOffered, matchesFilter, offeredScenarios, offeredSetups, withOption } from "../src/frame/selection";

const scenario = (id: string, setup: string, layouts: string[], description = ""): ScenarioEntry =>
  ({ id, setup, reference_layouts: layouts, description });

const domain = {
  name: "made_up",
  layouts: [{ id: "room_a", title: "A", notes: null }, { id: "room_b", title: "B", notes: null },
            { id: "room_c", title: "C", notes: null }],
  setups: [{ id: "shift_1", notes: null }, { id: "shift_2", notes: "two" }, { id: "shift_3", notes: null }],
  scenarios: [
    scenario("run_1", "shift_2", ["room_a"], "A walk past the Machine"),
    scenario("run_2", "shift_1", ["room_a"], "two tasks"),
    scenario("run_3", "shift_2", ["room_b"]),
    scenario("run_4", "shift_2", ["room_a", "room_b"]),
  ],
  appearance: {},
} as unknown as DomainEntry;

describe("the offer", () => {
  it("offers a layout's setups in the catalogue's order, those with a scenario on it", () => {
    expect(offeredSetups(domain, "room_a").map((s) => s.id)).toEqual(["shift_1", "shift_2"]);
    expect(offeredSetups(domain, "room_b").map((s) => s.id)).toEqual(["shift_2"]);
    expect(offeredSetups(domain, "room_c")).toEqual([]);
  });

  it("offers a setup's scenarios on the layout, in the catalogue's order", () => {
    expect(offeredScenarios(domain, "room_a", "shift_2").map((s) => s.id)).toEqual(["run_1", "run_4"]);
    expect(offeredScenarios(domain, "room_b", "shift_2").map((s) => s.id)).toEqual(["run_3", "run_4"]);
    expect(offeredScenarios(domain, "room_b", "shift_1")).toEqual([]);
  });

  it("offers a scenario only on its reference layouts", () => {
    expect(isOffered(domain.scenarios[0], "room_a")).toBe(true);
    expect(isOffered(domain.scenarios[0], "room_b")).toBe(false);
  });
});

describe("the filter", () => {
  it("keeps a scenario whose id and description hold every word, in any case", () => {
    const [run1, run2] = domain.scenarios;
    expect(matchesFilter(run1, "")).toBe(true);
    expect(matchesFilter(run1, "machine")).toBe(true);
    expect(matchesFilter(run1, "run_1 WALK")).toBe(true);
    expect(matchesFilter(run1, "walk tasks")).toBe(false);
    expect(matchesFilter(run2, "  two  ")).toBe(true);
  });
});

describe("the run options", () => {
  it("change one value at a time and keep the others as set, in their order (P13)", () => {
    const options = [{ kind: "switch", name: "aware", value: true }, { kind: "level", name: "alpha", value: 0.05 }] as const;
    expect(withOption([...options], { kind: "level", name: "alpha", value: 0.1 }))
      .toEqual([{ kind: "switch", name: "aware", value: true }, { kind: "level", name: "alpha", value: 0.1 }]);
  });
});
