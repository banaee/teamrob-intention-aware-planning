# domains/kitting/fixture_generation.py
"""
Programmatic layout / scenario generation and registration for the kitting
domain (TODO-47 (a), first part; built for T-B1b's two-table fixture).

A fixture module states its geometry and task assignments once, as Python
data, and calls:
    build_layout()      the env_layout dict, in the same form as the
                        hand-written env_layout<N>.json files
    delivery_scenario() a ScenarioConfig whose delivery task instances state
                        the table the layout designates for each item
    register_layout()   adds the layout and its scenarios to a domain_config

The layout JSON stays a file on disk (SimModel and the visualization read a
path): write_layout() regenerates it from the fixture module, and
register_layout() refuses a file that no longer equals the generated layout,
so the file and the module cannot drift apart. No edit to scenarios.py, and
one registration call in registry.py per fixture module.
"""

import json
from typing import Dict, List, Tuple

from shared.types import Var, Const, TaskInstance, AgentConfig, ScenarioConfig
from domains.kitting.tasks import deliver_item

Position = Tuple[float, float]


def build_layout(
    name: str,
    notes: str,
    width: int,
    height: int,
    tables: Dict[str, Position],
    shelves: Dict[str, Position],
    items: Dict[str, Tuple[str, str]],      # {item_id: (shelf_id, destination table_id)}
    robot_start: Position,
    human_start: Position,
) -> dict:
    """The env_layout dict: a room centred on (0, 0), its four quadrant zones,
    the tables, the shelves, and each item with its origin shelf and its
    designated table."""
    w, h = width // 2, height // 2
    quadrants = {"zone_NW": (-w, 0, 0, h), "zone_NE": (0, w, 0, h), "zone_SW": (-w, 0, -h, 0), "zone_SE": (0, w, -h, 0)}

    def zone_of(pos: Position) -> str:
        return next(z for z, (x0, x1, y0, y1) in quadrants.items() if x0 <= pos[0] <= x1 and y0 <= pos[1] <= y1)

    objects = [{"id": t, "type": "kitting_table", "position": list(p), "size": [200, 100], "zone": zone_of(p)}
               for t, p in tables.items()]
    objects += [{"id": s, "type": "shelf", "position": list(p), "size": [100, 100], "slots": 2, "zone": zone_of(p)}
                for s, p in shelves.items()]
    objects += [{"id": i, "type": "item", "initial_container": shelf, "destination": table, "size": [25, 25]}
                for i, (shelf, table) in items.items()]
    return {
        "space": {"width": width, "height": height, "name": name, "units": "cm", "notes": notes},
        "zones": [{"id": z, "bounds": {"x_min": x0, "x_max": x1, "y_min": y0, "y_max": y1}}
                  for z, (x0, x1, y0, y1) in quadrants.items()],
        "doors": [],
        "robots": [{"id": "robot_0", "type": "mobile_manipulator", "initial_container": zone_of(robot_start),
                    "initial_x": robot_start[0], "initial_y": robot_start[1]}],
        "humans": [{"id": "human_0", "type": "worker", "initial_container": zone_of(human_start),
                    "initial_x": human_start[0], "initial_y": human_start[1]}],
        "env_objects": objects,
    }


def delivery(layout: dict, item: str) -> TaskInstance:
    """deliver_item for `item`, stating the table the layout designates for it."""
    table = next(o["destination"] for o in layout["env_objects"] if o["id"] == item)
    return TaskInstance(schema=deliver_item, bindings={Var("?item"): Const(item), Var("?kitting_table"): Const(table)})


def delivery_scenario(
    id: str,
    name: str,
    description: str,
    layout: dict,
    human_start: Position,
    human_items: List[str],                 # the human's script, in order; also its work order
    robot_start: Position,
    robot_items: List[str],                 # the robot's pool, unordered
) -> ScenarioConfig:
    return ScenarioConfig(id=id, name=name, description=description, agents=[
        AgentConfig(agent_id="human_0", agent_type="human", start_position=human_start,
                    scheduled_tasks=[delivery(layout, i) for i in human_items],
                    assigned_tasks=[delivery(layout, i) for i in human_items], observes=[]),
        AgentConfig(agent_id="robot_0", agent_type="robot", start_position=robot_start,
                    assigned_tasks=[delivery(layout, i) for i in robot_items], observes=["human_0"]),
    ])


def write_layout(layout: dict, path: str) -> None:
    with open(path, "w") as f:
        json.dump(layout, f, indent=2)
        f.write("\n")


def register_layout(domain_config: dict, layout_name: str, path: str, layout: dict,
                    scenarios: List[ScenarioConfig]) -> None:
    """Add a generated layout and its scenarios to `domain_config`. The file at
    `path` must equal the generated layout (regenerate it with write_layout()).
    A layout entry written by hand in the registry (a viewing scenario) is kept:
    the generated scenarios are added to it, under the same path."""
    entry = domain_config["layouts"].get(layout_name)
    if entry is not None:
        clash = sorted(set(entry["scenarios"]) & {s.id for s in scenarios})
        if entry["path"] != path or clash:
            raise ValueError(f"register_layout: layout '{layout_name}' is already registered with "
                             f"path '{entry['path']}' and scenarios {sorted(entry['scenarios'])}")
    with open(path, "r") as f:
        on_disk = json.load(f)
    if on_disk != json.loads(json.dumps(layout)):
        raise ValueError(f"register_layout: '{path}' differs from the generated layout '{layout_name}'; "
                         f"regenerate it from its fixture module")
    entry = domain_config["layouts"].setdefault(layout_name, {"path": path, "scenarios": {}})
    entry["scenarios"].update({s.id: s for s in scenarios})
