/**
 * A recorded sim-run replayed on a slide (scripts/record_run.py), drawn by the env-pane's own Scene: the agents, the
 * movable objects, and on the floor the robot's plan (dashed blue), the human's real path (dashed orange) and the
 * robot's projection of the human (a blue stripe, filled from her intention, hatched from her motion), exactly as the
 * web-ui draws a tick update. Nothing is computed here: every position and every segment is the recording's.
 *
 * Stepped by clicks: each step of the slide is a stop (a tick and a line); a click plays the ticks up to the next
 * stop at a calm pace, the agents gliding between ticks as the web-ui's play does, and going back jumps. The tick
 * shown stands in a corner. The lines of all stops stand as a list under the scene from the start, one per line, grey;
 * each turns black and bold when its click comes (Hadi, tpres-v6).
 *
 * `hideHumans`: the human is not drawn, nor her path (talk stage 1, the robot alone: a human-unaware sim-run, in which the
 * robot's mind receives no human; flagged in the report).
 *
 * `mind`: what the robot's mind holds at the tick, beside the scene (MindPanel.tsx; the overall revision, point F).
 * `mark`: an object the slide points at (talk stage 6: the item she was to take), a ring on the floor in the human's
 * colour under its container, with its name; drawn by the deck in the canvas, no change in webui/. The agents' id
 * labels (the env-pane's pills, "robot_0") are
 * hidden on slides by the deck's stylesheet: the slides call them the robot and the human.
 *
 * The canvas renders only while its slide is the current one (R3F's frameloop "never" otherwise), so that the replays
 * kept mounted do not load the page while another slide runs; while the replay plays toward a stop it marks itself
 * busy (`data-busy`), which the PDF export and the click-through wait for.
 */

import { Html } from "@react-three/drei";
import { Canvas, useThree } from "@react-three/fiber";
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";

import { FramingCamera } from "../../../webui/page/src/env-pane/camera";
import { setPixelRatio } from "../../../webui/page/src/env-pane/material";
import { aheadOf, ALL_SHOWN } from "../../../webui/page/src/env-pane/paths";
import { foldBook } from "../../../webui/page/src/env-pane/places";
import { type Moment, type Room, Scene } from "../../../webui/page/src/env-pane/Scene";
import { disc, FloorPatch } from "../../../webui/page/src/env-pane/solids";
import { theme } from "../../../webui/page/src/theme";
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
  robots: Pick<RobotDescription, "robot" | "condition" | "assigned" | "hypotheses" | "theta">[];   // assigned: its own tasks
  ticks: TickUpdate[];     // cut to what the slide draws (record_run.py, cut); read as tick updates
}

export interface Stop { tick: number; caption: string }

const TICK_MS = 140;    // the pace between stops: about seven ticks a second (a replay may set its own, `tickMs`),
const MOVE_MAX_MS = 4000;   // and faster where a move would take longer than this

/** `step`: the index of the stop the slide shows (0: the first). */
export function RunReplay({ recorded, stops, step, hideHumans = false, mind, tickMs = TICK_MS, mark }: {
  recorded: RecordedRun; stops: Stop[]; step: number; hideHumans?: boolean; mind?: MindParts; tickMs?: number;
  mark?: Mark;
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
  // The last stop the replay has reached: its line turns bold when the replay arrives, not when it sets off.
  const reached = Math.max(0, stops.reduce((r, st, i) => (index(st.tick) <= shown ? i : r), -1));
  const marked = mark === undefined ? null : markedAt(recorded, update, mark);
  const tallest = Math.max(recorded.appearance.human.height, recorded.appearance.robot.height,
    recorded.appearance.default_fixed.height, ...Object.values(recorded.appearance.fixed).map((l) => l.height));

  return (
    <div className={`replay${mind !== undefined ? " with-mind" : ""}`} data-busy={shown !== target ? "true" : undefined}>
      <div className="replay-main">
      <div className="replay-left">
      <div className="replay-scene">
        {near && (
          <Canvas orthographic flat dpr={[1, 2]} gl={{ antialias: true, stencil: true }}
                  frameloop={current ? "always" : "never"}>
            <PixelRatio />
            <FramingCamera view="tilted" free={false} onFree={() => {}} bounds={room.space.bounds} height={tallest} />
            <Scene room={room} moment={moment} book={book} appearance={recorded.appearance}
                   glideMs={target > shown ? pace : 0} ahead={ahead} shown={ALL_SHOWN} />
            {marked !== null && <MarkOnFloor {...marked} />}
          </Canvas>
        )}
        <div className="replay-tick">tick {update.tick}</div>
      </div>
      <ol className="replay-lines">
        {stops.map((st, i) => (
          <li key={st.tick} className={i <= reached ? "is-reached" : ""}>{st.caption}</li>
        ))}
      </ol>
      </div>
      {mind !== undefined && <MindPanel recorded={recorded} shown={shown} parts={mind} />}
      </div>
    </div>
  );
}

/** An object a slide points at: its id and the name the slide gives it. */
export interface Mark { object: string; label: string }

/** Where a marked movable object is at the tick: the position and size of the fixed object holding it (null while
 * carried or absent). */
function markedAt(recorded: RecordedRun, update: TickUpdate, mark: Mark): { x: number; y: number; r: number; label: string } | null {
  const holder = update.world.fixed_object_contents.find((c) => c.movable_objects.includes(mark.object));
  const fixed = holder === undefined ? undefined : recorded.world.fixed_objects.find((f) => f.id === holder.fixed_object);
  if (fixed === undefined) return null;
  return { x: fixed.position.x, y: fixed.position.y, r: 0.85 * Math.max(fixed.size.x, fixed.size.y), label: mark.label };
}

function MarkOnFloor({ x, y, r, label }: { x: number; y: number; r: number; label: string }) {
  const ring = useMemo(() => disc(r), [r]);
  return (
    <>
      <FloorPatch x={x} y={y} shape={ring} colour={theme.color.human} opacity={0.35} />
      <Html position={[x, 110, -y]} center zIndexRange={[10, 0]} className="replay-mark-anchor">
        <div className="replay-mark">{label}</div>
      </Html>
    </>
  );
}

/** The hatching's spacing in device pixels, as the env-pane sets it. */
function PixelRatio() {
  const dpr = useThree((state) => state.viewport.dpr);
  useLayoutEffect(() => setPixelRatio(dpr), [dpr]);
  return null;
}

/** A replay with its steps: one hidden step marker per stop after the first. */
export function ReplayView({ recorded, stops, hideHumans = false, mind, tickMs, mark }: {
  recorded: RecordedRun; stops: Stop[]; hideHumans?: boolean; mind?: MindParts; tickMs?: number; mark?: Mark;
}) {
  const step = useSlideSteps(".step-stop");
  return (
    <>
      <RunReplay recorded={recorded} stops={stops} step={step} hideHumans={hideHumans} mind={mind} tickMs={tickMs}
                 mark={mark} />
      {stops.slice(1).map((s) => <span key={s.tick} className="fragment step-marker step-stop" aria-hidden />)}
    </>
  );
}
