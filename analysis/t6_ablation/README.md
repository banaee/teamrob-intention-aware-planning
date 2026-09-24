# T6 — ablation of the meta-planner's policy components

> Superseding note (24 Sept 2026, the terminology ruling; `docs/glossary.md` §7, `docs/terminology_revision.md`): "a deviation from the projection" → a departure from the projection; "deviation" means a departure from the work order only (label A).

What each component does on the kitting fixtures, and why: realization (B3 `cost_strategy` realized against
plain), commitment (B2 `gate_strategy` b2a against none, with a ρ existence test), and the execution-time
separation stop (C, on against off). HEAD 9127b2a, no code change; PYTHONHASHSEED=0; θ 0.75, s = min_separation
50 cm throughout, ρ 0.5 unless swept. The D2 trigger is not an axis: `analysis/d2_recognition_trigger/` is the
old/new comparison and its stop-off, gate none, realized runs are this task's reference cell.

The findings are statements about the components, bound to these fixtures. Nothing here selects a value
of s, ρ, θ or any other parameter: safety parameters come from the body, standards and experts, and
fixtures never set design decisions (Hadi, mid-session). Where a result seems to ask for one it is listed
under "Observations for the design chat".

Changes to the task as posed, decided mid-session by Hadi: the s (min_separation) sweep is dropped
(never run); the ρ sweep stays as an existence test only (does b2a ever differ from none on these
fixtures), not as a selection.

## Files

- `run.py`: run_mesa headless with `T6_RHO` (and `T6_SEP_CM`, unused after the change above) injected into
  the MetaPlanner's constructor in-process, so ρ can be swept without a run option. The `[run]` header
  records the values used.
- `sweep.sh <out_dir> [run_mesa args]`: the eight fixtures × prior off/on through `run.py`, at the
  established step counts (s00 300, s10 450, s20 300, s30 200, s40 400, s50 / s70 / s71 300; the caps for
  the stop-on runs that do not complete). `CONDS` picks fixtures.
- `metrics.py`: every metric below from the logs alone. Output `matrix.md` (committed): the full run
  matrix per cell, the pairwise tables for (a), (b), (c), and the ρ sweep.
- `core/<cell>/`, `rho/rho<ρ>/`: logs, git-ignored.

Regenerate (~5 min):

    H=analysis/t6_ablation
    for g in none b2a; do for c in plain realized; do for s in false true; do
      $H/sweep.sh $H/core/g${g}_c${c}_s$([ $s = true ] && echo on || echo off) \
        --gate_strategy $g --cost_strategy $c --separation_stop $s; done; done; done
    for r in 0.1 0.25 1.0; do CONDS="s20 s30 s50 s70 s71" T6_RHO=$r \
      $H/sweep.sh $H/rho/rho$r --gate_strategy b2a --cost_strategy realized --separation_stop false; done
    ~/python-envs/teamrob-sp4-env/bin/python $H/metrics.py > $H/matrix.md

## Run matrix

Core cross: gate {none, b2a} × cost {plain, realized} × stop {off, on} × prior {off, on} on s00, s10, s20,
s30, s40, s50, s70, s71: 16 cells × 8 fixtures = 128 runs, all run (no cell was skipped as identical by
construction; the only such argument, ρ under gate none, is not a core axis). ρ sweep: {0.1, 0.25, 1.0}
(0.5 is the core cell gb2a_crealized_soff), b2a + realized, stop off, both priors, on s20, s30, s50, s70,
s71: the fixtures where the core's `[meta-b2]` lines carry a non-zero δ. On s00, s10 and s40 every
admitted B2 verdict has δ = 0, which continues at any ρ > 0 by construction, so they are not swept. 30 runs.

**Gate and cost are not independent axes (ruled at review).** B2 `b2a` realizes the current task whatever
`cost_strategy` is, so the cell b2a + plain is realization restricted to the current task, not "commitment
without realization". The clean comparisons are:

- realization: none + plain against none + realized;
- commitment: none + realized against b2a + realized.

The b2a + plain cells are kept in `matrix.md` as run, and are read as neither comparison. No change to b2a.

Drift check: the reference cell (gate none, realized, stop off, both priors, all eight fixtures) is
byte-identical to the D2 baselines (`sweep/`, `fixtures/`) on all ten CLAUDE.md greps.

## Measurement

