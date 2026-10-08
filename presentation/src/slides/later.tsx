/**
 * Talk stages 3 to 12 and levels 2 and 3, as placeholders (T-pres part 1): each talk stage's card with the keywords of
 * section 5 and a TODO box for what it will show, the architecture in that talk stage's state, and speaker notes that
 * say what the stage will say. Parts 2, 3 and 5 build their content; part 4 fills the boxes that need a sim-run.
 */

import type { ReactNode } from "react";

import { STAGES, type TalkStage } from "../talk";
import { ArchitectureView, LevelTitle, Slide, StageCard, StageTitle, Todo } from "./kit";

function CardSlide({ stage, todo, by = "part 4", notes }: {
  stage: TalkStage; todo: ReactNode; by?: string; notes: ReactNode;
}) {
  return (
    <Slide stage={stage} className="card-slide" notes={notes}>
      <StageCard stage={stage}>
        <Todo by={by} className="todo-card">{todo}</Todo>
      </StageCard>
    </Slide>
  );
}

function ArchSlide({ stage, notes, caption }: { stage: TalkStage; notes: ReactNode; caption?: string }) {
  return (
    <Slide stage={stage} className="arch-slide" notes={notes}>
      <ArchitectureView stage={stage} title="The architecture so far" />
      {caption !== undefined && <p className="arch-caption fragment">{caption}</p>}
    </Slide>
  );
}

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

export function Stage3Card() {
  return (
    <CardSlide stage={3} by="part 2 and part 4" todo={<>
      The belief formula, written once: belief = normalise(prior × evidence) over H, with H = {"{"}assigned tasks{"}"}{" "}
      beside it. Then a recorded sim-run in the web-ui's look with the robot's panel: the belief over her tasks rising
      as she walks, the confidence check passing, the projection from her intention on the floor (a filled blue
      stripe), and Anton's hold or task choice against it. Why: this is where recognition first changes what Anton
      does.
    </>} notes={<>
      {PLACEHOLDER}
      <p>Will say: Anton now knows her task list. It is the same task knowledge Anton plans its own work with (C1):
        one knowledge, two uses, the AAAI paper's first contribution in one sentence; why talk stage 1 was not wasted
        (handoff, addition a).</p>
      <p>Believe: H is her assigned tasks. The belief update: belief = normalise(prior × evidence) over H, the one
        formula of the talk, written here and kept fixed; only H changes beside it later. Support: her movement toward
        a task's next target, or an observed completion. The confidence check admits the leading belief when it is at
        least θ (0.75), has support, and the evidence alone ranks no other hypothesis above it. (It also reads fit; the
        talk introduces fit at talk stage 6.)</p>
      <p>Decide: the trusted intention (or none) goes to the projection: from her intention, her admitted task's plan.
        The realizer: for each task of a candidate plan, the smallest hold that keeps Anton's moving path at the
        minimum separation from her projected path; its cost is the plan's duration plus the hold. Task choice: the
        cheapest candidate, one task (switch) or an ordering of all (reorder), only the first hold executed.</p>
      <p>The heaviest stage: most of the time goes here. Mechanisms shown abstractly, no flowcharts.</p>
    </>} />
  );
}

export function Stage3Architecture() {
  return (
    <ArchSlide stage={3} notes={<>
      {PLACEHOLDER}
      <p>Click: recognition (C4) appears with belief update, support and the confidence check; C1 gains her task list;
        the world state gives her actions to recognition. The one arrow from recognition to planning, "trusted
        intention, or none", is the visual centre: where recognition affects planning. Task choice takes the realizer's
        cost and sends the next task and hold; the direct arrow from the realizer to execute gives way.</p>
      <p>In the code the confidence check is the meta-planner's gate; the talk places it in recognition, because
        everything it reads is recognition's output.</p>
    </>} />
  );
}

export function Stage4Card() {
  return (
    <CardSlide stage={4} by="part 2 and part 4" todo={<>
      H growing beside the fixed formula: H = {"{"}assigned tasks + foreseeable behaviours{"}"}. Then a recorded
      sim-run of an existing kitting scenario with a coffee break: the break recognised, and a visible planning
      consequence, for example a reorder caused by the admitted break. Why: one later stage should show planning
      change, not only recognition.
    </>} notes={<>
      {PLACEHOLDER}
      <p>Will say: Anton also knows what people foreseeably do besides their tasks: a coffee break, switching on the
        A/C (C2, knowledge about the human). H grows to her assigned tasks plus the foreseeable behaviours. A coffee
        break is modelled behaviour, foreseen: Anton plans around her break.</p>
      <p>Words: "foreseeable behaviours". Never call the coffee break anything else here.</p>
    </>} />
  );
}

export function Stage4Architecture() {
  return (
    <ArchSlide stage={4} notes={<>
      {PLACEHOLDER}
      <p>Click: knowledge about the human (C2) appears, its foreseeable behaviours going to recognition, where H
        grows.</p>
    </>} />
  );
}

