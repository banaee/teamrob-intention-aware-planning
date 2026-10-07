/**
 * One colour per task across the page (T-viz 1c; Hadi, 7 October 2026, preferred): the same task has the same colour
 * in panel 4c's lanes, in the right panel's belief chart and in the left panel's script, stack and action in hand. A
 * task is known by its identity, which the simulator's side sends (`TaskRef.identity`, task equality; it equals the key
 * of the hypothesis that names the task); the page only compares identities.
 *
 * The colours are fixed once per sim-run from its run description, so that no colour changes during a sim-run or after
 * a reload, in this order: each human's script (its entries in written order, each followed by the tasks its events
 * start; the repeatable entries; the closing part), each robot's own assigned tasks, then the hypotheses in the
 * recognizer's order. The first tasks get the palette's hues (src/theme.ts, `task`), every further task the neutral
 * `taskOther`: the tasks the human and the robot perform always have a hue of their own.
 */

import type { RunDescription, ScriptEntry, TaskRef } from "../gen/messages";
import { theme } from "../theme";

export type TaskColours = ReadonlyMap<string, string>;

export const NO_COLOURS: TaskColours = new Map();

export function taskColours(description: RunDescription, palette: readonly string[] = theme.task,
                            other: string = theme.taskOther): TaskColours {
  const order: string[] = [];
  const add = (identity: string) => { if (!order.includes(identity)) order.push(identity); };
  const entry = (e: ScriptEntry) => {
    add(e.task.identity);
    for (const ev of e.events) if (ev.decision.kind === "start") add(ev.decision.task.identity);
  };
  for (const script of description.world.scripts) {
    script.entries.forEach(entry);
    for (const r of script.repeatable) add(r.task.identity);
    script.closing.forEach(entry);
  }
  for (const robot of description.robots) for (const t of robot.assigned) add(t.identity);
  for (const robot of description.robots) for (const h of robot.hypotheses) add(h.key);
  return new Map(order.map((identity, i) => [identity, palette[i] ?? other]));
}

/** The colour of a task or a hypothesis by its identity; `taskOther` for one the description does not name. */
export function colourOf(colours: TaskColours, identity: string): string {
  return colours.get(identity) ?? theme.taskOther;
}

export function taskColour(colours: TaskColours, task: TaskRef): string {
  return colourOf(colours, task.identity);
}
