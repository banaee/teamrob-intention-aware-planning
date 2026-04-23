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
    - No YAML parsing for scenarios or operator definitions

COORDINATE SYSTEM:
    Matches env_layout1.json exactly: origin (0,0) at center of room.
"""

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from shared.domain_knowledge import DomainKnowledgeBase
from shared.types import ScenarioConfig
from domains.kitting.registry import register_kitting_domain
from domains.dock_loading.registry import register_dock_loading_domain


from mesa_sim.mesa_fork import model, space, time, datacollection
from mesa_sim.sim_agents import HumanAgent, RobotAgent


# =============================================================================
# Environment object dataclasses
# =============================================================================

@dataclass
class EnvObject:
    obj_id: str
    obj_type: str
    position: Tuple[float, float]
    size: Tuple[float, float]
    zone: Optional[str] = None


@dataclass
class ItemObject:
    obj_id: str
    obj_type: str
    item_type: str
    position: Tuple[float, float]
    size: Tuple[float, float]
    zone: Optional[str] = None
    held_by: Optional[str] = None
    at_location: Optional[str] = None
    # for pallet loading domain
    good_type: Optional[str] = None
    is_empty: bool = False
    # runtime scan state — set by executor on TOUCH
    is_scanned: bool = False

# =============================================================================
# FactoryModel
# =============================================================================

class FactoryModel(model.Model):

    # TODO: for now it is hardcoded to load the kitting domain — make it flexible to load other domains as well
    def __init__(self,
                 scenario: ScenarioConfig,
                 register_fn=register_kitting_domain,
                 env_layout_path: str = "domains/kitting/env_layout1.json", 
                #  register_fn=register_dock_loading_domain,
                    # env_layout_path: str = "domains/dock_loading/env_layout1.json",
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
        room = env_layout["room"]
        width = room["width"]
        height = room["height"]

        self.space = space.ContinuousSpace(
            x_min=-width / 2,
            x_max=width / 2,
            y_min=-height / 2,
            y_max=height / 2,
            torus=False
        )

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
        # Environment objects registry
        # ------------------------------------------------------------------
        self.env_objects: Dict[str, EnvObject] = {}
        self.items: Dict[str, ItemObject] = {}

        self._init_shelves(env_layout.get("shelves", []))
        self._init_kitting_table(env_layout.get("kitting_table", {}))
        self._init_coffee_machines(env_layout.get("coffee_machine", []))
        self._init_ac_switches(env_layout.get("AC_switches", []))
        self._init_obstacles(env_layout.get("obstacles", []))
        # ADD for dock domain
        self._init_env_objects(env_layout.get("env_objects", []))
        # both domains use it
        self._init_items(env_layout.get("items", []))


        # ------------------------------------------------------------------
        # Agents
        # ------------------------------------------------------------------
        self.humans: Dict[str, HumanAgent] = {}
        self.robots: Dict[str, RobotAgent] = {}

        self._spawn_agents(scenario)

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

    def _init_shelves(self, shelves_data: list):
        for s in shelves_data:
            self.env_objects[s["id"]] = EnvObject(
                obj_id=s["id"], obj_type="shelf",
                position=tuple(s["position"]), size=tuple(s["size"]),
                zone=s.get("zone")
            )

    def _init_kitting_table(self, kt_data: dict):
        if not kt_data:
            return
        self.env_objects["kitting_table"] = EnvObject(
            obj_id="kitting_table", obj_type="kitting_table",
            position=tuple(kt_data["position"]), size=tuple(kt_data["size"]),
            zone=kt_data.get("zone")
        )

    def _init_coffee_machines(self, cm_data: list):
        for cm in cm_data:
            self.env_objects[cm["id"]] = EnvObject(
                obj_id=cm["id"], obj_type="coffee_machine",
                position=tuple(cm["position"]), size=tuple(cm["size"]),
                zone=cm.get("zone")
            )

    def _init_ac_switches(self, ac_data: list):
        for ac in ac_data:
            self.env_objects[ac["id"]] = EnvObject(
                obj_id=ac["id"], obj_type="ac_switch",
                position=tuple(ac["position"]), size=tuple(ac["size"]),
                zone=ac.get("zone")
            )

    def _init_obstacles(self, obs_data: list):
        for ob in obs_data:
            self.env_objects[ob["id"]] = EnvObject(
                obj_id=ob["id"], obj_type="obstacle",
                position=tuple(ob["position"]), size=tuple(ob["size"]),
                zone=None
            )

    def _init_env_objects(self, objects_data: list):
        """Generic loader for flat env_objects list (dock_loading and future domains)."""
        for obj in objects_data:
            self.env_objects[obj["id"]] = EnvObject(
                obj_id=obj["id"],
                obj_type=obj["type"],
                position=tuple(obj["position"]),
                size=tuple(obj["size"]),
                zone=obj.get("zone"),
            )
            
    def _init_items(self, items_data: list):
        for it in items_data:
            shelf_id = it["initial_location"]
            shelf = self.env_objects.get(shelf_id)
            self.items[it["id"]] = ItemObject(
                obj_id=it["id"], obj_type="item",
                item_type=it["type"],
                position=shelf.position if shelf else (0.0, 0.0),
                size=tuple(it["size"]),
                zone=shelf.zone if shelf else None,
                held_by=None,
                at_location=shelf_id,
                good_type=it.get("good_type"),      # for dock domain, e.g. "dry" or "frozen"
                is_empty=it.get("is_empty", False), # for dock domain, True if it's an empty pallet
            )

    def _spawn_agents(self, scenario: ScenarioConfig):
        """
        Spawn agents from ScenarioConfig.
        HumanAgent receives its TaskInstance list as script.
        RobotAgent receives its TaskInstance list as assigned_tasks.
        """
        for agent_cfg in scenario.agents:
            start_pos = agent_cfg.start_position

            if agent_cfg.agent_type == "human":
                agent = HumanAgent(
                    unique_id=agent_cfg.agent_id,
                    model=self,
                    pos=start_pos,
                    script=agent_cfg.assigned_tasks,  # List[TaskInstance]
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
                    assigned_tasks=agent_cfg.assigned_tasks,  # List[TaskInstance]
                    observed_agent_id=observed_id,
                )
                self.space.place_agent(agent, start_pos)
                self.schedule.add(agent)
                self.robots[agent_cfg.agent_id] = agent

    # =========================================================================
    # Public query methods
    # =========================================================================

    def get_env_object(self, obj_id: str) -> Optional[EnvObject]:
        return self.env_objects.get(obj_id)

    def get_item(self, item_id: str) -> Optional[ItemObject]:
        return self.items.get(item_id)

    def get_movable_objects(self) -> Dict[str, ItemObject]:
        """Return all items — used by world_state_builder."""
        return self.items

    def get_zone_of_position(self, x: float, y: float) -> Optional[str]:
        for zone_id, bounds in self.zone_map.items():
            if (bounds["x_min"] <= x <= bounds["x_max"] and
                    bounds["y_min"] <= y <= bounds["y_max"]):
                return zone_id
        return None

    def get_objects_in_zone(self, zone_id: str) -> List[EnvObject]:
        return [obj for obj in self.env_objects.values() if obj.zone == zone_id]

    def get_item_location(self, item_id: str) -> Optional[Tuple[float, float]]:
        item = self.items.get(item_id)
        if item is None:
            return None
        if item.held_by:
            ag = self.humans.get(item.held_by) or self.robots.get(item.held_by)
            return getattr(ag, "pos", None)
        if item.at_location:
            loc = self.env_objects.get(item.at_location)
            return loc.position if loc else None
        return item.position