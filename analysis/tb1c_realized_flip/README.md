## T-D cycle 1.5b: E8, E9, E10 and G1 — the logs from here on

Regenerated at cycle 1 session 1.5b (27 September 2026), superseding the "E6 amended" table below. CAUSE: E8 (the
advance tick a member at S = 1), E9 (s_exp by the Projector's attribution), E10 (the belief's evidence per phase
L(v·D)) and G1 (the guard on admission: `_clears_gate` also requires the leader's hypothesis adequacy to be adequate;
new refusals `none(leader_no_observation)`, `none(leader_inadequate)`); design_decisions.md, "T-D R and E", "1.5
rulings". Every `[IR]` line on a live tick differs (the new `leader_adequacy=` field; the tails under E8, E9); `[IR-dist]` differs
where standing now charges the belief (E10); decisions differ at admissions (G1) and wherever the belief moved.
World lines (the agents' per-tick lines) changed in 1 of 8 (s06_03 realized off). The `.rec` streams are byte-identical to the table
below. Per-run diff and the acceptance: `analysis/td_stage1b/` (`baseline_diff.txt`, REPORT.md).

Command (from the repo root; the section headers below lost their commands at 7f4559a, the command is restated):
`analysis/tb1c_realized_flip/sweep.sh analysis/tb1c_realized_flip/sweep`

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_plain_off | 5441e3e44bb86b2d47007a4792dd1739 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_plain_on | c5c8964185e3cc2d317ed86c935fb7e7 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_off | 98d32dbd4fe4ccdf6f4c5d00f25a2ccc | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_on | 25a26eb6b44f3779dee9f94868554765 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_03_plain_off | 2f418f3ff8dfc851d5a3e3981fc39969 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_plain_on | 965c827855eaa688a3fc51ba64099e79 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_off | 3ade34d4da811f67c654b7a1a2f7ac8c | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_on | dbd8e0e7adab2415edd8d7db9209c7f7 | b9f1a0ec26cfa8c022b9951e9ec1b34b |



## T-D Stage 1, E6 amended: stationary-phase members — the logs from here on

Regenerated at cycle 1 session 1.3b (27 September 2026), superseding the T-D R and E Stage 1 table. CAUSE: E6
amended (design_decisions.md, "T-D R and E"): a stationary phase within its priced duration is a member of the
adequacy test with S = 1. Only `[IR]` lines differ from the Stage 1 logs, and in them only the finding and the
tails (members added at S = 1; the belief and every existing member's S unchanged); every other line and the
`.rec` streams are byte-identical. Same commands as the section above.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_plain_off | f1ceaf546f6138df90126d3de0dd0cbb | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_plain_on | 9a2721aa3fc921ff9333768e00ccda02 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_off | be05b6251fcc3c5547999bcb30d0f3a7 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_realized_on | b9f756085305e49091005cbde9dc27ba | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_03_plain_off | f0d15133ca437f4bc11c1da732c73efe | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_plain_on | 0951585744111e81e91f444c2128d76c | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_off | 94a9b707f68c58585001aa0cd16edecb | b9f1a0ec26cfa8c022b9951e9ec1b34b |
| env_layout_08_scenario_s06_03_realized_on | d395d91a396a323670b846f0ffbf1c88 | b9f1a0ec26cfa8c022b9951e9ec1b34b |
