"""
shared/domain_knowledge.py

PURPOSE:
    Central access point for domain knowledge used by the cognitive layer.
    Receives a DomainModel at construction — no YAML parsing for operators.

WHAT THIS MODULE DOES:
    - Accepts a DomainModel (from domains/kitting/registry.py or equivalent)
    - Exposes clean query methods returning typed objects, not strings
    - Optionally loads costs.yaml for cost-based planning (Phase 4)
    - Provides reverse-lookup methods for the intention recognizer

WHAT THIS MODULE DOES NOT DO:
    - Does NOT parse YAML for task or action operator definitions
    - Does NOT resolve variable bindings (that is shared/planner.py)
    - Does NOT know about Mesa, ROS, or any simulator
    - Does NOT handle scenarios or agent assignments (that is sim_model.py)

USED BY:
    - shared/recognizer.py   → get_all_intentions(), get_tasks_for_action()
    - shared/planner.py      → get_task_schema(), get_action_operator()
    - mesa_sim/executor.py   → get_action_operator()
    - mesa_sim/sim_agents.py → get_task_schema()
"""

import yaml
from typing import Dict, List, Optional

from shared.types import DomainModel, TaskSchema, ActionOperator


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

    # =========================================================================
    # Task queries
    # =========================================================================

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

    # =========================================================================
    # Action queries
    # =========================================================================

    def get_action_operator(self, action_name: str) -> Optional[ActionOperator]:
        """Return ActionOperator for an action type, or None if not found."""
        return self._domain.actions.get(action_name)

    def get_microactions(self) -> List[str]:
        """Terminal microactions: ['STEP', 'GRASP', 'RELEASE', 'STAND']."""
        return self._domain.microactions

    # =========================================================================
    # Reverse lookups — used by recognizer for bottom-up inference
    # =========================================================================

    def get_tasks_for_action(self, action_name: str) -> List[TaskSchema]:
        """
        Return all task schemas whose methods contain a step calling this action.
        Used by recognizer: observed action → candidate tasks.
        """
        return self._domain.get_tasks_for_action(action_name)

    def get_actions_for_microaction(self, mu: str) -> List[ActionOperator]:
        """
        Return all action operators that decompose to this microaction.
        Used by recognizer: observed microaction → candidate actions.
        """
        return self._domain.get_actions_for_microaction(mu)

    # =========================================================================
    # Cost data (Phase 4)
    # =========================================================================

    def get_cost(self, key: str) -> Optional[float]:
        """Return cost value by key from costs.yaml, or None if not found."""
        return self._costs.get(key)