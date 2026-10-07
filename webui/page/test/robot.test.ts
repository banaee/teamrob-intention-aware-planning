/**
 * Panel 4b's reading of the robot (src/frame/robot.ts; plan_T-viz_1b.md; Hadi's review, 7 October 2026): a label for
 * every gate answer, trigger, cause and change of task the messages declare; admission's first part, what the robot
 * holds since its last decision; the rows of the belief chart, each hypothesis keeping its row; a hypothesis written by
 * its values; a decision's admission; the last decisions newest first, one per tick that took one.
 */

import { describe, expect, it } from "vitest";

import schema from "../src/gen/messages.schema.json";
import type { DecisionMade, RobotDescription, TickUpdate } from "../src/gen/messages";
import {
  admissionText, beliefRows, CAUSE_SHORT, CHANGE_SHORT, GATE_SHORT, held, keyText, recentDecisions, tickText,
  TRIGGER_SHORT,
} from "../src/frame/robot";

const values = (name: string): string[] => (schema.$defs as Record<string, { enum?: string[] }>)[name].enum ?? [];

const decision = (tick: number, over: Partial<DecisionMade> = {}): DecisionMade => ({
  tick, trigger: "no_current_task", cause: null, gate_answer: "none(below_theta)",
  projection: { kind: "fallback", mode: "standing", span: 1, until: tick }, change: "starts",
  chosen: { task: "work", bindings: [], label: "work()" }, hold: 0, queue: [], ...over,
}) as DecisionMade;
const admitted = (tick: number, hypothesis: string) =>
  decision(tick, { gate_answer: "clears", projection: { kind: "admitted", hypothesis, plan: [], until: tick + 9 } });

const update = (tick: number | null, d: DecisionMade | null) =>
  ({ tick, robots: [{ robot: "r", decision: d, belief: null }] }) as unknown as TickUpdate;
const live = (tick: number, ...keys: string[]) =>
  ({ tick, robots: [{ robot: "r", decision: null, belief: { live: keys.map((key) => ({ key })) } }] }) as
    unknown as TickUpdate;

describe("panel 4b's reading", () => {
  it("has a label for every value the messages declare", () => {
    expect(Object.keys(GATE_SHORT).sort()).toEqual(values("Gate").sort());
    expect(Object.keys(TRIGGER_SHORT).sort()).toEqual(values("TriggerKind").sort());
    expect(Object.keys(CAUSE_SHORT).sort()).toEqual(values("Cause").sort());
    expect(Object.keys(CHANGE_SHORT).sort()).toEqual(values("TaskChange").sort());
  });

  it("reads what the robot holds since its last decision: the admitted hypothesis, or none", () => {
    expect(held(null)).toBeNull();
    expect(held(admitted(4, "h"))).toEqual({ since: 4, hypothesis: "h" });
    expect(held(decision(9))).toEqual({ since: 9, hypothesis: null });
    expect(held(decision(9, { gate_answer: "clears" }))).toEqual({ since: 9, hypothesis: null });
  });

  it("keeps every hypothesis in the row it first had, in the order first live, those of one tick by key", () => {
    const ticks = [update(null, null), live(0, "b", "a"), live(1, "a"), live(2, "c", "a"), live(3, "b")];
    expect(beliefRows(ticks, "r")).toEqual(["a", "b", "c"]);
    expect(beliefRows(ticks.slice(0, 2), "r")).toEqual(["a", "b"]);
    expect(beliefRows([live(0, "z"), live(1, "a", "z")], "r")).toEqual(["z", "a"]);
    expect(beliefRows(ticks, "other")).toEqual([]);
  });

  it("writes a hypothesis by its values, and an unknown key as it is", () => {
    const robot = { hypotheses: [{ key: "work(?x=a)", task: "work", bindings: [{ parameter: "?x", value: "a" }] }] } as
      unknown as RobotDescription;
    expect(keyText(robot, "work(?x=a)")).toBe("work(a)");
    expect(keyText(robot, "rest()")).toBe("rest()");
  });

  it("writes a decision's admission", () => {
    expect(admissionText(admitted(3, "h"))).toBe("admitted");
    expect(admissionText(decision(3, { gate_answer: "clears" }))).toBe("passes, not projectable");
    expect(admissionText(decision(3))).toBe(GATE_SHORT["none(below_theta)"]);
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
