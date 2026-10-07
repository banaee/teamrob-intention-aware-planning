/**
 * Panel 4a, the human and the world's context at the tick (T-viz 1a (iv); docs/handoffs/plan_T-viz_1a.md, P27, P28).
 * Per human, under its id and its colour, in the glossary's words (§6):
 *   (A) the human now: the action in hand with its progress, the task it belongs to with its tag per task, the stack;
 *   (C) the human's script, which the robot does not know: one line per entry in written order, an event under its
 *       entry, each with its state by colour and its tag; ◀ on the line in progress (src/frame/script.ts);
 *   (B) the last switches of the stack and resumptions, newest first, each with its tick.
 * Then (D) the world's context now: the timeline facts in force and the object states that hold.
 * Tasks are written by their values (P31). The tag per task (in accord, not in accord, no fact) is computed on the
 * simulator's side (world/tag.py) and only shown here. A task's swatch is its colour across the page (T-viz 1c,
 * src/frame/colours.ts).
 */

import { useEffect, useMemo, useRef } from "react";

import type { HumanActivity, HumanScript, TaskTagged, TickUpdate } from "../gen/messages";
import { actionText, type Change, recentChanges, stackLines, taskText, whereText } from "./activity";
import { type TaskColours, taskColour } from "./colours";
import { type ScriptLine, scriptLines } from "./script";

const RECENT = 5;

export function HumanPanel({ humans, scripts, ticks, colours }: {
  humans: readonly string[]; scripts: readonly HumanScript[]; ticks: readonly TickUpdate[] | null; colours: TaskColours;
}) {
  const now = ticks === null ? null : ticks[ticks.length - 1];
  return (
    <aside className="panel panel-human" aria-label="The human and the world's context">
      <h2 className="panel-title">The human</h2>
      {now === null || humans.length === 0 ? (
        <p className="panel-later">No sim-run: what the human does shows once a scenario is chosen.</p>
      ) : (
        <>
          {humans.map((id) => {
            const activity = now.world.activity.find((a) => a.human === id);
            const script = scripts.find((s) => s.human === id);
            return activity ? <Human key={id} id={id} activity={activity} script={script ?? null} ticks={ticks!}
                                     colours={colours} />
              : null;
          })}
          <Context update={now} />
        </>
      )}
    </aside>
  );
}

function Human({ id, activity, script, ticks, colours }: {
  id: string; activity: HumanActivity; script: HumanScript | null; ticks: readonly TickUpdate[]; colours: TaskColours;
}) {
  const changes = useMemo(() => recentChanges(ticks, id, RECENT), [ticks, id]);
  const lines = useMemo(() => (script === null ? [] : scriptLines(script, ticks)), [script, ticks]);
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
        </>
      )}
      {top !== null && (
        <p className="human-of">of <span className="human-task"><Swatch colour={taskColour(colours, top)} />{taskText(top)}</span>{" "}
          <TagMark tagged={activity.tag} /></p>
      )}

      <h4 className="human-heading">Stack</h4>
      {activity.stack.length === 0 ? <p className="human-none">no task</p> : (
        <ol className="human-stack">
          {stackLines(activity).map(({ task, suspended }, i) => (
            <li key={i} className={suspended ? "is-suspended" : undefined}>
              <span className="human-task"><Swatch colour={taskColour(colours, task)} />{taskText(task)}</span>
              <span className="human-state">{suspended ? "suspended" : "in progress"}</span>
            </li>
          ))}
        </ol>
      )}

      {script !== null && <Script script={script} lines={lines} colours={colours} />}

      <h4 className="human-heading">Switches and resumptions</h4>
      {changes.length === 0 ? <p className="human-none">none yet</p> : (
        <ol className="human-changes">
          {changes.map((c, i) => <ChangeLine key={i} change={c} />)}
        </ol>
      )}
    </section>
  );
}

