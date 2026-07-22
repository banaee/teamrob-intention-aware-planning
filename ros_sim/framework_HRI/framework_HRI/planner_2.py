#!/usr/bin/env python3
"""
planner_2.py  —  PlannerVisualizer ROS2 node

CHANGES FROM ORIGINAL (Step 5 + human_sim):
    1. New imports: CostConfig, best_ordering, reselect_or_continue,
       should_replan, ExecutorState, ScriptedHuman, SCENARIOS.
    2. New constant: COSTS_PATH, COGNITIVE_PERIOD.
    3. New class: LayoutAdapterFromDict — wraps the already-loaded layout
       dict and provides position_of()/zone_of()/zone_of_pos() interface
       that shared/costs.py expects.
    4. __init__: constructs CostConfig, LayoutAdapterFromDict, human_sim,
       _current_belief, _cognitive_timer. Calls _reorder_remaining_tasks()
       before first _load_next_task().
    5. New method _reorder_remaining_tasks(): calls best_ordering() to
       reorder remaining tasks by cost. Replaces random.shuffle().
    6. _load_next_task(): uses self._current_belief instead of local dummy.
    7. New method _cognitive_tick(): periodic Trigger 3 check (cost delta).
    8. _main_loop(): adds cognitive clock; uses _reorder_remaining_tasks()
       on TASK_DONE and NEEDS_REPLAN; steps human_sim; feeds live human
       position to PRIEST instead of static layout["human"].
    9. publish_human(): uses live self.human_sim.x/y instead of static
       layout["human"] so RViz marker moves.

WHAT IS NOT CHANGED:
    All visualization methods, load_layout(), build_minimal_world_state(),
    PRIEST_CONFIG, DT, MESH_PKG, all publishers, _viz_loop(),
    request_interrupt(), publish_obstacles(), publish_robot(),
    publish_all_object_goals(), publish_target_goal(),
    publish_coffee_machine(), publish_task_label(),
    publish_trajectory_buffered(), _publish_circle(), publish_zones().
"""

import rclpy
from rclpy.node import Node
import numpy as np
import threading
import time
import json
import sys

import jax.numpy as jnp

from geometry_msgs.msg import PoseStamped, Point
from nav_msgs.msg import Path
from visualization_msgs.msg import Marker, MarkerArray

from framework_HRI.local_planner_priest_interrupt import PRIESTLocalPlanner
from framework_HRI.ContinuousExecutor import ActionExecutor
from framework_HRI.human_sim import ScriptedHuman, SCENARIOS          # [NEW]


# --- Repo imports -----------------------------------------------------------
REPO_PATH = "/home/fatemeh/Github_human_robot_codes/Github/teamrob-intention-aware-planning"
if REPO_PATH not in sys.path:
    sys.path.insert(0, REPO_PATH)

from shared.types import Var, Const, BeliefState, WorldState
from shared.types import AbstractPlan, GroundedAction, WorldState, Predicate, ProcessCompletion

from shared.planner import AdaptivePlanner
from shared.domain_knowledge import DomainKnowledgeBase
from shared.replanning import should_replan                             # [NEW]
from shared.meta_planner import (                                       # [NEW]
    best_ordering,
    reselect_or_continue,
    ExecutorState,
)
from shared.costs import CostConfig                                     # [NEW]

from domains.kitting.registry import register_kitting_domain
from domains.kitting.scenarios import scenario_10
# ---------------------------------------------------------------------------


# =============================================================================
# Constants
# =============================================================================

LAYOUT_PATH = "/home/fatemeh/Github_human_robot_codes/Github/teamrob-intention-aware-planning/domains/kitting/env_layout1.json"
COSTS_PATH  = "/home/fatemeh/Github_human_robot_codes/Github/teamrob-intention-aware-planning/costs.yaml"   # [NEW]
CM          = 0.01
MESH_PKG    = "planner"
DT          = 0.1

COGNITIVE_PERIOD = 0.2    # seconds between cognitive clock ticks (5 Hz)

PRIEST_CONFIG = {
    "v_max":             1.0,
    "v_min":             0.02,
    "a_max":             1.0,
    "num_batch":         110,
    "maxiter_mpc":       100,
    "t_fin":             10.0,
    "num":               100,
    "dt_step":           DT,
    "a_obs_1":           1.0,  "b_obs_1": 1.0,
    "a_obs_2":           1.3,  "b_obs_2": 1.3,
    "num_obs_1":         3,
    "num_obs_2":         1,
    "maxiter":           1,
    "maxiter_cem":       12,
    "weight_smoothness": 1.0,
    "weight_track":      0.001,
    "way_point_shape":   1000,
    "v_des":             1.0,
}


# =============================================================================
# Layout loader  (unchanged)
# =============================================================================

def load_layout(path: str) -> dict:
    with open(path, "r") as f:
        raw = json.load(f)

    layout = {}

    r = raw["robots"][0]
    layout["robot"] = {
        "id": r["id"],
        "x":  r["initial_x"] * CM,
        "y":  r["initial_y"] * CM,
    }

    h = raw["humans"][0]
    layout["human"] = {
        "id": h["id"],
        "x":  h["initial_x"] * CM,
        "y":  h["initial_y"] * CM,
    }

    env_objects = raw.get("env_objects", [])

    layout["obstacles"] = [
        {"id": o["id"],
         "x":  o["position"][0] * CM,
         "y":  o["position"][1] * CM}
        for o in env_objects if o["type"] == "obstacle"
    ]

    layout["shelves"] = [
        {"id":              o["id"],
         "x":               o["position"][0] * CM,
         "y":               o["position"][1] * CM,
         "zone":            o.get("zone", ""),
         "orientation_deg": o.get("orientation_deg", 0)}
        for o in env_objects if o["type"] == "shelf"
    ]

    kt_list = [o for o in env_objects if o["type"] == "kitting_table"]
    if kt_list:
        kt = kt_list[0]
        layout["kitting_table"] = {
            "x": kt["position"][0] * CM,
            "y": kt["position"][1] * CM,
        }

    cm_list = [o for o in env_objects if o["type"] == "coffee_machine"]
    if cm_list:
        layout["coffee_machine"] = {
            "x": cm_list[0]["position"][0] * CM,
            "y": cm_list[0]["position"][1] * CM,
        }

    layout["zones"] = [
        {"id":    z["id"],
         "label": z["label"],
         "x_min": z["bounds"]["x_min"] * CM,
         "x_max": z["bounds"]["x_max"] * CM,
         "y_min": z["bounds"]["y_min"] * CM,
         "y_max": z["bounds"]["y_max"] * CM}
        for z in raw.get("zones", [])
    ]

    shelf_map = {s["id"]: s for s in layout["shelves"]}
    layout["items"] = []
    for item in raw.get("items", []):
        shelf_id = item["initial_container"]
        shelf    = shelf_map.get(shelf_id, {})
        layout["items"].append({
            "id":              item["id"],
            "type":            item["type"],
            "shelf_id":        shelf_id,
            "x":               shelf.get("x", 0.0),
            "y":               shelf.get("y", 0.0),
            "orientation_deg": item.get("orientation_deg", 0),
        })

    return layout


