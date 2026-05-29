"""
continuous_sim/world.py

PURPOSE:
    Single source of ground truth for the continuous simulation.
    Replaces Mesa's FactoryModel for the continuous backend.

WHAT THIS MODULE OWNS:
    - Robot continuous state       (x, y, vx, vy, ax, ay)
    - Human scripted motion state  (x, y, vx, vy, phase, current_microaction)
    - Static obstacle positions    (JAX arrays, fixed at construction)
    - Item / object states         (location, held_by)
    - Zone map                     (loaded from env_layout1.json)

UNITS:
    Everything internal is in METERS.
    env_layout1.json stores positions in centimetres — converted on load.
    PRIEST was written and tuned in metres — no conversion needed at that boundary.

    NOTE: env_layout1.json has a kitting-table y-position discrepancy (4.0 m)
    vs the obstacle corners that PRIEST was tuned with (6.0 m).
    The two kitting-table obstacle corners are therefore hardcoded to match
    PRIEST: (-3.0, 6.0) and (-1.0, 6.0).
    Fix the JSON when the environment layout is finalised.

JAX POLICY:
    - Obstacle arrays are stored as JAX arrays (they never change and PRIEST
      reads them directly every step — no conversion overhead).
    - Human and robot states are stored as plain Python floats (mutable state
      updated every dt; JAX arrays are immutable so mutation would require
      re-allocation every step, which is wasteful here).
    - get_priest_snapshot() assembles the jnp arrays PRIEST expects from the
      live float state. Obstacle arrays are passed through as-is (no copy).
      Human arrays are built fresh each call from live floats.
    - agent_near() uses numpy for a single scalar distance — no JAX overhead.

WHAT THIS MODULE DOES NOT DO:
    - Does NOT call the cognitive layer (recognizer, planner, replanning)
    - Does NOT build WorldState or Observation (those are separate builders)
    - Does NOT visualise anything

CALLED BY:
    continuous_sim/run_continuous.py

READ BY:
    continuous_sim/world_state_builder_continuous.py  -> WorldState
    continuous_sim/obs_builder_continuous.py          -> Observation
    local_planner_priest_interrupt.py                 -> get_priest_snapshot()
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import jax.numpy as jnp


# =============================================================================
# Internal dataclasses
# =============================================================================

@dataclass
class RobotState:
    """
    Full continuous kinematic state of the robot.
    Plain Python floats — updated by Euler integration every dt.
    """
    x:  float
    y:  float
    vx: float = 0.0
    vy: float = 0.0
    ax: float = 0.0
    ay: float = 0.0

    def as_tuple(self) -> Tuple[float, float, float, float, float, float]:
        """Return (x, y, vx, vy, ax, ay) — format PRIESTLocalPlanner.step() expects."""
        return (self.x, self.y, self.vx, self.vy, self.ax, self.ay)


@dataclass
class HumanState:
    """
    Continuous state of one human agent.
    Plain Python floats — updated by scripted motion every dt.
    """
    agent_id:            str
    x:                   float
    y:                   float
    vx:                  float = 0.0
    vy:                  float = 0.0
    phase:               str   = "to_goal"   # "to_goal" | "hold" | "done"
    hold_elapsed:        float = 0.0         # seconds spent in current hold
    current_microaction: str   = "stand"     # read by obs_builder_continuous


@dataclass
class HumanWaypoint:
    """
    One destination in a scripted human path.

    x, y         : destination in metres
    hold_s       : seconds to stay at this point (0 = pass through immediately)
    move_label   : microaction label while travelling toward this waypoint
    arrive_label : microaction label while holding at this waypoint
    """
    x:            float
    y:            float
    hold_s:       float = 0.0
    move_label:   str   = "step"
    arrive_label: str   = "stand"


@dataclass
class ItemState:
    """State of one kitting item."""
    item_id:     str
    item_type:   str
    location_id: str            # shelf_id | "held" | "kitting_table"
    x:           float          # world position in metres
    y:           float
    held_by:     Optional[str] = None   # agent_id if carried, else None


@dataclass
class Zone:
    """Axis-aligned rectangular zone loaded from env_layout1.json."""
    zone_id: str
    x_min:   float   # metres
    x_max:   float
    y_min:   float
    y_max:   float
    label:   str


# =============================================================================
# ContinuousWorld
# =============================================================================

class ContinuousWorld:
    """
    Ground-truth world for the continuous simulation.

    Parameters
    ----------
    layout_path : str | Path
        Path to env_layout1.json.
    dt : float
        Timestep in seconds. Must match PRIEST dt_step (default 0.1 s).
    human_speed : float
        Human walking speed m/s (default 0.15 — same as planner_2.py).
    human_arrival_eps : float
        Arrival tolerance metres (default 0.2 — same as planner_2.py).

    Typical usage
    -------------
        world = ContinuousWorld("domains/kitting/env_layout1.json")

        world.set_human_script([
            HumanWaypoint(x=-9.5, y=-3.0, hold_s=15.0, move_label="step"),
            HumanWaypoint(x= 5.0, y=-5.0, hold_s= 0.0, move_label="step"),
        ])

        # inside main loop:
        snapshot          = world.get_priest_snapshot()
        state             = world.get_robot_state_tuple()
        (traj), cmd, stat = local_planner.step(state, snapshot)
        world.step(cmd)
    """

    _CM_TO_M: float = 0.01   # env_layout1.json is centimetres; we work in metres

    def __init__(
        self,
        layout_path:       str | Path,
        dt:                float = 0.1,
        human_speed:       float = 0.15,
        human_arrival_eps: float = 0.2,
    ):
        self.dt                = dt
        self.human_speed       = human_speed
        self.human_arrival_eps = human_arrival_eps
        self.sim_time: float   = 0.0

        # --- Load layout -------------------------------------------------
        layout = self._load_layout(layout_path)

        # --- Zones -------------------------------------------------------
        self.zones: List[Zone] = self._parse_zones(layout)

        # --- Shelves (metres) --------------------------------------------
        self.shelves: Dict[str, Tuple[float, float]] = self._parse_shelves(layout)

        # --- Items -------------------------------------------------------
        self.items: Dict[str, ItemState] = self._parse_items(layout)

        # --- Static obstacle JAX arrays (metres) -------------------------
        # SOURCE: planner_2.py lines 108-109.
        # These are the values PRIEST was tuned with — do not reorder.
        # The last two entries are the kitting-table obstacle corners;
        # they are hardcoded here because the JSON y-value is wrong (see docstring).
        self._obs_x: jnp.ndarray = jnp.array([
             0.0,   0.0,   4.0,  -2.0,
             7.0,   7.0,  -7.0,  -7.0,
           -10.0, -10.0, -10.0,  10.0,
            10.0,  10.0,
            -3.0,  -1.0,          # kitting-table corners (hardcoded)
        ])                         # shape (16,)  units: metres

        self._obs_y: jnp.ndarray = jnp.array([
             1.0,  -2.0,   0.0,   0.0,
             3.0,  -3.0,   3.0,  -1.0,
             2.0,  -2.0,  -4.5,   2.0,
            -1.0,  -3.8,
             6.0,   6.0,          # kitting-table corners (hardcoded)
        ])                         # shape (16,)  units: metres

        n_obs = self._obs_x.shape[0]   # 16
        self._obs_vx: jnp.ndarray = jnp.zeros(n_obs)
        self._obs_vy: jnp.ndarray = jnp.zeros(n_obs)

        # --- Robot state -------------------------------------------------
        # SOURCE: planner_2.py line 87  self.state = (2.0, 2.0, 0.1, 0.0, 0.0, 0.0)
        # Also cross-checked with env_layout1.json robots[0].initial_x/y (200 cm = 2.0 m)
        robot_data  = layout.get("robots", [{}])[0]
        rx          = robot_data.get("initial_x", 200) * self._CM_TO_M
        ry          = robot_data.get("initial_y", 200) * self._CM_TO_M
        self.robot  = RobotState(x=rx, y=ry, vx=0.1, vy=0.0, ax=0.0, ay=0.0)
        self.robot_id:      str           = robot_data.get("id", "robot_0")
        self.robot_holding: Optional[str] = None   # item_id or None

        # --- Human state -------------------------------------------------
        # SOURCE: planner_2.py lines 113-118
        # initial_x = -400 cm = -4.0 m,  initial_y = -300 cm = -3.0 m
        human_data  = layout.get("humans", [{}])[0]
        hx          = human_data.get("initial_x", -400) * self._CM_TO_M
        hy          = human_data.get("initial_y", -300) * self._CM_TO_M
        self.human  = HumanState(
            agent_id=human_data.get("id", "human_0"),
            x=hx,
            y=hy,
        )

        # Scripted waypoints — set via set_human_script() before running
        self._waypoints: List[HumanWaypoint] = []
        self._wp_index:  int                 = 0

    # =========================================================================
    # Configuration — call before main loop
    # =========================================================================

    def set_human_script(self, waypoints: List[HumanWaypoint]) -> None:
        """
        Define the scripted path for the human agent.

        Replicating the planner_2.py three-phase default
        (start → goal → hold 15 s → end):

            world.set_human_script([
                HumanWaypoint(x=-9.5, y=-3.0, hold_s=15.0, move_label="step"),
                HumanWaypoint(x= 5.0, y=-5.0, hold_s= 0.0, move_label="step"),
            ])
        """
        self._waypoints         = list(waypoints)
        self._wp_index          = 0
        self.human.phase        = "to_goal" if waypoints else "done"
        self.human.hold_elapsed = 0.0

    # =========================================================================
    # Main step — called once per dt by run_continuous.py
    # =========================================================================

    def step(self, robot_command: Optional[Tuple[float, float, float, float]]) -> None:
        """
        Advance the entire world by one dt.

        Pattern in run_continuous.py:

            snapshot          = world.get_priest_snapshot()
            state             = world.get_robot_state_tuple()
            (traj), cmd, stat = local_planner.step(state, snapshot)
            world.step(cmd)          # <-- this method

        robot_command : (vx, vy, ax, ay) from PRIEST, or None to hold in place.
        """
        self._human_step()
        self._robot_step(robot_command)
        self.sim_time += self.dt

    # =========================================================================
    # Snapshots — read-only, consumed by external modules
    # =========================================================================

    def get_priest_snapshot(self) -> dict:
        """
        Build the world dict that PRIESTLocalPlanner.step(state, world) expects.

        SOURCE: planner_2.py self.world dict (lines 106-119).

        Obstacle arrays are the cached JAX arrays (no allocation).
        Human arrays are rebuilt from live floats each call (one jnp.array per
        component — unavoidable because human position changes every step).

        Returns
        -------
        {
            "obs":    {"x": jnp (16,), "y": jnp (16,), "vx": jnp (16,), "vy": jnp (16,)},
            "humans": {"x": jnp (1,),  "y": jnp (1,),  "vx": jnp (1,),  "vy": jnp (1,) },
        }
        All values in metres / m/s.
        """
        return {
            "obs": {
                "x":  self._obs_x,
                "y":  self._obs_y,
                "vx": self._obs_vx,
                "vy": self._obs_vy,
            },
            "humans": {
                "x":  jnp.array([self.human.x]),
                "y":  jnp.array([self.human.y]),
                "vx": jnp.array([self.human.vx]),
                "vy": jnp.array([self.human.vy]),
            },
        }

    def get_robot_state_tuple(self) -> Tuple[float, float, float, float, float, float]:
        """
        Return (x, y, vx, vy, ax, ay) in metres / m/s / m/s².
        Format expected by PRIESTLocalPlanner.step(state, world).
        """
        return self.robot.as_tuple()

    # =========================================================================
    # Zone lookup — equivalent to Mesa model.get_zone_of_position()
    # =========================================================================

    def get_zone_of_position(self, x: float, y: float) -> Optional[str]:
        """
        Return zone_id for position (x, y) in metres.
        Returns None if (x, y) falls outside all defined zones.

        Used by world_state_builder_continuous to produce in_zone predicates.
        Equivalent to mesa_sim/world_state_builder.py zone derivation.
        """
        for zone in self.zones:
            if zone.x_min <= x <= zone.x_max and zone.y_min <= y <= zone.y_max:
                return zone.zone_id
        return None

    # =========================================================================
    # Proximity helper
    # =========================================================================

    def agent_near(
        self,
        ax: float, ay: float,
        tx: float, ty: float,
        threshold: float = 0.4,
    ) -> bool:
        """
        True if (ax, ay) is within threshold metres of (tx, ty).
        Uses numpy for a single scalar — avoids JAX dispatch overhead on scalars.
        """
        dx = ax - tx
        dy = ay - ty
        return float(np.sqrt(dx * dx + dy * dy)) < threshold

    # =========================================================================
    # Item manipulation — called by goal_executor_continuous
    # =========================================================================

    def pick_item(self, agent_id: str, item_id: str) -> bool:
        """
        Mark item as held by agent.
        Returns False if item does not exist or is already held by someone.
        """
        if item_id not in self.items:
            return False
        item = self.items[item_id]
        if item.held_by is not None:
            return False
        item.held_by     = agent_id
        item.location_id = "held"
        if agent_id == self.robot_id:
            self.robot_holding = item_id
        return True

    def place_item(self, agent_id: str, item_id: str, location_id: str) -> bool:
        """
        Place item at a named location (shelf_id or "kitting_table").
        Returns False if item not found or not currently held by this agent.
        """
        if item_id not in self.items:
            return False
        item = self.items[item_id]
        if item.held_by != agent_id:
            return False
        shelf_pos = self.shelves.get(location_id)
        if shelf_pos is not None:
            item.x, item.y = shelf_pos
        item.location_id = location_id
        item.held_by     = None
        if self.robot_holding == item_id:
            self.robot_holding = None
        return True

    # =========================================================================
    # Private — robot integration
    # =========================================================================

    def _robot_step(
        self,
        command: Optional[Tuple[float, float, float, float]],
    ) -> None:
        """
        Euler-integrate one PRIEST velocity command into the robot state.

        SOURCE: new — Mesa mutated agent.pos directly; here we integrate
                the continuous (vx, vy, ax, ay) from PRIEST.

        command : (vx, vy, ax, ay)  metres/s and metres/s²
                  None  →  hold in place (zero everything).
        """
        if command is None:
            self.robot.vx = 0.0
            self.robot.vy = 0.0
            self.robot.ax = 0.0
            self.robot.ay = 0.0
            return

        # float() unwraps any JAX scalar that PRIEST might return
        vx = float(command[0])
        vy = float(command[1])
        ax = float(command[2])
        ay = float(command[3])

        self.robot.x  += vx * self.dt
        self.robot.y  += vy * self.dt
        self.robot.vx  = vx
        self.robot.vy  = vy
        self.robot.ax  = ax
        self.robot.ay  = ay

        # Carry held item with the robot
        if self.robot_holding is not None:
            item = self.items.get(self.robot_holding)
            if item is not None:
                item.x = self.robot.x
                item.y = self.robot.y

    # =========================================================================
    # Private — human scripted motion
    # =========================================================================

    def _human_step(self) -> None:
        """
        Advance human scripted motion by one dt.

        SOURCE: direct port of planner_2.py update_humans() lines 313-381,
                generalised to an arbitrary waypoint list instead of
                hardcoded human_start / human_goal / human_end attributes.

        Phase machine
        -------------
        "to_goal"  move toward _waypoints[_wp_index] at human_speed
                   on arrival: → "hold" if hold_s > 0, else advance wp_index
        "hold"     stay at waypoint, accumulate hold_elapsed
                   when elapsed >= hold_s: advance wp_index → "to_goal"
        "done"     no motion, microaction = "stand"
        """
        h = self.human

        # Terminal / empty
        if h.phase == "done" or not self._waypoints:
            h.vx                  = 0.0
            h.vy                  = 0.0
            h.current_microaction = "stand"
            return

        if self._wp_index >= len(self._waypoints):
            h.phase               = "done"
            h.vx                  = 0.0
            h.vy                  = 0.0
            h.current_microaction = "stand"
            return

        wp = self._waypoints[self._wp_index]

        # ------------------------------------------------------------------
        if h.phase == "to_goal":
            dx   = wp.x - h.x
            dy   = wp.y - h.y
            dist = float(np.sqrt(dx * dx + dy * dy))

            if dist < self.human_arrival_eps:
                # Snap to waypoint exactly
                h.x  = wp.x
                h.y  = wp.y
                h.vx = 0.0
                h.vy = 0.0

                if wp.hold_s > 0.0:
                    h.phase               = "hold"
                    h.hold_elapsed        = 0.0
                    h.current_microaction = wp.arrive_label
                else:
                    self._wp_index       += 1
                    h.phase               = "to_goal"
                    h.current_microaction = "stand"
                return

            # Euler step toward waypoint
            inv_dist = 1.0 / (dist + 1e-9)
            vx = dx * inv_dist * self.human_speed
            vy = dy * inv_dist * self.human_speed

            h.x  += vx * self.dt
            h.y  += vy * self.dt
            h.vx  = vx
            h.vy  = vy
            h.current_microaction = wp.move_label

        # ------------------------------------------------------------------
        elif h.phase == "hold":
            h.vx           = 0.0
            h.vy           = 0.0
            h.hold_elapsed += self.dt
            h.current_microaction = wp.arrive_label

            if h.hold_elapsed >= wp.hold_s:
                self._wp_index += 1
                h.phase         = "to_goal"
                h.hold_elapsed  = 0.0

    # =========================================================================
    # Private — layout parsing (all outputs in metres)
    # =========================================================================

    @staticmethod
    def _load_layout(path: str | Path) -> dict:
        with open(path, "r") as f:
            return json.load(f)

    def _parse_zones(self, layout: dict) -> List[Zone]:
        zones = []
        for z in layout.get("zones", []):
            b = z["bounds"]
            zones.append(Zone(
                zone_id=z["id"],
                x_min=b["x_min"] * self._CM_TO_M,
                x_max=b["x_max"] * self._CM_TO_M,
                y_min=b["y_min"] * self._CM_TO_M,
                y_max=b["y_max"] * self._CM_TO_M,
                label=z["label"],
            ))
        return zones

    def _parse_shelves(self, layout: dict) -> Dict[str, Tuple[float, float]]:
        shelves = {}
        for s in layout.get("shelves", []):
            px, py = s["position"]
            shelves[s["id"]] = (
                px * self._CM_TO_M,
                py * self._CM_TO_M,
            )
        return shelves

    def _parse_items(self, layout: dict) -> Dict[str, ItemState]:
        """Place each item at its initial shelf position."""
        shelves = self._parse_shelves(layout)
        items   = {}
        for it in layout.get("items", []):
            shelf_id = it["initial_location"]
            sx, sy   = shelves.get(shelf_id, (0.0, 0.0))
            items[it["id"]] = ItemState(
                item_id=it["id"],
                item_type=it["type"],
                location_id=shelf_id,
                x=sx,
                y=sy,
            )
        return items
