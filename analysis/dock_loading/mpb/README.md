# The MPB on dock_loading (T-G stage 1)

The data and figures of this set (.json, .csv, .png) are not in git (Hadi, 2 October 2026). They are regenerated
by the set's run script (`analysis/instruments/mpb/run.sh dock_loading`). A byte comparison uses the local copy or the outside copy,
`/home/hadi/teamrob_analysis_2026-10-02/` (the whole of analysis/ as it was at 38d66ea).

The recognition-to-planning chain with a working robot in the second domain, with nothing domain-specific in `shared/`
(design_decisions.md, "T-G: the second domain's rulings", THE MPB ON DOCK_LOADING: MPB-DL1 to MPB-DL7, DISPOSITIONS,
THE SET, RULED ON THE SET, THE BUILD'S PLAN CONFIRMED with DL-P1 to DL-P9). A test and an analysis: it changes nothing
in the framework. Kitting's MPB rules carry over ("The meta-planner test-bed (MPB)", MPB-1 to MPB-6): the oracle, the
compare levels, the five disagreement classes and the three readings of class 2.

- The artefacts and the derivations of every authored value: `authoring.md`.
- K8's per-tick table at the cut, written before its runs (DL-P1): `predictions.md`.
- The results: `REPORT.md`.

The scope of stage 1 (Hadi, 2 October 2026; THE MPB ON DOCK_LOADING, the closing record): the MPB establishes that the
recognizer and the recognition-to-planning chain run on dock_loading and produce runs, logs and figures, compared with
the oracle; the behavioural analysis is stage 2's. The alteration test on dock_loading (`alteration.py`) is built and
not run in stage 1.

## The instrument

The shared code is `analysis/instruments/mpb/` (kitting's README, `analysis/kitting/mpb/README.md`, states the pipeline,
the oracle's rules M0 to M7 and C1 to C6 with their sources, and the compare levels). dock_loading's own parts, here:
- `horizon.py`: the step cap (MPB-5; DL-P7 for a script that depends on the robot; DL-P8 bounds its use of the
  planner's decomposition). No module of the oracle imports it.
- `properties.py`: the declared properties (K1; M1, M2, M4) and the reported measures (K3's switch, K4's holds, K9's
  admission and retraction, M2's two occurrences), on the shared `measures.py`; `CONTROLS`, K1's two scenarios, whose
  comparison run (`reference.py`: the human removed) `run.sh` makes.
- `alteration.py`: the alteration test, the shared rules with dock_loading's B1 and E1 to E3.
- `disjoint.py`: the disjointness check (MPB-DL7) per controlled scenario and for M3.

The run files: `configs/dock_loading/mpb/`, prior on, `single_task` (`--strategy full_reorder` for the second run).

```bash
bash analysis/instruments/mpb/run.sh dock_loading configs/dock_loading/mpb/scenario_s0{8,9}_0{1..9}.yaml
bash analysis/instruments/mpb/run.sh dock_loading --strategy full_reorder configs/dock_loading/mpb/scenario_s0{8,9}_0{1..9}.yaml
bash analysis/instruments/mpb/run.sh dock_loading [--strategy full_reorder] configs/dock_loading/mpb/scenario_s0{5,7}_0{4,5,6}.yaml configs/dock_loading/mpb/scenario_s0{8,9}_10.yaml
```

Outputs per scenario in `<scenario>/on_<strategy>/` (kitting's files; `separation.md`, the separation counts: a moving
robot violating or receding, a standing robot with the human passing or beside it). The logs and `.rec` streams in
`runs/` (git-ignored; md5s in REPORT.md).

## The expectations before the runs

`run.sh dock_loading --expect` writes, for each scenario, the trajectory (the executor's own selection rule) and the oracle's per-tick
table (`trajectory.json`, `expected_ticks.json`) from the scenario's run file, with no run: θ is the value of record
(0.75; the run's own oracle call reads it from the run's [run] header and must reproduce the committed table byte for
byte). The chain is assembled only at the compare step, from the table and the run's observed `no_current_task` ticks
(MPB-1, C1 to C6).
