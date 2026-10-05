# TeamRob handoff: T-F part 1 (the conditions human-unaware and intention-unaware), closed; T-F part 2 parked

Written 5 October 2026 by ccode at T-F part 1's close (design_records.md, "T-F part 1: the conditions human-unaware and
intention-unaware", THE CLOSE). Everything named here is committed on `main`; Hadi pushes. Nothing is open in ccode.

## 0. How to use this document

- The repo is authoritative over this document. A session that takes up T-F part 2 verifies sections 1 to 3 from the
  repo first and reports every disagreement to Hadi.
- Every item is marked:
  - **[ruling]** a recorded ruling of Hadi, with its place in the records;
  - **[finding]** a measured result, recorded, not ruled;
  - **[suggestion]** ccode's proposal; not a ruling, and not an order of work.
- This file states no order of work that Hadi has not confirmed. The only confirmed order: T-F part 2 is parked; Hadi's
  next chat is T-G's next stage with T-K part 1's steps on dock_loading.
- The records of T-F part 1: design_decisions.md, the entry "T-F part 1: the conditions human-unaware and
  intention-unaware" (R2, R4, R5's premise, R6, R7; A, B, C, E, F's Q4); design_records.md, the heading of that title
  (R1, R3, R5's form, R8 to R10; D, F's Q3, G; H to J; K to O; the stages; THE CLOSE); glossary §9; the plan
  docs/handoffs/plan_T-F_part1.md.

## 1. The two run options and how a run states a condition

- **[ruling]** Two run options, `human_aware` and `intention_aware`, both on by default (R3). A run states them in its run
  file (`human_aware: false`, `intention_aware: false`) or on the command line (`--human_aware false`,
  `--intention_aware false`). The three conditions of the robot (glossary §9):
  - human-unaware (`human_aware` off): the robot is given no observed human (D); it plans and moves as if the room were
    empty; the human is in the world and moves.
  - intention-unaware (`intention_aware` off): the robot observes the human's position and motion; the recognizer
    computes nothing (A); the gate refuses with `none(intention_off)` for both its callers (R6); every decision rests on
    the fallback projection, or on none before a first observation.
  - intention-aware (both on): the framework as designed; assignment knowledge and context knowledge are its own
    options.
- **[ruling]** The override (R5): an option that is off sets every option above it to off, whatever the default, the run
  file or the command states. `human_aware` off sets `intention_aware`, `assignment_knowledge`, `context_knowledge` and
  the separation stop off; `intention_aware` off sets both knowledge options off. Applied in one place,
  `SimModel.__init__` (mesa_sim/sim_model.py), which the headless run, the viewer and every instrument reach. The run
  prints `[run_mesa] options <option>=off sets off: ...` and the `[run]` header prints the effective values. Nothing
  stops at load.
- **[ruling]** Admission asks `none(no_human)` before the gate in every run (E); no `[coverage]` or `[scenario-coverage]`
  lines when the recognizer does not run (F).
- **[ruling]** `--cost_strategy plain` is untouched and is not a column of the measurement (R8).

## 2. The instruments as they are now

