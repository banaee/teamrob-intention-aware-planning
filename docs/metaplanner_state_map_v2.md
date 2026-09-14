# MetaPlanner — state map v2, after the realization redesign

Meta-planner side only. The recognizer is settled (`docs/recognizer_handback.md` is
authoritative on what it does).

This is a chat-side working map: the design picture plus the task queue. The repo carries the
design itself — `docs/design_decisions.md`, `docs/TODOS_AND_DEFERRED.md`,
`shared/io_contracts.md`. **Where this file and the repo disagree, the repo wins.**

Marked **[NEW]** where the realization redesign (Sept 2026) changed what v1 recorded.

---

## 1. The cognitive loop

One simulator tick, `mesa_sim/sim_agents.py: RobotAgent.step`:

```
  build_world_state(model)                        -> WorldState     (rebuilt fresh each tick)
  build_observation(human) -> recognizer.update() -> BeliefState    (no human: "unknown", 0.0)
  ExecutorState(agent_id, current_task, holding)

  decision = meta_planner.evaluate_triggers(belief, world, exec)
  if decision.fired:
      human_proj = meta_planner.update_human_projection(belief, world)
      result     = meta_planner.update(belief, world, exec, human_proj)
      if result.current_task is None: robot.finished = True
      else: current_plan = planner.plan(result.current_task, world, ...)
            attach result.hold to the plan as an execution HINT        [NEW]
  executor.step(current_plan)                     (every tick, fired or not)
  task completes -> advance_task() clears current_task -> next tick fires no_current_task
```

Layering, one-way, no cycles — **[NEW]** one layer added:

```
  trajectory_algorithms.py   pure geometry     segments in -> earliest violation / conflicts out
          |
  realization (hold-only)    "what would this trajectory actually be, given the human?"   [NEW]
          |
  projection.py              Projector         task + world -> predicted trajectory
          |
  meta_planner.py            MetaPlanner       which trajectory to pick
```

`shared/` never imports from `mesa_sim/` or `ros_sim/`, carries no domain strings, and holds no
world-unit constant.

---

## 2. Components and I/O

| component | in | out | policy? |
|---|---|---|---|
| `recognizer.update()` | Observation, WorldState | `BeliefState` (distribution, `most_likely`, `confidence`) | evidence model only |
| `planner.plan()` | TaskInstance, WorldState | `AbstractPlan` (flat, grounded) | none — decomposes, never schedules |
| `planner.is_complete()` **[NEW, T7]** | TaskInstance, WorldState | bool | none — terminal condition of the guard-selected decomposition, whoever made it hold |
| `Projector.project()` | task, WorldState, start_tick | `ProjectedPlan` (Segments, duration in ticks) | none |
| `Projector.project_human()` | hypothesis, WorldState | `ProjectedPlan` from the human's live position | none |
| `trajectory_algorithms` | segment + human projection + separation | earliest violation / clear time | none — measures only |
| **`realize()`** **[NEW]** | ProjectedPlan, human projection, `min_separation`, start_tick | `RealizedPlan` or `None` | none — separation passed IN |
| `MetaPlanner.evaluate_triggers()` | BeliefState, WorldState, ExecutorState | `TriggerDecision(fired, reason, score)` | **when to deliberate** |
| `MetaPlanner.update_human_projection()` | BeliefState, WorldState | `ProjectedPlan` or `None` | **whether the belief is trustworthy** |
| `MetaPlanner.update()` | BeliefState, WorldState, ExecutorState, human projection | `UpdateResult(current_task, queue, hold)` **[NEW: hold]** | **what the robot does** |

`RealizedPlan` carries: placed segments; holds (where, how long); total duration
(walking + holds); and the share of the trajectory beyond the human's horizon, i.e. unassessed
(TODO-69).

Injected into `MetaPlanner`: `knowledge`, `projector`, `recognizer` (live, by reference, for
`get_hypothesis()` only), `human_agent_id`.
Policy constants: `theta=0.75`, **`min_separation`** (was `min_safe_distance`) **[NEW]**,
`strategy`, `gate_strategy`, `interference_algorithm`.
Internal state: `_queue`, `_prev_belief`, `_prev_executor_state`.

---

## 3. The three questions, every fired tick

**Q1 — when to deliberate.** `evaluate_triggers()`:

