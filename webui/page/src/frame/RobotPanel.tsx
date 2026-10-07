/**
 * Panel 4b, the robot at the tick (T-viz 1b; docs/handoffs/plan_T-viz_1b.md; Hadi's review, 7 October 2026). Read at a
 * glance during play: short labels and values, no sentences. Per robot, under its id in the robot's colour:
 *   Body: its task, the action at its plan's cursor with its progress, the microaction of the tick, what it carries, a
 *   hold in progress;
 *   Intention recognition, the recognizer's outputs, each named: the leader, the adequacy finding, the lifecycle, an
 *   episode boundary; the belief over the live hypotheses as a bar chart with θ marked, each hypothesis keeping its row,
 *   with its hypothesis adequacy, observation warrant, evidence rank, tail probability S and prior; the levels; and,
 *   marked as an input, the memory's recency facts;
 *   Planning, what the meta-planner does with them: admission (what it holds since its last decision; the gate's answer
 *   at the tick), projection (the last decision's), decision (the last, then the ones before it).
 * The page decides nothing: every answer is the robot's, as the simulator's side sends it (src/frame/robot.ts). Each
 * bar of the belief chart has its task's colour, the colour the task has across the page (T-viz 1c, src/frame/colours.ts).
 */

import { useMemo } from "react";

import type {
  Carried, DecisionMade, HypothesisBelief, RobotBelief, RobotDescription, RobotTick, TickUpdate,
} from "../gen/messages";
import { actionText, taskText } from "./activity";
import { colourOf, type TaskColours } from "./colours";
import {
  admissionText, beliefRows, CAUSE_SHORT, CHANGE_SHORT, GATE_SHORT, held, keyText, recentDecisions, tickText,
  TRIGGER_SHORT,
} from "./robot";

const EARLIER = 3;

export function RobotPanel({ robots, ticks, colours }: {
  robots: readonly RobotDescription[]; ticks: readonly TickUpdate[] | null; colours: TaskColours;
}) {
  const now = ticks === null ? null : ticks[ticks.length - 1];
  return (
    <aside className="panel panel-robot" aria-label="The robot: its body and its mind">
      <h2 className="panel-title">The robot</h2>
      {now === null || robots.length === 0 ? <p className="panel-later">no sim-run</p>
        : robots.map((robot) => {
          const tick = now.robots.find((r) => r.robot === robot.robot);
          return tick ? <Robot key={robot.robot} robot={robot} tick={tick} now={now} ticks={ticks!} colours={colours} />
            : null;
        })}
    </aside>
  );
}

function Robot({ robot, tick, now, ticks, colours }: {
  robot: RobotDescription; tick: RobotTick; now: TickUpdate; ticks: readonly TickUpdate[]; colours: TaskColours;
}) {
  const rows = useMemo(() => beliefRows(ticks, robot.robot), [ticks, robot.robot]);
  const aware = robot.condition === "intention-aware";
  const human = robot.condition !== "human-unaware";
  return (
    <section className="robot">
      <h3 className="human-id">
        <span className="panel-dot robot-dot" />{robot.robot}
        {!aware && <span className="robot-chip">{robot.condition}</span>}
      </h3>
      <Body tick={tick} carried={now.world.carried.filter((c) => c.agent === robot.robot)} />

      <div className="robot-part part-recognition">
        <h4 className="part-title">Intention recognition <small>the recognizer's outputs</small></h4>
        {!aware ? <p className="human-none">off</p>
          : tick.belief === null ? <p className="human-none">{now.tick === null ? "no observation yet" : "none"}</p>
          : <Recognition robot={robot} belief={tick.belief} rows={rows} colours={colours} />}
      </div>

      <div className="robot-part part-planning">
        <h4 className="part-title">Planning <small>what the meta-planner does with them</small></h4>
        <h5 className="robot-heading">Admission</h5>
        {!human ? <p className="human-none">off</p> : <Admission robot={robot} tick={tick} started={now.tick !== null} />}
        <h5 className="robot-heading">Projection</h5>
        {!human ? <p className="human-none">off</p>
          : <Projection robot={robot} decision={tick.decision} now={now.tick} />}
        <h5 className="robot-heading">Decision</h5>
        <Decisions robot={robot} decision={tick.decision} ticks={ticks} />
      </div>
    </section>
  );
}

