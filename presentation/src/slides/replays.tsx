/**
 * The sim-runs replayed on slides, recorded at every build (scripts/record.mjs, RUNS). Talk stage 3's is T-F part 1's
 * run_060; the others are Hadi's scenarios for the talk (tpres-v4, 8 October 2026) or, where his scenario did not show
 * the stage's mechanism, copies of them under new ids with the change named (tpres-v5: scenario_s305_01 for talk stage
 * 2, scenario_s306_01 for talk stage 5), each run from its own run file under configs/kitting/tpres/, outside every
 * measured set; its log pair and figure are kept in presentation/runs/ (untracked). Each stop is a tick and a caption;
 * every caption states only what the run's log shows at that tick (the recognizer's leader and its belief, the gate,
 * the decision, the hold, the human's record), in the talk's words: a slide never states what its replay does not show
 * (Hadi, tpres-v5). Beside each scene, the robot's mind at the tick (scene/MindPanel.tsx), the parts each talk stage is
 * about.
 */

import s1 from "../../data/run_stage1_alone.json";
import s2 from "../../data/run_stage2_reactive.json";
import s3 from "../../data/run_stage3_switch.json";
import s4 from "../../data/run_stage4_break.json";
import s5with from "../../data/run_stage5_with.json";
import s5without from "../../data/run_stage5_without.json";
import s6 from "../../data/run_stage6_unmodelled.json";
import { type RecordedRun, ReplayView, type Stop } from "../scene/RunReplay";

const run = (r: unknown) => r as RecordedRun;   // the JSON's enumerations are read as strings

/** Talk stage 1: Hadi's scenario_s301_01 on env_layout_14 (configs/kitting/tpres/stage1_s301_01.yaml; the options of
 * T-F part 1's run_061, human-unaware; the scenario has no human), ticks 0 to 150, played fast (about 14 ticks a
 * second): the robot chooses deliver item 1 at 0, picks it up at 32, places it at 64; chooses deliver item 2 at 67,
 * picks it up at 97, places it at 145. */
export function ReplayAlone() {
  const stops: Stop[] = [
    { tick: 0, caption: "The robot chooses a task, deliver item 1, and plans its actions: the dashed line." },
    { tick: 32, caption: "It picks up item 1; what is left of its plan leads to the table." },
    { tick: 67, caption: "Item 1 delivered: it chooses the next task, deliver item 2." },
    { tick: 97, caption: "It picks up item 2." },
    { tick: 150, caption: "Both delivered." },
  ];
  return <ReplayView recorded={run(s1)} stops={stops} hideHumans mind={{}} tickNote tickMs={70} />;
}

/** Talk stage 2: scenario_s305_01 on env_layout_12 (configs/kitting/tpres/stage2_s305_01.yaml, intention-unaware), a
 * copy of Hadi's scenario_s302_02 with the robot starting at (300, 60) instead of (390, 160): in scenario_s302_02 no
 * hold is decided anywhere in the run. Ticks 0 to 44: the projection from her motion, the robot deciding again each time
 * it runs out; she picks up item 1 at 24 (the robot carries item 7 from 23); at 34 the robot holds 7 ticks (34 to 40),
 * her projected path crossing its own at the room's crossing; it goes on behind her, closest 58.26 cm at 42 (the
 * minimum separation 50 cm). */
export function ReplayReactive() {
  const stops: Stop[] = [
    { tick: 0, caption: "The robot knows nothing of her task: it projects her motion (the hatched blue stripe) and sets off to deliver item 7." },
    { tick: 24, caption: "She picks up item 1 and turns toward her table; the robot carries item 7 toward its own." },
    { tick: 34, caption: "Its path would come closer than the minimum separation to the projection of her motion: the robot holds, 7 ticks." },
    { tick: 40, caption: "She crosses its path; the hold ends." },
    { tick: 44, caption: "The robot goes on behind her. Closest: 58 cm, at tick 42, beyond the minimum separation of 50 cm." },
  ];
  return <ReplayView recorded={run(s2)} stops={stops} mind={{ belief: true, hold: true, projection: true }} />;
}

/** Talk stage 3: scenario_s12_01 on env_layout_14 (T-F part 1's run_060): her delivery of item 1 trusted at tick 8, and
 * the robot switches from deliver item 7 to deliver item 13 (task choice); in the intention-unaware run_058 the robot
 * carries item 7 across her route, with holds. */
export function ReplayTrusted() {
  const stops: Stop[] = [
    { tick: 0, caption: "She starts work. The robot chooses deliver item 7; it does not yet know which of her tasks she does." },
    { tick: 6, caption: "Her delivery of item 1 leads with a belief of 0.71: below 0.75, not trusted yet." },
    { tick: 8, caption: "0.78, and it has support: trusted. Realized against her projected path, deliver item 13 is now cheaper: the robot switches to it." },
    { tick: 29, caption: "It picks up item 13." },
    { tick: 62, caption: "Item 13 delivered, far from her path. Item 7 comes next." },
  ];
  return <ReplayView recorded={run(s3)} stops={stops}
                     mind={{ belief: true, support: true, hold: true, projection: true }} />;
}

/** Talk stage 4: Hadi's scenario_s304_14 on env_layout_07 (configs/kitting/tpres/stage4_s304_14_ck_off.yaml, context
 * knowledge off), ticks 70 to 150 (Hadi, tpres-v5): at 70 the robot carries item 55 (decided at 63, her delivery of item
 * 52 trusted then, 0.80; 0.97 at 70); she delivers item 52 at 90 and starts her second coffee break; the robot chooses
 * deliver item 56 at 97; the break trusted at 106 (0.76), and the robot switches to deliver item 54, item 56 realized
 * with a hold of 26 ticks; the break ends at 150. */
