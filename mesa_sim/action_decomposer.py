"""
mesa_sim/action_decomposer.py

PURPOSE:
    Expands GroundedActions from the planner into concrete Mesa-executable
    microaction sequences. This is the top-down symbolic→physical translation
    layer for the Mesa embodiment.

WHAT THIS MODULE DOES:
    - Takes one GroundedAction at a time
    - Reads operator.microactions to determine expansion type
    - Reads operator.movement_target_key to resolve movement targets
      from action.bindings — no action name string matching
    - Expands "STEP*" into a full STEP sequence using steps_toward()
    - Expands "STAND*" into N STAND microactions
    - Expands fixed lists e.g. ["GRASP"], ["RELEASE"], ["TOUCH"] into single microactions

WHAT THIS MODULE DOES NOT DO:
    - Does NOT execute microactions — that is mesa_sim/executor.py
    - Does NOT do path planning — uses straight-line steps for skeleton phase
    - Does NOT know about IR or planning logic
    - Does NOT handle ROS
    - Does NOT match action names — expansion is driven by operator.microactions

ROS EQUIVALENT:
    In ROS, this module has NO direct equivalent because ROS works in reverse:
    - ros_sim/microaction_classifier_ros.py goes BOTTOM-UP:
      raw sensor streams → discrete microaction labels → Observation → recognizer
    - ros_sim/goal_executor_ros.py handles GroundedAction execution by sending
      goals directly to ROS action servers (move_base, MoveIt, etc.)
    - ROS handles its own motion planning internally — no STEP expansion needed

STEP EXPANSION (skeleton):
    Currently uses straight-line interpolation toward target position.
    Step size is read from mesa_configs.yaml.
    TODO Phase 4: replace with proper path planning (A*, RRT, etc.)
    that respects obstacles from env_layout1.json.

CALLED BY:
    - mesa_sim/executor.py — calls expand(action, model, agent_pos)
"""

from dataclasses import dataclass, field
import logging
from typing import List, Dict, Any, Tuple, Optional
import math
import yaml
from pathlib import Path

from shared.types import GroundedAction


# =============================================================================
# Microaction dataclass
# =============================================================================

@dataclass
class Microaction:
    """
    A single atomic Mesa-executable step.
    Produced by expand(), consumed one per step by executor.py.
    """
    name: str                              # "step", "grasp", "release", "stand", "touch", etc.
    params: Dict[str, Any] = field(default_factory=dict)

    def __str__(self):
        return f"{self.name}({self.params})"


# =============================================================================
# Main expansion function
# =============================================================================

def expand(
    action: GroundedAction,
    model,
    agent_pos: Tuple[float, float],
) -> List[Microaction]:
    """
    Expand one GroundedAction into a list of concrete Microactions.

    Expansion is driven entirely by action.operator.microactions —
    no action name string matching anywhere.

    INPUT:
        action    — GroundedAction from current AbstractPlan
        model     — for position lookups (read-only)
        agent_pos — agent's current position, needed for STEP* expansion

    OUTPUT:
        List[Microaction] — ordered sequence to execute, one per Mesa step

    EXPANSION RULES:
        operator.microactions == "STEP*"   → full STEP sequence to movement target
        operator.microactions == "STAND*"  → N STAND microactions (duration from bindings)
        operator.microactions == ["GRASP"] → single GRASP with item_id from bindings
        operator.microactions == ["RELEASE"] → single RELEASE
        operator.microactions == ["TOUCH"] → single TOUCH with item_id from bindings
        unknown                            → empty list with warning
    """
    spec = action.operator.microactions

    if spec == "STEP*":
        return _expand_step(action, model, agent_pos)

    elif spec == "STAND*":
        return _expand_stand(action, model)

    elif isinstance(spec, list):
        return _expand_fixed(action, spec)

    else:
        logging.warning(f"[action_decomposer] WARNING: unknown microactions spec "
              f"'{spec}' for action '{action.action_name}' — no expansion")
        return []


# =============================================================================
# Expansion helpers
# =============================================================================

