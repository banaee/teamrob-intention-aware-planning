# The IRB's instrument (shared code)

The code of the IRB (design_decisions.md, "The intention-recognition test-bed (IRB)"; glossary §8, IRB), shared by the domains since the
sort (1 October 2026). What it runs, what it derives from which record, and how it compares are stated in kitting's
record, `analysis/kitting/irb/README.md` (the pipeline, the columns, rules 1 to 23 with their sources, the
readings R1 to R4); a domain's set, its expectations and its report live in `analysis/<domain>/irb/`, its run
files in `configs/<domain>/irb/`.

```bash
analysis/instruments/irb/run.sh <domain>                         # every configs/<domain>/irb/*.yaml
analysis/instruments/irb/run.sh <domain> [-o <out root>] [run files]
```

Outputs per scenario in `<out root>/<scenario>/` (default `analysis/<domain>/irb/`), the run's log and `.rec` in
`<out root>/runs/` (git-ignored). Run from the repo root; PYTHONHASHSEED=0 is set by the script.

## The preparation for dock_loading (the sort, part 2; 1 October 2026)

Made by derivation from the records before any dock_loading run; kitting's seventeen IR runs and the MPB's sixteen under
each strategy, rerun through the changed code, are byte-identical in every output (new: `separation.md`).

- **The human's sequence: the executor's own selection rule** (design_decisions.md, "T-G", STAGE 1 PLAN APPROVED, the
  requirement on the instruments; the plan's question 3). `trajectory.py` drives a `StackMachine` built on the whole
  script, repeatable entries and closing part included, as `HumanAgent._step_stack` drives it, against the world the
  environment's builder makes from the body state mirrored into the model. Under R1 the load-time replay skips the
  standby entry, so it can no longer be the source. With the robot idle, a Wait with nothing in hand lasts to the
  run's end; the run length (last acknowledgement + 1 + 30) is read there. Check: kitting's 17 IR and 16 MPB
  trajectories byte-identical to the replay-derived ones.
- **The body's new rules**: TOUCH (a scan) is one tick with no physical change; when an action's last microaction has
  run the model applies its declared state changes (`SimModel.apply_state_changes`, T-G A5); a declared state is
  among the row's facts and can be an action's completion (`is_scanned`).
- **The domain** from the run file (`domains/<domain>/registry.py`) in every script.

| # | rule (new) | source |
|---|---|---|
| 24 | The agent's area: the world of a tick carries `in_area(human, area)` from the layout's declared areas, read as the environment reads them, by the one definition `shared.types.area_fact` (no kitting method reads it) | T-G A9, R2; glossary §10 |
| 25 | Liveness by applicability: a key whose task has no applicable method (decomposition fails) leaves H, its phase state dropped; pinned at the floor on output (as every non-live key); when applicable again, retired if its terminal fact holds, else it re-enters at 1/\|H\| as rule 21; a retired key that becomes inapplicable stays retired | T-G A4; HB §1.1, its A4 amendment |
| 26 | The boundary, also through each terminal action's preconditions and completion (the last action of some method of a task schema of the robot's task model): its preconditions held for the observed human on the previous tick and, under that binding, a grounding of its completion holds now that did not then. It adds `scan_it` (at(h, x) then, is_scanned(x) newly now); on kitting it adds no tick to rule 5b | DL L1 as amended, its as-built reading |
| 27 | The completion signal of `scan_it`: TOUCH is its declared microaction list, so rule 7 applies to it unchanged (HIT if is_scanned holds, else FALSE_ALARM); s_exp of `scan_it` is the entry latency + the default action cost 1 (rule 11), e = 0 (no progress evaluator, rule 9) | HB §1.4 (the declared vocabulary), reading R1; DD E9 |

The log reader (`analysis/instruments/common/tdlib.py`): the `[IR-inapplicable]` lines; the live set read from the log
is the support minus the keys retired and the keys out for want of an applicable method; the pool read by each task's
first binding. `summary.py` lists the entries still open at the run's end for a script that depends on the robot.

**The separation counts** (`analysis/instruments/common/separation.py`, `separation.md` per scenario; the plan's
question 5): the ticks whose continuous [sep] minimum lies below min_separation, by F1's execution class
(`sep_classes.rule`): a moving robot violating, a moving robot receding, a standing robot with the human passing (it
moved on the tick) or standing beside it (it did not).

**The baseline table** (`baseline.py <set dir>`, reporting only, 2 October 2026): from a set's existing outputs, per true
stretch (summary.py's definition) its length, the live hypotheses at its first tick and the ticks to the first tick
with the true hypothesis's belief at or above θ, or "never"; one table per room and the counts.
