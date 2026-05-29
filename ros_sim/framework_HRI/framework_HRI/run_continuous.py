#!/usr/bin/env python3
"""
continuous_sim/run_continuous.py

PURPOSE:
    Main entry point for the continuous simulation backend.
    Replaces planner_2.py (PlannerVisualizer) using world.py as ground truth.

WHAT CHANGED vs planner_2.py:
    - Robot state lives in world.robot  (was self.state tuple)
    - Human state lives in world.human  (was self.world["humans"] JAX dict)
    - Obstacles live in world._obs_x/y  (was self.world["obs"] JAX dict)
    - world.step(command) replaces the inline Euler integration in main_loop
    - world.update_humans() is gone — world.step() calls it internally
    - world_lock is gone — world is only written by main_loop thread,
      only read by viz thread (race is benign: floats are atomic on CPython)
    - All visualization methods read from world.* instead of self.state / self.world

WHAT IS IDENTICAL to planner_2.py:
    - All RViz publish methods (robot, human, obstacles, trajectory, labels, meshes)
    - TaskPlanner import and usage
    - PRIESTLocalPlanner import and usage
    - Main loop structure (PICK_WAIT / PLACE_WAIT / GOTO / INTERRUPTED / REACHED)
    - Interrupt API (request_interrupt / interrupt_active flag)
    - All ROS2 publisher topics and QoS

NEXT STEPS (not yet connected):
    - world_state_builder_continuous.py  reads world.* → WorldState
    - obs_builder_continuous.py          reads world.human → Observation
    - shared/recognizer.py               consumes Observation → BeliefState
    - shared/replanning.py               consumes BeliefState → interrupt signal
    Those will replace the hardcoded interrupt rules below.
"""

import threading
import time
import os

import numpy as np
import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Duration
from geometry_msgs.msg import Point, PoseStamped
from nav_msgs.msg import Path
from visualization_msgs.msg import Marker, MarkerArray

from framework_HRI.local_planner_priest_interrupt import PRIESTLocalPlanner
from framework_HRI.task_planner_interrupt import TaskPlanner
from framework_HRI.world_con import ContinuousWorld, HumanWaypoint

from ament_index_python.packages import get_package_share_directory



# =============================================================================
# Configuration — mirrors planner_2.py __init__ values exactly

# =============================================================================

