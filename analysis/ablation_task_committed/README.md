# The trigger set without task_committed — an ablation, measured on the corrected body (T-B Q7)

> Superseding note (T-L stage 3, 26 Sept 2026): the layout and scenario ids here are the old ones; `docs/rename_table.md` maps them to the serial ids. The scripts and records stay frozen at their commit.

SUPERSEDED IN PART (TODO-90 check, September 2026; `analysis/todo90_b2a_window/`). Under prior on, the s10 b2a
decision is at tick 24, not 29. The in-window counts include tick 23 of s30 b2a prior on (15.47 cm), which lies
outside every window: it is the observation offset of the decision at 23, and `measure.py` checked the end of the
tick, not the whole tick. The remaining in-window sub-50 ticks (s10 72–74, s30 24) are standing ticks that realization
itself projected below min_separation; no robot step inside a window came below min_separation. The evaluation rule
from here on: a defect is a robot STEP (a moving tick) inside an assessed window that ends below min_separation;
standing ticks are judged by whether realization projected them (F1: the robot answers for its own motion only).
Nothing else in this folder is changed.

A measurement, nothing decided here. Each condition run with the trigger (the default) and without it
(`--task_committed_trigger false`): s80, s81, s83 (env_layout8, 340 steps), s20 (300), s70 (300) × `--strategy`
single_task / full_reorder × assignment prior off / on, gate none; and s10 (450), s20, s30 (200) under gate b2a,
single_task, both priors. Cost realized, stop off, PYTHONHASHSEED=0, code at e76f2d8 plus the run option (R1).

## The run option

`MetaPlanner(task_committed_trigger: bool = True)`; False makes `evaluate_triggers()` never raise
`task_committed` (the grasp condition is AND-ed with the flag). The other two triggers are asked exactly as
before, so a `recognition_changed` on the grasp tick fires as it did. Threaded as the other run options are:
`configs/experiment.yaml` key and `--task_committed_trigger true|false`, `SimModel`, `RobotAgent`. The `[run]`
header gains ` task_committed_trigger=off` only when it is off, so default logs keep their bytes.

Default unchanged: every with-trigger log here is byte-identical to its baseline (T-B3's 12 in
`analysis/tb3_full_reorder/`, the T-B Q7 single_task logs of s20 / s70 / s80 / s81, and the six b2a logs
recorded at e76f2d8 before the change), and so are the regression five and s50 / s71 (`analysis/tb1a_destination/`).

## The table

