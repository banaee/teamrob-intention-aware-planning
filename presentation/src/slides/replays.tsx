/**
 * The first drafts of the sim-runs on slides (T-pres, task B of 8 October 2026; before part 4 is planned): existing
 * scenarios and T-F part 1's own run files only, recorded at every build (scripts/record.mjs, RUNS). Each stop is a
 * tick and a caption; every caption states what the run's log shows at that tick (the recognizer's leader and its
 * belief, the gate, the decision, the hold, the human's record), in the talk's words. Beside each scene, Anton's mind at
 * the tick (scene/MindPanel.tsx), the parts each talk stage is about.
 */

import s1 from "../../data/run_stage1_alone.json";
import s2 from "../../data/run_stage2_reactive.json";
import s3 from "../../data/run_stage3_switch.json";
import s4 from "../../data/run_stage4_break.json";
import s5 from "../../data/run_stage5_breaktime.json";
import s6 from "../../data/run_stage6_unmodelled.json";
import { type RecordedRun, ReplayView, type Stop } from "../scene/RunReplay";

const run = (r: unknown) => r as RecordedRun;   // the JSON's enumerations are read as strings

/** Talk stage 1: kitting scenario_s12_02 on env_layout_14, human-unaware (T-F part 1's run_061): Anton's two
 * deliveries, each with its two walks (to the item, to its table) in clearly different directions (87 and 101 degrees
 * between them); the human is not drawn (the robot's mind receives no human in this condition). */
export function ReplayAlone() {
  const stops: Stop[] = [
    { tick: 0, caption: "Anton chooses a task, deliver item 3, and plans its actions: the dashed line." },
    { tick: 8, caption: "It picks up item 3; what is left of its plan turns toward the table." },
    { tick: 30, caption: "Item 3 delivered: it chooses the next task, deliver item 14." },
    { tick: 95, caption: "It picks up item 14." },
    { tick: 136, caption: "Both delivered." },
  ];
  return <ReplayView recorded={run(s1)} stops={stops} hideHumans mind={{}} tickNote />;
}

/** Talk stage 2: scenario_s10_02, intention-unaware (run_006): the projection from her motion and a hold of 5 ticks. */
export function ReplayReactive() {
  const stops: Stop[] = [
    { tick: 24, caption: "Anton knows nothing of her task: it projects her motion (the hatched blue stripe)." },
    { tick: 40, caption: "Its path would come closer than the minimum separation to her projected path: it holds, 5 ticks." },
    { tick: 45, caption: "The hold is over: it goes on." },
    { tick: 52, caption: "Each time the projection from her motion runs out, Anton decides again." },
  ];
  return <ReplayView recorded={run(s2)} stops={stops} mind={{ belief: true, hold: true, projection: true }} />;
}

/** Talk stage 3: scenario_s12_01 on env_layout_14 (T-F part 1's run_060): her delivery of item 1 trusted at tick 8, and
 * Anton switches from deliver item 7 to deliver item 13 (task choice); in the intention-unaware run_058 Anton carries
 * item 7 across her route, with holds. */
export function ReplayTrusted() {
  const stops: Stop[] = [
    { tick: 0, caption: "She starts work. Anton chooses deliver item 7; it does not yet know which of her tasks she does." },
    { tick: 6, caption: "Her delivery of item 1 leads with a belief of 0.71: below 0.75, not trusted yet." },
    { tick: 8, caption: "0.78, and it has support: trusted. Realized against her projected path, deliver item 13 is now cheaper: Anton switches to it." },
    { tick: 29, caption: "It picks up item 13." },
    { tick: 62, caption: "Item 13 delivered, far from her path. Item 7 comes next." },
  ];
  return <ReplayView recorded={run(s3)} stops={stops}
                     mind={{ belief: true, support: true, hold: true, projection: true }} />;
}

/** Talk stage 4: scenario_s24_14 on env_layout_07 (T-F part 1's run_264, no context fact in force): her coffee break
 * trusted at tick 116, and Anton switches from deliver item 56 to deliver item 54 (the human-unaware run_261 does item
 * 56 at 85 to 169). */
export function ReplayBreak() {
  const stops: Stop[] = [
    { tick: 85, caption: "Anton starts its next task: deliver item 56." },
    { tick: 90, caption: "She has delivered her item and walks off to the coffee machine." },
    { tick: 115, caption: "The coffee break leads with 0.74: not trusted yet." },
    { tick: 116, caption: "0.78, and it has support: the coffee break is trusted. Anton switches to deliver item 54." },
    { tick: 150, caption: "Item 54 first; item 56 comes after her break." },
  ];
  return <ReplayView recorded={run(s4)} stops={stops} mind={{ belief: true, hold: true, projection: true }} />;
}

/** Talk stage 5: scenario_s23_03 on env_layout_07 (T-F part 1's run_576; scenario_s05_01 with break time in force from
 * tick 0 to 56): the coffee break trusted at tick 27, and Anton switches to deliver item 2. Without the fact (scenario_s05_01,
 * run_108) the break is trusted only at 52 and Anton passes her at 31.62 cm at tick 28. */
export function ReplayBreakTime() {
  const stops: Stop[] = [
    { tick: 0, caption: "Break time. She walks to the coffee machine; break time raises the coffee break's prior: it leads from the start." },
    { tick: 26, caption: "The coffee break leads with 0.74: not trusted yet." },
    { tick: 27, caption: "0.76, and it has support: trusted. Anton switches from deliver item 1 to deliver item 2." },
    { tick: 62, caption: "The same shift without break time: the break is trusted only at tick 52, and Anton passes her closer than the minimum separation." },
  ];
  return <ReplayView recorded={run(s5)} stops={stops}
                     mind={{ belief: true, hold: true, projection: true, context: true }} />;
}

/** Talk stage 6 (the merge of 8 October 2026; the old talk stage 7's replay): scenario_s10_07 (run_028): a 60-tick stand
 * cut into her delivery mid-walk (unmodelled), unexplained from 62, the fallback, she walks on at 107, her delivery
 * adequate and trusted again at 120 (the log: [meta-proj] projection=built at the decision of tick 120). */
export function ReplayStand() {
  const stops: Stop[] = [
    { tick: 40, caption: "Anton trusts her task: deliver item 1." },
    { tick: 46, caption: "Mid-way she stops and stands: unmodelled behaviour." },
    { tick: 62, caption: "After 16 ticks of standing no hypothesis fits: her behaviour is unexplained, and Anton stops trusting her task. It falls back on the projection from her motion, as the reactive robot did." },
    { tick: 107, caption: "She walks on with her delivery." },
    { tick: 120, caption: "Deliver item 1 fits again: Anton trusts her task again." },
  ];
  return <ReplayView recorded={run(s6)} stops={stops}
                     mind={{ belief: true, fit: true, hold: true, projection: true }} />;
}
