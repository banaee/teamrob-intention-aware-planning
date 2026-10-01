# TODO-90: the two in-window approaches under gate b2a (attribution or hole)

> Superseding note (T-L stage 3, 26 Sept 2026): the layout and scenario ids here are the old ones; `docs/rename_table.md` maps them to the serial ids. The scripts and records stay frozen at their commit.

A check, nothing fixed. s10 prior off / on, s30 prior on; `--gate_strategy b2a --strategy single_task
--cost_strategy realized --separation_stop false`, PYTHONHASHSEED=0, main at 7f122fd (post-D3), 450 / 200 steps.
`capture.py` runs `run_mesa.py` unchanged and records each `realize()` call's segments (log byte-identical apart
from the timestamps); `tables.py` builds the tables. Logs local.

R1. The world did not move: `[sep]`, `[meta] `, `[hold]`, `[IR] step=` are byte-identical to the ablation's
without-trigger logs. Sub-50 cm ticks: s10 (both priors) 72 = 44.79, 73–75 = 30.87, 76 = 38.99 (tick-sampled);
s30 on 21 = 36.64, 22 = 11.03, 23 = 15.47 (min over the tick 8.47), 24 = 34.01 (min 15.47). Correction to the
ablation / TODO-90: under prior on the s10 decision is at tick **24**, not 29.

## R2. Decisions

Assessed window as the glossary and `realize()` define it: [decision, T_h] ∩ the human projection's span (from
the observation offset, 1 on the clock) ∩ the realized plan's span; tick k covers [k − t, k − t + 1] on the clock
of the decision at t (the executor's `[stop]` convention; the capture matches it: s10 off human and robot
positions equal the projection to 0.01 cm at every end of tick k at τ = k − t + 1 up to tick 72). "Ticks inside":
those whose whole interval lies in the window, up to the next decision. `T_h` = B2's `remaining` (T_h − 0).

**s10 prior off**

| tick | trigger | admitted hypothesis / refusal | T_h | realized end | assessed window (clock) | ticks inside | hold | block |
|---|---|---|---|---|---|---|---|---|
| 0 | no_current_task | refused (below_theta) | — | — | — | — | 0 | B3 |
| 29 | recognition_changed | deliver_item(?item=item_2) | 48.29 | 46.81 | [1, 46.81] | 30–74 | 0 | B2 continue |
| 75 | recognition_changed | refused (below_theta) | — | — | — | — | 0 | B3 |
| 123 | recognition_changed | coffee_break(?coffee_machine=coffee_machine_0) | 34.00 | 45.33 | [1, 34.00] | 124–153 | 0 | B2 continue |
| 154 | recognition_changed | refused (below_theta) | — | — | — | — | 0 | B2 continue |
| 169 | no_current_task | refused (below_theta) | — | — | — | — | 0 | B3 |
| 245 | recognition_changed | deliver_item(?item=item_5) | 67.05 | 40.27 | [1, 40.27] | 246–284 | 0 | B2 continue |
| 286 | no_current_task | deliver_item(?item=item_5) | 27.93 | 137.27 | [1, 27.93] | 287–310 | 0 | B3 |
| 311 | recognition_changed | refused (below_theta) | — | — | — | — | 0 | B2 continue |
| 341 | recognition_changed | ac_activation(?ac_switch=ac_switch_0) | 26.52 | 82.27 | [1, 26.52] | 342–364 | 0 | B2 continue |
| 365 | recognition_changed | refused (below_theta) | — | — | — | — | 0 | B2 continue |
| 424 | no_current_task | refused (below_theta) | — | — | — | — | — | — (pool empty) |

**s10 prior on**

| tick | trigger | admitted hypothesis / refusal | T_h | realized end | assessed window (clock) | ticks inside | hold | block |
|---|---|---|---|---|---|---|---|---|
| 0 | no_current_task | refused (below_theta) | — | — | — | — | 0 | B3 |
| 24 | recognition_changed | deliver_item(?item=item_2) | 53.02 | 50.81 | [1, 50.81] | 25–73 | 0 | B2 continue |
| 75 | recognition_changed | refused (below_theta) | — | — | — | — | 0 | B3 |
| 123 | recognition_changed | coffee_break(?coffee_machine=coffee_machine_0) | 34.00 | 45.33 | [1, 34.00] | 124–153 | 0 | B2 continue |
| 154 | recognition_changed | refused (below_theta) | — | — | — | — | 0 | B2 continue |
| 169 | no_current_task | refused (below_theta) | — | — | — | — | 0 | B3 |
| 202 | recognition_changed | deliver_item(?item=item_5) | 110.05 | 82.09 | [1, 82.09] | 203–283 | 0 | B2 continue |
| 286 | no_current_task | deliver_item(?item=item_5) | 27.93 | 137.27 | [1, 27.93] | 287–310 | 0 | B3 |
| 311 | recognition_changed | refused (below_theta) | — | — | — | — | 0 | B2 continue |
| 339 | recognition_changed | ac_activation(?ac_switch=ac_switch_0) | 28.52 | 84.27 | [1, 28.52] | 340–364 | 0 | B2 continue |
| 365 | recognition_changed | refused (unknown) | — | — | — | — | 0 | B2 continue |
| 424 | no_current_task | refused (unknown) | — | — | — | — | — | — (pool empty) |

**s30 prior on**

