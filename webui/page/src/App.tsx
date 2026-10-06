/**
 * The web-ui's page (T-viz 1a): the frame of the page for the whole of stage 1 (docs/handoffs/plan_T-viz_1a.md,
 * section 5) and the sim-run in the browser.
 *
 *   header          the choice as a path, the lock, the selection panel's button
 *   selection       domain, layout, setup, scenario, run options (open before the first step, folded after it)
 *   main row        panel 4a (the human and the world) | the env-pane with its control bar | panel 4b (the robot's
 *                   mind, stage 1b, a rail in 1a)
 *   panel 4c        plots over ticks (stage 1c), a strip in 1a
 *
 * The page's states (section 5): nothing chosen; a layout's view; a layout and setup's view; a start (unlocked); a
 * sim-run stepped (locked); ended. A layout chosen asks for its view, a setup its view with the setup's objects (P3,
 * P7); a scenario, or a run option changed with a scenario chosen, builds the model and shows its start; the first
 * step locks the choices; reset unlocks them. A choice that cannot be built shows its BuildFailure, and the page stays
 * on what it showed (its controls disabled when the server holds no sim-run for it).
 *
 * The address mirrors the choice (P10; src/address.ts). On loading, the server's state wins: a stepped current
 * sim-run is shown whatever the address says; otherwise the address's choice is opened, or with none the catalogue's
 * default choice (P9); an address that cannot be opened says why and opens the default choice.
 *
 * The page holds no simulation logic and no rule between run options: it asks the server (src/api.ts) and draws the
 * answers. Play requests one step after another; it pauses by itself on the tick at which all agents have finished
 * (the tick update's `run.finished_at`), and step and play go on from there.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { addressOf, readAddress, type RunOptionValue } from "./address";
import { api } from "./api";
import { ControlBar, type Speed } from "./frame/ControlBar";
import { isOffered, offeredSetups, type Selection } from "./frame/selection";
import { SelectionPanel } from "./frame/SelectionPanel";
import type {
  BuildFailure, Catalogue, LayoutView, ScenarioEntry, SimRunChoice, SimRunState, TickUpdate,
} from "./gen/messages";
import type { View } from "./env-pane/camera";
import { EnvPane } from "./env-pane/EnvPane";
import type { Moment, Room } from "./env-pane/Scene";

const DEFAULT_SPEED: Speed = 5;

/** What the env-pane shows: a sim-run (`built` false when the server holds none for it: its choice failed after it
 * was shown), a view of a layout or of a layout and a setup, or nothing. */
type Shown =
  | { kind: "run"; state: SimRunState; built: boolean }
  | { kind: "view"; view: LayoutView }
  | null;

function selectionOf(state: SimRunState): Selection {
  const run = state.description.run;
  return { domain: run.domain, layout: run.layout, setup: run.setup, scenario: run.scenario };
}

