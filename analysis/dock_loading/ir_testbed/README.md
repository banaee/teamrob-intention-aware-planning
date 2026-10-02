# The IR test-bed on dock_loading (T-G stage 1)

The data and figures of this set (.json, .csv, .png) are not in git (Hadi, 2 October 2026). They are regenerated
by the set's run script (`analysis/instruments/ir_testbed/run.sh dock_loading`). A byte comparison uses the local copy or the outside copy,
`/home/hadi/teamrob_analysis_2026-10-02/` (the whole of analysis/ as it was at 38d66ea).

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

## Runs of the controlled set (git-ignored logs; md5s at the controlled runs, 1 October 2026)

```
73db1cdde82c8b297bcfacedcf51a711  runs/env_layout_02_scenario_s02_02_on.log
e4533fff5f0e1ded6704f6c3411f327e  runs/env_layout_02_scenario_s02_03_on.log
95a24f4daa329e1bc18ae1ec3ba40958  runs/env_layout_02_scenario_s02_04_on.log
683940f501f38f6259a66a38c2e89f26  runs/env_layout_02_scenario_s02_05_on.log
cb42fc8d157e5f965e546068dd29f069  runs/env_layout_02_scenario_s02_06_on.log
a8e921588ab2612a5e40fc47ebf9f384  runs/env_layout_02_scenario_s02_07_on.log
09f0d623cfcb463840cdac99a61ecdcb  runs/env_layout_02_scenario_s02_08_on.log
8d1a3df60a31897cab70986b4c9d2fd5  runs/env_layout_02_scenario_s02_09_on.log
48d20ac01b72eb8bb21ab5804f6f4815  runs/env_layout_02_scenario_s02_10_on.log
75d7a80c1a92eed3359fc893d7c78f05  runs/env_layout_02_scenario_s02_11_on.log
5224068a05ec78be8fad4784607c0d39  runs/env_layout_02_scenario_s02_12_on.log
6bd1507a9634c3fe80fafc8ef6695ca4  runs/env_layout_02_scenario_s02_13_on.log
46625f74b3a4ab85ae1ded18391b6461  runs/env_layout_02_scenario_s02_14_on.log
c7447254816caafdf9ec2ae3a6a557ad  runs/env_layout_02_scenario_s02_15_on.log
e2a8d2bb3bf796ed5d6510c7d25d309d  runs/env_layout_03_scenario_s04_02_on.log
f13ae8baaa5c384514d60068e4885748  runs/env_layout_03_scenario_s04_03_on.log
16c9340962b2aea2eb71ee029216998b  runs/env_layout_03_scenario_s04_04_on.log
0e6efcd1959ee6d28c252c33fecb446b  runs/env_layout_03_scenario_s04_05_on.log
a78088b4d668d93fab56b578964ab4bb  runs/env_layout_03_scenario_s04_06_on.log
15613d90f4b2334c8bf17c1c51383664  runs/env_layout_03_scenario_s04_07_on.log
5581f07f4ff89a6b00d5438fc0312791  runs/env_layout_03_scenario_s04_08_on.log
dbdfae4d13f4ca0122bd218b0bd1cfbd  runs/env_layout_03_scenario_s04_09_on.log
ab46185b1d20312b5ba3741a23ec4c67  runs/env_layout_03_scenario_s04_10_on.log
634d89c7c4276a146b52ffea1a57ac15  runs/env_layout_03_scenario_s04_11_on.log
ac6d47eab51e9e559b7f7266fd514b12  runs/env_layout_03_scenario_s04_12_on.log
a75b972d402e26c52adb72a2c8f8a396  runs/env_layout_03_scenario_s04_13_on.log
2f68a4f01915cc30319101c7a2fb742b  runs/env_layout_03_scenario_s04_14_on.log
2007794cc72aed749ea88d7836105af6  runs/env_layout_03_scenario_s04_15_on.log
6cacdddc4e32ae7299879dcf2245e9f3  runs/env_layout_04_scenario_s06_02_on.log
37b300bd1c030376002a5c2a9a3a1f6d  runs/env_layout_04_scenario_s06_03_on.log
2e50767b6c529a9f212e1a20f21696d0  runs/env_layout_04_scenario_s06_04_on.log
f6f3094bb921fe741381deb4b8ead127  runs/env_layout_04_scenario_s06_05_on.log
b958a4511ca96858d2033f19d5058321  runs/env_layout_04_scenario_s06_06_on.log
af7af0619cc0eacb747a629957925028  runs/env_layout_04_scenario_s06_07_on.log
12020b48b6fda941f6c814bfe9b5c94a  runs/env_layout_04_scenario_s06_08_on.log
04a2ad158a6fe01d0a8481b2bd2356e2  runs/env_layout_04_scenario_s06_09_on.log
5731f6a602fb904c2821201874ff61b7  runs/env_layout_04_scenario_s06_10_on.log
786218ae003079ed9c37d0e9edca355a  runs/env_layout_04_scenario_s06_11_on.log
b6e5ba25aab9605e7138afe8beef36a8  runs/env_layout_04_scenario_s06_12_on.log
2a1fe16426a3f72058c0a15905f298a4  runs/env_layout_04_scenario_s06_13_on.log
95c554b63589f7eb0aacd5f559656ab5  runs/env_layout_04_scenario_s06_14_on.log
45bcc3cf2bfd42683d8b924e80b95a22  runs/env_layout_04_scenario_s06_15_on.log
8189182557c813c13a90291f13184682  runs/env_layout_02_scenario_s02_02_on.rec
440d8f1a93a4197672db07d89941365e  runs/env_layout_02_scenario_s02_03_on.rec
1af4d32105c48ff59f0788f22a799fb9  runs/env_layout_02_scenario_s02_04_on.rec
af257ff2ed09dc0a2f4563ba9db78352  runs/env_layout_02_scenario_s02_05_on.rec
c892e5b4fb7cdf8ee54eeee438b6656e  runs/env_layout_02_scenario_s02_06_on.rec
f6397be589bef36d53674c55c66afa38  runs/env_layout_02_scenario_s02_07_on.rec
dc135341ed1c37812847b7cb2057a06c  runs/env_layout_02_scenario_s02_08_on.rec
8f5849a84c871439cfdf387948a614d8  runs/env_layout_02_scenario_s02_09_on.rec
99d14fffdb424b3c6d48180b1cb894c5  runs/env_layout_02_scenario_s02_10_on.rec
c382b6e14c7cccb1ab35911876837a3f  runs/env_layout_02_scenario_s02_11_on.rec
1b131baee07b73fe00b8394723d21440  runs/env_layout_02_scenario_s02_12_on.rec
045425f38604dbee3bce2a031ffad433  runs/env_layout_02_scenario_s02_13_on.rec
f380bf175b5961f702550f1a0498bc2c  runs/env_layout_02_scenario_s02_14_on.rec
a1b90ac6d7ce31008e03e1e280cfae5b  runs/env_layout_02_scenario_s02_15_on.rec
b286b443228cb3c5d8e3f6bb192f7ccc  runs/env_layout_03_scenario_s04_02_on.rec
083fe98a584b1ccb8d9b32e418dd3221  runs/env_layout_03_scenario_s04_03_on.rec
1af4d32105c48ff59f0788f22a799fb9  runs/env_layout_03_scenario_s04_04_on.rec
03efea3dab4f6fbfcd4557dc86fc401f  runs/env_layout_03_scenario_s04_05_on.rec
f46d8c135b51f27763ed8920de70eb89  runs/env_layout_03_scenario_s04_06_on.rec
ac54ef36279f8aa0c0ae237806671a32  runs/env_layout_03_scenario_s04_07_on.rec
a1b694a04c6471ebd66c9746fda8cb6a  runs/env_layout_03_scenario_s04_08_on.rec
27d3850cd788b39ff08bf590efb15e96  runs/env_layout_03_scenario_s04_09_on.rec
7d5a9a527fed01df19c89cde59d50dee  runs/env_layout_03_scenario_s04_10_on.rec
3f3fc474906d08d51517bf746eaf57ac  runs/env_layout_03_scenario_s04_11_on.rec
2395d34e1d7a99e64e810b486399e5cf  runs/env_layout_03_scenario_s04_12_on.rec
64854fd22c681879fd9731b19f1705bd  runs/env_layout_03_scenario_s04_13_on.rec
f380bf175b5961f702550f1a0498bc2c  runs/env_layout_03_scenario_s04_14_on.rec
2a1c77e70f0fed7157bc0cacb0267036  runs/env_layout_03_scenario_s04_15_on.rec
fbe51c2810f2298bf10fb8c4c7eafe41  runs/env_layout_04_scenario_s06_02_on.rec
fbc7f5a445a516b89fc02f7735871541  runs/env_layout_04_scenario_s06_03_on.rec
d8c8dc9e733f5bae111b866712002291  runs/env_layout_04_scenario_s06_04_on.rec
56cb131fb3b31d85f91b9167c0237757  runs/env_layout_04_scenario_s06_05_on.rec
267fdea56b8c91a9d8d198cf06eb9177  runs/env_layout_04_scenario_s06_06_on.rec
b7429ed79c7093787581f52b37416555  runs/env_layout_04_scenario_s06_07_on.rec
313e878656b2a8e21968ee2ab9324c00  runs/env_layout_04_scenario_s06_08_on.rec
27d61256df322cfca27953aa9cd14450  runs/env_layout_04_scenario_s06_09_on.rec
4482c797527e2260bd7a30be36dec5bf  runs/env_layout_04_scenario_s06_10_on.rec
d67ca4e8bb84fb9226c3fdbc68edac4f  runs/env_layout_04_scenario_s06_11_on.rec
f4617adcc13dd0c22e71eab9376c254d  runs/env_layout_04_scenario_s06_12_on.rec
172943cadccabfcf3eba9134d3a5bc4a  runs/env_layout_04_scenario_s06_13_on.rec
aeed6d20cedafe764fc590683234190d  runs/env_layout_04_scenario_s06_14_on.rec
05807f9313023ccc28a9b6af7c35913a  runs/env_layout_04_scenario_s06_15_on.rec
```

