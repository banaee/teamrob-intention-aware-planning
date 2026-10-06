/**
 * The page's input in stage 0.3: a sample's three files, exported by mesa_sim/webui_export.py into public/samples/
 * (the run description, the start tick update, the domain's scene appearance). Stage 1a reads the same messages from
 * the server instead.
 */

import type { Appearance, RunDescription, TickUpdate } from "./gen/messages";

export interface SampleEntry {
  name: string;
  domain: string;
  layout: string;
  setup: string;
  scenario: string;
}

export interface Sample {
  entry: SampleEntry;
  description: RunDescription;
  tick: TickUpdate;
  appearance: Appearance;
}

const BASE = `${import.meta.env.BASE_URL}samples/`;

async function json<T>(path: string): Promise<T> {
  const response = await fetch(BASE + path);
  if (!response.ok) throw new Error(`${path}: ${response.status} ${response.statusText}`);
  return (await response.json()) as T;
}

export function loadIndex(): Promise<SampleEntry[]> {
  return json<SampleEntry[]>("index.json");
}

export async function loadSample(entry: SampleEntry): Promise<Sample> {
  const [description, tick, appearance] = await Promise.all([
    json<RunDescription>(`${entry.name}/run_description.json`),
    json<TickUpdate>(`${entry.name}/tick_update.json`),
    json<Appearance>(`${entry.name}/appearance.json`),
  ]);
  return { entry, description, tick, appearance };
}
