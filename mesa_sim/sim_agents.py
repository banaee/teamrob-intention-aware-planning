"""
mesa_sim/sim_agents.py

PURPOSE:
    Mesa agent implementations for HumanAgent and RobotAgent.
    Bridges the Mesa simulation loop with the shared cognitive layer.

AGENTS:
    HumanAgent  — scripted agent, executes a fixed TaskInstance sequence.
                  Provides ground truth for IR evaluation.
                  Robot has no access to this script.

    RobotAgent  — cognitive agent. Each step:
                    1. builds Observation of human via obs_builder
                    2. updates belief via shared/recognizer.py
                    3. checks replanning trigger via shared/replanning.py
                    4. replans if needed via shared/planner.py
                    5. executes one microaction via executor.py

IMPORT BOUNDARY:
    mesa_sim/ may import from shared/. shared/ never imports from mesa_sim/.

STEP ORDER (RobotAgent):
    obs_builder → recognizer → replanning → planner → executor
    This order is fixed and must not be changed without updating the paper.
"""

from __future__ import annotations
import logging
from typing import TYPE_CHECKING, List, Optional, Dict

from shared.domain_knowledge import DomainKnowledgeBase, ContextKnowledge
from shared.recognizer_domain_aware import IntentionRecognizer, HypothesisKey, build_hypothesis_space
from shared.planner import AdaptivePlanner
from shared.replanning import should_replan
from shared.types import AbstractPlan, BeliefState, TaskInstance

from mesa_sim.mesa_fork import agent
from mesa_sim.obs_builder import build_observation
from mesa_sim.world_state_builder import build_world_state
from mesa_sim.executor import Executor

if TYPE_CHECKING:
    from mesa_sim.sim_model import SimModel


# =============================================================================
# Base agent
# =============================================================================

class FactoryAgent(agent.Agent):

    def __init__(self, unique_id: str, model: "SimModel", pos: tuple):
        super().__init__(unique_id, model)
        self.carrying: Optional[str] = None
        self.current_task: Optional[str] = None
        self.current_action: Optional[str] = None
        self.current_microaction: Optional[str] = None

    def step(self):
        raise NotImplementedError


# =============================================================================
# HumanAgent
# =============================================================================

class HumanAgent(FactoryAgent):
    """
    Scripted human worker. Executes a fixed List[TaskInstance] sequence.
    Robot has no reference to this script.
    """

    def __init__(self, unique_id: str, model: "SimModel",
                 pos: tuple, script: List[TaskInstance]):
        super().__init__(unique_id, model, pos)

        self.script: List[TaskInstance] = script
        self.script_index: int = 0
        self.finished: bool = False

        self.planner = AdaptivePlanner(knowledge=model.knowledge)
        self.current_plan: Optional[AbstractPlan] = None

        self.executor = Executor(agent=self)


    def step(self):
        if self.finished:
            return

        task_instance = self.get_current_task_instance()
        if task_instance is None:
            self.finished = True
            self.current_task = None
            return

        world = build_world_state(self.model)
        

        # Build plan once per task — reuse until advance_script() clears it: 
        # for human agent, the plan is scripted and unaffected by belief updates, so no replanning logic needed.
        if self.current_plan is None:
            self.current_plan = self._task_instance_to_plan(task_instance, world)
            logging.info(f"[planner] self.current_plan for {task_instance.schema.name}: {self.current_plan}")

        self._execute(plan=self.current_plan, world=world)
        

    def _execute(self, plan, world):
        self.executor.step(plan=plan, world=world)
        self.current_task = self.executor.current_task
        self.current_action = self.executor.current_action
        self.current_microaction = self.executor.current_microaction

    def get_current_task_instance(self) -> Optional[TaskInstance]:
        """Return current TaskInstance. Used by obs_builder."""
        if self.script_index < len(self.script):
            return self.script[self.script_index]
        return None

    def advance_script(self):
        """Called by executor when current task completes."""
        self.script_index += 1
        self.current_plan = None  # Clear plan to trigger new plan generation for next task
        if self.script_index >= len(self.script):
            self.finished = True

    def _task_instance_to_plan(
        self, task_instance: TaskInstance, world
    ) -> AbstractPlan:
        """
        Convert a TaskInstance into an AbstractPlan via the planner.
        Bindings are already Dict[Var, Const] — no string manipulation.
        Uses a dummy belief since human script has no IR.
        """
        # Convert Dict[Var, Const] → Dict[str, str] for planner
        task_params = {k.name: v.value for k, v in task_instance.bindings.items()}

        dummy_belief = BeliefState(
            timestamp=float(self.model.schedule.steps),
            agent_id=self.unique_id,
            distribution={},
            most_likely="unknown",
            confidence=0.0,
        )

        return self.planner.plan(
            my_intention=task_instance.schema.name,
            task_params=task_params,
            agent_id=self.unique_id,
            belief=dummy_belief,
            world=world,
        )


