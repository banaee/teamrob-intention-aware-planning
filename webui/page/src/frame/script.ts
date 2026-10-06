/**
 * The human's script as panel 4a lists it (T-viz 1a (iv), block C): one line per entry in the script's written order
 * (the ordinary entries, the repeatable entries, the closing part), each authored event a line under its entry. Each
 * line's state is read from the tick updates the page holds, in the glossary's words (§6, **outcome**): an entry is
 * open, in progress (its task on top of the stack), suspended (below the top), or closed with its outcome (completed,
 * abandoned, infeasible); a repeatable entry is never closed. An event is pending until it fires; a Start event's task
 * is then in progress and leaves with its outcome; a Drop event, which starts nothing, has fired when its entry was
 * abandoned; an event that will not fire is unfired. The messages name each line's entry or event (`stack_entries`,
 * `Left.entry`, `Started.event`, `Unfired.position`); the page compares positions, never names.
 *
 * The tag per task of a line is the one its task last had on top of the stack (the tick update's `tag`, computed on the
 * simulator's side, world/tag.py); the page computes no tag.
 */

import type {
  EntryPosition, EventPosition, HumanScript, Outcome, TaskRef, TaskTagged, TickUpdate, UnfiredReason,
} from "../gen/messages";

export type EntryState = "open" | "in progress" | "suspended" | Outcome;
export type EventState = "pending" | "in progress" | "fired" | "unfired" | Outcome;

export interface EntryLine {
  kind: "entry";
  position: EntryPosition;
  task: TaskRef;
  state: EntryState;
  tick: number | null;           // when it closed (its outcome), or null
  completions: number;           // a repeatable entry: how often its task was completed
  tag: TaskTagged | null;
}

export interface EventLine {
  kind: "event";
  position: EventPosition;
  task: TaskRef | null;          // a Start event's task; null for a Drop
  state: EventState;
  tick: number | null;           // when it fired, or null
  unfired: UnfiredReason | null;
  tag: TaskTagged | null;
}

export type ScriptLine = EntryLine | EventLine;

const samePosition = (a: EntryPosition | null, b: EntryPosition | null) =>
  a !== null && b !== null && a.part === b.part && a.index === b.index;
const sameEvent = (a: EventPosition | null, b: EventPosition) =>
  a !== null && samePosition(a.entry, b.entry) && a.index === b.index;
const CLOSED: readonly string[] = ["completed", "abandoned", "infeasible"];

export function scriptLines(script: HumanScript, ticks: readonly TickUpdate[]): ScriptLine[] {
  const human = script.human;
  const parts: [EntryPosition["part"], readonly { task: TaskRef; events?: HumanScript["entries"][number]["events"] }[]][] =
    [["ordinary", script.entries], ["repeatable", script.repeatable], ["closing", script.closing]];

  // One pass over the tick updates: per entry its outcome, completions and last tag; per event its firing, its task's
  // outcome and last tag.
  const outcome = new Map<string, { state: Outcome; tick: number }>();
  const completions = new Map<string, number>();
  const entryTag = new Map<string, TaskTagged | null>();
  const fired = new Map<string, number>();
  const eventOutcome = new Map<string, Outcome>();
  const eventTag = new Map<string, TaskTagged | null>();
  const unfired = new Map<string, UnfiredReason>();
  const keyOf = (p: EntryPosition) => `${p.part} ${p.index}`;
  const eventKey = (p: EventPosition) => `${keyOf(p.entry)} ${p.index}`;
  let onTopEvent: EventPosition | null = null;      // the event whose task is on top, while it is
  for (const update of ticks) {
    if (update.tick === null) continue;
    const activity = update.world.activity.find((a) => a.human === human);
    if (!activity) continue;
    for (const t of activity.transitions) {
      if (t.kind === "started") {
        if (t.event !== null) fired.set(eventKey(t.event), update.tick);
        onTopEvent = t.event;
      } else if (t.kind === "unfired") {
        unfired.set(eventKey(t.position), t.reason);
      } else if (t.kind === "left" && t.outcome !== "suspended") {
        if (t.entry !== null) {
          outcome.set(keyOf(t.entry), { state: t.outcome, tick: update.tick });
          if (t.outcome === "completed") completions.set(keyOf(t.entry), (completions.get(keyOf(t.entry)) ?? 0) + 1);
        } else if (onTopEvent !== null) {
          eventOutcome.set(eventKey(onTopEvent), t.outcome);
          onTopEvent = null;
        }
      }
    }
    const top = activity.stack_entries.length > 0 ? activity.stack_entries[0] : undefined;
    if (top !== undefined && top !== null) entryTag.set(keyOf(top), activity.tag);
    else if (top === null && onTopEvent !== null) eventTag.set(eventKey(onTopEvent), activity.tag);
  }

  const now = ticks.length > 0 ? ticks[ticks.length - 1].world.activity.find((a) => a.human === human) : undefined;
  const lines: ScriptLine[] = [];
  for (const [part, entries] of parts) {
    entries.forEach((entry, index) => {
      const position: EntryPosition = { part, index };
      const key = keyOf(position);
      const onStack = now?.stack_entries.findIndex((p) => samePosition(p, position)) ?? -1;
      const isOpen = now === undefined || part === "repeatable" || now.open_entries.some((p) => samePosition(p, position));
      const closed = outcome.get(key);
      const state: EntryState = onStack === 0 ? "in progress" : onStack > 0 ? "suspended"
        : !isOpen && closed ? closed.state : "open";
      lines.push({ kind: "entry", position, task: entry.task, state,
                   tick: CLOSED.includes(state) && closed ? closed.tick : null,
                   completions: completions.get(key) ?? 0, tag: entryTag.get(key) ?? null });
      (entry.events ?? []).forEach((event, k) => {
        const p: EventPosition = { entry: position, index: k };
        const ek = eventKey(p);
        const start = event.decision.kind === "start" ? event.decision.task : null;
        const onTop = now !== undefined && now.stack_entries.length > 0 && now.stack_entries[0] === null
          && sameEvent(onTopEvent, p);
        let st: EventState;
        if (unfired.has(ek)) st = "unfired";
        else if (start === null) st = state === "abandoned" ? "fired" : "pending";
        else if (onTop) st = "in progress";
        else if (eventOutcome.has(ek)) st = eventOutcome.get(ek)!;
        else st = fired.has(ek) ? "fired" : "pending";
        lines.push({ kind: "event", position: p, task: start, state: st, tick: fired.get(ek) ?? null,
                     unfired: unfired.get(ek) ?? null, tag: eventTag.get(ek) ?? null });
      });
    });
  }
  return lines;
}