| trigger | condition | reaches B2? |
|---|---|---|
| `no_current_task` | `current_task is None` — covers t=0 and every completion | no (B1.5 bypasses) |
| `theta_crossed` | crossing, `prev < θ ≤ now`, no hysteresis | yes |
| `task_committed` | `holding` goes `None -> item` | yes |

Prior-off, `theta_crossed` fires up to three times inside one grasp stop (rivals'
`deliver_with_return` phases lift them, dipping the true task below θ and back). Prior-on: one
per recognition. The recognizer is correct; the contract promises a crossing event, never one
per task (TODO-68).

**Q2 — what the human will do.** `update_human_projection()` admits only if `confidence ≥ θ`,
a human exists, the hypothesis resolves, and the winner is not `unknown` (T8).

Three facts bear on this gate:
- the belief is **episode-local**: it re-initialises to the prior at every human task boundary,
  so `None` is a **routine** mid-run state, not an edge case;
- confidence is **live-set dependent**: θ = 0.75 is a different bar with 3 and with 8
  hypotheses; ceiling `1/(1+uⁿ)` (TODO-64, TODO-65);
- one θ still serves both triggering and admission — under pressure, §8.

**Q3 — what the robot does.** `update()`.

---

## 4. `update()` — v2

**[NEW] The central change:** interference detection is no longer a separate step that drops
candidates. Each candidate is *realized* against the human's projection, and its cost is what
that realization actually takes.

```
update(belief, world, executor_state, human_projection) -> UpdateResult

  # --- Block 0: pool assembly -------------------------------------------
  pool = ([current_task] if not None else []) + _queue
  drop tasks already complete in the world (planner.is_complete)      [NEW, T7]
  if pool is empty:
      return UpdateResult(None, [])                 # terminal, returned not raised

  # --- B1.5: branch, not a block ----------------------------------------
  if current_task is None:
      goto B3                                       # nothing to continue

  # --- B2: PLAUSIBILITY gate --------------------------------------------
  #   "none": False always                                   [IMPLEMENTED, default]
  #   "b2a" : realize the CURRENT TASK ALONE -> judge hold δ  [NEW shape; open §8]
  #   "b2b" : realize current + each other    -> margin       [redundant with B3]
  #   human_projection is None -> True (continue)
  if _is_current_task_plausible(...):
      return UpdateResult(current_task, _queue)     # skip B3 entirely

  # --- B3: REORDER / selection ------------------------------------------
  for task in pool:
      proj     = projector.project(task, world)     # HTN method choice happens here, so a
                                                    # cancel/return detour is already counted
      realized = realize(proj, human_projection, min_separation, now)   [NEW]
      if realized is None: continue                 # no realization within the horizon
      cost = realized.duration                      # walking + holds, ONE number
  if nothing realized: -> the open case, §8
  winner = argmin cost
  _queue = pool - winner
  return UpdateResult(winner, _queue, hold = winner's holds)            [NEW]
```

**When `human_projection is None`** (routine, see Q2): realization is not called; cost is the
plain projected duration, as before.

### The realization algorithm (hold-only)

```
t = start_tick ; total_hold = 0
for each robot segment in order:
    loop:
        v = earliest_violation(segment placed at t, human_projection, min_separation)
        if v is None: break
        if v.clear_time beyond the human's horizon: break      # no human left to conflict with
        total_hold += (v.clear_time - t) ; t = v.clear_time
    place segment at t ; t += segment duration
return RealizedPlan(..., duration = walking + total_hold)
```

Two properties the loop must preserve:
- **A hold is a position.** While holding the robot stands where it is, so that stationary
  stretch is checked like any other. T1 found holds that "cleared" only because the waiting
  position was never checked.
- **Termination.** Each iteration moves `t` strictly forward past a violation interval ending
  within a finite horizon.

**`earliest_violation` is closed-form.** Two constant-velocity segments: relative motion is
linear, squared distance is a quadratic in time. No real root below `min_separation²` means no
violation; the roots give the violation interval and the earliest clear time. No sampling, no
resolution parameter, no world-unit constant in `shared/`. This is what
`closest_point_of_approach` was reserved for; `discretized_time_sampling` is a fallback that
computes more than a hold needs.

**Out of scope, recorded as such:** a hold placed *mid*-segment (cheaper sometimes, but holding
before starting always converges and is what T1 measured); waiting somewhere other than where
you are, which is a detour, i.e. a different strategy.

