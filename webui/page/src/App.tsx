/**
 * The web-ui's page. Stage 0.3: the env-pane alone, drawing an exported sample (src/data.ts). The sample and the view
 * are named in the address (?sample=<name>&view=tilted|top), so a view can be shared and screenshotted.
 */

import { useEffect, useState } from "react";

import { loadIndex, loadSample, type Sample, type SampleEntry } from "./data";
import type { View } from "./env-pane/camera";
import { EnvPane } from "./env-pane/EnvPane";

function fromAddress(): { sample: string | null; view: View } {
  const params = new URLSearchParams(window.location.search);
  return { sample: params.get("sample"), view: params.get("view") === "top" ? "top" : "tilted" };
}

function toAddress(sample: string, view: View): void {
  const params = new URLSearchParams({ sample, view });
  window.history.replaceState(null, "", `?${params}`);
}

export function App() {
  const [entries, setEntries] = useState<SampleEntry[] | null>(null);
  const [name, setName] = useState<string | null>(fromAddress().sample);
  const [view, setView] = useState<View>(fromAddress().view);
  const [sample, setSample] = useState<Sample | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadIndex().then(setEntries).catch((e: Error) => setError(
      `No samples (${e.message}). Write them first: PYTHONHASHSEED=0 python -m mesa_sim.webui_export`));
  }, []);

  const entry = entries?.find((e) => e.name === name) ?? entries?.[0] ?? null;

  useEffect(() => {
    if (!entry) return;
    toAddress(entry.name, view);
    if (sample?.entry.name === entry.name) return;
    loadSample(entry).then(setSample).catch((e: Error) => setError(e.message));
  }, [entry, view, sample]);

  return (
    <main className="page">
      <header className="page-header">
        <span className="page-title">TeamRob web-ui</span>
        <span className="page-note">stage 0.3 · the style trial · the start of a sim-run, from saved messages</span>
        {entries && entries.length > 1 && (
          <label className="page-choice">
            Sample
            <select value={entry?.name ?? ""} onChange={(e) => setName(e.target.value)}>
              {entries.map((e) => <option key={e.name} value={e.name}>{e.domain} · {e.scenario}</option>)}
            </select>
          </label>
        )}
      </header>
      {error && <p className="page-error">{error}</p>}
      {sample && sample.entry.name === entry?.name && (
        <EnvPane description={sample.description} tick={sample.tick} appearance={sample.appearance}
                 view={view} onView={setView} />
      )}
    </main>
  );
}
