# The meta-planner test-bed (MPB)

This folder is the instrument: what it runs, what it derives and from which records, and how it compares. It was built
in MPB step 2 (29 September 2026) under design_decisions.md, "The meta-planner test-bed (MPB)", MPB-1 to MPB-6.
- The recognition-to-planning chain (the recognizer, the gate, the projection, the meta-planner) is tested with a
  working robot, one authored scenario per decision.
- The oracle states the expected decision before the run.
- A disagreement is classified, never fitted.
- The artefacts and their derivations are in `authoring.md`; the results are in `REPORT.md`.

Standing rule: the records' mechanism stands over runs, baselines and tests. An expectation changes only by derivation
from the records; a disagreement is classified under MPB-4's five classes.

## The artefacts

- The room: `env_layout_12`; since part (v) also `env_layout_13` (without the coffee machine) and `env_layout_14` (plus
  two robot station pairs).
- The setups: `env_setup_10` and `env_setup_11`; since part (v) also `env_setup_12` (on `env_layout_14`).
- The scenarios: `scenario_s10_01` to `_09` and `scenario_s11_01`, `_02` (eleven). `scenario_s10_07` to `_09` were added
  in part (iv) for coverage; `scenario_s11_01` and `_02` were re-authored in part (iv): the human's assigned delivery,
  never performed. Part (v) added five, one per claimed cell of the coverage matrix (`coverage.md`): `scenario_s12_01`,
  `_02`, `scenario_s11_03`, `scenario_s10_10`, `_11` (sixteen).
- The run files: `configs/mpb/`.

`authoring.md` gives the geometry, the disjointness check (MPB-3), the pre-run timing check and the control's fact.

## The pipeline (`run.sh`)

```bash
analysis/mpb/run.sh                                  # prior on, single_task, every configs/mpb/*.yaml
analysis/mpb/run.sh --strategy full_reorder          # the second run of the same scripts (MPB-6)
analysis/mpb/run.sh --prior off                      # the diagnostic appendix: no oracle comparison (MPB-6)
analysis/mpb/run.sh -o <dir> configs/mpb/scenario_s10_03.yaml
```

Outputs go to `<scenario>/<prior>_<strategy>/`. The logs and `.rec` streams go to `runs/` (git-ignored; their md5s are
in REPORT.md).

1. **`horizon.py`** computes the safety cap (MPB-5; TODO-138, ruled for MPB runs), which is the run's steps. It is the
   robot's pool chained along its authored order from its start on plain cost, plus the human's replay length, plus 30.
   - Plain cost is the layout's path lengths and the body's step rule, per task: the walk, its ack, the grasp and its
     ack; the carry, its ack, the release and its ack; the task-completion tick.
   - It is not a behavioural timeout. A run that does not complete within it is classified 2 or 4, never given a
     longer cap.
2. **The run** (`mesa_sim/run_mesa.py`, the run file and the options).
3. **`analysis/ir_testbed/trajectory.py`** (imported, unchanged) expands the load-time replay per tick with the body's
   timing. Its own check compares it with the run's human lines on every tick.
4. **`actual.py`** re-executes the run in-process (the primary source) and reads the run log (the check).
   - Pass-through recorders on the robot's MetaPlanner instance capture `evaluate_triggers` (the TriggerDecision and
     the world the robot built: its perception facts), `update_human_projection` (the ProjectedPlan) and `update` (the
     UpdateResult).
   - Each recorder calls the original and returns its result unchanged.
   - Per tick it reads the BeliefState, the gate from its one home (`_clears_gate`) and the decision record.
   - The model's log lines are asserted identical to the logged run's.
   - `observed.json` holds the run's `no_current_task` ticks, its terminal decision, and the comparison horizon: the
     first observed completion point (the human's script ended and the robot's pool empty) plus 30, capped at the steps
     (MPB-5).
5. **`mpb_oracle.py`** derives the per-tick table of parts 1 to 3 before any comparison, from the trajectory and the
   records: `expected_ticks.json`.
