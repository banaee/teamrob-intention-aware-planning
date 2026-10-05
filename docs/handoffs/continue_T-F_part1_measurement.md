# Continuation note: T-F part 1, the measurement (ccode, 5 October 2026)

RESOLVED (the same session resumed, 5 October 2026): the three remaining steps are done; the record is
design_records.md, "T-F part 1", THE MEASUREMENT, RULINGS K TO O. This note stays as written below.

Written at a safe stop, in case the session cannot resume. Nothing is running; nothing was deleted; no file is
half-edited. The step's prompt: "STEP: the measurement of T-F part 1" (parts A to E, rulings K to O), with Hadi's three
later changes below.

## Done, with commits

- f849db9 Instruments, part A: one figure per run on one tick axis (N), `analysis/instruments/irb/plot.py` `draw` the
  builder, `mpb/plot.py` the planning runs' figure (figure_ir.png no longer drawn; `plot_ir.py` keeps the rows helper),
  `mpb/decision_panel.py` (the oracle's expected decisions, the key under the figure), `mpb/figure_of_log.py` (the
  figure of a run made by run_mesa.py directly); `run_set.sh` and `table.py` name a run's folder
  `<out_root>/<scenario>/<run>/`, the log inside (K).
- edae0e4 The four maintained sets' sweep.sh draw each run's figure beside its log (the milestone sweep added here was
  withdrawn in 8da7b2a).
- 3d7a26a The 688 run files, `configs/kitting/tf1/measurement/<scenario>/run_NNN.yaml`, written by
  `analysis/kitting/tf1/make_runs.py` (L, K).
- 8da7b2a dock_loading's milestone sweep withdrawn (O corrected).
- 26ca369 The four maintained sets regenerated with their figures (O): 48 `.rec` byte-identical, every log identical
  except ` human_aware=on intention_aware=on` in `[run]`; new md5 sections in their READMEs; logs and figures copied into
  `analysis/kitting/tb*/sweep/`.
- efb16fe The measurement (B, D): 688 runs, the oracle compared on all 688, 0 disagreements, settings agree with R5 in
  all, the 128 human-unaware rows equal the robot-alone reference; `analysis/kitting/tf1/REPORT.md` (tables per set and
  condition, the pair counts, findings 1 to 7, four example figures: scenario_s05_01 run_105 to _108),
  `analysis/kitting/tf1/tables.py`, `analysis/kitting/tf1/measurement/results.md`. A correction of ccode's own: the
  result table's `completion` is the tick after the last release even when the pool did not complete;
  `tables.py` counts completion only with a terminal decision (five runs do not complete: scenario_s02_02 in IU, IA-off,
  IA-on, and its copies s17_08, s17_10).

## The three remaining steps (as listed at the stop)

1. Rerun the three O jobs I stopped (tk1, tk2, and the MPB set with assignment knowledge off). Compare the kitting
   test-bed outputs that are already in the scratchpad with those on disk. Copy them in only where nothing beyond the
   named lines differs.
2. Record rulings K to O in `design_records.md`, plus a status line in CLAUDE.md.
3. The final report: verification, flags, part E's table (the inventory is already collected), and the list of 881
   tracked per-run files with a proposed untrack step.

Detail for step 1: the O jobs are the lines of `ojobs.txt` (copy below), each run by `ojob.sh <k>` in its own copy of
HEAD (`git archive HEAD | tar -x`; the runners pick the newest `logs/run_*.log`, so one copy per job). Done and
complete: job 1 (kitting IRB s08/s09, 17), job 4 (irb/tk5b), job 5 (MPB single_task), job 6 (MPB full_reorder).
Stopped, to rerun whole: job 2 (irb/tk1), job 3 (irb/tk2 and tk2/off), job 7 (MPB `--prior off`). Compare with
`compare_o.py <new_root> <old_root> [skip subdirs]` (logs compared with the two `[run]` fields removed; figures not
compared): `kitting_irb` against `analysis/kitting/irb`, `kitting_mpb` against `analysis/kitting/mpb` (skip `tk`,
`tk5b`). Not rerun, by Hadi's changes: step 5e's recognition runs, dock_loading's IRB, MPB and milestone runs. Old
`figure_ir*.png` / `figure_N.png` left beside the new `figure.png` go on part E's list, not deleted. `ojob.sh` and
`ojobs.txt` name the old scratchpad path; rewrite the paths before reuse.

## Rulings K to O (Hadi, 5 October 2026), not yet recorded

- K. Names: one folder per scenario, named by the scenario id; inside it the runs of the conditions by serial; no
  setting in any file or folder name. Supersedes naming every run by serial alone. Why: the scenario is what a run is
  about; the runs of one scenario lie side by side, and a reader finds a figure without opening the table.
- L. The scenarios: the planning test-bed's 16, step 5's 6 planning cases and step 5e's 106 planning scenarios in the
  form with no timeline fact, 128 in all four conditions (512 runs); step 5e's 176 copies with timeline facts,
  intention-aware with context knowledge on only; 688 in total. Why: the four conditions must run identical
  scenarios; a timeline acts only through context knowledge.
