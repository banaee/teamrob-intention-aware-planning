# Plan: T-viz stage 1b, the right panel (the robot: its body and its mind)

Written by ccode, 6 October 2026, and built in the same session without a pause (the task of stage 1b). Every item is
decided by ccode unless marked preferred. Hadi's preferences it builds on: design_records.md, "T-viz, the web-ui", 1b,
THE RIGHT PANEL'S CONTENT AND STAGES 1d AND 1e (five blocks in the order body, belief, admission, projection,
decision). Not in 1b: anything drawn in the scene (1d, 1e), the plots (1c).

## 1. What each block shows (per robot, at the tick)

1. **Body.** The robot's current task (the task its last decision chose, while it runs); the action at its plan's cursor
   with its progress (the executor's microactions done of the action's expansion, in ticks, as panel 4a's progress);
   what the body did this tick (its microaction: step, grasp, release, stand; none on a tick the executor spends
   acknowledging a completion); what it carries (the world's `carried`); a hold in progress: the ticks stood of the
   hold its last decision carried. When its pool is empty: "all its tasks are complete; it still observes".
2. **Belief.** The belief over the live hypotheses (`BeliefState.belief`, the value the gate compares with θ, AM42), one
   row per live hypothesis, highest first, θ marked on each bar; the leader marked. Beside each: its hypothesis
   adequacy, its observation warrant, its evidence rank (outranked or not), its tail probability S when it is a member
   of the adequacy test, and its prior when context knowledge is on. Above them: the lifecycle, the adequacy finding,
   an episode boundary on this tick. Below: with context knowledge on, each foreseeable task's level (suppressed,
   ordinary, raised) and the recency facts of the robot's memory of observed completions; the count of hypotheses of
   the space that are not live.
3. **Admission.** The gate's answer at this tick for the leader, asked at its one home (`MetaPlanner._clears_gate`, as
   the test-beds ask it): "passes the gate", or the refusal as a short phrase with the log's code small beside it. The
   gate is asked at a decision; a line says so, and names the hypothesis the last decision rests on (the decision
   record) if any.
4. **Projection.** What the last decision expected the human to do: the admitted task with its plan's actions and the
   tick its projection runs to; the fallback projection (the human standing where seen, or walking straight on) with
   its span and the tick it runs to (re-decided after it, `projection_expired`); or none (no human observed, or no
   previous observation). Past its end the block says it has run out.
5. **Decision.** The last decision: its tick, its trigger in plain words and its cause, the admission's answer then, the
   chosen task and whether it starts, continues or switches the task (task equality, `same_task`, as the robot reads
   it), the hold it carries, the rest of the pool (the queue, unordered). Under it the last five decisions, newest
   first.

Run conditions (glossary §9): intention-unaware, the belief block says the recognizer does not run, admission refuses
every hypothesis (`none(intention_off)`), the projection is the fallback; human-unaware, belief, admission and
projection say the robot does not take the human into account (`none(no_human)`), the decision block applies. Before the
first step: "no observation yet".

## 2. The messages (`webui/messages.py`)

- Run description: `robots`, per robot `RobotDescription`: its id, its condition (intention-aware, intention-unaware,
  human-unaware), the human it observes, θ, the test level α, min_separation, whether context knowledge is on, the
  hypothesis space (each hypothesis by its key, as the logs write it, its task and bindings), its own assigned tasks,
  and the observed human's assigned tasks it knows (assignment knowledge; none when off).
- Tick update: `robots`, per robot `RobotTick`: `body` (task, action with progress, microaction, hold, finished);
  `belief` (None when the recognizer has produced none); `gate` (the gate's answer at the tick); `decision` (the last
  decision, kept on every tick after it; None before the first): tick, trigger, cause, gate, projection (admitted,
  fallback or none, a union by kind), the change of task (starts, continues, switches, finishes), the chosen task, the
  hold, the queue.
- Both new fields have an empty default; nothing 0.4 or 1a defined changes. The robot's position and what it carries
  stay in `world`. Every value is typed: enums for the trigger, the cause, the gate, the adequacy, the warrant, the
  rank, the level, the lifecycle and the finding.

## 3. Mesa's piece and the model

- `RobotAgent` keeps its last decision (`last_decision`: the tick, the trigger decision, the human projection and the
  meta-planner's result, the values `step()` already holds), for readers; nothing in the loop reads it. No change to
  the recognizer, the gate, the projection, the meta-planner or the executor.
- The piece reads after each step: the belief (`RobotAgent.belief`), the gate (`_clears_gate`; `none(no_human)` when
  the robot observes no human, asked first as admission asks it), the last decision, the executor's cursor, progress
  and hold, the memory's recency facts. The trigger's reason is a string in `shared/types.py`; the piece translates it
  by a closed table and stops on an unknown one.

## 4. The tests

- `tests/test_tviz_robot.py`: per reference sim-run (both domains; an admission, a refusal, a fallback projection, a
  hold, a retraction; an intention-unaware and a human-unaware run; one with context knowledge on), driven through the
  piece, the values the panel receives equal the run log's at every tick: the leader, its confidence, the lifecycle,
  the finding, the leader's adequacy, the tails and warrants (`[IR]`), the ranks (`[IR-rank]`), the prior, the levels
  and the recency facts (`[IR-context]`); the gate, derived from the logged values in the gate's order; per decision the
  trigger and cause (`[meta-trig]`), the admission and the projection's kind (`[meta-proj]`), the chosen task and the
  queue (`[meta]`), the hold (`[hold]` start); a fallback's end where `projection_expired` fires; the hold in progress
  against the `[hold]` start and end lines; the body's task, action and microaction against the step lines.
- The headless log pair unchanged by the record and by producing messages (byte-identical, the four maintained sets
  and dock_loading's three runs); the suite; the page's vitest for its reading of the messages (phrases, ordering, the
  recent decisions); the build and type check; one look in a browser; the solara-ui's light check (`mesa_sim/` changes).

## 5. The page

Panel 4b takes the rail's place: 340 px, beside the env-pane, which keeps working at 1440 px (panel 4a 360 px). Its
title is the robot's id in the robot's colour; the five blocks in order, each under its heading, in the glossary's
words. The page computes nothing of the simulation: it orders rows, chooses phrases and reads the tick updates.
