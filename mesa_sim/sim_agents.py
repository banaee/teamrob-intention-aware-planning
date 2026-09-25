"""
mesa_sim/sim_agents.py

PURPOSE:
    Mesa agent implementations for HumanAgent and RobotAgent.
    Bridges the Mesa simulation loop with the shared cognitive layer.

AGENTS:
    HumanAgent  — scripted agent. Two script forms until T-H3: the C1 resolved
                  list of primitives, run one by one (T-C2b); and the T-H Script,
                  run by the stack machine (world/human_executor.py, T-H2),
                  this agent being its body-side driver. Exposes no task to the
                  world: the robot has no access to the script, the stack or
                  the record.

    RobotAgent  — cognitive agent. Each step:
                    1. builds Observation of human via obs_builder
                    2. updates belief via shared/recognizer.py
                    3. checks re-evaluation trigger via shared/meta_planner.py
                    4. selects/replans current task if triggered
                    5. executes one microaction via executor.py

IMPORT BOUNDARY:
    mesa_sim/ may import from shared/. shared/ never imports from mesa_sim/.

STEP ORDER (RobotAgent):
    obs_builder → recognizer → meta_planner → planner → executor
    This order is fixed and must not be changed without updating the paper.
"""

from __future__ import annotations
import logging
from typing import TYPE_CHECKING, List, Optional, Dict

from shared.knowledge import TaskModel, ContextKnowledge
from shared.projection import Projector
from shared.recognizer import IntentionRecognizer, HypothesisKey, build_hypothesis_space

from shared.planner import AdaptivePlanner
from shared.meta_planner import MetaPlanner
from shared.types import (AbstractPlan, BeliefState, Decision, ExecutorState, GroundedAction, Script, Start, Stay,
                          TaskInstance, task_instance_key)
from world.record import Record, Snapshot
from domains.script import ground
from world.human_executor import StackMachine, RunAction, ResumeAction

from mesa_sim.mesa_fork import agent
from mesa_sim.obs_builder import build_observation
from mesa_sim.world_state_builder import build_world_state, PROXIMITY_THRESHOLD
from mesa_sim.executor import Executor, Suspended, ACTION_COMPLETION_LATENCY, TASK_COMPLETION_LATENCY
from mesa_sim.action_decomposer import _get_step_size, _get_min_separation, _get_beta, _parse_duration_to_steps  # single reader of mesa_configs.yaml

if TYPE_CHECKING:
    from mesa_sim.sim_model import SimModel


# Mesa ticks between a robot's own "now" and the time the human it observes was
# seen in that state. Exactly one: BaseScheduler runs agents in insertion order
# and the human is spawned first (sim_model._spawn_agents, scenario order), so
# within a tick the human has already moved when the robot builds its
# WorldState, while the robot itself has not moved yet. The human's observed
# position is therefore the position it holds at step 1 of the robot's
# projection, not at step 0 — the same fact RobotAgent.observe_initial() exists
# for. Handed to the Projector so the two projections share a clock (L2).
OBSERVATION_OFFSET = 1.0

# The human executor's record stream (T-H2): one `[rec]` line per tick, its own
# logger so that mesa_sim/run_mesa.py can send it to a file beside the run log.
_REC = logging.getLogger("rec")

# Mesa ticks the HUMAN's body spends completing a task: none. Its executor is
# action-level (HumanAgent, T-C2b): it runs primitives, knows no task, and
# hands the next primitive to the Executor on the tick after the last one's
# acknowledgement, so no tick is spent between the end of one task and the
# start of the next. Handed to the robot's Projector for the human's projection
# beside the robot's own TASK_COMPLETION_LATENCY; the per-action
# acknowledgement (ACTION_COMPLETION_LATENCY) is the same executor's for both.
HUMAN_TASK_COMPLETION_LATENCY = 0.0


# =============================================================================
# Base agent
# =============================================================================

