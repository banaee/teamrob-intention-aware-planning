/**
 * Panel 4b, the robot at the tick (T-viz 1b; docs/handoffs/plan_T-viz_1b.md). Per robot, under its id in the robot's
 * colour, five blocks in the order of the chain from recognition to planning (Hadi, 6 October 2026, preferred):
 *   (1) Body: its task, the action at its plan's cursor with its progress, the microaction of the tick, what it carries,
 *       a hold in progress;
 *   (2) Belief: the belief over the live hypotheses, highest first, θ marked, with each hypothesis's adequacy, warrant,
 *       rank, tail probability and prior; the levels and recency facts with context knowledge on;
 *   (3) Admission: the gate's answer for the leader at the tick, and the hypothesis the last decision rests on;
 *   (4) Projection: what the last decision expected the human to do;
 *   (5) Decision: the last decision, then the ones before it.
 * The page decides nothing: every answer is the robot's, as the simulator's side sends it (src/frame/robot.ts).
 */

import type {
  Carried, DecisionMade, RobotBelief, RobotDescription, RobotTick, TickUpdate,
} from "../gen/messages";
import { actionText, taskText } from "./activity";
import {
  admissionText, CAUSE_PHRASE, CHANGE_PHRASE, conditionNote, GATE_PHRASE, keyText, liveRows, recentDecisions,
  tickText, TRIGGER_PHRASE,
} from "./robot";

const RECENT = 5;

export function RobotPanel({ robots, ticks }: {
  robots: readonly RobotDescription[]; ticks: readonly TickUpdate[] | null;
}) {
  const now = ticks === null ? null : ticks[ticks.length - 1];
  return (
    <aside className="panel panel-robot" aria-label="The robot: its body and its mind">
      <h2 className="panel-title">The robot</h2>
      {now === null || robots.length === 0 ? (
        <p className="panel-later">No sim-run: what the robot believes and decides shows once a scenario is chosen.</p>
      ) : robots.map((robot) => {
        const tick = now.robots.find((r) => r.robot === robot.robot);
        return tick ? <Robot key={robot.robot} robot={robot} tick={tick} now={now} ticks={ticks!} /> : null;
      })}
    </aside>
  );
}

function Robot({ robot, tick, now, ticks }: {
  robot: RobotDescription; tick: RobotTick; now: TickUpdate; ticks: readonly TickUpdate[];
}) {
  const note = conditionNote(robot.condition);
  const started = now.tick !== null;
  return (
    <section className="robot">
      <h3 className="human-id"><span className="panel-dot robot-dot" />{robot.robot}</h3>
      {note !== null && <p className="robot-condition">{note}</p>}
      <Body tick={tick} carried={now.world.carried.filter((c) => c.agent === robot.robot)} />
      <h4 className="human-heading">Belief <small>over the human's tasks</small></h4>
      {robot.condition !== "intention-aware" ? <p className="human-none">does not apply</p>
        : tick.belief === null ? <p className="human-none">{started ? "no belief" : "no observation yet"}</p>
        : <Belief robot={robot} belief={tick.belief} />}
      <h4 className="human-heading">Admission <small>θ = {robot.theta}</small></h4>
      <Admission robot={robot} tick={tick} started={started} />
      <h4 className="human-heading">Projection <small>of the human, the last decision's</small></h4>
      <Projection robot={robot} decision={tick.decision} now={now.tick} />
      <h4 className="human-heading">Decision</h4>
      <Decisions robot={robot} decision={tick.decision} ticks={ticks} />
    </section>
  );
}

