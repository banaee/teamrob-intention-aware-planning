# The MPB on dock_loading (T-G stage 1): report

SUPERSEDING NOTE (Hadi, 3 Oct 2026): the results of the run files of 500 steps or more are potentially confounded by an
undeclared weight (the hardcoded context weight multiplies coffee_break by 2.5 from step 500); they are not declared
invalid; the recorded violations of the minimum separation at ticks 387 and 224 to 226 fall before step 500. Pointer:
design_records.md, "T-G stage 1", SCOPE REDUCED AND THE MPB ON DOCK_LOADING RUN, its CAVEAT. The report's own text is
unchanged.

The set, its rulings and the build: README.md, authoring.md; design_decisions.md, "T-G: the second domain's rulings",
THE MPB ON DOCK_LOADING. The expectations (trajectory.json, expected_ticks.json, 20 scenarios, both strategies) and K8's
table (predictions.md) were committed before any run (8fb9981). Run 2 October 2026.

Scope (Hadi, 2 October 2026; the closing record): stage 1's MPB establishes that the recognizer and the
recognition-to-planning chain run on dock_loading and produce runs, logs and figures, compared with the oracle where the
records give full expectations. The behavioural analysis is stage 2's. No property-by-property interpretation here; the
observations at the end are unanalysed.

## What ran

