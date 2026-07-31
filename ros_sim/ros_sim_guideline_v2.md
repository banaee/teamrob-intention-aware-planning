# ros_sim/ — Design Guideline & Development Plan (v2)

This document is a guide for developing `ros_sim/` — the ROS 2 embodiment layer of the
TeamRob Intention-Aware Planning Framework. It captures architectural decisions, design
constraints, and a file-by-file development plan with schematics and TODOs.

**v2 changes from v1:** integrates `meta_planner.py` into the cognitive loop (v1 predated
its design and went straight from `replanning.should_replan()` to `planner.plan()`); fixes
a periodic-cognitive-tick pattern that was present in v1's own code sketches (see §1 and
File 6 below — this was found to match a real anti-pattern encountered reviewing an early
ROS integration attempt, and had been sitting in this guideline unflagged); adds two new
invariants (§5) and a Phase 4C dependency note (§6). Sections not touched: §2, File 1, File
3, File 4, File 7, §4, and the executor's PRIEST-dispatch logic in File 5.

---

## 0. The Big Picture

The framework has two layers:

- **`shared/`** — the cognitive layer (mind). Simulator-agnostic. Pure Python.
  Contains: `recognizer.py`, `planner.py`, `meta_planner.py`, `types.py`, `domain_knowledge.py`.
  `replanning.py` is being absorbed into `meta_planner.py` (its trigger logic becomes
  `evaluate_triggers()`) and retired once Phase 4C validates end-to-end against
  `scenario_00` — by the time `ros_sim/` is built, treat `replanning.py` as gone and
  `meta_planner.py` as the sole trigger-and-ordering module. Confirm this against the
  actual repo state before writing `ros_agents.py` — don't assume from this doc alone.
  **Never modified for ROS. Never imports from `ros_sim/` or `mesa_sim/`.**

- **`ros_sim/`** — the embodiment layer (body). ROS-specific.
  Handles: motion, world state construction, observation building, action execution.
  Calls `shared/` via plain Python function calls — same as Mesa does.
  **Executes decisions; never makes them.** If a piece of logic in `ros_sim/` is deciding
  *which* task to run next, *whether* to abandon the current one, or *whether* a conflict
  exists — that logic belongs in `shared/meta_planner.py`, not here. See Invariant 9.

The ROS team's existing code (`task_planner.py`, `planner_1.py`, etc.) is used only as
a reference for understanding the PRIEST local planner and RViz setup. Its hardcoded
task logic is entirely replaced by the framework's cognitive loop.

---

## 1. What Changes vs. Mesa, What Stays the Same

### Same as Mesa
- Cognitive loop order: `obs_builder → recognizer → meta_planner (evaluate_triggers +
  update, absorbing replanning's old trigger role) → planner → executor`
- All `shared/` types: `WorldState`, `Observation`, `BeliefState`, `AbstractPlan`,
  `GroundedAction`, `ProjectedPlan`
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
Cognitive clock  event-driven: task done / belief   (slowest — drives IR + meta_planner)
```
`shared/` is called only at the cognitive clock level for meta_planner's actual
reordering/reselection work. It does not know about motion or world state frequencies.

**Explicit warning, not just implicit from the diagram above:** the cognitive-clock
trigger must never be implemented as a fixed timer, and must never be derived
arithmetically from the motion-clock tick rate (e.g. "every K PRIEST ticks," "every 0.2s
regardless of what's happening"). A periodic poll is the easy/idiomatic default in ROS
(`rclpy` timers), so this needs to be treated as a hard constraint, not an incidental
detail — v1 of this guideline had exactly this pattern in its own File 2/File 6 sketches
(see below), which is a concrete example of how easily it creeps in even when the prose
elsewhere says "event-driven."

**Where the line actually sits, since "event-driven" alone is easy to get wrong in
practice:** `recognizer.update()` can run every world-state-clock sample — that's cheap,
continuous belief tracking, and matches "recognizer updates belief every cognitive clock
tick from the start" in `design_decisions.md` (read as *every time it's called*, not
*only on discrete events*). What must be strictly event-gated is **meta_planner's actual
candidate re-evaluation** (`update()` / `evaluate_triggers()`) — fired only on task
completion, a belief threshold θ crossing *detected from* the belief just computed, or a
task commit (holding state change). Recognizer updates cheaply and often; meta_planner
re-evaluates rarely and only on real events. Don't gate the recognizer call itself behind
an event check — gate meta_planner's heavier work instead.

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
    Owns the full cognitive loop.

    Cognitive loop — recognizer runs every world-state-clock sample (cheap);
    meta_planner's actual re-evaluation is event-gated (see §1):
        world  = build_world_state(sim_state, config)
        obs    = build_observation(sim_state, config)
        belief = recognizer.update(obs, prev_belief)          # every call, cheap
        if meta_planner.evaluate_triggers(belief, world, executor_state):
            # fires only on: task completion, theta crossing detected from the
            # belief just computed, or task commit (holding state change) —
            # never on a fixed elapsed-time period
            result = meta_planner.update(belief, world, executor_state)
            current_task, queue = result["current_task"], result["queue"]
            current_plan = planner.plan(current_task, world)
        executor.step(current_plan, world)

    Motion loop (called every PRIEST tick at 10Hz):
        executor drives PRIEST for current GroundedAction
    """
    def __init__(self, agent_id, scheduled_tasks, knowledge, initial_pos, config):
        self.recognizer = IntentionRecognizer(knowledge)
        self.meta_planner = MetaPlanner(knowledge)   # owns the task queue internally (Q1)
        self.planner = ...   # TODO: confirm actual class/import path against the
                              # current shared/planner.py — this guide previously named
                              # it AdaptivePlanner, unverified against present repo state
        self.executor = RosExecutor(agent=self, config=config)
        self.belief = None
        self.current_plan = None
        ...

    def cognitive_tick(self, sim_state: dict):
        """
        Called every world-state-clock sample. Always runs recognizer.update()
        (cheap). Only invokes meta_planner's actual re-evaluation when
        meta_planner.evaluate_triggers() reports a real event — never on a
        fixed schedule. See §1 for the recognizer-vs-meta_planner distinction.
        """
        ...

    def motion_tick(self, dt: float, sim_state: dict):
        """
        Called at PRIEST clock rate (10Hz). Drives executor only — must not
        contain any independent decision logic (no proximity-based reselect
        heuristics, no ad hoc queue reordering). See Invariant 9.
        """
        ...
```

