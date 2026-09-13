# I4b — the task-boundary origin reset, and the completion gate

Built on `3545d4a` (I4). Sweep: s00 (300 steps), s20 (200), s30 (200), s40 (400) × assignment_prior
off/on, `PYTHONHASHSEED=0`, interpreter `~/python-envs/teamrob-sp4-env/bin/python`. scenario_10 stays
dropped (TODO-52). β = 0.01 /cm and u = 0.1 unchanged. Baseline = I4's `run_mesa.py` logs at `3545d4a`
(`baseline/`, the same files as I4's `new/`).

**The one-paragraph result.** Candidate A — a retirement whose hypothesis expected its TERMINAL action
on the previous tick, i.e. the observed agent's own derived phase had reached the completing action —
fires at exactly the human's task boundaries in every condition (18 of 18, none at the robot's five
prior-off completions, none anywhere else) and is the only candidate that needs no new constant, no
invented rule and no microaction vocabulary; it was ranked first from the architecture and the
existing logs before any code was written (§2). Shipped, it reproduces the I4 what-if's chain
exactly: coffee's excess is 0 cm from tick 115 to the end of its walk, `ac_activation`'s grows at
1.8 cm per cm walked, and `coffee_break` crosses θ at 125 (0.759) and reaches the ceiling 0.904 by
150 in both prior settings (§4). s00, s20 and s30 are byte-identical to I4 on the four regression
greps: the boundary changes nothing where no hypothesis is stuck. Two findings qualify it. (1) The
principle's second sentence is not true of the recognizer's state: a never-advanced hypothesis's
charge lives in its open stretch, not in its base, so moving the origin DROPS it — that drop is the
coffee reveal (the `fold` variant, which keeps the belief literally, changes nothing anywhere), and
it applies unequally: a rival whose method flipped keeps its folds (item_6 stays at the floor;
criterion 4 not met), a hypothesis that never advanced returns to its prior (§3). (2) The reset
re-arms every surviving stuck hypothesis at zero excess, and zero excess is scored as a perfect fit
against `unknown`'s per-tick 0.1, so a lone survivor sits at 0.904 on the boundary tick with nothing
observed: `ac_activation` is above θ for 16 ticks after coffee retires and for the 46 idle ticks after
the last delivery — the "wrong-θ ticks (task)" 63 of criterion 3 (§5). Neither is the boundary's
doing; both are how I4's model scores a zero-length stretch, and both are for I5 (§8). The gate stays,
with a statement of what it withholds (§6): the ×10⁻³ false-alarm charge that a discrete event of the
action being performed would place, permanently, on every hypothesis whose expected action is
elsewhere — under the boundary that charge is the difference between coffee at 0.904 and coffee
never (`ungated` variant), and the "real cross-action evidence" the task worried about has value 1.0
under I4's detection model.

## How to read this directory

| File | Content |
|---|---|
| `candidates.py` | Task 1's measurement, from I4's CSVs and logs, no simulator: where A (phase), A (RELEASE), B, C(N) for N = 2/3/5 and D would fire, whether each firing is a task/segment change of the human, and the excess (cm) every live non-truth hypothesis holds on its open stretch there (what a reset drops). |
| `check_i4b.py` | The matrix. Reuses I4's harness (`check_i4.py`, given a `setup` hook); variants `nobound`, `A_release`, `B`, `C5`, `D`, `fold`, `ungated`, `ownshelf`; `--sweep` runs I4's fine grid under the boundary. |
| `summary.md`, `metrics.csv` | Per condition and variant: boundary ticks, crossings, reveals, wrong-θ ticks, the s40 segment metrics. |
| `sweep_abs_fine.csv` | The 25-cell fine grid under the boundary (criterion 6). |
| `trace.csv`, `excess.csv`, `phase_advances.csv`, `completions.csv`, `completion_events.csv` | As in I4 (per-tick CSVs: base for all conditions, variants for s40). I4's `chain.py --dir analysis/i4b_boundary` reads them. |
| `baseline/`, `new/`, `logs_instrumented/<variant>/`, `diffs/` | Not in git (`*.log`); `stages.sh` regenerates them (~6 min). `diffs/` is committed. |

---

## 1. What changed and where

