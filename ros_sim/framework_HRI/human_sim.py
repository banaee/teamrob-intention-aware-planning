"""
continuous_sim/human_sim.py

SCENARIOS UPDATED for visible robot interruption:

    SCENARIO_WAIT — human blocks the kitting_table while robot is delivering
    Human walks to kitting_table, stays 20s (t=14.6 to t=34.6).
    Robot arrives kitting_table at ~26.9s while HOLDING item_5.
    Result: WAIT decision. Robot waits ~7.7s for human to leave.

    SCENARIO_RESELECT — human blocks shelf_5 before robot picks up
    Human starts at (4.0, -1.0) zone_SE, close to shelf_5.
    Arrives shelf_5 at ~11.2s, dwells 10s.
    Robot arrives shelf_5 at ~9.7s — NOT yet holding.
    Result: RESELECT evaluated. Robot skips item_5 and picks item_1 or item_7.

    SCENARIO_COFFEE / SCENARIO_AC — baselines, no conflict, no reordering.

INTERFACE CONTRACT WITH HADI (unchanged):
    .agent_id, .x, .y, .vx, .vy, .current_zone, .micro_action, .step(dt)
"""

import math
from dataclasses import dataclass
from typing import List

MICRO_STEP    = "STEP"
MICRO_STAND   = "STAND"
MICRO_GRASP   = "GRASP"
MICRO_RELEASE = "RELEASE"


@dataclass
class Waypoint:
    x:            float
    y:            float
    label:        str
    dwell_s:      float
    micro_action: str = MICRO_STAND


@dataclass
class Scenario:
    name:      str
    intention: str
    waypoints: List[Waypoint]


SCENARIOS = {

    # WAIT scenario: human blocks kitting_table during robot delivery
    "SCENARIO_WAIT": Scenario(
        name="SCENARIO_WAIT", intention="deliver_item",
        waypoints=[
            Waypoint(x=-4.0, y=-3.0, label="start",         dwell_s=0.5,   micro_action=MICRO_STAND),
            Waypoint(x=-2.0, y=4.0,  label="kitting_table", dwell_s=20.0,  micro_action=MICRO_GRASP),
            Waypoint(x=-4.0, y=-3.0, label="start",         dwell_s=999.0, micro_action=MICRO_STAND),
        ],
    ),

    # RESELECT scenario: human blocks shelf_5 before robot picks up
    "SCENARIO_RESELECT": Scenario(
        name="SCENARIO_RESELECT", intention="deliver_item",
        waypoints=[
            Waypoint(x=4.0,  y=-1.0, label="start_zone_SE", dwell_s=0.5,   micro_action=MICRO_STAND),
            Waypoint(x=9.5,  y=0.0,  label="shelf_5",       dwell_s=10.0,  micro_action=MICRO_GRASP),
            Waypoint(x=-2.0, y=4.0,  label="kitting_table", dwell_s=3.0,   micro_action=MICRO_RELEASE),
            Waypoint(x=4.0,  y=-1.0, label="start_zone_SE", dwell_s=999.0, micro_action=MICRO_STAND),
        ],
    ),

    # Baseline: human stays in zone_SW, no conflict with robot
    "SCENARIO_COFFEE": Scenario(
        name="SCENARIO_COFFEE", intention="coffee_break",
        waypoints=[
            Waypoint(x=-4.0,  y=-3.0,  label="start",         dwell_s=0.5,   micro_action=MICRO_STAND),
            Waypoint(x=-9.75, y=-2.75, label="coffee_machine", dwell_s=15.0,  micro_action=MICRO_GRASP),
            Waypoint(x=-4.0,  y=-3.0,  label="start",         dwell_s=999.0, micro_action=MICRO_STAND),
        ],
    ),

    # Baseline: human stays in zone_SW, no conflict
    "SCENARIO_AC": Scenario(
        name="SCENARIO_AC", intention="ac_activation",
        waypoints=[
            Waypoint(x=-4.0,  y=-3.0,  label="start",     dwell_s=0.5,   micro_action=MICRO_STAND),
            Waypoint(x=-9.75, y=-3.50, label="AC_switch",  dwell_s=3.0,   micro_action=MICRO_GRASP),
            Waypoint(x=-4.0,  y=-3.0,  label="start",     dwell_s=999.0, micro_action=MICRO_STAND),
        ],
    ),

    # Legacy names kept for compatibility
    "DELIVER_ITEM_item5": Scenario(
        name="DELIVER_ITEM_item5", intention="deliver_item",
        waypoints=[
            Waypoint(x=-4.0, y=-3.0, label="start",         dwell_s=1.0,   micro_action=MICRO_STAND),
            Waypoint(x=9.5,  y=0.0,  label="shelf_5",       dwell_s=2.0,   micro_action=MICRO_GRASP),
            Waypoint(x=-2.0, y=4.0,  label="kitting_table", dwell_s=2.0,   micro_action=MICRO_RELEASE),
            Waypoint(x=-4.0, y=-3.0, label="start",         dwell_s=999.0, micro_action=MICRO_STAND),
        ],
    ),
    "DELIVER_ITEM_item1": Scenario(
        name="DELIVER_ITEM_item1", intention="deliver_item",
        waypoints=[
            Waypoint(x=-4.0, y=-3.0, label="start",         dwell_s=1.0,   micro_action=MICRO_STAND),
            Waypoint(x=-9.5, y=-4.5, label="shelf_1",       dwell_s=2.0,   micro_action=MICRO_GRASP),
            Waypoint(x=-2.0, y=4.0,  label="kitting_table", dwell_s=2.0,   micro_action=MICRO_RELEASE),
            Waypoint(x=-4.0, y=-3.0, label="start",         dwell_s=999.0, micro_action=MICRO_STAND),
        ],
    ),
    "DELIVER_ITEM_item7": Scenario(
        name="DELIVER_ITEM_item7", intention="deliver_item",
        waypoints=[
            Waypoint(x=-4.0, y=-3.0, label="start",         dwell_s=1.0,   micro_action=MICRO_STAND),
            Waypoint(x=3.0,  y=-4.5, label="shelf_7",       dwell_s=2.0,   micro_action=MICRO_GRASP),
            Waypoint(x=-2.0, y=4.0,  label="kitting_table", dwell_s=2.0,   micro_action=MICRO_RELEASE),
            Waypoint(x=-4.0, y=-3.0, label="start",         dwell_s=999.0, micro_action=MICRO_STAND),
        ],
    ),
    "COFFEE_BREAK": Scenario(
        name="COFFEE_BREAK", intention="coffee_break",
        waypoints=[
            Waypoint(x=-4.0,  y=-3.0,  label="start",         dwell_s=1.0,   micro_action=MICRO_STAND),
            Waypoint(x=-9.75, y=-2.75, label="coffee_machine", dwell_s=15.0,  micro_action=MICRO_GRASP),
            Waypoint(x=-4.0,  y=-3.0,  label="start",         dwell_s=999.0, micro_action=MICRO_STAND),
        ],
    ),
    "AC_ACTIVATION": Scenario(
        name="AC_ACTIVATION", intention="ac_activation",
        waypoints=[
            Waypoint(x=-4.0,  y=-3.0,  label="start",     dwell_s=1.0,   micro_action=MICRO_STAND),
            Waypoint(x=-9.75, y=-3.50, label="AC_switch",  dwell_s=3.0,   micro_action=MICRO_GRASP),
            Waypoint(x=-4.0,  y=-3.0,  label="start",     dwell_s=999.0, micro_action=MICRO_STAND),
        ],
    ),
}


