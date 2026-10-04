# T-K part 1, step 5: the planning cases with context knowledge (kitting, a working robot, env_layout_18)

The records: design_records.md, "T-K", THE PLANNING CASES, RULED (KT15), THE ROOM, RULED, THE STEP'S MODE AND SIZE and
STEP 5, STAGE 1, REVISED: THE SET. A basic check that context knowledge works through the planning chain, not a coverage
set: (1) the chain follows the oracle and the reference; (2) a gain where the human acts in accord with the context;
(3) a cost where the human acts against it. Results: `REPORT.md` (stage 3).

## The set (stage 2, authored before any run with context knowledge on)

- The room `env_layout_18`: env_layout_17 and the robot's `kitting_table_1` (440, -450), `shelf_5` (-470, -400),
  `shelf_6` (480, -60) (the layout's notes give why each is there). The setup `env_setup_16`: item_4 on shelf_4 for
  kitting_table_0 (the human's); item_5 on shelf_5 and item_6 on shelf_6 for kitting_table_1 (the robot's). No
  default timeline.
- The human: from (0, 450), assigned deliver_item(item_4) alone (step 4's last-delivery state), every script ending
  with the exit walk to corner_NE. The robot: one task.
- Six scenarios (`domains/kitting/scenarios/scenarios_s16.py`), nine runs, single_task, run files in
  `configs/kitting/mpb/tk/` (context knowledge on) and `configs/kitting/mpb/tk/off/` (off). Outputs in this folder and
  in `off/`, per scenario in `on_single_task/` (the instrument's name for assignment knowledge on).

| scenario | timeline | script | robot | sides | case |
|---|---|---|---|---|---|
| scenario_s16_01 | none | deliver item_4 | (-470, -120), item_5 past the turn at shelf_4 | off, on | 3 (on); reference for 2, 3 (off) |
| scenario_s16_02 | break_time from 0 | as _01 | as _01 | on | 2 |
| scenario_s16_03 | none | coffee_break, deliver item_4 | (-200, 0), item_6 past the stand at the machine | off, on | 4 (on); reference for 1, 4 (off) |
| scenario_s16_04 | break_time from 0 | as _03 | as _03 | on | 1 |
| scenario_s16_05 | none | ac_activation, deliver item_4 | (400, 210), item_5 across the walk to the switch | off, on | 5 (on); reference (off) |
| scenario_s16_06 | room_warm from 0 | as _05 | as _05 | on | 5, the A/C raised |

Commands (from the repo root):

    analysis/instruments/mpb/run.sh kitting --expect -o analysis/kitting/mpb/tk configs/kitting/mpb/tk/scenario_s16_0*.yaml
    analysis/instruments/mpb/run.sh kitting --expect -o analysis/kitting/mpb/tk/off configs/kitting/mpb/tk/off/scenario_s16_0*.yaml
    analysis/instruments/mpb/run.sh kitting -o analysis/kitting/mpb/tk configs/kitting/mpb/tk/scenario_s16_0*.yaml
    analysis/instruments/mpb/run.sh kitting -o analysis/kitting/mpb/tk/off configs/kitting/mpb/tk/off/scenario_s16_0*.yaml
    analysis/kitting/mpb/tk/tk5.py expect | report

## The expectations

What is compared and what is declared:
- Parts 1 to 3 (MPB-1): the oracle's per-tick table (`expected_ticks.json`, `mpb_oracle.py` with the prior of the run
  file's side) and the chain assembled from it with the run's no_current_task ticks; compared by `compare.py`.
- Part 4: the declared properties PK1 to PK5 per side (`analysis/kitting/mpb/properties.py`, its docstring), stated
  before any run. The reference: the robot alone (`reference.py`, now carrying the scenario's own timeline), run for
  each of the six (`properties.CONTROLS`).

The expected chain before the robot's completion (`tk5.py expect`; the oracle's table with the one no_current_task
tick known before the run, tick 0; nct no_current_task, rc recognition_changed, pe projection_expired):

| scenario | side | case | expected decisions before the robot's completion (tick trigger/cause: projection) |
|---|---|---|---|
| scenario_s16_01 | off | 3, 2 (reference) | 0 nct: fallback moving k=1 end=2; 2 pe: fallback moving k=3 end=6; 6 pe: fallback moving k=7 end=14; 14 pe: fallback moving k=15 end=30; 30 pe: fallback moving k=31 end=44; 45 pe: fallback standing k=1 end=47; 47 rc/entered: admitted deliver_item(item_4); 93 rc/replaced: fallback standing k=2 end=96; 96 pe: fallback moving k=2 end=99; 99 pe: fallback moving k=5 end=105; 105 rc/entered: admitted coffee_break; 117 rc/retraction: fallback standing k=2 end=120; 120 pe: fallback standing k=5 end=126; 126 pe: fallback standing k=11 end=138 |
| scenario_s16_01 | on, no fact | 3 | 0 nct: admitted deliver_item(item_4); 93 rc/replaced: fallback standing k=2 end=96; 96 pe: fallback moving k=2 end=99; 99 pe: fallback moving k=5 end=105; 105 rc/entered: admitted coffee_break; 117 rc/retraction: fallback standing k=2 end=120; 120 pe: fallback standing k=5 end=126; 126 pe: fallback standing k=11 end=138 |
| scenario_s16_02 | on, break_time | 2 | 0 nct: fallback moving k=1 end=2; 2 pe: fallback moving k=3 end=6; 6 pe: fallback moving k=7 end=14; 14 pe: fallback moving k=15 end=30; 30 pe: fallback moving k=31 end=44; 38 rc/entered: admitted deliver_item(item_4); 93 rc/replaced: fallback standing k=2 end=96; 95 rc/entered: admitted coffee_break; 117 rc/retraction: fallback standing k=2 end=120; 120 pe: fallback standing k=5 end=126; 126 pe: fallback standing k=11 end=138 |
| scenario_s16_03 | off | 1, 4 (reference) | 0 nct: fallback moving k=1 end=2; 2 pe: fallback moving k=3 end=6; 6 pe: fallback moving k=7 end=14; 14 pe: fallback moving k=15 end=30; 30 pe: fallback moving k=31 end=42; 36 rc/entered: admitted coffee_break; 72 rc/replaced: fallback standing k=31 end=104; 97 rc/entered: admitted deliver_item(item_4) |
| scenario_s16_03 | on, no fact | 4 | 0 nct: admitted deliver_item(item_4); 43 rc/retraction: fallback standing k=2 end=46; 46 pe: fallback standing k=5 end=52; 52 pe: fallback standing k=11 end=64; 55 rc/entered: admitted coffee_break; 72 rc/replaced: fallback standing k=31 end=104; 73 rc/entered: admitted deliver_item(item_4) |
| scenario_s16_04 | on, break_time | 1 | 0 nct: fallback moving k=1 end=2; 2 pe: fallback moving k=3 end=6; 6 pe: fallback moving k=7 end=14; 14 pe: fallback moving k=15 end=30; 22 rc/entered: admitted coffee_break; 72 rc/replaced: fallback standing k=31 end=104; 73 rc/entered: admitted deliver_item(item_4) |
| scenario_s16_05 | off | 5 (reference) | 0 nct: fallback moving k=1 end=2; 2 pe: fallback moving k=3 end=6; 6 pe: fallback moving k=7 end=14; 14 pe: fallback moving k=15 end=30; 30 pe: fallback moving k=31 end=45; 45 pe: fallback standing k=1 end=47; 47 pe: fallback standing k=3 end=51; 51 pe: fallback moving k=4 end=54; 54 pe: fallback standing k=1 end=56; 56 pe: fallback standing k=3 end=60; 60 pe: fallback moving k=4 end=65; 63 rc/entered: admitted deliver_item(item_4); 102 rc/replaced: fallback standing k=2 end=105; 105 pe: fallback moving k=2 end=108; 108 pe: fallback moving k=5 end=114; 114 rc/entered: admitted coffee_break; 126 rc/retraction: fallback standing k=2 end=129; 129 pe: fallback standing k=5 end=135 |
| scenario_s16_05 | on, no fact | 5 | 0 nct: admitted deliver_item(item_4); 46 rc/boundary: fallback standing k=2 end=49; 47 rc/entered: admitted deliver_item(item_4); 102 rc/replaced: fallback standing k=2 end=105; 104 rc/entered: admitted coffee_break; 126 rc/retraction: fallback standing k=2 end=129; 129 pe: fallback standing k=5 end=135 |
| scenario_s16_06 | on, room_warm | 5, the A/C raised | 0 nct: fallback moving k=1 end=2; 2 pe: fallback moving k=3 end=6; 6 pe: fallback moving k=7 end=14; 14 pe: fallback moving k=15 end=30; 30 pe: fallback moving k=31 end=45; 45 pe: fallback standing k=1 end=47; 47 rc/entered: admitted deliver_item(item_4); 102 rc/replaced: fallback standing k=2 end=105; 104 rc/entered: admitted coffee_break; 126 rc/retraction: fallback standing k=2 end=129; 129 pe: fallback standing k=5 end=135 |

The expected decisions in words (the declared properties):
- Cases 3 and 2 (_01, _02), the turn at shelf_4 (the human stands 45 to 47 and steps north at 48). Off has no
  projection past the arrival at 44 and is expected to come below min_separation in 40 to 60 (PK3off.sep; the authoring
  run: the robot moving at 42 cm at 44, then standing at 42 cm). On with no fact admits deliver_item(item_4) at 0 and
  holds at 0 against the turn, no fallback decision before 47, and stays above min_separation (PK3a to PK3c: the gain
  with no fact). On with break_time rests on off's fallbacks until 38, then admits and holds, 7 ticks before the turn
  (PK2a, PK2b).
- Cases 1 and 4 (_03, _04), the stand at the machine (42 to 73). Off admits coffee_break at 36 and holds (PK1off); at
  72, when the break ends, it rests on the observed stand of 31 ticks and holds until item_4's admission at 97
  (PK1off.stale). On with break_time admits coffee_break at 22, after off's fallback decisions 0, 2, 6, 14, and holds
  14 ticks earlier than off (PK1a: the gain in the raised state). On with no fact rests on item_4 from 0 to 42 with no
  hold (PK4a), and at 43 the retraction's decision, on the stand fallback, holds the robot short of the standing human
  (PK4b, PK4c); coffee_break is admitted at 55 (PK4d): the cost, and what the retraction changes. Both on sides admit
  item_4 at 73 after the observed break and rest on no stand fallback after 72 (PK4e, PK1b; E2's form, an observation).
- Case 5 (_05, _06), the walk to the switch. Off holds at 14 on the fallback, no violation in 15 to 35 (PK5off). On
  with no fact rests on item_4 from 0 with no hold and no other decision before 46, and the robot violates in 15 to 35
  (PK5a, PK5b: the cost). On with room_warm admits nothing before 47 and holds as off (PK5rw).

md5s of the expectations (committed before any run with context knowledge on; `expected_ticks.json` and the
`trajectory.json` it is derived from):

    eae448df322fcad96ce6b142641cb9ec  off/scenario_s16_01/on_single_task/expected_ticks.json
    87f64839194e6b2fcbd84a9bb5a2b780  off/scenario_s16_01/on_single_task/trajectory.json
    5dcdec18d84ba1486f29c4f4c2296449  off/scenario_s16_03/on_single_task/expected_ticks.json
    a8e3451465cd3753905e4c1e61ac2e4b  off/scenario_s16_03/on_single_task/trajectory.json
    fb0aa231fd0d6cf3ab71ca7b1868c0d2  off/scenario_s16_05/on_single_task/expected_ticks.json
    adbb6324dc00ef52a3d2345e38bf57ff  off/scenario_s16_05/on_single_task/trajectory.json
    7d122aa626559b7cea6895eab64f3812  scenario_s16_01/on_single_task/expected_ticks.json
    87f64839194e6b2fcbd84a9bb5a2b780  scenario_s16_01/on_single_task/trajectory.json
    fbf6ca3837f0e744f47f945d846a956b  scenario_s16_02/on_single_task/expected_ticks.json
    dade28a05adf321606307c486faee0a3  scenario_s16_02/on_single_task/trajectory.json
    4ee1ad9263f1fa4bca5f20f9893ad211  scenario_s16_03/on_single_task/expected_ticks.json
    a8e3451465cd3753905e4c1e61ac2e4b  scenario_s16_03/on_single_task/trajectory.json
    9592146e2ffe50643c71d95e116b995a  scenario_s16_04/on_single_task/expected_ticks.json
    ddfd45002ab2411d212d1a0e7f6a6483  scenario_s16_04/on_single_task/trajectory.json
    83b75d80de3e2c8980f758f569da29ca  scenario_s16_05/on_single_task/expected_ticks.json
    adbb6324dc00ef52a3d2345e38bf57ff  scenario_s16_05/on_single_task/trajectory.json
    fccb70761bc4449243b443d5894559d9  scenario_s16_06/on_single_task/expected_ticks.json
    fdc99b95573c0d142eaf38b4e6f40c3c  scenario_s16_06/on_single_task/trajectory.json

## Runs (stage 3; git-ignored; md5s)

    9c225a6ead52fecde1d48e82a7cca77c  off/runs/env_layout_18_scenario_s16_01_on_single_task.log
    8f8202925985958770a81871f3c02b0e  off/runs/env_layout_18_scenario_s16_01_reference_single_task.log
    b04e380a5e094279dcda67f067ce9d6a  off/runs/env_layout_18_scenario_s16_03_on_single_task.log
    170650d7431ec052246d27b5cca6a621  off/runs/env_layout_18_scenario_s16_03_reference_single_task.log
    fa5478e6cfad2dd465d8ef4d00f098e8  off/runs/env_layout_18_scenario_s16_05_on_single_task.log
    f9929f298f171991bf56f9f04d29b30a  off/runs/env_layout_18_scenario_s16_05_reference_single_task.log
    9cfcd166b8fd4971d50c6a03d88711b9  runs/env_layout_18_scenario_s16_01_on_single_task.log
    a679767445a6ec38c0c8e9185a2a8b33  runs/env_layout_18_scenario_s16_01_reference_single_task.log
    c62b3221d103d6b9fe05793def52351d  runs/env_layout_18_scenario_s16_02_on_single_task.log
    1de66ae2fa87f8c5afb3610f12d074a8  runs/env_layout_18_scenario_s16_02_reference_single_task.log
    dc6a446c63a665d51087632cf54a95ce  runs/env_layout_18_scenario_s16_03_on_single_task.log
    77fc6a362c4d5ef9915d26ab3ce5c5bf  runs/env_layout_18_scenario_s16_03_reference_single_task.log
    3e26647cd2ce453dcc5156151794af2b  runs/env_layout_18_scenario_s16_04_on_single_task.log
    7135203fb5ad3a45e4dd136bc6c66f93  runs/env_layout_18_scenario_s16_04_reference_single_task.log
    469142457429c96e528f81837dd7d6e7  runs/env_layout_18_scenario_s16_05_on_single_task.log
    4a8995b59a6ac2bd26b2ce15abd3c9f2  runs/env_layout_18_scenario_s16_05_reference_single_task.log
    0e4c459cfb92dc0909be337ab65f613c  runs/env_layout_18_scenario_s16_06_on_single_task.log
    0322dfb2e9c441f47866ca3c374923c0  runs/env_layout_18_scenario_s16_06_reference_single_task.log

Results: `REPORT.md`. 0 disagreements with the oracle in all nine; the expectations' md5s unchanged by the runs.

## Step 5d: the expectations after the gate change (5 October 2026, committed before the runs)

The oracle after the gate's build (8357b74: the rank column, D3; observation warrant at admission, AM67;
none(leader_outranked) last, AM68 and D1) recomputes every table; the trajectories are byte-identical to stage 1's
(the human's script is open-loop). Commands as above, with --expect. The runs follow in the next commit; the reading:
analysis/kitting/tk5d/REPORT.md. Step 5's properties moved by the rulings are re-declared in
analysis/kitting/mpb/properties.py (D5 (a); the old ones kept in its docstring, marked superseded): PK4a.r, PK4b.r,
PK4e.r (scenario_s16_03), PK1b.r (s16_04), PK5a.r (s16_05); PK4c and PK5b have no successor, the separation in their
windows a measure. The expected chain (tk5.py expect) agrees with the plan's section 4: s16_03 on refused
none(leader_outranked) at 0, coffee_break entered at 55, item_4 at 74; s16_04 coffee_break at 22, item_4 at 74;
s16_05 refused none(leader_outranked) at 0, item_4 first admitted at 48; s16_06 item_4 at 48; s16_01 and s16_02
unchanged (item_4 at 0 and 38). Off: s16_03 coffee_break 36, item_4 97; s16_05 item_4 63.

    6d01fc6c5897726ada80d8f1e92ad066  off/scenario_s16_01/on_single_task/expected_ticks.json
    a85612a49071befde40dbad7e36d5263  off/scenario_s16_03/on_single_task/expected_ticks.json
    d78b9273888bd91c8089ef962904ac44  off/scenario_s16_05/on_single_task/expected_ticks.json
    e45523c3f845dfb1c0f0b6d8f7f0a7b7  scenario_s16_01/on_single_task/expected_ticks.json
    7518ff025ae3dfbe2d87c96f49c333d5  scenario_s16_02/on_single_task/expected_ticks.json
    97b038557fa12240c294a05372a0021b  scenario_s16_03/on_single_task/expected_ticks.json
    a5e0b6da5725137936ba0f7050714cac  scenario_s16_04/on_single_task/expected_ticks.json
    c21d7ea06c28baf9182db64d53677823  scenario_s16_05/on_single_task/expected_ticks.json
    237cbdf8442eac7dc2efe2259f802e47  scenario_s16_06/on_single_task/expected_ticks.json

## Step 5d: the runs (5 October 2026)

The runs with the commands above, at f02b04c (the code of the gate's build); each run's own oracle call reproduced
the expectations committed in the section above (md5 check). D3 was then amended by Hadi (exact ties:
design_records.md, "T-K", D3's AMENDED line) and the oracle and the comparison rerun on these runs (no simulation):
every change of the tables a cell marked undetermined before. The reading, with the comparison off / on before the
gate change / on after it: analysis/kitting/tk5d/REPORT.md. 6 on runs and 3 off runs: 0 disagreements on parts 1 to
3. Properties: every re-declared one holds (PK4a.r, PK4b.r, PK4e.r, PK1b.r, PK5a.r) and PK1a, PK1c, PK2a, PK3a, PK3b,
PK4d, PK5rw, PK1off, PK1off.stale, PK3off, PK3off.sep, PK5off hold; PK3c and PK2b fail as before the gate change (the
turn, TODO-146). B12's instance (D4): s16_03 and s16_05 refuse their tick-0 decision none(leader_outranked). The
alteration test (D6): C4 detected in s16_03 and s16_05 (56 each), C6 the same, C5 (since D3's amendment: an exact tie
counted outranked) undetected in all six, since on no tick of the six a leader passes θ, adequacy and warrant tied
with another key: a property of the set.

The expected tables after D3's amendment (md5):

    6d01fc6c5897726ada80d8f1e92ad066  off/scenario_s16_01/on_single_task/expected_ticks.json
    a85612a49071befde40dbad7e36d5263  off/scenario_s16_03/on_single_task/expected_ticks.json
    d78b9273888bd91c8089ef962904ac44  off/scenario_s16_05/on_single_task/expected_ticks.json
    e45523c3f845dfb1c0f0b6d8f7f0a7b7  scenario_s16_01/on_single_task/expected_ticks.json
    7518ff025ae3dfbe2d87c96f49c333d5  scenario_s16_02/on_single_task/expected_ticks.json
    97b038557fa12240c294a05372a0021b  scenario_s16_03/on_single_task/expected_ticks.json
    a5e0b6da5725137936ba0f7050714cac  scenario_s16_04/on_single_task/expected_ticks.json
    c21d7ea06c28baf9182db64d53677823  scenario_s16_05/on_single_task/expected_ticks.json
    237cbdf8442eac7dc2efe2259f802e47  scenario_s16_06/on_single_task/expected_ticks.json

Runs (git-ignored; md5s):

    0050c7cb6c10db9f84bd7f75d11f3ca4  off/runs/env_layout_18_scenario_s16_01_on_single_task.log
    707f245e178199a79489dea107fd85a7  off/runs/env_layout_18_scenario_s16_01_on_single_task.rec
    8f8202925985958770a81871f3c02b0e  off/runs/env_layout_18_scenario_s16_01_reference_single_task.log
    3e5debb5007061e9d1e1effd50f1e7a3  off/runs/env_layout_18_scenario_s16_03_on_single_task.log
    678830665da62649ad71e5fd5db6e679  off/runs/env_layout_18_scenario_s16_03_on_single_task.rec
    170650d7431ec052246d27b5cca6a621  off/runs/env_layout_18_scenario_s16_03_reference_single_task.log
    96bd07da7c99ad08c497cce202479a66  off/runs/env_layout_18_scenario_s16_05_on_single_task.log
    4c9b7e1d71713afc3d4f4512f1430a41  off/runs/env_layout_18_scenario_s16_05_on_single_task.rec
    f9929f298f171991bf56f9f04d29b30a  off/runs/env_layout_18_scenario_s16_05_reference_single_task.log
    9d7650d67f159e38da8d4b3c6d20e0f9  runs/env_layout_18_scenario_s16_01_on_single_task.log
    707f245e178199a79489dea107fd85a7  runs/env_layout_18_scenario_s16_01_on_single_task.rec
    a679767445a6ec38c0c8e9185a2a8b33  runs/env_layout_18_scenario_s16_01_reference_single_task.log
    db9f16a84d8dcc6fc294f6c2e62dfd78  runs/env_layout_18_scenario_s16_02_on_single_task.log
    707f245e178199a79489dea107fd85a7  runs/env_layout_18_scenario_s16_02_on_single_task.rec
    1de66ae2fa87f8c5afb3610f12d074a8  runs/env_layout_18_scenario_s16_02_reference_single_task.log
    68e8868774796f7ad4055b6391c99c15  runs/env_layout_18_scenario_s16_03_on_single_task.log
    678830665da62649ad71e5fd5db6e679  runs/env_layout_18_scenario_s16_03_on_single_task.rec
    77fc6a362c4d5ef9915d26ab3ce5c5bf  runs/env_layout_18_scenario_s16_03_reference_single_task.log
    fe60bfb1b38e47b82bef65cfc96b1443  runs/env_layout_18_scenario_s16_04_on_single_task.log
    678830665da62649ad71e5fd5db6e679  runs/env_layout_18_scenario_s16_04_on_single_task.rec
    7135203fb5ad3a45e4dd136bc6c66f93  runs/env_layout_18_scenario_s16_04_reference_single_task.log
    919a7c2299d64c53db89ca049c1b2473  runs/env_layout_18_scenario_s16_05_on_single_task.log
    4c9b7e1d71713afc3d4f4512f1430a41  runs/env_layout_18_scenario_s16_05_on_single_task.rec
    4a8995b59a6ac2bd26b2ce15abd3c9f2  runs/env_layout_18_scenario_s16_05_reference_single_task.log
    fd6de3ddeabf737f8ae53652a4a8affc  runs/env_layout_18_scenario_s16_06_on_single_task.log
    4c9b7e1d71713afc3d4f4512f1430a41  runs/env_layout_18_scenario_s16_06_on_single_task.rec
    0322dfb2e9c441f47866ca3c374923c0  runs/env_layout_18_scenario_s16_06_reference_single_task.log
