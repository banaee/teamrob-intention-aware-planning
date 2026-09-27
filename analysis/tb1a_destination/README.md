## T-D cycle 1.5b: E8, E9, E10 and G1 — the logs from here on

Regenerated at cycle 1 session 1.5b (27 September 2026), superseding the "E6 amended" table below. CAUSE: E8 (the
advance tick a member at S = 1), E9 (s_exp by the Projector's attribution), E10 (the belief's evidence per phase
L(v·D)) and G1 (the guard on admission: `_clears_gate` also requires the leader's hypothesis adequacy to be adequate;
new refusals `none(leader_no_observation)`, `none(leader_inadequate)`); design_decisions.md, "T-D R and E", "1.5
rulings". Every `[IR]` line on a live tick differs (the new `leader_adequacy=` field; the tails under E8, E9); `[IR-dist]` differs
where standing now charges the belief (E10); decisions differ at admissions (G1) and wherever the belief moved.
World lines (the agents' per-tick lines) changed in 10 of 16 (s01_01 off, s03_01 on/off, s01_06 off, s04_01 off, s03_06 off, s05_01 on/off, s05_02 on/off). The `.rec` streams are byte-identical to the table
below. Per-run diff and the acceptance: `analysis/td_stage1b/` (`baseline_diff.txt`, REPORT.md).

Command (from the repo root; the section headers below lost their commands at 7f4559a, the command is restated):
`analysis/tb1a_destination/sweep.sh analysis/tb1a_destination/sweep`

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_01_scenario_s01_01_off | 2ceb544eaeabce7bb4c6555a9fa8e470 | 5c7835ba3417ff28b5d3caf1d00d906e |
| env_layout_01_scenario_s01_01_on | c3f553a4c0a8010490c864af7b5ef3a9 | 5c7835ba3417ff28b5d3caf1d00d906e |
| env_layout_02_scenario_s02_01_off | 443f20a8c5563bd3193e3eba251bd3f1 | 3e5fd9cd96dad4e0c56cfc626a770ff4 |
| env_layout_02_scenario_s02_01_on | eaedb0a4717210c6f3830ff34725983c | 3e5fd9cd96dad4e0c56cfc626a770ff4 |
| env_layout_03_scenario_s03_01_off | 4d047d15a6b6bd77221358c163d483dc | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_on | 521ebeac3f97ab4106f1174c6198460f | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_04_scenario_s01_06_off | e8ee3bf0305def3a0bf823e4ca445d7c | 65d234649396c9ab242841050082e9b0 |
| env_layout_04_scenario_s01_06_on | 5028b8395897b2b6d9e041d12ce74586 | 65d234649396c9ab242841050082e9b0 |
| env_layout_05_scenario_s04_01_off | ad8b7fe68e32d2bda74f5ac07558858b | f6da9d345530212df9b0446aa53d1f1e |
| env_layout_05_scenario_s04_01_on | 5f61ed2cf0a750995235897b0250d3e9 | f6da9d345530212df9b0446aa53d1f1e |
| env_layout_06_scenario_s03_06_off | 21ed5258eb50bfa3688f52bcfe6b7a0d | 3e4fd412ba39ddd3267d1d37089beaac |
| env_layout_06_scenario_s03_06_on | 6b14c110ec7df4c3f27a6c76e632796b | 3e4fd412ba39ddd3267d1d37089beaac |
| env_layout_07_scenario_s05_01_off | e320797265ceb5a4572adcfdc5a4b27a | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_on | 24d53d63e6a5fccbd14c13e05e5c74e8 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_02_off | 827a7a7aa07ad8370fba7a2f8ea662a0 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_02_on | dd7e7b22357386a157663163bfbadcc9 | dab078d5ca51e5b378054ee6a60ccca7 |



## T-D Stage 1, E6 amended: stationary-phase members — the logs from here on

Regenerated at cycle 1 session 1.3b (27 September 2026), superseding the T-D R and E Stage 1 table. CAUSE: E6
amended (design_decisions.md, "T-D R and E"): a stationary phase within its priced duration is a member of the
adequacy test with S = 1. Only `[IR]` lines differ from the Stage 1 logs, and in them only the finding and the
tails (members added at S = 1; the belief and every existing member's S unchanged); every other line and the
`.rec` streams are byte-identical. Same commands as the section above.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_01_scenario_s01_01_off | c57f7400c0ab272b9a26d3da02a34ff6 | 5c7835ba3417ff28b5d3caf1d00d906e |
| env_layout_01_scenario_s01_01_on | 44a138d5c95734d9b802f448b971e410 | 5c7835ba3417ff28b5d3caf1d00d906e |
| env_layout_02_scenario_s02_01_off | d6cbf514ac0e19448ceee8ce14145496 | 3e5fd9cd96dad4e0c56cfc626a770ff4 |
| env_layout_02_scenario_s02_01_on | 83df35d5523fd26f51963c26fa975f50 | 3e5fd9cd96dad4e0c56cfc626a770ff4 |
| env_layout_03_scenario_s03_01_off | 5ac10a84262310b487474e3a503abb80 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_on | cc2407b0a7baa038c827dce6ad07ae1a | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_04_scenario_s01_06_off | d4adcd01a3e48361795109f00e52738b | 65d234649396c9ab242841050082e9b0 |
| env_layout_04_scenario_s01_06_on | 4eaf7366b0ed7573a4766b881d38f1e9 | 65d234649396c9ab242841050082e9b0 |
| env_layout_05_scenario_s04_01_off | b6adfa1292699a54168ad27834a94a2b | f6da9d345530212df9b0446aa53d1f1e |
| env_layout_05_scenario_s04_01_on | 43dc033ef1b2339706c182a70db76827 | f6da9d345530212df9b0446aa53d1f1e |
| env_layout_06_scenario_s03_06_off | 65492364dce8e5df67845605dc8c7033 | 3e4fd412ba39ddd3267d1d37089beaac |
| env_layout_06_scenario_s03_06_on | 91eea63f54f8ed74fea260d4f2ba9cc9 | 3e4fd412ba39ddd3267d1d37089beaac |
| env_layout_07_scenario_s05_01_off | a76d2899a4aa89576776fbbad617e3f2 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_on | 7fd86fd9b82820a2c1450ebb224c2d05 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_02_off | d4a6e31d44261846a79176a10d232de5 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_02_on | 74b78adc6b319f10dc1107fb5d6ce932 | dab078d5ca51e5b378054ee6a60ccca7 |