| tick | trigger | admitted hypothesis / refusal | T_h | realized end | assessed window (clock) | ticks inside | hold | block |
|---|---|---|---|---|---|---|---|---|
| 0 | no_current_task | refused (below_theta) | — | — | — | — | 0 | B3 |
| 23 | recognition_changed | deliver_item(?item=item_3) | 52.68 | 59.68 | [1, 52.68] | 24–73 | 7 | B2 continue_hold |
| 74 | recognition_changed | refused (below_theta) | — | — | — | — | 0 | B2 continue |
| 84 | no_current_task | refused (below_theta) | — | — | — | — | 0 | B3 |
| 87 | recognition_changed | deliver_item(?item=item_7) | 34.61 | 74.82 | [1, 34.61] | 88–120 | 0 | B2 continue |
| 121 | recognition_changed | refused (unknown) | — | — | — | — | 0 | B2 continue |
| 163 | no_current_task | refused (unknown) | — | — | — | — | — | — (pool empty) |

## R3. Which window each sub-50 tick falls in

| run | tick | dist (min) | decision in effect | window verdict | robot during the tick |
|---|---|---|---|---|---|
| s10 off | 72 | 44.79 | 29 | inside (τ 43–44) | stands (`move_to` ack; arrived end of 71) |
| s10 off | 73, 74 | 30.87 | 29 | inside (τ 44–46) | stands (release, `place` ack) |
| s10 off | 75, 76 | 30.87, 38.99 | 75 | none (no projection) | stands (completion tick); 76 moves away |
| s10 on | 72, 73 | 44.79, 30.87 | 24 | inside (τ 48–50) | stands |
| s10 on | 74 | 30.87 | 24 | edge: [50, 51] straddles the realized end 50.81 | stands |
| s30 on | 21, 22 | 36.64, 11.03 | 0 | none (no projection) | moves (the known tail, C: s30 21–24) |
| s30 on | 23 | 15.47 (8.47) | 23 | none: [0, 1] is the observation offset, before the human's span | stands (hold, 1st tick) |
| s30 on | 24 | 34.01 (15.47) | 23 | inside (τ 1–2) | stands (hold, 2nd tick) |

`measure.py` (ablation) takes the decision in effect as the record does (last fired trigger at or before the
tick) and reads T_h correctly, but tests one instant, the tick's end k − t + 1 ∈ [1, T_h], instead of the whole
tick, and omits the realized plan's span. It differs from the record at s30 tick 23 (offset, counted inside:
this is the 15.47 cm "min in window") and at s10 on tick 74 (edge, counted inside). Every other tick above is
inside by both rules, so case (1) does not dispose of the rest.

## R4. The in-window ticks: projected against executed

| run | tick | τ | realization's projected distance (min over the tick) | executed (min) | human: projected → actual | robot: projected → actual |
|---|---|---|---|---|---|---|
| s10 off | 72 | 44 | 47.16 | 44.78 | on the projection (0.00) | 3.78 off, standing |
| s10 off | 73, 74 | 45, 46 | 42.89 | 30.88 | walk ends 14.26 cm farther along than projected | 3.78 off, standing |
| s10 on | 72 | 49 | 43.10 | 44.78 | 5.35 off | 3.78 off, standing |
| s10 on | 73 | 50 | 42.81 | 30.88 | walk ends 14.26 cm farther along | 3.78 off, standing |
| s30 on | 24 | 2 | 34.01 (15.47) | 34.01 (15.47) | on the projection (0.00) | on the plan (0.01), holding |

- The decision's own realization projected these ticks below min_separation: the robot's last moving segment ends
  at τ 42.81 (s10 off) / 46.81 (s10 on), 67.2 / 80.5 cm from the projected human (its closest approach while
  moving); it then stands at the table (place) while the projected human walks in to 42.9 cm. Stationary robot segments have no violating shift interval (F1), so δ = 0
  is the correct realization, not a missed check. In s30 the 15.47 cm is the human crossing the robot standing
  in the decided 7-tick hold, exactly as projected.
- No hypothesis change without a re-decision: the belief stays on the admitted hypothesis (item_2, 0.99; item_3)
  through every in-window tick. Projection and execution part in two small places, neither of which moves the
  robot: the human's walk ends 14.26 cm farther along than its projection (s10, tick 73; 3.5 cm at the station,
  s10 on, tick 29: the stop-point error within the arrival radius, TODO-89), and the robot stops 3.78 cm from its projected table point (arrival quantisation). In s10 on
  the robot also runs one tick (20.0 cm) behind its projection from tick 24 (the `pick_up` acknowledgement owed at
  the continue, TODO-77's hold-0 residual).
- No robot step inside any window comes within 50 cm: under F1 (`evaluate.py` labels) every in-window sub-50 tick
  is "stand", none "viol".

## Verdict

Evaluation rule (Hadi's ruling on this check): a defect is a robot STEP (a moving tick) inside an assessed window that
ends below min_separation; standing ticks are judged by whether realization projected them (F1: the robot answers for
its own motion only).

- s10 prior off: neither (1) nor (2) as posed: ticks 72–74 are in decision 29's window, and they are not a hole
  but F1 "stand" ticks that realization itself projected below 50 cm; the ablation counted distance inside a
  window, not robot responsibility.
- s10 prior on: the same, under decision 24 (ticks 72–73; 74 is on the window's edge).
- s30 prior on: (1) for tick 23, which falls in no window (the observation offset); tick 24 is inside and, as
  in s10, a stand that the decision projected exactly.

## Run (repo root)

    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/todo90_b2a_window/capture.py <out>.json \
      --domain kitting --layout env_layout1 --scenario scenario_10 --steps 450 --strategy single_task \
      --gate_strategy b2a --cost_strategy realized --separation_stop false --assignment_prior false
    python analysis/todo90_b2a_window/tables.py logs/run_<ts>.log <out>.json
