# The meta-planner test-bed: the coverage matrix (MPB, post-(iv) records, 29 September 2026)

Which decision paths of the recognition-to-planning chain the eleven verified scenarios instantiate, and, for every
path they do not, whether the framework can reach it in scope. UPDATED at part (v) (30 September 2026): the five
reachable claimed cells are verified by one authored instance each (rows A4, C2, D8, D9, E6); the MPB is closed
(Closure, below). Derived from the committed outputs of the eleven runs
(`scenario_*/on_single_task/` and `on_full_reorder/`: `actual_decisions.json`, `selection.json`, `robot.json`,
`expected_ticks.json`, `observed.json`), prior on. No run was made for it. Nothing is authored in this step.

## What a cell is

A row is a materially different decision path, not a product of the dimensions: a combination the records make
identical to another row (the same refusal, the same projection, the same selection rule) is covered by type, as the
coverage principle states (design_decisions.md, "The meta-planner test-bed (MPB)", the COVERAGE PRINCIPLE). The
dimensions:
- **the trigger and its cause:** `no_current_task`; `recognition_changed` with cause entered, replaced, boundary or
  retraction; `projection_expired`;
- **the gate's outcome:** below θ; no observation; inadequate; unwarranted; clears by commitment, by observation, by
  both;
- **the projection the decision rests on:** an admitted plan; a moving fallback not cut, cut at the wall, at an object,
  at a landmark; a standing fallback; none;
- **the robot's state at the decision:** idle, walking to a shelf, carrying;
- **the selection:** continue; select with hold zero; select with hold positive; a switch of task.

Every cell has one of three kinds (the coverage principle as extended by the matrix; MPB-2, dated line):
- **verified:** an instance in a verified run, (scenario, tick) given;
- **unreachable:** no instance, and a derivation from the records that the framework cannot reach it in scope;
- **out of coverage:** no instance, and a recorded reason why it is not part of the mechanism the MPB claims.

Two labels mark the cells between: **reachable** (no instance, and the derivation shows it can be reached: to be
authored or ruled), and **not a distinct path** (reachable, and identical in its decision to a verified row).

How a decision is classified (from the committed outputs):
- the robot's state is read on the tick before the decision (`robot.json`): no task, or the `no_current_task` trigger,
  is idle; carrying an item is carrying; otherwise walking to a shelf;
- a switch is a winner other than the task the robot held, that task not completed: a decision on the tick after the
  robot's own release is a new selection, not a switch (scenario_s10_03 at 121, scenario_s10_08 full_reorder at 135);
- a moving fallback is cut when its duration is below its run length k; what cut it is found with the oracle's own
  geometry (`mpblib.reach`: the wall, or the first fixed object's arrival radius along the ray; landmarks are fixed
  objects, "T-D P", P4, AS BUILT);
- the shared ticks are found by replaying `chain.py`'s rules (C1 to C4) without the masking.

Instances are single_task (S) unless marked full_reorder (F).

## The whole-set facts

Measured on all 22 prior-on runs (169 decisions under single_task, 158 under full_reorder):
- **The cause boundary fired in no run.**
- **Every admitted record ended before its T_h:** at a replaced boundary, at a retraction, or at the robot's own
  decision. No robot ran past an admitted projection's end with the record standing.
- **No record was kept through a dip below θ:** on every tick a record stood, its hypothesis led and the gate cleared.

Re-measured at part (v) on the sixteen (32 prior-on runs, 240 decisions under single_task, 227 under full_reorder): the
cause boundary fires in scenario_s10_11 only (53, both strategies); every admitted record still ends before its T_h (no
P3 exposure); the only record kept while the gate refuses is scenario_s10_10's (the regress at 31, the dip at 34 to 36).

## A. The trigger and its cause

