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
import logging
from typing import List, Optional
import math

from shared.types import AbstractPlan, GroundedAction, WorldState, Predicate, ProcessCompletion
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
        self._queue_was_exhausted: bool = False

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
            return True  # no-op
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