- **The runner of a set whose settings live in its run files** (`analysis/instruments/mpb/run_set.sh <domain> -o
  <out_root> <run files>`) **[ruling: I, K]**: no setting on the command line; a run is named by its run file (a
  serial); its outputs in `<out_root>/<scenario>/<run>/`, its log and `.rec` inside (`<run>.log`). Per run: the step cap
  (the domain's horizon.py), the run, the human's replay, the in-process actual (`actual.py`), the settings and the
  condition (`conditions.py`, `settings.json`), the robot-alone reference run for human-unaware, the oracle and the
  comparison where a table is derivable (R9 as amended by A: intention-unaware, the decisions and the fallback
  projections; human-unaware, `none(no_human)`, hold 0 and the positions against the reference run), the measures with
  no declared property (`measures.py`, M), the figure, the separation counts. Last, the result table.
- **The result table** (`analysis/instruments/mpb/table.py <out_root>`) **[ruling: I]**: `results.csv` and `results.md`,
  one row per run, the effective settings as columns (`human_aware`, `intention_aware`, `assignment_knowledge`,
  `context_knowledge`, `strategy`, from the `[run]` header; `settings_agree` with R5's reading), then completion
  (`unfinished` when the run has no terminal decision within its cap, since 9a710df), terminal, decisions, held
  ticks, the ticks below min_separation and F1's classes (viol, recede, stand_passing, stand_beside), the continuous
  `[sep]` minimum, the oracle's check, objects_separate, the reference.
- **The runner of the maintained test-bed outputs** (`analysis/instruments/mpb/run.sh`, `analysis/instruments/irb/run.sh`):
  unchanged in names and folders (`<scenario>/<prior>_<strategy>/` for the MPB); `run.sh` of the MPB still evaluates the
  declared properties. **[suggestion]** They take K's names on their next run (part E's table: "maintained").
- **The figure** **[ruling: the standing rule on figures; N]**: one file per run, `figure.png`, every panel on one tick
  axis: the belief over H, the context panel (context knowledge on), S, the finding, the warrant per hypothesis and the
  gate's answer per tick (one row per answer), the decision panel (with the oracle's expected decisions), the
  robot–human distance on 0 to 4 × min_separation with the ticks below it shaded by F1's class. Built by
  `analysis/instruments/irb/plot.py` (`draw`); the planning runs through `analysis/instruments/mpb/plot.py`; a run made
  by run_mesa.py directly through `analysis/instruments/mpb/figure_of_log.py <log> <png>` (the four maintained sets'
  sweep.sh call it). The context panel stands under the belief, not after the finding as N lists it (ccode's flag).
- **The measurement's tools** (analysis/kitting/tf1/): `make_runs.py` (wrote the 688 run files; its sources were deleted
  in part E, held by 362af19), `tables.py` (REPORT.md's tables), `comparison.py` (COMPARISON.md and comparison.html).

## 3. The measurement's result

- **[finding]** 128 kitting scenarios (the planning test-bed's 16, step 5's 6, step 5e's 106 with no timeline fact; 10
  rooms) in the four conditions, and step 5e's 176 timeline copies intention-aware with context knowledge on: 688 runs,
  `single_task`. The oracle compared on all 688: 0 disagreements. Every human-unaware run moves as the robot alone.
- **[finding]** Step 1, planning against the observed human (human-unaware → intention-unaware): violation ticks
  137 → 14; completion later in 36 of 127 scenarios, equal in 91, earlier in none; mean +5.83 ticks; 741 ticks of
  delay for 117 violation ticks removed.
- **[finding]** Step 2, recognition (intention-unaware → intention-aware, context knowledge off): completion 15 earlier,
  101 equal, 11 later, mean −0.84; violation ticks 14 → 17. Step 3, context knowledge (off → on): completion 8 earlier,
  112 equal, 7 later, mean −0.28; violation ticks 17 → 23. For both steps the 95% interval of the mean change, resampling
  the rooms, includes zero: no difference this set can distinguish from zero.
- Documents: analysis/kitting/tf1/REPORT.md (the working record, per-scenario tables, findings 1 to 7);
  analysis/kitting/tf1/COMPARISON.md and comparison.html (for a reader outside the repository; accepted by Hadi).

## 4. The findings (none ruled)

- **[finding]** A stand at the robot's target that does not end (TODO-184). scenario_s02_02: the script ends with the
  human delivering at kitting_table_0, the robot's remaining target, and no exit walk (docs/assumptions.md 1.1); from
  tick 250 the human stands there. The three conditions that observe the human hold on lengthening fallback projections
  (up to 256 ticks at 502, intention-unaware; 384 at 630, intention-aware) and do not finish within 704 ticks;
  human-unaware completes at 422. The same in the copies scenario_s17_08 and s17_10. Open: what the robot does when the
  stand does not end (X1 set aside a give-up threshold; X5 communication).
- **[finding]** An admission at tick 0 with context knowledge on, of a task the human is not doing: scenario_s05_01 and
  s05_02 (the human's first task coffee_break, no timeline fact in force, deliver_item(item_5) at about 0.97; admitted at
  0, violations at 27 to 29, minimum 30.0 cm); the same form in scenario_s16_01 (admission at 0, violations 49 and 50)
  and s16_02 (admission at 38, violations 48 and 49). With context knowledge off those ticks rest on fallback decisions.
- **[finding]** Violations in the intention-aware runs where intention-unaware has none, in two forms (REPORT.md,
  finding 4): the tick a two-tick fallback ends after a refused `recognition_changed` (scenario_s03_06 and s21_07 at 57,
  s20_26 at 99, s22_24 at 136); and long after a decision on an admitted projection with no trigger in between
  (scenario_s24_14 at 268 and 269, decision at 191; s26_48 at 180 and 184, decision at 72).
- **[finding]** The robot that holds is passed by the human: most ticks below min_separation in the intention-unaware and
  intention-aware runs are a standing robot's. Step 1 adds ticks below min_separation in 9 scenarios; in each of the 9 it
  adds ticks of a standing robot and removes violation ticks.

## 5. Parked notes for T-F part 2

- **[ruling]** `full_reorder` becomes the default strategy of the actual evaluation's runs (J; design_records.md, "T-F
  part 1", H TO J): under it an early admission can change the next task and the whole remaining order.
- **[ruling]** Strategy is a second dimension of the same result table (J); the human-unaware condition needs its own
  reference run per strategy; TODO-141 applies.
- **[ruling]** No setting in a file or folder name; the settings are columns of the result table (I, K).
- **[suggestion]** Scenarios in which the admitted task changes the robot's choice (the next task or the order), so that
  recognition has a decision to change; in this set step 2 changed completion in 26 of 127 scenarios.
- **[suggestion]** For a paper: randomly generated scenarios (TODO-47's harness) and `full_reorder`; a human who reacts to
  the robot, or variation in the human's speed and timing; a mixed-effects model with room and script as random effects
  in place of the room bootstrap, with effect sizes and intervals; a definition of "interacting" independent of the
  human-unaware run; recognition quality per run (time to the correct admission, wrong admissions) linked to the
  outcomes; the outcomes by kind of human behaviour.
- **[suggestion]** Whether `--cost_strategy plain` is kept (R8 left its removal to a cleanup ruled with T-F).
- **[suggestion]** Whether the four maintained sets are still needed beside the test-beds (tb1a, tb1b, tb1c, tb3; logs
  only, regenerated on every behaviour change).
- **[ruling]** The recognition sets of steps 4 to 5b (analysis/kitting/irb/tk1, tk2, tk5b, with their run files) stay
  until T-F part 2 (O as narrowed). **[suggestion]** Decide at part 2 whether they are rerun under its runner or deleted.

## 6. Open TODOs this work touched (verify the numbers in the repo)

- TODO-137 closed (built and measured). TODO-144 (the evaluation's framing): part 1's result recorded, part 2 parked.
- TODO-181 (an execution-time avoidance that acts in a human-unaware run) and TODO-182 (human-unaware with the observed
  human kept): open, future work.
- TODO-183 (may a domain forbid a run condition?): forwarded to T-G's next stage.
- TODO-184 (a stand at the robot's target that does not end): recorded, open.

## 7. Provenance

Repo facts verified by ccode at the commit that adds this file. The commits of T-F part 1: the rulings and plan
df01ae9, 9509ada, adaa9ca, 6cc69fb; stage 1 f269b6a, 2f3d61b, a34ccde; stage 2 f320f99, ca8a4aa, a84977d, 07ae835,
02f18ff; the measurement f849db9, edae0e4, 3d7a26a, 8da7b2a, 26ca369, efb16fe, 54e3d75, 7c8b841, 9a710df; the
statistics report 362af19; the close a63e11b, 02c8e5c, 92314fa. Outside the repository: /home/hadi/teamrob_tf1_handoff/
(the backup of the reran sets' outputs before the reruns, o_sets_before.tgz; everything part E deleted,
deleted_2026-10-05_part_E.tgz; the inventory of part E).
