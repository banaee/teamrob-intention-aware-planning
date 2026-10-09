/**
 * Talk stages 3 to 11. Talk stages 3 to 6 (the overall revision of 8 October 2026): each opens with its transition
 * slide (the six talk stages, the starting one with its three columns), then a replayed sim-run with the robot's mind
 * beside it, then the architecture, a click adding what the talk stage adds and one click per block it opens or extends
 * (architecture/unboxing.tsx). Talk stage 5 replays Hadi's scenario of talk stage 4 with context knowledge on, a plot of
 * the timeline under the robot's mind (tpres-v6).
 * Talk stage 6 is the merge of the same day (the old talk stages 6, switch and resumption, and 7, unmodelled behaviour,
 * both resting on fit); since tpres-v4 it shows unmodelled behaviour only, the switch to a known behaviour one line of its
 * notes. After them (tpres-v5: no number on any of them): the recap, the lift truck (a placeholder), the results (Hadi's
 * table, on four slides), the afternoon (a placeholder), and "Thank you". A slide never states what its replay
 * does not show (Hadi, tpres-v5).
 */

import type { ReactNode } from "react";

import type { Unboxable } from "../architecture/unboxing";
import { Ensemble } from "../scene/Ensemble";
import { STAGES, type TalkStage } from "../talk";
import { ArchitectureView, Slide, StageTitle, Todo, TransitionSlide } from "./kit";
import { ReplayBreak, ReplayBreakTime, ReplayStand, ReplayTrusted } from "./replays";

/** A talk stage's replayed sim-run, with the robot's mind beside it. `todo`: what the TODO box this replay stands in
 * asked for (in the notes). */
function ReplaySlide({ stage, title, notes, todo, children }: {
  stage: TalkStage; title: string; notes: ReactNode; todo: ReactNode; children: ReactNode;
}) {
  return (
    <Slide stage={stage} className="replay-slide" notes={<>
      {notes}
      <p><strong>TODO (part 4)</strong>, the box this draft stands in: {todo}</p>
    </>}>
      <h1 className="slide-head">{title}</h1>
      {children}
    </Slide>
  );
}

function ArchSlide({ stage, notes, caption, opens }: {
  stage: TalkStage; notes: ReactNode; caption?: string; opens: Unboxable[];
}) {
  return (
    <Slide stage={stage} className="arch-slide" notes={notes}>
      <ArchitectureView stage={stage} title="The architecture so far" caption={caption} opens={opens} />
    </Slide>
  );
}

const FIRST = <p><strong>FIRST VERSION</strong> (T-pres, 8 October 2026; revised the same day), for Hadi's revision.</p>;
const PLACEHOLDER = <p><strong>PLACEHOLDER</strong> (T-pres part 1): the content is built in a later part.</p>;
const MIND = <p>Beside the scene, the robot's mind at the tick, as the robot panel at the station shows it: the
  hypotheses as bars (θ the thin line on each), the trusted intention marked; its task, its hold, which projection of
  her it uses.</p>;

// ---- 3 Assigned tasks --------------------------------------------------------------------------------------------

export function Stage3Transition() {
  return (
    <TransitionSlide stage={3} notes={<>
      <p>The robot now knows her task list: the tasks she is assigned. What it believes: which of her tasks she is doing.
        What it decides: its own next task and hold, against where her task will take her.</p>
      <p>The heaviest stage: most of the time goes here.</p>
    </>} />
  );
}