/** (1) The body. */
function Body({ tick, carried }: { tick: RobotTick; carried: readonly Carried[] }) {
  const { task, action, microaction, hold, finished } = tick.body;
  return (
    <>
      <h4 className="human-heading">Body</h4>
      {finished ? <p className="human-none">all its tasks are complete; it still observes</p> : (
        <p className="human-of">task <span className="human-task">{task === null ? "none" : taskText(task)}</span></p>
      )}
      {action !== null && (
        <>
          <p className="human-action">{actionText(action.action)}</p>
          <div className="human-progress">
            <span className="human-bar robot-bar" aria-hidden>
              <span style={{ width: `${action.total > 0 ? (100 * action.done) / action.total : 0}%` }} />
            </span>
            <span className="human-ticks">
              {action.total === 0 ? "not begun" : `${action.done} of ${action.total} ticks`}
            </span>
          </div>
        </>
      )}
      <dl className="robot-facts">
        <div><dt>this tick</dt><dd>{microaction ?? "no microaction"}</dd></div>
        <div><dt>carries</dt><dd>{carried.length === 0 ? "nothing" : carried.map((c) => c.movable_object).join(", ")}</dd></div>
        <div><dt>hold</dt><dd>{hold === null ? "none" : (
          <span className="robot-hold">stood {hold.stood} of {hold.planned} ticks, decided at tick {hold.decided_at}</span>
        )}</dd></div>
      </dl>
    </>
  );
}

/** (2) The belief over the live hypotheses. */
function Belief({ robot, belief }: { robot: RobotDescription; belief: RobotBelief }) {
  const rows = liveRows(belief);
  const notLive = robot.hypotheses.length - belief.live.length;
  return (
    <>
      <p className="robot-summary">
        {belief.lifecycle === "exhausted" ? "exhausted: no hypothesis is live"
          : <>finding <b>{belief.finding}</b></>}
        {belief.boundary && <span className="robot-flag">episode boundary</span>}
      </p>
      <ol className="belief">
        {rows.map((h) => (
          <li key={h.key} className={h.key === belief.leader ? "is-leader" : undefined}>
            <div className="belief-head">
              <span className="human-task">{keyText(robot, h.key)}</span>
              <span className="belief-value">{h.belief.toFixed(3)}</span>
            </div>
            <span className="belief-bar" aria-hidden>
              <span style={{ width: `${100 * h.belief}%` }} />
              <i style={{ left: `${100 * robot.theta}%` }} />
            </span>
            <div className="belief-marks">
              <span className={`mark-${h.adequacy}`}>{h.adequacy.replace("_", " ")}</span>
              <span className={h.warrant === "observation" ? "" : "mark-faint"}>
                {h.warrant === "observation" ? "warranted" : "no warrant"}</span>
              {h.rank === "outranked" && <span className="mark-outranked">outranked</span>}
              {h.tail !== null && <span title="tail probability of the adequacy test">S {h.tail.toFixed(3)}</span>}
              {h.prior !== null && <span title="prior from context knowledge">prior {h.prior.toFixed(3)}</span>}
            </div>
          </li>
        ))}
      </ol>
      {belief.levels.length > 0 && (
        <p className="robot-note">levels: {belief.levels.map((l) => `${l.task} ${l.level}`).join(", ")}</p>
      )}
      {robot.context_knowledge && (
        <p className="robot-note">recently completed (its memory): {belief.recent.length === 0 ? "none"
          : belief.recent.join(", ")}</p>
      )}
      <p className="robot-note">
        {notLive > 0 && <>{notLive} other {notLive === 1 ? "hypothesis is" : "hypotheses are"} not live. </>}
        {robot.known_assigned === null ? "It is not told the human's assigned tasks."
          : `It is told the human's assigned tasks: ${robot.known_assigned.map(taskText).join(", ") || "none"}.`}
      </p>
    </>
  );
}

/** (3) The gate's answer at the tick, and what the last decision rests on. */
function Admission({ robot, tick, started }: { robot: RobotDescription; tick: RobotTick; started: boolean }) {
  if (robot.condition === "human-unaware") return <p className="human-none">does not apply</p>;
  const leader = tick.belief?.leader ?? null;
  const rests = tick.decision?.projection.kind === "admitted" ? tick.decision.projection.hypothesis : null;
  return (
    <>
      {!started ? <p className="human-none">no observation yet</p> : (
        <p className={`robot-gate ${tick.gate_answer === "clears" ? "is-clear" : "is-refused"}`}>
          {tick.gate_answer === "clears" ? "passes" : "refused"}: {GATE_PHRASE[tick.gate_answer]}
          {leader !== null && tick.belief !== null && <> ({keyText(robot, leader)}, {tick.belief.confidence.toFixed(3)})</>}
          <code>{tick.gate_answer}</code>
        </p>
      )}
      <p className="robot-note">
        The gate is asked at a decision; this is its answer now.
        {tick.decision !== null && (rests === null ? " The last decision rests on no admitted hypothesis."
          : <> The last decision rests on <span className="human-task">{keyText(robot, rests)}</span>.</>)}
      </p>
    </>
  );
}

