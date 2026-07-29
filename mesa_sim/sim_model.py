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
from shared.types import ScenarioConfig
# from domains.kitting.registry import register_kitting_domain
# from domains.dock_loading.registry import register_dock_loading_domain


from mesa_sim.mesa_fork import model, space, time, datacollection
from mesa_sim.sim_agents import HumanAgent, RobotAgent

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
                                 
# =============================================================================
# SimModel
# =============================================================================

class SimModel(model.Model):

    def __init__(self,
                 scenario: ScenarioConfig,
                 register_fn,
                 env_layout_path: str = "domains/kitting/env_layout1.json", 
                 seed=None):
        super().__init__()

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
        self.knowledge = DomainKnowledgeBase.from_domain(register_fn())


        # ------------------------------------------------------------------
        # Environment objects registry — unified, single dict
        # ------------------------------------------------------------------
        self.objects: Dict[str, SimObject] = {}
        self._objects_by_type: Dict[str, List[str]] = {}

        self._init_objects(env_layout.get("env_objects", []))


        # ------------------------------------------------------------------
        # Agents
        # ------------------------------------------------------------------
        self.humans: Dict[str, HumanAgent] = {}
        self.robots: Dict[str, RobotAgent] = {}

        self._spawn_agents(scenario)


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

    def _init_objects(self, objects_data: list):
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
            )
            # print(f"Loaded portable object {obj['id']} with home_container {container_id}")

        # Build type → instance-ids registry, feeds IR's hypothesis space
        for obj_id, obj in self.objects.items():
            self._objects_by_type.setdefault(obj.type, []).append(obj_id)



    # =========================================================================
    # Agent spawning
    # =========================================================================

    def _spawn_agents(self, scenario: ScenarioConfig):
        """
        Spawn agents from ScenarioConfig.
        HumanAgent receives its TaskInstance list as script.
        RobotAgent receives its TaskInstance list as scheduled_tasks.
        """
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
                agent = RobotAgent(
                    unique_id=agent_cfg.agent_id,
                    model=self,
                    pos=start_pos,
                    knowledge=self.knowledge,
                    scheduled_tasks=agent_cfg.scheduled_tasks,  # List[TaskInstance]
                    known_objects_by_type=self._objects_by_type,
                    observed_agent_id=observed_id,
                )
                self.space.place_agent(agent, start_pos)
                self.schedule.add(agent)
                self.robots[agent_cfg.agent_id] = agent

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