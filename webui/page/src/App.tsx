/**
 * The web-ui's page (T-viz 1a): the frame of the page for the whole of stage 1 (docs/handoffs/plan_T-viz_1a.md,
 * section 5) and the sim-run in the browser.
 *
 *   header          the choice as a path, the lock, the selection panel's button
 *   selection       domain, layout, setup, scenario, run options (open before the first step, folded after it)
 *   main row        panel 4a (the human and the world) | the env-pane with its control bar | panel 4b (the robot: its
 *                   body and its mind, T-viz 1b)
 *   panel 4c        plots over ticks (T-viz 1c): five lanes on one tick axis (src/plots/PlotPanel.tsx)
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
 * The page holds a sim-run as the sequence of its tick updates (T-viz 1a (iii)): the display places are folded over it
 * (src/env-pane/places.ts), so that a reload, which receives the whole sequence from `current`, keeps the picture.
 * The camera is the screen-user's own: moved freely it stays through the ticks, a reset and a change of scenario on
 * the same layout, and returns to the last preset when the layout changes.
 *
 * The past view (T-viz 1c; Hadi, 7 October 2026, preferred): a click on panel 4c pauses play and shows an earlier tick
 * k; the env-pane and both side panels then read the tick updates up to k (the prefix the page held when the sim-run
 * was at k), the control bar says so, and play or step first returns to the latest tick. No request goes to the
 * server: the sim-run never goes back and its log pair is not touched. One colour per task across the page, fixed
 * from the run description (src/frame/colours.ts).
 *
 * The page holds no simulation logic and no rule between run options: it asks the server (src/api.ts) and draws the
 * answers. Play requests one step after another; it pauses by itself on the tick at which all agents have finished
 * (the tick update's `run.finished_at`), and step and play go on from there.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { addressOf, type RunOptionValue } from "./address";
import { api } from "./api";
import { NO_COLOURS, taskColours } from "./frame/colours";
import { ControlBar, type Speed } from "./frame/ControlBar";
import { type Selection, withOption } from "./frame/selection";
import { HumanPanel } from "./frame/HumanPanel";
import { RobotPanel } from "./frame/RobotPanel";
import { SelectionPanel } from "./frame/SelectionPanel";
import type {
  BuildFailure, Catalogue, LayoutView, RunDescription, ScenarioEntry, SimRunChoice, SimRunHistory, SimRunState,
  TickUpdate,
} from "./gen/messages";
import type { View } from "./env-pane/camera";
import { EnvPane } from "./env-pane/EnvPane";
import { opening } from "./opening";
import { type BookFold, EMPTY_BOOK, foldBook, type PlaceBook } from "./env-pane/places";
import type { Moment, Room } from "./env-pane/Scene";
import { foldLanes, type Lanes } from "./plots/lanes";
import { PlotPanel } from "./plots/PlotPanel";
import { viewedTicks } from "./plots/past";

const DEFAULT_SPEED: Speed = 5;

/** What the env-pane shows: a sim-run with every tick update it gave, the start's first (`built` false when the
 * server holds none for it: its choice failed after it was shown), a view of a layout or of a layout and a setup, or
 * nothing. */
type Shown =
  | { kind: "run"; description: RunDescription; ticks: TickUpdate[]; built: boolean }
  | { kind: "view"; view: LayoutView }
  | null;

function selectionOf(description: RunDescription): Selection {
  const run = description.run;
  return { domain: run.domain, layout: run.layout, setup: run.setup, scenario: run.scenario };
}

const last = (ticks: readonly TickUpdate[]) => ticks[ticks.length - 1];