# =============================================================================
# RobotAgent
# =============================================================================

class RobotAgent(FactoryAgent):
    """
    Intention-aware robot agent. Owns the full cognitive loop.
    """

    def __init__(self, 
                 unique_id: str, 
                 model: "SimModel",
                 pos: tuple,
                 knowledge: DomainKnowledgeBase,
                 scheduled_tasks: List[TaskInstance],
                 known_item_ids=List[str],
                 observed_agent_id: Optional[str] = None):
        super().__init__(unique_id, model, pos)

        self.observed_agent_id = observed_agent_id
        self.scheduled_tasks: List[TaskInstance] = scheduled_tasks
        self.task_index: int = 0

        # Build hypothesis space from observed human's scheduled_tasks
        hypotheses = build_hypothesis_space(knowledge=knowledge, known_item_ids=known_item_ids)

        context = ContextKnowledge.default()

        self.recognizer = IntentionRecognizer(
            knowledge=knowledge,
            hypotheses=hypotheses,
            context=context
        )
        
        self.belief: Optional[BeliefState] = None
        self.prev_belief: Optional[BeliefState] = None

        self.planner = AdaptivePlanner(knowledge=knowledge)
        self.current_plan: Optional[AbstractPlan] = None

        self.executor = Executor(agent=self)
    
    
    def step(self):
        """
        Full cognitive loop: observe → recognize → replan? → plan → execute.
        """
        human = self._get_observed_human()

        world = build_world_state(model=self.model)

        if human is not None:
            obs = build_observation(
                human_agent=human,
                model=self.model,
                timestamp=float(self.model.schedule.steps)
            )
            if obs is not None:
                self.prev_belief = self.belief
                self.belief = self.recognizer.update(
                    obs=obs,
                    world=world,
                    prev_belief=self.prev_belief
                )


        # Seed initial plan (also triggers after advance_task() clears current_plan)
        if self.current_plan is None:
            task_instance = self._get_current_task_instance()
            if task_instance is not None:
                task_params = {k.name: v.value for k, v in task_instance.bindings.items()}
                self.current_plan = self.planner.plan(
                    my_intention=task_instance.schema.name,
                    task_params=task_params,
                    agent_id=self.unique_id,
                    belief=self.belief or self._make_dummy_belief(),
                    world=world,
                )

        if self.belief is not None and human is not None:
            logging.info(f"[IR] step={int(obs.timestamp)} most_likely={self.belief.most_likely} confidence={self.belief.confidence:.3f}")
     
            dist_str = "  ".join(
            f"{k}={v:.3f}"
            for k, v in sorted(self.belief.distribution.items(), key=lambda x: -x[1])
            )
            logging.info(
                f"[IR-dist] step={int(obs.timestamp)} "
                f"most_likely={self.belief.most_likely} "
                f"confidence={self.belief.confidence:.3f} "
                f"dist=[{dist_str}]"
            )
            
            trigger = should_replan(
                current_plan=self.current_plan,
                new_belief=self.belief,
                world=world,
                prev_belief=self.prev_belief
            )
            if trigger["replan"]:
                task_instance = self._get_current_task_instance()
                if task_instance is not None:
                    task_params = {k.name: v.value for k, v in task_instance.bindings.items()}
                    self.current_plan = self.planner.plan(
                        my_intention=task_instance.schema.name,
                        task_params=task_params,
                        agent_id=self.unique_id,
                        belief=self.belief,
                        world=world,
                        current_plan=self.current_plan
                    )

        self._execute(plan=self.current_plan, world=world)    
        
    
    # =========================================================================
    # Internal helpers
    # =========================================================================

    def _make_dummy_belief(self) -> BeliefState:
        return BeliefState(
            timestamp=float(self.model.schedule.steps),
            agent_id=self.unique_id,
            distribution={},
            most_likely="unknown",
            confidence=0.0,
        )


    def _execute(self, plan, world):
        self.executor.step(plan=plan, world=world)
        self.current_task = self.executor.current_task
        self.current_action = self.executor.current_action
        self.current_microaction = self.executor.current_microaction

    def _get_observed_human(self) -> Optional[HumanAgent]:
        if self.observed_agent_id is None:
            return None
        return self.model.humans.get(self.observed_agent_id)

    def _get_current_task_instance(self) -> Optional[TaskInstance]:
        """Return current TaskInstance, or None if all tasks done."""
        logging.info(f"[robot] _get_current_task_instance: task_index={self.task_index} len={len(self.scheduled_tasks)}")

        if self.task_index < len(self.scheduled_tasks):
            return self.scheduled_tasks[self.task_index]
        return None

    def advance_task(self):
        """Called by executor when current task completes."""
        self.task_index += 1
        self.current_plan = None