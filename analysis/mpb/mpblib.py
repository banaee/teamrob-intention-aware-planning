"""
mpblib.py — the meta-planner test-bed's typed values and its own derivations of P4's perception facts and the fallback
projection's shape (design_decisions.md, "T-D P", P4, Q6; glossary §2 "fallback projection", §9 "run length /
standing count"). Standard library only: the oracle (oracle.py), the chain assembly (chain.py), the compare and the
tests import it, and it imports nothing of the framework (MPB-1, the independence boundary).

Every rule is marked with its source: DP = design_decisions.md "T-D P" (P2 as superseded by P4, Q6); GL = glossary;
IO = shared/io_contracts.md §2.2.
"""
import json
import math
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Sequence, Tuple

Point = Tuple[float, float]

# DP P4: "the unit directions agree within 1e-9, the body's numerical resolution"; read as the Euclidean distance
# between the two unit vectors (the records name no norm; at this resolution the norms cannot disagree on a scripted
# walk, whose deviations are ~1e-14, nor on a turn, whose are > 1e-3).
DIRECTION_RESOLUTION = 1e-9


class Trigger(Enum):
    """IO §2.2: the three triggers."""
    NO_CURRENT_TASK = "no_current_task"
    RECOGNITION_CHANGED = "recognition_changed"
    PROJECTION_EXPIRED = "projection_expired"


class Cause(Enum):
    """IO §2.2 (L-build): the condition of recognition_changed that fired."""
    ENTERED = "entered"
    REPLACED = "replaced"
    BOUNDARY = "boundary"
    RETRACTION = "retraction"


class Gate(Enum):
    """The gate's outcome (design_decisions.md "T-D G", AD1, AD4; G1), by the names the records give it."""
    CLEARS = "clears"
    BELOW_THETA = "none(below_theta)"
    LEADER_NO_OBSERVATION = "none(leader_no_observation)"
    LEADER_INADEQUATE = "none(leader_inadequate)"
    LEADER_UNWARRANTED = "none(leader_unwarranted)"


class Mode(Enum):
    """DP P4: the fallback's two cases."""
    MOVING = "moving"
    STANDING = "standing"


@dataclass(frozen=True)
class Perception:
    """P4's perception facts of the observed human on one tick: the last displacement, the run length, the standing
    count (GL §9)."""
    displacement: Point
    run_length: int
    standing_count: int


@dataclass(frozen=True)
class Fallback:
    """The fallback projection a decision on the tick would rest on: its mode, the observed persistence k (the run
    length or the standing count), its duration (k, or less where the ray is cut) and its end on the world's clock
    (the decision tick + the observation offset + the duration; DP Q6 and IO: projection_expired fires on the first
    tick at or after it)."""
    mode: Mode
    k: int
    duration: float
    end: float

    def expiry_tick(self) -> int:
        return math.ceil(self.end)


@dataclass(frozen=True)
class Action:
    """A grounded action by its name and bindings (the IR test-bed's `sig`)."""
    name: str
    bindings: Tuple[Tuple[str, str], ...]


@dataclass(frozen=True)
class Admitted:
    """An admitted projection's identity: the admitted hypothesis's key and its plan, the planner's decomposition."""
    key: str
    actions: Tuple[Action, ...]


@dataclass(frozen=True)
class Refused:
    """A refused admission: the gate's refusal and the fallback it builds (None: no human, or none observed before)."""
    gate: Gate
    fallback: Optional[Fallback]


@dataclass(frozen=True)
class TickRow:
    """The per-tick table of parts 1 to 3 (MPB-1): what a decision on this tick would read and produce."""
    tick: int
    leader: Optional[str]
    boundary: bool
    gate: Gate
    adequacy: Dict[str, str]                      # live hypothesis -> adequate | inadequate | no_observation
    observation_warrant: Dict[str, str]           # live hypothesis -> observation | none (DG AD1, AD2)
    warrant: Tuple[str, ...]                      # the leader's warrant sources when the gate clears, else ()
    perception: Optional[Perception]
    fallback: Optional[Fallback]
    admitted: Optional[Admitted]                  # when the gate clears


@dataclass(frozen=True)
class Decision:
    """One decision of the chain: the trigger and cause (part 1), the gate and leader (part 2), the projection (part 3)."""
    tick: int
    trigger: Trigger
    cause: Optional[Cause]
    gate: Gate
    leader: Optional[str]
    warrant: Tuple[str, ...]
    admitted: Optional[Admitted]
    fallback: Optional[Fallback]