export function Stage3Replay() {
  return (
    <ReplaySlide stage={3} title="Assigned tasks: a sim-run" todo={<>
      A recorded sim-run in the web-ui's look: the belief over her tasks rising as she walks, the confidence check
      passing, the projection from her intention on the floor (a filled blue stripe), and the robot's hold or task
      choice against it. Why: this is where recognition first changes what the robot does.
    </>} notes={<>
      {FIRST}
      <p><strong>DRAFT</strong> (the second search, 8 October 2026): kitting scenario_s12_01 on env_layout_14, T-F part
        1's run_060 (intention-aware), ticks 0 to 62. Her delivery of item 1 trusted at 8 (0.78), and the robot switches
        from item 7 to item 13: task choice changes what the robot does. In the intention-unaware run_058 the robot
        carries item 7 across her route, with holds at 40 (5 ticks), 103 (4) and 113 (1). Weakness: item 7's and item
        13's shelves are close on one approach line, so the switch shows from the carry on (tick 29). The earlier draft,
        run_008 of scenario_s10_02, held 5 ticks far from her. One click per stop.</p>
      {MIND}
    </>}>
      <ReplayTrusted />
    </ReplaySlide>
  );
}

export function Stage3Architecture() {
  return (
    <ArchSlide stage={3} opens={["B41", "B43", "B44", "B51", "B53", "B54"]} notes={<>
      {FIRST}
      <p>Click 1: recognition appears with belief update, support and the confidence check; the team task knowledge
        gains her task list; the world state gives her actions to recognition. The arrow "trusted intention, or none"
        is the visual centre: where recognition affects planning. Task choice takes the realizer's cost; the realizer's
        direct arrow to execute gives way.</p>
      <p>Click 2, belief update: Bayes. The hypotheses H are her assigned tasks; o is what the robot has seen her do.
        Taken off the panel: the likelihood P(o | h) is a product over the actions of h, one factor L(x) = 2 / (1 +
        e^(βx)) per action, x her extra path beyond the shortest way to the action's target plus her standing beyond what
        the action takes (β = 0.01 per cm). The prior is equal for now; talk stage 5 opens it.</p>
      <p>Click 3, support: a belief needs support from what she actually does. Knowing which task is probable does not
        say when she starts. A wait has only the second source (a completion the robot saw).</p>
      <p>Click 4, confidence check: the leader is trusted when it is strong enough (θ = 0.75) and supported; out comes
        the trusted intention, or none. In the code the check also reads fit from here on; the talk adds it at talk
        stage 6. In the code the check is the meta-planner's gate; the talk places it in recognition, because everything
        it reads is recognition's output.</p>
      <p>Click 5, projection: from her intention, her path is the plan of the trusted task, broken down into actions from
        where she is now: where she will be, and when. Say it here, once: one knowledge, two uses; the AAAI paper's first
        contribution in one sentence, and why talk stage 1 was not wasted.</p>
      <p>Click 6, realizer: per task of the robot's plan, in order, the smallest hold in whole ticks such that the
        robot's moving path never comes closer than the minimum separation (50 cm in the simulation) to her projected
        path; a later task's hold counts from the holds before it. Cost: the plan's duration plus its holds.</p>
      <p>Click 7, task choice: each candidate (one task under single_task, or an order of all remaining tasks under
        full_reorder) realized, the cheapest chosen. Only the first hold is carried out; the rest is lookahead, decided
        again later.</p>
    </>} />
  );
}

// ---- 4 Foreseeable behaviours ------------------------------------------------------------------------------------

export function Stage4Transition() {
  return (
    <TransitionSlide stage={4} notes={<>
      <p>The robot also knows what people foreseeably do besides their tasks: a coffee break, switching on the A/C. A
        coffee break is modelled behaviour, foreseen. Words: "foreseeable behaviours"; never a deviation.</p>
    </>} />
  );
}

