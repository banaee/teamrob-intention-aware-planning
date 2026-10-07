/**
 * The control bar at the env-pane's foot (T-viz 1a): reset, step, play and pause, the speed, and the tick. The tick is
 * the run log's number of the step executed, so a moment seen here is found in the log; beside it the steps done, of
 * the step limit when one is set. It states when all agents have finished (the tick update's `run.finished_at`) and
 * why a sim-run ended. In the past view (T-viz 1c) it states the tick shown beside the sim-run's latest, with a button
 * back to the latest; step and play also return to it first (App.tsx). It holds no rule: what the server answers
 * decides what is shown. Without a sim-run (a view of a
 * layout, or a choice that was not built) every control is disabled and the bar says why (`idle`).
 */

import type { EndReason, TickUpdate } from "../gen/messages";

/** Ticks per second during play; 0: as fast as the server answers. */
export const SPEEDS = [1, 2, 5, 10, 20, 0] as const;
export type Speed = (typeof SPEEDS)[number];

const END_WORDS: Record<EndReason, string> = {
  steps_reached: "the step limit reached",
  reset: "reset",
  choice_changed: "the choice changed",
  server_stopped: "the server stopped",
};

export function ControlBar({ tick, idle, limit, viewed, onLatest, playing, busy, speed, onSpeed, onPlay, onPause, onStep,
                             onReset }: {
  tick: TickUpdate | null;
  idle: string;
  limit: number | null;
  viewed: number | null;
  onLatest: () => void;
  playing: boolean;
  busy: boolean;
  speed: Speed;
  onSpeed: (speed: Speed) => void;
  onPlay: () => void;
  onPause: () => void;
  onStep: () => void;
  onReset: () => void;
}) {
  if (tick === null) {
    return (
      <footer className="control-bar">
        <div className="control-buttons">
          <button type="button" disabled><Icon d={RESET} /> Reset</button>
          <button type="button" disabled><Icon d={STEP} /> Step</button>
          <button type="button" className="control-main" disabled><Icon d={PLAY} /> Play</button>
        </div>
        <div className="control-state"><span className="control-steps">{idle}</span></div>
      </footer>
    );
  }
  const ended = tick.end !== null;
  const done = tick.tick === null ? 0 : tick.tick + 1;
  const finished = tick.run.finished_at;
  return (
    <footer className="control-bar">
      <div className="control-buttons">
        <button type="button" onClick={onReset} disabled={busy || tick.tick === null} title="Reset: back to the start">
          <Icon d={RESET} /> Reset
        </button>
        <button type="button" onClick={onStep} disabled={busy || playing || ended} title="One step">
          <Icon d={STEP} /> Step
        </button>
        {playing ? (
          <button type="button" className="control-main" onClick={onPause} title="Pause">
            <Icon d="M2 1h3v10H2zM7 1h3v10H7z" /> Pause
          </button>
        ) : (
          <button type="button" className="control-main" onClick={onPlay} disabled={busy || ended} title="Play">
            <Icon d={PLAY} /> Play
          </button>
        )}
        <label className="control-speed">
          <select value={speed} onChange={(e) => onSpeed(Number(e.target.value) as Speed)} aria-label="Speed">
            {SPEEDS.map((s) => <option key={s} value={s}>{s === 0 ? "as fast as possible" : `${s} ticks/s`}</option>)}
          </select>
        </label>
      </div>
      <div className="control-state">
        {viewed !== null && (
          <span className="control-past" role="status">
            viewing tick {viewed} · sim-run at tick {tick.tick}
            <button type="button" onClick={onLatest} title="Back to the latest tick">latest</button>
          </span>
        )}
        {viewed === null && finished !== null && <span className="control-note">All agents have finished at tick {finished}</span>}
        {viewed === null && ended && <span className="control-note control-ended">Ended at tick {tick.tick}: {END_WORDS[tick.end!.reason]}</span>}
        {viewed === null && <span className="control-tick">
          {tick.tick === null ? "start" : `tick ${tick.tick}`}
          <span className="control-steps">
            {" · "}{done}{limit === null ? "" : ` of ${limit}`} steps
          </span>
        </span>}
        {limit !== null && (
          <span className="control-progress" aria-hidden>
            <span style={{ width: `${Math.min(100, (100 * done) / limit)}%` }} />
          </span>
        )}
      </div>
    </footer>
  );
}

const RESET = "M6 1.5a4.5 4.5 0 1 1-4.3 5.8h1.6A3 3 0 1 0 6 3v1.8L3 2.3 6 0z";
const STEP = "M1 1l6 5-6 5zM8.5 1H11v10H8.5z";
const PLAY = "M2 1l9 5-9 5z";

/** A control's glyph, drawn on a 12 x 12 grid in the text's colour. */
function Icon({ d }: { d: string }) {
  return <svg className="control-icon" viewBox="0 0 12 12" aria-hidden><path d={d} /></svg>;
}
