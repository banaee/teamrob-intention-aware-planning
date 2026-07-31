# ros_sim/ — Design Guideline & Development Plan

This document is a guide for developing `ros_sim/` — the ROS 2 embodiment layer of the
TeamRob Intention-Aware Planning Framework. It captures architectural decisions, design
constraints, and a file-by-file development plan with schematics and TODOs.

---

## 0. The Big Picture

The framework has two layers:

- **`shared/`** — the cognitive layer (mind). Simulator-agnostic. Pure Python.
  Contains: `recognizer.py`, `planner.py`, `replanning.py`, `types.py`, `domain_knowledge.py`.
  **Never modified for ROS. Never imports from `ros_sim/` or `mesa_sim/`.**

- **`ros_sim/`** — the embodiment layer (body). ROS-specific.
  Handles: motion, world state construction, observation building, action execution.
  Calls `shared/` via plain Python function calls — same as Mesa does.

The ROS team's existing code (`task_planner.py`, `planner_1.py`, etc.) is used only as
a reference for understanding the PRIEST local planner and RViz setup. Its hardcoded
task logic is entirely replaced by the framework's cognitive loop.

---

## 1. What Changes vs. Mesa, What Stays the Same

### Same as Mesa
- Cognitive loop order: `obs_builder → recognizer → replanning → planner → executor`
- All `shared/` types: `WorldState`, `Observation`, `BeliefState`, `AbstractPlan`, `GroundedAction`
- Predicate families: `at(agent, obj)` for completion, `in_zone(agent, zone)` for IR context
- Domain files: `domains/kitting/` unchanged — same tasks, actions, scenarios, env_layout
- `at(agent, obj)` is a proximity predicate (Euclidean distance <= threshold), not "exactly at"
- `WorldState` is ephemeral — built fresh each cognitive tick, never persisted

### Different from Mesa
- **No `action_decomposer.py`** — Mesa needed discrete grid microactions (STEP, GRASP).
  ROS executes `GroundedAction` directly. `MOVE_TO` = nav goal to PRIEST. `PICK_UP` = wait.
- **No Mesa scheduler** — ROS uses `rclpy.spin()` + a `time.sleep(dt)` loop (dt=0.1s, 10Hz)
- **Motion is continuous** — PRIEST computes smooth velocity commands, not grid steps
- **`executor.py` calls PRIEST** instead of expanding microaction queues
- **Completion check** is still predicate-based (`at(robot, target)` in `WorldState.predicates`),
  but triggered by proximity check in `world_state_builder` after each PRIEST tick
- **Coordinate lookup** — executor must resolve symbolic object IDs to `(x, y)` before calling PRIEST
- **`obs_builder.py`** is a stub for now — human microaction classification from sensor streams
  is deferred until IR is real (Phase 4)

### Three-Clock Architecture
```
Motion clock     PRIEST dt loop at 10Hz            (fastest)
World state      sampled at ~Mesa step rate         (configurable in ros_configs.yaml)
Cognitive clock  event-driven: task done / belief   (slowest — drives IR + replanning)
```
`shared/` is called only at the cognitive clock level. It does not know about motion or
world state frequencies.

---

## 2. Coordinate System — R0 (prerequisite, done outside ros_sim/)

`env_layout1.json` already stores `"position": [x, y]` for every `env_object`.
The executor's lookup is simply:

```python
layout = {obj["id"]: tuple(obj["position"]) for obj in env_layout["env_objects"]}
# e.g. layout["shelf_3"] == (950, 400)  -- in Mesa world units
```

**TODO R0 (confirm with ROS team before writing executor):**
- What coordinate system and units does PRIEST use? (origin, meters vs. world units)
- If different from Mesa's center-origin world units, add a scale/offset constant to
  `ros_configs.yaml`: `mesa_to_ros_scale: 0.001` (if Mesa units are mm, ROS is meters).
- No new files needed. No changes to `shared/` or `domains/`.

---

## 3. File-by-File Development Plan

Develop in this order. Each file depends on the previous ones being stable.

---

### File 1: `ros_configs.yaml`

**Develop first** — all other files read from it.

