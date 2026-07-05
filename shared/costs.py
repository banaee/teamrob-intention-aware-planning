# shared/costs.py
"""
Backend-agnostic cost functions for the meta-planner.

All costs are in SECONDS.
Both Mesa and ROS backends provide positions as (x, y) in metres
through their respective layout adapters.

This file has NO imports from mesa_sim, ros_sim, or ROS.
It only imports from shared/types.py and standard Python.
"""

import math
import yaml
from dataclasses import dataclass
from typing import Dict, Tuple, List, Optional, Any


# ── Import from shared only ───────────────────────────────────────────────
from shared.types import BeliefState


# =========================================================================
# Configuration dataclass — loaded from costs.yaml
# =========================================================================

@dataclass
class CostConfig:
    robot_speed:        float   # m/s
    T_pick:             float   # seconds
    T_place:            float   # seconds
    cancel_overhead:    float   # seconds
    priest_correction:  Dict    # zone pair → float
    human_correction:   float   # scalar
    block_radius_m:     float   # metres (continuous)
    block_radius_cells: int     # cells (Mesa)
    ignore_threshold:   float   # min P_block to count
    belief_decay:       float   # per second
    conflict_threshold: float   # Level 1 trigger

    @staticmethod
    def from_yaml(path: str) -> "CostConfig":
        with open(path) as f:
            raw = yaml.safe_load(f)
        return CostConfig(
            robot_speed        = raw["robot"]["speed_ms"],
            T_pick             = raw["actions"]["T_pick"],
            T_place            = raw["actions"]["T_place"],
            cancel_overhead    = raw["actions"]["cancel_overhead"],
            priest_correction  = raw["priest_correction"],
            human_correction   = raw["human_correction"],
            block_radius_m     = raw["blocking"]["continuous_radius_m"],
            block_radius_cells = raw["blocking"]["mesa_radius_cells"],
            ignore_threshold   = raw["interference"]["ignore_threshold"],
            belief_decay       = raw["interference"]["belief_decay_per_second"],
            conflict_threshold = raw["reselect"]["conflict_threshold"],
        )


# =========================================================================
# 1. Travel time
# =========================================================================

def c_travel(
    pos_from:  Tuple[float, float],
    pos_to:    Tuple[float, float],
    zone_from: str,
    zone_to:   str,
    cfg:       CostConfig,
) -> float:
    """
    Estimated travel time in seconds between two positions.

    Formula:
        C_travel = (||pos_to - pos_from||_2 / v_robot) * alpha(z_a, z_b) * beta

    alpha: geometry correction for PRIEST curvature (from costs.yaml)
    beta:  human replanning overhead (global scalar from costs.yaml)
    """
    dist = math.sqrt(
        (pos_to[0] - pos_from[0]) ** 2 +
        (pos_to[1] - pos_from[1]) ** 2
    )

    t_straight = dist / cfg.robot_speed

    # Look up geometry correction for this zone pair
    zones_table = cfg.priest_correction.get("zones", {})
    key = f"{zone_from}_to_{zone_to}"
    alpha = zones_table.get(key, cfg.priest_correction.get("default", 1.2))

    return t_straight * alpha * cfg.human_correction


# =========================================================================
# 2. Arrival time windows
# =========================================================================

def arrival_windows(
    shelf_pos:    Tuple[float, float],
    delivery_pos: Tuple[float, float],
    shelf_zone:   str,
    delivery_zone:str,
    robot_pos:    Tuple[float, float],
    robot_zone:   str,
    t0:           float,
    cfg:          CostConfig,
) -> Dict[str, Tuple[float, float]]:
    """
    Returns {zone_id: (t_start, t_end)} for each goal position
    the robot will occupy during this task.

    The robot occupies:
        shelf_zone    during [eta_s, eta_s + T_pick]
        delivery_zone during [eta_d, eta_d + T_place]
    """
    t_to_shelf = c_travel(robot_pos, shelf_pos,
                          robot_zone, shelf_zone, cfg)
    t_to_delivery = c_travel(shelf_pos, delivery_pos,
                             shelf_zone, delivery_zone, cfg)

    eta_s = t0 + t_to_shelf
    eta_d = eta_s + cfg.T_pick + t_to_delivery

    return {
        "shelf":    (eta_s,  eta_s + cfg.T_pick),
        "delivery": (eta_d,  eta_d + cfg.T_place),
    }


