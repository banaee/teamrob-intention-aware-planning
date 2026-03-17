"""
shared/knowledge.py

PURPOSE:
    Load and expose domain knowledge from YAML config files.
    This is the read-only source of truth for the cognitive layer.

WHAT THIS MODULE DOES:
    - Loads tasks_library.yaml and actions_library.yaml at startup
    - Exposes the intention set T (all known task types)
    - Exposes task decompositions: τ → [a1, a2, ...]
    - Exposes action decompositions: a → [μ1, μ2, ...] or "STEP*"
    - Exposes the micro-action set M

WHAT THIS MODULE DOES NOT DO:
    - Does NOT instantiate task instances (that is the planner's job)
    - Does NOT bind parameters like {item_zone} (resolved at runtime by planner)
    - Does NOT know about Mesa, ROS, or any simulator
    - Does NOT handle scenarios or agent assignments (that is mesa_sim/model.py)

USED BY:
    - shared/recognizer.py  → needs intention set T and micro-action likelihoods
    - shared/planner.py     → needs task decompositions to build plans
"""

import yaml
from pathlib import Path
from typing import Dict, List


class KnowledgeBase:

    def __init__(self, tasks_data: dict, actions_data: dict, costs_data: dict = None):
        self._tasks = tasks_data
        self._actions = actions_data
        self._costs = costs_data or {}


    @classmethod
    def from_yaml(cls, tasks_path: str, actions_path: str,
                costs_path: str = None) -> "KnowledgeBase":
        with open(tasks_path, "r") as f:
            tasks_data = yaml.safe_load(f)
        with open(actions_path, "r") as f:
            actions_data = yaml.safe_load(f)
        costs_data = {}
        if costs_path:
            with open(costs_path, "r") as f:
                costs_data = yaml.safe_load(f)
        return cls(tasks_data, actions_data, costs_data)


    def get_action_completion_predicate(self, action_name: str) -> str:
        # returns e.g. "at({agent_id}, {zone_id})"
        actions = self._actions.get("actions", {})
        action = actions.get(action_name, {})
        return action.get("completion_predicate", "")

    def get_task_completion_predicate(self, task_name: str) -> str:
        # returns e.g. "item_at({item_id}, kitting_table)"
        for section in ["assigned_tasks", "foreseeable_tasks"]:
            for task in self._tasks.get(section, []):
                if task["name"] == task_name:
                    return task.get("completion_predicate", "")
        return ""

    # -------------------------------------------------------------------------
    # Intention set T
    # -------------------------------------------------------------------------

    def get_all_intentions(self) -> List[str]:
        """All known task names (assigned + foreseeable)."""
        assigned = [t["name"] for t in self._tasks.get("assigned_tasks", [])]
        foreseeable = [t["name"] for t in self._tasks.get("foreseeable_tasks", [])]
        return assigned + foreseeable

    def get_assigned_intentions(self) -> List[str]:
        return [t["name"] for t in self._tasks.get("assigned_tasks", [])]

    def get_foreseeable_intentions(self) -> List[str]:
        return [t["name"] for t in self._tasks.get("foreseeable_tasks", [])]

    # -------------------------------------------------------------------------
    # Task decomposition τ → actions
    # -------------------------------------------------------------------------

    def get_task_actions(self, task_name: str) -> List[str]:
        """
        Return the action sequence for a given task type.
        Actions are returned as raw strings with placeholders,
        e.g. ["GOTO_ZONE({item_zone})", "PICK_UP({item_id})", ...]
        Placeholder resolution is the planner's responsibility.
        """
        for section in ["assigned_tasks", "foreseeable_tasks"]:
            for task in self._tasks.get(section, []):
                if task["name"] == task_name:
                    return task["actions"]
        return []

    def get_task_parameters(self, task_name: str) -> List[str]:
        """Return declared parameters for a task type, e.g. ["item_id"]."""
        for section in ["assigned_tasks", "foreseeable_tasks"]:
            for task in self._tasks.get(section, []):
                if task["name"] == task_name:
                    return task.get("parameters", [])
        return []

    # -------------------------------------------------------------------------
    # Action decomposition a → μ
    # -------------------------------------------------------------------------

    def get_action_decomposition(self, action_name: str):
        """
        Return decomposition of an action type.
        Returns either:
          - "STEP*" or "STAND*"  (dynamic expansion at runtime)
          - ["GRASP"]            (fixed single microaction)
          - ["MOVE_TO({zone})"]  (delegates to another action)
        """
        actions = self._actions.get("actions", {})
        action = actions.get(action_name, {})
        return action.get("decomposes_to", [])

    def get_action_parameters(self, action_name: str) -> List[str]:
        actions = self._actions.get("actions", {})
        action = actions.get(action_name, {})
        return action.get("parameters", [])

    # -------------------------------------------------------------------------
    # Micro-action set M
    # -------------------------------------------------------------------------

    def get_microactions(self) -> List[str]:
        """Terminal micro-actions: ["STEP", "GRASP", "RELEASE", "STAND"]."""
        return self._actions.get("microactions", [])