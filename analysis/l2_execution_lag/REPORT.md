# L2 — Removing the systematic execution lag from the projection

Code before: `1295e44` (the θ single-source change; projection as T9 left it). Code after: HEAD.
Ten conditions per side, `PYTHONHASHSEED=0`, via `analysis/t9_arrival_radius/sweep.sh`. Test set as
specified: scenario_30 (`env_layout3`) and scenario_20 (`env_layout2`), assignment prior off and on,
each run to completion. The other six conditions are verification only and no finding is drawn from
them. The meta-planner is otherwise untouched: `min_safe_distance = 1.0` is still live and the
all-candidates `RuntimeError` is still in the code. No condition raised.

Units: ticks (1 tick = 20 cm of motion), distances in cm. "Lead" is TODO-77's measure,
`(trigger + projected place start) − actual release tick`; negative means execution behind projection.

## How to read this directory

| File | Content |
|---|---|
| `stages.sh` | Regenerates everything (~1 min). |
| `timing.py` | TODO-77's measure. Locates the `place` segment by stride, so it reads pre- and post-L2 captures alike. `timing_before.md`, `timing_after.md`. |
| `residual.py` | Attributes what is left: per-walk quantisation, the robot's skipped acknowledgement, and a discrete-step forward model of the executor. `residual.md`. |
| `ablate.py` | Runs one condition with each half of L2 alone. `ablation.md`. |
| `compare.py` | Decisions vs the T9 baselines. `comparison.md`. |
| `new/` | The ten logs (git-ignored). **These are the baselines for T3, T4 and T10.** md5s below. |

## How the latency reaches the projection, and where the human's projection starts

`Projector` gained two body-supplied arguments, alongside `assumed_speed`, `default_action_cost` and
T9's `arrival_radius`. `shared/` holds neither constant; both default to 0.0, a unit-less placeholder,
and at 0.0 the projection is exactly what it was.

**`action_completion_latency`.** `build_segments()` appends, after every action's own segment, a
STATIONARY segment of that duration at the position the action ended at. Stationary because the agent
is standing still while the body catches up, not moving slowly; as a segment because that hold is then
checked by interference like any other. Mesa passes
`mesa_sim/executor.ACTION_COMPLETION_LATENCY = 1.0`, defined in the executor because it is a property
of that loop: `step()` sees the completion predicate in the WorldState it was handed, calls
`_advance_action()` and returns, executing no microaction that tick. It is not a tunable — change
`step()`'s structure and it changes with it. Consequence for consumers: **two segments per action**,
so a plan's actions can no longer be indexed by segment position without the stride.

**`observation_offset`.** `project_human()` passes it as `start_step` instead of 0. Mesa passes
`mesa_sim/sim_agents.OBSERVATION_OFFSET = 1.0`, defined beside the scheduler fact that causes it:
`BaseScheduler` runs agents in insertion order and the human is spawned first, so at the instant the
robot decides, the human has already moved this tick and the robot has not. The robot's projection
starts from where the robot stood at the end of the previous tick; the human's observed position is
where it stands at the end of THIS one. Without the offset a common `t` compared the robot's position
with the human's position one tick later. The human's projection now says nothing about
[0, offset) — nothing was observed of the human at the robot's own now — and that interval is simply
outside its span. No invented position, and no hole in the geometry: `pair_violation` and every other
interference routine intersect windows, so an unassessed prefix is an unassessed prefix.

## Projected versus executed timing, in TODO-77's terms

Both sides measured by the same script (`timing.py`), which reproduces T9's published numbers exactly
on the old captures.

| rows | n | before: min / median / max | after: min / median / max |
|---|---|---|---|
| robot, 2-action plan | 30 | −1.98 / **−1.46** / −1.00 | −0.98 / **−0.46** / +0.00 |
| robot, 4-action plan | 35 | −4.55 / **−3.32** / −2.26 | −1.55 / **−0.32** / +0.74 |
| human, 2-action plan | 21 | −2.89 / **−2.21** / −2.07 | −0.89 / **−0.21** / −0.07 |
| human, 4-action plan | 17 | −6.39 / **−5.32** / −4.07 | −2.39 / **−1.32** / −0.07 |

Every median moves by exactly the whole number of ticks the two causes predict: +1 per acknowledged
action before the release (1 for a 2-action plan, 3 for a 4-action one) and +1 for the human's offset.
The systematic whole-tick lag is gone; no median exceeds half a tick except the human's 4-action rows.

### What remains, and why (not compensated)

A discrete-step forward model of the executor — which replays the walk in 20 cm steps stopping on the
first step inside the 30 cm radius, recovering targets from the projection's own segments and using
**no execution data** — predicts the actual release tick:

| rows | n | forward model vs actual | exact |
|---|---|---|---|
| human, 2- and 4-action | 38 | +0.00 | 38/38 |
| robot, 2-action | 30 | +0.00 | 30/30 |
| robot, 4-action | 35 | +1.00 (always) | 0/35 |

So the residual is fully attributed, with nothing left over.

**Step quantisation** (decided: not compensated) accounts for all 68 human and robot 2-action rows
exactly. It has two forms. Within a walk, a projected duration `dur` is executed as `ceil(dur)` steps,
so execution is `ceil(dur) − dur` ticks late, always in [0, 1). Across walks it compounds: the walker
stops on the first step INSIDE the radius, not on it, so the next walk starts up to one step off the
projected start and can be a whole step longer. That is why the human's 4-action median is −1.32 rather
than sub-tick — two walks, one of them displaced. Measured instance, scenario_30 prior-off, trigger 86:
the human stopped 15.07 cm from item_7 where the projection assumed 30.00, lengthening the carry from
367.23 cm to 382.14 cm, which crosses a step boundary (19 projected steps, 20 executed). Per walk the
residual is under a tick; over a two-walk plan it need not be.