### The hold reaches the executor as a hint

`UpdateResult` carries the winner's holds; they ride on the plan. Mesa honours them literally
(no motion layer); ROS passes them to its motion layer as a temporal constraint. The executor
may **refine** a hold — the human may deviate within a few ticks — but the decision is made
once, in `shared/`: the executor must not independently decide whether to wait, which task to
run, or silently cancel the decision.

Rejected: estimate the pause now, execute in 4D. A cost containing a hold the robot never takes
is a fiction, and any B2/B3 result measured on it would describe a plan that was not executed.

---

## 5. Why the redesign (two findings)

**(a) The conflicts are timing conflicts, not path conflicts.** T1 measured the fixture
interference as both agents arriving at the shared table within a tick of each other. The
proportionate response is to wait briefly, not to abandon the task. With selection as the only
lever, the only available response was to switch — the over-reaction.

**(b) A batch interference profile cannot place a hold.** `_detect_interference` answered "over
these two FIXED trajectories, where do they come close" — it cannot see that holding at the
first conflict shifts everything after it. Its answer is stale the moment a hold is placed. T1
also measured its aggregates as misleading: every conflicted `min_dist` sat at the LAST step of
the shared window (an arrival gap, not a closest approach), and exposure ranked candidates
opposite to the pause actually required.

---

## 6. What replaced what

| v1 | now | replacement |
|---|---|---|
| `_detect_interference()` a public step in B3 | superseded | internal to `realize()` |
| `_cost()` returns duration; conflicts computed, carried, unused (DESIGN-08 open) | **DESIGN-08 resolved** | conflict becomes cost *by construction* — a conflicted task is dearer because avoiding the human takes longer. No weight to tune |
| `min_safe_distance` = exclusion threshold | restated | `min_separation` = clearance realization must **achieve**; still the single policy decision, still uncalibrated |
| "infeasible" = a ConflictPoint below threshold | restated | "infeasible" = **no realization exists** within the human's horizon |
| all-candidates-excluded raises `RuntimeError` | superseded | condition changed meaning; outcome **open**, §8 |
| batch measurement over whole trajectories | superseded | per segment, earliest violation given a start time |
| B2 has no scalar that exists | resolved | realization gives B2 the current task's hold δ |
| B2 supplies what B3's argmin cannot express | **gone** | B3's argmin now accounts for conflict; B2's remaining roles are narrower (§8) |

**DESIGN-08 — what survives.** The **observe / value split is intact, relocated**:
`earliest_violation` observes (pure geometry, no policy); holding is what turns the observation
into a number; realization is *given* `min_separation` rather than choosing it. And **team-level
semantic costs stay parked** — realization prices only the robot's own time.

---

## 7. Settled, do not relitigate without new evidence

- **DESIGN-16** single-task receding horizon: best next task per trigger, re-decided from fresh
  world and belief. Realization changes what a candidate *costs*, not how many are chosen.
- The current task competes as an ordinary candidate inside B3; continuation vs reselection
  falls out of the argmin.
- **Realization is shared machinery, owned by neither block.** B2 realizes one task; B3 realizes
  all of them.
- Queue invariant: `_queue` excludes the executing task. **Task completion is a world fact**
  (T7): one fact, one owner.
- Cancellation is an HTN method choice, never a cost term. Realization adds **holds**, never
  methods.
- Plans are re-decomposed from scratch; realization produces no persistent state.
- Interference is geometric, not zone-based.
- Trajectory algorithms measure only and hold no policy.
- Projection is a service separate from selection; realization sits on the projection side.
- Task exhaustion is returned, not raised.
- Waiting is part of 4C, as a computed pause reaching the executor as a hint.

---

## 8. Open

**Belongs to D1, on re-measured data:**
1. **`min_separation`'s value.** Cannot be read off a distribution (T1: no gap in the data).
   Must be argued and expressed **relative to scale** — motion per tick, or layout scale — so it
   survives randomised layouts (TODO-47).
2. **Does B2 survive as a block?** δ in isolation has no reference: two ticks is cheap against a
   19-tick switch and expensive against a 3-tick one. Three readings — δ against the human's
   **remaining horizon** (self-contained, distinguishes "hold briefly" from "hold until the human
   is gone"); δ as a fraction of the task's own duration (an overhead ratio, arbitrary like a
   bare threshold); or B2 reduces to computation saving and hysteresis (the latter matters more
   now that prior-off triggers fire up to three times per recognition).
