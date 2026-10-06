/**
 * The look by state (src/env-pane/look.ts; plan_T-viz_1a.md, section 4, "An object's state changes its shape"): the first look whose state holds for
 * the object replaces its type's look; a type with no entry takes the default.
 */

import { describe, expect, it } from "vitest";

import type { Appearance } from "../src/gen/messages";
import { fixedLook, heldBy, movableLook, statesHeld } from "../src/env-pane/look";

const appearance = {
  fixed: {
    frame: { shape: "barrier", height: 130, presence: "background",
             states: [{ state: "raised", look: { shape: "barrier", height: 8, presence: "background" } }] },
  },
  movable: {
    load: { shape: "loaded_skid", height: 40, states: [
      { state: "bare", look: { shape: "skid", height: 14 } },
      { state: "marked", look: { shape: "crate", height: 20 } }] },
  },
  default_fixed: { shape: "block", height: 60, presence: "background" },
  default_movable: { shape: "crate", height: 20 },
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
