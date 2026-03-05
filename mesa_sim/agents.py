"""
mesa_sim/agents.py

PURPOSE:
    Mesa agent implementations for HumanAgent and RobotAgent.
    Bridges the Mesa simulation loop with the shared cognitive layer.

AGENTS:

    HumanAgent  — scripted agent, executes a fixed task sequence loaded from
                  scenarios.yaml. Provides ground truth for IR evaluation.
                  The robot has no access to this script.

    RobotAgent  — cognitive agent. Each step it:
                    1. builds an Observation of the human via obs_builder
                    2. updates belief via shared/recognizer.py
                    3. checks replanning trigger via shared/replanning.py
                    4. replans if needed via shared/planner.py
                    5. executes one microaction via executor.py

WHAT THIS MODULE DOES NOT DO:
    - No IR logic lives here — that is shared/recognizer.py
    - No planning logic lives here — that is shared/planner.py
    - No microaction expansion lives here — that is mesa_sim/microactions.py
    - No WorldState construction lives here — that is mesa_sim/world_state_builder.py
    - No Observation construction lives here — that is mesa_sim/obs_builder.py

IMPORT BOUNDARY:
    mesa_sim/ may import from shared/. shared/ never imports from mesa_sim/.

STEP ORDER (RobotAgent):
    obs_builder → recognizer → replanning → planner → executor
    This order is fixed and must not be changed without updating the paper formalization.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, List, Optional, Dict, Any

import mesa

from shared.knowledge import KnowledgeBase
from shared.recognizer import IntentionRecognizer
from shared.planner import AdaptivePlanner
from shared.replanning import should_replan
from shared.types import AbstractPlan, BeliefState

# Translation layer imports — defined in sibling files
# Imported here as stubs; will resolve once those files exist
# from mesa_sim.obs_builder import build_observation
# from mesa_sim.world_state_builder import build_world_state
# from mesa_sim.executor import Executor

if TYPE_CHECKING:
    from mesa_sim.model import FactoryModel


# =============================================================================
# Base agent — shared physical attributes
# =============================================================================

class FactoryAgent(mesa.Agent):
    """
    Base class for all mobile agents in the factory.
    Holds physical state only — no cognitive logic here.
    """

    def __init__(self, unique_id: str, model: FactoryAgent, pos: tuple):
        super().__init__(unique_id, model)
        self.pos: tuple = pos               # (x, y) in center-origin coordinates
        self.carrying: Optional[str] = None # item_id if holding an item, else None
        self.current_task: Optional[str] = None    # task name string
        self.current_action: Optional[str] = None  # action name string
        self.current_microaction: Optional[str] = None  # microaction name string

    def step(self):
        raise NotImplementedError("Subclasses must implement step()")


# =============================================================================
# HumanAgent — scripted, no cognitive layer
# =============================================================================

class HumanAgent(FactoryAgent):
    """
    Scripted human worker. Executes a fixed task sequence from scenarios.yaml.

    The script is a list of dicts built by model._build_human_script():
        [
            {"task": "DELIVER_ITEM", "parameters": {"item_id": "item_1"}, "origin": "assigned"},
            {"task": "COFFEE_BREAK", "parameters": {},                     "origin": "foreseeable"},
            ...
        ]

    The robot has no reference to this script — privacy enforced by not
    exposing it through any model attribute the robot can access.

    Execution is delegated to mesa_sim/executor.py (stubbed until that file exists).
    """

    def __init__(self, unique_id: str, model: FactoryModel,
                 pos: tuple, script: List[Dict[str, Any]]):
        super().__init__(unique_id, model, pos)

        self.script: List[Dict[str, Any]] = script  # private task sequence
        self.script_index: int = 0                  # current position in script
        self.finished: bool = False

        # Executor handles microaction-level execution each step
        # TODO: uncomment when executor.py exists
        # self.executor = Executor(agent=self)

    def step(self):
        """
        Advance human by one microaction.
        Executor pulls the current task from script and executes one microaction.
        When a task completes, script_index advances to the next entry.
        """
        if self.finished:
            return

        # TODO: replace with executor call when executor.py exists
        # self.executor.step()
        # self.current_task = self.executor.current_task
        # self.current_action = self.executor.current_action
        # self.current_microaction = self.executor.current_microaction

        # Skeleton stub: just report current script entry
        if self.script_index < len(self.script):
            entry = self.script[self.script_index]
            self.current_task = entry["task"]
        else:
            self.finished = True
            self.current_task = None

    def get_current_script_entry(self) -> Optional[Dict[str, Any]]:
        """Return the current task entry from script. Used by obs_builder."""
        if self.script_index < len(self.script):
            return self.script[self.script_index]
        return None

    def advance_script(self):
        """Called by executor when current task is completed."""
        self.script_index += 1
        if self.script_index >= len(self.script):
            self.finished = True


# =============================================================================
# RobotAgent — cognitive agent, calls shared core each step
# =============================================================================

class RobotAgent(FactoryAgent):
    """
    Intention-aware robot agent. Owns the full cognitive loop.

    Each step:
        1. Build Observation of the human (obs_builder)
        2. Update belief over human intentions (recognizer)
        3. Check if replanning is needed (replanning)
        4. Replan if triggered (planner)
        5. Execute one microaction (executor)

    Cognitive components (from shared/) are instantiated here and owned
    by the robot for its lifetime. They are never shared with the model
    or other agents.

    observed_agent_id: the human agent this robot observes. In the current
    single-human single-robot setup this is always human_0, but the field
    is kept explicit to support multi-agent extensions.
    """

    def __init__(self, unique_id: str, model: FactoryModel,
                 pos: tuple,
                 knowledge: KnowledgeBase,
                 assigned_tasks: List[Dict[str, Any]],
                 observed_agent_id: Optional[str] = None):
        super().__init__(unique_id, model, pos)

        self.observed_agent_id: Optional[str] = observed_agent_id
        self.assigned_tasks: List[Dict[str, Any]] = assigned_tasks
        self.task_index: int = 0

        # ------------------------------------------------------------------
        # Cognitive components — all from shared/, no Mesa dependencies
        # ------------------------------------------------------------------
        self.recognizer = IntentionRecognizer(knowledge=knowledge)
        self.planner = AdaptivePlanner(knowledge=knowledge)

        # Belief state — updated each step by recognizer
        self.belief: Optional[BeliefState] = None
        self.prev_belief: Optional[BeliefState] = None

        # Current plan — updated when replanning triggers
        self.current_plan: Optional[AbstractPlan] = None

        # Executor handles microaction-level execution each step
        # TODO: uncomment when executor.py exists
        # self.executor = Executor(agent=self)

    def step(self):
        """
        Full cognitive loop: observe → recognize → replan? → plan → execute.
        Order is fixed per paper formalization.
        """

        # ------------------------------------------------------------------
        # 1. Get the observed human agent
        # ------------------------------------------------------------------
        human = self._get_observed_human()
        if human is None:
            # No human to observe — execute current plan if any, then return
            self._execute()
            return

        # ------------------------------------------------------------------
        # 2. Build Observation from human's current Mesa state
        # ------------------------------------------------------------------
        # TODO: uncomment when obs_builder.py exists
        # obs = build_observation(
        #     human_agent=human,
        #     model=self.model,
        #     timestamp=float(self.model.schedule.steps)
        # )

        # Skeleton stub
        obs = None  # placeholder — obs_builder not yet available

        # ------------------------------------------------------------------
        # 3. Update belief over human intentions
        # ------------------------------------------------------------------
        if obs is not None:
            self.prev_belief = self.belief
            self.belief = self.recognizer.update(
                obs=obs,
                prev_belief=self.prev_belief
            )

        # ------------------------------------------------------------------
        # 4. Build WorldState snapshot
        # ------------------------------------------------------------------
        # TODO: uncomment when world_state_builder.py exists
        # world = build_world_state(model=self.model)

        world = None  # placeholder — world_state_builder not yet available

        # ------------------------------------------------------------------
        # 5. Check replanning trigger
        # ------------------------------------------------------------------
        if self.belief is not None and world is not None:
            trigger = should_replan(
                current_plan=self.current_plan,
                new_belief=self.belief,
                world=world,
                prev_belief=self.prev_belief
            )

            # ------------------------------------------------------------------
            # 6. Replan if triggered
            # ------------------------------------------------------------------
            if trigger["replan"]:
                my_intention = self._get_current_intention()
                if my_intention is not None:
                    self.current_plan = self.planner.plan(
                        my_intention=my_intention,
                        belief=self.belief,
                        world=world,
                        current_plan=self.current_plan
                    )

        # ------------------------------------------------------------------
        # 7. Execute one microaction from current plan
        # ------------------------------------------------------------------
        self._execute()

    # =========================================================================
    # Internal helpers
    # =========================================================================

    def _get_observed_human(self) -> Optional[HumanAgent]:
        """Return the HumanAgent this robot is observing, or None."""
        if self.observed_agent_id is None:
            return None
        return self.model.humans.get(self.observed_agent_id)

    def _get_current_intention(self) -> Optional[str]:
        """Return the robot's current assigned task name, or None if done."""
        if self.task_index < len(self.assigned_tasks):
            return self.assigned_tasks[self.task_index]["task"]
        return None

    def _execute(self):
        """
        Execute one microaction from current_plan via executor.
        Stubbed until executor.py exists.
        """
        # TODO: uncomment when executor.py exists
        # self.executor.step()
        # self.current_task = self.executor.current_task
        # self.current_action = self.executor.current_action
        # self.current_microaction = self.executor.current_microaction
        pass

    def advance_task(self):
        """Called by executor when current assigned task completes."""
        self.task_index += 1
        self.current_plan = None  # force replan on next step
