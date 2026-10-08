/**
 * Talk stages 3 to 12. Talk stages 3 to 7 (the overall revision of 8 October 2026): each opens with its transition
 * slide (the seven talk stages, the starting one with its three columns), then a replayed sim-run with Anton's mind
 * beside it, then the architecture, a click adding what the talk stage adds and one click per block it opens or extends
 * (architecture/unboxing.tsx). Talk stages 8 to 12 stay placeholders (parts 3 and 5). A replay that does not yet meet
 * its criterion (the mechanism visibly changes what Anton does) carries the mark "not settled".
 */

import type { ReactNode } from "react";

import type { Unboxable } from "../architecture/unboxing";
import { STAGES, type TalkStage } from "../talk";
import { ArchitectureView, Slide, StageTitle, Todo, TransitionSlide, Unsettled } from "./kit";
import { ReplayBreak, ReplayBreakTime, ReplayStand, ReplaySwitch, ReplayTrusted } from "./replays";

/** A talk stage's replayed sim-run, with Anton's mind beside it. `todo`: what the TODO box this replay stands in asked
 * for (in the notes); `unsettled`: a visible mark where the replay does not yet meet its criterion. */
function ReplaySlide({ stage, title, notes, todo, unsettled, children }: {
  stage: TalkStage; title: string; notes: ReactNode; todo: ReactNode; unsettled?: ReactNode; children: ReactNode;
}) {
  return (
    <Slide stage={stage} className="replay-slide" notes={<>
      {notes}
      <p><strong>TODO (part 4)</strong>, the box this draft stands in: {todo}</p>
    </>}>
      {unsettled !== undefined && <Unsettled>{unsettled}</Unsettled>}
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
const MIND = <p>Beside the scene, Anton's mind at the tick, as the robot panel at the station shows it: the hypotheses
  as bars (θ the thin line on each), the trusted intention marked; its task, its hold, which projection of her it
  uses.</p>;

// ---- 3 Assigned tasks --------------------------------------------------------------------------------------------

export function Stage3Transition() {
  return (
    <TransitionSlide stage={3} notes={<>
      <p>Anton now knows her task list: the tasks she is assigned. What it believes: which of her tasks she is doing.
        What it decides: its own next task and hold, against where her task will take her.</p>
      <p>The heaviest stage: most of the time goes here.</p>
    </>} />
  );
}

export function Stage3Replay() {
  return (
    <ReplaySlide stage={3} title="Assigned tasks: a sim-run" todo={<>
      A recorded sim-run in the web-ui's look: the belief over her tasks rising as she walks, the confidence check
      passing, the projection from her intention on the floor (a filled blue stripe), and Anton's hold or task choice
      against it. Why: this is where recognition first changes what Anton does.
    </>} notes={<>
      {FIRST}
      <p><strong>DRAFT</strong> (the second search, 8 October 2026): kitting scenario_s12_01 on env_layout_14, T-F part
        1's run_060 (intention-aware), ticks 0 to 62. Her delivery of item 1 trusted at 8 (0.78), and Anton switches
        from item 7 to item 13: task choice changes what Anton does. In the intention-unaware run_058 Anton carries item 7
        across her route, with holds at 40 (5 ticks), 103 (4) and 113 (1). Weakness: item 7's and item 13's shelves are
        close on one approach line, so the switch shows from the carry on (tick 29). The earlier draft, run_008 of
        scenario_s10_02, held 5 ticks far from her. One click per stop.</p>
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
      <p>Click 2, belief update: Bayes. The hypotheses H are her assigned tasks; o is what Anton has seen her do. Taken
        off the panel: the likelihood P(o | h) is a product over the actions of h, one factor L(x) = 2 / (1 + e^(βx)) per
        action, x her extra path beyond the shortest way to the action's target plus her standing beyond what the
        action takes (β = 0.01 per cm). The prior is equal for now; talk stage 5 opens it.</p>
      <p>Click 3, support: a belief needs support from what she actually does. Knowing which task is probable does not
        say when she starts. A wait has only the second source (a completion Anton saw).</p>
      <p>Click 4, confidence check: the leader is trusted when it is strong enough (θ = 0.75) and supported; out comes
        the trusted intention, or none. In the code the check also reads fit from here on; the talk adds it at talk
        stage 6. In the code the check is the meta-planner's gate; the talk places it in recognition, because everything
        it reads is recognition's output.</p>
      <p>Click 5, projection: from her intention, her path is the plan of the trusted task, broken down into actions from
        where she is now: where she will be, and when. Say it here, once: one knowledge, two uses; the AAAI paper's first
        contribution in one sentence, and why talk stage 1 was not wasted.</p>
      <p>Click 6, realizer: per task of Anton's plan, in order, the smallest hold in whole ticks such that Anton's moving
        path never comes closer than the minimum separation (50 cm in the simulation) to her projected path; a later
        task's hold counts from the holds before it. Cost: the plan's duration plus its holds.</p>
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
      <p>Anton also knows what people foreseeably do besides their tasks: a coffee break, switching on the A/C. A coffee
        break is modelled behaviour, foreseen. Words: "foreseeable behaviours"; never a deviation.</p>
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
      <p><strong>DRAFT</strong> (the second search): kitting scenario_s24_14 on env_layout_07, T-F part 1's run_264
        (context knowledge on, no fact in force), ticks 85 to 150. The coffee break trusted at 116 (0.78), and Anton
        switches from item 56 to item 54; the human-unaware run_261 does item 56 at 85 to 169. Weakness: from 90 to 114
        Anton walks about 55 cm behind her. The earlier draft, run_064 of scenario_s12_02, held 18 ticks with no change of
        task. One click per stop.</p>
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
      <p>Context: facts of the situation (break time, a warm room, a break just taken) set how likely Anton considers
        each foreseeable behaviour before it sees her move. Her observed movement still decides.</p>
    </>} />
  );
}

export function Stage5Replay() {
  return (
    <ReplaySlide stage={5} title="Context: a sim-run" todo={<>
      A recorded sim-run with a context fact in force (break time), the same script with and without it if one exists:
      the prior favouring the coffee break, its trust coming earlier, her movement still deciding. Why: the audience
      sees the situation make Anton adapt earlier.
    </>} notes={<>
      {FIRST}
      <p><strong>DRAFT</strong> (the second search): kitting scenario_s23_03 on env_layout_07 (scenario_s05_01 with break
        time in force from 0 to 56), T-F part 1's run_576, ticks 0 to 62: the coffee break leads from tick 0 (0.66) and is
        trusted at 27 (0.76); Anton switches to item 2 and walks away, no violation. The same shift without the fact
        (scenario_s05_01, run_108, context knowledge on): the break is trusted only at 52, Anton passes her at 31.62 cm at
        tick 28 (3 ticks below the minimum separation). Weakness: in run_108 the context makes the start worse than
        with context knowledge off (her walk read as deliver item 5 at 0.97; off, run_107, the break is trusted at 32).
        The earlier draft, run_707 against run_064, changed only where and when Anton paused. One click per stop.</p>
      <p>Measured (T-F part 1, COMPARISON.md, step 3b): with a fact in force, a fact in accord with her task speeds its
        trust, one not in accord delays it, with little change in completion. A number on a slide comes from an actual
        run.</p>
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
        earlier; it never makes Anton trust a hypothesis that her movement alone ranks below another (the evidence
        rank).</p>
    </>} />
  );
}

// ---- 6 Switch and resumption -------------------------------------------------------------------------------------

export function Stage6Transition() {
  return (
    <TransitionSlide stage={6} notes={<>
      <p>She leaves a task mid-way: Anton's trusted intention no longer explains what she does. Anton notices, stops
        trusting it, and plans again; when she resumes, her task is trusted again.</p>
    </>} />
  );
}

export function Stage6Replay() {
  return (
    <ReplaySlide stage={6} title="Switch and resumption: a sim-run"
                 unsettled="In this run the trust ends because the break overtakes her delivery, not because it stops fitting."
                 todo={<>
      A recorded sim-run in which she switches mid-way and later resumes: the trusted intention stops fitting, Anton
      stops trusting it and plans again against the projection from her motion, and recognition picks her up again when
      she resumes. Why: fit is what makes Anton keep pace with her; the audience sees it change the outcome.
    </>} notes={<>
      {FIRST}
      <p><strong>DRAFT</strong> (the second search): kitting scenario_s23_23 on env_layout_07, T-F part 1's run_584
        (break time in force from 48 to 84), ticks 30 to 100. Her delivery trusted at 36, a hold of 7; the coffee break
        cut in at 48 leads, and Anton stops trusting the delivery; the break trusted at 53, a hold (planned 33, 29
        stood); her break over at 82, a new hold; she resumes at 84; the delivery trusted again at 94, the hold ends
        after 12 ticks and Anton walks on.</p>
      <p><strong>NOT SETTLED</strong>: in this run the trust ends at 48 because the coffee break overtakes the delivery
        (the log's cause "replaced"), not because the delivery stops fitting: the delivery is adequate throughout. The
        switch and the resumption change what Anton does; fit is not what changes it. The earlier draft, run_012 of
        scenario_s10_03, shows fit (the delivery stops fitting at 55) but Anton's tasks are those of the human-unaware
        run_009, with no hold: fit changes nothing for Anton there. Hadi chooses, or authors a scenario.</p>
      {MIND}
    </>}>
      <ReplaySwitch />
    </ReplaySlide>
  );
}

export function Stage6Architecture() {
  return (
    <ArchSlide stage={6} opens={["B42", "B44"]} notes={<>
      {FIRST}
      <p>Click 1: fit appears, going into the confidence check.</p>
      <p>Click 2, fit: for each hypothesis, how much later than its plan she would finish its current action, from her
        extra path and her extra standing. Taken off the panel: it fits unless that delay is surprising at a test level
        of 5 % (in kitting about 334 cm off the way, or 17 ticks of standing beyond the action). When the trusted
        intention stops fitting, Anton stops trusting it (withdrawing a trusted intention, one sentence) and plans again,
        against the projection from her motion until a hypothesis is trusted again.</p>
      <p>Click 3, confidence check: the condition "it fits" added. In the code it was read from talk stage 3 on; the talk
        introduces it here, where it changes the outcome.</p>
    </>} />
  );
}

// ---- 7 Unmodelled behaviour --------------------------------------------------------------------------------------

export function Stage7Transition() {
  return (
    <TransitionSlide stage={7} notes={<>
      <p>She does something the robot has no model of: unmodelled behaviour, the only deviation in the glossary's sense
        (a part of what she does that Anton's task model lacks). This is the one place the talk says "deviation". It may
        say here why common sense would call a coffee break a deviation and the framework does not: the coffee break is
        foreseen, in Anton's model.</p>
    </>} />
  );
}

export function Stage7Replay() {
  return (
    <ReplaySlide stage={7} title="Unmodelled behaviour: a sim-run"
                 unsettled="No existing run shows Anton act differently on it: Anton is far from her. A scenario is proposed."
                 todo={<>
      A recorded sim-run with unmodelled behaviour (for example a walk to a corner): no hypothesis fits, the projection
      from her motion takes over as the fallback, and recognition resumes when she returns to modelled behaviour. Why:
      the hardest case, handled by blocks the audience already knows.
    </>} notes={<>
      {FIRST}
      <p><strong>DRAFT</strong>: kitting scenario_s10_07 on env_layout_12, run_028, ticks 40 to 125. One click per
        stop.</p>
      <p><strong>NOT SETTLED</strong>: no existing run meets the criterion (the second search, 8 October 2026: no
        retraction at an unexplained finding is followed by a hold or a switch within 40 ticks). Here Anton's tasks are
        those of the human-unaware run_025, no hold, Anton at least 405 cm away. The proposal for Hadi to author is in
        the report of the overall revision.</p>
      {MIND}
    </>}>
      <ReplayStand />
    </ReplaySlide>
  );
}

export function Stage7Architecture() {
  return (
    <ArchSlide stage={7} opens={["B42", "B51"]}
               caption="Nothing new: fit, now for every hypothesis, and the projection from her motion, now as the fallback."
               notes={<>
      {FIRST}
      <p>Click 1: nothing is added. Click 2: the caption: the hardest case is handled by blocks the audience already
        knows.</p>
      <p>Click 3, fit: no hypothesis fits: her behaviour is unexplained; Anton knows that it does not know.</p>
      <p>Click 4, projection: with no trusted intention, the projection from her motion, the reactive robot's only option
        at talk stage 2, is now the fallback; when she returns to modelled behaviour and a hypothesis is trusted again,
        the projection from her intention returns. The call back to talk stage 2.</p>
    </>} />
  );
}

// ---- After the seven talk stages -----------------------------------------------------------------------------------

export function Stage8Recap() {
  return (
    <Slide stage={8} className="arch-slide" notes={<>
      {PLACEHOLDER}
      <p>Will show: the complete architecture, coloured by the three questions: what Anton knows (the knowledge
        column), what it believes (recognition), what it decides (adaptive planning). Its own content is part 3's.</p>
      <p><strong>OPEN</strong> (handoff 11): the explicit list of contributions the talk claims, marking what is new
        since June; settled after the architecture's content is final.</p>
    </>}>
      <ArchitectureView stage={8} step={false} colouring="questions" title={`8 ${STAGES[8].title}`} />
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

export function Stage9() {
  return (
    <SideSlide stage={9} by="part 3" diagram todo={<>
      The lift truck's turn: the same mind in dock loading, its room drawn by the web-ui's own code and, from part 4, a
      recorded dock_loading sim-run. Why: the second domain shows that the mind does not depend on kitting.
    </>} notes={<>
      {PLACEHOLDER}
      <p>Will say: the lift truck, waiting since the opening, gets its turn: the same mind in dock loading (defined with
        Scania). Nothing of the mind is written for one domain; the domain's knowledge is given, as Anton's was.</p>
      <p><strong>OPEN</strong>: the wording ("Anton changes jobs", or similar), the lift truck's and the dock worker's
        names.</p>
    </>} />
  );
}

export function Stage10() {
  return (
    <SideSlide stage={10} by="part 5" diagram={false} todo={<>
      The talk stages measured, in both domains: talk stage 2 is the intention-unaware run, talk stages 3 to 7 together
      the intention-aware run (T-F part 1, analysis/kitting/tf1/REPORT.md and COMPARISON.md; dock loading's
      measurements). Every number from an actual run. Why: evidence for the mechanisms the talk showed.
    </>} notes={<>
      {PLACEHOLDER}
      <p>Will show: the talk stages as run conditions (the levels of the handoff, removed from the slides in the overall
        revision). Human-unaware may appear as a mode of the implementation. The oracle (as if Anton could see her
        intention) is the upper bound only if it is built (TODO-101, recorded, not built).</p>
      <p><strong>PARKED</strong> (E1): every stage's illustration a moment from a real sim-run, so that evidence
        accumulates along the talk.</p>
    </>} />
  );
}

export function Stage11() {
  return (
    <SideSlide stage={11} by="part 5" diagram={false} todo={<>
      Limits and outlook, as Hadi chooses them. Why: an industrial audience needs to know what the framework does not do
      yet.
    </>} notes={<>
      {PLACEHOLDER}
      <p>Candidates from the records, for Hadi to choose: the framework does no perception (the simulator hands over
        her micro-actions); paths are assumed straight; communication (Hadi plans a minimal signal before demo day;
        "communication: none" in the diagram changes when it is built); degrees of context (T-K part 2); the execution
        on ROS (T-S, future work).</p>
    </>} />
  );
}

export function Stage12() {
  return (
    <SideSlide stage={12} by="part 5" diagram={false} todo={<>
      The afternoon station: the web-ui, with a screenshot (Hadi or part 4) labelled with what the audience learned to
      read in the talk: the env-pane, the robot's panel (intention recognition, planning), the human's panel. Why: the
      talk is the entry point to the station.
    </>} notes={<>
      {PLACEHOLDER}
      <p>Will say: come to the station this afternoon. The same names and drawings as in the talk: blue Anton, orange
        Donny, the dashed blue plan, the blue stripe of Anton's projection of her (filled from her intention, hatched
        from her motion), and the robot panel's bars of the hypotheses, as beside every replay.</p>
      <p><strong>OPEN</strong> (handoff 7): whether the web-ui's two labels "Prediction from intention" and "Prediction
        from motion" change; the slides say "projection".</p>
    </>} />
  );
}