- Completion from the world fact. The robot's pool is the first `[meta]` line's winner plus queue; the
  terminal condition `obj_at(item, table)` comes to hold on the tick the release microaction executes
  (per-tick line `action=place micro=release`) and is first observable on the next tick, which is the
  completion tick reported. With the prior off the recognizer pins the same tick (`[IR-complete]`; checked,
  no mismatch); with the prior on the hypotheses are the human's pool and the robot's items are never
  pinned, which is why the read is from the release. The declared tick (the empty-pool line) is the world
  tick + 2 in all 126 completing runs: one tick of executor bookkeeping, one for `no_current_task`.
  Every completion figure below is the world tick; the D2 README's figures are declared ticks.
- Decision sequence key: step:trigger:winner. The hold is not in the key, so the first differing DECISION
  can come after the first behavioural difference (s20: both cost strategies decide item_4 at 20; realized
  also holds 8 ticks there, and the sequences first differ at the next decision, the grasp trigger at 23 vs
  31). ("Entry" is reserved for a ProjectedPlan's per-task part; docs/glossary.md.)
- Blocked time, outcome, human-borne proximity and the sequential-motion violations follow
  `analysis/c_separation_stop/blocked.py`; added here: each refusal and each violation split by the rule it
  concerns ((a) the step started at or beyond s; (b) within), and the sub-s ticks labelled against the
  assessed window of the decision in effect (F1's `evaluate.py` labels).

## (a) Realization: cost realized against plain

Same gate, stop and prior; world completion, first differing decision.

| fixture | plain | realized | where they part | what realization does |
|---|---|---|---|---|
| s00, s10, s40 | 166 / 418 / 376 | same | identical in all 8 conditions (gate × stop × prior) | nothing to place: no candidate's minimal shift is non-zero at any admitted trigger (holds 0/0/0), so realized cost = T_r = plain cost |
| s20 (off / on) | 226 / 226 | 235 / 237 | crossing at 20 (prior off) / 6 (on) | hold 8 on item_4 (34.74 + 8 = 42.74, still the argmin against item_6 56.64): the winner is unchanged, the plan is hold-then-go; a 1-tick hold at the grasp (31); prior on adds a 2-tick hold at 57. Completion +9 / +11 = the ticks held |
| s30 | 150 | 160 | crossing at 28 | hold 7 on item_4 + 1 at the grasp (47); +10 |
| s50 | 226 | 235 | as s20 (its end-state variant) | as s20; +9 |
| s70 | 169 | 185 | 23: the foreseen coffee stay on item_1's route | switch: item_1 57 + 32 = 89 against item_2 80.15, so B3 takes item_2 and returns to item_1 at 105 (order item_1 item_2 item_1 against plain's item_1 item_2); +16 |
| s71 | 170 | 199 (off) / 201 (on) | 23: the same stay, the alternative across | hold 32 on item_1 (89 against item_3 118), executed 31 (the boundary retraction at 54 replaces its last tick); +29 |

With the stop on the comparison changes sign where plain walked through the human. On s70 / s71 plain's
completion above is bought with sequential-motion violations at the stay (6 per run against realized's 0 /
3; on s20 / s30 both strategies violate at the table convergence past T_h, 6 to 8 per run); with the stop
on, plain is refused 35 ticks at the stay (25–59, 29 of them inside its own decision's window,
which the plain cost had ignored) and completes s70 at 204 against realized's 185 with no refusal at all,
and s71 at 205 against realized's 205 with 4 refusals (56–59: the human is still at the coffee machine when
the hold ends). So on s70 and s71 realization replaces execution-time blocking by a decided switch or hold;
on s20 / s30 it reduces the blocked ticks (167 → 158 / 156, 52 → 48 / 44) without changing the outcome (the
last delivery is blocked to the cap either way, R2); on s50 realized is refused 2 ticks at the table (57–58: after
the hold at 20 it arrives while the human is there; plain, 8 ticks earlier, is not), 235 → 237.

Trigger fires differ only where decisions differ (s20_on, s30, s50_on, s71_off: one `recognition_changed`
or `no_current_task` more or fewer, from the shifted timing).

Same result under gate b2a, except that b2a + plain already places the crossing holds, see (b).

What these fixtures cannot show: a case where a hold changes the argmin among more than two candidates
(only s70 has a cheaper alternative), a case where realized cost picks a worse order than plain, or any
crossing other than one table convergence (s20 / s30 / s50) and one stay (s70 / s71) per run.

