# Context knowledge on against off: an overview of T-K part 1's kitting runs (steps 4, 5 and 5b)

A reading of existing outputs only (4 October 2026): no run was made for it. `comparison.py` in this folder writes
every table below "The full tables" from the outputs of `analysis/kitting/irb/tk1/`, `tk2/` and `tk5b/` and
`analysis/kitting/mpb/` (the reference), `mpb/tk/` and `mpb/tk5b/`.

**The scenarios are authored.** Each was written to place a case. The counts compare the two settings on the same
scripts. They are no rate of occurrence. No design conclusion is drawn here.

The settings: off (context knowledge off, the equal prior); on with no raising fact; on with the raising fact
(break_time, room_warm). Each comparison is within one script: the on run against the off run of the same script.
Recognition: 74 pairs (57 of step 4, 17 of step 5b), the robot idle. Planning: 22 on runs (6 of step 5, 16 of step 5b)
against their off runs (3 and 16), single_task.

## C. The summary

| measure | off | on |
|---|---|---|
| admissions of the true task (325 true stretches): earlier / equal / later than off | - | 206 / 48 / 42; admitted on only 10, neither 19 |
| ticks gained / lost in those admissions | - | 3005 earlier, 365 later |
| of which assigned deliveries (266 stretches) | - | 193 earlier (2824 ticks), 44 equal, 18 later (47 ticks); median −8 with no raising fact, +1 with one |
| of which coffee_break (39 stretches) | - | raised: 11 of 11 earlier (median −14); ordinary: 24 of 28 later (median +13.5) |
| admissions of a hypothesis that is not the true task, during modelled tasks: count; gate ticks; trigger-rule ticks | 17; 114; 146 | 47; 504; 613 |
| of those on, by the evidence alone (the off run): (i) a near-tie; (ii) the true task first, the prior overruling; (iii) the evidence itself ranking the admitted one first; no true hypothesis | - | rows 0 / 17 / 26 / 4; gate ticks 0 / 310 / 149 / 45; single ticks (i) 18, (ii) 293, (iii) 141 |
| the same on the exit walk: count; gate ticks | 52; 1089 (per pair) | 51; 1166 |
| one-tick admissions of the next delivery on the previous task's pin tick | 6 (per pair) | 58 |
| a lone assigned task admitted before the human starts it, retracted: count; ticks (median, range) | 1; 7 | 9; 247 (22, 8 to 60) |
| planning, completion against off (22 runs) | - | better 7, equal 13, worse 2 |
| planning, completion ticks gained / lost | - | 134 gained (78 of them s11_03), 3 lost |
| planning, cases below min_separation | 2 (s16_01, s12_02) | 5 (s16_01, s16_02, s16_05, s11_03, s12_02) |
| their ticks: standing robot / moving robot (F1 viol / recede) | 8 / 3 (2 / 1) | 7 / 18 (10 / 8) |
| by cause: a wrong admission | 0 | 2 (s16_05 28.3 cm; s11_03 11.3 cm) |
| by cause: the gap between plan and execution at a turn (TODO-146) | 0 | 2 (s16_01 41.7 cm; s16_02 29.3 cm) |
| by cause: other | 2 (s16_01 37.0 cm, no projection past the arrival; s12_02 32.3 cm, the human walking past the robot standing in its hold) | 1 (s12_02 33.6 cm, the same) |

Notes on the measures:
- A1's category is the state on the true stretch's first tick, on (KT14). An A/C activation is never admitted on
  either side in 18 of its 20 stretches; its measure in step 4 is its belief at arrival (KT10), not given here.
- A2's kinds are read per wrong tick from the off run of the same script (the equal prior's belief is the evidence
  alone): the ratio of the true task's belief to the admitted one's. (i) within [1/1.01, 1.01]; (ii) above 1.01 with the
  true task first; (iii) below 1/1.01. A row takes the kind of most of its ticks. 1.01 is a reporting threshold, not a
  design value; every row's first and last ratio is in the table. Kind (iii) is not one of the two kinds asked for. It
  is reported because 26 rows fit neither: the evidence alone ranks the admitted hypothesis higher, as at the start of
  an interrupted delivery, and the off run mostly makes the same admission there.
