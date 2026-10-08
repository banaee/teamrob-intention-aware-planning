/**
 * The sim-runs replayed on slides, recorded at every build (scripts/record.mjs, RUNS). Talk stage 3's is T-F part 1's
 * run_060; the others are Hadi's scenarios for the talk (tpres-v4, 8 October 2026), each run from its own run file
 * under configs/kitting/tpres/, outside every measured set; its log pair and figure are kept in presentation/runs/
 * (untracked). Each stop is a tick and a caption; every caption states only what the run's log shows at that tick (the
 * recognizer's leader and its belief, the gate, the decision, the hold, the human's record), in the talk's words.
 * Beside each scene, Anton's mind at the tick (scene/MindPanel.tsx), the parts each talk stage is about.
 */

import s1 from "../../data/run_stage1_alone.json";
import s2 from "../../data/run_stage2_reactive.json";
import s3 from "../../data/run_stage3_switch.json";
import s4 from "../../data/run_stage4_break.json";
import s5 from "../../data/run_stage5_context.json";
import s6 from "../../data/run_stage6_unmodelled.json";
import { type RecordedRun, ReplayView, type Stop } from "../scene/RunReplay";

const run = (r: unknown) => r as RecordedRun;   // the JSON's enumerations are read as strings

/** Talk stage 1: Hadi's scenario_s301_01 on env_layout_14 (configs/kitting/tpres/stage1_s301_01.yaml; the options of
 * T-F part 1's run_061, human-unaware; the scenario has no human), ticks 0 to 150, played fast (about 14 ticks a
 * second): Anton chooses deliver item 1 at 0, picks it up at 32, places it at 64; chooses deliver item 2 at 67, picks it
 * up at 97, places it at 145. */
export function ReplayAlone() {
  const stops: Stop[] = [
    { tick: 0, caption: "Anton chooses a task, deliver item 1, and plans its actions: the dashed line." },
    { tick: 32, caption: "It picks up item 1; what is left of its plan leads to the table." },
    { tick: 67, caption: "Item 1 delivered: it chooses the next task, deliver item 2." },
    { tick: 97, caption: "It picks up item 2." },
    { tick: 150, caption: "Both delivered." },
  ];
  return <ReplayView recorded={run(s1)} stops={stops} hideHumans mind={{}} tickNote tickMs={70} />;
}

/** Talk stage 2: Hadi's scenario_s302_02 on env_layout_12 (configs/kitting/tpres/stage2_s302_02.yaml; the options of
 * T-F part 1's run_006, intention-unaware), ticks 0 to 26: the projection from her motion, Anton deciding again each
 * time it runs out (2, 6, 14, 23, 25); no hold: every candidate's hold is 0; the two are 626 cm apart at 0 and 428 cm
 * at 26 (their closest, 60.31 cm, is at 42, outside the range). She picks up item 1 at 24. */
