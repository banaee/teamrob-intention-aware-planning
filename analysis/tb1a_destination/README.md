# analysis/tb1a_destination — baselines after T-B1a (an item's destination table is a layout fact)

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

## md5 (`sweep/`)

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
