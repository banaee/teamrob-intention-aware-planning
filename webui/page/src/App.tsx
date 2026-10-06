/**
 * The web-ui's page (T-viz 1a, increment (i)): the frame of the page for the whole of stage 1 (docs/handoffs/
 * plan_T-viz_1a.md, section 5) and the first sim-run in the browser.
 *
 *   header          the choice as a path, the lock, the selection panel's button
 *   selection       domain, layout, setup, scenario, run options (open before the first step, folded after it)
 *   main row        panel 4a (the human and the world) | the env-pane with its control bar | panel 4b (the robot's
 *                   mind, stage 1b, a rail in 1a)
 *   panel 4c        plots over ticks (stage 1c), a strip in 1a
 *
 * The page holds no simulation logic and no rule between run options: it asks the server (src/api.ts) and draws the
 * answers. Every choice that completes a triple builds the model and the env-pane shows its start; the first step
 * locks the choices; reset unlocks them. Play requests one step after another; it pauses by itself on the tick at which
 * all agents have finished (the tick update's `run.finished_at`), and step and play go on from there.
 */

import { useCallback, useEffect, useRef, useState } from "react";

import { api } from "./api";
import { ControlBar, type Speed } from "./frame/ControlBar";
import { SelectionPanel } from "./frame/SelectionPanel";
import type { Catalogue, ScenarioEntry, SimRunChoice, SimRunState, TickUpdate } from "./gen/messages";
import type { View } from "./env-pane/camera";
import { EnvPane } from "./env-pane/EnvPane";

const DEFAULT_SPEED: Speed = 5;

export function App() {
  const [catalogue, setCatalogue] = useState<Catalogue | null>(null);
  const [run, setRun] = useState<SimRunState | null>(null);
  const [domainName, setDomainName] = useState<string | null>(null);
  const [view, setView] = useState<View>("tilted");
  const [speed, setSpeed] = useState<Speed>(DEFAULT_SPEED);
  const [playing, setPlaying] = useState(false);
  const [busy, setBusy] = useState(false);
  const [selectionOpen, setSelectionOpen] = useState(true);
  const [message, setMessage] = useState<string | null>(null);
  const playingRef = useRef(false);
  const speedRef = useRef<Speed>(DEFAULT_SPEED);
  speedRef.current = speed;

  const show = useCallback((state: SimRunState) => {
    setRun(state);
    setDomainName(state.description.run.domain);
  }, []);

  // The start: the catalogue, then the server's current sim-run, or the default choice built.
  useEffect(() => {
    (async () => {
      try {
        const [c, current] = await Promise.all([api.catalogue(), api.current()]);
        setCatalogue(c);
        if (current.state !== null) {
          show(current.state);
          if (current.state.tick.tick !== null) setSelectionOpen(false);
          return;
        }
        const built = await api.choose(c.default_choice);
        if (built.ok) show(built.value);
        else { setDomainName(c.default_choice.domain); setMessage(built.refusal.message); }
      } catch (e) {
        setMessage(`The server does not answer: ${(e as Error).message}`);
      }
    })();
  }, [show]);

  const choose = useCallback(async (choice: SimRunChoice) => {
    setBusy(true);
    try {
      const built = await api.choose(choice);
      if (built.ok) { show(built.value); setMessage(null); }
      else setMessage(`Not built: ${built.refusal.message}`);
    } finally {
      setBusy(false);
    }
  }, [show]);

  const onScenario = useCallback((scenario: ScenarioEntry) => {
    if (!catalogue || !domainName) return;
    // The run options stay as set when the scenario changes (P13).
    const options = run?.description.stated.options ?? catalogue.default_choice.options;
    void choose({ domain: domainName, layout: scenario.reference_layouts[0], scenario: scenario.id, options });
  }, [catalogue, domainName, run, choose]);

  const applyTick = useCallback((tick: TickUpdate) => {
    setRun((r) => (r && r.description.sim_run === tick.sim_run ? { ...r, tick } : r));
  }, []);

  /** One step; false when the server refused it or the sim-run ended. */
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
    try { await stepOnce(run.description.sim_run); } finally { setBusy(false); }
  }, [run, stepOnce]);

  const onPause = useCallback(() => { playingRef.current = false; setPlaying(false); }, []);

  const onPlay = useCallback(async () => {
    if (!run || playingRef.current) return;
    const simRun = run.description.sim_run;
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
      if (answer.ok) { show(answer.value); setSelectionOpen(true); setMessage(null); }
      else setMessage(`Reset refused: ${answer.refusal.reason}`);
    } finally {
      setBusy(false);
    }
  }, [run, show]);

  const locked = run !== null && run.tick.tick !== null;
  const domain = catalogue?.domains.find((d) => d.name === domainName) ?? null;
  const runDomain = catalogue?.domains.find((d) => d.name === run?.description.run.domain) ?? null;
  const limitValue = run?.description.effective.find((v) => v.kind === "limit");
  const limit = limitValue?.kind === "limit" ? limitValue.value : null;
  const glideMs = playing && speed !== 0 ? 1000 / speed : 0;

  return (
    <main className="page">
      <header className="page-header">
        <span className="page-title">TeamRob web-ui</span>
        {run && (
          <span className="page-path">
            {[run.description.run.domain, run.description.run.layout, run.description.run.setup,
              run.description.run.scenario].join(" / ")}
          </span>
        )}
        {locked && <span className="page-lock" title="The choices are locked after the first step; reset unlocks them">locked</span>}
        <button type="button" className="page-toggle" aria-expanded={selectionOpen}
                onClick={() => setSelectionOpen((o) => !o)}>
          {selectionOpen ? "▴" : "▾"} Selection
        </button>
      </header>

      {selectionOpen && catalogue && domain && (
        <SelectionPanel catalogue={catalogue} domain={domain} description={run?.description ?? null}
                        locked={locked || busy || playing} onDomain={setDomainName} onScenario={onScenario} />
      )}
      {message && <p className="page-message" role="status">{message}</p>}

      <div className="main-row">
        <aside className="panel panel-human" aria-label="The human and the world">
          <h2 className="panel-title"><span className="panel-dot" />The human</h2>
          <p className="panel-later">The action in hand, the stack, the last switches and resumptions: increment (iv).</p>
        </aside>
        {run && runDomain ? (
          <EnvPane description={run.description} tick={run.tick} appearance={runDomain.appearance} view={view}
                   onView={setView} glideMs={glideMs}
                   controls={<ControlBar tick={run.tick} limit={limit} playing={playing} busy={busy} speed={speed}
                                         onSpeed={setSpeed} onPlay={onPlay} onPause={onPause} onStep={onStep}
                                         onReset={onReset} />} />
        ) : (
          <section className="env-pane env-pane-empty">{catalogue ? "No sim-run chosen" : "Connecting to the server"}</section>
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