## Runs of the mixed set (git-ignored logs; md5s at the mixed runs, 2 October 2026)

```
0edd555a654ae673a62f78067cab99fd  runs/env_layout_02_scenario_s02_16_on.log
5e3b8207d2df73ab20a511d1710678eb  runs/env_layout_02_scenario_s02_17_on.log
d7c8202a1295a8bf85c8e064ec7f4726  runs/env_layout_02_scenario_s02_18_on.log
df4b18de4a4b2a64d16fb1e5f41717fb  runs/env_layout_02_scenario_s02_19_on.log
7d6eef385b33b9785f0c61aef2d7ba0d  runs/env_layout_03_scenario_s04_16_on.log
ed394544c37869e507c799c95d62402c  runs/env_layout_03_scenario_s04_17_on.log
402cc55fe17abc6697a38a5a8cd09c23  runs/env_layout_03_scenario_s04_18_on.log
e66765cace548ea216d201145eb292f4  runs/env_layout_03_scenario_s04_19_on.log
946935375de3c198c582ef9b70d7bb72  runs/env_layout_04_scenario_s06_16_on.log
adfb696f0bc2de4d0a3a58b19234f12b  runs/env_layout_04_scenario_s06_17_on.log
1a4e8555c764afb4457ad24d58b61b13  runs/env_layout_04_scenario_s06_18_on.log
9c416d6e128901f2173ac2041730813a  runs/env_layout_04_scenario_s06_19_on.log
07398fbda10e6d40932833fa6eccc61a  runs/env_layout_02_scenario_s02_16_on.rec
6a031043227b120330975cf40d486eb8  runs/env_layout_02_scenario_s02_17_on.rec
dc85950d8bf3f540e1b8289261491c12  runs/env_layout_02_scenario_s02_18_on.rec
1a6a44ca235cc8f0c95357e8b6d8a444  runs/env_layout_02_scenario_s02_19_on.rec
c4a9f343c413befa37c5be823ee57fc8  runs/env_layout_03_scenario_s04_16_on.rec
e26753a0a85bc5fcaec5210987812876  runs/env_layout_03_scenario_s04_17_on.rec
883ce3a256a82b9af31987391d33105f  runs/env_layout_03_scenario_s04_18_on.rec
c561f544bbed0ffacc530d807014ae6d  runs/env_layout_03_scenario_s04_19_on.rec
898a8a6d1d39a1fafed0193df3794bc4  runs/env_layout_04_scenario_s06_16_on.rec
86c38b3b8188048b2f3cad1acdd3bf04  runs/env_layout_04_scenario_s06_17_on.rec
8b624615562c23afc3076ee8f5f52625  runs/env_layout_04_scenario_s06_18_on.rec
d7035dd3b18639cfe78e00d688091982  runs/env_layout_04_scenario_s06_19_on.rec
```
