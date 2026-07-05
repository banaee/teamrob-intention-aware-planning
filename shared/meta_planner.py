"""
shared/meta_planner.py

PURPOSE:
    The robot's task ORDERING module.
    Decides, given a set of remaining tasks, the cost-minimising order to
    execute them in — and, when replanning.py has already decided that a
    cost-based interrupt is worth considering, whether to actually abandon
    the current task (RESELECT) or stay the course (WAIT).

WHAT THIS MODULE DOES:
    - cost_of_ordering(): total cost of executing a list of tasks in a given order
    - best_ordering():    search for the lowest-cost ordering of a task set
    - reselect_or_continue(): compare cancelling-and-reordering vs waiting,
      for the SINGLE task currently in progress

WHAT THIS MODULE DOES NOT DO:
    - Does NOT decide WHETHER to even consider replanning — that decision
      (the trigger) belongs entirely to shared/replanning.should_replan().
      This module is only ever consulted AFTER that trigger has fired.
    - Does NOT update beliefs (that is recognizer.py)
    - Does NOT ground actions into an AbstractPlan (that is planner.py)
    - Does NOT know about Mesa, ROS, or any simulator internals — it only
      calls shared/costs.py and reads from a layout adapter interface

RELATIONSHIP TO OTHER shared/ MODULES:

    recognizer.py      → BeliefState
                              │
                              ▼
    replanning.py       "should we even reconsider right now, and why?"
       (TRIGGER ONLY)
                              │
                    replan == True, reason == "cost_delta"
                              ▼
    meta_planner.py     "given that we ARE reconsidering, what's the best
       (THIS FILE)        ordering, and is reselecting worth the
                          cancellation cost?"
                              │
                    "RESELECT"        "WAIT"
                         │                │
                         ▼                ▼
    planner.py      ground chosen   stop PRIEST goal,
                     next task        hold position
                     into AbstractPlan
                     (unchanged)

    For "no_plan", "belief_divergence", or "precondition_broken" triggers
    from replanning.py, the simulator calls planner.plan() directly — this
    module is only relevant for the "cost_delta" trigger.

INPUTS:
    - TaskInstance objects from shared/types.py (same objects Mesa already uses)
    - BeliefState from recognizer.py
    - A layout adapter (continuous_sim or mesa_sim) providing position_of()/zone_of()
    - CostConfig from shared/costs.py (loaded from costs.yaml)
    - ExecutorState — a snapshot of the robot's current execution state

OUTPUTS:
    - best_ordering()         → (List[TaskInstance], total_cost: float)
    - reselect_or_continue()  → dict with "decision" in {"RESELECT", "WAIT"}
"""

from __future__ import annotations

from itertools import permutations
from dataclasses import dataclass
from typing import List, Tuple, Optional, Any, Dict

from shared.costs import (
    CostConfig, c_travel, c_task, c_cancel,
    propagate_belief,
)
from shared.types import BeliefState, TaskInstance, Var


SMALL_N = 6   # full enumeration of orderings below this, greedy above


# =============================================================================
# ExecutorState — snapshot of what the executor is doing right now
# =============================================================================

@dataclass
class ExecutorState:
    """
    Minimal snapshot of the executor's state, built fresh by the simulator
    (run_continuous.py or mesa_sim/run_mesa.py) at each cognitive tick.

    This is the SAME object passed to replanning.should_replan() (for
    Trigger 3) and to meta_planner.reselect_or_continue() (for the
    RESELECT/WAIT decision) — built once per tick, used by both.
    """
    robot_pos:               Tuple[float, float]
    robot_zone:              str
    holding:                 bool
    # Position the robot is currently navigating toward (None if between tasks)
    current_goal_pos:        Optional[Tuple[float, float]]
    current_goal_zone:       Optional[str]
    # Estimated seconds until the current action completes
    estimated_remaining_s:   float
    # Shelf of the currently held item (needed for c_cancel when holding=True)
    held_shelf_pos:          Optional[Tuple[float, float]]
    held_shelf_zone:         Optional[str]