- M. Declared properties are not checked in the measurement; the oracle check runs on every row where it applies.
  Why: they were written for one condition; the planning test-bed keeps checking them in its maintained outputs.
- N. The figure: one file per run, every panel on one shared tick axis: belief; S; adequacy finding; context panel
  (context knowledge on); observation warrant and the gate's answer per tick with its refusal reason; decision panel;
  robot–human distance, readable near min_separation. A human-unaware or intention-unaware run keeps the panels that
  apply. Why: the reader lines up belief, gate, decision and distance on one tick by eye; the ticks below
  min_separation are the measure, and a scale of 0 to 1600 cm hides them.
- O. Figures for the sets the measurement does not run: run them once more; every other output identical to the
  existing one, any that is not reported. Why: the standing rule on figures should hold for what exists now.

Hadi's later changes, the same session, also not yet recorded:
- O narrowed: of the recognition runs of steps 4 to 5e, only those of steps 4 to 5b (irb/tk1, tk2, tk5b) are rerun;
  they stay as sets until T-F part 2. Step 5e's recognition runs are not rerun (Hadi intends to delete them).
- O corrected: dock_loading's two test-beds and its milestone runs are not rerun; the records hold them stale since
  the gate rulings, until dock_loading's own step, which brings their figures.
- E widened: the table covers every folder under analysis/ and the run files under configs/; per folder what it is,
  whether a record cites it (present path or the path before the sort of 1 October), and a judgement: maintained (takes
  K's names on its next run), replaced (runs deleted, report kept), old record (data deleted, reports and scripts
  kept), or keep. Hadi's intentions: step 5e, steps 5 and 5b's planning runs, stage 2's check and their run files are
  replaced; the old frozen analyses lose their data. One line on the tracked per-run detail files (.gitignore names
  them) and a proposed untrack step. Why: analysis/ holds about 18,000 files and 2.5 GB, step 5e alone 12,001 and 1.7 GB.
- E, the frozen analyses under analysis/kitting (td_stage1, td_stage1b, l_build, irb2b_exposed_interval,
  ablation_task_committed, f47_fixtures, t1_conflict_measurement, todo90_b2a_window, tc2c_scripts, tb1d_designations,
  tb2c_per_entry_holds, big_picture): Hadi intends to delete each folder completely, as on 4 October (one note in
  analysis/README.md naming the last commit that holds them; the records' citations stay). The table says for each
  whether anything in it is still used; such a folder is not deleted. ccode's check (grep of code, tests, configs and
  the maintained sets): nothing in any of the twelve is imported or read; every hit is a comment or a citation.
- Nothing is deleted or untracked before Hadi rules on the table.

## Flags so far (for the final report)

- L: step 5's six include three timeline copies (scenario_s16_02, _04, _06); L runs them in all four conditions, against
  L's own reason. Run as ruled; they equal their bases in HU, IU and IA-off (a check, REPORT.md).
- N: the context panel is drawn directly under the belief (the earlier figures ruling's place), not after the finding
  as N's list orders it.
- E: deleting the recognition runs' run files (Hadi's intention) leaves their outputs with no way to rerun them.
- The verification (VERIFY FIRST) found the code as recorded: the override in `SimModel.__init__`
  (mesa_sim/sim_model.py), reached by the headless run, the viewer (both through `resolve_model_params`) and every
  instrument; `_clears_gate` returns `none(intention_off)` first, and both callers (`evaluate_triggers`' entering
  side, `update_human_projection`) refuse; the recognizer is not called with `intention_aware` off (`RobotAgent.step`,
  `observe_initial`), nor with `human_aware` off (no observed human); intention-unaware still perceives the human's
  position and motion (`_perceive`) and the world state, the meta-planner getting the dummy belief.

## Where things lie (outside /tmp, survives a restart): `~/teamrob_tf1_handoff/`

- `kitting_irb/`, `kitting_mpb/`: O's rerun outputs of the kitting test-beds (jobs 1, 4, 5, 6 complete; tk1, tk2 and
  the `off_single_task` folders partial, to be redone).
- `o_maintained/`: the regenerated maintained sets (already copied into analysis/).
- `o_sets_before.tgz`: the backup of every O set's outputs before any rerun (analysis/kitting/irb, tk5e/irb, mpb,
  dock_loading, the four maintained sets).
- `inventory.tsv` (per folder of analysis/ and configs/: files, size, tracked count, citations by present and old
  path) and `inventory.py`; `tracked_ignored.txt` (the 881 tracked files .gitignore names: separation.md 303, diff.md
  275, summary.md 178, properties.md 125; in analysis/kitting/irb, kitting/mpb, dock_loading/irb, dock_loading/mpb;
  proposed untrack: `git rm --cached` on that list, one commit, the files staying on disk).
- `compare_o.py`, `ojobs.txt`, `ojob.sh`, `oc_logs/` (each job's output).
