# Handoff: Phase 6, interactive deviations and a context stream

Recorded 23 September 2026 (cchat, Hadi). An idea for a later phase, after the planned pipeline
T-A to T-G. Nothing here is decided; it is recorded so that the phase opens with its own chat
from this document. The committed documents (CLAUDE.md, docs/glossary.md, docs/roadmap.md,
docs/design_decisions.md, docs/TODOS_AND_DEFERRED.md) are authoritative over this handoff.

## 0. The idea in plain words

Today every human behaviour in a run is pre-loaded: a script written before the run (T-C makes
that script a list of primitive actions with controlled deviations applied at load). Phase 6
adds a second source of deviations: events arriving during the run. A person watching the
simulation in the viewer clicks a button ("coffee break now", "stay here", "change mind: item_5",
"walk to the corner") and the human executor injects that deviation at the next action boundary.
The robot's mind is unchanged: it sees a trajectory, as always.

A second, related idea: a stream of context knowledge (room temperature, coffee-break time
slots, shift changes) fed into the world state during the run, so that the recognizer can
condition its belief on situation, not only on walked path.

## 1. Why

- It shows the property the framework claims and that no pre-loaded demo can show convincingly:
  the robot reacting to a departure it could not have known was coming.
- It makes `unknown`, retraction, re-recognition, wait against reconsider, and the blocked case
  demonstrable live, on the demo day and as a capability claim in the paper.
- The context stream opens a second scientific claim: recognition conditioned on situation.

## 2. What is fixed already (from T-C's design, C1)

- The executed form of the human's behaviour is a flat list of primitive actions (`move_to`,
  `pick_up`, `place`, `stay`), produced by `expand(task)` and edited by a small deviation
  vocabulary (interrupt, deviate, abandon, stay) applied at action boundaries.
- A run-time event is the same operation as a load-time edit; only its source and its tick
  differ. So Phase 6 does not redesign the script; it adds an input path to the human executor.
- The robot's mind receives nothing from the script or from events. Unchanged.

## 3. Decisions to take when the phase opens (the first is the design rule)

1. Replay rule. The viewer offers a fixed set of buttons, the C1 deviation vocabulary, nothing
   free-form. Every event is logged with its tick and its arguments. A finished live run exports
   its event log as a pre-loaded script that reproduces the run exactly from a fresh start. Live
   runs are for demonstration; every number in an evaluation table comes from pre-loaded scripts.
2. The event path in the human executor: a queue drained at the start of each step; an event
   takes effect at the next action boundary (mid-action interruption deferred, as in C1).
   Mesa's step loop is synchronous; an in-process viewer needs no asynchronous machinery. A
   separate UI process would need a socket and the same queue.
3. The viewer: which buttons, what it shows (belief, admitted projection, decision, hold,
   refusal, the event marks). Builds on T-E's viewer.
4. The context stream (its own task): what a context item is, how the world state carries it
   in real time, how the robot's mind reads it, and which recognizer channel uses it (a prior
   term or a likelihood term conditioned on context; today's evidence is walked path only).
   Scientific item, not a simulator one.
5. Communication as an action (its own task): when the robot, facing a live `unknown` or a
   block, raises communication instead of adapting its plan; how that enters B3's candidates.
6. Phase and task naming: Phase 6 if free, tasks P6-T-A, P6-T-B, ... (T-H is reserved for the
   recognizer's duration term, TODO-85 half a).

## 4. Readiness of the components, as of 23 September 2026

- Human executor: ready after C2 (the load-time injection path is the event path).
- Robot's mind (recognizer, meta-planner, realization): ready as is; nothing to change for
  events. Not ready for context: no channel, no representation of non-spatial state.
- World state: no representation of non-spatial state today.
- Viewer: T-E, not built.
- Replay: not built; small once the event log exists.

## 5. Cost, rough

Moderate for the live-deviation demo: the queue, a few buttons on T-E's viewer, the export to a
script. Larger for the context stream: a recognizer extension with its own reasoning and a
world-state extension, plus fixtures that make context matter.

## 6. What to read first when the phase opens

docs/roadmap.md (the pipeline and where Phase 6 sits), docs/design_decisions.md ("The human's
scenario is an action script", "Robustness is tested in kitting", the T-C entries), the C2 record
(the human executor's action-level path), T-E's viewer record, TODO-85 (the stationary human),
TODO-15 (human cooperation), TODO-80 (the blocked event and reconsider).
