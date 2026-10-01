# The diagnostic rows C13, C14 and M4: predictions written before the runs

The standby walks of the IR test-bed set on dock_loading are diagnostic observations (design_decisions.md, "T-G: the
second domain's rulings", T-G Q16's block, the rules of the set). Written here before any run of the set, committed
with the expectations (the build's step 3.3). Only the present model's expectation is compared with the run; the
predictions under H1 and H2 are not compared and change nothing.

- **The present model** (Q16: the walk stays without a hypothesis): the oracle's expected values, `expected.csv` of
  each scenario, derived from the records (`analysis/kitting/ir_testbed/README.md`, rules 1 to 23;
  `analysis/instruments/ir_testbed/README.md`, rules 24 to 27). The table below is read from them.
- **H1** (TODO-155, a candidate, not approved): a foreseeable task "the human steps aside to the standby place",
  always possible, with the standby place as a fixed object. A PersonalTask, so in the support under the prior.
- **H2** (TODO-155, a candidate, not approved), read as Hadi ruled at the build's approval (1 October 2026): a
  hypothesis live only while no assigned task of the human is live.

## The predictions under H1 and H2 (qualitative, from the records; not compared)

H1, every row: while the human stands at the standby place its completion condition holds, so it is retired (L4); it
re-enters at 1/|H| on the first tick the human is out of reach of the place and, the human walking away from it, its
walk phase gains excess and it turns inadequate within a few ticks of every walk away (it competes with the scans when
a pallet waits, as Q16 records). On the standby walk its excess is zero (the walk goes straight to its target): it
leads, clears θ and holds observation warrant (movement source), so the gate clears on it within the walk; it is
pinned on arrival (its completion holds) and the live set is then the other hypotheses, as under the present model:
the finding unexplained once the human stands. If H1 is a walk only (its method's last action a `move_to`), `move_to`
becomes a terminal action of the task model and, under L1, the arrival at any target is an episode boundary: every
scan's walk would end an episode one action before the scan. A wait at the end of H1 would avoid that and changes the
pin to the wait's end.

H2, as read: no assigned task is live once every assigned scan is retired (its pallet scanned, L4) or inapplicable
(A4: pallet_4 in the truck).
- C13, C14: from the scan's pin (scan 0, respectively scan 2, retired; scan 4 never live) H2 is live; it is the only
  hypothesis predicting the walk to the standby place, so it leads the standby walk, clears θ with observation warrant
  and is pinned on arrival; then as under the present model.
- M4: scan 0 is assigned, never scanned and applicable throughout (pallet_0 stands in its bay), so it is live to the
  run's end and H2 is never live: the prediction under H2 equals the present model's expectation.

## The present model's expectation on the standby walk (from expected.csv, before the runs)

Per row and room: the standby walk's ticks (first step to its acknowledgement; the run ends at the last tick), the live set at its start, the leader and the gate per stretch to the run's end, and the finding's stretches. Read from `expected.csv` (rule 23 for the gate, θ = 0.75 the value of record).

| row | scenario (room) | walk | live at its start | leader and gate, per stretch | finding |
|---|---|---|---|---|---|
| C13 | scenario_s02_14 (env_layout_02) | 30–56 (end 86) | coffee_break(coffee_machine_0), office_break(office_chair) | 30–49 coffee_break(coffee_machine_0) none(below_theta); 50–70 coffee_break(coffee_machine_0) clears; 71–86 coffee_break(coffee_machine_0) none(leader_inadequate) | 30–70 adequate; 71–86 unexplained |
| C13 | scenario_s04_14 (env_layout_03) | 30–56 (end 86) | coffee_break(coffee_machine_0), office_break(office_chair) | 30–45 office_break(office_chair) none(below_theta); 46–56 office_break(office_chair) clears; 57–86 office_break(office_chair) none(leader_inadequate) | 30–56 adequate; 57–86 unexplained |
| C13 | scenario_s06_14 (env_layout_04) | 19–34 (end 64) | coffee_break(coffee_machine_0), office_break(office_chair) | 19–26 office_break(office_chair) none(below_theta); 27–64 coffee_break(coffee_machine_0) none(below_theta) | 19–35 adequate; 36–64 unexplained |
| C14 | scenario_s02_15 (env_layout_02) | 30–56 (end 86) | coffee_break(coffee_machine_0), office_break(office_chair) | 30–37 office_break(office_chair) none(below_theta); 38–56 office_break(office_chair) clears; 57–86 office_break(office_chair) none(leader_inadequate) | 30–56 adequate; 57–86 unexplained |
| C14 | scenario_s04_15 (env_layout_03) | 28–52 (end 82) | coffee_break(coffee_machine_0), office_break(office_chair) | 28–50 coffee_break(coffee_machine_0) none(below_theta); 51–66 coffee_break(coffee_machine_0) clears; 67–82 coffee_break(coffee_machine_0) none(leader_inadequate) | 28–66 adequate; 67–82 unexplained |
| C14 | scenario_s06_15 (env_layout_04) | 28–52 (end 82) | coffee_break(coffee_machine_0), office_break(office_chair) | 28–36 office_break(office_chair) none(below_theta); 37–58 office_break(office_chair) clears; 59–82 office_break(office_chair) none(leader_inadequate) | 28–58 adequate; 59–82 unexplained |
| M4 | scenario_s02_19 (env_layout_02) | 145–171 (end 201) | coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair) | 145–166 confirm_delivered_pallet(pallet_0) none(below_theta); 167–182 confirm_delivered_pallet(pallet_0) clears; 183–201 confirm_delivered_pallet(pallet_0) none(leader_inadequate) | 145–182 adequate; 183–201 unexplained |
| M4 | scenario_s04_19 (env_layout_03) | 148–172 (end 202) | coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair) | 148–202 confirm_delivered_pallet(pallet_0) none(below_theta) | 148–186 adequate; 187–202 unexplained |
| M4 | scenario_s06_19 (env_layout_04) | 126–150 (end 180) | coffee_break(coffee_machine_0), confirm_delivered_pallet(pallet_0), office_break(office_chair) | 126–142 office_break(office_chair) none(below_theta); 143–156 office_break(office_chair) clears; 157–180 office_break(office_chair) none(leader_inadequate) | 126–156 adequate; 157–180 unexplained |

## The three side by side, per row (the run compares the first column only)

| row | the present model (above) | H1 | H2 (no assigned task live) |
|---|---|---|---|
| C13 | the walk read as coffee_break or office_break by the room's bearings: cleared on the observation warrant in env_layout_02 (coffee_break, from 50) and env_layout_03 (office_break, from 46), never above θ in env_layout_04; unexplained once the human stands at the standby place | H1 leads the walk at zero excess and clears θ within it (observation warrant); pinned on arrival; then as the present model | live from the pin of scan 0 (scan 4 never live): as H1 on the walk; pinned on arrival; then as the present model |
| C14 | as C13 from the frozen bay: office_break cleared in env_layout_02 (38) and env_layout_04 (37), coffee_break in env_layout_03 (51) | as C13 | live from the pin of scan 2: as C13 |
| M4 | scan 0 (assigned, never scanned: commitment warrant) leads the walk in env_layout_02 (cleared from 167) and env_layout_03 (never above θ); office_break in env_layout_04 (cleared from 143); unexplained once standing | H1 at zero excess against scan 0's walk phase: H1 leads; scan 0 stays live and adequate only while its excess stays small | never live (scan 0 is live to the run's end): equal to the present model |
