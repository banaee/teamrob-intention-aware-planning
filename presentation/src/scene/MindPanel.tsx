/**
 * What the robot's mind holds at the replayed tick, beside the scene (the overall revision of 8 October 2026, point F): first
 * the live hypotheses as a bar chart whose bars rise and fall per tick, θ marked on each bar and the trusted intention
 * marked; further parts where a talk stage is about them (support, fit, the hold, the projection of her, the context).
 *
 * A TEMPORARY VERSION of the web-ui's robot panel (webui/page/src/frame/RobotPanel.tsx, panel 4b) in its look and its
 * order: its belief chart (one row per hypothesis live at some tick so far, each keeping its row, the bar in the task's
 * colour with θ marked, the value, the marks ✓ ✗ ·) and its facts. The panel's own row and fact components are not
 * exported, and the deck changes nothing in webui/ for this; so the rows are drawn here, at the deck's sizes, from the
 * web-ui's exported helpers (beliefRows, taskColours, colourOf). The change that would let the deck reuse them is named
 * in the report of the revision: export ChartRow and Facts from RobotPanel.tsx, with their sizes read from CSS
 * variables, so that the deck can scale them.
 *
 * Nothing is computed here: every value is the recorded tick update's (scripts/record_run.py). The hypotheses are
 * written in the talk's words (deliver_item(?item=item_1) as "deliver item 1"); display text only.
 */

import { colourOf, taskColours } from "../../../webui/page/src/frame/colours";
import { beliefRows } from "../../../webui/page/src/frame/robot";
import type {
  Adequacy, Hypothesis, RobotTick, RunDescription, TaskRef, TickUpdate,
} from "../../../webui/page/src/gen/messages";
import type { RecordedRun } from "./RunReplay";

/** The parts of the mind a slide shows: the hypotheses' chart is the default where the robot recognises. */
export interface MindParts {
  /** All the robot's tasks with their steps, a step bold once reached (talk stage 1, Hadi, tpres-v6). */
  tasks?: boolean;
  belief?: boolean;
  support?: boolean;
  fit?: boolean;
  hold?: boolean;
  projection?: boolean;
  context?: boolean;
}

/** Tasks whose schema's words are not the talk's (the talk says "switching on the A/C"). */
const SAID: Record<string, string> = { ac_activation: "switching on the A/C" };

/** A task or a hypothesis in the talk's words: its schema's words, and the number of a binding whose object the
 * schema names (deliver_item with item_1: "deliver item 1"); other bindings are left out (coffee_break with
 * coffee_machine_0: "coffee break"). */
export function talkName(task: string, bindings: readonly { value: string }[]): string {
  if (task in SAID) return SAID[task];
  const words = task.split("_");
  for (const b of bindings) {
    const m = /^(.*)_(\d+)$/.exec(b.value);
    if (m !== null && task.endsWith(m[1])) words.push(m[2]);
  }
  return words.join(" ");
}

const taskName = (t: TaskRef) => talkName(t.task, t.bindings);

function hypothesisName(hypotheses: readonly Hypothesis[], key: string): string {
  const h = hypotheses.find((x) => x.key === key);
  return h === undefined ? key : talkName(h.task, h.bindings);
}

/** A kitting task's steps in the talk's words (as the slide of the robot's task knowledge names them), and which one
 * the body's action at its plan's cursor is: a walk to a table is the third, any other walk the first. Display text. */
const STEPS = ["go to the item", "pick it up", "go to its table", "place it"];
function stepOf(action: string, target: string | undefined): number {
  if (action === "pick_up") return 1;
  if (action === "place") return 3;
  return target !== undefined && target.startsWith("kitting_table") ? 2 : 0;
}

const ADEQUACY: Record<Adequacy, string> = { adequate: "✓", inadequate: "✗", no_observation: "·" };