```yaml
# ros_sim/ros_configs.yaml

sim:
  dt: 0.1                        # PRIEST loop period (seconds)
  world_state_sample_every: 1    # sample WorldState every N PRIEST ticks
  proximity_threshold: 0.4       # meters — at(agent, obj) emitted within this distance

coordinate:
  mesa_to_ros_scale: 1.0         # TODO R0: set after confirming with ROS team
  origin_offset: [0.0, 0.0]      # TODO R0: set if origins differ

priest:
  goal_tolerance: 0.4            # meters — same as proximity_threshold by default
  max_velocity: 1.0
  # ... other PRIEST params moved from her hardcoded values

ros:
  robot_frame: "robot_base"
  world_frame: "world"
  # topic names go here if/when real subscribers are added
```

**Key principle:** PRIEST's hardcoded `0.4**2` distance check is replaced by
`proximity_threshold` from this file.

---

### File 2: `ros_agents.py`

Parallel to `mesa_sim/sim_agents.py`. Owns agent state and the cognitive loop.

**Structure:**

```python
# ros_sim/ros_agents.py

class RosAgentBase:
    """Owns continuous sim state: position, velocity, carrying, current_task."""
    def __init__(self, agent_id, initial_pos):
        self.agent_id = agent_id
        self.pos = list(initial_pos)       # [x, y] in ROS coordinates
        self.vel = [0.0, 0.0]             # [vx, vy]
        self.carrying = None               # item_id or None
        self.current_task = None
        self.current_action = None
        self.finished = False


class RosHumanAgent(RosAgentBase):
    """
    Scripted human — mirrors mesa_sim HumanAgent.
    Follows a fixed TaskInstance list. Uses Euler integration for motion.
    Robot has no access to this script.

    Motion: simple interpolation toward current waypoint at fixed speed.
    No PRIEST — human motion is scripted, not optimized.

    step(dt):
        1. If no current waypoint, pop next action from script
        2. Move toward waypoint: pos += direction * speed * dt
        3. If close enough (proximity_threshold): action done, advance script
        4. Update carrying state for PICK_UP / PLACE actions
    """
    def __init__(self, agent_id, script: List[TaskInstance], knowledge, initial_pos, config):
        ...

    def step(self, dt: float, sim_state: dict):
        # Euler integration toward waypoint
        # Returns nothing — updates self.pos, self.carrying in place
        ...


class RosRobotAgent(RosAgentBase):
    """
    Cognitive robot agent — mirrors mesa_sim RobotAgent.
    Owns the full cognitive loop, called at the cognitive clock rate.

    Cognitive loop (called every K PRIEST ticks or on event):
        world  = build_world_state(sim_state, config)
        obs    = build_observation(sim_state, config)
        belief = recognizer.update(obs, prev_belief)
        result = should_replan(current_plan, belief, world, prev_belief)
        if result["replan"]:
            current_plan = planner.plan(...)
        executor.step(current_plan, world)

    Motion loop (called every PRIEST tick at 10Hz):
        executor drives PRIEST for current GroundedAction
    """
    def __init__(self, agent_id, scheduled_tasks, knowledge, initial_pos, config):
        self.recognizer = IntentionRecognizer(knowledge)
        self.planner = AdaptivePlanner(knowledge)
        self.executor = RosExecutor(agent=self, config=config)
        self.belief = None
        self.current_plan = None
        ...

    def cognitive_tick(self, sim_state: dict):
        """Called at world state clock rate. Calls shared/ modules."""
        ...

    def motion_tick(self, dt: float, sim_state: dict):
        """Called at PRIEST clock rate (10Hz). Drives executor."""
        ...
```

**Important import boundary:**
```python
# ALLOWED in ros_agents.py:
from shared.recognizer import IntentionRecognizer
from shared.planner import AdaptivePlanner
from shared.replanning import should_replan
from ros_sim.world_state_builder import build_world_state
from ros_sim.obs_builder import build_observation
from ros_sim.executor import RosExecutor

# NEVER:
# from mesa_sim import anything
```

---

### File 3: `world_state_builder.py`

Parallel to `mesa_sim/world_state_builder.py`. Translates internal sim state dict
into a symbolic `WorldState`. **Careful work needed — dedicated session recommended.**

