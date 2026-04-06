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
    OUT: world mutations       agent.pos, item.held_by, item.at_location

COMPLETION CHECKING:
    Each GroundedAction carries a fully instantiated completion_predicate
    (Predicate with Const args). Executor checks set membership in
    WorldState.predicates directly — no string parsing, no template resolution.
"""

from __future__ import annotations
from typing import List, Optional
import math

from shared.types import AbstractPlan, GroundedAction, WorldState, Predicate
from mesa_sim.action_decomposer import Microaction, expand


class Executor:
    """
    Execution engine for one agent (human or robot).
    Instantiated per agent, owned by the agent.
    """

    def __init__(self, agent):
        self.agent = agent

        # Current tracking state
        self.current_plan: Optional[AbstractPlan] = None
        self.action_index: int = 0
        self.microaction_queue: List[Microaction] = []

        # Exposed to agent and obs_builder
        self.current_task: Optional[str] = None
        self.current_action: Optional[str] = None
        self.current_microaction: Optional[str] = None

    # =========================================================================
    # Main step — called once per Mesa step by agent.step()
    # =========================================================================

    def step(self, plan: AbstractPlan, world: WorldState):
        """
        Execute one microaction from the current plan.

        FLOW:
            1. Load plan if new or changed
            2. Get current action
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
        self.current_microaction = microaction.name

        success = self._execute(microaction)

        if success:
            self.microaction_queue.pop(0)
        else:
            self.microaction_queue = []
            self.current_microaction = None

    # =========================================================================
    # Action completion checking
    # =========================================================================

    def _is_action_complete(self, action: GroundedAction, world: WorldState) -> bool:
        """
        Check if action's completion_predicate is satisfied in WorldState.
        Direct set membership — no string parsing, no template resolution.
        """
        return action.completion_predicate in world.predicates

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
            return True  # no-op
        else:
            return False

    def _execute_step(self, microaction: Microaction) -> bool:
        """Move agent one step toward target_pos."""
        target_pos = microaction.params.get("target_pos")
        if target_pos is None:
            return False

        self.agent.model.space.move_agent(self.agent, target_pos)
        self.agent.pos = target_pos

        if self.agent.carrying:
            item = self.agent.model.items.get(self.agent.carrying)
            if item:
                item.position = target_pos

        return True

    def _execute_grasp(self, microaction: Microaction) -> bool:
        """Pick up an item. Updates agent.carrying and item state."""
        item_id = microaction.params.get("item_id")
        if not item_id:
            return False

        item = self.agent.model.items.get(item_id)
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

        return True

    def _execute_release(self, microaction: Microaction) -> bool:
        """
        Place carried item at current agent position.
        Detects target env object by proximity.
        """
        if not self.agent.carrying:
            return False

        item_id = self.agent.carrying
        item = self.agent.model.items.get(item_id)
        if item is None:
            return False

        target_id = self._nearest_env_object()
        if target_id is None:
            return False

        target_obj = self.agent.model.get_env_object(target_id)
        if target_obj is None:
            print(f"[executor] WARNING: no env object found near "
                  f"{self.agent.unique_id} for releasing {item_id}")
            return False

        print(f"[executor] {self.agent.unique_id} releasing {item_id} "
              f"at {target_id} ({target_obj.obj_type})")

        item.held_by = None
        item.at_location = target_id
        item.position = target_obj.position
        item.zone = target_obj.zone
        self.agent.carrying = None

        return True

    def _nearest_env_object(self) -> Optional[str]:
        """Find closest non-obstacle env object to agent. Used by release."""
        agent_x, agent_y = self.agent.pos
        nearest_id = None
        nearest_dist = float("inf")

        for obj_id, obj in self.agent.model.env_objects.items():
            if obj.obj_type == "obstacle":
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

    def _load_plan(self, plan: AbstractPlan):
        """Load a new plan, resetting action index and queue."""
        self.current_plan = plan
        self.action_index = 0
        self.microaction_queue = []
        self.current_task = plan.goal_intention

    def _advance_action(self):
        """Move to next action in plan."""
        self.action_index += 1
        self.microaction_queue = []
        self.current_microaction = None

    def _on_task_complete(self):
        """Called when all actions in plan are done."""
        self.current_task = None
        self.current_action = None
        self.current_microaction = None
        self.microaction_queue = []

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