# =========================================================================
# 3. Belief propagation
# =========================================================================

def propagate_belief(
    belief:  BeliefState,
    delta_t: float,
    cfg:     CostConfig,
) -> BeliefState:
    """
    Decay belief toward uniform over a time horizon delta_t.

    Formula:
        b_{t+dt}(h) = b_t(h) * exp(-lambda * dt)
                    + (1 - exp(-lambda * dt)) / |H|

    As delta_t → ∞, belief returns to uniform.
    """
    import math

    n = len(belief.distribution)
    if n == 0:
        return belief

    decay = math.exp(-cfg.belief_decay * delta_t)
    uniform_share = (1.0 - decay) / n

    new_dist = {
        h: prob * decay + uniform_share
        for h, prob in belief.distribution.items()
    }

    # Renormalise (floating point safety)
    total = sum(new_dist.values())
    new_dist = {h: p / total for h, p in new_dist.items()}

    most_likely = max(new_dist, key=new_dist.get)

    return BeliefState(
        timestamp             = belief.timestamp + delta_t,
        agent_id              = belief.agent_id,
        distribution          = new_dist,
        most_likely           = most_likely,
        confidence            = new_dist[most_likely],
        predicted_next_actions= {},
    )


# =========================================================================
# 4. Goal position blockage probability
# =========================================================================

def p_goal_blocked(
    goal_pos:     Tuple[float, float],
    t_start:      float,
    t_end:        float,
    belief:       BeliefState,
    knowledge:    Any,    # DomainKnowledgeBase — provides task decompositions
    layout:       Any,    # layout adapter — provides position_of()
    cfg:          CostConfig,
) -> float:
    """
    Probability that the human will be blocking goal_pos
    during time window [t_start, t_end].

    A hypothesis h contributes to blockage if:
      (a) h predicts the human to be within block_radius_m of goal_pos
      (b) the human's predicted dwell window overlaps [t_start, t_end]

    Currently a simplified version:
      - Checks if h's goal position matches goal_pos within block_radius_m
      - Uses T_pick/T_place as dwell duration depending on goal type
      - Temporal overlap: assumed if belief window and robot window intersect

    Returns probability in [0, 1].
    """
    total = 0.0

    for h, prob in belief.distribution.items():
        if prob < cfg.ignore_threshold:
            continue

        # Get the positions this hypothesis visits
        # For now: use knowledge base to get expected goal positions for h
        # This is a stub that will improve when IR is fully implemented
        h_goal_pos = _get_hypothesis_goal_position(h, knowledge, layout)
        if h_goal_pos is None:
            continue

        # Spatial overlap: is human predicted near robot's goal?
        dist = math.sqrt(
            (h_goal_pos[0] - goal_pos[0]) ** 2 +
            (h_goal_pos[1] - goal_pos[1]) ** 2
        )
        if dist > cfg.block_radius_m:
            continue

        # Temporal overlap: does hypothesis predict human there
        # during robot's window?
        # Simplified: assume human is at their goal for T_pick seconds
        # This will be refined when we have per-hypothesis timing
        h_dwell = cfg.T_pick   # conservative estimate
        h_t_start = 0.0        # placeholder — replace with projected eta
        h_t_end = h_t_start + h_dwell

        overlap = (h_t_start < t_end) and (h_t_end > t_start)
        if not overlap:
            continue

        total += prob * h_dwell

    return min(total, 1.0)   # cap at 1.0


def _get_hypothesis_goal_position(
    hypothesis_name: str,
    knowledge:       Any,
    layout:          Any,
) -> Optional[Tuple[float, float]]:
    """
    Returns the primary goal position for a hypothesis.
    For DELIVER_ITEM(item_X): the shelf position of item_X.
    For foreseeable tasks: their destination position.

    This is a simplified lookup — will be expanded with full
    decomposition tree traversal in Phase 4A.
    """
    try:
        schema = knowledge.get_task_schema(hypothesis_name)
        if schema is None:
            return None

        # Find the first move_to action in the decomposition
        # and return its target position
        for method in schema.methods:
            for step in method.steps:
                if step.action_name == "move_to":
                    # The target binding tells us where the human goes first
                    # This is a heuristic — full version uses progress pointer
                    target = step.bindings.get("?target")
                    if target:
                        return layout.position_of(target)
    except Exception:
        pass

    return None


