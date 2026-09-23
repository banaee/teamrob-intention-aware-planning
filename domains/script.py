# domains/script.py
"""
The human action script, scenario layer (T-C1, built in T-C2a). Domain-generic.

A human's scheduled_tasks is written as a flat list of primitives, TaskInstances
and deviations (interrupt / deviate / abandon), in any mix. At load it is
resolved into primitives only: every TaskInstance is expanded by the planner's
own decomposition (expand), every deviation is applied to its task's expansion by
the list helpers below. Expansion is SEQUENTIAL (T-C2b): each task is expanded
against the symbolic state the elements before it leave behind, the initial world
advanced by what their action schemas declare (shared/projection.py,
successor_state(), the successor state the robot's orderings are projected
through), so the script is what the executor would have decided at run time and
is fully known at load. The robot's mind receives nothing from any of it.

Where a world is needed: expand() and resolve_script() take the world, so they
run only where one exists (the loader, tests, a later scenario generator). The
vocabulary (interrupt, deviate, abandon) is written in scenario files at import,
where no world exists, so it returns a deferred edit (Deviation) that the loader
resolves; anchor errors surface there, naming the scenario and printing the
expansion. The list helpers (insert_after, insert_before, retarget, truncate) are
pure operations on an expanded list and may be called directly on one.

The data types (ScriptAction, Stay, Provenance, Deviation) live in shared/types.py
beside AgentConfig, whose work-order check reads provenance.
"""

from typing import Dict, List, Optional, Sequence, Union

from shared.projection import successor_state
from shared.target_resolution import movement_target_position
from shared.types import (
    ConditionSchema, Const, Deviation, GroundedAction, Provenance, ScriptAction, Stay,
    TaskInstance, Var, WorldState, check_task_bindings, destination_derivations,
)

Anchor = Union[str, int]


# =============================================================================
# expand and ground
# =============================================================================

def expand(task: TaskInstance, planner, world: WorldState, agent_id: str,
           method: Optional[str] = None) -> List[ScriptAction]:
    """
    The planner's own decomposition of `task` for `agent_id` against `world` (the
    scenario's initial world at load), as one ScriptAction per action of the
    selected method, each carrying the same Provenance (the task it came from).
    `method` names one of the task's methods; it must apply in `world`. Omitted,
    the planner chooses as it does for any plan. ?agent is execution context and
    is not kept: it is injected again when the element is grounded.
    """
    params = {var.name: const.value for var, const in task.bindings.items()}
    actions = planner.decompose(task.schema.name, params, agent_id, world, method=method)
    provenance = Provenance(task)
    return [
        ScriptAction.of(a.action_name,
                        {k: v for k, v in a.bindings.items() if k != "?agent"},
                        provenance=provenance)
        for a in actions
    ]


def ground(element: ScriptAction, agent_id: str, knowledge) -> GroundedAction:
    """
    The GroundedAction a ScriptAction stands for, for `agent_id`: its action
    schema and a fully grounded completion predicate, the substitution decompose()
    applies to the same action inside a method. A Stay grounds to nothing and is
    not accepted here; a coordinate-valued target has no object to ground to.
    """
    schema = knowledge.get_action_schema(element.action_name)
    if schema is None:
        raise ValueError(f"{element}: '{element.action_name}' is not an action of this domain")
    bindings: Dict[str, str] = {"?agent": agent_id}
    for var_name, value in element.bindings:
        if not isinstance(value, str):
            raise ValueError(f"{element}: {var_name} is a coordinate, which grounds to no object")
        bindings[var_name] = value
    completion = None
    if isinstance(schema.completion, ConditionSchema):
        completion = schema.completion.to_predicate(bindings)
    return GroundedAction(action_name=schema.name, bindings=bindings,
                          completion_predicate=completion, schema=schema)


# =============================================================================
# list helpers — pure operations on an expanded list
# =============================================================================

def _render(elements: Sequence) -> str:
    return "[" + ", ".join(f"{i}: {e}" for i, e in enumerate(elements)) + "]"


