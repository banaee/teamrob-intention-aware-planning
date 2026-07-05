"""
shared/replanning.py

PURPOSE:
    The robot's replanning trigger logic (see robot agent architecture, HCM paper).
    Decides WHETHER the robot should replan given a new belief about human intentions.
    Sits between recognizer.py and planner.py in the cognitive loop.

WHAT THIS MODULE DOES:
    - Compares new BeliefState against previous BeliefState
    - Checks if current plan is still feasible given updated belief and world state
    - Returns a decision dict: should we replan, why, and how strongly

WHAT THIS MODULE DOES NOT DO:
    - Does NOT produce a new plan (that is planner.py)
    - Does NOT update beliefs (that is recognizer.py)
    - Does NOT know about Mesa steps or ROS callbacks
    - Does NOT decide the best task ORDER if we do replan (that is meta_planner.py)
    - Simulators decide WHEN to call this — core decides WHAT counts as a trigger

INPUTS:
    - current_plan    AbstractPlan currently being executed (or None if no plan yet)
    - new_belief      latest BeliefState from recognizer.py
    - world           current WorldState from the simulator
    - prev_belief     previous BeliefState to compare against (or None)
    - executor_state  [NEW] snapshot of robot's current execution state
                       (position, holding flag, current goal) — needed for Trigger 3
    - knowledge       [NEW] DomainKnowledgeBase — needed for Trigger 3 goal-blockage lookup
    - layout          [NEW] layout adapter (continuous or Mesa) — needed for Trigger 3
    - cfg             [NEW] CostConfig from costs.yaml — needed for Trigger 3 threshold

OUTPUTS:
    - dict with keys:
        "replan"  : bool    — whether replanning is recommended
        "reason"  : str     — e.g. "belief_divergence", "precondition_broken",
                              "cost_delta", "no_plan"
        "score"   : float   — trigger strength 0.0..1.0 (0 = no trigger, 1 = strong trigger)

TRIGGER CONDITIONS:
    1. Belief divergence   — most_likely intention changed, or probability shift exceeds
                              threshold.  STILL A PLACEHOLDER — Phase 4 IR work.
    2. Precondition broken — current plan's next action is no longer feasible in world
                              state.  STILL A PLACEHOLDER — Phase 4 planner work.
    3. Cost delta           — [NEW, IMPLEMENTED] is the robot's CURRENT action's goal
                              position about to be blocked by the human, according to
                              the latest belief?  Uses shared/costs.p_goal_blocked().
                              This is the only trigger needed to connect IR to the
                              cost-aware reselect/wait decision in meta_planner.py.
    4. No plan              — robot has no current plan at all.  Always real, unchanged.

ALGORITHM:
    Trigger 4 (no_plan) and the structure for Triggers 1/2 are exactly as before.
    Trigger 3 (cost_delta) is now implemented using shared/costs.py.
    Triggers 1 and 2 remain placeholders — untouched, for Phase 4 IR/planner work.

WHAT TO DO WITH THE RESULT:
    If should_replan() returns replan=True with reason="cost_delta":
        → call meta_planner.reselect_or_continue(...) to decide RESELECT vs WAIT.
    If reason is "no_plan", "belief_divergence", or "precondition_broken":
        → call planner.plan(...) directly as before (full replan, not a reorder).
"""

from typing import Optional, Any

from shared.types import AbstractPlan, BeliefState, WorldState


