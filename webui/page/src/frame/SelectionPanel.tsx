/**
 * The selection panel (T-viz 1a): five columns in the order of the choice, domain, layout, setup, scenario, then the
 * run options. Increment (i) builds the frame with a minimal choice: the domain, and a scenario from the domain's
 * list, on its reference layout; the layout and the setup columns show what the scenario binds, and the run options
 * are shown as stated and in effect, not changeable yet. Increment (ii) fills the columns (docs/handoffs/
 * plan_T-viz_1a.md, section 5).
 *
 * Locked after the first step: the panel is read only until a reset.
 */

import { type ReactNode, useEffect, useRef } from "react";

import type { Catalogue, DomainEntry, RunDescription, ScenarioEntry, SimRunChoice } from "../gen/messages";

type RunOptionDeclaration = Catalogue["run_options"][number];
type RunOptionValue = SimRunChoice["options"][number];

export function SelectionPanel({ catalogue, domain, description, locked, onDomain, onScenario }: {
  catalogue: Catalogue;
  domain: DomainEntry;
  description: RunDescription | null;
  locked: boolean;
  onDomain: (name: string) => void;
  onScenario: (scenario: ScenarioEntry) => void;
}) {
  const run = description?.run ?? null;
  const shown = run !== null && run.domain === domain.name;
  const layout = shown ? domain.layouts.find((l) => l.id === run.layout) : undefined;
  return (
    <section className={`selection${locked ? " is-locked" : ""}`} aria-label="Selection">
      <Column title="Domain">
        {catalogue.domains.map((d) => (
          <button key={d.name} type="button" className="choice" aria-pressed={d.name === domain.name}
                  disabled={locked} onClick={() => onDomain(d.name)}>
            {d.name}
          </button>
        ))}
      </Column>
      <Column title="Layout" note="the scenario's reference layout">
        {layout && <div className="choice is-static" aria-pressed>{layout.id}<small>{layout.title}</small></div>}
      </Column>
      <Column title="Setup" note="the scenario's setup">
        {shown && <div className="choice is-static" aria-pressed>{run.setup}</div>}
      </Column>
      <Column title="Scenario" note={`${domain.scenarios.length} in ${domain.name}`}>
        <ScenarioList scenarios={domain.scenarios} chosen={shown ? run.scenario : null} locked={locked}
                      onScenario={onScenario} />
      </Column>
      <Column title="Run options" note="as stated · in effect">
        {description && <Options declared={catalogue.run_options} stated={description.stated.options}
                                 effective={description.effective} />}
      </Column>
    </section>
  );
}

function Column({ title, note, children }: { title: string; note?: string; children: ReactNode }) {
  return (
    <div className="selection-column">
      <div className="selection-heading">
        <span>{title}</span>
        {note && <small>{note}</small>}
      </div>
      <div className="selection-list">{children}</div>
    </div>
  );
}

function ScenarioList({ scenarios, chosen, locked, onScenario }: {
  scenarios: readonly ScenarioEntry[]; chosen: string | null; locked: boolean; onScenario: (s: ScenarioEntry) => void;
}) {
  const list = useRef<HTMLDivElement>(null);
  useEffect(() => {
    list.current?.querySelector("[aria-pressed='true']")?.scrollIntoView({ block: "nearest" });
  }, [chosen, scenarios]);
  return (
    <div ref={list} className="selection-scroll">
      {scenarios.map((s) => (
        <button key={s.id} type="button" className="choice" aria-pressed={s.id === chosen} disabled={locked}
                onClick={() => onScenario(s)}>
          {s.id}
        </button>
      ))}
    </div>
  );
}

/** Each run option: the value as stated, and the value in effect where the model applied another (an option that
 * another sets off). The page holds no rule between them: the run description's `effective` says it. */
function Options({ declared, stated, effective }: {
  declared: readonly RunOptionDeclaration[]; stated: readonly RunOptionValue[]; effective: readonly RunOptionValue[];
}) {
  return (
    <dl className="options">
      {declared.map((d) => {
        const s = stated.find((v) => v.name === d.name);
        const e = effective.find((v) => v.name === d.name);
        const differs = s !== undefined && e !== undefined && s.value !== e.value;
        return (
          <div key={d.name} className="option" title={d.description}>
            <dt>{d.name}</dt>
            <dd>
              {s === undefined ? "" : shown(s)}
              {differs && <span className="option-effect">{shown(e!)} in effect</span>}
            </dd>
          </div>
        );
      })}
    </dl>
  );
}

function shown(v: RunOptionValue): string {
  switch (v.kind) {
    case "switch": return v.value ? "on" : "off";
    case "limit": return v.value === null ? "none" : String(v.value);
    default: return String(v.value);
  }
}
