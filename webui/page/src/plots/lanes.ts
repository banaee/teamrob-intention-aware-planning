/**
 * Panel 4c's reading of a sim-run (T-viz 1c; docs/handoffs/plan_T-viz_1c.md; Hadi, 7 October 2026, preferred): the
 * values of the five lanes per tick, read from the tick updates the page holds, and the bands they form. The page
 * computes nothing of the simulation: each value is a field of a tick update, and a band is a run of ticks with one
 * value.
 *
 *   (1) the human's task: the task on top of the human's stack (the truth) and its tag per task;
 *   (2) the robot's belief: the recognizer's belief over the live hypotheses, and what the robot holds since its last
 *       decision (the hypothesis that decision admitted, panel 4b's "held");
 *   (3) context: whether each timeline fact holds;
 *   (4) the robot's task: its task, a hold in progress, the decision taken on the tick;
 *   (5) distance: the robot-human distance over the tick, as the run log's [sep] line states it.
 *
 * Index t of every per-tick array is tick t (the tick update after the start's). The lanes are folded one tick update
 * at a time and kept between calls (foldLanes), so that play stays cheap in a long sim-run: their arrays only grow, and
 * a reader reads them up to `length`.
 */

import type {
  DecisionMade, RobotBelief, RobotDescription, RunDescription, Separation, TaskRef, TaskTagged, TickUpdate,
} from "../gen/messages";

export interface HumanLane {
  human: string;
  task: (TaskRef | null)[];
  tag: (TaskTagged | null)[];
}

export interface RobotLane {
  robot: RobotDescription;
  belief: (RobotBelief | null)[];
  /** The hypothesis the last decision admitted (its admitted projection's), held until the next decision; null when
   * that decision admitted none, or before the first decision. */
  held: (string | null)[];
  task: (TaskRef | null)[];
  hold: boolean[];
  /** The decision taken on the tick, else null. */
  decision: (DecisionMade | null)[];
  /** Every hypothesis that has been the leader at some tick so far. */
  leaders: Set<string>;
}

export interface FactLane {
  fact: string;
  holds: boolean[];
}

export interface PairLane {
  robot: string;
  human: string;
  separation: (Separation | null)[];
}

export interface Lanes {
  /** The sim-run the lanes read. */
  key: string;
  /** The ticks folded: ticks 0 to length − 1. */
  length: number;
  humans: HumanLane[];
  robots: RobotLane[];
  facts: FactLane[];
  pairs: PairLane[];
}

function emptyLanes(description: RunDescription): Lanes {
  const world = description.world;
  // The timeline's facts in the order of their first window; a sim-run without a window has no context lane.
  const facts = [...world.timeline.windows].sort((a, b) => a.start - b.start || a.fact.localeCompare(b.fact))
    .map((w) => w.fact).filter((f, i, all) => all.indexOf(f) === i);
  return {
    key: description.sim_run,
    length: 0,
    humans: world.humans.map((h) => ({ human: h.id, task: [], tag: [] })),
    robots: description.robots.map((robot) => ({
      robot, belief: [], held: [], task: [], hold: [], decision: [], leaders: new Set<string>(),
    })),
    facts: facts.map((fact) => ({ fact, holds: [] })),
    pairs: description.robots.flatMap((r) => world.humans.map((h) => ({ robot: r.robot, human: h.id, separation: [] }))),
  };
}

