/**
 * The sim-runs replayed on slides, recorded at every build (scripts/record.mjs, RUNS). Talk stage 3's is T-F part 1's
 * run_060; the others are Hadi's scenarios for the talk (tpres-v4, 8 October 2026) or, where his scenario did not show
 * the stage's mechanism, a copy of one under a new id with the change named (tpres-v5: scenario_s305_01 for talk stage
 * 2), each run from its own run file under configs/kitting/tpres/, outside every
 * measured set; its log pair and figure are kept in presentation/runs/ (untracked). Each stop is a tick and a caption;
 * every line states only what the run's log shows at that tick (the recognizer's leader and its belief, the gate,
 * the decision, the hold, the human's record), in the talk's words: a slide never states what its replay does not show
 * (Hadi, tpres-v5). Beside each scene, the robot's mind at the tick (scene/MindPanel.tsx), the parts each talk stage is
 * about.
 */

import s1 from "../../data/run_stage1_alone.json";
import s2 from "../../data/run_stage2_reactive.json";
import s3 from "../../data/run_stage3_switch.json";
import s4 from "../../data/run_stage4_break.json";
import s5 from "../../data/run_stage5_context.json";
import s6 from "../../data/run_stage6_unmodelled.json";
import s8 from "../../data/run_stage8_dock.json";
import { type RecordedRun, ReplayView, type Stop } from "../scene/RunReplay";

const run = (r: unknown) => r as RecordedRun;   // the JSON's enumerations are read as strings

/** Talk stage 1: Hadi's scenario_s301_01 on env_layout_14 (configs/kitting/tpres/stage1_s301_01.yaml; the options of
 * T-F part 1's run_061, human-unaware; the scenario has no human), ticks 0 to 150, played fast (about 14 ticks a
 * second): the robot chooses deliver item 1 at 0, picks it up at 32, places it at 64; chooses deliver item 2 at 67,
 * picks it up at 97, places it at 145. */
export function ReplayAlone() {
  const stops: Stop[] = [
    { tick: 0, caption: "Robot chooses item 1 and plans its actions (dashed)." },
    { tick: 32, caption: "It picks up item 1." },
    { tick: 67, caption: "Item 1 delivered; robot chooses item 2." },
    { tick: 97, caption: "It picks up item 2." },
    { tick: 150, caption: "Both delivered." },
  ];
  return <ReplayView recorded={run(s1)} stops={stops} hideHumans mind={{ tasks: true }} tickMs={70} />;
}

/** Talk stage 2: scenario_s305_01 on env_layout_12 (configs/kitting/tpres/stage2_s305_01.yaml, intention-unaware), a
 * copy of Hadi's scenario_s302_02 with the robot starting at (300, 60) instead of (390, 160): in scenario_s302_02 no
 * hold is decided anywhere in the run. Ticks 0 to 44: the projection from her motion, the robot deciding again each time
 * it runs out; she picks up item 1 at 24 (the robot carries item 7 from 23); at 34 the robot holds 7 ticks (34 to 40),
 * her projected path crossing its own at the room's crossing; it goes on behind her, closest 58.26 cm at 42 (the
 * minimum separation 50 cm). */
export function ReplayReactive() {
  const stops: Stop[] = [
    { tick: 0, caption: "Robot projects her motion (hatched blue) and sets off for item 7." },
    { tick: 24, caption: "She picks up item 1; robot carries item 7." },
    { tick: 34, caption: "Too close to her projected motion: robot holds 7 ticks." },
    { tick: 40, caption: "She crosses; the hold ends." },
    { tick: 44, caption: "Robot goes on behind her; closest 58 cm (minimum 50)." },
  ];
  return <ReplayView recorded={run(s2)} stops={stops} mind={{ belief: true, hold: true, projection: true }} />;
}

/** Talk stage 3: scenario_s12_01 on env_layout_14 (T-F part 1's run_060): her delivery of item 1 recognised at tick 8, and
 * the robot switches from deliver item 7 to deliver item 13 (task choice); in the intention-unaware run_058 the robot
 * carries item 7 across her route, with holds. */
export function ReplayRecognised() {
  const stops: Stop[] = [
    { tick: 0, caption: "Robot chooses item 7; her task is not yet known." },
    { tick: 6, caption: "Her delivery of item 1 leads at 0.71: not yet recognised." },
    { tick: 8, caption: "0.78: recognised. Item 13 is now cheaper: robot switches." },
    { tick: 29, caption: "It picks up item 13." },
    { tick: 62, caption: "Item 13 delivered, far from her path." },
  ];
  return <ReplayView recorded={run(s3)} stops={stops}
                     mind={{ belief: true, hold: true, projection: true }} />;
}

/** Talk stage 4: Hadi's scenario_s304_14 on env_layout_07 (configs/kitting/tpres/stage4_s304_14_ck_off.yaml, context
 * knowledge off), ticks 70 to 150 (Hadi, tpres-v5): at 70 the robot carries item 55 (decided at 63, her delivery of item
 * 52 recognised then, 0.80; 0.97 at 70); she delivers item 52 at 90 and starts her second coffee break; the robot chooses
 * deliver item 56 at 97; the break recognised at 106 (0.76), and the robot switches to deliver item 54, item 56 realized
 * with a hold of 26 ticks; the break ends at 150. Talk stage 5 replays the same scenario with context knowledge on. */