| row | instance | kind |
|---|---|---|
| A1 `no_current_task` | s10_01 0 (S, F) | verified |
| A2 entered | s10_01 25 (S, F) | verified |
| A3 replaced | s10_01 61 (S, F); at a boundary tick, s10_04 133 (S, F) | verified |
| A4 boundary (the recorded hypothesis still leads after the reset) | s10_11 53 (S, F), part (v) | verified (derivation A4) |
| A5 retraction | s10_03 55 (S, F) | verified |
| A6 `projection_expired` | s10_01 2 (S, F) | verified |
| A7 shared tick: `no_current_task` masks an expiry | s10_01 67 (S); s10_09 72 (F); six in all | verified |
| A8 shared tick: `recognition_changed` masks an expiry | s10_06 14, entered (S, F) | verified |
| A9 shared tick: `no_current_task` masks `recognition_changed` | none | not a distinct path (derivation A9) |

**A4, the boundary cause.** The chain asks replaced before boundary (C3), so the cause needs a boundary tick at which
the recorded hypothesis is still the leader after the reset to the prior (L5 B). At the reset every live hypothesis
holds 1/|H| and the leader is the first in the recognizer's order, which is by `repr` (`shared/recognizer.py`,
`self._hypotheses = sorted(hypotheses, key=repr)`): `coffee_break(...)` before every `deliver_item(...)`. Hence:
- the recorded hypothesis must not be pinned at the boundary (a pin removes it from the live set: replaced), so the
  terminal action is not its own: a misdelivery, or a return;
- it must still be recorded on the boundary tick, so adequate up to the place (not retracted before it);
- it must be the first live hypothesis in that order. With a coffee machine in the room `coffee_break` is live after
  every delivery boundary (L4) and wins the tie (scenario_s10_08 at 33 shows it), so the recorded hypothesis would
  have to be `coffee_break`, ended by another task's terminal action while it is recorded and adequate, which the
  one-level stack does not give without a retraction first.

Without a `coffee_break` hypothesis the path is open: a misdelivery of the tie-first item that stays adequate to its
place (a hand estimate, for item_1 from shelf_1 to kitting_table_3, 440 cm north of it: e ≈ 271 cm at the place, below 334 cm at α = 0.05; derived properly in part (v)). The
task model is the registry's default, not a run fact (`domains/kitting/registry.py`, `task_model`), so the hypothesis
is removed by the room: a layout without the coffee machine. Ruled (Hadi, 29 September 2026): claimed, one authored
instance on a new layout; the derivation stays in the authoring record.

**A9.** On a shared tick `no_current_task` masks `recognition_changed` (D3; C2). The decision asks admission once
either way (C5), so it differs only in the reported trigger ("only the reported reason and score differ", D3).
Reachable by timing alone; covered by A1 and A2.

## B. The gate at a trigger

| row | instance | kind |
|---|---|---|
| B1 below θ | s10_01 0 (S, F) | verified |
| B2 θ passed, no observation | s10_04 133 (S, F) | verified |
| B3 θ passed, adequacy failed | s10_09 60 (S, F); at `no_current_task`, s10_09 67 (S), s10_07 116 (F) | verified |
| B4 θ and adequacy passed, warrant failed | s10_05 127 (S, F) | verified |
| B5 clears by commitment only | s10_04 134 (S, F) | verified |
| B6 clears by observation only | s10_01 126 (S, F) | verified |
| B7 clears by both | s10_01 25 (S, F) | verified |
| B8 entered with a refusal | none | **unreachable** by construction |
| B9 `projection_expired` with the gate clearing | none | **unreachable** by construction |
| B10 retraction with the gate clearing | none | **unreachable** by construction |
| B11 replaced with the new leader admitted on the same tick | none | **unreachable** in scope (derivation B11) |

**B8 to B10.** C3: entered fires only when no record stands and the gate clears. C2 and C3: with a fallback recorded,
a clearing gate fires entered, which precedes the expiry on the tick, so the expiry never meets a clearing gate. C3:
retraction is asked only while the recorded hypothesis leads (replaced is asked first) and is inadequate, and the gate
asks the leader's adequacy (AD1), so it refuses. The gate's other refusals at these causes (a retraction below θ, a
replacement below θ) are the same path as B1 to B3.