PRIEST_CONFIG = {
    "v_max":             1.0,
    "v_min":             0.02,
    "a_max":             1.0,
    "num_batch":         110,
    "maxiter_mpc":       100,
    "t_fin":             10.0,
    "num":               100,
    "dt_step":           0.1,
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

# Tasks — identical to planner_2.py lines 75-84
TASKS = [
    {"object": (-10.0,  3.0), "target": (-2.0, 6.0)},
    {"object": (-10.0, -3.0), "target": (-2.0, 6.0)},
    {"object": (-10.0,  0.0), "target": (-2.0, 6.0)},
    {"object": ( 10.0,  3.0), "target": (-2.0, 6.0)},
    {"object": ( 10.0, -3.0), "target": (-2.0, 6.0)},
    {"object": ( 10.0,  0.0), "target": (-2.0, 6.0)},
    {"object": ( -7.0, -5.0), "target": (-2.0, 6.0)},
    {"object": (  3.0, -5.0), "target": (-2.0, 6.0)},
]

# Human scripted path — replicates planner_2.py lines 122-132
HUMAN_SCRIPT = [
    HumanWaypoint(x=-9.5, y=-3.0, hold_s=15.0, move_label="step", arrive_label="stand"),
    HumanWaypoint(x= 5.0, y=-5.0, hold_s= 0.0, move_label="step", arrive_label="stand"),
]

# Layout file — adjust path if needed
LAYOUT_PATH = "/home/fatemeh/Github_human_robot_codes/Github/teamrob-intention-aware-planning/domains/kitting/env_layout1.json"

# Simulation timestep (must match PRIEST_CONFIG["dt_step"])
DT = 0.1

# Visualization rate
VIZ_HZ = 20.0


# =============================================================================
# ROS2 Node
# =============================================================================

class ContinuousSimNode(Node):
    """
    ROS2 node for the continuous simulation.
    Replaces PlannerVisualizer from planner_2.py.
    """

    def __init__(self):
        super().__init__("continuous_sim")

        # ----- World (ground truth) --------------------------------------
        self.world = ContinuousWorld(
            layout_path=LAYOUT_PATH,
            dt=DT,
            human_speed=0.15,
            human_arrival_eps=0.2,
        )
        self.world.set_human_script(HUMAN_SCRIPT)

        # ----- Local planner (PRIEST) ------------------------------------
        self.local_planner = PRIESTLocalPlanner(PRIEST_CONFIG)

        # ----- Task planner ----------------------------------------------
        self.task_planner = TaskPlanner(tasks=TASKS)

        # ----- Interrupt state -------------------------------------------
        # SOURCE: planner_2.py lines 27, 93-100
        self.interrupt_active   = False
        self.interrupted_rules  = set()
        self.mpc_iter           = 0
        self.interruption_threshold = 30   # demo value

        # ----- Trajectory buffer for viz thread --------------------------
        # Written by main_loop, read by viz_loop — CPython GIL makes this safe
        self.traj_buffer = None

        # ----- ROS2 publishers -------------------------------------------
        # Identical topics to planner_2.py lines 31-43
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
        self.wait_msg_pub      = self.create_publisher(Marker,       "/wait_message",          10)
        self.coffee_pub        = self.create_publisher(Marker,       "/coffee_marker",          1)

        # ----- Set first goal and start PRIEST ---------------------------
        goal = self.task_planner.current_goal()
        self.local_planner.reset(goal)

        # ----- Threads ---------------------------------------------------
        viz_thread = threading.Thread(target=self._viz_loop, daemon=True)
        viz_thread.start()

        main_thread = threading.Thread(target=self._main_loop, daemon=True)
        main_thread.start()

    # =========================================================================
    # Interrupt API — same interface as planner_2.py
    # =========================================================================

    def request_interrupt(self, reason: str = "unspecified") -> None:
        if not self.interrupt_active:
            self.get_logger().warn(f"[INTERRUPT REQUESTED] {reason}")
            self.interrupt_active = True

    # =========================================================================
    # Main loop — port of planner_2.py main_loop() lines 431-567
    # Key change: world.step(command) replaces inline Euler + update_humans()
    # =========================================================================

    def _main_loop(self) -> None:

        while rclpy.ok():

            # ------------------------------------------------------------------
            # WAIT phases — robot holds, task planner counts down delays
            # SOURCE: planner_2.py lines 438-443
            # ------------------------------------------------------------------
            if self.task_planner.phase in ["PICK_WAIT", "PLACE_WAIT"]:
                self._handle_pick_place_interrupt()
                self.get_logger().info(f"Waiting... phase={self.task_planner.phase}")
                self.task_planner.update()
                self.world.step(None)          # hold robot, still advance human
                time.sleep(DT)
                continue

            # ------------------------------------------------------------------
            # All tasks finished
            # SOURCE: planner_2.py lines 449-451
            # ------------------------------------------------------------------
            if self.task_planner.task_index >= len(self.task_planner.tasks):
                self.get_logger().info("All tasks completed.")
                return

            goal = self.task_planner.current_goal()
            if goal is None:
                self.task_planner.update()
                self.world.step(None)
                time.sleep(DT)
                continue

            # ------------------------------------------------------------------
            # Fire abort if interrupt was requested
            # SOURCE: planner_2.py lines 463-465
            # ------------------------------------------------------------------
            if self.interrupt_active and self.local_planner.status == "RUNNING":
                self.get_logger().warn("[MPC] Abort requested")
                self.local_planner.abort()

            # ------------------------------------------------------------------
            # Handle INTERRUPTED status
            # SOURCE: planner_2.py lines 470-513
            # ------------------------------------------------------------------
            if self.local_planner.status == "INTERRUPTED":

                task_id = self.task_planner.current_task_id()
                phase   = self.task_planner.phase
                self.get_logger().warn(f"[INTERRUPTED] task_id={task_id} phase={phase}")

                time.sleep(5)

                if phase == "GOTO_OBJECT":
                    self.get_logger().info("[RECOVERY] GOTO_OBJECT → reshuffle tasks")
                    self.task_planner.reshuffle_unfinished_tasks_randomly()
                    task_ids = [t["id"] for t in self.task_planner.tasks]
                    self.get_logger().info(f"[TASK ORDER AFTER RESHUFFLE] {task_ids}")
                    time.sleep(5)
                    self.interrupt_active = False
                    self.mpc_iter = 0

                elif phase == "GOTO_TARGET":
                    self.get_logger().info("[RECOVERY] GOTO_TARGET → cancellation")
                    self.task_planner.start_cancellation()
                    new_goal = self.task_planner.current_goal()
                    if new_goal is None:
                        self.get_logger().warn("[RECOVERY] No goal after cancellation.")
                        time.sleep(0.1)
                        continue
                    self.local_planner.reset(new_goal)
                    self.interrupt_active = False
                    self.mpc_iter = 0

                new_goal = self.task_planner.current_goal()
                self.local_planner.reset(new_goal)
                continue

            # ------------------------------------------------------------------
            # Re-arm planner when REACHED (needed between goal phases)
            # SOURCE: planner_2.py lines 519-521
            # ------------------------------------------------------------------
            if self.local_planner.status == "REACHED":
                self.local_planner.reset(goal)
                self.mpc_iter = 0

            if self.local_planner.goal is None:
                self.get_logger().warn("[MPC] No active goal, skipping step")
                time.sleep(0.1)
                continue

            # ------------------------------------------------------------------
            # ONE MPC ITERATION
            # SOURCE: planner_2.py lines 529-557
            # Change: world.get_priest_snapshot() replaces world_snapshot dict
            #         world.step(command) replaces inline Euler + update_humans()
            # ------------------------------------------------------------------
            t_start = time.time()

            snapshot = self.world.get_priest_snapshot()
            state    = self.world.get_robot_state_tuple()

            traj, command, status = self.local_planner.step(state, snapshot)

            comp_ms = (time.time() - t_start) * 1000
            self.get_logger().info(
                f"[TASK {self.task_planner.current_task_id()}] "
                f"phase={self.task_planner.phase} | "
                f"MPC={comp_ms:.1f} ms | status={status}"
            )

            self.mpc_iter += 1

            # Buffer trajectory for viz thread
            if traj is not None:
                self.traj_buffer = traj

            # Advance world — integrates command and advances human script
            self.world.step(command)

            # ------------------------------------------------------------------
            # Goal reached → advance task planner
            # SOURCE: planner_2.py lines 563-565
            # ------------------------------------------------------------------
            if status == "REACHED":
                self.get_logger().info("Reached goal!")
                self.task_planner.advance()

            time.sleep(DT)

    # =========================================================================
    # Pick/place interrupt handler
    # SOURCE: planner_2.py lines 203-217
    # =========================================================================

    def _handle_pick_place_interrupt(self) -> None:
        if not self.interrupt_active:
            return
        if self.task_planner.phase not in ["PICK_WAIT", "PLACE_WAIT"]:
            return
        self.get_logger().info(
            f"Interrupt during {self.task_planner.phase}: waiting 10 s"
        )
        self._publish_wait_message("wait for 10 seconds")
        time.sleep(10)
        self.interrupt_active = False

    # =========================================================================
    # Visualization loop — 20 Hz, separate thread
    # SOURCE: planner_2.py lines 385-426
    # Change: reads world.robot / world.human instead of self.state / self.world
    # =========================================================================

    def _viz_loop(self) -> None:
        rate = 1.0 / VIZ_HZ

        while rclpy.ok():
            goal     = self.task_planner.current_goal()
            task_idx = self.task_planner.task_index
            phase    = self.task_planner.phase
            n_tasks  = len(self.task_planner.tasks)
            task_id  = self.task_planner.current_task_id()

            if goal is not None:
                self._publish_circle(goal["x"], goal["y"], self.goal_pub,
                                     r=0.3, color=(1.0, 0.0, 0.0))

            if self.local_planner.status == "INTERRUPTED":
                label = f"⚠ INTERRUPTED — TASK ID: {task_id} — Phase: {phase}"
            elif task_idx >= n_tasks:
                label = "ALL TASKS COMPLETED"
            else:
                label = f"TASK ID: {task_id} — Task Counter: {task_idx+1}/{n_tasks} — {phase}"

            self._publish_task_label(label)
            self._publish_robot_circle()
            self._publish_robot_pose()
            self._publish_trajectory_buffered()
            self._publish_obstacles()
            self._publish_humans()
            self._publish_all_object_goals()
            self._publish_target_goal_once()
            self._publish_coffee_machine()

            time.sleep(rate)

    # =========================================================================
    # RViz publish methods
    # SOURCE: planner_2.py lines 573-778 — identical logic,
    #         reads from world.robot / world.human instead of self.state / self.world
    # =========================================================================

    def _publish_robot_pose(self) -> None:
        msg = PoseStamped()
        msg.header.frame_id = "map"
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.position.x = float(self.world.robot.x)
        msg.pose.position.y = float(self.world.robot.y)
        msg.pose.orientation.w = 1.0
        self.pose_pub.publish(msg)

    def _publish_robot_circle(self) -> None:
        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.type = Marker.MESH_RESOURCE
        m.mesh_resource = "package://planner/meshes/hokuyo.dae"
        m.mesh_use_embedded_materials = True
        m.action = Marker.ADD
        m.pose.position.x = float(self.world.robot.x)
        m.pose.position.y = float(self.world.robot.y)
        m.pose.position.z = 0.0
        m.pose.orientation.w = 1.0
        m.scale.x = 7.0
        m.scale.y = 7.0
        m.scale.z = 3.0
        m.color.a = 1.0
        m.id = 0
        m.ns = "robot"
        self.robot_marker_pub.publish(m)

    def _publish_obstacles(self) -> None:
        arr = MarkerArray()
        x_obs = np.array(self.world._obs_x)
        y_obs = np.array(self.world._obs_y)
        for i, (x, y) in enumerate(zip(x_obs, y_obs)):
            m = Marker()
            m.header.frame_id = "map"
            m.header.stamp = self.get_clock().now().to_msg()
            m.type = Marker.MESH_RESOURCE
            m.mesh_resource = "package://planner/meshes/aws_robomaker_warehouse_ClutteringC_01_visual.DAE"
            m.mesh_use_embedded_materials = True
            m.action = Marker.ADD
            m.pose.position.x = float(x)
            m.pose.position.y = float(y)
            m.pose.position.z = 0.05
            m.scale.x = 0.3
            m.scale.y = 0.3
            m.scale.z = 0.6
            m.color.a = 1.0
            m.ns = "obstacles"
            m.id = i
            arr.markers.append(m)
        self.obs_pub.publish(arr)

    def _publish_humans(self) -> None:
        arr = MarkerArray()
        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.type = Marker.MESH_RESOURCE
        m.mesh_resource = "package://planner/meshes/standing.dae"
        m.mesh_use_embedded_materials = True
        m.action = Marker.ADD
        m.pose.position.x = float(self.world.human.x)
        m.pose.position.y = float(self.world.human.y)
        m.pose.orientation.z = float(np.sin(np.radians(-45.0)))
        m.pose.orientation.w = float(np.cos(np.radians(-45.0)))
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

    def _publish_trajectory_buffered(self) -> None:
        if self.traj_buffer is None:
            return
        x_best, y_best = self.traj_buffer

        # Thick line marker
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

        # Nav_msgs/Path
        path = Path()
        path.header.frame_id = "map"
        path.header.stamp = self.get_clock().now().to_msg()
        for x, y in zip(np.array(x_best), np.array(y_best)):
            p = PoseStamped()
            p.pose.position.x = float(x)
            p.pose.position.y = float(y)
            p.pose.orientation.w = 1.0
            path.poses.append(p)
        self.traj_pub.publish(path)

    def _publish_circle(self, x, y, pub, r=0.9, color=(1.0, 0.0, 0.0)) -> None:
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

    def _publish_task_label(self, text: str) -> None:
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

    def _publish_all_object_goals(self) -> None:
        arr = MarkerArray()
        for i, task in enumerate(self.task_planner.tasks):
            x, y    = task["object"]
            task_id = task["id"]

            m = Marker()
            m.header.frame_id = "map"
            m.header.stamp = self.get_clock().now().to_msg()
            m.ns = "all_object_goals"
            m.id = i
            m.type = Marker.MESH_RESOURCE
            m.mesh_resource = "package://planner/meshes/aws_robomaker_warehouse_ShelfE_01_visual.DAE"
            m.mesh_use_embedded_materials = True
            m.action = Marker.ADD
            m.pose.position.x = float(x)
            m.pose.position.y = float(y)
            m.pose.position.z = 0.05
            m.pose.orientation.x = 0.0
            m.pose.orientation.y = 0.0
            if y >= -4.5:
                m.pose.orientation.z = float(np.sin(np.radians(-90) / 2))
                m.pose.orientation.w = float(np.cos(np.radians(-90) / 2))
            else:
                m.pose.orientation.z = 0.0
                m.pose.orientation.w = 1.0
            m.scale.x = 0.3
            m.scale.y = 0.3
            m.scale.z = 0.8
            m.color.a = 1.0
            arr.markers.append(m)

            # Task ID label
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
            t.text = f"ID {task_id}"
            arr.markers.append(t)

        self.all_goals_pub.publish(arr)

    def _publish_target_goal_once(self) -> None:
        if not self.task_planner.tasks:
            return
        x, y = self.task_planner.tasks[0]["target"]
        arr = MarkerArray()

        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "delivery_point"
        m.id = 0
        m.type = Marker.MESH_RESOURCE
        m.mesh_resource = "package://planner/meshes/aws_robomaker_warehouse_DeskC_01_visual.DAE"
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
        t.text = "Delivery point"
        arr.markers.append(t)

        self.target_goal_pub.publish(arr)

    def _publish_coffee_machine(self) -> None:
        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "coffee_machine"
        m.id = 0
        m.type = Marker.CUBE
        m.action = Marker.ADD
        m.pose.position.x = -10.0
        m.pose.position.y = -3.9
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

        text = Marker()
        text.header.frame_id = "map"
        text.header.stamp = m.header.stamp
        text.ns = "coffee_machine_label"
        text.id = 1
        text.type = Marker.TEXT_VIEW_FACING
        text.action = Marker.ADD
        text.pose.position.x = -11.0
        text.pose.position.y = -4.9
        text.pose.position.z = 1.8
        text.scale.z = 0.5
        text.color.r = 0.7
        text.color.g = 0.7
        text.color.b = 0.0
        text.color.a = 1.0
        text.text = "Coffee Machine"
        self.coffee_pub.publish(text)

    def _publish_wait_message(self, text: str) -> None:
        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "wait_message"
        m.id = 0
        m.type = Marker.TEXT_VIEW_FACING
        m.action = Marker.ADD
        m.pose.position.x = 0.0
        m.pose.position.y = 0.0
        m.pose.position.z = 2.0
        m.pose.orientation.w = 1.0
        m.scale.z = 0.6
        m.color.r = 1.0
        m.color.g = 0.0
        m.color.b = 1.0
        m.color.a = 1.0
        m.text = text
        m.lifetime = Duration(sec=10)
        self.wait_msg_pub.publish(m)


# =============================================================================
# Entry point
# =============================================================================

def main(args=None):
    rclpy.init(args=args)
    node = ContinuousSimNode()
    rclpy.spin(node)


if __name__ == "__main__":
    main()