function Facts({ items }: { items: readonly [string, React.ReactNode][] }) {
  return (
    <dl className="robot-facts">
      {items.map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}
    </dl>
  );
}

function Body({ tick, carried }: { tick: RobotTick; carried: readonly Carried[] }) {
  const { task, action, microaction, hold, finished } = tick.body;
  return (
    <>
      <h5 className="robot-heading">Body</h5>
      <Facts items={[
        ["task", finished ? "all done" : task === null ? "none" : <span className="human-task">{taskText(task)}</span>],
        ["action", action === null ? "none" : (
          <span className="robot-action">
            <span className="human-task">{actionText(action.action)}</span>
            <span className="human-bar robot-bar" aria-hidden>
              <span style={{ width: `${action.total > 0 ? (100 * action.done) / action.total : 0}%` }} />
            </span>
            <span className="human-ticks">{action.done}/{action.total}</span>
          </span>
        )],
        ["this tick", microaction ?? "–"],
        ["carries", carried.length === 0 ? "–" : carried.map((c) => c.movable_object).join(", ")],
        ["hold", hold === null ? "–" : <span className="robot-hold">{hold.stood}/{hold.planned} · from {hold.decided_at}</span>],
      ]} />
    </>
  );
}

/** The recognizer's outputs at the tick. */
function Recognition({ robot, belief, rows, colours }: {
  robot: RobotDescription; belief: RobotBelief; rows: readonly string[]; colours: TaskColours;
}) {
  const live = new Map(belief.live.map((h) => [h.key, h]));
  const prior = robot.context_knowledge;
  return (
    <>
      <Facts items={[
        ["leader", belief.leader === null ? "–" : <span className="human-task">{keyText(robot, belief.leader)}</span>],
        ["finding", belief.finding ?? "–"],
        ["lifecycle", <>{belief.lifecycle}{belief.boundary && <span className="robot-chip">episode boundary</span>}</>],
      ]} />
      <div className={`chart${prior ? " with-prior" : ""}`} role="table" aria-label="belief over the live hypotheses">
        <div className="chart-row chart-head" role="row">
          <span>belief <small>θ {robot.theta}</small></span><span />
          <span title="hypothesis adequacy">adeq</span><span title="observation warrant">warr</span>
          <span title="evidence rank: outranked">rank</span><span title="tail probability S">S</span>
          {prior && <span title="prior from context knowledge">prior</span>}
        </div>
        {rows.map((key) => <ChartRow key={key} label={keyText(robot, key)} h={live.get(key) ?? null}
                                     leader={key === belief.leader} theta={robot.theta} prior={prior}
                                     colour={colourOf(colours, key)} />)}
      </div>
      {belief.levels.length > 0 && (
        <Facts items={[["levels", belief.levels.map((l) => `${l.task} ${l.level}`).join(" · ")]]} />
      )}
      {prior && (
        <Facts items={[["memory", <span title="an input of the recognizer: the memory of observed completions">
          recent: {belief.recent.length === 0 ? "–" : belief.recent.join(", ")} <small>(input)</small></span>]]} />
      )}
    </>
  );
}

const ADEQUACY = { adequate: "✓", inadequate: "✗", no_observation: "·" } as const;

function ChartRow({ label, h, leader, theta, prior, colour }: {
  label: string; h: HypothesisBelief | null; leader: boolean; theta: number; prior: boolean; colour: string;
}) {
  return (
    <div className={`chart-row${leader ? " is-leader" : ""}${h === null ? " is-dead" : ""}`} role="row"
         title={h === null ? `${label}: not live` : label}>
      <span className="chart-label human-task"><i className="task-swatch" style={{ background: colour }} />{label}</span>
      <span className="chart-bar" aria-hidden>
        <span style={{ width: `${h === null ? 0 : 100 * h.belief}%`, background: colour }} />
        <i style={{ left: `${100 * theta}%` }} />
      </span>
      <span className="chart-value">{h === null ? "–" : h.belief.toFixed(2)}</span>
      <span className={h === null ? "" : `mark-${h.adequacy}`}>{h === null ? "" : ADEQUACY[h.adequacy]}</span>
      <span className={h?.warrant === "observation" ? "mark-adequate" : "mark-faint"}>
        {h === null ? "" : h.warrant === "observation" ? "✓" : "·"}</span>
      <span className="mark-outranked">{h?.rank === "outranked" ? "↓" : ""}</span>
      <span>{h === null || h.tail === null ? "" : h.tail.toFixed(2)}</span>
      {prior && <span>{h === null || h.prior === null ? "" : h.prior.toFixed(2)}</span>}
    </div>
  );
}