/** (C) The human's script: the robot does not know it. A long script scrolls, the line in progress kept in view. */
function Script({ script, lines, colours }: { script: HumanScript; lines: readonly ScriptLine[]; colours: TaskColours }) {
  const list = useRef<HTMLOListElement>(null);
  const current = lines.findIndex((l) => l.state === "in progress");
  useEffect(() => {
    list.current?.querySelector(".is-current")?.scrollIntoView({ block: "nearest" });
  }, [current]);
  const parts = { ordinary: "", repeatable: "repeatable", closing: "closing" } as const;
  return (
    <>
      <h4 className="human-heading">The human's script <small>the robot does not know it</small></h4>
      {script.dependence === "on_robot" && (
        <p className="human-note">The written priority order, not the order of execution: what the human can do
          depends on the robot.</p>
      )}
      <p className="human-note">The tag compares what the human does with what the facts suggest; the robot never
        has it.</p>
      <ol ref={list} className="script">
        {lines.map((line, i) => {
          const isEvent = line.kind === "event";
          const label = line.kind === "entry"
            ? taskText(line.task)
            : line.task !== null ? `start ${taskText(line.task)}` : "drop the task";
          const part = line.kind === "entry" && line.position.part !== "ordinary" ? parts[line.position.part] : "";
          return (
            <li key={i} className={`script-line state-${line.state.replace(" ", "-")}${isEvent ? " is-event" : ""}`
              + (line.state === "in progress" ? " is-current" : "")}>
              <span className="script-dot" aria-hidden />
              <span className="script-text">
                {part && <span className="script-part">{part} </span>}
                <span className="human-task">
                  {line.task !== null && <Swatch colour={taskColour(colours, line.task)} />}{label}</span>
                {line.state === "in progress" && <span className="script-mark"> ◀</span>}
                <span className="script-state">
                  {" "}{line.state}
                  {line.kind === "entry" && line.position.part === "repeatable" && line.completions > 0
                    ? `, completed ${line.completions}×` : ""}
                  {line.kind === "event" && line.unfired !== null ? ` (${line.unfired.replace(/_/g, " ")})` : ""}
                  {line.tick !== null ? ` at tick ${line.tick}` : ""}
                </span>
                {line.tag !== null && <> <TagMark tagged={line.tag} /></>}
              </span>
            </li>
          );
        })}
      </ol>
    </>
  );
}

/** A task's colour across the page, a small square before its text. */
function Swatch({ colour }: { colour: string }) {
  return <i className="task-swatch" style={{ background: colour }} aria-hidden />;
}

/** The tag per task in plain words, in its own colour; its raising facts' tasks as a hint. */
function TagMark({ tagged }: { tagged: TaskTagged | null }) {
  if (tagged === null) return null;
  const hint = tagged.raised.length > 0 ? `the facts at tick ${tagged.since} make more likely: ${tagged.raised.join(", ")}`
    : `no fact at tick ${tagged.since}`;
  return <span className={`tag tag-${tagged.tag.replace(/ /g, "-")}`} title={hint}>{tagged.tag}</span>;
}

/** (D) The world's context now: the timeline facts in force, and the object states that hold, by state. */
function Context({ update }: { update: TickUpdate }) {
  const facts = update.world.timeline_facts;
  const byState = new Map<string, string[]>();
  for (const s of update.world.object_states) {
    if (!byState.has(s.state)) byState.set(s.state, []);
    if (s.object !== null) byState.get(s.state)!.push(s.object);
  }
  return (
    <section className="human">
      <h3 className="human-id">The world's context</h3>
      <h4 className="human-heading">Timeline facts</h4>
      {facts.length === 0 ? <p className="human-none">no timeline fact in force</p>
        : <p className="context-facts">{facts.map((f) => <span key={f} className="context-fact">{f}</span>)}</p>}
      <h4 className="human-heading">Object states</h4>
      {byState.size === 0 ? <p className="human-none">no object state holds</p> : (
        <dl className="context-states">
          {[...byState].map(([state, objects]) => (
            <div key={state}><dt>{state}</dt><dd>{objects.length > 0 ? objects.join(", ") : "holds"}</dd></div>
          ))}
        </dl>
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
          switch to <span className="human-task">{taskText(change.task)}</span>
          {change.below !== null
            ? <>; <span className="human-task">{taskText(change.below)}</span> suspended {whereText(change.where)}</>
            : <> {whereText(change.where)}</>}
        </span>
      ) : (
        <span>resumption of <span className="human-task">{taskText(change.task)}</span></span>
      )}
    </li>
  );
}