export function App() {
  const [catalogue, setCatalogue] = useState<Catalogue | null>(null);
  const [shown, setShown] = useState<Shown>(null);
  const [selection, setSelection] = useState<Selection | null>(null);
  const [options, setOptions] = useState<RunOptionValue[]>([]);
  const [ready, setReady] = useState(false);        // the address is written only once the page has read it
  const [view, setView] = useState<View>("tilted");
  const [free, setFree] = useState(false);
  const [speed, setSpeed] = useState<Speed>(DEFAULT_SPEED);
  const [playing, setPlaying] = useState(false);
  const [busy, setBusy] = useState(false);
  const [selectionOpen, setSelectionOpen] = useState(true);
  const [message, setMessage] = useState<string | null>(null);
  const [viewed, setViewed] = useState<number | null>(null);   // an earlier tick shown (the past view), or the latest
  const playingRef = useRef(false);
  const speedRef = useRef<Speed>(DEFAULT_SPEED);
  speedRef.current = speed;

  const showRun = useCallback((run: SimRunState | SimRunHistory) => {
    const ticks = "ticks" in run ? [...run.ticks] : [run.tick];
    setShown({ kind: "run", description: run.description, ticks, built: true });
    setViewed(null);
    setSelection(selectionOf(run.description));
    setOptions([...run.description.stated.options]);
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

  // The start: the catalogue and the server's current state, and what to open on them (src/opening.ts).
  useEffect(() => {
    (async () => {
      try {
        const [c, current] = await Promise.all([api.catalogue(), api.current()]);
        setCatalogue(c);
        const open = opening(c, current, window.location.search);
        let problem: string | null = null;
        switch (open.kind) {
          case "current":
            showRun(open.run);
            setSelectionOpen(false);
            return;
          case "choose":
            setOptions(open.options);
            problem = await choose(open.choice);
            break;
          case "view":
            setOptions(open.options);
            problem = await requestView(open.selection);
            break;
          case "domain":
            setOptions(open.options);
            setSelection(open.selection);
            return;
          case "default":
            problem = open.problem;
        }
        if (open.kind !== "default" && problem === null) return;
        if (problem !== null) setMessage(`The address's choice was not opened: ${problem}. The default choice is shown.`);
        const failed = await choose(c.default_choice);
        if (failed !== null) {
          setSelection({ domain: c.default_choice.domain, layout: null, setup: null, scenario: null });
          setOptions([...c.default_choice.options]);
          setMessage(`The default choice was not built: ${failed}`);
        }
      } catch (e) {
        setMessage(`The server does not answer: ${(e as Error).message}`);
      } finally {
        setReady(true);
      }
    })();
  }, [showRun, choose, requestView]);

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
    const next = withOption(options, value);
    setOptions(next);
    if (selection?.layout && selection.scenario) {
      void act(() => choose({ domain: selection.domain, layout: selection.layout!, scenario: selection.scenario!,
                              options: next }), "Not built");
    }
  }, [options, selection, act, choose]);

  const run = shown?.kind === "run" ? shown : null;

  const applyTick = useCallback((tick: TickUpdate) => {
    setShown((s) => (s?.kind === "run" && s.description.sim_run === tick.sim_run
      ? { ...s, ticks: [...s.ticks, tick] } : s));
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
    setViewed(null);
    setBusy(true);
    try { await stepOnce(run.description.sim_run); } finally { setBusy(false); }
  }, [run, stepOnce]);

  const onPause = useCallback(() => { playingRef.current = false; setPlaying(false); }, []);

  /** The past view: a tick shown, play paused; null returns to the latest tick. */
  const onView = useCallback((tick: number | null) => {
    if (tick !== null) { playingRef.current = false; setPlaying(false); }
    setViewed(tick);
  }, []);

  const onPlay = useCallback(async () => {
    if (!run || playingRef.current) return;
    const simRun = run.description.sim_run;
    setViewed(null);
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
      const answer = await api.reset(run.description.sim_run);
      if (answer.ok) { showRun(answer.value); setSelectionOpen(true); setMessage(null); }
      else setMessage(`Reset refused: ${answer.refusal.reason}`);
    } finally {
      setBusy(false);
    }
  }, [run, showRun]);

  const tickNow = run === null ? null : last(run.ticks);
  // What the env-pane and the side panels read: the tick updates up to the viewed tick, or all of them.
  const shownTicks = useMemo(() => (run === null ? null : viewedTicks(run.ticks, viewed)), [run, viewed]);
  const tickShown = shownTicks === null ? null : last(shownTicks);
  const locked = tickNow !== null && tickNow.tick !== null;
  const domain = catalogue?.domains.find((d) => d.name === selection?.domain) ?? null;
  const shownDomain = shown === null ? null
    : shown.kind === "run" ? shown.description.run.domain : shown.view.domain;
  const appearance = catalogue?.domains.find((d) => d.name === shownDomain)?.appearance ?? null;
  const limitValue = run?.description.effective.find((v) => v.kind === "limit");
  const limit = limitValue?.kind === "limit" ? limitValue.value : null;
  const glideMs = playing && speed !== 0 && viewed === null ? 1000 / speed : 0;

  const description = run?.description ?? null;
  const layoutView = shown?.kind === "view" ? shown.view : null;
  const room = useMemo<Room | null>(() => {
    if (description !== null) return { key: description.sim_run, ...description.world };
    if (layoutView === null) return null;
    return { key: `view ${layoutView.domain} ${layoutView.layout} ${layoutView.setup?.id ?? ""}`,
             space: layoutView.space, areas: layoutView.areas, fixed_objects: layoutView.fixed_objects,
             movable_objects: layoutView.setup?.movable_objects ?? [] };
  }, [description, layoutView]);
  const moment = useMemo<Moment | null>(() => {
    if (tickShown !== null) return tickShown.world;
    if (layoutView === null) return null;
    const setup = layoutView.setup;
    return { humans: [], robots: [], carried: [], fixed_object_contents: setup?.fixed_object_contents ?? [],
             object_states: setup?.object_states ?? [] };
  }, [tickShown, layoutView]);
  // The place book folded over the tick updates, one new tick at a time; anew for another sim-run or view.
  const bookFold = useRef<BookFold | null>(null);
  const book = useMemo<PlaceBook>(() => {
    if (room === null) return EMPTY_BOOK;
    const sequence = run !== null ? run.ticks.map((u) => u.world.fixed_object_contents)
      : [moment?.fixed_object_contents ?? []];
    bookFold.current = foldBook(bookFold.current, room.key, sequence);
    return bookFold.current.book;
  }, [room, run, moment]);
  // In the past view, the place book folded over the prefix: the book the page held when the sim-run was there.
  const bookShown = useMemo<PlaceBook>(() => {
    if (room === null || run === null || viewed === null || shownTicks === null) return book;
    return foldBook(null, room.key, shownTicks.map((u) => u.world.fixed_object_contents)).book;
  }, [room, run, viewed, shownTicks, book]);

  // Panel 4c's lanes, folded one tick update at a time; one colour per task, fixed from the run description.
  const laneFold = useRef<Lanes | null>(null);
  const lanes = useMemo<Lanes | null>(() => {
    if (run === null || !run.built) return null;
    laneFold.current = foldLanes(laneFold.current, run.description, run.ticks);
    return laneFold.current;
  }, [run]);
  const colours = useMemo(() => (description === null ? NO_COLOURS : taskColours(description)), [description]);

  // The camera returns to the last preset when the layout changes.
  const shownLayout = shown === null ? null : shown.kind === "run" ? shown.description.run.layout : shown.view.layout;
  useEffect(() => setFree(false), [shownLayout]);

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
                        effective={run?.built ? run.description.effective : null}
                        locked={locked || busy || playing} onDomain={onDomain} onLayout={onLayout}
                        onSetup={onSetup} onScenario={onScenario} onOption={onOption} />
      )}
      {message && <p className="page-message" role="status">{message}</p>}

      <div className="main-row">
        <HumanPanel humans={run?.description.world.humans.map((h) => h.id) ?? []}
                    scripts={run?.description.world.scripts ?? []} ticks={run?.built ? shownTicks : null}
                    colours={colours} />
        {shown && room && moment && appearance ? (
          <EnvPane layout={shownLayout!} room={room} moment={moment} book={bookShown} appearance={appearance} view={view}
                   free={free} onView={(v) => { setView(v); setFree(false); }} onFree={() => setFree(true)}
                   glideMs={glideMs}
                   controls={<ControlBar tick={run?.built ? tickNow : null} idle={idle} limit={limit}
                                         viewed={run?.built ? viewed : null} onLatest={() => setViewed(null)}
                                         playing={playing} busy={busy} speed={speed} onSpeed={setSpeed}
                                         onPlay={onPlay} onPause={onPause} onStep={onStep} onReset={onReset} />} />
        ) : (
          <section className="env-pane env-pane-empty">
            {catalogue ? "Choose a layout" : "Connecting to the server"}
          </section>
        )}
        <RobotPanel robots={run?.description.robots ?? []} ticks={run?.built ? shownTicks : null} colours={colours} />
      </div>

      <PlotPanel lanes={lanes} colours={colours} viewed={viewed} onView={onView} />
    </main>
  );
}
