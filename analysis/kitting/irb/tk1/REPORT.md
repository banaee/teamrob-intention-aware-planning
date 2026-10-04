# T-K part 1, round 1 (no context knowledge): the report

31 runs (3 October 2026): scenario_s13_01 to _07 (env_layout_15), s14_01 to _11 (env_layout_16), s15_01 to _13
(env_layout_17); the set, its order and its measure are in `README.md`; the expectations and their md5s were committed
before any run (4cd7bca). Prior on (assignment knowledge), robot idle, test level 0.05, θ = 0.75. The recognizer's
outputs are checked; nothing here measures recognition quality against a target, and no value or room was changed
after a run.

## The comparison

- **0 disagreements at 1e-9 against the in-process BeliefState in all 31 runs**; 0 rows on one side only; the
  trajectory equals the run's human lines on every tick; the in-process `[IR*]` lines are byte-identical to the logged
  runs'.
- At print precision against the log: 1 disagreement, s14_02 tick 181 (ac_activation's adequacy; S = 0.049970 prints
  as 0.0500), classified in its `diff.md`: the IRB's known print-precision flag, not a disagreement with the records.
- Every committed `expected.csv` and `trajectory.json` was reproduced byte-identical by the run's own oracle call (the
  README's md5s).
- **TODO-66's context weight did not act**: the last observed tick of any run is 480 (s13_07, s15_07), below 500.

## The measure per scenario

KT3's measure (`admission.py ... actual.csv 0.75`; identical, row for row, to the same table read from `expected.csv`
before the runs). Ticks inclusive; delay from the stretch's first tick in brackets. No retraction occurs in any run:
once admitted, the true hypothesis stays admitted until its pin.