# ---- the perception facts (DP P4; GL §9) --------------------------------------------------------------------------
def perception(positions: Sequence[Point]) -> List[Optional[Perception]]:
    """From consecutive observed positions (the first the observation before the clock starts): None for the first
    (no previous observation); then the displacement; a zero displacement is a standing tick (the count grows, the run
    is 0); a step continues the run when its unit direction agrees with the previous step's within
    DIRECTION_RESOLUTION, otherwise a run of 1 starts (a turn, or the first step after a stand); a step resets the
    count."""
    out: List[Optional[Perception]] = [None]
    run, standing, last_u = 0, 0, None
    for prev, pos in zip(positions[:-1], positions[1:]):
        d = (pos[0] - prev[0], pos[1] - prev[1])
        if d == (0.0, 0.0):
            standing, run, last_u = standing + 1, 0, None
        else:
            length = math.hypot(*d)
            u = (d[0] / length, d[1] / length)
            run = run + 1 if last_u is not None and math.dist(u, last_u) <= DIRECTION_RESOLUTION else 1
            standing, last_u = 0, u
        out.append(Perception(d, run, standing))
    return out


# ---- the fallback's shape (DP P2 as kept by P4, P4, Q6) -----------------------------------------------------------
@dataclass(frozen=True)
class Room:
    """The workspace rectangle and the fixed objects (every non-portable object of the layout, landmarks included:
    DP P4, AS BUILT), with the arrival radius a walk stops at."""
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    fixed: Dict[str, Point] = field(default_factory=dict)
    arrival_radius: float = 0.0


def reach(position: Point, direction: Point, room: Room) -> float:
    """DP P2 (kept by P4): the distance along the ray to where the projected motion ends: the nearer of the workspace
    boundary and the entry into the arrival radius of the first fixed object along the ray; an object whose radius
    contains the ray's start is skipped."""
    px, py = position
    dx, dy = direction
    bounds = []
    if dx > 0:
        bounds.append((room.x_max - px) / dx)
    elif dx < 0:
        bounds.append((room.x_min - px) / dx)
    if dy > 0:
        bounds.append((room.y_max - py) / dy)
    elif dy < 0:
        bounds.append((room.y_min - py) / dy)
    r = max(0.0, min(bounds)) if bounds else 0.0
    for cx, cy in room.fixed.values():
        wx, wy = px - cx, py - cy
        if wx * wx + wy * wy <= room.arrival_radius ** 2:
            continue                                   # the start inside its radius: skipped
        along = -(wx * dx + wy * dy)                   # the distance to the closest approach, along the ray
        if along <= 0:
            continue                                   # behind the start
        miss2 = (wx * wx + wy * wy) - along * along    # the squared distance of the closest approach
        if miss2 > room.arrival_radius ** 2:
            continue                                   # the ray misses the disc
        r = min(r, along - math.sqrt(room.arrival_radius ** 2 - miss2))
    return r


def skipped_objects(position: Point, room: Room) -> List[str]:
    """The fixed objects whose arrival radius contains the position (the ones the ray skips)."""
    return sorted(i for i, (cx, cy) in room.fixed.items()
                  if (position[0] - cx) ** 2 + (position[1] - cy) ** 2 <= room.arrival_radius ** 2)


def fallback(tick: int, position: Point, p: Optional[Perception], room: Room, offset: float) -> Optional[Fallback]:
    """DP P4: MOVING, the last displacement continued for as many ticks as the run has lasted, ended earlier where the
    ray is cut (reach), no stand after it; STANDING, a stand at the observed position for as many ticks as the human has
    stood; no previous observation, none. From the observation offset; its end is the decision tick + offset +
    duration (Q6: the record's second value, the world's timestamp plus the fallback's T_h)."""
    if p is None:
        return None
    if p.displacement == (0.0, 0.0):
        return Fallback(Mode.STANDING, p.standing_count, float(p.standing_count),
                        tick + offset + float(p.standing_count))
    length = math.hypot(*p.displacement)
    u = (p.displacement[0] / length, p.displacement[1] / length)
    duration = min(float(p.run_length), reach(position, u, room) / length)
    return Fallback(Mode.MOVING, p.run_length, duration, tick + offset + duration)


# ---- JSON form ---------------------------------------------------------------------------------------------------
def _enc(value):
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {k: _enc(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_enc(v) for v in value]
    return value


def dump(objs, path):
    json.dump([_enc(asdict(o)) for o in objs], open(path, "w"), indent=0)


def _perception(d):
    return None if d is None else Perception(tuple(d["displacement"]), d["run_length"], d["standing_count"])


def _fallback(d):
    return None if d is None else Fallback(Mode(d["mode"]), d["k"], d["duration"], d["end"])


def _admitted(d):
    return None if d is None else Admitted(d["key"], tuple(Action(a["name"], tuple(tuple(b) for b in a["bindings"]))
                                                           for a in d["actions"]))


def load_ticks(path) -> List[TickRow]:
    return [TickRow(d["tick"], d["leader"], d["boundary"], Gate(d["gate"]), d["adequacy"], d["observation_warrant"],
                    tuple(d["warrant"]),
                    _perception(d["perception"]), _fallback(d["fallback"]), _admitted(d["admitted"]))
            for d in json.load(open(path))]


def load_decisions(path) -> List[Decision]:
    return [Decision(d["tick"], Trigger(d["trigger"]), None if d["cause"] is None else Cause(d["cause"]),
                     Gate(d["gate"]), d["leader"], tuple(d["warrant"]), _admitted(d["admitted"]),
                     _fallback(d["fallback"]))
            for d in json.load(open(path))]
