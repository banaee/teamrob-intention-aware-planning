/**
 * Talk stage 0, the opening (handoff_T-pres.md, section 5): Anton and the lift truck as actors that use the same mind,
 * the lift truck waiting for its turn; Donny; the problem; Hadi and the team; the robot's mind and its three questions.
 * A first version for Hadi's revision. "Anton" and "Donny" are display text only.
 */

import { useRef } from "react";

import dock from "../../data/dock_loading_env_layout_03.json";
import kitting from "../../data/kitting_env_layout_01.json";
import { useShown } from "../Deck";
import { AgentsInRoom, type Recorded } from "../scene/AgentsInRoom";
import { QUESTION_TEXT, QUESTIONS } from "../talk";
import { ArchitectureView, Slide, Todo } from "./kit";

// The JSON's enumerations are read as strings; the recording wrote the web-ui's messages (LayoutView, Appearance).
export const KITTING = kitting as unknown as Recorded;
const DOCK = dock as unknown as Recorded;

// Free places on the floor of kitting's env_layout_01, with nothing between them and the tilted view's camera.
export const ANTON = { who: "robot" as const, x: 150, y: 100 };
export const DONNY = { who: "human" as const, x: -160, y: -40 };
// The lift truck on dock_loading's dock platform (env_layout_03: outside the gate, beside the truck), facing the hall.
const LIFT_TRUCK = { who: "robot" as const, x: 260, y: -370, facing: { x: 0, y: 1 } };

export function TitleSlide() {
  return (
    <Slide stage={0} footer={false} className="title-slide" notes={<>
      <p><strong>OPEN</strong>: the talk's title. The one shown is a placeholder by ccode.</p>
      <p>About 30 minutes plus 5 of questions. Time is budgeted per section only (for example 5 + 7 + 7 + 8 + 3).</p>
    </>}>
      <p className="title-kicker">TeamRob final demo day</p>
      <h1 className="title-main">Working beside a human</h1>
      <p className="title-sub">How a robot recognises what a person is doing, and plans around it</p>
      <p className="title-who">Hadi Banaee · TeamRob SP4, intention recognition, with SP3, planning</p>
    </Slide>
  );
}

/** The trial slide, kept: the robot alone, then the robot in kitting's room. */
export function AntonSlide() {
  const second = useRef<HTMLHeadingElement>(null);
  const inRoom = useShown(second);
  return (
    <Slide stage={0} className="scene-slide" notes={<>
      <p>Anton, the kitting robot: it brings items from the shelves to the kitting table.</p>
      <p>The room is kitting's env_layout_01, drawn by the web-ui's own code: what the audience sees this afternoon.</p>
    </>}>
      <h1 className="scene-line">This is Anton, a robot.</h1>
      <h1 className="scene-line fragment" ref={second}>Anton is in a factory setup.</h1>
      <AgentsInRoom recorded={KITTING} figures={[ANTON]} inRoom={inRoom} />
    </Slide>
  );
}

/** Anton and the lift truck: two robots that use the same mind; the lift truck waits for its turn. */
export function ActorsSlide() {
  const second = useRef<HTMLParagraphElement>(null);
  return (
    <Slide stage={0} className="actors-slide" notes={<>
      <p>Anton has a colleague: the lift truck at the dock (dock loading, defined with Scania). It uses the same mind
        as Anton. Today it waits for its turn; it comes back before the results (talk stage 9).</p>
      <p><strong>OPEN</strong>: the lift truck's name and the dock worker's, and the wording of its return.</p>
      <p><strong>OPTIONAL</strong> (handoff 9): the lift truck stays small and idle in a corner of the stage slides,
        still waiting.</p>
    </>}>
      <h1 className="scene-line">Two robots, one mind.</h1>
      <div className="actors">
        <figure className="actor">
          <div className="actor-scene"><AgentsInRoom recorded={KITTING} figures={[ANTON]} inRoom /></div>
          <figcaption><span className="dot dot-robot" />Anton, kitting</figcaption>
        </figure>
        <figure className="actor">
          <div className="actor-scene"><AgentsInRoom recorded={DOCK} figures={[LIFT_TRUCK]} inRoom /></div>
          <figcaption><span className="dot dot-robot" />The lift truck, dock loading</figcaption>
        </figure>
      </div>
      <p className="scene-note fragment" ref={second}>The lift truck waits for its turn.</p>
    </Slide>
  );
}

