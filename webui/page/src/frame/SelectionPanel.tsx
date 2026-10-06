/**
 * The selection panel (T-viz 1a): five columns in the order of the choice, domain, layout, setup, scenario (P2,
 * src/frame/selection.ts), then the run options. A layout and a setup show their notes in two lines; a scenario its
 * description in two lines, the whole of it when chosen; a plain text filter and the count over the scenarios (P4).
 * The run options are edited by their declared kinds (a switch, one of a list, a level, a step limit that reads
 * "none" when empty), each with its value in effect beside it where the model applied another (the run description's
 * `effective`; the page holds no rule between options). They stay as set when the layout, the setup or the scenario
 * changes (P13).
 *
 * Locked after the first step: the panel is read only until a reset.
 */

import { type KeyboardEvent, type ReactNode, useEffect, useRef, useState } from "react";

import type { RunOptionValue } from "../address";
import type { Catalogue, DomainEntry, ScenarioEntry } from "../gen/messages";
import { matchesFilter, offeredScenarios, offeredSetups, type Selection } from "./selection";

type RunOptionDeclaration = Catalogue["run_options"][number];

export function SelectionPanel({ catalogue, domain, selection, options, effective, locked, onDomain, onLayout,
  onSetup, onScenario, onOption }: {
  catalogue: Catalogue;
  domain: DomainEntry;
  selection: Selection | null;
  options: readonly RunOptionValue[];
  effective: readonly RunOptionValue[] | null;
  locked: boolean;
  onDomain: (name: string) => void;
  onLayout: (id: string) => void;
  onSetup: (id: string) => void;
  onScenario: (scenario: ScenarioEntry) => void;
  onOption: (value: RunOptionValue) => void;
}) {
  const [filter, setFilter] = useState("");
  const layout = selection?.layout ?? null;
  const setup = selection?.setup ?? null;
  const setups = layout === null ? [] : offeredSetups(domain, layout);
  const scenarios = layout === null || setup === null ? [] : offeredScenarios(domain, layout, setup);
  const shownScenarios = scenarios.filter((s) => s.id === selection?.scenario || matchesFilter(s, filter));
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
      <Column title="Layout" note={`${domain.layouts.length}`}>
        <Scrolled chosen={layout}>
          {domain.layouts.map((l) => (
            <Choice key={l.id} id={l.id} text={l.notes} chosen={l.id === layout} whole={false} disabled={locked}
                    onClick={() => onLayout(l.id)} />
          ))}
        </Scrolled>
      </Column>
      <Column title="Setup" note={layout === null ? "after a layout" : `${setups.length} on ${layout}`}>
        <Scrolled chosen={setup}>
          {setups.map((s) => (
            <Choice key={s.id} id={s.id} text={s.notes} chosen={s.id === setup} whole={false} disabled={locked}
                    onClick={() => onSetup(s.id)} />
          ))}
        </Scrolled>
      </Column>
      <Column title="Scenario" note={setup === null ? "after a setup" : `${shownScenarios.length} of ${scenarios.length}`}>
        {setup !== null && (
          <input className="selection-filter" type="search" placeholder="filter by id or description" value={filter}
                 aria-label="Filter the scenarios" onChange={(e) => setFilter(e.target.value)} />
        )}
        <Scrolled chosen={selection?.scenario ?? null}>
          {shownScenarios.map((s) => (
            <Choice key={s.id} id={s.id} text={s.description} chosen={s.id === selection?.scenario} whole
                    disabled={locked} onClick={() => onScenario(s)} />
          ))}
        </Scrolled>
      </Column>
      <Column title="Run options" note={effective === null ? "as stated" : "as stated · in effect"}>
        <dl className="options">
          {catalogue.run_options.map((d) => {
            const stated = options.find((v) => v.name === d.name);
            const inEffect = effective?.find((v) => v.name === d.name);
            const differs = stated !== undefined && inEffect !== undefined && stated.value !== inEffect.value;
            return (
              <div key={d.name} className="option" title={d.description}>
                <dt>{d.name}</dt>
                <dd>
                  {stated !== undefined && <OptionEditor declaration={d} value={stated} disabled={locked}
                                                         onChange={onOption} />}
                  {differs && <span className="option-effect">{shown(inEffect!)} in effect</span>}
                </dd>
              </div>
            );
          })}
        </dl>
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

/** A scrolling list that brings its chosen entry into view. */
function Scrolled({ chosen, children }: { chosen: string | null; children: ReactNode }) {
  const list = useRef<HTMLDivElement>(null);
  useEffect(() => {
    list.current?.querySelector("[aria-pressed='true']")?.scrollIntoView({ block: "nearest" });
  }, [chosen]);
  return <div ref={list} className="selection-scroll">{children}</div>;
}

/** An entry of a list: its id and its text, in two lines, or the whole text when it is chosen and `whole`. */
function Choice({ id, text, chosen, whole, disabled, onClick }: {
  id: string; text: string | null; chosen: boolean; whole: boolean; disabled: boolean; onClick: () => void;
}) {
  return (
    <button type="button" className="choice" aria-pressed={chosen} disabled={disabled} onClick={onClick}
            title={text ?? undefined}>
      {id}
      {text && <small className={chosen && whole ? "choice-text is-whole" : "choice-text"}>{text}</small>}
    </button>
  );
}

/** One run option's editor, by its declared kind. A number is taken when the field is left or Enter is pressed; text
 * that is not a number of the option's kind is not taken, and the field returns to the value stated. Whether a number
 * is in the option's range is the simulator's to say (a BuildFailure). */
function OptionEditor({ declaration, value, disabled, onChange }: {
  declaration: RunOptionDeclaration; value: RunOptionValue; disabled: boolean; onChange: (v: RunOptionValue) => void;
}) {
  const name = declaration.name;
  switch (declaration.kind) {
    case "switch": {
      const on = value.value === true;
      return (
        <button type="button" className="option-switch" aria-pressed={on} disabled={disabled}
                onClick={() => onChange({ kind: "switch", name, value: !on })}>
          {on ? "on" : "off"}
        </button>
      );
    }
    case "one_of":
      return (
        <select value={String(value.value)} disabled={disabled} aria-label={name}
                onChange={(e) => onChange({ kind: "one_of", name, value: e.target.value })}>
          {declaration.values.map((v) => <option key={v} value={v}>{v}</option>)}
        </select>
      );
    case "level":
      return <NumberField text={String(value.value)} placeholder="" step="0.01" min={undefined} disabled={disabled}
                          name={name}
                          onCommit={(t) => {
                            const v = Number(t);
                            if (t !== "" && Number.isFinite(v)) onChange({ kind: "level", name, value: v });
                          }} />;
    case "limit":
      return <NumberField text={value.value === null ? "" : String(value.value)} placeholder="none" step="1"
                          min={declaration.minimum} disabled={disabled} name={name}
                          onCommit={(t) => {
                            const v = Number(t);
                            if (t === "" || Number.isInteger(v)) onChange({ kind: "limit", name, value: t === "" ? null : v });
                          }} />;
  }
}

function NumberField({ text, placeholder, step, min, disabled, name, onCommit }: {
  text: string; placeholder: string; step: string; min: number | undefined; disabled: boolean; name: string;
  onCommit: (text: string) => void;
}) {
  const [draft, setDraft] = useState(text);
  useEffect(() => setDraft(text), [text]);
  const commit = () => {
    if (draft.trim() !== text) onCommit(draft.trim());
    setDraft(text);
  };
  return (
    <input className="option-number" type="number" value={draft} placeholder={placeholder} step={step} min={min}
           disabled={disabled} aria-label={name} onChange={(e) => setDraft(e.target.value)} onBlur={commit}
           onKeyDown={(e: KeyboardEvent<HTMLInputElement>) => { if (e.key === "Enter") commit(); }} />
  );
}

function shown(v: RunOptionValue): string {
  switch (v.kind) {
    case "switch": return v.value ? "on" : "off";
    case "limit": return v.value === null ? "none" : String(v.value);
    default: return String(v.value);
  }
}