def anchor_index(elements: Sequence, anchor: Anchor) -> int:
    """
    The index an anchor names: an action name that occurs exactly once among the
    ScriptActions, or a 0-based index. Anything else, a name absent or repeated,
    or an index out of range, is an error that prints the list.
    """
    if isinstance(anchor, bool) or not isinstance(anchor, (str, int)):
        raise ValueError(f"anchor {anchor!r}: an action name or a 0-based index; expansion {_render(elements)}")
    if isinstance(anchor, int):
        if not 0 <= anchor < len(elements):
            raise ValueError(f"anchor {anchor}: index out of range; expansion {_render(elements)}")
        return anchor
    hits = [i for i, e in enumerate(elements) if isinstance(e, ScriptAction) and e.action_name == anchor]
    if len(hits) != 1:
        raise ValueError(
            f"anchor '{anchor}': must occur exactly once, occurs at {hits}; expansion {_render(elements)}")
    return hits[0]


def insert_after(elements: Sequence, anchor: Anchor, content: Sequence) -> list:
    i = anchor_index(elements, anchor)
    return list(elements[:i + 1]) + list(content) + list(elements[i + 1:])


def insert_before(elements: Sequence, anchor: Anchor, content: Sequence) -> list:
    i = anchor_index(elements, anchor)
    return list(elements[:i]) + list(content) + list(elements[i:])


def truncate(elements: Sequence, after: Optional[Anchor] = None, before: Optional[Anchor] = None) -> list:
    """The list cut at an anchor: up to and including it (after=), or up to it (before=)."""
    _one_anchor(after, before)
    if after is not None:
        return list(elements[:anchor_index(elements, after) + 1])
    return list(elements[:anchor_index(elements, before)])


def retarget(elements: Sequence, old: str, new: str) -> list:
    """
    Every ScriptAction binding whose value is `old` bound to `new` instead, the
    provenance kept. On a delivery's expansion with old = its destination this is
    the place and the walk before it.
    """
    out = []
    for e in elements:
        if isinstance(e, ScriptAction) and any(v == old for _, v in e.bindings):
            e = ScriptAction.of(e.action_name,
                                {k: (new if v == old else v) for k, v in e.bindings},
                                provenance=e.provenance)
        out.append(e)
    return out


def _one_anchor(after, before) -> None:
    if (after is None) == (before is None):
        raise ValueError("exactly one of after= and before= is given")


# =============================================================================
# the vocabulary — deferred edits, resolved at load
# =============================================================================

def interrupt(task: TaskInstance, after: Optional[Anchor] = None, before: Optional[Anchor] = None,
              with_: Sequence = ()) -> List[Deviation]:
    """`with_` (tasks and/or primitives) inserted inside `task`, at an anchor of its expansion."""
    _one_anchor(after, before)
    return [Deviation("interrupt", task, after=after, before=before, content=list(with_))]


def deviate(task: TaskInstance, destination: str) -> List[Deviation]:
    """`task`'s carry goes to `destination`: the place and the walk before it are retargeted."""
    if not destination_derivations(task.schema):
        raise ValueError(f"deviate: task '{task.schema.name}' declares no destination parameter")
    return [Deviation("deviate", task, destination=destination)]


def abandon(task: TaskInstance, after: Optional[Anchor] = None, before: Optional[Anchor] = None,
            then: Sequence = ()) -> List[Deviation]:
    """`task` stops at an anchor of its expansion; `then` (tasks and/or primitives) follows."""
    _one_anchor(after, before)
    return [Deviation("abandon", task, after=after, before=before, content=list(then))]


# =============================================================================
# resolution at load
# =============================================================================

def deviation_destination(dev: Deviation, world: WorldState):
    """(var name, old value) of the destination a `deviate` rebinds: the task's own
    binding of the determined parameter, else the station's destination."""
    var_name, source_var = destination_derivations(dev.task.schema)[0]
    bound = {var.name: const.value for var, const in dev.task.bindings.items()}
    if var_name in bound:
        return var_name, bound[var_name]
    return var_name, world.object_destination.get(bound[source_var])


