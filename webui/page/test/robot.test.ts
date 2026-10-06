/**
 * Panel 4b's reading of the robot (src/frame/robot.ts; plan_T-viz_1b.md): a phrase for every gate answer, trigger,
 * cause and change of task the messages declare; the live hypotheses highest first; a hypothesis written by its values;
 * the admission of a decision whose leader passed but whose plan was not admitted; the last decisions newest first,
 * one per tick that took one.
 */

import { describe, expect, it } from "vitest";

import schema from "../src/gen/messages.schema.json";
import type { DecisionMade, RobotBelief, RobotDescription, TickUpdate } from "../src/gen/messages";
import {
  admissionText, CAUSE_PHRASE, CHANGE_PHRASE, conditionNote, GATE_PHRASE, keyText, liveRows, recentDecisions,
  tickText, TRIGGER_PHRASE,
} from "../src/frame/robot";

const values = (name: string): string[] => (schema.$defs as Record<string, { enum?: string[] }>)[name].enum ?? [];

const live = (key: string, belief: number) => ({
  key, belief, prior: null, adequacy: "adequate", tail: 1, warrant: "observation", rank: "not_outranked",
});

const decision = (tick: number, over: Partial<DecisionMade> = {}): DecisionMade => ({
  tick, trigger: "no_current_task", cause: null, gate_answer: "none(below_theta)",
  projection: { kind: "fallback", mode: "standing", span: 1, until: tick }, change: "starts",
  chosen: { task: "work", bindings: [], label: "work()" }, hold: 0, queue: [], ...over,
}) as DecisionMade;

const update = (tick: number | null, d: DecisionMade | null) =>
  ({ tick, robots: [{ robot: "r", decision: d }] }) as unknown as TickUpdate;

describe("panel 4b's reading", () => {
  it("has a phrase for every value the messages declare", () => {
    expect(Object.keys(GATE_PHRASE).sort()).toEqual(values("Gate").sort());
    expect(Object.keys(TRIGGER_PHRASE).sort()).toEqual(values("TriggerKind").sort());
    expect(Object.keys(CAUSE_PHRASE).sort()).toEqual(values("Cause").sort());
    expect(Object.keys(CHANGE_PHRASE).sort()).toEqual(values("TaskChange").sort());
    for (const c of values("RobotCondition")) expect(conditionNote(c as never) === null).toBe(c === "intention-aware");
  });

  it("orders the live hypotheses by belief, highest first, ties by key", () => {
    const belief = { live: [live("b", 0.2), live("c", 0.5), live("a", 0.2)] } as unknown as RobotBelief;
    expect(liveRows(belief).map((h) => h.key)).toEqual(["c", "a", "b"]);
  });

  it("writes a hypothesis by its values, and an unknown key as it is", () => {
    const robot = { hypotheses: [{ key: "work(?x=a)", task: "work", bindings: [{ parameter: "?x", value: "a" }] }] } as
      unknown as RobotDescription;
    expect(keyText(robot, "work(?x=a)")).toBe("work(a)");
    expect(keyText(robot, "rest()")).toBe("rest()");
  });

  it("says when the leader passed the gate but no plan was admitted", () => {
    expect(admissionText(decision(3, { gate_answer: "clears" }))).toMatch(/cannot be projected/);
    expect(admissionText(decision(3, {
      gate_answer: "clears", projection: { kind: "admitted", hypothesis: "h", plan: [], until: 9 },
    }))).toBe("the leader was admitted");
    expect(admissionText(decision(3))).toBe(GATE_PHRASE["none(below_theta)"]);
  });

  it("writes a whole tick whole, else to one decimal", () => {
    expect(tickText(12)).toBe("12");
    expect(tickText(12.34)).toBe("12.3");
  });

  it("reads the last decisions newest first, one per tick that took one", () => {
    const d0 = decision(0), d4 = decision(4, { trigger: "projection_expired" }), d7 = decision(7);
    const ticks = [update(null, null), update(0, d0), update(1, d0), update(4, d4), update(5, d4), update(7, d7)];
    expect(recentDecisions(ticks, "r", 5).map((d) => d.tick)).toEqual([7, 4, 0]);
    expect(recentDecisions(ticks, "r", 2).map((d) => d.tick)).toEqual([7, 4]);
    expect(recentDecisions(ticks, "other", 5)).toEqual([]);
  });
});