# =========================================================================
# 5. Interference cost
# =========================================================================

def c_interference(
    shelf_pos:     Tuple[float, float],
    delivery_pos:  Tuple[float, float],
    shelf_zone:    str,
    delivery_zone: str,
    robot_pos:     Tuple[float, float],
    robot_zone:    str,
    t0:            float,
    belief:        BeliefState,
    knowledge:     Any,
    layout:        Any,
    cfg:           CostConfig,
) -> float:
    """
    Expected waiting cost due to human blocking robot's goal positions.

    Two components:
      (a) Shelf blockage: human at shelf when robot arrives to pick up
      (b) Delivery blockage: human at kitting_table when robot arrives to place
      (c) Bottleneck cost: human in narrow passage on robot's path
          (currently zero for env_layout1 — no narrow passages)
    """
    windows = arrival_windows(
        shelf_pos, delivery_pos,
        shelf_zone, delivery_zone,
        robot_pos, robot_zone,
        t0, cfg
    )

    total = 0.0

    # Shelf blockage
    t1, t2 = windows["shelf"]
    p_shelf = p_goal_blocked(
        shelf_pos, t1, t2, belief, knowledge, layout, cfg
    )
    if p_shelf >= cfg.ignore_threshold:
        total += p_shelf * cfg.T_pick   # expected wait = human's dwell time

    # Delivery blockage
    t1, t2 = windows["delivery"]
    p_delivery = p_goal_blocked(
        delivery_pos, t1, t2, belief, knowledge, layout, cfg
    )
    if p_delivery >= cfg.ignore_threshold:
        total += p_delivery * cfg.T_place

    # Bottleneck (none in current layout — zero cost)
    # Extend here when narrow passages are added to env_layout1.json

    return total


# =========================================================================
# 6. Single task total cost
# =========================================================================

def c_task(
    shelf_pos:     Tuple[float, float],
    delivery_pos:  Tuple[float, float],
    shelf_zone:    str,
    delivery_zone: str,
    robot_pos:     Tuple[float, float],
    robot_zone:    str,
    t0:            float,
    belief:        BeliefState,
    knowledge:     Any,
    layout:        Any,
    cfg:           CostConfig,
) -> Tuple[float, float]:
    """
    Returns (total_cost_seconds, finish_time) for one task.
    finish_time is used to chain tasks in c_ordering.

    Formula:
        C_task = C_travel(robot→shelf) + T_pick
               + C_travel(shelf→delivery) + T_place
               + C_interference
    """
    t_to_shelf = c_travel(robot_pos, shelf_pos,
                          robot_zone, shelf_zone, cfg)
    t_to_delivery = c_travel(shelf_pos, delivery_pos,
                             shelf_zone, delivery_zone, cfg)

    base = t_to_shelf + cfg.T_pick + t_to_delivery + cfg.T_place

    interference = c_interference(
        shelf_pos, delivery_pos,
        shelf_zone, delivery_zone,
        robot_pos, robot_zone,
        t0, belief, knowledge, layout, cfg
    )

    total = base + interference
    finish_time = t0 + total

    return total, finish_time


# =========================================================================
# 7. Cancellation cost
# =========================================================================

def c_cancel(
    robot_pos:         Tuple[float, float],
    robot_zone:        str,
    holding:           bool,
    held_item_shelf_pos:   Optional[Tuple[float, float]],
    held_item_shelf_zone:  Optional[str],
    cfg:               CostConfig,
) -> float:
    """
    Cost of abandoning the current task mid-execution.

    If not holding: just stop — cost is cancel_overhead (small constant).
    If holding: must return item to shelf — cost is travel back + T_place.

    The discontinuity at holding=False→True is the key property.
    """
    if not holding:
        return cfg.cancel_overhead

    if held_item_shelf_pos is None:
        # Should not happen — if holding, we must know the shelf
        return cfg.cancel_overhead

    return (
        c_travel(robot_pos, held_item_shelf_pos,
                 robot_zone, held_item_shelf_zone, cfg)
        + cfg.T_place
    )