52 runs: K1 to K9 and M3 (kind 3, full expectations) and M1, M2, M4 (kind 2, dependent on the robot, declared properties
only, MPB-DL3), in env_layout_03 and env_layout_04, prior on, `single_task` and `full_reorder`. Every run completed (the
robot's pool empty within the cap). K1's comparison runs (reference.py, the human removed): 4.

Comparison with the oracle (parts 1 to 3, exact; MPB-3), the 40 runs with full expectations: **0 disagreements per tick,
per decision and in the log in every run**; each run's own oracle call reproduced the committed table byte for byte;
every trajectory equal to the run's human lines. The per-tick tables are identical across the strategies.

| row | scenario | room | strategy | completed | disagreements | viol (moving robot) | standing robot: human passing / beside | holds (tick, hold) | declared properties |
|---|---|---|---|---|---|---|---|---|---|
| K1 | scenario_s08_01 | env_layout_03 | single_task | terminal 127 (cap 201) | 0 | 0 | 0 / 0 | - | P1a=yes, P1b=yes, P1c=yes |
| K1 | scenario_s08_01 | env_layout_03 | full_reorder | terminal 127 (cap 201) | 0 | 0 | 0 / 0 | - | P1a=yes, P1b=yes, P1c=yes |
| K1 | scenario_s09_01 | env_layout_04 | single_task | terminal 59 (cap 144) | 0 | 0 | 0 / 0 | - | P1a=yes, P1b=yes, P1c=yes |
| K1 | scenario_s09_01 | env_layout_04 | full_reorder | terminal 59 (cap 144) | 0 | 0 | 0 / 0 | - | P1a=yes, P1b=yes, P1c=yes |
| K2 | scenario_s08_02 | env_layout_03 | single_task | terminal 215 (cap 393) | 0 | 0 | 0 / 0 | - | - |
| K2 | scenario_s08_02 | env_layout_03 | full_reorder | terminal 177 (cap 393) | 0 | 0 | 0 / 0 | - | - |
| K2 | scenario_s09_02 | env_layout_04 | single_task | terminal 238 (cap 360) | 0 | 0 | 0 / 0 | - | - |
| K2 | scenario_s09_02 | env_layout_04 | full_reorder | terminal 196 (cap 360) | 0 | 0 | 0 / 0 | - | - |
| K3 | scenario_s08_03 | env_layout_03 | single_task | terminal 215 (cap 465) | 0 | 0 | 0 / 0 | - | - |
| K3 | scenario_s08_03 | env_layout_03 | full_reorder | terminal 334 (cap 465) | 0 | 0 | 5 / 0 | [[49, 13], [73, 48], [121, 96]] | - |
| K3 | scenario_s09_03 | env_layout_04 | single_task | terminal 247 (cap 431) | 0 | 0 | 0 / 0 | - | - |
| K3 | scenario_s09_03 | env_layout_04 | full_reorder | terminal 349 (cap 431) | 0 | 0 | 0 / 0 | [[38, 10], [62, 48]] | - |
| K4 | scenario_s08_04 | env_layout_03 | single_task | terminal 223 (cap 269) | 0 | 0 | 5 / 0 | [[49, 13], [73, 48], [121, 96]] | - |
| K4 | scenario_s08_04 | env_layout_03 | full_reorder | terminal 223 (cap 269) | 0 | 0 | 5 / 0 | [[49, 13], [73, 48], [121, 96]] | - |
| K4 | scenario_s09_04 | env_layout_04 | single_task | terminal 213 (cap 241) | 0 | 0 | 4 / 0 | [[38, 10], [62, 48], [110, 96]] | - |
| K4 | scenario_s09_04 | env_layout_04 | full_reorder | terminal 213 (cap 241) | 0 | 0 | 4 / 0 | [[38, 10], [62, 48], [110, 96]] | - |
| K5 | scenario_s08_05 | env_layout_03 | single_task | terminal 215 (cap 371) | 0 | 0 | 0 / 0 | - | - |
| K5 | scenario_s08_05 | env_layout_03 | full_reorder | terminal 177 (cap 371) | 0 | 0 | 0 / 0 | - | - |
| K5 | scenario_s09_05 | env_layout_04 | single_task | terminal 238 (cap 337) | 0 | 0 | 0 / 0 | - | - |
| K5 | scenario_s09_05 | env_layout_04 | full_reorder | terminal 196 (cap 337) | 0 | 0 | 0 / 0 | - | - |
| K6 | scenario_s08_06 | env_layout_03 | single_task | terminal 276 (cap 531) | 0 | 0 | 0 / 0 | - | - |
| K6 | scenario_s08_06 | env_layout_03 | full_reorder | terminal 255 (cap 531) | 0 | 0 | 0 / 0 | [[141, 7]] | - |
| K6 | scenario_s09_06 | env_layout_04 | single_task | terminal 329 (cap 498) | 0 | 0 | 0 / 0 | - | - |
| K6 | scenario_s09_06 | env_layout_04 | full_reorder | terminal 270 (cap 498) | 0 | 2 | 0 / 0 | [[96, 5]] | - |
| K7 | scenario_s08_07 | env_layout_03 | single_task | terminal 279 (cap 548) | 0 | 0 | 0 / 0 | [[157, 3]] | - |
| K7 | scenario_s08_07 | env_layout_03 | full_reorder | terminal 248 (cap 548) | 0 | 0 | 0 / 0 | - | - |
| K7 | scenario_s09_07 | env_layout_04 | single_task | terminal 329 (cap 538) | 0 | 0 | 0 / 0 | - | - |
| K7 | scenario_s09_07 | env_layout_04 | full_reorder | terminal 267 (cap 538) | 0 | 0 | 0 / 0 | - | - |
| K8 | scenario_s08_08 | env_layout_03 | single_task | terminal 215 (cap 466) | 0 | 0 | 0 / 0 | - | - |
| K8 | scenario_s08_08 | env_layout_03 | full_reorder | terminal 179 (cap 466) | 0 | 2 | 0 / 0 | [[162, 2]] | - |
| K8 | scenario_s09_08 | env_layout_04 | single_task | terminal 244 (cap 436) | 0 | 0 | 2 / 0 | [[130, 6]] | - |
| K8 | scenario_s09_08 | env_layout_04 | full_reorder | terminal 196 (cap 436) | 0 | 0 | 0 / 0 | - | - |
| K9 | scenario_s08_09 | env_layout_03 | single_task | terminal 127 (cap 260) | 0 | 0 | 0 / 0 | - | - |
| K9 | scenario_s08_09 | env_layout_03 | full_reorder | terminal 127 (cap 260) | 0 | 0 | 0 / 0 | - | - |
| K9 | scenario_s09_09 | env_layout_04 | single_task | terminal 147 (cap 282) | 0 | 2 | 0 / 0 | - | - |
| K9 | scenario_s09_09 | env_layout_04 | full_reorder | terminal 130 (cap 282) | 0 | 0 | 0 / 0 | - | - |
| M1 | scenario_s05_04 | env_layout_03 | single_task | terminal 430 (cap 686) | not compared (MPB-DL3) | 0 | 0 / 0 | - | M(i)=yes, M(ii)=yes, M(iii)=yes, M(iv)=yes |
| M1 | scenario_s05_04 | env_layout_03 | full_reorder | terminal 385 (cap 686) | not compared (MPB-DL3) | 0 | 7 / 3 | - | M(i)=yes, M(ii)=yes, M(iii)=yes, M(iv)=yes |
| M1 | scenario_s07_04 | env_layout_04 | single_task | terminal 471 (cap 639) | not compared (MPB-DL3) | 1 | 2 / 0 | [[382, 6]] | M(i)=yes, M(ii)=yes, M(iii)=NO, M(iv)=yes |
| M1 | scenario_s07_04 | env_layout_04 | full_reorder | terminal 435 (cap 639) | not compared (MPB-DL3) | 0 | 10 / 3 | [[63, 6], [206, 5]] | M(i)=yes, M(ii)=yes, M(iii)=yes, M(iv)=yes |
| M2 | scenario_s05_05 | env_layout_03 | single_task | terminal 424 (cap 803) | not compared (MPB-DL3) | 0 | 6 / 3 | - | M(i)=yes, M(ii)=yes, M(iii)=yes, M(iv)=yes |
| M2 | scenario_s05_05 | env_layout_03 | full_reorder | terminal 385 (cap 803) | not compared (MPB-DL3) | 0 | 6 / 3 | - | M(i)=yes, M(ii)=yes, M(iii)=yes, M(iv)=yes |
| M2 | scenario_s07_05 | env_layout_04 | single_task | terminal 471 (cap 760) | not compared (MPB-DL3) | 4 | 2 / 0 | [[382, 6]] | M(i)=yes, M(ii)=yes, M(iii)=NO, M(iv)=yes |
| M2 | scenario_s07_05 | env_layout_04 | full_reorder | terminal 435 (cap 760) | not compared (MPB-DL3) | 0 | 11 / 3 | [[63, 6], [206, 5]] | M(i)=yes, M(ii)=yes, M(iii)=yes, M(iv)=yes |
| M3 | scenario_s08_10 | env_layout_03 | single_task | terminal 276 (cap 658) | 0 | 0 | 0 / 0 | - | - |
| M3 | scenario_s08_10 | env_layout_03 | full_reorder | terminal 328 (cap 658) | 0 | 0 | 5 / 0 | [[239, 80]] | - |
| M3 | scenario_s09_10 | env_layout_04 | single_task | terminal 329 (cap 626) | 0 | 0 | 0 / 0 | - | - |
| M3 | scenario_s09_10 | env_layout_04 | full_reorder | terminal 267 (cap 626) | 0 | 0 | 0 / 0 | - | - |
| M4 | scenario_s05_06 | env_layout_03 | single_task | terminal 430 (cap 858) | not compared (MPB-DL3) | 0 | 0 / 0 | - | M(i)=yes, M(ii)=yes, M(iii)=yes, M(iv)=yes |
| M4 | scenario_s05_06 | env_layout_03 | full_reorder | terminal 385 (cap 858) | not compared (MPB-DL3) | 0 | 15 / 4 | - | M(i)=yes, M(ii)=yes, M(iii)=yes, M(iv)=yes |
| M4 | scenario_s07_06 | env_layout_04 | single_task | terminal 471 (cap 716) | not compared (MPB-DL3) | 1 | 2 / 0 | [[382, 6]] | M(i)=yes, M(ii)=yes, M(iii)=NO, M(iv)=yes |
| M4 | scenario_s07_06 | env_layout_04 | full_reorder | terminal 435 (cap 716) | not compared (MPB-DL3) | 0 | 15 / 4 | [[63, 6], [206, 5]] | M(i)=yes, M(ii)=yes, M(iii)=yes, M(iv)=yes |

"viol": the ticks whose continuous [sep] minimum lies below min_separation (50 cm) with a moving robot closing in;
"passing" and "beside": ticks below it with a standing robot, the human moving on the tick or not (separation.md).

## The cases, as the runs show them (no interpretation)

- K1: P1a, P1b, P1c hold in both rooms and strategies (completion 125 and 57 equal to the comparison runs').
- K3 (DL-P2): the switch by cost did not occur in env_layout_03 (either strategy). In env_layout_04 it occurred:
  single_task at the expiry of 104 (deliver-dry's hold 51, T_r 45.46, against return-1's 91.76: hold above the cost
  difference 46.3, X1's condition on the logged values), the robot holding pallet_4 at the truck, which it put back
  (105) before return-1; full_reorder at the expiry of 110, after holds 10 and 48, to deliver-frozen while carrying
  pallet_4.
- K4: holds 13, 48, 96 at the expiries 49, 73, 121 (env_layout_03) and 10, 48, 96 at 38, 62, 110 (env_layout_04),
  both strategies; the last outlasts the stand (the human leaves at 127 and 116). Evidence for TODO-132 (a).
- K8 (DL-P1): env_layout_03 entered 14, retraction 34, then the fallback, coffee_break entered 46, scan 0 re-entered 94,
  scan 2 entered 128 (single_task); the case formed. env_layout_04: no admission of scan 0, no retraction: the case did
  not form.
- K9: env_layout_03 coffee_break entered at 51 on the walk to the standby place (the wrong reading, expected), the
  robot's winner deliver-dry with hold 0, the retraction at 67, both strategies. env_layout_04 office_break entered at
  37, hold 0; single_task: the robot's no_current_task at 59 falls on the tick the recorded hypothesis turns
  inadequate and masks the retraction (DL-P4: not formed there); full_reorder: the retraction at 59.
- M2: two scans of one bay live on one tick did not occur; a decision while the human stood at the bay of the winner's
  delivery occurred at 84 and 319 (env_layout_03) and 83 and 367 (env_layout_04).

The closing walk to the desk (and K9's walk to the standby place) admitted as a break (DL-P5; expected by the oracle;
findings about the mind, with TODO-155), the entered decisions on such a walk, both strategies unless stated:
env_layout_03 coffee_break: K1 at 37, K2 at 93, K6 at 141, K7 at 157, K8 at 167 (and 179, full_reorder), K9 at 51;
env_layout_04 office_break: K2 at 54 and 59, K6 at 100, K7 at 141, K8 at 130, K9 at 37.

## Not run, not formed

- The alteration test on dock_loading (alteration.py, B1, E1 to E3): built, not run in stage 1; for stage 2.
- env_layout_02 (MPB-DL6).
- Not formed: K2's admission and K8's retraction in env_layout_04 (no admission of scan 0); K9's retraction in
  env_layout_04 under single_task (masked); K3's switch in env_layout_03; M2's two scans live at once in one bay.

## Observations for stage 2 (unanalysed)

1. M1, M2, M4 in env_layout_04, single_task: one F1 violation with a moving robot at 387 (M2 also 224 to 226): a hold
   of 6 decided at 382 on a moving fallback, then at 387 scan 1 entered and the re-decision against the admitted
   projection gave hold 0. M(iii) does not hold in those three runs.
2. K8 full_reorder env_layout_03: two F1 violations with a moving robot; K9 single_task env_layout_04: two.
3. Standing-robot ticks below min_separation (TODO-135's measure, MPB-DL4): up to 15 passing and 4 beside in the mixed
   full_reorder runs; 4 to 5 passing in K3, K4 and M3 (the robot holding beside the standing human).
4. The switch while carrying in K3 env_layout_04 puts the full pallet back into the truck first (B8's held-object rule).
5. K9 env_layout_04: the robot's own completion masks the retraction under one strategy and not the other.
6. The desk walk read as a break in most controlled runs (list above).
7. In the mixed runs, M1 and M4 of one room end on the same terminal tick under each strategy (env_layout_03: 430, 385;
   env_layout_04: 471, 435), M2 too except env_layout_03 single_task (424).

## Where the artefacts are

Per run, `<scenario>/on_<strategy>/`: trajectory.json, expected_ticks.json, expected_decisions.json, actual_*.json,
observed.json, selection.json, robot.json, diff.md and diff.json (the comparison), properties.md and properties.json,
figure.png, figure_ir.png (full expectations only), separation.md; K1's reference.json. The logs and the executor's
records in `runs/` (git-ignored), their md5s:

```
a0b31ea72d2f07f60cae33c2d708e1e0  runs/env_layout_03_scenario_s05_04_on_full_reorder.log
8cfbbeb1f9ec2d087ef5e8ff77aee974  runs/env_layout_03_scenario_s05_04_on_single_task.log
b4c4e1904b0ba1f51296dd19c4e3e347  runs/env_layout_03_scenario_s05_05_on_full_reorder.log
029683208e08a9a4533acaa80ac83873  runs/env_layout_03_scenario_s05_05_on_single_task.log
d731f3f6461404b075159e1426d2e407  runs/env_layout_03_scenario_s05_06_on_full_reorder.log
b810dfff079be3dbc6cecad020a0a0c2  runs/env_layout_03_scenario_s05_06_on_single_task.log
5d6616c21726ea500bd9662d29ddc21d  runs/env_layout_03_scenario_s08_01_on_full_reorder.log
ab6ce2e4e3b4a51ee520b780b46a10f4  runs/env_layout_03_scenario_s08_01_on_single_task.log
fd73288fcd2ada372ff60207606d87b8  runs/env_layout_03_scenario_s08_01_reference_full_reorder.log
0ebc3800c7dacffad37a4dc2859e9401  runs/env_layout_03_scenario_s08_01_reference_single_task.log
7c761fbff31103e9b393917562f6fa52  runs/env_layout_03_scenario_s08_02_on_full_reorder.log
648fac150b2049202dff825211e8d745  runs/env_layout_03_scenario_s08_02_on_single_task.log
d5c04ff53501df0c99c33506de879eda  runs/env_layout_03_scenario_s08_03_on_full_reorder.log
27eea971947e22b89e73ff668e3734ea  runs/env_layout_03_scenario_s08_03_on_single_task.log
ebbc7838f1d99b3fc06f4535d19189d4  runs/env_layout_03_scenario_s08_04_on_full_reorder.log
4c7e71e3fa1217dfddc70f02cbf9c401  runs/env_layout_03_scenario_s08_04_on_single_task.log
0c1209adaef538e4205cd6fb5d285c07  runs/env_layout_03_scenario_s08_05_on_full_reorder.log
94e556d11646a57d9f9c9d108471329b  runs/env_layout_03_scenario_s08_05_on_single_task.log
39ea50f858232271d3ba43c5e088bfe4  runs/env_layout_03_scenario_s08_06_on_full_reorder.log
afa657872e018049c6a529164e39e309  runs/env_layout_03_scenario_s08_06_on_single_task.log
650237d2bc4058bb77002420deb96312  runs/env_layout_03_scenario_s08_07_on_full_reorder.log
91d97c76ffb67e8a6885b59347d7cfdc  runs/env_layout_03_scenario_s08_07_on_single_task.log
0a2e6777d6d0aa5b600509e169944807  runs/env_layout_03_scenario_s08_08_on_full_reorder.log
cc379a51537ddf0920d212877f65ab0e  runs/env_layout_03_scenario_s08_08_on_single_task.log
aa5a436c9e2d8ce2e87b78a1267465e8  runs/env_layout_03_scenario_s08_09_on_full_reorder.log
d262275d664d0221b56159bf118ec396  runs/env_layout_03_scenario_s08_09_on_single_task.log
475c5bcdf576d7670eaeaf1ff2dd2c5e  runs/env_layout_03_scenario_s08_10_on_full_reorder.log
69238d3d649f6775c3643a93205d2fe1  runs/env_layout_03_scenario_s08_10_on_single_task.log
336c3baaeb62deeb3a235c87f3f1b478  runs/env_layout_04_scenario_s07_04_on_full_reorder.log
3d9c62ac498d7a0f6cc9f6965e31a60e  runs/env_layout_04_scenario_s07_04_on_single_task.log
1ddacc7c42d4707f2f5e36cb96c93c9a  runs/env_layout_04_scenario_s07_05_on_full_reorder.log
5185b1c64a979c60872682c286f20802  runs/env_layout_04_scenario_s07_05_on_single_task.log
5333377b89e54dbce5cab7279ed0a743  runs/env_layout_04_scenario_s07_06_on_full_reorder.log
9363dfbad6dbc9f8d99fd7185898861d  runs/env_layout_04_scenario_s07_06_on_single_task.log
445e312e7f27ed8823feb857e0f3a939  runs/env_layout_04_scenario_s09_01_on_full_reorder.log
3633da67efcf6d93478896f71e6eef63  runs/env_layout_04_scenario_s09_01_on_single_task.log
d32e7bd925c3c7e6024acf2c1f41fdf7  runs/env_layout_04_scenario_s09_01_reference_full_reorder.log
3b69f6d1aa58b3f94807b8333936fb43  runs/env_layout_04_scenario_s09_01_reference_single_task.log
33110ecc6d90e5f488d159038a847243  runs/env_layout_04_scenario_s09_02_on_full_reorder.log
181dbeea7b66a51f4bd71be761a31269  runs/env_layout_04_scenario_s09_02_on_single_task.log
89a294df11cdc07f7722a6980011a6cb  runs/env_layout_04_scenario_s09_03_on_full_reorder.log
68bacaf9bd276661c662704fe492cb7a  runs/env_layout_04_scenario_s09_03_on_single_task.log
5309483144723824ff7afba7b0ab6a51  runs/env_layout_04_scenario_s09_04_on_full_reorder.log
5e0f857b2dc5eb53f201c5f93d024f83  runs/env_layout_04_scenario_s09_04_on_single_task.log
8e4ef5004e17f87a83988619b570f4ba  runs/env_layout_04_scenario_s09_05_on_full_reorder.log
a28e2f6dc83d8714bd7850d2820a2a97  runs/env_layout_04_scenario_s09_05_on_single_task.log
1ea2a24e59610c62cc30285b05e8d17f  runs/env_layout_04_scenario_s09_06_on_full_reorder.log
cf947f743454b1cac4d3cb6d5836eaab  runs/env_layout_04_scenario_s09_06_on_single_task.log
e6dac932ec92f4a9d9d070b0c3094560  runs/env_layout_04_scenario_s09_07_on_full_reorder.log
ccfe9dc29ba7efdf411096c618e2acab  runs/env_layout_04_scenario_s09_07_on_single_task.log
10304d72429ac390d7f963affbe416ae  runs/env_layout_04_scenario_s09_08_on_full_reorder.log
4654fc9457ea5aa06936ff4ea4676ef6  runs/env_layout_04_scenario_s09_08_on_single_task.log
f4c865b48bcee86be541f3470aacaccf  runs/env_layout_04_scenario_s09_09_on_full_reorder.log
f480f87437e24055ab14b8ae8e45f8ed  runs/env_layout_04_scenario_s09_09_on_single_task.log
ce4001c0c7c20046813214c02b1e28cd  runs/env_layout_04_scenario_s09_10_on_full_reorder.log
e6779d7d7dc5c67be6433d96137e2a76  runs/env_layout_04_scenario_s09_10_on_single_task.log
a210384ad227528e3e96d63fef5faf5c  runs/env_layout_03_scenario_s05_04_on_full_reorder.rec
9d9d3c483e317dded8817cdb544ee348  runs/env_layout_03_scenario_s05_04_on_single_task.rec
4b1cc0c3e6f9dd79ad81740f9e9e948a  runs/env_layout_03_scenario_s05_05_on_full_reorder.rec
ef923174df3107cb1487ba978ac24053  runs/env_layout_03_scenario_s05_05_on_single_task.rec
dda3d69adccb5dff12b3ecb59b2db06f  runs/env_layout_03_scenario_s05_06_on_full_reorder.rec
b3cd2abe1bb189f0c27863542b525160  runs/env_layout_03_scenario_s05_06_on_single_task.rec
52e0a091c4cb4ade47ae9f5f4bf033ee  runs/env_layout_03_scenario_s08_01_on_full_reorder.rec
52e0a091c4cb4ade47ae9f5f4bf033ee  runs/env_layout_03_scenario_s08_01_on_single_task.rec
403cceedd798e27adfe208e864975dce  runs/env_layout_03_scenario_s08_02_on_full_reorder.rec
403cceedd798e27adfe208e864975dce  runs/env_layout_03_scenario_s08_02_on_single_task.rec
6dd7f096be826f92405f138e405b5653  runs/env_layout_03_scenario_s08_03_on_full_reorder.rec
6dd7f096be826f92405f138e405b5653  runs/env_layout_03_scenario_s08_03_on_single_task.rec
f5722c84e55961f47bf3f80b489ea45c  runs/env_layout_03_scenario_s08_04_on_full_reorder.rec
f5722c84e55961f47bf3f80b489ea45c  runs/env_layout_03_scenario_s08_04_on_single_task.rec
ea3310c543190c7f858efb2cb50462fd  runs/env_layout_03_scenario_s08_05_on_full_reorder.rec
ea3310c543190c7f858efb2cb50462fd  runs/env_layout_03_scenario_s08_05_on_single_task.rec
c6468ba79cd3406cc8a0296c85f7570b  runs/env_layout_03_scenario_s08_06_on_full_reorder.rec
c6468ba79cd3406cc8a0296c85f7570b  runs/env_layout_03_scenario_s08_06_on_single_task.rec
b5e178afd986e8269cf6cf76667a6e60  runs/env_layout_03_scenario_s08_07_on_full_reorder.rec
b5e178afd986e8269cf6cf76667a6e60  runs/env_layout_03_scenario_s08_07_on_single_task.rec
052068b414428033211a27db10d1cb21  runs/env_layout_03_scenario_s08_08_on_full_reorder.rec
052068b414428033211a27db10d1cb21  runs/env_layout_03_scenario_s08_08_on_single_task.rec
003008a41d3f698710c32ee1e82b4a09  runs/env_layout_03_scenario_s08_09_on_full_reorder.rec
003008a41d3f698710c32ee1e82b4a09  runs/env_layout_03_scenario_s08_09_on_single_task.rec
e7ba7aa95e0f2004a0208155122f1ea1  runs/env_layout_03_scenario_s08_10_on_full_reorder.rec
e7ba7aa95e0f2004a0208155122f1ea1  runs/env_layout_03_scenario_s08_10_on_single_task.rec
f5c4239b5391788d36bdbfb2b24d8d8f  runs/env_layout_04_scenario_s07_04_on_full_reorder.rec
f1d54a00545d269b0d558f9ed4dcffe9  runs/env_layout_04_scenario_s07_04_on_single_task.rec
0b5fd98b651d6af5172250f2268c5235  runs/env_layout_04_scenario_s07_05_on_full_reorder.rec
248d1c0dbecd27f2aa3369fa5f30c48d  runs/env_layout_04_scenario_s07_05_on_single_task.rec
34670e16faefc35669fd772432e923a8  runs/env_layout_04_scenario_s07_06_on_full_reorder.rec
9e5ef21d01c985bb42a085b51db6e11c  runs/env_layout_04_scenario_s07_06_on_single_task.rec
02aa03f5ea9ffc51d32b2c18fbbc7428  runs/env_layout_04_scenario_s09_01_on_full_reorder.rec
02aa03f5ea9ffc51d32b2c18fbbc7428  runs/env_layout_04_scenario_s09_01_on_single_task.rec
a4ef1a8b6ef3bae13ac7b1812e20951f  runs/env_layout_04_scenario_s09_02_on_full_reorder.rec
a4ef1a8b6ef3bae13ac7b1812e20951f  runs/env_layout_04_scenario_s09_02_on_single_task.rec
a2b5e87936b6e72fb8973ecbacf87fb9  runs/env_layout_04_scenario_s09_03_on_full_reorder.rec
a2b5e87936b6e72fb8973ecbacf87fb9  runs/env_layout_04_scenario_s09_03_on_single_task.rec
c6d1111603fa49d6eea8c5a4ccdf792c  runs/env_layout_04_scenario_s09_04_on_full_reorder.rec
c6d1111603fa49d6eea8c5a4ccdf792c  runs/env_layout_04_scenario_s09_04_on_single_task.rec
765ec364be327b28012089778523eda8  runs/env_layout_04_scenario_s09_05_on_full_reorder.rec
765ec364be327b28012089778523eda8  runs/env_layout_04_scenario_s09_05_on_single_task.rec
487377e6f559e4994e64bbf9a92b56d6  runs/env_layout_04_scenario_s09_06_on_full_reorder.rec
487377e6f559e4994e64bbf9a92b56d6  runs/env_layout_04_scenario_s09_06_on_single_task.rec
4516b3240c0fb246643ea556be9fe36f  runs/env_layout_04_scenario_s09_07_on_full_reorder.rec
4516b3240c0fb246643ea556be9fe36f  runs/env_layout_04_scenario_s09_07_on_single_task.rec
1c27e559b1fa17bb004f9e07a2e2884c  runs/env_layout_04_scenario_s09_08_on_full_reorder.rec
1c27e559b1fa17bb004f9e07a2e2884c  runs/env_layout_04_scenario_s09_08_on_single_task.rec
635745cb27a5888896c640f9143b1a82  runs/env_layout_04_scenario_s09_09_on_full_reorder.rec
635745cb27a5888896c640f9143b1a82  runs/env_layout_04_scenario_s09_09_on_single_task.rec
374e6d97d6ba6c8847adb9079da2fc0c  runs/env_layout_04_scenario_s09_10_on_full_reorder.rec
374e6d97d6ba6c8847adb9079da2fc0c  runs/env_layout_04_scenario_s09_10_on_single_task.rec
```
