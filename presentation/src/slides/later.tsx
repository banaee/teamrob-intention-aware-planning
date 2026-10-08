/**
 * Levels 2 and 3 and talk stages 3 to 12. Talk stages 3 to 7, a first version: each talk stage's card (its keywords,
 * and the sim-run that will show it), then the architecture, a click adding what the talk stage adds and one click
 * per block it opens or extends (architecture/unboxing.tsx: Hadi, 8 October 2026, preferred). Talk stages 8 to 12 stay
 * placeholders (parts 3 and 5).
 */

import type { ReactNode } from "react";

import type { Unboxable } from "../architecture/unboxing";
import { STAGES, type TalkStage } from "../talk";
import { ArchitectureView, LevelTitle, Slide, StageCard, StageTitle, Todo } from "./kit";

/** A talk stage's card. `scene` (a replayed sim-run) stands in the TODO box's place once it exists; the box's text then
 * goes to the notes. */
function CardSlide({ stage, todo, by = "part 4", notes, scene }: {
  stage: TalkStage; todo: ReactNode; by?: string; notes: ReactNode; scene?: ReactNode;
}) {
  return (
    <Slide stage={stage} className={`card-slide${scene !== undefined ? " card-scene" : ""}`} notes={<>
      {notes}
      {scene !== undefined && <p><strong>TODO ({by})</strong>, the box this draft stands in: {todo}</p>}
    </>}>
      <StageCard stage={stage}>
        {scene ?? <Todo by={by} className="todo-card">{todo}</Todo>}
      </StageCard>
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

const FIRST = <p><strong>FIRST VERSION</strong> (T-pres, 8 October 2026), for Hadi's revision.</p>;
const PLACEHOLDER = <p><strong>PLACEHOLDER</strong> (T-pres part 1): the content is built in a later part.</p>;

// ---- Level 2 ---------------------------------------------------------------------------------------------------

export function Level2Slide() {
  return (
    <Slide stage={3} className="level-slide" notes={<>
      <p>Level 2: Anton works with her. What Anton knows grows, one kind of knowledge per stage: her task list, the
        behaviours one can foresee, the situation.</p>
    </>}>
      <LevelTitle level={2} />
    </Slide>
  );
}

export const STAGE3_TODO = <>
  A recorded sim-run in the web-ui's look: the belief over her tasks rising as she walks, the confidence check
  passing, the projection from her intention on the floor (a filled blue stripe), and Anton's hold or task choice
  against it. Why: this is where recognition first changes what Anton does.
</>;

export function Stage3Card({ scene }: { scene?: ReactNode }) {
  return (
    <CardSlide stage={3} todo={STAGE3_TODO} scene={scene} notes={<>
      {FIRST}
      <p>Anton now knows her task list. What it believes: which of her tasks she is doing. What it decides: its own
        next task and hold, against where her task will take her. The heaviest stage: most of the time goes here.</p>
    </>} />
  );
}

export function Stage3Architecture() {
  return (
    <ArchSlide stage={3} opens={["B41", "B43", "B44", "B51", "B53", "B54"]} notes={<>
      {FIRST}
      <p>Click 1: recognition appears with belief update, support and the confidence check; C1 gains her task list; the
        world state gives her actions to recognition. The arrow "trusted intention, or none" is the visual centre: where
        recognition affects planning. Task choice takes the realizer's cost; the realizer's direct arrow to execute
        gives way.</p>
      <p>Click 2, belief update: the one formula: belief = prior times evidence, normalised over H, with H her assigned
        tasks. The evidence is her movement: walking off the shortest way to a step's target, or standing longer than
        the step takes, lowers it. The prior is equal for now; talk stage 5 opens it.</p>
      <p>Click 3, support: a belief needs support from what she actually does: a step toward the target, or a completion
        Anton saw. Knowing which task is probable does not say when she starts.</p>
      <p>Click 4, confidence check: the leader is trusted when it is strong enough (θ = 0.75) and supported; out comes
        the trusted intention, or none. In the code the check also reads fit from here on; the talk adds it at talk
        stage 6. In the code the check is the meta-planner's gate; the talk places it in recognition, because
        everything it reads is recognition's output.</p>
      <p>Click 5, projection: from her intention, her path is the plan of the trusted task, decomposed with the same
        task knowledge Anton plans its own work with. Say it here, once: one knowledge, two uses; the AAAI paper's
        first contribution in one sentence, and why talk stage 1 was not wasted.</p>
      <p>Click 6, realizer: per task of Anton's plan, the smallest hold that keeps the minimum separation (50 cm in the
        simulation) from her projected path; cost = duration plus holds. A hold always exists.</p>
      <p>Click 7, task choice: each candidate (one task, or an ordering) realized, the cheapest chosen. That is where a
        switch or a reorder comes from; only the first hold is carried out.</p>
    </>} />
  );
}

export const STAGE4_TODO = <>
  A recorded sim-run with a coffee break: the break recognised, and a visible planning consequence, for example a
  reorder caused by the trusted break. Why: one later stage should show planning change, not only recognition.
</>;

export function Stage4Card({ scene }: { scene?: ReactNode }) {
  return (
    <CardSlide stage={4} todo={STAGE4_TODO} scene={scene} notes={<>
      {FIRST}
      <p>Anton also knows what people foreseeably do besides their tasks: a coffee break, switching on the A/C. A coffee
        break is modelled behaviour, foreseen: Anton plans around her break. Words: "foreseeable behaviours".</p>
    </>} />
  );
}

export function Stage4Architecture() {
  return (
    <ArchSlide stage={4} opens={["B41"]} notes={<>
      {FIRST}
      <p>Click 1: knowledge about the human (C2) appears, its foreseeable behaviours going to recognition.</p>
      <p>Click 2, belief update again: the same formula; only H grows, by the foreseeable behaviours. Nothing else in
        the mind changes: the same blocks now also recognise a break.</p>
    </>} />
  );
}

export const STAGE5_TODO = <>
  A recorded sim-run with a fact in force (break time), the same script with and without it if one exists: the prior
  favouring the coffee break, its trust coming earlier, her movement still deciding. Why: the audience sees the situation
  make Anton adapt earlier.
</>;

export function Stage5Card({ scene }: { scene?: ReactNode }) {
  return (
    <CardSlide stage={5} todo={STAGE5_TODO} scene={scene} notes={<>
      {FIRST}
      <p>Context: facts of the situation (break time, a warm room, a break just taken) set how strongly Anton considers
        each foreseeable behaviour. The prior favours what the situation makes likely; observations still decide.</p>
      <p>Measured (T-F part 1, COMPARISON.md, step 3b): with a fact in force, a fact in accord with her task speeds its
        trust, one not in accord delays it, with little change in completion. A number on a slide comes from an actual
        run.</p>
    </>} />
  );
}

export function Stage5Architecture() {
  return (
    <ArchSlide stage={5} opens={["B41", "B44"]} notes={<>
      {FIRST}
      <p>Click 1: context (C3) appears, its prior going into the belief update.</p>
      <p>Click 2, belief update: the prior opened. Her assigned tasks together weigh 1; each foreseeable behaviour weighs
        its strength, which the situation sets: ordinary 0.02, raised by its favouring fact (break time: coffee break 2;
        a warm room: the A/C 0.5), lowered to 0.005 just after it happened. The evidence is untouched.</p>
      <p>Click 3, confidence check: one condition added: observations still decide. Context may make the trust come
        earlier; it never makes Anton trust a task that her movement alone ranks below another (the evidence rank).</p>
    </>} />
  );
}

// ---- Level 3 ---------------------------------------------------------------------------------------------------

export function Level3Slide() {
  return (
    <Slide stage={6} className="level-slide" notes={<>
      <p>Level 3: Anton keeps up with her. Anton checks whether its belief still fits.</p>
      <p>From here on the talk may say "deviation", in the glossary's sense only (talk stage 7). It may say once why
        common sense would call a coffee break a deviation and the framework does not.</p>
    </>}>
      <LevelTitle level={3} />
    </Slide>
  );
}

export const STAGE6_TODO = <>
  A recorded sim-run in which she switches mid-way and later resumes: the trusted belief stops fitting, Anton stops
  trusting it and replans against the projection from her motion, and recognition picks her up again when she resumes.
  Why: fit is what makes Anton keep up; the audience sees it change the outcome.
</>;

export function Stage6Card({ scene }: { scene?: ReactNode }) {
  return (
    <CardSlide stage={6} todo={STAGE6_TODO} scene={scene} notes={<>
      {FIRST}
      <p>She switches mid-way: Anton's trusted belief no longer explains what she does. Anton notices, stops trusting it,
        and replans; when she resumes, recognition picks it up again.</p>
    </>} />
  );
}

export function Stage6Architecture() {
  return (
    <ArchSlide stage={6} opens={["B42", "B44"]} notes={<>
      {FIRST}
      <p>Click 1: fit (B4.2) appears, going into the confidence check.</p>
      <p>Click 2, fit: for each hypothesis, how much later than its plan she would finish its current step; it fits
        unless that delay is surprising at 5 % (about 334 cm off the way, or 17 ticks of standing). When the trusted
        hypothesis stops fitting, Anton stops trusting it (withdrawing a trusted belief, one sentence) and replans,
        against the projection from her motion until a belief is trusted again.</p>
      <p>Click 3, confidence check: the condition "it fits" added. In the code it was read from talk stage 3 on; the
        talk introduces it here, where it changes the outcome.</p>
    </>} />
  );
}

export const STAGE7_TODO = <>
  A recorded sim-run with unmodelled behaviour (for example a walk to a corner): no hypothesis fits, the projection
  from her motion takes over as the fallback, and recognition resumes when she returns to modelled behaviour. Why: the
  hardest case, handled by blocks the audience already knows.
</>;

export function Stage7Card({ scene }: { scene?: ReactNode }) {
  return (
    <CardSlide stage={7} todo={STAGE7_TODO} scene={scene} notes={<>
      {FIRST}
      <p>She does something nobody modelled: the only deviation in the glossary's sense (a node of her plan the robot's
        model lacks). Words: "unmodelled behaviour".</p>
    </>} />
  );
}

