# The MPB on dock_loading: authoring

The set, its rulings and the build plan's dispositions: design_decisions.md, "T-G: the second domain's rulings", THE MPB
ON DOCK_LOADING (MPB-DL1 to MPB-DL7, DISPOSITIONS, THE SET, RULED ON THE SET, THE BUILD'S PLAN CONFIRMED with DL-P1 to
DL-P9). This file holds the artefacts, the derivations of every authored duration and cut point from path lengths, the
disjointness check and the step cap. Hand-derived ticks below are the plan's; none is binding (DL-P6): the oracle's
table, committed before the runs, decides every tick.

## The rooms (unchanged) and the body's rule

env_layout_03 and env_layout_04 (B14). Positions in cm; one tick is 2 seconds; the body walks in whole steps of 20 cm
toward the target until within the arrival radius (30 cm), then one acknowledgement tick; a scan is a touch and its
acknowledgement; a wait or a stand of n ticks is n ticks and its acknowledgement. This rule reproduces the IRB's
last acknowledgement ticks of C1, C5, C6, C11 and C14 in both rooms exactly.

| object | env_layout_03 | env_layout_04 |
|---|---|---|
| dry_delivery_bay_0 | (-515, 215) | (-255, 215) |
| frozen_delivery_bay_0 | (515, 0) | (-515, -35) |
| empty_pallet_bay_0 | (-515, -35) | (515, -35) |
| coffee_machine_0 | (-400, -230) | (-400, -230) |
| truck_interior, dock_gate, office_door, office_chair, desk, standby_place | (0, -590), (0, -300), (0, 300), (130, 365), (300, -260), (0, 0) | the same |

## The setups of kind 3 (MPB-DL2 as amended and named)

