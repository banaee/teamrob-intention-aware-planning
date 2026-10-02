# Record of planning and building: T-C, the human action script

Moved verbatim from `docs/design_decisions.md` on 2 October 2026 (Hadi's ruling of that day: one record file per task;
the conceptual design stays in design_decisions.md). Each block is headed by the title of the entry it comes from
and its id; in design_decisions.md an index line with the same id stands where the block was.

**The human action script (T-C1, decided)** — RECORD [T-C/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
RECORDED FOR T-D, not designed here: an observed history of the human's tasks in the robot's mind (completed,
dropped, `unknown` episodes), for evaluation (TODO-92). The robot taking over an abandoned task is TODO-15.
Not decided in T-C1 and left where they are: TODO-85 (a stationary human; half (b), the robot's action under
`unknown`, with T-D) and TODO-88 (its own item).

AS BUILT (T-C2b): SEQUENTIAL EXPANSION. `resolve_script()` resolves the script's elements in order, each
against the initial world advanced by every element before it: the primitives grounded and handed to
`shared.projection.successor_state()`, the successor state of T-B2a, made a module function so that the
projection of an ordering and the script share one derivation (no second successor state); the agent stands at
the target of its last walk; a `Stay` changes nothing. A deviation's injected content is resolved against the
state its task's expansion leaves at the anchor (after the kept part, for `abandon`); anchors are resolved
against the task's own expansion as before. Check: `abandon(deliver(item_3), after="pick_up",
then=[deliver(item_5)])` expands the second delivery with `deliver_with_return` (item_3 to its shelf first);
with `before="pick_up"` it expands with `deliver_default`.
AS BUILT (T-C2b): THE ACTION-LEVEL HUMAN EXECUTOR. `HumanAgent` holds the resolved list (`load_script()`, by the
loader); each `ScriptAction` is grounded when reached (`ground()`) and handed to the shared `Executor` as a
one-action plan; the executor is handed no plan before the next one, so it owes no per-task completion tick; the
next primitive's first microaction runs on the tick after the last one's acknowledgement. `Stay(n)` stands n
ticks, `Stay()` to the end, an empty list stands. `current_task` stays `None`. The C2a compatibility path is
removed. The shared `Executor` is unchanged: its `_on_task_complete()` is no longer reached by the human. The
human's body reports 0 for the per-task tick to the projector (`observed_task_completion_latency`,
`HUMAN_TASK_COMPLETION_LATENCY` in `mesa_sim/sim_agents.py`); the robot's candidates keep its own. CONSEQUENCE,
measured: the human projection ends one tick earlier, so a decision may move before any human task completes
(s20 `single_task`: the hold at step 11 is 7 ticks, was 8); with the human's latency set back to 1 the run is
identical up to the first dropped tick. RULING (Hadi, T-C2b): the decision working, not a defect — the human's
projection without the per-task tick ends one tick earlier and the human arrives one tick earlier, so the hold
that clears it is one tick shorter. Holds moved in the fixtures (prior on): s20 `single_task` 8 -> 7, s70 (both
strategies) 1 -> none, s83 `full_reorder` a new hold of 2 at step 190. Nothing in `shared/` reads another
agent's `current_task` (checked by grep: `WorldState.agent_states` is read nowhere in `shared/`), so the
human's `current_task = None` reaches no decision. Fixture results: every human line identical up to the dropped per-task
tick in all ten runs (s00, s20, s70, s80, s83; `single_task`, `full_reorder`; prior on).

AS BUILT (T-C2c): SCENARIO-AUTHORING CONVENTION (Hadi, cchat, 23 September 2026). A human's script ends with the
human leaving the workspace (`MoveTo("door")` or a corner, then the empty list's stand), unless the scenario is
about the terminal stand at a table (TODO-80's blocked case, stated in the scenario's description). Reason: a human
standing at a table after its script deadlocks the robot with the stop on; that is the scenario's artefact, not a
design result, and a stay that ends is waited out (scenario_94). The 22 play scripts and the two C2c fixtures
(scenario_11, scenario_01) are not edited: they are examples and TODO-80 fixtures. New scenarios follow the
convention.
SUPERSEDED IN PART (Track 2.5, ruled by Hadi 28 Sept 2026): "New scenarios follow the convention" is extended to the
existing regression fixtures where their terminal stand is not part of the fixture's purpose (docs/assumptions.md
1.1); the six scripts behind the occupied-target logs (scenario_s01_01, s01_06, s02_01, s03_01, s04_01, s06_03) end
with `go_to("corner_SE")` since 52295f7. The play scripts and the C2c fixtures are unchanged.

T-C2, THE BUILD: C2a the script layer (primitives, `expand`, the vocabulary, landmarks, the provenance check);
C2b the human executor, action-level (both built). Fixtures s00, s20, s70, s80, s83, prior on; the check is identity up to
the dropped per-task completion tick; the baselines are regenerated once. Then two literal scenarios, an
interrupt and a stay, one run each, observed and not judged. From here debugging runs use prior on only; off /
on returns for the paper.
