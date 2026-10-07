/**
 * The past view (T-viz 1c; Hadi, 7 October 2026, preferred): what the page reads to show an earlier tick. The page
 * holds a sim-run as the sequence of its tick updates, the start's first; at tick k it held the updates up to and
 * including tick k's, and the env-pane and the side panels read nothing else. So the view of tick k is that prefix:
 * what the page showed when the sim-run was at tick k. Display only; nothing is asked of the server.
 */

import type { TickUpdate } from "../gen/messages";

/** The tick updates up to the viewed tick's (all of them when none is viewed, or the viewed tick is not yet held). */
export function viewedTicks(ticks: readonly TickUpdate[], viewed: number | null): readonly TickUpdate[] {
  if (viewed === null || viewed + 2 > ticks.length) return ticks;
  return ticks.slice(0, viewed + 2);
}
