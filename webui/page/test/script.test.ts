/**
 * The human's script in panel 4a (src/frame/script.ts): the state of each script line over a sim-run, in panel 4a's
 * four reference cases (a task in progress; an interruption after an action; an interruption inside an action; a
 * resumption), derived by the page from the messages, equals the state read from the human executor's own state
 * (tests/tviz_panel_cases.py, which writes the fixtures under tests/fixtures/tviz_panel/ and checks them).
 */

import { readdirSync, readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

import { scriptLines } from "../src/frame/script";
import type { HumanScript, TickUpdate } from "../src/gen/messages";

const DIR = new URL("../../../tests/fixtures/tviz_panel/", import.meta.url);
const cases = readdirSync(DIR).filter((f) => f.endsWith(".json"));

describe("the script's lines over a sim-run", () => {
  it("has the four reference cases", () => expect(cases).toHaveLength(4));

  for (const file of cases) {
    it(`agree with the executor's state at every tick: ${file}`, () => {
      const c = JSON.parse(readFileSync(new URL(file, DIR), "utf8"));
      const script = c.script as HumanScript;
      const ticks = (c.ticks as { tick: number | null; activity: object }[])
        .map((t) => ({ tick: t.tick, world: { activity: [t.activity] } }) as unknown as TickUpdate);
      const seen = new Set<string>();
      ticks.forEach((_, n) => {
        const got: Record<string, string> = {};
        for (const line of scriptLines(script, ticks.slice(0, n + 1))) {
          const key = line.kind === "entry" ? `entry ${line.position.part} ${line.position.index}`
            : `event ${line.position.entry.part} ${line.position.entry.index} ${line.position.index}`;
          got[key] = line.state;
          seen.add(line.state);
        }
        expect(got, `${file} at tick ${ticks[n].tick}`).toEqual(c.truth[n]);
      });
      expect([...seen]).toEqual(expect.arrayContaining(["open", "in progress", "suspended", "completed", "pending"]));
    });
  }
});
