# continuous_sim/layout_adapter.py

import json
import math
from typing import Tuple, List, Optional


class ContinuousLayoutAdapter:
    """
    Wraps env_layout1.json for the continuous backend.
    All positions are returned in METRES.
    env_layout1.json stores positions in cm — we divide by 100.
    
    Provides the interface that shared/costs.py expects.
    No ROS imports. No simulation imports. Pure data.
    """

    def __init__(self, layout_path: str):
        with open(layout_path) as f:
            raw = json.load(f)

        # Build object lookup: id → full object dict
        self._objects = {
            obj["id"]: obj
            for obj in raw.get("env_objects", [])
        }

        # Items also need positions (they sit at their shelf)
        # In env_layout1.json, items reference a container shelf
        # We resolve item position = shelf position
        self._items = {
            item["id"]: item
            for item in raw.get("items", [])
        }

        self._zones = raw.get("zones", [])

        # Bottlenecks: narrow passages where zone-level reasoning applies.
        # In env_layout1 (open warehouse) there are none.
        # Add manually here if your environment has narrow corridors.
        self.bottlenecks = []

    # ------------------------------------------------------------------ #
    # Core interface used by shared/costs.py                              #
    # ------------------------------------------------------------------ #

    def position_of(self, object_id: str) -> Tuple[float, float]:
        """
        Returns (x, y) in METRES for a named object.
        Accepts: shelf ids (shelf_0..shelf_7), kitting_table,
                 item ids (item_0..item_7 → resolved to their shelf).
        """
        # Direct object lookup (shelves, kitting_table, etc.)
        if object_id in self._objects:
            pos = self._objects[object_id]["position"]
            return (pos[0] / 100.0, pos[1] / 100.0)

        # Item → find its container shelf, return shelf position
        if object_id in self._items:
            shelf_id = self._items[object_id]["initial_container"]
            return self.position_of(shelf_id)

        raise KeyError(
            f"ContinuousLayoutAdapter: '{object_id}' not found in layout. "
            f"Known objects: {list(self._objects.keys())}"
        )

    def zone_of(self, object_id: str) -> str:
        """
        Returns the zone_id of a named object.
        Read directly from the 'zone' field in env_objects.
        """
        if object_id in self._objects:
            return self._objects[object_id].get("zone", "zone_unknown")

        if object_id in self._items:
            shelf_id = self._items[object_id]["initial_container"]
            return self.zone_of(shelf_id)

        raise KeyError(f"ContinuousLayoutAdapter: '{object_id}' not found")

    def zone_of_pos(self, pos: Tuple[float, float]) -> str:
        """
        Returns the zone_id for a continuous position (x, y) in METRES.
        Checks bounds defined in env_layout1.json zones (stored in cm).
        """
        x_cm = pos[0] * 100.0
        y_cm = pos[1] * 100.0

        for zone in self._zones:
            b = zone["bounds"]
            if (b["x_min"] <= x_cm <= b["x_max"] and
                    b["y_min"] <= y_cm <= b["y_max"]):
                return zone["id"]

        return "zone_unknown"

    def all_object_positions(self) -> dict:
        """
        Returns {object_id: (x_m, y_m)} for all env_objects.
        Useful for debugging and visualisation.
        """
        return {
            obj_id: self.position_of(obj_id)
            for obj_id in self._objects
        }
