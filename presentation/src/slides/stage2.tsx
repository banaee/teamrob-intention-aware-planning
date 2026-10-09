/**
 * Talk stage 2, a human in the shared space (handoff_T-pres.md, sections 4, 5, 9; the name of the overall revision):
 * the robot knows nothing about her intentions, it believes nothing; it projects her motion and holds to keep the
 * minimum separation: the reactive robot. The planner stays; what changes is the projection it receives. Then the
 * turning point: what if the robot knows something about her behaviour? A first version for Hadi's revision.
 *
 * The drawing of the projection from motion is an abstraction in the web-ui's visual language (the robot's
 * projection of the human a wide hatched blue stripe, the robot's plan a dashed blue line, the human orange), so that
 * the audience can read the env-pane at the station. Its rule is the fallback projection's (glossary, **fallback
 * projection**, T-D P4): the last displacement continued for as many ticks as the current straight run has lasted.
 */

import { ArchitectureView, Slide, StepMarker, TransitionSlide, useStep } from "./kit";
import { ReplayReactive } from "./replays";

export function Stage2Transition() {
  return (
    <TransitionSlide stage={2} notes={<>
      <p>A human enters the shared space. The robot knows nothing about her intentions and believes nothing about them:
        it reacts to her motion.</p>
      <p><strong>OPTIONAL</strong> (2024 callback): Hadi's October 2024 deck and the HHAI/CHAI 2024 poster contrasted an
        "intrinsic reaction" (the robot halts to avoid a collision) with an "enhanced reaction" (it recognises the
        intention and adapts its plan). Talk stage 2 is the intrinsic reaction; talk stages 3 to 6 the enhanced one.</p>
    </>} />
  );
}

export function AudienceQuestionSlide() {
  return (
    <Slide stage={2} className="question-slide" notes={<>
      <p>The one question to the audience. Let them answer; collect two or three answers, then go on: first, the
        simplest robot, which knows nothing about her.</p>
      <p>Wording: the handoff's candidate.</p>
    </>}>
      <p className="ask">What would the robot need to know to work beside her?</p>
    </Slide>
  );
}

// The drawing's ground: a room seen from above, in its own unit.
const W = 1100;
const H = 600;
const TRAIL = [[150, 470], [215, 437], [280, 404], [345, 371]] as const;
const HUMAN = [410, 338] as const;
const AHEAD = [670, 206] as const;        // as many steps ahead as were observed in a straight run
const ROBOT = [860, 470] as const;
const ROBOT_GOAL = [470, 110] as const;