## (b) Commitment: gate b2a against none

Under realized cost, ρ 0.5 (T4's condition): identical to none in 15 of 16 fixture × prior conditions,
both stop settings, on every grep. The exception is s71 prior off at step 108: none decides item_3, b2a
continues item_1; completion 199 against 201. The mechanism is a bookkeeping lag, not a commitment: the
robot releases item_1 at 107, the world fact holds and `[meta-pool]` drops item_1 on 108, and the D2 trigger
fires on that same tick. Under none B3 sees the pool without item_1 (candidates = 1) and starts item_3 at
once; under b2a B2 judges `executor_state.current_task`, still item_1 (the executor closes it a tick later),
finds δ = 0 and continues, and item_3 starts on `no_current_task` at 110. Two ticks. So the task's premise
"never at ρ = 0.5" holds for the T4 / T10 / F1 fixtures and for s50 / s70, and fails on s71 only in this way.
RULED AT REVIEW: a defect, not a commitment and not an accounting item: one decision read two owners of one
fact. Fixed in the wrap-up (below); after the fix b2a + realized equals none + realized in all 16 conditions
at ρ 0.5.

Under plain cost, b2a differs from none on s20, s30 and s50 (both priors, both stop settings): B2 realizes
the current task on its own, and its `continue_hold` places the crossing hold (8 at 20, 7 at 28, 1 at the
grasp) although B3's cost is plain. The decisions and completions equal the realized cells (235 / 237 /
160 / 235). On s70 / s71 the stay's δ = 32 exceeds the bound (0.5 × 34 = 17), B2 escalates, and B3 on plain
cost takes item_1 without a hold, as none does (169 / 170; with the stop on, 204 / 205). b2a under plain is
realization for the current task only.

ρ sweep (existence test, b2a + realized, stop off, both priors, s20 / s30 / s50 / s70 / s71):