export function Stage4Replay() {
  return (
    <ReplaySlide stage={4} title="Foreseeable behaviours: a sim-run" todo={<>
      A recorded sim-run with a coffee break: the break recognised, and a visible planning consequence, for example a
      reorder caused by the trusted break. Why: one later stage should show planning change, not only recognition.
    </>} notes={<>
      {FIRST}
      <p><strong>HADI'S SCENARIO</strong> (tpres-v4, 8 October 2026; from tick 70 since tpres-v5): kitting
        scenario_s304_14 on env_layout_07, context knowledge off, run file configs/kitting/tpres/stage4_s304_14_ck_off.yaml,
        ticks 70 to 150. At 70 the robot carries item 55 and her delivery of item 52 is trusted (since 63). Her second
        coffee break starts at 90; the robot chooses deliver item 56 at 97; the break is trusted at 106 (0.76), and the
        robot switches to deliver item 54: item 56, realized against her break, would need a hold of 26 ticks. No hold
        carried out; closest 96.48 cm (tick 89). One click per stop.</p>
      {MIND}
    </>}>
      <ReplayBreak />
    </ReplaySlide>
  );
}

export function Stage4Architecture() {
  return (
    <ArchSlide stage={4} opens={["B41"]} notes={<>
      {FIRST}
      <p>Click 1: knowledge about the human appears, its foreseeable behaviours going to recognition.</p>
      <p>Click 2, belief update again: the same formula; only H grows, by the foreseeable behaviours. Nothing else in the
        mind changes: the same blocks now also recognise a break.</p>
    </>} />
  );
}

// ---- 5 Context ---------------------------------------------------------------------------------------------------

export function Stage5Transition() {
  return (
    <TransitionSlide stage={5} notes={<>
      <p>Context: facts of the situation (break time, a warm room, a break just taken) set how likely the robot
        considers each foreseeable behaviour before it sees her move. Her observed movement still decides.</p>
      <p><strong>FIRST VERSION OF THE WORDING</strong> (tpres-v6, 9 October 2026), for Hadi: "the robot adapts its plan
        when the break is trusted" in place of "earlier".</p>
    </>} />
  );
}

export function Stage5Replay() {
  return (
    <ReplaySlide stage={5} title="Context: a sim-run" todo={<>
      A recorded sim-run with a context fact in force (break time), the same script with and without it if one exists:
      the prior favouring the coffee break, her movement still deciding.
    </>} notes={<>
      <p><strong>FIRST VERSION OF THE WORDING</strong> (tpres-v6, 9 October 2026), for Hadi.</p>
      <p><strong>HADI'S SCENARIO</strong>, exactly as he gave it: kitting scenario_s304_14 on env_layout_07
        (env_setup_304), context knowledge on, run file configs/kitting/tpres/stage5_s304_14_ck_on.yaml, ticks 70 to 150,
        the same scenario and period as talk stage 4 (context knowledge off). One click per stop.</p>
      <p>From the two runs' logs, for Hadi (on no slide): the coffee break is trusted at 116 here and at 106 in talk
        stage 4's run, and the robot's switch from item 56 to item 54 (item 56 would need a hold of 26 ticks) comes at
        the same ticks. Here the coffee break is lowered from tick 51 to 138, her first break observed complete at 49; this
        run has no timeline, so no context fact is in force on any tick.</p>
      {MIND}
    </>}>
      <ReplayBreakTime />
    </ReplaySlide>
  );
}

export function Stage5Architecture() {
  return (
    <ArchSlide stage={5} opens={["B41", "B44"]} notes={<>
      {FIRST}
      <p>Click 1: context appears, its prior going into the belief update.</p>
      <p>Click 2, belief update: the prior depends on the context. Taken off the panel: her assigned tasks together weigh
        1; each foreseeable behaviour weighs its strength, which the context sets: ordinary 0.02, raised by its
        favouring fact (break time: coffee break 2; a warm room: the A/C 0.5), lowered to 0.005 just after it happened.
        The likelihood is untouched: it holds no context.</p>
      <p>Click 3, confidence check: one condition added, observations still decide. Context may make the trust come
        earlier or later; it never makes the robot trust a hypothesis that her movement alone ranks below another (the
        evidence rank).</p>
    </>} />
  );
}

// ---- 6 Unmodelled behaviour --------------------------------------------------------------------------------------

