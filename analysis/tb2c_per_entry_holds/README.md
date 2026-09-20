# T-B2c — one minimal-shift search per entry: the checks

`check.py` regenerates `checks.md` (about 25 s):

    PYTHONHASHSEED=0 ~/python-envs/teamrob-sp4-env/bin/python analysis/tb2c_per_entry_holds/check.py \
        > analysis/tb2c_per_entry_holds/checks.md

What it checks, on every ordering of the pool at every B3 call of scenario_81 (both priors; the calls of the
`full_reorder` run and of the `single_task` run), is stated in its docstring: dominance of one search per entry
over one common shift (the common-shift realizer exists in the script only), the hold before the first entry
against the head realized alone, validity by sampling (F1's method) and minimality, and a synthetic two-entry
case. The decision and the reading of the results: `docs/design_decisions.md`, "One hold per entry".
`check.py` ends with a verdict and exits non-zero on a defect: a per-entry cost above the common-shift cost,
a first hold that is not the head's realized alone, a violating sample in a winning ordering or in an ordering
with a later hold, or an empty winner table (check 9 not produced).

## A finding for T-B3

From these checks and the T-B2c runs: on every current fixture NO WINNING ORDERING UNDER `full_reorder` CARRIES A HOLD (scenario_80, scenario_81,
scenario_00, both priors; every hold sent is 0 and every `[meta-win]` line reads `holds=0,...`), so T-B2c
changes NOTHING EXECUTED against T-B2b. scenario_81 does not exercise realized cost under `full_reorder`: its
conflict belongs to `single_task`'s course (heads 6, 1, 7, 4: the hold before item_1, 3 ticks at step 40), and
the course `full_reorder` chooses (7, 4, 6, 1) never meets the human (0 of the 206 orderings priced on that
course carry any hold; the 12 that do, 8 of them before a later entry, are all priced on `single_task`'s
course). Its saving (completion 224 against 268, world fact) therefore MIXES TWO CAUSES, the order of the
tasks and not meeting the human, and cannot be attributed to either. A FIXTURE FOR T-B3b MUST PUT A CONFLICT
INTO THE ORDERINGS `full_reorder` WOULD CHOOSE. Hadi designs it; no scenario, designation or constant is
adjusted to make an effect appear.
Recorded in `docs/TODOS_AND_DEFERRED.md`, TODO-47 (f-designations).

## Numbers here against the record (T-B Q7, de70e98)

`checks.md` and the counts above were produced BEFORE T-B Q7, which made the body spend the completion ticks a
reload used to cancel (`docs/design_decisions.md`, "A reload never cancels a completion tick the body states").
FOR A READER COMPARING WITH THE RECORD: every completion tick recorded before that fix IS ONE TICK SHORTER PER
ROBOT DELIVERY than the behaviour from here on, less where a decided hold carried the tick — the two completion
ticks and the hold in the finding above are given at T-B Q7 (220 → 224, 265 → 268, the 4-tick hold at step 39 →
3 ticks at step 40). The finding itself is unchanged and re-checked at de70e98: under `full_reorder` no winning
ordering on scenario_80 or scenario_81 carries a hold, at either prior, and the head order is still 7, 4, 6, 1.
The per-ordering counts (402 orderings, the 12 with a hold) are the pre-fix run's and are not re-derived; the
argument they support is about which course meets the human, which the fix does not touch.

No baselines live here.