**Input:** `sim_state` dict (owned by `RosSimNode`) containing:
- `robots`: `{agent_id: {"pos": [x,y], "vel": [vx,vy], "carrying": item_id|None}}`
- `humans`: same structure
- `items`: `{item_id: {"pos": [x,y], "held_by": agent_id|None, "at_location": loc_id|None}}`
- `env_objects`: loaded once from `env_layout1.json`
- `zones`: loaded once from `env_layout1.json`

**Output:** `WorldState` with same predicate families as Mesa:

```python
# Predicates emitted — identical contract to mesa_sim/world_state_builder.py:
#
#   in_zone(agent_id, zone_id)    — coarse, for IR context
#   at(agent_id, obj_id)          — proximity <= threshold, for executor completion
#   holding(agent_id, item_id)    — agent is carrying item
#   obj_at(item_id, location_id)  — item rests at location
#
# PROXIMITY CHECK (replaces PRIEST's hardcoded 0.4**2):
#   dist = sqrt((ax-ox)**2 + (ay-oy)**2)
#   if dist <= config["proximity_threshold"]:
#       emit at(agent_id, obj_id)
```

```python
def build_world_state(sim_state: dict, config: dict) -> WorldState:
    """
    IN:  sim_state (internal dict), config (from ros_configs.yaml)
    OUT: WorldState with symbolic predicates
    Same predicate contract as mesa_sim/world_state_builder.py.
    """
    ...
```

**Notes:**
- Zone lookup: same polygon-in-bounds check as Mesa (`zone_map` from `env_layout1.json`)
- Proximity threshold: read from `config["proximity_threshold"]`, not hardcoded
- `WorldState` is ephemeral — built fresh each call, never stored

---

### File 4: `obs_builder.py`

Parallel to `mesa_sim/obs_builder.py`. Produces `Observation` for IR.

**For now: stub.** Return a dummy observation — same as Mesa's current skeleton behavior.
Real classification (human sensor streams → discrete microaction label) is deferred to
Phase 4 / IR development session.

```python
def build_observation(sim_state: dict, config: dict) -> Observation:
    """
    IN:  sim_state, config
    OUT: Observation with detected_microaction label

    STUB: infers microaction from human agent's current scripted action.
    This is ground truth inference — same privilege as Mesa.
    Real sensor-based classification deferred to Phase 4.

    TODO Phase 4: replace with classifier over human position/velocity history
    """
    human = sim_state["humans"]["human_0"]
    # Infer microaction from scripted action label (ground truth, like Mesa)
    detected = human.get("current_action", "idle")
    return Observation(
        timestamp=sim_state["time"],
        agent_id="human_0",
        detected_microaction=detected,
        spatial_context=SpatialContext(
            position=tuple(human["pos"]),
            orientation=0.0,
            zone=human.get("current_zone"),
        ),
        action_context=ActionContext(
            target_object=human.get("current_target"),
        ),
        confidence=1.0,  # ground truth in sim
    )
```

---

### File 5: `executor.py`

Parallel to `mesa_sim/executor.py` but **no microaction queue, no action_decomposer**.
Receives `GroundedAction`, drives PRIEST, checks completion via `WorldState` predicates.

**Structure:**

