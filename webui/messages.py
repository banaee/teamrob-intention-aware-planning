"""
webui/messages.py

PURPOSE:
    The messages between the web-ui and a simulator (T-viz 0.4), defined once, as typed classes; the page's types are
    generated from them later (their JSON Schema, `model_json_schema()`). Three messages: the catalogue (what can be
    chosen), the run description (everything constant in one sim-run, sent when a model is built), the tick update
    (the complete changing state at the tick reached, not differences). Beside them the screen-user's choice of a
    sim-run (SimRunChoice, the body of a build request), the two refusals (BuildFailure, StepRefusal), and the other
    bodies and answers of the server's requests (SimRunRef, SimRunState, Current; T-viz 1a, webui/server.py).

THE VIEW (T-viz 1a, increment (ii)):
    With a layout chosen and no scenario, the page shows the layout alone; with a setup chosen as well, the layout with
    the setup's movable objects in their home containers and the setup's object states at its start (LayoutView, asked
    for by ViewChoice). A view has no sim-run, no agent and no tick. Its fields are the run description's and the tick
    update's types, produced by the simulator's side from the same reading of the layout and the setup as a model's,
    so that a view equals the matching part of the run description and the start tick update of every scenario on it.

THE TERMS:
    The framework's, as docs/glossary.md defines them: agents (humans, robots), fixed objects, movable objects, areas,
    the space, the human's script, the human executor's record, ticks. No simulator class or attribute name, no domain
    name, object type or area id: those arrive as data.

    `fixed_object_contents` lists the fixed objects that hold movable objects at that tick, each with the movable
    objects it holds in their order of arrival. It does not say which fixed objects are containers (glossary §10): a
    container that holds nothing at a tick is absent from it, and in stage 1a the messages name no container as such;
    the run description names the home container and the designated destination of each movable object.

    The order of arrival is supplied by the simulator's side so that a page reload keeps it. A display place (where
    the page draws a movable object inside a fixed object's footprint) is derived on the page from it; it is a display
    convention, not a world fact, and is written nowhere.

SECTIONS:
    The run description and the tick update hold the world under `world`. Stage 1b adds the robot's mind beside it,
    stage 1c the plots, each as a new field with an empty default; nothing defined here changes. The world's
    vocabulary and the mind's stay in separate sections. The tick update's `run` (T-viz 1a) holds the facts of the
    sim-run that are neither the world's nor the robot's mind's: the tick at which every agent had finished.

THE STEP LIMIT (T-viz 1a):
    A sim-run in the web-ui has a step limit only when one is set (LimitOption); without one it ends by reset, by a
    change of choice or at the server's stop.

TICKS:
    `TickUpdate.tick` is the number the run log gives the last step executed (its `step: N` lines, the record's
    `[rec] step=N`, the figures); None at the start, before tick 0. Durations are in ticks; lengths in the layout's unit.

TAGS:
    A class of a union carries `kind`, a literal fixed by its class: the JSON form's discriminator, never set by hand.
"""

from enum import Enum
from typing import Annotated, Literal, Optional, Union

from pydantic import Field

from webui.appearance import Appearance
from webui.message_base import Message

SimRunId = str   # opaque, assigned by the web-ui's server; every message after the catalogue names its sim-run


# =============================================================================
# Geometry
# =============================================================================

class Point(Message):
    x: float
    y: float


class Extent(Message):
    """A size: the extent along x and along y."""
    x: float
    y: float


class Direction(Message):
    """A unit direction."""
    x: float
    y: float


class Bounds(Message):
    x_min: float
    x_max: float
    y_min: float
    y_max: float


# =============================================================================
# Run options: declared by the simulator (catalogue), stated and in effect (run description)
# =============================================================================

class SwitchOption(Message):
    """A run option that is on or off."""
    kind: Literal["switch"] = "switch"
    name: str
    default: bool
    description: str


class OneOfOption(Message):
    """A run option that takes one value of a closed list."""
    kind: Literal["one_of"] = "one_of"
    name: str
    values: tuple[str, ...]
    default: str
    description: str


class LevelOption(Message):
    """A run option that is a number strictly between 0 and 1."""
    kind: Literal["level"] = "level"
    name: str
    default: float
    description: str


class LimitOption(Message):
    """A run option that is a limit: a whole number, at least `minimum`, or no limit (None)."""
    kind: Literal["limit"] = "limit"
    name: str
    default: Optional[int]
    minimum: int
    description: str


RunOptionDeclaration = Annotated[Union[SwitchOption, OneOfOption, LevelOption, LimitOption],
                                 Field(discriminator="kind")]


