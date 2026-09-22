# T-B3 — full_reorder beside single_task; the first full_reorder logs

A comparison table and a regression set, not an evaluation (generality is T-F's). Fixtures s80, s81, s83
(env_layout8, two tables), s20 (env_layout2) and s70 (env_layout7); `--strategy` single_task and full_reorder,
assignment prior off and on; cost realized, gate none, stop off; PYTHONHASHSEED=0; code at 2a44c65.

## The table

Completion from the world fact (the robot's last release + 1). Heads: the robot's tasks in the order it
delivered them (item numbers). Admitted: `[meta-b3]` calls with `selection=realized` (the projection admitted)
over all `[meta-b3]` calls; 0 admitted would mean the row says nothing about realized cost. Holds: executed
holds as start tick (ticks executed); none interrupted.

| fixture | prior | completion ST / FR | heads ST | heads FR | admitted ST | admitted FR | holds ST | holds FR |
|---|---|---|---|---|---|---|---|---|
| s80 | off | 265 / 224 | 6 1 7 4 | 7 4 6 1 | 6/12 | 4/11 | — | — |
| s80 | on | 265 / 224 | 6 1 7 4 | 7 4 6 1 | 6/12 | 4/11 | — | — |
| s81 | off | 268 / 224 | 6 1 7 4 | 7 4 6 1 | 8/12 | 6/11 | 40 (3) | — |
| s81 | on | 268 / 224 | 6 1 7 4 | 7 4 6 1 | 8/12 | 6/11 | 40 (3) | — |
| s83 | off | 265 / 226 | 6 1 7 4 | 7 4 1 6 | 6/12 | 8/12 | — | — |
| s83 | on | 265 / 226 | 6 1 7 4 | 7 4 1 6 | 7/12 | 8/12 | — | — |
| s20 | off | 237 / 221 | 4 6 7 | 6 4 7 | 4/10 | 4/10 | 20 (8), 31 (1) | — |
| s20 | on | 237 / 221 | 4 6 7 | 6 4 7 | 4/10 | 4/9 | 11 (8), 31 (1) | — |
| s70 | off | 186 / 186 | 2 1 | 2 1 | 3/10 | 3/10 | 61 (1) | 61 (1) |
| s70 | on | 186 / 186 | 2 1 | 2 1 | 3/10 | 3/10 | 60 (1) | 60 (1) |

- s20, one table: full_reorder takes a different head order and completes 16 ticks earlier without a hold.
- s70: the same course under both strategies; the logs differ in the decision lines alone (`[meta-cand]` against
  `[meta-ord]`, the `ordering=` field of `[meta-b3]`, the `[run]` line).

## R3 — separation inside the assessed window

No `[sep]` distance below min_separation (50 cm) falls inside the assessed window [trigger, T_h] of the decision
in effect, in any of the 20 runs. For information, every sub-s tick falls under a decision with no admitted
projection (no assessed window):

| run | ticks | min `[sep]` |
|---|---|---|
| s83 ST, both priors | 262–339 (completion 265) | 39.69 cm |
| s83 FR, both priors | 223–339 (completion 226; the arrival past T_h in `analysis/tb1c_realized_flip/`) | 42.87 cm |
| s20 ST, both priors | 57–58; 143–149; 231–299 (completion 237) | 37.49; 30.15; 4.23 cm |
| s20 FR, both priors | 127–135; 216–299 (completion 221) | 17.92; 3.94 cm |

## R4 — byte-identity

The eight single_task logs with a baseline regenerate byte-identical by md5: s20 and s70 against
`analysis/tb1a_destination/README.md` (T-B Q7), s80 and s81 against `analysis/tb1b_two_tables/README.md`. s83
has no single_task log in `analysis/tb1c_realized_flip/` (its sweep is full_reorder only), so its two
single_task logs had no baseline (baselined here since, below); its two full_reorder realized logs, and s80's, match that record's md5s.

## Logs (`sweep/`, local, git-ignored) — the diff target under full_reorder

Regenerated when a fixture changes. md5 at 2a44c65:

| log | md5 |
|---|---|
| s20_off | 921d61aceff9483d686744e63fb393f5 |
| s20_on | 9280684355c318deac1ec0cfe5ca6e22 |
| s70_off | 2e5c0bf17ba8ff24df211663a911c082 |
| s70_on | c37c7416c899950ceea6093369d6cf70 |
| s80_off | 004075a3e44afeef4ed611b2211f1a0b |
| s80_on | ab6e64456ff45a03c4e49d4e9e101aed |
| s81_off | f061d439f7bd5fdbac00a3bf4196ed04 |
| s81_on | 4415744aecf4c29f46c8fd787d6aaa13 |
| s83_off | 7b719acbbf4c63020146a83fbd5f3ff8 |
| s83_on | 36f29241b7f85f0255e14284d98e117e |

(files `sweep/<fixture>_full_reorder_<prior>.log`.)

s83 under single_task (realized, both priors) is baselined here too, since no earlier record holds it (Hadi,
at T-B3's close): `sweep/s83_single_task_<prior>.log`, md5 at 2a44c65:

| log | md5 |
|---|---|
| s83_single_task_off | 6d696902c38a9356a53c27764c40adc8 |
| s83_single_task_on | 4ecc5729f47b69195c5e6d67ad5e9ab6 |

## Run (repo root)

    analysis/tb3_full_reorder/sweep.sh <out_dir>

All 20 runs; the full_reorder logs and s83's single_task logs go to `sweep/`
(`cp <out_dir>/*_full_reorder_*.log <out_dir>/s83_single_task_*.log analysis/tb3_full_reorder/sweep/`).