| what | where |
|---|---|
| `_task_boundary(previous, actions)`: the retirement's hypothesis expected `actions[-1]` on the previous tick. In `update()`, a retirement that satisfies it sets `boundary`; after normalisation every live origin and origin odometer moves to the agent's position, logged as `[IR-boundary]`. The belief (bases, folds, events) is untouched; this tick's values were the old stretches' closing values; nothing is folded. Docstrings: the pin/reset distinction. | `shared/recognizer.py` |
| Evaluator validation at construction: an action schema naming a `progress_evaluator` not in the registry raises `ValueError` (a domain modelling error must not look like uncertainty — it would otherwise score every movement at the perfect fit, silently). | `shared/recognizer.py` (`__init__`), `shared/domain_knowledge.py` (`get_all_actions`) |
| `move_to.progress_evaluator = "excess_path"` (was the deleted `"directional"`). | `domains/dock_loading/actions.py` (one word) |
| `run_condition(..., setup=None)`; `chain.py --dir`. | `analysis/i4_evidence_model/` |

The pin and the reset — recorded in `design_decisions.md`: the terminal pin fires on the world's
completion condition, whoever satisfied it (the task cannot be done again); the reset fires only on
a completion the observed agent's own phase state accounts for (its behavioural reference frame
changed). Same event class, different criteria, deliberately not unified. Verification: unit checks
U1–U6 PASS; instrumented logs equal `run_mesa.py`'s in all eight; `nobound` equals the I4 baseline in
all eight; s40_on byte-identical under `PYTHONHASHSEED` 0/1/7; dock_loading imports and its schema
passes the new validation.

## 2. Task 1 — the four candidates

### 2.1 From the architecture

What the recognizer exposes per tick: the observed agent's position and microaction; per hypothesis
the planner's grounded action list, the derived expected action, the previous tick's expected action,
the origin; retirements (terminal completion held). What it does not have: who satisfied a predicate
(I1 finding 5), the agent's executor state, a task list.

| | operational meaning | what supports it | generic? | new constant / rule | domain assumption |
|---|---|---|---|---|---|
| **A (phase)** | a retirement whose hypothesis expected its terminal action on the previous tick | the phase state the recognizer already keeps (`_expected`) and the planner's action list | yes: any domain with terminal completion conditions | none | an agent whose derived phase reached the terminal action is the one who completed it |
| A (RELEASE) | a retirement on a tick where the observed agent's microaction is in the terminal action's vocabulary | the observation stream + the schema's microaction list | only for actions with a discrete vocabulary | none | tasks end in an observable discrete microaction — kitting's deliveries do (`place` → RELEASE), its waits do not (`wait_at` → `STAND*`, a pattern, not a list) |
| B | after any retirement, the first tick at which any hypothesis's expected action changes | retirements + per-hypothesis advances | yes | the rule "which hypothesis's advance counts" — I had to take "any" | none |
| C (stop) | the N-th consecutive stationary tick | positions only | yes, and to domains with no completable tasks | N, and it fires on every stop | that pauses and task boundaries coincide |
| D | any tick at which any hypothesis's expected action changes | per-hypothesis advances | yes | none | none |

A is the only candidate that is literally the thing meant (the observed agent finished a task) and
needs nothing the recognizer does not already hold. Its assumption is named: authorship is inferred
from the agent's own derived phase, not read from the world. In kitting it cannot misfire — a
hypothesis expects `place(X, table)` only while the agent holds X, and `waited(agent, ·)` names the
agent — but a domain where another agent can satisfy a terminal condition while the observed agent
stands in its terminal phase would attribute wrongly. The RELEASE reading is the domain-assumption
version of A and was predicted to miss coffee at 184 from the schema alone. B needs a rule. C needs N
and its alignment with boundaries is an empirical question, answered below from the logs. D is the
degenerate end.

### 2.2 From the existing logs (`candidates.py`, no runs)

Truth boundaries: the ticks where the human's task or s40 segment changes. "Forgiven" = Σ excess of
live non-truth hypotheses at the firing (what a reset there drops).