6. **`chain.py`** assembles the expected chain from the table and the run's observed `no_current_task` ticks:
   `expected_decisions.json`.
7. **`compare.py`** compares parts 1 to 3 exactly: `diff.md`, `diff.json`.
8. **`properties.py`** checks part 4 (the declared properties) and writes the measures and detectors:
   `properties.md`, `properties.json`.
9. **`reference.py`** runs the reference: the control's robot alone, the human removed. It is not registered (a
   reference run, not a scenario).
10. **`plot.py`** draws `figure.png`, the MPB's decisions-and-distance figure.
11. **`plot_ir.py`** (prior on; added at the close-out) draws `figure_ir.png`: the IR test-bed's figure
    (`analysis/ir_testbed/plot.py`, imported unchanged), the same panels, on the MPB's oracle table and in-process
    actual: the belief and the tail probability S per hypothesis of the support (expected lines, actual dots), the
    finding band, the observation-warrant bands and the gate's clearing, θ and α marked.
12. **`alteration.py`** runs the single-rule alteration test (MPB-4) over the committed outputs.

## Saved beside the compared columns (the MPB close-out, 30 September 2026)

Instrument additions; none is compared (`compare.py` reads its named fields), and no framework file changed. The sixteen
were rerun with them, every log and `.rec` stream byte-identical to REPORT.md's md5s.
- **The belief and S, per tick.** `expected_ticks.json` carries the IR oracle's belief, S and lifecycle per hypothesis of
  the support. `actual_ticks.json` carries the robot's whole distribution, the tails of the adequacy test's members and
  the lifecycle. `plot_ir.py` draws them.
  - **The belief here carries the output floor of the robot's items.** The setup's robot items are hypotheses outside
    the support, each held at the floor, so the support's shares sum to slightly less than 1 (0.995 with env_setup_10's
    five items), on both sides. This is the floor that moved scenario_s10_08's crossing from 46 to 47 and
    scenario_s12_01's admission from 25 to 26.
  - A retired hypothesis keeps its floor share in the robot's distribution (actual dots at 0) where the oracle's row has
    no belief (the expected line stops).
- **The segments, per admitted decision.** `actual_decisions.json` carries, for every decision that admitted a
  projection:
  - `human_segments`: the admitted human projection's segments;
  - `robot_segments`: the winner's realized plan, the hold before the first entry included.

  Each segment is [start_step, end_step, start_pos, end_pos] on the projection clock, **where step s is the end of world
  tick (decision tick − 1 + s)**: step 0 is the robot's position at the decision, and the human projection starts at the
  observation offset, step 1. The clock was established, not assumed, on scenario_s12_01's decision of 26 (part (v),
  objection 1): the recorded positions equal the executed ones at steps 1 and 2 (the human) and through the hold (the
  robot).
  - The winner's realized plan is taken by a pass-through wrapper around `shared.meta_planner.realize`: of the plans
    realized on the decision's tick, the least-cost one headed by the winner.
  - With these a check of projected against actual, and planned against executed, is read-only. The class-2
    correction's re-check of scenario_s12_01 at 45 to 47 was read this way (REPORT.md, "The class-2 correction"), and
    track 3b reuses it (TODO-145).

## What the oracle derives, with its sources

The oracle is `mpb_oracle.py`, with `mpblib.py`.
- It imports `shared.types`, `shared.knowledge.TaskModel`, `shared.planner` (AdaptivePlanner, DecompositionError),
  `domains.kitting.registry`, and the IR test-bed's `oracle.py` (which imports the same).
- At exit it asserts that none of these is loaded: `shared.meta_planner`, `shared.realization`, `shared.projection`,
  `shared.recognizer`, `shared.likelihood_functions`, `world.human_executor` (which imports `shared.projection`), any
  `mesa_sim` module (`RobotAgent._perceive`).
- The trajectory is expanded in its own process, as in the IR test-bed.
- θ is read from the run's `[run]` header, the one value read from a log.

