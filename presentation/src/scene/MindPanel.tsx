/**
 * What Anton's mind holds at the replayed tick, beside the scene (the overall revision of 8 October 2026, point F): first
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
  belief?: boolean;
  support?: boolean;
  fit?: boolean;
  hold?: boolean;
  projection?: boolean;
  context?: boolean;
}

/** A task or a hypothesis in the talk's words: its schema's words, and the number of a binding whose object the
 * schema names (deliver_item with item_1: "deliver item 1"); other bindings are left out (coffee_break with
 * coffee_machine_0: "coffee break"). */
export function talkName(task: string, bindings: readonly { value: string }[]): string {
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
    <aside className="mind" aria-label="What Anton's mind holds at this tick">
      <h2 className="mind-title"><span className="mind-dot" />Anton's mind</h2>
      <dl className="mind-facts">
        <div><dt>its task</dt><dd>{finished ? "all done" : task === null ? "–" : taskName(task)}</dd></div>
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
          {belief === null ? <p className="mind-none">none: Anton knows nothing about her intentions</p>
            : rows.map((key) => {
              const h = live.get(key) ?? null;
              const colour = colourOf(colours, key);
              return (
                <div key={key} className={`mind-row${h === null ? " is-dead" : ""}${key === trusted ? " is-trusted" : ""}`}>
                  <span className="mind-label">
                    <i className="mind-swatch" style={{ background: colour }} />{hypothesisName(robot.hypotheses, key)}
                    {key === trusted && <span className="mind-trusted">trusted</span>}
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
