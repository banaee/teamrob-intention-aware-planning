/**
 * Panel 4a's reading of a human's activity (src/frame/activity.ts; plan_T-viz_1a.md, section 4, "What panel 4a
 * shows"): the action as written, the stack top first with the task below suspended, the last switches and
 * resumptions newest first with their ticks, and where a switch cut the task below it.
 */

import { describe, expect, it } from "vitest";

import type { TickUpdate } from "../src/gen/messages";
import { actionText, recentChanges, stackLines, whereText } from "../src/frame/activity";

const task = (label: string) => ({ task: label.split("(")[0], bindings: [], label });
const act = (action: string, ...values: string[]) =>
  ({ action, bindings: values.map((value, i) => ({ parameter: `?p${i}`, value })) });
const A = task("work(?x=a)");
const B = task("rest(?y=b)");

function update(tick: number | null, human: string, stack: ReturnType<typeof task>[], transitions: object[]) {
  return { tick, world: { activity: [{ human, stack, action: null, transitions, open_entries: [] }] } } as unknown as TickUpdate;
}

const ticks = [
  update(null, "h", [], []),
  update(0, "h", [A], [{ kind: "entered", task: A }]),
  update(7, "h", [B, A], [{ kind: "left", task: A, outcome: "suspended" },
                          { kind: "started", task: B, trigger: { kind: "now" },
                            where: { kind: "cut", action: act("walk", "h", "spot"), occurrence: 0, done: 4 } }]),
  update(9, "other", [B], [{ kind: "started", task: B, trigger: { kind: "now" }, where: null }]),
  update(12, "h", [A], [{ kind: "left", task: B, outcome: "completed" }, { kind: "resumed", task: A }]),
];

describe("the panel's reading", () => {
  it("writes an action with its bindings' values", () => {
    expect(actionText(act("lift", "h", "box_1"))).toBe("lift(h, box_1)");
  });

  it("reads the stack top first, the task below the top suspended", () => {
    expect(stackLines({ human: "h", stack: [B, A], action: null, transitions: [], open_entries: [] }))
      .toEqual([{ task: B, suspended: false }, { task: A, suspended: true }]);
  });

  it("lists the human's own switches and resumptions, newest first, with their ticks", () => {
    expect(recentChanges(ticks, "h", 5)).toEqual([
      { kind: "resumption", tick: 12, task: A },
      { kind: "switch", tick: 7, task: B, below: A,
        where: { kind: "cut", action: act("walk", "h", "spot"), occurrence: 0, done: 4 } },
    ]);
    expect(recentChanges(ticks, "h", 1)).toHaveLength(1);
    expect(recentChanges(ticks, "other", 5)).toEqual([{ kind: "switch", tick: 9, task: B, below: null, where: null }]);
    expect(recentChanges(ticks.slice(0, 2), "h", 5)).toEqual([]);      // an entry taken onto the stack is no switch
  });

  it("says where a switch cut the task below it", () => {
    expect(whereText(null)).toBe("on the empty stack");
    expect(whereText({ kind: "beginning" })).toBe("before its first action");
    expect(whereText({ kind: "boundary", action: act("lift", "h", "box_1"), occurrence: 0 })).toBe("after lift(h, box_1)");
    expect(whereText({ kind: "cut", action: act("walk", "h", "spot"), occurrence: 0, done: 1 }))
      .toBe("inside walk(h, spot), 1 tick done");
  });
});
