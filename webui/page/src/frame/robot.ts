/**
 * Panel 4b's reading of the robot (T-viz 1b; docs/handoffs/plan_T-viz_1b.md): plain phrases for the gate's answers,
 * the triggers, their causes and what a decision did to the task, in the glossary's words (§2, §5, §7, §9); the live
 * hypotheses in the order the panel shows them; the last decisions. Everything is read from the run description and
 * the tick updates; the page decides nothing: the gate's answer, the projection and the decision are the robot's, as
 * the simulator's side sends them. No domain word: tasks, hypotheses and actions arrive as data.
 */

import type {
  Cause, DecisionMade, Gate, Hypothesis, HypothesisBelief, RobotBelief, RobotCondition, RobotDescription, TaskChange,
  TickUpdate, TriggerKind,
} from "../gen/messages";

/** The gate's answer as a short phrase; the log's code is shown small beside it. */
export const GATE_PHRASE: Record<Gate, string> = {
  "clears": "the leader passes the gate",
  "none(no_human)": "no human observed",
  "none(intention_off)": "intention-unaware: the gate admits nothing",
  "none(below_theta)": "the leader's belief is below θ",
  "none(leader_no_observation)": "nothing observed yet of the leader's current phase",
  "none(leader_inadequate)": "the leader does not explain what is observed (inadequate)",
  "none(leader_unwarranted)": "no observation warrant for the leader",
  "none(leader_outranked)": "the evidence alone ranks another hypothesis above the leader",
};

export const TRIGGER_PHRASE: Record<TriggerKind, string> = {
  no_current_task: "no current task",
  recognition_changed: "recognition changed",
  projection_expired: "the fallback projection ran out",
};

export const CAUSE_PHRASE: Record<Cause, string> = {
  entered: "a hypothesis passed the gate",
  replaced: "the leader changed",
  boundary: "the human's task ended (episode boundary)",
  retraction: "retraction: the admitted hypothesis became inadequate",
};

export const CHANGE_PHRASE: Record<TaskChange, string> = {
  starts: "starts",
  continues: "continues",
  switches: "switches to",
  finishes: "all its tasks are complete",
};

/** What a robot in a condition other than the framework as designed does not do, in plain words; null as designed. */
export function conditionNote(condition: RobotCondition): string | null {
  switch (condition) {
    case "intention-aware": return null;
    case "intention-unaware":
      return "Intention-unaware: the robot observes where the human is and how it moves, but the recognizer does not "
        + "run. It holds no belief, and the gate admits nothing.";
    case "human-unaware":
      return "Human-unaware: the robot does not take the human into account. It holds no belief, admits nothing and "
        + "projects nothing.";
  }
}

/** A hypothesis written by its values, as panel 4a writes a task: `name(value, value)`. */
export function hypothesisText(h: Hypothesis): string {
  return `${h.task}(${h.bindings.map((b) => b.value).join(", ")})`;
}

/** The hypothesis of a key, written by its values; the key itself when the space does not hold it. */
export function keyText(robot: RobotDescription, key: string): string {
  const h = robot.hypotheses.find((x) => x.key === key);
  return h === undefined ? key : hypothesisText(h);
}

/** The live hypotheses, highest belief first, ties by key. */
export function liveRows(belief: RobotBelief): HypothesisBelief[] {
  return [...belief.live].sort((a, b) => b.belief - a.belief || (a.key < b.key ? -1 : a.key > b.key ? 1 : 0));
}

/** The decision's admission in words: the gate's phrase, or, where the leader passed and no plan was admitted, that its
 * plan could not be projected. */
export function admissionText(d: DecisionMade): string {
  if (d.gate_answer === "clears" && d.projection.kind !== "admitted") {
    return "the leader passes the gate, but its plan cannot be projected";
  }
  return d.gate_answer === "clears" ? "the leader was admitted" : GATE_PHRASE[d.gate_answer];
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