export function Stage7Architecture() {
  return (
    <ArchSlide stage={7} opens={["B42", "B51"]}
               caption="Nothing new: fit, now for every hypothesis, and the projection from motion, now as a fallback."
               notes={<>
      {FIRST}
      <p>Click 1: nothing is added. Click 2: the caption: the hardest case is handled by blocks the audience already
        knows.</p>
      <p>Click 3, fit: no hypothesis fits: her behaviour is unexplained; Anton knows that it does not know.</p>
      <p>Click 4, projection: with no trusted intention, the projection from her motion, the reactive robot's only option
        at talk stage 2, is now a deliberate fallback; when she returns to modelled behaviour and a belief is trusted
        again, the projection from her intention returns. The call back to talk stage 2.</p>
    </>} />
  );
}

// ---- After the levels ------------------------------------------------------------------------------------------

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
      The levels measured, in both domains: level 1 is the intention-unaware run, levels 2 and 3 together the
      intention-aware run (T-F part 1, analysis/kitting/tf1/REPORT.md and COMPARISON.md; dock loading's measurements).
      Every number from an actual run. Why: evidence for the mechanisms the talk showed.
    </>} notes={<>
      {PLACEHOLDER}
      <p>Will show: the levels as run conditions. Human-unaware may appear as a mode of the implementation. The oracle
        (as if Anton could see her intention) is the upper bound only if it is built (TODO-101, recorded, not
        built).</p>
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
        from her motion).</p>
      <p><strong>OPEN</strong> (handoff 7): whether the web-ui's two labels "Prediction from intention" and "Prediction
        from motion" change; the slides say "projection".</p>
    </>} />
  );
}