# =============================================================================
# Task geometry helper
# =============================================================================

def _task_geometry(task: TaskInstance, layout: Any) -> Tuple:
    """
    Extract shelf and delivery positions + zones for a task.

    TaskInstance.bindings is Dict[Var, Const] — e.g.
        {Var("?item"): Const("item_5")}
    Delivery target is not always bound explicitly (kitting tasks always
    deliver to "kitting_table"); fall back to that domain constant when
    ?target is absent, matching domains/kitting/tasks.py.
    """
    item_const = task.bindings.get(Var("?item"))
    if item_const is None:
        raise ValueError(
            f"TaskInstance for schema '{task.schema.name}' has no '?item' "
            f"binding. bindings={task.bindings}"
        )
    item_id = item_const.value

    target_const = task.bindings.get(Var("?target"))
    target_id = target_const.value if target_const is not None else "kitting_table"

    shelf_pos     = layout.position_of(item_id)
    delivery_pos  = layout.position_of(target_id)
    shelf_zone    = layout.zone_of(item_id)
    delivery_zone = layout.zone_of(target_id)
    return shelf_pos, delivery_pos, shelf_zone, delivery_zone


# =============================================================================
# Ordering cost
# =============================================================================

def cost_of_ordering(
    ordering:   List[TaskInstance],
    robot_pos:  Tuple[float, float],
    robot_zone: str,
    belief:     BeliefState,
    knowledge:  Any,
    layout:     Any,
    cfg:        CostConfig,
) -> float:
    """
    Total cost (seconds) of executing tasks in the given order.
    Chains position, time, and belief forward across tasks —
    see Definition 8 in the cost formulation document.
    """
    total        = 0.0
    current_pos  = robot_pos
    current_zone = robot_zone
    current_time = 0.0
    current_b    = belief

    for task in ordering:
        shelf_pos, delivery_pos, shelf_zone, delivery_zone = \
            _task_geometry(task, layout)

        cost, finish_time = c_task(
            shelf_pos, delivery_pos,
            shelf_zone, delivery_zone,
            current_pos, current_zone,
            current_time,
            current_b, knowledge, layout, cfg,
        )

        total       += cost
        current_pos  = delivery_pos
        current_zone = delivery_zone
        dt           = finish_time - current_time
        current_time = finish_time
        current_b    = propagate_belief(current_b, dt, cfg)

    return total


# =============================================================================
# Best ordering search
# =============================================================================

def best_ordering(
    tasks:      List[TaskInstance],
    robot_pos:  Tuple[float, float],
    robot_zone: str,
    belief:     BeliefState,
    knowledge:  Any,
    layout:     Any,
    cfg:        CostConfig,
) -> Tuple[List[TaskInstance], float]:
    """
    Returns (best_ordering, best_cost) — see Definition 8 / sigma*.

    N <= SMALL_N : enumerate all N! permutations (exact optimum).
    N >  SMALL_N : greedy nearest-cost insertion (O(N^2) approximation).
    """
    if not tasks:
        return [], 0.0

    if len(tasks) <= SMALL_N:
        best_order: Optional[List[TaskInstance]] = None
        best_cost = float("inf")

        for sigma in permutations(tasks):
            cost = cost_of_ordering(
                list(sigma), robot_pos, robot_zone,
                belief, knowledge, layout, cfg,
            )
            if cost < best_cost:
                best_cost = cost
                best_order = list(sigma)

        return best_order, best_cost

    # Greedy fallback for larger task sets
    remaining    = list(tasks)
    result: List[TaskInstance] = []
    current_pos  = robot_pos
    current_zone = robot_zone
    current_b    = belief
    current_time = 0.0
    total_cost   = 0.0

    while remaining:
        best_task = None
        best_step_cost = float("inf")

        for task in remaining:
            shelf_pos, delivery_pos, shelf_zone, delivery_zone = \
                _task_geometry(task, layout)
            cost, _ = c_task(
                shelf_pos, delivery_pos, shelf_zone, delivery_zone,
                current_pos, current_zone, current_time,
                current_b, knowledge, layout, cfg,
            )
            if cost < best_step_cost:
                best_step_cost = cost
                best_task = task

        result.append(best_task)
        remaining.remove(best_task)

        shelf_pos, delivery_pos, shelf_zone, delivery_zone = \
            _task_geometry(best_task, layout)
        _, finish_time = c_task(
            shelf_pos, delivery_pos, shelf_zone, delivery_zone,
            current_pos, current_zone, current_time,
            current_b, knowledge, layout, cfg,
        )

        total_cost  += best_step_cost
        current_pos  = delivery_pos
        current_zone = delivery_zone
        dt           = finish_time - current_time
        current_time = finish_time
        current_b    = propagate_belief(current_b, dt, cfg)

    return result, total_cost


