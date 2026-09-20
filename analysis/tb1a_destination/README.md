# analysis/tb1a_destination — baselines after T-B1a and its follow-ups (an item's destination table is a layout fact)

The plain sweep at the T-B1a HEAD (1e9b644): PYTHONHASHSEED=0; gate none, cost realized, stop off; the
regression five (s00 300, s10 450, s20 300, s30 200, s40 400 steps) and the evaluation fixtures (s50 / s70 /
s71, 300), prior off and on. `sweep/` (logs, git-ignored) replaces `analysis/g1_graded_evidence/sweep/` as
the baselines.

Regenerate from the repo root:

    H=analysis/tb1a_destination
    CONDS="s00 s10 s20 s30 s40" analysis/f1_robot_responsible/sweep.sh $H/sweep \
        --cost_strategy realized --gate_strategy none --separation_stop false
    analysis/f47_fixtures/sweep.sh $H/sweep --cost_strategy realized --gate_strategy none --separation_stop false

## Comparison with the pre-change HEAD (2a942cc)

The same sixteen runs at 2a942cc agree with `analysis/g1_graded_evidence/sweep/` on every CLAUDE.md grep;
only the `[run]` header differs (later header commits). Against them, the T-B1a logs are identical line for
line — header included — once the table part is removed from the old keys
(`,?kitting_table=kitting_table_0` and `, '?kitting_table': 'kitting_table_0'`), in all sixteen. Completion
from the world fact (t6_ablation/metrics.py), old = new:
s00 166, s10 418, s20 235, s30 160, s40 376, s50 235, s70 185, s71 201 (each prior off and on).

## md5 at T-B1a (superseded; 933cf40)

| log | md5 |
|---|---|
| s00_off | 6dfa36361762a69661ae0d81df3f322a |
| s00_on | f2999d96fe9a8c58332670f5cc4d6e1e |
| s10_off | ede2566822e34ae4c6eceb8a28a47a1b |
| s10_on | 65428ef4f887485e59ea0dbab6e37fd7 |
| s20_off | d2ebbcbb018c4e8700af2804eff758e1 |
| s20_on | c3d51e500a3b798a511733e63f0a8bd9 |
| s30_off | bab88e1da3aac958705b4151dc1bfffe |
| s30_on | d3b04b600a12d021e748a7239e6a661b |
| s40_off | fac30dcff0cd1dba118840d451a70218 |
| s40_on | 5920cb3d07210e50c59af18102c5fc90 |
| s50_off | d0aba7445714d2449f41e549a561268b |
| s50_on | bb09af697c2c49ece5c066dbb36a76b5 |
| s70_off | 39f8d97d18e7e86b66504f125871b442 |
| s70_on | b08ac981d66c326ca87ea57b21300c05 |
| s71_off | 00b297d44f3f1e3b5f6563a5c9c769eb |
| s71_on | 1844a1c6957442cdf5913e39de379a15 |

## T-B1a follow-up 2 — THE BASELINES from here on (1cbecb1)

`sweep/` now holds the logs of T-B1a follow-up 2, which supersede T-B1a's (same command). Follow-up 1
(determined_parameters, 62c7fc1) left the sixteen logs byte-identical to T-B1a's. Follow-up 2 restores the table
binding in the scenarios' task instances, so every task instance key carries `?kitting_table` again; the
hypothesis keys do not. Against T-B1a's logs, all sixteen are identical line for line once the table part is
removed from the keys (same two patterns as above): decisions, holds, `[IR]`, `[sep]` and completion unchanged
(s00 166, s10 418, s20 235, s30 160, s40 376, s50 235, s70 185, s71 201, both priors). With the prior on, no
fixture logs `matches no hypothesis`: the assigned tasks are admitted on the item.

| log | md5 |
|---|---|
| s00_off | 914d0b0fafe7f551b72895cba1ad99c4 |
| s00_on | ff65089364f9bb12b81166f8bc63a108 |
| s10_off | 67b9acf6c6ed6d72c654e20e1074b60f |
| s10_on | 0779cd7df4778662626f847c94930883 |
| s20_off | 7c8c777e0e12e0f597d06b71587f08d8 |
| s20_on | f0f2dc6d9a40c0cddafc914a0af39f72 |
| s30_off | 018d4978c108404c7727d2f981c2e872 |
| s30_on | a66fb62a659737442c17168a12f9c7d5 |
| s40_off | 642806be45f89084105a9e49c788ac22 |
| s40_on | 805f833350eefa25fd8f94ab5f41cf44 |
| s50_off | 6cb7d49ebc5c497ad9b44c020648dd3c |
| s50_on | 3408f9c14894a1ec9be487b590c82dd6 |
| s70_off | cbf5d29fa744e72a448ab473876a88b6 |
| s70_on | 8ff838519ebac10cb4c3ba831f696afe |
| s71_off | a93dde2c804f95466829d2d288d98a0a |
| s71_on | d0d26e17f469f28266158ecb00cf7893 |

## T-B2d — THE BASELINES from here on (79fb0ee): the `[run]` header names the strategy

`sweep/` now holds the sixteen logs regenerated at 79fb0ee (same command, `--strategy` left at its default,
`single_task`), which supersede follow-up 2's above. T-B2d made B3's strategy a run option and named it in the
`[run]` header, so that ONE line of every log changed: `[run] robot_0 strategy=single_task gate_strategy=...`.
Nothing else did: each log differs from follow-up 2's in exactly that line, and removing ` strategy=single_task`
from it restores follow-up 2's log byte for byte (all sixteen, and the four of `analysis/tb1b_two_tables/sweep/`).
No `full_reorder` baselines are recorded before T-B2c: until then `full_reorder` with `cost_strategy realized`
is a hybrid (design_decisions.md, "B3.B on plain cost: the internal queue stays in pool order, and until T-B2c
`full_reorder` is a hybrid").

| log | md5 |
|---|---|
| s00_off | 3230c5bd764e0523e76ceb665b21033e |
| s00_on | 7edc128545d3b7e50f5463955687709a |
| s10_off | b0f257001045c95325f2acd57059fa69 |
| s10_on | 91cc5e87f10a8976f5d49770b9d508ba |
| s20_off | 210126acefa694ae71e1aed74d9ba068 |
| s20_on | ea8fa4b76f11a07c93316057bee22646 |
| s30_off | 84136e8bc0423635aa1c2afcd5178ed2 |
| s30_on | 821b00ecee2463bce05f9a39a8cb122e |
| s40_off | 0bf2331b5e4a3c76a74c743957076c7e |
| s40_on | e0cad83d301bd7c347b396ad6139f77e |
| s50_off | 0002d7cc30a6da526682268554951f20 |
| s50_on | 5ee070644ff8b57cd8921b1611bdbdeb |
| s70_off | 1b51d98d7ab385f7f688e87bc5705601 |
| s70_on | 2e08ec7003a293de14d1368a5919bcdb |
| s71_off | 65b336a39b11e239caa99c93644ffcc9 |
| s71_on | 208d11f64e55323f0db0e099ba6d5042 |
