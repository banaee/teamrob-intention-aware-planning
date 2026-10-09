/**
 * The look by state (src/env-pane/look.ts; plan_T-viz_1a.md, section 4, "An object's state changes its shape"): the first look whose state holds for
 * the object replaces its type's look; a type with no entry takes the default.
 */

import { describe, expect, it } from "vitest";

import type { Appearance } from "../src/gen/messages";
import { drawnSize, fixedLook, heldBy, movableLook, statesHeld } from "../src/env-pane/look";

const appearance = {
  fixed: {
    frame: { shape: "barrier", height: 130, presence: "background",
             states: [{ state: "raised", look: { shape: "barrier", height: 8, presence: "background" } }] },
  },
  movable: {
    load: { shape: "loaded_skid", height: 40, tint: "ink", footprint_scale: 0.5,
            subtype_tints: { warm_kind: "tan", cool_kind: "slate" }, states: [
      { state: "bare", look: { shape: "skid", height: 14, tint: "pale_wood" } },
      { state: "marked", look: { shape: "crate", height: 20, tint: "ink" } }] },
  },
  default_fixed: { shape: "block", height: 60, presence: "background" },
  default_movable: { shape: "crate", height: 20, tint: "ink" },
} as unknown as Appearance;

describe("the look by state", () => {
  const held = statesHeld([
    { state: "raised", object: "frame_1" }, { state: "bare", object: "load_1" }, { state: "marked", object: "load_1" },
    { state: "marked", object: "load_2" }, { state: "warm", object: null }]);

  it("takes the first listed state that holds for the object", () => {
    expect(fixedLook(appearance, "frame", heldBy(held, "frame_1")).height).toBe(8);
    expect(movableLook(appearance, "load", heldBy(held, "load_1")).shape).toBe("skid");
    expect(movableLook(appearance, "load", heldBy(held, "load_2")).shape).toBe("crate");
  });

  it("keeps the type's look when no listed state holds, and the default for a type with no entry", () => {
    expect(fixedLook(appearance, "frame", heldBy(held, "frame_2")).height).toBe(130);
    expect(movableLook(appearance, "load", heldBy(held, "load_3")).shape).toBe("loaded_skid");
    expect(fixedLook(appearance, "unknown", heldBy(held, "frame_1"))).toEqual(appearance.default_fixed);
  });
});

describe("the tint and the drawn footprint", () => {
  const held = statesHeld([{ state: "bare", object: "load_1" }]);

  it("takes the type's tint for the subtype, the type's tint for another subtype or none", () => {
    expect(movableLook(appearance, "load", heldBy(held, "load_2"), "warm_kind").tint).toBe("tan");
    expect(movableLook(appearance, "load", heldBy(held, "load_2"), "cool_kind").tint).toBe("slate");
    expect(movableLook(appearance, "load", heldBy(held, "load_2"), "other_kind").tint).toBe("ink");
    expect(movableLook(appearance, "load", heldBy(held, "load_2"), null).tint).toBe("ink");
  });

  it("takes a look by state's tint whatever the subtype", () => {
    expect(movableLook(appearance, "load", heldBy(held, "load_1"), "warm_kind").tint).toBe("pale_wood");
  });

  it("draws the footprint at the type's share, a type with no entry at its size", () => {
    expect(drawnSize(appearance, "load", { x: 80, y: 120 })).toEqual({ x: 40, y: 60 });
    expect(drawnSize(appearance, "unknown", { x: 80, y: 120 })).toEqual({ x: 80, y: 120 });
  });
});