export function App() {
  const [catalogue, setCatalogue] = useState<Catalogue | null>(null);
  const [shown, setShown] = useState<Shown>(null);
  const [selection, setSelection] = useState<Selection | null>(null);
  const [options, setOptions] = useState<RunOptionValue[]>([]);
  const [ready, setReady] = useState(false);        // the address is written only once the page has read it
  const [view, setView] = useState<View>("tilted");
  const [speed, setSpeed] = useState<Speed>(DEFAULT_SPEED);
  const [playing, setPlaying] = useState(false);
  const [busy, setBusy] = useState(false);
  const [selectionOpen, setSelectionOpen] = useState(true);
  const [message, setMessage] = useState<string | null>(null);
  const playingRef = useRef(false);
  const speedRef = useRef<Speed>(DEFAULT_SPEED);
  speedRef.current = speed;

  const showRun = useCallback((state: SimRunState) => {
    setShown({ kind: "run", state, built: true });
    setSelection(selectionOf(state));
    setOptions([...state.description.stated.options]);
  }, []);

  /** Builds a choice; its BuildFailure's message, or null when built. */
  const choose = useCallback(async (choice: SimRunChoice): Promise<string | null> => {
    const built = await api.choose(choice);
    if (built.ok) { showRun(built.value); return null; }
    setShown((s) => (s?.kind === "run" ? { ...s, built: false } : s));
    return built.refusal.message;
  }, [showRun]);

  /** Asks for the view of a selection's layout, and setup if one is chosen; why it was not shown, or null. */
  const requestView = useCallback(async (next: Selection): Promise<string | null> => {
    const answer = await api.view({ domain: next.domain, layout: next.layout!, setup: next.setup });
    if (answer.ok) {
      setShown({ kind: "view", view: answer.value });
      setSelection({ ...next, scenario: null });
      return null;
    }
    if (answer.status === 409) return "the choices are locked after the first step: reset first";
    return (answer.refusal as BuildFailure).message;
  }, []);

  /** Opens a selection read from the address with its run options; why it could not be opened, or null. */
  const openSelection = useCallback(async (c: Catalogue, next: Selection, stated: RunOptionValue[]) => {
    const domain = c.domains.find((d) => d.name === next.domain)!;
    if (next.layout === null) { setSelection(next); setShown(null); return null; }
    if (next.scenario !== null) {
      const scenario = domain.scenarios.find((s) => s.id === next.scenario);
      if (scenario && !isOffered(scenario, next.layout)) {
        return `scenario ${scenario.id} is not offered on ${next.layout} (its reference layouts: `
          + `${scenario.reference_layouts.join(", ")})`;
      }
      return choose({ domain: next.domain, layout: next.layout, scenario: next.scenario, options: stated });
    }
    if (next.setup !== null && !offeredSetups(domain, next.layout).some((s) => s.id === next.setup)) {
      return `setup ${next.setup} is not offered on ${next.layout}`;
    }
    return requestView(next);
  }, [choose, requestView]);

  // The start: the catalogue and the server's current state; a stepped sim-run wins; else the address's choice, or
  // the catalogue's default choice.
  useEffect(() => {
    (async () => {
      try {
        const [c, current] = await Promise.all([api.catalogue(), api.current()]);
        setCatalogue(c);
        if (current.state !== null && current.state.tick.tick !== null) {
          showRun(current.state);
          setSelectionOpen(false);
          return;
        }
        const address = readAddress(window.location.search, c);
        let problem: string | null = null;
        if (!address.ok) problem = address.problem;
        else if (address.selection !== null) {
          setOptions(address.options);
          problem = await openSelection(c, address.selection, address.options);
        }
        if (problem !== null) setMessage(`The address's choice was not opened: ${problem}. The default choice is shown.`);
        if (problem !== null || (address.ok && address.selection === null)) {
          const failed = await choose(c.default_choice);
          if (failed !== null) {
            setSelection({ domain: c.default_choice.domain, layout: null, setup: null, scenario: null });
            setOptions([...c.default_choice.options]);
            setMessage(`The default choice was not built: ${failed}`);
          }
        }
      } catch (e) {
        setMessage(`The server does not answer: ${(e as Error).message}`);
      } finally {
        setReady(true);
      }
    })();
  }, [showRun, choose, openSelection]);

  // The address mirrors the choice, without a new entry in the browser's history.
  useEffect(() => {
    if (!ready) return;
    const query = addressOf(selection, options);
    if (query !== window.location.search) window.history.replaceState(null, "", query);
  }, [ready, selection, options]);

  /** A request on the selection: busy while it runs, its problem shown, or the message cleared. */
  const act = useCallback(async (request: () => Promise<string | null>, what: string) => {
    setBusy(true);
    try {
      const problem = await request();
      setMessage(problem === null ? null : `${what}: ${problem}`);
    } finally {
      setBusy(false);
    }
  }, []);

  const onDomain = useCallback((name: string) => {
    if (selection?.domain === name) return;
    setSelection({ domain: name, layout: null, setup: null, scenario: null });
    setShown(null);
    setMessage(null);
  }, [selection]);

  const onLayout = useCallback((layout: string) => {
    if (!selection) return;
    void act(() => requestView({ domain: selection.domain, layout, setup: null, scenario: null }), "Not shown");
  }, [selection, act, requestView]);

  const onSetup = useCallback((setup: string) => {
    if (!selection) return;
    void act(() => requestView({ ...selection, setup, scenario: null }), "Not shown");
  }, [selection, act, requestView]);

  const onScenario = useCallback((scenario: ScenarioEntry) => {
    if (!selection?.layout) return;
    // The run options stay as set when the layout, the setup or the scenario changes (P13).
    void act(() => choose({ domain: selection.domain, layout: selection.layout!, scenario: scenario.id, options }),
             "Not built");
  }, [selection, options, act, choose]);

  const onOption = useCallback((value: RunOptionValue) => {
    const next = options.map((v) => (v.name === value.name ? value : v));
    setOptions(next);
    if (selection?.layout && selection.scenario) {
      void act(() => choose({ domain: selection.domain, layout: selection.layout!, scenario: selection.scenario!,
                              options: next }), "Not built");
    }
  }, [options, selection, act, choose]);

  const run = shown?.kind === "run" ? shown : null;

  const applyTick = useCallback((tick: TickUpdate) => {
    setShown((s) => (s?.kind === "run" && s.state.description.sim_run === tick.sim_run
      ? { ...s, state: { ...s.state, tick } } : s));
  }, []);

  /** One step; null when the server refused it. */
  const stepOnce = useCallback(async (simRun: string): Promise<TickUpdate | null> => {
    const answer = await api.step(simRun);
    if (!answer.ok) {
      setMessage(`Step refused: ${answer.refusal.reason}`);
      return null;
    }
    applyTick(answer.value);
    setSelectionOpen(false);
    return answer.value;
  }, [applyTick]);

  const onStep = useCallback(async () => {
    if (!run) return;
    setBusy(true);
    try { await stepOnce(run.state.description.sim_run); } finally { setBusy(false); }
  }, [run, stepOnce]);

  const onPause = useCallback(() => { playingRef.current = false; setPlaying(false); }, []);

  const onPlay = useCallback(async () => {
    if (!run || playingRef.current) return;
    const simRun = run.state.description.sim_run;
    playingRef.current = true;
    setPlaying(true);
    while (playingRef.current) {
      const started = performance.now();
      const tick = await stepOnce(simRun);
      if (tick === null || tick.end !== null) break;
      if (tick.run.finished_at !== null && tick.run.finished_at === tick.tick) break;   // all agents have finished
      const rate = speedRef.current;
      const wait = rate === 0 ? 0 : 1000 / rate - (performance.now() - started);
      await new Promise((resolve) => (wait > 0 ? setTimeout(resolve, wait) : requestAnimationFrame(resolve)));
    }
    playingRef.current = false;
    setPlaying(false);
  }, [run, stepOnce]);

  const onReset = useCallback(async () => {
    if (!run) return;
    playingRef.current = false;
    setPlaying(false);
    setBusy(true);
    try {
      const answer = await api.reset(run.state.description.sim_run);
      if (answer.ok) { showRun(answer.value); setSelectionOpen(true); setMessage(null); }
      else setMessage(`Reset refused: ${answer.refusal.reason}`);
    } finally {
      setBusy(false);
    }
  }, [run, showRun]);

  const locked = run !== null && run.state.tick.tick !== null;
  const domain = catalogue?.domains.find((d) => d.name === selection?.domain) ?? null;
  const shownDomain = shown === null ? null
    : shown.kind === "run" ? shown.state.description.run.domain : shown.view.domain;
  const appearance = catalogue?.domains.find((d) => d.name === shownDomain)?.appearance ?? null;
  const limitValue = run?.state.description.effective.find((v) => v.kind === "limit");
  const limit = limitValue?.kind === "limit" ? limitValue.value : null;
  const glideMs = playing && speed !== 0 ? 1000 / speed : 0;

  const description = run?.state.description ?? null;
  const tickNow = run?.state.tick ?? null;
  const layoutView = shown?.kind === "view" ? shown.view : null;
  const room = useMemo<Room | null>(() => {
    if (description !== null) return { key: description.sim_run, ...description.world };
    if (layoutView === null) return null;
    return { key: `view ${layoutView.domain} ${layoutView.layout} ${layoutView.setup?.id ?? ""}`,
             space: layoutView.space, areas: layoutView.areas, fixed_objects: layoutView.fixed_objects,
             movable_objects: layoutView.setup?.movable_objects ?? [] };
  }, [description, layoutView]);
  const moment = useMemo<Moment | null>(() => {
    if (tickNow !== null) return tickNow.world;
    if (layoutView === null) return null;
    const setup = layoutView.setup;
    return { humans: [], robots: [], carried: [], fixed_object_contents: setup?.fixed_object_contents ?? [],
             object_states: setup?.object_states ?? [] };
  }, [tickNow, layoutView]);
  const idle = shown?.kind === "run" ? "Not built: change the choice"
    : shown?.kind === "view" && shown.view.setup !== null ? "No sim-run: choose a scenario"
    : "No sim-run: choose a setup, then a scenario";
  const path = selection === null ? [] : [selection.domain, selection.layout, selection.setup, selection.scenario]
    .filter((p): p is string => p !== null);

  return (
    <main className="page">
      <header className="page-header">
        <span className="page-title">TeamRob web-ui</span>
        {path.length > 0 && <span className="page-path">{path.join(" / ")}</span>}
        {locked && <span className="page-lock" title="The choices are locked after the first step; reset unlocks them">locked</span>}
        <button type="button" className="page-toggle" aria-expanded={selectionOpen}
                onClick={() => setSelectionOpen((o) => !o)}>
          {selectionOpen ? "▴" : "▾"} Selection
        </button>
      </header>

      {selectionOpen && catalogue && domain && (
        <SelectionPanel catalogue={catalogue} domain={domain} selection={selection} options={options}
                        effective={run?.built ? run.state.description.effective : null}
                        locked={locked || busy || playing} onDomain={onDomain} onLayout={onLayout}
                        onSetup={onSetup} onScenario={onScenario} onOption={onOption} />
      )}
      {message && <p className="page-message" role="status">{message}</p>}

      <div className="main-row">
        <aside className="panel panel-human" aria-label="The human and the world">
          <h2 className="panel-title"><span className="panel-dot" />The human</h2>
          <p className="panel-later">The action in hand, the stack, the last switches and resumptions: increment (iv).</p>
        </aside>
        {shown && room && moment && appearance ? (
          <EnvPane layout={shown.kind === "run" ? shown.state.description.run.layout : shown.view.layout}
                   room={room} moment={moment} appearance={appearance} view={view} onView={setView} glideMs={glideMs}
                   controls={<ControlBar tick={run?.built ? run.state.tick : null} idle={idle} limit={limit}
                                         playing={playing} busy={busy} speed={speed} onSpeed={setSpeed}
                                         onPlay={onPlay} onPause={onPause} onStep={onStep} onReset={onReset} />} />
        ) : (
          <section className="env-pane env-pane-empty">
            {catalogue ? "Choose a layout" : "Connecting to the server"}
          </section>
        )}
        <aside className="rail" aria-label="The robot's mind">
          <span className="rail-title">The robot's mind · stage 1b</span>
        </aside>
      </div>

      <aside className="strip" aria-label="Plots over ticks">
        <span className="strip-title">Plots over ticks · stage 1c</span>
      </aside>
    </main>
  );
}
