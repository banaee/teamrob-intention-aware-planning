# The meta-planner test-bed (MPB)

The data and figures of this set (.json, .csv, .png) are not in git (Hadi, 2 October 2026). They are regenerated
by the set's run script (`analysis/instruments/mpb/run.sh kitting`). A byte comparison uses the local copy or the outside copy,
`/home/hadi/teamrob_analysis_2026-10-02/` (the whole of analysis/ as it was at 38d66ea).

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
3. **`analysis/irb/trajectory.py`** (imported, unchanged) expands the load-time replay per tick with the body's
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
11. **`plot_ir.py`** (prior on; added at the close-out) draws `figure_ir.png`: the IRB's figure
    (`analysis/irb/plot.py`, imported unchanged), the same panels, on the MPB's oracle table and in-process
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
  `domains.kitting.registry`, and the IRB's `oracle.py` (which imports the same).
- At exit it asserts that none of these is loaded: `shared.meta_planner`, `shared.realization`, `shared.projection`,
  `shared.recognizer`, `shared.likelihood_functions`, `world.human_executor` (which imports `shared.projection`), any
  `mesa_sim` module (`RobotAgent._perceive`).
- The trajectory is expanded in its own process, as in the IRB.
- θ is read from the run's `[run]` header, the one value read from a log.

Sources: DP = "T-D P" (P2 as kept by P4, P4, Q6); DG = "T-D G" (AD1, AD4); IO = `shared/io_contracts.md` §2.2;
GL = `docs/glossary.md`; IR = `analysis/irb/README.md`.