export function ProjectionSlide() {
  const [seen, seenShown] = useStep();
  const [projected, projectedShown] = useStep();
  const [held, heldShown] = useStep();
  return (
    <Slide stage={2} notes={<>
      <p>Click 1: the robot sees where she moves, step by step.</p>
      <p>Click 2: the projection from her motion: the robot continues her last motion, for as long as it has seen her move
        that way (a straight run of k ticks is projected k ticks ahead; a stand, as long as she has stood). It claims
        nothing about what she intends.</p>
      <p>Click 3: where the robot's path would come closer than the minimum separation to her projected path, it holds, then
        goes on.</p>
      <p>This is the reactive robot. The planner stays; what changes is the projection it receives. The same drawing
        is on the floor of the web-ui this afternoon: the robot's plan a dashed blue line, its projection of her a wide
        hatched blue stripe.</p>
    </>}>
      <h1 className="slide-head">Projection from her motion</h1>
      <div className="projection">
        <svg className="projection-drawing" viewBox={`0 0 ${W} ${H}`} role="img"
             aria-label="The human's observed steps, the projection from her motion, and the robot holding">
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
            <line x1={HUMAN[0]} y1={HUMAN[1]} x2={AHEAD[0]} y2={AHEAD[1]} className="stripe" />
            <text x={AHEAD[0] + 30} y={AHEAD[1] - 20} className="drawing-label drawing-label-robot">projection from her motion</text>
          </g>
          <g className={`appear${heldShown ? " on" : ""}`}>
            <line x1={ROBOT[0]} y1={ROBOT[1]} x2={ROBOT_GOAL[0]} y2={ROBOT_GOAL[1]} className="plan" />
            <circle cx={ROBOT_GOAL[0]} cy={ROBOT_GOAL[1]} r="7" className="plan-end" />
            <text x={ROBOT[0] - 120} y={ROBOT[1] + 92} className="drawing-label drawing-label-robot">holds, then goes on</text>
            <circle cx={ROBOT[0]} cy={ROBOT[1]} r="44" className="hold-ring" />
          </g>
          <circle cx={HUMAN[0]} cy={HUMAN[1]} r="30" className="agent-ring agent-ring-human" />
          <circle cx={HUMAN[0]} cy={HUMAN[1]} r="13" className="agent agent-human" />
          <text x={HUMAN[0] - 62} y={HUMAN[1] + 60} className="drawing-label drawing-label-human">the human</text>
          <circle cx={ROBOT[0]} cy={ROBOT[1]} r="30" className="agent-ring agent-ring-robot" />
          <circle cx={ROBOT[0]} cy={ROBOT[1]} r="13" className="agent agent-robot" />
          <text x={ROBOT[0] + 54} y={ROBOT[1] + 9} className="drawing-label drawing-label-robot">robot</text>
        </svg>
        <div className="projection-text">
          <p className={`appear${seenShown ? " on" : ""}`}>Robot sees where she moves.</p>
          <p className={`appear${projectedShown ? " on" : ""}`}>It continues her motion, for as long as it has seen it.</p>
          <p className={`appear${heldShown ? " on" : ""}`}>Where its path would come closer than the minimum separation, it
            holds.</p>
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
    <Slide stage={2} className="replay-slide" notes={<>
      <p>The reactive robot in a real run: the robot holds to keep the minimum separation from her projected path.
        One click per stop. Beside the scene, the robot's mind: no hypotheses, the projection from her motion, its
        hold.</p>
      <p><strong>THE COPY</strong> (tpres-v5, 8 October 2026): kitting scenario_s305_01 on env_layout_12, a copy of Hadi's
        scenario_s302_02 with the robot starting at (300, 60) instead of (390, 160); run file
        configs/kitting/tpres/stage2_s305_01.yaml (intention-unaware), ticks 0 to 44. In scenario_s302_02 no hold is
        decided anywhere in the run (the two pass 60.31 cm apart at tick 42). In the copy her carry from shelf_1 and the
        robot's from shelf_5 meet at the room's crossing: at 34 the robot holds 7 ticks (34 to 40) against the
        projection from her motion; it goes on behind her, closest 58.26 cm at 42. The robot's start was chosen from a
        grid of starts (the longest hold of the grid); what it then does is the framework's own result.</p>
      <p>In the results this is the intention-unaware run: the same planner, fed only with the projection from her
        motion.</p>
    </>}>
      <h1 className="slide-head">The reactive robot</h1>
      <ReplayReactive />
      <p className="slide-foot-line">The planner stays; what changes is the projection it receives.</p>
    </Slide>
  );
}

export function Stage2Architecture() {
  return (
    <Slide stage={2} className="arch-slide" notes={<>
      <p>Click: with the human in the room, the world state holds her motion. The projection turns it into her path; the
        realizer takes the planner's plan and her path, and decides the next action and the hold. The direct arrow from
        the planner to execute gives way to the realizer's.</p>
      <p>Recognition is still absent: the robot believes nothing about her.</p>
    </>}>
      <ArchitectureView stage={2} title="The architecture so far" />
    </Slide>
  );
}

export function TurningPointSlide() {
  return (
    <Slide stage={2} className="turning-slide" notes={<>
      <p>The challenge: the robot keeps the minimum separation, but it only reacts to her present motion. The solution
        the rest of the talk builds: let the robot know something about her behaviour.</p>
      <p>A challenge followed by a solution, never a list of failures.</p>
    </>}>
      <p className="turning-challenge">Robot keeps the minimum separation from her. It reacts only to her present
        motion.</p>
      <p className="turning-solution fragment">What if the robot knows something about her behaviour?</p>
    </Slide>
  );
}