env_setup_08 (env_layout_03) and env_setup_09 (env_layout_04), the same content: pallet_0 and pallet_1 in the dry bay,
pallet_2 and pallet_3 in the frozen bay, each designated to the bay it stands in (the human scans only these); pallet_4
in the truck designated to the dry bay (deliver-dry), pallet_5 in the truck designated to the frozen bay
(deliver-frozen); pallet_6 and pallet_7 empty in the empties container, designated to the truck (return-1, return-2);
`is_open(dock_gate)`. A test condition, not the work cycle (D9). The robot places its pallets at a container point that
already holds two (B9's note, one point per container).

## The scenarios

The human starts at the standby place (0, 0) and closes with `go_to("desk")`; the robot starts on the truck side at
(0, -370); prior on. "scan n" is `confirm_delivered_pallet("pallet_n")`; the assigned tasks are the script's scans.

| row | env_layout_03 | env_layout_04 | script | robot pool |
|---|---|---|---|---|
| K1 | scenario_s08_01 | scenario_s09_01 | 03: scan 2; 04: scan 0 | 03: deliver 4, return 6; 04: deliver 5 |
| K2 | scenario_s08_02 | scenario_s09_02 | scan 0, scan 2 | deliver 4, deliver 5, return 6 |
| K3 | scenario_s08_03 | scenario_s09_03 | scan 0, stand PT192S | deliver 4, deliver 5, return 6 |
| K4 | scenario_s08_04 | scenario_s09_04 | as K3 | deliver 4 |
| K5 | scenario_s08_05 | scenario_s09_05 | scan 0, scan 1 | deliver 4, deliver 5, return 6 |
| K6 | scenario_s08_06 | scenario_s09_06 | scan 0, coffee_break, scan 2 | the four |
| K7 | scenario_s08_07 | scenario_s09_07 | scan 0, office_break, scan 2 | the four |
| K8 | scenario_s08_08 | scenario_s09_08 | scan 0 `.during(move_to, PT52S / PT30S, coffee_break)`, scan 2 | deliver 4, deliver 5, return 6 |
| K9 | scenario_s08_09 | scenario_s09_09 | scan 2, go_to(standby_place), stand PT60S | deliver 4, return 6 |
| M3 | scenario_s08_10 | scenario_s09_10 | scan 0 `.at(move_to, coffee_break)`, scan 1, scan 2, stand PT192S | the four |
| M1 | scenario_s05_04 | scenario_s07_04 | kind 2, ON_ROBOT: scans 0 to 3, standby entry | deliver 0 to 3, return 4, 5 |
| M2 | scenario_s05_05 | scenario_s07_05 | as M1, scan 2 `.at(scan_it, office_break)` | as M1 |
| M4 | scenario_s05_06 | scenario_s07_06 | kind 2, ON_ROBOT: scan 2 `.during(move_to, PT28S, drop)`, scan 3 `.at(move_to, coffee_break)`, scan 0, scan 1, scan 2, standby | as M1 |

## The derivations

- **K1, the pairing** (RULED ON THE SET, K1; DL-P3). The condition: every human walk and stand (and so every fallback ray,
  which lies on the human's walk and stops at its target or the first fixed object) keeps more than min_separation
  (50 cm) from every robot route segment and stopping point, in every order of the pool; then no realized plan can
  violate and no hold is possible, whatever the timing. Searched over the scans of pallet_0 and pallet_2 and every
  subset of deliver-dry, deliver-frozen, return-1 (scratch geometry, the body's rule): env_layout_03, scan 2 with
  deliver-dry and return-1, minimum clearance 225.6 cm (the original pairing); env_layout_04, scan 0 with deliver-frozen
  alone, 248.3 cm; every other pairing of env_layout_04 crosses a human walk (with a return: the desk walk crosses the
  route to the empties at x = 37; with deliver-dry: the walk to the frozen bay crosses it at (-154, 10)).
- **The stand of K3, K4 and M3: 96 ticks, PT192S.** K4's test needs three holds at successive expiries. After the scan's
  boundary the standing fallback's cadence is end = t + 1 + k (k the standing count): decisions at 28, 31, 37, 49, 73,
  121, 217 (env_layout_03) and 17, 20, 26, 38, 62, 110 (env_layout_04). With the robot's plain arrival at the dry bay at
  about 61 (03) and 54 (04), the holds fall at 49, 73, 121 and 38, 62, 110; the human must still stand at 121 (03) and
  110 (04): 91 ticks from the stand's first tick in both rooms. 96 adds 5 against an off-by-one in this hand count
  (the oracle's table is exact). K3 and M3 use the same human stand (K3 is "as K4" for the human; M3 combines K3).
- **The stand of K9: 30 ticks, PT60S**: MPB-5's idle margin, which covers E5's standing threshold (25 ticks at
  alpha = 0.01); the IRB's C14 shows the leader inadequate 15 (03) and 7 (04) ticks after the arrival.
- **K8's cut, DL-P1**: on the last step of the walk to pallet_0. The walk from the standby place is 27 steps in
  env_layout_03 (558 cm) and 16 in env_layout_04 (334 cm); the cut fires after 26, respectively 15, executed ticks:
  PT52S and PT30S. The human then walks to the coffee machine, waits, resumes the scan (the walk to pallet_0), scans
  pallet_2 and closes.
- **M4's drop: PT28S** (14 ticks), the IRB's approved value; shorter than every walk to a bay from the standby
  place.
- coffee_break and office_break last 60 and 90 seconds (the schema's; MPB-DL5).

## The disjointness check (MPB-DL7)

`disjoint.py` over the controlled scenarios and M3, before any run (its output, at authoring):

```
scenario_s08_01: the human's assigned scans ['pallet_2']; the robot's pool ['pallet_4', 'pallet_6']; named by both: none
scenario_s08_02: the human's assigned scans ['pallet_0', 'pallet_2']; the robot's pool ['pallet_4', 'pallet_5', 'pallet_6']; named by both: none
scenario_s08_03: the human's assigned scans ['pallet_0']; the robot's pool ['pallet_4', 'pallet_5', 'pallet_6']; named by both: none
scenario_s08_04: the human's assigned scans ['pallet_0']; the robot's pool ['pallet_4']; named by both: none
scenario_s08_05: the human's assigned scans ['pallet_0', 'pallet_1']; the robot's pool ['pallet_4', 'pallet_5', 'pallet_6']; named by both: none
scenario_s08_06: the human's assigned scans ['pallet_0', 'pallet_2']; the robot's pool ['pallet_4', 'pallet_5', 'pallet_6', 'pallet_7']; named by both: none
scenario_s08_07: the human's assigned scans ['pallet_0', 'pallet_2']; the robot's pool ['pallet_4', 'pallet_5', 'pallet_6', 'pallet_7']; named by both: none
scenario_s08_08: the human's assigned scans ['pallet_0', 'pallet_2']; the robot's pool ['pallet_4', 'pallet_5', 'pallet_6']; named by both: none
scenario_s08_09: the human's assigned scans ['pallet_2']; the robot's pool ['pallet_4', 'pallet_6']; named by both: none
scenario_s08_10: the human's assigned scans ['pallet_0', 'pallet_1', 'pallet_2']; the robot's pool ['pallet_4', 'pallet_5', 'pallet_6', 'pallet_7']; named by both: none
scenario_s09_01: the human's assigned scans ['pallet_0']; the robot's pool ['pallet_5']; named by both: none
scenario_s09_02: the human's assigned scans ['pallet_0', 'pallet_2']; the robot's pool ['pallet_4', 'pallet_5', 'pallet_6']; named by both: none
scenario_s09_03: the human's assigned scans ['pallet_0']; the robot's pool ['pallet_4', 'pallet_5', 'pallet_6']; named by both: none
scenario_s09_04: the human's assigned scans ['pallet_0']; the robot's pool ['pallet_4']; named by both: none
scenario_s09_05: the human's assigned scans ['pallet_0', 'pallet_1']; the robot's pool ['pallet_4', 'pallet_5', 'pallet_6']; named by both: none
scenario_s09_06: the human's assigned scans ['pallet_0', 'pallet_2']; the robot's pool ['pallet_4', 'pallet_5', 'pallet_6', 'pallet_7']; named by both: none
scenario_s09_07: the human's assigned scans ['pallet_0', 'pallet_2']; the robot's pool ['pallet_4', 'pallet_5', 'pallet_6', 'pallet_7']; named by both: none
scenario_s09_08: the human's assigned scans ['pallet_0', 'pallet_2']; the robot's pool ['pallet_4', 'pallet_5', 'pallet_6']; named by both: none
scenario_s09_09: the human's assigned scans ['pallet_2']; the robot's pool ['pallet_4', 'pallet_6']; named by both: none
scenario_s09_10: the human's assigned scans ['pallet_0', 'pallet_1', 'pallet_2']; the robot's pool ['pallet_4', 'pallet_5', 'pallet_6', 'pallet_7']; named by both: none
```

## The step cap (MPB-5; DL-P7)

`horizon.py`: the robot's pool chained along its authored order from its start on plain cost (the method the planner's
decomposition selects in the chain's state; the body's walk rule; 2 ticks per pick_up and per place; one completion tick
per task; DL-P8: the decomposition's only use), plus the human's replay length (the replay's last acknowledgement + 1),
plus 30. For a script that depends on the robot (M1, M2, M4) the replay runs on the state after the robot's chain
(DL-P7). A safety cap, not an expectation; a run that reaches it is reported as such and the cap is not raised.

| row | env_layout_03 | cap | env_layout_04 | cap |
|---|---|---|---|---|
| K1 | scenario_s08_01 | 201 | scenario_s09_01 | 144 |
| K2 | scenario_s08_02 | 393 | scenario_s09_02 | 360 |
| K3 | scenario_s08_03 | 465 | scenario_s09_03 | 431 |
| K4 | scenario_s08_04 | 269 | scenario_s09_04 | 241 |
| K5 | scenario_s08_05 | 371 | scenario_s09_05 | 337 |
| K6 | scenario_s08_06 | 531 | scenario_s09_06 | 498 |
| K7 | scenario_s08_07 | 548 | scenario_s09_07 | 538 |
| K8 | scenario_s08_08 | 466 | scenario_s09_08 | 436 |
| K9 | scenario_s08_09 | 260 | scenario_s09_09 | 282 |
| M3 | scenario_s08_10 | 658 | scenario_s09_10 | 626 |
| M1 | scenario_s05_04 | 686 | scenario_s07_04 | 639 |
| M2 | scenario_s05_05 | 803 | scenario_s07_05 | 760 |
| M4 | scenario_s05_06 | 858 | scenario_s07_06 | 716 |

## The load and replay checks

Every one of the 26 scenarios loads through SimModel with its run file's options (the loader's checks, the load-time
replay, `check_script`): the 20 scripts independent of the robot replay exactly (an entry left open would stop the load);
the 6 that depend on the robot load with their open entries reported, as declared (T-G A3, Q13b).