class SwitchValue(Message):
    kind: Literal["switch"] = "switch"
    name: str
    value: bool


class OneOfValue(Message):
    kind: Literal["one_of"] = "one_of"
    name: str
    value: str


class LevelValue(Message):
    kind: Literal["level"] = "level"
    name: str
    value: float


class LimitValue(Message):
    """A limit's value; None: no limit."""
    kind: Literal["limit"] = "limit"
    name: str
    value: Optional[int]


RunOptionValue = Annotated[Union[SwitchValue, OneOfValue, LevelValue, LimitValue], Field(discriminator="kind")]


class SimRunChoice(Message):
    """The screen-user's choice of a sim-run: the domain, the layout, the scenario (its setup is the scenario's) and
    a value for every run option the catalogue declares."""
    domain: str
    layout: str
    scenario: str
    options: tuple[RunOptionValue, ...]


# =============================================================================
# The catalogue
# =============================================================================

class LayoutEntry(Message):
    """A layout: its id, its title (stale in older layouts), and its notes, the free text of the layout file that says
    what the room is for (None when it has none)."""
    id: str
    title: str
    notes: Optional[str]


class SetupEntry(Message):
    """A setup: its id and its notes, the free text of the setup file (None when it has none)."""
    id: str
    notes: Optional[str]


class ScenarioEntry(Message):
    """A scenario with its two bindings: the one setup it binds and its reference layouts (the first is the one a
    run takes when it names no layout). A run on another layout of the domain is valid and never a baseline."""
    id: str
    setup: str
    reference_layouts: tuple[str, ...]
    description: str


class DomainEntry(Message):
    """A domain: what can be chosen in it, and its scene appearance (the defaults where it states none)."""
    name: str
    layouts: tuple[LayoutEntry, ...]
    setups: tuple[SetupEntry, ...]
    scenarios: tuple[ScenarioEntry, ...]
    appearance: Appearance


class Catalogue(Message):
    """What can be chosen: per domain its layouts, setups and scenarios, and the run options with their values and
    defaults; `default_choice` is the run file's."""
    domains: tuple[DomainEntry, ...]
    run_options: tuple[RunOptionDeclaration, ...]
    default_choice: SimRunChoice


# =============================================================================
# Tasks, actions and the human's script
# =============================================================================

class Binding(Message):
    parameter: str
    value: str


class TaskRef(Message):
    """A task instance: its schema's name and its bindings; `label` is the framework's derived label, the text the
    logs show."""
    task: str
    bindings: tuple[Binding, ...]
    label: str


class ActionRef(Message):
    """A grounded action: its schema's name and its bindings."""
    action: str
    bindings: tuple[Binding, ...]


class AfterActionTrigger(Message):
    """After the action (its schema's name) of the entry's expansion completes; `occurrence` its 0-based occurrence,
    None when it occurs once."""
    kind: Literal["after_action"] = "after_action"
    action: str
    occurrence: Optional[int]


class DuringActionTrigger(Message):
    """A cut `time` (as written, ISO-8601) into the action."""
    kind: Literal["during_action"] = "during_action"
    action: str
    time: str
    occurrence: Optional[int]


class NowTrigger(Message):
    """A live event, fired on the tick it is applied."""
    kind: Literal["now"] = "now"


Trigger = Annotated[Union[AfterActionTrigger, DuringActionTrigger, NowTrigger], Field(discriminator="kind")]


class StartDecision(Message):
    kind: Literal["start"] = "start"
    task: TaskRef


class DropDecision(Message):
    kind: Literal["drop"] = "drop"


Decision = Annotated[Union[StartDecision, DropDecision], Field(discriminator="kind")]


class Event(Message):
    trigger: Trigger
    decision: Decision


class ScriptEntry(Message):
    task: TaskRef
    events: tuple[Event, ...]


class RepeatableEntry(Message):
    task: TaskRef


class ScriptDependence(str, Enum):
    INDEPENDENT = "independent"
    ON_ROBOT = "on_robot"


class HumanScript(Message):
    """A human's script: the ordinary entries of the priority list in written order, its repeatable entries, its
    closing part, and whether it depends on the robot."""
    human: str
    dependence: ScriptDependence
    entries: tuple[ScriptEntry, ...]
    repeatable: tuple[RepeatableEntry, ...]
    closing: tuple[ScriptEntry, ...]


class EntryPart(str, Enum):
    ORDINARY = "ordinary"
    REPEATABLE = "repeatable"
    CLOSING = "closing"


class EntryPosition(Message):
    """Which entry of the script: its part and its index there."""
    part: EntryPart
    index: int