/** Donny: the human who shares the space with Anton. */
export function DonnySlide() {
  const second = useRef<HTMLHeadingElement>(null);
  const inRoom = useShown(second);
  return (
    <Slide stage={0} className="scene-slide" notes={<>
      <p>Donny works in the same room. Blue is always Anton, orange always Donny, as in the web-ui this afternoon.</p>
      <p>Anton cannot see what Donny intends; it sees only what she does.</p>
    </>}>
      <h1 className="scene-line">This is Donny.</h1>
      <h1 className="scene-line fragment" ref={second}>Donny shares the space with Anton.</h1>
      <AgentsInRoom recorded={KITTING} figures={[DONNY, ANTON]} inRoom={inRoom} />
    </Slide>
  );
}

export function ProblemSlide() {
  return (
    <Slide stage={0} className="problem-slide" notes={<>
      <p>The problem: a human and a robot share one workspace. They should work together, get the work done, and stay
        safe.</p>
      <p><strong>OPEN</strong> (handoff 11): the opening's problem sentence; it may need the tension "stopping is safe,
        but it is not teamwork".</p>
      <p><strong>PARKED</strong> (E2): one measured headline sentence from T-F part 1 here.</p>
    </>}>
      <h1 className="problem-head">Human-robot teaming</h1>
      <div className="problem-words">
        <span className="fragment">collaboration</span>
        <span className="fragment">efficiency</span>
        <span className="fragment">safety</span>
      </div>
    </Slide>
  );
}

export function TeamSlide() {
  return (
    <Slide stage={0} notes={<>
      <p>Hadi's work is SP4, intention recognition, done as a synergy with SP3, the planning side of the framework.</p>
      <p>Most of what follows was done from July to October 2026.</p>
    </>}>
      <h1 className="slide-head">The team</h1>
      <p className="slide-lead">TeamRob SP4, intention recognition, together with SP3, planning</p>
      <Todo by="Hadi" className="todo-large">
        Photos and names of Hadi and the team, as Hadi supplies them. Why: the audience meets the people behind the
        work before the work.
      </Todo>
    </Slide>
  );
}

/** The robot's mind and its three questions: the columns of every talk stage that follows. */
export function QuestionsSlide() {
  return (
    <Slide stage={0} notes={<>
      <p>Anton's mind answers three questions. They are the columns of every stage that follows; the stages grow in
        complexity, one row at a time.</p>
      <p>What I know: knowledge representation. What I believe: intention recognition. What I decide: adaptive
        planning.</p>
    </>}>
      <h1 className="slide-head">Anton's mind answers three questions</h1>
      <div className="questions">
        {QUESTIONS.map((q) => (
          <div key={q} className={`question fragment column-${q}`}>
            <h2>{QUESTION_TEXT[q].ask}</h2>
            <p>{QUESTION_TEXT[q].field}</p>
          </div>
        ))}
      </div>
    </Slide>
  );
}

/** The architecture's empty frames, the three questions laid over them; it grows from talk stage 1 on. */
export function ArchitectureFrameSlide() {
  return (
    <Slide stage={0} className="arch-slide" notes={<>
      <p>This is the picture of Anton's mind we will fill, one stage at a time: what it is given (knowledge, left),
        its mind (what it believes, what it decides), its body, and the world, which it reaches only through its
        body.</p>
      <p>Click: the three questions over the regions they will fill.</p>
      <p>Suggestion by ccode: the empty frames here, so that the diagram is introduced once and then only grows.</p>
    </>}>
      <ArchitectureView stage={0} questionTags title="The picture we will fill" />
    </Slide>
  );
}