/** Admission: (a) what the robot holds since its last decision; (b) the gate's answer at this tick. */
function Admission({ robot, tick, started }: { robot: RobotDescription; tick: RobotTick; started: boolean }) {
  const h = held(tick.decision);
  return (
    <Facts items={[
      ["held", h === null ? "–" : <>
        {h.hypothesis === null ? "nothing admitted" : <span className="human-task">{keyText(robot, h.hypothesis)}</span>}
        <small> · since {h.since}</small></>],
      ["gate now", !started ? "–" : (
        <span className={tick.gate_answer === "clears" ? "robot-pass" : undefined}>
          <span className="robot-nowrap">{GATE_SHORT[tick.gate_answer]}</span><code>{tick.gate_answer}</code></span>
      )],
    ]} />
  );
}

function Projection({ robot, decision, now }: {
  robot: RobotDescription; decision: DecisionMade | null; now: number | null;
}) {
  if (decision === null) return <p className="human-none">–</p>;
  const p = decision.projection;
  if (p.kind === "none") return <Facts items={[["kind", p.reason === "no_human" ? "none · no human" : "none · unassessed"]]} />;
  const over = now !== null && now > p.until;
  const end = <>to {tickText(p.until)}{over && <span className="robot-chip">ran out</span>}</>;
  if (p.kind === "fallback") {
    return <Facts items={[["fallback", <>{p.mode} · {tickText(p.span)} ticks · {end}</>]]} />;
  }
  return (
    <Facts items={[
      ["admitted", <><span className="human-task">{keyText(robot, p.hypothesis)}</span> · {end}</>],
      ["plan", <span className="human-task">{p.plan.map((a) => actionText(a)).join(" › ")}</span>],
    ]} />
  );
}

function Decisions({ robot, decision, ticks }: {
  robot: RobotDescription; decision: DecisionMade | null; ticks: readonly TickUpdate[];
}) {
  if (decision === null) return <p className="human-none">–</p>;
  const earlier = recentDecisions(ticks, robot.robot, EARLIER + 1).filter((d) => d.tick !== decision.tick)
    .slice(0, EARLIER);
  const task = (d: DecisionMade) => d.chosen === null ? CHANGE_SHORT.finishes
    : <>{CHANGE_SHORT[d.change]} <span className="human-task">{taskText(d.chosen)}</span></>;
  return (
    <>
      <Facts items={[
        ["tick", <>{decision.tick} · {TRIGGER_SHORT[decision.trigger]}{decision.cause !== null
          && ` · ${CAUSE_SHORT[decision.cause]}`}</>],
        ["task", task(decision)],
        ["hold", decision.hold === 0 ? "–" : `${decision.hold} ticks`],
        ["queue", decision.queue.length === 0 ? "–"
          : <span className="human-task">{decision.queue.map((t) => taskText(t)).join(", ")}</span>],
        ["admission", robot.condition === "human-unaware" ? "off" : admissionText(decision)],
      ]} />
      {earlier.length > 0 && (
        <ol className="human-changes robot-earlier">
          {earlier.map((d) => (
            <li key={d.tick}>
              <span className="human-tick">{d.tick}</span>
              <span>{TRIGGER_SHORT[d.trigger]}{d.cause !== null ? ` · ${CAUSE_SHORT[d.cause]}` : ""} · {task(d)}
                {d.hold > 0 ? ` · hold ${d.hold}` : ""}</span>
            </li>
          ))}
        </ol>
      )}
    </>
  );
}
