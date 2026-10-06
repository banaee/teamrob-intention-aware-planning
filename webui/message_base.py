"""
webui/message_base.py

PURPOSE:
    The base class of every message of the web-ui (webui/messages.py) and of the scene appearance (webui/appearance.py),
    in a module of its own so that a message can carry the appearance (the catalogue does, T-viz 1a) without the two
    modules importing each other.
"""

from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    """Frozen, no field beyond the definition, no coercion between types."""
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)
