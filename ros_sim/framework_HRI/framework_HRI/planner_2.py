#!/usr/bin/env python3

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


# --- Repo imports -----------------------------------------------------------
# Add repo to path so shared/ and domains/ are importable
REPO_PATH = "/home/fatemeh/Github_human_robot_codes/Github/teamrob-intention-aware-planning"
if REPO_PATH not in sys.path:
    sys.path.insert(0, REPO_PATH)

from shared.types import Var, Const, BeliefState, WorldState
from shared.planner import AdaptivePlanner
from shared.domain_knowledge import DomainKnowledgeBase
from domains.kitting.registry import register_kitting_domain
from domains.kitting.scenarios import scenario_10
# ---------------------------------------------------------------------------

# =============================================================================
# Constants
# =============================================================================

LAYOUT_PATH = "/home/fatemeh/Github_human_robot_codes/Github/teamrob-intention-aware-planning/domains/kitting/env_layout1.json"
CM       = 0.01
MESH_PKG = "planner"
DT       = 0.1

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
# Layout loader
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
# Minimal WorldState builder
# (will be replaced by world_state_builder_continuous.py later)
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
    This is enough for ContinuousExecutor to check completion predicates.
    Will be replaced by world_state_builder_continuous.py once connected.
    """
    from shared.types import Predicate, Const, AgentState

    PROXIMITY = 0.4
    predicates = set()
    robot_id   = layout["robot"]["id"]

    # at() predicates — check robot proximity to all items and shelves
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

    # holding() predicate
    if robot_holding:
        predicates.add(Predicate("holding", (Const(robot_id), Const(robot_holding))))

    # obj_at() predicates — items at their initial locations
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
        self.robot_holding: str = None   # item_id or None

        # --- Repo: domain knowledge + planner -----------------------------
        domain_model   = register_kitting_domain()
        self.knowledge = DomainKnowledgeBase.from_domain(domain_model)
        self.planner   = AdaptivePlanner(self.knowledge)

        # --- Repo: get robot task list from scenario_10 -------------------
        # scenario_10 robot_0: deliver_item(item_5), deliver_item(item_1), deliver_item(item_7)
        robot_agent = next(
            a for a in scenario_10.agents if a.agent_id == "robot_0"
        )
        self.task_queue = list(robot_agent.scheduled_tasks)  # list of TaskInstance
        self.task_index  = 0

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

        # --- Threads ------------------------------------------------------
        viz_thread  = threading.Thread(target=self._viz_loop,  daemon=True)
        main_thread = threading.Thread(target=self._main_loop, daemon=True)
        viz_thread.start()
        main_thread.start()

        self.get_logger().info("PlannerVisualizer ready — using AdaptivePlanner + ContinuousExecutor")

    # =========================================================================
    # Task loading — uses AdaptivePlanner to get AbstractPlan from repo
    # =========================================================================

    def _load_next_task(self) -> bool:
        """
        Load the next task from the queue via AdaptivePlanner.
        Returns True if a task was loaded, False if all done.
        """
        if self.task_index >= len(self.task_queue):
            self.get_logger().info("All tasks completed.")
            return False

        task_instance = self.task_queue[self.task_index]

        # Convert TaskInstance bindings to Dict[str, str] for planner
        task_params = {
            var.name: const.value
            for var, const in task_instance.bindings.items()
        }

        # Build a minimal world state for planning
        world_state = build_minimal_world_state(
            self.state[0], self.state[1], self.layout, self.robot_holding
        )

        # Dummy belief state — IR not connected yet
        belief = BeliefState(
            timestamp=time.time(),
            agent_id=self.layout["human"]["id"],
            distribution={},
            most_likely="unknown",
            confidence=0.0,
        )

        # Get AbstractPlan from repo's planner
        plan = self.planner.plan(
            my_intention=task_instance.schema.name,
            task_params=task_params,
            agent_id=self.layout["robot"]["id"],
            belief=belief,
            world=world_state,
        )

        self.get_logger().info(
            f"[planner] Task {self.task_index + 1}/{len(self.task_queue)}: "
            f"{task_instance.schema.name}({task_params}) → "
            f"{len(plan.actions)} actions: "
            f"{[a.action_name for a in plan.actions]}"
        )

        # Load into executor
        self.action_executor.load_plan(plan)

        # Reset PRIEST for first move_to goal
        if self.action_executor.current_nav_goal:
            self.local_planner.reset(self.action_executor.current_nav_goal)

        return True

    # =========================================================================
    # Main loop
    # =========================================================================

    def _main_loop(self):
        while rclpy.ok():

            # --- Build world state for completion checking -----------------
            world_state = build_minimal_world_state(
                self.state[0], self.state[1],
                self.layout, self.robot_holding,
            )

            # --- Interrupt -------------------------------------------------
            if self.interrupt_active and self.local_planner.status == "RUNNING":
                self.get_logger().warn("[MPC] Abort requested")
                self.local_planner.abort()

            # --- Step executor ---------------------------------------------
            exec_status = self.action_executor.step(world_state, self.local_planner.status)

            self.get_logger().info(
                f"[executor] {self.action_executor.current_task_label()} | "
                f"exec={exec_status} | priest={self.local_planner.status}"
            )

            # --- Handle executor status ------------------------------------

            if exec_status == "TASK_DONE":
                # Advance to next task
                self.task_index += 1
                if not self._load_next_task():
                    self.get_logger().info("All tasks done — stopping.")
                    return
                time.sleep(DT)
                continue

            if exec_status == "NEEDS_REPLAN":
                # PRIEST was interrupted — for now reshuffle tasks
                self.get_logger().warn("[executor] NEEDS_REPLAN — reshuffling remaining tasks")
                remaining = self.task_queue[self.task_index:]
                import random
                random.shuffle(remaining)
                self.task_queue[self.task_index:] = remaining
                self._load_next_task()
                self.interrupt_active = False
                time.sleep(DT)
                continue

            if exec_status == "NAVIGATING":
                # Executor wants us to navigate — check if goal changed
                nav_goal = self.action_executor.current_nav_goal
                if nav_goal and self.local_planner.goal != nav_goal:
                    self.local_planner.reset(nav_goal)

                if self.local_planner.status != "RUNNING":
                    time.sleep(DT)
                    continue

                # --- ONE PRIEST STEP ---------------------------------------
                obs_x  = jnp.array([o["x"] for o in self.layout["obstacles"]])
                obs_y  = jnp.array([o["y"] for o in self.layout["obstacles"]])
                n_obs  = len(self.layout["obstacles"])
                snapshot = {
                    "obs": {
                        "x":  obs_x,
                        "y":  obs_y,
                        "vx": jnp.zeros(n_obs),
                        "vy": jnp.zeros(n_obs),
                    },
                    "humans": {
                        "x":  jnp.array([self.layout["human"]["x"]]),
                        "y":  jnp.array([self.layout["human"]["y"]]),
                        "vx": jnp.array([0.0]),
                        "vy": jnp.array([0.0]),
                    },
                }

                traj, command, priest_status = self.local_planner.step(
                    self.state, snapshot
                )

                if traj is not None:
                    self.traj_buffer = traj

                # Euler integration
                if command is not None:
                    vx = float(command[0])
                    vy = float(command[1])
                    ax = float(command[2])
                    ay = float(command[3])
                    x  = self.state[0] + vx * DT
                    y  = self.state[1] + vy * DT
                    self.state = (x, y, vx, vy, ax, ay)

            elif exec_status == "WAITING":
                # Pick or place delay — robot holds position
                pass

            time.sleep(DT)

    # =========================================================================
    # Viz loop — 20 Hz
    # =========================================================================

    def _viz_loop(self):
        while rclpy.ok():
            label = self.action_executor.current_task_label()

            nav_goal = self.action_executor.current_nav_goal
            if nav_goal:
                self._publish_circle(nav_goal["x"], nav_goal["y"], self.goal_pub)

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
    # Interrupt API
    # =========================================================================

    def request_interrupt(self, reason: str = "unspecified") -> None:
        if not self.interrupt_active:
            self.get_logger().warn(f"[INTERRUPT] {reason}")
            self.interrupt_active = True

    # =========================================================================
    # Visualization methods — unchanged from previous version
    # =========================================================================

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
        x = self.layout["human"]["x"]
        y = self.layout["human"]["y"]

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
        m.pose.orientation.z = float(np.sin(np.radians(-90.0 / 2)))
        m.pose.orientation.w = float(np.cos(np.radians(-90.0 / 2)))
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

    def _publish_circle(self, x, y, pub, color=(1.0, 0.0, 0.0)):
        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.type = Marker.CYLINDER
        m.action = Marker.ADD
        m.pose.position.x = float(x)
        m.pose.position.y = float(y)
        m.pose.orientation.w = 1.0
        m.scale.x = 0.8
        m.scale.y = 0.8
        m.scale.z = 0.2
        m.color.r = color[0]
        m.color.g = color[1]
        m.color.b = color[2]
        m.color.a = 1.0
        m.id = 0
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
# Entry point
# =============================================================================

def main(args=None):
    rclpy.init(args=args)
    node = PlannerVisualizer()
    rclpy.spin(node)


if __name__ == "__main__":
    main()