| scenario | true hypothesis | ticks | first ≥ θ | admitted | after admission (not clearing for it) | other admissions |
|---|---|---|---|---|---|---|
| s13_01 | deliver_item(item_3) | 0 to 66 | 26 (26) | 26 (26) | - | - |
| s13_01 | deliver_item(item_2) | 67 to 123 | 97 (30) | 97 (30) | - | - |
| s13_01 | deliver_item(item_1) | 124 to 216 | 161 (37) | 161 (37) | - | - |
| s13_01 | deliver_item(item_4) | 217 to 308 | 248 (31) | 248 (31) | - | - |
| s13_02 | deliver_item(item_3) | 0 to 66 | 26 (26) | 26 (26) | - | - |
| s13_02 | coffee_break(coffee_machine_0) | 67 to 140 | 101 (34) | 101 (34) | - | - |
| s13_02 | deliver_item(item_2) | 141 to 192 | 149 (8) | 149 (8) | - | - |
| s13_02 | deliver_item(item_1) | 193 to 285 | 230 (37) | 230 (37) | - | - |
| s13_02 | deliver_item(item_4) | 286 to 377 | 317 (31) | 317 (31) | - | - |
| s13_03 | deliver_item(item_3) | 0 to 66 | 26 (26) | 26 (26) | - | - |
| s13_03 | deliver_item(item_2) | 67 to 123 | 97 (30) | 97 (30) | - | - |
| s13_03 | coffee_break(coffee_machine_0) | 124 to 197 | 158 (34) | 158 (34) | - | - |
| s13_03 | deliver_item(item_1) | 198 to 279 | 219 (21) | 219 (21) | - | - |
| s13_03 | deliver_item(item_4) | 280 to 371 | 311 (31) | 311 (31) | - | - |
| s13_04 | deliver_item(item_3) | 0 to 66 | 26 (26) | 26 (26) | - | - |
| s13_04 | deliver_item(item_2) | 67 to 123 | 97 (30) | 97 (30) | - | - |
| s13_04 | deliver_item(item_1) | 124 to 216 | 161 (37) | 161 (37) | - | - |
| s13_04 | coffee_break(coffee_machine_0) | 217 to 289 | 249 (32) | 249 (32) | - | 289 deliver_item(item_4) |
| s13_04 | deliver_item(item_4) | 290 to 356 | 295 (5) | 295 (5) | - | - |
| s13_05 | deliver_item(item_3) | 0 to 66 | 26 (26) | 26 (26) | - | - |
| s13_05 | deliver_item(item_2) | 67 to 93 | never | never | - | - |
| s13_05 | coffee_break(coffee_machine_0) | 94 to 146 | 103 (9) | 103 (9) | - | - |
| s13_05 | deliver_item(item_2) | 147 to 198 | 156 (9) | 156 (9) | - | - |
| s13_05 | deliver_item(item_1) | 199 to 291 | 236 (37) | 236 (37) | - | - |
| s13_05 | deliver_item(item_4) | 292 to 383 | 323 (31) | 323 (31) | - | - |
| s13_06 | deliver_item(item_3) | 0 to 66 | 26 (26) | 26 (26) | - | - |
| s13_06 | deliver_item(item_2) | 67 to 95 | never | never | - | - |
| s13_06 | coffee_break(coffee_machine_0) | 96 to 148 | 104 (8) | 104 (8) | - | - |
| s13_06 | deliver_item(item_2) | 149 to 193 | 170 (21) | 170 (21) | - | - |
| s13_06 | deliver_item(item_1) | 194 to 286 | 231 (37) | 231 (37) | - | - |
| s13_06 | deliver_item(item_4) | 287 to 378 | 318 (31) | 318 (31) | - | - |
| s13_07 | deliver_item(item_3) | 0 to 66 | 26 (26) | 26 (26) | - | - |
| s13_07 | deliver_item(item_2) | 67 to 121 | 97 (30) | 97 (30) | - | - |
| s13_07 | coffee_break(coffee_machine_0) | 122 to 195 | 153 (31) | 163 (41) | - | 123 to 130 deliver_item(item_2) |
| s13_07 | deliver_item(item_2) | 196 to 240 | 217 (21) | 217 (21) | - | - |
| s13_07 | deliver_item(item_1) | 241 to 334 | 278 (37) | 278 (37) | - | - |
| s13_07 | deliver_item(item_4) | 335 to 428 | 367 (32) | 367 (32) | - | - |
| s14_01 | deliver_item(item_0) | 0 to 88 | 50 (50) | 50 (50) | - | - |
| s14_01 | deliver_item(item_2) | 89 to 180 | 138 (49) | 138 (49) | - | - |
| s14_01 | deliver_item(item_1) | 181 to 282 | 232 (51) | 232 (51) | - | - |
| s14_02 | deliver_item(item_0) | 0 to 88 | 50 (50) | 50 (50) | - | - |
| s14_02 | coffee_break(coffee_machine_0) | 89 to 166 | 143 (54) | 143 (54) | - | - |
| s14_02 | deliver_item(item_2) | 167 to 225 | 177 (10) | 177 (10) | - | - |
| s14_02 | deliver_item(item_1) | 226 to 325 | 277 (51) | 277 (51) | - | - |
| s14_03 | deliver_item(item_0) | 0 to 88 | 50 (50) | 50 (50) | - | - |
| s14_03 | deliver_item(item_2) | 89 to 180 | 138 (49) | 138 (49) | - | - |
| s14_03 | coffee_break(coffee_machine_0) | 181 to 259 | 235 (54) | 235 (54) | - | - |
| s14_03 | deliver_item(item_1) | 260 to 318 | 269 (9) | 269 (9) | - | - |
| s14_04 | deliver_item(item_0) | 0 to 88 | 50 (50) | 50 (50) | - | - |
| s14_04 | deliver_item(item_2) | 89 to 132 | never | never | - | - |
| s14_04 | coffee_break(coffee_machine_0) | 133 to 174 | 149 (16) | 149 (16) | - | - |
| s14_04 | deliver_item(item_2) | 175 to 233 | 187 (12) | 187 (12) | - | - |
| s14_04 | deliver_item(item_1) | 234 to 333 | 285 (51) | 285 (51) | - | - |
| s14_05 | deliver_item(item_0) | 0 to 88 | 50 (50) | 50 (50) | - | - |
| s14_05 | deliver_item(item_2) | 89 to 134 | never | never | - | - |
| s14_05 | coffee_break(coffee_machine_0) | 135 to 176 | 150 (15) | 150 (15) | - | - |
| s14_05 | deliver_item(item_2) | 177 to 226 | 187 (10) | 187 (10) | - | - |
| s14_05 | deliver_item(item_1) | 227 to 328 | 278 (51) | 278 (51) | - | - |
| s14_06 | deliver_item(item_0) | 0 to 88 | 50 (50) | 50 (50) | - | - |
| s14_06 | deliver_item(item_2) | 89 to 178 | 138 (49) | 138 (49) | - | - |
| s14_06 | coffee_break(coffee_machine_0) | 179 to 257 | 231 (52) | 231 (52) | - | 180 to 187 deliver_item(item_2) |
| s14_06 | deliver_item(item_2) | 258 to 307 | 267 (9) | 267 (9) | - | - |
| s14_06 | deliver_item(item_1) | 308 to 409 | 359 (51) | 359 (51) | - | - |
| s14_07 | deliver_item(item_0) | 0 to 88 | 50 (50) | 50 (50) | - | - |
| s14_07 | ac_activation(ac_switch_0) | 89 to 137 | never | never | - | - |
| s14_07 | deliver_item(item_2) | 138 to 192 | 148 (10) | 148 (10) | - | - |
| s14_07 | deliver_item(item_1) | 193 to 294 | 244 (51) | 244 (51) | - | - |
| s14_08 | deliver_item(item_0) | 0 to 88 | 50 (50) | 50 (50) | - | - |
| s14_08 | deliver_item(item_2) | 89 to 180 | 138 (49) | 138 (49) | - | - |
| s14_08 | ac_activation(ac_switch_0) | 181 to 229 | never | never | - | - |
| s14_08 | deliver_item(item_1) | 230 to 293 | 242 (12) | 242 (12) | - | - |
| s14_09 | deliver_item(item_0) | 0 to 88 | 50 (50) | 50 (50) | - | - |
| s14_09 | deliver_item(item_2) | 89 to 132 | never | never | - | - |
| s14_09 | ac_activation(ac_switch_0) | 133 to 140 | never | never | - | - |
| s14_09 | deliver_item(item_2) | 141 to 194 | 151 (10) | 151 (10) | - | - |
| s14_09 | deliver_item(item_1) | 195 to 296 | 246 (51) | 246 (51) | - | - |
| s14_10 | deliver_item(item_0) | 0 to 88 | 50 (50) | 50 (50) | - | - |
| s14_10 | deliver_item(item_2) | 89 to 134 | never | never | - | - |
| s14_10 | ac_activation(ac_switch_0) | 135 to 142 | never | never | - | - |
| s14_10 | deliver_item(item_2) | 143 to 191 | 151 (8) | 151 (8) | - | - |
| s14_10 | deliver_item(item_1) | 192 to 293 | 243 (51) | 243 (51) | - | - |
| s14_11 | deliver_item(item_0) | 0 to 88 | 50 (50) | 50 (50) | - | - |
| s14_11 | deliver_item(item_2) | 89 to 178 | 138 (49) | 138 (49) | - | - |
| s14_11 | ac_activation(ac_switch_0) | 179 to 227 | never | never | - | 180 to 187 deliver_item(item_2) |
| s14_11 | deliver_item(item_2) | 228 to 276 | 236 (8) | 236 (8) | - | - |
| s14_11 | deliver_item(item_1) | 277 to 378 | 328 (51) | 328 (51) | - | - |
| s15_01 | deliver_item(item_3) | 0 to 66 | 28 (28) | 28 (28) | - | - |
| s15_01 | deliver_item(item_2) | 67 to 123 | 97 (30) | 97 (30) | - | - |
| s15_01 | deliver_item(item_1) | 124 to 216 | 171 (47) | 171 (47) | - | - |
| s15_01 | deliver_item(item_4) | 217 to 308 | 262 (45) | 262 (45) | - | - |
| s15_02 | deliver_item(item_3) | 0 to 66 | 28 (28) | 28 (28) | - | - |
| s15_02 | coffee_break(coffee_machine_0) | 67 to 140 | 103 (36) | 103 (36) | - | - |
| s15_02 | deliver_item(item_2) | 141 to 192 | 150 (9) | 150 (9) | - | - |
| s15_02 | deliver_item(item_1) | 193 to 285 | 240 (47) | 240 (47) | - | - |
| s15_02 | deliver_item(item_4) | 286 to 377 | 332 (46) | 332 (46) | - | - |
| s15_03 | deliver_item(item_3) | 0 to 66 | 28 (28) | 28 (28) | - | - |
| s15_03 | deliver_item(item_2) | 67 to 123 | 97 (30) | 97 (30) | - | - |
| s15_03 | coffee_break(coffee_machine_0) | 124 to 197 | 160 (36) | 160 (36) | - | - |
| s15_03 | deliver_item(item_1) | 198 to 279 | 227 (29) | 227 (29) | - | - |
| s15_03 | deliver_item(item_4) | 280 to 371 | 325 (45) | 325 (45) | - | - |
| s15_04 | deliver_item(item_3) | 0 to 66 | 28 (28) | 28 (28) | - | - |
| s15_04 | deliver_item(item_2) | 67 to 123 | 97 (30) | 97 (30) | - | - |
| s15_04 | deliver_item(item_1) | 124 to 216 | 171 (47) | 171 (47) | - | - |
| s15_04 | coffee_break(coffee_machine_0) | 217 to 289 | 252 (35) | 252 (35) | - | - |
| s15_04 | deliver_item(item_4) | 290 to 356 | 313 (23) | 313 (23) | - | - |
| s15_05 | deliver_item(item_3) | 0 to 66 | 28 (28) | 28 (28) | - | - |
| s15_05 | deliver_item(item_2) | 67 to 93 | never | never | - | - |
| s15_05 | coffee_break(coffee_machine_0) | 94 to 146 | 104 (10) | 104 (10) | - | - |
| s15_05 | deliver_item(item_2) | 147 to 198 | 157 (10) | 157 (10) | - | - |
| s15_05 | deliver_item(item_1) | 199 to 291 | 246 (47) | 246 (47) | - | - |
| s15_05 | deliver_item(item_4) | 292 to 383 | 338 (46) | 338 (46) | - | - |
| s15_06 | deliver_item(item_3) | 0 to 66 | 28 (28) | 28 (28) | - | - |
| s15_06 | deliver_item(item_2) | 67 to 95 | never | never | - | - |
| s15_06 | coffee_break(coffee_machine_0) | 96 to 148 | 104 (8) | 104 (8) | - | - |
| s15_06 | deliver_item(item_2) | 149 to 193 | 170 (21) | 170 (21) | - | - |
| s15_06 | deliver_item(item_1) | 194 to 286 | 241 (47) | 241 (47) | - | - |
| s15_06 | deliver_item(item_4) | 287 to 378 | 332 (45) | 332 (45) | - | - |
| s15_07 | deliver_item(item_3) | 0 to 66 | 28 (28) | 28 (28) | - | - |
| s15_07 | deliver_item(item_2) | 67 to 121 | 97 (30) | 97 (30) | - | - |
| s15_07 | coffee_break(coffee_machine_0) | 122 to 195 | 153 (31) | 163 (41) | - | 123 to 130 deliver_item(item_2) |
| s15_07 | deliver_item(item_2) | 196 to 240 | 217 (21) | 217 (21) | - | - |
| s15_07 | deliver_item(item_1) | 241 to 334 | 288 (47) | 288 (47) | - | - |
| s15_07 | deliver_item(item_4) | 335 to 428 | 381 (46) | 381 (46) | - | - |
| s15_08 | deliver_item(item_3) | 0 to 66 | 28 (28) | 28 (28) | - | - |
| s15_08 | ac_activation(ac_switch_0) | 67 to 114 | never | never | - | - |
| s15_08 | deliver_item(item_2) | 115 to 183 | 135 (20) | 135 (20) | - | - |
| s15_08 | deliver_item(item_1) | 184 to 276 | 231 (47) | 231 (47) | - | - |
| s15_08 | deliver_item(item_4) | 277 to 368 | 322 (45) | 322 (45) | - | - |
| s15_09 | deliver_item(item_3) | 0 to 66 | 28 (28) | 28 (28) | - | - |
| s15_09 | deliver_item(item_2) | 67 to 123 | 97 (30) | 97 (30) | - | - |
| s15_09 | ac_activation(ac_switch_0) | 124 to 171 | never | never | - | - |
| s15_09 | deliver_item(item_1) | 172 to 229 | 180 (8) | 180 (8) | - | - |
| s15_09 | deliver_item(item_4) | 230 to 323 | 276 (46) | 276 (46) | - | - |
| s15_10 | deliver_item(item_3) | 0 to 66 | 28 (28) | 28 (28) | - | - |
| s15_10 | deliver_item(item_2) | 67 to 123 | 97 (30) | 97 (30) | - | - |
| s15_10 | deliver_item(item_1) | 124 to 216 | 171 (47) | 171 (47) | - | - |
| s15_10 | ac_activation(ac_switch_0) | 217 to 263 | never | never | - | - |
| s15_10 | deliver_item(item_4) | 264 to 321 | 280 (16) | 280 (16) | - | - |
| s15_11 | deliver_item(item_3) | 0 to 66 | 28 (28) | 28 (28) | - | - |
| s15_11 | deliver_item(item_2) | 67 to 93 | never | never | - | - |
| s15_11 | ac_activation(ac_switch_0) | 94 to 134 | never | never | - | - |
| s15_11 | deliver_item(item_2) | 135 to 203 | 155 (20) | 155 (20) | - | - |
| s15_11 | deliver_item(item_1) | 204 to 296 | 251 (47) | 251 (47) | - | - |
| s15_11 | deliver_item(item_4) | 297 to 388 | 342 (45) | 342 (45) | - | - |
| s15_12 | deliver_item(item_3) | 0 to 66 | 28 (28) | 28 (28) | - | - |
| s15_12 | deliver_item(item_2) | 67 to 95 | never | never | - | - |
| s15_12 | ac_activation(ac_switch_0) | 96 to 136 | 121 (25) | 133 (37) | - | - |
| s15_12 | deliver_item(item_2) | 137 to 184 | 164 (27) | 164 (27) | - | - |
| s15_12 | deliver_item(item_1) | 185 to 278 | 232 (47) | 232 (47) | - | - |
| s15_12 | deliver_item(item_4) | 279 to 372 | 325 (46) | 325 (46) | - | - |
| s15_13 | deliver_item(item_3) | 0 to 66 | 28 (28) | 28 (28) | - | - |
| s15_13 | deliver_item(item_2) | 67 to 121 | 97 (30) | 97 (30) | - | - |
| s15_13 | ac_activation(ac_switch_0) | 122 to 169 | 154 (32) | 166 (44) | - | 123 to 130 deliver_item(item_2) |
| s15_13 | deliver_item(item_2) | 170 to 216 | 197 (27) | 197 (27) | - | - |
| s15_13 | deliver_item(item_1) | 217 to 308 | 263 (46) | 263 (46) | - | - |
| s15_13 | deliver_item(item_4) | 309 to 400 | 354 (45) | 354 (45) | - | - |

