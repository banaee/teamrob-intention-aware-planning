#!/usr/bin/env python3

# planner_node.py

import rclpy
from rclpy.node import Node
import numpy as np
import threading
import jax.numpy as jnp
from geometry_msgs.msg import PoseStamped, Point
from nav_msgs.msg import Path
from visualization_msgs.msg import Marker, MarkerArray
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from local_planner_priest import PRIESTLocalPlanner
from task_planner import TaskPlanner
import time


class PlannerVisualizer(Node):

    def __init__(self):
        super().__init__("planner_visualizer")

        
        # --- Publishers ---
        self.pose_pub = self.create_publisher(PoseStamped, "/robot_pose", 100)
        self.traj_pub = self.create_publisher(Path, "/trajectory", 100)
        self.obs_pub  = self.create_publisher(MarkerArray, "/obstacles", 100)
        self.hum_pub  = self.create_publisher(MarkerArray, "/humans", 100)
        self.robot_marker_pub = self.create_publisher(Marker, "/robot_marker", 100)
        self.start_pub = self.create_publisher(Marker, "/start_marker", 100)
        self.goal_pub  = self.create_publisher(Marker, "/goal_marker", 100)
        self.task_label_pub = self.create_publisher(Marker, "/task_label", 100)
        self.path_marker_pub = self.create_publisher(Marker, "trajectory_marker", 10)




        # Simulation dt (same as ROS1 loop)
        self.dt = 0.1

        # --- Load your existing code ---

        config = {
            "v_max": 1.0,
            "v_min": 0.02,
            "a_max": 1.0,
            "num_batch": 110,
            "maxiter_mpc": 100,
            "t_fin": 10.0,
            "num": 100,
            "dt_step": 0.1,
            "a_obs_1": 0.5, "b_obs_1": 0.5,
            "a_obs_2": 0.68, "b_obs_2": 0.68,
            "num_obs_1": 3,
            "num_obs_2": 1,
            "maxiter": 1,
            "maxiter_cem": 12,
            "weight_smoothness": 1.0,
            "weight_track": 0.001,
            "way_point_shape": 1000,
            "v_des": 1.0,
        }

        self.local_planner = PRIESTLocalPlanner(config)

        self.task_planner = TaskPlanner(tasks=[
            {"object": (-10.0, 4.0), "target": (-5.0, 5.0)},
            {"object": (-10.0, 6.0), "target": (-5.0, 5.0)},
            {"object": (10.0, 4.0), "target": (-5.0, 5.0)},
            {"object": (10.0, 6.0), "target": (-5.0, 5.0)},
            {"object": (-7.0, -5.0), "target": (-5.0, 5.0)},
            {"object": (3.0, -5.0), "target": (-5.0, 5.0)},
            ])

        # Robot initial state
        self.state = (2.0, 2.0, 0.1, 0.0, 0.0, 0.0)

        self.start_pose = (self.state[0], self.state[1])
        self.start_publish_count = 0
        self.traj_buffer = None

        # World model (empty for now)
        self.world = {
            "obs": {
                "x": jnp.array([0.0, 7.0, 7.0]),
                "y": jnp.array([2.0, 3.0, -3.0]),
                "vx": jnp.zeros(3),
                "vy": jnp.zeros(3),
            },
            "humans": {
                "x": jnp.array([7.0]),
                "y": jnp.array([4.0]),
                "vx": jnp.array([0.0]),
                "vy": jnp.array([-0.1]),
            },
        }

        # Set first navigation goal
        goal = self.task_planner.current_goal()
        self.local_planner.reset(goal)

        # Start visualization thread
        self.viz_thread = threading.Thread(target=self.visualization_loop)
        self.viz_thread.daemon = True
        self.viz_thread.start()
       

        # Start MPC thread (ROS1-style behavior)
        thread = threading.Thread(target=self.main_loop)
        thread.daemon = True
        thread.start()

    #################
    def visualization_loop(self):
        rate = 0.05  # 20 Hz

        while rclpy.ok():

            
            # Start marker (published a few times)
            if self.start_publish_count < 20:
                self.publish_circle(self.start_pose[0], self.start_pose[1],
                                    self.start_pub, r=0.3, color=(0.0, 1.0, 1.0))
                self.start_publish_count += 1

            # Goal marker
            goal = self.task_planner.current_goal()
            if goal is not None:
                self.publish_circle(goal["x"], goal["y"], self.goal_pub, r=0.3, color=(1.0, 0.0, 0.0))

            task_index = self.task_planner.task_index
            phase = self.task_planner.phase
            num_tasks = len(self.task_planner.tasks)

            if task_index >= num_tasks:
                label_text = "ALL TASKS COMPLETED"
            else:
                label_text = f"Task {task_index+1} / {num_tasks} — {phase}"

            # Visualize robot and world
            self.publish_task_label(label_text)
            self.publish_robot_circle()
            self.publish_robot_pose()
            self.publish_trajectory_buffered()
            self.publish_obstacles()
            self.publish_humans()

            time.sleep(rate)

    # =====================================================================
    #                 MAIN LOOP — SAME STRUCTURE AS YOUR ROS1 CODE
    # =====================================================================
    def main_loop(self):

        while rclpy.ok():

            # WAIT phases (same as ROS1)
            if self.task_planner.phase in ["PICK_WAIT", "PLACE_WAIT"]:
                self.get_logger().info(f"Waiting... phase={self.task_planner.phase}")
                self.task_planner.update()
                time.sleep(self.dt)
                continue

            ################## Navigation goal
            goal = self.task_planner.current_goal()

            # CASE 1 — all tasks finished
            if self.task_planner.task_index >= len(self.task_planner.tasks):
                print("All tasks completed. Stopping planner loop.")
                return

            # CASE 2 — waiting phases (PICK or PLACE)
            if goal is None:
                # In PICK_WAIT or PLACE_WAIT → do NOT stop
                self.task_planner.update()
                time.sleep(self.dt)
                continue
            ########################3

            # Reset PRIEST when starting new navigation
            if self.local_planner.status != "RUNNING":
                self.local_planner.reset(goal)

            # ====== ONE MPC ITERATION (same as ROS1) ======
            start = time.time()
            traj, command, status = self.local_planner.step(self.state, self.world)
            comp_time = time.time() - start

            # Print compute time like ROS1
            print(f"[MPC] Computation time: {comp_time*1000:.2f} ms | status={status}")

            # ====== Publish everything ======
            if traj is not None:
                self.traj_buffer = traj

            # ====== Apply control ======
            if command is not None:
                x, y, vx, vy, ax, ay = self.state
                vx_cmd, vy_cmd, ax_cmd, ay_cmd = command

                x_new = x + vx_cmd * self.dt
                y_new = y + vy_cmd * self.dt
                self.state = (x_new, y_new, vx_cmd, vy_cmd, ax_cmd, ay_cmd)

            # ====== Goal reached ======
            if status == "REACHED":
                print("Reached goal!")
                self.task_planner.advance()

            time.sleep(self.dt)


    # =====================================================================
    #                         RVIZ VISUALIZATION
    # =====================================================================
    def publish_robot_pose(self):
        msg = PoseStamped()
        msg.header.frame_id = "map"
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.position.x = float(self.state[0])
        msg.pose.position.y = float(self.state[1])
        msg.pose.orientation.w = 1.0
        self.pose_pub.publish(msg)

    def publish_trajectory(self, traj):
        x_best, y_best = traj
        msg = Path()
        msg.header.frame_id = "map"
        msg.header.stamp = self.get_clock().now().to_msg()
        for x, y in zip(np.array(x_best), np.array(y_best)):
            p = PoseStamped()
            p.pose.position.x = float(x)
            p.pose.position.y = float(y)
            p.pose.orientation.w = 1.0
            msg.poses.append(p)
        self.traj_pub.publish(msg)

    def publish_obstacles(self):
        arr = MarkerArray()

        x_obs = np.array(self.world["obs"]["x"])
        y_obs = np.array(self.world["obs"]["y"])

        for i, (x, y) in enumerate(zip(x_obs, y_obs)):
            m = Marker()
            m.header.frame_id = "map"
            m.header.stamp = self.get_clock().now().to_msg()
            m.type = Marker.CYLINDER
            m.action = Marker.ADD

            m.pose.position.x = float(x)
            m.pose.position.y = float(y)
            m.pose.position.z = 0.05

            m.scale.x = 0.4   # diameter
            m.scale.y = 0.4
            m.scale.z = 0.1   # height

            m.color.r = 1.0
            m.color.g = 0.5
            m.color.b = 0.0
            m.color.a = 1.0

            m.ns = "obstacles"
            m.id = i

            arr.markers.append(m)

        self.obs_pub.publish(arr)

    ###############################
    def publish_humans(self):
        arr = MarkerArray()

        x_h = np.array(self.world["humans"]["x"])
        y_h = np.array(self.world["humans"]["y"])

        for i, (x, y) in enumerate(zip(x_h, y_h)):
            m = Marker()
            m.header.frame_id = "map"
            m.header.stamp = self.get_clock().now().to_msg()
            m.type = Marker.SPHERE
            m.action = Marker.ADD

            m.pose.position.x = float(x)
            m.pose.position.y = float(y)
            m.pose.position.z = 0.8

            m.scale.x = 0.5
            m.scale.y = 0.5
            m.scale.z = 1.6   # tall "person"

            m.color.r = 0.0
            m.color.g = 0.2
            m.color.b = 1.0
            m.color.a = 1.0

            m.ns = "humans"
            m.id = i

            arr.markers.append(m)

        self.hum_pub.publish(arr)
    ###############################
    def publish_robot_circle(self):
        x, y, _, _, _, _ = self.state

        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.type = Marker.CYLINDER   # circle from top view
        marker.action = Marker.ADD

        marker.pose.position.x = float(x)
        marker.pose.position.y = float(y)
        marker.pose.position.z = 0.0
        marker.pose.orientation.w = 1.0

        marker.scale.x = 0.3   # diameter
        marker.scale.y = 0.3
        marker.scale.z = 0.05  # small height

        marker.color.r = 0.1
        marker.color.g = 0.8
        marker.color.b = 0.2
        marker.color.a = 1.0

        marker.id = 0
        marker.ns = "robot"

        self.robot_marker_pub.publish(marker)

    def publish_circle(self, x, y, topic_pub, r=0.9, color=(1.0, 0.0, 0.0)):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.type = Marker.CYLINDER
        marker.action = Marker.ADD

        marker.pose.position.x = float(x)
        marker.pose.position.y = float(y)
        marker.pose.orientation.w = 1.0

        marker.scale.x = 0.8
        marker.scale.y = 0.8
        marker.scale.z = 0.2

        marker.color.r = color[0]
        marker.color.g = color[1]
        marker.color.b = color[2]
        marker.color.a = 1.0

        marker.id = 0
        topic_pub.publish(marker)

    #################################
    def publish_trajectory_buffered(self):
        if self.traj_buffer is None:
            return

        x_best, y_best = self.traj_buffer

        # -----------------------------
        # 2) Publish a thick line using Marker
        # -----------------------------
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = "trajectory_thick"
        marker.id = 0
        marker.type = Marker.LINE_STRIP
        marker.action = Marker.ADD

        # THICKNESS (change this to adjust thickness)
        marker.scale.x = 0.15   # 0.05 = thin, 0.15 = thick, 0.3 = very thick

        # SAME COLOR AS DEFAULT PATH (white-ish)
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        # Add points
        for x, y in zip(np.array(x_best), np.array(y_best)):
            pt = Point()
            pt.x = float(x)
            pt.y = float(y)
            pt.z = 0.0
            marker.points.append(pt)

        # PUBLISH THE MARKER  (this is the part missing in your code!)
        self.path_marker_pub.publish(marker)

        msg = Path()
        msg.header.frame_id = "map"
        msg.header.stamp = self.get_clock().now().to_msg()

        for x, y in zip(np.array(x_best), np.array(y_best)):
            p = PoseStamped()
            p.pose.position.x = float(x)
            p.pose.position.y = float(y)
            p.pose.orientation.w = 1.0
            msg.poses.append(p)


        self.traj_pub.publish(msg)

    #############################
    def publish_task_label(self, text):

        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()

        marker.ns = "task_label"
        marker.id = 0
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD

        # Position of the label (floating at top-left, safe location)
        marker.pose.position.x = float(0.0)
        marker.pose.position.y = float(10.0)
        marker.pose.position.z = float(3.0)

        marker.scale.z = float(0.8)   # text height

        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        marker.text = text

        self.task_label_pub.publish(marker)




def main(args=None):
    rclpy.init(args=args)
    node = PlannerVisualizer()
    rclpy.spin(node)


if __name__ == "__main__":
    main()
