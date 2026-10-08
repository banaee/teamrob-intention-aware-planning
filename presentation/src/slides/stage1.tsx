/**
 * Talk stage 1, Anton works alone (handoff_T-pres.md, section 5): it knows its own tasks, decomposed down to actions;
 * it plans, then executes. The decomposition is kitting's own: the work task deliver_item, its three methods (chosen
 * by the situation: domains/kitting/tasks.py) and the actions of the usual one. A first version for Hadi's revision.
 */

import { ArchitectureView, Slide, StageCard, Todo } from "./kit";

export function Stage1Card() {
  return (
    <Slide stage={1} notes={<>
      <p>First, Anton alone, no human in the room. It knows its own tasks; it plans, then executes.</p>
      <p>Nothing to believe yet: nobody else is there. Light stage: keep it short.</p>
    </>}>
      <StageCard stage={1} />
    </Slide>
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
      <p>Anton's task knowledge, as kitting really has it. Its tasks: deliver item 1, 2, 3 to the kitting table.</p>
      <p>A task has ways of being done (methods), and the situation picks one: the usual way; or, if Anton already holds
        the item, go straight to the table; or, if it holds another item, return that one first.</p>
      <p>Each way is a list of actions: go to the item, pick it up, go to its table, place it. Below the actions are the
        body's micro-actions (a step, a grasp, a release), which the talk does not show.</p>
      <p>Keep this knowledge in mind: at talk stage 3 the same knowledge reads Donny.</p>
    </>}>
      <h1 className="slide-head">Anton knows its own tasks</h1>
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
    <Slide stage={1} notes={<>
      <p>Anton chooses a task, its planner decomposes it into actions, and its body executes them one at a time. When the
        task is done, it chooses the next.</p>
      <p>Part 4 fills the box with a fast-forward of Anton delivering items.</p>
    </>}>
      <h1 className="slide-head">It plans, then executes</h1>
      <div className="two-col">
        <ol className="steps-list">
          <li className="fragment">Choose a task</li>
          <li className="fragment">Plan its actions</li>
          <li className="fragment">Execute them, one at a time</li>
        </ol>
        <Todo by="part 4">
          A fast-forward of Anton alone, delivering items, replayed from a recorded sim-run of an existing kitting
          scenario, in the web-ui's env-pane look: the robot in blue, its plan as its dashed blue line on the floor.
          Several ticks per click or a short continuous play. Why: the audience sees "plan, then execute" happen, and
          learns to read the floor drawing they meet at the station.
        </Todo>
      </div>
    </Slide>
  );
}

export function Stage1Architecture() {
  return (
    <Slide stage={1} className="arch-slide" notes={<>
      <p>Click: what Anton needs to work alone. Its task knowledge (C1, Anton's tasks); in the mind only the planner;
        the body observes the world into a world state and executes the planner's next action.</p>
      <p>The world reaches Anton only through its body: sense, and act.</p>
    </>}>
      <ArchitectureView stage={1} title="The architecture so far" />
    </Slide>
  );
}