**The robot's skipped acknowledgement** accounts for the remaining +1 on all 35 robot 4-action rows,
and it is the projection running LONG, not short. The projection charges four latencies; execution
spends three before the release. The robot re-plans at its own `task_committed` trigger, which fires on
the tick that would have acknowledged the `pick_up`, and the fresh `deliver_already_held` plan does not
contain that `pick_up`, so `continue_plan()` loads from the start and the carry begins on that very
tick. Verified in the log (scenario_30 prior-off): tick 38 acknowledges the walk, tick 39 grasps, tick
40 is already a carry step. The human, which never re-plans, pays every acknowledgement. Not
compensated, and not compensable in the same way: the projection would have to predict the robot's own
future triggers, which are decided FROM the projection. It partly cancels the quantisation in those
rows (median −0.32), which is arithmetic, not accuracy. Recorded in TODO-77.

## Decision-sequence changes against the T9 baselines

**Test set.** scenario_20 prior off and on: decision sequence unchanged, and the full log minus
`[meta-cand]` and `[sep]` is byte-identical. scenario_30 prior off: the same. scenario_30 prior on:
one change, below.

**Verification only** (no findings drawn): s00, s10 and s40, both priors, are unchanged on the same
test, so nine of the ten conditions decide identically.

**The mechanism is not durations.** The task was set with "B3 is still plain-cost argmin, so any change
comes from durations". That is not what the code does, and the code wins: B3 is an argmin over
candidates `_detect_interference()` has not excluded, and that filter is still live. Across the ten
conditions the latency raised every candidate's cost by one tick per action and **reordered no
candidate set at any of the 93 triggers compared**. The single change comes from the offset.

**scenario_30, prior on, step 21** — the mirror crossing, the trigger M1 studied:

| | `min_dist` | outcome |
|---|---|---|
| baseline | item_4 15.37, item_2 22.68 | item_4 wins on cost (50 vs 61) |
| new | item_4 **0.49**, item_2 9.44 | item_4 `feasible=False`, item_2 wins |

With the two agents finally in phase, the projection sees the head-on crossing as the near-coincidence
it is: the agents pass through each other between ticks 22 and 23, swapping sides with identical y, so
the continuous-time minimum is essentially zero. `[sep]`'s 11.0 cm was the closest integer-tick sample,
not the true minimum. The baseline's 15.37 cm was the artefact of comparing the robot's position with
the human's a tick later. The superseded `min_safe_distance = 1.0` then excludes item_4.

Ablation (`ablation.md`, the two halves run separately on this condition) settles the attribution:
latency alone leaves `min_dist` at 15.37 and the decision unchanged; offset alone produces 0.49 and the
whole change. Downstream, the robot delivers item_2 first, the run ends at 159 instead of 154, and its
actual separation minimum becomes 9.6 cm over 50 sub-50 cm ticks instead of 11.0 over 64. The belief is
untouched while both runs last — all 310 baseline `[IR]`/`[IR-dist]` lines are identical and the new run
merely has 10 more, because prior-on the human's live set excludes the robot's items (support
restriction), so the robot's deliveries are not evidence.

This exclusion is a vestigial mechanism reacting to a newly-accurate number, not a new policy:
`min_safe_distance` was superseded at R1 and is removed in T10 (TODO-30). Flagged, not fixed — out of
scope here.

## Verification

1. `timing.py` reproduces T9's published before-numbers exactly on T9's captures, so the before/after
   table is one measurement, not two.
2. Instrumentation is neutral: T1b's `measure.py` re-run at HEAD writes logs byte-identical to `new/`
   minus the `[sep]` lines, in all eight conditions it covers.
3. The forward model uses no execution data and is exact on 68 of 103 rows and exactly +1 on the other
   35, which is the attribution above rather than a fit.
4. `domains/dock_loading` still imports (every run goes through `run_mesa.py`, which imports its
   registry).
5. Nine of the ten conditions are byte-identical outside `[meta-cand]` and `[sep]`; the tenth is
   explained above and ablated.

## Baselines for T3, T4 and T10

`analysis/l2_execution_lag/new/`, md5:

| condition | md5 | condition | md5 |
|---|---|---|---|
| s00_off | d4321dcaa6b2f22e8a3c5f6730933bd6 | s00_on | 13059b4f5169f89f865264a44230f232 |
| s10_off | 374838d83f72dffc63eb7e073dd628dc | s10_on | b466d447539f2d1cc89e72bfdf5356f5 |
| s20_off | 437369082836f5c890288bb2bdd1179e | s20_on | de91a0cd0110a6b2f52833f9ea783abb |
| s30_off | 302d1e67fafd8299e7f2107cb88c7def | s30_on | 8562464354b8f55b5bee4b86176c6f9e |
| s40_off | 69791e05e82b4fc57599219a7adfcb9b | s40_on | 704f500ba94340043936d9b0767bf1a7 |

## Flagged, out of scope

- **`min_safe_distance = 1.0` is live again**, once in the sweep (above). Superseded at R1, removed in
  T10; not touched here.
- **Two segments per action** breaks any 1:1 indexing of actions by segment position.
  `analysis/t1b_realization/analyze.py`'s `phase_at()` assumes 1:1 and would mislabel phases if re-run
  against post-L2 captures; it is a record of T1b's runs and was not changed. L2's own scripts read the
  stride and handle both shapes.
- **The trailing task-completion tick is still unmodelled.** After the last action's acknowledgement the
  executor spends one more tick on `_on_task_complete()` before the next task starts. It is a
  task-level cost, not per-action, and falls outside L2's decided scope; it does not affect the
  placement measure, which ends at the release.