/** (4) What the last decision expected the human to do. */
function Projection({ robot, decision, now }: {
  robot: RobotDescription; decision: DecisionMade | null; now: number | null;
}) {
  if (robot.condition === "human-unaware") return <p className="human-none">does not apply</p>;
  if (decision === null) return <p className="human-none">no decision yet</p>;
  const p = decision.projection;
  const over = now !== null && p.kind !== "none" && now > p.until;
  if (p.kind === "none") {
    return <p className="robot-proj">{p.reason === "no_human" ? "none: no human observed"
      : "none: no previous observation of the human (unassessed)"}</p>;
  }
  if (p.kind === "fallback") {
    return (
      <>
        <p className="robot-proj"><span className="robot-kind">fallback</span>
          {p.mode === "standing" ? "the human stays where it was seen" : "the human walks straight on"},
          for {tickText(p.span)} ticks, to tick {tickText(p.until)}</p>
        <p className="robot-note">
          {over ? `Ran out after tick ${tickText(p.until)}. ` : ""}
          From tick {decision.tick}, admission refused: {GATE_PHRASE[decision.gate_answer]}.
          After its end the decision is taken again (the fallback projection ran out), unless another trigger fires
          first.
        </p>
      </>
    );
  }
  return (
    <>
      <p className="robot-proj"><span className="robot-kind robot-kind-admitted">admitted</span>
        <span className="human-task">{keyText(robot, p.hypothesis)}</span>, to tick {tickText(p.until)}</p>
      <ol className="robot-plan">
        {p.plan.map((a, i) => <li key={i} className="human-task">{actionText(a)}</li>)}
      </ol>
      <p className="robot-note">From tick {decision.tick}.{over
        ? ` Ran out after tick ${tickText(p.until)}: nothing past its end is assessed.` : ""}</p>
    </>
  );
}

/** (5) The last decision, then the ones before it. */
function Decisions({ robot, decision, ticks }: {
  robot: RobotDescription; decision: DecisionMade | null; ticks: readonly TickUpdate[];
}) {
  if (decision === null) return <p className="human-none">no decision yet</p>;
  const earlier = recentDecisions(ticks, robot.robot, RECENT + 1).filter((d) => d.tick !== decision.tick).slice(0, RECENT);
  return (
    <>
      <p className="robot-decision">
        <span className="human-tick">tick {decision.tick}</span> {TRIGGER_PHRASE[decision.trigger]}
        {decision.cause !== null && <>: {CAUSE_PHRASE[decision.cause]}</>}
        <code>{decision.trigger}{decision.cause !== null ? ` ${decision.cause}` : ""}</code>
      </p>
      <dl className="robot-facts">
        <div><dt>task</dt><dd>{decision.chosen === null ? CHANGE_PHRASE.finishes : (
          <>{CHANGE_PHRASE[decision.change]} <span className="human-task">{taskText(decision.chosen)}</span></>
        )}</dd></div>
        <div><dt>hold</dt><dd>{decision.hold === 0 ? "none" : `${decision.hold} ticks`}</dd></div>
        <div><dt>queue</dt><dd>{decision.queue.length === 0 ? "empty"
          : decision.queue.map((t) => taskText(t)).join(", ")}</dd></div>
        <div><dt>admission</dt><dd>{robot.condition === "human-unaware" ? "does not apply" : admissionText(decision)}</dd></div>
      </dl>
      {earlier.length > 0 && (
        <ol className="human-changes robot-earlier">
          {earlier.map((d) => (
            <li key={d.tick}>
              <span className="human-tick">tick {d.tick}</span>
              <span>{TRIGGER_PHRASE[d.trigger]}{d.cause !== null ? ` (${d.cause})` : ""}: {d.chosen === null
                ? "finished" : <>{CHANGE_PHRASE[d.change]} <span className="human-task">{taskText(d.chosen)}</span></>}
                {d.hold > 0 ? `, hold ${d.hold}` : ""}</span>
            </li>
          ))}
        </ol>
      )}
    </>
  );
}
