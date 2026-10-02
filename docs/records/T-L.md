# Record of planning and building: T-L, layouts, setups and scenarios

Moved verbatim from `docs/design_decisions.md` on 2 October 2026 (Hadi's ruling of that day: one record file per task;
the conceptual design stays in design_decisions.md). Each block is headed by the title of the entry it comes from
and its id; in design_decisions.md an index line with the same id stands where the block was.

**Layouts, setups and scenarios: the three artefacts of a run (T-L, 26 September 2026)** — RECORD [T-L/1], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
   - THE STATED TABLE (ruling b): the stated table stays explicit in a scenario's assigned tasks and script, validated
     against the setup's designations as today. A readability choice: the HTN model does not require it ("T-H: the
     human behaviour model", item 5; the T-B1a precedence rule). Consequence: a scenario fits a setup whose
     designations agree with its stated tables, and that is what the check says.

**Layouts, setups and scenarios: the three artefacts of a run (T-L, 26 September 2026)** — RECORD [T-L/2], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
4. NAMING: descriptive ids, nothing encoded. One id per artefact, snake_case, unique within the domain and artefact
   kind; the Python variable of a `ScenarioConfig` equals its id; the `name` field is dropped; `description` holds the
   purpose. The same rule for layout and setup ids.
   FORM AMENDED (Hadi, 26 September 2026; the principle stands — the variable equals the id, `name` dropped,
   `description` holds the purpose, nothing about the script's content in an id): serial ids.
   - Layout ids `env_layout_KK`; setup ids `env_setup_NN`; scenario ids `scenario_sNN_MM`, NN the scenario's setup
     serial and MM a counter per setup. KK, NN, MM are independent serials with no meaning beyond order of writing.
     Example: `env_layout_07`, `env_setup_04`, `scenario_s04_01` (today's env_layout7, env_setup7, scenario_70);
     scenario_71 becomes `scenario_s04_02`.
     NOTE (Hadi, 26 September 2026, the stage-3 task): the example's serials were illustrative. The built numbering is
     the rule's: stage 2 numbered env_setup7 as `env_setup_05`, so scenario_70 is `scenario_s05_01` and scenario_71
     `scenario_s05_02`; env_layout7 is `env_layout_07`. `docs/rename_table.md` holds every id.
   - The setup serial in a scenario id repeats the validated `setup` field. The code does not check that they agree
     (a check that reads an id out of an id string is string matching, which BUILD DISCIPLINE forbids); the agreement
     is an authoring convention stated in CLAUDE.md, and an author who moves a scenario to another setup renames it.
   - A layout's serial is never in a scenario id (a scenario has one or more reference layouts).
   - Stage 3 merges the identical setups (env_setup0 = env_setup3, env_setup2 = env_setup5) before numbering, so
     numbering is done once. SUPERSEDED (Hadi, 26 Sept 2026, the stage-2 task): the merge and the setup ids
     `env_setup_NN` are stage 2's, because the module division (one module per setup, `scenarios_sNN.py`) keys on
     the setup serial and a stage-3 rename would touch every module twice; scenario and layout ids stay old until
     stage 3.
   - Baseline file names: `<layout id>_<scenario id>_<run options>.log`, as ruling 6 states.

5. REGISTRATION BY DISCOVERY: a `ScenarioConfig` is registered at import of the domain package (a decorator or a module
   scan; ccode chooses in stage 2), with no side effect beyond adding to a dict; a duplicate id is an error. Layouts
   and setups are registered by their files. BUILT (stage 2): a module scan (`domains/discovery.py`) — a decorator
   can be forgotten on a new scenario, which recreates the omission this ruling closes; registration runs at import
   of `domains.<domain>.registry`, the one entry every reader uses (importing the bare domain package registers
   nothing). Scenarios stay hand-written literals; T-B1b's ruling (TODO-47 (a))
   reversed a generator that produced fixtures, not a mechanism that lists them. That distinction is recorded under
   TODO-47 (a).

6. BASELINES ARE KEYED BY THE RUN. File names carry the layout id and the scenario id plus the run options already
   present (prior, strategy); the setup is omitted from names because ruling 3 gives a scenario exactly one setup.
   THE TRIPLE LINE: the `[run_mesa]` start line, where the layout and scenario ids are printed today, prints all three
   ids; stage 1 adds the setup to it. The four maintained sets are regenerated under the new names in stage 3, `.rec`
   streams byte-identical, a new md5 section in each README. Frozen records are not touched; one file
   `docs/rename_table.md` maps every old layout and scenario id to its new id, and says in one line that the frozen
   analysis scripts stay frozen at their commit; each frozen README gets one superseding line pointing to it.

**Layouts, setups and scenarios: the three artefacts of a run (T-L, 26 September 2026)** — RECORD [T-L/3], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
8. SEQUENCING: T-L precedes T-D. kitting and dock_loading migrate together (this task and its stages may touch
   `domains/dock_loading/`; it must still import). dock_loading's two scenarios fail at load before T-L (TODO-104);
   TODO-104 stands and T-L must not worsen it. ros_sim stays parked: TODO-111, with TODO-108, records that its layout
   readers move to the same sources when it resumes. The stages after this record task, each its own ccode task, each
   ending in the acceptance check below:
   - stage 1: types (`ScenarioConfig` gains `setup` and `reference_layouts`, loses `name`), loader, resolver,
     validator; every registered layout split into a layout file and a setup file with the object ids unchanged and the
     dead spawn entries deleted (`env_layout99.json` stays an unregistered file); scenarios unchanged in content and
     id; the tests' helpers move with the registry shape; the setup id added to the `[run_mesa]` line; the docs pass
     on the lines the survey listed (roadmap, T-L, stage 1).
   - stage 2: the scenarios package (one module per theme) and registration by discovery; `list_scenarios` and the
     tests' helpers on the declared pairs. AMENDED (Hadi, 26 Sept 2026, the stage-2 task): one module per SETUP,
     `scenarios_sNN.py`, and the setups finished here — the merge and the final ids `env_setup_NN` — because the
     module division keys on the setup serial.
   - stage 3: the rename to the serial ids (ruling 4 as amended), the identical setups merged before numbering
     [DONE IN STAGE 2, with the setup ids],
     `docs/rename_table.md`, the four maintained sets regenerated under the new names, sweep scripts and READMEs.
     BUILT (26 September 2026): the layouts and scenarios of both domains under their serial ids, `docs/rename_table.md`,
     the four maintained sets regenerated as `<layout id>_<scenario id>_<run options>.log` (tb1a gained its own
     `sweep.sh`; tb3 keeps all 20 runs), differing from the stage-2 logs in the `[run_mesa]` line alone, every `.rec`
     byte-identical; one superseding line in each frozen analysis README pointing to the rename table.
   - stage 4: the run file and the override mechanism, with the viewer reading it.
     BUILT (26 September 2026): `--run <path>` (replacing `--experiment`, no alias) and `--override
     <path>=<value>` (repeatable) in `mesa_sim/run_mesa.py`; a path is `<artefact>.<id>.<fact>`, the same in the run
     file's flat `overrides:` block (path: value) and on the command line, read once at the input boundary into one of
     three typed classes (`mesa_sim/overrides.py`: `StartPositionOverride` for `scenario.<agent>.start_position`,
     `FixedPositionOverride` for `layout.<object>.position`, `HomeContainerOverride` for
     `setup.<object>.initial_container`, the file keys), every other path refused with the path named; the value typed
     by the fact (two numbers, an id); a command-line override replaces the file's for the same path. `SimModel`
     applies them to the artefacts as read, before `_init_objects` and `_spawn_agents` (the registered scenario is
     copied, never changed); an unknown agent or object, or a layout position for a setup's object, is an error naming
     the path; bounds, container existence, destinations and the replay are the existing checks. Each override is
     printed after the start line as `[run_mesa] override <path>=<value>`, sorted by path, in the `--override` form.
     The viewer's `Page` reads the run file it is started from on every reload and shows the triple and the overrides
     (`mesa_sim/viz/run_file_panel.py`); its form, limited to the three kinds, builds the run first, writes the file's
     block only if it loads (a path the command line gives is refused: its value, not the file's, is run) (round-trip through `ruamel.yaml`, comments kept, a new dependency) and reloads. A run with
     no overrides is byte-identical to stage 3, and the four maintained sweeps are unchanged. NOT COVERED, as built: a
     fixed object moved out of the space or onto another object is not checked (ruling 7: the checks of any run); a
     moved fixed object keeps its declared `zone`, which nothing in the run reads; a duplicate path in the yaml block
     is PyYAML's last-one-wins; the viewer prints no `[run_mesa]` line (as before), so an override applied in the
     viewer is not in its log; a viewer started on `configs/experiment.yaml` writes its overrides there, where every
     run that takes the default file (the sweeps included) picks them up.

ACCEPTANCE, at every stage: the four maintained sweeps (tb1a, tb1b, tb1c, tb3) are run from scratch and diffed against
the previous stage's logs, with no difference outside the lines the stage names (the triple line, the ids); AND pytest
is green. Nothing is aligned to older analyses.

**Layouts, setups and scenarios: the three artefacts of a run (T-L, 26 September 2026)** — RECORD [T-L/4], moved verbatim from docs/design_decisions.md (2 October 2026); the conceptual part stays there under this title.
MEASURED AT RECORD TIME, CLOSED BY RULING a (read-only, the registered scenarios against their registered layouts'
fixed objects, a footprint being the object's `size` centred on its `position`): an object check would have refused
scenario_40, scenario_41 and scenario_42 (robot_0 at (-950, -550), the centre of the landmark `corner_SW`), and left
undecided the starts on the edge of `kitting_table_0` (scenario_40 to 42's human_0, scenario_70 to 73's robot_0).
Every registered start lies inside its space's bounds.