# =============================================================================
# The run description
# =============================================================================

class RunTriple(Message):
    domain: str
    layout: str
    setup: str
    scenario: str


class Space(Message):
    title: str
    bounds: Bounds


class Area(Message):
    id: str
    bounds: Bounds


class FixedObject(Message):
    """A fixed object of the layout, at its position for the whole sim-run (an override applied)."""
    id: str
    type: str
    subtype: Optional[str]
    position: Point
    size: Extent


class MovableObject(Message):
    """A movable object of the setup: its home container and, where the domain determines one, its designated
    destination. Where it is at a tick is the tick update's."""
    id: str
    type: str
    subtype: Optional[str]
    size: Extent
    home_container: str
    destination: Optional[str]


class AgentEntry(Message):
    id: str


class TimelineSource(str, Enum):
    SCENARIO = "scenario"
    SETUP = "setup"
    NONE = "none"


class TimelineWindow(Message):
    """A timeline fact holds on the ticks [start, until); `until` None: to the run's end."""
    fact: str
    start: int
    until: Optional[int]


class TimelineInForce(Message):
    source: TimelineSource
    windows: tuple[TimelineWindow, ...]


class WorldDescription(Message):
    space: Space
    areas: tuple[Area, ...]
    fixed_objects: tuple[FixedObject, ...]
    movable_objects: tuple[MovableObject, ...]
    humans: tuple[AgentEntry, ...]
    robots: tuple[AgentEntry, ...]
    scripts: tuple[HumanScript, ...]
    timeline: TimelineInForce


class RunDescription(Message):
    """Everything constant in one sim-run, sent when its model is built: the triple, the run options as the
    screen-user stated them and as the model applies them (an option set off by another shows here), and the world."""
    sim_run: SimRunId
    run: RunTriple
    stated: SimRunChoice
    effective: tuple[RunOptionValue, ...]
    world: WorldDescription


# =============================================================================
# The tick update
# =============================================================================

class AgentTick(Message):
    """An agent at the tick: its position, and the unit direction of its most recent step that moved it (None before
    it has moved), computed from its own positions."""
    id: str
    position: Point
    last_motion: Optional[Direction]


class FixedObjectContents(Message):
    """A fixed object that holds movable objects at the tick, with them in their order of arrival (at the start, the
    setup's order; two arriving on one tick, the setup's order)."""
    fixed_object: str
    movable_objects: tuple[str, ...]


class Carried(Message):
    agent: str
    movable_object: str


class ObjectState(Message):
    """A declared state that holds; `object` None for a fact about no object."""
    state: str
    object: Optional[str]


class ActionInHand(Message):
    """The action the human's executor has in hand, its occurrence in the task's expansion, and its progress in
    ticks."""
    action: ActionRef
    occurrence: int
    done: int
    total: int


class Outcome(str, Enum):
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    ABANDONED = "abandoned"
    INFEASIBLE = "infeasible"


class DecisionRefusalReason(str, Enum):
    STACK_FULL = "stack_full"
    EMPTY_STACK = "empty_stack"


class UnfiredReason(str, Enum):
    ANCHOR_ABSENT = "anchor_absent"
    ANCHOR_AMBIGUOUS = "anchor_ambiguous"
    ANCHOR_OUT_OF_RANGE = "anchor_out_of_range"
    NEVER_REACHED = "never_reached"
    PAST_ACTION = "past_action"


class AtBoundary(Message):
    """After the action (its occurrence) completed."""
    kind: Literal["boundary"] = "boundary"
    action: ActionRef
    occurrence: int


class AtBeginning(Message):
    """Before the task's first action."""
    kind: Literal["beginning"] = "beginning"


class AtCut(Message):
    """Inside the action (its occurrence), `done` of its ticks executed."""
    kind: Literal["cut"] = "cut"
    action: ActionRef
    occurrence: int
    done: int


Where = Annotated[Union[AtBoundary, AtBeginning, AtCut], Field(discriminator="kind")]


class Entered(Message):
    """A script entry's task pushed on the empty stack."""
    kind: Literal["entered"] = "entered"
    task: TaskRef


class Started(Message):
    """A task pushed on the stack by an event; `where` on the task below it, None on an empty stack."""
    kind: Literal["started"] = "started"
    task: TaskRef
    trigger: Trigger
    where: Optional[Where]


class Resumed(Message):
    kind: Literal["resumed"] = "resumed"
    task: TaskRef


class Left(Message):
    """A task left the top of the stack, or was pushed down (suspended)."""
    kind: Literal["left"] = "left"
    task: TaskRef
    outcome: Outcome