## Per room, in short

| room | deliveries: reach θ (median delay) | coffee_break: reach θ (median delay) | ac_activation: reach θ |
|---|---|---|---|
| env_layout_15 (basic) | 29 of 31 (30) | 6 of 6 (31.5; admitted 33) | no A/C switch |
| env_layout_16 (dense) | 35 of 39 (50) | 5 of 5 (52) | 0 of 5 |
| env_layout_17 (A/C between two shelves) | 54 of 58 (30) | 6 of 6 (33; admitted 35.5) | 2 of 6 |

The deliveries that never reach θ are first parts of the second delivery cut by the foreseeable task (the walk to the
shelf, or the walk and the grasp), except in env_layout_16, where the whole walk to shelf_2 (44 ticks, s14_04, _05,
_09, _10) ends without it.

## What the rooms show about separation by movement alone

- **env_layout_15, the basic room.** The movement separates every task within its walk, late: a delivery reaches θ at
  about 70 to 85 % of the walk to its shelf (item_3 at 26 of 32 ticks, item_1 at 37 of 45, item_4 at 31 of 44), the
  short walk to shelf_2 only on the carry back (30, after the 27-tick walk and the grasp); the coffee break from the
  table at 32 to 34 ticks of its 43-tick walk. From shelf_2 (inside the second delivery) the coffee break reaches θ
  after 8 to 10 ticks: no live delivery lies in that direction.
