"""
webui/appearance.py

PURPOSE:
    The scene appearance (T-viz 0.3): how the env-pane draws the things of one domain. Not a world fact: the
    simulation never reads it, and nothing here goes into a layout or a setup. A domain states its values in its own
    file (domains/<domain>/appearance.json), validated against these definitions; the page reads them as data.

THE SHAPE VOCABULARY:
    The page knows a closed set of forms (ShapeKind, MovableShape, Figure), each drawn by the page's code. The
    vocabulary names forms, never a domain's object types: the data maps an object type to a form. A type with no
    entry takes the default look below, and a domain without a file is drawn entirely from defaults, so a new domain is
    drawn without a change to the web-ui's code. A new form is web-ui code. No form has a front: the messages carry no
    orientation (TODO-192).

PRESENCE:
    A property of the look, declared per object type in the appearance data: background (drawn as lines and pale
    faces) or active (an object the agents' activities use, drawn with a representative form and a tone). It is not a
    world fact. Deriving it from a run's bindings was measured in 0.3 and found unstable (docs/design_records.md,
    "T-viz, the web-ui", 0.3).

UNITS:
    Heights in the layout's unit, like the sizes of the run description.
"""

from enum import Enum

from webui.message_base import Message


class ShapeKind(str, Enum):
    """The forms of a fixed object, drawn over its footprint."""
    BLOCK = "block"            # a closed box
    RACK = "rack"              # four posts and boards; contents on the lowest board
    COUNTER = "counter"        # a top on legs; contents on the top
    PAD = "pad"                # a marked rectangle on the floor; contents on the floor
    ENCLOSURE = "enclosure"    # low walls on every side, no roof (no orientation, TODO-192); contents on its floor
    APPLIANCE = "appliance"    # a box with a cup-like form on its top
    PANEL = "panel"            # a plate on a slim post, with a round dial on its top
    SEAT = "seat"              # a round seat on a stem
    MARKER = "marker"          # a slim post with a small square flag
    BARRIER = "barrier"        # a thin wall over the footprint


class MovableShape(str, Enum):
    """The forms of a movable object."""
    CRATE = "crate"            # a box with a lid line
    SKID = "skid"              # a low slatted platform


class Figure(str, Enum):
    """The figures of the agents."""
    PERSON = "person"                      # a body and a round head
    CUBE_HEAD_ROBOT = "cube_head_robot"    # a wheeled base, a column and a cube head
    LIFT_VEHICLE = "lift_vehicle"          # a body, a mast and two forks


class Presence(str, Enum):
    BACKGROUND = "background"
    ACTIVE = "active"


class FixedLook(Message):
    shape: ShapeKind
    height: float
    presence: Presence


class MovableLook(Message):
    shape: MovableShape
    height: float


class FigureLook(Message):
    figure: Figure
    height: float


DEFAULT_FIXED = FixedLook(shape=ShapeKind.BLOCK, height=60.0, presence=Presence.BACKGROUND)
DEFAULT_MOVABLE = MovableLook(shape=MovableShape.CRATE, height=20.0)


class Appearance(Message):
    """A domain's scene appearance: per object type its look; the agents' figures. Every field has a default."""
    fixed: dict[str, FixedLook] = {}
    movable: dict[str, MovableLook] = {}
    default_fixed: FixedLook = DEFAULT_FIXED
    default_movable: MovableLook = DEFAULT_MOVABLE
    human: FigureLook = FigureLook(figure=Figure.PERSON, height=150.0)
    robot: FigureLook = FigureLook(figure=Figure.CUBE_HEAD_ROBOT, height=120.0)
