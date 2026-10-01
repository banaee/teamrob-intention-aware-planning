"""
mesa_sim/sim_model.py

PURPOSE:
    Mesa embodiment of the factory environment.
    Loads a layout JSON (the room) and a setup JSON (the shift, T-L), receives
    a ScenarioConfig, builds the physical space, spawns agents, and drives the
    simulation step loop.

WHAT THIS MODULE DOES:
    - Reads the layout JSON (space, areas, fixed objects) and the setup JSON
      (movable objects with their home containers and destinations, and the
      object states that hold at the start)
    - Holds the true state facts the domain declares (T-G A5) and changes them
      when an action that declares one has run (apply_state_changes)
    - Receives a ScenarioConfig (Python object) — no YAML scenario parsing
    - Creates Mesa ContinuousSpace with center-origin (0,0)
    - Instantiates env objects as plain dataclasses (not Mesa agents)
    - Spawns HumanAgent and RobotAgent via sim_agents.py
    - Runs schedule.step() each tick

WHAT THIS MODULE DOES NOT DO:
    - No WorldStateManager — ground truth lives in env_objects
    - No IR, no planning, no task assignment logic
    - No YAML parsing for scenarios or action schema definitions

COORDINATE SYSTEM:
    Matches the layout JSON exactly: origin (0,0) at center of room.
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Set, Tuple

from shared.knowledge import StateDeclaration, Tree, TaskModel
from shared.planner import AdaptivePlanner
from shared.recognizer import build_hypothesis_space
from shared.types import (
    Area, Const, GroundedAction, Predicate, ScenarioConfig, Start, TaskInstance, TaskSchema, check_task_bindings,
    check_task_destinations, destination_derivations, task_instance_key,
)
from world.human_executor import check_script
from world.record import ClosingRef, OrdinaryRef, RepeatableRef, StillOpen
from world.composition import scenario_composition
from world.queries import ObservingRobot, coverage
# from domains.kitting.registry import register_kitting_domain
# from domains.dock_loading.registry import register_dock_loading_domain


from mesa_sim.mesa_fork import model, space, time, datacollection
from mesa_sim.sim_agents import HumanAgent, RobotAgent
from mesa_sim.world_state_builder import build_world_state
from mesa_sim.action_decomposer import _parse_duration_to_steps, _get_step_size, walk_positions
from mesa_sim.overrides import Override, apply_overrides

import logging 
logger = logging.getLogger(__name__)

# =============================================================================
# Environment object dataclass
# EnvObject and PortItemObject merged into one class called SimObject
# TODO: move to shared/types.py if ROS later use it
# =============================================================================

@dataclass
class SimObject:
    obj_id: str
    type: str                          # enumeration category — "item", "shelf", "gate", etc.
    position: Tuple[float, float]
    size: Tuple[float, float]
    subtype: Optional[str] = None      # domain-specific classification:
                                        # kitting: "part_A", "part_D", ...
                                        # dock loading: "frozen", "dry"

    held_by: Optional[str] = None
    at_location: Optional[str] = None
    is_portable: bool = False   # set once at load time — True if loaded via
                                 # "initial_container" (items/pallets); never
                                 # mutated afterward. Distinct from at_location/
                                 # held_by, which change during carrying.
    home_container: Optional[str] = None  # set once at load time from
                                 # "initial_container" — the item's origin shelf/bay.
                                 # None for non-portable objects. Never mutated
                                 # afterward, unlike at_location/held_by.
    destination: Optional[str] = None     # set once at load time from "destination"
                                 # — where the object is to go (kitting: its
                                 # designated table), a fact of the station.
                                 # Required for the types the domain resolves
                                 # through "destination_of"; never mutated.
                                 
# =============================================================================
# SimModel
# =============================================================================

class SimModel(model.Model):

    def __init__(self,
                 scenario: ScenarioConfig,
                 register_fn,
                 task_model_schemas: Sequence[TaskSchema],
                 layout_path: str,
                 setup_path: str,
                 seed=None,
                 assignment_prior: bool = False,
                 strategy: str = "single_task",
                 gate_strategy: str = "none",
                 cost_strategy: str = "realized",
                 separation_stop: bool = False,
                 test_level: float = 0.05,
                 overrides: Sequence[Override] = (),
                 state_declarations: Sequence[StateDeclaration] = ()):
        super().__init__()

        # Evaluation switch: give each robot the observed human's assigned_tasks
        # as a persistent IR prior. Off = the robot knows no assigned tasks of it.
        self.assignment_prior = assignment_prior
        # MetaPlanner B3 strategy for every robot ("single_task" | "full_reorder");
        # a run option, not a scenario fact (T-B2d).
        self.strategy = strategy
        # MetaPlanner B2 strategy for every robot ("none" | "b2a" | "b2b"); a run
        # option, not a scenario fact.
        self.gate_strategy = gate_strategy
        # MetaPlanner B3 cost strategy for every robot ("realized" | "plain");
        # likewise a run option (T10).
        self.cost_strategy = cost_strategy
        # Execution-time separation stop for every robot (C, TODO-73); a run
        # option, off by default.
        self.separation_stop = separation_stop
        # The recognizer's adequacy test level alpha for every robot (T-D E5); a
        # run option, 0.05 by convention, never chosen from a scenario.
        self.test_level = test_level

        # ------------------------------------------------------------------
        # Load the layout (the room) and the setup (the shift) — T-L, stage 1
        # ------------------------------------------------------------------
        with open(layout_path, "r") as f:
            env_layout = json.load(f)
        with open(setup_path, "r") as f:
            env_setup = json.load(f)
        # The run file's overrides (T-L stage 4, ruling 7): applied to the
        # artefacts as read, before anything below validates or builds them.
        scenario = apply_overrides(overrides, scenario, env_layout, env_setup, layout_path, setup_path)

        # ------------------------------------------------------------------
        # Space
        # ------------------------------------------------------------------
        space_config = env_layout["space"]
        env_width = space_config["width"]
        env_height = space_config["height"]
        self.space = space.ContinuousSpace(
            x_min=-env_width / 2,
            x_max=env_width / 2,
            y_min=-env_height / 2,
            y_max=env_height / 2,
            torus=False,
        )
        self.env_display_name = space_config.get("name", "TeamRob Simulation")
        

        # ------------------------------------------------------------------
        # Scheduler
        # ------------------------------------------------------------------
        self.schedule = time.BaseScheduler(self)

        # ------------------------------------------------------------------
        # The declared areas (A9), in declaration order: the boundary rule
        # reads the order (shared/types.area_at)
        # ------------------------------------------------------------------
        self.areas: Tuple[Area, ...] = tuple(
            Area(id=a["id"], x_min=a["bounds"]["x_min"], x_max=a["bounds"]["x_max"],
                 y_min=a["bounds"]["y_min"], y_max=a["bounds"]["y_max"])
            for a in env_layout.get("areas", [])
        )

        # ------------------------------------------------------------------
        # The two knowledge objects (T-H): the world's tree, loaded once, which
        # the human's script uses; one task model per robot, built from it in
        # _spawn_agents() from the schemas the domain declares for a robot.
        # ------------------------------------------------------------------
        self.tree: Tree = register_fn()
        self._task_model_schemas = list(task_model_schemas)


        # ------------------------------------------------------------------
        # Environment objects registry — unified, single dict
        # ------------------------------------------------------------------
        self.objects: Dict[str, SimObject] = {}
        self._objects_by_type: Dict[str, List[str]] = {}

        self._init_objects(env_layout.get("env_objects", []), env_setup.get("env_objects", []),
                           layout_path, setup_path)

        # ------------------------------------------------------------------
        # The object states (T-G A5): the domain declares them, the setup
        # states which hold at the start, the environment holds the true facts
        # (state_facts), emitted to every WorldState by the builder
        # ------------------------------------------------------------------
        self.state_declarations: Dict[str, StateDeclaration] = {}
        for declaration in state_declarations:
            if declaration.name in self.state_declarations:
                raise ValueError(f"the domain declares the state '{declaration.name}' twice")
            self.state_declarations[declaration.name] = declaration
        self._check_declared_effects()
        self.state_facts: Set[Predicate] = set()
        self._init_states(env_setup.get("states", []), setup_path)


        # ------------------------------------------------------------------
        # Agents
        # ------------------------------------------------------------------
        self.humans: Dict[str, HumanAgent] = {}
        self.robots: Dict[str, RobotAgent] = {}
        # Per robot, what the record's coverage is judged against (T-H4,
        # world/queries.py): its task model, its hypothesis space and the
        # station's destinations. The world's side; the robot never holds it.
        self.observing: Dict[str, ObservingRobot] = {}

        self._spawn_agents(scenario)
        # First observation before the clock starts: the human acts before the
        # robot observes within a tick, so without this the first step is never
        # scored (see RobotAgent.observe_initial).
        for robot in self.robots.values():
            robot.observe_initial()


        # MY_TEST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        # manually seed robot_0 as already carrying item_6 (its own second      #
        # assigned task's item) at t=0, to trigger deliver_with_return on the   #
        # first task (item_4). Temporary hack for testing, not permanent.       #
        # self.robots["robot_0"].carrying = "item_6"                              #                              
        # self.objects["item_6"].held_by = "robot_0"                              #
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


        # ------------------------------------------------------------------
        # DataCollector
        # ------------------------------------------------------------------
        self.datacollector = datacollection.DataCollector(
            model_reporters={"Step": lambda m: m.schedule.steps},
            agent_reporters={"Position": lambda a: getattr(a, "pos", None)}
        )

    # =========================================================================
    # Step
    # =========================================================================

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)

    # =========================================================================
    # Initialization helpers
    # =========================================================================

    def _init_objects(self, layout_objects: list, setup_objects: list,
                      layout_path: str, setup_path: str):
        """
        Unified loader for all env_objects entries. Two passes, as before the
        split (T-L, stage 1): the layout's fixed objects first (shelves, gates,
        tables, machines...), then the setup's movable objects (items,
        pallets), whose position is derived from their home container.
        A layout entry has a "position" and no "initial_container"; a setup
        entry has an "initial_container"; every home container named by the
        setup is an object of the layout — each an error naming the artefact
        and the mismatch.
        """
        for obj in layout_objects:
            if "initial_container" in obj:
                raise ValueError(
                    f"layout '{layout_path}': object '{obj['id']}' declares "
                    f"\"initial_container\"; a movable object belongs to the setup"
                )
            if "position" not in obj:
                raise ValueError(
                    f"layout '{layout_path}': object '{obj['id']}' has no \"position\""
                )
        for obj in setup_objects:
            if "initial_container" not in obj:
                raise ValueError(
                    f"setup '{setup_path}': object '{obj['id']}' has no "
                    f"\"initial_container\"; a fixed object belongs to the layout"
                )

        for obj in layout_objects:
            self.objects[obj["id"]] = SimObject(
                obj_id=obj["id"],
                type=obj["type"],
                position=tuple(obj["position"]),
                size=tuple(obj["size"]),
                subtype=obj.get("subtype"),
                is_portable=False,  # direct-position objects are not portable
            )

        layout_ids = {obj["id"] for obj in layout_objects}

        for obj in setup_objects:
            container_id = obj["initial_container"]
            container = self.objects.get(container_id) if container_id in layout_ids else None
            if container is None:
                raise ValueError(
                    f"setup '{setup_path}': object '{obj['id']}' has home container "
                    f"'{container_id}', which is not an object of layout '{layout_path}'"
                )
            self.objects[obj["id"]] = SimObject(
                obj_id=obj["id"],
                type=obj["type"],
                position=container.position,
                size=tuple(obj["size"]),
                subtype=obj.get("subtype"),
                held_by=None,
                at_location=container_id,
                is_portable=True,  # items/pallets are portable, even if not currently held
                home_container=container_id,   # set once at load time, never mutated afterward
                destination=obj.get("destination"),   # likewise
            )
            # print(f"Loaded portable object {obj['id']} with home_container {container_id}")

        # Every object of a type the domain resolves through "destination_of"
        # declares its destination, naming an object of the layout of a type
        # the domain declares for it (T-B1a; T-G A5: one of the declared
        # destination types). An error, not a default.
        types_with_destination = self.tree.get_types_with_destination()
        for obj_id, obj in self.objects.items():
            if obj.type not in types_with_destination:
                continue
            dest_types = types_with_destination[obj.type]
            if obj.destination is None:
                raise ValueError(
                    f"setup '{setup_path}': {obj.type} '{obj_id}' declares no "
                    f"\"destination\" (the domain determines one for type '{obj.type}')"
                )
            dest = self.objects.get(obj.destination) if obj.destination in layout_ids else None
            if dest is None:
                raise ValueError(
                    f"setup '{setup_path}': {obj.type} '{obj_id}' has destination "
                    f"'{obj.destination}', which is not an object of layout '{layout_path}'"
                )
            if dest.type not in dest_types:
                raise ValueError(
                    f"setup '{setup_path}': {obj.type} '{obj_id}' has destination "
                    f"'{obj.destination}' of type '{dest.type}', but the domain declares for "
                    f"type '{obj.type}' the destination types {sorted(dest_types)}"
                )

        # Build type → instance-ids registry, feeds IR's hypothesis space
        for obj_id, obj in self.objects.items():
            self._objects_by_type.setdefault(obj.type, []).append(obj_id)

    # =========================================================================
    # The object states (T-G A5)
    # =========================================================================

    def _init_states(self, entries: list, setup_path: str):
        """
        The setup's "states" block: one entry per fact that holds at the start,
        {"state": <declared name>, "object": <object id>}, the object omitted
        for a fact about no object. A declared state not listed does not hold.
        Each entry is validated (_state_fact); an entry with another key, or
        listed twice, is an error naming the setup.
        """
        for entry in entries:
            unknown = set(entry) - {"state", "object"}
            if "state" not in entry or unknown:
                raise ValueError(
                    f"setup '{setup_path}': states entry {entry} is not of the form "
                    f"{{\"state\": <name>, \"object\": <object id>}} (\"object\" omitted for a fact about no object)"
                )
            try:
                fact = self._state_fact(entry["state"], entry.get("object"))
            except ValueError as e:
                raise ValueError(f"setup '{setup_path}': {e}") from e
            if fact in self.state_facts:
                raise ValueError(f"setup '{setup_path}': the state {fact} is listed twice")
            self.state_facts.add(fact)

    def _state_fact(self, name: str, obj_id: Optional[str]) -> Predicate:
        """
        The state fact `name` about `obj_id` (None: about no object), validated
        against the declarations: the name is declared; a state about an
        object of a type names an existing object of that type; a state about
        no object names none.
        """
        declaration = self.state_declarations.get(name)
        if declaration is None:
            raise ValueError(f"'{name}' is not a state the domain declares ({sorted(self.state_declarations)})")
        if declaration.object_type is None:
            if obj_id is not None:
                raise ValueError(f"the state '{name}' is a fact about no object, but names '{obj_id}'")
            return Predicate(name, ())
        if obj_id is None:
            raise ValueError(f"the state '{name}' is about an object of type '{declaration.object_type}', but names none")
        obj = self.objects.get(obj_id)
        if obj is None:
            raise ValueError(f"the state '{name}' names '{obj_id}', which is not an object of this run")
        if obj.type != declaration.object_type:
            raise ValueError(
                f"the state '{name}' names '{obj_id}' of type '{obj.type}', but is declared for type "
                f"'{declaration.object_type}'"
            )
        return Predicate(name, (Const(obj_id),))

    def _check_declared_effects(self):
        """
        Every effect and retraction of the tree's action schemas whose name is a
        declared state has the declared form: one argument for a state about an
        object, none for a fact about no object.
        """
        for action in self.tree.get_all_actions():
            for condition in list(action.effects) + list(action.retracts):
                declaration = self.state_declarations.get(condition.name)
                if declaration is None:
                    continue
                arity = 0 if declaration.object_type is None else 1
                if len(condition.args) != arity:
                    raise ValueError(
                        f"action '{action.name}': '{condition.name}' is a declared state with {arity} "
                        f"argument(s), but the action states it with {len(condition.args)}"
                    )

    def apply_state_changes(self, action: GroundedAction):
        """
        The environment's change when `action`'s last microaction has run (the
        executor calls it): its retractions, then its effects, whose names are
        declared states, grounded with the action's own bindings — the order
        successor_state() reads them in. Physical facts (at, holding, obj_at,
        waited) are not states: the builder derives them.
        """
        for condition in action.schema.retracts:
            if condition.name in self.state_declarations:
                fact = condition.to_predicate(action.bindings)
                self._state_fact(fact.name, fact.args[0].value if fact.args else None)
                self.state_facts.discard(fact)
        for condition in action.schema.effects:
            if condition.name in self.state_declarations:
                fact = condition.to_predicate(action.bindings)
                self._state_fact(fact.name, fact.args[0].value if fact.args else None)
                self.state_facts.add(fact)



    # =========================================================================
    # Agent spawning
    # =========================================================================

    def _spawn_agents(self, scenario: ScenarioConfig):
        """
        Spawn agents from ScenarioConfig.
        HumanAgent receives its scheduled_tasks, a Script, checked at load and
        run by its stack machine (_load_human_scripts()).
        RobotAgent receives its assigned_tasks as its task pool (with the prior
        on or off); when the assignment_prior switch is on, also the observed
        human's assigned_tasks, which go to its recognizer (the support
        restriction) and its meta-planner (commitment warrant, T-D G), never to
        its pool, and never the script; and its task model, built from the tree (T-H), with
        the hypothesis space built from it here, kept with the station's
        destinations as the robot's ObservingRobot (T-H4).
        """
        agent_cfgs = {a.agent_id: a for a in scenario.agents}

        # Every scripted and assigned task must be well typed against this layout
        # (F47b, TODO-49): the bound objects exist, with the types the schema
        # declares, and a duration parameter is a duration the body's own parser
        # reads (T-H). An error, not a warning.
        # A script is checked for types only (T-H): every task it names, an
        # entry's or a Start's.
        # Every start position lies inside the space's bounds (T-L, ruling a:
        # bounds only, objects are not obstacles for a start), checked with the
        # body's own bounds test before any agent is placed.
        for agent_cfg in scenario.agents:
            if self.space.out_of_bounds(agent_cfg.start_position):
                raise ValueError(
                    f"scenario '{scenario.id}', agent '{agent_cfg.agent_id}': start_position "
                    f"{agent_cfg.start_position} lies outside the space's bounds "
                    f"[{self.space.x_min}, {self.space.x_max}) x [{self.space.y_min}, {self.space.y_max})"
                )

        object_type_by_id = {obj_id: obj.type for obj_id, obj in self.objects.items()}
        check_duration = lambda duration: _parse_duration_to_steps(duration, self)
        for agent_cfg in scenario.agents:
            try:
                for task in agent_cfg.scheduled_tasks.tasks():
                    check_task_bindings(task, object_type_by_id, check_duration)
                for task in agent_cfg.assigned_tasks or []:
                    check_task_bindings(task, object_type_by_id, check_duration)
            except ValueError as e:
                raise ValueError(f"scenario '{scenario.id}', agent '{agent_cfg.agent_id}': {e}") from e

        # Every assigned task's determined parameter, resolved from the station,
        # has the type its schema declares (T-G A5): an assigned delivery of an
        # object whose designation is of another kind is refused.
        for agent_cfg in scenario.agents:
            for task in agent_cfg.assigned_tasks or []:
                try:
                    self._check_designated_types(task)
                except ValueError as e:
                    raise ValueError(f"scenario '{scenario.id}', agent '{agent_cfg.agent_id}': {e}") from e

        for agent_cfg in scenario.agents:
            start_pos = agent_cfg.start_position

            if agent_cfg.agent_type == "human":
                # Its script is checked and loaded once every agent is placed
                # (_load_human_scripts(), below): the replay needs the initial world.
                agent = HumanAgent(
                    unique_id=agent_cfg.agent_id,
                    model=self,
                    pos=start_pos,
                )
                self.space.place_agent(agent, start_pos)
                self.schedule.add(agent)
                self.humans[agent_cfg.agent_id] = agent

            elif agent_cfg.agent_type == "robot":
                # The robot's task model (T-H): built from the tree, per robot.
                # Every robot is given the use case's declared task model
                # (TODO-102: a per-robot task model on the robot's AgentConfig).
                task_model = TaskModel(self.tree, self._task_model_schemas)
                hypotheses = build_hypothesis_space(task_model=task_model, known_objects_by_type=self._objects_by_type)
                self.observing[agent_cfg.agent_id] = ObservingRobot(task_model, frozenset(hypotheses),
                                                                    self._destination_by_id())
                self._check_destinations(scenario, agent_cfg, agent_cfgs)
                observed_id = agent_cfg.observes[0] if agent_cfg.observes else None
                observed_cfg = agent_cfgs.get(observed_id) if observed_id else None
                observed_assigned = (
                    observed_cfg.assigned_tasks
                    if (self.assignment_prior and observed_cfg is not None)
                    else None
                )
                if agent_cfg.scheduled_tasks.entries and not agent_cfg.assigned_tasks:
                    logger.warning(
                        "Robot %s declares scheduled_tasks but no assigned_tasks — "
                        "its task pool is empty (robot scheduled_tasks is not read; see TODO-39)",
                        agent_cfg.agent_id,
                    )
                agent = RobotAgent(
                    unique_id=agent_cfg.agent_id,
                    model=self,
                    pos=start_pos,
                    task_model=task_model,
                    assigned_tasks=agent_cfg.assigned_tasks,  # List[TaskInstance]
                    hypotheses=hypotheses,
                    observed_agent_id=observed_id,
                    observed_assigned_tasks=observed_assigned,
                )
                self.space.place_agent(agent, start_pos)
                self.schedule.add(agent)
                self.robots[agent_cfg.agent_id] = agent

        self._load_human_scripts(scenario)

    def _check_destinations(self, scenario: ScenarioConfig, robot_cfg, agent_cfgs: Dict) -> None:
        """
        The tasks the robot's mind holds agree with the layout's destinations
        (T-B1a), checked where its task model is built: its own assigned tasks,
        its plans, and the assigned tasks of the agent it observes, which it may
        be told. The human's script is not checked: it may send an object
        elsewhere (T-H: types only).
        """
        destination_by_id = self._destination_by_id()
        checked = [robot_cfg] + [agent_cfgs[a] for a in robot_cfg.observes if a in agent_cfgs]
        for agent_cfg in checked:
            for task in agent_cfg.assigned_tasks or []:
                try:
                    check_task_destinations(task, destination_by_id)
                except ValueError as e:
                    raise ValueError(f"scenario '{scenario.id}', agent '{agent_cfg.agent_id}': {e}") from e

    def _check_designated_types(self, task: TaskInstance) -> None:
        """
        Each parameter `task` determines through "destination_of" (T-B1a): the
        destination the setup designates for its bound source object has the
        type the schema declares for that parameter. Raises ValueError naming
        the task, the source object, the designation and both types.
        """
        bound = {var.name: const.value for var, const in task.bindings.items()}
        for var_name, source_var in destination_derivations(task.schema):
            if source_var not in bound or source_var not in task.schema.parameter_types:
                continue
            source = bound[source_var]
            designated = self.objects[source].destination
            expected = task.schema.parameter_types[var_name]
            actual = self.objects[designated].type
            if actual != expected:
                raise ValueError(
                    f"{task_instance_key(task)}: {var_name} resolves to '{designated}', the destination the setup "
                    f"designates for {source_var}='{source}', of type '{actual}', but the schema requires type "
                    f"'{expected}'"
                )

    def _destination_by_id(self) -> Dict[str, str]:
        """The station: each object with a designated destination, and that destination."""
        return {obj_id: obj.destination for obj_id, obj in self.objects.items() if obj.destination is not None}

    def _load_human_scripts(self, scenario: ScenarioConfig):
        """
        Each human's script (T-H) checked against the initial world by the
        load-time replay (world/human_executor.check_script): every anchor
        against the sequential expansion, events and resumptions included, by
        the same stack machine the agent runs; then handed to the HumanAgent.
        A script that depends on the robot loads with the entries the replay
        left open, printed as one `[replay] ... not replayed:` line (T-G A3).
        Expanded with the world's tree. Then one `[coverage]` line per script
        entry for each robot observing the human, and its [scenario-coverage]
        line (_log_coverage).
        """
        world = build_world_state(self)
        planner = AdaptivePlanner(knowledge=self.tree)
        # The body's conversions for the replay: a duration to ticks, a walk to
        # its step positions up to where the body stops (the same functions the
        # executor runs).
        ticks_of = lambda duration: _parse_duration_to_steps(duration, self)
        walk = lambda start, target: walk_positions(start, target, _get_step_size(self))
        for agent_cfg in scenario.agents:
            if agent_cfg.agent_type != "human":
                continue
            try:
                replay = check_script(agent_cfg.scheduled_tasks, planner, world, agent_cfg.agent_id, ticks_of, walk)
            except ValueError as e:
                raise ValueError(f"scenario '{scenario.id}', agent '{agent_cfg.agent_id}': {e}") from e
            not_replayed = [t for t in replay.transitions if isinstance(t, StillOpen)]
            if not_replayed:
                logger.info(f"[replay] {agent_cfg.agent_id} not replayed: "
                            + " ".join(f"{t.entry!r} {task_instance_key(t.task)}" for t in not_replayed))
            self.humans[agent_cfg.agent_id].load_stack(agent_cfg.scheduled_tasks, planner)
            self._log_coverage(scenario, agent_cfg)

    def _log_coverage(self, scenario: ScenarioConfig, human_cfg) -> None:
        """
        Which script entries the observing robots' models cover (T-H4): one
        line per entry per robot observing the human (`entry=i`, then
        `repeatable=i` and `closing=j`, T-G A3), the entry's task and each
        of its events' started tasks (an interruption is judged on its own),
        each with its coverage (world/queries.coverage), in the run log beside
        the [IR] lines it is read against. Information for the reader: no run
        reads it, and it is the same with the assignment prior on and off.
        Then one `[scenario-coverage]` line per robot: the script's composition
        and its scenario coverage (world/composition.scenario_composition).
        """
        observers = [a.agent_id for a in scenario.agents
                     if a.agent_type == "robot" and human_cfg.agent_id in a.observes]
        for robot_id in observers:
            robot = self.observing[robot_id]
            script = human_cfg.scheduled_tasks
            lines = ([(OrdinaryRef(i), e.task, e.events) for i, e in enumerate(script.entries)]
                     + [(RepeatableRef(i), r.task, ()) for i, r in enumerate(script.repeatable)]
                     + [(ClosingRef(j), e.task, e.events) for j, e in enumerate(script.closing)])
            for ref, task, events in lines:
                judged = [f"{task_instance_key(task)}={coverage(task, robot)!r}"]
                judged += [f"start:{task_instance_key(ev.decision.task)}={coverage(ev.decision.task, robot)!r}"
                           for ev in events if isinstance(ev.decision, Start)]
                logger.info(f"[coverage] {human_cfg.agent_id} {robot_id} {ref!r} " + " ".join(judged))
            composition, scenario_coverage = scenario_composition(human_cfg.scheduled_tasks, robot)
            logger.info(f"[scenario-coverage] {human_cfg.agent_id} {robot_id} "
                        f"scenario_coverage={scenario_coverage.value} {composition!r}")

    # =========================================================================
    # Public query methods
    # =========================================================================

    def get_object(self, obj_id: str) -> Optional[SimObject]:
        return self.objects.get(obj_id)

    def get_objects_by_type(self, type: str) -> List[str]:
        return self._objects_by_type.get(type, [])

    def get_movable_objects(self) -> Dict[str, SimObject]:
        """Return all items — used by world_state_builder."""
        return {oid: o for oid, o in self.objects.items() if o.type == "item"}

    def get_item_location(self, item_id: str) -> Optional[Tuple[float, float]]:
        item = self.objects.get(item_id)
        if item is None:
            return None
        if item.held_by:
            ag = self.humans.get(item.held_by) or self.robots.get(item.held_by)
            return getattr(ag, "pos", None)
        if item.at_location:
            loc = self.objects.get(item.at_location)
            return loc.position if loc else None
        return item.position