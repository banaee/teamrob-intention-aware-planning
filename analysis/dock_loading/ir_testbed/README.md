# The IR test-bed on dock_loading (T-G stage 1)

The recognizer in isolation on dock_loading, against expectations derived from the records before the runs
(design_decisions.md, "T-G: the second domain's rulings", T-G Q16's block: the set and its rules; "The IR test-bed").
The instrument is the shared one, `analysis/instruments/ir_testbed/` (its README: rules 24 to 27 and the human's
sequence from the executor's own selection rule); its rules 1 to 23 are stated in `analysis/kitting/ir_testbed/README.md`.

## The artefacts

- The rooms of B14: env_layout_02, env_layout_03, env_layout_04, each with its IR setup (kind 1): env_setup_02,
  env_setup_04, env_setup_06 (pallet_0 and pallet_1 in the dry bay, pallet_2 and pallet_3 in the frozen bay, pallet_4
  in the truck, each designated to its bay; pallet_4 to the dry bay).
- The scenarios, literals in `domains/dock_loading/scenarios/scenarios_s02.py`, `_s04.py`, `_s06.py`: `_02` to `_15` the
  controlled rows C1 to C14, `_16` to `_19` the mixed rows M1 to M4 (ids after the viewing fixtures `_01`). The robot
  idle on the gate's centre point (0, -300) with no task; the human starting at the standby place (0, 0); prior on;
  the closing part `go_to("desk")` (B13). Each scenario's description states its row, its purpose and its unmodelled
  behaviour.
- Authoring values, approved by Hadi (1 October 2026): a cut or a drop during a walk at PT28S (14 ticks; kitting's
  mid-action cut, scenario_s09_13); the stand at the bay just scanned, `stand("PT80S")` (40 ticks; kitting's long stand,
  scenario_s09_06); M3 scans pallet_2 after the stand (the set's scan 1 has no walk after a stand at the same bay); C13,
  C14 and M4 declared dependent on the robot: the scan of pallet_4 never becomes applicable, the priority list is never
  finished and the walk to the desk is not taken (intended), the record states the entries still open at the run's end.
- `office_break` lasts 90 seconds (45 ticks), `coffee_break` 60 (30).
- Run files: `configs/dock_loading/ir_testbed/scenario_sNN_MM.yaml`: prior on, single_task, gate none, cost realized,
  separation stop off, test level 0.05; steps by TB.3b's rule, the last acknowledgement of the human's sequence + 1 + 30.

## The order (the set's rules)

1. The expectations before any run: `run.sh dock_loading --expect` writes each scenario's `trajectory.json`,
   `expected.csv` and `phases.json` (θ = 0.75, the value of record); committed with `predictions.md` (the diagnostic rows
   C13, C14, M4: the present model's expectation and the predictions under H1 and H2) before any run of the set.
2. The controlled runs (C1 to C14, 42 runs), compared and reported (`REPORT.md`, "Controlled"); the run's own oracle
   call reproduces the committed expectations (θ from the run's [run] header).
3. The mixed runs (M1 to M4, 12 runs), after Hadi's reading of the controlled ones; read only against them.

```bash
analysis/instruments/ir_testbed/run.sh dock_loading --expect                 # the expectations, no run
analysis/instruments/ir_testbed/run.sh dock_loading configs/dock_loading/ir_testbed/scenario_s0{2,4,6}_{02..15}.yaml
```

## The scenarios: the human's actions and the run length

The human's actions per entry (`|` between entries, `‖` a suspension or resumption; mv = move_to; the trajectory's
action table in each `trajectory.json`), and per room the last acknowledgement tick and the run's steps.

| row | MM | env_layout_02 (s02) | env_layout_03 (s04) | env_layout_04 (s06) | actions (env_layout_02) |
|---|---|---|---|---|---|
| C1 | 02 | 108 / 139 | 100 / 131 | 80 / 111 | mv, scan_it, mv, scan_it, mv |
| C2 | 03 | 129 / 160 | 127 / 158 | 83 / 114 | mv, scan_it, mv, scan_it, mv |
| C3 | 04 | 78 / 109 | 78 / 109 | 57 / 88 | mv, scan_it, mv, scan_it, mv |
| C4 | 05 | 214 / 245 | 208 / 239 | 118 / 149 | mv, scan_it, mv, scan_it, mv, scan_it, mv, scan_it, mv |
| C5 | 06 | 147 / 178 | 147 / 178 | 127 / 158 | mv, scan_it, mv, wait_at, mv, scan_it, mv |
| C6 | 07 | 170 / 201 | 164 / 195 | 167 / 198 | mv, scan_it, mv, mv, wait_at, mv, mv, scan_it, mv |
| C7 | 08 | 241 / 272 | 174 / 205 | 155 / 186 | mv, ‖ mv, wait_at, ‖ mv, scan_it, mv, scan_it, mv |
| C8 | 09 | 213 / 244 | 157 / 188 | 154 / 185 | mv, ‖ mv, wait_at, ‖ mv, mv, scan_it, mv, scan_it, mv |
| C9 | 10 | 80 / 111 | 70 / 101 | 76 / 107 | mv, mv, scan_it, mv |
| C10 | 11 | 152 / 183 | 155 / 186 | 91 / 122 | mv, mv, scan_it, mv, scan_it, mv |
| C11 | 12 | 149 / 180 | 141 / 172 | 121 / 152 | mv, scan_it, stand, mv, scan_it, mv |
| C12 | 13 | 108 / 139 | 100 / 131 | 80 / 111 | mv, scan_it, mv, scan_it, mv |
| C13 | 14 | 56 / 87 | 56 / 87 | 34 / 65 | mv, scan_it, mv |
| C14 | 15 | 56 / 87 | 52 / 83 | 52 / 83 | mv, scan_it, mv |
| M1 | 16 | 300 / 331 | 238 / 269 | 244 / 275 | mv, ‖ mv, wait_at, ‖ mv, scan_it, mv, mv, wait_at, mv, mv, scan_it, mv |
| M2 | 17 | 192 / 223 | 209 / 240 | 137 / 168 | mv, mv, wait_at, mv, scan_it, mv, scan_it, mv |
| M3 | 18 | 189 / 220 | 202 / 233 | 173 / 204 | mv, scan_it, stand, mv, ‖ mv, wait_at, ‖ mv, mv, scan_it, mv |
| M4 | 19 | 171 / 202 | 172 / 203 | 150 / 181 | mv, scan_it, mv, mv, wait_at, mv, mv, scan_it, mv |
