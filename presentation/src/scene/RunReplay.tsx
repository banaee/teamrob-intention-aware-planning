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
 * `hideHumans`: the human is not drawn, nor her path (talk stage 1, Anton alone: a human-unaware sim-run, in which the
 * robot's mind receives no human; flagged in the report).
 */

import { Canvas, useThree } from "@react-three/fiber";
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";

import { FramingCamera } from "../../../webui/page/src/env-pane/camera";
import { setPixelRatio } from "../../../webui/page/src/env-pane/material";
import { aheadOf, ALL_SHOWN } from "../../../webui/page/src/env-pane/paths";
import { foldBook } from "../../../webui/page/src/env-pane/places";
import { type Moment, type Room, Scene } from "../../../webui/page/src/env-pane/Scene";
import type { Appearance, RunTriple, TickUpdate, WorldDescription } from "../../../webui/page/src/gen/messages";
import { useSlideNear, useSlideSteps } from "../slides/kit";

export interface RecordedRun {
  name: string;
  run_file: string;
  appearance: Appearance;
  run: RunTriple;
  sim_run: string;
  world: Pick<WorldDescription, "space" | "areas" | "fixed_objects" | "movable_objects">;
  ticks: TickUpdate[];     // cut to what the slide draws (record_run.py, cut); read as tick updates
}

export interface Stop { tick: number; caption: string }

const TICK_MS = 140;    // the pace between stops: about seven ticks a second,
const MOVE_MAX_MS = 4000;   // and faster where a move would take longer than this

/** `step`: the index of the stop the slide shows (0: the first). */
export function RunReplay({ recorded, stops, step, hideHumans = false }: {
  recorded: RecordedRun; stops: Stop[]; step: number; hideHumans?: boolean;
}) {
  // Mounted when the slide first comes near and then kept: the env-pane's Scene places the agents' labels as DOM
  // elements beside its canvas, and removing the canvas while the deck runs throws (a React removeChild error). The
  // web-ui never removes its scene during a sim-run; the deck keeps it too, at the cost of one WebGL context per
  // replay seen (seven at most).
  const nearNow = useSlideNear();
  const [near, setNear] = useState(nearNow);
  useEffect(() => { if (nearNow) setNear(true); }, [nearNow]);
  const first = recorded.ticks[0].tick!;
  const index = (tick: number) => Math.max(0, Math.min(recorded.ticks.length - 1, tick - first));
  const target = index(stops[Math.min(step, stops.length - 1)].tick);
  const [shown, setShown] = useState(target);
  const from = useRef(shown);
  from.current = shown;
  const [pace, setPace] = useState(TICK_MS);
  useEffect(() => {
    if (target <= from.current) { setShown(target); return; }      // back, or no move: jump
    const ms = Math.max(30, Math.min(TICK_MS, MOVE_MAX_MS / (target - from.current)));
    setPace(ms);
    const id = setInterval(() => setShown((s) => {
      if (s + 1 >= target) { clearInterval(id); return target; }
      return s + 1;
    }), ms);
    return () => clearInterval(id);
  }, [target]);

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
    <div className="replay">
      <div className="replay-scene">
        {near && (
          <Canvas orthographic flat dpr={[1, 2]} gl={{ antialias: true, stencil: true }}>
            <PixelRatio />
            <FramingCamera view="tilted" free={false} onFree={() => {}} bounds={room.space.bounds} height={tallest} />
            <Scene room={room} moment={moment} book={book} appearance={recorded.appearance}
                   glideMs={target > shown ? pace : 0} ahead={ahead} shown={ALL_SHOWN} />
          </Canvas>
        )}
        <div className="replay-tick">tick {update.tick}</div>
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
export function ReplayView({ recorded, stops, hideHumans = false }: {
  recorded: RecordedRun; stops: Stop[]; hideHumans?: boolean;
}) {
  const step = useSlideSteps(".step-stop");
  return (
    <>
      <RunReplay recorded={recorded} stops={stops} step={step} hideHumans={hideHumans} />
      {stops.slice(1).map((s) => <span key={s.tick} className="fragment step-marker step-stop" aria-hidden />)}
    </>
  );
}
