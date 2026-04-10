
#!/usr/bin/env python3

import numpy as np
import jax.numpy as jnp
import time
from jax import random
from expert import batch_crowd_nav


class PRIESTLocalPlanner:


    def __init__(self, config):

        # ---- Robot dynamic parameters ----
        self.v_max = config["v_max"]
        self.v_min = config["v_min"]
        self.a_max = config["a_max"]

        # ---- Optimization parameters ----
        self.num_batch = config["num_batch"]
        self.maxiter_mpc = config["maxiter_mpc"]
        self.t_fin = config["t_fin"]
        self.num = config["num"]
        self.tot_time = np.linspace(0, self.t_fin, self.num)
        self.dt_step = config["dt_step"]


        # ---- Shared module influence (future IR integration) ----
        self.interrupt = False

        # ---- PRIEST / MPC backend 
        self.optimizer = batch_crowd_nav(
            config["a_obs_1"], config["b_obs_1"],
            config["a_obs_2"], config["b_obs_2"],
            config["v_max"], config["v_min"], config["a_max"],
            config["num_obs_1"], config["num_obs_2"],
            config["t_fin"], config["num"],
            config["num_batch"],
            config["maxiter"],
            config["maxiter_cem"],
            config["weight_smoothness"],
            config["weight_track"],
            config["way_point_shape"],
            config["v_des"],
        )

        # ---- Internal variables ----
        self.goal = None
        self.last_traj = None
        self.status = "IDLE"
        self.key = random.PRNGKey(0)

    def reset(self, goal):
        """Called once per task by the Task Planner."""
        self.goal = goal
        self.status = "RUNNING"
        self.last_traj = None
        self.interrupt = False


    def abort(self):
        """Called by IR to interrupt the behavior."""
        self.interrupt = True
        self.status = "INTERRUPTED"


    def step(self, state, world):

        if self.status != "RUNNING":

            return None, None, self.status

        x0, y0, vx0, vy0, ax0, ay0 = state
        gx, gy = self.goal["x"], self.goal["y"]

        # -----------------------------
        # 1. Build waypoints to goal
        # -----------------------------
        theta = np.arctan2(gy - y0, gx - x0)
        x_wp = jnp.linspace(x0, gx, 1000)
        y_wp = jnp.linspace(y0, gy, 1000)

        # Compute spline + arc
        arc_len, arc_vec, x_diff, y_diff = self.optimizer.path_spline(x_wp, y_wp)


        ### Warming 
        init_state = jnp.asarray([x0, y0, vx0, vy0, ax0, ay0])
        x_guess_per, y_guess_per = self.optimizer.compute_warm_traj(init_state,self.optimizer.v_des,x_wp,y_wp,arc_vec,x_diff,y_diff,)


        # -----------------------------
        # 2. Predict obstacles / humans
        # -----------------------------
        obs = world["obs"]
        humans = world["humans"]    # reserved for later IR integration

        # static obstacles (walls, objects, etc.)
        x_obs_init = jnp.asarray(obs["x"]).flatten()
        y_obs_init = jnp.asarray(obs["y"]).flatten()
        vx_obs = jnp.asarray(obs["vx"]).flatten()
        vy_obs = jnp.asarray(obs["vy"]).flatten()

        # humans as dynamic obstacles
        x_hum_init = jnp.asarray(humans["x"]).flatten()
        y_hum_init = jnp.asarray(humans["y"]).flatten()
        vx_hum = jnp.asarray(humans["vx"]).flatten()
        vy_hum = jnp.asarray(humans["vy"]).flatten()

        # Predict obstacle & human trajectories
        (x_obs_traj,y_obs_traj,x_obs_traj_proj,y_obs_traj_proj,x_hum_traj,y_hum_traj,) = self.optimizer.compute_obs_traj_prediction(x_hum_init, y_hum_init, vx_hum, vy_hum,x_obs_init, y_obs_init, vx_obs, vy_obs,x0, y0,)
        

        # -----------------------------
        # 3. Create initial guess (unchanged from your code)
        # -----------------------------
        init_state = jnp.asarray([x0, y0, vx0, vy0, ax0, ay0])

        (sol_x_bar, sol_y_bar, x_guess, y_guess, xdot_guess, ydot_guess, xddot_guess, yddot_guess, c_mean, c_cov, x_fin, y_fin) = self.optimizer.compute_traj_guess(init_state, x_obs_traj, y_obs_traj, x_hum_traj, y_hum_traj, self.optimizer.v_des, x_wp, y_wp, arc_vec, x_guess_per, y_guess_per, x_diff, y_diff)

        lamda_x = jnp.zeros((self.num_batch, self.optimizer.nvar))
        lamda_y = jnp.zeros((self.num_batch, self.optimizer.nvar))

        # -----------------------------
        # 4. Run CEM optimization (unchanged!)
        # -----------------------------
        (_, _, c_x_best, c_y_best, x_best, y_best, x_guess_per, y_guess_per) = self.optimizer.compute_cem(self.key, init_state, x_fin, y_fin, lamda_x, lamda_y, x_obs_traj, y_obs_traj, x_obs_traj_proj, y_obs_traj_proj, x_hum_traj, y_hum_traj, sol_x_bar, sol_y_bar, x_guess, y_guess, xdot_guess, ydot_guess, xddot_guess, yddot_guess, x_wp, y_wp, arc_vec, c_mean, c_cov)

        # -----------------------------
        # 5. Convert trajectory → ONE STEP CONTROL
        # -----------------------------
        c_x_best = sol_x_bar[0]
        c_y_best = sol_y_bar[0]

        vx_cmd, vy_cmd, ax_cmd, ay_cmd, norm_v_t, angle_v_t = self.optimizer.compute_controls(c_x_best, c_y_best)
        
        command = (vx_cmd, vy_cmd, ax_cmd, ay_cmd)
        
        # -----------------------------
        # 6. Check if reached goal
        # -----------------------------
        dist = (x0 - gx)**2 + (y0 - gy)**2
        if dist < (0.4**2):
            self.status = "REACHED"

        # -----------------------------
        # 7. Check for interruptions
        # -----------------------------
        if self.interrupt:
            self.status = "INTERRUPTED"

        return (x_best, y_best), command, self.status



