## T-D cycle 1.5b: E8, E9, E10 and G1 — the logs from here on

Regenerated at cycle 1 session 1.5b (27 September 2026), superseding the "E6 amended" table below. CAUSE: E8 (the
advance tick a member at S = 1), E9 (s_exp by the Projector's attribution), E10 (the belief's evidence per phase
L(v·D)) and G1 (the guard on admission: `_clears_gate` also requires the leader's hypothesis adequacy to be adequate;
new refusals `none(leader_no_observation)`, `none(leader_inadequate)`); design_decisions.md, "T-D R and E", "1.5
rulings". Every `[IR]` line on a live tick differs (the new `leader_adequacy=` field; the tails under E8, E9); `[IR-dist]` differs
where standing now charges the belief (E10); decisions differ at admissions (G1) and wherever the belief moved.
World lines (the agents' per-tick lines) changed in none. The `.rec` streams are byte-identical to the table
below. Per-run diff and the acceptance: `analysis/td_stage1b/` (`baseline_diff.txt`, REPORT.md).

Command (from the repo root; the section headers below lost their commands at 7f4559a, the command is restated):
`analysis/tb1b_two_tables/sweep.sh analysis/tb1b_two_tables/sweep --cost_strategy realized --gate_strategy none --separation_stop false`

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_off | 9d2229e6ae945886574b2c261780b2a7 | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_on | 2c2a9d79ef4932252f3afffe47c0887b | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_off | 2824fd4ef817d8b87e358ea8ceca09dc | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_on | 5cafd2c3debfef3eece74af7be7f1073 | 329590c9c1249859bfe20d107588c50a |



## T-D Stage 1, E6 amended: stationary-phase members — the logs from here on

Regenerated at cycle 1 session 1.3b (27 September 2026), superseding the T-D R and E Stage 1 table. CAUSE: E6
amended (design_decisions.md, "T-D R and E"): a stationary phase within its priced duration is a member of the
adequacy test with S = 1. Only `[IR]` lines differ from the Stage 1 logs, and in them only the finding and the
tails (members added at S = 1; the belief and every existing member's S unchanged); every other line and the
`.rec` streams are byte-identical. Same commands as the section above.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| env_layout_08_scenario_s06_01_off | 8af7df2af74e80fae6e7bbf8a6fe592f | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_01_on | 2cf7861e47fa192870f8d8fb4b4d949e | 8cf0930761924a3aab1f1713f3f4bf29 |
| env_layout_08_scenario_s06_02_off | 8b02c0d458e525332d8d11136591b884 | 329590c9c1249859bfe20d107588c50a |
| env_layout_08_scenario_s06_02_on | e1d36827fb3bc877013eb17137265d4e | 329590c9c1249859bfe20d107588c50a |