# =============================================================================
# RESELECT vs WAIT decision
# =============================================================================

def reselect_or_continue(
    executor:         ExecutorState,
    remaining_tasks:  List[TaskInstance],   # current task MUST be remaining_tasks[0]
    belief:           BeliefState,
    knowledge:        Any,
    layout:           Any,
    cfg:              CostConfig,
) -> Dict:
    """
    Called ONLY after replanning.should_replan() has already returned
    replan=True with reason="cost_delta" — i.e. Trigger 3 has fired and
    the robot's current goal position is predicted to be blocked.

    Compares two options:
        WAIT      — stay on the current task, absorb the expected wait,
                    then continue with the best ordering of the rest
        RESELECT  — cancel the current task now, pay the cancellation
                    cost, and re-order ALL remaining tasks (including
                    the abandoned one, to be done later)

    Returns:
        {"decision": "WAIT",     "wait_s": float}
        {"decision": "RESELECT", "new_ordering": List[TaskInstance]}

    NOTE: if the robot is already holding an item, RESELECT is never
    offered — the discontinuity in c_cancel makes it always at least
    as expensive as waiting in practice, and physically the robot
    cannot "drop" a task mid-placement. WAIT is the only option.
    """
    if not remaining_tasks:
        return {"decision": "WAIT", "wait_s": 0.0}

    current_task = remaining_tasks[0]
    future_tasks = remaining_tasks[1:]

    # Expected wait if we just hold position until the goal clears.
    # Uses the same dwell-time logic as the interference cost (T_pick
    # for a shelf goal, T_place for the delivery goal) — approximated
    # here via T_pick as the conservative default.
    expected_wait_s = cfg.T_pick

    if executor.holding:
        # Cannot abandon mid-carry — WAIT is the only physically valid option.
        return {"decision": "WAIT", "wait_s": expected_wait_s}

    # --- Cost of WAIT: absorb the wait, then finish current task,
    #     then best ordering of everything after it ---
    shelf_pos, delivery_pos, shelf_zone, delivery_zone = \
        _task_geometry(current_task, layout)

    _, finish_time_after_current = c_task(
        shelf_pos, delivery_pos, shelf_zone, delivery_zone,
        executor.robot_pos, executor.robot_zone,
        0.0, belief, knowledge, layout, cfg,
    )

    belief_after_current = propagate_belief(
        belief, finish_time_after_current, cfg
    )

    _, future_cost = best_ordering(
        future_tasks, delivery_pos, delivery_zone,
        belief_after_current, knowledge, layout, cfg,
    )

    cost_wait = expected_wait_s + finish_time_after_current + future_cost

    # --- Cost of RESELECT: pay cancellation, then best ordering of
    #     ALL remaining tasks (current one goes back into the pool) ---
    cancel_cost = c_cancel(
        executor.robot_pos, executor.robot_zone,
        executor.holding,
        executor.held_shelf_pos, executor.held_shelf_zone,
        cfg,
    )

    all_order, all_cost = best_ordering(
        remaining_tasks, executor.robot_pos, executor.robot_zone,
        belief, knowledge, layout, cfg,
    )

    cost_reselect = cancel_cost + all_cost

    if cost_reselect < cost_wait:
        return {"decision": "RESELECT", "new_ordering": all_order}

    return {"decision": "WAIT", "wait_s": expected_wait_s}