# =============================================================================
# Minimal WorldState builder  (unchanged)
# =============================================================================

def build_minimal_world_state(
    robot_x: float, robot_y: float,
    layout:  dict,
    robot_holding: str = None,
) -> WorldState:
    """
    Build a minimal WorldState from current robot position and layout.
    Emits:
        at(robot_0, object_id)    — if robot within 0.4 m of object
        holding(robot_0, item_id) — if robot_holding is set
        obj_at(item_id, location) — item locations from layout
    Will be replaced by world_state_builder_continuous.py once connected.
    """
    from shared.types import Predicate, Const, AgentState

    PROXIMITY = 0.4
    predicates = set()
    robot_id   = layout["robot"]["id"]

    def near(tx, ty):
        return ((robot_x - tx) ** 2 + (robot_y - ty) ** 2) < PROXIMITY ** 2

    for item in layout["items"]:
        if near(item["x"], item["y"]):
            predicates.add(Predicate("at", (Const(robot_id), Const(item["id"]))))

    for shelf in layout["shelves"]:
        if near(shelf["x"], shelf["y"]):
            predicates.add(Predicate("at", (Const(robot_id), Const(shelf["id"]))))

    kt = layout.get("kitting_table")
    if kt and near(kt["x"], kt["y"]):
        predicates.add(Predicate("at", (Const(robot_id), Const("kitting_table"))))

    if robot_holding:
        predicates.add(Predicate("holding", (Const(robot_id), Const(robot_holding))))

    obj_locations = {}
    for item in layout["items"]:
        obj_locations[item["id"]] = item["shelf_id"]
        predicates.add(Predicate("obj_at", (Const(item["id"]), Const(item["shelf_id"]))))

    return WorldState(
        timestamp=time.time(),
        agent_states={
            robot_id: AgentState(
                agent_id=robot_id,
                current_zone="unknown",
                holding=robot_holding,
                current_task=None,
            )
        },
        object_locations=obj_locations,
        object_zones={},
        predicates=predicates,
    )


# =============================================================================
# [NEW] Layout adapter — wraps load_layout() dict for shared/costs.py
# =============================================================================

class LayoutAdapterFromDict:
    """
    Wraps the layout dict produced by load_layout() and provides the
    interface shared/costs.py expects:
        position_of(object_id) → (x, y) in metres
        zone_of(object_id)     → zone_id string
        zone_of_pos(pos)       → zone_id string

    Uses the layout dict already in memory — no second JSON read needed.
    All positions already in metres (load_layout applies CM = 0.01).
    """

    def __init__(self, layout: dict):
        self._layout = layout
        self._pos:  dict = {}
        self._zone: dict = {}

        for shelf in layout.get("shelves", []):
            self._pos[shelf["id"]]  = (shelf["x"], shelf["y"])
            self._zone[shelf["id"]] = shelf.get("zone", "zone_unknown")

        for item in layout.get("items", []):
            self._pos[item["id"]]  = (item["x"], item["y"])
            shelf_id = item.get("shelf_id", "")
            self._zone[item["id"]] = self._zone.get(shelf_id, "zone_unknown")

        kt = layout.get("kitting_table")
        if kt:
            self._pos["kitting_table"]  = (kt["x"], kt["y"])
            self._zone["kitting_table"] = "zone_NW"

        cm = layout.get("coffee_machine")
        if cm:
            self._pos["coffee_machine"]  = (cm["x"], cm["y"])
            self._zone["coffee_machine"] = "zone_SW"

        self.bottlenecks = []   # none in env_layout1 (open warehouse)

    def position_of(self, object_id: str):
        if object_id not in self._pos:
            raise KeyError(
                f"LayoutAdapterFromDict: '{object_id}' not found. "
                f"Known: {list(self._pos.keys())}"
            )
        return self._pos[object_id]

    def zone_of(self, object_id: str) -> str:
        return self._zone.get(object_id, "zone_unknown")

    def zone_of_pos(self, pos) -> str:
        x, y = pos
        for zone in self._layout.get("zones", []):
            if (zone["x_min"] <= x <= zone["x_max"] and
                    zone["y_min"] <= y <= zone["y_max"]):
                return zone["id"]
        return "zone_unknown"


# =============================================================================
# ROS2 Node
# =============================================================================