export function ReplayReactive() {
  const stops: Stop[] = [
    { tick: 0, caption: "Anton knows nothing of her task: it projects her motion (the hatched blue stripe) and sets off to deliver item 7." },
    { tick: 14, caption: "Each time the projection from her motion runs out, Anton decides again. Its path stays clear of hers: no hold." },
    { tick: 24, caption: "She picks up item 1." },
    { tick: 26, caption: "She turns toward the table. Anton goes on, 428 cm from her: no hold so far." },
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

/** Talk stage 4: Hadi's scenario_s304_14 on env_layout_07 (configs/kitting/tpres/stage4_s304_14_ck_off.yaml, context
 * knowledge off), ticks 85 to 150: she delivers item 52 at 90 and starts her second coffee break; Anton chooses deliver
 * item 56 at 97; the break trusted at 106 (0.76), and Anton switches to deliver item 54, item 56 realized with a hold of
 * 26 ticks; the break ends at 150. Talk stage 5 replays the same scenario with context knowledge on. */
export function ReplayBreak() {
  const stops: Stop[] = [
    { tick: 85, caption: "Anton carries item 55; she is on her way with her delivery of item 52." },
    { tick: 90, caption: "She has delivered item 52 and walks to the coffee machine: her second coffee break." },
    { tick: 97, caption: "Item 55 delivered: Anton chooses deliver item 56." },
    { tick: 106, caption: "0.76, and it has support: the coffee break is trusted. Against her break, item 56 would need a hold of 26 ticks: Anton switches to deliver item 54." },
    { tick: 150, caption: "Her break is over and she goes on with item 53; Anton is on item 54, item 56 comes after." },
  ];
  return <ReplayView recorded={run(s4)} stops={stops} mind={{ belief: true, hold: true, projection: true }} />;
}

/** Talk stage 5: the same scenario_s304_14 (configs/kitting/tpres/stage5_s304_14_ck_on.yaml, context knowledge on), the
 * same ticks 85 to 150. No timeline: no context fact is in force; her first coffee break (completed at 51) makes the
 * coffee break recent, its level suppressed until 141. The break is trusted at 116 (0.78), 10 ticks later than with
 * context knowledge off (106); at 106 it stands at 0.37 behind ac_activation's 0.46 ([IR-dist]); Anton switches to deliver item 54 at 116,
 * item 56 realized with a hold of 26 ticks. */
export function ReplayBreakTime() {
  const stops: Stop[] = [
    { tick: 85, caption: "The same shift, now with context knowledge. Anton carries item 55; she is on her way with her delivery of item 52." },
    { tick: 90, caption: "She walks to the coffee machine again. Her first break ended at tick 51: just after a break, Anton's prior makes another one less likely." },
    { tick: 97, caption: "Item 55 delivered: Anton chooses deliver item 56." },
    { tick: 106, caption: "Without context knowledge the break was trusted at this tick. Here it stands at 0.37, behind switching on the A/C: not trusted, and Anton goes on toward item 56." },
    { tick: 116, caption: "0.78, and it has support: trusted, 10 ticks later. Item 56 would need a hold of 26 ticks: Anton switches to deliver item 54." },
    { tick: 150, caption: "Her break is over and she goes on with item 53; Anton is on item 54." },
  ];
  return <ReplayView recorded={run(s5)} stops={stops}
                     mind={{ belief: true, hold: true, projection: true, context: true }} />;
}

/** Talk stage 6: Hadi's scenario_s111_02 on env_layout_12 (configs/kitting/tpres/stage6_s111_02.yaml; the options of
 * T-F part 1's run_028), ticks 0 to 70. Her script is unmodelled throughout: a walk to door_N, a stand of 60 seconds at
 * spot_E (standing from 26 to 57), a walk to corner_SE. Her assigned delivery of item 12 leads at 0.98 but is not
 * trusted: no support to 9, no fit from 10 (unexplained, every live hypothesis inadequate). The projection from her
 * motion all along; holds of 2 ticks at 14, 20 and 25, then 4 at 27, 8 at 31, 16 at 39 and 32 at 55 (to 86), while she
 * stands; closest 50.44 cm (24 and 56). Nothing is trusted again within the range. */
export function ReplayStand() {
  const stops: Stop[] = [
    { tick: 0, caption: "She walks to the north door. Her delivery of item 12 leads the belief, but has no support: not trusted." },
    { tick: 10, caption: "Her walk fits none of Anton's hypotheses: her behaviour is unexplained. Anton knows that it does not know." },
    { tick: 14, caption: "It falls back on the projection from her motion, as the reactive robot did: a hold of 2 ticks." },
    { tick: 26, caption: "She stands at a spot by the east wall: something Anton has no model of." },
    { tick: 39, caption: "The longer she stands, the further the projection of her stand reaches: Anton's holds grow, 4, 8, now 16 ticks." },
    { tick: 57, caption: "She walks on, still unexplained. Anton's hold of 32 ticks, decided at tick 55 on her stand, runs on." },
    { tick: 70, caption: "Anton still holds. No hypothesis fits her walk: nothing is trusted." },
  ];
  return <ReplayView recorded={run(s6)} stops={stops}
                     mind={{ belief: true, fit: true, hold: true, projection: true }} />;
}