Sources: DP = "T-D P" (P2 as kept by P4, P4, Q6); DG = "T-D G" (AD1, AD4); IO = `shared/io_contracts.md` §2.2;
GL = `docs/glossary.md`; IR = `analysis/ir_testbed/README.md`.

| # | rule | source |
|---|---|---|
| M0 | The support: the assigned tasks and every PersonalTask hypothesis; an empty assignment switches the restriction off, and the table is then not derivable before the run (the robot's items' deliveries are live): the oracle refuses (exit 3). Added in part (iii), class 1 | `shared/io_contracts.md` (the recognizer's `assigned_tasks`: None or [] switches the restriction off); MPB-3, MPB-6 |
| M1 | The belief's leader, the boundary, the adequacy finding (added in part (iv)), every live hypothesis's hypothesis adequacy and observation warrant, the gate's outcome per tick | IR rules 1 to 23 (its oracle, imported unchanged) |
| M2 | The warrant sources when the gate clears: commitment if the leader is an assigned task (IR rule 1's keys), observation if its observation warrant holds; in that order | DG AD1, AD4 |
| M3 | Perception facts from consecutive observed positions (the first the observation before the clock): the displacement; a zero displacement is a standing tick (the count grows, the run is 0); a step continues the run when its unit direction agrees with the previous step's within 1e-9 (the Euclidean distance of the unit vectors; the records name no norm), else starts a run of 1; a step resets the count | DP P4; GL §9 |
| M4 | The ray: the nearer of the workspace rectangle and the entry into the arrival radius (the body's, 30 cm) of the first fixed object along it (every object of the layout, landmarks included); an object whose radius contains the start is skipped | DP P2 (kept by P4), P4 AS BUILT |
| M5 | The fallback on a tick: standing, k = the standing count, duration k; moving, k = the run length, duration min(k, reach / step length); none without a previous observation | DP P4 |
| M6 | Its end: the tick + the observation offset (1) + the duration; `projection_expired` fires on the first tick at or after it | DP Q6; IO |
| M7 | The admitted projection's identity: the leader's key and the planner's decomposition of its task in the tick's world (the full decomposition, as `Projector.project` builds it) | MPB-1 (the planner's decomposition, as the IR test-bed uses it) |
| C1 | The decision record: the hypothesis on admission (cleared on a refusal) and the fallback's end (set when admission returns one, cleared otherwise), set at every decision, the robot's included | D2; DP Q6; MPB-1 |
| C2 | On a tick: `no_current_task`, then `recognition_changed`, then `projection_expired`; a `no_current_task` tick masks the others | D3 as superseded by Q6; IO |
| C3 | `recognition_changed` with a record: replaced, then boundary, then retraction (the recorded hypothesis inadequate); without one: entered (the gate clears) | IO (L-build); T-D L, L2 (ii), L5 B; D2 |
| C4 | `projection_expired`: a recorded fallback end reached | IO; DP Q6 |
| C5 | On a fired trigger admission is asked once: the gate clears, the leader's plan; otherwise the fallback | IO; DP P4 |
| C6 | Nothing is evaluated after the terminal decision | "The cognitive loop does not end with the task pool" |

The chain (C1 to C6) is assembled at the compare step from the per-tick table and the run's observed `no_current_task`
ticks. The robot enters there only (MPB-3).

## What is compared

Everything is exact unless stated.
- **Per tick (in-process):**
  - the leader, the boundary flag, the adequacy finding, the gate's outcome, every live hypothesis's hypothesis adequacy and observation
    warrant;
  - on the ticks the robot evaluated its triggers, the perception facts (the displacement at 1e-9 absolute).
- **Part 1:** the set of (tick, trigger, cause) of the decisions other than `no_current_task` (those ticks are the
  run's).
- **Part 2:** at every decision, the gate's outcome, the leader and the warrant sources.
- **Part 3:** at every decision, the admitted key and plan, or the fallback's mode, k, duration and end (1e-9
  relative) and its expiry tick.
- **The log:** per logged decision, the trigger and cause, the `[meta-proj]` text the decision implies, and the tick's
  `[IR]` leader.

Prior off is not compared (MPB-6). Its runs are reported by completion, holds, near-encounters and F1's classes.

## Part 4: the declared properties

These are booleans over the logged robot state.
- The planner's logged values (the winner, its hold, `[meta-cand]` delta) are observed inputs.
- The instrument's own computations are F1's classes over the executed positions (`analysis/tb1a_destination/
  sep_classes.py`) and the layout's path lengths; never a hold.

| scenario | property |
|---|---|
| scenario_s10_02 | P2a, the decision admitting deliver_item(item_1) (entered) carries a positive hold; P2b, no F1 robot violation within its assessed window |
| scenario_s10_03 | Retention through a deviation (D2's retention by identity until the retraction, L2 (ii); relabelled in part (iv): AD3 is not exercisable in the MPB set, "T-D G", AD3): P3a, no decision between the cut into the carry and the retraction; P3b, the decision record keeps the delivery; P3c, the leader is the delivery, an assigned task (commitment). The delivery's observation warrant over the interval is measured (entry-warranted: it persists). Defined for single_task: the pre-run timing check that keeps the robot's own triggers out of the interval is single_task's |
| scenario_s11_01 | P6.1, the switch to the alternative at a `projection_expired` decision, before the grasp of item_8, the human standing; P6.2 (single_task), at the switch item_8's hold exceeds the layout's cost difference, and at every earlier decision it does not (X1; the stand ends at 1 + k, so the hold is at most k + 1) |
| scenario_s10_06 | P8a, no hold at any decision; P8b, the completion equals the reference run's; P8c, the robot's per-tick positions equal the reference run's |
| scenario_s11_02 | none: TODO-132 (a)'s evidence (the decisions on the stand, the holds, the tick the persistence broke) |
| scenario_s10_07, _08 | none: the chain (retraction in the carry, the standing fallback's doubling, re-admission only at the place; replaced through the coffee hypothesis, then entered) is parts 1 to 3 |
| scenario_s10_09 | X5's ground (1), measured, not a mechanism: the stretches of the finding unexplained, the refused re-decisions inside them, and the first tick the finding has outlived one |

**The detectors** are recorded and classified by hand:
- TODO-134: a decision on a fallback stand whose first robot tick is an F1 violation;
- the arrival-tick ray: a decision on a moving fallback whose ray starts inside the radius of an object the human
  entered that tick. It is class 3 under MPB-4 and returns to Hadi.

## The alteration test (`alteration.py`)

One rule at a time, in a scratch copy:
- A1 to A5, the expiry cadence: the offset, the 1e-9 resolution, the turn's reset, the landmarks, the order on a shared
  tick;
- B1 to B3, the projection's identity: the method guards, the skip, the ray's cut;
- C1 to C3, the gate with warrant: commitment, the movement source, the order of adequacy and warrant;
- D1, D2, the chain's retraction and its cause order.

## The sort (1 October 2026): paths only, no change of behaviour

This folder holds kitting's set: the scenarios' outputs, `runs/` (git-ignored), this README, `REPORT.md`,
`authoring.md`, `coverage.md`, and the instrument's kitting-bound parts, `properties.py` (the declared properties),
`horizon.py` (MPB-5's cap, on kitting's `deliver_item` chain) and `alteration.py` (`docs/rename_table.md`, "Paths: the
sort"). The shared code moved to `analysis/instruments/mpb/`; the run files to `configs/kitting/mpb/`; `logparse.py` and
`sep_classes.py` to `analysis/instruments/common/`. Every command above reads `bash analysis/instruments/mpb/run.sh
kitting [-o <dir>] [--strategy ...] [--prior ...] [run files]`; `alteration.py` takes the scenario folders under
`analysis/kitting/mpb/`. The sixteen runs under each strategy were regenerated from the sorted tree: every output
byte-identical.
