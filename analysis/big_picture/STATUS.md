# Where the framework stands

A big-picture reading of the repository on 2026-09-19, at commit `2d5fc2c`. Written to be read
without the entry numbers: labels appear in brackets only so that an entry can be found, and
section 6 maps plain names to labels. Nothing was run for this document; it is distilled from
the design record, the analysis reports and the code. Where they disagree, the code wins, then
the later entry; section 5 lists each case.

Symbols, once: the **confidence bar** is θ (0.75); the **hold** is δ, the ticks the robot
stands still before its plan runs; the **end of the human's projection** is T_h; the
**separation** is `min_separation`, the distance the robot's motion must keep from the human
(2.5 × the robot's motion per tick, 50 cm in Mesa); the **commitment share** is ρ (0.5).

---

## 1. Where we are

**The short version.** The robot's mind is complete for choosing *one next task at a time*:
it recognises what the human is doing, predicts the human's path for that task, prices each of
its own remaining tasks as walking time plus the wait needed to stay clear of the human, picks
the cheapest, and sends the body a task and a wait. That whole path is built, measured on
eight hand-made kitting fixtures, and its work queue is empty. What has *not* been started is
choosing an *order* for the whole remaining pool, going *around* the human instead of waiting,
the evaluation phase, and the ROS body.

| Phase | What it is | State |
|---|---|---|
| 1 Foundations | types, contracts between mind and body, domain-knowledge interfaces | done |
| 2 Skeletons, visualization, dock domain | first recognizer and planner skeletons; the Solara viewer; a second domain | done; the dock domain is deferred and only has to keep importing |
| 3 Kitting domain and Mesa body | tasks, actions, layouts, scenarios, the simulated body | done |
| 4A Recognition, first version | Bayesian belief over typed hypotheses | superseded: an audit showed the likelihood never did what was written; rebuilt below |
| 4B Task decomposition | recursive HTN decomposer with real guards | done |
| 4C Meta-planner and the recognizer rebuild | everything in the short version above | **built; queue empty** |
| 4D Going around the human | detour strategy, a wait at a chosen point, human cooperation for a stuck robot | not started, by decision |
| 5 Evaluation | recognition quality, adaptation latency, team efficiency | not started |
| 6 ROS body | | paused |

**What 4C delivered, in the order it was decided.**

1. The recognizer was rebuilt from an audit upward and handed back with a statement of what
   the meta-planner may and may not assume.
2. A measurement showed that the conflicts in the fixtures are *timing* conflicts (both agents
   reach the table within a tick), so the proportionate response is a short wait, which the
   robot could not express. Decided: **the robot can wait**, and a conflict is priced as the
   time the wait costs. No conflict weight, no exclusion threshold.
3. That pricing ("realization") was built as a service beside the projector, then used by the
   commitment gate and by selection.
4. The rule for what counts as a violation was changed to **robot-responsible separation**:
   only the robot's own motion can violate; a standing robot never does. A clearing wait then
   always exists, so every candidate has a cost and nothing is ever excluded.
5. The body got an optional **separation stop** for what the plan cannot foresee.
6. The **trigger set was settled**: a trigger is a change in what the last decision rested on.
7. The policy components were **ablated**; one defect was found and fixed.
8. The recognizer's evidence was **graded by how much of the expected path was covered**, so a
   task is revealed along the walk instead of on the human's first step; and the **gate
   ruling** kept the confidence bar a fixed share.

**The next step** is the generated (randomised) fixtures [TODO-47]. The reason is not more
coverage for its own sake. Three questions are open and the record says each can only be
answered there, because the standing rule is that hand-made fixtures evaluate components and
never set a parameter or a design decision:

- whether the commitment gate earns its place (on the present fixtures it changed one decision,
  and lost);
- whether the confidence bar needs reopening (only a walk that crosses the bar with a live
  rival at similar odds would reopen it; no present fixture shows one);
- what the separation value and the recognizer's detour tolerance do at other layout scales.

---

## 2. Diagrams

### A. The framework as a whole

```
                         MIND  (shared/, knows no simulator, no units, no domain strings)
  +-----------------------------------------------------------------------------------------+
  |                                                                                         |
  |   recognizer  ----belief---->  meta-planner  ----one task---->  planner                 |
  |   "what is the human           "is a decision due? which       "decompose that task     |
  |    doing now?"                  task next, and how long         into grounded actions,  |
  |        ^                        to wait first?"                 from the live world"    |
  |        |                          |      ^                          |                   |
  |        | asks the planner to      |      | projector + realization  |                   |
  |        | decompose every          |      | (paths in time; the wait |                   |
  |        | hypothesis, every tick   v      |  that keeps separation)  |                   |
  |        +------------------ planner (same decomposer) <--------------+                   |
  +--------^-----------------------------^----------------------------------|---------------+
           | observation                 | world snapshot                   | plan + hold
           | (human's position,          | (rebuilt every tick,             | (+ continue, by
           |  micro-action)              |  never stored)                   |   task identity)
  +--------|-----------------------------|----------------------------------v---------------+
  |   observation builder          world-state builder                  executor            |
  |                                                                     one micro-action    |
  |                         BODY  (mesa_sim/)                           per tick            |
  +-----------------------------------------------------------------------------------------+

  The body also hands the mind, once, at construction, everything that depends on the body:
  motion per tick, stopping distance, the ticks an action and a task take to acknowledge,
  the observation delay, and how to turn a schema duration into ticks.
```

Per robot tick, in `mesa_sim/sim_agents.py`: build the world snapshot, build the observation of
the human, update the belief, snapshot the executor's state once, ask the meta-planner whether
a trigger fired; only if one did: build the human's projection, decide, re-decompose the
chosen task, install the hold; then execute one micro-action. Humans act before robots within
a tick. The human has no recognizer and no meta-planner: it follows its script.

### B. How the recognizer feeds the meta-planner

```
  built once, from the domain's task schemas x the typed objects in the layout
  (never from the human's script):
        hypotheses = every (task, typed binding)  +  "unknown"
        with the assignment-prior switch on: restricted to the human's assigned tasks
        plus the foreseeable ones (a restriction of the support, not a weight)

  every tick, for every hypothesis still live:
        planner decomposes it against the world  -->  the action it expects NOW
                                                     (the phase is derived, never stored)
        walking?   excess path = distance wasted against the straight way to the target
                   likelihood L = 1 at no waste, falling with the waste
                   one stretch toward one target = ONE observation, however many ticks
        its evidence against "unknown" is graded by the share f of the path covered:
                   L / u^f      (u = 0.1;  f = 1 at an arrival, by the completion fact)
        a grasp / release that the expected action predicts: scored by detection reliability
        standing still, or nothing walked: not an observation at all

  two different endings:
        PIN        the task's terminal condition holds in the world, whoever did it
                   --> hypothesis retired for the run; nothing re-initialises
        BOUNDARY   the HUMAN's own task just ended
                   --> belief restarts from the uniform prior; nothing crosses over

  one normalisation over all live hypotheses and "unknown"  -->  BELIEF
        distribution      logged, not read by the meta-planner
        most likely   ----+
        confidence    ----+--->  META-PLANNER reads exactly these, in three places:
        hypothesis lookup -+        1. the confidence bar (one method, the only place θ is)
                                    2. the trigger "recognition changed"
                                    3. admission of the human's projection
```

The recognizer emits a belief and **gates nothing**. What the meta-planner may assume: a task
at or above the bar is the task being executed now; a completed task never returns; right
after the human's own completion the most likely hypothesis carries no information until the
human moves. What it must not assume: that confidence is comparable across different numbers
of live hypotheses, that it is monotone within a task, that `unknown` above the bar means the
human is idle, or that a robot completion is a human boundary. A lone live task clears the bar
at about half of its walk.

### C. The meta-planner

```
  every tick:  IS A DECISION DUE?   (event-driven; never a timer)
  +------------------------------------------------------------------------------------+
  | 1. nothing to do        the robot has no current task (start of run, or task done) |
  | 2. recognition changed  against the DECISION RECORD = the hypothesis the last      |
  |                         decision was projected on (one field):                     |
  |                           - one is recorded and the belief no longer points at it  |
  |                             (replaced / the human's task ended / "unknown" took    |
  |                              over), or                                             |
  |                           - none is recorded and a task hypothesis clears the bar  |
  |                         a recorded hypothesis that dips under the bar but stays    |
  |                         most likely fires nothing                                  |
  | 3. robot committed      the robot just grasped something                           |
  +------------------------------------------------------------------------------------+
        no  --> keep executing                     yes
                                                    |
                                                    v
  ADMISSION of the human's projection  (once per decision, passed on explicitly)
        below the bar           --> none          each refusal clears the decision record
        no human observed       --> none
        most likely = "unknown" --> none
        hypothesis unresolvable --> none
        otherwise --> project the human's CURRENT task as a path in time; record the hypothesis
        "none" is routine (the belief restarts at every human task boundary): every
        candidate is then priced at its plain walking time, never as always-conflicting
                                                    |
                                                    v
  update()
   0   POOL = [current task] + the rest, minus every task already complete IN THE WORLD
       (whoever did it).  Empty --> "all tasks complete", a normal return.
   1   No current task, or the pool just dropped it as complete --> go to SELECTION.
   2   COMMITMENT GATE, mid-task only.  It can keep the current task; it can never choose one.
         none (default)  always go to selection
         b2a             realize the current task alone; continue with its hold if
                         hold <= 0.5 x (the human's remaining projected time), else go on;
                         no projection admitted --> continue, no hold
         b2b             a stub: redundant with selection by construction
   3   SELECTION.  Each task in the pool is a candidate, the current one on equal terms.
         project it alone from the live world
         realize it against the human's projection --> the smallest whole-tick hold at the
             robot's present position that keeps separation until the human's projection ends
         cost = walking time + hold            (run option "plain": walking time only)
         winner = the cheapest; ties by pool order
         the rest stay an UNORDERED pool: order carries no commitment, it is re-decided
         at the next trigger
                                                    |
                                                    v
  RESULT:  the task to run  +  the unordered rest  +  the winner's hold in whole ticks
```

"Continue, paying a 2-tick wait" and "switch, paying 19 ticks of walking" compare on one
number. There is no wait-or-reselect branch inside selection.

### D. Projection, realization, geometry

```
  geometry      segments in --> the shifts that would violate, in closed form (no sampling)
     |
  realization   "what would this path be, given the human?"  --> hold, cost, the share of
     |           the plan lying past the human's projection (logged, not priced)
  projector     task + world --> a path in time (walks end where the body stops; an
     |           acknowledgement tick per action; schema wait durations; the human's path
     |           starts one observation-delay later)
  meta-planner  which path to pick; supplies the separation value; holds no geometry
```

A violation is the robot **moving** within the separation distance of the human without the
distance increasing. Standing still never violates; moving away never violates. One wait, at
the position where the decision is made, then the whole plan shifted; never a wait somewhere
else (that would be a detour) and not part-way along a walk. Beyond the end of the human's
projection the plan is *unassessed*: neither clear nor blocked.

### E. What the executor receives

```
  the PLAN        grounded actions for ONE task, re-decomposed from the live world at every
                  decision; never resumed (the world is the cursor)
  CONTINUE        not a flag: the decided task equals the running one by task identity -->
                  the fresh plan is adopted without restarting the action in flight; costs nothing
  the HOLD        stand N ticks where you are, then run the plan. A hint the body may refine
                  but not drop, and never re-decide. Every new decision replaces the hold in
                  progress (a decision with no projection drops it). Mesa executes it as decided.
  SEPARATION STOP a run option, default off. Before each step the body checks the step against
                  the human's ACTUAL position under the same rule and stands instead if it would
                  violate. Adds to the hold, fires no trigger, tells the mind nothing. It cannot
                  go around: a human standing where the robot must go blocks it until they leave.
```

---

## 3. Component by component

"Due" means parked in the record but needed by the next step or sitting in the live pipeline.
Future extensions are left out (section 6 of the roadmap's "later" list, team-level costs,
objects appearing mid-run, the dock domain, the ROS items, the two analytical tools, renames).

### World snapshot and observation (body)
- **Done.** Symbolic snapshot rebuilt every tick; positions carried as a scoped exception, read
  in the mind only through one target-resolution function; two separate predicate families
  (in a zone, for recognition; at an object, for completion); waits observable as a world fact.
- **Note, not a task.** Three observation fields the contract defines (orientation, action
  progress, observation confidence) are filled with constants in Mesa and read by nothing.
- **Open now.** Nothing.

### Recognizer
- **Done.** Typed hypothesis space; phase derived from the planner every tick; excess-path
  likelihood; detection reliability for grasp and release; a constant `unknown` as the
  reference, its evidence graded by path covered; pin versus episode boundary; one
  normalisation; an accounting invariant checked independently to 7e-15. Four parameters with
  physical meanings, chosen jointly once and closed: not to be reopened by sweeping. Handed
  back with a guarantee statement. Not under active change.
- **Due.** The detour tolerance is in centimetres [TODO-58], so a layout twice the size needs
  half the value; the fractional form was measured and rejected, and a scale-invariant form
  needs a layout-level length the world snapshot does not carry. This is the recognizer's half
  of the scale calibration the generated fixtures require.
- **Due.** Two silent-failure checks are still only proposed [TODO-49]: a log line stating the
  hypothesis space, and catching a type-name clash between layout and schema. A generator is
  exactly where a silent mismatch would bite; two hand-made scenarios already had to be retired
  for it.
- **Open, characterised, waiting for the generated fixtures to say whether they matter:**
  phases with no graded signal (pick up, place, wait) still count as one whole observation, so
  an arrival counts twice; collinear decoys under the grade, in particular a decoy *before* the
  target on the same bearing, which could cross the bar wrongly and which no fixture has; the
  return-first delivery method's guard as a prediction of the *human*.

### Triggers
- **Done and settled.** Three triggers, as in diagram C. The confidence bar is asked on entry
  only; retention is by identity. The repeated crossings and the missing fire on a change of
  hypothesis that the old crossing-trigger produced are consequences of this, not special cases.
- **Due.** The **blocked event** is designed and not built: the separation stop's refusal
  becomes a fact in the executor's state, fires once per blocked episode, and goes straight to
  selection. It waits for a valid fixture that blocks mid-run. None exists, for a good reason:
  a human stay that the projection carries is priced by realization, so the stop only fires
  past the end of the projection and on deviations. Until it is built the mind does not know
  the body has stopped.

### Admission and the human's projection
- **Done.** Diagram C. One projection per decision, passed explicitly, never stored.
- **By design, and the root of section 4:** the projection is the human's *current task only*.
  Its end is the horizon of everything the robot can price.

### Commitment gate
- **Done.** `none` and `b2a` built; `b2b` a documented stub, not to be filled in.
- **Open, and it is the first thing the generated fixtures must answer:** does this block
  survive? Its original reason (catching conflict cheaply) is gone, since selection already
  prices conflict. What remains is commitment: holding the current task against flips on small
  cost differences. On the present fixtures it equals no gate in all sixteen conditions at the
  default share; across the share sweep it took one real commitment decision (at a share of 1.0,
  twice the default), and that one lost 15 ticks to the switch (13 with the prior off, after
  the fix). The record states that nothing about it, and no value of the
  share, is decided from these fixtures. It cannot even be exercised properly yet: no fixture
  has a genuine *crossing* on the robot's current task; every conflict is convergence at the table.

### Selection
- **Done.** Single-task, on realized cost, total (nothing excluded, nothing raised).
- **Open now.** Nothing in the single-task path. The full-queue strategy exists as a switch
  that raises "not implemented" in two places: section 4.
- **Small, real:** ties go by pool order, which is reproducible only under the fixed hash seed.

### Projection and realization
- **Done.** Diagram D. Whole-tick holds (the plan that is checked is the plan that is
  executed); walking time stays fractional; the separation value is relative to motion.
- **Due.** The separation *value* is to be revisited at other scales and body sizes. One value
  currently governs two situations that collaborative practice treats differently: passing in
  the open, and working side by side at a place modelled as one point.
- **Known bias, accepted for now.** Step quantisation is not compensated and the minimal hold
  has no margin. One measured consequence: after the robot's grasp, clearance depends on the
  re-decision the grasp triggers; without it the robot would run a plan that no longer clears.
  If fixed, the fix is on the projector's accounting, not a trigger [TODO-77].
- **Logged, not priced:** the share of each plan lying past the human's projection. Nothing
  consumes it yet.

### Planner
- **Done.** Recursive decomposer; plans always rebuilt from the live world; three delivery
  methods, most specific first, covering every state a task can resume from; also the
  recognizer's oracle and the owner of the completion test.
- **Due before section 4, not before the next step:** action effects are declared and not
  consumed, and conditions have no way to say a fact stops being true [TODO-07].
- **Small.** The recognizer keeps a private copy of the completion test that should delegate
  to the planner's.

### Executor and body
- **Done.** Diagram E.
- **Due.** Hold *refinement* (shortening or extending a wait against what the world shows) and
  how a refined hold is reported back are open; Mesa has none.
- **Measured limit, not to be fixed by a special case:** with the stop on, four of the five
  regression fixtures do not complete, because the scripted human idles at the table for ever.
  Blocked time is the reported outcome; the variant where the human steps aside exists as an
  evaluation fixture. The real remedies are the detour and human cooperation, both later.

### Fixtures, baselines, determinism
- **Done.** Five regression fixtures and three evaluation fixtures, each with the assignment
  prior off and on; scheduled bindings type-checked at spawn; current baselines are the
  graded-evidence sweep. Stop-off baselines contain walk-throughs: they compare decisions and
  support no safety claim.
- **Due.** Programmatic registration of layouts and scenarios (today: three manual edits per
  layout). Runs still need the fixed hash seed until every consumer of the unordered intention
  set is checked [TODO-42]; the generator's whole premise is that variation comes from
  generated inputs, not from seeds.

---

## 4. Before the full-queue reordering selection can start

**What the record says.** Choosing one next task was a decision about semantics, not a
shortcut: the architecture exists to keep improving its information about the human, and
optimising the robot's whole future against a forecast that will be better at the next trigger
inverts that. The full-queue strategy is kept as a switch for domains where tasks are strongly
coupled (travel or set-up between tasks, deadlines, dependencies, batching). To build it the
record names three things and adds: **not piecemeal**.

**Already in place, deliberately.**
- The strategy switch exists in code; both refusals are explicit.
- "Candidate" means whatever the selection ranges over, a task or an ordering.
- Realization already takes the path of *any* ordering, not only one task.
- Cost is one number, so orderings would compete on the same quantity as tasks do.

**What is missing, in the order I would take it.**

1. **The generated fixtures first.** They are the next step anyway, and the full-queue work
   depends on them three times over: they decide whether the commitment gate stays (which
   changes what an ordering competes against), they carry the scale calibration, and they are
   where the missing fixture comes from: *several remaining robot tasks whose order, not only
   the next choice, changes cost under a human stay*. Every present fixture leaves the robot at
   most one alternative.

2. **A hypothetical world carried from one projected task to the next** [TODO-07]. The second
   task's guards and walking time must see the world as if the first had completed. The right
   mechanism is applying declared action effects; the obstacle is that conditions cannot
   retract: a place adds "not holding" without removing the earlier "holding", so a naive union
   is contradictory and guard matching still finds the stale fact. This touches the core
   predicate model and needs its own design session. The record forbids a narrow
   position-and-holding stopgap inside the projector, because it would silently fail for any
   guard on another predicate. This is the structural blocker; the projector refuses orderings
   longer than one task because of it.

3. **The horizon question** [DESIGN-12]. The human is projected for the current task only. An
   ordering of three robot tasks runs far past that, so almost all of it lies in the unassessed
   stretch, where realization charges nothing. Priced as things stand, an ordering would differ
   from a single-task choice mainly by plain walking. Either the human's projection must reach
   further (a belief about the human's *next* tasks, which the episode-local recognizer
   deliberately does not hold, and which the robot may not read from the human's script), or
   confidence at a future horizon must come from the recognizer, or the unassessed share must
   start to be priced. This was moot only while one task was chosen at a time.

4. **A search shape.** Not brute permutation: bounded lookahead, an assignment formulation, or
   beam search.

**My reading, flagged as mine.** In the present kitting fixtures every delivery ends at the
table, so the robot's tasks are nearly independent in walking cost: what is left of "order
matters" is the human's timing, which is exactly what item 3 says the robot cannot yet see.
So item 3, not item 2, is where the design work is; item 2 is the larger code change but a
well-posed one. And the fixture in item 1 has to be one where order *can* matter, or the
comparison against single-task selection will show nothing by construction.

---

## 5. Where the documents disagree, and which I followed

Flagged only; nothing was edited.

| Where | What it says | What I followed |
|---|---|---|
| `shared/meta_planner.py`, the docstrings on the default bar and on the gate method | the bar is "not a settled constant"; two directions (a derived bar, a margin gate) are open | the gate ruling and the roadmap: both closed, the bar stays a fixed share |
| `shared/io_contracts.md`, recognizer section | a stretch folds as `L/u`, `unknown` is constant; the header's change log stops before the trigger, stop, ablation and grading work | the code and the hand-back: `L/u^f`. The body of the contracts is current on triggers, the stop and the ablation fix; only the recognizer section is behind |
| `shared/io_contracts.md`, two sentences | selection runs "over the realizable candidates"; "Mesa has no execution-time avoidance" | the same file a few lines later and the code: nothing is unrealizable; the stop is built |
| `docs/design_decisions.md`, older entries without a banner | the bar "gates reordering decisions"; the hard-gate entry "still describes the code"; the wait-decision preamble says nothing is implemented; two titles name a flag and a fallback that were removed; the prediction horizon "may span the full queue" | the later entries and the code |
| `docs/design_decisions.md`, one anticipated reversal | "no trigger fires on a stop" is expected to be reversed | it was not: the blocked event is designed, not built, and the claim that it removes the deadlock was withdrawn |
| `docs/TODOS_AND_DEFERRED.md` | many titles closed while the retained original text below still says open (the exclusion branch, the separation constant, the s10 crash, the block split); the next step is tagged "post-4C"; the newest items sit under "Known Limitations (Phase 2.1)" | titles and the newest paragraph of each entry; the lower half of a long entry is history |
| `docs/roadmap.md`, Phase 5 metrics | reveal tick and adaptation latency defined on the old crossing-trigger | to be restated on "recognition changed" when Phase 5 starts |
| analysis reports | completion ticks: the trigger report gives *declared* ticks, the ablation and grading reports *world* ticks | world ticks (declared minus 2), as the project now rules |

---

## 6. Plain name to label

| Plain name | Label | Lives in |
|---|---|---|
| choosing one next task vs ordering the whole pool | DESIGN-16 | design record "Single-task selection"; `meta_planner.py` strategy switch |
| the robot can wait; conflict priced as time | wait-decision revision, R1; DESIGN-08 resolved | design record "The robot can wait" |
| realization as a service | T3, T3b | `shared/realization.py`; `analysis/t3_realize/` |
| commitment gate, `b2a`, commitment share | T4; TODO-36 | `_is_current_task_plausible`; `analysis/t4_b2a/` |
| selection on realized cost | T10 | `_replan_tasks`; `analysis/t10_b3_realized/` |
| a continue costs nothing | T5; TODO-43 | `Executor.continue_plan` |
| projection time includes the body's delays | L2; TODO-77 | `analysis/l2_execution_lag/` |
| robot-responsible separation; realization total | F1; TODO-30 closed | `analysis/f1_robot_responsible/` |
| separation stop | C; TODO-73 | `mesa_sim/executor.py`; `analysis/c_separation_stop/` |
| one point place, blocked time as outcome, schema wait durations | R2; TODO-32, TODO-74 | design record |
| typed scheduled bindings; evaluation fixtures | F47, F47b; TODO-49 | `analysis/f47_fixtures/` |
| what a trigger is an event of; decision record; blocked event | D2; TODO-48/54/68 closed; TODO-80 | `evaluate_triggers`; `analysis/d2_recognition_trigger/` |
| ablation of the policy components; completed current task not continued | T6 | `analysis/t6_ablation/` |
| evidence graded by path covered | graded evidence (G1); TODO-61 (a) | `shared/likelihood_functions.py`; `analysis/g1_graded_evidence/` |
| the bar stays a fixed share | the gate ruling; TODO-64/65 closed | `_clears_gate` |
| recognizer rebuild and hand-back | I1 to I5 | `docs/recognizer_handback.md` |
| generated fixtures; their prerequisites and notes | TODO-47 (a) registration, (b) scale, (c) crossing fixture, (f) ordering fixture, (g) what reopens the bar | TODO file |
| separation value; detour tolerance in centimetres | TODO-28; TODO-58 | `MetaPlanner` constructor; `likelihood_functions.py` |
| hold refinement and reporting; wait at a chosen point | TODO-71; TODO-70 | TODO file |
| effects and retraction; confidence at a future horizon | TODO-07; DESIGN-12 | `shared/planner.py`, `shared/types.py` |
| fixed hash seed | TODO-42 | TODO file |
| unassessed stretch past the human's projection | TODO-69 | `RealizedPlan.unassessed_share` |
| detour, off-the-shelf path planner, human cooperation | Phase 4D; DESIGN-13, TODO-09, TODO-15 | roadmap |
