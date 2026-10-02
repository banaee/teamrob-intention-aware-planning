# Record of planning and building: Phase 4 (4A to 4C: the I-series, the T-series, F1, C, D2, D3)

Moved verbatim from `docs/design_decisions.md` on 2 October 2026 (Hadi's ruling of that day: one record file per task;
the conceptual design stays in design_decisions.md). Each block is headed by the title of the entry it comes from
and its id; in design_decisions.md an index line with the same id stands where the block was.

**One leg is one observation — replace, do not multiply** — RECORD [phase4/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
Crossings after the change (PYTHONHASHSEED=0; runs 20260910_1552xx — superseded as regression
baselines by runs 20260911_0826xx after T2 rescaled projection time to execution ticks; the
`theta_crossed` steps below are unchanged in those runs, the built/selected columns are not —
see TODO-28 and TODO-30). `theta_crossed` = crossing events; "built" = admitted projections:

| run      | first ≥ θ            | theta_crossed | built projections  | note |
|----------|----------------------|---------------|--------------------|------|
| s20 off  | 22 (0.797), grasp    | 22, 89        | 22, 24, 89, 96     | late-reveal condition |
| s20 on   | **11 (0.780)**       | 11, 82        | 11, 23, 82, 95     | PRE-GRASP: human crosses x=0 into zone_SW at 11 (13.99 → −2.92) and ZONE_BOOST doubles item_3 (0.641 → 0.780); robot at (−393, 85), its move_to to shelf_4 completes at 21 — roughly half the approach; projection built, item_4 min_dist 14.98 at cost 812. This is the fixture condition B2 needs. It is a zone-state reveal on top of one honest chord (0.641), not an accumulation. |
| s00 off  | 41 (0.797), grasp    | 41, 111       | 41, 63, 111, 131   | |
| s00 on   | 41 (0.797), grasp    | 41, 81        | 41, 63, 81, 95, 131| leg-2 first chord 0.856 (carry-leg chord had already favoured shelf_2, 49° off, L 3.4) |
| s10 off  | 257 (0.769), grasp of item_4 | 257   | 257, 262           | grasp of item_2 at 31 gives 0.662: item_2 : coffee : unknown = 4 : 1 : 1 — coffee has no item binding and survives the pin |
| s10 on   | **107 (0.853) on item_6 — wrong** | 107, 257 | 107, 142, 200, 257, 262 | coffee-leg criterion FAILED, known consequence of TODO-46: `coffee_break` gets no chord evidence, so the walk to the coffee machine is credited to shelf_6 (27° off) and doubled on zone_SW entry |

Every belief change in all six runs is attributable to a leg start, a discrete event, a
quadrant crossing, or a world change (a robot-carried item's expected position moving with
the robot — switch-off only, since those hypotheses are inadmissible switch-on). No
per-step accumulation remains; within-leg values are flat to the third decimal.

**Projection time includes what the body spends finishing an action, and the human's projection starts when it was observed (L2)** — RECORD [phase4/2], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
MEASURED (L2, `analysis/l2_execution_lag/REPORT.md` (deleted in the analysis cleanup, September 2026; carried in the L2 entry of design_decisions.md and TODO-77), TODO-77's own terms). The systematic whole-tick lag
is gone: medians move from −1.46/−3.32 to −0.46/−0.32 for the robot (2- and 4-action plans) and from
−2.21/−5.32 to −0.21/−1.32 for the human. What remains is exactly the two things above: a discrete-step
forward model of the executor, using no execution data, predicts the actual release tick EXACTLY for all
68 human and robot 2-action rows, and exactly one tick early for all 35 robot 4-action rows. That last
+1 is not quantisation and is not compensated either: the robot re-plans at its own `task_committed`
trigger, which fires on the tick that would have acknowledged the `pick_up`; the fresh
`deliver_already_held` plan does not contain that `pick_up`, so `continue_plan()` loads from the start
and the carry begins on that very tick. One of the four charged latencies is never spent. Modelling it
would mean the projection predicting the robot's own future triggers, which are decided FROM the
projection — recorded in TODO-77, not fixed.

CONSEQUENCE, and a correction to the expectation this task was set with. "B3 is plain-cost argmin, so
any change comes from durations" is not what the code does: B3 is an argmin over candidates that
`_detect_interference()` has not excluded, and that filter is still live. Across the ten sweep
conditions the latency changed every cost (by one tick per action) and reordered NO candidate set at any
of the 93 triggers compared. The single decision change in the sweep comes from the offset instead:
with the two agents finally in phase, scenario_30's mirror crossing is projected as the near-coincidence
it is (`min_dist` 15.37 → 0.49 cm, the continuous-time minimum of two agents passing through each other
— `[sep]`'s 11.0 cm was the closest integer-tick sample), and the superseded `min_safe_distance = 1.0`
excludes the candidate. Ablation confirms it: latency alone changes no decision, offset alone produces
the whole change. That threshold is already superseded (R1; removed in T10), so the exclusion is a
vestigial mechanism firing on a newly-accurate number, not a new policy.

**B3 selects on realized cost: the argmin of T_r + δ over the realizable candidates, the winner's hold executed, plain cost when nothing realizes (T10)** — RECORD [phase4/3], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
MEASURED (T10; `analysis/t10_b3_realized/comparison.md` (deleted in the analysis cleanup, September 2026; carried in the T10 entry of design_decisions.md, TODO-36 and TODO-79); s00/s10/s20/s30 × prior off/on, run to
completion, PYTHONHASHSEED=0; `plain`+`none`, `realized`+`none`, `realized`+`b2a` with ρ = 0.5):
- PLAIN against L2: identical in every condition but s30_on, where at step 21 the superseded
  `min_safe_distance` exclusion no longer fires and item_4 stays selected (the L2 report predicted
  this). Plain is therefore the old B3 minus the vestigial filter, on the fractional T_r.
- REALIZED against PLAIN — realization's effect. s00 (both priors): identical; every δ is 0. s10, s20,
  s30: the same TASK ORDER except s20_on (below), reached later: the holds B2 executed under T4's
  `b2a` are now B3's, at the same triggers with the same δ (s10 29/33/35 → 6, 2, 0; s20_off 20/24/30
  → 7, 3, 1; s20_on 6/30 → 7, 1; s30_off 28/46 → 6, 1), plus s30_on 40/77 → 7, 1, which T4 did not
  have because its old B3 had switched to item_2 at 21. 12 holds, 43 ticks held, 2 interrupted
  (s10_off 29→33 and s20_off 20→24, the remainder re-decided as at T4). Completion slips by the held
  ticks: s10 +6, s20_off +8, s30 +7/+8. ONE all-unrealizable event, s30_on 21 (the mirror crossing,
  both candidates `hold_position_violated`): the fallback keeps item_4 on plain cost, which is what
  plain does too; its residual conflict is the 0.00 cm pass-through at tick 23, inside that window.
- REALIZED, `none` against `b2a`: IDENTICAL decision sequences, greps and holds in all eight
  conditions. B2 continued exactly where B3 keeps the current task, and both escalations reach a B3
  that decides as it would have without the gate. On these fixtures at ρ = 0.5 `b2a` is a computation
  saving (one realization per trigger instead of one per candidate) and nothing else (TODO-36).
- s40 (regression sweep only, `realized`+`none`): byte-identical to L2 on every grep — no δ > 0.
- ACTUAL SEPARATION (TODO-79, `dist` and the continuous `min`): every moment below 50 cm is past T_h,
  under no projection, after the robot finished, or inside the s30_on fallback's window, EXCEPT s10
  tick 75 at 49.15 cm (both priors, both realized configurations) — TODO-77's step-quantisation
  residual, inside the step-35 decision's window by 0.29 tick. The continuous minimum lowers the
  crossing minima (s30 tick 23: 11.03 → 0.00; s20_off crossing: 11.64 at tick 51 → 9.02 over tick 52) and extends episodes by
  one tick; it moves nothing from outside to inside.

FINDING (RESOLVED by F1, "Robot-responsible separation", which redefined the violation; the mechanism
below is corrected there: it was the robot's stationary placement, not its walk, that the joint-state
rule counted), recorded at T10: s20_on, step 57 (`theta_crossed`, the human's next
task admitted). The robot is carrying item_4, 3.95 projected ticks from placing it. The human has just
placed at the table and is walking away, and at the trigger stands 37.5 cm from the robot — already
inside `min_separation`. item_4's plan converges on the departing human at δ = 0 and its hold position
is violated at step 1, so it is UNREALIZABLE; item_6's plan (return item_4 to its shelf first, then
fetch item_6 — six actions) walks away from the human and realizes at δ = 0, cost 84.65. B3 selects
item_6. Under plain the robot had delivered item_4 at 54 (no holds earlier); under realized the
step-6 and step-30 holds placed the robot's arrival exactly where the human departs. Consequence:
completion 292 vs 228 ticks (+64), item_4 delivered third instead of first, and the human passed the
robot anyway (56–57: 35.1 cm, past T_h). RESOLVED (F1, next entry but one: the flag and the
hold-position check are gone; item_4 wins at 57 with δ = 2). Mechanism as it was: realizability is a HARD GATE inside B3 whenever
some candidate realizes — the argmin ranges over realizable candidates only, so an unrealizable
candidate cannot win however short its plan — and `hold_position_violated` fires here not on a
projected conflict but on the PRESENT state (the human already within `min_separation` of where the
robot stands), which no hold can change and which afflicts every candidate whose first step converges.
This is the over-reaction the wait revision set out to remove, returning through the realizability
flag: switching cost 64 ticks to avoid a 4-tick completion whose "conflict" was the human leaving.
The design as decided says this is what B3 does (the all-unrealizable fallback covers only the case
where NOTHING realizes), so it was built as decided and is reported here. Where it belongs: T6 (the
ablation will show it as the largest realized-vs-plain difference) and D2 / the R1 follow-up — whether
an unrealizable current task a few ticks from completion should compete on plain cost, whether a
present-state violation is a realization question at all, or whether this is `min_separation`'s value
(TODO-28) at the table. Nothing here was tuned.

**What a trigger is an event of: `recognition_changed` against the decision record replaces `theta_crossed`; the blocked event designed, not built (D2)** — RECORD [phase4/4], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
MEASURED (PYTHONHASHSEED=0; the sweep and the evaluation fixtures, prior off / on; baselines at the
pre-D2 HEAD agree byte-for-byte with F1's and F47b's on the decision grep):
- Fires of the replaced trigger, old `theta_crossed` → new `recognition_changed`: s00 5→4 / 2→4, s10 6→7 /
  4→7, s20 7→4 / 2→4, s30 2→4 / 2→4, s40 5→10 / 5→10, s50 8→6 / 3→6, s70 5→6 / 3→6, s71 5→7 / 3→6. The new
  count is two per human task everywhere (a recognition, then its end) except s71_off, where item_5 enters
  twice (61 and 72): the robot's own `task_committed` at 69 fell inside item_5's dip (0.572), its admission
  refused, the record was cleared, and item_5's next clearing of the gate is a new recognition. A property
  of the rule, stated here: the record is what the LAST decision projected, whichever trigger made it, so
  the guarantee is "no fire while a projection stands", not one fire per hypothesis. Every fire that retracts — admission `none(below_theta)` or
  `none(unknown)` — decided a CONTINUE in all 16 conditions.
- PRIOR-ON: decisions identical modulo the reason string and the added retraction continues in s00, s10,
  s20, s30, s40, s50, s70 (completion 168 / 420 / 239 / 162 / 378 / 237 / 187, unchanged; `[sep]`
  byte-identical). s71_on: the retraction at the human's boundary, step 54, replaces the last tick of the
  32-tick hold placed against the coffee stay that ended on that tick (executed 31, interrupted); the
  robot leaves one tick earlier, completion 204 → 203. Expected under T4's rule that a later decision
  replaces the hold in progress.
- PRIOR-OFF: the repeated crossings no longer decide (s00 113 / 115, s10 33 / 35, s20 and s50 24 / 30 /
  91 / 95, s70 and s71 65); s20 and s50's first hold runs its 8 ticks in one piece instead of 4 + 4
  (interrupted and re-realized at 24). Robot motion identical in s00, s10, s20, s30, s40, s50, s70
  (`[sep]` byte-identical). Completion DECLARED two ticks later in s00, s20, s50 (166 → 168, 235 → 237,
  235 → 237): the old `theta_crossed` on `unknown` at the robot's own last delivery (TODO-54) declared the
  empty pool on that tick; nothing enters on `unknown` now, so `no_current_task` declares it when the
  executor's bookkeeping learns of the completion, two ticks later. The run's behaviour is the same;
  two trailing `[IR]` lines are the only other difference. s71_off: the boundary retraction at 54
  interrupts the hold's last tick as prior-on, the switch to item_3 comes at 108 instead of 111,
  completion 204 → 201.
These are the meta-planner-side regression baselines from here on: `analysis/d2_recognition_trigger/`
(`sweep/` for s00–s40, `fixtures/` for s50 / s70 / s71; logs local, README committed).