| candidate | firings | at a boundary | off-boundary firings forgive (cm) | note |
|---|---|---|---|---|
| **A (phase)** | 18 | 18 | 0 | every human release and the coffee `waited`; none of the five prior-off robot completions (31/93/166, 52/136, 86/156, 145/243/376: the hypothesis expected `move_to`, not `place`) |
| A (RELEASE) | 16 | 16 | 0 | misses 184 (coffee) in both s40 conditions |
| B | 19 | 12 | 23,621 | prior-off fires at the next advance after a ROBOT completion, mid-approach: s00_off 39 (2,300 cm of decoy excess dropped), 109; s20_off 52 (3,347); s30_off 96 (1,162); s40 270 (item_6's arrival at shelf_6) |
| C(2) | 30 | 0 | 90,322 | every arrival stop |
| C(3) | 30 | 14 | 16,744 | grasp stops too |
| C(5) | 16 | 14 | 9,531 | place stops are 5 ticks, grasp stops 4: N = 5 separates them by ONE tick of kitting's executor timing; fires mid-wait at 157 (harmless, the agent does not move) and never at the wander stops (1 tick) |
| D | 74 | 12 | 132,250 | every 30 cm arrival and departure |

The stop data: s00 39–42 (4), 76–80 (5), 109–112 (4); s20 20–23 (4), 52–56 (5), 87–90 (4), 120– (idle);
s30 37–40 (4), 72–76 (5), 96–99 (4), 119– (idle); s40 58–61 (4), 113–117 (5), 153–186 (34), 329– (idle).
The wander waypoints (207–209, 228–230) are not stops at all in the position stream. So stops track
task boundaries in these data only through a one-tick timing accident (a place stop lasts one tick
longer than a grasp stop) — C is not dead but its N cannot be set from a principle, and no N sees the
one boundary A cannot see either (segment 3's waypoints). The measurement settles Task 1 without a
run: A (phase) fires where the semantics say and forgives nothing off-boundary.

### 2.3 In the matrix (`summary.md`)

| variant | first-task reveals | coffee (s40) | wrong-θ ticks (task), s40 | other |
|---|---|---|---|---|
| **A (shipped)** | unchanged from I4 (s00 39/11, s20 31/6, s30 28/21, s40 19/19) | 125 → 0.904 both | 63 (ac 185–200, 333–378) | s00/s20/s30 byte-identical to I4 |
| A (RELEASE) | unchanged | 125 → 0.904 | 47 (ac 333–378 only: the miss at 184 leaves ac's 1,190 cm charge in place) | a better number by a domain accident |
| B | unchanged prior-on; s00_off 52 second crossing | 125 | 106 off / 42 on | s20_off 54 item_6! 77 unknown!, s40 at 272 `ac` |
| C5 | unchanged | 125 | 82 | 184/210 ac!, 262 unknown! |
| D | second-task reveals appear (s00_on 80, s20_on 56, s30_on 76 pre-grasp) | 135/143 | 101 on / 38 off | 24/6/7 wrong prior-off, TODO-52 crash s20_off 142 |
| fold | unchanged | **never** (0.001) | 0 | identical to I4 everywhere |

D's second-task reveals are not discrimination: it resets at every 30 cm arrival, two ticks before
each grasp and release, so every fold the method flips would have taken is of a zero-length stretch —
the permanent charges of I4 §3.3 are neutralised by timing, long-range commitment stops accumulating,
and prior-off it hands the idle human to the robot's items (s00_off 142 item_4!, s20_off 136 item_7!,
s30_off 161 item_6!). It is the degenerate case the task predicted, reached in full.

## 3. The principle, as the state actually holds it

"Reset the geometry, keep the belief; their charge is already in the belief." The recognizer keeps
two things per hypothesis: the base (folded phases and events, persistent) and the open stretch's
value (recomputed from the origin every tick, REPLACED, never in the base). For a hypothesis whose
expected action has never changed — coffee, `ac_activation`, every task the agent has not started —
the whole charge is in the open stretch. Moving its origin drops that charge; nothing else can happen.
Measured both ways:

- `fold` (base ×= open value, then move the origin — the belief at the boundary tick preserved
  exactly): identical to I4 in all eight conditions; coffee 0.001 for ever. The literal reading of
  "keep the belief" is inert.
- shipped (origins move, bases untouched — the text's operational sentence): coffee's 2,144 cm is
  gone at 116 (0.001 → 0.474); that drop IS the reveal.

And it is unequal: item_6, whose method flipped twice during segment 1, carries ×3e-9 × 1e-9 in its
base and stays at the floor through segments 2–4 (criterion 4 not met — §5); coffee, whose method
never flipped, returns to its prior. The difference between the two is not semantic; it is whether
`deliver_with_return`'s guard happened to select a different method under the hypothesis while the
human carried item_3 (TODO-55 (d)'s point). Under `ownshelf` (rivals decomposed as if nothing were
held — no flip, no fold) the boundary treats every hypothesis alike and item_6 gets exactly the
fixture's shape (§7). Not chosen here; recorded.

## 4. coffee_break under the shipped boundary — the chain (`chain.py … --dir analysis/i4b_boundary`)

s40_on; prior-off identical to three decimals (`unknown` 0.092 instead of 0.094).

| step | segment | human | coffee excess | L | base | P(coffee) | strongest other | P(unknown) |
|---|---|---|---|---|---|---|---|---|
| 114 | 1 | carry | 2143.8 | 0.000 | 0.91 | 0.001 | item_3 0.904 | 0.093 |
| 115 | release — **boundary** | | 0.0 | 1.000 | 10 | 0.001 | unknown 0.997 | 0.997 |
| 116 | | place | 0.0 | 1.000 | 0.48 | 0.474 | ac 0.474 | 0.051 |
| 118 | 2 | walk | 0.0 | 1.000 | 0.51 | 0.502 | ac 0.443 | 0.054 |
| 120 | 2 | walk | 0.0 | 1.000 | 0.57 | 0.570 | ac 0.368 | 0.061 |
| 125 | 2 | walk | 0.0 | 1.000 | 0.76 | **0.759** | ac 0.160 | 0.080 |
| 130 | 2 | walk | 0.0 | 1.000 | 0.87 | 0.866 | unknown 0.091 | 0.091 |
| 140 | 2 | walk | 0.0 | 1.000 | 0.91 | 0.903 | unknown 0.094 | 0.094 |
| 150–183 | 2 | walk, wait | 0.0 / wait | 1 | 0.91 | 0.904 | unknown 0.094 | 0.094 |

The chain is the what-if's: coffee's excess stays at 0 for the whole walk; `ac_activation`'s grows
from 0 at the table at 1.8 cm per cm walked (the switch is 100° off the coffee bearing: 39 cm at
tick 118, 165 at 120, 245 at 125), its value 1.000 → 0.16 by 125; item_6 is at the floor; `unknown`
0.1. Coffee crosses θ at 125 and reaches the ceiling 1/(1+u) = 0.909 by 150. Coffee gains support
because its competitors' excess grows while its own stays at zero — the claim as stated, confirmed,
with one correction to the wording: nothing's excess FALLS; the boundary set every excess to zero and
only coffee's stayed there.

item_6 over segment 3 (excess only — its base is ≈ 0, §3): 0.0 through 3a (the walk to wander_0 is a
walk toward shelf_6), 28.5 at 210, 208 at 216, 539 at 227 — the retraction is real in the geometry and
at the floor in the posterior, exactly as in I4. `ac_activation` over the same stretch is the lone
survivor: 0.0 excess and 0.904 at 185 with the human standing at the coffee machine; 39 cm / 0.884 at
190; 165 cm / 0.759 at 200; 245 cm / 0.611 at 206 (end of 3a, 55° off the switch); 402 cm / 0.258 at
213 after the turn; 0.002 by 227. `unknown` wins from 211.

## 5. Acceptance

| # | criterion | outcome | evidence |
|---|---|---|---|
| 1 | boundary justified by semantics + Task 1's measurements, rejected candidates' numbers reported | yes | §2: A is the only definition that is the thing meant and needs nothing new; 18/18 at boundaries, 0 cm forgiven off-boundary; RELEASE misses coffee (16/18), B forgives 23,621 cm at robot completions and needs a rule, C needs N = 5 from a one-tick timing accident and forgives 9,531 cm, D forgives 132,250 cm and collapses to the current leg. Not by the coffee outcome: `fold` (§3) and RELEASE (§2.3) both reveal coffee too. |
| 2 | coffee_break's behaviour, plainly | **crosses θ at 125 (0.759), 0.904 from 150 — both prior settings**, by the what-if's chain (§4). No part of the chain differs. |
| 3 | I4's results hold | **partly** | s30 mid-approach 21/28, TODO-53 closed (ac 0.001 at 272, `most_likely` 0 ticks in 231–271), no delivery ≥ θ in segment 2 (0.001), s00/s20/s30 byte-identical. **New wrong reveals: yes** — `ac_activation` ≥ θ at 185–200 (segment 3a, 15–16 ticks, both settings) and 333–378 (the idle tail, 46 ticks); 63 wrong-task ticks vs I4's 0. Mechanism in §8(a): zero excess is scored as a perfect fit against `unknown`'s 0.1, so a lone surviving stuck hypothesis is at 0.904 on the boundary tick with nothing observed. Not a crossing event under the meta-planner's rule (TODO-48: confidence stays above θ across the winner change at 184/185), but a wrong `most_likely` above θ. |
| 4 | segment 3b retraction visible | **no** | item_6 0.001 → 0.001; its excess 0 → 539 cm through 3b is the right shape, its base carries the two segment-1 folds (×3e-9 × 1e-9), and a boundary that keeps the belief keeps them (§3). Visible under `ownshelf` + boundary (0.79 → 0.083) and under D. |
| 5 | the gate decision with its statement | §6: stays, with the statement. |
| 6 | working region still wide | **yes** | fine grid β ∈ {0.005…0.02} × u ∈ {0.05…0.2}: first-task pre-grasp reveals in 24 of 25 cells (s30 at β = 0.005, u = 0.2 is at 39, the grasp tick), no wrong crossing; identical reveal ticks to I4's grid. coffee ≥ θ in every cell (0.83–0.95, 48–63 ticks). The boundary's cost is also in every cell: ac `most_likely` 12–37 ticks in 184–271, 53–78 wrong-task ticks, monotone in β and u (a smaller u or larger β shortens the lone-survivor stretch). Nothing narrows. |
| 7 | every difference attributed | §9. |

## 6. Task 2 — what the completion gate withholds

Under I4's detection model a completion check returns 1.0 (hit) or 10⁻³ (false alarm). A hit is the
multiplicative identity. So the ungated channel adds exactly one thing to the gated one: the false-alarm
charge on every hypothesis whose expected action's completion does NOT hold at a discrete tick. The
"real cross-action evidence" the task named — a rival expecting `move_to(shelf_X)` when the human grasps
at shelf_X, `at(agent, shelf_X)` holding — is a hit: ×1.0, no information, in both readings. Measured:
of 124 ungated events in the I4 matrix and again under the boundary, 16 are hits, all on `pick_up`
(the grasped item), and 108 are false alarms, all on `move_to`; zero hits on a movement action.

**Statement.** The gate withholds the permanent ×10⁻³ that a discrete event of the action being
performed would place on every hypothesis whose expected action is elsewhere. That charge is
generatively correct for a FIXED intention (a walker to shelf_Y does not emit GRASP at shelf_X) and
it is permanent by design (an event multiplies into the base). Under sequential tasks it turns every
grasp and release of task N into a refutation of every task the agent has not started — coffee and
`ac_activation` receive it at 60 and 115 in s40 (`completion_events.csv`) — and the boundary reset
cannot undo it (it moves origins, not bases). The movement channel already carries the same fact (the
wasted path to shelf_X instead of shelf_Y) in the one form the boundary can reset. So withholding is
right, and the gate is not redundant under the phase model: it is what keeps the event channel from
being a second, unresettable copy of the movement channel.

**The divergences.** (i) s20_off: the two decoys beyond item_3 on the same bearing (excess 11 and
61 cm at the grasp) are not separated by the walk; ungated, the grasp charges them and the reveal
moves from 31 to 22. Real evidence about the CURRENT intention, and the one case where withholding
costs something (9 ticks, one condition). (ii) s40 with the boundary: `ungated` gives coffee 0.001
for ever — the ×10⁻³ × 10⁻³ from the grasp and release of item_3 is in coffee's base when its walk
begins. Under the boundary the gate is the difference between a coffee reveal and none.

**Decision: the gate stays**, for the reason above, not by inheritance and not because of s20_off. If
a grasp-tick reveal of the current task is wanted, the honest mechanism is a completion charge that
the boundary can reset — an event whose scope is the current task — which is a change to the event
channel's semantics, recorded for I5, not a gate flag.

## 7. TODO-55 re-measured under the boundary (`ownshelf` = reading (c); not settled)

Under (a), the shipped code: next-task reveals never, in all eight conditions (unchanged from I4 —
the rival's carry folds are in its base and the boundary keeps them). Under (c) + boundary: the
approach excess a rival accumulated from t = 0 is dropped at the human's release (no method flip, no
fold), so next-task reveals appear PRE-GRASP prior-on — s00_on 80 (grasp 111), s20_on 56 (89),
s30_on 76 (98) — and post-grasp prior-off (s00_off 116, s20_off 95; s30_off 87 pre-grasp), with
prior-off wrong crossings on the idle human (s20_off 136 item_7!, s30_off 161 item_6!, s40_off 376 ac!:
the lone-survivor effect of §8(a) on the robot's undelivered items) and TODO-52's crash in s20_off at
142. In s40 (c) gives the fixture's shape: coffee 135/143, item_6 0.47 → 0.79 through 3a (203 crossing,
truth `unknown` — the walk toward shelf_6), 0.80 → 0.083 through 3b, 0.08 at its own grasp (its
segment-3 excess of 539 cm is not reset: no boundary between segments 3 and 4). I4's finding stands
with one change of sign: with a boundary in place, reading (c) is no longer "identical to (a)"; it is
the reading under which every hypothesis is treated alike at the boundary (§3). (b), (d), (e) not
measured here. No reading chosen.

## 8. What remains open — for I5

**(a) A zero-length stretch is scored as a perfect fit.** L(0) = 1 and `unknown` pays 0.1 on every
tick, including a tick on which nothing has been walked. After a boundary every surviving stuck
hypothesis is at parity, and when only one survives it is at 1/(1+u) = 0.909 before the agent moves
(ac at 185 and at 333–378 here; at t = 0 the same would hold in any one-task space — no current
scenario has one). This is I4's model, not the boundary; the boundary exposes it because it manufactures
zero-length stretches mid-run. The candidates are semantic, not tuning: `unknown`'s value as a
function of what has been observed on the stretch (u per unit of evidence rather than per tick), or the
belief at a boundary re-primed from the prior for hypotheses with no folds (TODO-55 (b) restricted).
Out of I4b's scope (the likelihood form, u).

**(b) The boundary keeps the belief unequally** (§3): folds are permanent and whether a rival folded
during the previous task depends on the method its guard selected under the carry. TODO-55's readings
(b), (d), (e) and `ownshelf`'s numbers are the material.

**(c) The boundary the recognizer sees is the one its phase state accounts for.** Segment 3's waypoint
stops are invisible to A, and to every candidate (they are 1-tick pauses that retire nothing). A
domain whose tasks end in a `ProcessCompletion` has no boundary at all. Named, not solved.

**(d) The event channel is unresettable by construction** (§6): an event scoped to the current task
would need a different bookkeeping from "multiply into the base".

## 9. Attribution of every difference from I4 (`diffs/*_base_to_new.txt`)

s00_off, s00_on, s20_off, s20_on, s30_off, s30_on: **identical** on `[IR]`, `[IR-dist]`, `[meta]`,
`[meta-cand]` — the boundary fires (78/142, 54/122, 74/121) and moves the origins of hypotheses whose
bases are ≈ 0; the delivered item is pinned; nothing live is stuck. s40_off and s40_on, three
episodes, both settings alike (the robot's completions do not fire): (1) 116–183: coffee 0.001 → 0.474
(116) → 0.904, `ac` 0.001 → 0.474 → 0.001, `unknown` 0.993 → 0.05–0.09 — the reset at 115 (§4);
(2) 185–233: `ac` 0.001 → 0.904 → 0.002, `unknown` 0.993 → 0.09 → 0.997 — the reset at 184, the lone
survivor (§8(a)), its excess 0 → 918 cm; (3) 332–378: `ac` 0.904, `unknown` 0.09 — the reset at 331
with no live rival and no movement. `[meta]`: two new `theta_crossed` (125 coffee, 214 `unknown`), the
robot's winners unchanged.

## Flagged, not fixed

- `theta_crossed` does not fire on the 184 → 185 winner change (confidence stays above θ): TODO-48.
- TODO-52's crash returned in the `D` and `ownshelf` what-ifs (s20_off, 142).
- `check_i4b.py`'s `C5` and `B` are harness-side approximations of candidates the recognizer would
  implement differently; their numbers are for ranking, and the ranking did not depend on them.