def _expand_step(
    action: GroundedAction,
    model,
    agent_pos: Tuple[float, float],
) -> List[Microaction]:
    """
    Expand a STEP* action into a full step sequence.
    Target is resolved from action.operator.movement_target_key → action.bindings.
    No action name matching — movement_target_key declared in ActionOperator.
    """
    target_pos = _resolve_movement_target(action, model)
    if target_pos is None:
        logging.warning(f"[action_decomposer] WARNING: could not resolve movement target "
              f"for '{action.action_name}' bindings={action.bindings}")
        return []

    step_size = _get_step_size(model)
    return steps_toward(agent_pos, target_pos, step_size)


def _expand_stand(
    action: GroundedAction,
    model,
) -> List[Microaction]:
    """
    Expand a STAND* action into N stand microactions.
    Duration comes from ?duration binding if present, else defaults to 1 step.
    TODO Phase 4: parse ISO 8601 duration from binding if domain uses it.
    """
    duration_str = action.bindings.get("?duration", "PT1S")
    n_steps = _parse_duration_to_steps(duration_str, model)
    return [Microaction(name="stand", params={"remaining": n_steps})] * n_steps


def _expand_fixed(
    action: GroundedAction,
    spec: List[str],
) -> List[Microaction]:
    """
    Expand a fixed microaction list e.g. ["GRASP"] or ["RELEASE"] or ["TOUCH"] into the corresponding microaction(s).
    Reads item_id from bindings for GRASP.
    RELEASE needs no params — executor detects target by proximity.
    TOUCH ???
    """
    result = []
    for mu in spec:
        mu_lower = mu.lower()
        if mu_lower == "grasp":
            item_id = action.bindings.get("?item", "")
            result.append(Microaction(name="grasp", params={"item_id": item_id}))
        elif mu_lower == "release":
            result.append(Microaction(name="release", params={}))
        
        elif mu_lower == "touch":
            item_id = action.bindings.get("?item", "")
            result.append(Microaction(name="touch", params={"item_id": item_id}))
        
        # Add more fixed microactions here as needed, e.g. based on the domain's microaction vocabulary
        
        else:
            result.append(Microaction(name=mu_lower, params={}))
    return result


# =============================================================================
# Movement target resolution
# =============================================================================

def _resolve_movement_target(
    action: GroundedAction,
    model,
) -> Optional[Tuple[float, float]]:
    """
    Resolve the (x, y) movement target for a STEP* action.
    Uses action.operator.movement_target_key to find the relevant binding.
    No action name string matching.
    """
    key = action.operator.movement_target_key
    if key is None:
        return None

    target_id = action.bindings.get(key)
    if not target_id:
        return None

    target_type = action.operator.movement_target_type
    if target_type == "object":
        return _env_object_position(target_id, model)
    else:
        logging.warning(f"[action_decomposer] WARNING: movement_target_type not set "
                        f"for '{action.action_name}' — cannot resolve target")
        return None


def _env_object_position(obj_id: str, model) -> Optional[Tuple[float, float]]:
    """Return the position of a named env object or item."""
    obj = model.get_env_object(obj_id)
    if obj is not None:
        return obj.position
    item = model.get_item(obj_id)
    if item is not None:
        return item.position
    return None

# =============================================================================
# Step sequence generation
# =============================================================================

def steps_toward(
    current_pos: Tuple[float, float],
    target_pos: Tuple[float, float],
    step_size: float,
) -> List[Microaction]:
    """
    Generate the full STEP sequence from current_pos to target_pos.
    Straight-line interpolation.
    TODO Phase 4: replace with obstacle-aware path planning (A*, RRT, etc.)
    """
    steps = []
    x0, y0 = current_pos
    x1, y1 = target_pos
    dist = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    if dist <= step_size:
        steps.append(Microaction(name="step", params={"target_pos": target_pos}))
        return steps

    n_steps = math.ceil(dist / step_size)
    for i in range(1, n_steps + 1):
        t = min(i * step_size / dist, 1.0)
        ix = x0 + t * (x1 - x0)
        iy = y0 + t * (y1 - y0)
        steps.append(Microaction(name="step", params={"target_pos": (ix, iy)}))

    return steps


# =============================================================================
# Duration parsing
# =============================================================================

def _parse_duration_to_steps(duration_str: str, model) -> int:
    """
    Convert ISO 8601 duration string to number of Mesa steps.
    PT5M = 5 minutes, PT20S = 20 seconds.
    Step duration read from mesa_configs.yaml (seconds_per_step).
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