/**
 * The page's choice mirrored in the address (T-viz 1a; docs/handoffs/plan_T-viz_1a.md, P10 and section 5, "The
 * address"): the domain, the layout, the setup and the scenario as far as chosen, and every run option's value, as the
 * query of the page's address, e.g. `?domain=…&layout=…&setup=…&scenario=…&<option>=<value>…`. A link reopens a choice
 * at its start, not at a tick; it is not a run file (TODO-189).
 *
 * The run options are read by the kinds the catalogue declares; the page holds no rule between them. A switch is
 * written `true` or `false`, a step limit a whole number or `none`.
 */

import type { Catalogue, SimRunChoice } from "./gen/messages";
import type { Selection } from "./frame/selection";

type RunOptionDeclaration = Catalogue["run_options"][number];
export type RunOptionValue = SimRunChoice["options"][number];

const SELECTION_KEYS = ["domain", "layout", "setup", "scenario"] as const;

/** What an address asks for: a choice as far as made (none: the address names nothing) with every run option's value,
 * or why it cannot be read. */
export type AddressChoice =
  | { ok: true; selection: Selection | null; options: RunOptionValue[] }
  | { ok: false; problem: string };

export function readAddress(search: string, catalogue: Catalogue): AddressChoice {
  const query = new URLSearchParams(search);
  const options = catalogue.default_choice.options.map((v) => ({ ...v }));
  for (const [name, text] of query) {
    if ((SELECTION_KEYS as readonly string[]).includes(name)) continue;
    const declaration = catalogue.run_options.find((d) => d.name === name);
    if (!declaration) return { ok: false, problem: `the address names the run option '${name}', which is not declared` };
    const value = parseValue(declaration, text);
    if (value === undefined) return { ok: false, problem: `the address gives '${name}' the value '${text}'` };
    const index = options.findIndex((v) => v.name === name);
    options[index] = value;
  }
  const domain = query.get("domain");
  if (domain === null) return { ok: true, selection: null, options };
  if (!catalogue.domains.some((d) => d.name === domain)) {
    return { ok: false, problem: `the address names the domain '${domain}', which the catalogue does not hold` };
  }
  const layout = query.get("layout");
  const setup = layout === null ? null : query.get("setup");
  const scenario = layout === null ? null : query.get("scenario");
  return { ok: true, selection: { domain, layout, setup, scenario }, options };
}

function parseValue(declaration: RunOptionDeclaration, text: string): RunOptionValue | undefined {
  const name = declaration.name;
  switch (declaration.kind) {
    case "switch":
      return text === "true" || text === "false" ? { kind: "switch", name, value: text === "true" } : undefined;
    case "one_of":
      return { kind: "one_of", name, value: text };
    case "level": {
      const value = Number(text);
      return text.trim() !== "" && Number.isFinite(value) ? { kind: "level", name, value } : undefined;
    }
    case "limit": {
      if (text === "none") return { kind: "limit", name, value: null };
      const value = Number(text);
      return Number.isInteger(value) ? { kind: "limit", name, value } : undefined;
    }
  }
}

/** The address's query for a choice as far as made, with every run option's value. */
export function addressOf(selection: Selection | null, options: readonly RunOptionValue[]): string {
  const query = new URLSearchParams();
  if (selection !== null) {
    for (const key of SELECTION_KEYS) {
      const value = selection[key];
      if (value !== null) query.set(key, value);
    }
  }
  for (const v of options) query.set(v.name, v.kind === "limit" && v.value === null ? "none" : String(v.value));
  return `?${query.toString()}`;
}
