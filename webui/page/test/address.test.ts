/**
 * The address (src/address.ts; plan_T-viz_1a.md, P10): a choice and its run options written as the address's query
 * and read back; what cannot be read says why.
 */

import { describe, expect, it } from "vitest";

import { addressOf, readAddress } from "../src/address";
import type { Catalogue } from "../src/gen/messages";

const catalogue = {
  domains: [{ name: "made_up", layouts: [], setups: [], scenarios: [], appearance: {} }],
  run_options: [
    { kind: "switch", name: "aware", default: true, description: "" },
    { kind: "one_of", name: "plan", values: ["one", "two"], default: "one", description: "" },
    { kind: "level", name: "alpha", default: 0.05, description: "" },
    { kind: "limit", name: "steps", default: null, minimum: 1, description: "" },
  ],
  default_choice: {
    domain: "made_up", layout: "room_a", scenario: "run_1",
    options: [{ kind: "switch", name: "aware", value: true }, { kind: "one_of", name: "plan", value: "one" },
              { kind: "level", name: "alpha", value: 0.05 }, { kind: "limit", name: "steps", value: null }],
  },
} as unknown as Catalogue;

describe("the address", () => {
  it("reads back what it wrote", () => {
    const selection = { domain: "made_up", layout: "room_a", setup: "shift_1", scenario: "run_1" };
    const options = [{ kind: "switch", name: "aware", value: false }, { kind: "one_of", name: "plan", value: "two" },
                     { kind: "level", name: "alpha", value: 0.1 }, { kind: "limit", name: "steps", value: 40 }] as const;
    const query = addressOf(selection, [...options]);
    expect(query).toBe("?domain=made_up&layout=room_a&setup=shift_1&scenario=run_1&aware=false&plan=two&alpha=0.1&steps=40");
    expect(readAddress(query, catalogue)).toEqual({ ok: true, selection, options: [...options] });
  });

  it("writes a choice as far as made, and no step limit as none", () => {
    const query = addressOf({ domain: "made_up", layout: "room_a", setup: null, scenario: null },
                            catalogue.default_choice.options);
    expect(query).toBe("?domain=made_up&layout=room_a&aware=true&plan=one&alpha=0.05&steps=none");
    const read = readAddress(query, catalogue);
    expect(read.ok && read.selection).toEqual({ domain: "made_up", layout: "room_a", setup: null, scenario: null });
  });

  it("takes the catalogue's defaults for options it does not name, and names nothing without a domain", () => {
    expect(readAddress("", catalogue)).toEqual({ ok: true, selection: null, options: catalogue.default_choice.options });
  });

  it("says why it cannot be read", () => {
    for (const query of ["?domain=other", "?domain=made_up&beta=1", "?domain=made_up&aware=yes",
                         "?domain=made_up&alpha=x", "?domain=made_up&steps=2.5"]) {
      const read = readAddress(query, catalogue);
      expect(read.ok, query).toBe(false);
    }
  });
});
