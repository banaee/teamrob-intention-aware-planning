/**
 * Panel 4b's reading of the robot (T-viz 1b; docs/handoffs/plan_T-viz_1b.md; Hadi's review, 7 October 2026): short
 * labels for the gate's answers, the triggers, their causes and what a decision did to the task, in the glossary's
 * words; the admission block's two parts (what the robot holds since its last decision, and the gate's answer at the
 * tick); the rows of the belief chart, each hypothesis keeping its row; the last decisions. Everything is read from the
 * run description and the tick updates; the page decides nothing: the gate's answer, the projection and the decision
 * are the robot's, as the simulator's side sends them. No domain word: tasks, hypotheses and actions arrive as data.
 */

import type {
  Cause, DecisionMade, Gate, Hypothesis, RobotDescription, TaskChange, TickUpdate, TriggerKind,
} from "../gen/messages";

/** The gate's answer, short; the log's code is shown small beside it. */
export const GATE_SHORT: Record<Gate, string> = {
  "clears": "passes",
  "none(no_human)": "no human",
  "none(intention_off)": "intention off",
  "none(below_theta)": "below θ",
  "none(leader_no_observation)": "leader not observed",
  "none(leader_inadequate)": "leader inadequate",
  "none(leader_unwarranted)": "leader unwarranted",
  "none(leader_outranked)": "leader outranked",
};

/** The two kinds of the robot's projection of the human, named for a lay viewer wherever the page names them, the
 * scene's switches and panel 4b alike (Hadi, 7 October 2026, preferred): the admitted projection is the prediction
 * from intention, the fallback projection the prediction from motion. Labels only: the glossary's terms are unchanged. */
export const PREDICTION: Record<"admitted" | "fallback", string> = {
  admitted: "Prediction from intention",
  fallback: "Prediction from motion",
};

export const TRIGGER_SHORT: Record<TriggerKind, string> = {
  no_current_task: "no current task",
  recognition_changed: "recognition changed",
  projection_expired: "projection expired",
};

export const CAUSE_SHORT: Record<Cause, string> = {
  entered: "entered",
  replaced: "replaced",
  boundary: "boundary",
  retraction: "retraction",
};

export const CHANGE_SHORT: Record<TaskChange, string> = {
  starts: "starts",
  continues: "continues",
  switches: "switches to",
  finishes: "all done",
};

/** A hypothesis written by its values, as panel 4a writes a task: `name(value, value)`. */
export function hypothesisText(h: Hypothesis): string {
  return `${h.task}(${h.bindings.map((b) => b.value).join(", ")})`;
}

/** The hypothesis of a key, written by its values; the key itself when the space does not hold it. */
export function keyText(robot: RobotDescription, key: string): string {
  const h = robot.hypotheses.find((x) => x.key === key);
  return h === undefined ? key : hypothesisText(h);
}

/** Admission's first part: what the robot holds since its last decision (the decision record): the hypothesis that
 * decision admitted, or none; with the decision's tick. Null before the first decision. */
export interface Held {
  since: number;
  hypothesis: string | null;
}

export function held(decision: DecisionMade | null): Held | null {
  if (decision === null) return null;
  return { since: decision.tick, hypothesis: decision.projection.kind === "admitted" ? decision.projection.hypothesis : null };
}

/** A decision's admission, short: admitted; or the gate's answer; or, where the leader passed and no plan was
 * admitted, that its plan could not be projected. */
export function admissionText(d: DecisionMade): string {
  if (d.gate_answer === "clears") return d.projection.kind === "admitted" ? "admitted" : "passes, not projectable";
  return GATE_SHORT[d.gate_answer];
}

/** The rows of the belief chart up to the last tick update: every hypothesis live at some tick so far, in the order in
 * which it was first live (those first live on one tick by key), so that a row never moves during a sim-run. */
export function beliefRows(ticks: readonly TickUpdate[], robot: string): string[] {
  const rows: string[] = [];
  for (const update of ticks) {
    const belief = update.robots.find((r) => r.robot === robot)?.belief;
    if (!belief) continue;
    const fresh = belief.live.map((h) => h.key).filter((k) => !rows.includes(k)).sort();
    rows.push(...fresh);
  }
  return rows;
}

/** A tick on the projection clock, written whole where it is whole, else to one decimal. */
export function tickText(t: number): string {
  return Number.isInteger(t) ? `${t}` : t.toFixed(1);
}

/** A robot's last `n` decisions, newest first: the decision of every tick update that took one on its own tick. */
export function recentDecisions(ticks: readonly TickUpdate[], robot: string, n: number): DecisionMade[] {
  const found: DecisionMade[] = [];
  for (let i = ticks.length - 1; i >= 0 && found.length < n; i--) {
    const update = ticks[i];
    const r = update.robots.find((x) => x.robot === robot);
    if (r?.decision && r.decision.tick === update.tick) found.push(r.decision);
  }
  return found;
}
