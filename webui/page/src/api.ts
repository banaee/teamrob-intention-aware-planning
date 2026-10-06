/**
 * The page's requests to the web-ui's server (webui/server.py, T-viz 1a): plain request and response, JSON, the
 * messages of webui/messages.py. The server holds every rule; the page only asks and draws the answers.
 */

import type {
  BuildFailure, Catalogue, Current, LayoutView, SimRunChoice, SimRunState, StepRefusal, TickUpdate, ViewChoice,
  ViewRefusal,
} from "./gen/messages";

/** An answer: the message asked for, or the refusal the server gave instead. */
export type Answer<T, R> = { ok: true; value: T } | { ok: false; status: number; refusal: R };

const BASE = "/api/";

async function ask<T, R>(path: string, body?: unknown): Promise<Answer<T, R>> {
  const response = await fetch(BASE + path, body === undefined ? undefined : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  });
  if (response.ok) return { ok: true, value: (await response.json()) as T };
  if (response.status === 409 || response.status === 422) {
    return { ok: false, status: response.status, refusal: (await response.json()) as R };
  }
  throw new Error(`${path}: ${response.status} ${await response.text()}`);
}

async function get<T>(path: string): Promise<T> {
  const answer = await ask<T, never>(path);
  if (!answer.ok) throw new Error(`${path}: refused`);
  return answer.value;
}

export const api = {
  catalogue: () => get<Catalogue>("catalogue"),
  current: () => get<Current>("current"),
  choose: (choice: SimRunChoice) => ask<SimRunState, BuildFailure>("choose", choice),
  /** The view of a layout, or of a layout and a setup: 422 BuildFailure, 409 ViewRefusal (a stepped sim-run). */
  view: (choice: ViewChoice) => ask<LayoutView, BuildFailure | ViewRefusal>("view", choice),
  step: (simRun: string) => ask<TickUpdate, StepRefusal>("step", { sim_run: simRun }),
  reset: (simRun: string) => ask<SimRunState, StepRefusal>("reset", { sim_run: simRun }),
};
