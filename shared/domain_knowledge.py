"""
shared/domain_knowledge.py

PURPOSE:
    Knowledge layer for the cognitive layer. Contains two classes:
    - DomainKnowledgeBase: structural HTN knowledge (tasks, actions, intentions)
    - ContextKnowledge: background context facts (shift info, environment state)
      used by IR for ω_context weighting

WHAT THIS MODULE DOES:
    - Accepts a DomainModel (from domains/<domain>/registry.py)
    - Exposes clean query methods returning typed objects, not strings
    - Optionally loads costs.yaml for cost-based planning (Phase 4)
    - Provides reverse-lookup methods for the intention recognizer
    - Holds slowly-changing background context facts for IR context weighting

WHAT THIS MODULE DOES NOT DO:
    - Does NOT parse YAML for task or action schema definitions
    - Does NOT resolve variable bindings (that is shared/planner.py)
    - Does NOT know about Mesa, ROS, or any simulator
    - Does NOT hold observable/sensor-based state (that is WorldState)
    - Does NOT handle scenarios or agent assignments (that is sim_model.py)

USED BY:
    - shared/recognizer.py   → get_all_intentions(), get_tasks_for_action(), ContextKnowledge
    - shared/planner.py      → get_task_schema(), get_action_schema()
    - mesa_sim/executor.py   → get_action_schema()
    - mesa_sim/sim_agents.py → get_task_schema(), ContextKnowledge.default()
"""

import yaml
from typing import Dict, List, Optional

from shared.types import DomainModel, TaskSchema, ActionSchema

# ========================================================================
# Class domain-specific knowledge bases here, e.g. KittingDomainKnowledgeBase, if we want to add domain-specific helper methods.
# ========================================================================
class DomainKnowledgeBase:

    def __init__(self, domain: DomainModel, costs_data: dict = None):
        self._domain = domain
        self._costs = costs_data or {}

    @classmethod
    def from_domain(cls, domain: DomainModel, costs_path: str = None) -> "DomainKnowledgeBase":
        """
        Primary constructor. Accepts a pre-built DomainModel.
        Optionally loads costs.yaml for Phase 4 cost-based planning.
        """
        costs_data = {}
        if costs_path:
            with open(costs_path, "r") as f:
                costs_data = yaml.safe_load(f)
        return cls(domain, costs_data)
    
    # ----------------------------------------------------------------------
    # Task queries
    # ----------------------------------------------------------------------
 
    def get_task_schema(self, task_name: str) -> Optional[TaskSchema]:
        """Return TaskSchema for a task type, or None if not found."""
        return self._domain.tasks.get(task_name)

    def get_all_intentions(self) -> List[str]:
        """All task names registered as valid IR hypotheses."""
        return list(self._domain.intentions)

    def get_assigned_intentions(self) -> List[str]:
        """Tasks that are part of the team assignment."""
        return [name for name in self._domain.intentions
                if self._domain.tasks[name].is_assigned]

    def get_foreseeable_intentions(self) -> List[str]:
        """Tasks that are foreseeable human deviations."""
        return [name for name in self._domain.intentions
                if self._domain.tasks[name].is_foreseeable]

    def get_intention_schemas(self) -> List[TaskSchema]:
        """Full TaskSchema objects for all registered intentions."""
        return [self._domain.tasks[name] for name in self._domain.intentions]

    # def get_objects_by_type(self, type: str) -> List[str]:
    #     return self._objects_by_type.get(type, [])
    # ----------------------------------------------------------------------
    # Action queries
    # ----------------------------------------------------------------------

    def get_action_schema(self, action_name: str) -> Optional[ActionSchema]:
        """Return ActionSchema for an action type, or None if not found."""
        return self._domain.actions.get(action_name)

    def get_microactions(self) -> List[str]:
        """Terminal microactions: ['STEP', 'GRASP', 'RELEASE', 'STAND']."""
        return self._domain.microactions

    # ----------------------------------------------------------------------
    # Reverse lookups — used by recognizer for bottom-up inference
    # ----------------------------------------------------------------------

    def get_tasks_for_action(self, action_name: str) -> List[TaskSchema]:
        """
        Return all task schemas whose methods contain a step calling this action.
        Used by recognizer: observed action → candidate tasks.
        """
        return self._domain.get_tasks_for_action(action_name)

    def get_actions_for_microaction(self, mu: str) -> List[ActionSchema]:
        """
        Return all action schemas that decompose to this microaction.
        Used by recognizer: observed microaction → candidate actions.
        """
        return self._domain.get_actions_for_microaction(mu)

    # ----------------------------------------------------------------------
    # Cost data (Phase 4)
    # ----------------------------------------------------------------------

    def get_cost(self, key: str) -> Optional[float]:
        """Return cost value by key from costs.yaml, or None if not found."""
        return self._costs.get(key)
    
    
    
# ========================================================================
# Context knowledge — e.g. shift duration, room temperature, etc. that may affect human
# behavior and should be considered by the intention recognizer and planner.
# ========================================================================

class ContextKnowledge:
    def __init__(
        self,
        shift_start_step: int = 0,
        room_temperature: float = 21.0,   # default comfortable temperature
        metadata: dict = None,
    ):
        self.shift_start_step = shift_start_step
        self.room_temperature = room_temperature
        self.metadata = metadata or {}

    @classmethod
    def default(cls) -> "ContextKnowledge":
        """Default context — used when no external context source is available."""
        return cls()

    def shift_duration(self, current_step: int) -> int:
        """Steps elapsed since shift start — proxy for fatigue."""
        return current_step - self.shift_start_step
    