**B11.** The new leader must clear θ on the tick it first leads. Between ticks the belief changes by one tick's
evidence per hypothesis (the likelihood L(v·D), E10), which cannot carry a rival from below the recorded hypothesis's
share to θ in one tick. A share jumps only by renormalisation when the live set changes: a re-entry takes exactly
1/|H| (L4, as amended), never the lead above θ; a pin removes a hypothesis, and a pin by the observed human's own
terminal action is a boundary tick, on which no hypothesis is a member (E8), so the gate refuses (no observation); a
pin without a boundary needs another agent to make a human hypothesis's terminal fact, which MPB-3's disjointness and
the prior exclude. Checked on the committed tables: no leader change onto a clearing gate on any of the 4285 ticks of
the IR test-bed's seventeen scenarios, nor on any tick of the eleven MPB scenarios.

## C. The projection the decision rests on

| row | instance | kind |
|---|---|---|
| C1 an admitted plan, a hold against the human's walk | s10_02 25, hold 5 (S, F) | verified |
| C2 an admitted plan, a hold against a standing segment (the human's `wait_at`, `place` or `pick_up` on a robot route) | s12_02 76, hold 18 against the admitted wait (S, F), part (v) | verified |
| C3 a moving fallback, not cut | s10_01 2 (S, F) | verified |
| C4 a moving fallback cut at an object | s10_09 60, kitting_table_2 (S, F); shelf_1 at 14 in several | verified |
| C5 a moving fallback cut at a landmark | s11_02 14, door_N (S, F); s10_01 157, corner_SE (S) | verified |
| C6 a moving fallback cut at the wall | none | **out of coverage** until TODO-142 is ruled |
| C7 a standing fallback | s11_01 0 (S, F) | verified |
| C8 none | none | **unreachable** in scope (track 4's) |

**C2.** scenario_s10_02's hold is against the human's carry through the crossing (the diagonal's midpoint between ticks
44 and 45, `authoring.md`); the human's stationary segments (the grasp at shelf_1, the place at kitting_table_0) lie
far from every robot route in the set, and no robot route in env_layout_12 passes the coffee machine. `realize()`
prices a stationary human segment as any segment (F1), so a robot route within `min_separation` of a human station
during the admitted plan's stationary segment reaches it. Ruled (Hadi, 29 September 2026): claimed; one authored
instance, the human's `wait_at` at the machine on a robot route.

**C6.** In the body a human's walk points at its target (Mesa moves straight toward it), so the ray along the last
displacement meets the target's arrival radius, or a nearer object's, before the wall. The wall ends the ray only when
the target is skipped: the start is inside its arrival radius, an arrival or pass-through tick, which is exactly the
skip rule's activation (TODO-142, class 3, open). Out of coverage until TODO-142 is ruled (Hadi, 29 September 2026).

**C8.** P1: no human observed, no fallback; P4: no previous observation, no projection. In scope one human is observed
on every tick (`docs/assumptions.md` 5.1, 5.2), and the run's first decision already has the observation of tick −1
(every tick-0 decision rests on a fallback). Reachable only once a human can leave observation: track 4
(TODO-140).

## D. The robot's state and the selection

| row | instance | kind |
|---|---|---|
| D1 idle: select, hold 0 | s10_01 0 (S, F) | verified |
| D2 idle: select, hold positive | s11_01 33, hold 23 (S, F) | verified |
| D3 walking to a shelf or carrying: continue, hold 0 | s10_01 25 (S, F) | verified |
| D4 walking to a shelf: continue, hold positive, against an admitted plan | s10_02 25, hold 5 (S, F) | verified |
| D5 walking to a shelf: continue, hold positive, against a fallback | s11_02 14, hold 2 (S) | verified |
| D6 a re-decision inside a running hold | s11_02 27 (S); where the hold drops to 0, s11_02 22 and 87 (S) | verified |
| D7 a switch while walking to a shelf, against a fallback | s11_01 14 (S, F) | verified |
| D8 a switch against an admitted projection (B3's realized-cost choice) | s12_01 26 (S), part (v) | verified |
| D9 a switch while carrying (`deliver_with_return`, X1's return walk) | s11_03 30 (S, F), part (v) | verified |

**D8.** The MPB's one switch (s11_01 at 14) is against a fallback stand. scenario_s10_02, the one decision whose hold
comes from an admitted plan, has a single candidate. With a second candidate whose realized cost falls below the held
one's, B3 selects it (the glossary's **realization**: conflict becomes cost). Ruled (Hadi, 29 September 2026):
claimed; a new setup on env_layout_12, the switch caused by the admitted projection.

**D9.** X1 names it: the occupied task's hold must exceed the cost difference, "the return walk included when the robot
carries the occupied task's item (`deliver_with_return`)". In s11_01 the switch fell before the grasp. Ruled: claimed;
a new scenario on env_setup_11, the stand beginning after the grasp.

A switch with a positive hold on the winner, and a switch at a retraction, decide by the same rule as D7 and D8 and are
covered by type.

## E. The negative rows

| row | instance | kind |
|---|---|---|
| E1 a trigger with no admission | s10_01 0 (S, F) | verified |
| E2 θ passed and adequacy failed | B3 | verified |
| E3 θ and adequacy passed and warrant failed | B4 | verified |
| E4 a projection change with no change of choice | entered, s10_01 25; retraction, s10_03 55 (S, F) | verified |
| E5 no decision opportunity: a fallback outliving its evidence | s11_02 55 → 87, the stand broken at 57 (S) | verified |
| E6 no decision opportunity: a record kept through a dip below θ (D2's retention by identity) | s10_10 34 to 36, the record kept from 25 to 36 (S, F), part (v) | verified |
| E7 no decision opportunity: the loss of observation warrant (AD3) | none | **out of coverage** |
| E8 no decision opportunity: an admitted projection past its T_h (P3) | none | reachable, not claimed |
| E9 no decision opportunity: a change after the terminal decision | none | **out of coverage** |
| E10 a decision inside the observation-offset gap against a fallback stand (TODO-134) | none | **out of coverage** |
| E11 X5's ground (1): unexplained, outliving a re-decision | s10_09 60 to 72; refused re-decisions 60, 67, 72 (S), 60, 72 (F) | verified |
| E12 X5's ground (2): every candidate holds, at a decision and at the next | s11_02 25, 27, 31, 39, 55 (S) | verified |

**E6.** D2: "a recorded hypothesis that dips below θ while staying most likely fires nothing, and keeps its projection
until it is replaced, ends, or the human stops". Reachable after an admission where the human's walk raises a rival for
some ticks without turning the recorded hypothesis inadequate and without the rival taking the lead. Ruled: claimed; a
new scenario on env_setup_10, with no inadequacy and no other trigger in the dip.

**E7.** AD3, NOT EXERCISABLE IN THE MPB SET (Hadi, 29 September 2026): loss of observation warrant while still
adequate requires an admission after less than about 167 cm of gain, which occurs only for a lone hypothesis admitted
at once, followed by a turn back; the instance belongs to the evaluation's authored deviations. Kept apart from A4:
both have no instance, but A4 is claimed and reachable under a changed hypothesis space, and E7 is not exercisable here.

**E8, P3.** Reachable: an admitted plan always ends at the task's terminal action, and a human delayed in a phase but
still adequate (a stand under the inadequacy delay, about 17 standing ticks at α = 0.05, v = 20 cm/tick) reaches it
after T_h, so the robot runs past T_h with the record standing until the boundary. Not claimed: P3 is parked ("T-D
P", P3). The class-3 reading of P3's bound is recorded there (Hadi, 29 September 2026).

**E9.** After the terminal decision nothing is planned (C6; "The cognitive loop does not end with the task pool").

**E10.** TODO-134 is parked, to be ruled only on an instance in scope; no MPB decision fell in the gap (REPORT.md).

**E12, new at this step.** In scenario_s11_02 (single_task, two candidates) every candidate's realized plan holds at
the expiries of 25, 27, 31, 39 and 55: X5's ground (2) holds at a decision and at the next re-decision from 25 on,
until the decision of 87 (hold 0). Read from `selection.json` (`[meta-cand] delta=`); under full_reorder the robot is
elsewhere during the stand, and full_reorder logs no per-candidate hold (TODO-141).

## Counts

| kind | rows |
|---|---|
| verified | 36 (A1 to A8; B1 to B7; C1 to C5, C7; D1 to D9; E1 to E6, E11, E12) |
| unreachable, with a derivation | 5 (B8 to B11; C8) |
| out of coverage, with a reason | 4 (C6; E7, E9, E10) |
| reachable, claimed, no instance | 0 (A4, C2, D8, D9, E6 verified in part (v); 5 before it) |
| reachable, not claimed | 1 (E8, P3) |
| not a distinct path | 1 (A9) |

E2 and E3 repeat B3 and B4 as negative rows and are counted once, as verified.

## The reachable cells the contribution claims, and their remedies under MPB-2

VERIFIED IN PART (v) (30 September 2026; REPORT.md, "Part (v)"; authoring.md, part (v)), with the remedies as built:
D8 on env_layout_14 and env_setup_12 (the ruled "new setup on env_layout_12" was not expressible, derivation in
authoring.md; Hadi ruled the layout); C2 on the same (a new layout, as the ruling allowed); D9 on env_setup_11 with the
stand from tick 0 and the robot grasping before the decisive expiry (the variable is the carrying state); E6 on
env_setup_10 with scenario_s09_04's script (the planned drop-cut detour is not expandable by the oracle's trajectory);
A4 on env_layout_13 with env_setup_10.

Ruled by Hadi, 29 September 2026, in this order; each gets one authored instance in part (v):
1. **D8, the switch against an admitted projection:** a new setup on env_layout_12 (item_7's crossing task plus an
   alternative whose cost difference lies below the hold), the switch caused by the admitted projection, not by a
   fallback or a robot-state effect.
2. **C2, the hold against an admitted standing segment:** the human's `wait_at` at the machine on a robot route; a new
   scenario on env_setup_10 whose robot start puts a walk past the waiting point; a new layout only if the geometry
   cannot express it cleanly, never a tuned one.
3. **D9, the switch while carrying:** a new scenario on env_setup_11, the stand beginning after the grasp, X1's
   condition with the return walk.
4. **E6, a record kept through a dip below θ:** a new scenario on env_setup_10, the dip shown without inadequacy or
   another trigger in the same interval.
5. **A4, the cause boundary:** a new layout without the coffee machine, because the mechanism requires the absence of
   the `coffee_break` hypothesis (the tie order at a reset), not because the room is inconvenient.

MPB-2's rule as amended applies to each (a placement or setup change only if it alters no verified scenario on that
setup: the output floor couples every scenario on a setup).

## Closure

The MPB closes when every materially distinct in-scope decision path is verified, unreachable with a recorded
derivation, or outside the claimed mechanism with a recorded reason: here, when A4, C2, D8, D9 and E6 are verified.
CLOSED (part (v), 30 September 2026; provisional until Hadi reads the check of scenario_s12_01's three F1 violations,
REPORT.md, part (v)): all five are verified (zero disagreements on parts 1 to 3 under both strategies,
prior on; every declared part-4 property under single_task). Every row is now verified (36), unreachable with a
derivation (5), out of coverage with a reason (4), reachable and not claimed (1, P3) or not a distinct path (1).