Columns (`measure.py`, which states each rule): completion from the world fact; decisions = fired triggers,
nc / rc / tc = no_current_task / recognition_changed / task_committed; holds executed as start (ticks); in<50 =
`[sep]` ticks below min_separation (50 cm) inside the assessed window of the decision in effect, T10's
convention; min in window = the smallest `[sep]` inside any window; <50 outside = sub-min_separation ticks under
no window, up to completion (information); B2 reached = `[meta-b2]` lines (how many continued); release residual
= per robot delivery, executed release tick − (t + hold executed + the head's projected place start) of the
decision in effect, the last fired trigger strictly before the release, from `capture.py` (the head's segments,
recorded inside `update()`, nothing written to the log); `*` = that decision projected nothing (B2 continued
without an admitted projection), so the last decision on the task that did project is used.

| run | prior | trigger | completion | decisions (nc/rc/tc) | holds executed | in<50 | min in window | <50 outside window (to completion) | B2 reached | release residual per delivery |
|---|---|---|---|---|---|---|---|---|---|---|
| s80 ST | off | with | 265 | 12 (4/4/4) | — | 0 | 169.99 | — | — | +1.62 +1.67 +1.92 +1.48 |
| s80 ST | off | without | 265 | 8 (4/4/0) | — | 0 | 169.99 | — | — | +0.73 +1.31 +1.32 +1.89 |
| s80 ST | on | with | 265 | 12 (4/4/4) | — | 0 | 169.99 | — | — | +1.62 +1.67 +1.92 +1.48 |
| s80 ST | on | without | 265 | 8 (4/4/0) | — | 0 | 169.99 | — | — | +0.73 +1.31 +1.32 +1.89 |
| s80 FR | off | with | 224 | 11 (3/4/4) | — | 0 | 408.44 | — | — | +1.49 +0.53 +1.81 +1.59 |
| s80 FR | off | without | 224 | 7 (3/4/0) | — | 0 | 408.44 | — | — | +0.62 +0.53 -0.19 +1.39 |
| s80 FR | on | with | 224 | 11 (3/4/4) | — | 0 | 408.44 | — | — | +1.49 +0.53 +1.81 +1.59 |
| s80 FR | on | without | 224 | 7 (3/4/0) | — | 0 | 408.44 | — | — | +0.62 +0.53 -0.19 +1.39 |
| s81 ST | off | with | 268 | 12 (4/4/4) | 40 (3) | 0 | 126.60 | — | — | +1.62 +0.67 +1.92 +0.48 |
| s81 ST | off | without | 268 | 8 (4/4/0) | 40 (3) | 0 | 126.60 | — | — | +0.73 +0.67 -0.08 +0.48 |
| s81 ST | on | with | 268 | 12 (4/4/4) | 40 (3) | 0 | 126.60 | — | — | +1.62 +0.67 +1.92 +0.48 |
| s81 ST | on | without | 268 | 8 (4/4/0) | 40 (3) | 0 | 126.60 | — | — | +0.73 +0.67 +1.32 +0.48 |
| s81 FR | off | with | 224 | 11 (3/4/4) | — | 0 | 383.45 | — | — | +1.49 +0.53 +1.81 +1.59 |
| s81 FR | off | without | 224 | 7 (3/4/0) | — | 0 | 383.45 | — | — | +0.62 +0.53 +0.90 +2.39 |
| s81 FR | on | with | 224 | 11 (3/4/4) | — | 0 | 355.02 | — | — | +1.49 +0.53 +1.81 +1.59 |
| s81 FR | on | without | 224 | 7 (3/4/0) | — | 0 | 355.02 | — | — | +0.62 +0.53 +0.90 +2.39 |
| s83 ST | off | with | 265 | 12 (4/4/4) | — | 0 | 727.53 | 262–264 | — | +1.62 +1.67 +0.92 +0.48 |
| s83 ST | off | without | 265 | 8 (4/4/0) | — | 0 | 727.53 | 262–264 | — | +0.73 +1.31 +0.92 +0.48 |
| s83 ST | on | with | 265 | 12 (4/4/4) | — | 0 | 727.53 | 262–264 | — | +0.62 +1.67 +0.92 +0.48 |
| s83 ST | on | without | 265 | 8 (4/4/0) | — | 0 | 727.53 | 262–264 | — | +0.62 +1.31 +0.92 +0.48 |
| s83 FR | off | with | 226 | 12 (4/4/4) | — | 0 | 101.97 | 223–225 | — | +1.49 +0.53 +1.26 +0.68 |
| s83 FR | off | without | 226 | 8 (4/4/0) | — | 0 | 101.97 | 223–225 | — | +0.62 +0.53 +1.73 +0.68 |
| s83 FR | on | with | 226 | 12 (4/4/4) | — | 0 | 101.97 | 223–225 | — | +0.49 +0.53 +1.26 +0.68 |
| s83 FR | on | without | 226 | 8 (4/4/0) | — | 0 | 101.97 | 223–225 | — | +0.49 +0.53 +1.73 +0.68 |
| s20 ST | off | with | 237 | 10 (3/4/3) | 20 (8), 31 (1) | 0 | 114.93 | 57–58, 143–149, 231–236 | — | +0.05 +0.06 +1.99 |
| s20 ST | off | without | 237 | 7 (3/4/0) | 20 (8) | 0 | 114.93 | 57–58, 143–149, 231–236 | — | +0.05 +0.06 +1.54 |
| s20 ST | on | with | 237 | 10 (3/4/3) | 11 (8), 31 (1) | 0 | 114.93 | 57–58, 143–149, 231–236 | — | +0.05 +0.06 +1.99 |
| s20 ST | on | without | 237 | 7 (3/4/0) | 11 (8) | 0 | 114.93 | 57–58, 143–149, 231–236 | — | +0.05 +0.06 +1.54 |
| s20 FR | off | with | 221 | 10 (3/4/3) | — | 0 | 148.79 | 127–135, 216–220 | — | +0.68 +0.68 +1.12 |
| s20 FR | off | without | 221 | 7 (3/4/0) | — | 0 | 148.79 | 127–135, 216–220 | — | +0.68 +0.68 +0.41 |
| s20 FR | on | with | 221 | 9 (3/3/3) | — | 0 | 148.79 | 127–135, 216–220 | — | +0.68 +0.68 +1.12 |
| s20 FR | on | without | 221 | 6 (3/3/0) | — | 0 | 148.79 | 127–135, 216–220 | — | +0.68 +0.68 +0.41 |
| s70 ST | off | with | 186 | 10 (2/6/2) | 61 (1) | 0 | 99.39 | — | — | +0.70 +1.93 |
| s70 ST | off | without | 186 | 8 (2/6/0) | 61 (1) | 0 | 99.39 | — | — | +0.70 +0.93 |
| s70 ST | on | with | 186 | 10 (2/6/2) | 60 (1) | 0 | 99.39 | — | — | +0.70 +1.93 |
| s70 ST | on | without | 186 | 8 (2/6/0) | 60 (1) | 0 | 99.39 | — | — | +0.70 +0.93 |
| s70 FR | off | with | 186 | 10 (2/6/2) | 61 (1) | 0 | 99.39 | — | — | +0.70 +1.93 |
| s70 FR | off | without | 186 | 8 (2/6/0) | 61 (1) | 0 | 99.39 | — | — | +0.70 +0.93 |
| s70 FR | on | with | 186 | 10 (2/6/2) | 60 (1) | 0 | 99.39 | — | — | +0.70 +1.93 |
| s70 FR | on | without | 186 | 8 (2/6/0) | 60 (1) | 0 | 99.39 | — | — | +0.70 +0.93 |
| s10 b2a ST | off | with | 422 | 15 (3/8/4) | — | 3 | 30.87 | 75–76 | 11 (11 cont.) | +0.19 +0.67* +0.73 +1.64* |
| s10 b2a ST | off | without | 422 | 11 (3/8/0) | — | 3 | 30.87 | 75–76 | 7 (7 cont.) | +0.19 +0.67* +0.73 +0.73* |
| s10 b2a ST | on | with | 422 | 14 (3/8/3) | — | 3 | 30.87 | 75–76 | 10 (10 cont.) | +1.19 +0.67* +1.73 +1.64* |
| s10 b2a ST | on | without | 422 | 11 (3/8/0) | — | 3 | 30.87 | 75–76 | 7 (7 cont.) | +1.19 +0.67* +1.91 +0.73* |
| s20 b2a ST | off | with | 237 | 10 (3/4/3) | 20 (8), 31 (1) | 0 | 114.93 | 57–58, 143–149, 231–236 | 7 (7 cont.) | +0.05* +1.06* +1.54* |
| s20 b2a ST | off | without | 237 | 7 (3/4/0) | 20 (8) | 0 | 114.93 | 57–58, 143–149, 231–236 | 4 (4 cont.) | +0.26* +1.94* +1.54 |
| s20 b2a ST | on | with | 237 | 10 (3/4/3) | 11 (8), 31 (1) | 0 | 114.93 | 57–58, 143–149, 231–236 | 7 (7 cont.) | +0.05* +1.06* +1.54* |
| s20 b2a ST | on | without | 237 | 7 (3/4/0) | 11 (8) | 0 | 114.93 | 57–58, 143–149, 231–236 | 4 (4 cont.) | +0.26* +1.94* +1.54 |
| s30 b2a ST | off | with | 161 | 8 (2/4/2) | 27 (7), 47 (1) | 0 | 105.33 | 21–24, 157–160 | 6 (6 cont.) | +0.46* +1.18* |
| s30 b2a ST | off | without | 161 | 6 (2/4/0) | 27 (7) | 0 | 105.33 | 21–24, 157–160 | 4 (4 cont.) | +1.32* +1.18* |
| s30 b2a ST | on | with | 161 | 8 (2/4/2) | 23 (7), 47 (1) | 2 | 15.47 | 21–22, 157–160 | 6 (6 cont.) | +0.46* +1.18* |
| s30 b2a ST | on | without | 161 | 6 (2/4/0) | 23 (7) | 2 | 15.47 | 21–22, 157–160 | 4 (4 cont.) | +1.32* +1.18* |

## What changed, per row (one line each)

The world is identical with and without the trigger in all 26 pairs: every `[sep]` line, every human line,
every `[IR] step=` line and every `[meta]` line other than the `task_committed` ones are byte-identical; so are
completion, and every hold except the two below.
- Every row: the `task_committed` decisions are gone (2–4 per run) and nothing takes their place.
- s20 ST and s20 b2a, both priors: the hold 31 (1), placed at the grasp's `task_committed`, is not executed; on
  tick 31 the robot, at the same position, spends the `pick_up` acknowledgement instead (`micro=stand` →
  `action=pick_up micro=None`). Robot lines differ at that tick only.
- s30 b2a, both priors: likewise the hold 47 (1), at tick 47.
  (D3 note: the same hold 47 (1) also occurred under gate none, single_task, both priors — tb1a's s30, not a
  row here — and went the same way at D3's regeneration, `analysis/tb1a_destination/README.md`.)
- s10 / s20 / s30 b2a: B2 is still reached (7, 4, 4 times; every one continues); the calls removed are the
  `task_committed` ones.
- In-window sub-min_separation ticks: s10 b2a (72–74, 30.87 cm, under the decision at 29) and s30 b2a prior on
  (23–24, 15.47 cm, under the decision at 23) — present with the trigger, unchanged without it.
- Release residual: with the trigger, a delivery whose decision in effect is the grasp's `task_committed` carries
  its hold-0 reload tick (s80 ST +1.62 = carry +0.62 + 1); without it that decision is an earlier one and the
  residual is the whole plan's quantisation (s80 ST +0.73 +1.31 +1.32 +1.89, T-B Q7's totals). The two sides are
  measured against different decisions. Two negatives without the trigger, s80 FR 3rd (−0.19, decision at 172)
  and s81 ST off 3rd (−0.08, at 131): sub-tick, from a mid-fetch `recognition_changed` projection.

## Logs (`sweep/`, local, git-ignored, no md5s)

`<fixture>_<single_task|full_reorder|b2a>_<prior>_<with|without>.log`, and the `.json` capture beside each.

## Run (repo root)

    analysis/ablation_task_committed/sweep.sh analysis/ablation_task_committed/sweep
    python analysis/ablation_task_committed/measure.py analysis/ablation_task_committed/sweep

D3 note (September 2026): `task_committed` is removed from the code (dd880be), so the `tc` column of the table is
0 from D3 on, and the run option `--task_committed_trigger` was discarded: `sweep.sh` no longer runs as is.
This folder is a frozen record at 142deaa.
