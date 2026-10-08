/**
 * Level 1 and talk stage 2, Donny enters (handoff_T-pres.md, sections 4, 5, 9): Anton knows nothing about her
 * intentions, its belief is empty; it projects from her motion and holds near her: the reactive robot. The planner
 * stays; what changes is the projection it receives. Then the turning point: what if Anton knows something about her
 * behaviour? A first version for Hadi's revision.
 *
 * The drawing of the projection from motion is an abstraction in the web-ui's visual language (the robot's
 * projection of the human a wide hatched blue stripe, the robot's plan a dashed blue line, the human orange), so that
 * the audience can read the env-pane at the station. Its rule is the fallback projection's (glossary, **fallback
 * projection**, T-D P4): the last displacement continued for as many ticks as the current straight run has lasted.
 */

import { ArchitectureView, LevelTitle, Slide, StageCard, Todo, useStep, StepMarker } from "./kit";

export function Level1Slide() {
  return (
    <Slide stage={2} className="level-slide" notes={<>
      <p>Level 1: Anton works around her. It sees where she moves, and keeps clear.</p>
      <p><strong>OPTIONAL</strong> (2024 callback): Hadi's October 2024 deck and the HHAI/CHAI 2024 poster contrasted an
        "intrinsic reaction" (the robot halts to avoid a collision) with an "enhanced reaction" (it recognises the
        intention and adapts its plan). Level 1 is the intrinsic reaction; levels 2 and 3 the enhanced one.</p>
    </>}>
      <LevelTitle level={1} />
    </Slide>
  );
}

export function DonnyEntersSlide() {
  return (
    <Slide stage={2} notes={<>
      <p>Donny enters the room while Anton works.</p>
      <p><strong>PARKED</strong> (handoff 11): the comparison with centralised multi-agent planning, candidate place
        here. Agreed wording: a central planner can command robots; nobody can command a human, whose current intention
        is not communicated and whose behaviour is only partly modelled. A different setting, not a weaker approach.</p>
    </>}>
      <h1 className="slide-head">Donny enters</h1>
      <Todo by="part 4" className="todo-large">
        Donny walking into the room while Anton works, replayed from a recorded sim-run of an existing kitting
        scenario: the human in orange, the robot in blue, the floor as the web-ui draws it. A few clicks, or a short
        play that stops when she is in the room. Why: the moment the human enters is the moment the question below is
        asked.
      </Todo>
    </Slide>
  );
}

export function AudienceQuestionSlide() {
  return (
    <Slide stage={2} className="question-slide" notes={<>
      <p>The one question to the audience. Let them answer; collect two or three answers, then go on: first, the
        simplest robot, which knows nothing about her.</p>
      <p>Wording: the handoff's candidate.</p>
    </>}>
      <p className="ask">What would Anton need to know to work beside her?</p>
    </Slide>
  );
}

export function Stage2Card() {
  return (
    <Slide stage={2} notes={<>
      <p>Anton knows nothing about her intentions; its belief is empty. What it can do: see where she moves, project
        that motion ahead, and hold where its own path would come too close.</p>
    </>}>
      <StageCard stage={2} />
    </Slide>
  );
}

// The drawing's ground: a room seen from above, in its own unit.
const W = 1100;
const H = 600;
const TRAIL = [[150, 470], [215, 437], [280, 404], [345, 371]] as const;
const DONNY = [410, 338] as const;
const AHEAD = [670, 206] as const;        // as many steps ahead as were observed in a straight run
const ANTON = [860, 470] as const;
const ANTON_GOAL = [470, 110] as const;

