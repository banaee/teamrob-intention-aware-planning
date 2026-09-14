# T5 — a continue decision costs nothing (TODO-43)

`PYTHONHASHSEED=0`. Baselines: the T7/T8 sweep (`analysis/t7_t8_meta_bugs/new/`, HEAD 4c5684e).
New: `new/` at HEAD after the fix. `comparison.md` is `compare.py`'s per-condition output;
`inject_s00_off.txt` / `inject_s30_off.txt` are `inject.py`'s. Regenerate with `stages.sh`.

## What was measured before the fix

The run log carries the robot's per-tick `(action, micro)`. A lost tick is a tick with a task
set and `micro=None` that a no-trigger run would have spent on a microaction.

**Ticks lost to continue decisions in the eight sweep conditions: 0 of 0 ... in every condition.**
Every continue in the sweep (s00_off 7/39/63/109/113/115/131, s00_on 7/11/63/81/131, s20_off
29/30/87/91/95/103/190, s20_on 29/57/101/176, s30_off 48/121, s30_on 48/77/123, s40_off
19/98/143/195/226/274/311, s40_on 19/98/135/195/203/223/274/311) fires while the robot is in a
`move_to` with steps remaining, or on an action-boundary acknowledgement tick (s40_off 143), or
is the `task_committed` after a grasp. On none of those does the old reload cost a tick:
- mid-walk: `_load_plan` resets to the plan's first action, which is the walk in progress and
  not complete, and `expand()` re-derives the same straight path from the current position —
  the next step is the same point;
- on the acknowledgement tick: the reloaded plan's first action is the action just completed,
  the executor advances past it and returns, which is exactly what it does with no trigger;
- `task_committed`: the fresh decomposition (`deliver_already_held`) has no `pick_up` to
  acknowledge, so the reload starts the carry on the trigger tick — one tick EARLIER than a
  no-trigger run, which would spend that tick acknowledging the grasp. Pre-existing, unchanged.

The dead ticks in every condition (s00: 5, 29, 31, 61, 91, 93, 129, 164; s30_off: 46, 84, 86, 119,
153, 155; …) are all action-boundary acknowledgements and the task-complete tick — the
executor's normal one-tick-per-boundary, identical with and without triggers, out of scope.

So premise (a) of the task — that each of the three prior-off `theta_crossed` crossings costs a
tick — does not hold at HEAD: the crossings sit inside the HUMAN's grasp stop while the robot is
walking (s00_off 109/113/115: item_4's walk, queue 22/18/16 steps left; s20_off 87/91/95:
item_6's walk, 16/12/8 left). The measurement TODO-43 recorded (s20_off step 22, grasp at 23
instead of 22) was made before the recognizer rework moved the trigger ticks off the one tick
where a reload does lose the robot a step.

## The mechanism, isolated (`inject.py`)

`inject.py` makes `evaluate_triggers()` fire on a chosen tick (reason `injected`) if no real
trigger fired; everything downstream is the real path (`update()` → B3 → planner → executor).
On every injected tick below `update()` re-selected the executing task (a continue).

| condition | injected on | tick's role in the no-trigger run | before | after |
|---|---|---|---|---|
| s00_off | 3 | mid-walk to shelf_7 | grasp 6, release 30 | grasp 6, release 30 |
| s00_off | 5 | arrival acknowledgement (dead tick) | grasp 6, release 30 | grasp 6, release 30 |
| s00_off | **6** | **the GRASP tick** | **grasp 7, release 31** | grasp 6, release 30 |
| s00_off | 29 | table-arrival acknowledgement | grasp 6, release 30 | grasp 6, release 30 |
| s00_off | **30** | **the RELEASE tick** | **grasp 6, release 31** | grasp 6, release 30 |
| s30_off | 46 | arrival acknowledgement at shelf_2 | grasp 47, release 85 | grasp 47, release 85 |
| s30_off | **47** | **the GRASP tick** | **grasp 48, release 86** | grasp 47, release 85 |
| s30_off | 84 | table-arrival acknowledgement | grasp 47, release 85 | grasp 47, release 85 |
| s30_off | **85** | **the RELEASE tick** | **grasp 47, release 86** | grasp 47, release 85 |

(no injection: s00_off grasp 6 / release 30; s30_off grasp 47 / release 85. "before" = HEAD
4c5684e in a worktree; "after" = this commit.)

The lost tick has one cause. A continue on the tick AFTER an acknowledgement — the executor has
already advanced its cursor past the completed `move_to` and would grasp or release now — reloads
a plan whose first action is that completed `move_to`; the executor spends the tick advancing
past it a second time. Mid-walk and on the acknowledgement tick itself nothing is lost. After the
fix a continue keeps the cursor and the microaction queue (`[executor] continue_plan … action_index
1->1 queue_len=0` at the grasp; `0->0 queue_len=24` mid-walk), and every injected run is
tick-for-tick the no-injection run.

## The sweep after the fix (`comparison.md`)

- Decision sequence: unchanged in all eight conditions (every `[meta]`, `[meta-proj]`,
  `[meta-pool]` line identical). Run ends identical.
- `[IR]` / `[IR-dist]`: byte-identical in all eight. The recognizer is untouched and, since no
  continue in the sweep was losing a tick, the world it reads did not change either.
- Robot per-tick `(task, action, micro, pos)` lines: identical in all eight.
- `[executor]`: `_load_plan` becomes `continue_plan … action_index 0->0 queue_len=N` on 21 of the
  continues (the in-flight walk found in the fresh plan; queue kept). The `task_committed`
  continues still `_load_plan` (the fresh `deliver_already_held` has no `pick_up`), as before.
  s30_off has no `continue_plan` at all: its 48 and 121 are both `task_committed`.
- The only other difference: `[meta-cand] … min_dist=` in the 14th–16th significant digit at
  12 / 6 / 8 / 2 / 0 / 0 / 6 / 6 lines (s00_off … s40_on). The kept queue's step points were
  interpolated from the walk's start; the old reload re-interpolated the same straight line from
  the current position, landing ~1e-13 cm away. Costs, feasibility, conflict counts and the
  2-dp positions are identical. These are the new baselines; a `grep meta-cand` against the
  T7/T8 logs differs only in those digits.

## Premise (b) — the scenario_30 cancel-and-return

Not in the record. Neither T7/T8 s30 log nor T1's instrumented logs contain a
`deliver_with_return` execution (no 6-action `_load_plan`), and no s30 continue at HEAD loses a
tick. In s30_off the item the robot holds is delivered on the tick a no-trigger run delivers it
(item_2 at 85, item_4 at 160 → 157 after T7), all four items delivered, before and after. The
run that showed the cancel-and-return must predate T7 (which removed the step-87 re-pick) or
have used a different `min_safe_distance`; it cannot be reproduced from HEAD, so "does the
cancel disappear" has no before-case to answer against. What is answered: the tick that would
have caused it is no longer lost (rows 47 and 85 above).
