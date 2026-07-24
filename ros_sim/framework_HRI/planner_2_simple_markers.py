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

from local_planner_priest_interrupt import PRIESTLocalPlanner
from task_planner_interrupt import TaskPlanner
import time
from builtin_interfaces.msg import Duration


class PlannerVisualizer(Node):

    def __init__(self):
        super().__init__("planner_visualizer")

        ##########
        self.interrupt_active = False

        
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
        self.all_goals_pub = self.create_publisher(MarkerArray, "/all_object_goals", 100)
        self.target_goal_pub = self.create_publisher(MarkerArray, "/target_goal_marker", 100)
        self.wait_msg_pub = self.create_publisher(Marker, "/wait_message", 10)
        self.coffee_pub = self.create_publisher(Marker, "/coffee_marker", 1)



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
            "a_obs_1": 0.9, "b_obs_1": 0.9,
            "a_obs_2": 0.7, "b_obs_2": 0.7,
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
            {"object": (-10.0, 3.0), "target": (-2.0, 6.0)},
            {"object": (-10.0, -3.0), "target": (-2.0, 6.0)},
            {"object": (-10.0, 0.0), "target": (-2.0, 6.0)},
            {"object": (10.0, 3.0), "target": (-2.0, 6.0)},
            {"object": (10.0, -3.0), "target": (-2.0, 6.0)},
            {"object": (10.0, 0.0), "target": (-2.0, 6.0)},
            {"object": (-7.0, -5.0), "target": (-2.0, 6.0)},
            {"object": (3.0, -5.0), "target": (-2.0, 6.0)},
            ])

        # Robot initial state
        self.state = (2.0, 2.0, 0.1, 0.0, 0.0, 0.0)

        self.start_pose = (self.state[0], self.state[1])
        self.start_publish_count = 0
        self.traj_buffer = None

        self.mpc_iter = 0
        # Interrupt configuration
        self.interruption_threshold = 30      # demo value (can be 10000 later)
        self.interrupted_task_ids = set()     # latch: remember which tasks already interrupted
        

        # One-shot latch per (task_id, phase)
        self.interrupted_rules = set()

        
        self.world_lock = threading.Lock()

        # World model (empty for now)
        self.world = {
            "obs": {
                "x": jnp.array([0.0,  0.0, 2.0, -2.0,  7.0, 7.0, -7.0, -7.0, ]),
                "y": jnp.array([2.0, -2.0, 0.0, 0.0,  3.0, -3.0, 3.0, -1.0, ]),
                "vx": jnp.zeros(8),
                "vy": jnp.zeros(8),
            },
            "humans": {
                "x": jnp.array([-4.0]),
                "y": jnp.array([-3.0]),
                "vx": jnp.array([0.0]),
                "vy": jnp.array([0.0]),
            },
        }

        # Human scripted motion: start -> goal -> hold -> start
        self.human_start = jnp.array([-4.0, -3.0])
        self.human_goal  = jnp.array([-10.0, -3.3])

        self.human_speed = 0.20      # m/s (tune)
        self.human_hold_s = 40.0     # seconds

        self.human_phase = "to_goal" # "to_goal" | "hold" | "to_start"
        self.human_hold_elapsed = 0.0
        self.human_eps = 0.02        # arrival tolerance (m)


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

        

    #_______________API to request an interrupt______
    def request_interrupt(self, reason="unspecified"):
        if not self.interrupt_active:
            print(f"[INTERRUPT REQUESTED] reason={reason}")
            self.interrupt_active = True
    
    #_____________Example of interrupt
    
    def example_interrupt_source(self):
        # Disable demo interrupts
        if self.interruption_threshold is None:
            return

        task_id = self.task_planner.current_task_id()
        if task_id is None:
            return

        phase = self.task_planner.phase

        # Optional timing gate
        if self.mpc_iter < self.interruption_threshold:
            return

        # ----- Define interrupt rules -----
        rule_1 = (task_id == 1 and phase == "GOTO_OBJECT")
        rule_2 = (task_id == 4 and phase == "GOTO_TARGET")
        # rule_3 = (task_id == 5 and phase in ["PICK_WAIT", "PLACE_WAIT"])

        # if not rule_3:
        #     if self.mpc_iter < self.interruption_threshold:
        #         return

        # if not (rule_1 or rule_2 or rule_3):
        if not (rule_1 or rule_2 ):
            return

        # Latch per (task_id, phase)
        rule_key = (task_id, phase)
        if rule_key in self.interrupted_rules:
            return

        # Fire interrupt ONCE for this rule
        self.interrupted_rules.add(rule_key)
        self.request_interrupt(
            reason=f"demo interrupt: task={task_id}, phase={phase}, iter={self.mpc_iter}"
        )

    def handle_pick_place_interrupt(self):
        if not self.interrupt_active:
            return
        if self.task_planner.phase not in ["PICK_WAIT", "PLACE_WAIT"]:
            return

        self.get_logger().info(
            f"Interrupt during {self.task_planner.phase}: asking to wait 10 seconds"
        )

        # your requested published marker text (and console marker print)
        self.publish_wait_message("wait for 20 seconds")

        time.sleep(10)
        self.interrupt_active = False


    ############################
    # def update_humans(self):
    #     # Euler integration: x += vx*dt, y += vy*dt
    #     with self.world_lock:
    #         x = self.world["humans"]["x"]
    #         y = self.world["humans"]["y"]
    #         vx = self.world["humans"]["vx"]
    #         vy = self.world["humans"]["vy"]

    #         self.world["humans"]["x"] = x + vx * self.dt
    #         self.world["humans"]["y"] = y + vy * self.dt

    def update_humans(self):
        with self.world_lock:
            # current position (single human)
            x = float(self.world["humans"]["x"][0])
            y = float(self.world["humans"]["y"][0])

            pos = jnp.array([x, y])

            if self.human_phase == "to_goal":
                target = self.human_goal
                vec = target - pos
                dist = float(jnp.linalg.norm(vec))

                if dist < self.human_eps:
                    # snap + switch to hold
                    self.world["humans"]["x"] = jnp.array([float(target[0])])
                    self.world["humans"]["y"] = jnp.array([float(target[1])])
                    self.world["humans"]["vx"] = jnp.array([0.0])
                    self.world["humans"]["vy"] = jnp.array([0.0])

                    self.human_phase = "hold"
                    self.human_hold_elapsed = 0.0
                    return

                direction = vec / (dist + 1e-9)
                v = direction * self.human_speed

                # integrate
                new_pos = pos + v * self.dt
                self.world["humans"]["x"] = jnp.array([float(new_pos[0])])
                self.world["humans"]["y"] = jnp.array([float(new_pos[1])])
                self.world["humans"]["vx"] = jnp.array([float(v[0])])
                self.world["humans"]["vy"] = jnp.array([float(v[1])])

            elif self.human_phase == "hold":
                self.human_hold_elapsed += self.dt

                # stay exactly at goal
                self.world["humans"]["x"] = jnp.array([float(self.human_goal[0])])
                self.world["humans"]["y"] = jnp.array([float(self.human_goal[1])])
                self.world["humans"]["vx"] = jnp.array([0.0])
                self.world["humans"]["vy"] = jnp.array([0.0])

                if self.human_hold_elapsed >= self.human_hold_s:
                    self.human_phase = "to_start"
                return

            elif self.human_phase == "to_start":
                target = self.human_start
                vec = target - pos
                dist = float(jnp.linalg.norm(vec))

                if dist < self.human_eps:
                    # snap + stop (or repeat)
                    self.world["humans"]["x"] = jnp.array([float(target[0])])
                    self.world["humans"]["y"] = jnp.array([float(target[1])])
                    self.world["humans"]["vx"] = jnp.array([0.0])
                    self.world["humans"]["vy"] = jnp.array([0.0])

                    # Option A: stop here
                    self.human_phase = "done"

                    # Option B: repeat the cycle
                    self.human_phase = "to_goal"
                    self.human_hold_elapsed = 0.0
                    return

                direction = vec / (dist + 1e-9)
                v = direction * self.human_speed

                new_pos = pos + v * self.dt
                self.world["humans"]["x"] = jnp.array([float(new_pos[0])])
                self.world["humans"]["y"] = jnp.array([float(new_pos[1])])
                self.world["humans"]["vx"] = jnp.array([float(v[0])])
                self.world["humans"]["vy"] = jnp.array([float(v[1])])

            else:
                # "done" or unknown: no motion
                self.world["humans"]["vx"] = jnp.array([0.0])
                self.world["humans"]["vy"] = jnp.array([0.0])



    #################
    def visualization_loop(self):
        rate = 0.05  # 20 Hz

        while rclpy.ok():

            
            # Start marker (published a few times)
            # if self.start_publish_count < 20:
            #     self.publish_circle(self.start_pose[0], self.start_pose[1],
            #                         self.start_pub, r=0.3, color=(0.0, 1.0, 1.0))
            #     self.start_publish_count += 1

            # Goal marker
            goal = self.task_planner.current_goal()
            if goal is not None:
                self.publish_circle(goal["x"], goal["y"], self.goal_pub, r=0.3, color=(1.0, 0.0, 0.0))

            task_index = self.task_planner.task_index
            phase = self.task_planner.phase
            num_tasks = len(self.task_planner.tasks)
            task_id = self.task_planner.current_task_id()

            if self.local_planner.status == "INTERRUPTED":
                label_text = (f"⚠ INTERRUPTED — TASK ID: {task_id} — Phase: {phase}")
            elif task_index >= num_tasks:
                label_text = "ALL TASKS COMPLETED"
            else:
                label_text = f"TASK ID: {task_id} — Task Counter: {task_index+1} / {num_tasks} — {phase}"

            # Visualize robot and world
            self.publish_task_label(label_text)
            self.publish_robot_circle()
            self.publish_robot_pose()
            self.publish_trajectory_buffered()
            self.publish_obstacles()
            self.publish_humans()
            self.publish_all_object_goals()
            self.publish_target_goal_once()
            self.publish_coffee_machine()


            time.sleep(rate)

    # =====================================================================
    #                 MAIN LOOP — SAME STRUCTURE AS YOUR ROS1 CODE
    # =====================================================================
    def main_loop(self):

        while rclpy.ok():

            self.example_interrupt_source()

            # WAIT phases (same as ROS1)
            if self.task_planner.phase in ["PICK_WAIT", "PLACE_WAIT"]:
                self.handle_pick_place_interrupt()
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

            #####################Interrupt example
            # self.example_interrupt_source()

            if self.interrupt_active and self.local_planner.status == "RUNNING":
                print("[MPC] Abort requested")
                self.local_planner.abort()

            # -------------------------
            # 2) If interrupted → hold
            # -------------------------
            if self.local_planner.status == "INTERRUPTED":

                task_id = self.task_planner.current_task_id()
                phase = self.task_planner.phase

                print(f"[INTERRUPTED] task_id={task_id} phase={phase}")

                # Optional delay
                time.sleep(5)

                # -------- CASE A: Interrupted while going to object --------
                if phase == "GOTO_OBJECT":
                    print("[RECOVERY] Interrupted in GOTO_OBJECT → reshuffle tasks")
                    self.task_planner.reshuffle_unfinished_tasks_randomly()
                    task_ids = [t["id"] for t in self.task_planner.tasks]
                    print(f"[TASK ORDER AFTER RESHUFFLE] {task_ids}")
                    time.sleep(5)# Clear interrupt flag
                    self.interrupt_active = False
                    self.mpc_iter = 0
                    # self.interruption_threshold = None

                # -------- CASE B: Interrupted while going to target --------
                elif phase == "GOTO_TARGET":
                    print("[RECOVERY] Interrupted in GOTO_TARGET -> start cancellation (return object)")

                    # start cancellation state machine
                    self.task_planner.start_cancellation()

                    new_goal = self.task_planner.current_goal()
                    if new_goal is None:
                        print("[RECOVERY] Cancellation produced no goal (unexpected). Skipping.")
                        time.sleep(0.1)
                        continue

                    self.local_planner.reset(new_goal)

                    # clear interrupt latch so we can continue
                    self.interrupt_active = False
                    self.mpc_iter = 0                    
               
                new_goal = self.task_planner.current_goal()
                self.local_planner.reset(new_goal)
                
                continue

                # new_goal = self.task_planner.current_goal()
                # self.local_planner.reset(new_goal)
                # continue

            if self.local_planner.status in ["REACHED"]:
                self.local_planner.reset(goal)
                self.mpc_iter = 0


            # ====== ONE MPC ITERATION ======
            if self.local_planner.goal is None:
                print("[MPC] No active goal, skipping step")
                time.sleep(0.1)
                continue
            start = time.time()

            with self.world_lock:
                world_snapshot = {
                    "obs": {k: v for k, v in self.world["obs"].items()},
                    "humans": {k: v for k, v in self.world["humans"].items()},}

            traj, command, status = self.local_planner.step(self.state, world_snapshot)
            comp_time = time.time() - start
            self.mpc_iter += 1

            # Print compute time 
            task_id = self.task_planner.current_task_id()
            phase = self.task_planner.phase

            print(f"[TASK {task_id}] | phase={phase} | MPC time={comp_time*1000:.2f} ms | status={status}")

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

            ########update Human position
            self.update_humans()

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

        with self.world_lock:
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

    def publish_coffee_machine(self):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = self.get_clock().now().to_msg()

        marker.ns = "coffee_machine"
        marker.id = 0
        marker.type = Marker.CUBE
        marker.action = Marker.ADD

        # position
        marker.pose.position.x = -10.5
        marker.pose.position.y = -3.7
        marker.pose.position.z = 0.5

        marker.pose.orientation.w = 1.0

        # size (meters)
        marker.scale.x = 0.6
        marker.scale.y = 0.6
        marker.scale.z = 1.2

        # color (brown-ish coffee color)
        marker.color.r = 0.4
        marker.color.g = 0.25
        marker.color.b = 0.1
        marker.color.a = 1.0

        self.coffee_pub.publish(marker)

        # -------- text label --------
        text = Marker()
        text.header.frame_id = "map"
        text.header.stamp = marker.header.stamp

        text.ns = "coffee_machine_label"
        text.id = 1
        text.type = Marker.TEXT_VIEW_FACING
        text.action = Marker.ADD

        text.pose.position.x = -12.0
        text.pose.position.y = -4.0
        text.pose.position.z = 1.8

        text.scale.z = 0.5  # font size

        text.color.r = 0.0
        text.color.g = 1.0
        text.color.b = 0.0
        text.color.a = 1.0

        text.text = "Coffee Machine"

        self.coffee_pub.publish(text)


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
    
    ##################################
    def publish_all_object_goals(self):
        arr = MarkerArray()

        for i, task in enumerate(self.task_planner.tasks):
            x, y = task["object"]
            task_id = task["id"]

            # ---- Rectangle marker (object location) ----
            m = Marker()
            m.header.frame_id = "map"
            m.header.stamp = self.get_clock().now().to_msg()
            m.ns = "all_object_goals"
            m.id = i
            m.type = Marker.CUBE
            m.action = Marker.ADD

            m.pose.position.x = float(x)
            m.pose.position.y = float(y)
            m.pose.position.z = 0.05
            m.pose.orientation.w = 1.0

            m.scale.x = 0.3
            m.scale.y = 0.3
            m.scale.z = 0.1

            m.color.r = 0.0
            m.color.g = 0.0
            m.color.b = 1.0
            m.color.a = 1.0

            arr.markers.append(m)

            # ---- Text label (task ID) ----
            t = Marker()
            t.header.frame_id = "map"
            t.header.stamp = m.header.stamp
            t.ns = "all_object_goal_labels"
            t.id = 1000 + i
            t.type = Marker.TEXT_VIEW_FACING
            t.action = Marker.ADD

            t.pose.position.x = float(x + 0.35)
            t.pose.position.y = float(y + 0.35)
            t.pose.position.z = 0.5

            t.scale.z = 0.35

            t.color.r = 0.0
            t.color.g = 0.0
            t.color.b = 1.0
            t.color.a = 1.0

            t.text = f"ID {task_id}"

            arr.markers.append(t)

        self.all_goals_pub.publish(arr)

    ############################################
    def publish_target_goal_once(self):
        # If there are no tasks, do nothing
        if not self.task_planner.tasks:
            return

        # All tasks share the same target → take it from the first task
        x, y = self.task_planner.tasks[0]["target"]

        arr = MarkerArray()

        # ---- Pink rectangle for delivery point ----
        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "delivery_point"
        m.id = 0
        m.type = Marker.CUBE
        # m.mesh_resource = "package://planner/meshes/aws_robomaker_warehouse_DeskC_01_visual.DAE"
        # m.mesh_use_embedded_materials = True   
        m.action = Marker.ADD

        m.pose.position.x = float(x)
        m.pose.position.y = float(y)
        m.pose.position.z = 0.05
        m.pose.orientation.w = 1.0

        m.scale.x = 0.4
        m.scale.y = 0.4
        m.scale.z = 0.1

        # Pink color
        m.color.r = 1.0
        m.color.g = 0.2
        m.color.b = 0.6
        m.color.a = 1.0

        arr.markers.append(m)

        # ---- Text label ----
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

    ########################
    def publish_wait_message(self, text: str):
        # console marker requested by you
        print("wait for 20 seconds")

        m = Marker()
        m.header.frame_id = "map"
        m.header.stamp = self.get_clock().now().to_msg()
        m.ns = "wait_message"
        m.id = 0
        m.type = Marker.TEXT_VIEW_FACING
        m.action = Marker.ADD

        # place text somewhere visible; adjust as desired
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

        # --- AUTO-DELETE after 10 seconds ---
        m.lifetime = Duration(sec=10)
        self.wait_msg_pub.publish(m)




def main(args=None):
    rclpy.init(args=args)
    node = PlannerVisualizer()
    rclpy.spin(node)


if __name__ == "__main__":
    main()