```python
# ros_sim/executor.py

class RosExecutor:
    """
    Execution engine for one ROS agent.
    Receives GroundedAction from planner, dispatches to PRIEST or waits.
    Completion checked via WorldState predicates — NOT via PRIEST status string.
    """

    def __init__(self, agent: RosAgentBase, config: dict):
        self.agent = agent
        self.config = config
        self.current_plan: Optional[AbstractPlan] = None
        self.action_index: int = 0
        self.current_action: Optional[GroundedAction] = None
        self._layout: dict = {}   # {obj_id: (x, y)} — loaded from env_layout1.json

    def load_layout(self, env_layout: dict):
        """Build symbolic_id -> (x, y) lookup from env_layout1.json."""
        self._layout = {
            obj["id"]: tuple(obj["position"])
            for obj in env_layout.get("env_objects", [])
        }
        # TODO R0: apply scale/offset from config["coordinate"] here

    def step(self, plan: AbstractPlan, world: WorldState) -> Optional[tuple]:
        """
        Called every PRIEST tick (10Hz).

        FLOW:
          1. Load plan if new
          2. Get current GroundedAction
          3. Check completion via WorldState predicates
          4. If complete: advance to next action
          5. If not complete: dispatch to PRIEST or wait
          Returns: (vx, vy) velocity command, or None if idle/waiting
        """
        ...

    def _dispatch(self, action: GroundedAction) -> Optional[tuple]:
        """
        Translate GroundedAction to motion or manipulation command.

        move_to(?target):
            goal_xy = self._layout[action.bindings["?target"]]
            return priest.step(self.agent.pos, goal_xy, sim_state["obstacles"])

        pick_up(?item):
            # No motion — robot is already at(robot, item) by precondition
            # Simulate grasp: set agent.carrying = item_id after short wait
            # TODO: replace with real gripper action server call
            return None

        place(?item, ?target):
            # No motion — robot is already at target by precondition
            # Simulate release: clear agent.carrying, set item.at_location
            # TODO: replace with real gripper action server call
            return None

        wait_at(?entity):
            # ProcessCompletion — advance on cognitive event, not predicate
            return None
        """
        ...

    def _is_action_complete(self, action: GroundedAction, world: WorldState) -> bool:
        """
        Same logic as mesa_sim/executor.py._is_action_complete().
        Check completion_predicate membership in world.predicates.
        ProcessCompletion actions: check external signal instead.
        """
        if action.completion_predicate is None:
            return self._process_complete  # ProcessCompletion path
        return action.completion_predicate in world.predicates
```

**Critical notes:**
- `PRIEST.step()` returns `(trajectory, velocity_command)` only — status string dropped
- Completion is determined by `at(robot, target)` in `world.predicates`, not by PRIEST
- `_layout` lookup must apply coordinate scale/offset from `ros_configs.yaml` (R0)
- `pick_up` and `place` are timed waits for now — gripper action server is future work

---

### File 6: `run_ros.py`

Entry point. Parallel to `mesa_sim/run_mesa.py`.

