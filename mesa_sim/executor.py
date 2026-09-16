"""
mesa_sim/executor.py

PURPOSE:
    Task/action tracking and microaction execution engine for Mesa agents.
    This is where AbstractPlans become physical world changes.

WHAT THIS MODULE DOES:
    For RobotAgent:
        - Tracks current position in AbstractPlan (action index)
        - Maintains a microaction queue for the current action
        - Executes one microaction per Mesa step
        - Checks completion_predicate against WorldState after each microaction
        - Advances to next action when current action is complete
        - Signals task completion to agent when all actions done
        - On a CONTINUE decision (the meta-planner re-selected the task already
          executing; io_contracts.md §1.9) adopts the fresh decomposition via
          continue_plan() without restarting: the action in flight keeps its
          microaction queue, so the tick is spent exactly as if no trigger had
          fired. A plan handed to step() any other way is loaded from its start.
        - Executes the hold a decision carries (UpdateResult.hold, T4) via
          hold(): one STAND per tick at the agent's position, starting on the
          decision tick, before the plan continues. Every decision replaces
          the hold; the executor never decides on its own whether to wait
          (TODO-71).
        - The execution-time SEPARATION STOP (C, TODO-73; a run option,
          `separation_stop`, off by default): before a STEP microaction is
          executed, the step is checked against every human's ACTUAL
          position this tick under the F1 rule (robot-responsible
          separation, design_decisions.md): the step is refused if at any
          point along it the robot–human distance is below min_separation
          and not strictly increasing. A refused step is a STAND this tick
          and is retried next tick; the plan cursor and microaction queue are
          untouched. Only STEP is checked — grasp, release, stand and the
          decided hold are stationary and always admissible. A SAFETY
          category, not a planning choice: it never shortens or cancels a
          decided hold, never advances the plan, and decides nothing about
          whether to wait for planning reasons or which task to run.

    For HumanAgent:
        - Same structure, but driven by script entries instead of AbstractPlan
        - Script entry is converted to a minimal GroundedAction plan internally

WHAT THIS MODULE DOES NOT DO:
    - Does NOT do planning or replanning — that is shared/planner.py
    - Does NOT build WorldState — that is world_state_builder.py
    - Does NOT build Observations — that is obs_builder.py
    - Does NOT expand GroundedActions — that is action_decomposer.py
    - Does NOT know about IR or belief states
    - Does NOT parse strings — completion checking is direct Predicate set membership

I/O:
    IN:  AbstractPlan          from RobotAgent.current_plan (actions are GroundedActions)
    IN:  WorldState            built fresh each step by world_state_builder
    IN:  model                 for physical world mutation
    OUT: current_task          str — exposed on agent
    OUT: current_action        str — exposed on agent
    OUT: current_microaction   str — exposed on agent, read by obs_builder
    OUT: world mutations       agent.pos, item.held_by, item.at_location,
                               agent.waited_at (the fixed object a completed wait
                               ended at; world_state_builder emits waited(agent, obj)
                               from it, as holding(agent, item) comes from carrying)

COMPLETION CHECKING:
    Each GroundedAction carries a fully instantiated completion_predicate
    (Predicate with Const args). Executor checks set membership in
    WorldState.predicates directly — no string parsing, no template resolution.
"""

from __future__ import annotations
import logging
from typing import List, Optional, Tuple
import math

from shared.types import AbstractPlan, GroundedAction, WorldState, Predicate, ProcessCompletion
from mesa_sim.action_decomposer import Microaction, expand


# Mesa ticks this executor spends LEARNING that an action finished, per action.
# Exactly one: step() sees the completion predicate hold in the WorldState it was
# handed, calls _advance_action() and returns, executing no microaction that tick
# (section 3 of step() below). So a four-action delivery pays four such ticks, and
# they are as real as the walking. Lives here because it is a property of this
# loop, the way PROXIMITY_THRESHOLD is a property of world_state_builder's `at`;
# mesa_sim/sim_agents.py hands it to the Projector so projection time matches
# execution time (L2). Not a tunable: change step()'s structure and this changes
# with it.
ACTION_COMPLETION_LATENCY = 1.0