**Important import boundary:**
```python
# ALLOWED in ros_agents.py:
from shared.recognizer import IntentionRecognizer
from shared.planner import ...          # TODO: confirm current class/function name
from shared.meta_planner import MetaPlanner
from ros_sim.world_state_builder import build_world_state
from ros_sim.obs_builder import build_observation
from ros_sim.executor import RosExecutor

# NEVER:
# from mesa_sim import anything
# from shared.replanning import anything  -- retired; confirm it's actually gone
#   from the repo before writing this file, per Phase 4C / Q4 in roadmap.md
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
    Must not contain reselect/reorder decision logic — see Invariant 9.
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
            # Note: this is real, committed execution — PRIEST handles obstacle
            # avoidance and any detour/pause dynamically. It is NOT the place to
            # add speculative interference reasoning; that belongs in
            # shared/meta_planner.py, evaluated before this action is ever
            # dispatched. (Future: if DESIGN-13's common path-realization
            # estimator is built, it affects meta_planner's cost estimation,
            # not this dispatch — see TODOS_AND_DEFERRED.md, not yet designed.)

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
                    calls cognitive_tick() every world-state-clock sample.
                    cognitive_tick() itself decides internally whether
                    meta_planner's heavier re-evaluation actually runs
                    (event-gated — see §1). The world-state-clock sample rate
                    is NOT the same thing as the cognitive-clock trigger rate;
                    do not conflate "how often we check" with "how often we
                    act" — v1 of this guideline had exactly that conflation.
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

            # world-state-clock sample: recognizer runs here (cheap, every
            # sample). meta_planner's actual re-evaluation is gated INSIDE
            # cognitive_tick() by evaluate_triggers() — not by this modulo
            # check. This modulo only controls how often we look, never
            # whether meta_planner acts.
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
| `task_planner_interrupt.py` | Discard — replaced by `shared/meta_planner.py`'s trigger logic |
| `planner_1.py`, `planner_2.py` | Discard as task/ordering/cost logic; keep as reference for node/thread structure only. Note: `planner_2.py`'s `_cognitive_tick()` contains both a fixed-period cognitive-clock poll and a hand-rolled geometric reselect heuristic running ahead of its own `should_replan()`/`reselect_or_continue()` calls — do not carry either pattern forward, even as a starting skeleton. See Invariants 8 and 9. |
| `expert.py`, `expert_interrupt.py` | Discard — hardcoded interruption rules |
| `local_planner_priest.py` | **Keep** — motion backend for `executor.py` |
| `local_planner_priest_interrupt.py` | Discard — interruption logic handled by `shared/meta_planner.py` |
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
8. **The cognitive-clock trigger (meta_planner's re-evaluation, not the recognizer call)
   must be event-driven — never a fixed timer, and never derived arithmetically from the
   motion-clock tick rate.** A periodic poll is the easy default in `rclpy` — resist it.
   See §1 for the precise line between recognizer's continuous updates and meta_planner's
   event-gated re-evaluation.
9. **The RESELECT/WAIT (or equivalent ordering) decision is made once, inside `shared/`.**
   The embodiment layer (`ros_agents.py`, `executor.py`) executes whatever decision
   `meta_planner` returns — it must never implement its own parallel heuristic capable of
   independently producing or short-circuiting that decision, even temporarily "to get a
   demo working." A shortcut placed in front of the principled path can end up being the
   only path that ever actually fires.

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
- [ ] **Prerequisite, blocking:** `shared/meta_planner.py` must exist and be validated
      against `scenario_00` (Phase 4C) before `ros_agents.py`'s cognitive loop can be
      finalized against real interfaces rather than this guide's sketch. Confirm Phase 4C
      status in roadmap.md before starting File 2.
- [ ] Confirm the actual class/function names and import path for `shared/planner.py`'s
      decomposer against current repo state — this guide's `AdaptivePlanner` reference
      (v1) was never verified and may be stale.