| ρ | differs from none? | where | why |
|---|---|---|---|
| 0.1 | s71_off only (the 108 lag above) | — | s20 / s50's 8-tick crossing hold exceeds the bound (0.1 × 36.24 = 3.62) and escalates; B3 on realized cost picks the same task with the same hold, so the verdict changes and the decision does not |
| 0.25 | s71_off only | — | every crossing hold is within its bound (8 ≤ 9.06, 7 ≤ its bound) and continues; the stay's 32 escalates as at 0.5; the verdict counts differ from 0.1, the decisions do not |
| 0.5 | s71_off only | — | the core cell |
| 1.0 | s70, both priors, and s71_off | s70 at 23: δ = 32 ≤ bound 34, b2a continues item_1 with a 32-tick hold (executed 31, replaced at the boundary 54) where none switches to item_2; order item_1 item_2 against item_1 item_2 item_1; completion 200 against 185 (after the fix: 198 prior off, the lag's two ticks removed; 200 prior on) | the only commitment decision in the set: b2a differs from none exactly when the current task's hold is within ρ × (T_h − now) AND B3 would have switched. s71 at ρ 1.0 is identical because B3's realized argmin is the held item_1 anyway |

Answer to the existence question: yes, once, as a commitment (s70 at ρ = 1.0, costing 15 ticks against the
switch; 13 prior off after the fix); and once as a two-tick lag (s71_off, any ρ), the defect fixed in the
wrap-up. Never on s20, s30, s50 at any ρ: at a table
convergence the held current task is B3's argmin, so continuing and re-selecting coincide.

What these fixtures cannot show: any case where committing is cheaper than switching (the one switch
available, s70, is the cheaper plan by 9 ticks and the commitment loses 15), a second robot task competing
with a switch (TODO-47 (c) stands), or a ρ effect at a crossing, since every crossing hold here is the
argmin's.

## (c) The separation stop: on against off

Gate none, cost realized (the b2a cells are the same runs modulo the lag in s71_off; the plain cells are
in `matrix.md`).

| fixture | blocked ticks off → on | outcome on | refusals: window; rule | robot violations off (a)/(b) → on | stand < s on: stop / hold / own / done |
|---|---|---|---|---|---|
| s00 | 0 → 139 | blocked to cap at the table, 2 of 3 delivered (161–299) | all outside (no projection); all (a) | 1/2 → 0/0 | 0/0/0/0 |
| s10 | 0 → 0 | 418, unchanged | — | 0/0 → 0/0 | 0/0/3/0 (the robot's grasp at 72–74, the human within s) |
| s20 | 0 → 158 (on-prior 156) | blocked to cap, 1 of 3 (144–299; plus 57–58 off-prior) | all outside; all (a) | 3/5 (2/4) → 0/0 | 0/0/0/0 |
| s30 | 0 → 48 (44) | blocked to cap, 1 of 2 (156–199; plus 21–24 off-prior) | all outside; (a) but one (b) at 22, the human closing on the standing robot | 2/3 (1/1) → 0/0 | 1/0/0/0 (0/1/0/0: the hold tick 22) |
| s40 | 0 → 29 | blocked to cap, 2 of 3 (371–399) | all outside; all (a) | 1/2 → 0/0 | 0/0/0/0 |
| s50 | 0 → 2 | done 237 (off: 235) | outside; (a) | 1/1 → 0/0 | 0/0/0/0 |
| s70 | 0 → 0 | done 185, unchanged | — | 0/0 → 0/0 | 0/0/0/0 |
| s71 | 0 → 4 | done 205 (off: 199 / 201) | outside; (a) | 1/2 → 0/0 | 0/0/0/0 |

Costs. Blocked time is where R2 put it: the human idling at the table after its script ends (s00, s20,
s30, s40: the last delivery refused to the cap, so these runs do not complete), the human's stay outlasting
the hold (s71, 4 ticks), or the robot arriving at the table under the human (s50, 2). Completion moves by
exactly the blocked ticks where the run completes (s50 +2, s71 +6 / +4). Decisions: the stop adds no
trigger (no blocked-execution event, D2) and changes the sequence only by the shifted timing (s20 / s50:
`no_current_task` at 65 instead of 63 after the 2 refusals; s71: the grasp at 73 instead of 69) or by the cap.

Prevents. With the stop off, every fixture but s10 and s70 has sequential-motion violations of the F1 rule by
the robot's own steps (totals per run 2 to 8, mostly (b), at the table convergence past T_h); with the stop
on, 0 in all 64 runs. The refusals are (a) throughout (the step would have brought the robot within s from
outside), with one (b) in s30 where the human walks up to the already-standing robot. In the realized cells
every refusal is outside the assessed window of the decision in effect (`outside(no_projection)`: past the
human's projection or under a decision that admitted none); the stop and realization do not overlap on these
fixtures, which is F47b's finding restated across the whole cross. In the plain cells the stop fires inside
the window (s70 / s71: 29 of 35; s30: 1 / 4) because the plain decision ignored the conflict its own
projection showed.

Human-borne proximity. With the stop on, the human is within s of a standing robot only during the robot's
own grasp (s10, 3 ticks) or a decided hold (s30 prior on, 1 tick); the 139 / 158 / 48 / 29 stop ticks
themselves are the human standing at the robot's goal. With the stop off, the sub-s ticks are almost all
after the robot's last delivery (139, 80, 48, 29 "done" ticks: the two agents idle at the table): the
point-place table, not a decision.

What these fixtures cannot show: what the stop does inside a realized decision's window (no refusal there),
a deviation from the projection other than a stay's end (F47b), or completion under the stop on s00 / s20 /
s30 / s40, whose human never leaves the table.

## Summary

- (a) Realization differs from plain cost on s20, s30, s50 (a hold at the one crossing, the same winner, +9
  to +11 ticks), s70 (a switch, +16 with the stop off, −19 with it on) and s71 (a 32-tick hold, +29 / equal
  with the stop on); identical on s00, s10, s40, where no hold is non-zero. It trades the violations plain
  commits for time, and with the stop on it moves the blocked time into decided holds. Not shown: a hold that
  changes a winner among several alternatives, or a worse order.
- (b) b2a differs from none once as a commitment (s70 at ρ = 1.0: keep item_1 with a 32-tick hold instead of
  switching, +15; +13 prior off after the fix) and once as a two-tick lag (s71_off, any ρ), a defect fixed
  in the wrap-up; never on s20 / s30 / s50 at ρ ∈
  {0.1, 0.25, 0.5, 1.0}, since a crossing hold is the argmin's. Under plain cost it acts as realization of
  the current task (s20 / s30 / s50). Fixture-bound: one switchable case, one robot task at a time
  (TODO-47 (c)).
- (c) The stop removes every robot-side violation (0 of 64 runs) at the cost of blocked time at the table
  (s00 / s20 / s30 / s40 do not complete; s50 +2; s71 +4 to +6), all of it outside realized decisions'
  windows and all of it rule (a) but one tick. Not shown: the stop inside a window, or a human who leaves.

## Observations for the design chat (not recommendations)

- B2 judges `executor_state.current_task`, which the executor closes one tick after the world fact; the pool
  drops the task on the fact (T7). When the D2 trigger fires on that tick (s71_off 108), b2a continues a task
  the pool no longer holds and none starts the next one. RULED at review: a defect (one decision reading two
  owners of one fact), fixed in the wrap-up.
- Under plain cost, b2a's `continue_hold` is the only place a hold enters; the cell "b2a + plain" is
  therefore realization restricted to the current task, not an ablation of realization. RULED at review:
  gate and cost are not independent axes (see the run matrix); no change to b2a.
- ρ decides only where B3's argmin is not the current task; on these fixtures that is one trigger (s70 at
  23). The ρ verdict counts move (escalations at 0.1 that continue at 0.25) without the decision moving.

## Wrap-up: `update()` never continues a task its own pool dropped as complete

The ruling: `update()` builds its pool from the world fact (T7), so a decision that then consults
`executor_state.current_task` reads a second, lagging owner of the same fact. Requirement: `update()` never
continues a task its own pool has dropped as complete. Built at B1.5 in `shared/meta_planner.py`: a current
task dropped at pool assembly is treated as no current task, so B2 is not asked and B3 decides. Docstrings
and `shared/io_contracts.md` (§2.2, Blocks) state it. No change to b2a, to B3, or to the executor.

Checked against the T6 logs (the pre-change baselines, same HEAD otherwise) on the CLAUDE.md greps plus
`[meta-b2]` / `[meta-b3]`, in `post_fix/` (git-ignored): gate none × realized × stop off / on (the regression
sweep and the evaluation fixtures), b2a × plain / realized × stop off / on, all eight fixtures, both priors,
and the ρ sweep. Five runs change, every gate-none run is byte-identical:

| run | before | after |
|---|---|---|
| b2a + realized, ρ 0.5, s71_off | 108 continues item_1; item_3 at 110; done 201 | 108 item_3, as none; done 199 |
| ρ 0.1, s71_off | as ρ 0.5 | as none |
| ρ 0.25, s71_off | as ρ 0.5 | as none |
| ρ 1.0, s71_off | 108 continues item_1; done 201 | 108 item_3; done 199 |
| ρ 1.0, s70_off | 108 continues item_1; item_2 at 110; done 200 | 108 item_2; done 198 (the commitment at 23 unchanged) |

s71_off under b2a now equals the none cell on `[meta]`, `[meta-pool]`, `[meta-proj]`, `[IR]`, `[IR-dist]`,
`[IR-complete]`, `[sep]`, `[hold]` and `[stop]`. `meta-cand` differs only in the B3 candidate lines that none
computes at mid-task triggers where b2a continues without running B3, as in every b2a run. These five are exactly the
pre-fix b2a runs in which B2 was called on a trigger whose pool assembly had dropped a task; in no other b2a
run does a trigger fall on that tick.
`matrix.md` stays the record of the T6 measurement at 9127b2a.

Regenerate `post_fix/` as the T6 sweeps with `post_fix/` in place of `core/` and `rho/`.

## Flags

- `metrics.py` copied `blocked.py`'s and F1 `evaluate.py`'s parsers because neither is importable without
  running its main body. Since the Phase 4C housekeeping all four scripts parse through `analysis/logparse.py`;
  `matrix.md`, C's `comparison.md` / `blocked.md`, F47's `blocked.md` and F1's `comparison.md` regenerate
  byte-identically (C's and F1's committed files carry a hand-added superseded note on top).
- The C `blocked.md` completion column is the declared tick (pre-D2 numbers); this task's tables are world
  ticks, two lower. Nothing in C's findings changes.
- `run.py`'s `T6_SEP_CM` path is written and smoke-tested but unused after the s sweep was dropped; left in
  as the record of the wrapper, not as an invitation to sweep s.

D3 note (September 2026): `task_committed` is removed from the trigger set (dd880be), so the task_committed count
in `metrics.py`'s decisions column (no_current_task / recognition_changed / task_committed) is 0 from D3 on.