export function ReplayBreak() {
  const stops: Stop[] = [
    { tick: 70, caption: "The robot carries item 55 to the table. She carries item 52 there too; her delivery is trusted: the projection from her intention." },
    { tick: 90, caption: "She has delivered item 52 and walks to the coffee machine: her second coffee break." },
    { tick: 97, caption: "Item 55 delivered: the robot chooses deliver item 56." },
    { tick: 106, caption: "0.76, and it has support: the coffee break is trusted. Against her break, item 56 would need a hold of 26 ticks: the robot switches to deliver item 54." },
    { tick: 150, caption: "Her break is over and she goes on with item 53; the robot is on item 54, item 56 comes after." },
  ];
  return <ReplayView recorded={run(s4)} stops={stops} mind={{ belief: true, hold: true, projection: true }} />;
}

/** Talk stage 5, one situation without and with context knowledge: scenario_s306_01 on env_layout_07, a copy of Hadi's
 * scenario_s304_14 without the first coffee break, the robot starting at (-750, -200), break_time in force from 50 to
 * 120 (configs/kitting/tpres/stage5_s306_01_ck_off.yaml and _ck_on.yaml), ticks 50 to 85. The two runs are the same to
 * tick 67. She delivers item 52 at 58 and walks to the coffee machine; the robot delivers item 54 at 68.
 * Without context knowledge: the coffee break at 0.36 at 58; at 68 (0.64, not trusted) the robot chooses deliver item 56,
 * whose shelf is behind the coffee machine (cost 82.52 against item 55's 94.51, no hold), and walks south toward her
 * from (-21, 30) to (-18, -70) by 73; trusted at 74 (0.76): item 56 would need a hold of 24 ticks, the robot switches to
 * deliver item 55 and turns back (at (-16, 70) by 80).
 * With context knowledge: break time raises the coffee break (prior 0.66 from 50); trusted at 59 (0.76); at 69 the robot
 * chooses deliver item 55 at once, item 56 needing a hold of 24 ticks, and walks north (at (-15, 270) by 80). */
export function ReplayWithoutContext() {
  const stops: Stop[] = [
    { tick: 50, caption: "Without context knowledge. She carries item 52 to the table; the robot carries item 54 there too." },
    { tick: 58, caption: "She has delivered item 52 and walks to the coffee machine. The coffee break leads at 0.36: not trusted." },
    { tick: 68, caption: "Item 54 delivered. Still not trusted (0.64): the robot chooses deliver item 56, whose shelf is behind the coffee machine." },
    { tick: 74, caption: "0.76: the coffee break is trusted. Against her break, item 56 would need a hold of 24 ticks: the robot switches to deliver item 55 and turns back." },
    { tick: 85, caption: "The robot is on its way to item 55, after a detour of 100 cm toward her." },
  ];
  return <ReplayView recorded={run(s5without)} stops={stops} mind={{ belief: true, hold: true, projection: true }} />;
}

export function ReplayWithContext() {
  const stops: Stop[] = [
    { tick: 50, caption: "The same situation, with context knowledge. It is break time: the context raises the coffee break's prior. Her movement still leads: her delivery of item 52." },
    { tick: 59, caption: "She has delivered item 52 and walks to the coffee machine. 0.76, and it has support: the coffee break is trusted, 15 ticks earlier." },
    { tick: 69, caption: "Item 54 delivered. Against her break, item 56 would need a hold of 24 ticks: the robot chooses deliver item 55 at once." },
    { tick: 85, caption: "The robot is on its way to item 55, without the detour toward her." },
  ];
  return <ReplayView recorded={run(s5with)} stops={stops}
                     mind={{ belief: true, hold: true, projection: true, context: true }} />;
}

/** Talk stage 6: Hadi's scenario_s111_02 on env_layout_12 (configs/kitting/tpres/stage6_s111_02.yaml; the options of
 * T-F part 1's run_028), ticks 0 to 39 (tpres-v5: the range ends while she stands; the hold of 32 ticks decided at 55
 * runs on after she walks off at 57, and does not serve the point). Her script is unmodelled throughout: a walk to
 * door_N, a stand of 60 seconds at spot_E (standing from 26 to 57), a walk to corner_SE. Her assigned delivery of item 12
 * leads but is not trusted: no support to 9, no fit from 10 (unexplained, every live hypothesis inadequate). The
 * projection from her motion all along; holds of 2 ticks at 14, 20 and 25, then 4 at 27, 8 at 31 and 16 at 39 while
 * she stands. */
export function ReplayStand() {
  const stops: Stop[] = [
    { tick: 0, caption: "She walks to the north door. Her delivery of item 12 leads the belief, but has no support: not trusted." },
    { tick: 10, caption: "Her walk fits none of the robot's hypotheses: her behaviour is unexplained. The robot knows that it does not know." },
    { tick: 14, caption: "It falls back on the projection from her motion, as the reactive robot did: a hold of 2 ticks." },
    { tick: 26, caption: "She stands at a spot by the east wall: something the robot has no model of." },
    { tick: 39, caption: "The longer she stands, the further the projection of her stand reaches: the robot's holds grow, 4, 8, now 16 ticks." },
  ];
  return <ReplayView recorded={run(s6)} stops={stops}
                     mind={{ belief: true, fit: true, hold: true, projection: true }} />;
}