class ScriptedHuman:
    """
    Executes a Scenario by walking between waypoints at fixed speed.
    Interface: see module docstring.
    Hadi replaces this class with his real human model when ready.
    """

    ARRIVAL_THRESHOLD = 0.20

    def __init__(self, scenario, layout_zones, speed=0.5, agent_id="human_0"):
        self.scenario     = scenario
        self.layout_zones = layout_zones
        self.speed        = speed
        self.agent_id     = agent_id

        first_wp  = scenario.waypoints[0]
        self.x:  float = first_wp.x
        self.y:  float = first_wp.y
        self.vx: float = 0.0
        self.vy: float = 0.0

        self.current_zone = self._compute_zone()
        self.micro_action = MICRO_STAND

        # Final goal = last waypoint with a real action (not the idle return)
        # For DELIVER_ITEM: kitting_table is waypoints[-2]
        # For COFFEE/AC: the machine/switch is waypoints[-2]
        # General rule: last waypoint whose micro_action is not STAND
        self.final_goal_x: float = first_wp.x
        self.final_goal_y: float = first_wp.y
        for wp in scenario.waypoints:
            if wp.micro_action != MICRO_STAND:
                self.final_goal_x = wp.x
                self.final_goal_y = wp.y
        # Override: use the LAST meaningful waypoint (delivery, not pickup)
        # Walk backward to find it
        for wp in reversed(scenario.waypoints):
            if wp.micro_action != MICRO_STAND:
                self.final_goal_x = wp.x
                self.final_goal_y = wp.y
                break

        self._wp_index    = 0
        self._dwell_timer = 0.0
        self._dwelling    = True
        self._start_dwell()

    def step(self, dt):
        if self._dwelling:
            self._step_dwell(dt)
        else:
            self._step_walk(dt)
        self.current_zone = self._compute_zone()

    def _start_dwell(self):
        self._dwelling    = True
        self._dwell_timer = 0.0
        self.vx = 0.0
        self.vy = 0.0
        self.micro_action = self.scenario.waypoints[self._wp_index].micro_action

    def _step_dwell(self, dt):
        wp = self.scenario.waypoints[self._wp_index]
        self._dwell_timer += dt
        if self._dwell_timer >= wp.dwell_s:
            if self._wp_index + 1 < len(self.scenario.waypoints):
                self._wp_index += 1
                self._dwelling = False
                self.micro_action = MICRO_STEP
            else:
                self.micro_action = MICRO_STAND

    def _step_walk(self, dt):
        wp = self.scenario.waypoints[self._wp_index]
        dx = wp.x - self.x
        dy = wp.y - self.y
        d  = math.sqrt(dx * dx + dy * dy)
        if d <= self.ARRIVAL_THRESHOLD:
            self.x = wp.x
            self.y = wp.y
            self.vx = 0.0
            self.vy = 0.0
            self._start_dwell()
        else:
            scale    = self.speed / d
            self.vx  = dx * scale
            self.vy  = dy * scale
            self.x  += self.vx * dt
            self.y  += self.vy * dt
            self.micro_action = MICRO_STEP

    def _compute_zone(self):
        for zone in self.layout_zones:
            if (zone["x_min"] <= self.x <= zone["x_max"] and
                    zone["y_min"] <= self.y <= zone["y_max"]):
                return zone["id"]
        return "zone_unknown"

    def is_done(self):
        return (self._wp_index == len(self.scenario.waypoints) - 1
                and self._dwelling and self.micro_action == MICRO_STAND)

    def current_waypoint_label(self):
        return self.scenario.waypoints[self._wp_index].label

    def status_str(self):
        return (f"[human_sim] {self.agent_id} | "
                f"pos=({self.x:.2f},{self.y:.2f}) | "
                f"zone={self.current_zone} | "
                f"action={self.micro_action} | "
                f"wp={self.current_waypoint_label()}")