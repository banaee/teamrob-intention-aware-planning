/**
 * The way through the catalogue (T-viz 1a; docs/handoffs/plan_T-viz_1a.md, P2): domain, layout, setup, scenario. The
 * setups offered for a layout are those with at least one scenario that has the layout among its reference layouts;
 * the scenarios offered are the chosen setup's scenarios with that layout among their reference layouts. Every list
 * keeps the catalogue's order. Read from the catalogue's bindings only: nothing here knows a domain.
 */

import type { DomainEntry, ScenarioEntry, SetupEntry } from "../gen/messages";

/** The page's choice as far as it is made. A setup needs a layout; a scenario needs a layout and a setup. */
export interface Selection {
  domain: string;
  layout: string | null;
  setup: string | null;
  scenario: string | null;
}

export function offeredSetups(domain: DomainEntry, layout: string): SetupEntry[] {
  const bound = new Set(domain.scenarios.filter((s) => s.reference_layouts.includes(layout)).map((s) => s.setup));
  return domain.setups.filter((s) => bound.has(s.id));
}

export function offeredScenarios(domain: DomainEntry, layout: string, setup: string): ScenarioEntry[] {
  return domain.scenarios.filter((s) => s.setup === setup && s.reference_layouts.includes(layout));
}

/** Whether a scenario is offered on a layout: the layout is among its reference layouts. */
export function isOffered(scenario: ScenarioEntry, layout: string): boolean {
  return scenario.reference_layouts.includes(layout);
}

/** The plain text filter over a scenario's id and description: every word of the filter appears in them, in any case
 * (P4). An empty filter keeps every scenario. */
export function matchesFilter(scenario: ScenarioEntry, filter: string): boolean {
  const words = filter.toLowerCase().split(/\s+/).filter((w) => w.length > 0);
  const text = `${scenario.id} ${scenario.description}`.toLowerCase();
  return words.every((w) => text.includes(w));
}
