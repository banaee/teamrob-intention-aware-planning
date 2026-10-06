/**
 * What the page opens on (src/opening.ts; plan_T-viz_1a.md, P9, P10, section 5 "The address"): a stepped sim-run on the
 * server wins over the address; else the address's choice; else the default choice; and why an address is not opened.
 */

import { describe, expect, it } from "vitest";

import type { Catalogue, Current, SimRunHistory } from "../src/gen/messages";
import { opening } from "../src/opening";

const scenario = (id: string, setup: string, layouts: string[]) => ({ id, setup, reference_layouts: layouts, description: "" });
const catalogue = {
  domains: [{
    name: "made_up", layouts: [{ id: "room_a", title: "", notes: null }, { id: "room_b", title: "", notes: null }],
    setups: [{ id: "shift_1", notes: null }, { id: "shift_2", notes: null }],
    scenarios: [scenario("run_1", "shift_1", ["room_a"]), scenario("run_2", "shift_2", ["room_b"])], appearance: {},
  }],
  run_options: [{ kind: "switch", name: "aware", default: true, description: "" }],
  default_choice: { domain: "made_up", layout: "room_a", scenario: "run_1",
                    options: [{ kind: "switch", name: "aware", value: true }] },
} as unknown as Catalogue;

const history = (ticks: (number | null)[]) => ({ description: {}, ticks: ticks.map((tick) => ({ tick })) }) as unknown as SimRunHistory;
const none: Current = { state: null, view: null };
const unstepped: Current = { state: history([null]), view: null };
const stepped: Current = { state: history([null, 0, 1]), view: null };
const bookmark = "?domain=made_up&layout=room_b&setup=shift_2&scenario=run_2&aware=false";

describe("the opening", () => {
  it("shows a stepped sim-run on the server whatever the address says", () => {
    expect(opening(catalogue, stepped, bookmark)).toEqual({ kind: "current", run: stepped.state });
  });

  it("builds the address's choice, with its run options, when the server's sim-run is not stepped", () => {
    for (const current of [none, unstepped]) {
      const open = opening(catalogue, current, bookmark);
      expect(open.kind).toBe("choose");
      if (open.kind === "choose") {
        expect(open.choice).toEqual({ domain: "made_up", layout: "room_b", scenario: "run_2",
                                      options: [{ kind: "switch", name: "aware", value: false }] });
      }
    }
  });

  it("views a layout, or a layout and a setup, and shows a domain alone with nothing chosen", () => {
    expect(opening(catalogue, none, "?domain=made_up&layout=room_a").kind).toBe("view");
    expect(opening(catalogue, none, "?domain=made_up&layout=room_a&setup=shift_1").kind).toBe("view");
    expect(opening(catalogue, none, "?domain=made_up").kind).toBe("domain");
  });

  it("opens the default choice without an address, and says why when the address is not offered or not read", () => {
    expect(opening(catalogue, none, "")).toEqual({ kind: "default", problem: null });
    for (const search of ["?domain=made_up&layout=room_a&scenario=run_2",       // run_2 is not offered on room_a
                          "?domain=made_up&layout=room_a&setup=shift_2",        // shift_2 is not offered on room_a
                          "?domain=other", "?domain=made_up&beta=1"]) {
      const open = opening(catalogue, none, search);
      expect(open.kind, search).toBe("default");
      expect(open.kind === "default" && open.problem, search).toBeTruthy();
    }
  });

  it("leaves an unknown scenario to the server", () => {
    expect(opening(catalogue, none, "?domain=made_up&layout=room_a&scenario=run_9").kind).toBe("choose");
  });
});
