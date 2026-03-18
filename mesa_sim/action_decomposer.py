"""
mesa_sim/action_exec_decomposer (before called microactions.py)

PURPOSE:
    Expands AbstractActions from the planner into concrete Mesa-executable
    microaction sequences. This is the top-down symbolic→physical translation
    layer for the Mesa embodiment.

WHAT THIS MODULE DOES:
    - Takes one AbstractAction at a time
    - Resolves parameter placeholders using WorldState and model ground truth
    - Expands "STEP*" actions into a list of N STEP microactions with (x,y) targets
    - Expands "STAND*" actions into a list of N STAND microactions
    - Returns single-microaction lists for GRASP and RELEASE

WHAT THIS MODULE DOES NOT DO:
    - Does NOT execute microactions — that is mesa_sim/executor.py
    - Does NOT do path planning — uses straight-line steps for skeleton phase
    - Does NOT know about IR or planning logic
    - Does NOT handle ROS

ROS EQUIVALENT:
    In ROS, this module has NO direct equivalent because ROS works in reverse:
    - ros_sim/microaction_classifier_ros.py goes BOTTOM-UP:
      raw sensor streams → discrete microaction labels → Observation → recognizer
    - ros_sim/goal_executor_ros.py handles AbstractAction execution by sending
      goals directly to ROS action servers (move_base, MoveIt, etc.)
    - ROS handles its own motion planning internally — no STEP expansion needed
    The shared boundary is: AbstractAction in, Observation out. Everything
    between is simulator-specific and handled differently in each embodiment.

MICROACTION DATACLASS:
    Each microaction is a simple object with:
        name   : str    — "step", "grasp", "release", "stand"
        params : dict   — e.g. {"target_pos": (x, y)} for STEP

STEP EXPANSION (skeleton):
    Currently uses straight-line interpolation toward target position.
    Step size is read from mesa_configs.yaml.
    TODO Phase 4: replace with proper path planning (A*, RRT, etc.)
    that respects obstacles from domain1.json.

CALLED BY:
    - mesa_sim/executor.py — when starting a new AbstractAction,
      calls expand(action, model) to get the microaction queue
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple
import math
import yaml
from pathlib import Path

from shared.types import AbstractAction


# =============================================================================
# Microaction dataclass
# =============================================================================

@dataclass
class Microaction:
    """
    A single atomic Mesa-executable step.
    Produced by expand(), consumed one per step by executor.py.
    """
    name: str                              # "step", "grasp", "release", "stand"
    params: Dict[str, Any] = field(default_factory=dict)

    def __str__(self):
        return f"{self.name}({self.params})"


# =============================================================================
# Main expansion function
# =============================================================================

def expand(action: AbstractAction, model) -> List[Microaction]:
    """
    Expand one AbstractAction into a list of concrete Microactions.

    INPUT:
        action  — AbstractAction from current AbstractPlan
        model   — for position/zone lookups (read-only)

    OUTPUT:
        List[Microaction] — ordered sequence to execute, one per Mesa step

    SKELETON BEHAVIOUR:
        - GOTO_ZONE / MOVE_TO → straight-line STEP sequence to target position
        - PICK_UP             → single GRASP
        - PLACE               → single RELEASE
        - WAIT_AT             → N STAND microactions from duration
        - unknown             → empty list with TODO warning
    """

    action_name = action.action_name.upper() if action.action_name else ""
    params = action.parameters

    if action_name in ("GOTO_ZONE", "MOVE_TO"):
        return _expand_movement(action_name, params, model)

    elif action_name == "PICK_UP":
        item_id = params.get("item_id", params.get("raw", ""))
        return [Microaction(name="grasp", params={"item_id": item_id})]

    elif action_name == "PLACE":
        item_id = params.get("item_id", "")
        target = params.get("target_holder", "")
        return [Microaction(name="release", params={"item_id": item_id, "target": target})]

    elif action_name == "WAIT_AT":
        duration_str = params.get("duration", "PT0S")
        n_steps = _parse_duration_to_steps(duration_str, model)
        return [Microaction(name="stand", params={"remaining": n_steps})] * n_steps

    else:
        # TODO: add new action types here as domain grows
        print(f"[microactions] WARNING: unknown action '{action_name}' — no expansion")
        return []


# =============================================================================
# Movement expansion
# =============================================================================

def _expand_movement(
    action_name: str,
    params: dict,
    model,
) -> List[Microaction]:
    """
    Expand a GOTO_ZONE or MOVE_TO action into a STEP sequence.

    GOTO_ZONE: target is zone centroid
    MOVE_TO:   target is an env object's position or a coordinate

    SKELETON: straight-line path, fixed step size from mesa_configs.yaml.
    TODO Phase 4: replace with obstacle-aware path planning.
    """

    step_size = _get_step_size(model)
    target_pos = _resolve_target_position(action_name, params, model)

    if target_pos is None:
        print(f"[microactions] WARNING: could not resolve target for {action_name} {params}")
        return []

    # TODO Phase 4: replace with path planner, this is straight-line only
    # For skeleton: we don't know agent's current pos here (executor handles that)
    # Return a single placeholder STEP — executor will generate remaining steps
    # as it moves, or we pre-compute here once executor passes current pos.
    #
    # For now: return one STEP toward target as placeholder.
    # Real implementation: executor calls _steps_toward(current_pos, target, step_size)
    # each tick until arrival.

    return [Microaction(name="step", params={"target_pos": target_pos, "step_size": step_size})]


def steps_toward(
    current_pos: Tuple[float, float],
    target_pos: Tuple[float, float],
    step_size: float,
) -> List[Microaction]:
    """
    Generate the full STEP sequence from current_pos to target_pos.
    Called by executor at runtime when it knows the agent's current position.

    Straight-line interpolation — one STEP per call until arrival.
    TODO Phase 4: replace with path planning respecting obstacles.
    """
    steps = []
    x0, y0 = current_pos
    x1, y1 = target_pos
    dist = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    if dist <= step_size:
        # Already close enough — one final step to exact target
        steps.append(Microaction(name="step", params={"target_pos": target_pos}))
        return steps

    # Straight-line interpolation
    n_steps = math.ceil(dist / step_size)
    for i in range(1, n_steps + 1):
        t = min(i * step_size / dist, 1.0)
        ix = x0 + t * (x1 - x0)
        iy = y0 + t * (y1 - y0)
        steps.append(Microaction(name="step", params={"target_pos": (ix, iy)}))

    return steps


# =============================================================================
# Target position resolution
# =============================================================================

def _resolve_target_position(
    action_name: str,
    params: dict,
    model,
) -> Tuple[float, float] | None:
    """
    Resolve the target (x, y) for a movement action.

    GOTO_ZONE: returns centroid of the named zone
    MOVE_TO:   returns position of the named env object or kitting table
    """

    if action_name == "GOTO_ZONE":
        zone_id = params.get("zone_id", "")
        return _zone_centroid(zone_id, model)

    elif action_name == "MOVE_TO":
        target = params.get("target", params.get("raw", ""))
        # Strip any placeholder syntax e.g. "MOVE_TO(shelf_1)" → "shelf_1"
        target = target.replace("MOVE_TO(", "").replace(")", "").strip()

        # Look up in env_objects (shelves, tables, coffee machines, etc.)
        obj = model.get_env_object(target)
        if obj:
            return obj.position

        # Fallback: try as zone centroid
        return _zone_centroid(target, model)

    return None


def _zone_centroid(zone_id: str, model) -> Tuple[float, float] | None:
    """Return the centroid (x, y) of a zone from zone_map."""
    bounds = model.zone_map.get(zone_id)
    if bounds is None:
        return None
    cx = (bounds["x_min"] + bounds["x_max"]) / 2.0
    cy = (bounds["y_min"] + bounds["y_max"]) / 2.0
    return (cx, cy)


# =============================================================================
# Duration parsing
# =============================================================================

def _parse_duration_to_steps(duration_str: str, model) -> int:
    """
    Convert ISO 8601 duration string to number of Mesa steps.
    PT5M = 5 minutes, PT20S = 20 seconds.

    Step duration is read from mesa_configs.yaml (seconds_per_step).
    TODO: extend to hours (PTxH) if needed.
    """
    seconds = 0
    duration_str = duration_str.upper().replace("PT", "")

    if "M" in duration_str:
        parts = duration_str.split("M")
        seconds += int(parts[0]) * 60
        duration_str = parts[1] if len(parts) > 1 else ""
    if "S" in duration_str:
        seconds += int(duration_str.replace("S", ""))

    seconds_per_step = _get_seconds_per_step(model)
    return max(1, int(seconds / seconds_per_step))


# =============================================================================
# Mesa config helpers
# =============================================================================

_mesa_config_cache: dict = {}

def _load_mesa_config(model) -> dict:
    global _mesa_config_cache
    if _mesa_config_cache:
        return _mesa_config_cache
    config_path = Path(__file__).parent / "mesa_configs.yaml"
    if config_path.exists():
        with open(config_path) as f:
            _mesa_config_cache = yaml.safe_load(f) or {}
    return _mesa_config_cache


def _get_step_size(model) -> float:
    cfg = _load_mesa_config(model)
    return float(cfg.get("step_size", 20.0))


def _get_seconds_per_step(model) -> float:
    cfg = _load_mesa_config(model)
    return float(cfg.get("seconds_per_step", 1.0))