def should_replan(
    current_plan: AbstractPlan | None,
    new_belief: BeliefState,
    world: WorldState,
    prev_belief: BeliefState | None = None,
    # --- NEW optional parameters, only needed for Trigger 3 ---
    # All default to None so every existing call site keeps working unchanged.
    executor_state: Optional[Any] = None,   # meta_planner.ExecutorState
    knowledge: Optional[Any] = None,        # DomainKnowledgeBase
    layout: Optional[Any] = None,           # layout adapter (continuous or Mesa)
    cfg: Optional[Any] = None,              # CostConfig from costs.yaml
) -> dict:
    """
    Evaluate whether the robot should replan.

    BEHAVIOUR:
        - If no plan exists yet → trigger replan (real, unchanged from before)
        - Trigger 1 (belief divergence)   → still a placeholder, returns False
        - Trigger 2 (precondition broken) → still a placeholder, returns False
        - Trigger 3 (cost delta)          → IMPLEMENTED. Only evaluated if
              executor_state, knowledge, layout, and cfg are all provided.
              If any are missing, this trigger silently contributes nothing
              (same as a placeholder), so calling should_replan() the old way
              (without these args) behaves exactly as it did before.

    TODO in Phase 4 (unchanged from before):
        - Trigger 1: belief divergence (KL-divergence or max-prob shift > threshold)
        - Trigger 2: precondition check (next action still feasible in world?)
    """

    # Real check: if there is no plan at all, we must plan
    if current_plan is None:
        return {
            "replan": True,
            "reason": "no_plan",
            "score": 1.0,
        }

    # --- Placeholder trigger 1: belief divergence ---
    # TODO: compare prev_belief vs new_belief distribution
    # e.g. if most_likely changed or KL-divergence > threshold → replan
    belief_divergence_detected = False  # placeholder — unchanged

    # --- Placeholder trigger 2: precondition broken ---
    # TODO: check if current_plan.actions[0] preconditions hold in world
    precondition_broken = False  # placeholder — unchanged

    # --- Trigger 3: cost delta [NEW] ---
    # Is the human, according to the latest belief, likely to be blocking
    # the exact goal position the robot's CURRENT action is heading toward?
    # This connects IR directly to the cost-aware reselect/wait decision.
    cost_trigger_score = _check_cost_delta(
        executor_state, new_belief, knowledge, layout, cfg
    )

    replan = (
        belief_divergence_detected
        or precondition_broken
        or (cost_trigger_score > 0.0)
    )

    # Priority order when multiple triggers fire: cost_delta is checked first
    # because it is the only one currently implemented with a real signal.
    if cost_trigger_score > 0.0:
        reason = "cost_delta"
        score = cost_trigger_score
    elif precondition_broken:
        reason = "precondition_broken"
        score = 1.0  # hard trigger
    elif belief_divergence_detected:
        reason = "belief_divergence"
        score = 0.8  # placeholder strength
    else:
        reason = "none"
        score = 0.0

    return {
        "replan": replan,
        "reason": reason,
        "score": score,
    }


# =============================================================================
# Trigger 3 helper — NEW
# =============================================================================

def _check_cost_delta(
    executor_state: Optional[Any],
    new_belief: BeliefState,
    knowledge: Optional[Any],
    layout: Optional[Any],
    cfg: Optional[Any],
) -> float:
    """
    Returns a score in [0, 1]: the probability that the human will be
    blocking the robot's CURRENT goal position, given the latest belief.

    Returns 0.0 (no trigger) if:
        - any required input is missing (executor_state, knowledge, layout, cfg)
        - the robot has no current navigation goal (e.g. between tasks)
        - the computed blockage probability is below cfg.conflict_threshold

    This function does NOT decide what to do about the conflict — it only
    reports whether one exists. The decision (RESELECT vs WAIT) is made by
    meta_planner.reselect_or_continue(), called by the simulator only when
    this trigger fires.
    """
    if executor_state is None or knowledge is None or layout is None or cfg is None:
        return 0.0

    goal_pos = getattr(executor_state, "current_goal_pos", None)
    if goal_pos is None:
        return 0.0

    remaining_s = getattr(executor_state, "estimated_remaining_s", 0.0)

    from shared.costs import p_goal_blocked  # local import avoids a hard
                                              # dependency for callers that
                                              # never use Trigger 3

    p_conflict = p_goal_blocked(
        goal_pos,
        t_start=0.0,
        t_end=remaining_s,
        belief=new_belief,
        knowledge=knowledge,
        layout=layout,
        cfg=cfg,
    )

    if p_conflict >= cfg.conflict_threshold:
        return p_conflict

    return 0.0
