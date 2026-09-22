# M1 — An earlier recognition trigger on scenario_30 (θ = 0.65 vs 0.75)

CLEANUP NOTE (September 2026): only this report is kept. The scripts, `realization.md` / `.json`, `why.md` /
`why.py` and the local logs it names below are deleted; the finding is carried in design_decisions.md ("θ has one
home") and TODO-64, and the tables here are the record of the rest.

Exploratory, measurement only. Code at HEAD `fd183b3` (R1 + T9). `shared/` untouched: θ is forced
per process by wrapping `MetaPlanner.__init__` in the analysis scripts (the T1b pattern), and no
θ change is committed. Four runs, `PYTHONHASHSEED=0`, `env_layout3` / `scenario_30`, 200 steps,
assignment prior off/on × θ ∈ {0.75, 0.65}. All four run to completion (`all tasks complete` at
step 154). Nothing below proposes a change to any default, threshold or document.

Units: ticks (1 tick = 20 cm of motion), distances in cm. δ = hold. T_r = the candidate's projected
duration, T_h = the end of the human's projection, both measured from the trigger tick.

**Where θ lives.** One place: `MetaPlanner.__init__(theta=0.75)`, stored as `self._theta` and read
in exactly two of its methods — `evaluate_triggers()` (the `theta_crossed` crossing test,
`prev < θ ≤ now`) and `update_human_projection()` (projection admission, `confidence >= θ`). Both
were changed together, which is the only consistent reading. `mesa_sim/sim_agents.py` does not pass
`theta`, so the constructor default governs every run. `shared/recognizer.py`'s
`CONFIDENCE_THRESHOLD = 0.75` is dead: nothing in `shared/` or `mesa_sim/` reads it (only
`analysis/i1_ir_audit/measure.py` does), so it was left alone.

## How to read this directory

| File | Content |
|---|---|
| `stages.sh` | Regenerates everything (~1 min). |
| `run_theta.py` | One plain run at a given θ, delegating to `run_mesa.run_headless()` so the log format, `[sep]` included, is the real one. |
| `capture.py` | T1b's `measure.py` (imported unchanged) over the four conditions → `captures.json` + `logs_instrumented/`. |
| `realize_m1.py` | T1b's realizer offline at s = 50 under R1's policy → `realization.md`, `realization.json`. |
| `why.py` | Hold budget vs shift needed per trigger and candidate → `why.md`. |
| `logs/`, `captures.json`, `logs_instrumented/` | Git-ignored; md5s below. |

**Verification.** The two θ = 0.75 runs are byte-identical to the T9 baselines
(`analysis/t9_arrival_radius/new/s30_off.log` f74121c2, `s30_on.log` 3f40a04e). The instrumented
logs are byte-identical to the plain runs minus their `[sep]` lines, in all four conditions.

---

## 1. First `theta_crossed` on the human's correct hypothesis

The human's actual first task is `deliver_item(item_3)`, and `most_likely` is correct at every
crossing in all four runs. Positions are as the meta-planner sees them at decision time: the robot
before its move this tick, the human after its move (within a tick the human acts before the robot
observes — `RobotAgent.observe_initial`).

| run | θ | step | confidence | robot pos / action | human pos / action | robot–human distance |
|---|---|---|---|---|---|---|
| s30_off | 0.75 | **28** | 0.775 | (58.5, −130.2) / move_to, step | (−71.3, −145.6) / move_to, step | 130.7 |
| s30_off | 0.65 | **24** | 0.653 | (7.3, −68.7) / move_to, step | (−20.1, −84.1) / move_to, step | 31.4 |
| s30_on | 0.75 | **21** | 0.761 | (−31.1, −22.7) / move_to, step | (18.3, −38.0) / move_to, step | 51.8 |
| s30_on | 0.65 | **15** | 0.651 | (−107.9, 69.5) / move_to, step | (95.1, 54.2) / move_to, step | 203.7 |

Prior-on the crossing moves 21 → **15**, matching your expectation. Prior-off it moves 28 → **24**;
the "21 or 22" figure is scenario_20's, not scenario_30's. Both agents are walking to their shelves
at every one of these ticks.

The layout is the mirror crossing: the two walk symmetric opposite paths, robot at (−x, y) and human
at (+x, y), and pass each other at tick 22 at **11.0 cm** (the `[sep]` minimum). The four triggers
therefore sit on different sides of that pass — step 15 seven ticks before it, 21 and 24 inside it,
28 six ticks after it. That placement, not the θ value itself, is what decides everything in §3.

The second crossing (on `deliver_item(item_7)`, also correct) moves 86 → 84 prior-off and stays at
77 prior-on, where confidence jumps 0.498 → 0.905 in one tick and crosses both thresholds together.

## 2. Extra triggers, and decisions

**No extra triggers.** Seven fired triggers per run at both θ, the same seven kinds in the same
order; the two `theta_crossed` events move earlier, nothing else appears. No trigger fires on a
wrong hypothesis or on `unknown` at 0.65 that did not already do so at 0.75 (prior-off's step-76
`no_current_task` carries a wrong `most_likely` at 0.249 and prior-on's step-154 one carries
`unknown` at 0.995, in both settings; neither is admitted).

**No decision changes.** Identical winner sequence in all four runs: item_4 at 0, 24/28 and 40, then
item_2 at 76, 84/86 and 114, complete at 154. Excluding `[meta*]` and `[executor]` lines, the θ =
0.65 log is **byte-identical** to the θ = 0.75 log in both priors — same per-tick positions, same
`[IR]` / `[IR-dist]`, same `[sep]`. The only non-`[meta]` difference is that the `[executor]
continue_plan` line moves to the earlier tick with a longer remaining microaction queue: a continue
that costs nothing (T5).

This is the flag in the task confirmed by measurement: realization is not built and
`min_safe_distance = 1.0` is inert (no `feasible=False` in any of the four runs, minimum observed
`min_dist` 15.4 cm), so B3 is plain-cost argmin and item_4 is the cheapest candidate at every
trigger under both settings. An earlier projection changes nothing the robot does.

## 3. What realization would have given (s = 50 cm)

R1's policy — whole-trajectory minimal shift, one δ at the robot's trigger position, realizable iff
no violation in [trigger, T_h], with R1's hold cap — computed offline with T1b's `realize_whole`
over these runs' own candidates and human projections. Admitted triggers only; where no projection
is admitted realization is not called, by design. Full table in `realization.md`, the decomposition
in `why.md`.

Two quantities decide each row. **Shift needed**: the smallest δ at which every shifted segment is
clear. **Hold budget**: the latest a hold at the robot's trigger position may run to before the
human walks within 50 cm of that spot — Property 1 (a hold is a position) makes this an upper bound
on δ. Realizable iff shift needed ≤ hold budget.

### The crossing triggers — the comparison asked for

| run | θ | step | cand | T_r | T_h | unheld min dist (absolute tick) | shift needed | hold budget | outcome |
|---|---|---|---|---|---|---|---|---|---|
| s30_on | 0.75 | 21 | item_4 (current) | 49.68 | 48.68 | 15.4 (22.93) | 2.26 | **0.26** | unrealizable |
| | | | item_2 | 61.45 | 48.68 | 22.7 (22.63) | 2.07 | 0.26 | unrealizable |
| s30_on | 0.65 | **15** | item_4 (current) | 55.68 | 54.68 | 15.4 (22.93) | 2.26 | **38.07** | **realizable, δ = 2.26** |
| | | | item_2 | 67.19 | 54.68 | 40.3 (21.83) | 0.72 | 38.07 | realizable, δ = 0.72 |
| s30_off | 0.65 | 24 | item_4 (current) | 46.68 | 45.68 | 16.7 (69.73) | 2.14 | **0.00** | unrealizable |
| | | | item_2 | 58.63 | 45.68 | 31.4 (24.00) | 0.97 | 0.00 | unrealizable |
| s30_off | 0.75 | **28** | item_4 (current) | 42.68 | 41.68 | 16.7 (69.73) | 2.14 | **∞** | **realizable, δ = 2.14** |
| | | | item_2 | 54.97 | 41.68 | 130.7 (28.00) | 0.00 | ∞ | realizable, δ = 0.00 |

**Prior-on: yes, the conflict is resolvable earlier where it is not later.** The conflict is the
same physical event in both rows — the tick-22.9 pass, 15.4 cm at its closest — and the shift that
fixes it is the same, δ = 2.26. From step 15 the robot may take it: the human does not reach its
parking spot for another 38 ticks. From step 21 it may not: the human is 51.8 cm away and walking
through that spot within 0.26 ticks. Probing the blocked case (`realize_m1.py`'s geometry, sampled):
δ = 0 violates at the crossing; δ = 0.26 or 1.0 clears the crossing but then violates at the table
at 18.8 / 29.4 cm; δ = 2.26 clears the trajectory but puts the human within **47.82 cm** of the
standing robot. The step-21 trigger fails by 2.2 cm on a 50 cm threshold — genuinely pinched, and
close enough to the threshold that this one row would flip at s ≲ 47.8.

**Prior-off: no — earlier is worse.** Both prior-off triggers are already past the tick-22 pass, so
the conflict they are asked to fix is the later table convergence at tick 69.7 (the second `[sep]`
run, 69–76). δ = 2.14 fixes it. At step 28 the robot has cleared the human's corridor and may hold;
at step 24 it is still inside it, 31.4 cm from the human, so the budget is zero and nothing is
realizable. Prior-off, the tick-22 pass itself is never assessed at either θ: no projection is
admitted before it happens.

So the effect is **not monotone in trigger time**. What matters is whether the trigger lands before,
during, or after the encounter: before it, a small hold resolves it; during it, the robot is itself
the obstacle and hold-only realization has no answer; after it, only the next conflict is in scope.
θ = 0.65 moves prior-on from "during" to "before" and prior-off from "after" to "during".

### Costs, winners and the assessed share

The realized argmin picks the same task as the log at every admitted trigger in all four runs
(`realization.md`, last two columns) — item_4 then item_2 — so realization would not change any
selection here either. What it adds is the hold: prior-on at θ = 0.65, item_4 wins at realized cost
57.94 (T_r 55.68 + δ 2.26) against item_2's 67.91, and the robot would stand still for 2.26 ticks
and not pass the human at 11 cm.

The earlier trigger also assesses more of the plan, because the human's remaining projection is
longer: unassessed share (T_r + δ − T_h)⁺ / (T_r + δ) is **0.06** at step 15 against 0.24–0.32 at
the later admitted triggers of the same run, and 0.86 at step 114 where the human is nearly done.
The two `task_committed` triggers at step 40 are identical across all four runs (δ = 3.13 for
item_4, unassessed 0.09) — the same tick, the same geometry, unaffected by θ.

## 4. Actual minimum robot–human separation (`[sep]`)

Identical in all four runs, as §2 implies:

| run | min during execution (tick) | ticks < 50 cm during execution | min after both idle |
|---|---|---|---|
| s30_off θ 0.75 / 0.65 | **11.0** (22) | 18 (21–24, 69–76, 148–153) | 25.3 |
| s30_on θ 0.75 / 0.65 | **11.0** (22) | 18 (21–24, 69–76, 148–153) | 25.3 |

The three sub-50 runs are the mirror crossing (21–24), the table convergence (69–76) and the final
placement next to an already-parked agent (148–153). The measure matches the T9 baselines exactly.

## Observations, recorded not acted on

1. **The minimal shift clears with no margin.** The realized trajectory at step 15 has a sampled
   minimum of **50.09 cm** against a 50 cm requirement — by construction, since δ is minimal. TODO-77
   measures the projection running 1 to 6 ticks ahead of execution; that is of the same order as
   δ = 2.26, so a hold computed this way is not robust to the timing bias that is already known to
   exist. Relevant to T3's validation and to T10, not resolved here.
2. **Whenever the two agents are already within s at decision time, the hold budget is zero** and the
   only realizable δ is 0 (s30_off 24, s30_on 77). Realization has nothing to offer once the
   violation has begun; that is the territory of the execution-time avoidance assumption (TODO-73).
3. This is one fixture and one separation value. The prior-on result rests on a single trigger whose
   margin is 2.2 cm, and the prior-off result on two triggers straddling one encounter.

## Tree state

Unchanged apart from this directory. No θ change on disk; `git status` shows only
`analysis/m1_theta_earlier/`. Logs, `captures.json` and `logs_instrumented/` are git-ignored, as in
the T1b and T9 directories. md5s of the four plain logs:
`s30_off_t075` f74121c2d0bb6c125bef6a7ba6443803, `s30_on_t075` 3f40a04e1d5888acfc492162f62ab3af,
`s30_off_t065` 82fd34a7f352800f3099e46353f346e5, `s30_on_t065` 10906e9badabe40315e965770d7f6a37.
