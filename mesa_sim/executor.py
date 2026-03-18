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
        - Script entry is converted to a minimal plan-like structure internally

WHAT THIS MODULE DOES NOT DO:
    - Does NOT do planning or replanning — that is shared/planner.py
    - Does NOT build WorldState — that is world_state_builder.py
    - Does NOT build Observations — that is obs_builder.py
    - Does NOT expand AbstractActions — that is action_decomposer.py
    - Does NOT know about IR or belief states

I/O:
    IN:  AbstractPlan          from RobotAgent.current_plan
    IN:  WorldState            built fresh each step by world_state_builder
    IN:  model                 for physical world mutation
    OUT: current_task          str — exposed on agent
    OUT: current_action        str — exposed on agent
    OUT: current_microaction   str — exposed on agent, read by obs_builder
    OUT: world mutations       agent.pos, item.held_by, item.at_location

COMPLETION CHECKING:
    Each action has a completion_predicate template in actions_library.yaml
    e.g. "at({agent_id}, {zone_id})"
    Executor resolves template with current parameters → Predicate object
    Checks if that Predicate exists in WorldState.predicates
    If yes → action complete, advance to next

PHYSICAL EXECUTION (Mesa-specific):
    STEP    → move agent (and carried item) to target_pos via space.move_agent()
    GRASP   → update item.held_by, item.at_location, agent.carrying
    RELEASE → update item.held_by, item.at_location, agent.carrying
    STAND   → no-op, agent stays in place
"""

from __future__ import annotations
from typing import List, Optional, Dict, Any
import math

from shared.types import AbstractPlan, AbstractAction, WorldState
from shared.types import Predicate
from shared.knowledge import KnowledgeBase
from mesa_sim.action_decomposer import Microaction, expand, steps_toward


class Executor:
    """
    Execution engine for one agent (human or robot).
    Instantiated per agent, owned by the agent.
    """

    def __init__(self, agent, knowledge: KnowledgeBase):
        self.agent = agent
        self.knowledge = knowledge

        # Current tracking state
        self.current_plan: Optional[AbstractPlan] = None
        self.action_index: int = 0                      # index into plan.actions
        self.microaction_queue: List[Microaction] = []  # expanded from current action

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

        INPUT:
            plan   — current AbstractPlan from robot/human
            world  — fresh WorldState snapshot from world_state_builder

        FLOW:
            1. Load plan if new or changed
            2. Check if current action is complete → advance if so
            3. Expand microaction queue if empty
            4. Execute one microaction
            5. Update tracking attributes
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
            # All actions done — task complete
            self._on_task_complete()
            return

        action = self.current_plan.actions[self.action_index]
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
                # Expansion failed — cannot proceed
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
            # Failed microaction — clear queue, will retry expansion next step
            self.microaction_queue = []
            self.current_microaction = None

    # =========================================================================
    # Action completion checking
    # =========================================================================

    def _is_action_complete(self, action: AbstractAction, world: WorldState) -> bool:
        """
        Check if action's completion_predicate is satisfied in WorldState.
        Resolves parameter placeholders from action.parameters + agent context.
        """
        predicate_template = self.knowledge.get_action_completion_predicate(
            action.action_name
        )
        if not predicate_template:
            return False

        resolved = self._resolve_predicate(predicate_template, action.parameters)
        if resolved is None:
            return False

        return resolved in world.predicates

    def _resolve_predicate(
        self, template: str, params: Dict[str, Any]
    ) -> Optional[Predicate]:
        """
        Resolve a completion_predicate template string into a Predicate object.

        Template format: "at({agent_id}, {zone_id})"
        Resolution context: action.parameters + agent_id from agent

        Returns None if template cannot be fully resolved.

        TODO Phase 4: handle nested resolution e.g. {item_zone} → zone of item
        """
        # Build resolution context
        context = dict(params)
        context["agent_id"] = self.agent.unique_id

        # Parse template: "predicate_name(arg1, arg2, ...)"
        try:
            name_part, args_part = template.split("(", 1)
            args_part = args_part.rstrip(")")
            name = name_part.strip()
            raw_args = [a.strip() for a in args_part.split(",")]

            resolved_args = []
            for arg in raw_args:
                if arg.startswith("{") and arg.endswith("}"):
                    key = arg[1:-1]
                    value = context.get(key)
                    if value is None:
                        return None  # unresolvable placeholder
                    resolved_args.append(str(value))
                else:
                    resolved_args.append(arg)

            return Predicate(name=name, args=tuple(resolved_args))

        except Exception:
            return None

    # =========================================================================
    # Microaction queue expansion
    # =========================================================================

    def _expand_queue(self, action: AbstractAction):
        """
        Expand current action into microaction queue.
        For STEP-based movement, uses steps_toward() with agent's current pos.
        """
        action_name = action.action_name.upper() if action.action_name else ""

        if action_name in ("GOTO_ZONE", "MOVE_TO"):
            # Movement: generate STEP sequence from current pos to target
            from mesa_sim.action_decomposer import _resolve_target_position, _get_step_size
            target_pos = _resolve_target_position(
                action_name, action.parameters, self.agent.model
            )
            if target_pos:
                step_size = _get_step_size(self.agent.model)
                self.microaction_queue = steps_toward(
                    current_pos=self.agent.pos,
                    target_pos=target_pos,
                    step_size=step_size,
                )
        else:
            # Non-movement actions: use standard expand()
            self.microaction_queue = expand(action, self.agent.model)

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
            return True  # no-op, agent stays in place
        else:
            return False

    def _execute_step(self, microaction: Microaction) -> bool:
        """Move agent one step toward target_pos."""
        target_pos = microaction.params.get("target_pos")
        if target_pos is None:
            return False

        # Move agent in Mesa space
        self.agent.model.space.move_agent(self.agent, target_pos)
        self.agent.pos = target_pos

        # If carrying an item, sync item position
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

        # Cannot grasp if already carrying something
        if self.agent.carrying:
            return False

        # Cannot grasp if item already held by someone else
        if item.held_by and item.held_by != self.agent.unique_id:
            return False

        # Update item state
        item.held_by = self.agent.unique_id
        item.at_location = None  # no longer at a shelf
        item.position = self.agent.pos

        # Update agent state
        self.agent.carrying = item_id

        return True

    def _execute_release(self, microaction: Microaction) -> bool:
        """Place carried item at target location. Updates item state."""
        if not self.agent.carrying:
            return False

        item_id = self.agent.carrying
        item = self.agent.model.items.get(item_id)
        if item is None:
            return False

        target = microaction.params.get("target", "")

        # Verify target env object exists
        target_obj = self.agent.model.get_env_object(target)
        if target_obj is None:
            return False

        # Update item state
        item.held_by = None
        item.at_location = target
        item.position = target_obj.position

        # Update agent state
        self.agent.carrying = None

        return True

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

        # Signal agent to advance to next task
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