- "Per pair": in step 4 one off run is the off side of several timelines. During modelled tasks the off count is the
  same per pair and per script (17); on the exit walk it is 52 per pair and 38 per script.
- B's "response decision" is the robot's first decision with a positive hold or a switch.

## The full tables

### A. Recognition (57 pairs of step 4, 17 of step 5b)

#### A1. Admissions of the true task, on against off

| category (the state on the stretch's first tick, on) | stretches | earlier | equal | later | difference on − off (ticks, both admitted) | ticks earlier, total | ticks later, total | admitted on only | off only | neither |
|---|---|---|---|---|---|---|---|---|---|---|
| assigned delivery, no raising fact | 238 | 182 | 43 | 2 | median -8, range -51 to 1 | 2641 | 2 | 10 | 0 | 1 |
| assigned delivery, a raising fact holding | 28 | 11 | 1 | 16 | median 1, range -37 to 5 | 183 | 45 | 0 | 0 | 0 |
| coffee_break, its raising fact holding | 11 | 11 | 0 | 0 | median -14, range -25 to -6 | 156 | 0 | 0 | 0 | 0 |
| coffee_break, no raising fact (ordinary) | 28 | 2 | 2 | 24 | median 13.5, range -14 to 22 | 25 | 318 | 0 | 0 | 0 |
| ac_activation, its raising fact holding | 8 | 0 | 0 | 0 | - | 0 | 0 | 0 | 0 | 8 |
| ac_activation, no raising fact (ordinary) | 12 | 0 | 2 | 0 | median 0, range 0 to 0 | 0 | 0 | 0 | 0 | 10 |

#### A2. Admissions of a hypothesis that is not the true task

During modelled tasks (the exit walk and the one-tick rows on a completion left out):

| side | count | gate: median | max | total ticks | trigger rule: median | max | total ticks |
|---|---|---|---|---|---|---|---|
| off (per pair) | 17 | 8 | 17 | 114 | 8 | 17 | 146 |
| off (each script once) | 17 | 8 | 17 | 114 | 8 | 17 | 146 |
| on | 47 | 8 | 60 | 504 | 9 | 60 | 613 |
| on, no raising fact | 41 | 8 | 60 | 448 | 9 | 60 | 539 |
| on, a raising fact holding | 6 | 9.5 | 11 | 56 | 12.5 | 17 | 74 |

The exit walk:

| side | count | gate: median | max | total ticks | trigger rule: median | max | total ticks |
|---|---|---|---|---|---|---|---|
| off (per pair) | 52 | 22 | 32 | 1089 | 22 | 32 | 1089 |
| off (each script once) | 38 | 22 | 32 | 851 | 22 | 32 | 851 |
| on | 51 | 22 | 32 | 1166 | 22 | 32 | 1166 |

The one-tick rows on a completion (the next delivery admitted on the previous task's pin tick; not wrong from the next tick):

| side | count | gate: median | max | total ticks | trigger rule: median | max | total ticks |
|---|---|---|---|---|---|---|---|
| off (per pair) | 6 | 1 | 1 | 6 | 1 | 1 | 6 |
| off (each script once) | 5 | 1 | 1 | 5 | 1 | 1 | 5 |
| on | 58 | 1 | 1 | 58 | 1 | 1 | 58 |

#### A2, the kinds: what the evidence alone said (the off run)

| step | scenario | admitted (on) | wrong ticks (gate) | true task | off ratio true / admitted: first wrong tick, last | ticks (i) / (ii) / (iii) | kind |
|---|---|---|---|---|---|---|---|
| step 4 | s13_03 | item_4 | 150-161 (12) | coffee_break | ×1.8963, ×5.5787 | 0 / 12 / 0 | (ii) |
| step 4 | s13_05 | item_2 | 94-94 (1) | coffee_break | ×0.4781, ×0.4781 | 0 / 0 / 1 | (iii) |
| step 4 | s13_05 | item_2 | 96-99 (4) | coffee_break | ×0.5894, ×1.3849 | 1 / 1 / 2 | (iii) |
| step 4 | s13_06 | item_2 | 96-103 (8) | coffee_break | ×0.4163, ×2.9061 | 0 / 4 / 4 | (ii) |
| step 4 | s13_07 | item_2 | 123-130 (8) | coffee_break | ×0.0000, ×0.0005 | 0 / 0 / 8 | (iii) |
| step 4 | s13_11 | coffee_break | 81-91 (11) | item_2 | ×1.2248, ×1.7103 | 0 / 11 / 0 | (ii) |
| step 4 | s13_12 | coffee_break | 81-91 (11) | item_2 | ×1.2248, ×1.7103 | 0 / 11 / 0 | (ii) |
| step 4 | s13_12 | item_4 | 150-161 (12) | coffee_break | ×1.8963, ×5.5787 | 0 / 12 / 0 | (ii) |
| step 4 | s13_13 | item_4 | 216-258 (43) | coffee_break | ×1.0092, ×12.7307 | 1 / 41 / 0 | (ii) |
| step 4 | s13_14 | coffee_break | 81-91 (11) | item_2 | ×1.2248, ×1.7103 | 0 / 11 / 0 | (ii) |
| step 4 | s13_15 | item_4 | 262-269 (8) | coffee_break | ×0.0465, ×0.4469 | 0 / 0 / 8 | (iii) |
| step 4 | s14_04 | item_2 | 133-133 (1) | coffee_break | ×0.3814, ×0.3814 | 0 / 0 / 1 | (iii) |
| step 4 | s14_04 | item_2 | 135-136 (2) | coffee_break | ×0.4665, ×0.5958 | 0 / 0 / 2 | (iii) |
| step 4 | s14_05 | item_2 | 135-146 (12) | coffee_break | ×0.3144, ×3.5912 | 0 / 5 / 6 / (iv) 1 | (iii) |
| step 4 | s14_06 | item_2 | 180-187 (8) | coffee_break | ×0.0000, ×0.0000 | 0 / 0 / 8 | (iii) |
| step 4 | s14_09 | item_2 | 133-133 (1) | ac_activation | ×0.6780, ×0.6780 | 0 / 0 / 1 | (iii) |
| step 4 | s14_09 | item_2 | 135-136 (2) | ac_activation | ×0.8283, ×1.0580 | 0 / 1 / 1 | (ii) |
| step 4 | s14_10 | item_2 | 135-140 (6) | ac_activation | ×0.6078, ×1.8381 | 0 / 3 / 3 | (ii) |
| step 4 | s14_11 | item_2 | 180-187 (8) | ac_activation | ×0.0000, ×0.0000 | 0 / 0 / 8 | (iii) |
| step 4 | s14_19 | item_1 | 180-239 (60) | coffee_break | ×1.0008, ×13.7117 | 10 / 49 / 0 | (ii) |
| step 4 | s14_21 | coffee_break | 221-227 (7) | ac_activation | ×1.1772, ×1.7775 | 0 / 7 / 0 | (ii) |
| step 4 | s15_03 | item_4 | 151-161 (11) | coffee_break | ×2.0139, ×5.5787 | 0 / 11 / 0 | (ii) |
| step 4 | s15_05 | item_2 | 94-94 (1) | coffee_break | ×0.4781, ×0.4781 | 0 / 0 / 1 | (iii) |
| step 4 | s15_05 | item_2 | 96-99 (4) | coffee_break | ×0.5894, ×1.3849 | 1 / 1 / 2 | (iii) |
| step 4 | s15_06 | item_2 | 96-103 (8) | coffee_break | ×0.4163, ×2.9061 | 0 / 4 / 4 | (ii) |
| step 4 | s15_07 | item_2 | 123-130 (8) | coffee_break | ×0.0000, ×0.0005 | 0 / 0 / 8 | (iii) |
| step 4 | s15_11 | item_2 | 94-94 (1) | ac_activation | ×0.0380, ×0.0380 | 0 / 0 / 1 | (iii) |
| step 4 | s15_11 | item_2 | 96-98 (3) | ac_activation | ×0.0469, ×0.0802 | 0 / 0 / 3 | (iii) |
| step 4 | s15_11 | item_4 | 111-118 (8) | ac_activation | ×0.4853, ×0.5553 | 0 / 0 / 8 | (iii) |
| step 4 | s15_12 | item_2 | 96-108 (13) | ac_activation | ×0.0285, ×0.3376 | 0 / 0 / 13 | (iii) |
| step 4 | s15_13 | item_2 | 123-130 (8) | ac_activation | ×0.0000, ×0.0004 | 0 / 0 / 8 | (iii) |
| step 4 | s15_19 | item_4 | 216-261 (46) | ac_activation | ×1.0015, ×3.0458 | 5 / 40 / 0 | (ii) |
| step 5b | s08_02 | item_2 | 62-83 (22) | coffee_break | ×1.0482, ×13.5576 | 0 / 21 / 0 | (ii) |
| step 5b | s08_03 | item_1 | 32-42 (11) | coffee_break | ×0.1521, ×1.6265 | 0 / 2 / 9 | (iii) |
| step 5b | s08_04 | item_1 | 30-30 (1) | coffee_break | ×0.1914, ×0.1914 | 0 / 0 / 1 | (iii) |
| step 5b | s08_04 | item_1 | 32-39 (8) | coffee_break | ×0.2338, ×2.2619 | 0 / 3 / 5 | (iii) |
| step 5b | s09_02 | item_2 | 62-83 (22) | coffee_break | ×1.0482, ×13.5576 | 0 / 21 / 0 | (ii) |
| step 5b | s09_03 | item_1 | 32-42 (11) | coffee_break | ×0.1521, ×1.6265 | 0 / 2 / 9 | (iii) |
| step 5b | s09_04 | item_1 | 30-30 (1) | coffee_break | ×0.1914, ×0.1914 | 0 / 0 / 1 | (iii) |
| step 5b | s09_04 | item_1 | 32-39 (8) | coffee_break | ×0.2338, ×2.2619 | 0 / 3 / 5 | (iii) |
| step 5b | s09_05 | item_1 | 32-47 (16) | unmodelled | - | - | none (the true task is no hypothesis) |
| step 5b | s09_06 | item_1 | 30-46 (17) | unmodelled | - | - | none (the true task is no hypothesis) |
| step 5b | s09_07 | item_1 | 32-32 (1) | item_2 | ×0.0005, ×0.0005 | 0 / 0 / 1 | (iii) |
| step 5b | s09_09 | item_2 | 62-72 (11) | item_1, item_3 | - | - | none (the true task is no hypothesis) |
| step 5b | s09_09 | item_2 | 108-108 (1) | item_3 | - | - | none (the true task is no hypothesis) |
| step 5b | s09_11 | item_3 | 62-79 (18) | coffee_break | ×1.0625, ×14.2002 | 0 / 17 / 0 | (ii) |
| step 5b | s09_13 | item_1 | 46-54 (9) | coffee_break | ×0.0025, ×0.0272 | 0 / 0 / 9 | (iii) |

Rows: (i) 0, (ii) 17, (iii) 26, no kind 4. Ticks: (i) 18, (ii) 293, (iii) 141, (iv) 1. Gate ticks per kind of row: (i) 0, (ii) 310, (iii) 149, none 45.

#### A3. A lone assigned task admitted before the human starts it

| side | ends | count | ticks until it ends: median | range | total | where (scenario: first tick, ticks) |
|---|---|---|---|---|---|---|
| off (each script once) | started on the next tick (1 tick) | 5 | 1 | 1 to 1 | 5 | 5 runs |
| off (each script once) | retracted | 1 | 7 | 7 to 7 | 7 | s13_15: 262, 7 |
| on (per run) | started on the next tick (1 tick) | 59 | 1 | 1 to 1 | 59 | 59 runs |
| on (per run) | retracted | 9 | 22 | 8 to 60 | 247 | s13_13: 216, 43; s13_15: 262, 8; s14_19: 180, 60; s15_19: 216, 46; s08_02: 62, 22; s09_02: 62, 22; s09_08: 132, 17; s09_09: 62, 11; s09_11: 62, 18 |

### B. Planning (6 on runs of step 5, 16 of step 5b)

#### B1 and B2. Completion, the response decision, the separation

| step | scenario | side | completion | Δ to off | response decision (tick: what) | Δ to off | min separation (tick) | ticks below: standing robot | moving robot (F1 viol / recede) | cases below (first-last: min) |
|---|---|---|---|---|---|---|---|---|---|---|
| step 5 | scenario_s16_01 | off | 69 | - | 45: hold 2 | - | 37.0 (48) | 6 | 1 (1 / 0) | 44-50: 37.0 |
| step 5 | scenario_s16_01 | on | 68 | -1 | 0: hold 5 | -45 | 41.7 (50) | 0 | 3 (2 / 1) | 49-51: 41.7 |
| step 5 | scenario_s16_02 | on | 67 | -2 | 38: hold 4 | -7 | 29.3 (49) | 0 | 3 (2 / 1) | 48-50: 29.3 |
| step 5 | scenario_s16_03 | off | 113 | - | 36: hold 31 | - | 59.5 (27) | 0 | 0 (0 / 0) | none |
| step 5 | scenario_s16_03 | on | 89 | -24 | 43: hold 3 | +7 | 55.5 (42) | 0 | 0 (0 / 0) | none |
| step 5 | scenario_s16_04 | on | 90 | -23 | 22: hold 32 | -14 | 68.5 (26) | 0 | 0 (0 / 0) | none |
| step 5 | scenario_s16_05 | off | 106 | - | 14: hold 5 | - | 60.4 (27) | 0 | 0 (0 / 0) | none |
| step 5 | scenario_s16_05 | on | 101 | -5 | -: none | - | 28.3 (25) | 0 | 6 (4 / 2) | 22-27: 28.3 |
| step 5 | scenario_s16_06 | on | 106 | +0 | 14: hold 5 | +0 | 60.4 (27) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_01 | off | 161 | - | -: none | - | 384.0 (59) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_01 | on | 161 | +0 | -: none | - | 384.0 (59) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_02 | off | 66 | - | 25: hold 5 | - | 52.2 (47) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_02 | on | 66 | +0 | 8: hold 5 | -17 | 52.2 (47) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_03 | off | 172 | - | -: none | - | 408.9 (155) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_03 | on | 172 | +0 | -: none | - | 408.9 (155) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_04 | off | 161 | - | -: none | - | 384.0 (59) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_04 | on | 161 | +0 | -: none | - | 384.0 (59) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_05 | off | 161 | - | -: none | - | 384.0 (59) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_05 | on | 161 | +0 | -: none | - | 384.0 (59) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_06 | off | 161 | - | -: none | - | 349.0 (47) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_06 | on | 161 | +0 | -: none | - | 349.0 (47) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_07 | off | 161 | - | -: none | - | 405.4 (120) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_07 | on | 161 | +0 | -: none | - | 405.4 (120) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_08 | off | 167 | - | -: none | - | 316.4 (0) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_08 | on | 167 | +0 | -: none | - | 316.4 (0) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_09 | off | 161 | - | -: none | - | 387.6 (66) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_09 | on | 161 | +0 | -: none | - | 387.6 (66) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_10 | off | 171 | - | -: none | - | 352.8 (1) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_10 | on | 171 | +0 | -: none | - | 352.8 (1) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_11 | off | 161 | - | -: none | - | 411.2 (127) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s10_11 | on | 161 | +0 | -: none | - | 411.2 (127) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s11_01 | off | 74 | - | 14: switch | - | 66.2 (56) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s11_01 | on | 76 | +2 | 16: switch | +2 | 66.2 (58) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s11_02 | off | 169 | - | 14: hold 2 | - | 50.4 (24) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s11_02 | on | 169 | +0 | 10: hold 2 | -4 | 50.4 (24) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s11_03 | off | 113 | - | 6: hold 3 | - | 51.3 (13) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s11_03 | on | 35 | -78 | -: none | - | 11.3 (12) | 4 | 5 (2 / 3) | 11-19: 11.3 |
| step 5b | scenario_s12_01 | off | 131 | - | 25: switch | - | 87.6 (79) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s12_01 | on | 130 | -1 | 8: switch | -17 | 72.1 (78) | 0 | 0 (0 / 0) | none |
| step 5b | scenario_s12_02 | off | 161 | - | 75: hold 18 | - | 32.3 (140) | 2 | 2 (1 / 1) | 138-141: 32.3 |
| step 5b | scenario_s12_02 | on | 162 | +1 | 93: hold 18 | +18 | 33.6 (139) | 3 | 1 (0 / 1) | 138-141: 33.6 |

#### B3. Every case below min_separation, with its cause

| step | scenario | side | ticks | min | standing / viol / recede | decision in force: projection | human's true task | cause | the same span below min_separation on the other side (±5 ticks) |
|---|---|---|---|---|---|---|---|---|---|
| step 5 | scenario_s16_01 | off | 44-50 | 37.0 | 6 / 1 / 0 | 30: fallback moving k=31 | item_4 | other: no projection past the human's arrival at shelf_4 (the moving fallback runs to 44); the robot arrives beside the turn and holds there, standing | 49-51 |
| step 5 | scenario_s16_01 | on | 49-51 | 41.7 | 0 / 2 / 1 | 0: admitted item_4 | item_4 | turn (TODO-146): the admitted plan about one tick and 18 cm ahead of the executed human at the turn | 44-50 |
| step 5 | scenario_s16_02 | on | 48-50 | 29.3 | 0 / 2 / 1 | 38: admitted item_4 | item_4 | turn (TODO-146): the admitted plan about one tick and 18 cm ahead of the executed human at the turn | 44-50 |
| step 5 | scenario_s16_05 | on | 22-27 | 28.3 | 0 / 4 / 2 | 0: admitted item_4 | ac_activation | wrong admission: deliver_item(item_4) admitted while the human walks to the A/C switch; no hold | none |
| step 5b | scenario_s11_03 | on | 11-19 | 11.3 | 4 / 2 / 3 | 0: admitted item_12 | unmodelled | wrong admission: deliver_item(item_12), assigned and never performed, admitted at 0 while the human stands at the occupied table; no hold, item_8 released beside the human | none |
| step 5b | scenario_s12_02 | off | 138-141 | 32.3 | 2 / 1 / 1 | 137: fallback moving k=3 | item_2 | other: the human, leaving the coffee machine, walks past the robot standing in its hold (decided at 137 on a moving fallback); the robot moves off at 140 | 138-141 |
| step 5b | scenario_s12_02 | on | 138-141 | 33.6 | 3 / 0 / 1 | 134: admitted item_2 | item_2 | other: the human, leaving the coffee machine, walks past the robot standing in its hold (decided at 134 on the admitted deliver_item(item_2), the true task); the robot moves off at 141 | 138-141 |

#### Planning tallies

- completion, on against off: better 7, equal 13, worse 2; ticks gained 134 over 7 runs ([-78, -24, -23, -5, -2, -1, -1]), ticks lost 3 over 2 runs ([1, 2])
- cases below min_separation, off, other: 2 (s16_01 44, s12_02 138)
- cases below min_separation, on, other: 1 (s12_02 138)
- cases below min_separation, on, turn (TODO-146): 2 (s16_01 49, s16_02 48)
- cases below min_separation, on, wrong admission: 2 (s16_05 22, s11_03 11)