- **env_layout_17, the A/C switch between two shelves.** The A/C hypothesis delays the two deliveries it stands
  between: in the control, item_1 reaches θ at 47 ticks (37 in env_layout_15), item_4 at 45 (31); item_3 and item_2,
  away from it, are nearly unchanged (28 and 30, against 26 and 30). The coffee break reaches θ 0 to 3 ticks later than in
  env_layout_15. The A/C activation itself, with empty hands (from the table after a delivery, s15_08 to _10; from
  shelf_2 before the grasp, s15_11), never reaches θ: it leads at its arrival but peaks at 0.61 to 0.75 and is pinned on
  the next tick (its wait is one tick, PT2S); twice (s15_10, s15_11) it peaks at 0.746 and 0.745, below θ by less than
  0.005. With item_2 in hand it reaches θ (s15_12 from shelf_2 at 25 ticks, s15_13 from the table at 32): holding an
  item, the rival deliveries expect it to be put back first (deliver_item's method with the return, `move_to(shelf_2)`),
  so the walk toward the A/C switch refutes them.
- **env_layout_16, the dense room.** The movement does not separate the cluster before the arrival. Every delivery
  reaches θ only after the grasp, on the carry back (49 to 51 ticks into a stretch whose walk out is 43 to 49 ticks); the
  walk to shelf_2 alone never reaches it. The coffee break reaches θ only during its wait (52 to 54 ticks into a
  47-tick walk from the table; 15 to 16 ticks from shelf_2, after the arrival). The A/C activation never, with the item
  in hand or not: its belief peaks at 0.43 to 0.55 at its arrival and it is pinned on the next tick.

## Observations (stated, not ruled)

1. **The A/C activation completes about when the movement could single it out.** Its one-tick wait leaves no
   standing time for the evidence (in contrast with the coffee break's 30 ticks, in which env_layout_16's coffee break
   is recognized). Without context knowledge it is never admitted in env_layout_16, and in env_layout_17 only when the
   human holds an item (which takes the rival deliveries out of its direction). For round 2: in the A/C cases admission may not be the informative measure; the A/C's belief at its arrival
   tick (the one tick it leads) shows the prior's effect directly. The duration is the schema's (PT2S); no value is
   proposed here.
2. **Two A/C peaks lie within 0.005 of θ** (s15_10, s15_11). Any small change in the prior moves them across; when
   context knowledge is on, those two will flip on almost any strength. Recorded so that the flip is not read as the
   strength's effect.
3. **A foreseeable task started after the carry, before the place** (s13_07, s15_07, s15_13, s14_06, s14_11): the
   delivery keeps leading and is admitted for the first 8 ticks of the walk away from the table (the item still in
   hand, its place pending); the coffee break then leads with belief ≥ θ but is inadequate until the arrival (s13_07,
   s15_07: θ at 153, admitted at 163). Its phase origin is the episode's start, so the walk to shelf_2 and back
   already counts against it, and no boundary falls between (the delivery is not complete). The same in s15_13 for the
   A/C (θ 154, admitted 166).
4. **The interrupted delivery's first part** (the walk to shelf_2, inside the second delivery) never reaches θ in any
   room: short in 15 and 17 (27 to 29 ticks), the whole walk in 16.

## For the runs with context knowledge

- The foreseeable tasks' start and completion ticks per scenario are in `README.md` ("The foreseeable tasks' ticks"),
  from the trajectory, which context knowledge does not change (R1); the timelines of break_time and room_warm can be
  authored from them so that the task falls inside the window in one setup and outside in the other.
- Every scenario keeps a delivery live while its foreseeable task runs (placements after the third delivery at most in
  15 and 17, the second in 16), so the prior has work as a whole to weigh against.
- The run lengths stay below 500; the round with context knowledge removes TODO-66's weight (AM22), after which the
  bound no longer matters.

## The gate on the belief over the live hypotheses: the rerun (T-K part 1, build stage 2, 4 October 2026)

The tables above are the old gate's (the reported distribution's leader value). Rerun with the gate of AM42 (the belief
over the live hypotheses, before the floor and the pin scaling), the 31 runs:
- 0 disagreements at 1e-9 against the in-process BeliefState in all 31; at print precision the one known flag (s14_02
  tick 181). The trajectories are byte-identical: the robot is idle, and the gate changes no human tick.
- The measure moves in four rows, each an admission one tick earlier, no retraction:
  s15_02 deliver_item(item_4) 331 (45), was 332 (46); s15_05 deliver_item(item_4) 337 (45), was 338 (46);
  s15_10 deliver_item(item_4) 279 (15), was 280 (16); s15_12 deliver_item(item_1) 231 (46), was 232 (47).
- The per-room table is unchanged (counts and medians).
- The two A/C peaks of observation 2 read 0.7487 (s15_10) and 0.7468 (s15_11) over the live hypotheses, still below θ.
- Beyond the measure, the gate's per-tick answer moves on 15 ticks in env_layout_17 (s15_01 to _13), each a leader at
  0.747 to 0.750 that now clears (or, s15_07 tick 146, turns inadequate instead of below θ): ten on the coffee break's
  hypothesis during the exit walk, after the last delivery. env_layout_15 and _16 move on no tick.
