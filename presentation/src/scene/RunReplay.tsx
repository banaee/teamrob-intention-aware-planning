/**
 * A recorded sim-run replayed on a slide (scripts/record_run.py), drawn by the env-pane's own Scene: the agents, the
 * movable objects, and on the floor the robot's plan (dashed blue), the human's real path (dashed orange) and the
 * robot's projection of the human (a blue stripe, filled from her intention, hatched from her motion), exactly as the
 * web-ui draws a tick update. Nothing is computed here: every position and every segment is the recording's.
 *
 * Stepped by clicks: each step of the slide is a stop (a tick and a caption); a click plays the ticks up to the next
 * stop at a calm pace, the agents gliding between ticks as the web-ui's play does, and going back jumps. The tick
 * shown stands in a corner, in ticks.
 *
 * `hideHumans`: the human is not drawn, nor her path (talk stage 1, the robot alone: a human-unaware sim-run, in which the
 * robot's mind receives no human; flagged in the report).
 *
 * `mind`: what the robot's mind holds at the tick, beside the scene (MindPanel.tsx; the overall revision, point F).
 * `tickNote`: the first replay says once what a tick is. The agents' id labels (the env-pane's pills, "robot_0") are
 * hidden on slides by the deck's stylesheet: the slides call them the robot and the human.
 *
 * The canvas renders only while its slide is the current one (R3F's frameloop "never" otherwise), so that the replays
 * kept mounted do not load the page while another slide runs; while the replay plays toward a stop it marks itself
 * busy (`data-busy`), which the PDF export and the click-through wait for.
 */

import { Canvas, useThree } from "@react-three/fiber";
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";

import { FramingCamera } from "../../../webui/page/src/env-pane/camera";
import { setPixelRatio } from "../../../webui/page/src/env-pane/material";
import { aheadOf, ALL_SHOWN } from "../../../webui/page/src/env-pane/paths";
import { foldBook } from "../../../webui/page/src/env-pane/places";
import { type Moment, type Room, Scene } from "../../../webui/page/src/env-pane/Scene";
import type {
  Appearance, RobotDescription, RunTriple, TickUpdate, WorldDescription,
} from "../../../webui/page/src/gen/messages";
import { useSlideCurrent, useSlideNear, useSlideSteps } from "../slides/kit";
import { type MindParts, MindPanel } from "./MindPanel";

export interface RecordedRun {
  name: string;
  run_file: string;
  appearance: Appearance;
  run: RunTriple;
  sim_run: string;
  world: Pick<WorldDescription, "space" | "areas" | "fixed_objects" | "movable_objects" | "scripts">;
  robots: Pick<RobotDescription, "robot" | "condition" | "assigned" | "hypotheses" | "theta">[];
  ticks: TickUpdate[];     // cut to what the slide draws (record_run.py, cut); read as tick updates
}

export interface Stop { tick: number; caption: string }

const TICK_MS = 140;    // the pace between stops: about seven ticks a second (a replay may set its own, `tickMs`),
const MOVE_MAX_MS = 4000;   // and faster where a move would take longer than this