export function Stage6Transition() {
  return (
    <TransitionSlide stage={6} notes={<>
      <p>One mechanism carries this talk stage: fit. The robot checks whether its hypotheses fit what she does; when none
        does, her behaviour is unexplained.</p>
      <p>Said only here, on no slide (the run of this stage shows neither; tpres-v5): when the trusted intention stops
        fitting, the robot stops trusting it; when she returns to a modelled behaviour, her task is trusted again.</p>
      <p>If she turns mid-way to something the robot knows, a coffee break, the belief moves to it and the robot trusts
        it (said only here, on no slide).</p>
      <p>She does something the robot has no model of: unmodelled behaviour, the only deviation in the glossary's sense
        (a part of what she does that the robot's task model lacks). This talk stage is the one place the talk says
        "deviation", and only for the unmodelled case. It may say here why common sense would call a coffee break a
        deviation and the framework does not: the coffee break is foreseen, in the robot's model.</p>
      <p>(The merge of 8 October 2026: the old talk stages 6, switch and resumption, and 7, unmodelled behaviour, are
        this one talk stage, since both rest on fit; since tpres-v4 it shows only unmodelled behaviour.)</p>
    </>} />
  );
}

export function Stage6Replay() {
  return (
    <ReplaySlide stage={6} title="Unmodelled behaviour: a sim-run"
                 todo={<>
      A recorded sim-run with unmodelled behaviour: no hypothesis fits, the projection from her motion takes over as the
      fallback. Why: the hardest case, and the one in which fit changes what the robot does.
    </>} notes={<>
      {FIRST}
      <p><strong>HADI'S SCENARIO</strong> (tpres-v4, 8 October 2026), the stage's one example: kitting scenario_s111_02 on
        env_layout_12, run file configs/kitting/tpres/stage6_s111_02.yaml, ticks 0 to 39 (tpres-v5: the replay ends while
        she stands). Her whole script is unmodelled: a walk to the north door, a stand of 60 seconds at spot_E (standing
        from 26 to 57), a walk to the south-east corner. Her assigned delivery of item 12 leads the belief but is never
        trusted: no support up to tick 9, and from 10 no hypothesis fits (unexplained). The robot uses the projection
        from her motion throughout: holds of 2 ticks at 14, 20 and 25, then 4 at 27, 8 at 31 and 16 at 39 while she
        stands, the projection of a stand reaching as far as she has stood. One click per stop.</p>
      <p>Not in this run: a trusted intention withdrawn (nothing was trusted before her behaviour became unexplained;
        before tick 10 the refusal was for lack of support, with the same projection from her motion), and her return
        to a modelled behaviour with her task trusted again (her script ends unmodelled). Beyond the replay, the robot
        decides a hold of 32 ticks at 55, which runs on after she walks off at 57; closest 50.44 cm (ticks 24 and
        56).</p>
      {MIND}
    </>}>
      <ReplayStand />
    </ReplaySlide>
  );
}

export function Stage6Architecture() {
  return (
    <ArchSlide stage={6} opens={["B42", "B44", "B51"]}
               caption="The reactive robot's projection from her motion is now the robot's fallback."
               notes={<>
      {FIRST}
      <p>Click 1: fit appears, going into the confidence check. New at this talk stage.</p>
      <p>Click 2, fit: for each hypothesis, how much later than its plan she would finish its current action, from her
        extra path and her extra standing. Taken off the panel: it fits unless that delay is surprising at a test level
        of 5 % (in kitting about 334 cm off the way, or 17 ticks of standing beyond the action). When the trusted
        intention stops fitting, the robot stops trusting it (withdrawing a trusted intention, one sentence) and plans
        again. When no hypothesis fits, her behaviour is unexplained: the robot knows that it does not know.</p>
      <p>Click 3, confidence check: the condition "it fits" added. In the code it is read from talk stage 3 on; the talk
        introduces it here, where it changes the outcome.</p>
      <p>Click 4, projection: with no trusted intention, the projection from her motion, the reactive robot's only option
        at talk stage 2, is now the fallback; when she returns to modelled behaviour and a hypothesis is trusted again,
        the projection from her intention returns.</p>
      <p>Click 5: the caption, the call back to talk stage 2.</p>
    </>} />
  );
}

// ---- After the six talk stages: no number on any slide (tpres-v5) -------------------------------------------------

export function RecapSlide() {
  return (
    <Slide stage={7} className="arch-slide" notes={<>
      {PLACEHOLDER}
      <p>Will show: the complete architecture, coloured by the three questions: what the robot knows (the knowledge
        column), what it believes (recognition), what it decides (adaptive planning). Its own content is part 3's.</p>
      <p><strong>OPEN</strong> (handoff 11): the explicit list of contributions the talk claims, marking what is new
        since June; settled after the architecture's content is final.</p>
    </>}>
      <ArchitectureView stage={7} step={false} colouring="questions" title={STAGES[7].title} />
    </Slide>
  );
}

function SideSlide({ stage, todo, by, notes, diagram }: {
  stage: TalkStage; todo: ReactNode; by: string; notes: ReactNode; diagram: boolean;
}) {
  return (
    <Slide stage={stage} className={`side-slide${diagram ? "" : " side-plain"}`} notes={notes}>
      <StageTitle stage={stage} />
      <div className="side">
        <Todo by={by} className={diagram ? "" : "todo-large"}>{todo}</Todo>
        {diagram && <div className="side-arch"><ArchitectureView stage={stage} step={false} title="" /></div>}
      </div>
    </Slide>
  );
}

export function LiftTruckSlide() {
  return (
    <SideSlide stage={8} by="part 3" diagram todo={<>
      The lift truck's turn: the same mind in dock loading, its room drawn by the web-ui's own code and, from part 4, a
      recorded dock_loading sim-run. Why: the second domain shows that the mind does not depend on kitting.
    </>} notes={<>
      {PLACEHOLDER}
      <p>Will say: the lift truck, waiting since the opening, gets its turn: the same mind in dock loading (defined with
        Scania). Nothing of the mind is written for one domain; the domain's knowledge is given, as the kitting robot's
        was.</p>
      <p><strong>OPEN</strong>: the wording of its return ("the robot changes jobs", or similar).</p>
    </>} />
  );
}

// ---- The results: Hadi's table, on four slides (tpres-v5) ---------------------------------------------------------

/** Hadi's table of measured results (8 October 2026, made in another chat from T-F's analyses), exactly as he gave it:
 * its columns, labels, numbers and words; neither traced nor reworded here, by his instruction. One slide per group of
 * rows, the two groups of one row each on one slide (tpres-v5: the single table was too small to read in a hall), each
 * row in large type with the two values drawn
 * as a pair of bars on one scale (a count "of" a total as a share of it, a range "to" with its span); a word (no
 * task known, reference) is shown as the word, without a bar. A row measured on one scenario (its n a scenario's id) is
 * marked. The bars are plain HTML and CSS: no library. */
type Row = [measure: string, without: string, withIt: string, betterIs: string, result: string, n: string];
const RESULTS: { stage: string; rows: Row[] }[] = [
  { stage: "Level 1, prediction from motion", rows: [
    ["Violation ticks", "137", "14", "lower", "better", "128 scen."],
    ["Closest distance (cm)", "18.5", "52.2", "higher", "better", "s10_02"],
    ["Completion delay (ticks, mean)", "0", "+5.8", "lower", "worse, 1%", "128 scen."],
  ] },
  { stage: "Level 2, recognition", rows: [
    ["Task known before the human arrives (ticks, median)", "no task known", "41", "higher", "better", "102 arrivals"],
    ["Tick of the robot's hold decision", "40", "25", "lower", "better", "s10_02"],
  ] },
  { stage: "Level 2, context knowledge", rows: [
    ["Ticks to admit a coffee break (median)", "39", "4", "lower", "better", "5 cases"],
    ["Tasks admitted earlier, human in accord", "reference", "52 of 66", "higher", "better", "66 tasks"],
    ["Runs that complete earlier, designed runs", "reference", "7 of 22", "higher", "better", "2 later"],
  ] },
  { stage: "Level 3, unmodelled", rows: [
    ["Ticks below min_separation (median)", "5.5", "3 to 4", "lower", "better", "20 scen."],
  ] },
  { stage: "Whole chain", rows: [
    ["Disagreements with the oracle", "", "0", "lower", "as designed", "1070 runs"],
  ] },
];

/** A value of the table read for its bar: a number, a count of a total, a range, or a word (no bar). */
type Value = { kind: "number"; v: number } | { kind: "share"; v: number; of: number }
  | { kind: "range"; lo: number; hi: number } | { kind: "word" };

function valueOf(text: string): Value {
  let m = /^([+-]?\d+(?:\.\d+)?)$/.exec(text);
  if (m !== null) return { kind: "number", v: Number(m[1]) };
  m = /^(\d+) of (\d+)$/.exec(text);
  if (m !== null) return { kind: "share", v: Number(m[1]), of: Number(m[2]) };
  m = /^(\d+(?:\.\d+)?) to (\d+(?:\.\d+)?)$/.exec(text);
  if (m !== null) return { kind: "range", lo: Number(m[1]), hi: Number(m[2]) };
  return { kind: "word" };
}

/** The scale of a row's bars: the larger of its two values (a share has its own total). */
function scaleOf(a: Value, b: Value): number {
  const top = (x: Value) => (x.kind === "number" ? Math.abs(x.v) : x.kind === "range" ? x.hi : 0);
  return Math.max(top(a), top(b));
}

function Bar({ value, scale, side }: { value: Value; scale: number; side: "without" | "with" }) {
  if (value.kind === "word") return null;
  const pct = (x: number, of: number) => `${of === 0 ? 0 : (100 * x) / of}%`;
  return (
    <span className={`rbar rbar-${side}`} aria-hidden>
      {value.kind === "number" && <span className="rbar-fill" style={{ width: pct(Math.abs(value.v), scale) }} />}
      {value.kind === "share" && <span className="rbar-fill" style={{ width: pct(value.v, value.of) }} />}
      {value.kind === "range" && <>
        <span className="rbar-fill" style={{ width: pct(value.lo, scale) }} />
        <span className="rbar-span" style={{ left: pct(value.lo, scale), width: pct(value.hi - value.lo, scale) }} />
      </>}
    </span>
  );
}

const ONE_SCENARIO = /^s\d+_\d+$/;

/** The groups each results slide shows: one group per slide, the two groups of one row each together. */
const RESULT_SLIDES: number[][] = [[0], [1], [2], [3, 4]];

function ResultRow({ row }: { row: Row }) {
  const [measure, without, withIt, betterIs, result, n] = row;
  const a = valueOf(without);
  const b = valueOf(withIt);
  const scale = scaleOf(a, b);
  return (
    <div className={`r-row${ONE_SCENARIO.test(n) ? " r-one" : ""}`} role="row">
      <span className="r-measure" role="cell">{measure}</span>
      <span className="r-value r-without" role="cell">
        <span className={a.kind === "word" ? "r-word" : "r-num"}>{without === "" ? "–" : without}</span>
        <Bar value={a} scale={scale} side="without" />
      </span>
      <span className="r-value r-with" role="cell">
        <span className={b.kind === "word" ? "r-word" : "r-num"}>{withIt}</span>
        <Bar value={b} scale={scale} side="with" />
      </span>
      <span className="r-better" role="cell">{betterIs}</span>
      <span className={`r-result${result.startsWith("worse") ? " r-worse" : ""}`} role="cell">{result}</span>
      <span className="r-n" role="cell">{n}</span>
    </div>
  );
}

function ResultsSlide({ groups }: { groups: number[] }) {
  const gs = groups.map((i) => RESULTS[i]);
  const names = gs.map((g) => g.stage).join("; ");
  return (
    <Slide stage={9} className="results-slide" notes={<>
      <p><strong>FIRST VERSION</strong> (T-pres, 8 October 2026; on four slides since tpres-v5): Hadi's table of measured
        results, made in another chat from T-F's analyses, placed exactly as he gave it. ccode has not traced, checked,
        reworded or regrouped it (Hadi's instruction). Its words are the earlier ones (levels, "prediction", "admit",
        min_separation), not yet the deck's present terms.</p>
      <p>{names}. Each row: the measure; without and with, as numbers and as a pair of bars on one scale (a count of a
        total as its share); which direction is better; the result; n. A row whose n is a scenario (s10_02) is measured
        on that one scenario; the others over many runs, scenarios or cases.</p>
      {groups.includes(0) && <p>Keep the row where the result is worse (the completion delay): the cost is shown as
        well.</p>}
    </>}>
      <div className="results-head">
        <StageTitle stage={9} />
        {gs.length === 1 && <p className="results-group">{gs[0].stage}</p>}
      </div>
      <div className="results" role="table" aria-label={`Results: ${names}`}>
        <div className="r-row r-labels" role="row">
          <span role="columnheader">Measure</span><span role="columnheader">Without</span>
          <span role="columnheader">With</span><span role="columnheader">Better is</span>
          <span role="columnheader">Result</span><span role="columnheader">n</span>
        </div>
        {gs.map((g) => (
          <div key={g.stage} role="rowgroup">
            {gs.length > 1 && <p className="r-group" role="row">{g.stage}</p>}
            {g.rows.map((r) => <ResultRow key={r[0]} row={r} />)}
          </div>
        ))}
      </div>
    </Slide>
  );
}

export const ResultsSlides = RESULT_SLIDES.map((groups, i) => {
  const S = () => <ResultsSlide groups={groups} />;
  S.displayName = `Results${i + 1}`;
  return S;
});

// ---- The afternoon, and the end -----------------------------------------------------------------------------------

export function AfternoonSlide() {
  return (
    <SideSlide stage={10} by="part 5" diagram={false} todo={<>
      The afternoon station: the web-ui, with a screenshot (Hadi or part 4) labelled with what the audience learned to
      read in the talk: the env-pane, the robot's panel (intention recognition, planning), the human's panel. Why: the
      talk is the entry point to the station.
    </>} notes={<>
      {PLACEHOLDER}
      <p>Will say: come to the station this afternoon. The same names and drawings as in the talk: blue the robot, orange
        the human, the dashed blue plan, the blue stripe of the robot's projection of her (filled from her intention,
        hatched from her motion), and the robot panel's bars of the hypotheses, as beside every replay.</p>
      <p><strong>OPEN</strong> (handoff 7): whether the web-ui's two labels "Prediction from intention" and "Prediction
        from motion" change; the slides say "projection".</p>
    </>} />
  );
}

/** The last slide (Hadi, tpres-v5): "Thank you", with the kitting robot, the lift truck and the two humans (the kitting
 * worker and the dock worker) standing together, drawn by the web-ui's own figures (scene/Ensemble.tsx). */
export function ThankYouSlide() {
  return (
    <Slide stage={11} footer={false} className="thanks-slide" notes={<>
      <p>Thank you. Questions (about 5 minutes).</p>
      <p>The four figures are the web-ui's own: the kitting worker and the kitting robot, the lift truck and the dock
        worker, as at the station this afternoon.</p>
    </>}>
      <h1 className="thanks-head">Thank you</h1>
      <Ensemble />
    </Slide>
  );
}