def resolve_script(elements: Sequence, planner, world: WorldState, agent_id: str) -> List[Union[ScriptAction, Stay]]:
    """
    The executed form of a script: TaskInstances expanded, deviations applied,
    primitives kept, in order. Sequential (T-C2b): each element is resolved
    against `world` advanced by every element before it (after()), so a task
    that follows a change of mind is expanded with the return the planner would
    choose at run time. Content injected by a deviation is resolved first, at
    its anchor, so it may mix tasks and primitives.
    """
    out: List[Union[ScriptAction, Stay]] = []
    for e in elements:
        if isinstance(e, TaskInstance):
            resolved = expand(e, planner, world, agent_id)
        elif isinstance(e, (ScriptAction, Stay)):
            resolved = [e]
        elif isinstance(e, Deviation):
            resolved = _apply(e, planner, world, agent_id)
        else:
            raise TypeError(f"script element {e!r}: not a primitive, a TaskInstance or a deviation")
        out.extend(resolved)
        world = after(resolved, world, agent_id, planner.knowledge)
    return out


def after(elements: Sequence, world: WorldState, agent_id: str, knowledge) -> WorldState:
    """
    The symbolic state `elements` (primitives) leave `world` in, for `agent_id`:
    each ScriptAction grounded and handed to successor_state(), the one the
    projection of an ordering uses, so the script's state and the robot's
    projected state are one derivation; the agent stands at the target of its
    last walk. A Stay changes nothing. A new value; `world` is not written.
    """
    actions = [ground(e, agent_id, knowledge) for e in elements if isinstance(e, ScriptAction)]
    end_pos = None
    for action in actions:
        if action.schema.movement_target_key is not None:
            end_pos = movement_target_position(action, world) or end_pos
    return successor_state(world, actions, agent_id, end_pos) if actions else world


def _apply(dev: Deviation, planner, world: WorldState, agent_id: str) -> list:
    """
    A deviation applied to its task's expansion against `world`; injected
    content is resolved against the state the expansion's part before the
    anchor leaves behind (after the truncated part, for `abandon`).
    """
    base = expand(dev.task, planner, world, agent_id)
    knowledge = planner.knowledge
    if dev.kind == "interrupt":
        i = anchor_index(base, dev.after if dev.after is not None else dev.before)
        prefix = base[:i + 1] if dev.after is not None else base[:i]
        content = resolve_script(dev.content, planner, after(prefix, world, agent_id, knowledge), agent_id)
        if dev.after is not None:
            return insert_after(base, dev.after, content)
        return insert_before(base, dev.before, content)
    if dev.kind == "abandon":
        kept = truncate(base, after=dev.after, before=dev.before)
        content = resolve_script(dev.content, planner, after(kept, world, agent_id, knowledge), agent_id)
        return kept + content
    if dev.kind == "deviate":
        _, old = deviation_destination(dev, world)
        return retarget(base, old, dev.destination)
    raise ValueError(f"unknown deviation kind '{dev.kind}'")


def check_script_bindings(script: Sequence, object_type_by_id: Dict[str, str], knowledge) -> None:
    """
    Every task in a script is well typed against the layout (check_task_bindings,
    F47b), including a deviation's task, its content and, for `deviate`, the task
    rebound to its new destination; every object a primitive names exists. A
    coordinate and a schema's duration binding name no object.
    """
    for e in script:
        if isinstance(e, TaskInstance):
            check_task_bindings(e, object_type_by_id)
        elif isinstance(e, Deviation):
            check_task_bindings(e.task, object_type_by_id)
            if e.kind == "deviate":
                var_name, _ = destination_derivations(e.task.schema)[0]
                bindings = {v: c for v, c in e.task.bindings.items() if v.name != var_name}
                bindings[Var(var_name)] = Const(e.destination)
                check_task_bindings(TaskInstance(schema=e.task.schema, bindings=bindings), object_type_by_id)
            check_script_bindings(e.content, object_type_by_id, knowledge)
        elif isinstance(e, ScriptAction):
            schema = knowledge.get_action_schema(e.action_name)
            if schema is None:
                raise ValueError(f"{e}: '{e.action_name}' is not an action of this domain")
            for var_name, value in e.bindings:
                if var_name == schema.duration_key or not isinstance(value, str):
                    continue
                if value not in object_type_by_id:
                    raise ValueError(f"{e}: {var_name} is '{value}', which is not an object of this layout")