# Mesa ticks this executor spends COMPLETING a task, after its last action's
# acknowledgement and before the next task's first microaction. Exactly one:
# the tick on which step() finds action_index past the plan's end, calls
# _on_task_complete() (which advances the agent's script or clears its task)
# and returns. The next tick loads the next plan and executes its first
# microaction in the same call. Both agents pay it — the human through
# advance_script(), the robot through advance_task() and the no_current_task
# trigger on the following tick. Handed to the Projector as a per-task
# stationary segment at the end of every projected task (F1; the L2 report
# left it unmodelled). Not a tunable: change step()'s structure and this
# changes with it.
TASK_COMPLETION_LATENCY = 1.0


class Executor:
    """
    Execution engine for one agent (human or robot).
    Instantiated per agent, owned by the agent.
    """

    def __init__(self, agent, separation_stop: Optional[float] = None):
        """
        separation_stop: min_separation in world units when the execution-time
        separation stop is ON for this agent (the robot: the same value its
        MetaPlanner hands to realize()), None when off or for the human, which
        gets no avoidance rule.
        """
        self.agent = agent
        self._separation_stop = separation_stop
        # The assessed window of the decision in effect (decision tick, T_h on
        # that decision's projection clock, or None when no projection was
        # admitted), set by the agent on every decision; for the [stop] log's
        # inside / outside label only. Nothing decides on it.
        self._window: Tuple[Optional[int], Optional[float]] = (None, None)

        # Current tracking state
        self.current_plan: Optional[AbstractPlan] = None
        self.action_index: int = 0
        self.microaction_queue: List[Microaction] = []

        # Exposed to agent and obs_builder
        self.current_task: Optional[str] = None
        self.current_action: Optional[str] = None
        self.current_microaction: Optional[str] = None
        self._queue_was_exhausted: bool = False

        # The decided hold (T4): STAND ticks still to run before the plan
        # continues, and its planned / executed lengths for the [hold] log.
        self._hold_remaining: int = 0
        self._hold_planned: int = 0
        self._hold_executed: int = 0

    # =========================================================================
    # Main step — called once per Mesa step by agent.step()
    # =========================================================================

    def step(self, plan: AbstractPlan, world: WorldState):
        """
        Execute one microaction from the current plan.

        FLOW:
            1. Load plan if new or changed
            2. Get current action
            2b. Run a decided hold's STAND, if one is in progress
            3. Check if current action is complete → advance if so
            4. Expand microaction queue if empty
            5. Execute one microaction
        """

        # ------------------------------------------------------------------
        # 1. Load or update plan
        # ------------------------------------------------------------------
        if plan is None:
            self._clear()
            return

        if plan is not self.current_plan:
            self._load_plan(plan)

        # ------------------------------------------------------------------
        # 2. Get current action
        # ------------------------------------------------------------------
        if self.action_index >= len(self.current_plan.actions):
            self._on_task_complete()
            return

        action: GroundedAction = self.current_plan.actions[self.action_index]
        self.current_task = self.current_plan.goal_intention
        self.current_action = action.action_name

        # ------------------------------------------------------------------
        # 2b. A decided hold runs first: stand where the agent is this tick,
        #     leaving the plan cursor and microaction queue untouched
        # ------------------------------------------------------------------
        if self._hold_remaining > 0:
            stand = Microaction(name="stand")
            self.current_microaction = stand.name
            self._execute(stand)
            self._hold_remaining -= 1
            self._hold_executed += 1
            if self._hold_remaining == 0:
                self._log_hold_end(interrupted_by=None)
            return

        # ------------------------------------------------------------------
        # 3. Check if current action is already complete
        # ------------------------------------------------------------------
        if self._is_action_complete(action, world):
            self._advance_action()
            return

        # ------------------------------------------------------------------
        # 4. Expand microaction queue if empty
        # ------------------------------------------------------------------
        if not self.microaction_queue:
            self._expand_queue(action)
            if not self.microaction_queue:
                self.current_microaction = None
                return

        # ------------------------------------------------------------------
        # 5. Execute one microaction
        # ------------------------------------------------------------------
        microaction = self.microaction_queue[0]

        # 5a. The separation stop (C): a STEP that would break the F1 rule
        #     against a human's actual position this tick is a STAND instead;
        #     queue and cursor untouched, retried next tick.
        if self._separation_stop is not None and microaction.name.lower() == "step":
            blocked = self._separation_blocked(microaction)
            if blocked is not None:
                self.current_microaction = "stand"
                self._execute(Microaction(name="stand"))
                self._log_stop(action, blocked)
                return

        self.current_microaction = microaction.name

        success = self._execute(microaction)

        if success:
            self.microaction_queue.pop(0)
            if not self.microaction_queue:
                self._queue_was_exhausted = True
        else:
            self.microaction_queue = []
            self.current_microaction = None

    # =========================================================================
    # Action completion checking
    # =========================================================================

    def _is_action_complete(self, action: GroundedAction, world: WorldState) -> bool:
        """
        Check if action is complete.
        Branches on completion type declared in the action schema:
        - ConditionSchema: checks completion_predicate membership in WorldState.predicates
        - ProcessCompletion: checks if microaction queue was fully exhausted
        No string parsing, no template resolution.
        """
        if isinstance(action.schema.completion, ProcessCompletion):
            result = self._queue_was_exhausted
        else:
            result = action.completion_predicate in world.predicates
        
        # if self.agent.unique_id == "human_0":
        #     logging.info(f"[executor] is_complete: {action.action_name} → {result} predicate={getattr(action, 'completion_predicate', None)}")
        
        return result

    # =========================================================================
    # Microaction queue expansion
    # =========================================================================

    def _expand_queue(self, action: GroundedAction):
        """
        Expand current GroundedAction into microaction queue.
        Fully delegates to action_decomposer.expand() — no domain logic here.
        Target resolution for movement actions is handled inside expand().
        """
        self.microaction_queue = expand(action, self.agent.model, self.agent.pos)



    # =========================================================================
    # Physical microaction execution
    # =========================================================================

    def _execute(self, microaction: Microaction) -> bool:
        """
        Physically execute one microaction in Mesa.
        Mutates agent position and/or item state in model.
        Returns True if successful, False if failed.
        """
        name = microaction.name.lower()

        if name == "step":
            return self._execute_step(microaction)
        elif name == "grasp":
            return self._execute_grasp(microaction)
        elif name == "release":
            return self._execute_release(microaction)
        elif name == "stand":
            return self._execute_stand(microaction)
        elif name == "touch":
            return self._execute_touch(microaction)
        else:
            return False

    def _execute_step(self, microaction: Microaction) -> bool:
        """Move agent one step toward target_pos."""
        target_pos = microaction.params.get("target_pos")
        if target_pos is None:
            return False

        self.agent.model.space.move_agent(self.agent, target_pos)
        self.agent.pos = target_pos
        self.agent.waited_at = None

        if self.agent.carrying:
            item = self.agent.model.objects.get(self.agent.carrying)
            if item:
                item.position = target_pos

        return True

    def _execute_grasp(self, microaction: Microaction) -> bool:
        """Pick up an item. Updates agent.carrying and item state."""
        item_id = microaction.params.get("item_id")
        if not item_id:
            return False

        item = self.agent.model.objects.get(item_id)
        if item is None:
            return False

        if self.agent.carrying:
            return False

        if item.held_by and item.held_by != self.agent.unique_id:
            return False

        item.held_by = self.agent.unique_id
        item.at_location = None
        item.position = self.agent.pos
        self.agent.carrying = item_id
        self.agent.waited_at = None

        return True

    def _execute_release(self, microaction: Microaction) -> bool:
        """
        Place carried item at current agent position.
        Detects target env object by proximity.
        """
        if not self.agent.carrying:
            return False

        item_id = self.agent.carrying
        item = self.agent.model.objects.get(item_id)
        if item is None:
            return False

        target_id = self._nearest_env_object()
        if target_id is None:
            return False

        target_obj = self.agent.model.get_object(target_id)
        if target_obj is None:
            logging.warning(f"[executor] WARNING: no env object found near "
                  f"{self.agent.unique_id} for releasing {item_id}")
            return False


        item.held_by = None
        item.at_location = target_id
        item.position = target_obj.position
        item.zone = target_obj.zone
        self.agent.carrying = None
        self.agent.waited_at = None

        return True

    def _execute_touch(self, microaction: Microaction) -> bool:
        """Scan an item. Sets item.is_scanned = True."""
        item_id = microaction.params.get("item_id")
        if not item_id:
            return False
        item = self.agent.model.objects.get(item_id)
        if item is None:
            return False
        item.is_scanned = True
        self.agent.waited_at = None
        return True

    def _execute_stand(self, microaction: Microaction) -> bool:
        """
        Stand still for one tick. On the last STAND of a wait (remaining == 1,
        see action_decomposer._expand_stand) the body records where the wait
        ended — the nearest fixed object, the same proximity rule release uses
        for its target — so that world_state_builder can emit
        waited(agent, object). The wait's end is a body fact: the body runs
        the timer, so the body says when it is over, the way a grasp makes
        holding true. Cleared by the next step/grasp/release/touch — the fact
        describes an agent that has finished waiting and not yet moved on.
        """
        if microaction.params.get("remaining") == 1:
            self.agent.waited_at = self._nearest_env_object()
        return True

    def _nearest_env_object(self) -> Optional[str]:
        """Find closest non-obstacle, non-portable object to agent. Used by release.
        CHECK LATER: obj.at_location is not None is the same "is this a portable object" signal we used 
                        in world_state_builder.py — consistent criterion across both files now.
        """
        agent_x, agent_y = self.agent.pos
        nearest_id = None
        nearest_dist = float("inf")

        for obj_id, obj in self.agent.model.objects.items():
            if obj.type == "obstacle" or obj.is_portable:
                continue
            ox, oy = obj.position
            dist = math.sqrt((agent_x - ox) ** 2 + (agent_y - oy) ** 2)
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_id = obj_id

        return nearest_id

    # =========================================================================
    # Plan management helpers
    # =========================================================================

    def continue_plan(self, plan: AbstractPlan):
        """
        Adopt `plan` as the fresh decomposition of the task ALREADY executing
        (a continue decision, TODO-43): re-decomposition stays, execution
        progress survives. If the action in flight appears in the new plan,
        the cursor moves to it and the microaction queue and completion
        bookkeeping are kept — the tick then proceeds exactly as it would
        have with no trigger, whether that is a step, the acknowledgement of
        an action the world already shows complete, or the next grasp. If it
        does not appear — the world moved and the decomposition genuinely
        changed, e.g. task_committed after a pick_up selects a method with no
        pick_up — the plan is loaded from its start as any new plan is; the
        world remains the cursor. Same-action is dataclass equality on the
        GroundedAction (name, bindings, completion predicate, schema), never
        object identity: the planner builds fresh objects every call.
        """
        if self.current_plan is None or self.action_index >= len(self.current_plan.actions):
            self._load_plan(plan)
            return
        in_flight = self.current_plan.actions[self.action_index]
        index = next((i for i, a in enumerate(plan.actions) if a == in_flight), None)
        if index is None:
            self._load_plan(plan)
            return
        logging.info(f"[executor] continue_plan: {self.agent.unique_id} goal={plan.goal_intention} "
                     f"actions={len(plan.actions)} action_index {self.action_index}->{index} "
                     f"queue_len={len(self.microaction_queue)}")
        self.current_plan = plan
        self.action_index = index
        self.current_task = plan.goal_intention

    def hold(self, ticks: int, trigger: str):
        """
        Adopt the hold of the decision just taken (UpdateResult.hold, whole
        ticks; T4, TODO-71): stand still for `ticks` ticks, starting with this
        tick's step(), then continue the plan. Called on EVERY decision, so a
        later trigger's decision replaces a hold in progress — re-realized
        from where the agent now stands, or 0 when that decision carries none
        — and the ticks not yet run are logged as interrupted by `trigger`.
        The executor adds no hold of its own and drops none silently.
        The STAND carries no `remaining` param, so it records no waited_at:
        a hold is not a wait_at action and makes no world fact true.
        """
        if self._hold_remaining > 0:
            self._log_hold_end(interrupted_by=trigger)
        self._hold_remaining = ticks
        self._hold_planned = ticks
        self._hold_executed = 0
        if ticks > 0:
            logging.info(f"[hold] step={int(self.agent.model.schedule.steps)} {self.agent.unique_id} "
                         f"start planned={ticks} trigger={trigger} pos={tuple(round(float(c), 2) for c in self.agent.pos)}")

    # =========================================================================
    # The execution-time separation stop (C, TODO-73)
    # =========================================================================

    def set_assessed_window(self, decision_tick: int, horizon: Optional[float]):
        """The decision in effect: its tick and T_h (None: no projection). Log label only."""
        self._window = (decision_tick, horizon)

    def _separation_blocked(self, microaction: Microaction):
        """
        The F1 rule on one step, against each human's ACTUAL position this tick
        (Mesa's scheduler has already moved the human, so it stands at `human.pos`
        while the robot steps): the step from the agent's position r0 to
        `target_pos` r1 is REFUSED if at any point along it the distance to the
        human is below min_separation and not strictly increasing. With the
        human fixed and the robot on a straight line, the distance is convex in
        the step parameter t ∈ [0, 1] with its minimum at
        t* = clamp(−(r0 − h)·(r1 − r0) / |r1 − r0|², 0, 1): decreasing before t*,
        increasing after. So the step is clear iff t* = 0 (the distance
        increases from the first instant, whatever its value — moving away is
        never a violation) or the minimum d(t*) ≥ min_separation (the step never
        comes within it). Otherwise the decreasing stretch up to t* lies below
        min_separation: rule (a) if the step started at or beyond it, rule (b)
        if within. Exact; the whole step, not its endpoint. A step starting
        exactly perpendicular to the human (t* = 0, derivative 0 for one
        instant) is clear, as realization's interval endpoints are.
        Returns (human_id, human_pos, distance now, minimum along the step) for
        the first blocking human, else None.
        """
        target = microaction.params.get("target_pos")
        if target is None:
            return None
        s = self._separation_stop
        r0 = (float(self.agent.pos[0]), float(self.agent.pos[1]))
        r1 = (float(target[0]), float(target[1]))
        ex, ey = r1[0] - r0[0], r1[1] - r0[1]
        ee = ex * ex + ey * ey
        if ee == 0.0:
            return None
        for hid, human in self.agent.model.humans.items():
            h = (float(human.pos[0]), float(human.pos[1]))
            dx, dy = r0[0] - h[0], r0[1] - h[1]
            t = -(dx * ex + dy * ey) / ee
            if t <= 0.0:
                continue
            t = min(1.0, t)
            d_min = math.hypot(dx + t * ex, dy + t * ey)
            if d_min < s:
                return (hid, h, math.hypot(dx, dy), d_min)
        return None

    def _log_stop(self, action: GroundedAction, blocked):
        hid, h, d_now, d_min = blocked
        tick = int(self.agent.model.schedule.steps)
        decision, horizon = self._window
        if decision is None:
            window = "outside(no_decision)"
        elif horizon is None:
            window = "outside(no_projection)"
        else:
            start, end = tick - decision, tick - decision + 1   # the step on the projection clock
            if start >= 1.0 and end <= horizon:
                window = "inside"
            elif start >= horizon:
                window = "outside(past_T_h)"
            elif end <= 1.0:
                window = "outside(offset)"
            else:
                window = "edge"
        target = ",".join(str(c.value) for c in action.completion_predicate.args) if action.completion_predicate else ""
        logging.info(
            f"[stop] step={tick} {self.agent.unique_id} human={hid} "
            f"pos=({self.agent.pos[0]:.2f}, {self.agent.pos[1]:.2f}) human_pos=({h[0]:.2f}, {h[1]:.2f}) "
            f"dist={d_now:.2f} step_min={d_min:.2f} action={action.action_name}({target}) "
            f"window={window} decision={decision} T_h={'None' if horizon is None else f'{horizon:.2f}'}"
        )

    def _log_hold_end(self, interrupted_by: Optional[str]):
        logging.info(f"[hold] step={int(self.agent.model.schedule.steps)} {self.agent.unique_id} "
                     f"end planned={self._hold_planned} executed={self._hold_executed} "
                     f"interrupted={interrupted_by is not None}"
                     + (f" by={interrupted_by}" if interrupted_by is not None else ""))
        self._hold_remaining = 0

    def _load_plan(self, plan: AbstractPlan):
        """Load a new plan, resetting action index and queue."""
        logging.info(f"[executor] _load_plan: {self.agent.unique_id} goal={plan.goal_intention} actions={len(plan.actions)}")
        
        self.current_plan = plan
        self.action_index = 0
        self.microaction_queue = []
        self.current_task = plan.goal_intention
        self._queue_was_exhausted = False

    def _advance_action(self):
        """Move to next action in plan."""
        self.action_index += 1
        self.microaction_queue = []
        self.current_microaction = None
        self._queue_was_exhausted = False
        # logging.info(f"[executor] _advance_action: {self.agent.unique_id} {self.action_index} → {self.action_index+1}")

    def _on_task_complete(self):
        """Called when all actions in plan are done."""
        self.current_task = None
        self.current_action = None
        self.current_microaction = None
        self.microaction_queue = []
        
        logging.info(f"[executor] _on_task_complete: {self.agent.unique_id} action_index={self.action_index} plan_len={len(self.current_plan.actions)}")

        if hasattr(self.agent, "advance_task"):
            self.agent.advance_task()
        elif hasattr(self.agent, "advance_script"):
            self.agent.advance_script()

    def _clear(self):
        """Clear all execution state."""
        self.current_plan = None
        self.action_index = 0
        self.microaction_queue = []
        self.current_task = None
        self.current_action = None
        self.current_microaction = None