/** `step`: the index of the stop the slide shows (0: the first). */
export function RunReplay({ recorded, stops, step, hideHumans = false, mind, tickNote = false, tickMs = TICK_MS }: {
  recorded: RecordedRun; stops: Stop[]; step: number; hideHumans?: boolean; mind?: MindParts; tickNote?: boolean;
  tickMs?: number;
}) {
  // Mounted when the slide first comes near and then kept: the env-pane's Scene places the agents' labels as DOM
  // elements beside its canvas, and removing the canvas while the deck runs throws (a React removeChild error). The
  // web-ui never removes its scene during a sim-run; the deck keeps it too, at the cost of one WebGL context per
  // replay seen (six at most).
  const nearNow = useSlideNear();
  const current = useSlideCurrent();
  const [near, setNear] = useState(nearNow);
  useEffect(() => { if (nearNow) setNear(true); }, [nearNow]);
  const first = recorded.ticks[0].tick!;
  const index = (tick: number) => Math.max(0, Math.min(recorded.ticks.length - 1, tick - first));
  const target = index(stops[Math.min(step, stops.length - 1)].tick);
  const [shown, setShown] = useState(target);
  const from = useRef(shown);
  from.current = shown;
  const [pace, setPace] = useState(tickMs);
  useEffect(() => {
    if (target <= from.current) { setShown(target); return; }      // back, or no move: jump
    const ms = Math.max(30, Math.min(tickMs, MOVE_MAX_MS / (target - from.current)));
    setPace(ms);
    const id = setInterval(() => setShown((s) => {
      if (s + 1 >= target) { clearInterval(id); return target; }
      return s + 1;
    }), ms);
    return () => clearInterval(id);
  }, [target, tickMs]);

  const update = recorded.ticks[shown];
  const room = useMemo<Room>(() => ({ key: recorded.sim_run, ...recorded.world }), [recorded]);
  const moment = useMemo<Moment>(() => {
    const w = update.world;
    return hideHumans ? { ...w, humans: [] } : w;
  }, [update, hideHumans]);
  const ahead = useMemo(() => {
    const a = aheadOf(update);
    return hideHumans ? { humans: [], robots: a.robots.map((r) => ({ ...r, expectation: null })) } : a;
  }, [update, hideHumans]);
  const book = useMemo(() => foldBook(null, room.key,
    recorded.ticks.slice(0, shown + 1).map((u) => u.world.fixed_object_contents)).book, [recorded, room, shown]);
  // The caption of the last stop the replay has reached: it changes when the replay arrives, not when it sets off.
  const caption = [...stops].reverse().find((st) => index(st.tick) <= shown)?.caption ?? stops[0].caption;
  const tallest = Math.max(recorded.appearance.human.height, recorded.appearance.robot.height,
    recorded.appearance.default_fixed.height, ...Object.values(recorded.appearance.fixed).map((l) => l.height));

  return (
    <div className={`replay${mind !== undefined ? " with-mind" : ""}`} data-busy={shown !== target ? "true" : undefined}>
      <div className="replay-main">
      <div className="replay-scene">
        {near && (
          <Canvas orthographic flat dpr={[1, 2]} gl={{ antialias: true, stencil: true }}
                  frameloop={current ? "always" : "never"}>
            <PixelRatio />
            <FramingCamera view="tilted" free={false} onFree={() => {}} bounds={room.space.bounds} height={tallest} />
            <Scene room={room} moment={moment} book={book} appearance={recorded.appearance}
                   glideMs={target > shown ? pace : 0} ahead={ahead} shown={ALL_SHOWN} />
          </Canvas>
        )}
        <div className="replay-tick">tick {update.tick}{tickNote && <small>one tick: one time step</small>}</div>
      </div>
      {mind !== undefined && <MindPanel recorded={recorded} shown={shown} parts={mind} />}
      </div>
      <p className="replay-caption">{caption}</p>
    </div>
  );
}

/** The hatching's spacing in device pixels, as the env-pane sets it. */
function PixelRatio() {
  const dpr = useThree((state) => state.viewport.dpr);
  useLayoutEffect(() => setPixelRatio(dpr), [dpr]);
  return null;
}

/** A replay with its steps: one hidden step marker per stop after the first. */
export function ReplayView({ recorded, stops, hideHumans = false, mind, tickNote, tickMs }: {
  recorded: RecordedRun; stops: Stop[]; hideHumans?: boolean; mind?: MindParts; tickNote?: boolean; tickMs?: number;
}) {
  const step = useSlideSteps(".step-stop");
  return (
    <>
      <RunReplay recorded={recorded} stops={stops} step={step} hideHumans={hideHumans} mind={mind} tickNote={tickNote}
                 tickMs={tickMs} />
      {stops.slice(1).map((s) => <span key={s.tick} className="fragment step-marker step-stop" aria-hidden />)}
    </>
  );
}
