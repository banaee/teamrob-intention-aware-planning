/**
 * The first drafts of the sim-runs on slides (T-pres, task B of 8 October 2026; before part 4 is planned): existing
 * scenarios and T-F part 1's own run files only, recorded at every build (scripts/record.mjs, RUNS). Each stop is a
 * tick and a caption; every caption states what the run's log shows at that tick (the recognizer's leader and its
 * belief, the gate, the decision, the hold, the human's record), in the talk's words.
 */

import s1 from "../../data/run_stage1_alone.json";
import s2 from "../../data/run_stage2_reactive.json";
import s3 from "../../data/run_stage3_hold.json";
import s4 from "../../data/run_stage4_break.json";
import s5 from "../../data/run_stage5_breaktime.json";
import s6 from "../../data/run_stage6_switch.json";
import s7 from "../../data/run_stage7_stand.json";
import { type RecordedRun, ReplayView, type Stop } from "../scene/RunReplay";

const run = (r: unknown) => r as RecordedRun;   // the JSON's enumerations are read as strings

/** Talk stage 1: kitting scenario_s12_01, human-unaware (T-F part 1's run_057): Anton's two deliveries; the human is
 * not drawn (the robot's mind receives no human in this condition). */
export function ReplayAlone() {
  const stops: Stop[] = [
    { tick: 0, caption: "Anton chooses a task, deliver item 7, and plans its actions." },
    { tick: 30, caption: "It executes them, one at a time: the dashed line is what is left of its plan." },
    { tick: 63, caption: "Item 7 delivered: it chooses the next task, deliver item 13." },
    { tick: 126, caption: "Both delivered." },
  ];
  return <ReplayView recorded={run(s1)} stops={stops} hideHumans />;
}

/** Talk stage 2: scenario_s10_02, intention-unaware (run_006): the projection from her motion and a hold of 5 ticks. */
export function ReplayReactive() {
  const stops: Stop[] = [
    { tick: 24, caption: "Anton knows nothing of her task: it projects her motion (the hatched blue stripe)." },
    { tick: 40, caption: "Its path would come too close to her projected path: it holds, 5 ticks." },
    { tick: 45, caption: "Clear of her: it goes on." },
    { tick: 52, caption: "Each time the projection from her motion runs out, Anton decides again." },
  ];
  return <ReplayView recorded={run(s2)} stops={stops} />;
}

/** Talk stage 3: scenario_s10_02, intention-aware (run_008): her task trusted at tick 8, a hold of 5 ticks. */
export function ReplayTrusted() {
  const stops: Stop[] = [
    { tick: 0, caption: "She starts work; Anton does not yet know which of her tasks it is." },
    { tick: 6, caption: "Deliver item 1 leads with a belief of 0.71: below 0.75, not trusted yet." },
    { tick: 8, caption: "0.78, and her movement supports it: trusted. Anton projects her task's path (filled stripe) and holds 5 ticks." },
    { tick: 13, caption: "Clear of her path: it goes on with its own delivery." },
    { tick: 24, caption: "The projection follows her task, not only her last steps." },
  ];
  return <ReplayView recorded={run(s3)} stops={stops} />;
}

/** Talk stage 4: scenario_s12_02 (run_064): the coffee break trusted at tick 93, a hold of 18 ticks around her break. */
export function ReplayBreak() {
  const stops: Stop[] = [
    { tick: 63, caption: "Item 1 delivered; she walks off toward the coffee machine." },
    { tick: 92, caption: "The coffee break leads with 0.74: not trusted yet." },
    { tick: 93, caption: "0.79 and supported: the coffee break is trusted. Anton plans around her break: it holds 18 ticks." },
    { tick: 110, caption: "It goes on." },
  ];
  return <ReplayView recorded={run(s4)} stops={stops} />;
}

/** Talk stage 5: scenario_s12_04 (run_707), scenario_s12_02's copy with break time in force from tick 63: the coffee
 * break trusted at tick 69, 24 ticks earlier than without it. */
export function ReplayBreakTime() {
  const stops: Stop[] = [
    { tick: 63, caption: "The same shift, now in break time. Item 1 delivered; she walks off toward the coffee machine." },
    { tick: 68, caption: "Break time raises the coffee break: it leads with 0.74 after 5 ticks." },
    { tick: 69, caption: "Trusted at tick 69, not 93: 24 ticks earlier. Anton holds 18 ticks around her break." },
    { tick: 86, caption: "It goes on. Her movement still decided: break time only made the trust come earlier." },
  ];
  return <ReplayView recorded={run(s5)} stops={stops} />;
}

/** Talk stage 6: scenario_s10_03 (run_012): the coffee break cut into her delivery mid-walk, the withdrawal at 55,
 * the break trusted at 76, the resumption at 107. */
export function ReplaySwitch() {
  const stops: Stop[] = [
    { tick: 40, caption: "Anton trusts her task: deliver item 1." },
    { tick: 46, caption: "Mid-way, carrying the item, she turns to the coffee machine." },
    { tick: 55, caption: "Deliver item 1 no longer fits: Anton stops trusting it and plans against her motion." },
    { tick: 76, caption: "The coffee break is trusted." },
    { tick: 107, caption: "She resumes her delivery." },
    { tick: 120, caption: "Deliver item 1 is trusted again." },
  ];
  return <ReplayView recorded={run(s6)} stops={stops} />;
}

/** Talk stage 7: scenario_s10_07 (run_028): a 60-tick stand cut into her delivery mid-walk (unmodelled), unexplained
 * from 62, the fallback, the resumption at 107, adequate again at 120. */
export function ReplayStand() {
  const stops: Stop[] = [
    { tick: 40, caption: "Anton trusts her task: deliver item 1." },
    { tick: 46, caption: "Mid-way she stops and stands. Nobody modelled this." },
    { tick: 62, caption: "After 16 ticks of standing nothing fits: her behaviour is unexplained. Anton falls back on her motion." },
    { tick: 107, caption: "She walks on with her delivery." },
    { tick: 120, caption: "Deliver item 1 fits again: recognition resumes." },
  ];
  return <ReplayView recorded={run(s7)} stops={stops} />;
}
