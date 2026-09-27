## T-D cycle 1.5b: E8, E9, E10 and G1 — the logs from here on

Regenerated at cycle 1 session 1.5b (27 September 2026), superseding the "E6 amended" table below. CAUSE: E8 (the
advance tick a member at S = 1), E9 (s_exp by the Projector's attribution), E10 (the belief's evidence per phase
L(v·D)) and G1 (the guard on admission: `_clears_gate` also requires the leader's hypothesis adequacy to be adequate;
new refusals `none(leader_no_observation)`, `none(leader_inadequate)`); design_decisions.md, "T-D R and E", "1.5
rulings". Every `[IR]` line on a live tick differs (the new `leader_adequacy=` field; the tails under E8, E9); `[IR-dist]` differs
where standing now charges the belief (E10); decisions differ at admissions (G1) and wherever the belief moved.
World lines (the agents' per-tick lines) changed in 8 of 20 (s03_01 single_task on/off, s05_01 both strategies on/off, s06_03 both strategies off). The `.rec` streams are byte-identical to the table
below. Per-run diff and the acceptance: `analysis/td_stage1b/` (`baseline_diff.txt`, REPORT.md).

Command (from the repo root; the section headers below lost their commands at 7f4559a, the command is restated):
`analysis/tb3_full_reorder/sweep.sh analysis/tb3_full_reorder/sweep`

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_off | 014e7d4db38f6f043f9881d35af69c89 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_full_reorder_on | 28bf81dc4d3f8b3536ff6023149e16c6 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_off | 4d047d15a6b6bd77221358c163d483dc | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_on | 521ebeac3f97ab4106f1174c6198460f | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_07_scenario_s05_01_full_reorder_off | e2b722adea65ff98a60aa85e993bf2d3 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_full_reorder_on | f6a9ecbd880e01275de6655c5ee88381 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_off | e320797265ceb5a4572adcfdc5a4b27a | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_on | 24d53d63e6a5fccbd14c13e05e5c74e8 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_08_scenario_s06_01_full_reorder_off | 98d32dbd4fe4ccdf6f4c5d00f25a2ccc | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_full_reorder_on | 25a26eb6b44f3779dee9f94868554765 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_off | 9d2229e6ae945886574b2c261780b2a7 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_on | 2c2a9d79ef4932252f3afffe47c0887b | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_full_reorder_off | 3e4da85ded842e2fcaf85bcee0498b7b | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_full_reorder_on | d71ffb6539ffd04dcef4dc26ea0bf35e | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_off | 2824fd4ef817d8b87e358ea8ceca09dc | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_on | 5cafd2c3debfef3eece74af7be7f1073 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_03_full_reorder_off | 3ade34d4da811f67c654b7a1a2f7ac8c | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_full_reorder_on | dbd8e0e7adab2415edd8d7db9209c7f7 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_off | 7730d87a85035f48362cc265d34666b5 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_on | 3a15f70a05d37e5e4d8e56134c6eccce | b9f1a0ec26cfa8c022b9951e9ec1b34b |



## T-D Stage 1, E6 amended: stationary-phase members — the logs from here on

Regenerated at cycle 1 session 1.3b (27 September 2026), superseding the T-D R and E Stage 1 table. CAUSE: E6
amended (design_decisions.md, "T-D R and E"): a stationary phase within its priced duration is a member of the
adequacy test with S = 1. Only `[IR]` lines differ from the Stage 1 logs, and in them only the finding and the
tails (members added at S = 1; the belief and every existing member's S unchanged); every other line and the
`.rec` streams are byte-identical. Same commands as the section above.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_03_scenario_s03_01_full_reorder_off | a1be6065a3169f88d3a31f055af8b5a8 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_full_reorder_on | 2b40778b258aacbb239be453a650b9d0 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_off | 5ac10a84262310b487474e3a503abb80 | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_03_scenario_s03_01_single_task_on | cc2407b0a7baa038c827dce6ad07ae1a | 9f6d010e2fbc537952fa6ece4e96f469 |
| env_layout_07_scenario_s05_01_full_reorder_off | ed09ebd80a196948d6ad0e84a87b2745 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_full_reorder_on | f58c3a3e89c3b73eb3ba60b5e14b947b | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_off | a76d2899a4aa89576776fbbad617e3f2 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_07_scenario_s05_01_single_task_on | 7fd86fd9b82820a2c1450ebb224c2d05 | dab078d5ca51e5b378054ee6a60ccca7 |
| env_layout_08_scenario_s06_01_full_reorder_off | be05b6251fcc3c5547999bcb30d0f3a7 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_full_reorder_on | b9f756085305e49091005cbde9dc27ba | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_off | 8af7df2af74e80fae6e7bbf8a6fe592f | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_single_task_on | 2cf7861e47fa192870f8d8fb4b4d949e | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_full_reorder_off | 259da95765afaeaea012970cc7a7c32c | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_full_reorder_on | 995107cb8473be46307af9122cac5b6d | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_off | 8b02c0d458e525332d8d11136591b884 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_single_task_on | e1d36827fb3bc877013eb17137265d4e | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_03_full_reorder_off | 94a9b707f68c58585001aa0cd16edecb | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_full_reorder_on | d395d91a396a323670b846f0ffbf1c88 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_off | 386969055f6f4028f019bdd5fc14d357 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_single_task_on | d11fbca7c112a7e847fe5fd0478a2d63 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
