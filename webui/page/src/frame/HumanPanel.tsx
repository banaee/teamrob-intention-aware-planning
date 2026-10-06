/**
 * Panel 4a, the human and the world (T-viz 1a (iv); docs/handoffs/plan_T-viz_1a.md, section 4, "What panel 4a shows",
 * P5): per human, under its id and its colour, in the glossary's words (§6, P14):
 *   - the action in hand, with its progress (a bar and "d of n ticks") and the task it belongs to, the top of the stack;
 *   - the stack, top first: the task in progress, and below it the suspended task, if any; "no task" when empty;
 *   - the last switches of the stack and resumptions, newest first, five at most, each with its tick.
 * Read from the tick updates (src/frame/activity.ts); not shown in 1a, though the messages carry them: the script's
 * open entries, the other transitions, the script itself.
 */

import { useMemo } from "react";

import type { HumanActivity, TickUpdate } from "../gen/messages";
import { actionText, type Change, recentChanges, stackLines, whereText } from "./activity";

const RECENT = 5;

export function HumanPanel({ humans, ticks }: { humans: readonly string[]; ticks: readonly TickUpdate[] | null }) {
  const now = ticks === null ? null : ticks[ticks.length - 1];
  return (
    <aside className="panel panel-human" aria-label="The human and the world">
      <h2 className="panel-title">The human</h2>
      {now === null || humans.length === 0 ? (
        <p className="panel-later">No sim-run: what the human does shows once a scenario is chosen.</p>
      ) : humans.map((id) => {
        const activity = now.world.activity.find((a) => a.human === id);
        return activity ? <Human key={id} id={id} activity={activity} ticks={ticks!} /> : null;
      })}
    </aside>
  );
}

function Human({ id, activity, ticks }: { id: string; activity: HumanActivity; ticks: readonly TickUpdate[] }) {
  const changes = useMemo(() => recentChanges(ticks, id, RECENT), [ticks, id]);
  const action = activity.action;
  const top = activity.stack[0] ?? null;
  return (
    <section className="human">
      <h3 className="human-id"><span className="panel-dot" />{id}</h3>

      <h4 className="human-heading">Action in hand</h4>
      {action === null ? (
        <p className="human-none">{top === null ? "none: no task" : "none: the human waits"}</p>
      ) : (
        <>
          <p className="human-action">{actionText(action.action)}</p>
          <div className="human-progress">
            <span className="human-bar" aria-hidden>
              <span style={{ width: `${action.total > 0 ? (100 * action.done) / action.total : 0}%` }} />
            </span>
            <span className="human-ticks">{action.done} of {action.total} ticks</span>
          </div>
          {top !== null && <p className="human-of">of <span className="human-task">{top.label}</span></p>}
        </>
      )}

      <h4 className="human-heading">Stack</h4>
      {activity.stack.length === 0 ? <p className="human-none">no task</p> : (
        <ol className="human-stack">
          {stackLines(activity).map(({ task, suspended }, i) => (
            <li key={i} className={suspended ? "is-suspended" : undefined}>
              <span className="human-task">{task.label}</span>
              <span className="human-state">{suspended ? "suspended" : "in progress"}</span>
            </li>
          ))}
        </ol>
      )}

      <h4 className="human-heading">Switches and resumptions</h4>
      {changes.length === 0 ? <p className="human-none">none yet</p> : (
        <ol className="human-changes">
          {changes.map((c, i) => <ChangeLine key={i} change={c} />)}
        </ol>
      )}
    </section>
  );
}

function ChangeLine({ change }: { change: Change }) {
  return (
    <li>
      <span className="human-tick">tick {change.tick}</span>
      {change.kind === "switch" ? (
        <span>
          switch to <span className="human-task">{change.task.label}</span>
          {change.below !== null
            ? <>; <span className="human-task">{change.below.label}</span> suspended {whereText(change.where)}</>
            : <> {whereText(change.where)}</>}
        </span>
      ) : (
        <span>resumption of <span className="human-task">{change.task.label}</span></span>
      )}
    </li>
  );
}
