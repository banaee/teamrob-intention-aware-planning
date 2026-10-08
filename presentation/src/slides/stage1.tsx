/**
 * Talk stage 1, the robot alone (handoff_T-pres.md, section 5; the name of the overall revision): it knows its own tasks,
 * broken down into actions; it plans, then executes. The decomposition is kitting's own: the work task deliver_item, its three methods (chosen
 * by the situation: domains/kitting/tasks.py) and the actions of the usual one. A first version for Hadi's revision.
 */

import { ArchitectureView, Slide, TransitionSlide } from "./kit";
import { ReplayAlone } from "./replays";

export function Stage1Transition() {
  return (
    <TransitionSlide stage={1} notes={<>
      <p>Six steps, each one making the situation harder; the list on the left comes back at the start of each.</p>
      <p>First, the robot alone, no human in the room. It knows its own tasks; it plans, then executes. Nothing to believe
        yet: nobody else is there. Light stage: keep it short.</p>
    </>} />
  );
}

const WAYS = [
  { text: "the usual way", usual: true },
  { text: "already holding the item", usual: false },
  { text: "holding another item: return it first", usual: false },
];
const ACTIONS = ["go to the item", "pick it up", "go to its table", "place it"];

export function DecompositionSlide() {
  return (
    <Slide stage={1} notes={<>
      <p>The robot's task knowledge, as kitting really has it. Its tasks: deliver item 1, 2, 3 to the kitting table.</p>
      <p>A task has ways of being done (methods), and the situation picks one: the usual way; or, if the robot already holds
        the item, go straight to the table; or, if it holds another item, return that one first.</p>
      <p>Each way is a list of actions: go to the item, pick it up, go to its table, place it. Below the actions are the
        body's micro-actions (a step, a grasp, a release), which the talk does not show.</p>
      <p>Keep this knowledge in mind: at talk stage 3 the same knowledge reads the human.</p>
    </>}>
      <h1 className="slide-head">The robot knows its own tasks</h1>
      <div className="tree">
        <div className="tree-row">
          <div className="tree-label">Its tasks</div>
          <div className="tree-items">
            <span className="chip chip-on">deliver item 1</span>
            <span className="chip">deliver item 2</span>
            <span className="chip">deliver item 3</span>
          </div>
        </div>
        <div className="tree-row fragment">
          <div className="tree-label">Ways to do one<small>chosen by the situation</small></div>
          <div className="tree-items">
            {WAYS.map((w) => <span key={w.text} className={`chip${w.usual ? " chip-on" : " chip-faint"}`}>{w.text}</span>)}
          </div>
        </div>
        <div className="tree-row fragment">
          <div className="tree-label">Actions</div>
          <div className="tree-items tree-actions">
            {ACTIONS.map((a, i) => (
              <span key={a} className="action-step">
                {i > 0 && <span className="action-arrow">→</span>}<span className="chip chip-action">{a}</span>
              </span>
            ))}
          </div>
        </div>
      </div>
    </Slide>
  );
}

export function PlanExecuteSlide() {
  return (
    <Slide stage={1} className="replay-slide" notes={<>
      <p>The robot chooses a task, its planner breaks it down into actions, and its body executes them one at a time. When the
        task is done, it chooses the next. One click per stop of the replay.</p>
      <p>Say it once, here: the counter in the corner counts ticks; one tick is one time step of the simulation. Every
        duration in the talk is in ticks.</p>
      <p>Beside the scene, the robot's mind: for now only its task.</p>
      <p><strong>HADI'S SCENARIO</strong> (tpres-v4, 8 October 2026): kitting scenario_s301_01 on env_layout_14, no human
        in it, run file configs/kitting/tpres/stage1_s301_01.yaml (human-unaware, as the replay it replaced), ticks 0 to
        150, played fast (about 14 ticks a second). Deliver item 1 chosen at 0, picked up at 32, placed at 64; deliver
        item 2 chosen at 67, picked up at 97, placed at 145. One click per stop.</p>
    </>}>
      <h1 className="slide-head">It plans, then executes</h1>
      <ReplayAlone />
    </Slide>
  );
}

export function Stage1Architecture() {
  return (
    <Slide stage={1} className="arch-slide" notes={<>
      <p>Click: what the robot needs to work alone. Its task knowledge (the robot's tasks); in the mind only the planner;
        the body observes the world into a world state and executes the planner's next action.</p>
      <p>The world reaches the robot only through its body: sense, and act.</p>
    </>}>
      <ArchitectureView stage={1} title="The architecture so far" />
    </Slide>
  );
}
