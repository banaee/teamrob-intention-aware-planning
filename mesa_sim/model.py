"""
mesa_sim/model.py

PURPOSE:
    Mesa embodiment of the factory environment.
    Loads domain1.json and scenarios.yaml, builds the physical space,
    spawns agents, and drives the simulation step loop.

WHAT THIS MODULE DOES:
    - Reads domain1.json for environment layout (space, zones, shelves,
      items, tables, coffee machines, AC switches, obstacles)
    - Reads scenarios.yaml for agent roles, start positions, task scripts
    - Creates Mesa ContinuousSpace with center-origin (0,0) matching domain1.json
    - Instantiates env objects as plain dataclasses (not Mesa agents)
    - Spawns HumanAgent (scripted) and RobotAgent (cognitive) via agents.py
    - Runs schedule.step() each tick — no centralized state management

WHAT THIS MODULE DOES NOT DO:
    - No WorldStateManager — ground truth lives in env_objects, read on
      demand by mesa_sim/world_state_builder.py
    - No IR, no planning, no task assignment logic
    - No TaskLibrary — that belongs to shared/knowledge.py
    - Does not touch tasks_library.yaml or actions_library.yaml

COORDINATE SYSTEM:
    Matches domain1.json exactly: origin (0,0) at center of room.
    ContinuousSpace configured with x_min=-width/2, x_max=width/2,
    y_min=-height/2, y_max=height/2. No translation needed anywhere.

USED BY:
    - mesa_sim/run_mesa.py  (entry point)
    - mesa_sim/world_state_builder.py  (reads env_objects, agent positions)
"""

import json
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import mesa
from mesa.space import ContinuousSpace
from mesa.time import BaseScheduler

# Agents imported here — defined in mesa_sim/agents.py
# from mesa_sim.agents import HumanAgent, RobotAgent  # uncomment when agents.py exists


# =============================================================================
# Environment object dataclasses
# Ground truth physical state. Mutated by agents during microaction execution.
# Read by world_state_builder.py to construct WorldState snapshots.
# =============================================================================

@dataclass
class EnvObject:
    obj_id: str
    obj_type: str           # "shelf", "kitting_table", "coffee_machine", "ac_switch", "obstacle"
    position: Tuple[float, float]
    size: Tuple[float, float]
    zone: Optional[str] = None


@dataclass
class ItemObject:
    obj_id: str
    obj_type: str           # always "item"
    item_type: str          # "part_A", "part_B", etc.
    position: Tuple[float, float]
    size: Tuple[float, float]
    zone: Optional[str] = None
    held_by: Optional[str] = None       # agent_id if being carried, else None
    at_location: Optional[str] = None   # env obj id (shelf_id or "kitting_table")


# =============================================================================
# FactoryModel
# =============================================================================

