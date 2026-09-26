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

## T-B Q7 (de70e98) — THE BASELINES from here on: the body spends every completion tick it states

`sweep/` now holds the sixteen logs regenerated at de70e98, superseding T-B2d's above, from the same command.
T-B Q7 made the Mesa executor spend the completion ticks a reload used to cancel: the acknowledgement after
the robot's grasp, and under the general rule a completed action's acknowledgement and a finished task's
completion tick at any reload (`docs/design_decisions.md`, "A reload never cancels a completion tick the body
states"). Nothing in `shared/` changed.

FOR A READER COMPARING WITH THE RECORD: every completion tick recorded above — and in the reports that cite
these fixtures — IS ONE TICK SHORTER PER ROBOT DELIVERY than the behaviour from here on, less where a decided
hold carried the tick. The robot's plan and its decisions are not otherwise different.

Completion from the world fact (`analysis/t6_ablation/metrics.py`), T-B2d → T-B Q7, each prior off and on:

| fixture | s00 | s10 | s20 | s30 | s40 | s50 | s70 | s71 |
|---|---|---|---|---|---|---|---|---|
| T-B2d | 166 | 418 | 235 | 160 | 376 | 235 | 185 | 201 |
| T-B Q7 | 169 | 422 | 237 | 161 | 379 | 237 | 186 | 203 |
| deliveries | 3 | 4 | 3 | 2 | 3 | 3 | 2 | 2 |

One tick per delivery, except where a hold carried the tick: s20 / s50 and s30 (δ = 1 at the post-grasp
decision, the acknowledgement taken as its first tick) and s70 (the hold at 61 / 60 re-realized 2 → 1 from a
robot standing there one tick later). The human's lines are byte-identical to T-B2d's in all sixteen, and the
`[IR]` lines are identical with the prior on; with it off they move where the robot's own timing reaches the
WorldState the recognizer reads — a carried item's position and task completion as a world fact
(`docs/TODOS_AND_DEFERRED.md`, TODO-88). Two decision sequences change beyond the shift, both traced in
`docs/design_decisions.md`: s10 (both priors) and s00_on, where a trigger that used to land on a cancelled
completion tick now lands on a spent one.

| log | md5 |
|---|---|
| s00_off | 6f522a03d9cafbc2ac839bab0ee724a3 |
| s00_on | ab7c0a8528f1607560aa109ebb12143e |
| s10_off | 7a90201e5e5528104e63a03d4061f9f1 |
| s10_on | fc32c37a34d01402d88d42d9561110ff |
| s20_off | 8ed5af00ede1e7f92c4598ba806159d9 |
| s20_on | a98d844f3d1773f0cfb591b3f994b3ce |
| s30_off | 14601bfef447afdb0810278fdd5c0188 |
| s30_on | e0448eca611b4fb12578e00a0f680df5 |
| s40_off | 609ed0de66f167d266a406a090fd3563 |
| s40_on | f25b80d87a2e04e6139b0291c3a4de74 |
| s50_off | a412bb391532b0490ea4ff287734b422 |
| s50_on | 1e22ee999c5378f38fb25e5709bd3671 |
| s70_off | d61892811de60b8f128c687b9f2193ff |
| s70_on | e5596b4d042d170537890d3a56d5c788 |
| s71_off | 4a6b769e8c46bcabd75af48c43d83d41 |
| s71_on | 909bcee05faf0be3368381cec7b448be |

## D3 (dd880be) — THE BASELINES from here on: `task_committed` is not a trigger

Regenerated at dd880be with the same command, superseding the table above. Only the trigger set changed
(`shared/meta_planner.py`, `evaluate_triggers()`: `task_committed` removed; `docs/design_decisions.md`, "D3:
task_committed is not a trigger"). Against the previous logs, checked per tick: every `[sep]` line, every human
line, every `[IR] step=` and `[IR-dist]` line and the `[run]` header are byte-identical, and so is completion. What
changed: the `[meta*]` lines of the removed `task_committed` decisions (43 in these logs); and the executor's
bookkeeping, positions and ticks identical — no `_load_plan` at the grasp (the removed decision's reload of
`deliver_already_held`), a later `continue_plan` mapping `action_index 2->0` / `3->1` instead of `0->0` / `1->1`,
and `_on_task_complete` on the 4-action plan (`action_index=4 plan_len=4`) instead of the 2-action one.

HOLDS PLACED BY `task_committed` in the previous baselines (their `[hold] … trigger=` field), all 1 tick, all gone:
s20_off / s20_on at tick 31, s50_off / s50_on at tick 31, s30_off / s30_on at tick 47. At each of those ticks the
robot, at the same position, spends the `pick_up` acknowledgement instead of the stand (`action=move_to
micro=stand` → `action=pick_up micro=None`), and the hold's `[hold]` start / end lines are gone. Every other hold
is unchanged.

| log | md5 |
|---|---|
| s00_off | 16f4c3ffb63b94c3ad5c361454e5cfef |
| s00_on | f60b6783ddb06d13688f09afd737669a |
| s10_off | 6e55ff7907c6e0917c2949ebf740d547 |
| s10_on | 774e1ca891c726de0a1c1581dd5ba103 |
| s20_off | d1dea6a5f4fed9140b07044ea1ef7a1b |
| s20_on | 36e8f7cab47250cf91c412bfeda56933 |
| s30_off | 6610f3822d250906aebc216ad78b0d59 |
| s30_on | b0bb633ffd8aeb3563e1ef7b5e37cfda |
| s40_off | b39736f56d97621237580c1316daaff1 |
| s40_on | dd2bcac3a6a6082f7cc6cab4fb142108 |
| s50_off | f0ff48006e743e3b8902d385a4a37988 |
| s50_on | 3d2fdebda9988ac0fc5b856962508e2c |
| s70_off | e02a25a2cff90eaf1dce9afa071ebc42 |
| s70_on | 8c24b8e30e4d5d69ed7681d63e171d88 |
| s71_off | 04dc790078cc570fc3c35cdff02b7b86 |
| s71_on | 1ae17d985f9a4cb92fefebc9d19e9187 |

## T-C2b (06093ee): the action-level human executor — the logs from here on

Regenerated at 06093ee with the same command, superseding the table above. CAUSE: the human's per-task completion
tick is dropped (`docs/design_decisions.md`, "The human action script (T-C1, decided)", AS BUILT T-C2b): its
executor is action-level and spends no tick between two tasks, and the human projection no longer carries that tick
(`HUMAN_TASK_COMPLETION_LATENCY` = 0). Against the previous logs every human line is identical once the human is
one tick earlier per task it completed before that tick (`task=` now `None`; the `_on_task_complete: human_0`
line and the human's `[planner]` lines are gone, one `[human] … primitive` line per primitive is new). Where the
human projection's shorter end reaches a hold, the hold is one tick shorter — the ruling in the AS BUILT note, not a
defect. Per log: the human's dropped ticks | first tick a world line (`[sep]`, `[IR] step=`, robot) differs |
completion (world tick) old -> new | holds (start:planned) old -> new.

| log | dropped | first diff | completion | holds old | holds new |
|---|---|---|---|---|---|
| s00_off | 80, 144 | 80 | 169 -> 169 | - | - |
| s00_on | 80, 144 | 80 | 169 -> 169 | - | - |
| s10_off | 77, 156, 313, 367 | 77 | 422 -> 422 | - | - |
| s10_on | 77, 156, 313, 367 | 77 | 422 -> 422 | - | - |
| s20_off | 56, 124 | 27 | 237 -> 236 | 20:8 | 20:7 |
| s20_on | 56, 124 | 18 | 237 -> 236 | 11:8 | 11:7 |
| s30_off | 76, 123 | 33 | 161 -> 160 | 27:7 | 27:6 |
| s30_on | 76, 123 | 29 | 161 -> 160 | 23:7 | 23:6 |
| s40_off | 117, 186, 209, 230, 333 | 117 | 379 -> 379 | - | - |
| s40_on | 117, 186, 209, 230, 333 | 117 | 379 -> 379 | - | - |
| s50_off | 56, 124, 180 | 27 | 237 -> 236 | 20:8 | 20:7 |
| s50_on | 56, 124, 180 | 18 | 237 -> 236 | 11:8 | 11:7 |
| s70_off | 56, 97, 145 | 56 | 186 -> 185 | 61:1 | - |
| s70_on | 56, 97, 145 | 56 | 186 -> 185 | 60:1 | - |
| s71_off | 56, 97, 145 | 56 | 203 -> 203 | 23:32 | 23:31 |
| s71_on | 56, 97, 145 | 56 | 203 -> 203 | 23:32 | 23:31 |

| log | md5 |
|---|---|
| s00_off | 0a1373714b265d9bd74ffeba9345460b |
| s00_on | 357c21b0d80dec9f0c2bddc382067bb0 |
| s10_off | 59089a5b605f2182d3a474873cd155a4 |
| s10_on | 90a6b95db50183ea16d4172aa087ee13 |
| s20_off | e7b13670c6b384ad1113da38885c2746 |
| s20_on | a43cfcaea0d171713e50c575d8edd8e0 |
| s30_off | 7c5a7d40ab3c89394af3dc7ac74af624 |
| s30_on | 5b9a8bbe87246849934fb4fad788593e |
| s40_off | 98344452c657a8c5009d4c72b0aec5d4 |
| s40_on | ab3875e49cdbc98129040b6de204ec03 |
| s50_off | 3108b07ed64975872c9d867301841ddb |
| s50_on | 98499f8f8bd224e9aeb55a79866142c5 |
| s70_off | ba4ed101f2177b0ae037352d64b8f875 |
| s70_on | cac5f1f9ce11892656a21b7e9960bde4 |
| s71_off | 962f51ae814cdbdf71edd0546784cea8 |
| s71_on | d47cc020e9d358ff2712e0a72db5bcca |

## T-H3: the human's script on the stack machine — the logs from here on

Regenerated after T-H3 with the same command, superseding the T-C2b table. CAUSE: every scenario's human script is a
`Script` run by the human's stack machine (`docs/design_decisions.md`, "T-H: the human behaviour model", as built
T-H3); the C1 list form is deleted. Against the T-C2b logs every line outside `[human]` is byte-identical, the human's
step lines included: the robot sees the same body. The `[human] … primitive k: <action>` lines are replaced by the
record's transitions (`entered:<task>`, `completed:<task>`), the step-0 one printed after the executor's `_load_plan`
line. Each log now has its `.rec` stream beside it (the human executor's record, one `[rec]` line per tick; the first
non-empty `.rec` baselines), git-ignored like the logs.

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| s00_off | 9015bf77def82770c083fbc12b98bbb3 | 5c7835ba3417ff28b5d3caf1d00d906e |
| s00_on | 1021b473b4cb063cb036068eb388724c | 5c7835ba3417ff28b5d3caf1d00d906e |
| s10_off | 7fe951f958c1a15fd637ce0429f1607e | 3e5fd9cd96dad4e0c56cfc626a770ff4 |
| s10_on | 28cee0b23d7d79d121ca73ff23526f89 | 3e5fd9cd96dad4e0c56cfc626a770ff4 |
| s20_off | 11e95a9c54575913174d945387f671c9 | 9f6d010e2fbc537952fa6ece4e96f469 |
| s20_on | cb9390c69b72708feaf61643776d96c8 | 9f6d010e2fbc537952fa6ece4e96f469 |
| s30_off | 1bb96f0e36db67a7568e1eac538bc30b | 65d234649396c9ab242841050082e9b0 |
| s30_on | 67a17f9e5cf5d26f94719992dff113be | 65d234649396c9ab242841050082e9b0 |
| s40_off | 4c9a27a98fb4f8b303c2aab968d16e3e | f6da9d345530212df9b0446aa53d1f1e |
| s40_on | 5f623007f875b4baf5e3a4f2d4253812 | f6da9d345530212df9b0446aa53d1f1e |
| s50_off | 389fb15adeed493a4665a7a922b90ea6 | 3e4fd412ba39ddd3267d1d37089beaac |
| s50_on | 73446fc4205d0ad660b229eb620d80d7 | 3e4fd412ba39ddd3267d1d37089beaac |
| s70_off | fb674a86b3957a4c62be2a17712870a0 | dab078d5ca51e5b378054ee6a60ccca7 |
| s70_on | be162273ccbb0afa69dd7a18133476ac | dab078d5ca51e5b378054ee6a60ccca7 |
| s71_off | 6f56274520131c22fa3e4357c0f42cc5 | dab078d5ca51e5b378054ee6a60ccca7 |
| s71_on | 6d3d29b11454fa41f93dcfda5e6fd0cc | dab078d5ca51e5b378054ee6a60ccca7 |

## T-H4: the record's queries and the coverage line — the logs from here on

Regenerated after T-H4 with the same command, superseding the T-H3 table. CAUSE: the loader prints one `[coverage]`
line per script entry for each robot observing the human, after the `[run]` headers (`docs/design_decisions.md`, "T-H:
the human behaviour model", as built T-H4). Against the T-H3 logs every other line is byte-identical, and every `.rec`
stream is byte-identical (its md5 unchanged).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| s00_off | 51ef9d8cf71995533902b222c357169d | 5c7835ba3417ff28b5d3caf1d00d906e |
| s00_on | f4bf6bd1e50ff7fbf2114b8f8f632a76 | 5c7835ba3417ff28b5d3caf1d00d906e |
| s10_off | f4f5df8d0b2c62f99cf9c541b8fb9f13 | 3e5fd9cd96dad4e0c56cfc626a770ff4 |
| s10_on | 68301538d51f66a3652a8f3f9eebb538 | 3e5fd9cd96dad4e0c56cfc626a770ff4 |
| s20_off | 455f722656e202a9e6fbe6a16ddcbbbc | 9f6d010e2fbc537952fa6ece4e96f469 |
| s20_on | fc4bc808ef9afc32b4253b491ed06418 | 9f6d010e2fbc537952fa6ece4e96f469 |
| s30_off | 8994efea289233a561bb0af359486fd6 | 65d234649396c9ab242841050082e9b0 |
| s30_on | 9f2f3ccdaba00d980ebdec7c2a730812 | 65d234649396c9ab242841050082e9b0 |
| s40_off | d874e4aa63d47730d2c1053799e5fdc2 | f6da9d345530212df9b0446aa53d1f1e |
| s40_on | babc3bea02577c8f5af322debc32830d | f6da9d345530212df9b0446aa53d1f1e |
| s50_off | b70d55ef7723c1a62ebbe792283a9074 | 3e4fd412ba39ddd3267d1d37089beaac |
| s50_on | 307d8b5b24718c2f7da300043fe5735a | 3e4fd412ba39ddd3267d1d37089beaac |
| s70_off | 557a61441bd29b30960302be3d70d730 | dab078d5ca51e5b378054ee6a60ccca7 |
| s70_on | be391644cd03f4ba324b66ddef6e9596 | dab078d5ca51e5b378054ee6a60ccca7 |
| s71_off | a961d30bb772d1f935f28bf3e5771411 | dab078d5ca51e5b378054ee6a60ccca7 |
| s71_on | ef9e2b2cea9d8f9a83b22218f9403a49 | dab078d5ca51e5b378054ee6a60ccca7 |

## T-H follow-up: the scenario-coverage line — the logs from here on

Regenerated after the T-H follow-up with the same command, superseding the T-H4 table. CAUSE: the loader prints
one `[scenario-coverage]` line per robot observing the human, after its `[coverage]` lines: the script's composition
and scenario coverage (`docs/design_decisions.md`, "T-H: the human behaviour model", as built T-H follow-up). Against
the T-H4 logs every other line is byte-identical, and every `.rec` stream is byte-identical (its md5 unchanged).

| log | md5 (.log) | md5 (.rec) |
|---|---|---|
| s00_off | 92de8c98c88f05c015041d2b1ae2d87e | 5c7835ba3417ff28b5d3caf1d00d906e |
| s00_on | 9090b8fb68581fa0d5cc63a45eecdc9b | 5c7835ba3417ff28b5d3caf1d00d906e |
| s10_off | 23769792c689a779beb433840757d42c | 3e5fd9cd96dad4e0c56cfc626a770ff4 |
| s10_on | c190fd7536f11fd3321297d06687c69d | 3e5fd9cd96dad4e0c56cfc626a770ff4 |
| s20_off | cd87b734b4930eb4fec3b87ba9937b2b | 9f6d010e2fbc537952fa6ece4e96f469 |
| s20_on | 00988b879c197f405c11f20b1c381432 | 9f6d010e2fbc537952fa6ece4e96f469 |
| s30_off | 837446a89ed22d082a19dbdabdf610b7 | 65d234649396c9ab242841050082e9b0 |
| s30_on | 4f289a8a6cbe85eebbee31c1f7e2fc5a | 65d234649396c9ab242841050082e9b0 |
| s40_off | 2f36acdbcd1b59b50b1f34ce56d1624c | f6da9d345530212df9b0446aa53d1f1e |
| s40_on | d25227bf1144778b98c5da0c74d5dfcd | f6da9d345530212df9b0446aa53d1f1e |
| s50_off | ea3b2206ef22e639a3e7eaff24ea8077 | 3e4fd412ba39ddd3267d1d37089beaac |
| s50_on | 0dfbb71a383d4a672c1856fbba6d86fb | 3e4fd412ba39ddd3267d1d37089beaac |
| s70_off | 646ff5fb694db55f2aad6bc931d1196a | dab078d5ca51e5b378054ee6a60ccca7 |
| s70_on | 6386bab6d4ba67728b269f2290149457 | dab078d5ca51e5b378054ee6a60ccca7 |
| s71_off | 09ef3397c91b2d8ca528daa18f06b3d0 | dab078d5ca51e5b378054ee6a60ccca7 |
| s71_on | c6b7af0dda5637f011cd3fbbe6e63961 | dab078d5ca51e5b378054ee6a60ccca7 |