function append(lanes: Lanes, update: TickUpdate): void {
  const t = lanes.length;
  if (update.tick !== t) throw new Error(`tick update ${update.tick} where tick ${t} was expected`);
  for (const lane of lanes.humans) {
    const activity = update.world.activity.find((a) => a.human === lane.human);
    lane.task.push(activity?.stack[0] ?? null);
    lane.tag.push(activity?.tag ?? null);
  }
  for (const lane of lanes.robots) {
    const r = update.robots.find((x) => x.robot === lane.robot.robot);
    const belief = r?.belief ?? null;
    lane.belief.push(belief);
    if (belief?.leader) lane.leaders.add(belief.leader);
    const d = r?.decision ?? null;
    lane.held.push(d !== null && d.projection.kind === "admitted" ? d.projection.hypothesis : null);
    lane.task.push(r?.body.task ?? null);
    lane.hold.push(r?.body.hold != null);
    lane.decision.push(d !== null && d.tick === t ? d : null);
  }
  for (const lane of lanes.facts) lane.holds.push(update.world.timeline_facts.includes(lane.fact));
  for (const lane of lanes.pairs) {
    lane.separation.push(update.world.separations.find((s) => s.robot === lane.robot && s.human === lane.human) ?? null);
  }
  lanes.length = t + 1;
}

/** The lanes of a sim-run's tick updates (the start's first): the ticks not yet folded are appended to the previous
 * lanes; another sim-run, or a sequence shorter than the one folded, starts anew. Returns a new object over the same
 * arrays, so that a change is seen. */
export function foldLanes(previous: Lanes | null, description: RunDescription,
                          ticks: readonly TickUpdate[]): Lanes {
  const steps = ticks.length - 1;   // the start's update carries no tick
  const lanes = previous !== null && previous.key === description.sim_run && previous.length <= steps
    ? previous : emptyLanes(description);
  for (let t = lanes.length; t < steps; t++) append(lanes, ticks[t + 1]);
  return { ...lanes };
}

/** A run of ticks [start, end] (both included) over which `values` hold one value, by `same`; null values form none. */
export interface Band<T> {
  start: number;
  end: number;
  value: T;
}

export function bands<T>(values: readonly (T | null)[], length: number, same: (a: T, b: T) => boolean): Band<T>[] {
  const out: Band<T>[] = [];
  for (let t = 0; t < length; t++) {
    const v = values[t];
    if (v === null || v === undefined) continue;
    const last = out[out.length - 1];
    if (last !== undefined && last.end === t - 1 && same(last.value, v)) last.end = t;
    else out.push({ start: t, end: t, value: v });
  }
  return out;
}

/** The human's task stretches: one band while the same task stays on top, a new one where its tag's stretch begins
 * anew (the tag's `since`, world/tag.py's stretches). */
export interface Stretch {
  task: TaskRef;
  tag: TaskTagged | null;
}

export function humanBands(lane: HumanLane, length: number): Band<Stretch>[] {
  const stretches = lane.task.map((task, t) => (task === null ? null : { task, tag: lane.tag[t] }));
  return bands(stretches, length, (a, b) => a.task.label === b.task.label && a.tag?.since === b.tag?.since);
}

export function robotBands(lane: RobotLane, length: number): Band<TaskRef>[] {
  return bands(lane.task, length, (a, b) => a.label === b.label);
}

export function heldBands(lane: RobotLane, length: number): Band<string>[] {
  return bands(lane.held, length, (a, b) => a === b);
}

export function trueBands(values: readonly boolean[], length: number): Band<true>[] {
  return bands(values.map((v) => (v ? true : null)), length, () => true);
}

/** Per hypothesis of the robot's hypothesis space, its belief at each tick it is live, else null. */
export function beliefLines(lane: RobotLane, length: number): Map<string, (number | null)[]> {
  const out = new Map<string, (number | null)[]>(lane.robot.hypotheses.map((h) => [h.key, new Array(length).fill(null)]));
  for (let t = 0; t < length; t++) {
    for (const h of lane.belief[t]?.live ?? []) {
      if (!out.has(h.key)) out.set(h.key, new Array(length).fill(null));
      out.get(h.key)![t] = h.belief;
    }
  }
  return out;
}

/** The tick axis, from tick 0 to the next multiple of `portion` past the latest tick: it extends in fixed portions
 * and is not rescaled at every tick. */
export const PORTION = 100;

export function axisEnd(length: number): number {
  return Math.max(PORTION, PORTION * Math.ceil(length / PORTION));
}