export function ProjectionSlide() {
  const [seen, seenShown] = useStep();
  const [projected, projectedShown] = useStep();
  const [held, heldShown] = useStep();
  return (
    <Slide stage={2} notes={<>
      <p>Click 1: Anton sees where she moves, step by step.</p>
      <p>Click 2: the projection from her motion: Anton continues her last motion, for as long as it has seen her move
        that way (a straight run of k ticks is projected k ticks ahead; a stand, as long as she has stood). It claims
        nothing about what she intends.</p>
      <p>Click 3: where Anton's path would come too close to her projected path, it holds, then goes on.</p>
      <p>This is the reactive robot. The planner stays; what changes is the projection it receives. The same drawing
        is on the floor of the web-ui this afternoon: the robot's plan a dashed blue line, its projection of her a wide
        hatched blue stripe.</p>
    </>}>
      <h1 className="slide-head">Projection from her motion</h1>
      <div className="projection">
        <svg className="projection-drawing" viewBox={`0 0 ${W} ${H}`} role="img"
             aria-label="Donny's observed steps, the projection from her motion, and Anton holding">
          <defs>
            <pattern id="hatch-motion" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
              <rect width="14" height="14" className="hatch-ground" />
              <line x1="0" y1="0" x2="0" y2="14" className="hatch-line" />
            </pattern>
          </defs>
          <rect x="2" y="2" width={W - 4} height={H - 4} rx="18" className="room" />
          <g className={`appear${seenShown ? " on" : ""}`}>
            {TRAIL.map(([x, y]) => <circle key={x} cx={x} cy={y} r="7" className="trail" />)}
          </g>
          <g className={`appear${projectedShown ? " on" : ""}`}>
            <line x1={DONNY[0]} y1={DONNY[1]} x2={AHEAD[0]} y2={AHEAD[1]} className="stripe" />
            <text x={AHEAD[0] + 30} y={AHEAD[1] - 20} className="drawing-label drawing-label-robot">projection from her motion</text>
          </g>
          <g className={`appear${heldShown ? " on" : ""}`}>
            <line x1={ANTON[0]} y1={ANTON[1]} x2={ANTON_GOAL[0]} y2={ANTON_GOAL[1]} className="plan" />
            <circle cx={ANTON_GOAL[0]} cy={ANTON_GOAL[1]} r="7" className="plan-end" />
            <text x={ANTON[0] - 120} y={ANTON[1] + 92} className="drawing-label drawing-label-robot">holds, then goes on</text>
            <circle cx={ANTON[0]} cy={ANTON[1]} r="44" className="hold-ring" />
          </g>
          <circle cx={DONNY[0]} cy={DONNY[1]} r="30" className="agent-ring agent-ring-human" />
          <circle cx={DONNY[0]} cy={DONNY[1]} r="13" className="agent agent-human" />
          <text x={DONNY[0] - 30} y={DONNY[1] + 60} className="drawing-label drawing-label-human">Donny</text>
          <circle cx={ANTON[0]} cy={ANTON[1]} r="30" className="agent-ring agent-ring-robot" />
          <circle cx={ANTON[0]} cy={ANTON[1]} r="13" className="agent agent-robot" />
          <text x={ANTON[0] + 54} y={ANTON[1] + 9} className="drawing-label drawing-label-robot">Anton</text>
        </svg>
        <div className="projection-text">
          <p className={`appear${seenShown ? " on" : ""}`}>Anton sees where she moves.</p>
          <p className={`appear${projectedShown ? " on" : ""}`}>It continues her motion, for as long as it has seen it.</p>
          <p className={`appear${heldShown ? " on" : ""}`}>Where its path would come too close, it holds.</p>
        </div>
      </div>
      <StepMarker r={seen} />
      <StepMarker r={projected} />
      <StepMarker r={held} />
    </Slide>
  );
}

export function ReactiveRunSlide() {
  return (
    <Slide stage={2} notes={<>
      <p>The reactive robot in a real sim-run: Anton keeps clear, and it holds near her.</p>
      <p><strong>OPEN</strong> (handoff 5, 11): a screenshot of Fatemeh's PRIEST trajectory adaptation (ROS side) may
        acknowledge her work here, labelled as such; Hadi fixes its wording.</p>
      <p>In the results this is the intention-unaware run: the same planner, fed only with the projection from her
        motion.</p>
    </>}>
      <h1 className="slide-head">The reactive robot</h1>
      <div className="two-col two-col-wide">
        <Todo by="part 4">
          Anton holding near Donny, replayed from a recorded sim-run of an existing kitting scenario with the robot
          intention-unaware (T-F part 1's condition), in the env-pane's look: the hatched blue stripe of the projection
          from her motion, the dashed blue plan, the hold. Stepped by clicks around the hold. Why: the audience sees
          the reactive robot keep clear, and reads the same drawing at the station.
        </Todo>
        <Todo by="Hadi, open">
          Optional: a screenshot of Fatemeh's PRIEST trajectory adaptation (ROS side), labelled as her work, if Hadi
          keeps the acknowledgement here.
        </Todo>
      </div>
      <p className="slide-foot-line">The planner stays; what changes is the projection it receives.</p>
    </Slide>
  );
}

export function Stage2Architecture() {
  return (
    <Slide stage={2} className="arch-slide" notes={<>
      <p>Click: with Donny in the room, the world state holds her motion. The projection turns it into her path; the
        realizer takes the planner's plan and her path, and decides the next action and the hold. The direct arrow from
        the planner to execute gives way to the realizer's.</p>
      <p>Recognition is still empty: Anton believes nothing about her.</p>
    </>}>
      <ArchitectureView stage={2} title="The architecture so far" />
    </Slide>
  );
}

export function TurningPointSlide() {
  return (
    <Slide stage={2} className="turning-slide" notes={<>
      <p>The challenge: Anton keeps clear, but it only reacts to where she is going now. The solution the rest of the
        talk builds: let Anton know something about her behaviour.</p>
      <p>A challenge followed by a solution, never a list of failures.</p>
    </>}>
      <p className="turning-challenge">Anton keeps clear of her. It reacts to where she is going now.</p>
      <p className="turning-solution fragment">What if Anton knows something about her behaviour?</p>
    </Slide>
  );
}