```python
# ros_sim/run_ros.py
"""
Entry point for ROS 2 simulation.
Usage: ros2 run teamrob_ros run_ros.py
   or: python ros_sim/run_ros.py (headless, no ROS spin)

Mirrors mesa_sim/run_mesa.py:
  - loads domain + scenario from experiment.yaml (same CLI pattern)
  - initialises agents
  - runs the simulation loop
"""

import rclpy
from rclpy.node import Node
import yaml, json, threading, time

from domains.kitting.registry import register as kitting_register
from shared.domain_knowledge import DomainKnowledgeBase
from ros_sim.ros_agents import RosRobotAgent, RosHumanAgent
from ros_sim.world_state_builder import build_world_state
from ros_sim.executor import RosExecutor


class RosSimNode(Node):
    """
    ROS 2 node that owns the simulation state dict and drives both agents.

    Two threads:
      main_loop   — PRIEST at dt=0.1s; calls executor.step() each tick;
                    calls cognitive_tick() every K ticks (world state clock)
      viz_loop    — publishes RViz markers at 20Hz

    sim_state dict (ground truth, owned here):
      {
        "time": float,
        "robots":  {agent_id: {"pos": [x,y], "vel": [vx,vy], "carrying": ...}},
        "humans":  {agent_id: {"pos": [x,y], "vel": [vx,vy], "carrying": ...}},
        "items":   {item_id:  {"pos": [x,y], "held_by": ..., "at_location": ...}},
        "env_objects": [...],   # from env_layout1.json, static
        "zones": [...],         # from env_layout1.json, static
        "obstacles": [...],     # for PRIEST collision avoidance
      }
    """

    def __init__(self, config, scenario, knowledge):
        super().__init__("ros_sim_node")
        self.config = config
        self.dt = config["sim"]["dt"]
        self.sample_every = config["sim"]["world_state_sample_every"]
        self.tick = 0

        # initialise sim_state from scenario + env_layout
        self.sim_state = self._init_sim_state(scenario)

        # init agents
        self.robot = RosRobotAgent(...)
        self.human = RosHumanAgent(...)

        # start threads
        threading.Thread(target=self._main_loop, daemon=True).start()
        threading.Thread(target=self._viz_loop, daemon=True).start()

    def _main_loop(self):
        while rclpy.ok():
            self.tick += 1
            self.sim_state["time"] += self.dt

            # motion tick — every PRIEST step
            vel_cmd = self.robot.motion_tick(self.dt, self.sim_state)
            self._integrate_robot(vel_cmd)
            self.human.step(self.dt, self.sim_state)

            # cognitive tick — every K steps (world state clock)
            if self.tick % self.sample_every == 0:
                self.robot.cognitive_tick(self.sim_state)

            time.sleep(self.dt)

    def _viz_loop(self):
        # TODO R5: publish RViz markers
        ...

    def _integrate_robot(self, vel_cmd):
        if vel_cmd is None:
            return
        vx, vy = vel_cmd
        self.sim_state["robots"]["robot_0"]["pos"][0] += vx * self.dt
        self.sim_state["robots"]["robot_0"]["pos"][1] += vy * self.dt
        self.sim_state["robots"]["robot_0"]["vel"] = [vx, vy]


def main():
    # load config (same pattern as run_mesa.py with experiment.yaml)
    with open("ros_sim/ros_configs.yaml") as f:
        config = yaml.safe_load(f)

    # load domain + scenario (same as Mesa)
    knowledge = DomainKnowledgeBase.from_domain(kitting_register())
    # TODO: load scenario from experiment.yaml CLI pattern

    rclpy.init()
    node = RosSimNode(config, scenario, knowledge)
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

---

### File 7: `viz_node.py` (Phase R5 — deferred)

RViz marker publisher. Deferred until R1–R5 run end-to-end.
Publishes: robot pose, human pose, obstacle markers, trajectory, task label text.
Mirrors Mesa's `mesa_sim/viz/space_drawer.py` role.

---

## 4. What NOT to Port from ROS Team Code

| Her file | Disposition |
|---|---|
| `task_planner.py` | Discard — replaced by `shared/planner.py` + scenario config |
| `task_planner_interrupt.py` | Discard — replaced by `shared/replanning.py` |
| `planner_1.py`, `planner_2.py` | Discard as task logic; keep as reference for node/thread structure |
| `expert.py`, `expert_interrupt.py` | Discard — hardcoded interruption rules |
| `local_planner_priest.py` | **Keep** — motion backend for `executor.py` |
| `local_planner_priest_interrupt.py` | Discard — interruption logic handled by `shared/replanning.py` |
| `bernstein_coeff_order10_arbitinterval.py` | **Keep** — math backend for PRIEST |

**Modification to `local_planner_priest.py`:**
Drop the `self.status = "REACHED"` return. Change return signature from
`(trajectory, command, status)` to `(trajectory, command)`.
Completion is determined by `world_state_builder` predicates, not PRIEST.

---

## 5. Invariants — Must Never Be Violated

These are non-negotiable, matching the rest of the framework:

1. **`ros_sim/` never imports from `mesa_sim/`** — and vice versa.
2. **`shared/` never imports from `ros_sim/`** — cognitive layer is simulator-agnostic.
3. **`at` and `in_zone` are distinct predicates** — never use `at(agent, zone_id)`.
   That is a silent bug: executor completion will never be satisfied.
4. **`WorldState` is ephemeral** — built fresh each cognitive tick, never stored or mutated.
5. **No string parsing in the cognitive layer** — all bindings are typed `Var`/`Const`.
6. **Completion is checked via `WorldState.predicates`** — not via PRIEST status strings.
7. **`shared/` is called via plain Python function calls** — rclpy wraps the loop, it does
   not change how `recognizer.update()` or `planner.plan()` are called.

---

## 6. Open Questions / TODOs

- [ ] **R0**: confirm PRIEST coordinate system and units with ROS team
- [ ] **R0**: set `mesa_to_ros_scale` and `origin_offset` in `ros_configs.yaml`
- [ ] Confirm ROS 2 version (Humble / Iron / Jazzy) — affects rclpy import paths
- [ ] Confirm whether Gazebo is used or purely Python sim (affects Phase R5 viz)
- [ ] `pick_up` / `place` timing — how long is the simulated grasp/release wait?
- [ ] `obs_builder.py` real classification — deferred to Phase 4 / IR session
- [ ] PRIEST config parameters — move all hardcoded values to `ros_configs.yaml`
- [ ] RViz marker publishing — deferred to Phase R5 after end-to-end run confirmed