3. **Per-segment vs whole-trajectory holds.** T1 measured a whole-trajectory shift; the algorithm
   above holds per segment. Confirm on data.
4. **All-candidates-unrealizable.** Means: for every task, no start time within the horizon
   clears the separation (e.g. a human idle at the table). Three readings, none chosen —
   (1) hold and re-decide at the next trigger, needing a re-entry rule and a deadlock guard;
   (2) pick the least-bad candidate and let the executor handle the residual, defensible because
   the hold is a hint; (3) treat it as evidence `min_separation` is wrong or the horizon too
   short, and record rather than act.

**Belongs to D2:**
- **What a trigger is an event of** — TODO-68 (repeated crossings), TODO-48 (`most_likely` change
  above θ), TODO-54 (`theta_crossed` on `unknown`) are one question.
- Whether the gate should read a **likelihood ratio** rather than a normalised posterior
  (TODO-65), and whether triggering and admission want the **same θ** (TODO-64).

**Still open, unowned:**
- **The horizon.** Realization assesses only within the human's projected horizon; beyond it,
  segments are shifted but not assessed. Bias accepted (TODO-69) — **and a hold makes it worse**,
  since holding pushes more of the trajectory past the horizon. Not to be closed by projecting
  the human's *next* task from `scheduled_tasks`: that is the script, not something the robot can
  know. The horizon can only be extended by observation.
- **Is sharing the kitting table a distance conflict or a capacity conflict?** Modelled as one
  point, so any time overlap reads as zero distance.
- **What time margin shared-place decisions need**, given a 1–2 tick prediction error (executor
  stops 30 cm short) plus the one-tick re-plan shift (TODO-43).

**Deferred:** TODO-29, TODO-32 (`wait_at` duration — now load-bearing, since foreseeable tasks
are recognised and a long human occupation changes the wait/switch calculus), TODO-37, TODO-39,
TODO-41, TODO-44, TODO-45, TODO-47.

---

## 9. The queue

Nothing completed needs redoing. The redesign changes what comes next, not what came before.
One plan is deleted rather than built on: calibrating `min_safe_distance` as an *exclusion
threshold*. It becomes clearance-to-achieve instead.

| # | id | content | you? |
|---|---|---|---|
| ✅ | **T1** | conflict-geometry measurement | rows stale (old IR, pre-T2 units); **findings stand and produced this redesign** |
| ✅ | **T2** | projection time = execution ticks; unit assumptions out of `shared/` | realization needs this — a hold in arbitrary units is meaningless |
| ✅ | **T7/T8** | completed-task drop (world fact); `unknown` not admitted | independent of the redesign |
| ✅ | **design record** | this redesign documented in the repo; mechanical comment/doc updates | |
| **1** | **T5** | TODO-43, the one-tick re-plan cost | no |
| **2** | **T1b** | re-measure — **reshaped**: what realization would produce per candidate (hold δ, unrealizable cases, unassessed share), not conflict profiles. Throwaway realizer in the analysis script, not in `shared/` | no |
| **3** | **D1** | decide §8 items 1–4 | **yes** |
| **4** | **T3** | implement realization: `earliest_violation` closed-form, hold-only `realize()`, wired into B3, hold as an executor hint, `min_separation` from D1 | no |
| **5** | **D2** | what a trigger is an event of; θ's two roles | **yes** |
| **6** | **T4** | B2, if D1 keeps it: realize the current task alone, gate on δ | no |
| **7** | **T6** | ablation across B2 × B3, new scenario set (s10 dropped, s30/s40 added) | no |

**Why T5 first:** independent of the redesign, and it distorts every measurement taken after it
— prior-off, triggers now fire up to three times per recognition, so the one-tick shift repeats.

**Why T1b before D1:** T1's rows came from the old IR and pre-T2 units, and its question has
changed. Deciding a separation from them would repeat a failure this project has had twice.

**How T3 grew:** it was "calibrate a threshold and exercise the exclusion branch". It is now
"build realization" — the core of the redesign. **D1 shrank** correspondingly: the conflict
scalar and DESIGN-08 answered themselves.
