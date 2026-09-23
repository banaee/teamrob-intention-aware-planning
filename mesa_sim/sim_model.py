"""
mesa_sim/sim_model.py

PURPOSE:
    Mesa embodiment of the factory environment.
    Loads env_layout1.json, receives a ScenarioConfig, builds the physical
    space, spawns agents, and drives the simulation step loop.

WHAT THIS MODULE DOES:
    - Reads env_layout1.json for environment layout
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
    Matches env_layout1.json exactly: origin (0,0) at center of room.
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from shared.domain_knowledge import DomainKnowledgeBase
from shared.planner import AdaptivePlanner
from shared.types import (ScenarioConfig, TaskInstance, check_task_bindings, check_task_destinations,
                          check_no_landmark_parameters, check_work_order)
from domains.script import check_script_bindings, resolve_script
# from domains.kitting.registry import register_kitting_domain
# from domains.dock_loading.registry import register_dock_loading_domain


from mesa_sim.mesa_fork import model, space, time, datacollection
from mesa_sim.sim_agents import HumanAgent, RobotAgent
from mesa_sim.world_state_builder import build_world_state

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
                 env_layout_path: str = "domains/kitting/env_layout1.json", 
                 seed=None,
                 assignment_prior: bool = False,
                 strategy: str = "single_task",
                 gate_strategy: str = "none",
                 cost_strategy: str = "realized",
                 separation_stop: bool = False):
        super().__init__()

        # Evaluation switch: give each robot the observed human's assigned_tasks
        # as a persistent IR prior. Off = the robot knows no work order.
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
        # Load env layout
        # ------------------------------------------------------------------
        with open(env_layout_path, "r") as f:
            env_layout = json.load(f)

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
        # DomainKnowledgeBase — loaded once, shared across agents
        # ------------------------------------------------------------------
        domain = register_fn()
        # No task may bind a landmark (T-C1): it is a place for a human's script only.
        check_no_landmark_parameters(domain)
        self.knowledge = DomainKnowledgeBase.from_domain(domain)


        # ------------------------------------------------------------------
        # Environment objects registry — unified, single dict
        # ------------------------------------------------------------------
        self.objects: Dict[str, SimObject] = {}
        self._objects_by_type: Dict[str, List[str]] = {}

        self._init_objects(env_layout.get("env_objects", []), env_layout_path)


        # ------------------------------------------------------------------
        # Agents
        # ------------------------------------------------------------------
        self.humans: Dict[str, HumanAgent] = {}
        self.robots: Dict[str, RobotAgent] = {}

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

    def _init_objects(self, objects_data: list, env_layout_path: str):
        """
        Unified loader for all env_objects entries — items and fixed objects alike.
        Two passes: objects with a direct "position" first (shelves, gates, tables,
        machines...), then objects with "initial_container" (items, pallets), whose
        position/zone are derived from their container. Two-pass avoids depending
        on JSON array order — items may appear before or after their container.
        """
        direct = [o for o in objects_data if "initial_container" not in o]
        contained = [o for o in objects_data if "initial_container" in o]

        for obj in direct:
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

        for obj in contained:
            container_id = obj["initial_container"]
            container = self.objects.get(container_id)
            if container is None:
                # container itself missing a position (shouldn't happen — direct
                # pass above should have created it) — fall back, but this is a
                # layout authoring bug, not expected at runtime.
                logger.warning(
                    "Object %s references unknown/unresolved container %s",
                    obj["id"], container_id,
                )
            self.objects[obj["id"]] = SimObject(
                obj_id=obj["id"],
                type=obj["type"],
                position=container.position if container else (0.0, 0.0),
                size=tuple(obj["size"]),
                zone=container.zone if container else None,
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
        # declares its destination, naming an object of this layout of the
        # type the schema declares for it (T-B1a). An error, not a default.
        types_with_destination = self.knowledge.get_types_with_destination()
        for obj_id, obj in self.objects.items():
            if obj.type not in types_with_destination:
                continue
            task_name, dest_type = types_with_destination[obj.type]
            if obj.destination is None:
                raise ValueError(
                    f"layout '{env_layout_path}': {obj.type} '{obj_id}' declares no "
                    f"\"destination\" (required by task '{task_name}')"
                )
            dest = self.objects.get(obj.destination)
            if dest is None:
                raise ValueError(
                    f"layout '{env_layout_path}': {obj.type} '{obj_id}' has destination "
                    f"'{obj.destination}', which is not an object of this layout"
                )
            if dest_type is not None and dest.type != dest_type:
                raise ValueError(
                    f"layout '{env_layout_path}': {obj.type} '{obj_id}' has destination "
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
        HumanAgent receives its scheduled_tasks as script — its execution order.
        RobotAgent receives its assigned_tasks as its task pool, plus (when the
        assignment_prior switch is on) the observed human's assigned_tasks: the
        work order, never the script.
        """
        agent_cfgs = {a.agent_id: a for a in scenario.agents}

        # Every scripted and assigned task must be well typed against this layout
        # (F47b, TODO-49): the bound objects exist, with the types the schema
        # declares. An error, not a warning.
        # A human's script is checked element by element: every task in it
        # (a deviation's too), and every object a primitive names (T-C2a).
        object_type_by_id = {obj_id: obj.type for obj_id, obj in self.objects.items()}
        for agent_cfg in scenario.agents:
            try:
                check_script_bindings(agent_cfg.scheduled_tasks or [], object_type_by_id, self.knowledge)
                for task in agent_cfg.assigned_tasks or []:
                    check_task_bindings(task, object_type_by_id)
            except ValueError as e:
                raise ValueError(f"scenario '{scenario.id}', agent '{agent_cfg.agent_id}': {e}") from e

        # Assigned tasks — the robot's pool and the human's work order — agree
        # with the layout's destinations (T-B1a). The human's scheduled_tasks is
        # not checked: its script may send an object elsewhere.
        destination_by_id = {obj_id: obj.destination for obj_id, obj in self.objects.items()
                             if obj.destination is not None}
        for agent_cfg in scenario.agents:
            for task in agent_cfg.assigned_tasks or []:
                try:
                    check_task_destinations(task, destination_by_id)
                except ValueError as e:
                    raise ValueError(f"scenario '{scenario.id}', agent '{agent_cfg.agent_id}': {e}") from e

        for agent_cfg in scenario.agents:
            start_pos = agent_cfg.start_position

            if agent_cfg.agent_type == "human":
                agent = HumanAgent(
                    unique_id=agent_cfg.agent_id,
                    model=self,
                    pos=start_pos,
                    script=agent_cfg.scheduled_tasks,  # List[TaskInstance]
                )
                self.space.place_agent(agent, start_pos)
                self.schedule.add(agent)
                self.humans[agent_cfg.agent_id] = agent

            elif agent_cfg.agent_type == "robot":
                observed_id = agent_cfg.observes[0] if agent_cfg.observes else None
                observed_cfg = agent_cfgs.get(observed_id) if observed_id else None
                observed_assigned = (
                    observed_cfg.assigned_tasks
                    if (self.assignment_prior and observed_cfg is not None)
                    else None
                )
                if agent_cfg.scheduled_tasks and not agent_cfg.assigned_tasks:
                    logger.warning(
                        "Robot %s declares scheduled_tasks but no assigned_tasks — "
                        "its task pool is empty (robot scheduled_tasks is not read; see TODO-39)",
                        agent_cfg.agent_id,
                    )
                agent = RobotAgent(
                    unique_id=agent_cfg.agent_id,
                    model=self,
                    pos=start_pos,
                    knowledge=self.knowledge,
                    assigned_tasks=agent_cfg.assigned_tasks,  # List[TaskInstance]
                    known_objects_by_type=self._objects_by_type,
                    observed_agent_id=observed_id,
                    observed_assigned_tasks=observed_assigned,
                )
                self.space.place_agent(agent, start_pos)
                self.schedule.add(agent)
                self.robots[agent_cfg.agent_id] = agent

        self._resolve_human_scripts(scenario)

    def _resolve_human_scripts(self, scenario: ScenarioConfig):
        """
        Each human's script resolved against the initial world (T-C1, T-C2a):
        every TaskInstance expanded by the planner's decomposition, every
        deviation applied, so the executed form is primitives only; the work
        order checked again on it, by provenance. Kept in `human_scripts` for
        the action-level human executor (T-C2b).
        COMPATIBILITY PATH, removed in T-C2b: HumanAgent still runs a list of
        TaskInstances, planning each at its start, so a script written as tasks
        only is handed to it as written; a script with a primitive or a
        deviation cannot run before T-C2b and is refused here.
        """
        world = build_world_state(self)
        planner = AdaptivePlanner(knowledge=self.knowledge)
        self.human_scripts: Dict[str, list] = {}
        for agent_cfg in scenario.agents:
            if agent_cfg.agent_type != "human":
                continue
            where = f"scenario '{scenario.id}', agent '{agent_cfg.agent_id}'"
            try:
                resolved = resolve_script(agent_cfg.scheduled_tasks or [], planner, world, agent_cfg.agent_id)
                if agent_cfg.assigned_tasks:
                    check_work_order(agent_cfg.agent_id, resolved, agent_cfg.assigned_tasks)
            except ValueError as e:
                raise ValueError(f"{where}: {e}") from e
            if not all(isinstance(e, TaskInstance) for e in agent_cfg.scheduled_tasks or []):
                raise ValueError(
                    f"{where}: the script holds primitives or deviations, which the task-level "
                    f"HumanAgent cannot run; the action-level human executor is T-C2b"
                )
            self.human_scripts[agent_cfg.agent_id] = resolved

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