class FactoryModel(mesa.Model):

    def __init__(self,
                 scenario_id: str,
                 domain_path: str = "configs/domain1.json",
                 scenarios_path: str = "configs/scenarios.yaml"):
        super().__init__()

        # ------------------------------------------------------------------
        # Load configs
        # ------------------------------------------------------------------
        with open(domain_path, "r") as f:
            domain = json.load(f)

        with open(scenarios_path, "r") as f:
            scenarios_raw = yaml.safe_load(f)

        scenario = self._find_scenario(scenarios_raw, scenario_id)

        # ------------------------------------------------------------------
        # Space — center-origin, matches domain1.json coordinates directly
        # ------------------------------------------------------------------
        room = domain["room"]
        width = room["width"]
        height = room["height"]

        self.space = ContinuousSpace(
            x_min=-width / 2,
            x_max=width / 2,
            y_min=-height / 2,
            y_max=height / 2,
            torus=False
        )

        # ------------------------------------------------------------------
        # Scheduler
        # ------------------------------------------------------------------
        self.schedule = BaseScheduler(self)

        # ------------------------------------------------------------------
        # Zone map  {zone_id: bounds_dict}
        # ------------------------------------------------------------------
        self.zone_map: Dict[str, dict] = {
            z["id"]: z["bounds"] for z in domain.get("zones", [])
        }

        # ------------------------------------------------------------------
        # Environment objects registry
        # {obj_id: EnvObject}  and  {item_id: ItemObject}
        # ------------------------------------------------------------------
        self.env_objects: Dict[str, EnvObject] = {}
        self.items: Dict[str, ItemObject] = {}

        self._init_shelves(domain.get("shelves", []))
        self._init_kitting_table(domain.get("kitting_table", {}))
        self._init_coffee_machines(domain.get("coffee_machine", []))
        self._init_ac_switches(domain.get("AC_switches", []))
        self._init_obstacles(domain.get("obstacles", []))
        self._init_items(domain.get("items", []))

        # ------------------------------------------------------------------
        # Agents — humans first, then robots (mirrors old repo ordering)
        # Human script is private: robot has no access to it
        # ------------------------------------------------------------------
        self.humans: Dict[str, object] = {}
        self.robots: Dict[str, object] = {}

        self._spawn_agents(scenario, domain)

        # ------------------------------------------------------------------
        # DataCollector (stub)
        # ------------------------------------------------------------------
        self.datacollector = mesa.DataCollector(
            model_reporters={"Step": lambda m: m.schedule.steps},
            agent_reporters={"Position": lambda a: getattr(a, "pos", None)}
        )

    # =========================================================================
    # Step
    # =========================================================================

    def step(self):
        """Advance simulation by one tick. Each agent executes one microaction."""
        self.schedule.step()
        self.datacollector.collect(self)

    # =========================================================================
    # Initialization helpers
    # =========================================================================

    def _init_shelves(self, shelves_data: list):
        for s in shelves_data:
            obj = EnvObject(
                obj_id=s["id"],
                obj_type="shelf",
                position=tuple(s["position"]),
                size=tuple(s["size"]),
                zone=s.get("zone")
            )
            self.env_objects[s["id"]] = obj

    def _init_kitting_table(self, kt_data: dict):
        if not kt_data:
            return
        obj = EnvObject(
            obj_id="kitting_table",
            obj_type="kitting_table",
            position=tuple(kt_data["position"]),
            size=tuple(kt_data["size"]),
            zone=kt_data.get("zone")
        )
        self.env_objects["kitting_table"] = obj

    def _init_coffee_machines(self, cm_data: list):
        for cm in cm_data:
            obj = EnvObject(
                obj_id=cm["id"],
                obj_type="coffee_machine",
                position=tuple(cm["position"]),
                size=tuple(cm["size"]),
                zone=cm.get("zone")
            )
            self.env_objects[cm["id"]] = obj

    def _init_ac_switches(self, ac_data: list):
        for ac in ac_data:
            obj = EnvObject(
                obj_id=ac["id"],
                obj_type="ac_switch",
                position=tuple(ac["position"]),
                size=tuple(ac["size"]),
                zone=ac.get("zone")
            )
            self.env_objects[ac["id"]] = obj

    def _init_obstacles(self, obs_data: list):
        for ob in obs_data:
            obj = EnvObject(
                obj_id=ob["id"],
                obj_type="obstacle",
                position=tuple(ob["position"]),
                size=tuple(ob["size"]),
                zone=None  # obstacles have no zone in domain1.json
            )
            self.env_objects[ob["id"]] = obj

    def _init_items(self, items_data: list):
        for it in items_data:
            shelf_id = it["initial_location"]
            shelf = self.env_objects.get(shelf_id)
            initial_pos = shelf.position if shelf else (0.0, 0.0)

            item = ItemObject(
                obj_id=it["id"],
                obj_type="item",
                item_type=it["type"],
                position=initial_pos,
                size=tuple(it["size"]),
                zone=shelf.zone if shelf else None,
                held_by=None,
                at_location=shelf_id
            )
            self.items[it["id"]] = item

    def _spawn_agents(self, scenario: dict, domain: dict):
        """
        Create HumanAgent and RobotAgent from scenario definition.
        Human receives its full task script. Robot receives nothing cognitive here.
        """
        # Build quick lookup for domain agent initial positions
        domain_humans = {h["id"]: h for h in domain.get("humans", [])}
        domain_robots = {r["id"]: r for r in domain.get("robots", [])}

        for agent_cfg in scenario.get("agents", []):
            agent_id = agent_cfg["id"]
            agent_type = agent_cfg["type"]
            start_pos = tuple(agent_cfg["start_position"])

            if agent_type == "human":
                # TODO: uncomment when agents.py exists
                # script = self._build_human_script(agent_cfg)
                # agent = HumanAgent(
                #     unique_id=agent_id,
                #     model=self,
                #     script=script,
                #     pos=start_pos
                # )
                # self.space.place_agent(agent, start_pos)
                # self.schedule.add(agent)
                # self.humans[agent_id] = agent
                pass  # placeholder until agents.py exists

            elif agent_type == "robot":
                # TODO: uncomment when agents.py exists
                # agent = RobotAgent(
                #     unique_id=agent_id,
                #     model=self,
                #     pos=start_pos,
                #     observed_agent_id=agent_cfg.get("observes", [None])[0]
                # )
                # self.space.place_agent(agent, start_pos)
                # self.schedule.add(agent)
                # self.robots[agent_id] = agent
                pass  # placeholder until agents.py exists

    def _build_human_script(self, agent_cfg: dict) -> list:
        """
        Convert scenario agent config into an ordered task script for HumanAgent.
        Script is a list of dicts: [{task, parameters}, ...] plus optional deviation.
        Robot never sees this.
        """
        script = []
        for task_entry in agent_cfg.get("assigned_tasks", []):
            script.append({
                "task": task_entry["task"],
                "parameters": task_entry.get("parameters", {}),
                "origin": "assigned"
            })

        deviation = agent_cfg.get("foreseeable_deviation")
        if deviation:
            # Insert deviation after the specified task index
            insert_after = deviation.get("after_task", len(script) - 1)
            script.insert(insert_after + 1, {
                "task": deviation["task"],
                "parameters": deviation.get("parameters", {}),
                "origin": "foreseeable"
            })

        return script

    # =========================================================================
    # Public query methods
    # Used by world_state_builder.py and agents
    # =========================================================================

    def get_env_object(self, obj_id: str) -> Optional[EnvObject]:
        return self.env_objects.get(obj_id)

    def get_item(self, item_id: str) -> Optional[ItemObject]:
        return self.items.get(item_id)

    def get_zone_of_position(self, x: float, y: float) -> Optional[str]:
        """Return zone_id for a given (x, y) coordinate, or None if outside all zones."""
        for zone_id, bounds in self.zone_map.items():
            if (bounds["x_min"] <= x <= bounds["x_max"] and
                    bounds["y_min"] <= y <= bounds["y_max"]):
                return zone_id
        return None

    def get_objects_in_zone(self, zone_id: str) -> List[EnvObject]:
        return [obj for obj in self.env_objects.values() if obj.zone == zone_id]

    def get_item_location(self, item_id: str) -> Optional[Tuple[float, float]]:
        """
        Return current (x, y) of an item.
        If held by an agent, returns agent's current position.
        If at a location, returns that env object's position.
        """
        item = self.items.get(item_id)
        if item is None:
            return None
        if item.held_by:
            # Find the carrying agent
            agent = self.humans.get(item.held_by) or self.robots.get(item.held_by)
            return getattr(agent, "pos", None)
        if item.at_location:
            loc = self.env_objects.get(item.at_location)
            return loc.position if loc else None
        return item.position

    # =========================================================================
    # Internal helpers
    # =========================================================================

    @staticmethod
    def _find_scenario(scenarios_raw: dict, scenario_id: str) -> dict:
        for s in scenarios_raw.get("scenarios", []):
            if s["id"] == scenario_id:
                return s
        raise ValueError(f"Scenario '{scenario_id}' not found in scenarios.yaml")
