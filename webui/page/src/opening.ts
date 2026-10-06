/**
 * What the page opens on when it is loaded (T-viz 1a; docs/handoffs/plan_T-viz_1a.md, P9, P10 and section 5, "The
 * address"). The server's state wins: a sim-run that has been stepped is shown whatever the address says, locked.
 * Otherwise the address's choice: a complete triple is built, a layout (with a setup) viewed, a domain alone shown with
 * nothing chosen; an address with no choice opens the catalogue's default choice. An address that cannot be read, or
 * that names a scenario or a setup the page does not offer on its layout (P2), opens the default choice and says why.
 * An unknown layout, setup or scenario is the server's to refuse (a BuildFailure), after which the page also opens the
 * default choice.
 */

import { readAddress, type RunOptionValue } from "./address";
import { isOffered, offeredSetups, type Selection } from "./frame/selection";
import type { Catalogue, Current, SimRunChoice, SimRunHistory } from "./gen/messages";

export type Opening =
  | { kind: "current"; run: SimRunHistory }
  | { kind: "choose"; choice: SimRunChoice; options: RunOptionValue[] }
  | { kind: "view"; selection: Selection; options: RunOptionValue[] }
  | { kind: "domain"; selection: Selection; options: RunOptionValue[] }
  | { kind: "default"; problem: string | null };

/** Whether a sim-run has been stepped: its latest tick update is not the start's. */
export function isStepped(run: SimRunHistory): boolean {
  return run.ticks[run.ticks.length - 1].tick !== null;
}

export function opening(catalogue: Catalogue, current: Current, search: string): Opening {
  if (current.state !== null && isStepped(current.state)) return { kind: "current", run: current.state };
  const address = readAddress(search, catalogue);
  if (!address.ok) return { kind: "default", problem: address.problem };
  const { selection, options } = address;
  if (selection === null) return { kind: "default", problem: null };
  if (selection.layout === null) return { kind: "domain", selection, options };
  const domain = catalogue.domains.find((d) => d.name === selection.domain)!;
  if (selection.scenario !== null) {
    const scenario = domain.scenarios.find((s) => s.id === selection.scenario);
    if (scenario && !isOffered(scenario, selection.layout)) {
      return { kind: "default", problem: `scenario ${scenario.id} is not offered on ${selection.layout} (its reference `
        + `layouts: ${scenario.reference_layouts.join(", ")})` };
    }
    return { kind: "choose", options,
             choice: { domain: selection.domain, layout: selection.layout, scenario: selection.scenario, options } };
  }
  if (selection.setup !== null && !offeredSetups(domain, selection.layout).some((s) => s.id === selection.setup)) {
    return { kind: "default", problem: `setup ${selection.setup} is not offered on ${selection.layout}` };
  }
  return { kind: "view", selection, options };
}