class FactoryAgent(agent.Agent):

    def __init__(self, unique_id: str, model: "SimModel", pos: tuple):
        super().__init__(unique_id, model)
        self.carrying: Optional[str] = None
        self.waited_at: Optional[str] = None   # fixed object a completed wait ended at (executor)
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
    Scripted human worker, action-level (T-C1, built in T-C2b). Holds the
    resolved list of primitives of its script (domains/script.resolve_script(),
    set by SimModel once the initial world exists). A ScriptAction is grounded
    when it is reached — schema, bindings, completion predicate; its target
    position is resolved by the executor at that moment, so an item the robot
    has already taken is not there — and handed to the same Executor as a
    one-action plan. Stay(n) idles n ticks, Stay() idles to the end of the run,
    an empty list stands. No task, no task completion, no per-task completion
    tick: the next primitive starts on the tick after the last one's
    acknowledgement. Robot has no reference to this script.
    """

    def __init__(self, unique_id: str, model: "SimModel", pos: tuple):
        super().__init__(unique_id, model, pos)

        self.script: List = []                   # ScriptAction | Stay, resolved at load
        self.script_index: int = 0
        self.current_plan: Optional[AbstractPlan] = None   # the primitive in hand, as a one-action plan
        self._stay_remaining: Optional[int] = None         # ticks left of the Stay in hand (-1: Stay()); None: no Stay

        # The T-H path (T-H2): the stack machine and its record, set by
        # load_stack(); the action in hand (a one-action plan, as the C1 path
        # hands it); the body's remainder of the one suspended action (the
        # stack is one level deep, so one); the live decisions to apply on the
        # next tick (inject).
        self.machine: Optional[StackMachine] = None
        self.record: Optional[Record] = None
        self._in_hand: Optional[GroundedAction] = None
        self._suspended: Optional[Suspended] = None
        self._injections: List[Decision] = []

        self.executor = Executor(agent=self)

    def load_script(self, primitives: List):
        """The resolved script (SimModel._resolve_human_scripts()), before step 0."""
        self.script = list(primitives)
        self.script_index = 0

    def load_stack(self, script: Script, planner: AdaptivePlanner):
        """The T-H script, checked at load (world/human_executor.check_script),
        before step 0. The planner is on the world's tree."""
        self.record = Record()
        self.machine = StackMachine(script, planner, self.unique_id,
                                    lambda duration: _parse_duration_to_steps(duration, self.model), self.record)

    def inject(self, decision: Decision) -> None:
        """A live event (trigger Now): applied at the start of this agent's
        next step(), before the body runs. Refused when a task is already
        suspended (Start) or the stack is empty (Drop), and recorded."""
        self._injections.append(decision)

    def step(self):
        if self.machine is not None:
            self._step_stack()
            return
        world = build_world_state(self.model)

        # The primitive in hand is done once its action is acknowledged: the
        # executor's cursor is past the plan's one action. Handing the executor
        # no plan clears it, so the next primitive loads from a clean executor
        # and owes nothing (the per-task completion tick is the robot's).
        if self.current_plan is not None and self.executor.action_index >= len(self.current_plan.actions):
            self.current_plan = None
            self.executor.step(plan=None, world=world)
            self.script_index += 1

        while self.current_plan is None and self._stay_remaining is None:
            if self.script_index >= len(self.script):
                self._idle()
                return
            element = self.script[self.script_index]
            logging.info(f"[human] step={int(self.model.schedule.steps)} {self.unique_id} "
                         f"primitive {self.script_index}: {element}")
            if isinstance(element, Stay):
                if element.ticks == 0:
                    self.script_index += 1
                    continue
                self._stay_remaining = element.ticks if element.ticks is not None else -1
            else:
                action = ground(element, self.unique_id, self.model.tree)
                self.current_plan = AbstractPlan(goal_intention=action.action_name, actions=[action])

        if self._stay_remaining is not None:
            # A Stay: this tick stands. Stay() (-1) never ends.
            self._idle()
            if self._stay_remaining > 0:
                self._stay_remaining -= 1
                if self._stay_remaining == 0:
                    self._stay_remaining = None
                    self.script_index += 1
            return

        self.executor.step(plan=self.current_plan, world=world)
        self.current_action = self.executor.current_action
        self.current_microaction = self.executor.current_microaction

    def _idle(self):
        self.current_action = None
        self.current_microaction = None

    # ------------------------------------------------------------------
    # The T-H path: the body-side driver of the stack machine (T-H2)
    # ------------------------------------------------------------------

    def _step_stack(self):
        """
        One tick. In order: the action in hand that the body acknowledged last
        tick is reported done (its AfterAction events fire now); the injected
        decisions are applied; a DuringAction whose tick is reached cuts the
        action in hand; then the machine says what to run and the body runs one
        microaction of it. The record gets this tick's snapshot and its `[rec]`
        line. The per-task completion tick is never spent (one action at a time,
        as the C1 path), so the human projection's 0 stays true.
        """
        world = build_world_state(self.model)
        tick = int(self.model.schedule.steps)
        machine, executor = self.machine, self.executor

        # 1. the action in hand was acknowledged: the executor's cursor is past
        #    its one action
        if self._in_hand is not None and executor.action_index >= 1:
            machine.action_done(world, tick)
            executor.step(plan=None, world=world)
            self._in_hand = None

        # 2. live decisions
        for decision in self._injections:
            if machine.refusal(decision) is not None:
                machine.inject(decision, world, tick, 0)
                continue
            done = 0
            if self._in_hand is not None:
                suspended = executor.suspend()
                self._in_hand = None
                done = suspended.done
                if isinstance(decision, Start):
                    # the remainder of the task now suspended; a Drop's is
                    # discarded, and the one below the dropped task is kept
                    self._suspended = suspended if done > 0 else None
            machine.inject(decision, world, tick, done)
        self._injections = []

        # 3. a during cut on the action in hand: that many of its ticks are
        #    executed and it has ticks left
        if self._in_hand is not None and executor.microaction_queue and machine.cut_due(executor.progress().done):
            self._suspended = executor.suspend()
            self._in_hand = None
            machine.cut(world, tick, self._suspended.done)

        # 4. run: one microaction of the action in hand, handed to the executor
        #    as a one-action plan (a new plan loads from its start on a cleared
        #    executor, which owes nothing; a resumed one is the executor's own)
        plan = executor.current_plan
        if self._in_hand is None:
            nxt = machine.next(world, tick)
            if isinstance(nxt, RunAction):
                self._in_hand = nxt.action
                plan = AbstractPlan(goal_intention=nxt.action.action_name, actions=[nxt.action])
            elif isinstance(nxt, ResumeAction):
                executor.resume(self._suspended)
                self._in_hand = nxt.cut.action
                plan = executor.current_plan
            else:
                self._idle()
        before = executor.progress()
        if self._in_hand is not None:
            executor.step(plan=plan, world=world)
        self.current_action = executor.current_action
        self.current_microaction = executor.current_microaction

        # 5. the record. On the acknowledgement tick the executor's cursor is
        #    past the action and its queue reset: the progress shown is the
        #    one before the step, the full count.
        current = machine.current()
        if current is not None and self._in_hand is not None:
            progress = before if executor.action_index >= 1 else executor.progress()
            snap = Snapshot(tick, machine.stack_tasks(), current[0], current[1], progress.done, progress.total)
        else:
            snap = Snapshot(tick, machine.stack_tasks(), None, 0, 0, 0)
        self.record.snapshot(snap)
        for transition in self.record.transitions_at(tick):
            logging.info(f"[human] step={tick} {self.unique_id} {transition!r}")
        _REC.info(self.record.line(tick))


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
                 task_model: TaskModel,
                 assigned_tasks: List[TaskInstance],
                 # known_item_ids=List[str],
                 known_objects_by_type: Dict[str, List[str]],
                 observed_agent_id: Optional[str] = None,
                 observed_assigned_tasks: Optional[List[TaskInstance]] = None):
        super().__init__(unique_id, model, pos)


        # task_index dropped — current_task_instance replaces it, 
        # populated from UpdateResult.current_task instead of indexing assigned_tasks.
        
        self.observed_agent_id = observed_agent_id
        self.assigned_tasks: List[TaskInstance] = assigned_tasks

        # Build hypothesis space from the robot's task model and the workspace objects
        hypotheses = build_hypothesis_space(task_model=task_model, known_objects_by_type=known_objects_by_type)

        context = ContextKnowledge.default()

        # The body's physical parameters for the mind, each with where it came
        # from, for the run header below (T-A1): beta in the body's length units
        # for the recognizer, min_separation for the MetaPlanner.
        beta, self._beta_source = _get_beta(model)
        min_separation, self._min_separation_source = _get_min_separation(model)

        self.recognizer = IntentionRecognizer(
            task_model=task_model,
            hypotheses=hypotheses,
            context=context,
            beta=beta,
            assigned_tasks=observed_assigned_tasks,
        )
        logging.info(
            f"[IR-prior] switch={'on' if self.model.assignment_prior else 'off'} "
            f"known={[task_instance_key(t) for t in (observed_assigned_tasks or [])]}"
        )

        # Projection time is execution time: one projection step is one Mesa tick.
        # The body supplies every constant that makes that true, and shared/ learns
        # none of them:
        #   assumed_speed              motion per tick (step_size, mesa_configs.yaml)
        #   default_action_cost        a stationary action is one tick (GRASP/RELEASE)
        #   arrival_radius             where a walk stops: the same PROXIMITY_THRESHOLD
        #                              that makes at(agent, object) hold, so projected
        #                              walks end where execution ends (T9)
        #   action_completion_latency  the tick the executor spends learning an action
        #                              finished, per action (L2)
        #   task_completion_latency    the tick the executor spends completing a task,
        #                              per task, the robot's (F1)
        #   observed_task_completion_latency
        #                              the human's per-task tick: 0, its executor is
        #                              action-level (T-C2b)
        #   observation_offset         how far ahead of this robot's now the observed
        #                              human's state was seen (L2)
        #   duration_to_steps          the ISO-8601 duration bound on wait_at, in ticks:
        #                              the decomposer's own parser over seconds_per_step,
        #                              so the projected wait is the executed wait (TODO-32)
        self.projector = Projector(
            task_model=task_model,
            assumed_speed=_get_step_size(model),
            default_action_cost=1.0,
            arrival_radius=PROXIMITY_THRESHOLD,
            action_completion_latency=ACTION_COMPLETION_LATENCY,
            task_completion_latency=TASK_COMPLETION_LATENCY,
            observed_task_completion_latency=HUMAN_TASK_COMPLETION_LATENCY,
            observation_offset=OBSERVATION_OFFSET,
            duration_to_steps=lambda duration: _parse_duration_to_steps(duration, model),
        )
    
        # B3's strategy, B2's gate and B3's cost are run options
        # (configs/experiment.yaml, --strategy / --gate_strategy /
        # --cost_strategy), not scenario facts. min_separation
        # is the body's, in world units (mesa_configs.yaml), like assumed_speed above.
        self.meta_planner = MetaPlanner(
            task_model=task_model,
            projector=self.projector,
            recognizer=self.recognizer,
            min_separation=min_separation,
            human_agent_id=observed_agent_id,
            strategy=self.model.strategy,
            gate_strategy=self.model.gate_strategy,
            cost_strategy=self.model.cost_strategy,
        )
        # The run header (TODO-78): the policy values and evaluation switches this
        # robot's decisions are taken under, once per run, so a log can be read
        # without knowing which code or command produced it. min_separation and
        # beta in the body's units (cm), each with where the body took it from.
        logging.info(
            f"[run] {self.unique_id} strategy={self.meta_planner.strategy} "
            f"gate_strategy={self.meta_planner.gate_strategy} "
            f"cost_strategy={self.meta_planner.cost_strategy} "
            f"separation_stop={'on' if self.model.separation_stop else 'off'} "
            f"assignment_prior={'on' if self.model.assignment_prior else 'off'} "
            f"theta={self.meta_planner.theta:.3f} rho={self.meta_planner.rho} "
            f"min_separation={self.meta_planner.min_separation:.2f} "
            f"min_separation_source={self._min_separation_source} "
            f"beta={beta:g} beta_source={self._beta_source} units=cm"
        )
        self.meta_planner.seed_tasks(assigned_tasks)
        self.current_task_instance: Optional[TaskInstance] = None
        self.finished: bool = False

        self.belief: Optional[BeliefState] = None
        self.prev_belief: Optional[BeliefState] = None

        self.planner = AdaptivePlanner(knowledge=task_model)
        self.current_plan: Optional[AbstractPlan] = None

        # The execution-time separation stop (C, TODO-73) is a run option; when
        # on, the executor checks every STEP against the humans' actual
        # positions at the SAME min_separation realization uses.
        self.executor = Executor(
            agent=self,
            separation_stop=self.meta_planner.min_separation if self.model.separation_stop else None,
        )
    
    
    def step(self):
        """
        Full cognitive loop: observe → recognize → replan? → plan → execute.
        """
        if self.finished:
            return
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

        # Note the "seed initial plan" block is gone as a separate step 
        # — evaluate_triggers()'s no_current_task condition already covers both t=0 and post-advance_task(), 
        # so the old two-block structure (seed-if-None, then separate should_replan check) collapses 
        # into one trigger-driven block. 
        # That's intentional, not an oversight — matches how evaluate_triggers() was designed.
        
        executor_state = ExecutorState(
            agent_id=self.unique_id,
            current_task=self.current_task_instance,
            holding=self.carrying,
        )
        belief_for_meta_planner = self.belief or self._make_dummy_belief()

        trigger = self.meta_planner.evaluate_triggers(
            belief=belief_for_meta_planner,
            world=world,
            executor_state=executor_state,
        )
        logging.info(f"[meta-trig] step={int(self.model.schedule.steps)} trigger={trigger.reason}")

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

        if trigger.fired:
            human_projection = self.meta_planner.update_human_projection(
                belief=belief_for_meta_planner,
                world=world,
            )
            result = self.meta_planner.update(
                belief=belief_for_meta_planner,
                world=world,
                executor_state=executor_state,
                human_projection=human_projection,
            )

            if result.current_task is None:
                self.executor.hold(0, trigger.reason)
                logging.info(f"[meta] step={int(self.model.schedule.steps)} all tasks complete")
                self.finished = True
                self.current_task_instance = None
                self.current_plan = None
                self.current_task = None
                return

            logging.info(
                f"[meta] step={int(self.model.schedule.steps)} trigger={trigger.reason} "
                f"winner={result.current_task.schema.name}"
                f"{ {k.name: v.value for k, v in result.current_task.bindings.items()} } "
                f"queue={[t.schema.name + str({k.name: v.value for k, v in t.bindings.items()}) for t in result.queue]}"
            )
            # A CONTINUE decision: the winner is the task already executing, by
            # task identity (task_instance_key), never object identity. The plan
            # is still re-decomposed from the live world (settled: never resumed),
            # but the executor adopts it without restarting — a continue costs
            # nothing (io_contracts.md §1.9, TODO-43).
            continues = (
                self.current_task_instance is not None
                and task_instance_key(result.current_task) == task_instance_key(self.current_task_instance)
            )
            self.current_task_instance = result.current_task
            self.current_plan = self.planner.plan(
                task=self.current_task_instance,
                agent_id=self.unique_id,
                belief=belief_for_meta_planner,
                world=world,
                current_plan=self.current_plan if continues else None,
            )
            if continues:
                self.executor.continue_plan(self.current_plan, world)
            # The decision's hold (T4): executed from this tick on, before the
            # plan continues; every decision replaces the previous hold (0 when
            # it carries none), so an interrupted hold is re-decided, never kept
            # or extended by the body (TODO-71).
            self.executor.hold(result.hold, trigger.reason)
            # The decision's assessed window, for the [stop] log's inside /
            # outside label: T_h is the human projection's end on this
            # decision's projection clock — the same value realize() reads.
            horizon = None
            if human_projection is not None:
                segments = [seg for entry in human_projection.entries for seg in entry.segments]
                horizon = segments[-1].end_step if segments else None
            self.executor.set_assessed_window(int(self.model.schedule.steps), horizon)
                            
        self._execute(plan=self.current_plan, world=world)        
    
    def observe_initial(self):
        """
        Hand the recognizer the observed human's position BEFORE the clock
        starts. Within a tick the human acts before the robot observes it
        (BaseScheduler, scenario order), so the tick-0 observation already
        shows the human one step from where it started; without this the
        recognizer opened its first stretch there and the first step was never
        scored (I1 audit 2.12). The belief this produces is the prior and is
        not stored — the first reported belief is still tick 0's. Called by
        SimModel once all agents exist.
        """
        human = self._get_observed_human()
        if human is None:
            return
        world = build_world_state(model=self.model)
        obs = build_observation(
            human_agent=human,
            model=self.model,
            timestamp=float(self.model.schedule.steps),
        )
        self.recognizer.update(obs=obs, world=world, prev_belief=None)

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

    def advance_task(self):
        """Called by executor when current task completes."""
        self.current_task_instance = None
        self.current_plan = None