class Refused(Message):
    kind: Literal["refused"] = "refused"
    decision: Decision
    reason: DecisionRefusalReason


class Unfired(Message):
    kind: Literal["unfired"] = "unfired"
    task: TaskRef
    event: Event
    reason: UnfiredReason


class StillOpen(Message):
    """An entry still open where the script stops being followed (a script that depends on the robot)."""
    kind: Literal["still_open"] = "still_open"
    task: TaskRef
    entry: EntryPosition


Transition = Annotated[Union[Entered, Started, Resumed, Left, Refused, Unfired, StillOpen],
                       Field(discriminator="kind")]


class HumanActivity(Message):
    """What a human's executor is doing at the tick, from its record: the stack, top first; the action in hand; the
    stack's transitions on the tick; the script's entries still open (ordinary, then closing)."""
    human: str
    stack: tuple[TaskRef, ...]
    action: Optional[ActionInHand]
    transitions: tuple[Transition, ...]
    open_entries: tuple[EntryPosition, ...]


class WorldTick(Message):
    """The world at the tick. Every movable object is in exactly one of `fixed_object_contents` and `carried`."""
    humans: tuple[AgentTick, ...]
    robots: tuple[AgentTick, ...]
    fixed_object_contents: tuple[FixedObjectContents, ...]
    carried: tuple[Carried, ...]
    object_states: tuple[ObjectState, ...]
    timeline_facts: tuple[str, ...]
    activity: tuple[HumanActivity, ...]


class EndReason(str, Enum):
    STEPS_REACHED = "steps_reached"
    RESET = "reset"
    CHOICE_CHANGED = "choice_changed"
    SERVER_STOPPED = "server_stopped"


class StillOpenEntry(Message):
    human: str
    task: TaskRef
    entry: EntryPosition


class RunEnd(Message):
    """The sim-run's end: why, and the entries still open of each script that depends on the robot."""
    reason: EndReason
    still_open: tuple[StillOpenEntry, ...]


class RunTick(Message):
    """The facts of the sim-run at the tick that are neither the world's nor the robot's mind's. `finished_at`: the
    first tick at which every human's script had ended (every entry closed, the stack empty) and every robot's task
    pool was empty (the tick of its empty-pool log line); None before. Once set, it is kept."""
    finished_at: Optional[int]


class TickUpdate(Message):
    sim_run: SimRunId
    tick: Optional[int]
    world: WorldTick
    run: RunTick
    end: Optional[RunEnd]


# =============================================================================
# The view of a layout, or of a layout and a setup (T-viz 1a)
# =============================================================================

class ViewChoice(Message):
    """The body of a view request: a layout of the domain, and optionally a setup."""
    domain: str
    layout: str
    setup: Optional[str]


class SetupView(Message):
    """A setup's part of a view: its movable objects in the setup's order, the fixed objects that hold them at the
    start (each with them in the setup's order), and the object states that hold at the start."""
    id: str
    movable_objects: tuple[MovableObject, ...]
    fixed_object_contents: tuple[FixedObjectContents, ...]
    object_states: tuple[ObjectState, ...]


class LayoutView(Message):
    """The view of a layout (the space, the areas, the fixed objects) and, with a setup chosen, of the setup at its
    start. No sim-run, no agent, no tick."""
    domain: str
    layout: str
    space: Space
    areas: tuple[Area, ...]
    fixed_objects: tuple[FixedObject, ...]
    setup: Optional[SetupView]


# =============================================================================
# Refusals
# =============================================================================

class BuildFailure(Message):
    """A model that could not be built from the choice; no sim-run exists and no log pair is written."""
    message: str


class SimRunRef(Message):
    """The body of a request on one sim-run (step, reset)."""
    sim_run: SimRunId


class SimRunState(Message):
    """A sim-run as the page needs it to draw: its run description and its latest tick update (the start's before
    the first step). The answer to choose, reset and current."""
    description: RunDescription
    tick: TickUpdate


class Current(Message):
    """The answer to current: the current sim-run, or the current view, or neither (both None). At most one is set."""
    state: Optional[SimRunState]
    view: Optional[LayoutView]


class StepRefusalReason(str, Enum):
    NOT_CURRENT = "not_current"
    ENDED = "ended"
    BUSY = "busy"


class ViewRefusal(Message):
    """A view refused: a sim-run that has been stepped is current, and the choices are locked until a reset."""
    sim_run: SimRunId


class StepRefusal(Message):
    """A step or a reset refused: the sim-run is not the current one, it has ended (a step only), or a step of it is
    under way."""
    sim_run: SimRunId
    reason: StepRefusalReason