| # | rule | source |
|---|---|---|
| M0 | The support: the assigned tasks and every PersonalTask hypothesis; an empty assignment switches the restriction off, and the table is then not derivable before the run (the robot's items' deliveries are live): the oracle refuses (exit 3). Added in part (iii), class 1 | `shared/io_contracts.md` (the recognizer's `assigned_tasks`: None or [] switches the restriction off); MPB-3, MPB-6 |
| M1 | The belief's leader, the boundary, the adequacy finding (added in part (iv)), every live hypothesis's hypothesis adequacy and observation warrant, the gate's outcome per tick | IR rules 1 to 23 (its oracle, imported unchanged) |
| M2 | The warrant sources when the gate clears: commitment if the leader is an assigned task (IR rule 1's keys), observation if its observation warrant holds; in that order | DG AD1, AD4 |
| M3 | Perception facts from consecutive observed positions (the first the observation before the clock): the displacement; a zero displacement is a standing tick (the count grows, the run is 0); a step continues the run when its unit direction agrees with the previous step's within 1e-9 (the Euclidean distance of the unit vectors; the records name no norm), else starts a run of 1; a step resets the count | DP P4; GL §9 |
| M4 | The ray: the nearer of the workspace rectangle and the entry into the arrival radius (the body's, 30 cm) of the first fixed object along it (every object of the layout, landmarks included); an object whose radius contains the start is skipped | DP P2 (kept by P4), P4 AS BUILT |
| M5 | The fallback on a tick: standing, k = the standing count, duration k; moving, k = the run length, duration min(k, reach / step length); none without a previous observation | DP P4 |
| M6 | Its end: the tick + the observation offset (1) + the duration; `projection_expired` fires on the first tick at or after it | DP Q6; IO |
| M7 | The admitted projection's identity: the leader's key and the planner's decomposition of its task in the tick's world (the full decomposition, as `Projector.project` builds it) | MPB-1 (the planner's decomposition, as the IRB uses it) |
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

## T-K part 1, build stage 2: the gate on the belief over the live hypotheses (4 October 2026)

The sixteen were rerun under both strategies, prior on, and the prior-off appendix, their outputs replaced (AM57). The
oracle is the IRB's (rule 28: the leader's belief over H); `actual_ticks.json` and the oracle's figure columns also
carry `belief_h`, which `plot_ir.py` draws. Old data and figures: Kept in one external copy, outside the repository (AM59): `/home/hadi/teamrob_analysis_2026-10-04/` (its README.txt).
The last commit holding the old results' reports: 3b05a8a (the build's stage 2b; the reports there are
93f9083's).
Results (`REPORT.md`, the section of this date): parts 1 to 3, 0 disagreements in all 32 prior-on runs; every declared
property of part 4 reads as before (each holds under single_task); every claimed cell of `coverage.md` is still reached.
Runs (git-ignored; md5s at the rerun):

```
9d1ae833e27dae217a56c0fd0a66d8e8  runs/env_layout_12_scenario_s10_01_off_single_task.log
8451bf1f7048ec68b33375c2cc99cb15  runs/env_layout_12_scenario_s10_01_off_single_task.rec
b05c35ef0ed8e46bb50a7a0d1a58fc82  runs/env_layout_12_scenario_s10_01_on_full_reorder.log
8451bf1f7048ec68b33375c2cc99cb15  runs/env_layout_12_scenario_s10_01_on_full_reorder.rec
3fabe8aeebc0e6f646c882b992e55fd2  runs/env_layout_12_scenario_s10_01_on_single_task.log
8451bf1f7048ec68b33375c2cc99cb15  runs/env_layout_12_scenario_s10_01_on_single_task.rec
30a3d29cb6cc7fe378ffc9b1e3fb94b5  runs/env_layout_12_scenario_s10_02_off_single_task.log
321732473c562c43b06ae158ca81cdef  runs/env_layout_12_scenario_s10_02_off_single_task.rec
a50ff043c85c7d21d3da42da8fb6c4e6  runs/env_layout_12_scenario_s10_02_on_full_reorder.log
321732473c562c43b06ae158ca81cdef  runs/env_layout_12_scenario_s10_02_on_full_reorder.rec
63845ad386e60dadf0e5a64c60ae5a0f  runs/env_layout_12_scenario_s10_02_on_single_task.log
321732473c562c43b06ae158ca81cdef  runs/env_layout_12_scenario_s10_02_on_single_task.rec
7e542390bb4d61aecc07d653b1642691  runs/env_layout_12_scenario_s10_03_off_single_task.log
7fa9d641f1a0df5af13e70ec188ad19e  runs/env_layout_12_scenario_s10_03_off_single_task.rec
32d7a86c2953e47a099bd22b3d92c6a3  runs/env_layout_12_scenario_s10_03_on_full_reorder.log
7fa9d641f1a0df5af13e70ec188ad19e  runs/env_layout_12_scenario_s10_03_on_full_reorder.rec
947eb469a27087d4cdbfae464c32ad07  runs/env_layout_12_scenario_s10_03_on_single_task.log
7fa9d641f1a0df5af13e70ec188ad19e  runs/env_layout_12_scenario_s10_03_on_single_task.rec
6f0a0520b3a48c03f6f43021d036f504  runs/env_layout_12_scenario_s10_04_off_single_task.log
88dcf2598e25a94807b1e1f981218bff  runs/env_layout_12_scenario_s10_04_off_single_task.rec
cac4fdf38acda5bfe9ff777de800cb7c  runs/env_layout_12_scenario_s10_04_on_full_reorder.log
88dcf2598e25a94807b1e1f981218bff  runs/env_layout_12_scenario_s10_04_on_full_reorder.rec
58fcad56bfbe7736241aa07412f2d7d1  runs/env_layout_12_scenario_s10_04_on_single_task.log
88dcf2598e25a94807b1e1f981218bff  runs/env_layout_12_scenario_s10_04_on_single_task.rec
8df9322b9db327755f0ab0e82d2de5fe  runs/env_layout_12_scenario_s10_05_off_single_task.log
c0b3c52826984a71c0637d8dfc8eba55  runs/env_layout_12_scenario_s10_05_off_single_task.rec
f3fdaeb27bd0f869ec6fced9c9e549ba  runs/env_layout_12_scenario_s10_05_on_full_reorder.log
c0b3c52826984a71c0637d8dfc8eba55  runs/env_layout_12_scenario_s10_05_on_full_reorder.rec
640489611aa4e38c328944432a39d588  runs/env_layout_12_scenario_s10_05_on_single_task.log
c0b3c52826984a71c0637d8dfc8eba55  runs/env_layout_12_scenario_s10_05_on_single_task.rec
d2d2ff83e89de102338bfde3e7ac80c5  runs/env_layout_12_scenario_s10_06_off_single_task.log
4bdc76ccc6f1ee3244e89c5458b19ffe  runs/env_layout_12_scenario_s10_06_off_single_task.rec
50cdea4b0c90a01d238f9f72083d1314  runs/env_layout_12_scenario_s10_06_on_full_reorder.log
4bdc76ccc6f1ee3244e89c5458b19ffe  runs/env_layout_12_scenario_s10_06_on_full_reorder.rec
0fc09c6a6448699b89a8f312a63fef59  runs/env_layout_12_scenario_s10_06_on_single_task.log
4bdc76ccc6f1ee3244e89c5458b19ffe  runs/env_layout_12_scenario_s10_06_on_single_task.rec
7cf6807fa86d405f88629fa7263d2aac  runs/env_layout_12_scenario_s10_06_reference_full_reorder.log
665e5a5422011e9b31f8057270f370c8  runs/env_layout_12_scenario_s10_06_reference_single_task.log
1e483c1bad4d3a09ac123ab2481590f7  runs/env_layout_12_scenario_s10_07_off_single_task.log
9f6bde960f345934b2423236f91fa158  runs/env_layout_12_scenario_s10_07_off_single_task.rec
f7c8d993f5ab4b07e859b324f38bb9dc  runs/env_layout_12_scenario_s10_07_on_full_reorder.log
9f6bde960f345934b2423236f91fa158  runs/env_layout_12_scenario_s10_07_on_full_reorder.rec
619cc1275852b1b4ac5a6fec00c22d44  runs/env_layout_12_scenario_s10_07_on_single_task.log
9f6bde960f345934b2423236f91fa158  runs/env_layout_12_scenario_s10_07_on_single_task.rec
58b2406fc540f9219b08f2cd318f61a4  runs/env_layout_12_scenario_s10_08_off_single_task.log
33ee73bcf6ffefa2c81b3607397ac879  runs/env_layout_12_scenario_s10_08_off_single_task.rec
2035bab0b0a78386a34b6b070e9c6e53  runs/env_layout_12_scenario_s10_08_on_full_reorder.log
33ee73bcf6ffefa2c81b3607397ac879  runs/env_layout_12_scenario_s10_08_on_full_reorder.rec
24ac5ccd94bfa3ef55bc7797396e38d5  runs/env_layout_12_scenario_s10_08_on_single_task.log
33ee73bcf6ffefa2c81b3607397ac879  runs/env_layout_12_scenario_s10_08_on_single_task.rec
c29f8d13e800e0d3c62df70261956aa1  runs/env_layout_12_scenario_s10_09_off_single_task.log
ebcb27b9f5dbf9cfcfa67e4b25a2ba3a  runs/env_layout_12_scenario_s10_09_off_single_task.rec
4393ea94df570465664d43e2997ca009  runs/env_layout_12_scenario_s10_09_on_full_reorder.log
ebcb27b9f5dbf9cfcfa67e4b25a2ba3a  runs/env_layout_12_scenario_s10_09_on_full_reorder.rec
609db8ad50af161845b9a406543310ac  runs/env_layout_12_scenario_s10_09_on_single_task.log
ebcb27b9f5dbf9cfcfa67e4b25a2ba3a  runs/env_layout_12_scenario_s10_09_on_single_task.rec
50a0a06817377f7ae9d19c9c08f8099d  runs/env_layout_12_scenario_s10_10_off_single_task.log
4251537079b3d12ed72aa11e6771f5e0  runs/env_layout_12_scenario_s10_10_off_single_task.rec
7a773c84f44c4587544f31288e797a3d  runs/env_layout_12_scenario_s10_10_on_full_reorder.log
4251537079b3d12ed72aa11e6771f5e0  runs/env_layout_12_scenario_s10_10_on_full_reorder.rec
05579aed5fb3da10ded2d3c32cee9355  runs/env_layout_12_scenario_s10_10_on_single_task.log
4251537079b3d12ed72aa11e6771f5e0  runs/env_layout_12_scenario_s10_10_on_single_task.rec
e588f5294049dd157c037706c1ff0f6a  runs/env_layout_12_scenario_s11_01_off_single_task.log
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_off_single_task.rec
0b2831c3afb16ac707e4e34cbca4c237  runs/env_layout_12_scenario_s11_01_on_full_reorder.log
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_on_full_reorder.rec
fe0cf31a57816a542ac658d6d44adc89  runs/env_layout_12_scenario_s11_01_on_single_task.log
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_on_single_task.rec
3ab5271278497f943d21b1dbb18f0944  runs/env_layout_12_scenario_s11_02_off_single_task.log
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_off_single_task.rec
5863e0a7a5dc0d475ea2154f2625d1db  runs/env_layout_12_scenario_s11_02_on_full_reorder.log
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_on_full_reorder.rec
46b21c2b7689e9374e4bf4ee8c07eae0  runs/env_layout_12_scenario_s11_02_on_single_task.log
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_on_single_task.rec
6d9553dd23b762cbdb749f3c92c3b54d  runs/env_layout_12_scenario_s11_03_off_single_task.log
bd84a77d4d232d4657b782614615bccb  runs/env_layout_12_scenario_s11_03_off_single_task.rec
fca0440d9ff3771c7462eb89a7ec7f52  runs/env_layout_12_scenario_s11_03_on_full_reorder.log
bd84a77d4d232d4657b782614615bccb  runs/env_layout_12_scenario_s11_03_on_full_reorder.rec
47ac02c6daaec8eb5a753656a62ce4f2  runs/env_layout_12_scenario_s11_03_on_single_task.log
bd84a77d4d232d4657b782614615bccb  runs/env_layout_12_scenario_s11_03_on_single_task.rec
f2efb30e09e71b9e7cce78f78c387157  runs/env_layout_13_scenario_s10_11_off_single_task.log
955c7b71a51a1cf3d80a3f8ed51931da  runs/env_layout_13_scenario_s10_11_off_single_task.rec
a613705b833c48cc4a909c87a7e8f366  runs/env_layout_13_scenario_s10_11_on_full_reorder.log
955c7b71a51a1cf3d80a3f8ed51931da  runs/env_layout_13_scenario_s10_11_on_full_reorder.rec
fe8e6b2bba3fddcd0bb11538b9cb9dee  runs/env_layout_13_scenario_s10_11_on_single_task.log
955c7b71a51a1cf3d80a3f8ed51931da  runs/env_layout_13_scenario_s10_11_on_single_task.rec
0d6a1949e35ba0da2939d46e5ecb7346  runs/env_layout_14_scenario_s12_01_off_single_task.log
fc4ef52bbf1c640efa64a535a9385f7f  runs/env_layout_14_scenario_s12_01_off_single_task.rec
3f5b2b2d338e8ea0b19947b050a98e77  runs/env_layout_14_scenario_s12_01_on_full_reorder.log
fc4ef52bbf1c640efa64a535a9385f7f  runs/env_layout_14_scenario_s12_01_on_full_reorder.rec
f545130a9d368e47b4587ab87a62b819  runs/env_layout_14_scenario_s12_01_on_single_task.log
fc4ef52bbf1c640efa64a535a9385f7f  runs/env_layout_14_scenario_s12_01_on_single_task.rec
48b645e0a75da9ea23a3eb056182ead6  runs/env_layout_14_scenario_s12_02_off_single_task.log
eeff90b54d1ee23e20d5635de4ce1a07  runs/env_layout_14_scenario_s12_02_off_single_task.rec
35930895c820ee8ba3dc37f57fc0b8cf  runs/env_layout_14_scenario_s12_02_on_full_reorder.log
eeff90b54d1ee23e20d5635de4ce1a07  runs/env_layout_14_scenario_s12_02_on_full_reorder.rec
3aac7d9841678527c0d9997c79127612  runs/env_layout_14_scenario_s12_02_on_single_task.log
eeff90b54d1ee23e20d5635de4ce1a07  runs/env_layout_14_scenario_s12_02_on_single_task.rec
```

## T-K part 1, build stages 6 and 7: the instruments and the final rerun (4 October 2026)

Stage 6 (766f7d3): the oracle is the IRB's with its prior from the declared context knowledge when the run file
states `context_knowledge: true` (the IRB's rules 29 to 33); `actual.py` and `reference.py` build the model with the
domain's declared context knowledge; `actual.py` sets the same `[run_mesa]`, `[sep]` and step-line prefixes aside on
both sides of its identity check (the model logs the `[run_mesa] timeline` line itself since stage 4a, which the
unfiltered in-process side kept; a defect found by the stage's check and repaired). The sixteen rerun at 766f7d3
under both strategies, prior on, and the prior-off appendix, context knowledge off. After setting aside the lines named since the gate stage, every log and `.rec` equals the gate stage's (0 differ):
the `[run]` header's `context_knowledge=off` (stage 3, bbb7227); the line `[run_mesa] timeline source=none windows=[]`
(stage 4a, f70f72f); `switch_on` for `wait_at` where an A/C activation runs (stage 4b, 2393935). The instrument
outputs equal the gate stage's after the three new columns `prior`, `levels`, `recent` (empty with context knowledge
off) and their rows in `diff.md`, `params.recency_ticks` and the A/C's name and effect `ac_on(switch)` in the
trajectory (stage 6, 766f7d3). Parts 1 to 3: 0
disagreements in all 32 prior-on runs; every declared property of part 4 reads as at the gate stage. Runs (git-ignored;
md5s at the rerun):

```
c9d7be5013e2039234be4c5a32c1e63c  runs/env_layout_12_scenario_s10_01_off_single_task.log
8451bf1f7048ec68b33375c2cc99cb15  runs/env_layout_12_scenario_s10_01_off_single_task.rec
a352c990af7c5d1228d132e8501f9a8d  runs/env_layout_12_scenario_s10_01_on_full_reorder.log
8451bf1f7048ec68b33375c2cc99cb15  runs/env_layout_12_scenario_s10_01_on_full_reorder.rec
c54aa36a594111c9e7097549c102ff6c  runs/env_layout_12_scenario_s10_01_on_single_task.log
8451bf1f7048ec68b33375c2cc99cb15  runs/env_layout_12_scenario_s10_01_on_single_task.rec
c4b430377b254e11436e4ebeef38d583  runs/env_layout_12_scenario_s10_02_off_single_task.log
321732473c562c43b06ae158ca81cdef  runs/env_layout_12_scenario_s10_02_off_single_task.rec
216a44afb517e4c83f3dc70a0a6abdf1  runs/env_layout_12_scenario_s10_02_on_full_reorder.log
321732473c562c43b06ae158ca81cdef  runs/env_layout_12_scenario_s10_02_on_full_reorder.rec
eb37f298ff5647426ef5b9dfc45afd11  runs/env_layout_12_scenario_s10_02_on_single_task.log
321732473c562c43b06ae158ca81cdef  runs/env_layout_12_scenario_s10_02_on_single_task.rec
17e3f77d2875eb946d7d649f02b41fd3  runs/env_layout_12_scenario_s10_03_off_single_task.log
7fa9d641f1a0df5af13e70ec188ad19e  runs/env_layout_12_scenario_s10_03_off_single_task.rec
8d44bd7985f65c4778695ee047da01cb  runs/env_layout_12_scenario_s10_03_on_full_reorder.log
7fa9d641f1a0df5af13e70ec188ad19e  runs/env_layout_12_scenario_s10_03_on_full_reorder.rec
dadf8054a097a0502529d29ad9454f28  runs/env_layout_12_scenario_s10_03_on_single_task.log
7fa9d641f1a0df5af13e70ec188ad19e  runs/env_layout_12_scenario_s10_03_on_single_task.rec
297291c89399ae6810b8598b6ac4666f  runs/env_layout_12_scenario_s10_04_off_single_task.log
88dcf2598e25a94807b1e1f981218bff  runs/env_layout_12_scenario_s10_04_off_single_task.rec
aac9cb65ddbec5898304af99d2f52a17  runs/env_layout_12_scenario_s10_04_on_full_reorder.log
88dcf2598e25a94807b1e1f981218bff  runs/env_layout_12_scenario_s10_04_on_full_reorder.rec
6d893a794524e9451dc6c541fe428823  runs/env_layout_12_scenario_s10_04_on_single_task.log
88dcf2598e25a94807b1e1f981218bff  runs/env_layout_12_scenario_s10_04_on_single_task.rec
6b1ec1c861ad9429ec423c9dfd2593be  runs/env_layout_12_scenario_s10_05_off_single_task.log
c0b3c52826984a71c0637d8dfc8eba55  runs/env_layout_12_scenario_s10_05_off_single_task.rec
c97cde510fbdeb6601f52520d6d50099  runs/env_layout_12_scenario_s10_05_on_full_reorder.log
c0b3c52826984a71c0637d8dfc8eba55  runs/env_layout_12_scenario_s10_05_on_full_reorder.rec
e1d8bbec173237a7c17e7463d58d7497  runs/env_layout_12_scenario_s10_05_on_single_task.log
c0b3c52826984a71c0637d8dfc8eba55  runs/env_layout_12_scenario_s10_05_on_single_task.rec
583ea224184f9b14e9d54d4b24a228f3  runs/env_layout_12_scenario_s10_06_off_single_task.log
4bdc76ccc6f1ee3244e89c5458b19ffe  runs/env_layout_12_scenario_s10_06_off_single_task.rec
511e12598a7ec5ed1c566d5f4ffaf9d3  runs/env_layout_12_scenario_s10_06_on_full_reorder.log
4bdc76ccc6f1ee3244e89c5458b19ffe  runs/env_layout_12_scenario_s10_06_on_full_reorder.rec
7f56d7822aab68a68c095a6feab6e1b0  runs/env_layout_12_scenario_s10_06_on_single_task.log
4bdc76ccc6f1ee3244e89c5458b19ffe  runs/env_layout_12_scenario_s10_06_on_single_task.rec
b1688e5b1e90922befee268a85468ad9  runs/env_layout_12_scenario_s10_06_reference_full_reorder.log
d4d0b0ba276092faccb54dbfe59f5305  runs/env_layout_12_scenario_s10_06_reference_single_task.log
41057c933ce04f1e85b9cacc66bb9279  runs/env_layout_12_scenario_s10_07_off_single_task.log
9f6bde960f345934b2423236f91fa158  runs/env_layout_12_scenario_s10_07_off_single_task.rec
8dc7f09a96cf171887dc8d7621293b2f  runs/env_layout_12_scenario_s10_07_on_full_reorder.log
9f6bde960f345934b2423236f91fa158  runs/env_layout_12_scenario_s10_07_on_full_reorder.rec
40aefe7e7122a0fb8f3aee2deae69d20  runs/env_layout_12_scenario_s10_07_on_single_task.log
9f6bde960f345934b2423236f91fa158  runs/env_layout_12_scenario_s10_07_on_single_task.rec
93044f44565ea074dfb6a79b098cadc1  runs/env_layout_12_scenario_s10_08_off_single_task.log
33ee73bcf6ffefa2c81b3607397ac879  runs/env_layout_12_scenario_s10_08_off_single_task.rec
e410c230088fbf64a6eecae2d5cc837d  runs/env_layout_12_scenario_s10_08_on_full_reorder.log
33ee73bcf6ffefa2c81b3607397ac879  runs/env_layout_12_scenario_s10_08_on_full_reorder.rec
d00075875d4ec94091bcc614c4ec7811  runs/env_layout_12_scenario_s10_08_on_single_task.log
33ee73bcf6ffefa2c81b3607397ac879  runs/env_layout_12_scenario_s10_08_on_single_task.rec
6b1545b3ace884b069a3b79e3be997ef  runs/env_layout_12_scenario_s10_09_off_single_task.log
ebcb27b9f5dbf9cfcfa67e4b25a2ba3a  runs/env_layout_12_scenario_s10_09_off_single_task.rec
7261c7ba201b99cba53f2d5cf2c66db8  runs/env_layout_12_scenario_s10_09_on_full_reorder.log
ebcb27b9f5dbf9cfcfa67e4b25a2ba3a  runs/env_layout_12_scenario_s10_09_on_full_reorder.rec
411bf2ae7763153297f3da21650c9910  runs/env_layout_12_scenario_s10_09_on_single_task.log
ebcb27b9f5dbf9cfcfa67e4b25a2ba3a  runs/env_layout_12_scenario_s10_09_on_single_task.rec
2067a29377048948fdc1c89589773046  runs/env_layout_12_scenario_s10_10_off_single_task.log
4251537079b3d12ed72aa11e6771f5e0  runs/env_layout_12_scenario_s10_10_off_single_task.rec
51bcb2bf5a8ed9375e3623ed3bf02917  runs/env_layout_12_scenario_s10_10_on_full_reorder.log
4251537079b3d12ed72aa11e6771f5e0  runs/env_layout_12_scenario_s10_10_on_full_reorder.rec
a0c6c5c33bc4e52a89d75d3c8bf26009  runs/env_layout_12_scenario_s10_10_on_single_task.log
4251537079b3d12ed72aa11e6771f5e0  runs/env_layout_12_scenario_s10_10_on_single_task.rec
d2a59e9cb279122ff6b26f2138d76c60  runs/env_layout_12_scenario_s11_01_off_single_task.log
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_off_single_task.rec
46faae8f298d80c5817d26cb0a17bec5  runs/env_layout_12_scenario_s11_01_on_full_reorder.log
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_on_full_reorder.rec
8c4ef95e7edae4821e0f237dcd2921af  runs/env_layout_12_scenario_s11_01_on_single_task.log
2b20839311f61f384b627483ddebc626  runs/env_layout_12_scenario_s11_01_on_single_task.rec
762773647e8c54b71698a77ef6bde860  runs/env_layout_12_scenario_s11_02_off_single_task.log
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_off_single_task.rec
673a4b12c44a01663afc88961af6488c  runs/env_layout_12_scenario_s11_02_on_full_reorder.log
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_on_full_reorder.rec
8d6e31e6ab608aff9cd34f42b0a93a7a  runs/env_layout_12_scenario_s11_02_on_single_task.log
86397e984d81ec47aa978760989c152f  runs/env_layout_12_scenario_s11_02_on_single_task.rec
b21fa8d6cf782513e3ff31100afccea6  runs/env_layout_12_scenario_s11_03_off_single_task.log
bd84a77d4d232d4657b782614615bccb  runs/env_layout_12_scenario_s11_03_off_single_task.rec
087566bdcfa7192319810f1b256bcf14  runs/env_layout_12_scenario_s11_03_on_full_reorder.log
bd84a77d4d232d4657b782614615bccb  runs/env_layout_12_scenario_s11_03_on_full_reorder.rec
c22e65faed8786f8be8da556f5158a1e  runs/env_layout_12_scenario_s11_03_on_single_task.log
bd84a77d4d232d4657b782614615bccb  runs/env_layout_12_scenario_s11_03_on_single_task.rec
33472e8caddcb2c12dd5f7d0234826ec  runs/env_layout_13_scenario_s10_11_off_single_task.log
955c7b71a51a1cf3d80a3f8ed51931da  runs/env_layout_13_scenario_s10_11_off_single_task.rec
4901efbc5cbafb6bce46b42614fec729  runs/env_layout_13_scenario_s10_11_on_full_reorder.log
955c7b71a51a1cf3d80a3f8ed51931da  runs/env_layout_13_scenario_s10_11_on_full_reorder.rec
2be3b85ec338a8b8762329ec7a213a81  runs/env_layout_13_scenario_s10_11_on_single_task.log
955c7b71a51a1cf3d80a3f8ed51931da  runs/env_layout_13_scenario_s10_11_on_single_task.rec
279a83b7e86c5dd22116a7e0884ba4e4  runs/env_layout_14_scenario_s12_01_off_single_task.log
fc4ef52bbf1c640efa64a535a9385f7f  runs/env_layout_14_scenario_s12_01_off_single_task.rec
99d8f73318ba0e188961d22e25c94ad9  runs/env_layout_14_scenario_s12_01_on_full_reorder.log
fc4ef52bbf1c640efa64a535a9385f7f  runs/env_layout_14_scenario_s12_01_on_full_reorder.rec
000f08e7173fc7144d13f34fb1cb2238  runs/env_layout_14_scenario_s12_01_on_single_task.log
fc4ef52bbf1c640efa64a535a9385f7f  runs/env_layout_14_scenario_s12_01_on_single_task.rec
64e247055bdca8e85bd85d39c3583918  runs/env_layout_14_scenario_s12_02_off_single_task.log
eeff90b54d1ee23e20d5635de4ce1a07  runs/env_layout_14_scenario_s12_02_off_single_task.rec
bcefb087274ba0d0921d039713afb1e4  runs/env_layout_14_scenario_s12_02_on_full_reorder.log
eeff90b54d1ee23e20d5635de4ce1a07  runs/env_layout_14_scenario_s12_02_on_full_reorder.rec
1a46377dbada34377b4110101c42e0e7  runs/env_layout_14_scenario_s12_02_on_single_task.log
eeff90b54d1ee23e20d5635de4ce1a07  runs/env_layout_14_scenario_s12_02_on_single_task.rec
```