export function ReplayBreak() {
  const stops: Stop[] = [
    { tick: 70, caption: "Robot carries item 55; her delivery of item 52 is recognised." },
    { tick: 90, caption: "She walks to the coffee machine: her second break." },
    { tick: 97, caption: "Item 55 delivered; robot chooses item 56." },
    { tick: 106, caption: "0.76: coffee break recognised. Item 56 would need a 26-tick hold: robot switches to item 54." },
    { tick: 150, caption: "Her break is over; robot is on item 54." },
  ];
  return <ReplayView recorded={run(s4)} stops={stops} mind={{ belief: true, hold: true, projection: true }} />;
}

/** Talk stage 5: Hadi's scenario_s304_14, the same as talk stage 4, with context knowledge on
 * (configs/kitting/tpres/stage5_s304_14_ck_on.yaml), the same ticks 70 to 150 (Hadi, tpres-v6: his scenario exactly).
 * No timeline: no context fact is in force. Her first coffee break, observed complete at 49, makes the coffee break
 * recent: lowered from 51 to 138 ([IR-context]). At 70 her delivery of item 52 is recognised (since 60; 0.99). At 90 she
 * delivers item 52 and walks to the coffee machine; the robot's belief reads her next delivery, item 53 (0.97), not
 * recognised (no observation, then no support). At 97 the robot chooses deliver item 56. At 106 the coffee break stands at
 * 0.37 behind switching on the A/C at 0.46 ([IR-dist]). Trusted at 116 (0.78): item 56 would need a hold of 26 ticks,
 * and the robot switches to deliver item 54. */
export function ReplayBreakTime() {
  const stops: Stop[] = [
    { tick: 70, caption: "Same shift, with context knowledge. Her delivery of item 52 is recognised." },
    { tick: 90, caption: "She walks to the coffee machine; just after a break, another is less likely." },
    { tick: 97, caption: "Item 55 delivered; robot chooses item 56." },
    { tick: 106, caption: "Coffee break at 0.37, behind the A/C: not recognised." },
    { tick: 116, caption: "0.78: coffee break recognised. Item 56 would need a 26-tick hold: robot switches to item 54." },
    { tick: 150, caption: "Her break is over; robot is on item 54." },
  ];
  return <ReplayView recorded={run(s5)} stops={stops}
                     mind={{ belief: true, hold: true, projection: true, context: true }} />;
}

/** Talk stage 6: Hadi's scenario_s111_02 on env_layout_12 (configs/kitting/tpres/stage6_s111_02.yaml; the options of
 * T-F part 1's run_028), ticks 0 to 39 (tpres-v5: the range ends while she stands; the hold of 32 ticks decided at 55
 * runs on after she walks off at 57, and does not serve the point). Her script is unmodelled throughout: a walk to
 * door_N, a stand of 60 seconds at spot_E (standing from 26 to 57), a walk to corner_SE. Her assigned delivery of item 12
 * leads but is not recognised: no support to 9, no fit from 10 (unexplained, every live hypothesis inadequate). The
 * projection from her motion all along; holds of 2 ticks at 14, 20 and 25, then 4 at 27, 8 at 31 and 16 at 39 while
 * she stands. */
export function ReplayStand() {
  const stops: Stop[] = [
    { tick: 0, caption: "She walks to the north door; her delivery of item 12 leads, not recognised." },
    { tick: 10, caption: "No hypothesis fits: unexplained. Robot knows that it does not know." },
    { tick: 14, caption: "It falls back on the projection from her motion: a 2-tick hold." },
    { tick: 26, caption: "She stands by the east wall: nothing robot has a model of." },
    { tick: 39, caption: "The longer she stands, the longer the holds: 4, 8, now 16 ticks." },
  ];
  return <ReplayView recorded={run(s6)} stops={stops}
                     mind={{ belief: true, fit: true, hold: true, projection: true }}
                     mark={{ object: "item_12", label: "item 12" }} />;
}

/** The lift truck's turn: Hadi's dock_loading scenario_s11_01 on env_layout_05 (configs/dock_loading/tpres/stage8_dl_s11_01.yaml,
 * intention-aware, the defaults otherwise), ticks 50 to 120: her scan of pallet 0 recognised from 48; pallet 5 delivered
 * and the return of pallet 6 chosen at 60; her scan of pallet 2 entered and recognised at 68; at 120 an office break
 * leads (0.80), not recognised. No hold in the run. */
export function ReplayDock() {
  const stops: Stop[] = [
    { tick: 50, caption: "Robot's task: deliver pallet 5." },
    { tick: 60, caption: "Pallet 5 delivered; robot chooses to return pallet 6." },
    { tick: 68, caption: "She moves to pallet 2: that scan is recognised." },
    { tick: 120, caption: "An office break leads at 0.80: not recognised." },
  ];
  return <ReplayView recorded={run(s8)} stops={stops} mind={{ belief: true, hold: true, projection: true }} />;
}