export function MindPanel({ recorded, shown, parts }: { recorded: RecordedRun; shown: number; parts: MindParts }) {
  const robot = recorded.robots[0];
  const ticks = recorded.ticks.slice(0, shown + 1) as unknown as TickUpdate[];
  const tick = recorded.ticks[shown].robots.find((r) => r.robot === robot.robot) as unknown as RobotTick;
  const colours = taskColours({ world: { scripts: recorded.world.scripts }, robots: recorded.robots } as unknown as
    RunDescription);
  const rows = beliefRows(ticks, robot.robot);
  const belief = tick.belief;
  const live = new Map((belief?.live ?? []).map((h) => [h.key, h]));
  const p = tick.decision?.projection;
  const trusted = p !== undefined && p.kind === "admitted" ? p.hypothesis : null;
  const { task, hold, finished } = tick.body;
  const raised = belief?.levels.filter((l) => l.level !== "ordinary") ?? [];

  return (
    <aside className="mind" aria-label="What the robot's mind holds at this tick">
      <h2 className="mind-title"><span className="mind-dot" />Robot's mind</h2>
      {parts.tasks && <TaskList recorded={recorded} ticks={ticks} />}
      <dl className="mind-facts">
        {!parts.tasks && <div><dt>its task</dt><dd>{finished ? "all done" : task === null ? "–" : taskName(task)}</dd></div>}
        {parts.hold && (
          <div><dt>hold</dt><dd className={hold === null ? "" : "mind-hold"}>
            {hold === null ? "–" : `${hold.stood} of ${hold.planned} ticks`}</dd></div>
        )}
        {parts.projection && (
          <div><dt>her path</dt><dd>{p === undefined || p.kind === "none" ? "–"
            : p.kind === "admitted" ? "projection from her intention" : "projection from her motion"}</dd></div>
        )}
        {parts.context && (
          <div><dt>context</dt><dd>{raised.length === 0 ? "–"
            : raised.map((l) => `${talkName(l.task, [])} ${l.level}`).join(", ")}</dd></div>
        )}
      </dl>
      {parts.belief && (
        <div className="mind-belief">
          <div className="mind-row mind-head">
            <span>hypotheses <small>belief, θ {robot.theta}</small></span>
            {parts.support && <span className="mind-mark">support</span>}
            {parts.fit && <span className="mind-mark">fits</span>}
          </div>
          {belief === null ? <p className="mind-none">none: robot knows nothing about her intentions</p>
            : rows.map((key) => {
              const h = live.get(key) ?? null;
              const colour = colourOf(colours, key);
              return (
                <div key={key} className={`mind-row${h === null ? " is-dead" : ""}${key === trusted ? " is-trusted" : ""}`}>
                  <span className="mind-label">
                    <i className="mind-swatch" style={{ background: colour }} />{hypothesisName(robot.hypotheses, key)}
                    {key === trusted && <span className="mind-trusted">recognised</span>}
                  </span>
                  <span className="mind-bar" aria-hidden>
                    <span style={{ width: `${h === null ? 0 : 100 * h.belief}%`, background: colour }} />
                    <i style={{ left: `${100 * robot.theta}%` }} />
                  </span>
                  <span className="mind-value">{h === null ? "–" : h.belief.toFixed(2)}</span>
                  {parts.support && <span className={h?.warrant === "observation" ? "mark-yes" : "mark-faint"}>
                    {h === null ? "" : h.warrant === "observation" ? "✓" : "·"}</span>}
                  {parts.fit && <span className={h === null ? "" : `mark-${h.adequacy}`}>
                    {h === null ? "" : ADEQUACY[h.adequacy]}</span>}
                </div>
              );
            })}
          {parts.fit && belief?.finding === "unexplained" && (
            <p className="mind-finding">No hypothesis fits: unexplained</p>
          )}
        </div>
      )}
    </aside>
  );
}

/** All the robot's own tasks (its assigned pool), in order, each with its steps, grey; a step bold once the running
 * task reaches it, every step of a task the body ran before (Hadi, tpres-v6). */
function TaskList({ recorded, ticks }: { recorded: RecordedRun; ticks: TickUpdate[] }) {
  const robot = recorded.robots[0];
  const at = (u: TickUpdate) => u.robots.find((r) => r.robot === robot.robot)!.body;
  const now = at(ticks[ticks.length - 1]);
  const ran = new Set(ticks.map((u) => at(u).task?.identity).filter((x): x is string => x !== undefined));
  const action = now.action;
  const step = action === null || action === undefined ? -1
    : stepOf(action.action.action, action.action.bindings.find((b) => b.parameter === "?target")?.value);
  return (
    <ol className="mind-tasks">
      {robot.assigned.map((t) => {
        const current = !now.finished && now.task?.identity === t.identity;
        const before = !current && ran.has(t.identity);
        return (
          <li key={t.identity}>{taskName(t)}
            <ol className="mind-steps">
              {STEPS.map((st, i) => (
                <li key={st} className={before || (current && i <= step) ? "is-reached" : ""}>{st}</li>
              ))}
            </ol>
          </li>
        );
      })}
    </ol>
  );
}