export function Stage5Card() {
  return (
    <CardSlide stage={5} by="part 2 and part 4" todo={<>
      The prior beside the fixed formula, changing with the situation: a fact such as break time raising the coffee
      break's weight, a recent break lowering it. Then a recorded sim-run of an existing scenario with a fact in force
      (the robot's panel shows the prior; the web-ui's left panel shows the world's context). Why: the audience sees the
      situation make Anton adapt earlier, while her movement still decides.
    </>} notes={<>
      {PLACEHOLDER}
      <p>Will say: context (C3). Facts of the situation (break time, a warm room, a break just taken) set how strongly
        Anton considers each foreseeable behaviour. The prior favours what the situation makes likely; observations
        still decide: Anton never trusts a belief that her movement alone ranks below another (one sentence, the
        evidence rank).</p>
      <p>Measured (T-F part 1, COMPARISON.md, step 3b): with a fact in force, a fact in accord with her task speeds its
        admission, one not in accord delays it, with little change in completion. Numbers on a slide come from an actual
        run.</p>
    </>} />
  );
}

export function Stage5Architecture() {
  return (
    <ArchSlide stage={5} notes={<>
      {PLACEHOLDER}
      <p>Click: context (C3) appears, its prior going into the belief update.</p>
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

export function Stage6Card() {
  return (
    <CardSlide stage={6} by="part 2 and part 4" todo={<>
      A recorded sim-run of an existing kitting scenario in which she switches mid-way and later resumes: the trusted
      belief stops fitting, Anton stops trusting it and replans against the projection from her motion, and recognition
      picks her up again when she resumes. Why: fit is what makes Anton keep up; the audience sees it change the
      outcome.
    </>} notes={<>
      {PLACEHOLDER}
      <p>Will say: fit (B4.2), for one hypothesis: does the trusted belief still explain what she does? When she
        switches mid-way, it stops fitting; Anton stops trusting it (withdrawing a trusted belief, one sentence) and
        replans, against the projection from her motion until a belief is trusted again. Resumption: when she returns to the
        suspended task, recognition picks it up again.</p>
      <p>In the code fit is read by the confidence check from talk stage 3 on; the talk introduces it here, where it
        changes the outcome.</p>
    </>} />
  );
}

export function Stage6Architecture() {
  return (
    <ArchSlide stage={6} notes={<>
      {PLACEHOLDER}
      <p>Click: fit (B4.2) appears, going into the confidence check.</p>
    </>} />
  );
}

export function Stage7Card() {
  return (
    <CardSlide stage={7} by="part 2 and part 4" todo={<>
      A recorded sim-run of an existing kitting scenario with unmodelled behaviour (for example a walk to a corner):
      no hypothesis fits, the projection from her motion takes over as the fallback, and recognition resumes when she
      returns to modelled behaviour. Why: the hardest case, handled by blocks the audience already knows.
    </>} notes={<>
      {PLACEHOLDER}
      <p>Will say: she does something nobody modelled: the only deviation in the glossary's sense (a node of her plan
        the robot's model lacks). Anton knows where its model ends: no hypothesis fits (fit, for all); Anton knows that
        it does not know. It falls back on the projection from motion, the reactive robot's only option at talk stage 2,
        now a deliberate fallback (the call back to talk stage 2). Recognition resumes when she returns to modelled
        behaviour.</p>
      <p>Words: "unmodelled behaviour".</p>
    </>} />
  );
}

export function Stage7Architecture() {
  return (
    <ArchSlide stage={7} caption="Nothing new: fit, now for every hypothesis, and the projection from motion, now as a fallback."
               notes={<>
      {PLACEHOLDER}
      <p>Click: nothing is added. That is the point: the hardest case is handled by blocks the audience already knows,
        fit (now for every hypothesis) and the projection from motion (now as the fallback).</p>
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

function SideSlide({ stage, todo, by, notes }: { stage: TalkStage; todo: ReactNode; by: string; notes: ReactNode }) {
  return (
    <Slide stage={stage} className="side-slide" notes={notes}>
      <StageTitle stage={stage} />
      <div className="side">
        <Todo by={by}>{todo}</Todo>
        <div className="side-arch"><ArchitectureView stage={stage} step={false} title="" /></div>
      </div>
    </Slide>
  );
}

export function Stage9() {
  return (
    <SideSlide stage={9} by="part 3" todo={<>
      The lift truck's turn: the same mind in dock loading, its room drawn by the web-ui's own code and, from part 4, a
      recorded dock_loading sim-run. Why: the second domain shows that the mind does not depend on kitting.
    </>} notes={<>
      {PLACEHOLDER}
      <p>Will say: the lift truck, waiting since the opening, gets its turn: the same mind in dock loading (defined with
        Scania). Nothing of the mind is written for one domain; the domain's knowledge is given, as Anton's was.</p>
      <p><strong>OPEN</strong>: the wording ("Anton changes jobs", or similar), the lift truck's and the dock worker's
        names.</p>
      <p>The diagram is shown here as the complete state; ccode suggests dropping it from talk stages 10 to 12.</p>
    </>} />
  );
}

export function Stage10() {
  return (
    <SideSlide stage={10} by="part 5" todo={<>
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
    <SideSlide stage={11} by="part 5" todo={<>
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
    <SideSlide stage={12} by="part 5" todo={<>
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
