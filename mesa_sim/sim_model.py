"""
mesa_sim/sim_model.py

PURPOSE:
    Mesa embodiment of the factory environment.
    Loads a layout JSON (the room) and a setup JSON (the shift, T-L), receives
    a ScenarioConfig, builds the physical space, spawns agents, and drives the
    simulation step loop.

WHAT THIS MODULE DOES:
    - Reads the layout JSON (space, zones, fixed objects) and the setup JSON
      (movable objects with their home containers and destinations)
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
from typing import Dict, List, Optional, Sequence, Tuple

from shared.knowledge import Tree, TaskModel
from shared.planner import AdaptivePlanner
from shared.recognizer import build_hypothesis_space
from shared.types import ScenarioConfig, Start, TaskSchema, check_task_bindings, check_task_destinations, task_instance_key
from world.human_executor import check_script
from world.composition import scenario_composition
from world.queries import ObservingRobot, coverage
# from domains.kitting.registry import register_kitting_domain
# from domains.dock_loading.registry import register_dock_loading_domain


from mesa_sim.mesa_fork import model, space, time, datacollection
from mesa_sim.sim_agents import HumanAgent, RobotAgent
from mesa_sim.world_state_builder import build_world_state
from mesa_sim.action_decomposer import _parse_duration_to_steps, _get_step_size, steps_toward
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
    zone: Optional[str] = None
    subtype: Optional[str] = None      # domain-specific classification:
                                        # kitting: "part_A", "part_D", ...
                                        # dock loading: "frozen", "dry"

    held_by: Optional[str] = None
    at_location: Optional[str] = None
    is_empty: bool = False             # dock loading: pallet empty/full state
    is_scanned: bool = False
    is_open: Optional[bool] = None     # gates — kept as attribute, not tracked/implemented this phase
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
                 overrides: Sequence[Override] = ()):
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
        # Zone map
        # ------------------------------------------------------------------
        self.zone_map: Dict[str, dict] = {
            z["id"]: z["bounds"] for z in env_layout.get("zones", [])
        }

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
        pallets), whose position/zone are derived from their home container.
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
                zone=obj.get("zone"),
                subtype=obj.get("subtype"),
                is_empty=obj.get("is_empty", False),
                is_scanned=obj.get("is_scanned", False),
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
                zone=container.zone,
                subtype=obj.get("subtype"),
                held_by=None,
                at_location=container_id,
                is_empty=obj.get("is_empty", False),
                is_scanned=obj.get("is_scanned", False),
                is_portable=True,  # items/pallets are portable, even if not currently held
                home_container=container_id,   # set once at load time, never mutated afterward
                destination=obj.get("destination"),   # likewise
            )
            # print(f"Loaded portable object {obj['id']} with home_container {container_id}")

        # Every object of a type the domain resolves through "destination_of"
        # declares its destination, naming an object of the layout of the
        # type the schema declares for it (T-B1a). An error, not a default.
        types_with_destination = self.tree.get_types_with_destination()
        for obj_id, obj in self.objects.items():
            if obj.type not in types_with_destination:
                continue
            task_name, dest_type = types_with_destination[obj.type]
            if obj.destination is None:
                raise ValueError(
                    f"setup '{setup_path}': {obj.type} '{obj_id}' declares no "
                    f"\"destination\" (required by task '{task_name}')"
                )
            dest = self.objects.get(obj.destination) if obj.destination in layout_ids else None
            if dest is None:
                raise ValueError(
                    f"setup '{setup_path}': {obj.type} '{obj_id}' has destination "
                    f"'{obj.destination}', which is not an object of layout '{layout_path}'"
                )
            if dest_type is not None and dest.type != dest_type:
                raise ValueError(
                    f"setup '{setup_path}': {obj.type} '{obj_id}' has destination "
                    f"'{obj.destination}' of type '{dest.type}', but task '{task_name}' "
                    f"requires type '{dest_type}'"
                )

        # Build type → instance-ids registry, feeds IR's hypothesis space
        for obj_id, obj in self.objects.items():
            self._objects_by_type.setdefault(obj.type, []).append(obj_id)



    # =========================================================================
    # Agent spawning
    # =========================================================================

    def _spawn_agents(self, scenario: ScenarioConfig):
        """
        Spawn agents from ScenarioConfig.
        HumanAgent receives its scheduled_tasks, a Script, checked at load and
        run by its stack machine (_load_human_scripts()).
        RobotAgent receives its assigned_tasks as its task pool, plus (when the
        assignment_prior switch is on) the observed human's assigned_tasks,
        never the script; and its task model, built from the tree (T-H), with
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

    def _destination_by_id(self) -> Dict[str, str]:
        """The station: each object with a designated destination, and that destination."""
        return {obj_id: obj.destination for obj_id, obj in self.objects.items() if obj.destination is not None}

    def _load_human_scripts(self, scenario: ScenarioConfig):
        """
        Each human's script (T-H) checked against the initial world by the
        load-time replay (world/human_executor.check_script): every anchor
        against the sequential expansion, events and resumptions included, by
        the same stack machine the agent runs; then handed to the HumanAgent.
        Expanded with the world's tree. Then one `[coverage]` line per script
        entry for each robot observing the human, and its [scenario-coverage]
        line (_log_coverage).
        """
        world = build_world_state(self)
        planner = AdaptivePlanner(knowledge=self.tree)
        # The body's conversions for the replay: a duration to ticks, a walk to
        # its step positions (the same functions the executor runs).
        ticks_of = lambda duration: _parse_duration_to_steps(duration, self)
        walk = lambda start, target: [m.params["target_pos"] for m in steps_toward(start, target, _get_step_size(self))]
        for agent_cfg in scenario.agents:
            if agent_cfg.agent_type != "human":
                continue
            try:
                check_script(agent_cfg.scheduled_tasks, planner, world, agent_cfg.agent_id, ticks_of, walk)
            except ValueError as e:
                raise ValueError(f"scenario '{scenario.id}', agent '{agent_cfg.agent_id}': {e}") from e
            self.humans[agent_cfg.agent_id].load_stack(agent_cfg.scheduled_tasks, planner)
            self._log_coverage(scenario, agent_cfg)

    def _log_coverage(self, scenario: ScenarioConfig, human_cfg) -> None:
        """
        Which script entries the observing robots' models cover (T-H4): one
        line per entry per robot observing the human, the entry's task and each
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
            for i, entry in enumerate(human_cfg.scheduled_tasks.entries):
                judged = [f"{task_instance_key(entry.task)}={coverage(entry.task, robot)!r}"]
                judged += [f"start:{task_instance_key(ev.decision.task)}={coverage(ev.decision.task, robot)!r}"
                           for ev in entry.events if isinstance(ev.decision, Start)]
                logger.info(f"[coverage] {human_cfg.agent_id} {robot_id} entry={i} " + " ".join(judged))
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

    def get_zone_of_position(self, x: float, y: float) -> Optional[str]:
        for zone_id, bounds in self.zone_map.items():
            if (bounds["x_min"] <= x <= bounds["x_max"] and
                    bounds["y_min"] <= y <= bounds["y_max"]):
                return zone_id
        return None

    def get_objects_in_zone(self, zone_id: str) -> List[SimObject]:
        return [obj for obj in self.objects.values() if obj.zone == zone_id]

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