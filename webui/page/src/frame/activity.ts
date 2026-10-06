/**
 * Panel 4a's reading of a human's activity (T-viz 1a (iv); docs/handoffs/plan_T-viz_1a.md, section 4, "What panel 4a
 * shows", P5, P14), in the glossary's words (§6): the action in hand with its progress and the task it belongs to (the
 * top of the stack); the stack, top first, the task below the top suspended; the last switches of the stack and
 * resumptions, newest first, each with its tick. Everything is read from the tick updates; the page derives nothing the
 * record does not state, and names no domain word: actions, tasks and bindings arrive as data.
 */

import type { ActionRef, HumanActivity, Started, TaskRef, TickUpdate } from "../gen/messages";

/** Where a switch cut the task below it (the record's `Where`); null on the empty stack. */
type Where = NonNullable<Started["where"]>;

/** An action as the logs write a grounded action: its name and its bindings' values, e.g. `name(value, value)`. */
export function actionText(action: ActionRef): string {
  return `${action.action}(${action.bindings.map((b) => b.value).join(", ")})`;
}

/** A task as panel 4a writes it: its schema's name and its bindings' values, as an action is written (P31). */
export function taskText(task: TaskRef): string {
  return `${task.task}(${task.bindings.map((b) => b.value).join(", ")})`;
}

/** One task of the stack, top first: the top is in progress, a task below it is suspended. */
export interface StackLine {
  task: TaskRef;
  suspended: boolean;
}

export function stackLines(activity: HumanActivity): StackLine[] {
  return activity.stack.map((task, i) => ({ task, suspended: i > 0 }));
}

/** A switch of the stack (a task started by an event, the task below it, if any, suspended) or a resumption (the
 * return to a suspended task), with the tick of the tick update that states it. */
export type Change =
  | { kind: "switch"; tick: number; task: TaskRef; below: TaskRef | null; where: Where | null }
  | { kind: "resumption"; tick: number; task: TaskRef };

/** A human's last `n` switches and resumptions, newest first, from the tick updates in order. Within one tick, the
 * transitions' order is the record's, reversed with the rest. */
export function recentChanges(ticks: readonly TickUpdate[], human: string, n: number): Change[] {
  const changes: Change[] = [];
  for (let i = ticks.length - 1; i >= 0 && changes.length < n; i--) {
    const update = ticks[i];
    if (update.tick === null) continue;
    const activity = update.world.activity.find((a) => a.human === human);
    if (!activity) continue;
    const found: Change[] = [];
    for (const t of activity.transitions) {
      if (t.kind === "started") {
        // The task below the started one: the second of the stack at that tick (the stack is top first).
        found.push({ kind: "switch", tick: update.tick, task: t.task, below: activity.stack[1] ?? null,
                     where: t.where });
      } else if (t.kind === "resumed") {
        found.push({ kind: "resumption", tick: update.tick, task: t.task });
      }
    }
    changes.push(...found.reverse());
  }
  return changes.slice(0, n);
}

/** Where a switch cut the task below it: after an action, before its first action, inside an action (with the ticks
 * of it done), or on the empty stack. */
export function whereText(where: Where | null): string {
  if (where === null) return "on the empty stack";
  switch (where.kind) {
    case "boundary": return `after ${actionText(where.action)}`;
    case "beginning": return "before its first action";
    case "cut": return `inside ${actionText(where.action)}, ${where.done} ${where.done === 1 ? "tick" : "ticks"} done`;
  }
}
