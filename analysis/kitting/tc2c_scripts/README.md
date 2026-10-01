# analysis/tc2c_scripts — T-C2c: the first two scripted scenarios

> Superseding note (T-L stage 3, 26 Sept 2026): the layout and scenario ids here are the old ones; `docs/rename_table.md` maps them to the serial ids. The scripts and records stay frozen at their commit.

> Superseding note (24 Sept 2026, the terminology ruling; `docs/glossary.md` §7, `docs/terminology_revision.md`): "a human who departs from the model mid-task (A)" → a human whose work order is interrupted (a deviation, label A) by a foreseeable task, which is modelled (label B): scenario_11's `coffee_break` has a hypothesis. "recognised again from scratch" → the delivery's hypothesis clears θ again (ROBOT).

Two literal scenarios on the human action script (T-C2a) and the action-level human (T-C2b): a human who departs
from the model mid-task (A), and a human who stays where the robot must go (B). Observed, not judged: one run each,
nothing measured against a criterion. Fixtures, not baselines: logs local (`logs/`), no md5s. Code at 679fcb0 plus
the scenarios (`domains/kitting/scenarios.py`, `scenario_11`, `scenario_01`).

## Run (repo root)

    PY=~/python-envs/teamrob-sp4-env/bin/python
    PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --domain kitting --layout env_layout1 --scenario scenario_11 --steps 500 \
        --assignment_prior true --strategy single_task --cost_strategy realized --gate_strategy none --separation_stop false
    PYTHONHASHSEED=0 $PY mesa_sim/run_mesa.py --domain kitting --layout env_layout0 --scenario scenario_01 --steps 200 \
        --assignment_prior true --strategy single_task --cost_strategy realized --gate_strategy none --separation_stop false
    # the same with --separation_stop true

## A — interrupted delivery (scenario_11, env_layout1)

env_layout0 has no coffee machine, so A is on s10's layout. Script: `interrupt(deliver(item_2), after="pick_up",
with_=[coffee_break(coffee_machine_0)])`, then `deliver(item_5)`. The second delivery is not in the prompt's
script: the prompt keeps s10's assigned tasks (item_2, item_5), and the work-order check requires every assigned
task in the script. Robot as s10 (item_4, item_1, item_7, item_6).

Resolved script and ticks: move_to item_2 (0), pick_up (31), move_to coffee_machine_0 carrying item_2 (33), wait_at
PT60S (46–75), move_to kitting_table_0 (77), place (124), then item_5 (126–249).

- **Belief.** `deliver_item(item_2)` leads from tick 4 and clears θ at 24 (0.774). On the walk away from the table
  with the item (33–46) it falls 0.98 → 0.55; `coffee_break(coffee_machine_0)` rises 0.001 → 0.345, `unknown`
  0.011 → 0.088. Through the 30-tick wait the distribution is frozen (0.550 / 0.345 / 0.088): standing produces no
  evidence (TODO-85). `deliver_item(item_2)` is NOT retracted; `coffee_break` never leads; `unknown` leads at no tick.
  At 75 `waited(human_0, coffee_machine_0)` pins `coffee_break` and ends the episode (`[IR-boundary]`): the belief is
  reset to the prior over ac_activation, item_2, item_5 and `unknown` (0.248 each). The interrupted delivery is then
  recognised again from scratch (`deliver_item(item_2)` clears θ at 100, 0.757), pinned at 124; item_5 clears θ at
  156 (0.755), pinned at 249. After 249 `ac_activation` leads at 0.495, below θ, to the end.
- **recognition_changed**: 24 (first clears the gate, item_2), 75 (boundary: the belief no longer points at item_2,
  below θ), 100 (clears the gate on item_2 again), 124 (boundary), 156 (clears the gate on item_5), 249 (boundary).
  No trigger during the walk away or the wait.
- **Robot.** item_7 (0, continued at 24; released 73), item_6 (from 75; released 166), item_1 (169; released 283),
  item_4 (286; released 421). Projections admitted at 24, 100, 156 and 169 (T_h 52.0, 25.5, 93.7, 80.7); no hold
  anywhere.
- **[sep] minimum**: 236.6 cm (tick 99) while the human works; 6.97 cm at 419, after the human's script ended
  (249): the human stands at the table, `ac_activation` 0.495 is below θ, no projection, and the robot's last
  delivery walks up to it (stop off).
- **Completion** (world fact): 422.

## B — declared stay (scenario_01, env_layout0)

Script: `deliver(item_3)`, then `Stay(40)`; the human's assigned tasks: item_3 (the prompt names none). Every item
of s00's robot pool goes to kitting_table_0, the only table; item_4 is the one whose carry reaches the table while
the human stands there (release at 83; item_6 and item_7 release at 46 and 31, before the human arrives). Robot: one
task, item_4, from s00's start.

Human: move_to item_3 (0), pick_up (41), move_to kitting_table_0 (43), place (78), `Stay(40)` from 80 to 119. The
script then ends, and an empty list stands: the human stays at the table to the end of the run.

- **Belief.** `deliver_item(item_3)` clears θ at 19 (0.752). The release at 78 pins it and ends the episode; the
  prior now has no hypothesis left (the human's pool is empty), so `unknown` holds 0.995 to the end.
- **recognition_changed**: 19 (first clears the gate), 78 (boundary).
- **Projection.** At 19: built, T_h = 59.48 on the decision's clock (tick ≈ 78.5; the human released at 78). At the
  release (78) and after: none (`none(unknown)`), T_h = None. The stay is not projected (TODO-85).
- **Hold.** One, decided at 19 against the projected delivery: 5 ticks at (-48.8, -31.7), on the robot's walk to
  item_4, where it crosses the human's walk to item_3 near the centre (the human at (33.0, -43.9)); executed
  19–23. Nothing at the table: none after the release.

Stop off:

- The robot comes below `min_separation` (50 cm) while the human stands: 29.3 cm at 80, 14.8 cm from 81; it
  releases at 83, 14.8 cm from the human, and stands there. [sep] minimum 14.8 cm. Completion (world fact): 84.

Stop on:

- The first step is refused at 79 (dist 67.4, step minimum 47.97), `window=outside(no_projection)`, decision 78,
  T_h None; then every tick to the end, 121 refusals. The robot stands at (31.8, 278.6), 67.4 cm from the human,
  carrying item_4. The human never leaves (the script ended), so the robot never delivers: no completion in 200
  steps. [sep] minimum 59.5 cm (tick 22).

Next to TODO-85's expectation ("expected today: frozen belief, no trigger, a hold placed for a moving human, the
conflict later than realized, refused by the stop inside the assessed window"): that expectation is for a stay
MID-CARRY. B's stay follows a completed delivery, and differs on every point: the belief is not frozen but
reset (the boundary at the release), a trigger fires (78), no hold is placed after the release (no projection:
`unknown`), and the refusals are OUTSIDE the assessed window (`outside(no_projection)`). The mid-carry case is A's
wait: there the belief is frozen and no trigger fires, as expected; no hold arises in A because the robot's
routes do not meet the waiting human.
B with the stop on is TODO-80's terminal stay at the table with one task left: under the script's end, the stay
does not end.