class PlannerVisualizer(Node):

    def __init__(self):
        super().__init__("planner_visualizer")

        # --- Layout -------------------------------------------------------
        self.layout = load_layout(LAYOUT_PATH)
        self.get_logger().info(
            f"Loaded layout: "
            f"{len(self.layout['obstacles'])} obstacles, "
            f"{len(self.layout['shelves'])} shelves, "
            f"{len(self.layout['items'])} items"
        )

        # --- Robot kinematic state ----------------------------------------
        self.state = (
            self.layout["robot"]["x"],
            self.layout["robot"]["y"],
            0.1, 0.0, 0.0, 0.0,
        )
        self.robot_holding: str = None

        # --- Repo: domain knowledge + planner -----------------------------
        domain_model   = register_kitting_domain()
        self.knowledge = DomainKnowledgeBase.from_domain(domain_model)
        self.planner   = AdaptivePlanner(self.knowledge)

        # --- Repo: get robot task list from scenario_10 -------------------
        robot_agent = next(
            a for a in scenario_10.agents if a.agent_id == "robot_0"
        )
        self.task_queue = list(robot_agent.scheduled_tasks)
        self.task_index  = 0

        # --- [NEW] Cost config + layout adapter ---------------------------
        self.cost_cfg       = CostConfig.from_yaml(COSTS_PATH)
        self.layout_adapter = LayoutAdapterFromDict(self.layout)

        # --- [NEW] Belief state — uniform stub until IR is wired ----------
        # When recognizer.py has a real Bayesian update, replace the
        # self._current_belief assignment in _cognitive_tick() with:
        #     obs = build_observation(self.human_sim, time.time())
        #     self._current_belief = self.recognizer.update(obs, self._current_belief)
        self._current_belief = BeliefState(
            timestamp=time.time(),
            agent_id=self.layout["human"]["id"],
            distribution={},
            most_likely="unknown",
            confidence=0.0,
            predicted_next_actions={},
        )

        # --- [NEW] Scripted human -----------------------------------------
        # Executes the DELIVER_ITEM_item5 scenario by default.
        # Change SCENARIOS["DELIVER_ITEM_item5"] to any other scenario key
        # to test different intention cases:
        #     SCENARIOS["COFFEE_BREAK"]
        #     SCENARIOS["AC_ACTIVATION"]
        #     SCENARIOS["DELIVER_ITEM_item1"]
        #     SCENARIOS["DELIVER_ITEM_item7"]
        # Hadi replaces ScriptedHuman with his real human model when ready.
        # The interface is identical: .x, .y, .vx, .vy, .current_zone,
        # .micro_action, .step(dt).
        # [SCENARIO SELECTOR] ─────────────────────────────────────────────
        # Change the key below to switch between scenarios:
        #
        #   "SCENARIO_RESELECT" — human blocks shelf_5 before robot picks up.
        #                         Robot NOT holding → RESELECT evaluated.
        #                         Robot skips item_5, reorders remaining tasks.
        #                         Start human: (4.0, -1.0) zone_SE
        #
        #   "SCENARIO_WAIT"     — human blocks kitting_table during delivery.
        #                         Robot IS holding item_5 → must WAIT.
        #                         Robot pauses at kitting_table ~7.7s.
        #                         Start human: (-4.0, -3.0) zone_SW
        #
        #   "SCENARIO_COFFEE"   — baseline: human stays in zone_SW, no conflict.
        #   "SCENARIO_AC"       — baseline: human stays in zone_SW, no conflict.
        # ──────────────────────────────────────────────────────────────────
        self.human_sim = ScriptedHuman(
            scenario=SCENARIOS["SCENARIO_RESELECT"],   # ← change this line
            layout_zones=self.layout["zones"],
            speed=0.5,
            agent_id=self.layout["human"]["id"],
        )

        # --- [NEW] Cognitive clock timer ----------------------------------
        self._cognitive_timer   = 0.0
        self._prev_belief       = None
        self._prev_world_state  = None
        self._reselect_cooldown = 0.0
        self._paused            = False   # True during RESELECT pause
        self._pause_timer       = 0.0    # counts down pause duration

        # --- ContinuousExecutor -------------------------------------------
        self.action_executor = ActionExecutor(
            layout=self.layout,
            pick_delay=2.0,
            place_delay=2.0,
        )

        # --- PRIEST -------------------------------------------------------
        self.local_planner    = PRIESTLocalPlanner(PRIEST_CONFIG)
        self.interrupt_active = False
        self.traj_buffer      = None

        # --- [NEW] Apply initial best_ordering before first task ----------
        self._reorder_remaining_tasks()

        # --- Load first task plan -----------------------------------------
        self._load_next_task()

        # --- Publishers ---------------------------------------------------
        self.pose_pub          = self.create_publisher(PoseStamped,  "/robot_pose",          100)
        self.traj_pub          = self.create_publisher(Path,         "/trajectory",           100)
        self.obs_pub           = self.create_publisher(MarkerArray,  "/obstacles",            100)
        self.hum_pub           = self.create_publisher(MarkerArray,  "/humans",               100)
        self.robot_marker_pub  = self.create_publisher(Marker,       "/robot_marker",         100)
        self.goal_pub          = self.create_publisher(Marker,       "/goal_marker",          100)
        self.task_label_pub    = self.create_publisher(Marker,       "/task_label",           100)
        self.path_marker_pub   = self.create_publisher(Marker,       "trajectory_marker",      10)
        self.all_goals_pub     = self.create_publisher(MarkerArray,  "/all_object_goals",     100)
        self.target_goal_pub   = self.create_publisher(MarkerArray,  "/target_goal_marker",   100)
        self.coffee_pub        = self.create_publisher(Marker,       "/coffee_marker",          1)
        self.zone_pub          = self.create_publisher(MarkerArray,  "/zones",                100)
        self.announce_pub      = self.create_publisher(Marker,       "/reselect_announcement", 1)  # [NEW]
        self.human_goal_pub    = self.create_publisher(Marker,       "/human_goal_marker",    100)  # [NEW]

        # --- Threads ------------------------------------------------------
        viz_thread  = threading.Thread(target=self._viz_loop,  daemon=True)
        main_thread = threading.Thread(target=self._main_loop, daemon=True)
        viz_thread.start()
        main_thread.start()

        self.get_logger().info(
            "PlannerVisualizer ready — "
            "AdaptivePlanner + ContinuousExecutor + meta_planner + human_sim"
        )

    # =========================================================================
    # [NEW] Task reordering helper
    # =========================================================================

    def _reorder_remaining_tasks(self) -> None:
        """
        Reorder self.task_queue[task_index:] using best_ordering().
        Called at startup, on TASK_DONE, on NEEDS_REPLAN, after RESELECT.
        With uniform belief (stub), this is geometry-only ordering.
        Once recognizer.py has real updates, this becomes IR-aware.
        """
        remaining = self.task_queue[self.task_index:]
        if not remaining:
            return

        robot_x, robot_y = self.state[0], self.state[1]
        robot_zone = self.layout_adapter.zone_of_pos((robot_x, robot_y))

        new_order, total_cost = best_ordering(
            remaining,
            (robot_x, robot_y),
            robot_zone,
            self._current_belief,
            self.knowledge,
            self.layout_adapter,
            self.cost_cfg,
        )

        self.task_queue[self.task_index:] = new_order

        item_ids = []
        for t in new_order:
            item_const = t.bindings.get(Var("?item"))
            item_ids.append(item_const.value if item_const else "?")

        self.get_logger().info(
            f"[meta_planner] Reordered tasks: {item_ids} "
            f"(est. total: {total_cost:.1f}s)"
        )

    # =========================================================================
    # Task loading  (updated to use self._current_belief)
    # =========================================================================

    def _load_next_task(self) -> bool:
        """
        Load the next task from the queue via AdaptivePlanner.
        Returns True if a task was loaded, False if all done.
        The ORDER of task_queue is set by _reorder_remaining_tasks()
        before this is called.
        """
        if self.task_index >= len(self.task_queue):
            self.get_logger().info("All tasks completed.")
            return False

        task_instance = self.task_queue[self.task_index]

        task_params = {
            var.name: const.value
            for var, const in task_instance.bindings.items()
        }

        world_state = build_minimal_world_state(
            self.state[0], self.state[1], self.layout, self.robot_holding
        )

        # [CHANGED] use self._current_belief instead of local dummy
        plan = self.planner.plan(
            my_intention=task_instance.schema.name,
            task_params=task_params,
            agent_id=self.layout["robot"]["id"],
            belief=self._current_belief,
            world=world_state,
        )

        self.get_logger().info(
            f"[planner] Task {self.task_index + 1}/{len(self.task_queue)}: "
            f"{task_instance.schema.name}({task_params}) → "
            f"{len(plan.actions)} actions: "
            f"{[a.action_name for a in plan.actions]}"
        )

        self.action_executor.load_plan(plan)

        if self.action_executor.current_nav_goal:
            self.local_planner.reset(self.action_executor.current_nav_goal)

        return True

    # =========================================================================
    # [NEW] Cognitive tick — Trigger 3 (cost delta)
    # =========================================================================

    def _cognitive_tick(self, world_state: WorldState) -> None:
        """
        Periodic cognitive update. Called every COGNITIVE_PERIOD seconds.

        Step A: update belief.
            Currently a stub — belief stays uniform.
            When Hadi's recognizer is ready, replace this stub with:
                from continuous_sim.obs_builder import build_observation
                obs = build_observation(self.human_sim, time.time())
                self._current_belief = self.recognizer.update(
                    obs, self._current_belief
                )

        Step B: call should_replan() with Trigger 3 (cost delta).
            Checks whether the human is predicted to block the robot's
            current goal. With uniform belief, P_goal_blocked = 0, so
            this tick is a no-op until Hadi's recognizer is wired in.

        Step C: if Trigger 3 fires, call reselect_or_continue().
        """

        # --- Step A: belief update (stub) ---------------------------------
        # self._current_belief = self.recognizer.update(obs, self._current_belief)

        # Read current nav goal once — used by both the geometric check
        # below and the should_replan() call further down
        nav_goal = self.action_executor.current_nav_goal

        # --- Geometric proximity check with trajectory projection ----------
        # Instead of checking where the human IS now, project their position
        # forward by LOOK_AHEAD_S seconds using their current velocity.
        # This gives the robot advance warning before the human actually
        # arrives at the goal — time to reselect rather than arrive and wait.
        #
        # LOOK_AHEAD_S = how many seconds ahead to project.
        # At human speed 0.5 m/s, 8s projection = 4m lookahead.
        # The robot's travel time to shelf_5 from start is ~9.7s, so
        # projecting 8s forward detects the conflict ~8s before arrival.
        LOOK_AHEAD_S = 8.0

        if nav_goal is not None and self._reselect_cooldown <= 0:

            # Project human position forward
            h_x_now  = self.human_sim.x
            h_y_now  = self.human_sim.y
            h_vx     = self.human_sim.vx
            h_vy     = self.human_sim.vy
            h_x_pred = h_x_now + h_vx * LOOK_AHEAD_S
            h_y_pred = h_y_now + h_vy * LOOK_AHEAD_S

            goal_x = nav_goal["x"]
            goal_y = nav_goal["y"]

            # Distance from PROJECTED human position to goal
            h_dist_pred = ((h_x_pred - goal_x) ** 2 +
                           (h_y_pred - goal_y) ** 2) ** 0.5

            # Also compute current distance — used for logging
            h_dist_now = ((h_x_now - goal_x) ** 2 +
                          (h_y_now - goal_y) ** 2) ** 0.5

            # Only act if human is actually moving toward the goal
            # (dot product of velocity vector and goal direction > 0)
            # This prevents false positives when human is moving away
            dx_to_goal = goal_x - h_x_now
            dy_to_goal = goal_y - h_y_now
            moving_toward = (h_vx * dx_to_goal + h_vy * dy_to_goal) > 0

            if h_dist_pred < self.cost_cfg.block_radius_m and moving_toward:
                holding = self.robot_holding is not None
                self.get_logger().warn(
                    f"[cognitive] PREDICTED BLOCK — "
                    f"human now=({h_x_now:.1f},{h_y_now:.1f}) "
                    f"pred=({h_x_pred:.1f},{h_y_pred:.1f}) "
                    f"goal=({goal_x:.1f},{goal_y:.1f}) "
                    f"pred_dist={h_dist_pred:.1f}m | holding={holding}"
                )
                if holding:
                    self.get_logger().warn("[cognitive] WAIT — holding item, cannot reselect")
                    return
                else:
                    remaining = self.task_queue[self.task_index:]
                    if len(remaining) > 1:
                        current   = remaining[0]
                        rest      = remaining[1:]
                        new_order = rest + [current]
                        self.task_queue[self.task_index:] = new_order

                        item_ids = []
                        for t in new_order:
                            ic = t.bindings.get(Var("?item"))
                            item_ids.append(ic.value if ic else "?")

                        self.get_logger().warn(
                            f"[cognitive] RESELECT — new order: {item_ids}"
                        )

                        self.local_planner.abort()
                        self.interrupt_active = False
                        self._reselect_cooldown = 15.0

                        # --- Pause robot and show announcement ----------------
                        # Freeze all movement for RESELECT_PAUSE_S seconds so
                        # the plan change is clearly visible in RViz.
                        RESELECT_PAUSE_S = 2.5
                        self._paused      = True
                        self._pause_timer = RESELECT_PAUSE_S

                        # Publish "PLAN CHANGED" marker immediately
                        self._publish_reselect_announcement(item_ids, RESELECT_PAUSE_S)

                        self._load_next_task()
                        return
                    else:
                        self.get_logger().warn("[cognitive] WAIT — only one task left")
                        return

        # --- Step B: check for cost-delta trigger -------------------------
        if nav_goal is None:
            return

        robot_x, robot_y = self.state[0], self.state[1]
        robot_zone = self.layout_adapter.zone_of_pos((robot_x, robot_y))

        goal_x = nav_goal["x"]
        goal_y = nav_goal["y"]
        dist   = ((robot_x - goal_x) ** 2 + (robot_y - goal_y) ** 2) ** 0.5
        t_rem  = dist / max(self.cost_cfg.robot_speed, 0.01)

        # Held item shelf — needed for C_cancel when holding
        held_shelf_pos  = None
        held_shelf_zone = None
        if self.robot_holding:
            for item in self.layout["items"]:
                if item["id"] == self.robot_holding:
                    for shelf in self.layout["shelves"]:
                        if shelf["id"] == item["shelf_id"]:
                            held_shelf_pos  = (shelf["x"], shelf["y"])
                            held_shelf_zone = shelf.get("zone", "zone_unknown")
                            break
                    break

        executor_state = ExecutorState(
            robot_pos               = (robot_x, robot_y),
            robot_zone              = robot_zone,
            holding                 = self.robot_holding is not None,
            current_goal_pos        = (goal_x, goal_y),
            current_goal_zone       = self.layout_adapter.zone_of_pos((goal_x, goal_y)),
            estimated_remaining_s   = t_rem,
            held_shelf_pos          = held_shelf_pos,
            held_shelf_zone         = held_shelf_zone,
        )

        trigger = should_replan(
            current_plan   = self.action_executor._plan,
            new_belief     = self._current_belief,
            world          = world_state,
            prev_belief    = self._prev_belief,
            executor_state = executor_state,
            knowledge      = self.knowledge,
            layout         = self.layout_adapter,
            cfg            = self.cost_cfg,
        )

        self._prev_belief      = self._current_belief
        self._prev_world_state = world_state

        if not trigger["replan"]:
            return

        self.get_logger().warn(
            f"[cognitive] Trigger: reason={trigger['reason']} "
            f"score={trigger['score']:.2f}"
        )

        if trigger["reason"] != "cost_delta":
            # Triggers 1 and 2 not yet implemented — do full reload
            self._load_next_task()
            return

        # --- Step C: RESELECT vs WAIT ------------------------------------
        remaining = self.task_queue[self.task_index:]
        decision  = reselect_or_continue(
            executor        = executor_state,
            remaining_tasks = remaining,
            belief          = self._current_belief,
            knowledge       = self.knowledge,
            layout          = self.layout_adapter,
            cfg             = self.cost_cfg,
        )

        self.get_logger().info(f"[cognitive] Decision: {decision['decision']}")

        if decision["decision"] == "RESELECT":
            new_order = decision["new_ordering"]
            self.task_queue[self.task_index:] = new_order

            item_ids = []
            for t in new_order:
                item_const = t.bindings.get(Var("?item"))
                item_ids.append(item_const.value if item_const else "?")

            self.get_logger().warn(
                f"[cognitive] RESELECT — new order: {item_ids}"
            )
            self.interrupt_active = True
            self._load_next_task()
        else:
            self.get_logger().info(
                f"[cognitive] WAIT — {decision.get('wait_s', 0.0):.1f}s"
            )

    # =========================================================================
    # Main loop  (updated)
    # =========================================================================

    def _main_loop(self):
        while rclpy.ok():

            # --- Build world state ----------------------------------------
            world_state = build_minimal_world_state(
                self.state[0], self.state[1],
                self.layout, self.robot_holding,
            )

            # --- Interrupt ------------------------------------------------
            if self.interrupt_active and self.local_planner.status == "RUNNING":
                self.get_logger().warn("[MPC] Abort requested")
                self.local_planner.abort()

            # --- Step executor --------------------------------------------
            exec_status = self.action_executor.step(
                world_state, self.local_planner.status
            )

            self.get_logger().info(
                f"[executor] {self.action_executor.current_task_label()} | "
                f"exec={exec_status} | priest={self.local_planner.status}"
            )

            # --- [NEW] Cognitive clock ------------------------------------
            self._cognitive_timer += DT
            if self._reselect_cooldown > 0:
                self._reselect_cooldown -= DT

            # Count down pause timer — robot freezes during this period
            if self._paused:
                self._pause_timer -= DT
                if self._pause_timer <= 0:
                    self._paused = False
                    self.get_logger().info("[cognitive] Pause ended — resuming execution")
                else:
                    time.sleep(DT)
                    continue   # skip all motion this tick

            if self._cognitive_timer >= COGNITIVE_PERIOD:
                self._cognitive_timer = 0.0
                self._cognitive_tick(world_state)

            # --- Handle executor status -----------------------------------

            if exec_status == "TASK_DONE":
                self.task_index += 1
                self._reorder_remaining_tasks()          # [CHANGED] was nothing
                if not self._load_next_task():
                    self.get_logger().info("All tasks done — stopping.")
                    return
                time.sleep(DT)
                continue

            if exec_status == "NEEDS_REPLAN":
                self.get_logger().warn(
                    "[executor] NEEDS_REPLAN — reordering with meta_planner"
                )
                self._reorder_remaining_tasks()          # [CHANGED] was random.shuffle
                self._load_next_task()
                self.interrupt_active = False
                time.sleep(DT)
                continue

            if exec_status == "NAVIGATING":
                nav_goal = self.action_executor.current_nav_goal
                if nav_goal and self.local_planner.goal != nav_goal:
                    self.local_planner.reset(nav_goal)

                if self.local_planner.status != "RUNNING":
                    time.sleep(DT)
                    continue

                # --- ONE PRIEST STEP --------------------------------------
                obs_x = jnp.array([o["x"] for o in self.layout["obstacles"]])
                obs_y = jnp.array([o["y"] for o in self.layout["obstacles"]])
                n_obs = len(self.layout["obstacles"])

                # [NEW] Step human sim and feed live position to PRIEST
                self.human_sim.step(DT)

                snapshot = {
                    "obs": {
                        "x":  obs_x,
                        "y":  obs_y,
                        "vx": jnp.zeros(n_obs),
                        "vy": jnp.zeros(n_obs),
                    },
                    "humans": {
                        # [CHANGED] live human position instead of static layout value
                        "x":  jnp.array([self.human_sim.x]),
                        "y":  jnp.array([self.human_sim.y]),
                        "vx": jnp.array([self.human_sim.vx]),
                        "vy": jnp.array([self.human_sim.vy]),
                    },
                }

                traj, command, priest_status = self.local_planner.step(
                    self.state, snapshot
                )

                if traj is not None:
                    self.traj_buffer = traj

                if command is not None:
                    vx = float(command[0])
                    vy = float(command[1])
                    ax = float(command[2])
                    ay = float(command[3])
                    x  = self.state[0] + vx * DT
                    y  = self.state[1] + vy * DT
                    self.state = (x, y, vx, vy, ax, ay)

            elif exec_status == "WAITING":
                # [NEW] Still step the human during pick/place delays
                self.human_sim.step(DT)

            time.sleep(DT)

    # =========================================================================
    # Viz loop — 20 Hz  (unchanged)
    # =========================================================================

    def _viz_loop(self):
        while rclpy.ok():
            label = self.action_executor.current_task_label()

            # During a RESELECT pause, overlay the announcement marker
            if self._paused:
                label = "⚠ REPLANNING..."

            # Robot goal — red hollow ring
            nav_goal = self.action_executor.current_nav_goal
            if nav_goal:
                self._publish_circle(
                    nav_goal["x"], nav_goal["y"],
                    self.goal_pub,
                    color=(1.0, 0.0, 0.0),
                    radius=1.0,
                    ns="robot_goal_ring",
                    marker_id=0,
                )

            # Human goal — blue hollow ring at current waypoint target
            wp = self.human_sim.scenario.waypoints[self.human_sim._wp_index]
            self._publish_circle(
                wp.x, wp.y,
                self.human_goal_pub,
                color=(0.0, 0.4, 1.0),
                radius=1.0,
                ns="human_goal_ring",
                marker_id=1,
            )

            self.publish_zones()
            self.publish_obstacles()
            self.publish_robot()
            self.publish_human()
            self.publish_all_object_goals()
            self.publish_target_goal()
            self.publish_coffee_machine()
            self.publish_task_label(label)
            self.publish_trajectory_buffered()

            time.sleep(1.0 / 20.0)

    # =========================================================================
    # Interrupt API  (unchanged)
    # =========================================================================

    def request_interrupt(self, reason: str = "unspecified") -> None:
        if not self.interrupt_active:
            self.get_logger().warn(f"[INTERRUPT] {reason}")
            self.interrupt_active = True

    # =========================================================================
    # Visualization methods — all unchanged except publish_human
    # =========================================================================

    def _publish_reselect_announcement(self, new_order: list, duration_s: float) -> None:
        """
        Publish a large text marker at the robot's current position
        announcing the plan change. Visible in RViz for duration_s seconds.
        The viz_loop will keep republishing it while _paused is True.
        """
        x, y = self.state[0], self.state[1]

        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "reselect_announcement"
        m.id = 0
        m.type = Marker.TEXT_VIEW_FACING
        m.action = Marker.ADD
        m.pose.position.x = float(x)
        m.pose.position.y = float(y)
        m.pose.position.z = 3.0     # above the robot
        m.pose.orientation.w = 1.0
        m.scale.z = 1.2             # large text
        m.color.r = 1.0
        m.color.g = 0.8
        m.color.b = 0.0
        m.color.a = 1.0
        m.text = f"⚠ PLAN CHANGED\nNew order: {' → '.join(new_order)}"
        m.lifetime.sec = int(duration_s) + 3   # stays visible a bit after pause ends
        self.announce_pub.publish(m)

    def _clear_reselect_announcement(self) -> None:
        """Delete the announcement marker from RViz."""
        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "reselect_announcement"
        m.id = 0
        m.action = Marker.DELETE
        self.announce_pub.publish(m)

    def publish_obstacles(self):
        arr = MarkerArray()
        for i, obs in enumerate(self.layout["obstacles"]):
            m = Marker()
            m.header.frame_id = "map"
            m.header.stamp = self.get_clock().now().to_msg()
            m.type = Marker.MESH_RESOURCE
            m.mesh_resource = f"package://{MESH_PKG}/meshes/aws_robomaker_warehouse_ClutteringC_01_visual.DAE"
            m.mesh_use_embedded_materials = True
            m.action = Marker.ADD
            m.pose.position.x = float(obs["x"])
            m.pose.position.y = float(obs["y"])
            m.pose.position.z = 0.05
            m.scale.x = 0.3
            m.scale.y = 0.3
            m.scale.z = 0.6
            m.color.a = 1.0
            m.ns = "obstacles"
            m.id = i
            arr.markers.append(m)
        self.obs_pub.publish(arr)

    def publish_robot(self):
        x, y = self.state[0], self.state[1]

        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.type = Marker.MESH_RESOURCE
        m.mesh_resource = f"package://{MESH_PKG}/meshes/hokuyo.dae"
        m.mesh_use_embedded_materials = True
        m.action = Marker.ADD
        m.pose.position.x = float(x)
        m.pose.position.y = float(y)
        m.pose.position.z = 0.0
        m.pose.orientation.w = 1.0
        m.scale.x = 7.0
        m.scale.y = 7.0
        m.scale.z = 3.0
        m.color.a = 1.0
        m.id = 0
        m.ns = "robot"
        self.robot_marker_pub.publish(m)

        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = m.header.stamp
        pose.pose.position.x = float(x)
        pose.pose.position.y = float(y)
        pose.pose.orientation.w = 1.0
        self.pose_pub.publish(pose)

    def publish_human(self):
        # [CHANGED] use live human_sim position so RViz marker moves
        x = self.human_sim.x
        y = self.human_sim.y

        # [CHANGED] human always faces toward their final goal.
        # Using final_goal (kitting_table for deliver tasks, machine for others)
        # is more stable than velocity-based heading which flickers when
        # the human is standing still or changing direction between waypoints.
        # The walk.dae mesh's forward axis is +X at zero rotation,
        # so atan2(dy, dx) gives the correct yaw with no offset needed.
        dx = self.human_sim.final_goal_x - x
        dy = self.human_sim.final_goal_y - y
        if abs(dx) > 0.01 or abs(dy) > 0.01:
            heading_rad = np.arctan2(dy, dx)
        else:
            heading_rad = 0.0   # already at final goal — face right as default

        half = heading_rad / 2.0
        qz   = float(np.sin(half))
        qw   = float(np.cos(half))

        arr = MarkerArray()
        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.type = Marker.MESH_RESOURCE
        m.mesh_resource = f"package://{MESH_PKG}/meshes/walk.dae"
        m.mesh_use_embedded_materials = True
        m.action = Marker.ADD
        m.pose.position.x = float(x)
        m.pose.position.y = float(y)
        m.pose.orientation.z = qz
        m.pose.orientation.w = qw
        m.scale.x = 0.8
        m.scale.y = 0.8
        m.scale.z = 1.2
        m.color.r = 0.0
        m.color.g = 0.2
        m.color.b = 1.0
        m.color.a = 1.0
        m.ns = "humans"
        m.id = 0
        arr.markers.append(m)
        self.hum_pub.publish(arr)

    def publish_all_object_goals(self):
        arr = MarkerArray()
        for i, item in enumerate(self.layout["items"]):
            x = item["x"]
            y = item["y"]

            m = Marker()
            m.header.frame_id = "map"
            m.header.stamp = self.get_clock().now().to_msg()
            m.ns = "all_object_goals"
            m.id = i
            m.type = Marker.MESH_RESOURCE
            m.mesh_resource = f"package://{MESH_PKG}/meshes/aws_robomaker_warehouse_ShelfE_01_visual.DAE"
            m.mesh_use_embedded_materials = True
            m.action = Marker.ADD
            m.pose.position.x = float(x)
            m.pose.position.y = float(y)
            m.pose.position.z = 0.05
            m.pose.orientation.x = 0.0
            m.pose.orientation.y = 0.0
            angle_deg = item.get("orientation_deg", 0)
            half_rad  = np.radians(angle_deg) / 2
            m.pose.orientation.z = float(np.sin(half_rad))
            m.pose.orientation.w = float(np.cos(half_rad))
            m.scale.x = 0.3
            m.scale.y = 0.3
            m.scale.z = 0.8
            m.color.a = 1.0
            arr.markers.append(m)

            t = Marker()
            t.header.frame_id = "map"
            t.header.stamp = m.header.stamp
            t.ns = "all_object_goal_labels"
            t.id = 1000 + i
            t.type = Marker.TEXT_VIEW_FACING
            t.action = Marker.ADD
            if x <= 0:
                t.pose.position.x = float(x - 1.5)
                t.pose.position.y = float(y - 0.4)
            else:
                t.pose.position.x = float(x + 1.5)
                t.pose.position.y = float(y + 0.4)
            t.pose.position.z = 0.6
            t.scale.z = 0.35
            t.color.r = 0.0
            t.color.g = 0.0
            t.color.b = 1.0
            t.color.a = 1.0
            t.text = f"{item['id']}"
            arr.markers.append(t)

        self.all_goals_pub.publish(arr)

    def publish_target_goal(self):
        x = self.layout["kitting_table"]["x"]
        y = self.layout["kitting_table"]["y"]
        arr = MarkerArray()

        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "delivery_point"
        m.id = 0
        m.type = Marker.MESH_RESOURCE
        m.mesh_resource = f"package://{MESH_PKG}/meshes/aws_robomaker_warehouse_DeskC_01_visual.DAE"
        m.mesh_use_embedded_materials = True
        m.action = Marker.ADD
        m.pose.position.x = float(x)
        m.pose.position.y = float(y)
        m.pose.position.z = 0.05
        m.pose.orientation.z = float(np.sin(np.radians(-90) / 2))
        m.pose.orientation.w = float(np.cos(np.radians(-90) / 2))
        m.scale.x = 0.8
        m.scale.y = 0.8
        m.scale.z = 0.5
        m.color.a = 1.0
        arr.markers.append(m)

        t = Marker()
        t.header.frame_id = "map"
        t.header.stamp = m.header.stamp
        t.ns = "delivery_point_label"
        t.id = 1
        t.type = Marker.TEXT_VIEW_FACING
        t.action = Marker.ADD
        t.pose.position.x = float(x + 0.4)
        t.pose.position.y = float(y + 0.4)
        t.pose.position.z = 0.6
        t.scale.z = 0.45
        t.color.r = 1.0
        t.color.g = 0.2
        t.color.b = 0.6
        t.color.a = 1.0
        t.text = "Kitting Table"
        arr.markers.append(t)
        self.target_goal_pub.publish(arr)

    def publish_coffee_machine(self):
        x = self.layout["coffee_machine"]["x"]
        y = self.layout["coffee_machine"]["y"]

        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "coffee_machine"
        m.id = 0
        m.type = Marker.CUBE
        m.action = Marker.ADD
        m.pose.position.x = float(x)
        m.pose.position.y = float(y)
        m.pose.position.z = 0.5
        m.pose.orientation.w = 1.0
        m.scale.x = 0.6
        m.scale.y = 0.6
        m.scale.z = 1.2
        m.color.r = 0.4
        m.color.g = 0.25
        m.color.b = 0.1
        m.color.a = 1.0
        self.coffee_pub.publish(m)

        t = Marker()
        t.header.frame_id = "map"
        t.header.stamp = m.header.stamp
        t.ns = "coffee_machine_label"
        t.id = 1
        t.type = Marker.TEXT_VIEW_FACING
        t.action = Marker.ADD
        t.pose.position.x = float(x - 1.0)
        t.pose.position.y = float(y - 1.0)
        t.pose.position.z = 1.8
        t.scale.z = 0.5
        t.color.r = 0.7
        t.color.g = 0.7
        t.color.b = 0.0
        t.color.a = 1.0
        t.text = "Coffee Machine"
        self.coffee_pub.publish(t)

    def publish_task_label(self, text: str):
        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "task_label"
        m.id = 0
        m.type = Marker.TEXT_VIEW_FACING
        m.action = Marker.ADD
        m.pose.position.x = 0.0
        m.pose.position.y = 10.0
        m.pose.position.z = 3.0
        m.scale.z = 0.8
        m.color.r = 1.0
        m.color.g = 0.0
        m.color.b = 0.0
        m.color.a = 1.0
        m.text = text
        self.task_label_pub.publish(m)

    def publish_trajectory_buffered(self):
        if self.traj_buffer is None:
            return
        x_best, y_best = self.traj_buffer

        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "trajectory_thick"
        m.id = 0
        m.type = Marker.LINE_STRIP
        m.action = Marker.ADD
        m.scale.x = 0.15
        m.color.r = 1.0
        m.color.g = 0.0
        m.color.b = 0.0
        m.color.a = 1.0
        for x, y in zip(np.array(x_best), np.array(y_best)):
            pt = Point()
            pt.x = float(x)
            pt.y = float(y)
            pt.z = 0.0
            m.points.append(pt)
        self.path_marker_pub.publish(m)

        path = Path()
        path.header.frame_id = "map"
        path.header.stamp = m.header.stamp
        for x, y in zip(np.array(x_best), np.array(y_best)):
            p = PoseStamped()
            p.pose.position.x = float(x)
            p.pose.position.y = float(y)
            p.pose.orientation.w = 1.0
            path.poses.append(p)
        self.traj_pub.publish(path)

    def _publish_circle(self, x, y, pub, color=(1.0, 0.0, 0.0), radius=1.6, ns="goal_ring", marker_id=0):
        """
        Publish a hollow circle (ring) as a LINE_STRIP marker.
        Radius is twice the original 0.8 cylinder = 1.6m.
        No fill — only the outline is drawn in the given colour.
        """
        import math
        N_POINTS = 36   # number of points around the circle
        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.type = Marker.LINE_STRIP
        m.action = Marker.ADD
        m.ns = ns
        m.id = marker_id
        m.pose.orientation.w = 1.0
        m.scale.x = 0.08   # line width in metres
        m.color.r = color[0]
        m.color.g = color[1]
        m.color.b = color[2]
        m.color.a = 1.0

        for i in range(N_POINTS + 1):   # +1 to close the ring
            angle = 2.0 * math.pi * i / N_POINTS
            pt = Point()
            pt.x = float(x) + radius * math.cos(angle)
            pt.y = float(y) + radius * math.sin(angle)
            pt.z = 0.05
            m.points.append(pt)

        pub.publish(m)

    ZONE_COLORS = {
        "zone_NW": (0.2, 0.6, 1.0, 0.15),
        "zone_NE": (0.2, 1.0, 0.4, 0.15),
        "zone_SW": (1.0, 0.6, 0.2, 0.15),
        "zone_SE": (1.0, 0.2, 0.4, 0.15),
    }

    def publish_zones(self):
        arr = MarkerArray()
        for i, zone in enumerate(self.layout["zones"]):
            cx = (zone["x_min"] + zone["x_max"]) / 2.0
            cy = (zone["y_min"] + zone["y_max"]) / 2.0
            sx = abs(zone["x_max"] - zone["x_min"])
            sy = abs(zone["y_max"] - zone["y_min"])
            r, g, b, a = self.ZONE_COLORS.get(zone["id"], (0.5, 0.5, 0.5, 0.15))

            m = Marker()
            m.header.frame_id = "map"
            m.header.stamp = self.get_clock().now().to_msg()
            m.ns = "zones"
            m.id = i
            m.type = Marker.CUBE
            m.action = Marker.ADD
            m.pose.position.x = float(cx)
            m.pose.position.y = float(cy)
            m.pose.position.z = -0.05
            m.pose.orientation.w = 1.0
            m.scale.x = float(sx)
            m.scale.y = float(sy)
            m.scale.z = 0.01
            m.color.r = r
            m.color.g = g
            m.color.b = b
            m.color.a = a
            arr.markers.append(m)

            t = Marker()
            t.header.frame_id = "map"
            t.header.stamp = m.header.stamp
            t.ns = "zone_labels"
            t.id = 100 + i
            t.type = Marker.TEXT_VIEW_FACING
            t.action = Marker.ADD
            t.pose.position.x = float(zone["x_min"] + 0.2)
            t.pose.position.y = float(zone["y_max"] - 0.2)
            t.pose.position.z = 0.3
            t.scale.z = 0.25
            t.color.r = r
            t.color.g = g
            t.color.b = b
            t.color.a = 1.0
            t.text = zone["label"]
            arr.markers.append(t)

        self.zone_pub.publish(arr)


# =============================================================================
# Entry point  (unchanged)
# =============================================================================

def main(args=None):
    rclpy.init(args=args)
    node = PlannerVisualizer()
    rclpy.spin(node)


if __name__ == "__main__":
    main()